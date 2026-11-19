import json
from pathlib import Path

t_path = Path(r"C:\Users\Kunal\.gemini\antigravity\brain\a64c937f-bb58-4071-8eb9-32f5edbb6c2c\.system_generated\logs\transcript.jsonl")
if t_path.is_file():
    with open(t_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    obj = json.loads(line)
                    if obj.get("step_index", 0) > 888 and obj.get("source") == "MODEL" and obj.get("type") == "PLANNER_RESPONSE":
                        print(f"Step {obj.get('step_index')}: {str(obj.get('content'))[:400]}")
                        print("="*60)
                except Exception as e:
                    pass
