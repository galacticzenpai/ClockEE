import json, re, os, sys

def parse_units_batch_2(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Split by: **Question XX:**
    blocks = re.split(r'\n(?=\*\*Question\s*\d+:\*\*)', text)
    questions = []

    for block in blocks:
        m_head = re.search(r'\*\*Question\s*(\d+):\*\*', block)
        if not m_head:
            continue
        q_num = int(m_head.group(1))

        # Statement
        m_stmt = re.search(r'-\s*\*\*Statement\*\*:\s*\"?(.*?)\"?(?=\n\s*-\s*\*\*Options\*\*:|\n\s*-\s*\*\*Stats|\Z)', block, re.DOTALL)
        statement = m_stmt.group(1).strip() if m_stmt else ""
        if statement in [".", ""]:
            print(f"Skipping empty question {q_num}")
            continue

        # Options
        # e.g.:
        #   1. Stress — **87.05%** [CORRECT]
        #   2. Strain — **2.41%**
        opt_matches = re.findall(r'(\d+)\.\s*(.*?)(?=\n\s*\d+\.|\n\s*-\s*\*\*Stats|\n\s*\*\*Question|\Z)', block, re.DOTALL)
        opts = []
        correct_opt = None
        for om in opt_matches:
            num = int(om[0])
            raw_text = om[1].strip()
            is_corr = "[CORRECT]" in raw_text
            m_pct = re.search(r'\*\*([\d\.]+)%\*\*', raw_text)
            pct_str = f"{m_pct.group(1)}%" if m_pct else "0%"
            clean_txt = re.sub(r'—\s*\*\*[\d\.]+%\*\*.*', '', raw_text).strip()
            clean_txt = re.sub(r'\[CORRECT\].*', '', clean_txt).strip()
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

        # Video / solution if present
        m_vid = re.search(r'Video solution available:\s*`?(.*?)`?(?:\n|\Z)', block)
        vid_url = m_vid.group(1).strip() if m_vid else ""

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
            "difficulty": "Easy" if q_num in [21, 22, 23, 24, 25, 26, 31, 33, 34, 35, 36, 40] else "Medium",
            "solutionText": f"Option {correct_opt} is the correct answer according to official curriculum standards and dimensional consistency.",
            "videoUrl": vid_url
        }
        questions.append(q_obj)

    print(f"Parsed {len(questions)} valid questions from {txt_path}")
    return questions

if __name__ == "__main__":
    qs = parse_units_batch_2('batch_units_measurements_21_40.txt')
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
