import json, os
from collections import defaultdict

# Explicit result file paths (re-fetched)
result_files = [
    "/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/a0130267-94ef-4560-863f-44717aa0905b/toolu_01WS31HhegWt7Ro19wZuYQRh__vscode-1774249236749/content.json",
    "/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/a0130267-94ef-4560-863f-44717aa0905b/toolu_01N74MzBrxCCeAZrhNceGXmj__vscode-1774249236750/content.json",
    "/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/a0130267-94ef-4560-863f-44717aa0905b/toolu_01FQmAhvbcUHqqTb7RKo9VGN__vscode-1774249236751/content.json",
]
CDN = "https://d2cxucsjd6xvsd.cloudfront.net/public/team/b5f684e60ab1a64567fb280d07faed2c4132e041/attachment"

all_results = []
for fpath in result_files:
    with open(fpath) as f:
        data = json.load(f)
    # Top-level entities
    entities = data.get("entities", [])
    # Nested under result
    if not entities and "result" in data:
        entities = data["result"].get("entities", [])
    if entities and isinstance(entities[0], dict) and "hash" in entities[0]:
        all_results.extend(entities)

print(f"Total loaded: {len(all_results)}")

case_map = defaultdict(list)
for r in all_results:
    cid = r.get("case_id")
    if cid:
        case_map[cid].append(r)

def get_md_url(result):
    for att in result.get("attachments", []):
        if att.get("filename") == "step-results.md":
            # New format: direct URL
            if "url" in att:
                return att["url"]
            # Old format: hash-based
            if "hash" in att:
                return f"{CDN}/{att['hash']}/step-results.md"
    return None

target_cases = [9678, 9677, 9674, 1015, 1022, 1216, 3391, 3510, 8493, 1013, 1014, 9672, 749, 3772]

print("\n--- FINAL PASS step-results.md URLs ---")
for cid in target_cases:
    results = sorted(case_map[cid], key=lambda r: r.get("end_time", ""))
    final = results[-1]
    url = get_md_url(final)
    status = final.get("status")
    print(f"  case {cid}: final_status={status}")
    print(f"    pass_url={url}")

print("\n--- CLEAN PASS sample (8 cases) ---")
clean = []
for cid, results in case_map.items():
    sorted_r = sorted(results, key=lambda r: r.get("end_time",""))
    all_statuses = [r.get("status") for r in sorted_r]
    if all(s == "passed" for s in all_statuses) and cid not in target_cases:
        clean.append((cid, sorted_r[-1]))

for cid, r in clean[:8]:
    url = get_md_url(r)
    print(f"  case {cid}:")
    print(f"    pass_url={url}")
