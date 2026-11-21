with open('cbt_master_bank.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in cbt_master_bank.js: {len(lines)}")
for i, l in enumerate(lines[:30]):
    print(f"{i+1}: {l}", end='')
