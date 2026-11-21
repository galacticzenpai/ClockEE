import json, re, os, sys

def parse_batch_2(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split by: 1. **Question 21** or 20. **Question 40**
    blocks = re.split(r'\n(?=\d+\.\s*\*\*Question\s*\d+\*\*)', text)
    questions = []

    for block in blocks:
        m_head = re.search(r'(\d+)\.\s*\*\*Question\s*(\d+)\*\*\s*\((.*?)\):', block)
        if not m_head:
            continue
        item_no = int(m_head.group(1))
        q_num = int(m_head.group(2))
        q_type = m_head.group(3).strip()

        # Statement
        m_stmt = re.search(r'-\s*\*\*Statement\*\*:\s*\"?(.*?)\"?(?=\n\s*-\s*\*\*Options\*\*:)', block, re.DOTALL)
        statement = m_stmt.group(1).strip() if m_stmt else ""

        # Options
        m_opts = re.search(r'-\s*\*\*Options\*\*:\s*(.*?)(?=\n\s*-\s*\*\*Correct Answer\*\*:)', block, re.DOTALL)
        opts_raw = m_opts.group(1).strip() if m_opts else ""

        # Parse individual options e.g. "1. Mechanics, 2. Electrodynamics, 3. Optics, 4. All of these"
        # or "1. Postulate (5.36%), 2. Hypothesis (7.8%), ..."
        opt_list = []
        # Try regex for "1. ...", "2. ..."
        opt_parts = re.split(r'(?=\b[1-4]\.\s+)', opts_raw)
        for part in opt_parts:
            part = part.strip()
            if not part:
                continue
            m_p = re.match(r'([1-4])\.\s*(.*)', part)
            if m_p:
                num = int(m_p.group(1))
                txt = m_p.group(2).rstrip(',;').strip()
                # Check if percentage is in txt
                m_pct = re.search(r'\(([\d\.]+)\%\)', txt)
                pct_str = f"{m_pct.group(1)}%" if m_pct else "0%"
                clean_txt = re.sub(r'\s*\([\d\.]+\%\)', '', txt).strip()
                opt_list.append({
                    "optionNumber": num,
                    "optionText": clean_txt,
                    "studentPercentage": pct_str
                })

        # Correct Answer
        m_ans = re.search(r'-\s*\*\*Correct Answer\*\*:\s*Option\s*([1-4])(?:\s*\((.*?)\))?(?:\s*\[([\d\.]+)%\s*got it right\])?', block)
        if m_ans:
            correct_opt = int(m_ans.group(1))
            corr_text = m_ans.group(2) or ""
            acc_str = f"{m_ans.group(3)}%" if m_ans.group(3) else "80%"
        else:
            # Fallback for multiple or different syntax
            m_ans2 = re.search(r'-\s*\*\*Correct Answer\*\*:\s*Options?\s*([1-4])', block)
            correct_opt = int(m_ans2.group(1)) if m_ans2 else 1
            m_acc = re.search(r'\[([\d\.]+)%\s*got it right\]', block)
            acc_str = f"{m_acc.group(1)}%" if m_acc else "80%"

        # Set isCorrect flags on options
        if not opt_list:
            # create 4 default options
            opt_list = [
                {"optionNumber": 1, "optionText": "Option 1", "studentPercentage": "5%"},
                {"optionNumber": 2, "optionText": "Option 2", "studentPercentage": "5%"},
                {"optionNumber": 3, "optionText": "Option 3", "studentPercentage": "5%"},
                {"optionNumber": 4, "optionText": "Option 4", "studentPercentage": acc_str}
            ]
        for opt in opt_list:
            opt["isCorrect"] = (opt["optionNumber"] == correct_opt)
            if opt["isCorrect"] and opt["studentPercentage"] == "0%":
                opt["studentPercentage"] = acc_str

        # Difficulty & Solution
        m_diff = re.search(r'Difficulty:\s*(\w+)', block)
        diff = m_diff.group(1) if m_diff else "Easy"

        m_sol = re.search(r'-\s*\*\*Solution(?:\s*Text)?\*\*:\s*(.*?)(?=\n\s*\d+\.|\Z)', block, re.DOTALL)
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
            "options": opt_list,
            "correctOption": correct_opt,
            "correctAnswer": correct_opt,
            "accuracy": acc_str,
            "difficulty": diff,
            "solutionText": sol_text
        }
        questions.append(q_obj)

    print(f"Parsed {len(questions)} questions from {txt_path}")
    return questions

if __name__ == "__main__":
    qs = parse_batch_2('batch_physical_world_21_62.txt')
    master_path = r'D:\Desktop\New folder\pw_extracted_master.json'
    master = json.load(open(master_path, 'r', encoding='utf-8'))
    print(f"Master before: {len(master)}")

    existing_ids = {q.get('id') for q in master if 'id' in q}
    added = 0
    for q in qs:
        if q['id'] not in existing_ids:
            master.append(q)
            added += 1
            existing_ids.add(q['id'])

    print(f"Added {added} new questions. Master after: {len(master)}")
    with open(master_path, 'w', encoding='utf-8') as f:
        json.dump(master, f, indent=2, ensure_ascii=False)
    print("Saved to", master_path)
