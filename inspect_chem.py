import json

with open("pw_extracted_master.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== Item 101 ===")
print(json.dumps(data[101], indent=2))
print("=== Item 106 ===")
print(json.dumps(data[106], indent=2))
