with open(r'D:\Desktop\ClockEE\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re

scripts = re.findall(r'<script[\s\S]*?</script>', text)
last_script = scripts[-1]

# Strip <script> and </script>
code = re.sub(r'^\s*<script[^>]*>', '', last_script)
code = re.sub(r'</script>\s*$', '', code)

with open('scripts/v1_bottom_script.js', 'w', encoding='utf-8') as out:
    out.write(code)

print("Saved scripts/v1_bottom_script.js, length:", len(code), "lines:", len(code.splitlines()))
