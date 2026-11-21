import re

with open('cbt_home.html', 'r', encoding='utf-8') as f:
    html = f.read()

print("Occurrences of Math/Mathematics in cbt_home.html:")
for line in html.splitlines():
    if 'math' in line.lower():
        print(line.strip()[:140])
