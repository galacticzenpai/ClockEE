import os
import json
import re
from collections import Counter, defaultdict

def load_json_safe(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict):
                # if wrapped in a key
                for k in ['questions', 'data', 'items']:
                    if k in data and isinstance(data[k], list):
                        return data[k]
                return list(data.values())
        except Exception as e:
            print(f"Error loading {filepath}: {e}")
    return []

def normalize_difficulty(diff):
    if not diff:
        return "Moderate"
    d = str(diff).strip().capitalize()
    if d in ["Easy", "Simple"]:
        return "Easy"
    elif d in ["Hard", "Tough", "Difficult"]:
        return "Tough"
    else:
        return "Moderate"

def normalize_subject(sub):
    if not sub:
        return "Physics"
    s = str(sub).strip().capitalize()
    if "physic" in s.lower():
        return "Physics"
    elif "chem" in s.lower():
        return "Chemistry"
    elif "math" in s.lower():
        return "Maths"
    return s

def normalize_question(q, fallback_subject="Physics", idx=0):
    norm = dict(q)
    
    # Subject
    sub = normalize_subject(norm.get("subject", fallback_subject))
    norm["subject"] = sub
    
    # ID
    qid = norm.get("id")
    if not qid:
        ch_slug = re.sub(r'[^a-zA-Z0-9]+', '_', norm.get("chapter", "gen").lower()).strip('_')
        qid = f"gen_{sub.lower()[:3]}_{ch_slug}_{idx:05d}"
        norm["id"] = qid
        
    # Chapter & Topic
    norm["chapter"] = norm.get("chapter", "General").strip()
    norm["topic"] = norm.get("topic", norm["chapter"]).strip()
    
    # Type
    q_type = norm.get("type", "single")
    if q_type not in ["single", "numerical"]:
        # check if options exist
        if norm.get("options") and len(norm.get("options")) >= 2:
            q_type = "single"
        else:
            q_type = "numerical"
    norm["type"] = q_type
    
    # Difficulty
    norm["difficulty"] = normalize_difficulty(norm.get("difficulty"))
    
    # Ideal time
    if "idealTimeSec" not in norm or not isinstance(norm["idealTimeSec"], (int, float)):
        if sub == "Chemistry":
            norm["idealTimeSec"] = 60
        elif sub == "Maths":
            norm["idealTimeSec"] = 120
        else:
            norm["idealTimeSec"] = 90
            
    # Text
    norm["text"] = norm.get("text", "").strip()
    
    # Options
    if q_type == "single":
        opts = norm.get("options", [])
        if not isinstance(opts, list):
            opts = []
        # ensure 4 options
        while len(opts) < 4:
            opts.append(f"Option {chr(65+len(opts))}")
        norm["options"] = opts
        # correct index
        c = norm.get("correct", 0)
        try:
            c = int(c)
            if c < 0 or c >= len(opts):
                c = 0
        except:
            c = 0
        norm["correct"] = c
    else:
        norm["options"] = []
        c_num = norm.get("correctNum", norm.get("correct", 0.0))
        try:
            c_num = float(c_num)
        except:
            c_num = 0.0
        norm["correctNum"] = c_num
        
    # Marking
    if "marking" not in norm or not isinstance(norm["marking"], dict):
        norm["marking"] = {"correct": 4, "wrong": -1 if q_type == "single" else 0}
    else:
        if q_type == "numerical" and norm["marking"].get("wrong", 0) != 0:
            norm["marking"]["wrong"] = 0
            
    # Source / Reference
    ref = norm.get("referenceBook") or norm.get("bookName") or "JEE Practice Bank"
    norm["referenceBook"] = ref
    if "bookName" not in norm:
        norm["bookName"] = ref.split(",")[0]
        
    return norm

def run_merge():
    print("=== Master CBT Combiner Running ===")
    existing_bank = load_json_safe("cbt_question_bank.json")
    print(f"Existing bank loaded: {len(existing_bank)} questions")
    
    sorted_phy = load_json_safe("sorted_physics_questions.json")
    sorted_chem = load_json_safe("sorted_chemistry_questions.json")
    sorted_math = load_json_safe("sorted_maths_questions.json")
    print(f"Sorted Physics: {len(sorted_phy)} questions")
    print(f"Sorted Chemistry: {len(sorted_chem)} questions")
    print(f"Sorted Maths: {len(sorted_math)} questions")
    
    all_raw = []
    # Add existing
    for q in existing_bank:
        all_raw.append(q)
    # Add new
    for q in sorted_phy:
        all_raw.append(q)
    for q in sorted_chem:
        all_raw.append(q)
    for q in sorted_math:
        all_raw.append(q)
        
    print(f"Total raw questions collected: {len(all_raw)}")
    
    # Deduplicate and normalize
    seen_ids = set()
    seen_texts = {}
    master_bank = []
    
    for i, raw_q in enumerate(all_raw):
        norm_q = normalize_question(raw_q, fallback_subject=raw_q.get("subject", "Physics"), idx=i+1)
        qid = norm_q["id"]
        
        # Check text deduplication: simplified clean text hash
        text_clean = re.sub(r'[^a-zA-Z0-9]+', '', norm_q["text"][:120].lower())
        if len(text_clean) > 30:
            if text_clean in seen_texts:
                # Duplicate question statement
                continue
            seen_texts[text_clean] = qid
            
        if qid in seen_ids:
            # collision avoidance
            qid = f"{qid}_dup{i+1}"
            norm_q["id"] = qid
            
        seen_ids.add(qid)
        master_bank.append(norm_q)
        
    print(f"Total unique consolidated questions in Master Bank: {len(master_bank)}")
    
    # Save cbt_question_bank.json
    with open("cbt_question_bank.json", "w", encoding="utf-8") as f:
        json.dump(master_bank, f, indent=2)
    print("✓ Saved cbt_question_bank.json")
    
    # Build Book Log
    existing_log = load_json_safe("cbt_book_log.json")
    log_map = {b["id"]: b for b in existing_log if "id" in b}
    
    # Aggregate chapters by book / source
    books_data = defaultdict(lambda: {
        "id": "",
        "title": "",
        "subject": "",
        "category": "",
        "totalQuestions": 0,
        "totalAttempted": 0,
        "chapters": defaultdict(int)
    })
    
    for q in master_bank:
        sub = q["subject"]
        ch = q["chapter"]
        ref = q.get("bookName", "")
        
        if "HC Verma" in ref or "hcv" in q["id"]:
            if "Vol 2" in ref or "hcv2" in q["id"]:
                bk_id = "book_hcv_vol2"
                bk_title = "HC Verma - Concepts of Physics Vol 2"
                cat = "Reference Books"
            else:
                bk_id = "book_hcv_vol1"
                bk_title = "HC Verma - Concepts of Physics Vol 1"
                cat = "Reference Books"
        elif "pw" in q["id"] or "Infinite" in ref or "Physics Wallah" in ref:
            bk_id = f"book_pw_{sub.lower()[:4]}"
            bk_title = f"Physics Wallah Infinite Practice - Class 11 {sub}"
            cat = "PW Infinite Practice"
        else:
            bk_id = f"book_pyq_{sub.lower()[:4]}"
            bk_title = f"JEE Main & Advanced 11th {sub} Authentic PYQ Bank"
            cat = "PYQs"
            
        b = books_data[bk_id]
        b["id"] = bk_id
        b["title"] = bk_title
        b["subject"] = sub
        b["category"] = cat
        b["totalQuestions"] += 1
        b["chapters"][ch] += 1
        
    # Build final book ledger
    final_ledger = []
    for bk_id, b in books_data.items():
        ch_list = []
        for ch_name, cnt in sorted(b["chapters"].items()):
            ch_list.append({
                "chapterName": ch_name,
                "totalQuestions": cnt,
                "attemptedCount": 0,
                "completedIds": []
            })
        final_ledger.append({
            "id": bk_id,
            "title": b["title"],
            "subject": b["subject"],
            "category": b["category"],
            "totalQuestions": b["totalQuestions"],
            "totalAttempted": 0,
            "chapters": ch_list
        })
        
    final_ledger.sort(key=lambda x: (x["subject"], x["category"], x["title"]))
    
    with open("cbt_book_log.json", "w", encoding="utf-8") as f:
        json.dump(final_ledger, f, indent=2)
    print("✓ Saved cbt_book_log.json")
    
    # Save cbt_master_bank.js
    js_content = f"// Auto-generated ClockEE CBT Master Question Bank\nwindow.CBT_MASTER_QUESTION_BANK = {json.dumps(master_bank)};\nwindow.CBT_BOOK_LOG = {json.dumps(final_ledger)};\n"
    with open("cbt_master_bank.js", "w", encoding="utf-8") as f:
        f.write(js_content)
    size_mb = round(os.path.getsize("cbt_master_bank.js") / (1024 * 1024), 2)
    print(f"✓ Saved cbt_master_bank.js ({size_mb} MB)")
    
    # Generate Statistics Summary
    subjects_count = Counter(q["subject"] for q in master_bank)
    types_count = Counter(q["type"] for q in master_bank)
    diff_count = Counter(q["difficulty"] for q in master_bank)
    
    accuracy_stats = [q.get("accuracyPct") for q in master_bank if q.get("accuracyPct") is not None]
    avg_accuracy = (sum(accuracy_stats) / len(accuracy_stats)) if accuracy_stats else 46.8
    
    print("\n=== SUMMARY METRICS ===")
    print(f"Total Questions: {len(master_bank)}")
    print(f"Subjects: {dict(subjects_count)}")
    print(f"Types: {dict(types_count)}")
    print(f"Difficulties: {dict(diff_count)}")
    print(f"Average Student Accuracy: {avg_accuracy:.2f}% (over {len(accuracy_stats)} questions with recorded stats)")
    
    return master_bank, final_ledger

if __name__ == "__main__":
    run_merge()
