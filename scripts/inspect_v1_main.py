with open('scripts/v1_main.html', 'r', encoding='utf-8') as f:
    main_text = f.read()

import re

# Find all cards / top-level divs inside main
cards = re.findall(r'<div[^>]*class="[^"]*(?:card|hud-card|glass-card|rounded-2xl|col-span)[^"]*"[^>]*id="([^"]+)"', main_text)
print("Cards with IDs:", cards)

# Find major section comments
comments = re.findall(r'<!--([\s\S]*?)-->', main_text)
print("\nMajor section comments:")
for c in comments:
    c_clean = c.strip()
    if len(c_clean) < 80 and not c_clean.startswith('card') and '\n' not in c_clean:
        print("  -", c_clean)
