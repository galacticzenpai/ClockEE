import json
import os
import shutil
import sys
from agentapi_rpc import AgentAPIRPCClient

PIPELINE_DIR = os.path.dirname(__file__)
QUEUE_PATH = os.path.join(PIPELINE_DIR, "queue.json")
ARCHIVE_PATH = os.path.join(PIPELINE_DIR, "queue_archive_plan_20261116_193500.json")

def execute_reset():
    # 1. Archive current queue
    if os.path.exists(QUEUE_PATH):
        shutil.copy2(QUEUE_PATH, ARCHIVE_PATH)
        print(f"✔ Current execution queue archived to: {ARCHIVE_PATH}")

    with open(QUEUE_PATH, "r", encoding="utf-8") as f:
        queue_data = json.load(f)

    # 2. Register 11th node: DEPLOY
    active_convs = queue_data.get("active_conversations", {})
    active_convs["deploy"] = {
        "id": "deploy_commander_v2",
        "role": "Production Deployment & Vercel Release Commander",
        "target": "vercel_production",
        "status": "READY"
    }
    queue_data["active_conversations"] = active_convs

    # Update current batch to Grand Reset
    queue_data["current_batch"] = {
        "batch_id": "batch_grand_reset_clean_slate_001",
        "source": "planning",
        "title": "ClockEE Grand Reset: Clean-Slate Architecture with 100% Knowledge Preservation",
        "status": "RESET_INITIALIZED",
        "timestamp": "2026-11-16T20:00:00+05:30",
        "mandate": "Wipe technical debt; 100% preservation of all 39 reels, research, and design tokens.",
        "nodes_active": 11
    }

    with open(QUEUE_PATH, "w", encoding="utf-8") as f:
        json.dump(queue_data, f, indent=2)
    print("✔ 11th mesh node (DEPLOY) registered and queue.json updated.")

    # 3. Broadcast across mesh
    client = AgentAPIRPCClient()
    broadcast_msg = (
        "=== 🏛️ CLOCKEE GRAND RESET & KNOWLEDGE PRESERVATION BROADCAST ===\n"
        "Directive: Clean-Slate Architectural Restart with 100% Knowledge Preservation.\n"
        "Mandate: Owner has initialized a clean-slate rebuild to eliminate technical debt.\n"
        "RULES OF ENGAGEMENT:\n"
        "1. ZERO KNOWLEDGE IS WIPED: Retain all 39 reel learnings, APCA contrast rules, Apple HIG design tokens, "
        "and database schemas.\n"
        "2. 11-NODE MESH EXPANSION: DEPLOY node is officially registered as the 11th mesh agent.\n"
        "3. Stand by for the interactive prioritization breakdown and Phase 1 architecture dispatch from Planning."
    )

    targets = [
        ("UI / UX", active_convs.get("ui_ux", {}).get("id")),
        ("MAIN FEATURE", active_convs.get("untitled_conversation", {}).get("id")),
        ("SIMULATION", active_convs.get("simulation", {}).get("id")),
        ("BUG FIXES", active_convs.get("bug_fixes", {}).get("id")),
        ("GITHUB", active_convs.get("github", {}).get("id")),
        ("DB / BACKEND", active_convs.get("db_backend", {}).get("id")),
        ("Q / A", active_convs.get("q_a", {}).get("id")),
        ("INSPIRATION", active_convs.get("inspiration", {}).get("id")),
        ("PLANNING", active_convs.get("planning", {}).get("id"))
    ]

    for name, cid in targets:
        if cid:
            lat = client.send_async(recipient_id=cid, content=broadcast_msg, title="[GLOBAL RESET] ClockEE Clean-Slate Directive")
            print(f"✔ Broadcast to {name} ({cid[:8]}...) in {lat:.2f}ms")

if __name__ == "__main__":
    execute_reset()
