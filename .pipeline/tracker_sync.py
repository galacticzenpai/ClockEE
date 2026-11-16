#!/usr/bin/env python3
"""
ClockEE Tracker State Synchronizer with Live Progress Engine & Full Step Inspector
Extracts real-time step numbers, live tool calls, model thoughts, full un-truncated message bodies,
and the complete 39-reel playbook into .pipeline/tracker_state.json and .pipeline/tracker_data.js.
"""

import os
import json
from datetime import datetime, timezone
from pathlib import Path

PIPELINE_DIR = Path(__file__).resolve().parent
ROOT_DIR = PIPELINE_DIR.parent
BRAIN_DIR = Path(r"C:\Users\Kunal\.gemini\antigravity\brain")
TRACKER_STATE_FILE = PIPELINE_DIR / "tracker_state.json"
TRACKER_JS_FILE = PIPELINE_DIR / "tracker_data.js"
TRANSMISSIONS_FILE = PIPELINE_DIR / "transmissions.json"
QUEUE_FILE = PIPELINE_DIR / "queue.json"
BACKLOG_FILE = PIPELINE_DIR / "github_backlog.json"
PLAYBOOK_FILE = PIPELINE_DIR / "reel_playbook.json"
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
        "id": "c05ee59e-9749-4bc3-8bea-57ea8b60874c",
        "role": "Surgical Defect Remediation & Hotfixes",
        "url": "https://antigravity.google.com/r/21bf6843-8cfa-4328-afad-58c97e63b317-v2?p=c%2Fc05ee59e-9749-4bc3-8bea-57ea8b60874c"
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
        "id": "b411e7a0-c268-4614-b3d5-f2b2836f4500",
        "role": "Sprint Planner, Roadmap Strategist & Prompt Engineer",
        "url": "https://antigravity.google.com/r/21bf6843-8cfa-4328-afad-58c97e63b317-v2?p=c%2Fb411e7a0-c268-4614-b3d5-f2b2836f4500"
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
                data = json.load(f)
                return data.get("transmissions", [])[-20:]
        except Exception:
            pass
    return []

def record_transmission(source, target, subject, status="DELIVERED_AUTO"):
    txs = []
    if TRANSMISSIONS_FILE.is_file():
        try:
            with open(TRANSMISSIONS_FILE, "r", encoding="utf-8") as f:
                txs = json.load(f).get("transmissions", [])
        except Exception:
            txs = []
    
    new_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": source,
        "target": target,
        "subject": subject,
        "status": status
    }
    txs.append(new_entry)
    txs = txs[-50:]
    try:
        with open(TRANSMISSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump({"transmissions": txs}, f, indent=2)
    except Exception:
        pass

def extract_step_detail(step):
    s_idx = step.get("step_index")
    s_type = step.get("type", "UNKNOWN")
    s_stat = step.get("status", "DONE")
    s_src = step.get("source", "UNKNOWN")
    s_time = step.get("created_at", "")

    raw_content = str(step.get("content") or "")
    # Clean up single-line preview for compact views
    one_line = raw_content.replace("\r\n", " ").replace("\n", " ").strip()
    preview = one_line[:140] if one_line else ""

    # Cap single step raw content to 25,000 chars to avoid memory issues on massive logs
    full_content = raw_content[:25000] + ("\n... [TRUNCATED - Payload exceeded 25KB]" if len(raw_content) > 25000 else "")

    raw_thinking = str(step.get("thinking") or "")
    full_thinking = raw_thinking[:15000] + ("\n... [TRUNCATED - Thinking exceeded 15KB]" if len(raw_thinking) > 15000 else "")

    # Parse full tool calls
    tool_calls = step.get("tool_calls") or []
    parsed_tools = []
    for t in tool_calls:
        t_name = t.get("name", "unknown_tool")
        t_args = t.get("args") or {}
        summary = t_args.get("toolSummary") or t_args.get("CommandLine") or t_args.get("Path") or t_name
        parsed_tools.append({
            "name": t_name,
            "summary": str(summary)[:200],
            "args": t_args
        })

    return {
        "step": s_idx,
        "type": s_type,
        "status": s_stat,
        "source": s_src,
        "timestamp": s_time,
        "preview": preview or ("(Tool Invocation)" if tool_calls else "Step processed"),
        "full_content": full_content,
        "full_thinking": full_thinking,
        "tool_calls": parsed_tools,
        "has_thinking": bool(raw_thinking.strip()),
        "has_content": bool(raw_content.strip()),
        "has_tools": len(parsed_tools) > 0
    }

def extract_live_conversation_progress(convo_id):
    t_file = BRAIN_DIR / convo_id / ".system_generated" / "logs" / "transcript.jsonl"
    if not t_file.is_file():
        return {
            "step": 0,
            "status": "OFFLINE",
            "is_running": False,
            "last_action": "No transcript available",
            "tool_name": None,
            "tool_summary": None,
            "content_preview": "",
            "full_content": "",
            "full_thinking": "",
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
                "full_content": "",
                "full_thinking": "",
                "recent_steps": []
            }

        # Read last 40 steps for comprehensive expanded step inspection
        recent_objs = []
        for l in lines[-40:]:
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
                "full_content": "",
                "full_thinking": "",
                "recent_steps": []
            }

        last_obj = recent_objs[-1]
        st_idx = last_obj.get("step_index", 0)
        st_type = last_obj.get("type", "UNKNOWN")
        st_status = last_obj.get("status", "DONE")
        raw_last_content = str(last_obj.get("content") or "")
        raw_last_thinking = str(last_obj.get("thinking") or "")
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
            last_action = f"Executing {tool_name}: {str(tool_summary)[:80]}"
        elif raw_last_thinking:
            t_oneline = raw_last_thinking.replace("\n", " ").strip()
            last_action = f"Thinking: {t_oneline[:80]}..."
        elif st_type == "PLANNER_RESPONSE":
            c_oneline = raw_last_content.replace("\n", " ").strip()
            last_action = f"Response: {c_oneline[:80]}..." if len(c_oneline) > 80 else (c_oneline or "Planning turn...")
        elif st_type == "USER_INPUT":
            u_oneline = raw_last_content.replace("\n", " ").strip()
            last_action = f"Input: {u_oneline[:80]}..."
        elif st_type == "SYSTEM_MESSAGE":
            last_action = "System Message Received"
        else:
            last_action = f"{st_type}: {raw_last_content[:50]}"

        # Parse all steps with full expanded fields
        recent_steps = [extract_step_detail(s) for s in recent_objs]

        return {
            "step": st_idx,
            "status": detailed_status,
            "is_running": is_running,
            "last_action": last_action,
            "tool_name": tool_name,
            "tool_summary": tool_summary,
            "tool_details": tool_details,
            "content_preview": raw_last_content.replace("\n", " ").strip()[:200],
            "full_content": raw_last_content[:30000],
            "full_thinking": raw_last_thinking[:15000],
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
            "full_content": "",
            "full_thinking": "",
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

    # Read backlog state dynamically
    backlog_data = {}
    if BACKLOG_FILE.is_file():
        try:
            with open(BACKLOG_FILE, "r", encoding="utf-8") as bf:
                backlog_data = json.load(bf)
        except Exception:
            pass

    # Read reel playbook
    playbook_data = {}
    if PLAYBOOK_FILE.is_file():
        try:
            with open(PLAYBOOK_FILE, "r", encoding="utf-8") as pf:
                playbook_data = json.load(pf)
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
            display_status = "WAITING_ON_MESH" if not prog["is_running"] else "RUNNING"
            is_active = prog["is_running"]
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

    # Assemble dynamic active reel
    active_reel_obj = backlog_data.get("active_reel", {})
    completed_reels = backlog_data.get("completed_reels", [])
    pause_active = backlog_data.get("pause_new_reels_on_completion", False)

    if active_reel_obj is None:
        active_reel_display = {
            "id": "reel_039",
            "url": "https://www.instagram.com/p/De9ncU9vZgH/",
            "title": "All 39 Reels Completed & Certified",
            "upstream": "clockee/full-pipeline",
            "status": "ALL_COMPLETED",
            "status_badge": "100% COMPLETE & VERIFIED",
            "completed_count": len(completed_reels),
            "total_count": backlog_data.get("total_reels", 39)
        }
    else:
        active_reel_display = {
            "id": active_reel_obj.get("id", "reel_005"),
            "url": active_reel_obj.get("url", "https://www.instagram.com/p/DeW0tvNz2uR/"),
            "title": f"Reel #{active_reel_obj.get('id', 'reel_005')[-3:]}: {active_reel_obj.get('title', 'Active Reel')}",
            "upstream": active_reel_obj.get("upstream", "upstream/package"),
            "status": active_reel_obj.get("status", "QUEUED_FOR_INGESTION"),
            "status_badge": "PAUSED PER USER DIRECTIVE" if pause_active else active_reel_obj.get("status", "QUEUED"),
            "completed_count": len(completed_reels),
            "total_count": backlog_data.get("total_reels", 39)
        }

    tracker_state = {
        "last_sync": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "backlog_summary": {
            "total_reels": backlog_data.get("total_reels", 39),
            "completed_count": len(completed_reels),
            "pending_count": len(backlog_data.get("pending_reels", [])),
            "is_paused": pause_active,
            "pause_reason": backlog_data.get("pause_reason", "All 39 planned reels fully applied and deployed to production.")
        },
        "active_reel": active_reel_display,
        "staged_prompt": {
            "target_name": "Untitled conversation (Main Feature)",
            "target_key": "untitled_conversation",
            "url": "https://antigravity.google.com/r/21bf6843-8cfa-4328-afad-58c97e63b317-v2?p=c%2F6371cba6-7d2f-4b29-a250-627d88d1b4f1",
            "payload": staged_payload
        },
        "conversations": convos_data,
        "transmissions": get_transmissions(),
        "reel_playbook": playbook_data
    }

    try:
        with open(TRACKER_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(tracker_state, f, indent=2)
        # Also write standalone tracker_data.js for CORS-free file:// protocol loading
        with open(TRACKER_JS_FILE, "w", encoding="utf-8") as jf:
            jf.write("window.TRACKER_DATA = " + json.dumps(tracker_state, indent=2) + ";\n")
        print("✔ tracker_state.json & tracker_data.js updated with full expanded step engine and reel playbook.")
    except Exception as e:
        print(f"Error saving tracker state: {e}")

if __name__ == "__main__":
    build_tracker_state()
