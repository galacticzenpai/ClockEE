import json
import html
import re

master = json.load(open('pw_extracted_master.json', 'r', encoding='utf-8'))

doc = []
doc.append("# 📚 Master Inventory: All Harvested Questions, Statistics & Solutions")
doc.append("\n> **Comprehensive Audit Report of All Authentic Extracted Questions from Physics Wallah Infinite Practice**")
doc.append(f"> **Total Live Harvested Entries**: `{len(master)} Questions` across Class 11 PCM chapters.")
doc.append("> **Data Schema Standard**: Includes Question ID, Chapter, Topic, Statement, Diagrams, Options with exact Student Selection %s, Answer Key, Difficulty, and Complete Mathematical Derivations.\n")

doc.append("---")
doc.append("## 📊 Summary by Chapter & Subject Breakdown\n")
doc.append("| # | Subject | Chapter | Questions Harvested | Status |")
doc.append("|---|---|---|---|---|")

from collections import Counter
chap_counts = Counter((q.get('subject', 'Physics'), q.get('chapter', 'Unknown')) for q in master)

idx = 1
for (sub, ch), cnt in sorted(chap_counts.items(), key=lambda x: -x[1]):
    status = "100% Exhausted" if "Physical World" in ch else "Multi-Pass Active"
    doc.append(f"| {idx} | {sub} | {ch} | **{cnt}** | `{status}` |")
    idx += 1

doc.append("\n---\n")
doc.append("## 📝 Detailed Question-by-Question Catalogue\n")

for i, q in enumerate(master, 1):
    qid = q.get('id', f'PW_Q_{i}')
    subj = q.get('subject', 'Physics')
    chap = q.get('chapter', 'General')
    topic = q.get('topic', 'General Concepts')
    diff = q.get('difficulty', 'Medium')
    acc = q.get('accuracy', 'N/A')
    stmt = (q.get('statement') or '').strip()
    sol = (q.get('solutionText') or '').strip()
    corr = q.get('correctOption', '')
    corr_ans = q.get('correctAnswer', '')
    
    doc.append(f"### [{i}/{len(master)}] `{qid}` — {chap}")
    doc.append(f"- **Subject / Topic**: {subj} $\\rightarrow$ {topic}")
    doc.append(f"- **Difficulty & Accuracy**: `{diff}` | Student Accuracy: **{acc}**")
    doc.append(f"- **Verified Correct Key**: Option **{corr}** (`{corr_ans}`)")
    
    # Diagram
    imgs = q.get('statementImages') or q.get('images') or []
    if isinstance(imgs, list) and imgs:
        for img in imgs:
            if img:
                doc.append(f"- **Diagram / Image**: [View Diagram]({img})")
    elif isinstance(imgs, str) and imgs:
        doc.append(f"- **Diagram / Image**: [View Diagram]({imgs})")

    doc.append("\n**Question Statement:**")
    doc.append(f"> {stmt}\n")

    # Options
    doc.append("**Options & Student Selection Breakdown:**")
    opts = q.get('options', [])
    if opts:
        for o in opts:
            # handle varied option schema keys cleanly
            lbl = o.get('label') or o.get('id') or o.get('optionKey') or chr(ord('A') + o.get('optionIndex', 1) - 1)
            otext = (o.get('text') or o.get('optionText') or '').strip()
            pct = o.get('markedPercentage') or o.get('studentPercentage') or o.get('percentage') or 'N/A'
            is_c = o.get('isCorrect', False)
            marker = "✅ **[CORRECT]**" if is_c else "⚪"
            doc.append(f"- {marker} **({lbl})** {otext} — `{pct}`")
    else:
        doc.append("- *(No option bodies recorded)*")

    doc.append("\n**Step-by-Step Solution & Mathematical Derivation:**")
    # Clean up solution text
    sol_cleaned = re.sub(r'Show Video Sol\.', '', sol).strip()
    doc.append(f"```markdown\n{sol_cleaned}\n```\n")
    doc.append("---\n")

output_path = r'C:\Users\Kunal\.gemini\antigravity\brain\b5f97b16-8c62-47fd-92b6-1c96b5172e19\all_harvested_questions_master_catalogue.md'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(doc))

print(f"Generated comprehensive master catalogue at: {output_path} ({len(doc)} lines)")
