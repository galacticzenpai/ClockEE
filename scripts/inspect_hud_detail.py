import json

transcript_path = r'C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\.system_generated\logs\transcript.jsonl'
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        idx = obj.get("step_index")
        if idx in [580, 581, 582, 583, 584, 585]:
            c = obj.get("content", "")
            if "[WEBVIEW_BROWSER_HUD]" in c:
                print(f"=== STEP {idx} HUD ===")
                for l in c.split("\n"):
                    if any(w in l for w in ["text:", "button", "generic", "ref="]) and "omitted" not in l and "pointer" not in l:
                        print("  ", l.strip()[:100])
