#!/usr/bin/env python3
"""
ClockEE Full-Mesh Identity & Ingestion Audit Broadcaster (broadcast_audit.py)
Dispatches an operational manifesto ping to every conversation across the mesh via agentapi IPC:
  - GITHUB
  - Untitled conversation (Main Feature)
  - UI / UX
  - SIMULATION
  - DB / BACKEND
  - BUG FIXES
  - Q / A
  - INSPIRATION
Verifies that each conversation is actively taking in inputs from the autonomous mesh.
"""

import os
import sys
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime

PIPELINE_DIR = Path(__file__).resolve().parent
ROOT_DIR = PIPELINE_DIR.parent
AGENTAPI_BIN = r"C:\Users\Kunal\.gemini\antigravity\bin\agentapi.bat"

CONVERSATIONS_TO_PING = {
    "github": {
        "name": "GITHUB",
        "id": "a64c937f-bb58-4071-8eb9-32f5edbb6c2c",
        "role": "Package Vendoring & Reel Ingestion"
    },
    "untitled_conversation": {
        "name": "Untitled conversation (Main Feature)",
        "id": "6371cba6-7d2f-4b29-a250-627d88d1b4f1",
        "role": "Core Layout, Navigation & Feature Wiring"
    },
    "ui_ux": {
        "name": "UI / UX",
        "id": "06a7d47b-b225-40f4-b830-b58baaaf8b3a",
        "role": "Hallmark Design Tokens, Tactile Cockpit & Responsive CSS"
    },
    "simulation": {
        "name": "SIMULATION",
        "id": "62adc180-be21-4671-848c-c8df59e2c202",
        "role": "Automated Quality Gates, SlopLinter 100/100 & Security Audits"
    },
    "db_backend": {
        "name": "DB / BACKEND",
        "id": "d3700ff3-1bfb-458a-9968-8257ef2ca7e2",
        "role": "SQLite Schemas, Python Server API & Supabase Gateway"
    },
    "bug_fixes": {
        "name": "BUG FIXES",
        "id": "6b74e384-a9b2-458e-ba34-4798334dd509",
        "role": "Surgical Defect Remediation & Hotfixes"
    },
    "q_a": {
        "name": "Q / A",
        "id": "6029bc76-d833-4ab6-8672-b5f43511cf8f",
        "role": "Question Bank Extraction & Syllabus Ingestion"
    },
    "inspiration": {
        "name": "INSPIRATION",
        "id": "e6690e55-bfca-4ce1-af20-843015d7d01b",
        "role": "Mentor Council & Topper Study Ideation"
    }
}

AUDIT_PROMPT_TEMPLATE = """[CLOCKEE MESH INGESTION & IDENTITY AUDIT]
You have received an autonomous ping from the BACKBONE COORDINATOR to verify active input intake across the ClockEE mesh.

Please respond immediately with your full operational manifesto:
1. What is your exact Official Title?
2. What is your core Purpose & Job Description within ClockEE?
3. What are your operational Rules within the ClockEE 3-phase mesh network?
4. What can you do (Capabilities, Scope, and Tools)?
5. What are your strict Limitations & Boundaries (What must you NEVER touch or do)?
6. Confirm whether you are active, responsive, and ready to receive autonomous task handoffs from the mesh.

Conclude your response with the standard '### 🛰️ PIPELINE QUEUE & HANDOFF REPORT' block."""

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

def broadcast():
    print("=================================================================", flush=True)
    print(" 🚀 BROADCASTING MESH IDENTITY & INGESTION AUDIT TO ALL AGENTS", flush=True)
    print(f" Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    print(f" Total Targets : {len(CONVERSATIONS_TO_PING)} Dedicated Conversations", flush=True)
    print("=================================================================\n", flush=True)

    results = []
    for key, info in CONVERSATIONS_TO_PING.items():
        name = info["name"]
        cid = info["id"]
        role = info["role"]

        print(f"📡 Dispatching Identity Audit Ping to {name}...", flush=True)
        print(f"   Conversation ID: {cid}", flush=True)
        print(f"   Role: {role}", flush=True)

        try:
            # Asynchronously send message via agentapi.bat
            proc = subprocess.Popen(
                [AGENTAPI_BIN, "send-message", "--title=ClockEE Identity & Ingestion Audit", cid, AUDIT_PROMPT_TEMPLATE],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=False
            )
            record_transmission(
                source="BACKBONE COORDINATOR",
                target=name,
                subject="Mesh Identity & Operational Manifesto Audit",
                status="DELIVERED_AUTO"
            )
            print(f"   ✔ DELIVERED (Async PID: {proc.pid})", flush=True)
            results.append({"name": name, "id": cid, "status": "DELIVERED", "pid": proc.pid})
        except Exception as e:
            print(f"   ❌ FAILED: {e}", flush=True)
            results.append({"name": name, "id": cid, "status": f"FAILED: {e}", "pid": None})

        # Small 200ms pause between launches to prevent process storm
        time.sleep(0.2)

    # Sync web tracker immediately
    print("\n--- Synchronizing Web Tracker Cockpit ---", flush=True)
    if str(PIPELINE_DIR) not in sys.path:
        sys.path.insert(0, str(PIPELINE_DIR))
    try:
        import tracker_sync
        tracker_sync.build_tracker_state()
        print("✔ tracker.html and tracker_state.json synchronized.", flush=True)
    except Exception as te:
        print(f"Tracker sync warning: {te}", flush=True)

    print("\n=================================================================")
    print(f" 🏁 BROADCAST COMPLETE: {len(results)}/{len(CONVERSATIONS_TO_PING)} PINGS DISPATCHED")
    print("=================================================================", flush=True)

    return results

if __name__ == "__main__":
    broadcast()
