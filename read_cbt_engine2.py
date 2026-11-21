with open('scripts/cbt-engine.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(100, min(len(lines), 200)):
    print(f"{i+1}: {lines[i]}", end='')
