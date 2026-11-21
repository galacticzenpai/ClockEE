import fitz

pdf_path = r"d:\Kunal's Library\PYQs\Mathematics\JEE_PYQs-(JEE-Main-and-Advanced)_11th_JEE-Mains_Maths_Basic Math & Logarithm.pdf"
doc = fitz.open(pdf_path)
print("Page count:", len(doc))
for i in range(len(doc)):
    txt = doc[i].get_text()
    print(f"Page {i+1}: length {len(txt)}, preview: {repr(txt[:100])}")
    if "ANSWER KEY" in txt or "HINTS" in txt:
        print(f"  --> Found KEY/HINTS on page {i+1}")
