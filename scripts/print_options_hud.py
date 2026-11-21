import json

transcript_path = r'C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\.system_generated\logs\transcript.jsonl'
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        idx = obj.get("step_index")
        if idx in [581, 583]:
            c = obj.get("content", "")
            if "[WEBVIEW_BROWSER_HUD]" in c:
                print(f"==================== STEP {idx} HUD OPTIONS ====================")
                lines = c.split("\n")
                record = False
                for l in lines:
                    if "text: A biker" in l or "text: A person is walking" in l:
                        record = True
                    if record and ("button \"Previous\"" in l or "omitted" in l):
                        record = False
                    if record:
                        print(" ", l.strip()[:100])
