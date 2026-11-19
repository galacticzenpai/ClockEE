import json
with open('mesh/mesh_tracker_state.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print("Metrics:", d['metrics'])
print("\n--- NODES HARVESTED ---")
for k, v in d['conversations'].items():
    tool = v['active_tool']['name'] if v['active_tool'] else 'None'
    print(f"- {v['name']} ({k}): {v['steps_count']} steps | Status: {v['status']} | Last Tool: {tool}")
