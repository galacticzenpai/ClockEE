#!/usr/bin/env python3
"""
ClockEE Real-Time Mesh Event Watcher (mesh_watcher.py)
Monitors all conversation transcripts continuously.
Immediately triggers mesh_orchestrator.py when any conversation finishes prompting.
Zero 15-minute delays: instant reactive handoffs via agentapi IPC.
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime

PIPELINE_DIR = Path(__file__).resolve().parent
ROOT_DIR = PIPELINE_DIR.parent
BRAIN_DIR = Path(r"C:\Users\Kunal\.gemini\antigravity\brain")
LOG_FILE = PIPELINE_DIR / "mesh_watcher.log"

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

# Conversations to watch (excluding backbone coordinator to avoid self-trigger loops)
WATCHED_CONVERSATIONS = {
    "untitled_conversation": {
        "id": "6371cba6-7d2f-4b29-a250-627d88d1b4f1",
        "name": "Untitled conversation (Main Feature)"
    },
    "github": {
        "id": "a64c937f-bb58-4071-8eb9-32f5edbb6c2c",
        "name": "GITHUB"
    },
    "ui_ux": {
        "id": "06a7d47b-b225-40f4-b830-b58baaaf8b3a",
        "name": "UI / UX"
    },
    "simulation": {
        "id": "62adc180-be21-4671-848c-c8df59e2c202",
        "name": "SIMULATION"
    },
    "db_backend": {
        "id": "d3700ff3-1bfb-458a-9968-8257ef2ca7e2",
        "name": "DB / BACKEND"
    },
    "bug_fixes": {
        "id": "6b74e384-a9b2-458e-ba34-4798334dd509",
        "name": "BUG FIXES"
    },
    "q_a": {
        "id": "6029bc76-d833-4ab6-8672-b5f43511cf8f",
        "name": "Q / A"
    },
    "inspiration": {
        "id": "e6690e55-bfca-4ce1-af20-843015d7d01b",
        "name": "INSPIRATION"
    }
}

BACKBONE_ID = "a80111ec-0657-4748-9e85-d620e8a2a535"

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] {msg}"
    print(entry, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(entry + "\n")
    except Exception:
        pass

def get_last_step(transcript_path: Path):
    if not transcript_path.is_file():
        return None
    try:
        with open(transcript_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = [l.strip() for l in f if l.strip().startswith("{")]
        if not lines:
            return None
        return json.loads(lines[-1])
    except Exception:
        return None

def main():
    log("=== ClockEE Event-Driven Mesh Watcher Started ===")
    log("Watching 8 conversation transcripts for turn completion events...")

    # Initialize baseline step counters
    last_steps = {}
    for key, info in WATCHED_CONVERSATIONS.items():
        t_path = BRAIN_DIR / info["id"] / ".system_generated" / "logs" / "transcript.jsonl"
        step_data = get_last_step(t_path)
        if step_data:
            last_steps[key] = step_data.get("step_index", 0)
            log(f"  • {info['name']}: Initial baseline Step {last_steps[key]}")
        else:
            last_steps[key] = 0

    import mesh_orchestrator
    import tracker_sync
    import check_floor_prompts

    # Initial floor check and tracker sync
    try:
        check_floor_prompts.check_and_execute_floor_prompts()
    except Exception as e:
        log(f"Initial floor check & tracker sync: {e}")

    last_sync_time = time.time()

    while True:
        try:
            step_changed = False
            for key, info in WATCHED_CONVERSATIONS.items():
                t_path = BRAIN_DIR / info["id"] / ".system_generated" / "logs" / "transcript.jsonl"
                step_data = get_last_step(t_path)
                if not step_data:
                    continue

                curr_step = step_data.get("step_index", 0)
                curr_type = step_data.get("type", "")
                curr_status = step_data.get("status", "")

                # Detect any step advancement
                if curr_step > last_steps.get(key, 0):
                    last_steps[key] = curr_step
                    step_changed = True

                    # Trigger immediately after any conversation completes a prompt
                    if curr_type == "PLANNER_RESPONSE" and curr_status == "DONE":
                        log(f"⚡ [EVENT DETECTED] {info['name']} completed prompting (Step {curr_step})!")
                        log(f"  Running check_floor_prompts to evaluate handoffs and quality gates...")

                        # Execute floor prompt check and dispatch cycle immediately
                        try:
                            floor_res = check_floor_prompts.check_and_execute_floor_prompts()
                            log(f"  ✔ Floor audit finished: {floor_res.get('total_floor_prompts', 0)} floor prompt(s) audited.")
                        except Exception as floor_err:
                            log(f"  Warning executing floor check: {floor_err}")

            # Sync tracker state on step advancement or periodically every 4 seconds
            if step_changed or (time.time() - last_sync_time > 4.0):
                try:
                    tracker_sync.build_tracker_state()
                    last_sync_time = time.time()
                except Exception as sync_err:
                    log(f"Tracker state sync error: {sync_err}")

            time.sleep(2)
        except KeyboardInterrupt:
            log("Mesh Watcher stopped by user.")
            break
        except Exception as e:
            log(f"Warning in watcher loop: {e}")
            time.sleep(3)

if __name__ == "__main__":
    main()
