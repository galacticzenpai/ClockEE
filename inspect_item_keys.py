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

print("Step 859 item 0 keys:", list(results[859][0].keys()))
for k in results[859][0].keys():
    v = str(results[859][0][k])
    if len(v) > 100: v = v[:100] + '...'
    print(f"  {k}: {repr(v)}")

print("\nStep 886 keys:", list(results[886].keys()))
for k in results[886].keys():
    v = str(results[886][k])
    if len(v) > 100: v = v[:100] + '...'
    print(f"  {k}: {repr(v)}")
