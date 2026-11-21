import json

transcript_path = r'C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\.system_generated\logs\transcript.jsonl'
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        idx = obj.get("step_index")
        if idx in [525, 529, 537]:
            tc = obj.get("tool_calls", [{}])[0]
            script = tc.get("args", {}).get("script", "")
            print(f"=== STEP {idx} script ===")
            print(script[:400])
