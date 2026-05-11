#!/usr/bin/env python3
"""
Scan all test cases under suite 248 (Lesson on BO) for literal backslash-n issues,
then fix them by replacing with actual newline characters.
"""

import json
import time
import urllib.request
import urllib.error

API_TOKEN = "7089c6bc3cac41f13fade01682726c8e3a6f70c5bfaae5df925f4188c12460a6"
PROJECT_CODE = "PX"
BASE_URL = "https://api.qase.io/v1"
ROOT_SUITE_ID = 248
LITERAL_BN = chr(92) + "n"  # literal backslash + n


def api_get(path, retries=3):
    url = f"{BASE_URL}{path}"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"Token": API_TOKEN})
            with urllib.request.urlopen(req, timeout=60) as resp:
                return json.loads(resp.read())
        except Exception as e:
            if attempt < retries - 1:
                wait = 2 ** attempt
                print(f"    Retry {attempt+1}/{retries} after {wait}s (error: {e})")
                time.sleep(wait)
            else:
                raise


def fetch_all_suites():
    all_suites = {}
    offset = 0
    total = None
    while True:
        data = api_get(f"/suite/{PROJECT_CODE}?limit=100&offset={offset}")
        result = data["result"]
        if total is None:
            total = result["total"]
        for s in result["entities"]:
            all_suites[s["id"]] = s
        offset += 100
        if offset >= total:
            break
    return all_suites


def get_descendants(root_id, all_suites):
    result = [root_id]
    queue = [root_id]
    while queue:
        current = queue.pop(0)
        children = [s for s in all_suites.values() if s.get("parent_id") == current]
        for child in children:
            result.append(child["id"])
            queue.append(child["id"])
    return result


def fetch_cases_for_suite(suite_id):
    cases = []
    offset = 0
    total = None
    while True:
        data = api_get(f"/case/{PROJECT_CODE}?suite_id={suite_id}&limit=100&offset={offset}")
        result = data["result"]
        if total is None:
            total = result["total"]
        cases.extend(result["entities"])
        offset += 100
        if offset >= total:
            break
        time.sleep(0.1)
    return cases


def has_issue(case):
    for field in ["preconditions", "description", "postconditions"]:
        if LITERAL_BN in (case.get(field) or ""):
            return True
    for step in (case.get("steps") or []):
        for f in ["action", "expected_result", "data"]:
            if LITERAL_BN in (step.get(f) or ""):
                return True
    return False


def fix_case(case):
    """Returns dict of only fields that changed."""
    updates = {}
    for field in ["preconditions", "description", "postconditions"]:
        text = case.get(field) or ""
        if LITERAL_BN in text:
            updates[field] = text.replace(LITERAL_BN, "\n")
    
    new_steps = []
    steps_changed = False
    for step in (case.get("steps") or []):
        new_step = dict(step)
        for f in ["action", "expected_result", "data"]:
            text = step.get(f) or ""
            if LITERAL_BN in text:
                new_step[f] = text.replace(LITERAL_BN, "\n")
                steps_changed = True
        new_steps.append(new_step)
    if steps_changed:
        updates["steps"] = new_steps
    
    return updates


def update_case(case_id, updates):
    url = f"{BASE_URL}/case/{PROJECT_CODE}/{case_id}"
    payload = json.dumps(updates).encode("utf-8")
    req = urllib.request.Request(
        url, data=payload, method="PATCH",
        headers={"Token": API_TOKEN, "Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            return result.get("status", False)
    except urllib.error.HTTPError as e:
        print(f"    HTTP {e.code}: {e.read().decode()[:200]}")
        return False
    except Exception as e:
        print(f"    Error: {e}")
        return False


def main():
    print("Step 1: Fetching all suites...")
    all_suites = fetch_all_suites()
    print(f"  Loaded {len(all_suites)} suites")

    print(f"\nStep 2: Finding descendants of suite {ROOT_SUITE_ID}...")
    suite_ids = get_descendants(ROOT_SUITE_ID, all_suites)
    print(f"  Found {len(suite_ids)} suites (including root): {suite_ids}")

    print("\nStep 3: Fetching all test cases...")
    all_cases = {}
    for sid in suite_ids:
        cases = fetch_cases_for_suite(sid)
        for c in cases:
            all_cases[c["id"]] = c
        suite_name = all_suites.get(sid, {}).get("title", "?")
        print(f"  Suite {sid} '{suite_name}': {len(cases)} cases")
        time.sleep(0.1)

    print(f"\nTotal unique cases: {len(all_cases)}")

    print("\nStep 4: Scanning for literal \\n issues...")
    issues = [(cid, case) for cid, case in all_cases.items() if has_issue(case)]
    print(f"  Cases with issues: {len(issues)}")
    for cid, case in issues:
        print(f"  - Case {cid} (suite {case.get('suite_id')}): {case['title'][:70]}")

    if not issues:
        print("\nNo issues found. Nothing to fix.")
        return

    print(f"\nStep 5: Fixing {len(issues)} cases...")
    success = 0
    failed = []
    for i, (cid, case) in enumerate(issues, 1):
        updates = fix_case(case)
        print(f"[{i}/{len(issues)}] Fixing case {cid}: {case['title'][:60]}")
        ok = update_case(cid, updates)
        if ok:
            success += 1
            print(f"    ✓ Fixed ({list(updates.keys())})")
        else:
            failed.append(cid)
            print(f"    ✗ Failed")
        time.sleep(0.2)

    print(f"\n{'='*50}")
    print(f"Done! Fixed: {success}/{len(issues)}")
    if failed:
        print(f"Failed IDs: {failed}")


if __name__ == "__main__":
    main()
