import os

files = [
    'analysis.html', 'cbt.html', 'cbt_cloner.html', 'cbt_exam.html', 
    'cbt_instructions.html', 'cbt_mistakes.html', 'cbt_notebooks.html', 
    'cbt_reference_vault.html', 'demo_cockpit.html', 'hackathon.html', 
    'mini_timer.html', 'syllabus_tracker.html', 'tracker.html'
]

link_tag = '''  <!-- Master Apple HIG & Apple Intelligence Design System -->
  <link rel="stylesheet" href="css/apple_design_system.css" />
</head>'''

for f in files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as fp:
            c = fp.read()
        if 'apple_design_system.css' not in c:
            c = c.replace('</head>', link_tag, 1)
            with open(f, 'w', encoding='utf-8') as fp:
                fp.write(c)
            print(f"✔ Linked in {f}")
        else:
            print(f"- Already linked in {f}")
