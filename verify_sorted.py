import json

with open("sorted_chemistry_questions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total questions in sorted file: {len(data)}")

# Verify schema on all items
required_keys = ["id", "subject", "chapter", "topic", "difficulty", "idealTimeSec", "text", "options", "correct", "accuracyPct", "solution"]

missing_keys_count = 0
time_out_of_bounds = 0
for idx, q in enumerate(data):
    for k in required_keys:
        if k not in q:
            missing_keys_count += 1
            print(f"Missing key {k} in item {idx}")
    if not (45 <= q["idealTimeSec"] <= 120):
        time_out_of_bounds += 1

print(f"Missing required keys count: {missing_keys_count}")
print(f"Ideal times outside 45-120s: {time_out_of_bounds}")

# Sample single choice question
scq = next(q for q in data if q["type"] == "single")
print("\n=== SAMPLE SINGLE CHOICE QUESTION ===")
print(json.dumps(scq, indent=2)[:1000])

# Sample numerical question
nat = next(q for q in data if q["type"] == "numerical")
print("\n=== SAMPLE NUMERICAL QUESTION ===")
print(json.dumps(nat, indent=2)[:1000])
