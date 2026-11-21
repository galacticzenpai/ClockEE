import json
import glob
import os
import pymupdf
import re

with open('cbt_question_bank.json', 'r', encoding='utf-8') as f:
    bank = json.load(f)

maths = [q for q in bank if q.get('subject') in ['Maths', 'Mathematics']]

# Group by bookName or chapter
bank_by_chap = {}
for q in maths:
    c = q.get('chapter')
    bank_by_chap[c] = bank_by_chap.get(c, 0) + 1

print("CBT Question Bank Maths count per chapter:")
for c, cnt in sorted(bank_by_chap.items()):
    print(f"  {c}: {cnt}")
