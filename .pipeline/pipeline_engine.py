#!/usr/bin/env python3
"""
ClockEE Autonomous Pipeline Engine
Monitors .pipeline/queue.json, executes automated validation runs,
and coordinates downstream tasks across project conversations.
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
PIPELINE_DIR = ROOT_DIR / ".pipeline"
QUEUE_FILE = PIPELINE_DIR / "queue.json"
HISTORY_FILE = PIPELINE_DIR / "history.json"

def load_queue():
    if not QUEUE_FILE.is_file():
        return None
    try:
        with open(QUEUE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[Pipeline Engine Error] Failed to read queue: {e}")
        return None

def save_queue(data):
    try:
        with open(QUEUE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"[Pipeline Engine Error] Failed to write queue: {e}")

def append_history(batch_record):
    history = []
    if HISTORY_FILE.is_file():
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []
    history.append(batch_record)
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"[Pipeline Engine Error] Failed to write history: {e}")

def run_automated_gate(command, name):
    print(f"\n[Quality Gate] Running {name}: {command}")
    try:
        res = subprocess.run(command, shell=True, cwd=str(ROOT_DIR), capture_output=True, text=True, timeout=60)
        print(f"[{name}] Exit Code: {res.returncode}")
        return {
            "success": res.returncode == 0,
            "stdout": res.stdout[-800:] if res.stdout else "",
            "stderr": res.stderr[-500:] if res.stderr else ""
        }
    except Exception as err:
        return {"success": False, "error": str(err)}

def process_pipeline():
    print("=================================================================")
    print(" ClockEE Autonomous Pipeline Engine - Run Check")
    print(f" Timestamp: {datetime.now().isoformat()}")
    print("=================================================================")

    queue = load_queue()
    if not queue or "current_batch" not in queue:
        print("[Pipeline Engine] No active batch found in queue.")
        return

    batch = queue["current_batch"]
    batch_id = batch.get("batch_id", "batch_unknown")
    status = batch.get("status", "QUEUED")
    print(f"[Batch] ID: {batch_id} | Status: {status} | Package: {batch.get('package')}")

    tasks = batch.get("tasks", {})
    pending_count = sum(1 for t in tasks.values() if t.get("status") == "PENDING")
    print(f"[Tasks] Total: {len(tasks)} | Pending: {pending_count}")

    # Check for Simulation automated gate
    if "simulation" in tasks and tasks["simulation"].get("status") == "PENDING":
        print("\n--- Executing Automated Simulation Gates ---")
        slop_check = run_automated_gate("python integrations/hallmark_design/sloplint.py index.html", "Hallmark Slop Linter")
        audit_check = run_automated_gate("python integrations/cloudflare_security_audit/audit_runner.py", "Cloudflare Security Audit")

        tasks["simulation"]["status"] = "GATES_EVALUATED"
        tasks["simulation"]["last_run"] = datetime.now().isoformat()
        tasks["simulation"]["gate_results"] = {
            "sloplint": slop_check["success"],
            "security_audit": audit_check["success"]
        }

    save_queue(queue)
    print("\n[Pipeline Engine] Queue updated and synchronized.")
    return queue

if __name__ == "__main__":
    process_pipeline()
