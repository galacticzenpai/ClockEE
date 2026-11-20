with open(r'D:\Desktop\ClockEE\clockee_core.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

for target in ['drive-links-list', 'pinned-playlists-list', 'switchDrawerTab']:
    idx = text.find(target)
    print(target, "in clockee_core.js:", idx)
    if idx != -1:
        print(text[idx-50:idx+250])
