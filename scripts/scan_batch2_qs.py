import os, glob, json, re

output_dir = r'C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\browser_sandbox\outputs'

all_qs = {}
step_files = sorted(glob.glob(os.path.join(output_dir, 'step_*.json')), key=lambda x: int(os.path.basename(x).split('_')[1].split('.')[0]))

for sf in step_files:
    num = int(os.path.basename(sf).split('_')[1].split('.')[0])
    if num < 575:
        continue
    try:
        with open(sf, 'r', encoding='utf-8') as f:
            d = json.load(f)
        val = d.get('value')
        if not val:
            continue
        if isinstance(val, dict):
            for k, v in val.items():
                if isinstance(v, dict) and ('quesText' in v or 'options' in v):
                    all_qs[k] = v
                elif k == 'quesText':
                    all_qs[f'step_{num}'] = val
        elif isinstance(val, list):
            for idx, item in enumerate(val):
                if isinstance(item, dict) and ('quesText' in item or 'options' in item):
                    all_qs[f'step_{num}_{idx}'] = item
    except Exception as e:
        pass

print(f"Total question entries found in range 575..: {len(all_qs)}")
for k in sorted(all_qs.keys()):
    q = all_qs[k]
    qtext = q.get('quesText', '')[:60].replace('\n', ' ')
    opts = len(q.get('options', []))
    correct = [i for i, o in enumerate(q.get('options', [])) if o.get('isCorrect')]
    print(f"{k}: opts={opts}, correct={correct}, text={qtext}")
