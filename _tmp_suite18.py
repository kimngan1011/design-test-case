import json

files = [
    '/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/4d376f18-7d39-4616-974e-87de78a1e110/toolu_01XvFc1MaxgZ6ixeKSWesWCk__vscode-1774492196331/content.json',
    '/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/4d376f18-7d39-4616-974e-87de78a1e110/toolu_01Rgxjq4RtEuwDSDgULkAN4j__vscode-1774492196334/content.json',
    '/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/4d376f18-7d39-4616-974e-87de78a1e110/toolu_01SZ9q5ZRWxkctfaNxhqNR6q__vscode-1774492196341/content.json',
    '/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/4d376f18-7d39-4616-974e-87de78a1e110/toolu_01HMFXCVDTn9rwGoWGEnmULB__vscode-1774492196344/content.json',
    '/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/4d376f18-7d39-4616-974e-87de78a1e110/toolu_0117NAWab7nF9umu11CxUmNj__vscode-1774492196347/content.json',
    '/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/4d376f18-7d39-4616-974e-87de78a1e110/toolu_01M1iDyQfUnUPNHmJkD3EN5A__vscode-1774492196350/content.json',
    '/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/4d376f18-7d39-4616-974e-87de78a1e110/toolu_01UU3fK81z7f77Qf7FYD8bw5__vscode-1774492196355/content.json',
    '/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/4d376f18-7d39-4616-974e-87de78a1e110/toolu_01UtKDetknPEG4DWyzRLjrEe__vscode-1774492196358/content.json',
    '/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/4d376f18-7d39-4616-974e-87de78a1e110/toolu_01GQRVNJeEK5hWjZrqPNDSmr__vscode-1774492196361/content.json',
    '/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/4d376f18-7d39-4616-974e-87de78a1e110/toolu_01MTcxbTBnP8xyP7wgucVk86__vscode-1774492196364/content.json',
    '/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/4d376f18-7d39-4616-974e-87de78a1e110/toolu_013uafsJUZSCx6MzfuXykTe4__vscode-1774492196367/content.json',
    '/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/4d376f18-7d39-4616-974e-87de78a1e110/toolu_01L9up5j7vdctHAWcQkRhhkY__vscode-1774492196370/content.json',
    '/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/4d376f18-7d39-4616-974e-87de78a1e110/toolu_01U5wZQ5xMUHiR1725ZGMKzs__vscode-1774492196373/content.json',
    '/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/4d376f18-7d39-4616-974e-87de78a1e110/toolu_017efcuAVF9QogybvdFxg7sy__vscode-1774492196376/content.json',
    '/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/4d376f18-7d39-4616-974e-87de78a1e110/toolu_017cgB7C9n5GerskzU32Bm6D__vscode-1774492196379/content.json',
]

all_suites = []
for f in files:
    with open(f) as fh:
        data = json.load(fh)
    all_suites.extend(data['entities'])

def get_descendants(suites, parent_id):
    children = [s for s in suites if s['parent_id'] == parent_id]
    result = list(children)
    for child in children:
        result.extend(get_descendants(suites, child['id']))
    return result

descendants = get_descendants(all_suites, 18)
print(f"All suites loaded: {len(all_suites)}")
print(f"Descendants of suite 18: {len(descendants)}")
for s in sorted(descendants, key=lambda x: x['id']):
    print(f"  ID={s['id']} parent={s['parent_id']} cases={s['cases_count']} | {s['title']}")

# IDs in page 2 that are new descendants
desc_ids = {s['id'] for s in descendants}
new_in_page2 = [s for s in all_suites[100:] if s['id'] in desc_ids]
print(f"\nNew descendants in page 2: {new_in_page2}")
