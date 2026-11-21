import json
import os

if os.path.exists('pw_extracted_master.json'):
    with open('pw_extracted_master.json', 'r', encoding='utf-8') as f:
        pw_data = json.load(f)
    print(f"Total questions in pw_extracted_master.json: {len(pw_data)}")
    subjects = {}
    for q in pw_data:
        s = q.get('subject', 'Unknown')
        subjects[s] = subjects.get(s, 0) + 1
    print("Subjects in pw_extracted_master.json:", subjects)
else:
    print("pw_extracted_master.json does not exist.")
