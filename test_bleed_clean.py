import json
import re

with open('cbt_question_bank.json', 'r', encoding='utf-8') as f:
    bank = json.load(f)

maths = [q for q in bank if q.get('subject') in ['Maths', 'Mathematics']]

bleed_samples = []
for q in maths:
    opts = q.get('options', [])
    for opt in opts:
        if isinstance(opt, str) and ('\n' in opt and any(w in opt.lower() for w in ['logarithm', 'chapter', 'answer key', 'hints', 'shift-'])):
            bleed_samples.append((q['id'], opt))

print(f"Found {len(bleed_samples)} bleed samples:")
for qid, opt in bleed_samples[:5]:
    print(f"\nQID: {qid}")
    print("Raw opt:", repr(opt)[:120])
    # Test cleaning
    cleaned = re.split(r'\n(?=[A-Z][a-z]+|\d+\.|\bANSWER KEY\b)', opt)[0].strip()
    print("Cleaned opt:", repr(cleaned))
