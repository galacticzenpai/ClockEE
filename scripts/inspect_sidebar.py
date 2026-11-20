with open(r'D:\Desktop\ClockEE\clockee_core.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re

# find sidebar function
sidebar_idx = text.find('clockee-sidebar-root')
if sidebar_idx != -1:
    start = max(0, sidebar_idx - 200)
    end = min(len(text), sidebar_idx + 1500)
    print("--- CLOCKEE_CORE.JS SIDEBAR SECTION ---")
    print(text[start:end])
else:
    print("clockee-sidebar-root not found in clockee_core.js")
