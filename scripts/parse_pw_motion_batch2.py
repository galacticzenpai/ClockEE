import os
import json
import re

out_dir = r"C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\browser_sandbox\outputs"

# Mapping questions to their canonical step files
# Q21, Q22: step_436
# Q23, Q24, Q25: step_438
# Q26, Q27, Q28: step_440
# Q29, Q30, Q31: step_442
# Q32: step_444 ('q32')
# Q33, Q34, Q35: step_446 ('q33', 'q34', 'q35')
# Q36, Q37, Q38: step_448 ('step_1', 'step_2', 'step_3')
# Q39, Q40: step_450 ('q39', 'q40')

raw_qs = {}

def load_step(s):
    f = os.path.join(out_dir, f"step_{s}.json")
    if os.path.exists(f):
        return json.load(open(f, encoding="utf-8")).get("value", {})
    return {}

v436 = load_step(436)
raw_qs[21] = v436.get("step_1")
raw_qs[22] = v436.get("step_2")

v438 = load_step(438)
raw_qs[23] = v438.get("step_1")
raw_qs[24] = v438.get("step_2")
raw_qs[25] = v438.get("step_3")

v440 = load_step(440)
raw_qs[26] = v440.get("step_1")
raw_qs[27] = v440.get("step_2")
raw_qs[28] = v440.get("step_3")

v442 = load_step(442)
raw_qs[29] = v442.get("step_1")
raw_qs[30] = v442.get("step_2")
raw_qs[31] = v442.get("step_3")

v444 = load_step(444)
raw_qs[32] = v444.get("q32")

v446 = load_step(446)
raw_qs[33] = v446.get("q33")
raw_qs[34] = v446.get("q34")
raw_qs[35] = v446.get("q35")

v448 = load_step(448)
raw_qs[36] = v448.get("step_1")
raw_qs[37] = v448.get("step_2")
raw_qs[38] = v448.get("step_3")

v450 = load_step(450)
raw_qs[39] = v450.get("q39")
raw_qs[40] = v450.get("q40")

processed = []

for num in range(21, 41):
    q = raw_qs.get(num)
    if not q:
        print(f"Warning: missing Q{num}")
        continue
    
    raw_stmt = q.get("statement", "")
    
    # Extract accuracy percentage if present in statement or options
    acc_match = re.search(r"([\d\.]+)%\s*of students got it right", raw_stmt)
    if not acc_match:
        acc_match = re.search(r"([\d\.]+)%\s*overall", raw_stmt)
    accuracy_pct = float(acc_match.group(1)) if acc_match else None
    
    # Extract difficulty
    diff_match = re.search(r"\b(Easy|Medium|Hard)\b", raw_stmt)
    difficulty = diff_match.group(1) if diff_match else "Medium"
    
    # Clean statement: remove header "XX of 90Motion in a Straight Line\nLeave\nXX\nType : Single Choice Question"
    clean_stmt = raw_stmt
    clean_stmt = re.sub(r"^\d+\s*of\s*90\s*Motion in a Straight Line\s*Leave\s*\d+\s*", "", clean_stmt, flags=re.IGNORECASE).strip()
    clean_stmt = re.sub(r"^Type\s*:\s*(Single|Multiple)\s*Choice\s*Question\s*", "", clean_stmt, flags=re.IGNORECASE).strip()
    
    # Remove options and footer from statement
    if "Marked this option" in clean_stmt:
        parts = clean_stmt.split("Marked this option")
        first_part = parts[0]
        clean_stmt = re.sub(r"\n\s*\d+\s*$", "", first_part).strip()
    elif "Solution" in clean_stmt:
        clean_stmt = clean_stmt.split("Solution", 1)[0].strip()
        
    # Clean leading question numbers
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
            
    # Correct option
    corr = q.get("correct_option") or q.get("correct_options")
    if isinstance(corr, list):
        corr_list = corr
    elif isinstance(corr, int):
        corr_list = [corr]
    else:
        corr_list = [1]
        
    correct_labels = [chr(ord('A') + idx - 1) for idx in corr_list if 1 <= idx <= 4]
    correct_label_str = ", ".join(correct_labels) if correct_labels else "A"
    
    # Clean options
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
        
    # If accuracy_pct is still None, take the max percentage marked on the correct option
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

print(f"Processed {len(processed)} questions cleanly from Batch 2.")
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
