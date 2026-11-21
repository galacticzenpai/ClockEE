import os, json, re

p = r'C:\Users\Kunal\.gemini\antigravity\brain\9b7f2b93-6e46-4371-91ca-186d7a6dc5b4\browser_sandbox\outputs'

for s in [47, 49, 184]:
    fp = os.path.join(p, f'step_{s}.json')
    if os.path.exists(fp):
        with open(fp, 'r', encoding='utf-8') as f:
            d = json.load(f)
            val = d.get('value')
            print(f"Step {s} value type: {type(val)}")
            if isinstance(val, list):
                print(f"  list length: {len(val)}")
                if len(val) > 0:
                    print(f"  item 0 keys: {list(val[0].keys())}")
                    print(f"  item 0 stmt: {repr(val[0].get('statement', '')[:60])}")
            elif isinstance(val, dict):
                print(f"  dict keys: {list(val.keys())}")
                print(f"  stmt: {repr(val.get('statement', '')[:60])}")
