import json

transcript_path = r'C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\.system_generated\logs\transcript.jsonl'
lines = []
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        lines.append(line)

print(f"Total steps in subagent transcript: {len(lines)}")
for l in lines[-6:]:
    obj = json.loads(l)
    sidx = obj.get("step_index")
    stype = obj.get("type")
    sstatus = obj.get("status")
    print(f"step_index: {sidx}, type: {stype}, status: {sstatus}")
    if obj.get("tool_calls"):
        for tc in obj.get("tool_calls"):
            print("  tool_call:", tc.get("name"), tc.get("args", {}).get("intention", ""))
    if obj.get("content") and stype != "PLANNER_RESPONSE":
        c = obj.get("content")
        print("  content:", c[:200].replace('\n', ' '))
