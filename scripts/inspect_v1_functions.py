with open(r'D:\Desktop\ClockEE\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re

# Find script 10
scripts = re.findall(r'<script[\s\S]*?</script>', text)
last_script = scripts[-1]

# Extract function names
fn_names = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', last_script)
print("Functions in v1 main script:", fn_names)

# Check event listeners or initialization
print("\nInitialization code:")
lines = last_script.splitlines()
for l in lines:
    if 'addEventListener' in l or 'window.onload' in l or 'document.addEventListener' in l or 'init' in l:
        print("  ", l.strip()[:100])
