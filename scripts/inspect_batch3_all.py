import json

steps = [
    (640, 'q41'), (640, 'q42'),
    (644, 'q43'), (644, 'q44'),
    (646, 'q45'), (646, 'q46'),
    (648, 'q47'), (648, 'q48'),
    (650, 'q49'), (650, 'q50'),
    (652, 'q51'), (652, 'q52'),
    (654, 'q53'), (654, 'q54'),
    (658, 'q55'), (658, 'q56'),
    (660, 'q57'), (660, 'q58'),
    (664, 'q59'), (664, 'q60')
]

for s, qk in steps:
    p = rf'C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\browser_sandbox\outputs\step_{s}.json'
    try:
        with open(p, 'r', encoding='utf-8') as f:
            d = json.load(f)
        val = d.get('value', {})
        if qk in val:
            qv = val[qk]
            txt = qv.get('quesText', '')
            corr = [i for i, o in enumerate(qv.get('options', [])) if o.get('isCorrect')]
            opts = [(o.get('text', ''), o.get('isCorrect'), o.get('percentage', '')) for o in qv.get('options', [])]
            print(f"=== {qk} (step_{s}) ===")
            print("  Statement:", txt[:100])
            print("  Correct:", corr)
            print("  Video:", qv.get('videoSrc', ''))
            print("  Options count:", len(opts))
            for idx, opt in enumerate(opts):
                print(f"    Opt {idx}: correct={opt[1]} | {opt[0][:40]}")
    except Exception as e:
        print(f"Error {s} {qk}: {e}")
