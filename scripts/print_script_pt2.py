with open('scripts/v1_bottom_script.js', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
print('\n'.join(lines[60:160]))
