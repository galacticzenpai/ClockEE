with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'id="split-drawer"' in l:
        print(f"Line {i+1}: {l.strip()}")
        # Replace w-[420px] with responsive classes
        lines[i] = l.replace('w-[420px]', 'w-full sm:w-[420px]')
        print("Updated to:", lines[i].strip())
        break

with open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
