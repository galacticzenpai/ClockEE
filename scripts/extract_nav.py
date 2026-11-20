with open('scripts/v1_header.html', 'r', encoding='utf-8') as f:
    hdr = f.read()

import re

# Find nav block
nav_match = re.search(r'<nav id="main-nav"[\s\S]*?</nav>', hdr) or re.search(r'<nav[^>]*id="main-nav"[^>]*>([\s\S]*?)</nav>', hdr)
if nav_match:
    print(nav_match.group(0))
else:
    print("Nav not found directly, showing entire header:")
    print(hdr)
