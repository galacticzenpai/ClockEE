import os
import json
import time

MESH_BUS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mesh_bus.json')
BACKBONE_ID = "b5f97b16-8c62-47fd-92b6-1c96b5172e19"

CONVERSATION_REGISTRY = {
    "Planner": "7b4415e6-d51f-45cf-9ccd-b3c103323d0e",
    "Backbone (Chitti)": "b5f97b16-8c62-47fd-92b6-1c96b5172e19",
    "GitHub": "d78b401e-4699-42cc-8aad-ed6f2c44c428",
    "Main Feature": "c3adf94a-9cfa-4a23-b055-c8df8757b041",
    "UI/UX": "7da67306-b0d1-425c-9ee4-166365f218d1",
    "Simulation": "56a83a63-c595-4bc7-a564-5defc1766715",
    "Bug Fix": "e5ca28e1-5055-4b76-89a8-d37b0b5930e8",
    "DB / Backend": "e2bd04a9-a20c-4d9a-bfa0-0db7fe390194",
    "Q/A Engine": "859110f2-3156-4c22-abb0-2a0253ab82c4",
    "Innovation": "37d092f4-06fe-43f4-886a-4070f5b28256"
}

def init_bus():
    default_data = {
        "version": "2.0.0",
        "backbone_orchestrator": BACKBONE_ID,
        "signals": [],
        "locks": {},
        "active_handoffs": [],
        "dispatches": [],
        "connector_bot_status": {k: "ONLINE" for k in CONVERSATION_REGISTRY if k != "Backbone (Chitti)"}
    }
    if not os.path.exists(MESH_BUS_FILE):
        with open(MESH_BUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, indent=2)
        return

    try:
        with open(MESH_BUS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        dirty = False
        if "dispatches" not in data:
            data["dispatches"] = []
            dirty = True
        if "connector_bot_status" not in data:
            data["connector_bot_status"] = default_data["connector_bot_status"]
            dirty = True
        if dirty:
            with open(MESH_BUS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
    except Exception:
        with open(MESH_BUS_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, indent=2)

def send_to_backbone(sender_node, intended_target, priority, handoff_data):
    """
    Called by ANY conversation's Connector Bot.
    Every signal MUST route through Backbone (Chitti).
    Priority: P0 (Blocker), P1 (Staggered Handoff), P2 (Parallel Audit)
    """
    init_bus()
    with open(MESH_BUS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    dispatch_id = f"disp_{int(time.time()*1000)}"
    entry = {
        "id": dispatch_id,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "sender": sender_node,
        "sender_id": CONVERSATION_REGISTRY.get(sender_node, "UNKNOWN"),
        "intended_target": intended_target,
        "target_id": CONVERSATION_REGISTRY.get(intended_target, "UNKNOWN"),
        "priority": priority,
        "backbone_status": "ROUTED_BY_CHITTI",
        "receiver_connector_status": "PENDING_CLAIM",
        "payload": handoff_data
    }
    data["dispatches"].append(entry)

    # Order by priority
    p_rank = {"P0": 0, "P1": 1, "P2": 2}
    data["dispatches"].sort(key=lambda x: p_rank.get(x.get("priority", "P2"), 9))

    with open(MESH_BUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    return dispatch_id

def receiver_poll_backbone(node_name):
    """
    Called by a conversation's Connector Bot to fetch tasks routed to it by Backbone.
    """
    init_bus()
    with open(MESH_BUS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    pending = [
        d for d in data.get("dispatches", [])
        if d.get("intended_target") == node_name and d.get("receiver_connector_status") == "PENDING_CLAIM"
    ]
    return pending

def receiver_acknowledge_dispatch(dispatch_id, result_summary):
    init_bus()
    with open(MESH_BUS_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for d in data.get("dispatches", []):
        if d.get("id") == dispatch_id:
            d["receiver_connector_status"] = "COMPLETED"
            d["completed_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            d["result"] = result_summary
            break

    with open(MESH_BUS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    init_bus()
    print("Backbone-Routed Connector Mesh Initialized successfully.")
