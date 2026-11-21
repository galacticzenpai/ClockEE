import pymupdf
import re

doc = pymupdf.open(r"d:\Kunal's Library\PYQs\Mathematics\JEE_PYQs-(JEE-Main-and-Advanced)_11th_JEE-Mains_Maths_Binomial Theorem.pdf")
full_text = ""
for page in doc:
    full_text += page.get_text() + "\n"

pos = full_text.find("ANSWER KEY")
if pos != -1:
    print("Found ANSWER KEY. Text after it:")
    print(full_text[pos:pos+1500])
else:
    print("ANSWER KEY not found")
