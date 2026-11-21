with open('cbt_exam.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'fetch' in line or 'question' in line.lower() and ('bank' in line.lower() or 'json' in line.lower() or 'load' in line.lower()):
        print(f"L{i+1}: {line.strip()[:120]}")
