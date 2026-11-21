with open('scripts/cbt-engine.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[:100]):
    print(f"{i+1}: {l}", end='')
