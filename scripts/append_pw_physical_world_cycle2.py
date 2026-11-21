import json, re

with open('pw_physical_world_cycle2_raw.json', 'r', encoding='utf-8') as f:
    c2_raw = json.load(f)

with open('pw_extracted_master.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

pw_existing = [q for q in master if q.get('chapter') == 'Physical World' or 'PW_PHY_PW' in q.get('id', '') or 'PW_PHY_PHYSICAL_WORLD' in q.get('id', '')]

def normalize_text(t):
    return re.sub(r'\s+', ' ', t.strip().lower())

existing_stem_map = {}
for q in pw_existing:
    s = normalize_text(q.get('statement', ''))
    if s:
        existing_stem_map[s[:80]] = q.get('id')

current_highest = 0
for q in pw_existing:
    m = re.search(r'PW_PHY_PHYSICAL_WORLD_(\d+)', q.get('id', ''))
    if m:
        num = int(m.group(1))
        if num > current_highest:
            current_highest = num

print(f"Current highest Physical World ID index: {current_highest}")

opt_letter = {1: 'A', 2: 'B', 3: 'C', 4: 'D'}

new_questions = []

for item in c2_raw:
    q_num = item.get('qNum')
    stmt = item.get('statement', '').strip()
    stem = normalize_text(stmt)[:80]
    
    if stem in existing_stem_map:
        continue  # skip duplicate
        
    current_highest += 1
    new_id = f"PW_PHY_PHYSICAL_WORLD_{current_highest:03d}"
    existing_stem_map[stem] = new_id
    
    raw_opts = item.get('options', [])
    processed_opts = []
    correct_opt_letter = None
    correct_text = ""
    
    for opt in raw_opts:
        idx = opt.get('index', 1)
        letter = opt_letter.get(idx, 'A')
        text = str(opt.get('text', '')).strip()
        pct = opt.get('percentage', '25%')
        is_corr = opt.get('isCorrect', False)
        if is_corr:
            correct_opt_letter = letter
            correct_text = text
        processed_opts.append({
            "id": letter,
            "text": text,
            "percentage": pct if '%' in pct else f"{pct}%",
            "isCorrect": is_corr
        })
        
    if not correct_opt_letter and processed_opts:
        correct_opt_letter = 'A'
        processed_opts[0]['isCorrect'] = True
        correct_text = processed_opts[0]['text']
        
    # Accuracy percentage from correct option
    acc_pct = 40.0
    for o in processed_opts:
        if o['isCorrect']:
            m = re.search(r'([\d\.]+)%', o['percentage'])
            if m:
                acc_pct = float(m.group(1))
            break
            
    diff = "Medium"
    if acc_pct >= 60.0: diff = "Easy"
    elif acc_pct < 35.0: diff = "Hard"
    
    diagram_url = item.get('qImages', [])[0] if item.get('qImages') else ""
    sol_text = item.get('solutionText', '').strip()
    if not sol_text:
        sol_text = f"The correct answer is Option {correct_opt_letter}: {correct_text}."
        
    q_entry = {
        "id": new_id,
        "subject": "Physics",
        "chapter": "Physical World",
        "topic": "Scope & Excitement of Physics",
        "questionNumber": current_highest,
        "questionType": "Single Choice Question",
        "statement": stmt,
        "diagramUrl": diagram_url,
        "options": processed_opts,
        "correctOption": correct_opt_letter,
        "correctAnswer": correct_text,
        "accuracy": f"{acc_pct:.2f}%",
        "accuracyPct": acc_pct,
        "difficulty": diff,
        "solutionText": sol_text,
        "videoSolutionUrl": item.get('videoSrc', ''),
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    }
    new_questions.append(q_entry)

print(f"Generated {len(new_questions)} new unique Physical World questions.")

for q in new_questions:
    master.append(q)

with open('pw_extracted_master.json', 'w', encoding='utf-8') as f:
    json.dump(master, f, indent=2, ensure_ascii=False)

print(f"Updated pw_extracted_master.json! Total questions now: {len(master)}")

with open('pw_physical_world_cycle2_new_only.json', 'w', encoding='utf-8') as f:
    json.dump(new_questions, f, indent=2, ensure_ascii=False)
