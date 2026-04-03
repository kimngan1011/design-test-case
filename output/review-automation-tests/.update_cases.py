#!/usr/bin/env python3
"""Scan all 117 run cases and update any with automation != 2."""
import urllib.request
import json
import time

TOKEN = "7089c6bc3cac41f13fade01682726c8e3a6f70c5bfaae5df925f4188c12460a6"

# Full 117-case list
cases_to_update = [
    668, 673, 674, 675, 676, 708, 712, 713, 715, 717, 719, 731, 735, 736,
    737, 738, 739, 747, 748, 749, 750, 758, 759, 761, 786, 1013, 1014, 1015,
    1016, 1022, 1023, 1039, 1216, 1218, 1263, 1265, 1377, 1456, 1919, 3144,
    3155, 3170, 3171, 3172, 3173, 3178, 3391, 3396, 3495, 3498, 3506, 3510,
    3570, 3571, 3574, 3575, 3585, 3587, 3597, 3787, 6931, 8493, 8494, 8497,
    8498, 8501, 8502, 8509, 8510, 8513, 8514, 8517, 8518, 9672, 9673, 9674,
    9675, 9676, 9677, 9678, 9680, 9681, 9745, 9746, 9747, 9748, 9749, 9750,
    9752, 9753, 9754, 9755, 9756, 9757, 9763, 9764, 9765, 9766, 9767, 9768,
    9770, 9771, 9772, 9773, 9774, 9775, 9786, 9788, 9789, 9790, 9791, 11285,
    11538, 13747, 13748, 13749, 13750
]

def get_automation(case_id):
    url = f"https://api.qase.io/v1/case/PX/{case_id}"
    req = urllib.request.Request(url, headers={"Token": TOKEN})
    with urllib.request.urlopen(req, timeout=15) as r:
        d = json.loads(r.read())
    return d["result"]["automation"]

def update_automation(case_id):
    url = f"https://api.qase.io/v1/case/PX/{case_id}"
    data = json.dumps({"automation": 2}).encode()
    req = urllib.request.Request(url, data=data,
                                  headers={"Token": TOKEN, "Content-Type": "application/json"},
                                  method="PATCH")
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

print("Checking and updating cases...")
updated = []
skipped = []
failed = []

for case_id in cases_to_update:
    try:
        current = get_automation(case_id)
        if current == 2:
            print(f"PX-{case_id}: already automation=2, skip")
            skipped.append(case_id)
        else:
            result = update_automation(case_id)
            if result.get("status"):
                print(f"PX-{case_id}: updated to automation=2 ✓")
                updated.append(case_id)
            else:
                print(f"PX-{case_id}: update failed: {result}")
                failed.append(case_id)
        time.sleep(0.3)
    except Exception as e:
        print(f"PX-{case_id}: ERROR - {e}")
        failed.append(case_id)

print(f"\nSummary: Updated={len(updated)}, Skipped={len(skipped)}, Failed={len(failed)}")
print(f"Updated: {updated}")
print(f"Skipped: {skipped}")
if failed:
    print(f"Failed: {failed}")
