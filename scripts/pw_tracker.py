#!/usr/bin/env python3
"""
PW Extraction Live Tracker
Prints real-time stats on the question bank and PW extracted master
"""
import json, os
from datetime import datetime
from collections import Counter

BANK   = r"D:\Desktop\New folder\cbt_question_bank.json"
PW_EXT = r"D:\Desktop\New folder\pw_extracted_master.json"

def fmt(n): return f"{n:,}"

def run():
    print(f"\n{'='*60}")
    print(f"  ClockEE Question Bank Live Tracker — {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*60}")

    # Master bank
    if os.path.exists(BANK):
        data = json.load(open(BANK, encoding='utf-8'))
        qs = data if isinstance(data, list) else data.get('questions', [])
        subj = Counter(q.get('subject','?') for q in qs)
        src  = Counter(q.get('source','?') for q in qs)
        print(f"\n📚 MASTER BANK: {fmt(len(qs))} questions  ({round(os.path.getsize(BANK)/1e6,1)} MB)")
        for s,c in sorted(subj.items()):
            print(f"   {s:<15} {fmt(c):>6}")
        print(f"\n   Sources:")
        for s,c in sorted(src.items(), key=lambda x:-x[1]):
            print(f"   {s:<30} {fmt(c):>6}")
    else:
        print("  [!] Master bank not found")

    # PW extracted
    if os.path.exists(PW_EXT):
        data = json.load(open(PW_EXT, encoding='utf-8'))
        ch = Counter(q.get('chapter','?') for q in data)
        subj2 = Counter(q.get('subject','?') for q in data)
        print(f"\n🔍 PW EXTRACTED: {fmt(len(data))} questions")
        for s,c in sorted(subj2.items()):
            print(f"   {s:<15} {fmt(c):>6}")
        print(f"\n   Chapter breakdown:")
        for k,v in sorted(ch.items()):
            bar = '█' * min(v, 50) + f' {v}'
            print(f"   {k:<45} {bar}")
    else:
        print("  [!] PW extracted file not found")

    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    import sys, time
    if '--watch' in sys.argv:
        while True:
            run()
            time.sleep(30)
    else:
        run()
