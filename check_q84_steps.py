import json

with open(r'C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        s = obj.get('step_index')
        if s in [888, 889, 890, 891]:
            print(f'=== STEP {s} ({obj.get("type")}) ===')
            c = obj.get('content', '')
            if c:
                print(c[:400].replace('\n', ' '))
