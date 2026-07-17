import csv
import json
import re
import urllib.request
import os

TOKEN = "7089c6bc3cac41f13fade01682726c8e3a6f70c5bfaae5df925f4188c12460a6"
HEADERS = {
    "Token": TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def parse_steps(actions_str, results_str, data_str):
    actions = actions_str.split('\n')
    results = results_str.split('\n') if results_str else []
    data = data_str.split('\n') if data_str else []
    
    steps = []
    max_len = max(len(actions), len(results), len(data))
    
    for i in range(max_len):
        act = actions[i] if i < len(actions) else ""
        res = results[i] if i < len(results) else ""
        dat = data[i] if i < len(data) else ""
        
        act = re.sub(r'^\d+\.\s*"', '', act)
        if act.endswith('"'): act = act[:-1]
        act = act.replace('""', '"')
        
        res = re.sub(r'^\d+\.\s*"', '', res)
        if res.endswith('"'): res = res[:-1]
        res = res.replace('""', '"')
        
        dat = re.sub(r'^\d+\.\s*"', '', dat)
        if dat.endswith('"'): dat = dat[:-1]
        dat = dat.replace('""', '"')
        
        if not act and not res and not dat:
            continue
            
        steps.append({
            "action": act.replace("<br>", "\n"),
            "expected_result": res.replace("<br>", "\n"),
            "data": dat.replace("<br>", "\n")
        })
    return steps

def update_case(v2_id, title, description, preconditions, priority, severity, steps):
    url = f"https://api.qase.io/v1/case/PX/{v2_id}"
    
    priority_map = {"high": 1, "medium": 2, "low": 3}
    severity_map = {"blocker": 1, "critical": 2, "major": 3, "normal": 4, "minor": 5, "trivial": 6}
    
    p_id = priority_map.get(priority.lower(), 2)
    s_id = severity_map.get(severity.lower(), 3)
    
    payload = {
        "title": title[:255] if title else "Untitled",
        "description": description,
        "preconditions": preconditions,
        "priority": p_id,
        "severity": s_id,
        "type": 2,
        "behavior": 1,
        "automation": 2,
        "status": 1,
        "layer": 1,
        "steps": steps
    }
    
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=HEADERS, method='PATCH')
    try:
        with urllib.request.urlopen(req) as res:
            print(f"✅ Updated {v2_id} - {title[:30]}...")
    except urllib.error.HTTPError as e:
        print(f"❌ Failed to update {v2_id}: HTTP {e.code} - {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"❌ Failed to update {v2_id}: {e}")

def process_file(filename):
    if not os.path.exists(filename):
        return
    print(f"\nProcessing {filename}...")
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if not row or not row[0]: continue
            v2_id = row[0]
            
            # pad row
            while len(row) < len(header):
                row.append("")
                
            title = row[1]
            description = row[2]
            preconditions = row[3]
            priority = row[6]
            severity = row[7]
            
            steps_actions_idx = header.index('steps_actions')
            steps_expected_idx = header.index('steps_expected') if 'steps_expected' in header else header.index('steps_expected_result') if 'steps_expected_result' in header else -1
            steps_data_idx = header.index('steps_data') if 'steps_data' in header else -1
            
            steps_actions = row[steps_actions_idx]
            steps_result = row[steps_expected_idx] if steps_expected_idx >= 0 else ""
            steps_data = row[steps_data_idx] if steps_data_idx >= 0 else ""
            
            steps = parse_steps(steps_actions, steps_result, steps_data)
            update_case(v2_id, title, description, preconditions, priority, severity, steps)

if __name__ == '__main__':
    process_file('book-lesson.csv')
    process_file('cancel-booking.csv')

