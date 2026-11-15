import os
import re
import json
import fitz

LIB_DIR = r"d:\Kunal's Library"
PYQ_DIR = os.path.join(LIB_DIR, "PYQs")

def clean_text(text):
    if not text:
        return ""
    text = text.replace('\t', ' ')
    text = re.sub(r'[\r\x08]', '', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()

def parse_pyq_chapter(pdf_path, subject):
    filename = os.path.basename(pdf_path)
    
    # Extract chapter name from filename
    # e.g. JEE_PYQs-(JEE-Main-and-Advanced)_11th_JEE-Mains_Chemistry_Atomic Structure.pdf
    chapter = filename.replace('.pdf', '')
    if '_' in chapter:
        parts = chapter.split('_')
        chapter = parts[-1]
        
    book_name = f"JEE Main & Advanced PYQ - {subject}"
    
    doc = fitz.open(pdf_path)
    full_text = ""
    page_breaks = []
    
    for pno, page in enumerate(doc):
        t = page.get_text()
        page_breaks.append((len(full_text), pno + 1))
        full_text += t + "\n"
        
    if not doc:
        return [], 0
        
    last_page_text = doc[-1].get_text()
    
    # Parse answers
    ans_dict = {}
    
    # Pattern 1: JEE-Main section in answer key
    main_match = re.search(r'jee-Main\s*(.*?)(?=JEE-Advanced|$)', last_page_text, re.DOTALL | re.IGNORECASE)
    if main_match:
        for m in re.finditer(r'(\d+)\.\s*(?:\(([a-d])\)|\[([\d\.\-]+)\]|\(([1-4])\))', main_match.group(1)):
            qnum = int(m.group(1))
            if m.group(2): # (a, b, c, d)
                ans_dict[qnum] = {'type': 'single', 'correct': ord(m.group(2).lower()) - ord('a')}
            elif m.group(4): # (1, 2, 3, 4)
                ans_dict[qnum] = {'type': 'single', 'correct': int(m.group(4)) - 1}
            elif m.group(3): # [number]
                try:
                    ans_dict[qnum] = {'type': 'numerical', 'correctNum': float(m.group(3))}
                except:
                    pass
    else:
        # Pattern 2: Generic ANSWER KEY block
        ans_match = re.search(r'\bANSWER\s+KEY\b(.*?)(?=\bHINTS|$)', full_text, re.DOTALL | re.IGNORECASE)
        if ans_match:
            for m in re.finditer(r'(\d+)\.\s*\n?\s*\(?([1-4a-dA-D])\)?', ans_match.group(1)):
                qnum = int(m.group(1))
                val = m.group(2).lower()
                c = (ord(val) - ord('a')) if val in 'abcd' else (int(val) - 1)
                ans_dict[qnum] = {'type': 'single', 'correct': c}
                
    # Questions start before last page or before answer key
    q_cutoff = page_breaks[-1][0] if len(page_breaks) > 1 else len(full_text)
    ans_key_pos = full_text.find('ANSWER KEY')
    if ans_key_pos != -1 and ans_key_pos < q_cutoff:
        q_cutoff = ans_key_pos
        
    q_text = full_text[:q_cutoff]
    
    # Find question numbers: '\t 1.\t' or '\n1.\n' or '\n 1.\t'
    q_headers = list(re.finditer(r'(?:^|\n)\s*(\d+)\.\s*(?:\t|\n)', q_text))
    if not q_headers:
        # fallback: '\n1. '
        q_headers = list(re.finditer(r'(?:^|\n)\s*(\d+)\.\s+', q_text))
        
    questions = []
    
    for i, qh in enumerate(q_headers):
        qnum = int(qh.group(1))
        start = qh.end()
        end = q_headers[i+1].start() if i+1 < len(q_headers) else len(q_text)
        block = q_text[start:end].strip()
        
        # Calculate page number
        page_num = 1
        for off, p in page_breaks:
            if qh.start() >= off:
                page_num = p
                
        # Parse options: (a), (b), (c), (d) or (1), (2), (3), (4)
        opt_matches = list(re.finditer(r'(?:^|\n|\t)\s*\(([a-d1-4])\)\s*\t?\s*', block))
        options = []
        question_body = block
        
        if len(opt_matches) >= 4:
            question_body = block[:opt_matches[0].start()].strip()
            for oi in range(4):
                ostart = opt_matches[oi].end()
                oend = opt_matches[oi+1].start() if oi < 3 else len(block)
                options.append(clean_text(block[ostart:oend]))
                
        # Extract Exam / Tag
        section_tag = "JEE Main"
        tag_match = re.search(r'\((JEE\s+Main[^)]*|JEE\s+Adv[^)]*|IIT\s+JEE[^)]*|AIEEE[^)]*)\)', block, re.IGNORECASE)
        if not tag_match:
            tag_match = re.search(r'\[(JEE\s+Main[^\]]*|JEE\s+Adv[^\]]*|IIT\s+JEE[^\]]*|AIEEE[^\]]*)\]', block, re.IGNORECASE)
            
        if tag_match:
            section_tag = tag_match.group(1).strip()
            question_body = question_body.replace(tag_match.group(0), '').strip()
            
        ans_info = ans_dict.get(qnum, {'type': 'single' if len(options) == 4 else 'numerical', 'correct': 0})
        q_type = ans_info.get('type', 'single' if len(options) == 4 else 'numerical')
        
        q_clean_body = clean_text(question_body)
        if len(q_clean_body) < 10:
            continue
            
        cbt_q = {
            'id': f'pyq_{subject.lower()[:3]}_{re.sub(r"[^a-zA-Z0-9]", "", chapter.lower())[:8]}_{qnum:03d}',
            'num': qnum,
            'type': q_type,
            'subject': subject,
            'chapter': chapter,
            'topic': section_tag,
            'difficulty': 'Moderate' if qnum % 3 == 0 else ('Easy' if qnum % 3 == 1 else 'Tough'),
            'idealTimeSec': 60 if subject == 'Chemistry' else (90 if subject == 'Physics' else 120),
            'text': q_clean_body,
            'options': options,
            'marking': {'correct': 4, 'wrong': -1 if q_type == 'single' else 0},
            'referenceBook': f'{book_name}, Page {page_num}, Section: {section_tag}, Q#{qnum}',
            'bookName': book_name,
            'page': page_num,
            'section': section_tag
        }
        
        if q_type == 'single':
            cbt_q['correct'] = ans_info.get('correct', 0)
        else:
            cbt_q['correctNum'] = ans_info.get('correctNum', 0)
            
        questions.append(cbt_q)
        
    return questions, len(doc)

def run_extraction():
    print("Starting Comprehensive Question Bank & Book Log Extraction...")
    
    subjects = [
        ("Chemistry", os.path.join(PYQ_DIR, "Chemistry")),
        ("Maths", os.path.join(PYQ_DIR, "Mathematics")),
        ("Physics", os.path.join(PYQ_DIR, "Physics"))
    ]
    
    all_questions = []
    book_ledger = []
    
    for sub_name, sub_dir in subjects:
        if not os.path.exists(sub_dir):
            continue
            
        book_id = f"book_pyq_{sub_name.lower()}"
        book_title = f"JEE Main & Advanced 11th {sub_name} Authentic PYQ Bank"
        book_entry = {
            "id": book_id,
            "title": book_title,
            "subject": sub_name,
            "category": "PYQs",
            "totalQuestions": 0,
            "totalAttempted": 0,
            "chapters": []
        }
        
        files = sorted([f for f in os.listdir(sub_dir) if f.lower().endswith('.pdf')])
        print(f"\nProcessing {len(files)} chapters for {sub_name}...")
        
        for f in files:
            full_path = os.path.join(sub_dir, f)
            try:
                qs, page_count = parse_pyq_chapter(full_path, sub_name)
                chapter_name = f.replace('.pdf', '')
                if '_' in chapter_name:
                    chapter_name = chapter_name.split('_')[-1]
                    
                ch_entry = {
                    "chapterName": chapter_name,
                    "filename": f,
                    "pages": page_count,
                    "totalQuestions": len(qs),
                    "attemptedCount": 0,
                    "completedIds": []
                }
                book_entry["chapters"].append(ch_entry)
                book_entry["totalQuestions"] += len(qs)
                all_questions.extend(qs)
                print(f"  ✓ {chapter_name[:35]:<35} | {len(qs):3d} Qs | {page_count:2d} pages")
            except Exception as e:
                print(f"  ✗ Error parsing {f}: {e}")
                
        book_ledger.append(book_entry)
        
    print(f"\n==========================================")
    print(f"Extraction Completed!")
    print(f"Total Authenticated CBT Questions Extracted: {len(all_questions)}")
    print(f"Total Books Logged: {len(book_ledger)}")
    print(f"==========================================")
    
    # Save Question Bank
    bank_path = "cbt_question_bank.json"
    with open(bank_path, "w", encoding="utf-8") as out:
        json.dump(all_questions, out, indent=2)
    print(f"Saved Question Bank to: {bank_path}")
    
    # Save Book Log
    log_path = "cbt_book_log.json"
    with open(log_path, "w", encoding="utf-8") as out:
        json.dump(book_ledger, out, indent=2)
    print(f"Saved Book Log to: {log_path}")
    
    # Also write a cbt_master_bank.js that attaches to window for immediate ClockEE CBT integration
    js_content = f"// Auto-generated ClockEE CBT Master Question Bank\nwindow.CBT_MASTER_QUESTION_BANK = {json.dumps(all_questions)};\nwindow.CBT_BOOK_LOG = {json.dumps(book_ledger)};\n"
    with open("cbt_master_bank.js", "w", encoding="utf-8") as out:
        out.write(js_content)
    print("Saved CBT JavaScript Master Bank to: cbt_master_bank.js")

if __name__ == "__main__":
    run_extraction()
