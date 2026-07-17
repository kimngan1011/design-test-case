import csv
import re
import os

files_to_fix = [
    'book-lesson.csv',
    'cancel-booking.csv',
    'teacher-notification.csv',
    'bookable-flag-config.csv'
]

for filename in files_to_fix:
    if not os.path.exists(filename):
        continue
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    modified = False
    for row in rows:
        if not row[0]: continue
        
        # We need to replace in description (3), preconditions (10 or so? let's just do it broadly)
        for i in range(len(row)):
            old_val = row[i]
            val = old_val.replace("Browse Lessons", "Lesson Lists")
            val = val.replace("Browse list", "Lesson Lists")
            val = val.replace("active LA for Location A", "active LA linked to a Location Course for Location A")
            val = val.replace("student's LA location", "student's LA's Location Course location")
            
            if val != old_val:
                row[i] = val
                modified = True

    if modified:
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)
        print(f"Fixed {filename}")

