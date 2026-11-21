import os, glob, json

output_dir = r'C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\browser_sandbox\outputs'
step_files = sorted(glob.glob(os.path.join(output_dir, 'step_*.json')), key=lambda x: int(os.path.basename(x).split('_')[1].split('.')[0]))

print(f"Total steps: {len(step_files)}")
for sf in step_files[-10:]:
    num = int(os.path.basename(sf).split('_')[1].split('.')[0])
    try:
        with open(sf, 'r', encoding='utf-8') as f:
            d = json.load(f)
        val = d.get('value')
        vsummary = list(val.keys()) if isinstance(val, dict) else (f"list({len(val)})" if isinstance(val, list) else str(type(val)))
        print(f"step_{num}: ok={d.get('ok')}, err={d.get('error')}, val={vsummary}")
        if isinstance(val, dict):
            for k in val:
                sub = val[k]
                if isinstance(sub, dict) and 'quesText' in sub:
                    print(f"   {k}: {sub['quesText'][:60]}... [opts: {len(sub.get('options', []))}]")
                elif k == 'quesText':
                    print(f"   quesText: {val['quesText'][:60]}... [opts: {len(val.get('options', []))}]")
    except Exception as e:
        print(f"step_{num}: {e}")
