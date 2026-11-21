import os
import json

out_dir = r"C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\browser_sandbox\outputs"
steps = [403, 405, 407, 409, 411, 413, 415, 417, 419, 421, 423, 425, 427]

for s in steps:
    fpath = os.path.join(out_dir, f"step_{s}.json")
    if os.path.exists(fpath):
        d = json.load(open(fpath, encoding="utf-8"))
        val = d.get("value")
        print(f"Step {s}: ok={d.get('ok')}")
        if isinstance(val, dict):
            print(f"  keys: {list(val.keys())}")
        elif isinstance(val, list):
            print(f"  list count: {len(val)}")
        else:
            print(f"  val: {val}")
