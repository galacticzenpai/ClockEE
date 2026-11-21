import json

transcript_path = r'C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\.system_generated\logs\transcript.jsonl'
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        idx = obj.get("step_index")
        if idx and idx >= 550:
            stype = obj.get("type")
            if stype == "PLANNER_RESPONSE":
                print(f"\n--- STEP {idx} (PLANNER_RESPONSE) ---")
                thinking = obj.get("thinking", "")
                if "Q14" in thinking or "Q15" in thinking or "Q16" in thinking:
                    for line_t in thinking.split("\n"):
                        if any(q in line_t for q in ["Q14", "Q15", "Q16", "swimmer", "obstacle", "angle"]):
                            print(f"  [think] {line_t}")
                for tc in obj.get("tool_calls", []):
                    args = tc.get("args", {})
                    print(f"  tool_call: {tc.get('name')} | intent: {args.get('intention')}")
                    if "script" in args:
                        s = args["script"]
                        if "extract" in s:
                            # print first 2 lines
                            lines_s = [l.strip() for l in s.split("\\n") if l.strip()][:3]
                            print(f"    script snippet: {lines_s}")
