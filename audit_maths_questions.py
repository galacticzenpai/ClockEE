import json
import re

with open('cbt_question_bank.json', 'r', encoding='utf-8') as f:
    bank = json.load(f)

maths = [q for q in bank if q.get('subject') in ['Maths', 'Mathematics']]

print(f"Total Maths questions: {len(maths)}")

# Check options bleeding or irregularities
bleed_count = 0
empty_opts_mcq = 0
wrong_opt_counts = 0
no_correct = 0

for q in maths:
    q_type = q.get('type')
    opts = q.get('options', [])
    if q_type == 'single':
        if not opts:
            empty_opts_mcq += 1
        elif len(opts) != 4:
            wrong_opt_counts += 1
        for opt in opts:
            if isinstance(opt, str) and ('\n' in opt and any(w in opt.lower() for w in ['logarithm', 'chapter', 'answer key', 'hints', 'shift-'])):
                bleed_count += 1
        if 'correct' not in q or q['correct'] is None:
            no_correct += 1

print(f"Bleed-over in options detected: {bleed_count}")
print(f"Empty options in single: {empty_opts_mcq}")
print(f"Single questions with != 4 options: {wrong_opt_counts}")
print(f"Single questions with no correct index: {no_correct}")

# Check numerical questions
no_correct_num = 0
num_with_opts = 0
for q in maths:
    if q.get('type') == 'numerical':
        if 'correctNum' not in q and 'correct' not in q:
            no_correct_num += 1
        if q.get('options') and len(q.get('options')) > 0:
            num_with_opts += 1

print(f"Numerical questions with no correct number: {no_correct_num}")
print(f"Numerical questions with options: {num_with_opts}")
