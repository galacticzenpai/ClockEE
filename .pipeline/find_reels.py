import json
from pathlib import Path

t_path = Path(r"C:\Users\Kunal\.gemini\antigravity\brain\a64c937f-bb58-4071-8eb9-32f5edbb6c2c\.system_generated\logs\transcript.jsonl")
if t_path.is_file():
    with open(t_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    obj = json.loads(line)
                    if obj.get("type") == "USER_INPUT":
                        content = str(obj.get("content", ""))
                        if "reel" in content.lower() or "instagram" in content.lower() or "github" in content.lower():
                            print(f"Step {obj.get('step_index')}: {content[:300]}")
                            print("="*60)
                except Exception as e:
                    pass
