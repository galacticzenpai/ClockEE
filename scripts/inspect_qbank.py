import json

with open('cbt_question_bank.json', 'r', encoding='utf-8', errors='ignore') as f:
    data = json.load(f)

print("Type of data:", type(data))
if isinstance(data, list):
    print("Total questions in bank:", len(data))
    if data:
        print("Sample keys:", list(data[0].keys()))
        print("Sample question 0:", json.dumps(data[0], indent=2)[:500])
elif isinstance(data, dict):
    print("Keys in data:", list(data.keys()))
    for k in list(data.keys())[:5]:
        val = data[k]
        if isinstance(val, list):
            print(f"Key '{k}' list length: {len(val)}")
        else:
            print(f"Key '{k}' type: {type(val)}")
