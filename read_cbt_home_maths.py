with open('cbt_home.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

recording = False
for line in lines:
    if 'Maths: [' in line:
        recording = True
    if recording:
        print(line, end='')
        if ']' in line and 'Maths' not in line:
            break
