import urllib.request
import json
import csv
import os

TOKEN = "7089c6bc3cac41f13fade01682726c8e3a6f70c5bfaae5df925f4188c12460a6"
HEADERS = {
    "Token": TOKEN,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def fix_preconditions_in_qase():
    files = ['lesson-lists.csv', 'my-lessons.csv', 'book-lesson.csv', 'cancel-booking.csv']
    for f in files:
        if not os.path.exists(f): continue
        with open(f, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            for row in reader:
                if not row or not row[0]: continue
                v2_id = row[0]
                
                url = f"https://api.qase.io/v1/case/PX/{v2_id}"
                req = urllib.request.Request(url, headers=HEADERS)
                try:
                    with urllib.request.urlopen(req) as res:
                        data = json.loads(res.read().decode('utf-8'))['result']
                        preconditions = data.get('preconditions', '')
                        
                        if preconditions:
                            new_pre = preconditions.replace('\\n', '\n')
                            new_pre = new_pre.replace('\n', '\n\n')
                            
                            # Split by ". " to make newlines for each sentence
                            new_pre = new_pre.replace('. ', '.\n\n- ')
                            
                            # Make the first sentence a bullet point too if we added bullets
                            if '.\n\n- ' in new_pre and not new_pre.startswith('- '):
                                new_pre = '- ' + new_pre
                                
                            while '\n\n\n' in new_pre:
                                new_pre = new_pre.replace('\n\n\n', '\n\n')
                                
                            if new_pre != preconditions:
                                payload = {"preconditions": new_pre}
                                p_data = json.dumps(payload).encode('utf-8')
                                p_req = urllib.request.Request(url, data=p_data, headers=HEADERS, method='PATCH')
                                urllib.request.urlopen(p_req)
                                print(f"Fixed newlines for {v2_id}")
                except Exception as e:
                    pass

fix_preconditions_in_qase()
