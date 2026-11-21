import pymupdf

doc = pymupdf.open(r"D:\Kunal's Library\Reference Books\Maths\11th JEE Restart Maths.pdf")
print("=== PAGE 5 ===")
print(doc[4].get_text()[:600])
print("=== PAGE 10 ===")
print(doc[9].get_text()[:600])
