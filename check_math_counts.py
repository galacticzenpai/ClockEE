import json
import collections

with open('cbt_question_bank.json', 'r', encoding='utf-8') as f:
    bank = json.load(f)

maths = [q for q in bank if q.get('subject') in ['Maths', 'Mathematics']]

print(f"Total existing maths: {len(maths)}")
chap_counts = collections.Counter(q.get('chapter') for q in maths)
for c, cnt in sorted(chap_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"{c}: {cnt}")
