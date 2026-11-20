with open(r'D:\Desktop\ClockEE\clockee_core.js', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

for fn in ['renderLecturesDrawer', 'renderDriveLinks', 'renderPinnedAudioPlaylists']:
    print(fn, "in clockee_core.js:", fn in text)
