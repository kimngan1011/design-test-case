import json, sys

with open(sys.argv[1]) as f:
    d = json.load(f)

# Extract unique case IDs
cases = {}
for r in d.get('entities', []):
    cid = r.get('case_id')
    if cid and cid not in cases:
        cases[cid] = r.get('status_text', '')

print(f"Unique cases: {len(cases)}")
for cid, status in sorted(cases.items()):
    print(f"  case_id={cid} status={status}")
