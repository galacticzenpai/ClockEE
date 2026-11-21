import os
import json
import re

out_dir = r"C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\browser_sandbox\outputs"

def load_step(s):
    f = os.path.join(out_dir, f"step_{s}.json")
    if os.path.exists(f):
        return json.load(open(f, encoding="utf-8")).get("value", {})
    return {}

v456 = load_step(456)
v458 = load_step(458)
v460 = load_step(460)
v462 = load_step(462)
v464 = load_step(464)
v466 = load_step(466)
v468 = load_step(468)

raw_qs = {
    41: v456.get("step_1"),
    42: v456.get("step_2"),
    43: v456.get("step_3"),
    44: v458.get("step_1"),
    45: v458.get("step_2"),
    46: v458.get("step_3"),
    47: v460.get("step_1"),
    48: v460.get("step_2"),
    49: v460.get("step_3"),
    50: v462.get("step_1"),
    51: v462.get("step_2"),
    52: v462.get("step_3"),
    53: v464.get("step_1"),
    54: v464.get("step_2"),
    55: v464.get("step_3"),
    56: v466.get("step_1"),
    57: v466.get("step_2"),
    58: v466.get("step_3"),
    59: v468.get("q59"),
    60: v468.get("q60")
}

processed = []

for num in range(41, 61):
    q = raw_qs.get(num)
    if not q:
        print(f"Warning: missing Q{num}")
        continue
    
    raw_stmt = q.get("statement", "")
    
    # Extract accuracy percentage
    acc_match = re.search(r"([\d\.]+)%\s*of students got it right", raw_stmt)
    if not acc_match:
        acc_match = re.search(r"([\d\.]+)%\s*overall", raw_stmt)
    accuracy_pct = float(acc_match.group(1)) if acc_match else None
    
    # Extract difficulty
    diff_match = re.search(r"\b(Easy|Medium|Hard)\b", raw_stmt)
    difficulty = diff_match.group(1) if diff_match else "Medium"
    
    # Clean statement
    clean_stmt = raw_stmt
    clean_stmt = re.sub(r"^\d+\s*of\s*90\s*Motion in a Straight Line\s*Leave\s*\d+\s*", "", clean_stmt, flags=re.IGNORECASE).strip()
    clean_stmt = re.sub(r"^Type\s*:\s*(Single|Multiple)\s*Choice\s*Question\s*", "", clean_stmt, flags=re.IGNORECASE).strip()
    
    if "Marked this option" in clean_stmt:
        parts = clean_stmt.split("Marked this option")
        first_part = parts[0]
        clean_stmt = re.sub(r"\n\s*\d+\s*$", "", first_part).strip()
    elif "Solution" in clean_stmt:
        clean_stmt = clean_stmt.split("Solution", 1)[0].strip()
        
    clean_stmt = re.sub(r"^\s*\d+\s*", "", clean_stmt).strip()
    
    # Solution text
    sol_text = q.get("solution_text", "")
    if not sol_text and "Solution" in raw_stmt:
        sol_parts = raw_stmt.split("Solution", 1)
        if len(sol_parts) > 1:
            sol_raw = sol_parts[1]
            sol_raw = re.sub(r"\b(Easy|Medium|Hard)\b", "", sol_raw)
            sol_raw = re.sub(r"Show Video Sol\.", "", sol_raw)
            sol_text = sol_raw.strip()
            
    corr = q.get("correct_option") or q.get("correct_options")
    if isinstance(corr, list):
        corr_list = corr
    elif isinstance(corr, int):
        corr_list = [corr]
    else:
        corr_list = [1]
        
    correct_labels = [chr(ord('A') + idx - 1) for idx in corr_list if 1 <= idx <= 4]
    correct_label_str = ", ".join(correct_labels) if correct_labels else "A"
    
    raw_opts = q.get("options", [])
    clean_opts = []
    
    for opt in raw_opts:
        idx = opt.get("index", 1)
        raw_t = opt.get("raw_text", "")
        parts = [p.strip() for p in raw_t.split("|")]
        pct_val = ""
        opt_text = raw_t
        for p in parts:
            if "Marked this option" in p:
                m = re.search(r"([\d\.]+)%", p)
                if m:
                    pct_val = f"{m.group(1)}%"
            elif p in ["1", "2", "3", "4", "(A)", "(B)", "(C)", "(D)"]:
                pass
            else:
                opt_text = p
                
        if opt_text == raw_t and len(parts) >= 2:
            opt_text = parts[1]
            
        is_corr = (idx in corr_list) or opt.get("is_correct", False)
        clean_opts.append({
            "index": idx,
            "optionText": opt_text.strip(),
            "isCorrect": is_corr,
            "studentPercentage": pct_val
        })
        
    if accuracy_pct is None:
        for opt in clean_opts:
            if opt["isCorrect"] and opt["studentPercentage"]:
                m = re.search(r"([\d\.]+)%", opt["studentPercentage"])
                if m:
                    accuracy_pct = float(m.group(1))
                    break
    if accuracy_pct is None:
        accuracy_pct = 50.0

    q_type = "Multiple Choice" if len(corr_list) > 1 else "Single Choice"

    q_data = {
        "id": f"PW_PHY_MOTION1D_{num:03d}",
        "subject": "Physics",
        "chapter": "Motion in a Straight Line",
        "topic": "Kinematics 1D",
        "questionNumber": num,
        "questionType": q_type,
        "statement": clean_stmt,
        "options": clean_opts,
        "correctOption": correct_label_str,
        "correctAnswer": correct_label_str,
        "accuracy": f"{accuracy_pct:.2f}%",
        "accuracyPct": accuracy_pct,
        "difficulty": difficulty,
        "solutionText": sol_text,
        "videoSolutionUrl": q.get("video_src", ""),
        "source": "PW Infinite Practice",
        "cohort": "Class 11 IIT JEE"
    }
    processed.append(q_data)

print(f"Processed {len(processed)} questions cleanly from Batch 3.")
for p in processed[:3]:
    print(f"--- {p['id']} (Q{p['questionNumber']}) ---")
    print("Statement:", p["statement"][:80])
    print("Correct:", p["correctOption"], "Diff:", p["difficulty"], "Acc:", p["accuracy"])
    print("Options:", [o["optionText"] for o in p["options"]])
    print("Solution:", p["solutionText"][:80])

# Append to pw_extracted_master.json
with open("pw_extracted_master.json", "r", encoding="utf-8") as f:
    master = json.load(f)

existing_ids = set(x.get("id") for x in master)
added_count = 0
for p in processed:
    if p["id"] not in existing_ids:
        master.append(p)
        added_count += 1
    else:
        for i, ex in enumerate(master):
            if ex.get("id") == p["id"]:
                master[i] = p
                break

with open("pw_extracted_master.json", "w", encoding="utf-8") as f:
    json.dump(master, f, indent=2, ensure_ascii=False)

print(f"Successfully appended {added_count} new questions to pw_extracted_master.json!")
print(f"New total in pw_extracted_master.json: {len(master)}")
