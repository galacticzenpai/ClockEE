import json

transcript_path = r'C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\.system_generated\logs\transcript.jsonl'
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        idx = obj.get("step_index")
        if idx in [580, 581, 582, 583, 584]:
            stype = obj.get("type")
            print(f"=== STEP {idx} ({stype}) ===")
            if stype == "PLANNER_RESPONSE":
                print("Thinking:", obj.get("thinking", "")[:500])
            else:
                c = obj.get("content", "")
                if "[WEBVIEW_BROWSER_HUD]" in c:
                    for l in c.split("\n"):
                        if any(k in l for k in ["text:", "21 of 90", "24 of 90", "Type :", "Single Choice", "Multiple Choice"]):
                            print(" ", l.strip())
