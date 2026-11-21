import json

steps = [859, 861, 863, 865, 867, 869, 871, 873, 875, 877, 879, 886, 892, 894, 896]
results = {}

with open(r'C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\.system_generated\logs\transcript_full.jsonl', 'r', encoding='utf-8') as f:
    for line in f:
        obj = json.loads(line)
        s = obj.get('step_index')
        if s in steps:
            c = obj.get('content', '')
            pos = c.find(f'[Browser Step {s}]\n')
            if pos != -1:
                pos += len(f'[Browser Step {s}]\n')
                end = c.find('\n\n[WEBVIEW_BROWSER_HUD]', pos)
                if end == -1: end = len(c)
                raw = c[pos:end].strip()
                d = json.loads(raw, strict=False)
                results[s] = d.get('value')

all_q_objs = []
for s in steps:
    val = results.get(s)
    if isinstance(val, list):
        for idx, item in enumerate(val):
            all_q_objs.append((s, idx, item))
    elif isinstance(val, dict):
        if 'statement' in val:
            all_q_objs.append((s, 0, val))
        else:
            for k, v in val.items():
                if isinstance(v, dict):
                    all_q_objs.append((s, k, v))

print(f"Total question objects gathered: {len(all_q_objs)}")
for i, (s, k, item) in enumerate(all_q_objs):
    stmt = item.get('statement', '')
    first_line = stmt.split('\n')[0] if stmt else 'EMPTY'
    second_line = stmt.split('\n')[2] if len(stmt.split('\n')) > 2 else ''
    print(f"Q-Index {i+1}: from Step {s}[{k}] -> Statement Head: {repr(first_line)} | {repr(second_line[:50])}")
