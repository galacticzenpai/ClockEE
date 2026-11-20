with open(r'D:\Desktop\ClockEE\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text_idx = f.read()

with open(r'D:\Desktop\ClockEE\clockee_core.js', 'r', encoding='utf-8', errors='ignore') as f:
    text_core = f.read()

for fn in ['switchDrawerTab', 'toggleSplitScreen', 'sendAIDoubtMessage', 'insertNoteTimestamp']:
    in_idx = fn in text_idx
    in_core = fn in text_core
    print(f"{fn} -> in index.html: {in_idx}, in clockee_core.js: {in_core}")
