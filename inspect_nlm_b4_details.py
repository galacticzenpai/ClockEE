import json
import re

with open("pw_extracted_master.json", "r", encoding="utf-8") as f:
    master = json.load(f)

nlm_b4 = [q for q in master if q.get("id", "").startswith("PW_PHY_NLM_") and int(q.get("id").split("_")[-1]) >= 61]

for q in nlm_b4:
    qid = q["id"]
    stmt = q["statement"]
    # Check if statement contains 'Marked this option'
    has_marked = "Marked this option" in stmt
    opts = q.get("options", [])
    opt_texts = [opt.get("text", "") for opt in opts]
    print(f"{qid}: has_marked={has_marked}, opts_len={len(opts)}, opt_texts={opt_texts[:4]}")
