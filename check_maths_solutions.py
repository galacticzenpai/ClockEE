import json

with open('cbt_question_bank.json', 'r', encoding='utf-8') as f:
    bank = json.load(f)

maths = [q for q in bank if q.get('subject') in ['Maths', 'Mathematics']]

has_sol = sum(1 for q in maths if 'solution' in q and q['solution'])
print(f"Total Maths: {len(maths)}, with solution: {has_sol}")
