with open(r'D:\Desktop\ClockEE\index.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

idx = text.find('id="split-drawer"')
start = text.rfind('<div', 0, idx)

# Find matching close tag or end comment
end_comment = text.find('<!-- /split-drawer -->', idx)
if end_comment != -1:
    end = text.find('</div>', end_comment) + 6
else:
    # find next main section or script
    end = text.find('<script', idx)

drawer_html = text[start:end]
print("Drawer length:", len(drawer_html))
with open('scripts/v1_drawer_full.html', 'w', encoding='utf-8') as out:
    out.write(drawer_html)
print("Saved scripts/v1_drawer_full.html")
