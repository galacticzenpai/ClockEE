import json

with open('pw_extracted_master.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

pw_phy = [q for q in data if q.get('subject', '').lower() == 'physics' and q.get('chapter') == 'Physical World']
print(f"Total Physical World Qs in master: {len(pw_phy)}")

with open('sorted_physics_questions.json', 'r', encoding='utf-8') as f:
    sorted_qs = json.load(f)

existing_orig_ids = set(q.get('originalId') for q in sorted_qs)
new_qs = [q for q in pw_phy if q.get('id') not in existing_orig_ids]
print(f"New Physical World Qs to integrate: {len(new_qs)}")

for i, q in enumerate(new_qs):
    opts = [o.get('optionText') or o.get('text') for o in q.get('options', [])]
    print(f"{i+21}. ID: {q.get('id')}, Diff: {q.get('difficulty')}, Acc: {q.get('accuracy')}, Ans: {q.get('correctOption')} / {q.get('correctAnswer')}")
    print(f"   Stmt: {q.get('statement')[:80]}...")
    print(f"   Opts: {opts}")
    print(f"   Sol: {q.get('solutionText')}")
