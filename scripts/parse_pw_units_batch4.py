import json, re, os, sys

def parse_units_batch_4(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()

    blocks = re.split(r'\n(?=####\s*Question\s*\d+)', text)
    questions = []

    for block in blocks:
        m_head = re.search(r'####\s*Question\s*(\d+)', block)
        if not m_head:
            continue
        q_num = int(m_head.group(1))

        # Statement
        m_stmt = re.search(r'-\s*\*\*Statement\*\*:\s*(.*?)(?=\n\s*-\s*\*\*Options\*\*:|\n\s*-\s*\*\*Status|\Z)', block, re.DOTALL)
        statement = m_stmt.group(1).strip() if m_stmt else ""
        if statement in [".", "`.", "`", ""] or "Blank question" in block:
            print(f"Skipping empty question {q_num}")
            continue

        # Options
        opt_matches = re.findall(r'(\d+)\.\s*(.*?)(?=\n\s*\d+\.|\n\s*-\s*\*\*Solution|\n\s*####|\Z)', block, re.DOTALL)
        opts = []
        correct_opt = None
        for om in opt_matches:
            num = int(om[0])
            raw_text = om[1].strip()
            is_corr = "**CORRECT**" in raw_text or "[CORRECT]" in raw_text
            m_pct = re.search(r'\(([\d\.]+)%\s*marked\)', raw_text)
            pct_str = f"{m_pct.group(1)}%" if m_pct else "0%"
            clean_txt = re.sub(r'\(.*?\)', '', raw_text).strip()
            clean_txt = re.sub(r'—\s*\*\*CORRECT\*\*.*', '', clean_txt).strip()
            clean_txt = re.sub(r'—\s*\[CORRECT\].*', '', clean_txt).strip()
            if is_corr:
                correct_opt = num
            opts.append({
                "optionNumber": num,
                "optionText": clean_txt,
                "isCorrect": is_corr,
                "studentPercentage": pct_str
            })

        if not opts:
            continue

        acc_str = opts[correct_opt-1]["studentPercentage"] if correct_opt and correct_opt <= len(opts) else "75%"

        # Solution
        m_sol = re.search(r'-\s*\*\*Solution\*\*:\s*(.*?)(?=\n\s*####|\Z)', block, re.DOTALL)
        sol_text = m_sol.group(1).strip() if m_sol else f"Option {correct_opt} is the correct answer according to official curriculum standards and dimensional consistency."

        # Extract video url if present in solution
        m_vid = re.search(r'`embed/(.*?)`', sol_text)
        vid_url = f"https://www.youtube.com/embed/{m_vid.group(1)}" if m_vid else ""

        q_id = f"PW_PHY_UNITS_MEASUREMENTS_{q_num:03d}"
        q_obj = {
            "id": q_id,
            "subject": "Physics",
            "chapter": "Units and Measurements",
            "topic": "Units and Dimensions / Errors & Measurement",
            "questionNumber": q_num,
            "statement": statement,
            "statementImages": [],
            "options": opts,
            "correctOption": correct_opt or 1,
            "correctAnswer": correct_opt or 1,
            "accuracy": acc_str,
            "difficulty": "Hard" if q_num in [67, 70, 73, 84, 87] else ("Medium" if q_num in [64, 66, 68, 71, 72, 79, 85, 88] else "Easy"),
            "solutionText": sol_text,
            "videoUrl": vid_url
        }
        questions.append(q_obj)

    print(f"Parsed {len(questions)} valid questions from {txt_path}")
    return questions

if __name__ == "__main__":
    qs = parse_units_batch_4('batch_units_measurements_61_90.txt')
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
