import json

transcript_path = r'C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\.system_generated\logs\transcript.jsonl'
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        idx = obj.get("step_index")
        if idx in [576, 577, 578, 579, 580, 582, 584, 586]:
            stype = obj.get("type")
            print(f"=== STEP {idx} ({stype}) ===")
            if stype == "PLANNER_RESPONSE":
                obs = obj.get("tool_calls", [{}])[0].get("args", {}).get("observation", "")
                intent = obj.get("tool_calls", [{}])[0].get("args", {}).get("intention", "")
                print(f"  intent: {intent}")
                print(f"  obs: {obs[:150]}")
            else:
                c = obj.get("content", "")
                if "[WEBVIEW_BROWSER_HUD]" in c:
                    hud_lines = [l.strip() for l in c.split("\n") if "text:" in l or "of 90" in l]
                    print("  HUD lines:", hud_lines[:10])
