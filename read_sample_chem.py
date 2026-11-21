import json

with open('sorted_chemistry_questions.json', 'r', encoding='utf-8') as f:
    chem = json.load(f)

print("Total chem questions:", len(chem))
print("\nSample 1 (MCQ):")
print(json.dumps(chem[0], indent=2))
print("\nSample 2 (NAT):")
for q in chem:
    if q.get('type') == 'numerical':
        print(json.dumps(q, indent=2))
        break
