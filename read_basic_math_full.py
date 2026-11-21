import pymupdf

pdf_path = r"d:\Kunal's Library\PYQs\Mathematics\JEE_PYQs-(JEE-Main-and-Advanced)_11th_JEE-Mains_Maths_Basic Math & Logarithm.pdf"
doc = pymupdf.open(pdf_path)
for i, page in enumerate(doc):
    print(f"=== PAGE {i+1} ===")
    print(page.get_text())
