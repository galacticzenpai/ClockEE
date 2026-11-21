with open('cbt_shared.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[:120]):
    print(f"{i+1}: {l}", end='')
