import json

with open('pw_extracted_master.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

batch3 = [q for q in data if q.get('id', '').startswith('PW_PHY_MOTION1D_') and int(q['id'].split('_')[-1]) >= 41]
print(f"Total Batch 3 questions found: {len(batch3)}")

with open('scratch_ch3_batch3_dump.txt', 'w', encoding='utf-8') as out:
    for q in batch3:
        out.write('='*70 + '\n')
        out.write(f"ID: {q.get('id')} (Q#{q.get('questionNumber')}): {q.get('statement')}\n")
        out.write(f"Chapter: {q.get('chapter')}, Topic: {q.get('topic')}\n")
        out.write(f"Correct: {q.get('correctAnswer') or q.get('correctOption')}, Accuracy: {q.get('accuracy')}, Diff: {q.get('difficulty')}\n")
        opts = q.get('options') or []
        out.write(f"Options ({len(opts)}):\n")
        for i, opt in enumerate(opts):
            t = opt.get('optionText') if isinstance(opt, dict) else str(opt)
            is_c = opt.get('isCorrect') if isinstance(opt, dict) else None
            pct = opt.get('studentPercentage') if isinstance(opt, dict) else None
            out.write(f"  [{i}] (isCorr={is_c}, pct={pct}): {t}\n")
        out.write(f"Solution: {q.get('solutionText')}\n")

print("Dumped to scratch_ch3_batch3_dump.txt")
