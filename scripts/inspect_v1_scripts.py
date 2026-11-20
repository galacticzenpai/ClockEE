with open(r'D:\Desktop\ClockEE\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re

# Find all script tags outside head
body_scripts = re.findall(r'<script[\s\S]*?</script>', text)
print(f"Total script tags in v1: {len(body_scripts)}")

for i, s in enumerate(body_scripts):
    src = re.search(r'src=["\']([^"\']+)["\']', s)
    if src:
        print(f"Script {i} src: {src.group(1)}")
    else:
        print(f"Script {i} inline, len: {len(s)}, preview: {s[:100]}...")
