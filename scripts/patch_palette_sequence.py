with open('cbt_exam.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace ${q.localNumber} with ${globalIdx + 1}
old_pattern = 'title="Question ${q.localNumber} (Section ${q.section})"'
new_pattern = 'title="Question ${globalIdx + 1} (Section ${q.section})"'

if old_pattern in text:
    text = text.replace(old_pattern, new_pattern)
    text = text.replace('>\n            ${q.localNumber}\n          </button>', '>\n            ${globalIdx + 1}\n          </button>')
    print("Replaced q.localNumber with globalIdx + 1 in palette buttons")

with open('cbt_exam.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Saved cbt_exam.html successfully")
