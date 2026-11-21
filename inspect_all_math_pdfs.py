import os
import glob
import pymupdf
import re

pdf_dir = r"d:\Kunal's Library\PYQs\Mathematics"
pdfs = glob.glob(os.path.join(pdf_dir, "*.pdf"))

print(f"Found {len(pdfs)} PDFs in {pdf_dir}")

for p in pdfs:
    fname = os.path.basename(p)
    doc = pymupdf.open(p)
    full_text = ""
    for page in doc:
        full_text += page.get_text() + "\n"
    
    # Check answer key
    main_match = re.search(r'jee-Main\s*(.*?)(?=JEE-Advanced|$)', full_text, re.DOTALL | re.IGNORECASE)
    adv_match = re.search(r'JEE-Advanced\s*(.*?)(?=ANSWER KEY|\bHINTS\b|$)', full_text, re.DOTALL | re.IGNORECASE)
    
    main_count = len(re.findall(r'\b\d+\.\s*(?:\([a-d1-4]\)|\[[\d\.\-]+\])', main_match.group(1))) if main_match else 0
    adv_count = len(re.findall(r'\b\d+\.\s*(?:\([a-d1-4,\s]+\)|\[[\d\.\-]+\])', adv_match.group(1))) if adv_match else 0
    
    print(f"{fname[:45]}: Pages={len(doc)}, Main Key Qs={main_count}, Adv Key Qs={adv_count}")
