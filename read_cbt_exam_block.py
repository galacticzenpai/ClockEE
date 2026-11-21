with open('cbt_exam.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(215, min(len(lines), 350)):
    print(f"{i+1}: {lines[i]}", end='')
