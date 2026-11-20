with open(r'D:\Desktop\ClockEE\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total lines: {len(lines)}')
for i, l in enumerate(lines[396:], start=397):
    stripped = l.strip()
    if any(k in stripped for k in ['<h1', '<h2', '<h3', 'class="glass-card', 'class="p-', 'id=']):
        print(f'{i:4}: {stripped[:100]}')
