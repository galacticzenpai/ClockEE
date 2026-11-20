with open('scripts/v1_main.html', 'r', encoding='utf-8') as f:
    main_text = f.read()

import re

# Split by the numbered comments
cards = re.split(r'<!--\s*([0-9]+\.[^>]+)-->', main_text)
print(f"Total split sections: {len(cards)}")

for i in range(1, len(cards), 2):
    title = cards[i].strip()
    content = cards[i+1]
    filename = f"scripts/card_{i//2 + 1}.html"
    with open(filename, "w", encoding="utf-8") as out:
        out.write(content.strip())
    print(f"Saved section {i//2 + 1}: '{title}' ({len(content)} chars) -> {filename}")
