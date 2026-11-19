with open('mesh/clockee_tracker_source.html', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

import re

print("File size:", len(text))

funcs = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', text)
print("\n=== Functions in ClockEE Tracker ===")
for fn in funcs:
    print("-", fn)

ids = re.findall(r'id=["\']([a-zA-Z0-9_-]+)["\']', text)
print("\n=== Key Element IDs ===")
for i in set(ids):
    print("-", i)

# Look for data structures or fetch endpoints
endpoints = re.findall(r'fetch\([\'"`](.*?)[\'"`]\)', text)
print("\n=== Fetch Endpoints ===")
for ep in set(endpoints):
    print("-", ep)
