with open('cbt_exam.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(450, min(len(lines), 530)):
    print(f"{i+1}: {lines[i]}", end='')
