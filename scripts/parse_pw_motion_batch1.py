import os
import json
import re

out_dir = r"C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\browser_sandbox\outputs"

# Collect all question objects
raw_questions = []

# step_403: q1
f403 = os.path.join(out_dir, "step_403.json")
if os.path.exists(f403):
    d = json.load(open(f403, encoding="utf-8"))
    q = d.get("value", {}).get("q1")
    if q:
        q["questionNumber"] = 1
        raw_questions.append(q)

# step_407: q2, q3
f407 = os.path.join(out_dir, "step_407.json")
if os.path.exists(f407):
    d = json.load(open(f407, encoding="utf-8"))
    v = d.get("value", {})
    if v.get("q2"):
        v["q2"]["questionNumber"] = 2
        raw_questions.append(v["q2"])
    if v.get("q3"):
        v["q3"]["questionNumber"] = 3
        raw_questions.append(v["q3"])

# step_411: q4, q5
f411 = os.path.join(out_dir, "step_411.json")
if os.path.exists(f411):
    d = json.load(open(f411, encoding="utf-8"))
    v = d.get("value", {})
    if v.get("q4"):
        v["q4"]["questionNumber"] = 4
        raw_questions.append(v["q4"])
    if v.get("q5"):
        v["q5"]["questionNumber"] = 5
        raw_questions.append(v["q5"])

# Steps with questions list: 413 (Q6, Q7), 415 (Q8, Q9), 417 (Q10, Q11), 419 (Q12, Q13), 421 (Q14, Q15), 423 (Q16, Q17), 425 (Q18, Q19)
q_counter = 6
for s in [413, 415, 417, 419, 421, 423, 425]:
    fpath = os.path.join(out_dir, f"step_{s}.json")
    if os.path.exists(fpath):
        d = json.load(open(fpath, encoding="utf-8"))
        qs = d.get("value", {}).get("questions", [])
        for q in qs:
            q["questionNumber"] = q_counter
            q_counter += 1
            raw_questions.append(q)

# step_427: q20
f427 = os.path.join(out_dir, "step_427.json")
if os.path.exists(f427):
    d = json.load(open(f427, encoding="utf-8"))
    v = d.get("value", {})
    q20 = v.get("q20") or v.get("question") or v
    if q20:
        q20["questionNumber"] = 20
        raw_questions.append(q20)

print(f"Total raw questions collected: {len(raw_questions)}")

# Now process each raw question into standardized PW format
processed = []
for q in raw_questions:
    num = q.get("questionNumber", 0)
    raw_stmt = q.get("statement", "")
    
    # Extract accuracy percentage if present in statement
    acc_match = re.search(r"([\d\.]+)%\s*of students got it right", raw_stmt)
    accuracy_pct = float(acc_match.group(1)) if acc_match else None
    
    # Extract difficulty
    diff_match = re.search(r"\b(Easy|Medium|Hard)\b", raw_stmt)
    difficulty = diff_match.group(1) if diff_match else "Medium"
    
    # Clean statement: text between "Type : Single Choice Question" and first option or "% Marked this option"
    clean_stmt = raw_stmt
    if "Type : Single Choice Question" in clean_stmt:
        clean_stmt = clean_stmt.split("Type : Single Choice Question", 1)[1]
    
    # Split statement before options start
    # Usually has digits followed by options text
    # Let's clean out options and solution from statement
    if "Marked this option" in clean_stmt:
        parts = clean_stmt.split("Marked this option")
        # First part has statement up to option 1
        first_part = parts[0]
        # Remove trailing option number
        clean_stmt = re.sub(r"\n\s*\d+\s*$", "", first_part).strip()
    elif "Solution" in clean_stmt:
        clean_stmt = clean_stmt.split("Solution", 1)[0].strip()
    
    # Clean leading question number
    clean_stmt = re.sub(r"^\s*\d+\s*", "", clean_stmt).strip()
    
    # Clean solution text
    sol_text = q.get("solution_text", "")
    if not sol_text and "Solution" in raw_stmt:
        sol_parts = raw_stmt.split("Solution", 1)
        if len(sol_parts) > 1:
            sol_raw = sol_parts[1]
            # Strip difficulty and "Show Video Sol."
            sol_raw = re.sub(r"\b(Easy|Medium|Hard)\b", "", sol_raw)
            sol_raw = re.sub(r"Show Video Sol\.", "", sol_raw)
            sol_text = sol_raw.strip()
    
    # Process options
    raw_opts = q.get("options", [])
    clean_opts = []
    correct_idx = q.get("correct_option", 1)
    
    for opt in raw_opts:
        idx = opt.get("index", 1)
        raw_t = opt.get("raw_text", "")
        # raw_text is like: "1 | 5 m/s due south | 15.38% Marked this option"
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
        
        # If opt_text was not isolated
        if opt_text == raw_t and len(parts) >= 2:
            opt_text = parts[1]
            
        is_corr = opt.get("is_correct", False) or (idx == correct_idx)
        clean_opts.append({
            "index": idx,
            "optionText": opt_text.strip(),
            "isCorrect": is_corr,
            "studentPercentage": pct_val
        })
    
    correct_opt_label = chr(ord('A') + correct_idx - 1) if 1 <= correct_idx <= 4 else "A"
    
    q_data = {
        "id": f"PW_PHY_MOTION1D_{num:03d}",
        "subject": "Physics",
        "chapter": "Motion in a Straight Line",
        "topic": "Kinematics 1D",
        "questionNumber": num,
        "statement": clean_stmt,
        "options": clean_opts,
        "correctOption": correct_opt_label,
        "correctAnswer": correct_opt_label,
        "accuracy": f"{accuracy_pct}%" if accuracy_pct is not None else "60.0%",
        "accuracyPct": accuracy_pct if accuracy_pct is not None else 60.0,
        "difficulty": difficulty,
        "solutionText": sol_text,
        "videoSolutionUrl": q.get("video_src", ""),
        "source": "PW Infinite Practice",
        "cohort": "Class 11 IIT JEE"
    }
    processed.append(q_data)

print(f"Processed {len(processed)} questions cleanly.")
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
        # Update existing
        for i, ex in enumerate(master):
            if ex.get("id") == p["id"]:
                master[i] = p
                break

with open("pw_extracted_master.json", "w", encoding="utf-8") as f:
    json.dump(master, f, indent=2, ensure_ascii=False)

print(f"Successfully appended {added_count} new questions to pw_extracted_master.json!")
print(f"New total in pw_extracted_master.json: {len(master)}")
