#!/usr/bin/env python3
"""
ClockEE 24/7 Continuous Mesh Bridge & Autonomous Floor IPC Dispatcher
Monitors all conversation transcripts in real time, extracts handoff prompts as soon as emitted,
dispatches them instantly via language_server.exe agentapi, and syncs the live tracker & Supabase cloud.
Designed to run continuously without stopping or crashing.
"""

import os
import sys
import time
import json
import hashlib
import traceback
import subprocess
from datetime import datetime
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parent
ROOT_DIR = PIPELINE_DIR.parent
BRAIN_DIR = Path(r"C:\Users\Kunal\.gemini\antigravity\brain")
LANG_SERVER_BIN = r"C:\Users\Kunal\AppData\Local\Programs\antigravity\resources\bin\language_server.exe"

DISPATCHED_LOG_FILE = PIPELINE_DIR / "dispatched_prompts.json"
DAILY_PLAN_FILE = PIPELINE_DIR / "daily_plan.json"
BACKLOG_FILE = PIPELINE_DIR / "github_backlog.json"

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

import tracker_sync

ALL_CONVERSATIONS = {
    "untitled_conversation": {
        "id": "6371cba6-7d2f-4b29-a250-627d88d1b4f1",
        "name": "Untitled conversation (Main Feature)",
        "aliases": ["main", "main feature", "untitled conversation", "untitled_conversation", "core"]
    },
    "github": {
        "id": "a64c937f-bb58-4071-8eb9-32f5edbb6c2c",
        "name": "GITHUB",
        "aliases": ["github", "git", "repo", "packages"]
    },
    "ui_ux": {
        "id": "06a7d47b-b225-40f4-b830-b58baaaf8b3a",
        "name": "UI / UX",
        "aliases": ["ui", "ux", "ui / ux", "ui_ux", "design", "styling"]
    },
    "simulation": {
        "id": "62adc180-be21-4671-848c-c8df59e2c202",
        "name": "SIMULATION",
        "aliases": ["simulation", "sim", "qa gate", "sloplint"]
    },
    "db_backend": {
        "id": "d3700ff3-1bfb-458a-9968-8257ef2ca7e2",
        "name": "DB / BACKEND",
        "aliases": ["db", "backend", "db / backend", "db_backend", "sqlite", "supabase", "database"]
    },
    "bug_fixes": {
        "id": "c05ee59e-9749-4bc3-8bea-57ea8b60874c",
        "name": "BUG FIXES",
        "aliases": ["bug fixes", "bug_fixes", "fixes", "patch", "hotfix"]
    },
    "q_a": {
        "id": "6029bc76-d833-4ab6-8672-b5f43511cf8f",
        "name": "Q / A",
        "aliases": ["q/a", "q_a", "question answer", "q & a", "questions"]
    },
    "inspiration": {
        "id": "e6690e55-bfca-4ce1-af20-843015d7d01b",
        "name": "INSPIRATION",
        "aliases": ["inspiration", "mentor", "topper", "ideas"]
    },
    "planning": {
        "id": "b411e7a0-c268-4614-b3d5-f2b2836f4500",
        "name": "PLANNING & ROADMAP ARCHITECT",
        "aliases": ["planning", "planner", "roadmap", "architect"]
    },
    "backbone": {
        "id": "a80111ec-0657-4748-9e85-d620e8a2a535",
        "name": "BACKBONE COORDINATOR",
        "aliases": ["backbone", "coordinator", "mesh coordinator"]
    }
}

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

def load_dispatched_hashes():
    if DISPATCHED_LOG_FILE.is_file():
        try:
            with open(DISPATCHED_LOG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return set(data.get("hashes", []))
        except Exception:
            pass
    return set()

def save_dispatched_hash(h_val):
    hashes = load_dispatched_hashes()
    hashes.add(h_val)
    try:
        with open(DISPATCHED_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump({"hashes": list(hashes), "last_updated": datetime.now().isoformat()}, f, indent=2)
    except Exception:
        pass

def resolve_target_conversation(target_raw):
    raw_lower = target_raw.lower().strip()
    for key, info in ALL_CONVERSATIONS.items():
        if raw_lower == key.lower() or raw_lower == info["name"].lower():
            return key, info
        for alias in info["aliases"]:
            if alias in raw_lower:
                return key, info
    return None, None

def scan_transcript_for_handoffs(convo_key, convo_info):
    cid = convo_info["id"]
    t_file = BRAIN_DIR / cid / ".system_generated" / "logs" / "transcript.jsonl"
    if not t_file.is_file():
        return []

    try:
        with open(t_file, "r", encoding="utf-8", errors="ignore") as f:
            lines = [l.strip() for l in f if l.strip().startswith("{")]
    except Exception:
        return []

    if not lines:
        return []

    # Check last 6 steps
    handoffs = []
    for l in lines[-6:]:
        try:
            obj = json.loads(l)
        except Exception:
            continue

        st_type = obj.get("type")
        content = obj.get("content") or ""
        step_idx = obj.get("step_index", 0)

        if not content:
            continue

        # Format A: "--- PROMPT FOR [Target] ---"
        if "--- PROMPT FOR " in content:
            parts = content.split("--- PROMPT FOR ")
            for part in parts[1:]:
                lines_part = part.splitlines()
                if not lines_part:
                    continue
                first_line = lines_part[0].strip()
                target_str = first_line.rstrip("-").strip()

                tgt_key, tgt_info = resolve_target_conversation(target_str)
                if not tgt_info or tgt_key == convo_key:
                    continue

                body_lines = lines_part[1:]
                clean_lines = []
                for bl in body_lines:
                    if "--- PROMPT FOR " in bl or bl.strip().startswith("```handoff") or bl.strip() == "```":
                        if bl.strip() == "```":
                            continue
                        if "--- PROMPT FOR " in bl:
                            break
                    clean_lines.append(bl)

                instruction = "\n".join(clean_lines).strip()
                if not instruction or len(instruction) < 15:
                    continue

                h_payload = f"{convo_key}->{tgt_key}:{instruction[:120]}:{step_idx}"
                h_digest = hashlib.sha256(h_payload.encode("utf-8")).hexdigest()

                handoffs.append({
                    "source_key": convo_key,
                    "source_name": convo_info["name"],
                    "target_key": tgt_key,
                    "target_name": tgt_info["name"],
                    "target_id": tgt_info["id"],
                    "instruction": instruction,
                    "step_index": step_idx,
                    "hash": h_digest
                })

        # Format B: "Next Queued Agent: [Target]" and "QUEUE DISPATCH REQUIRED"
        elif "Next Queued Agent" in content or "QUEUE DISPATCH REQUIRED" in content:
            tgt_str = ""
            for line in content.splitlines():
                line_clean = line.replace("*", "").replace(">", "").strip()
                if "Next Queued Agent:" in line_clean:
                    tgt_str = line_clean.split("Next Queued Agent:", 1)[1].strip()
                    break

            if tgt_str:
                tgt_key, tgt_info = resolve_target_conversation(tgt_str)
                if tgt_info and tgt_key != convo_key:
                    # Detect target task (e.g. TASK-03)
                    import re
                    task_id = ""
                    for line in content.splitlines():
                        m = re.search(r"TASK-\d+", line)
                        if m:
                            task_id = m.group(0)
                            break

                    instruction = ""
                    if task_id and DAILY_PLAN_FILE.is_file():
                        try:
                            with open(DAILY_PLAN_FILE, "r", encoding="utf-8") as dpf:
                                dp = json.load(dpf)
                            for t in dp.get("tasks", []):
                                if t.get("id") == task_id:
                                    instruction = (
                                        f"You are {tgt_info['name']}.\n\n"
                                        f"--- TASK ASSIGNMENT: {task_id} ---\n"
                                        f"Plan ID: {dp.get('plan_id')}\n"
                                        f"Task Description: {t.get('task')}\n\n"
                                        f"Please execute and complete {task_id}, mark as COMPLETED in .pipeline/daily_plan.json, "
                                        f"and output your standard PIPELINE QUEUE & HANDOFF REPORT."
                                    )
                                    break
                        except Exception:
                            pass

                    if not instruction:
                        instruction = (
                            f"You are {tgt_info['name']}.\n"
                            f"Handoff dispatch received from {convo_info['name']}:\n\n"
                            f"{content[-600:]}"
                        )

                    h_payload = f"{convo_key}->{tgt_key}:{task_id or 'queued'}:{step_idx}"
                    h_digest = hashlib.sha256(h_payload.encode("utf-8")).hexdigest()

                    handoffs.append({
                        "source_key": convo_key,
                        "source_name": convo_info["name"],
                        "target_key": tgt_key,
                        "target_name": tgt_info["name"],
                        "target_id": tgt_info["id"],
                        "instruction": instruction,
                        "step_index": step_idx,
                        "hash": h_digest
                    })

    return handoffs

def dispatch_handoff_prompt(handoff):
    tgt_id = handoff["target_id"]
    tgt_name = handoff["target_name"]
    src_name = handoff["source_name"]
    instruction = handoff["instruction"]
    title = f"ClockEE Mesh Handoff from {src_name}"

    log(f"🚀 [AUTO-DISPATCH] Transferring prompt: {src_name} ➔ {tgt_name} (Step #{handoff['step_index']})")
    try:
        res = subprocess.run(
            [LANG_SERVER_BIN, "agentapi", "send-message", f"--title={title}", tgt_id, instruction],
            capture_output=True,
            text=True,
            timeout=10
        )
        if res.returncode == 0:
            log(f"✔ Successfully delivered to {tgt_name} ({tgt_id[:8]}...)")
            save_dispatched_hash(handoff["hash"])
            tracker_sync.record_transmission(
                src_name,
                tgt_name,
                f"Auto-Handoff: {instruction[:50]}...",
                "DELIVERED_AUTO"
            )
            return True
        else:
            log(f"❌ Failed delivery to {tgt_name}: {res.stderr}")
            return False
    except Exception as e:
        log(f"❌ Error dispatching to {tgt_name}: {e}")
        return False

def push_to_supabase_cloud():
    try:
        from backend.db import get_supabase_client, is_supabase_configured
        if not is_supabase_configured():
            return
        client = get_supabase_client()
        if not client:
            return
        
        t_file = PIPELINE_DIR / "tracker_state.json"
        if t_file.is_file():
            with open(t_file, "r", encoding="utf-8") as f:
                state_data = json.load(f)
            client.table("mesh_tracker_state").upsert({
                "id": "active",
                "state": state_data
            }).execute()
    except Exception:
        pass

def run_bridge_loop():
    log("=================================================================")
    log(" ⚡ CLOCKEE 24/7 CONTINUOUS MESH BRIDGE & IPC DISPATCHER ACTIVE")
    log("=================================================================")
    dispatched_hashes = load_dispatched_hashes()
    log(f"  Initialized deduplication cache with {len(dispatched_hashes)} previous dispatches.")

    cycle = 0
    while True:
        cycle += 1
        try:
            # 1. Scan transcripts across all conversations
            for key, info in ALL_CONVERSATIONS.items():
                if key == "backbone":
                    continue
                try:
                    handoffs = scan_transcript_for_handoffs(key, info)
                    for h in handoffs:
                        if h["hash"] not in dispatched_hashes:
                            dispatched_hashes.add(h["hash"])
                            dispatch_handoff_prompt(h)
                except Exception as ce:
                    pass

            # 2. Build tracker state
            try:
                tracker_sync.build_tracker_state()
            except Exception:
                pass

            # 3. Every 5 cycles, push live state to Supabase cloud
            if cycle % 5 == 0:
                push_to_supabase_cloud()

        except Exception as e:
            log(f"Bridge loop warning: {e}")

        time.sleep(1.5)

if __name__ == "__main__":
    run_bridge_loop()
