import os
import json
import re
from collections import Counter, defaultdict

def validate_all():
    print("=" * 70)
    print("=== CBT MASTER BANK & QUESTION LOG VERIFICATION AUDIT ===")
    print("=" * 70)

    # 1. Check Files Existence
    files = [
        'cbt_question_bank.json',
        'cbt_master_bank.js',
        'cbt_book_log.json',
        'cbt_question_log_report.json',
        'cbt_home.html',
        'cbt_exam.html',
        'cbt_analysis.html',
        'scripts/cbt-engine.js'
    ]
    for fn in files:
        assert os.path.exists(fn), f"Missing required file: {fn}"
        size_kb = os.path.getsize(fn) / 1024
        print(f"✓ File exists: {fn:<30} ({size_kb:>8.1f} KB)")

    # 2. Parse Question Bank
    with open('cbt_question_bank.json', 'r', encoding='utf-8') as f:
        bank = json.load(f)
    print(f"\n✓ Successfully parsed `cbt_question_bank.json`: {len(bank)} questions")

    # 3. Parse Book Log
    with open('cbt_book_log.json', 'r', encoding='utf-8') as f:
        book_log = json.load(f)
    print(f"✓ Successfully parsed `cbt_book_log.json`: {len(book_log)} reference books")

    # 4. Parse Question Log Report
    with open('cbt_question_log_report.json', 'r', encoding='utf-8') as f:
        report = json.load(f)
    print(f"✓ Successfully parsed `cbt_question_log_report.json`")

    # 5. Validate Master Bank JS
    with open('cbt_master_bank.js', 'r', encoding='utf-8') as f:
        js_txt = f.read()
    assert "window.CBT_MASTER_QUESTION_BANK =" in js_txt, "window.CBT_MASTER_QUESTION_BANK missing in JS payload"
    assert "window.CBT_BOOK_LOG =" in js_txt, "window.CBT_BOOK_LOG missing in JS payload"
    print("✓ Successfully validated `cbt_master_bank.js` window globals structure")

    # 6. Deep Schema & Integrity Validation
    seen_ids = set()
    subject_counts = Counter()
    section_counts = Counter()
    type_counts = Counter()
    diff_counts = Counter()
    source_counts = Counter()
    chapter_counts = defaultdict(Counter)
    topic_counts = defaultdict(Counter)
    accuracies = []
    ideal_times = []

    for idx, q in enumerate(bank):
        qid = q.get('id')
        assert qid, f"Question at index {idx} has missing id"
        assert qid not in seen_ids, f"Duplicate ID collision: {qid}"
        seen_ids.add(qid)

        sub = q.get('subject')
        sub_short = q.get('subjectShort')
        assert sub in ['Physics', 'Chemistry', 'Mathematics'], f"Invalid subject: {sub}"
        assert sub_short in ['Physics', 'Chemistry', 'Maths'], f"Invalid subjectShort: {sub_short}"
        subject_counts[sub_short] += 1

        sec = q.get('section')
        assert sec in ['A', 'B'], f"Invalid section: {sec} in {qid}"
        section_counts[sec] += 1

        q_type = q.get('type')
        assert q_type in ['MCQ', 'NUMERICAL'], f"Invalid type: {q_type} in {qid}"
        type_counts[q_type] += 1

        diff = q.get('difficulty')
        assert diff in ['Easy', 'Medium', 'Hard'], f"Invalid difficulty: {diff} in {qid}"
        diff_counts[diff] += 1

        time_sec = q.get('idealTimeSec')
        assert isinstance(time_sec, int) and time_sec > 0, f"Invalid idealTimeSec in {qid}"
        ideal_times.append(time_sec)

        acc = q.get('accuracyPct')
        assert isinstance(acc, (int, float)) and 0.0 <= acc <= 100.0, f"Invalid accuracyPct in {qid}"
        accuracies.append(acc)

        text = q.get('text', '')
        assert len(text) > 5, f"Empty text in {qid}"

        marking = q.get('marking', {})
        assert marking.get('correct') == 4, f"Invalid marking.correct in {qid}"
        if sec == 'A':
            assert marking.get('wrong') == -1, f"Invalid marking.wrong for Sec A in {qid}"
            opts = q.get('options', [])
            assert len(opts) == 4, f"Section A question must have 4 options in {qid}"
            for oi, opt in enumerate(opts):
                assert opt.get('id') == chr(65 + oi), f"Option ID must be {chr(65+oi)} in {qid}"
                assert 'text' in opt, f"Option text missing in {qid}"
            opts_txt = q.get('optionsText', [])
            assert len(opts_txt) == 4, f"optionsText must have 4 items in {qid}"
            c = q.get('correct')
            assert c in [0, 1, 2, 3], f"Invalid correct index in {qid}"
            assert q.get('correctAnswer') == chr(65 + c), f"correctAnswer mismatch in {qid}"
        else:
            assert marking.get('wrong') == 0, f"Invalid marking.wrong for Sec B in {qid}"
            c_num = q.get('correctNum')
            assert isinstance(c_num, (int, float)), f"Invalid correctNum in {qid}"
            assert q.get('correctAnswer') is not None, f"correctAnswer missing in Sec B {qid}"

        sol = q.get('solution', '')
        assert len(sol) > 10, f"Solution missing or too short in {qid}"

        ref = q.get('referenceBook', '')
        assert len(ref) > 3, f"Reference book missing in {qid}"

        src = q.get('examSource', '')
        assert src in ['JEE Main PYQs', 'JEE Advanced PYQs', 'HC Verma Concepts of Physics', 'Physics Wallah Infinite Practice'], f"Invalid examSource: {src} in {qid}"
        source_counts[src] += 1

        ch = q.get('chapter', 'General')
        top = q.get('topic', 'General')
        chapter_counts[sub_short][ch] += 1
        topic_counts[sub_short][top] += 1

    print("\n--- 100% SCHEMA VALIDATION PASSED ---")
    print(f"Total Verified Questions: {len(bank)}")
    print(f"Unique Question IDs: {len(seen_ids)}")
    print(f"\n[Subject Breakdown]:")
    for s, c in subject_counts.items():
        print(f"  - {s:<15}: {c:>5} Qs ({c/len(bank)*100:.1f}%)")
    print(f"\n[Section & Type Breakdown]:")
    for sec, c in section_counts.items():
        print(f"  - Section {sec} ({'MCQ Single Choice' if sec=='A' else 'Numerical NAT'}): {c:>5} Qs ({c/len(bank)*100:.1f}%)")
    print(f"\n[Difficulty Breakdown]:")
    for d, c in diff_counts.items():
        print(f"  - {d:<15}: {c:>5} Qs ({c/len(bank)*100:.1f}%)")
    print(f"\n[Exam Source Breakdown]:")
    for src, c in source_counts.items():
        print(f"  - {src:<35}: {c:>5} Qs ({c/len(bank)*100:.1f}%)")
    print(f"\n[Accuracy Stats]:")
    print(f"  - Overall Average Accuracy : {sum(accuracies)/len(accuracies):.2f}%")
    print(f"  - Min / Max Accuracy       : {min(accuracies):.1f}% / {max(accuracies):.1f}%")
    print(f"\n[Time Stats]:")
    print(f"  - Average Ideal Time       : {sum(ideal_times)/len(ideal_times):.1f}s ({sum(ideal_times)/len(ideal_times)/60:.1f} min)")

    print(f"\n[Chapter Breadth]:")
    for sub, chs in chapter_counts.items():
        print(f"  - {sub}: {len(chs)} chapters, {len(topic_counts[sub])} micro-topics")

    # 7. Check Book Ledger Consistency
    total_book_qs = sum(b['totalQuestions'] for b in book_log)
    assert total_book_qs == len(bank), f"Book ledger total ({total_book_qs}) != bank total ({len(bank)})"
    print(f"\n✓ Book Ledger question count perfectly matches master bank: {total_book_qs} questions")

    print("\n==================================================================")
    print("=== ALL AUDIT CHECKS PASSED: MASTER CBT SUITE READY FOR PROD ===")
    print("==================================================================")

if __name__ == '__main__':
    validate_all()
