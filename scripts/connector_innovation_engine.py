#!/usr/bin/env python3
"""
scripts/connector_innovation_engine.py
================================================================================
Swarm Connector Bot for Innovation & Pedagogy Node (connector-innovation)
Conversation ID: 37d092f4-06fe-43f4-886a-4070f5b28256
Node Role: Innovation & Pedagogy

Mandate:
  - Interfaces directly with Backbone (Chitti) [b5f97b16-8c62-47fd-92b6-1c96b5172e19]
  - Dispatches research dossiers, pedagogical frameworks, and feature blueprints
    to Backbone for Planner [7b4415e6-d51f-45cf-9ccd-b3c103323d0e] review.
  - Strict research boundary (zero application code modifications).
================================================================================
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE))
sys.path.insert(0, str(WORKSPACE / "scripts"))

import mesh_connector_bus

# Canonical Node Identity
INNOVATION_NODE = "Innovation"
INNOVATION_ID = "37d092f4-06fe-43f4-886a-4070f5b28256"
BACKBONE_NODE = "Backbone (Chitti)"
BACKBONE_ID = "b5f97b16-8c62-47fd-92b6-1c96b5172e19"
PLANNER_NODE = "Planner"
PLANNER_ID = "7b4415e6-d51f-45cf-9ccd-b3c103323d0e"

DOSSIERS_DIR = WORKSPACE / "dossiers"
DOSSIERS_DIR.mkdir(parents=True, exist_ok=True)
STATE_PATH = WORKSPACE / "mesh" / "pipeline_state.json"
TRACKER_STATE_PATH = WORKSPACE / "mesh" / "mesh_tracker_state.json"

def dispatch_dossier_to_planner(dossier_json_path):
    """
    Reads a prepared research dossier and transmits it across the Mesh Connector Bus
    to Backbone (Chitti) targeted for Planner review.
    """
    with open(dossier_json_path, "r", encoding="utf-8") as f:
        dossier = json.load(f)

    md_filename = dossier_json_path.stem + ".md"
    md_path = dossier_json_path.parent / md_filename

    priority = "P1"
    if dossier.get("summary", {}).get("p0_priority", 0) > 0:
        priority = "P0"

    handoff_data = {
        "dossier_id": dossier["dossier_id"],
        "dossier_file": str(md_path.relative_to(WORKSPACE)),
        "summary": dossier.get("summary", {}),
        "proposal_count": len(dossier.get("proposals", [])),
        "proposals": [
            {
                "id": p["id"],
                "name": p["name"],
                "priority": p["priority"],
                "target_subsystem": p["target_subsystem"],
                "impact_metric": p["impact_metric"]
            }
            for p in dossier.get("proposals", [])
        ]
    }

    # 1. Send via Mesh Connector Bus
    dispatch_id = mesh_connector_bus.send_to_backbone(
        sender_node=INNOVATION_NODE,
        intended_target=PLANNER_NODE,
        priority=priority,
        handoff_data=handoff_data
    )
    print(f"🚀 Dispatched {dossier['dossier_id']} to Backbone (Chitti) -> Target: Planner. Bus ID: {dispatch_id}")

    # 2. Update mesh/pipeline_state.json
    if STATE_PATH.exists():
        try:
            with open(STATE_PATH, "r", encoding="utf-8") as f:
                state = json.load(f)

            task_id = f"TASK-{len(state.get('tasks', [])) + 1:03d}"
            new_task = {
                "id": task_id,
                "title": f"INNOVATION-DOSSIER: Architectural Review of {len(dossier.get('proposals', []))} Next-Gen Features ({dossier['dossier_id']})",
                "from_node": "innovation",
                "target_node": "planner",
                "target_convo_id": PLANNER_ID,
                "priority_rank": 2,
                "status": "QUEUED",
                "context_files": [str(md_path.relative_to(WORKSPACE))],
                "instructions": f"Planner: Evaluate {len(dossier.get('proposals', []))} feature blueprints cataloged in {md_path.name} (ChemPulse SRS, PercentileRadar, StreakForge, Topper Taxonomy). Prioritize implementation into Cycle 5 Sprint Backlog.",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            state.setdefault("tasks", []).append(new_task)
            state.setdefault("activity_log", []).append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "node": "innovation",
                "message": f"💡 Innovation & Pedagogy generated {dossier['dossier_id']} ({len(dossier.get('proposals', []))} proposals). Routed through Backbone for Planner."
            })
            with open(STATE_PATH, "w", encoding="utf-8") as f:
                json.dump(state, f, indent=2)
            print(f"✓ Recorded {task_id} in mesh/pipeline_state.json")
        except Exception as e:
            print(f"Warning: could not update pipeline_state.json: {e}")

    # 3. Update mesh/mesh_tracker_state.json telemetry
    if TRACKER_STATE_PATH.exists():
        try:
            with open(TRACKER_STATE_PATH, "r", encoding="utf-8") as f:
                t_state = json.load(f)
            if "nodes" in t_state and "innovation" in t_state["nodes"]:
                t_state["nodes"]["innovation"]["current_task"] = f"Dossier {dossier['dossier_id']} routed to Backbone -> Planner"
                t_state["nodes"]["innovation"]["last_dispatch"] = datetime.now().isoformat()
            with open(TRACKER_STATE_PATH, "w", encoding="utf-8") as f:
                json.dump(t_state, f, indent=2)
            print("✓ Updated mesh/mesh_tracker_state.json telemetry")
        except Exception as e:
            print(f"Warning: could not update mesh_tracker_state.json: {e}")

    return dispatch_id

def main():
    target_dossier = DOSSIERS_DIR / "DOSSIER-INNOVATION-20261122_000500.json"
    if not target_dossier.exists():
        print(f"Error: Dossier file {target_dossier} not found.")
        sys.exit(1)

    dispatch_id = dispatch_dossier_to_planner(target_dossier)
    print(f"Success: Dispatch completed with ID {dispatch_id}")

if __name__ == '__main__':
    main()
