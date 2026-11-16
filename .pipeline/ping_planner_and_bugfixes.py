#!/usr/bin/env python3
"""
Targeted Audit Dispatcher for PLANNER and BUG FIXES (ping_planner_and_bugfixes.py)
Delivers the official mesh manifesto audit directly into:
  1. PLANNING & ROADMAP ARCHITECT (b411e7a0-c268-4614-b3d5-f2b2836f4500)
  2. BUG FIXES (6b74e384-a9b2-458e-ba34-4798334dd509)
"""

import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

PIPELINE_DIR = Path(__file__).resolve().parent
ROOT_DIR = PIPELINE_DIR.parent
AGENTAPI_BIN = r"C:\Users\Kunal\.gemini\antigravity\bin\agentapi.bat"

TARGETS = [
    {
        "key": "planning",
        "name": "PLANNING & ROADMAP ARCHITECT",
        "id": "b411e7a0-c268-4614-b3d5-f2b2836f4500",
        "role": "Sprint Planner, Roadmap Strategist & Prompt Engineer"
    },
    {
        "key": "bug_fixes",
        "name": "BUG FIXES",
        "id": "6b74e384-a9b2-458e-ba34-4798334dd509",
        "role": "Surgical Defect Remediation & Hotfixes"
    }
]

AUDIT_PROMPT = """[CLOCKEE MESH INGESTION & IDENTITY AUDIT - ACTION REQUIRED]
You have received an autonomous ping from the BACKBONE COORDINATOR to verify your input intake and operational boundaries.

Please respond immediately with your full operational manifesto answering each question:
1. What is your exact Official Title?
2. What is your core Purpose & Job Description within ClockEE?
3. What are your operational Rules within the ClockEE 3-phase mesh network?
4. What can you do (Capabilities, Scope, and Tools)?
5. What are your strict Limitations & Boundaries (What must you NEVER touch or do)?
6. Confirm whether you are active, responsive, and ready to receive autonomous task handoffs from the mesh.

Conclude your response with your standard '### 🛰️ PIPELINE QUEUE & HANDOFF REPORT' block."""

def get_transmissions():
    tx_file = PIPELINE_DIR / "transmissions.json"
    if tx_file.is_file():
        try:
            with open(tx_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []

def record_transmission(source, target, subject, status="DELIVERED_AUTO"):
    txs = get_transmissions()
    txs.insert(0, {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": source,
        "target": target,
        "subject": subject,
        "status": status
    })
    tx_file = PIPELINE_DIR / "transmissions.json"
    try:
        with open(tx_file, "w", encoding="utf-8") as f:
            json.dump(txs[:80], f, indent=2)
    except Exception as e:
        print(f"Error saving transmission: {e}")

def main():
    print("=================================================================", flush=True)
    print(" 🚀 TARGETED DISPATCH TO PLANNER & BUG FIXES VIA AGENTAPI", flush=True)
    print(f" Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print("=================================================================\n", flush=True)

    for target in TARGETS:
        name = target["name"]
        cid = target["id"]
        print(f"📡 Sending Audit Prompt to {name}...", flush=True)
        print(f"   Conversation ID: {cid}", flush=True)

        try:
            proc = subprocess.Popen(
                [AGENTAPI_BIN, "send-message", "--title=ClockEE Identity & Ingestion Audit", cid, AUDIT_PROMPT],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=False
            )
            record_transmission(
                source="BACKBONE COORDINATOR",
                target=name,
                subject="Targeted Identity & Operational Manifesto Audit",
                status="DELIVERED_AUTO"
            )
            print(f"   ✔ DELIVERED_AUTO (Async PID: {proc.pid})\n", flush=True)
        except Exception as e:
            print(f"   ❌ FAILED: {e}\n", flush=True)

        time.sleep(0.5)

    if str(PIPELINE_DIR) not in sys.path:
        sys.path.insert(0, str(PIPELINE_DIR))
    import tracker_sync
    tracker_sync.build_tracker_state()
    print("✔ tracker_state.json updated with live conversation progress engine.")

    print("\n=================================================================")
    print(" 🏁 TARGETED DISPATCH COMPLETE")
    print("=================================================================", flush=True)

if __name__ == "__main__":
    main()
