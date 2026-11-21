import glob
import os
import pymupdf

pdf_dir = r"d:\Kunal's Library\PYQs\Mathematics"
for p in glob.glob(os.path.join(pdf_dir, "*.pdf"))[:4]:
    fname = os.path.basename(p)
    doc = pymupdf.open(p)
    has_hints = False
    for i, page in enumerate(doc):
        txt = page.get_text()
        if "HINTS & EXPLANATIONS" in txt or "HINTS AND SOLUTIONS" in txt or "HINTS" in txt:
            has_hints = True
            print(f"{fname}: Hints found on page {i+1} of {len(doc)}")
            break
    if not has_hints:
        print(f"{fname}: No hints section found")
