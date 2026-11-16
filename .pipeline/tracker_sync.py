#!/usr/bin/env python3
"""
ClockEE Tracker State Synchronizer with Live Progress Engine
Extracts real-time step numbers, live tool calls, model thoughts, and activity streams
for all conversations into .pipeline/tracker_state.json for tracker.html.
"""

import os
import json
from datetime import datetime, timezone
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
    "planning": {
        "name": "PLANNING & ROADMAP ARCHITECT",
        "id": "planning_conversation",
        "role": "Sprint Planner, Roadmap Strategist & Prompt Engineer",
        "url": "#"
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

def extract_live_conversation_progress(cid: str):
    """Parses transcript to extract real-time execution steps, tool calls, and model outputs."""
    t_file = BRAIN_DIR / cid / ".system_generated" / "logs" / "transcript.jsonl"
    if not t_file.is_file():
        return {
            "step": 0,
            "status": "OFFLINE",
            "is_running": False,
            "last_action": "No transcript available",
            "tool_name": None,
            "tool_summary": None,
            "content_preview": "",
            "recent_steps": []
        }

    try:
        with open(t_file, "r", encoding="utf-8", errors="ignore") as f:
            lines = [l.strip() for l in f if l.strip().startswith("{")]
        if not lines:
            return {
                "step": 0,
                "status": "EMPTY",
                "is_running": False,
                "last_action": "Initialized empty session",
                "tool_name": None,
                "tool_summary": None,
                "content_preview": "",
                "recent_steps": []
            }

        recent_objs = []
        for l in lines[-12:]:
            try:
                recent_objs.append(json.loads(l))
            except Exception:
                pass

        if not recent_objs:
            return {
                "step": 0,
                "status": "UNKNOWN",
                "is_running": False,
                "last_action": "Idle",
                "tool_name": None,
                "tool_summary": None,
                "content_preview": "",
                "thinking_preview": "",
                "recent_steps": []
            }

        last_obj = recent_objs[-1]
        st_idx = last_obj.get("step_index", 0)
        st_type = last_obj.get("type", "UNKNOWN")
        st_status = last_obj.get("status", "DONE")
        st_content = str(last_obj.get("content", "")).replace("\n", " ").strip()
        st_thinking = str(last_obj.get("thinking", "")).replace("\n", " ").strip()
        st_time = last_obj.get("created_at", "")

        # Detect active tool execution
        tool_name = None
        tool_summary = None
        tool_details = None
        tool_calls = last_obj.get("tool_calls") or []
        if tool_calls:
            first_tool = tool_calls[0]
            tool_name = first_tool.get("name")
            args = first_tool.get("args") or {}
            tool_summary = args.get("toolSummary") or args.get("CommandLine") or args.get("Path") or tool_name
            tool_details = {
                "name": tool_name,
                "summary": tool_summary,
                "path": args.get("Path"),
                "command": args.get("CommandLine")
            }

        # Calculate recency / running state
        is_running = (st_status in ["RUNNING", "IN_PROGRESS"]) or (len(tool_calls) > 0 and st_status != "DONE")

        # Determine detailed execution state
        if is_running:
            detailed_status = "EXECUTING_TOOL" if tool_name else "GENERATING"
        elif st_type == "PLANNER_RESPONSE":
            detailed_status = "RESPONSE_READY"
        elif st_type == "USER_INPUT":
            detailed_status = "INPUT_RECEIVED"
        else:
            detailed_status = "IDLE"

        # Determine last action text
        if tool_name:
            last_action = f"Executing {tool_name}: {tool_summary[:70]}"
        elif st_thinking:
            last_action = f"Thinking: {st_thinking[:70]}..."
        elif st_type == "PLANNER_RESPONSE":
            last_action = f"Response: {st_content[:70]}..." if len(st_content) > 70 else (st_content or "Planning turn...")
        elif st_type == "USER_INPUT":
            last_action = f"Input: {st_content[:70]}..."
        elif st_type == "SYSTEM_MESSAGE":
            last_action = "System Message Received"
        else:
            last_action = f"{st_type}: {st_content[:50]}"

        # Format recent steps for live terminal inspector
        recent_steps = []
        for step in recent_objs:
            s_idx = step.get("step_index")
            s_type = step.get("type")
            s_stat = step.get("status", "DONE")
            s_cnt = str(step.get("content", "")).replace("\n", " ").strip()
            s_thk = str(step.get("thinking", "")).replace("\n", " ").strip()
            s_tools = step.get("tool_calls") or []
            s_tool_desc = ""
            s_tool_name = None
            if s_tools:
                t = s_tools[0]
                s_tool_name = t.get("name")
                t_args = t.get("args") or {}
                s_tool_desc = f"{s_tool_name}: {t_args.get('toolSummary', t_args.get('CommandLine', t_args.get('Path', '')))}"

            recent_steps.append({
                "step": s_idx,
                "type": s_type,
                "status": s_stat,
                "tool_name": s_tool_name,
                "tool": s_tool_desc[:80] if s_tool_desc else None,
                "thinking": s_thk[:100] if s_thk else None,
                "preview": s_cnt[:100] if s_cnt else ("(Tool invocation)" if s_tools else "")
            })

        return {
            "step": st_idx,
            "status": detailed_status,
            "is_running": is_running,
            "last_action": last_action,
            "tool_name": tool_name,
            "tool_summary": tool_summary,
            "tool_details": tool_details,
            "content_preview": st_content[:180],
            "thinking_preview": st_thinking[:180],
            "timestamp": st_time,
            "recent_steps": recent_steps
        }
    except Exception as e:
        return {
            "step": 0,
            "status": f"ERROR: {e}",
            "is_running": False,
            "last_action": "Error reading transcript",
            "tool_name": None,
            "tool_summary": None,
            "content_preview": "",
            "recent_steps": []
        }

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

    # Build dynamic conversation state with real-time live progress
    convos_data = []
    for key, reg in CONVERSATION_REGISTRY.items():
        prog = extract_live_conversation_progress(reg["id"])
        
        # State tag determination
        if prog["is_running"]:
            display_status = "RUNNING"
            is_active = True
        elif key == "untitled_conversation":
            display_status = "ACTIVE"
            is_active = True
        elif key == "github":
            display_status = "WAITING_ON_MESH"
            is_active = False
        elif key == "simulation":
            display_status = "CERTIFIED_100"
            is_active = False
        elif key == "backbone":
            display_status = "DAEMON_ACTIVE"
            is_active = True
        else:
            display_status = "STANDBY"
            is_active = False

        convos_data.append({
            "key": key,
            "name": reg["name"],
            "role": reg["role"],
            "status": display_status,
            "is_active": is_active,
            "step": prog["step"],
            "url": reg["url"],
            "live_progress": prog
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
        print("✔ tracker_state.json updated with live conversation progress engine.")
    except Exception as e:
        print(f"Error saving tracker_state.json: {e}")

if __name__ == "__main__":
    build_tracker_state()
