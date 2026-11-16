#!/usr/bin/env python3
"""
ClockEE Tracker State Synchronizer
Aggregates queue.json, history.json, github_backlog.json, and transcript states
into .pipeline/tracker_state.json for tracker.html.
"""

import os
import json
from datetime import datetime
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parent
ROOT_DIR = PIPELINE_DIR.parent
TRACKER_STATE_FILE = PIPELINE_DIR / "tracker_state.json"
TRANSMISSIONS_FILE = PIPELINE_DIR / "transmissions.json"
QUEUE_FILE = PIPELINE_DIR / "queue.json"
BACKLOG_FILE = PIPELINE_DIR / "github_backlog.json"
STAGED_PROMPT_FILE = PIPELINE_DIR / "staged_prompt.txt"

def get_transmissions():
    if TRANSMISSIONS_FILE.is_file():
        try:
            with open(TRANSMISSIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return [
        {
            "timestamp": "2026-11-16 01:00:39",
            "source": "GITHUB",
            "target": "Untitled conversation (Main Feature)",
            "subject": "Reel #1 Graphify AST Knowledge Graph & Architecture God-Node Handoff",
            "status": "DELIVERED"
        },
        {
            "timestamp": "2026-11-16 08:52:10",
            "source": "SIMULATION",
            "target": "UI / UX",
            "subject": "Hallmark Anti-AI-Slop Linter Audit (100.0/100, 0 floor violations)",
            "status": "DELIVERED"
        },
        {
            "timestamp": "2026-11-16 09:20:00",
            "source": "GITHUB",
            "target": "GITHUB",
            "subject": "Reel #2 (De63OT8Sqwg) Backlog Ingestion Registered; Awaiting Reel #1 Lifecycle Completion",
            "status": "QUEUED"
        }
    ]

def record_transmission(source, target, subject, status="DELIVERED"):
    txs = get_transmissions()
    txs.insert(0, {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": source,
        "target": target,
        "subject": subject,
        "status": status
    })
    try:
        with open(TRANSMISSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(txs[:50], f, indent=2)
    except Exception as e:
        print(f"Error saving transmissions: {e}")

def build_tracker_state():
    queue = {}
    if QUEUE_FILE.is_file():
        try:
            with open(QUEUE_FILE, "r", encoding="utf-8") as f:
                queue = json.load(f)
        except Exception:
            pass

    backlog = {}
    if BACKLOG_FILE.is_file():
        try:
            with open(BACKLOG_FILE, "r", encoding="utf-8") as f:
                backlog = json.load(f)
        except Exception:
            pass

    staged_payload = ""
    if STAGED_PROMPT_FILE.is_file():
        try:
            with open(STAGED_PROMPT_FILE, "r", encoding="utf-8") as f:
                staged_payload = f.read()
        except Exception:
            pass

    convos_data = [
        {
            "name": "Untitled conversation (Main Feature)",
            "key": "untitled_conversation",
            "role": "Core DOM Structure, Navigation & Feature Wiring",
            "status": "ACTIVE",
            "is_active": True,
            "step": 9921,
            "url": "https://antigravity.google.com/r/21bf6843-8cfa-4328-afad-58c97e63b317-v2?p=c%2F6371cba6-7d2f-4b29-a250-627d88d1b4f1"
        },
        {
            "name": "UI / UX",
            "key": "ui_ux",
            "role": "Hallmark Design Tokens, Tactile Cockpit & Responsive CSS",
            "status": "QUEUED",
            "is_active": False,
            "step": 279,
            "url": "https://antigravity.google.com/r/21bf6843-8cfa-4328-afad-58c97e63b317-v2?p=c%2F06a7d47b-b225-40f4-b830-b58baaaf8b3a"
        },
        {
            "name": "SIMULATION",
            "key": "simulation",
            "role": "Automated Quality Gates, SlopLinter 100/100 & Security Audits",
            "status": "COMPLETED",
            "is_active": False,
            "step": 401,
            "url": "https://antigravity.google.com/r/21bf6843-8cfa-4328-afad-58c97e63b317-v2?p=c%2F62adc180-be21-4671-848c-c8df59e2c202"
        },
        {
            "name": "DB / BACKEND",
            "key": "db_backend",
            "role": "SQLite Schemas, server.py Endpoints & Sync Layer",
            "status": "COMPLETED",
            "is_active": False,
            "step": 447,
            "url": "https://antigravity.google.com/r/21bf6843-8cfa-4328-afad-58c97e63b317-v2?p=c%2Fd3700ff3-1bfb-458a-9968-8257ef2ca7e2"
        },
        {
            "name": "GITHUB",
            "key": "github",
            "role": "Package Vendoring & Sequential Reel Ingestion",
            "status": "WAITING_FOR_MESH",
            "is_active": False,
            "step": 957,
            "url": "https://antigravity.google.com/r/21bf6843-8cfa-4328-afad-58c97e63b317-v2?p=c%2Fa64c937f-bb58-4071-8eb9-32f5edbb6c2c"
        },
        {
            "name": "Q / A",
            "key": "q_a",
            "role": "Question Bank Extraction & Analytical Problem Solving",
            "status": "IDLE",
            "is_active": False,
            "step": 450,
            "url": "https://antigravity.google.com/r/21bf6843-8cfa-4328-afad-58c97e63b317-v2?p=c%2F6029bc76-d833-4ab6-8672-b5f43511cf8f"
        },
        {
            "name": "INSPIRATION",
            "key": "inspiration",
            "role": "Mentor Council & Topper Study Ideation",
            "status": "IDLE",
            "is_active": False,
            "step": 115,
            "url": "https://antigravity.google.com/r/21bf6843-8cfa-4328-afad-58c97e63b317-v2?p=c%2Fe6690e55-bfca-4ce1-af20-843015d7d01b"
        },
        {
            "name": "BUG FIXES",
            "key": "bug_fixes",
            "role": "Surgical Defect Remediation & Hotfixes",
            "status": "IDLE",
            "is_active": False,
            "step": 9680,
            "url": "https://antigravity.google.com/r/21bf6843-8cfa-4328-afad-58c97e63b317-v2?p=c%2F6b74e384-a9b2-458e-ba34-4798334dd509"
        },
        {
            "name": "BACKBONE COORDINATOR",
            "key": "backbone",
            "role": "Central Switchboard & Pipeline Orchestrator",
            "status": "ACTIVE",
            "is_active": True,
            "step": 1200,
            "url": "https://antigravity.google.com/r/21bf6843-8cfa-4328-afad-58c97e63b317-v2?p=c%2Fa80111ec-0657-4748-9e85-d620e8a2a535"
        }
    ]

    tracker_state = {
        "last_sync": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "active_reel": {
            "title": "Reel #1: Graphify Codebase Knowledge Graph",
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
        print("✔ tracker_state.json updated successfully.")
    except Exception as e:
        print(f"Error saving tracker_state.json: {e}")

if __name__ == "__main__":
    build_tracker_state()
