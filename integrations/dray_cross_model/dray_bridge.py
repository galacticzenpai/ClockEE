#!/usr/bin/env python3
"""
ClockEE Package: Dray Cross-Model Bridge (dray_bridge.py)
Adapted from Dray (drayhq.com / monorepo-labs/dray).

Captures active agent session state, serializes working context and constraints,
and outputs standardized /link handoff payloads so another model (ChatGPT, Gemini,
Claude, DeepSeek) can finish complex multi-step tasks without context loss.
"""

import os
import sys
import json
import time
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
BRIDGE_DIR = Path(__file__).resolve().parent
SNAPSHOT_FILE = BRIDGE_DIR / "active_session_snapshot.json"
LINK_PAYLOAD_FILE = BRIDGE_DIR / "dray_link_payload.md"

class DrayBridge:
    def __init__(self, workspace: Path = ROOT_DIR):
        self.workspace = workspace

    def capture(self, task_name: str, current_step: int, total_steps: int,
                completed_work: list, remaining_work: list,
                protected_files: list = None, touched_files: list = None):
        """Captures in-flight task state before rate limit or session reset."""
        snapshot = {
            "version": "1.0.0",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "generator": "Dray Cross-Model Bridge (drayhq.com)",
            "task": {
                "name": task_name,
                "current_step": current_step,
                "total_steps": total_steps,
                "progress_percent": round((current_step / max(1, total_steps)) * 100, 1),
                "completed": completed_work or [],
                "remaining": remaining_work or []
            },
            "boundaries": {
                "protected_files_do_not_touch": protected_files or ["cbt_master_bank.js", "backend/db.py"],
                "active_modified_files": touched_files or []
            }
        }
        with open(SNAPSHOT_FILE, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2)
        return snapshot

    def generate_link_payload(self) -> str:
        """Generates the standardized /link prompt for the receiving LLM."""
        if not SNAPSHOT_FILE.exists():
            return "No active session snapshot found. Run `capture` first."

        with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:
            snap = json.load(f)

        t = snap["task"]
        b = snap["boundaries"]

        payload = f"""# 🔗 DRAY CROSS-MODEL SESSION LINK (/link)
**Session Transferred at:** {snap['timestamp']}
**Task:** {t['name']} (Progress: {t['progress_percent']}% - Step {t['current_step']}/{t['total_steps']})

## 🎯 Finished Milestones:
{chr(10).join(f"- [x] {c}" for c in t['completed'])}

## ⏳ Next Step (Immediate Action Required):
**Current Action:** {t['remaining'][0] if t['remaining'] else 'Task completed.'}
{chr(10).join(f"- [ ] {r}" for r in t['remaining'][1:])}

## ⛔ STRICT BOUNDARIES & GUARDRAILS (DO NOT TOUCH):
{chr(10).join(f"- ⚠️ `{pf}`" for pf in b['protected_files_do_not_touch'])}

## 📁 Active Working Files:
{chr(10).join(f"- `{af}`" for af in b['active_modified_files'])}

---
*Instructions for Receiving Model: Read the active working files and execute the Immediate Action step cleanly without touching protected files.*
"""
        with open(LINK_PAYLOAD_FILE, "w", encoding="utf-8") as f:
            f.write(payload)
        return payload

    def verify_status(self):
        """Verifies active link file existence and schema integrity."""
        if not SNAPSHOT_FILE.exists():
            return False, "No snapshot exists."
        try:
            with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return True, f"Active session '{data['task']['name']}' at {data['task']['progress_percent']}% completion."
        except Exception as e:
            return False, str(e)

if __name__ == "__main__":
    bridge = DrayBridge()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "demo"

    if cmd == "demo":
        # Run a verified capture and link generation
        bridge.capture(
            task_name="CBT Webhook & Timer Resiliency",
            current_step=2,
            total_steps=4,
            completed_work=["Configured webhook listener in server.py", "Added retry logic for timer sync"],
            remaining_work=["Wire frontend storage event listener in cbt_exam.html", "Run regression simulation"],
            protected_files=["cbt_master_bank.js", "backend/db.py", "payment_routes.py"],
            touched_files=["cbt_exam.html", "clockee_core.js"]
        )
        payload = bridge.generate_link_payload()
        print("=" * 68)
        print(" DRAY: CROSS-MODEL CONTEXT HANDOFF BRIDGE (/link)")
        print("=" * 68)
        print(payload)
        print("=" * 68)
        print(f"✅ Active Snapshot Saved : {SNAPSHOT_FILE}")
        print(f"✅ Handoff Payload Saved : {LINK_PAYLOAD_FILE}")
        print("=" * 68)

    elif cmd == "link":
        print(bridge.generate_link_payload())

    elif cmd == "verify":
        ok, msg = bridge.verify_status()
        print(f"Status: {'OK' if ok else 'FAIL'} - {msg}")
