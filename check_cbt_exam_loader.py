with open('cbt_exam.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(?:fetch|load|import|bank|master)[^;\n]*', text, re.I)
for m in matches[:20]:
    print(m.strip())
