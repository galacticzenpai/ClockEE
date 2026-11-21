import json
import re

with open('pw_extracted_master.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

with open('sorted_physics_questions.json', 'r', encoding='utf-8') as f:
    sorted_qs = json.load(f)

existing_orig_ids = set(q.get('originalId') for q in sorted_qs)
new_qs = [q for q in master if q.get('subject', '').lower() == 'physics' and q.get('id') not in existing_orig_ids]

print(f"Total new questions in Batch 4: {len(new_qs)}")

def clean_opt_text(t):
    if not t:
        return ""
    t = str(t)
    t = re.sub(r'---\s*Both Chapter.*', '', t, flags=re.DOTALL)
    t = re.sub(r'---\s*Current progress:.*', '', t, flags=re.DOTALL)
    t = re.sub(r'</SYSTEM_MESSAGE>.*', '', t, flags=re.DOTALL)
    t = re.sub(r'\s*\[[\d\.]+%\]', '', t)
    t = re.sub(r'\s*\[Wait.*?\]', '', t)
    t = t.replace('\xa0', ' ')
    return t.strip()

for i, q in enumerate(new_qs):
    raw_opts = q.get('options', [])
    opt_texts = [clean_opt_text(o.get('optionText') or o.get('text')) for o in raw_opts if o]
    
    # Filter out empty or None
    opt_texts = [o for o in opt_texts if o and o != 'None']
    
    # Check if first element is an artifact header
    if len(opt_texts) >= 5 and ('Options' in opt_texts[0] or 'options' in opt_texts[0] or len(opt_texts[0]) > 35):
        cleaned_opts = opt_texts[1:5]
    elif len(opt_texts) >= 5:
        # Check if 5th element is an explanation or trailing artifact
        cleaned_opts = opt_texts[:4]
    else:
        cleaned_opts = opt_texts[:4]
        
    print(f"\nQ{i+61}: {q.get('id')} -> CorrectOption={q.get('correctOption')}")
    print(f"Stmt: {q.get('statement')[:70]}...")
    print(f"Cleaned Opts ({len(cleaned_opts)}): {cleaned_opts}")
    print(f"Sol: {q.get('solutionText')[:100]}...")
