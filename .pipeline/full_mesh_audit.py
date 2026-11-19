#!/usr/bin/env python3
"""
Comprehensive Mesh Audit Script
Checks every conversation's transcript, extracts all emitted prompts,
checks queue.json tasks, and verifies whether all tasks are completed.
"""

import json
import re
from pathlib import Path

brain = Path(r"C:\Users\Kunal\.gemini\antigravity\brain")
convos = {
    "untitled_conversation": {"id": "6371cba6-7d2f-4b29-a250-627d88d1b4f1", "name": "Untitled conversation (Main Feature)"},
    "github": {"id": "a64c937f-bb58-4071-8eb9-32f5edbb6c2c", "name": "GITHUB"},
    "ui_ux": {"id": "06a7d47b-b225-40f4-b830-b58baaaf8b3a", "name": "UI / UX"},
    "simulation": {"id": "62adc180-be21-4671-848c-c8df59e2c202", "name": "SIMULATION"},
    "db_backend": {"id": "d3700ff3-1bfb-458a-9968-8257ef2ca7e2", "name": "DB / BACKEND"},
    "bug_fixes": {"id": "6b74e384-a9b2-458e-ba34-4798334dd509", "name": "BUG FIXES"},
    "q_a": {"id": "6029bc76-d833-4ab6-8672-b5f43511cf8f", "name": "Q / A"},
    "inspiration": {"id": "e6690e55-bfca-4ce1-af20-843015d7d01b", "name": "INSPIRATION"},
    "backbone": {"id": "a80111ec-0657-4748-9e85-d620e8a2a535", "name": "BACKBONE COORDINATOR"}
}

def audit_all():
    print("=" * 65)
    print(" 🔍 COMPREHENSIVE CLOCKEE MESH AUDIT & PROMPT RECONCILIATION")
    print("=" * 65)

    # 1. Check all transcripts for emitted handoff prompts
    handoffs = []
    statuses = {}
    for key, info in convos.items():
        t_file = brain / info["id"] / ".system_generated" / "logs" / "transcript.jsonl"
        if not t_file.is_file():
            statuses[key] = {"last_step": 0, "last_content": "No transcript", "type": "NONE"}
            continue
        try:
            with open(t_file, "r", encoding="utf-8", errors="ignore") as f:
                lines = [l.strip() for l in f if l.strip().startswith("{")]
            if lines:
                last_obj = json.loads(lines[-1])
                statuses[key] = {
                    "last_step": last_obj.get("step_index"),
                    "last_type": last_obj.get("type"),
                    "last_status": last_obj.get("status"),
                    "last_content": str(last_obj.get("content", ""))[:120].replace("\n", " ")
                }
            for l in lines:
                try:
                    obj = json.loads(l)
                    cnt = str(obj.get("content", ""))
                    if "PROMPT FOR" in cnt or "Prompt for" in cnt:
                        matches = re.findall(r"(?:PROMPT FOR|Prompt for)\s+([A-Za-z /_() -]+)", cnt, re.I)
                        for m in matches:
                            target = m.strip("-*:# ")
                            handoffs.append({
                                "source": info["name"],
                                "target": target,
                                "step": obj.get("step_index"),
                                "preview": cnt[:80].replace("\n", " ")
                            })
                except:
                    pass
        except Exception as e:
            statuses[key] = {"error": str(e)}

    print("\n--- [1] Live Status of All 9 Conversations ---")
    for key, s in statuses.items():
        name = convos[key]["name"]
        st = s.get("last_step", "?")
        tp = s.get("last_type", "?")
        stat = s.get("last_status", "?")
        cnt = s.get("last_content", "")[:50]
        print(f"  • {name:<35} | Step: {str(st):<6} | {tp:<16} ({stat}) | {cnt}")

    # 2. Check Queue and History
    q_file = Path(r"d:\Desktop\ClockEE\.pipeline\queue.json")
    queue_tasks = {}
    current_batch = None
    if q_file.is_file():
        with open(q_file, "r", encoding="utf-8") as f:
            q = json.load(f)
            current_batch = q.get("current_batch", {})
            queue_tasks = current_batch.get("tasks", {})

    print(f"\n--- [2] Current Batch: {current_batch.get('batch_id')} ({current_batch.get('status')}) ---")
    for t_key, t_val in queue_tasks.items():
        print(f"  • Task: {t_key:<24} | Status: {t_val.get('status')} | Target: {t_val.get('target_name')}")

    # 3. Check Staged Prompt
    staged_file = Path(r"d:\Desktop\ClockEE\.pipeline\staged_prompt.txt")
    staged_content = ""
    if staged_file.is_file():
        with open(staged_file, "r", encoding="utf-8") as f:
            staged_content = f.read()
    print(f"\n--- [3] Mailbox Staged Prompt ({len(staged_content)} chars) ---")
    print(f"  Snippet: {staged_content[:150].replace(chr(10), ' ')}...")

    # 4. Check Backlog
    b_file = Path(r"d:\Desktop\ClockEE\.pipeline\github_backlog.json")
    if b_file.is_file():
        with open(b_file, "r", encoding="utf-8") as f:
            b = json.load(f)
            print(f"\n--- [4] GitHub Reel Backlog Status ---")
            print(f"  Total Backlog Remaining : {len(b.get('backlog', []))}")
            print(f"  Active Reel Target      : {b.get('active_reel')}")
            print(f"  Completed Reels         : {b.get('completed_reels')}")

    # 5. Check Transmissions
    tx_file = Path(r"d:\Desktop\ClockEE\.pipeline\transmissions.json")
    if tx_file.is_file():
        with open(tx_file, "r", encoding="utf-8") as f:
            txs = json.load(f)
            print(f"\n--- [5] Transmission History ({len(txs)} records) ---")
            for t in txs[:5]:
                print(f"  {t.get('timestamp')} | {t.get('source')} -> {t.get('target')} | {t.get('status')}")

    print("\n" + "=" * 65)

if __name__ == "__main__":
    audit_all()
