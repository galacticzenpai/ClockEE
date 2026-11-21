import os, json

p = r'C:\Users\Kunal\.gemini\antigravity\brain\9b7f2b93-6e46-4371-91ca-186d7a6dc5b4\browser_sandbox\outputs'

with open(os.path.join(p, 'step_47.json'), 'r', encoding='utf-8') as f:
    d = json.load(f)
    print("Step 47 q1Data keys:", list(d['value']['q1Data'].keys()))
    print("Step 47 q1Data statement:", repr(d['value']['q1Data'].get('statement', '')[:100]))

with open(os.path.join(p, 'step_49.json'), 'r', encoding='utf-8') as f:
    d = json.load(f)
    print("Step 49 batchResults keys/items:", len(d['value']['batchResults']))
    print("Step 49 batchResults[0] keys:", list(d['value']['batchResults'][0].keys()))
    print("Step 49 batchResults[0] statement:", repr(d['value']['batchResults'][0].get('statement', '')[:100]))
