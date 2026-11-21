import os
import json

out_dir = r"C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\browser_sandbox\outputs"
step_nums = [474, 476, 481, 483, 485, 487, 489, 491, 493, 495, 497, 499, 501, 503, 505]

for s in step_nums:
    fpath = os.path.join(out_dir, f"step_{s}.json")
    if os.path.exists(fpath):
        d = json.load(open(fpath, encoding="utf-8"))
        v = d.get("value", {})
        if isinstance(v, dict):
            print(f"Step {s}: ok={d.get('ok')}, keys={list(v.keys())}")
            for k, sub_v in v.items():
                if isinstance(sub_v, dict):
                    print(f"  {k}: correct={sub_v.get('correct_option') or sub_v.get('correct_options')}, stmt={sub_v.get('statement', '')[:40]}")
        else:
            print(f"Step {s}: ok={d.get('ok')}, val={v}")
