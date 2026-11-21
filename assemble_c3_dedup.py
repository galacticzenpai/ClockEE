import os, json, re

p = r'C:\Users\Kunal\.gemini\antigravity\brain\9b7f2b93-6e46-4371-91ca-186d7a6dc5b4\browser_sandbox\outputs'

with open('pw_extracted_master.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

pw_existing = [q for q in master if q.get('chapter') == 'Physical World' or 'PW_PHY_PW' in q.get('id', '') or 'PW_PHY_PHYSICAL_WORLD' in q.get('id', '')]
print(f"Total existing Physical World questions in master: {len(pw_existing)}")

def normalize_text(t):
    return re.sub(r'\s+', ' ', t.strip().lower())

existing_stems = {}
for q in pw_existing:
    s = normalize_text(q.get('statement', ''))
    if s:
        existing_stems[s[:80]] = q.get('id')

# Gather all 63 question objects from step files
q_map = {}

def extract_from_obj(obj, fallback_qnum=None):
    if not isinstance(obj, dict): return
    qnum = obj.get('questionNumber', fallback_qnum)
    if not qnum: return
    q_map[qnum] = obj

# Q1
with open(os.path.join(p, 'step_47.json'), 'r', encoding='utf-8') as f:
    extract_from_obj(json.load(f)['value']['q1Data'], 1)

# Pairs in batchResults
pair_steps = [
    (49, [2, 3]), (51, [4, 5]), (53, [6, 7]), (55, [8, 9]),
    (57, [10, 11]), (59, [12, 13]), (61, [14, 15]), (63, [16, 17]),
    (65, [18, 19]), (67, [20, 21]), (69, [22, 23]), (71, [24, 25]),
    (88, [28, 29]), (100, [30, 31]), (112, [35, 36]), (114, [37, 38]),
    (116, [39, 40]), (118, [41, 42]), (123, [43, 44]), (125, [45, 46]),
    (127, [47, 48]), (129, [49, 50]), (131, [51, 52]), (133, [53, 54]),
    (135, [55, 56]), (137, [57, 58]), (139, [59, 60]), (141, [61, 62])
]

for s, qnums in pair_steps:
    fp = os.path.join(p, f'step_{s}.json')
    if os.path.exists(fp):
        with open(fp, 'r', encoding='utf-8') as f:
            d = json.load(f)
            br = d.get('value', {}).get('batchResults', [])
            for idx, item in enumerate(br):
                qnum = item.get('questionNumber', qnums[idx] if idx < len(qnums) else None)
                extract_from_obj(item, qnum)

# Single step files
single_steps = [
    (184, 26, 'q26'), (186, 27, 'q27'),
    (168, 32, 'q32Data'), (170, 33, 'q33Data'),
    (110, 34, None), (145, 63, 'q63')
]

for s, qnum, key in single_steps:
    fp = os.path.join(p, f'step_{s}.json')
    if os.path.exists(fp):
        with open(fp, 'r', encoding='utf-8') as f:
            val = json.load(f).get('value', {})
            if key and key in val:
                extract_from_obj(val[key], qnum)
            elif isinstance(val, dict):
                # could be directly the question or in a key
                found = False
                for k, v in val.items():
                    if isinstance(v, dict) and ('questionText' in v or 'statement' in v):
                        extract_from_obj(v, qnum)
                        found = True
                        break
                if not found:
                    extract_from_obj(val, qnum)

print(f"Total question objects assembled: {len(q_map)} / 63")
print("Missing question numbers:", [i for i in range(1, 64) if i not in q_map])

new_unique = []
duplicates = []

for qnum in sorted(q_map.keys()):
    obj = q_map[qnum]
    stmt = obj.get('questionText', obj.get('statement', '')).strip()
    stem = normalize_text(stmt)[:80]
    if stem in existing_stems:
        duplicates.append((qnum, existing_stems[stem], stmt[:60]))
    else:
        new_unique.append((qnum, stmt, obj))

print(f"\nCycle 3 Extraction Analysis:")
print(f"  - Duplicates (already in master bank): {len(duplicates)}")
print(f"  - Brand New Unique Questions: {len(new_unique)}")

for n in new_unique:
    print(f"  NEW Q{n[0]}: {repr(n[1][:60])}")
