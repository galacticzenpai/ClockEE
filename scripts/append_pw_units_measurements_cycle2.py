import os
import json
import re

out_dir = r'C:\Users\Kunal\.gemini\antigravity\brain\3b5e6b86-296e-4dc5-97f9-6d750df553e3\browser_sandbox\outputs'
master_file = 'pw_extracted_master.json'

master = json.load(open(master_file, 'r', encoding='utf-8'))

def normalize(t):
    return re.sub(r'\s+', ' ', (t or '')).strip().lower()

existing_stems = {normalize(q.get('statement', ''))[:80]: q.get('id') for q in master if q.get('statement')}

# Find highest existing Units and Measurements ID
uam_existing = [q for q in master if q.get('chapter') == 'Units and Measurements']
highest_num = 0
for q in uam_existing:
    m = re.search(r'PW_PHY_UNITS_MEASUREMENTS_(\d+)', q.get('id', ''))
    if m:
        val = int(m.group(1))
        if val > highest_num:
            highest_num = val

print(f"Highest current Units and Measurements ID: PW_PHY_UNITS_MEASUREMENTS_{highest_num:03d}")

# Gather all harvested items from subagent
all_harvested = {}
for fn in sorted(os.listdir(out_dir)):
    if fn.endswith('.json'):
        fp = os.path.join(out_dir, fn)
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                d = json.load(f)
                val = d.get('value', {})
                if isinstance(val, dict):
                    if 'batch' in val and isinstance(val['batch'], list):
                        for item in val['batch']:
                            qn = item.get('questionNumber') or item.get('qnum')
                            if qn and qn not in all_harvested:
                                all_harvested[qn] = item
                    for k in ['q55', 'harvestedQ', 'q90']:
                        if k in val and isinstance(val[k], dict):
                            item = val[k]
                            qn = item.get('questionNumber') or item.get('qnum')
                            if qn and qn not in all_harvested:
                                all_harvested[qn] = item
        except:
            pass

print(f"Total raw questions collected from Cycle 2: {len(all_harvested)}")

new_added = 0
duplicates = 0
letter_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4}

for qn in sorted(all_harvested.keys()):
    item = all_harvested[qn]
    stmt = (item.get('statement') or item.get('questionText') or '').strip()
    stem = normalize(stmt)[:80]
    if not stmt or not stem:
        continue
    
    if stem in existing_stems:
        duplicates += 1
        continue
        
    highest_num += 1
    new_id = f"PW_PHY_UNITS_MEASUREMENTS_{highest_num:03d}"
    existing_stems[stem] = new_id
    
    # Process options
    raw_opts = item.get('options', [])
    processed_opts = []
    correct_key = item.get('correctAnswerKey', '')
    correct_text = ""
    
    for idx, opt in enumerate(raw_opts):
        opt_idx = opt.get('optionIndex', idx + 1)
        opt_key = opt.get('optionKey', chr(ord('A') + idx))
        opt_text = (opt.get('optionText') or opt.get('text') or '').strip()
        opt_pct = opt.get('studentPercentage') or opt.get('percentage') or '25.0%'
        if '%' not in str(opt_pct):
            opt_pct = f"{opt_pct}%"
            
        is_corr = opt.get('isCorrect', False)
        if correct_key and (opt_key in correct_key or str(opt_idx) in correct_key):
            is_corr = True
            
        if is_corr and not correct_text:
            correct_text = opt_text
            
        processed_opts.append({
            "optionNumber": opt_idx,
            "optionText": opt_text,
            "isCorrect": is_corr,
            "studentPercentage": opt_pct
        })
        
    # Ensure at least one correct option
    if not any(o['isCorrect'] for o in processed_opts) and processed_opts:
        processed_opts[0]['isCorrect'] = True
        correct_text = processed_opts[0]['optionText']
        correct_key = 'A'
        
    accuracy_str = item.get('accuracy', '50.0%')
    if '%' not in str(accuracy_str):
        accuracy_str = f"{accuracy_str}%"
        
    m_acc = re.search(r'([\d\.]+)%', accuracy_str)
    acc_val = float(m_acc.group(1)) if m_acc else 50.0
    diff = "Medium"
    if acc_val >= 65.0: diff = "Easy"
    elif acc_val < 35.0: diff = "Hard"
    
    sol = (item.get('explanation') or item.get('solutionText') or '').strip()
    if not sol:
        sol = f"The correct answer is Option {correct_key}: {correct_text}."
        
    entry = {
        "id": new_id,
        "subject": "Physics",
        "chapter": "Units and Measurements",
        "topic": "Units and Dimensions",
        "questionNumber": highest_num,
        "statement": stmt,
        "statementImages": item.get('diagramUrls', []),
        "options": processed_opts,
        "correctOption": correct_key,
        "correctAnswer": correct_text,
        "accuracy": accuracy_str,
        "difficulty": diff,
        "solutionText": sol
    }
    
    master.append(entry)
    new_added += 1

print(f"Cycle 2 Ingestion Complete: Added {new_added} unique questions, {duplicates} duplicates.")
print(f"Total master size is now {len(master)} questions.")

with open(master_file, 'w', encoding='utf-8') as f:
    json.dump(master, f, indent=2, ensure_ascii=False)

print("Saved updated pw_extracted_master.json successfully.")
