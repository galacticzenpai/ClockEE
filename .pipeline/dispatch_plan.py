import json
import os
import sys
from agentapi_rpc import AgentAPIRPCClient

PLAN_PATH = os.path.join(os.path.dirname(__file__), "daily_plan.json")
QUEUE_PATH = os.path.join(os.path.dirname(__file__), "queue.json")

def dispatch_all():
    if not os.path.exists(PLAN_PATH):
        print(f"Plan file not found: {PLAN_PATH}")
        return

    with open(PLAN_PATH, "r", encoding="utf-8") as f:
        plan = json.load(f)

    with open(QUEUE_PATH, "r", encoding="utf-8") as f:
        queue = json.load(f)

    active_convs = queue.get("active_conversations", {})
    client = AgentAPIRPCClient()

    print(f"Dispatching Plan: {plan.get('title')} ({plan.get('plan_id')})")
    
    for task in plan.get("tasks", []):
        target = task.get("target")
        task_id = task.get("id")
        priority = task.get("priority", "P1")
        instruction = task.get("task")
        
        target_info = active_convs.get(target)
        if not target_info:
            print(f"Target '{target}' not found in active conversations, skipping.")
            continue
            
        recipient_id = target_info.get("id")
        title = f"[{priority}] {task_id}: {target.upper()} Directive"
        
        content = (
            f"=== MESH SPRINT DIRECTIVE: {task_id} ===\n"
            f"Target: {target_info.get('role')} ({recipient_id})\n"
            f"Priority: {priority}\n"
            f"Instructions:\n{instruction}\n\n"
            f"Please execute this task immediately, update relevant files, and report back status."
        )
        
        lat = client.send_async(recipient_id=recipient_id, content=content, title=title)
        print(f"✔ Dispatched {task_id} -> {target} ({recipient_id[:8]}...) in {lat:.2f}ms")

if __name__ == "__main__":
    dispatch_all()
