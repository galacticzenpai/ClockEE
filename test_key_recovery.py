import os
import glob
import pymupdf
import re

pdf_dir = r"d:\Kunal's Library\PYQs\Mathematics"

def get_answer_key(pdf_path):
    doc = pymupdf.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text() + "\n"
    
    main_match = re.search(r'jee-Main\s*(.*?)(?=JEE-Advanced|$)', full_text, re.DOTALL | re.IGNORECASE)
    ans = {}
    if main_match:
        for m in re.finditer(r'(\d+)\.\s*(?:\(([a-d1-4])\)|\[([\d\.\-]+)\])', main_match.group(1)):
            qn = int(m.group(1))
            if m.group(2):
                val = m.group(2).lower()
                c = (ord(val) - ord('a')) if val in 'abcd' else (int(val) - 1)
                ans[qn] = {'type': 'single', 'correct': c}
            elif m.group(3):
                try:
                    ans[qn] = {'type': 'numerical', 'correctNum': float(m.group(3))}
                except:
                    pass
    return ans

# Test on Binomial and Complex Numbers
for p in glob.glob(os.path.join(pdf_dir, "*Binomial*.pdf")) + glob.glob(os.path.join(pdf_dir, "*Complex*.pdf")):
    keys = get_answer_key(p)
    fname = os.path.basename(p)
    print(f"{fname}: {len(keys)} answers found. Q103 in keys: {103 in keys}, Q2 in keys: {2 in keys}")
