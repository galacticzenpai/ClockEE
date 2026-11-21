import os, glob, json, re

output_dir = r'C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\browser_sandbox\outputs'

# Scan all step files from step 525 to 600
all_qs = {}

step_files = sorted(glob.glob(os.path.join(output_dir, 'step_*.json')), key=lambda x: int(os.path.basename(x).split('_')[1].split('.')[0]))

for sf in step_files:
    num = int(os.path.basename(sf).split('_')[1].split('.')[0])
    if num < 525:
        continue
    try:
        with open(sf, 'r', encoding='utf-8') as f:
            d = json.load(f)
        val = d.get('value')
        if not val:
            continue
        # Check if step_526 format (direct question dict)
        if isinstance(val, dict) and 'quesText' in val and 'options' in val:
            # Q1
            all_qs['q1'] = val
        elif isinstance(val, dict):
            for k, v in val.items():
                if isinstance(v, dict) and 'quesText' in v:
                    all_qs[k] = v
        elif isinstance(val, list):
            # Check step_532 (list of 2 questions Q4 and Q5) or step_546 (Q10 and Q11)
            if num == 532:
                all_qs['q4'] = val[0]
                all_qs['q5'] = val[1]
            elif num == 546:
                all_qs['q10'] = val[0]
                all_qs['q11'] = val[1]
            else:
                for idx, item in enumerate(val):
                    all_qs[f'step_{num}_{idx}'] = item
    except Exception as e:
        print(f"Error reading {sf}: {e}")

print(f"Total questions mapped in all_qs: {len(all_qs)}")
for k in sorted(all_qs.keys(), key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 999):
    q = all_qs[k]
    qtext = q.get('quesText', '')[:60].replace('\n', ' ')
    opts = len(q.get('options', []))
    correct = [i for i, o in enumerate(q.get('options', [])) if o.get('isCorrect')]
    print(f"{k}: opts={opts}, correct={correct}, text={qtext}")
