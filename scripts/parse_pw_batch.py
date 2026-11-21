import json, re, os, sys

def parse_batch_text(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split by numbered questions: e.g. "1. **Q1" or "2. **Q2"
    q_blocks = re.split(r'\n(?=\d+\.\s*\*\*Q\d+)', text)
    if len(q_blocks) <= 1:
        # Try alternate split
        q_blocks = re.split(r'(?=\b\d+\.\s*\*\*Q\d+)', text)

    questions = []
    for block in q_blocks:
        m_head = re.search(r'(\d+)\.\s*\*\*Q(\d+)\s*\((.*?)\)\*\*:\s*(.*?)(?=\n\s*-\s*Opt|\n\s*-\s*\*\*Opt)', block, re.DOTALL)
        if not m_head:
            continue
        item_no = int(m_head.group(1))
        q_num = int(m_head.group(2))
        q_type_diff = m_head.group(3).strip()
        statement = m_head.group(4).strip()

        # Parse difficulty
        diff = "Medium"
        if "Easy" in q_type_diff:
            diff = "Easy"
        elif "Hard" in q_type_diff:
            diff = "Hard"

        # Parse options
        # e.g. - Opt 1: French word 'Scientia' (2.52%)
        # or - **Opt 4 [CORRECT]**: Latin word 'Scientia', which means 'to know' (78.47%)
        opt_matches = re.findall(r'-\s*(\*\*)?Opt\s*(\d+)(\s*\[CORRECT\])?(\*\*)?:\s*(.*?)(?=\n\s*-\s*Opt|\n\s*-\s*\*\*Opt|\n\s*-\s*\*Stats\*|\n\s*-\s*Solution:|\Z)', block, re.DOTALL)
        options = []
        correct_opt = None
        for om in opt_matches:
            is_corr = bool(om[2])
            opt_idx = int(om[1])
            raw_opt_text = om[4].strip()
            # extract percentage if at end: e.g. (78.47%)
            m_pct = re.search(r'\(([\d\.]+)\%\)\s*$', raw_opt_text)
            pct_str = f"{m_pct.group(1)}%" if m_pct else "0%"
            clean_opt_text = re.sub(r'\s*\([\d\.]+\%\)\s*$', '', raw_opt_text).strip()
            if is_corr:
                correct_opt = opt_idx
            options.append({
                "optionNumber": opt_idx,
                "optionText": clean_opt_text,
                "isCorrect": is_corr,
                "studentPercentage": pct_str
            })

        # Accuracy
        m_stats = re.search(r'\*Stats\*:\s*([\d\.]+)%', block)
        acc_str = f"{m_stats.group(1)}%" if m_stats else (options[correct_opt-1]["studentPercentage"] if correct_opt and len(options)>=correct_opt else "50%")

        # Solution
        m_sol = re.search(r'Solution:\s*(.*?)(?=\n\s*-\s*Video|\n\d+\.|\Z)', block, re.DOTALL)
        sol_text = m_sol.group(1).strip() if m_sol else f"Option {correct_opt} is the correct answer according to official curriculum standards."

        q_id = f"PW_PHY_PHYSICAL_WORLD_{q_num:03d}"
        q_obj = {
            "id": q_id,
            "subject": "Physics",
            "chapter": "Physical World",
            "topic": "Physical World / Scope and Nature of Physical Laws",
            "questionNumber": q_num,
            "statement": statement,
            "statementImages": [],
            "options": options,
            "correctOption": correct_opt or 1,
            "correctAnswer": correct_opt or 1,
            "accuracy": acc_str,
            "difficulty": diff,
            "solutionText": sol_text
        }
        questions.append(q_obj)

    print(f"Successfully parsed {len(questions)} questions from {txt_path}")
    return questions

if __name__ == "__main__":
    txt_path = sys.argv[1] if len(sys.argv) > 1 else 'batch_physical_world_1_20.txt'
    qs = parse_batch_text(txt_path)
    
    master_path = r'D:\Desktop\New folder\pw_extracted_master.json'
    master = json.load(open(master_path, 'r', encoding='utf-8'))
    print(f"Master before: {len(master)}")
    
    # Avoid duplicate IDs
    existing_ids = {q.get('id') for q in master if 'id' in q}
    added = 0
    for q in qs:
        if q['id'] not in existing_ids:
            master.append(q)
            added += 1
            existing_ids.add(q['id'])
    
    print(f"Added: {added} new questions. Master after: {len(master)}")
    with open(master_path, 'w', encoding='utf-8') as f:
        json.dump(master, f, indent=2, ensure_ascii=False)
    print("Saved to", master_path)
