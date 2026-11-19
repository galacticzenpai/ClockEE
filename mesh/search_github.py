import os
import glob
import re

brain_dir = r"C:\Users\Kunal\.gemini\antigravity\brain"
pattern = re.compile(r'https?://github\.com/[a-zA-Z0-9_\-]+/[a-zA-Z0-9_\-]+', re.IGNORECASE)

found = set()
for root, dirs, files in os.walk(brain_dir):
    for f in files:
        if f in ('transcript.jsonl', 'transcript_full.jsonl'):
            fp = os.path.join(root, f)
            try:
                with open(fp, 'r', encoding='utf-8', errors='ignore') as infile:
                    for line in infile:
                        matches = pattern.findall(line)
                        for m in matches:
                            found.add(m)
            except Exception as e:
                pass

print("=== GITHUB LINKS FOUND ===")
for url in sorted(found):
    print(url)
