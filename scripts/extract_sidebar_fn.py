with open(r'D:\Desktop\ClockEE\clockee_core.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re

start_idx = text.find('window.renderClockEESidebar = function')
if start_idx != -1:
    end_idx = text.find('window.render', start_idx + 30)
    if end_idx == -1:
        end_idx = start_idx + 4000
    sidebar_code = text[start_idx:end_idx]
    with open('scripts/v1_sidebar_fn.js', 'w', encoding='utf-8') as out:
        out.write(sidebar_code)
    print("Saved scripts/v1_sidebar_fn.js, length:", len(sidebar_code))
