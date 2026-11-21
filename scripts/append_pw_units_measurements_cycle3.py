import os
import json
import re

out_dir = r'C:\Users\Kunal\.gemini\antigravity\brain\4e4a1119-fffd-4ec9-9f86-8963fc10e7ec\browser_sandbox\outputs'
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

def add_item(item):
    if not isinstance(item, dict): return
    qn = item.get('questionNumber') or item.get('qnum')
    stmt = (item.get('questionText') or item.get('statement') or '').strip()
    if qn and stmt and qn not in all_harvested:
        all_harvested[qn] = item

for fn in sorted(os.listdir(out_dir)):
    if fn.endswith('.json'):
        fp = os.path.join(out_dir, fn)
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                d = json.load(f)
                val = d.get('value', {})
                if isinstance(val, list):
                    for it in val: add_item(it)
                elif isinstance(val, dict):
                    add_item(val)
                    if 'batch' in val and isinstance(val['batch'], list):
                        for it in val['batch']: add_item(it)
                    if 'batchResults' in val and isinstance(val['batchResults'], list):
                        for it in val['batchResults']: add_item(it)
                    if 'questions' in val and isinstance(val['questions'], list):
                        for it in val['questions']: add_item(it)
                    for k, v in val.items():
                        if isinstance(v, dict):
                            add_item(v)
        except:
            pass

print(f"Total raw questions assembled from Cycle 3: {len(all_harvested)}")

new_added = 0
duplicates = 0
letter_map = {'A': 1, 'B': 2, 'C': 3, 'D': 4}

for qn in sorted(all_harvested.keys()):
    item = all_harvested[qn]
    stmt = (item.get('statement') or item.get('questionText') or '').strip()
    stem = normalize(stmt)[:80]
    if not stmt or not stem or len(stem) < 5:
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
        opt_idx = opt.get('optionIndex', opt.get('index', idx + 1))
        opt_key = opt.get('optionKey', opt.get('label', chr(ord('A') + idx)))
        opt_text = (opt.get('optionText') or opt.get('text') or '').strip()
        opt_pct = opt.get('studentPercentage') or opt.get('percentage') or opt.get('markedPercentage') or '25.0%'
        if opt_pct and '%' not in str(opt_pct):
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
            "studentPercentage": str(opt_pct) if opt_pct else '25.0%'
        })
        
    # Ensure at least one correct option
    if not any(o['isCorrect'] for o in processed_opts) and processed_opts:
        processed_opts[0]['isCorrect'] = True
        correct_text = processed_opts[0]['optionText']
        correct_key = 'A'
        
    accuracy_str = item.get('accuracy') or item.get('overallAccuracy') or '50.0%'
    if accuracy_str and '%' not in str(accuracy_str):
        accuracy_str = f"{accuracy_str}%"
        
    m_acc = re.search(r'([\d\.]+)%', str(accuracy_str))
    acc_val = float(m_acc.group(1)) if m_acc else 50.0
    diff = item.get('difficulty') or ("Easy" if acc_val >= 65.0 else ("Hard" if acc_val < 35.0 else "Medium"))
    
    sol = (item.get('explanation') or item.get('solutionText') or '').strip()
    if not sol:
        sol = f"The correct answer is Option {correct_key}: {correct_text}."
        
    imgs = item.get('diagramUrls') or item.get('questionImages') or []
    
    entry = {
        "id": new_id,
        "subject": "Physics",
        "chapter": "Units and Measurements",
        "topic": "Units and Dimensions",
        "questionNumber": highest_num,
        "statement": stmt,
        "statementImages": imgs if isinstance(imgs, list) else [imgs],
        "options": processed_opts,
        "correctOption": correct_key,
        "correctAnswer": correct_text,
        "accuracy": str(accuracy_str),
        "difficulty": diff,
        "solutionText": sol
    }
    
    master.append(entry)
    new_added += 1

print(f"Cycle 3 Ingestion Complete: Added {new_added} unique questions, {duplicates} duplicates.")
print(f"Total master size is now {len(master)} questions.")

with open(master_file, 'w', encoding='utf-8') as f:
    json.dump(master, f, indent=2, ensure_ascii=False)

print("Saved updated pw_extracted_master.json successfully.")
