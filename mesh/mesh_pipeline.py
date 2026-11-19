import json
import os
import sys
from datetime import datetime

REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "mesh_registry.json")
STATE_PATH = os.path.join(os.path.dirname(__file__), "pipeline_state.json")

# Strict Pipeline Stage Ordering
PRIORITY_RANKS = {
    "db_backend": 0,       # Foundation: Schemas, Auth, APIs
    "feature_builder": 1,  # Core: Business logic
    "ui_ux": 1,            # Core: Design language, layouts
    "qa_engine": 2,        # Data: Question ingestion & parsing
    "simulation": 3,       # Audit: NEVER run at start, runs after Trio finishes
    "bug_fix": 4,          # Surgical fixes: Triggered only by simulation
    "github": 5            # Deployment: Only after 0 bugs certified
}

def load_json(path, default=None):
    if not os.path.exists(path):
        return default or {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def init_pipeline():
    registry = load_json(REGISTRY_PATH)
    state = load_json(STATE_PATH, {
        "last_updated": datetime.now().isoformat(),
        "active_cycle": "Cycle 1: Foundation & Setup",
        "tasks": [],
        "activity_log": [
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "node": "backbone",
                "message": "Mesh system initialized. 10 nodes registered and active."
            }
        ]
    })
    save_json(STATE_PATH, state)
    return registry, state

def add_task(title, target_node, instructions, context_files=None, from_node="planner"):
    registry, state = init_pipeline()
    if target_node not in registry["nodes"]:
        raise ValueError(f"Unknown target node: {target_node}. Must be one of {list(registry['nodes'].keys())}")
    
    task_id = f"TASK-{len(state['tasks']) + 1:03d}"
    priority = PRIORITY_RANKS.get(target_node, 99)

    new_task = {
        "id": task_id,
        "title": title,
        "from_node": from_node,
        "target_node": target_node,
        "target_convo_id": registry["nodes"][target_node]["conversation_id"],
        "priority_rank": priority,
        "status": "QUEUED",
        "context_files": context_files or [],
        "instructions": instructions,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    state["tasks"].append(new_task)
    # Re-sort tasks by priority rank so foundational tasks execute first
    state["tasks"].sort(key=lambda t: t["priority_rank"])
    
    state["activity_log"].append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "node": "backbone",
        "message": f"Queued {task_id} for {registry['nodes'][target_node]['name']} (Priority Level {priority})"
    })
    state["last_updated"] = datetime.now().isoformat()
    save_json(STATE_PATH, state)
    print(f"✅ Created {task_id} [{registry['nodes'][target_node]['name']}] - Priority {priority}")
    return new_task

def format_dispatch_prompt(task_id):
    _, state = init_pipeline()
    registry = load_json(REGISTRY_PATH)
    task = next((t for t in state["tasks"] if t["id"] == task_id), None)
    if not task:
        print(f"❌ Task {task_id} not found.")
        return None
    
    target_info = registry["nodes"][task["target_node"]]
    prompt = f"""[DISPATCH FROM BACKBONE (CHITTI) // {task['id']}]
Target Node: {target_info['name']}
Target Conversation ID: {task['target_convo_id']}
Priority Rank: {task['priority_rank']} | Status: {task['status']}

---
OBJECTIVE:
{task['title']}

CONTEXT & FILES:
{', '.join(task['context_files']) if task['context_files'] else 'None'}

INSTRUCTIONS & SPECIFICATIONS:
{task['instructions']}

---
HANDOFF RULE:
When complete, provide your deliverable summary and output files, then report back to Backbone (Chitti) to trigger the next queued stage.
"""
    return prompt

if __name__ == "__main__":
    init_pipeline()
    print("Mesh pipeline initialized successfully.")
