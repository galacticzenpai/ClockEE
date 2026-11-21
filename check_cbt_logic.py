with open('cbt_home.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = re.findall(r'function [a-zA-Z0-9_]+\s*\([^)]*\)', html)
print("Functions in cbt_home.html:")
for m in matches:
    print(" -", m)

matches2 = re.findall(r'(?:selectCategory|filterBySubject|launchTest|startTest|renderTests|renderAccordion)[^{]*', html)
print("\nKey handlers:")
for m in matches2:
    print(" -", m.strip())
