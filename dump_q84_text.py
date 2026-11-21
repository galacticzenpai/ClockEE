import json

with open(r'C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        if obj.get('step_index') == 888:
            c = obj.get('content', '')
            pos = c.find('Two blocks of masses')
            end = c.find('36.66% of students got it right', pos)
            print(c[pos:end+60])
