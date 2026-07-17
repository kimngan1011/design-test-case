import re
import glob

def fix_csv(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We look for 4 commas followed by high, medium, or low.
    # We replace them with 3 commas.
    fixed_content = re.sub(r',,,,(high|medium|low)', r',,,\1', content)
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print(f"Fixed {filename}")

for file in glob.glob('/Users/kimngan/design-test-case/epics/OOP/nichibei/LT-96620-nichibei-lesson-booking/test-cases/*.csv'):
    fix_csv(file)
