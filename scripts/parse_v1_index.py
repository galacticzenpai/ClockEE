import re
import os

with open(r'D:\Desktop\ClockEE\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

print(f"Total lines: {len(text.splitlines())}")

# Header
header_match = re.search(r'<header[\s\S]*?</header>', text)
if header_match:
    nav = header_match.group(0)
    print("=== HEADER LENGTH ===", len(nav))
    with open("scripts/v1_header.html", "w", encoding="utf-8") as out:
        out.write(nav)
    print("Wrote scripts/v1_header.html")

# Main containers
main_match = re.search(r'<main[\s\S]*?</main>', text)
if main_match:
    main_content = main_match.group(0)
    print("=== MAIN LENGTH ===", len(main_content))
    with open("scripts/v1_main.html", "w", encoding="utf-8") as out:
        out.write(main_content)
    print("Wrote scripts/v1_main.html")

# Drawers / modals / split screen
scripts_match = re.search(r'(<aside[\s\S]*?</aside>)', text)
if scripts_match:
    print("=== ASIDE FOUND ===")

# Check for split drawer
split_match = re.search(r'(<!--\s*SPLIT[\s\S]*?-->[\s\S]*?)(?=<script|$)', text, re.IGNORECASE)
if split_match:
    print("=== SPLIT DRAWER FOUND ===")

# Check all IDs in the file
ids = re.findall(r'id=["\']([^"\']+)["\']', text)
print(f"Total IDs: {len(ids)}")
print("Sample IDs:", ids[:30])
