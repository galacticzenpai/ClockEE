with open(r'D:\Desktop\ClockEE\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

for fn in ['renderDriveLinks', 'renderPinnedAudioPlaylists']:
    idx = text.find(fn)
    print(fn, "in index.html:", idx)
    if idx != -1:
        print(text[idx-50:idx+300])
