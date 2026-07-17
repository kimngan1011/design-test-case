import re

with open('lesson-lists.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Browse Lessons -> Lesson Lists
content = content.replace("Browse Lessons", "Lesson Lists")

# 2. Location of LA
content = content.replace("active LA for Location A", "active LA linked to a Location Course for Location A")
content = content.replace("student's LA location", "student's LA's Location Course location")

# 3. Add "Tap Filter button to open Filter screen" to filter cases
# We can find actions in tables.
# Filter test cases start around line 135
# For TC 20868 (Location Filter):
content = content.replace(
    '| 2   | Open the Location filter dropdown',
    '| 2   | Tap Filter button to open Filter screen            | Filter screen opens                                                | —         |\n| 3   | Open the Location filter dropdown'
)

content = content.replace(
    '| 2   | Apply Schedule filter with date range:',
    '| 2   | Tap Filter button to open Filter screen, then Apply Schedule filter with date range:'
)

content = content.replace(
    '| 2   | Apply Schedule filter: select Monday only',
    '| 2   | Tap Filter button to open Filter screen, then Apply Schedule filter: select Monday only'
)

content = content.replace(
    '| 2   | Enable "available lessons only" toggle',
    '| 2   | Tap Filter button to open Filter screen, then Enable "available lessons only" toggle'
)

content = content.replace(
    '| 2   | Try to search/filter without selecting Eligible Subject',
    '| 2   | Tap Filter button to open Filter screen, then Try to search/filter without selecting Eligible Subject'
)

content = content.replace(
    '| 2   | Select Subject X in Eligible Subject and Location A in Location',
    '| 2   | Tap Filter button to open Filter screen, then Select Subject X in Eligible Subject and Location A in Location'
)

content = content.replace(
    '| 2   | Enter "Math" in Lesson Name search field',
    '| 2   | Tap Filter button to open Filter screen, then Enter "Math" in Lesson Name search field'
)

with open('lesson-lists.md', 'w', encoding='utf-8') as f:
    f.write(content)
