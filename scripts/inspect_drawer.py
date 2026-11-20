with open('scripts/v1_drawer_full.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

buttons = re.findall(r'<button[^>]*onclick="([^"]*)"[^>]*>([\s\S]*?)</button>', text)
print("Drawer buttons:")
for act, label in buttons:
    clean_l = re.sub(r'<[^>]+>', '', label).strip()
    print(f"  {clean_l} -> {act}")

tabs = re.findall(r'id="(tab-[^"]+|drawer-tab-[^"]+)"', text)
print("Drawer tab IDs:", tabs)
