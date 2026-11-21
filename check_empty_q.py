import os, json

p = r'C:\Users\Kunal\.gemini\antigravity\brain\9b7f2b93-6e46-4371-91ca-186d7a6dc5b4\browser_sandbox\outputs'

for s, qnum in [(184, 26), (186, 27), (168, 32), (170, 33)]:
    with open(os.path.join(p, f'step_{s}.json'), 'r', encoding='utf-8') as f:
        d = json.load(f)
        val = d.get('value', {})
        print(f"Step {s} (Q{qnum}) value keys: {list(val.keys()) if isinstance(val, dict) else type(val)}")
        print(f"  preview: {str(val)[:200]}")
