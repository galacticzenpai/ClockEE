import json
from collections import Counter

with open("cbt_question_bank.json", "r", encoding="utf-8") as f:
    bank = json.load(f)

chem_qs = [q for q in bank if q.get("subject") == "Chemistry"]
print(f"Total chemistry questions: {len(chem_qs)}")

chapter_counts = Counter(q.get("chapter", "None") for q in chem_qs)
print("\n--- Chapter Distribution ---")
for ch, count in sorted(chapter_counts.items(), key=lambda x: -x[1]):
    print(f"  {ch}: {count}")

diff_counts = Counter(q.get("difficulty", "None") for q in chem_qs)
print("\n--- Difficulty Distribution ---")
for d, count in diff_counts.items():
    print(f"  {d}: {count}")

types = Counter(q.get("type", "None") for q in chem_qs)
print("\n--- Type Distribution ---")
for t, count in types.items():
    print(f"  {t}: {count}")

# Check sample question
print("\n--- Sample Question ---")
print(json.dumps(chem_qs[0], indent=2)[:800])
