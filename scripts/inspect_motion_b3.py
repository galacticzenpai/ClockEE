import os
import json

out_dir = r"C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\browser_sandbox\outputs"
for s in [456, 458, 460, 462, 464, 466, 468]:
    fpath = os.path.join(out_dir, f"step_{s}.json")
    if os.path.exists(fpath):
        d = json.load(open(fpath, encoding="utf-8"))
        v = d.get("value", {})
        print(f"Step {s}: ok={d.get('ok')}, keys={list(v.keys()) if isinstance(v, dict) else len(v)}")
        if isinstance(v, dict):
            for k, sub_v in v.items():
                if isinstance(sub_v, dict):
                    print(f"  {k}: correct={sub_v.get('correct_option') or sub_v.get('correct_options')}, stmt={sub_v.get('statement', '')[:50]}")
