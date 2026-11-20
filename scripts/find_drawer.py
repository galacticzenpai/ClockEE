with open(r'D:\Desktop\ClockEE\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re

idx = text.find('split-drawer')
print('split-drawer index:', idx)
if idx != -1:
    # find enclosing element
    start = text.rfind('<', 0, idx)
    # find where this element ends
    print(text[start:start+1200])
    with open('scripts/v1_drawer_sample.html', 'w', encoding='utf-8') as out:
        out.write(text[start:start+10000])
