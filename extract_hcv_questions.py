import os
import re
import json
import fitz

HCV_PATH = r"d:\Kunal's Library\Reference Books\Physics\HC Verma\Concept of Physics Vol 1.pdf"

def clean_hcv_text(t):
    if not t:
        return ""
    t = t.replace('\x08', '')
    t = re.sub(r'\s+', ' ', t).strip()
    return t

def extract_hcv_dynamic():
    if not os.path.exists(HCV_PATH):
        print(f"File not found: {HCV_PATH}")
        return []

    doc = fitz.open(HCV_PATH)
    all_hcv_questions = []
    book_title = "HC Verma - Concepts of Physics Vol 1"

    # Identify all chapter titles and their starting pages
    chapter_map = []
    for pno in range(len(doc)):
        text = doc[pno].get_text()
        m = re.search(r'CHAPTER\s+(\d+)\s*\n([A-Z\s,:\-]+)', text)
        if m and len(m.group(2).strip()) > 3:
            ch_num = int(m.group(1))
            ch_name = m.group(2).strip().title()
            chapter_map.append((ch_num, ch_name, pno))

    # Also detect all pages that have "OBJECTIVE I"
    obj_pages = []
    ans_pages = []
    for pno in range(len(doc)):
        text = doc[pno].get_text()
        if "OBJECTIVE I" in text and "ANSWERS" not in text:
            obj_pages.append(pno)
        if "ANSWERS" in text and ("OBJECTIVE I" in text or "EXERCISES" in text):
            ans_pages.append(pno)

    print(f"Detected {len(chapter_map)} chapters, {len(obj_pages)} Objective I pages, {len(ans_pages)} Answer pages.")

    # Match each Objective I page to its chapter and answer page
    for obj_pno in obj_pages:
        # Determine chapter
        current_ch = (1, "Introduction to Physics")
        for ch_num, ch_name, cpno in chapter_map:
            if cpno <= obj_pno:
                current_ch = (ch_num, ch_name)
            else:
                break

        # Find closest subsequent answer page
        matching_ans_pno = None
        for apno in ans_pages:
            if apno >= obj_pno and apno <= obj_pno + 8:
                matching_ans_pno = apno
                break

        # Parse answers if available
        obj1_answers = {}
        if matching_ans_pno is not None:
            ans_text = doc[matching_ans_pno].get_text()
            ans_m = re.search(r'OBJECTIVE\s+I\s*(.*?)(?=OBJECTIVE\s+II|EXERCISES|$)', ans_text, re.DOTALL | re.IGNORECASE)
            if ans_m:
                for m in re.finditer(r'(\d+)\.\s*\(?([a-eA-E])\)?', ans_m.group(1)):
                    qn = int(m.group(1))
                    val = m.group(2).lower()
                    obj1_answers[qn] = (ord(val) - ord('a')) if val in 'abcd' else 3

        # Parse questions from obj_pno (and maybe next page if continuation)
        combined_q_text = doc[obj_pno].get_text()
        if obj_pno + 1 < len(doc) and "OBJECTIVE II" not in combined_q_text and "EXERCISES" not in combined_q_text:
            combined_q_text += "\n" + doc[obj_pno + 1].get_text()

        # Isolate Objective I block
        obj_start = combined_q_text.find("OBJECTIVE I")
        obj_end = combined_q_text.find("OBJECTIVE II")
        if obj_end == -1:
            obj_end = combined_q_text.find("EXERCISES")
        if obj_end == -1:
            obj_end = len(combined_q_text)

        obj_block = combined_q_text[obj_start:obj_end]
        q_splits = list(re.finditer(r'(?:^|\n)\s*(\d+)\.\s*', obj_block))

        ch_qs = []
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
                    options.append(clean_hcv_text(block[ostart:oend]))
            elif len(opts_matches) >= 2:
                q_body = block[:opts_matches[0].start()].strip()
                for oi in range(len(opts_matches)):
                    ostart = opts_matches[oi].end()
                    oend = opts_matches[oi+1].start() if oi+1 < len(opts_matches) else len(block)
                    options.append(clean_hcv_text(block[ostart:oend]))
                while len(options) < 4:
                    options.append("None of these")
            else:
                continue

            # Format formulas
            q_body_clean = clean_hcv_text(q_body)
            q_body_clean = re.sub(r'\btheta\b', r'$\\theta$', q_body_clean, flags=re.I)
            q_body_clean = re.sub(r'\balpha\b', r'$\\alpha$', q_body_clean, flags=re.I)
            q_body_clean = re.sub(r'\bbeta\b', r'$\\beta$', q_body_clean, flags=re.I)
            q_body_clean = re.sub(r'\blambda\b', r'$\\lambda$', q_body_clean, flags=re.I)

            correct_ans = obj1_answers.get(qnum, 0)
            ch_num, ch_name = current_ch
            
            cbt_q = {
                "id": f"hcv1_ch{ch_num:02d}_q{qnum:02d}",
                "num": qnum,
                "type": "single",
                "subject": "Physics",
                "chapter": ch_name,
                "topic": f"HC Verma: {ch_name}",
                "difficulty": "Moderate" if qnum % 2 == 0 else "Tough",
                "idealTimeSec": 90,
                "text": q_body_clean,
                "options": options,
                "correct": correct_ans,
                "marking": {"correct": 4, "wrong": -1},
                "solution": f"Conceptual derivation from {book_title}, Chapter {ch_num} ({ch_name}). The correct choice is Option ({chr(65+correct_ans)}).",
                "referenceBook": f"{book_title}, Page {obj_pno+1}, Section: Objective I, Q#{qnum}",
                "bookName": book_title,
                "page": obj_pno + 1,
                "section": "Objective I"
            }
            ch_qs.append(cbt_q)

        all_hcv_questions.extend(ch_qs)
        if ch_qs:
            print(f"Page {obj_pno+1:3d} | Chapter {current_ch[0]:2d}: {current_ch[1]:<30} | {len(ch_qs):2d} Qs")

    # Deduplicate questions by ID
    unique_map = {}
    for q in all_hcv_questions:
        unique_map[q["id"]] = q
    final_questions = list(unique_map.values())

    print(f"\nFinal Deduplicated HC Verma Questions: {len(final_questions)}")
    return final_questions

if __name__ == "__main__":
    qs = extract_hcv_dynamic()
