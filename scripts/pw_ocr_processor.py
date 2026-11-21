#!/usr/bin/env python3
"""
PW Screenshot OCR Processor
Processes screenshots from pw_screenshots/ directory using Windows OCR
Extracts question text, options, percentages, correct answers
Appends to pw_extracted_master.json
"""
import json, os, sys, glob, re, time, subprocess
from pathlib import Path
from datetime import datetime

BANK_PATH = r"D:\Desktop\New folder\pw_extracted_master.json"
SS_BASE   = r"C:\Users\Kunal\.gemini\antigravity\brain\b5f97b16-8c62-47fd-92b6-1c96b5172e19\pw_screenshots"

def load_bank():
    if os.path.exists(BANK_PATH):
        with open(BANK_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_bank(data):
    with open(BANK_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[SAVE] {len(data)} questions in bank")

def ocr_image_windows(img_path):
    """Use Windows.Media.Ocr via PowerShell"""
    ps_script = f"""
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$null = [Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime]
$null = [Windows.Media.Ocr.OcrEngine,Windows.Media.Ocr,ContentType=WindowsRuntime]

$file = [Windows.Storage.StorageFile]::GetFileFromPathAsync('{img_path}').GetAwaiter().GetResult()
$stream = $file.OpenAsync([Windows.Storage.FileAccessMode]::Read).GetAwaiter().GetResult()
$decoder = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream).GetAwaiter().GetResult()
$bitmap = $decoder.GetSoftwareBitmapAsync().GetAwaiter().GetResult()

$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
$result = $engine.RecognizeAsync($bitmap).GetAwaiter().GetResult()
$result.Text
"""
    try:
        result = subprocess.run(
            ['powershell', '-Command', ps_script],
            capture_output=True, text=True, timeout=30
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"[OCR ERROR] {e}")
        return ""

def parse_question_from_ocr(text, chapter, subject, q_num):
    """Parse OCR text into question dict"""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # Try to extract question statement (usually before option A/1)
    q_text = ""
    options = []
    answer = None
    percentages = []
    
    q_lines = []
    opt_mode = False
    cur_opt = ""
    
    for line in lines:
        # Detect option markers
        if re.match(r'^[A-D]\)', line) or re.match(r'^[A-D]\s+', line) or re.match(r'^\([A-D]\)', line):
            opt_mode = True
            if cur_opt:
                options.append(cur_opt.strip())
            cur_opt = line
        elif re.match(r'^\d+\.?\d+\s*%', line) or re.match(r'^\d+\s*%', line):
            # Percentage data
            pct = float(re.search(r'(\d+\.?\d*)\s*%', line).group(1))
            percentages.append(pct)
        elif opt_mode:
            cur_opt += " " + line
        else:
            q_lines.append(line)
    
    if cur_opt:
        options.append(cur_opt.strip())
    
    q_text = " ".join(q_lines).strip()
    
    # If not enough structure found, use full text as question
    if not q_text or len(q_text) < 10:
        q_text = text[:500] if len(text) > 500 else text
    
    # Build option objects
    opt_labels = ['A', 'B', 'C', 'D']
    opt_objs = []
    for i, opt in enumerate(options[:4]):
        label = opt_labels[i] if i < len(opt_labels) else str(i)
        pct = percentages[i] if i < len(percentages) else 0.0
        opt_objs.append({
            "label": label,
            "option_text": re.sub(r'^[A-D]\)?\s*', '', opt).strip(),
            "student_percentage": pct,
            "is_correct": False,
            "registered_answer": False
        })
    
    # If no options found, make placeholders
    if not opt_objs:
        opt_objs = [
            {"label": "A", "option_text": "[See image]", "student_percentage": 0, "is_correct": False, "registered_answer": False},
            {"label": "B", "option_text": "[See image]", "student_percentage": 0, "is_correct": False, "registered_answer": False},
            {"label": "C", "option_text": "[See image]", "student_percentage": 0, "is_correct": False, "registered_answer": False},
            {"label": "D", "option_text": "[See image]", "student_percentage": 0, "is_correct": False, "registered_answer": False},
        ]
    
    q_id = f"PW_{subject[:3].upper()}_{chapter[:6].upper().replace(' ','_')}_{q_num:04d}_{int(time.time())}"
    
    return {
        "id": q_id,
        "subject": subject,
        "chapter": chapter,
        "source": "PW Infinite Practice",
        "type": "MCQ",
        "statement": q_text,
        "options": opt_objs,
        "student_accuracy": sum(percentages[:1]) if percentages else 0,
        "solution_text": "",
        "video_url": "",
        "extracted_at": datetime.now().isoformat(),
        "needs_review": True  # flagged for manual review if OCR imperfect
    }

def process_chapter_screenshots(chapter_name, subject):
    """Process all screenshots for a chapter"""
    chapter_dir = os.path.join(SS_BASE, chapter_name.replace(' ', '_'))
    if not os.path.exists(chapter_dir):
        print(f"[WARN] No screenshot dir for: {chapter_name}")
        return []
    
    screenshots = sorted(glob.glob(os.path.join(chapter_dir, "*.png")))
    print(f"[INFO] Processing {len(screenshots)} screenshots for {chapter_name}")
    
    questions = []
    for i, ss_path in enumerate(screenshots, 1):
        print(f"  [{i}/{len(screenshots)}] OCR: {os.path.basename(ss_path)}")
        text = ocr_image_windows(ss_path)
        if text:
            q = parse_question_from_ocr(text, chapter_name, subject, i)
            questions.append(q)
        else:
            print(f"  [SKIP] No OCR text from {ss_path}")
    
    return questions

def main():
    if len(sys.argv) < 3:
        print("Usage: python pw_ocr_processor.py <chapter_name> <subject>")
        print("  e.g.: python pw_ocr_processor.py 'Motion in a Straight Line' Physics")
        sys.exit(1)
    
    chapter = sys.argv[1]
    subject = sys.argv[2]
    
    print(f"[START] Processing: {chapter} ({subject})")
    questions = process_chapter_screenshots(chapter, subject)
    
    if not questions:
        print("[DONE] No questions extracted.")
        return
    
    bank = load_bank()
    before = len(bank)
    bank.extend(questions)
    save_bank(bank)
    print(f"[DONE] Added {len(questions)} questions. Bank: {before} -> {len(bank)}")

if __name__ == "__main__":
    main()
