import json
import collections

with open('cbt_question_bank.json', 'r', encoding='utf-8') as f:
    bank = json.load(f)

maths = [q for q in bank if q.get('subject') in ['Maths', 'Mathematics']]

print(f"Total Maths Questions: {len(maths)}")

# Inspect keys
keys_freq = collections.Counter()
for q in maths:
    for k in q.keys():
        keys_freq[k] += 1
print("\nKeys frequency:")
for k, count in keys_freq.items():
    print(f"  {k}: {count}")

# Inspect question types
type_freq = collections.Counter(q.get('type') for q in maths)
print("\nTypes:")
for t, count in type_freq.items():
    print(f"  {t}: {count}")

# Inspect difficulty
diff_freq = collections.Counter(q.get('difficulty') for q in maths)
print("\nDifficulties:")
for d, count in diff_freq.items():
    print(f"  {d}: {count}")

# Check options length and numerical answers
opt_lens = collections.Counter()
for q in maths:
    if q.get('type') == 'single':
        opts = q.get('options')
        opt_lens[len(opts) if isinstance(opts, list) else 'not_list'] += 1
print("\nOption lengths for 'single':", opt_lens)

# Check samples of single and numerical
single_sample = next((q for q in maths if q.get('type') == 'single'), None)
num_sample = next((q for q in maths if q.get('type') == 'numerical'), None)

print("\n--- SAMPLE SINGLE ---")
if single_sample:
    for k, v in single_sample.items():
        print(f"{k}: {repr(v)[:150]}")

print("\n--- SAMPLE NUMERICAL ---")
if num_sample:
    for k, v in num_sample.items():
        print(f"{k}: {repr(v)[:150]}")
