import csv
import json
import re

def parse_steps(actions_str, results_str, data_str):
    # Regex to match `1. "text"` or `1. ""`
    pattern = re.compile(r'\d+\.\s*"([^"]*)"')
    actions = pattern.findall(actions_str)
    results = pattern.findall(results_str) if results_str else []
    data = pattern.findall(data_str) if data_str else []
    
    steps = []
    for i in range(len(actions)):
        step = {
            "action": actions[i].replace("<br>", "\n"),
            "expected_result": results[i].replace("<br>", "\n") if i < len(results) else "",
            "data": data[i].replace("<br>", "\n") if i < len(data) else ""
        }
        steps.append(step)
    return steps

with open('my-lessons.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if not row[0]: continue
        v2_id = row[0]
        title = row[1]
        steps_actions = row[15]
        steps_result = row[16]
        steps_data = row[17]
        steps = parse_steps(steps_actions, steps_result, steps_data)
        print(f"ID: {v2_id}")
        print(json.dumps(steps, indent=2))
        break
