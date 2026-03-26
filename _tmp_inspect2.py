#!/usr/bin/env python3
import json, re

DATA_FILE = '/Users/manabie/Library/Application Support/Code/User/workspaceStorage/c6d55808ef8e9cd506d8bc5970c3e4d1/GitHub.copilot-chat/chat-session-resources/bbb5c426-3169-47c7-a275-441c38312062/toolu_vrtx_016BoCKU8utQ4Qo3qHQWEGfK__vscode-1774414256511/content.json'
with open(DATA_FILE) as f:
    page_data = json.load(f)
body = page_data['bodyStorageValue']

marker_pos = body.find("Acceptance Test Coverage Summary")
table_start = body.find('<table', marker_pos)

pos = table_start
depth = 0
outer_tr_positions = []
i = pos

while i < len(body):
    if body[i:i+6] == '<table':
        depth += 1
        i += 6
        continue
    if body[i:i+8] == '</table>':
        depth -= 1
        if depth == 0:
            break
        i += 8
        continue
    if depth == 1 and body[i:i+3] == '<tr':
        tr_start = i
        j = i + 3
        tr_depth = 0
        while j < len(body):
            if body[j:j+6] == '<table':
                tr_depth += 1
                j += 6
                continue
            if body[j:j+8] == '</table>':
                tr_depth -= 1
                j += 8
                continue
            if tr_depth == 0 and body[j:j+5] == '</tr>':
                tr_end = j + 5
                outer_tr_positions.append((tr_start, tr_end))
                i = tr_end
                break
            j += 1
        else:
            i += 1
        continue
    i += 1

# Show ALL cells of rows 7-12 to understand the structure
for idx in range(7, min(14, len(outer_tr_positions))):
    tr_s, tr_e = outer_tr_positions[idx]
    tr_html = body[tr_s:tr_e]
    # Count <td> elements
    tds = re.findall(r'<td[^>]*>(.*?)</td>', tr_html, re.DOTALL)
    # Strip HTML for display
    cells = []
    for td in tds:
        clean = re.sub(r'<[^>]+>', '', td).strip()
        cells.append(clean[:50])
    print(f"Row {idx} ({len(tds)} cells): {cells}")
    # Also check for rowspan/colspan
    spans = re.findall(r'(rowspan|colspan)="(\d+)"', tr_html)
    if spans:
        print(f"  Spans: {spans}")
    # Check for PBT references
    if 'PBT-' in tr_html:
        pbt = re.search(r'PBT-\d+', tr_html)
        if pbt:
            print(f"  Contains: {pbt.group()}")

print("\n--- Row 0 (header) ---")
tr_s, tr_e = outer_tr_positions[0]
tr_html = body[tr_s:tr_e]
tds = re.findall(r'<td[^>]*>(.*?)</td>', tr_html, re.DOTALL)
headers = [re.sub(r'<[^>]+>', '', td).strip()[:30] for td in tds]
print(f"Headers: {headers}")
