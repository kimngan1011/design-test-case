import json

FILE1 = "/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/383d2ac7-7b21-4725-ad68-655411f35fe6/toolu_vrtx_01JRAzMxSJeb8V1cxfSPTthL__vscode-1775200276084/content.json"
FILE2 = "/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/383d2ac7-7b21-4725-ad68-655411f35fe6/toolu_vrtx_015sRe1RYzraQccqcayXeefg__vscode-1775200276091/content.json"

all_entities = []
for fp in [FILE1, FILE2]:
    with open(fp) as f:
        d = json.load(f)
    all_entities.extend(d['entities'])

print(f"Total raw entries loaded: {len(all_entities)}")

# Deduplicate by case_id using latest end_time
latest = {}
retries = {}
for r in all_entities:
    cid = r['case_id']
    et = r.get('end_time', '')
    retries.setdefault(cid, []).append(r['status'])
    if cid not in latest or et > latest[cid]['end_time']:
        latest[cid] = {
            'case_id': cid,
            'status': r['status'],
            'end_time': et,
            'time_spent_ms': r.get('time_spent_ms', 0),
            'step_json_url': next((a['url'] for a in r.get('attachments', []) if a.get('filename') == 'step-results.json'), None),
            'step_count': len(r.get('steps', [])),
        }

print(f"Unique cases: {len(latest)}")
failed = {k: v for k, v in latest.items() if v['status'] == 'failed'}
passed_clean = {k: v for k, v in latest.items() if v['status'] == 'passed' and len(retries[k]) == 1}
passed_retry = {k: v for k, v in latest.items() if v['status'] == 'passed' and len(retries[k]) > 1}
print(f"Passed (clean): {len(passed_clean)}, Passed (after retry): {len(passed_retry)}, Failed: {len(failed)}")

print("\n=== FAILED CASES ===")
for k, v in failed.items():
    print(f"  case_id={k}  steps={v['step_count']}  end={v['end_time']}")
    print(f"    url={v['step_json_url']}")

print("\n=== FLAKY CASES (passed after retries) ===")
for cid, hist in retries.items():
    if len(hist) > 1 and latest[cid]['status'] == 'passed':
        print(f"  case_id={cid}  history={hist}")

print("\n=== ALL CASE IDs (sorted) ===")
print(sorted(latest.keys()))

print("\n=== FLAKY case URLs ===")
for cid in [9736, 3585, 9735]:
    v = latest.get(cid)
    if v:
        print(f"case_id={cid} status={v['status']} steps={v['step_count']}")
        print(f"  {v['step_json_url']}")
