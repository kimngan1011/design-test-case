import json, sys
from collections import defaultdict

FILES = [
    "/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/a0130267-94ef-4560-863f-44717aa0905b/toolu_013XWWigFXBRzTkEjMtuf8hr__vscode-1774249236683/content.json",
    "/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/a0130267-94ef-4560-863f-44717aa0905b/toolu_01V6kiigGUGFBrkBAQ5ZHo6B__vscode-1774249236710/content.json",
    "/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/a0130267-94ef-4560-863f-44717aa0905b/toolu_01WWCFsaAre4Wm7XQQHRHoZW__vscode-1774249236711/content.json",
]

entries = []
for f_path in FILES:
    with open(f_path) as f:
        data = json.load(f)
    entries.extend(data['entities'])

# Build result map: case_id -> list of entries sorted by end_time ascending
case_map = defaultdict(list)
for e in entries:
    case_map[e['case_id']].append(e)

for cid in case_map:
    case_map[cid].sort(key=lambda x: x.get('end_time') or '')

flaky = []
failed = []
clean_pass = []

for cid, runs in sorted(case_map.items()):
    final = runs[-1]
    history = [r['status'] for r in runs]
    final_status = final['status']
    retries = len(runs) - 1
    md_url = next((a['url'] for a in final.get('attachments', []) if a['filename'] == 'step-results.md'), None)
    time_ms = final.get('time_spent_ms', 0)

    entry = {
        'case_id': cid,
        'final_status': final_status,
        'history': history,
        'retries': retries,
        'time_ms': time_ms,
        'md_url': md_url,
        'end_time': final.get('end_time')
    }

    has_failure = any(s in ('failed', 'invalid', 'blocked') for s in history)

    if final_status in ('failed', 'invalid', 'blocked'):
        failed.append(entry)
    elif retries > 0 and final_status == 'passed' and has_failure:
        # True flaky: had at least one failure before passing
        # Also grab the first failed attempt's md_url for evidence
        failed_runs = [r for r in runs if r['status'] in ('failed', 'invalid')]
        first_fail = failed_runs[0] if failed_runs else None
        entry['fail_md_url'] = next((a['url'] for a in first_fail.get('attachments', []) if a['filename'] == 'step-results.md'), None) if first_fail else None
        entry['fail_status'] = first_fail['status'] if first_fail else None
        flaky.append(entry)
    else:
        # All-pass history (parallel runs) or truly clean
        clean_pass.append(entry)

print(f"Total unique cases: {len(case_map)}")
print(f"Failed/Invalid (final): {len(failed)}")
print(f"Truly flaky (had failures before passing): {len(flaky)}")
print(f"Clean pass (no failures ever): {len(clean_pass)}")

print()
print("--- TRULY FLAKY (sorted by retry count desc) ---")
for e in sorted(flaky, key=lambda x: -x['retries']):
    print(f"  case {e['case_id']}: retries={e['retries']} | history={e['history']}")
    print(f"    fail_url={e['fail_md_url']}")
