import json, re

with open('pw_physical_world_cycle2_raw.json', 'r', encoding='utf-8') as f:
    c2_raw = json.load(f)

with open('pw_extracted_master.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

# Collect existing statements/IDs for Physical World
pw_existing = [q for q in master if q.get('chapter') == 'Physical World' or 'PW_PHY_PW' in q.get('id', '')]
print(f"Existing Physical World questions in master: {len(pw_existing)}")

def normalize_text(t):
    return re.sub(r'\s+', ' ', t.strip().lower())

existing_stmt_map = {}
for q in pw_existing:
    s = normalize_text(q.get('statement', ''))
    if s:
        existing_stmt_map[s[:80]] = q.get('id')

print(f"Existing unique Physical World statement stems: {len(existing_stmt_map)}")

new_unique_c2 = []
duplicate_c2 = []

opt_letters = {1: 'A', 2: 'B', 3: 'C', 4: 'D'}

for item in c2_raw:
    q_num = item.get('qNum')
    stmt = item.get('statement', '')
    stem = normalize_text(stmt)[:80]
    
    if stem in existing_stmt_map:
        duplicate_c2.append((q_num, existing_stmt_map[stem], stmt[:50]))
    else:
        new_unique_c2.append(item)

print(f"\nCycle 2 Results for Physical World (out of 63 questions):")
print(f"  - Duplicate (already captured in Cycle 1): {len(duplicate_c2)}")
print(f"  - Brand New Unique Questions: {len(new_unique_c2)}")

print("\nSample duplicates found:")
for d in duplicate_c2[:5]:
    print(f"  Q{d[0]} matches existing {d[1]}: {repr(d[2])}")

print("\nSample new unique questions:")
for n in new_unique_c2[:5]:
    print(f"  Q{n.get('qNum')}: {repr(n.get('statement')[:60])}")
