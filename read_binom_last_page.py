import pymupdf

doc = pymupdf.open(r"d:\Kunal's Library\PYQs\Mathematics\JEE_PYQs-(JEE-Main-and-Advanced)_11th_JEE-Mains_Maths_Binomial Theorem.pdf")
print("Total pages:", len(doc))
print("Last page text:")
print(doc[-1].get_text()[:1500])
