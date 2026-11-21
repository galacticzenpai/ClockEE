import json

with open("pw_extracted_master.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== Item 91 ===")
print(json.dumps(data[91], indent=2))
print("=== Item 95 ===")
print(json.dumps(data[95], indent=2))
