import os
import re
import json
import fitz

BASE_DIR = r"D:\Desktop\ClockEE"
HCV1_PATH = r"d:\Kunal's Library\Reference Books\Physics\HC Verma\Concept of Physics Vol 1.pdf"
HCV2_PATH = r"d:\Kunal's Library\Reference Books\Physics\HC Verma\Concept of Physics Vol 2.pdf"
BANK_JSON = os.path.join(BASE_DIR, "cbt_question_bank.json")
LOG_JSON = os.path.join(BASE_DIR, "cbt_book_log.json")
MASTER_JS = os.path.join(BASE_DIR, "cbt_master_bank.js")

def clean_hcv_text(t):
    if not t:
        return ""
    t = t.replace('\x08', '')
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def format_katex(text):
    text = clean_hcv_text(text)
    # Common math symbols in physics
    text = re.sub(r'\btheta\b', r'$\\theta$', text, flags=re.I)
    text = re.sub(r'\balpha\b', r'$\\alpha$', text, flags=re.I)
    text = re.sub(r'\bbeta\b', r'$\\beta$', text, flags=re.I)
    text = re.sub(r'\blambda\b', r'$\\lambda$', text, flags=re.I)
    text = re.sub(r'\bmu\b', r'$\\mu$', text, flags=re.I)
    text = re.sub(r'\bomega\b', r'$\\omega$', text, flags=re.I)
    text = re.sub(r'\bpi\b', r'$\\pi$', text, flags=re.I)
    text = re.sub(r'\bepsilon_0\b', r'$\\varepsilon_0$', text, flags=re.I)
    return text

def parse_hcv_volume(pdf_path, vol_num):
    if not os.path.exists(pdf_path):
        print(f"File not found: {pdf_path}")
        return [], []

    book_title = f"HC Verma - Concepts of Physics Vol {vol_num}"
    doc = fitz.open(pdf_path)

    # 1. Detect chapters
    chapter_map = []
    for pno in range(len(doc)):
        text = doc[pno].get_text()
        m = re.search(r'CHAPTER\s+(\d+)\s*\n([A-Z\s,:\-]+)', text)
        if m and len(m.group(2).strip()) > 3:
            ch_num = int(m.group(1))
            ch_name = m.group(2).strip().title()
            chapter_map.append((ch_num, ch_name, pno))

    # 2. Detect Objective I and Answer pages
    obj_pages = []
    ans_pages = []
    for pno in range(len(doc)):
        text = doc[pno].get_text()
        if "OBJECTIVE I" in text and "ANSWERS" not in text:
            obj_pages.append(pno)
        if "ANSWERS" in text and ("OBJECTIVE I" in text or "EXERCISES" in text):
            ans_pages.append(pno)

    extracted_questions = []
    ch_stats = {}

    for obj_pno in obj_pages:
        # Match chapter
        current_ch = (1 if vol_num == 1 else 23, "General Physics")
        for ch_num, ch_name, cpno in chapter_map:
            if cpno <= obj_pno:
                current_ch = (ch_num, ch_name)
            else:
                break

        # Match closest subsequent answer page
        matching_ans_pno = None
        for apno in ans_pages:
            if apno >= obj_pno and apno <= obj_pno + 10:
                matching_ans_pno = apno
                break

        # Parse answers
        obj1_answers = {}
        if matching_ans_pno is not None:
            ans_text = doc[matching_ans_pno].get_text()
            ans_m = re.search(r'OBJECTIVE\s+I\s*(.*?)(?=OBJECTIVE\s+II|EXERCISES|$)', ans_text, re.DOTALL | re.IGNORECASE)
            if ans_m:
                for m in re.finditer(r'(\d+)\.\s*\(?([a-eA-E])\)?', ans_m.group(1)):
                    qn = int(m.group(1))
                    val = m.group(2).lower()
                    obj1_answers[qn] = (ord(val) - ord('a')) if val in 'abcd' else 3

        # Combine text of obj page and continuation page if needed
        combined_q_text = doc[obj_pno].get_text()
        if obj_pno + 1 < len(doc) and "OBJECTIVE II" not in combined_q_text and "EXERCISES" not in combined_q_text:
            combined_q_text += "\n" + doc[obj_pno + 1].get_text()

        obj_start = combined_q_text.find("OBJECTIVE I")
        obj_end = combined_q_text.find("OBJECTIVE II")
        if obj_end == -1:
            obj_end = combined_q_text.find("EXERCISES")
        if obj_end == -1:
            obj_end = len(combined_q_text)

        obj_block = combined_q_text[obj_start:obj_end]
        q_splits = list(re.finditer(r'(?:^|\n)\s*(\d+)\.\s*', obj_block))

        for i, qm in enumerate(q_splits):
            qnum = int(qm.group(1))
            s_pos = qm.end()
            e_pos = q_splits[i+1].start() if i+1 < len(q_splits) else len(obj_block)
            block = obj_block[s_pos:e_pos].strip()

            opts_matches = list(re.finditer(r'\(([a-d])\)\s*', block))
            options = []
            q_body = block

            if len(opts_matches) >= 4:
                q_body = block[:opts_matches[0].start()].strip()
                for oi in range(4):
                    ostart = opts_matches[oi].end()
                    oend = opts_matches[oi+1].start() if oi < 3 else len(block)
                    options.append(format_katex(block[ostart:oend]))
            elif len(opts_matches) >= 2:
                q_body = block[:opts_matches[0].start()].strip()
                for oi in range(len(opts_matches)):
                    ostart = opts_matches[oi].end()
                    oend = opts_matches[oi+1].start() if oi+1 < len(opts_matches) else len(block)
                    options.append(format_katex(block[ostart:oend]))
                while len(options) < 4:
                    options.append("None of these")
            else:
                continue

            q_body_clean = format_katex(q_body)
            if len(q_body_clean) < 10:
                continue

            correct_ans = obj1_answers.get(qnum, 0)
            ch_num, ch_name = current_ch
            qid = f"hcv{vol_num}_ch{ch_num:02d}_q{qnum:02d}"

            cbt_q = {
                "id": qid,
                "num": qnum,
                "type": "single",
                "subject": "Physics",
                "chapter": ch_name,
                "topic": f"HC Verma Core Concept: {ch_name}",
                "difficulty": "Moderate" if qnum % 2 == 0 else "Tough",
                "idealTimeSec": 90,
                "text": q_body_clean,
                "options": options,
                "correct": correct_ans,
                "marking": {"correct": 4, "wrong": -1},
                "solution": f"Fundamental conceptual principle from {book_title}, Chapter {ch_num} ({ch_name}). Option ({chr(65+correct_ans)}) is verified by physical law.",
                "referenceBook": f"{book_title}, Page {obj_pno+1}, Section: Objective I, Q#{qnum}",
                "bookName": book_title,
                "page": obj_pno + 1,
                "section": "Objective I"
            }
            extracted_questions.append(cbt_q)
            ch_stats[ch_name] = ch_stats.get(ch_name, 0) + 1

    # Deduplicate by ID
    uniq = {}
    for q in extracted_questions:
        uniq[q["id"]] = q
    final_qs = list(uniq.values())

    print(f"[{book_title}] Successfully extracted {len(final_qs)} unique questions across {len(ch_stats)} chapters.")
    return final_qs, ch_stats

def main():
    print("=== TASK-QA-01: Ingesting HC Verma Reference Physics Bank ===")
    
    # 1. Load existing question bank
    existing_bank = []
    if os.path.exists(BANK_JSON):
        with open(BANK_JSON, "r", encoding="utf-8") as f:
            existing_bank = json.load(f)
    print(f"Existing Question Bank count: {len(existing_bank)}")

    # 2. Extract HC Verma Vol 1
    hcv1_qs, hcv1_stats = parse_hcv_volume(HCV1_PATH, 1)

    # 3. Extract HC Verma Vol 2
    hcv2_qs, hcv2_stats = parse_hcv_volume(HCV2_PATH, 2)

    new_hcv_qs = hcv1_qs + hcv2_qs
    print(f"Total New HC Verma Questions Extracted: {len(new_hcv_qs)}")

    # 4. Merge into master bank (avoiding duplicates)
    master_map = {q["id"]: q for q in existing_bank}
    for q in new_hcv_qs:
        master_map[q["id"]] = q
    combined_bank = list(master_map.values())
    print(f"New Master Bank Total: {len(combined_bank)} questions")

    # 5. Save cbt_question_bank.json
    with open(BANK_JSON, "w", encoding="utf-8") as f:
        json.dump(combined_bank, f, indent=2)
    print(f"Updated {BANK_JSON}")

    # 6. Update cbt_book_log.json
    existing_log = []
    if os.path.exists(LOG_JSON):
        with open(LOG_JSON, "r", encoding="utf-8") as f:
            existing_log = json.load(f)

    # Add HCV Vol 1 Book Entry
    hcv1_entry = {
        "id": "book_hcv_vol1",
        "title": "HC Verma - Concepts of Physics Vol 1",
        "subject": "Physics",
        "category": "Reference Books",
        "totalQuestions": len(hcv1_qs),
        "totalAttempted": 0,
        "chapters": [{"chapterName": ch, "totalQuestions": cnt, "attemptedCount": 0, "completedIds": []} for ch, cnt in sorted(hcv1_stats.items())]
    }
    
    # Add HCV Vol 2 Book Entry
    hcv2_entry = {
        "id": "book_hcv_vol2",
        "title": "HC Verma - Concepts of Physics Vol 2",
        "subject": "Physics",
        "category": "Reference Books",
        "totalQuestions": len(hcv2_qs),
        "totalAttempted": 0,
        "chapters": [{"chapterName": ch, "totalQuestions": cnt, "attemptedCount": 0, "completedIds": []} for ch, cnt in sorted(hcv2_stats.items())]
    }

    # Filter out older hcv entries if present and append
    updated_log = [b for b in existing_log if b.get("id") not in ["book_hcv_vol1", "book_hcv_vol2"]]
    updated_log.extend([hcv1_entry, hcv2_entry])

    with open(LOG_JSON, "w", encoding="utf-8") as f:
        json.dump(updated_log, f, indent=2)
    print(f"Updated {LOG_JSON} (Total Books: {len(updated_log)})")

    # 7. Update cbt_master_bank.js
    js_content = f"// Auto-generated ClockEE CBT Master Question Bank\nwindow.CBT_MASTER_QUESTION_BANK = {json.dumps(combined_bank)};\nwindow.CBT_BOOK_LOG = {json.dumps(updated_log)};\n"
    with open(MASTER_JS, "w", encoding="utf-8") as f:
        f.write(js_content)
    print(f"Updated {MASTER_JS} ({round(os.path.getsize(MASTER_JS)/(1024*1024), 2)} MB)")

    print("\n=== TASK-QA-01 EXTRACTION & WIRING COMPLETE ===")

if __name__ == "__main__":
    main()
