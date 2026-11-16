#!/usr/bin/env python3
"""
ClockEE Floor Prompt Checker & Real-Time Dispatcher (check_floor_prompts.py)
Scans all 9 conversation transcripts for handoff prompts on the floor.
Validates mesh gating rules (Reel Lifecycle, Strict Q/A, Double-Simulation).
Automatically triggers mesh_orchestrator to dispatch any pending prompt via agentapi IPC.
Can be executed directly or called after any conversation turn.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

PIPELINE_DIR = Path(__file__).resolve().parent
ROOT_DIR = PIPELINE_DIR.parent
BRAIN_DIR = Path(r"C:\Users\Kunal\.gemini\antigravity\brain")

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(PIPELINE_DIR) not in sys.path:
    sys.path.insert(0, str(PIPELINE_DIR))

import mesh_orchestrator as mo
import tracker_sync

def check_and_execute_floor_prompts():
    print("=================================================================", flush=True)
    print(" 📡 CLOCKEE FLOOR PROMPT AUDIT & REAL-TIME DISPATCH RUNNER", flush=True)
    print(f" Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print("=================================================================\n", flush=True)

    transmissions = tracker_sync.get_transmissions()
    recent_tx_keys = {
        (t.get("source"), t.get("target"), t.get("subject", "")[:40])
        for t in transmissions[:15]
    }

    queue = mo.load_queue()
    current_batch = queue.get("current_batch", {})
    tasks = current_batch.get("tasks", {})

    print("--- [Step 1] Inspecting Floor for Newly Emitted Handoff Prompts ---", flush=True)
    floor_prompts = []

    for key, info in mo.CONVERSATIONS.items():
        if key == "backbone":
            continue

        steps = mo.get_transcript_tail(info["id"], n=4)
        if not steps:
            continue

        discovered = mo.discover_handoff_prompts(key, steps)
        for d in discovered:
            src = info["name"]
            tgt_name = d["target_name"]
            tgt_key = d["target_key"]
            instr = d["instruction"]

            # Check if this prompt was already dispatched
            subject_prefix = f"Phase Hand-off: {instr[:30]}..."
            is_dispatched = (
                tasks.get(tgt_key, {}).get("status") == "DISPATCHED_TO_CONVERSATION"
                and tasks.get(tgt_key, {}).get("instruction") == instr
            )

            # Determine live status
            if is_dispatched:
                p_status = "DISPATCHED_AND_RUNNING"
            else:
                p_status = "PENDING_DISPATCH_ON_FLOOR"

            floor_prompts.append({
                "source_key": key,
                "source_name": src,
                "target_key": tgt_key,
                "target_name": tgt_name,
                "instruction": instr,
                "status": p_status
            })

            icon = "⚡" if p_status == "PENDING_DISPATCH_ON_FLOOR" else "✔"
            print(f"  {icon} [{p_status:<26}] {src} ➔ {tgt_name}", flush=True)
            print(f"     Snippet: {instr.replace(chr(10), ' ')[:75]}...", flush=True)

    if not floor_prompts:
        print("  ℹ No handoff prompts detected in recent conversation transcripts.", flush=True)

    # Check for actionable floor prompts
    pending_prompts = [p for p in floor_prompts if p["status"] == "PENDING_DISPATCH_ON_FLOOR"]

    print(f"\n--- [Step 2] Floor Evaluation: {len(pending_prompts)} Pending Prompts ---", flush=True)
    if pending_prompts:
        print(f"  🚀 Detected {len(pending_prompts)} actionable prompt(s) on the floor!")
        print("  Triggering mesh_orchestrator.run_mesh_process() to dispatch via agentapi IPC...")
        result = mo.run_mesh_process()
        staged = result.get("staged_task")
        if staged:
            print(f"  ✔ Successfully staged/dispatched to {staged['name']}.", flush=True)
    else:
        print("  ✔ All discovered floor prompts are already accounted for and dispatched to target sessions.", flush=True)

    # Sync web tracker
    print("\n--- [Step 3] Synchronizing Web Tracker Cockpit ---", flush=True)
    tracker_sync.build_tracker_state()
    print("  ✔ tracker.html and tracker_state.json synchronized.\n", flush=True)

    print("=================================================================")
    print(" 🏁 FLOOR PROMPT CHECK COMPLETE")
    print("=================================================================", flush=True)

    return {
        "total_floor_prompts": len(floor_prompts),
        "pending_prompts": len(pending_prompts),
        "prompts": floor_prompts
    }

if __name__ == "__main__":
    check_and_execute_floor_prompts()
