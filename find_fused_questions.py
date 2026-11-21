import json
import re

with open('cbt_question_bank.json', 'r', encoding='utf-8') as f:
    bank = json.load(f)

maths = [q for q in bank if q.get('subject') in ['Maths', 'Mathematics']]

fused_questions = []

for q in maths:
    opts = q.get('options', [])
    for opt_idx, opt in enumerate(opts):
        if not isinstance(opt, str):
            continue
        # Look for pattern of a question header inside the option
        m = re.search(r'\n\s*(\d+)\.\s+([A-Z].*?)(?=\n\s*(?:\([a-d1-4]\)|\[|\bANSWER|\Z))', opt, re.DOTALL)
        if m:
            qnum = m.group(1)
            qtext = m.group(2).strip()
            # Check if options are present inside opt after qtext
            tail = opt[m.start():]
            inner_opts = re.findall(r'\(([a-d1-4])\)\s*([^(\n]+(?:\n[^(\n]+)*)', tail)
            fused_questions.append({
                'parent_id': q['id'],
                'parent_chapter': q['chapter'],
                'extracted_num': int(qnum),
                'text': qtext,
                'tail': tail[:200]
            })

print(f"Total fused questions found: {len(fused_questions)}")
for f in fused_questions:
    print(f"Parent {f['parent_id']} -> Q#{f['extracted_num']} in {f['parent_chapter']}: {f['text'][:80]}...")
