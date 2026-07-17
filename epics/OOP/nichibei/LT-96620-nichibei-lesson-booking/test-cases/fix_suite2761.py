import csv
import re

def fix_csv():
    with open('lesson-lists.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    # 1. Browse Lessons -> Lesson Lists
    # 2. Add 'Tap Filter button' to filter cases
    # 3. Update Preconditions about LA Location Course

    filter_case_ids = ['20868', '20869', '20870', '20871', '20872', '20873', '20874']
    
    for row in rows:
        if not row[0]: continue
        v2_id = row[0]
        
        # 1. Browse Lessons -> Lesson Lists
        row[3] = row[3].replace("Browse Lessons", "Lesson Lists")
        row[15] = row[15].replace("Browse Lessons", "Lesson Lists")
        
        # 3. Location of LA -> Location of LA's Location Course
        # If it says "Student user has active LA for Location A", change to "Student user has an active LA. The LA's Location Course is at Location A"
        row[3] = row[3].replace("active LA for Location A", "active LA linked to a Location Course for Location A")
        # In TC 20868: "Student user has active LA for Location A only."
        row[3] = row[3].replace("student's LA location", "student's LA's Location Course location")
        
        # 2. Filter cases: Add opening filter screen
        if v2_id in filter_case_ids:
            # Add "Tap Filter button to open Filter screen" to action 2 if not there
            # Since actions are strings like "1. ""...""\n2. ""...""\n3. ""..."""
            actions = row[15].split('\n')
            results = row[16].split('\n')
            data = row[17].split('\n')
            
            if '20868' == v2_id:
                # [Nichibei] Lesson Booking – Location Filter – Only student's LA's Location Course locations shown
                # Old Action 2: "Open the Location filter dropdown"
                if "Tap Filter button" not in row[15]:
                    actions.insert(1, '2. "Tap Filter button to open Filter screen"')
                    results.insert(1, '2. "Filter screen opens"')
                    data.insert(1, '2. ""')
                    # Renumber actions 3...
                    for i in range(2, len(actions)):
                        actions[i] = re.sub(r'^\d+\.', f'{i+1}.', actions[i])
                        results[i] = re.sub(r'^\d+\.', f'{i+1}.', results[i])
                        data[i] = re.sub(r'^\d+\.', f'{i+1}.', data[i])
                    row[15] = '\n'.join(actions)
                    row[16] = '\n'.join(results)
                    row[17] = '\n'.join(data)
            else:
                # For others, if Action 2 starts with "Apply", "Enable", "Select", "Try", change to "Tap Filter button and ..."
                if not "Tap Filter button" in actions[1]:
                    actions[1] = actions[1].replace('2. "', '2. "Tap Filter button to open Filter screen, then ')
                    row[15] = '\n'.join(actions)

    with open('lesson-lists.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)

fix_csv()
