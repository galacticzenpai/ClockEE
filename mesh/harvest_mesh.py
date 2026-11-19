import json
import os
import glob
from datetime import datetime

BRAIN_DIR = r"C:\Users\Kunal\.gemini\antigravity\brain"
REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "mesh_registry.json")
STATE_PATH = os.path.join(os.path.dirname(__file__), "pipeline_state.json")
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "mesh_tracker_state.json")

def load_json(path, default=None):
    if not os.path.exists(path):
        return default or {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return default or {}

def parse_transcript(convo_id, max_steps=40):
    transcript_file = os.path.join(BRAIN_DIR, convo_id, ".system_generated", "logs", "transcript.jsonl")
    if not os.path.exists(transcript_file):
        return {
            "exists": False,
            "steps_count": 0,
            "status": "IDLE",
            "active_tool": None,
            "last_updated": None,
            "latest_content": "No activity recorded yet.",
            "latest_thinking": "",
            "steps": []
        }

    steps = []
    try:
        with open(transcript_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    steps.append(json.loads(line))
                except:
                    continue
    except Exception as e:
        print(f"Error reading transcript for {convo_id}: {e}")

    total_steps = len(steps)
    recent_steps = steps[-max_steps:] if steps else []
    
    # Analyze latest state
    active_tool = None
    latest_content = ""
    latest_thinking = ""
    last_updated = None
    status = "IDLE"

    if steps:
        last_step = steps[-1]
        last_updated = last_step.get("created_at")
        status = "ACTIVE" if last_step.get("status") == "RUNNING" else "COMPLETED"
        latest_content = last_step.get("content") or ""
        latest_thinking = last_step.get("thinking") or ""
        
        # Check for tool calls in reverse
        for s in reversed(steps):
            if s.get("tool_calls"):
                tc = s["tool_calls"][-1]
                active_tool = {
                    "name": tc.get("name"),
                    "summary": str(tc.get("args", {})).replace('"', '')[:80],
                    "status": s.get("status", "DONE")
                }
                break

    # Format simplified step models for inspector
    formatted_steps = []
    for s in recent_steps:
        formatted_steps.append({
            "step_index": s.get("step_index", 0),
            "source": s.get("source", "UNKNOWN"),
            "type": s.get("type", "GENERIC"),
            "status": s.get("status", "DONE"),
            "created_at": s.get("created_at", ""),
            "content": s.get("content") or "",
            "thinking": s.get("thinking") or "",
            "tool_calls": s.get("tool_calls", [])
        })

    return {
        "exists": True,
        "steps_count": total_steps,
        "status": status,
        "active_tool": active_tool,
        "last_updated": last_updated,
        "latest_content": latest_content[:1500] if latest_content else "",
        "latest_thinking": latest_thinking[:1500] if latest_thinking else "",
        "steps": formatted_steps
    }

def build_full_tracker_state():
    registry = load_json(REGISTRY_PATH, {"nodes": {}})
    pipeline_state = load_json(STATE_PATH, {"tasks": [], "activity_log": []})

    conversations_data = {}
    total_tokens = 0

    for key, node in registry.get("nodes", {}).items():
        convo_id = node.get("conversation_id")
        parsed = parse_transcript(convo_id)
        
        conversations_data[key] = {
            "key": key,
            "name": node.get("name"),
            "conversation_id": convo_id,
            "role": node.get("role"),
            "can_edit_code": node.get("can_edit_code", False),
            "status": parsed["status"],
            "steps_count": parsed["steps_count"],
            "last_updated": parsed["last_updated"],
            "active_tool": parsed["active_tool"],
            "latest_content": parsed["latest_content"],
            "latest_thinking": parsed["latest_thinking"],
            "steps": parsed["steps"]
        }

    # Transmissions from activity log
    transmissions = []
    for log in pipeline_state.get("activity_log", []):
        transmissions.append({
            "timestamp": log.get("timestamp"),
            "node": log.get("node"),
            "message": log.get("message")
        })

    # Playbook tasks
    playbook_tasks = []
    for t in pipeline_state.get("tasks", []):
        playbook_tasks.append({
            "id": t.get("id"),
            "title": t.get("title"),
            "target_node": t.get("target_node"),
            "priority": f"P{t.get('priority_rank', 1)}",
            "status": t.get("status"),
            "instructions": t.get("instructions"),
            "created_at": t.get("created_at")
        })

    full_payload = {
        "sync_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "project": "JEE Aspirant Educational Platform - Multi-Agent Mesh",
        "active_cycle": pipeline_state.get("active_cycle", "Cycle 1"),
        "metrics": {
            "total_nodes": len(registry.get("nodes", {})),
            "active_nodes": sum(1 for c in conversations_data.values() if c["steps_count"] > 0),
            "total_tasks": len(playbook_tasks),
            "completed_tasks": sum(1 for t in playbook_tasks if t["status"] in ["COMPLETED", "APPROVED"]),
            "pending_tasks": sum(1 for t in playbook_tasks if t["status"] not in ["COMPLETED", "APPROVED"])
        },
        "conversations": conversations_data,
        "playbook": playbook_tasks,
        "transmissions": transmissions
    }

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(full_payload, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Harvester compiled state with {len(conversations_data)} nodes into {OUTPUT_PATH}")
    return full_payload

if __name__ == "__main__":
    build_full_tracker_state()
