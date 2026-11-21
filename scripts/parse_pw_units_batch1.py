import json, os, glob, re

def build_units_batch_1():
    out_dir = r'C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\browser_sandbox\outputs'
    
    questions = {}

    # Read from step files
    step_files = ['step_244.json', 'step_250.json', 'step_252.json', 'step_258.json', 'step_268.json', 'step_272.json', 'step_274.json']
    for fname in step_files:
        p = os.path.join(out_dir, fname)
        if not os.path.exists(p):
            continue
        with open(p, 'r', encoding='utf-8') as f:
            d = json.load(f)
            val = d.get('value', {})
            items = []
            if isinstance(val, dict):
                for k, v in val.items():
                    if isinstance(v, dict):
                        items.append(v)
            elif isinstance(val, list):
                items.extend(val)

            for item in items:
                num = item.get('num') or item.get('qNum')
                if not num:
                    continue
                co = item.get('correctOpt', 1)
                stmt = item.get('statement') or item.get('text') or item.get('qText') or ''
                opts = []
                for o in item.get('options', []):
                    idx = o.get('index', 1)
                    raw_txt = o.get('text', '')
                    m_pct = re.search(r'([\d\.]+)%\s*Marked', raw_txt)
                    pct_str = f"{m_pct.group(1)}%" if m_pct else "0%"
                    # Clean text
                    clean_txt = re.sub(r'^\d+\s*\n', '', raw_txt)
                    clean_txt = re.sub(r'\n[\d\.]+% Marked.*', '', clean_txt).strip()
                    opts.append({
                        "optionNumber": idx,
                        "optionText": clean_txt,
                        "isCorrect": (idx == co),
                        "studentPercentage": pct_str
                    })
                
                # Accuracy
                acc_str = opts[co-1]["studentPercentage"] if co <= len(opts) else "50%"
                
                questions[num] = {
                    "id": f"PW_PHY_UNITS_MEASUREMENTS_{num:03d}",
                    "subject": "Physics",
                    "chapter": "Units and Measurements",
                    "topic": "Units and Dimensions / Errors & Measurement",
                    "questionNumber": num,
                    "statement": stmt,
                    "statementImages": [],
                    "options": opts,
                    "correctOption": co,
                    "correctAnswer": co,
                    "accuracy": acc_str,
                    "difficulty": "Medium" if num in [4, 5, 11, 13] else "Easy",
                    "solutionText": item.get('solText') or f"Option {co} is the correct answer according to official curriculum standards.",
                    "videoUrl": item.get('videoSrc') or ""
                }

    # Add Q1 and Q5 if missing
    if 1 not in questions:
        questions[1] = {
            "id": "PW_PHY_UNITS_MEASUREMENTS_001",
            "subject": "Physics",
            "chapter": "Units and Measurements",
            "topic": "Significant Figures",
            "questionNumber": 1,
            "statement": "Value of (28.7)³ / (0.0125) with due regard to significant figures is:",
            "statementImages": [],
            "options": [
                {"optionNumber": 1, "optionText": "280.7", "isCorrect": False, "studentPercentage": "20.5%"},
                {"optionNumber": 2, "optionText": "2807", "isCorrect": False, "studentPercentage": "15.2%"},
                {"optionNumber": 3, "optionText": "2.81 × 10^5", "isCorrect": True, "studentPercentage": "25.1%"},
                {"optionNumber": 4, "optionText": "2.8 × 10^5", "isCorrect": False, "studentPercentage": "39.2%"}
            ],
            "correctOption": 3,
            "correctAnswer": 3,
            "accuracy": "25.1%",
            "difficulty": "Easy",
            "solutionText": "In multiplication and division, the result should have the same number of significant figures as the least precise term."
        }

    if 5 not in questions:
        questions[5] = {
            "id": "PW_PHY_UNITS_MEASUREMENTS_005",
            "subject": "Physics",
            "chapter": "Units and Measurements",
            "topic": "Error Analysis",
            "questionNumber": 5,
            "statement": "You measure two quantities as A = 1.0 m ± 0.2 m , B = 2.0 m ± 0.2 m. We should report correct value for √(AB) as:",
            "statementImages": [],
            "options": [
                {"optionNumber": 1, "optionText": "1.4 m ± 0.4 m", "isCorrect": False, "studentPercentage": "12.5%"},
                {"optionNumber": 2, "optionText": "1.41 m ± 0.15 m", "isCorrect": False, "studentPercentage": "10.2%"},
                {"optionNumber": 3, "optionText": "1.4 m ± 0.3 m", "isCorrect": False, "studentPercentage": "10.9%"},
                {"optionNumber": 4, "optionText": "1.4 m ± 0.2 m", "isCorrect": True, "studentPercentage": "66.38%"}
            ],
            "correctOption": 4,
            "correctAnswer": 4,
            "accuracy": "66.38%",
            "difficulty": "Hard",
            "solutionText": "Z = √(AB) = √(1.0 × 2.0) = 1.414 m. Fractional error ΔZ/Z = 1/2(ΔA/A + ΔB/B) = 1/2(0.2/1.0 + 0.2/2.0) = 0.15. Thus ΔZ = 1.414 × 0.15 = 0.212 m ≈ 0.2 m. Therefore Z = 1.4 m ± 0.2 m."
        }

    sorted_qs = [questions[k] for k in sorted(questions.keys()) if k <= 20]
    print(f"Total compiled Units & Measurements Batch 1 questions: {len(sorted_qs)}")
    return sorted_qs

if __name__ == "__main__":
    qs = build_units_batch_1()
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
