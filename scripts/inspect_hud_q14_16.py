import json

transcript_path = r'C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\.system_generated\logs\transcript.jsonl'
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        idx = obj.get("step_index")
        if idx in [551, 552, 553, 554, 555, 556, 557, 567, 568, 569, 570, 571, 572, 573]:
            content = obj.get("content", "")
            if "[WEBVIEW_BROWSER_HUD]" in content:
                # print first 50 lines of HUD
                hud_lines = [l for l in content.split("\n") if "text:" in l or "14 of 90" in l or "15 of 90" in l or "16 of 90" in l]
                print(f"--- STEP {idx} HUD text lines: ---")
                for l in hud_lines[:15]:
                    print(" ", l.strip())
            elif obj.get("type") == "PLANNER_RESPONSE":
                obs = obj.get("tool_calls", [{}])[0].get("args", {}).get("observation", "")
                if obs:
                    print(f"--- STEP {idx} Observation: {obs[:150]} ---")
