import json

with open('pw_extracted_master.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

with open('sorted_physics_questions.json', 'r', encoding='utf-8') as f:
    sorted_qs = json.load(f)

existing_orig_ids = set(q.get('originalId') for q in sorted_qs)
new_qs = [q for q in master if q.get('subject', '').lower() == 'physics' and q.get('id') not in existing_orig_ids]

print(f"Total Physics in master: {len([q for q in master if q.get('subject', '').lower() == 'physics'])}")
print(f"Existing in sorted: {len(sorted_qs)}")
print(f"New to add: {len(new_qs)}")

for i, q in enumerate(new_qs):
    opts = [o.get('optionText') or o.get('text') for o in q.get('options', [])]
    print(f"\n--- Q{i+61}: ID={q.get('id')}, Ch={q.get('chapter')} (Diff={q.get('difficulty')}, Acc={q.get('accuracy')}) ---")
    print(f"Stmt: {q.get('statement')}")
    print(f"Opts: {opts}")
    print(f"CorrectOption: {q.get('correctOption')}, CorrectAnswer: {q.get('correctAnswer')}")
    print(f"Sol: {q.get('solutionText')}")
