#!/usr/bin/env python3
"""Send JPREP sync requests (create/update/delete a live lesson, assign students) to Staging or UAT.

Sources:
- Payload fields: Confluence "How to use API to create JPREP's data for testing" (TECH/47087636)
- Base URL:       Confluence "How to create and sync account on JPREP" (TECH/416940142)
- Signature:      backend internal/enigma/middlewares/jprep_signature.go
                  -> header JPREP-Signature = hex(HMAC-SHA256(signing_key, raw request body))
                  -> body "timestamp" must be recent (server rejects old payloads: "time is hack")
- Routes:         backend features/eibanam/lesson_helper.go
                  -> PUT /jprep/master-registration  (m_lesson)
                  -> PUT /jprep/user-course          (student_lesson)
- ID mapping:     m_course_name_id 119  -> JPREP_COURSE_000000119
                  m_lesson_id 90288001  -> JPREP_LESSON_090288001

The signing key is a secret (same key the Postman collection uses). Pass it via env var:
    export JPREP_SIGNING_KEY='<key from the JPREP Postman environment / team vault>'

Examples:
    # Create an online lesson in course JPREP_COURSE_000000119, 2026-10-05 18:00-19:00 JST
    python3 jprep_sync.py lesson --lesson-id 90288001 --name SYNC-L1 \
        --start "2026-10-05 18:00" --end "2026-10-05 19:00" --week "Week 5"

    # Update it (same lesson id, new name/time)
    python3 jprep_sync.py lesson --lesson-id 90288001 --name SYNC-L1-UPDATED \
        --start "2026-10-05 19:00" --end "2026-10-05 20:30" --week "Week 5"

    # Delete it
    python3 jprep_sync.py lesson --lesson-id 90288001 --name SYNC-L1 \
        --start "2026-10-05 18:00" --end "2026-10-05 19:00" --week "Week 5" --delete

    # Assign a student (Keycloak uid) to lessons; --lesson-ids with no value = empty list (removes all)
    python3 jprep_sync.py students --student-id <keycloak_uid> --lesson-ids 90288001 90288004
    python3 jprep_sync.py students --student-id <keycloak_uid> --lesson-ids 90288001 --delete

    # Preview only (prints URL, body, signature; sends nothing)
    python3 jprep_sync.py --dry-run lesson ...
"""
import argparse
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone

BASE_URLS = {
    'stg': 'https://web-api.staging.jprep.manabie.io/jprep',
    'uat': 'https://web-api.uat.jprep.manabie.io/jprep',
}
JST = timezone(timedelta(hours=9))


def jst_to_epoch(value):
    """'2026-10-05 18:00' (JST) -> epoch seconds."""
    return int(datetime.strptime(value, '%Y-%m-%d %H:%M').replace(tzinfo=JST).timestamp())


def send(env, path, payload, dry_run):
    body = json.dumps({'timestamp': int(time.time()), 'payload': payload},
                      ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    key = os.environ.get('JPREP_SIGNING_KEY', '')
    if not key and not dry_run:
        sys.exit('JPREP_SIGNING_KEY is not set.')
    signature = hmac.new(key.encode(), body, hashlib.sha256).hexdigest() if key else '<no key>'
    url = BASE_URLS[env] + path

    print(f'PUT {url}')
    print(json.dumps(json.loads(body), ensure_ascii=False, indent=2))
    if dry_run:
        print(f'JPREP-Signature: {signature}\n(dry run: nothing sent)')
        return

    req = urllib.request.Request(url, data=body, method='PUT', headers={
        'Content-Type': 'application/json',
        'JPREP-Signature': signature,
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            print(f'-> HTTP {resp.status}: {resp.read().decode()}')
    except urllib.error.HTTPError as e:
        sys.exit(f'-> HTTP {e.code}: {e.read().decode()}')


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--env', choices=BASE_URLS, default='stg')
    p.add_argument('--dry-run', action='store_true')
    sub = p.add_subparsers(dest='cmd', required=True)

    ls = sub.add_parser('lesson', help='Create/update (upserted) or delete a lesson via master-registration')
    ls.add_argument('--lesson-id', type=int, required=True, help='JPREP lesson id, e.g. 90288001 (must be unused to create)')
    ls.add_argument('--course-id', type=int, default=119, help='JPREP course id (119 = JPREP_COURSE_000000119)')
    ls.add_argument('--name', required=True, help='Lesson name (sent as class_name)')
    ls.add_argument('--start', required=True, help='Start in JST, "YYYY-MM-DD HH:MM"')
    ls.add_argument('--end', required=True, help='End in JST, "YYYY-MM-DD HH:MM"')
    ls.add_argument('--week', required=True, help='Week label, use the same format as existing weeks of the course')
    ls.add_argument('--type', default='online', choices=['online', 'offline', 'hybrid'],
                    help='Only online lessons are shown on the UI')
    ls.add_argument('--delete', action='store_true', help='Send action_kind = deleted')

    st = sub.add_parser('students', help='Assign / remove a student to lessons via user-course')
    st.add_argument('--student-id', required=True, help='Keycloak uid of the JPREP student')
    st.add_argument('--lesson-ids', type=int, nargs='*', default=[], help='JPREP lesson ids; empty = remove from all')
    st.add_argument('--delete', action='store_true', help='Send action_kind = deleted')

    a = p.parse_args()
    action = 'deleted' if a.delete else 'upserted'

    if a.cmd == 'lesson':
        start, end = jst_to_epoch(a.start), jst_to_epoch(a.end)
        if end <= start:
            sys.exit('--end must be after --start')
        print(f'Lesson JPREP_LESSON_{a.lesson_id:09d} in JPREP_COURSE_{a.course_id:09d}: '
              f'{a.start}-{a.end} JST = {start}-{end} epoch')
        send(a.env, '/master-registration', {'m_lesson': [{
            'm_lesson_id': a.lesson_id,
            'action_kind': action,
            'lesson_type': a.type,
            'm_course_name_id': a.course_id,
            'start_datetime': start,
            'end_datetime': end,
            'class_name': a.name,
            'week': a.week,
        }]}, a.dry_run)
    else:
        send(a.env, '/user-course', {'student_lesson': [{
            'action_kind': action,
            'student_id': a.student_id,
            'm_lesson_ids': a.lesson_ids,
        }]}, a.dry_run)


if __name__ == '__main__':
    main()
