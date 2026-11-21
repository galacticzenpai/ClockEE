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

print('Detailed breakdown of parsed values:')
total_items = 0
for s in steps:
    val = results.get(s)
    if isinstance(val, list):
        print(f'Step {s} (list of {len(val)}):')
        for idx, item in enumerate(val):
            opt = item.get('correctOpt')
            header = item.get('headerText', '').replace('\n', ' ')
            qtext = item.get('qText', '')[:60].replace('\n', ' ')
            print(f'   [{idx}] correctOpt={opt}, header="{header}", qText="{qtext}"')
            total_items += 1
    elif isinstance(val, dict):
        print(f'Step {s} (dict keys: {list(val.keys())}):')
        for k, v in val.items():
            if isinstance(v, dict):
                opt = v.get('correctOpt')
                header = v.get('headerText', '').replace('\n', ' ')
                qtext = v.get('qText', '')[:60].replace('\n', ' ')
                print(f'   {k}: correctOpt={opt}, header="{header}", qText="{qtext}"')
                total_items += 1
print(f'Total questions parsed: {total_items}')
