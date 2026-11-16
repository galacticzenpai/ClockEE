import json
from pathlib import Path

t_path = Path(r"C:\Users\Kunal\.gemini\antigravity\brain\a64c937f-bb58-4071-8eb9-32f5edbb6c2c\.system_generated\logs\transcript.jsonl")
if t_path.is_file():
    size = t_path.stat().st_size
    with open(t_path, "rb") as f:
        if size > 65536:
            f.seek(size - 65536)
        chunk = f.read()
    lines = chunk.decode("utf-8", errors="ignore").splitlines()
    for line in lines[-10:]:
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
            content = str(obj.get("content", ""))[:200].replace("\n", " ")
            print(f"Step {obj.get('step_index')} [{obj.get('source')}/{obj.get('type')}]: {content}")
        except Exception as e:
            pass
