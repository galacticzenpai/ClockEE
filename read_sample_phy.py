import json

with open('sorted_physics_questions.json', 'r', encoding='utf-8') as f:
    phy = json.load(f)

print("Total phy questions:", len(phy))
print("\nSample 1 (MCQ):")
print(json.dumps(phy[0], indent=2)[:800])
print("\nSample 2 (NAT):")
for q in phy:
    if q.get('section') == 'B' or q.get('type') in ['NUMERICAL', 'numerical']:
        print(json.dumps(q, indent=2)[:800])
        break
