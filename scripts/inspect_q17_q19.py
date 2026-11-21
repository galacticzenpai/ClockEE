import json

for s in [571, 575]:
    try:
        with open(rf'C:\Users\Kunal\.gemini\antigravity\brain\3902ce56-16d8-420d-a385-168b9ff5615b\browser_sandbox\outputs\step_{s}.json', 'r', encoding='utf-8') as f:
            d = json.load(f)
        val = d.get('value', {})
        print(f"=== STEP {s} ===")
        for qk, qv in val.items():
            print(f"[{qk}]")
            print("  Text:", qv.get('quesText'))
            print("  Difficulty:", qv.get('difficulty'))
            print("  Student%:", qv.get('studentPercentage'))
            print("  Video:", qv.get('videoSrc'))
            for idx, opt in enumerate(qv.get('options', [])):
                print(f"    Opt {idx}: correct={opt.get('isCorrect')} | {opt.get('text')}")
    except Exception as e:
        print(f"Error {s}: {e}")
