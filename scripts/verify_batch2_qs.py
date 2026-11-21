import json

# Inspect all questions in Batch 2 (Q21 to Q40)
step_mappings = [
    (581, 'q21'),
    (585, 'q22'),
    (585, 'q23'),
    (583, 'q24'),
    (587, 'q25'),
    (587, 'q26'),
    (589, 'q27'),
    (589, 'q28'),
    (591, 'q29'),
    (591, 'q30'),
    (593, 'q31'),
    (593, 'q32'),
    (595, 'q33'),
    (595, 'q34'),
    (597, 'q35'),
    (597, 'q36'),
    (599, 'q37'),
    (599, 'q38'),
    (604, 'q39'),
    (604, 'q40')
]

for s, qk in step_mappings:
    p = rf'C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\browser_sandbox\outputs\step_{s}.json'
    try:
        with open(p, 'r', encoding='utf-8') as f:
            d = json.load(f)
        val = d.get('value', {})
        if qk in val:
            qv = val[qk]
            txt = qv.get('quesText', '')[:60].replace('\n', ' ')
            opts = len(qv.get('options', []))
            corr = [i for i, o in enumerate(qv.get('options', [])) if o.get('isCorrect')]
            print(f"{qk} (from step_{s}): opts={opts}, corr={corr}, text={txt}")
        else:
            print(f"{qk} not in step_{s} value keys: {list(val.keys()) if isinstance(val, dict) else type(val)}")
    except Exception as e:
        print(f"Error reading step_{s}: {e}")
