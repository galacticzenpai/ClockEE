with open(r'D:\Desktop\ClockEE\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re
style_match = re.search(r'<style>([\s\S]*?)</style>', text)
if style_match:
    style_content = style_match.group(1)
    with open('scripts/v1_styles.css', 'w', encoding='utf-8') as out:
        out.write(style_content)
    print("Saved scripts/v1_styles.css, length:", len(style_content))
