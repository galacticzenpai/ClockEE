with open('scripts/v1_drawer_full.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("Full drawer lines:", len(text.splitlines()))
for i, l in enumerate(text.splitlines()):
    if 'id=' in l or 'onclick=' in l or 'class="drawer-tab' in l:
        print(f"{i+1}: {l.strip()[:100]}")
