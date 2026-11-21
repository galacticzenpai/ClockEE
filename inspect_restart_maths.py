import pymupdf

doc = pymupdf.open(r"D:\Kunal's Library\Reference Books\Maths\11th JEE Restart Maths.pdf")
print("Total pages in 11th JEE Restart Maths.pdf:", len(doc))
for i in range(min(10, len(doc))):
    txt = doc[i].get_text()
    first_line = txt.split('\n')[0] if txt else ''
    print(f"Page {i+1}: {repr(first_line)[:80]}")
