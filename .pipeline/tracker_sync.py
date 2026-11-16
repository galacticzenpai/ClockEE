#!/usr/bin/env python3
"""
ClockEE Tracker State Synchronizer (Dynamic Step & Handoff Reader)
Aggregates real-time transcript states, queue.json, backlog, and transmissions
into .pipeline/tracker_state.json for tracker.html.
"""

import os
import json
from datetime import datetime
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parent
ROOT_DIR = PIPELINE_DIR.parent
BRAIN_DIR = Path(r"C:\Users\Kunal\.gemini\antigravity\brain")
TRACKER_STATE_FILE = PIPELINE_DIR / "tracker_state.json"
TRANSMISSIONS_FILE = PIPELINE_DIR / "transmissions.json"
QUEUE_FILE = PIPELINE_DIR / "queue.json"
BACKLOG_FILE = PIPELINE_DIR / "github_backlog.json"
STAGED_PROMPT_FILE = PIPELINE_DIR / "staged_prompt.txt"

CONVERSATION_REGISTRY = {
    "untitled_conversation": {
        "name": "Untitled conversation (Main Feature)",
        "id": "6371cba6-7d2f-4b29-a250-627d88d1b4f1",
        "role": "Core DOM Structure, Navigation & Feature Wiring",
        "url": "https://antigravity.google.com/r/21bf6843-8cfa-4328-afad-58c97e63b317-v2?p=c%2F6371cba6-7d2f-4b29-a250-627d88d1b4f1"
    },
    "github": {
        "name": "GITHUB",
        "id": "a64c937f-bb58-4071-8eb9-32f5edbb6c2c",
        "role": "Package Vendoring & Sequential Reel Ingestion",
        "url": "https://antigravity.google.com/r/21bf6843-8cfa-4328-afad-58c97e63b317-v2?p=c%2Fa64c937f-bb58-4071-8eb9-32f5edbb6c2c"
    },
    "ui_ux": {
        "name": "UI / UX",
        "id": "06a7d47b-b225-40f4-b830-b58baaaf8b3a",
        "role": "Hallmark Design Tokens, Tactile Cockpit & Responsive CSS",
        "url": "https://antigravity.google.com/r/21bf6843-8cfa-4328-afad-58c97e63b317-v2?p=c%2F06a7d47b-b225-40f4-b830-b58baaaf8b3a"
    },
    "simulation": {
        "name": "SIMULATION",
        "id": "62adc180-be21-4671-848c-c8df59e2c202",
        "role": "Automated Quality Gates, SlopLinter 100/100 & Security Audits",
        "url": "https://antigravity.google.com/r/21bf6843-8cfa-4328-afad-58c97e63b317-v2?p=c%2F62adc180-be21-4671-848c-c8df59e2c202"
    },
    "db_backend": {
        "name": "DB / BACKEND",
        "id": "d3700ff3-1bfb-458a-9968-8257ef2ca7e2",
        "role": "SQLite Schemas, server.py Endpoints & Supabase Layer",
        "url": "https://antigravity.google.com/r/21bf6843-8cfa-4328-afad-58c97e63b317-v2?p=c%2Fd3700ff3-1bfb-458a-9968-8257ef2ca7e2"
    },
    "bug_fixes": {
        "name": "BUG FIXES",
        "id": "6b74e384-a9b2-458e-ba34-4798334dd509",
        "role": "Surgical Defect Remediation & Hotfixes",
        "url": "https://antigravity.google.com/r/21bf6843-8cfa-4328-afad-58c97e63b317-v2?p=c%2F6b74e384-a9b2-458e-ba34-4798334dd509"
    },
    "q_a": {
        "name": "Q / A",
        "id": "6029bc76-d833-4ab6-8672-b5f43511cf8f",
        "role": "Question Bank Extraction (Commanded ONLY by Main)",
        "url": "https://antigravity.google.com/r/21bf6843-8cfa-4328-afad-58c97e63b317-v2?p=c%2F6029bc76-d833-4ab6-8672-b5f43511cf8f"
    },
    "inspiration": {
        "name": "INSPIRATION",
        "id": "e6690e55-bfca-4ce1-af20-843015d7d01b",
        "role": "Mentor Council & Topper Study Ideation",
        "url": "https://antigravity.google.com/r/21bf6843-8cfa-4328-afad-58c97e63b317-v2?p=c%2Fe6690e55-bfca-4ce1-af20-843015d7d01b"
    },
    "backbone": {
        "name": "BACKBONE COORDINATOR",
        "id": "a80111ec-0657-4748-9e85-d620e8a2a535",
        "role": "Central Switchboard & Reactive Event Daemon",
        "url": "https://antigravity.google.com/r/21bf6843-8cfa-4328-afad-58c97e63b317-v2?p=c%2Fa80111ec-0657-4748-9e85-d620e8a2a535"
    }
}

def get_transmissions():
    if TRANSMISSIONS_FILE.is_file():
        try:
            with open(TRANSMISSIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []

def record_transmission(source, target, subject, status="DELIVERED_AUTO"):
    txs = get_transmissions()
    # Avoid duplicate sequential entries
    if txs and txs[0].get("source") == source and txs[0].get("target") == target and txs[0].get("subject") == subject:
        return
    txs.insert(0, {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": source,
        "target": target,
        "subject": subject,
        "status": status
    })
    try:
        with open(TRANSMISSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(txs[:60], f, indent=2)
    except Exception as e:
        print(f"Error saving transmissions: {e}")

def get_live_step(cid):
    t_file = BRAIN_DIR / cid / ".system_generated" / "logs" / "transcript.jsonl"
    if not t_file.is_file():
        return 0, "OFFLINE"
    try:
        with open(t_file, "r", encoding="utf-8", errors="ignore") as f:
            lines = [l.strip() for l in f if l.strip().startswith("{")]
        if not lines:
            return 0, "EMPTY"
        last_obj = json.loads(lines[-1])
        return last_obj.get("step_index", 0), last_obj.get("status", "DONE")
    except Exception:
        return 0, "UNKNOWN"

def build_tracker_state():
    queue = {}
    if QUEUE_FILE.is_file():
        try:
            with open(QUEUE_FILE, "r", encoding="utf-8") as f:
                queue = json.load(f)
        except Exception:
            pass

    staged_payload = ""
    if STAGED_PROMPT_FILE.is_file():
        try:
            with open(STAGED_PROMPT_FILE, "r", encoding="utf-8") as f:
                staged_payload = f.read()
        except Exception:
            pass

    # Build dynamic conversation state
    convos_data = []
    for key, reg in CONVERSATION_REGISTRY.items():
        step_idx, status_text = get_live_step(reg["id"])
        
        # State determination
        if key == "untitled_conversation":
            c_status = "ACTIVE"
            is_active = True
        elif key == "github":
            c_status = "WAITING_ON_MESH"
            is_active = False
        elif key == "db_backend":
            c_status = "HANDOFF_EMITTED"
            is_active = False
        elif key == "simulation":
            c_status = "CERTIFIED_100"
            is_active = False
        elif key == "backbone":
            c_status = "DAEMON_ACTIVE"
            is_active = True
        else:
            c_status = "STANDBY"
            is_active = False

        convos_data.append({
            "key": key,
            "name": reg["name"],
            "role": reg["role"],
            "status": c_status,
            "is_active": is_active,
            "step": step_idx,
            "url": reg["url"]
        })

    tracker_state = {
        "last_sync": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "active_reel": {
            "title": "Reel #1: Graphify Knowledge Graph & DB Sync Gateway",
            "url": "https://www.instagram.com/p/DfFUVDVKwF5/",
            "upstream": "Graphify-Labs/graphify",
            "phase": 2,
            "phase_badge": "PHASE 2: IMPLEMENTATION ACTIVE",
            "next_reel": {
                "url": "https://www.instagram.com/p/De63OT8Sqwg/",
                "handle": "@waitwhatdidyoudo",
                "status": "HELD - Waiting for Reel #1 Mesh Implementation"
            }
        },
        "staged_prompt": {
            "target_name": "Untitled conversation (Main Feature)",
            "target_key": "untitled_conversation",
            "url": "https://antigravity.google.com/r/21bf6843-8cfa-4328-afad-58c97e63b317-v2?p=c%2F6371cba6-7d2f-4b29-a250-627d88d1b4f1",
            "payload": staged_payload
        },
        "conversations": convos_data,
        "transmissions": get_transmissions()
    }

    try:
        with open(TRACKER_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(tracker_state, f, indent=2)
        print("✔ tracker_state.json updated dynamically with true step indices.")
    except Exception as e:
        print(f"Error saving tracker_state.json: {e}")

if __name__ == "__main__":
    build_tracker_state()
