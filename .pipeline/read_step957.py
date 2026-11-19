import json
from pathlib import Path

t_path = Path(r"C:\Users\Kunal\.gemini\antigravity\brain\a64c937f-bb58-4071-8eb9-32f5edbb6c2c\.system_generated\logs\transcript.jsonl")
if t_path.is_file():
    with open(t_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    obj = json.loads(line)
                    if obj.get("step_index") == 957:
                        print(obj.get("content"))
                except Exception as e:
                    pass
