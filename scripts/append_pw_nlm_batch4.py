import json, re

with open('b4_extracted_clean.json', 'r', encoding='utf-8') as f:
    raw_b4 = json.load(f)

with open('pw_extracted_master.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

existing_ids = {q.get('id') for q in master if q.get('id')}

topic_map = {
    61: ("Tension in Hanging Heavy Rope", "Laws of Motion"),
    62: ("Apparent Weight & Normal Reaction in Lift", "Laws of Motion"),
    63: ("Impulse from Force-Time Graph", "Laws of Motion"),
    64: ("Free Body Diagram of Leaning Rod", "Laws of Motion"),
    65: ("Two-Block System & Friction Threshold", "Laws of Motion"),
    66: ("Maximum Force for Accelerating Block System", "Laws of Motion"),
    67: ("Tension in Accelerated String Systems", "Laws of Motion"),
    68: ("Movable Pulley Dynamic Acceleration", "Laws of Motion"),
    69: ("Stacked Coins Normal Contact Forces", "Laws of Motion"),
    70: ("Direction of Friction Force on Moving Athlete", "Laws of Motion"),
    71: ("Normal Reaction in Accelerating Elevator", "Laws of Motion"),
    72: ("Three Connected Masses & String Tensions", "Laws of Motion"),
    73: ("Spring Force vs String Cut Accelerations", "Laws of Motion"),
    74: ("Horizontal Table & Hanging Block Acceleration", "Laws of Motion"),
    75: ("Kinematics & Acceleration of Block System", "Laws of Motion"),
    76: ("Static & Kinetic Friction Threshold", "Laws of Motion"),
    77: ("Limiting Friction & External Pull", "Laws of Motion"),
    78: ("Pulley System String Tension", "Laws of Motion"),
    79: ("Kinematic Constraint of Interconnected Blocks", "Laws of Motion"),
    80: ("Equilibrium State & Net Unbalanced Force", "Laws of Motion"),
    81: ("Equilibrium of Light String with Suspended Weights", "Laws of Motion"),
    82: ("Kinematics under Time-Varying Force Vector", "Laws of Motion"),
    83: ("Coupled Masses Friction & Minimum Force to Hold", "Laws of Motion"),
    84: ("Contact Force between Accelerating Adjacent Blocks", "Laws of Motion"),
    85: ("Dynamometer Reading between Two Accelerated Blocks", "Laws of Motion"),
    86: ("Equilibrium Position in Rotating Hemispherical Bowl", "Circular Dynamics"),
    87: ("Acceleration from 3D Force Vector on Mass", "Laws of Motion"),
    88: ("Impulse & Average Force during Ball Impact", "Laws of Motion"),
    89: ("Equilibrium & Acceleration on Smooth Incline", "Laws of Motion"),
    90: ("Tension in Connected Mass System on Incline", "Laws of Motion")
}

new_b4_questions = []

opt_letter = {1: 'A', 2: 'B', 3: 'C', 4: 'D', '1': 'A', '2': 'B', '3': 'C', '4': 'D'}

for qnum_str in sorted(raw_b4.keys(), key=lambda x: int(x)):
    qnum = int(qnum_str)
    raw = raw_b4[qnum_str]
    qid = f"PW_PHY_NLM_{qnum:03d}"
    
    # Clean statement: remove question number and "Type : Single Choice Question"
    raw_stmt = raw.get('statement', '')
    lines = [line.strip() for line in raw_stmt.split('\n') if line.strip()]
    cleaned_lines = []
    for line in lines:
        if line == str(qnum) or line.startswith(f"{qnum} ·") or line.startswith(f"{qnum}."):
            continue
        if "Type : Single Choice Question" in line or "Single Choice Question" in line:
            continue
        cleaned_lines.append(line)
    clean_statement = " ".join(cleaned_lines).strip()
    if not clean_statement:
        clean_statement = raw_stmt.strip()
    
    # Process options
    raw_opts = raw.get('options', [])
    processed_opts = []
    correct_opt_letter = None
    correct_text = ""
    
    # If correctOpt is specified directly (1-based index)
    target_correct_idx = raw.get('correctOpt')
    
    for idx, opt in enumerate(raw_opts):
        idx_1 = idx + 1
        letter = opt_letter.get(idx_1, 'A')
        text = str(opt.get('text', '')).strip()
        pct = opt.get('percentage', '25%')
        if 'Marked this option' in pct:
            pct = pct.replace('Marked this option', '').strip()
        is_corr = opt.get('is_correct', False)
        if target_correct_idx and idx_1 == int(target_correct_idx):
            is_corr = True
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
        correct_opt_letter = opt_letter.get(target_correct_idx, 'A') if target_correct_idx else 'A'
        for o in processed_opts:
            if o['id'] == correct_opt_letter:
                o['isCorrect'] = True
                correct_text = o['text']
                
    # Extract solution text
    sol_raw = raw.get('solutionText', [])
    if isinstance(sol_raw, list):
        sol_text = " ".join([str(s).replace('\n', ' ') for s in sol_raw]).strip()
    else:
        sol_text = str(sol_raw).strip()
    # remove leading Solution Medium/Easy/Hard tags
    sol_text = re.sub(r'^(Solution\s*(Easy|Medium|Hard)?\s*(Show Video Sol\.)?\s*)', '', sol_text).strip()
    
    # Extract images
    imgs = raw.get('images', [])
    diagram_url = imgs[0] if imgs else ""
    
    # Extract video
    vid = raw.get('iframeSrc', '')
    
    topic_name, chapter_name = topic_map.get(qnum, ("Laws of Motion", "Laws of Motion"))
    
    # Accuracy estimation from correct option percentage
    acc_pct = 40.0
    for o in processed_opts:
        if o['isCorrect']:
            m = re.search(r'([\d\.]+)%', o['percentage'])
            if m:
                acc_pct = float(m.group(1))
            break
            
    diff = "Medium"
    if acc_pct >= 55.0: diff = "Easy"
    elif acc_pct < 35.0: diff = "Hard"
    
    q_entry = {
        "id": qid,
        "subject": "Physics",
        "chapter": "Laws of Motion",
        "topic": topic_name,
        "questionNumber": qnum,
        "questionType": "Single Choice Question",
        "statement": clean_statement,
        "diagramUrl": diagram_url,
        "options": processed_opts,
        "correctOption": correct_opt_letter,
        "correctAnswer": correct_text,
        "accuracy": f"{acc_pct:.2f}%",
        "accuracyPct": acc_pct,
        "difficulty": diff,
        "solutionText": sol_text,
        "videoSolutionUrl": vid,
        "source": "PW Infinite Practice - Class 11 Physics",
        "cohort": "Class 11 JEE"
    }
    new_b4_questions.append(q_entry)

print(f"Constructed {len(new_b4_questions)} standardized questions for Batch 4.")

added_count = 0
for q in new_b4_questions:
    if q['id'] not in existing_ids:
        master.append(q)
        existing_ids.add(q['id'])
        added_count += 1

with open('pw_extracted_master.json', 'w', encoding='utf-8') as f:
    json.dump(master, f, indent=2, ensure_ascii=False)

print(f"Appended {added_count} questions to pw_extracted_master.json. Total count now: {len(master)}")

with open('batch4_nlm_clean.json', 'w', encoding='utf-8') as f:
    json.dump(new_b4_questions, f, indent=2, ensure_ascii=False)
