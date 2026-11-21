import pymupdf
import re

pdf_path = r"d:\Kunal's Library\PYQs\Mathematics\JEE_PYQs-(JEE-Main-and-Advanced)_11th_JEE-Mains_Maths_Basic Math & Logarithm.pdf"
doc = pymupdf.open(pdf_path)

p1 = doc[0].get_text()
p2 = doc[1].get_text()

print("P1 len:", len(p1))
print("P2 len:", len(p2))

# Let's see how question numbers are formatted on P1
p1_headers = list(re.finditer(r'(?:^|\n)\s*(\d+)\.\s*', p1))
print(f"P1 question headers: {[m.group(1) for m in p1_headers]}")

# On P2:
p2_headers = list(re.finditer(r'(?:^|\n)\s*(\d+)\.\s*', p2))
print(f"P2 question headers: {[m.group(1) for m in p2_headers]}")
