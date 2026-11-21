import json

transcript_path = r'C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\.system_generated\logs\transcript.jsonl'
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        idx = obj.get("step_index")
        if idx in [581, 583]:
            c = obj.get("content", "")
            if "[WEBVIEW_BROWSER_HUD]" in c:
                print(f"==================== STEP {idx} HUD FULL TEXT ====================")
                lines = c.split("\n")
                main_start = False
                count = 0
                for l in lines:
                    if "- main" in l:
                        main_start = True
                    if main_start and count < 60:
                        print(l)
                        count += 1
