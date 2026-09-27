# Test Cases: LT-111600 — JPREP Live Lesson

## Suite: [JPREP] Live Lesson – Sync from JPREP (Lesson & Student)

_JPREP creates, updates and deletes live lessons and assigns students to lessons through its sync. Teachers are not assigned to lessons. Sources: S27, S28, S29, S30._

### [JPREP] Live Lesson – Sync – New online lesson sent by JPREP – Lesson created under its week with the sent name, time and Online medium

**Description:** AC 01.3 — CRUD (Create) — A new online lesson sent by the JPREP sync is created and shown in Course > Lesson tab and in the lesson detail with the sent values.

**Spec sources:**
- [S27] Confluence – How to use API to create JPREP's data for testing — https://manabie.atlassian.net/wiki/spaces/TECH/pages/47087636
- [S29] Code – backend JPREP sync live lesson BDD (create / update / delete / missing field) — https://github.com/manabie-com/backend/blob/develop/features/gandalf/jprep/jprep_sync_live_lesson.feature
- [S1] Confluence – [JPREP] Agora in LMSv2 JPREP (functional spec) — https://manabie.atlassian.net/wiki/spaces/LT/pages/892403790
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Tester has the JPREP sync Postman collection with environment variable baseUrl = https://web-api.staging.jprep.manabie.io/jprep (one line, no port, no trailing line break) and the signing key used by its pre-request script (source S28)
- JPREP BO Admin account is available
- Course C1 = JPREP_COURSE_000000119 (JPREP course id 119) is on the Staging live lesson course whitelist
- Lesson id 90288001 has never been used on Staging

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Tester sends PUT {{baseUrl}}/master-registration from the JPREP sync Postman collection with the body in Test Data (the pre-request script sets timestamp = now and the JPREP-Signature header) | Response is HTTP 200 (no "signature is not match" or "time is hack" error) | URL: PUT https://web-api.staging.jprep.manabie.io/jprep/master-registration
Body:
{
  "timestamp": {{now}},
  "payload": {
    "m_lesson": [
      {
        "m_lesson_id": 90288001,
        "action_kind": "upserted",
        "lesson_type": "online",
        "m_course_name_id": 119,
        "start_datetime": 1791190800,
        "end_datetime": 1791194400,
        "class_name": "SYNC-L1",
        "week": "Week 5"
      }
    ]
  }
}
m_course_name_id 119 = JPREP_COURSE_000000119; start/end = 2026-10-05 18:00–19:00 JST |
| 2 | JPREP BO Admin opens Course > C1 > Lesson tab in JPREP Back Office | Row Week 5 shows lesson name SYNC-L1 | week = Week 5 |
| 3 | JPREP BO Admin clicks lesson name SYNC-L1 | Lesson detail of SYNC-L1 opens |  |
| 4 | JPREP BO Admin reads the lesson name, date/time and teaching medium on the lesson detail | Name = SYNC-L1; date/time = 2026-10-05 18:00–19:00; teaching medium = Online; Start Live Lesson button is shown | start 1791190800 = 2026-10-05 09:00 UTC = 18:00 JST; end 1791194400 = 19:00 JST |

**Severity:** critical
**Priority:** high

---

### [JPREP] Live Lesson – Sync – Existing lesson resent with new name and time – Back Office and Learner show the new values

**Description:** AC 01.3 — CRUD (Update) — Resending an existing lesson id with changed name and time updates the same lesson instead of creating a new one.

**Spec sources:**
- [S27] Confluence – How to use API to create JPREP's data for testing — https://manabie.atlassian.net/wiki/spaces/TECH/pages/47087636
- [S29] Code – backend JPREP sync live lesson BDD (create / update / delete / missing field) — https://github.com/manabie-com/backend/blob/develop/features/gandalf/jprep/jprep_sync_live_lesson.feature
- [S1] Confluence – [JPREP] Agora in LMSv2 JPREP (functional spec) — https://manabie.atlassian.net/wiki/spaces/LT/pages/892403790
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Tester has the JPREP sync Postman collection set to Staging (base URL https://web-api.staging.jprep.manabie.io/jprep) with a valid signature (source S28)
- JPREP BO Admin account is available
- Course C1 = JPREP_COURSE_000000119 (JPREP course id 119) is on the Staging live lesson course whitelist
- Student S1 and Student S2 are JPREP student accounts of a class of course C1 (e.g. Staging sync student tongan.pham+student45@manabie.com)
- Lesson SYNC-L1 (lesson id 90288001) exists in Week 5 of course C1 with time 2026-10-05 18:00–19:00 JST
- Student S1 is assigned to lesson SYNC-L1

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Tester sends a JPREP Master Registration sync for lesson id 90288001 with a new name and time | The sync is accepted (success response) | action = upserted; lesson id = 90288001; name = SYNC-L1-UPDATED; type = online; course id = 119; week = Week 5; start = 1791194400; end = 1791199800 (= 2026-10-05 19:00–20:30 JST) |
| 2 | JPREP BO Admin opens Course > C1 > Lesson tab | Row Week 5 shows SYNC-L1-UPDATED; no row shows SYNC-L1 and no second lesson was added |  |
| 3 | JPREP BO Admin opens the lesson detail of SYNC-L1-UPDATED | Date/time = 2026-10-05 19:00–20:30 |  |
| 4 | Student S1 opens the lesson list on Learner Web | The lesson is shown once, as SYNC-L1-UPDATED at 2026-10-05 19:00–20:30 |  |

**Severity:** major
**Priority:** high

---

### [JPREP] Live Lesson – Sync – Lesson deleted by JPREP – Lesson removed from Back Office and from the learner lesson list

**Description:** AC 01.3 — CRUD (Delete) — A lesson sent with action "deleted" is removed from the course week and from the learner lesson list.

**Spec sources:**
- [S27] Confluence – How to use API to create JPREP's data for testing — https://manabie.atlassian.net/wiki/spaces/TECH/pages/47087636
- [S29] Code – backend JPREP sync live lesson BDD (create / update / delete / missing field) — https://github.com/manabie-com/backend/blob/develop/features/gandalf/jprep/jprep_sync_live_lesson.feature
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Tester has the JPREP sync Postman collection set to Staging (base URL https://web-api.staging.jprep.manabie.io/jprep) with a valid signature (source S28)
- JPREP BO Admin account is available
- Course C1 = JPREP_COURSE_000000119 (JPREP course id 119) is on the Staging live lesson course whitelist
- Student S1 and Student S2 are JPREP student accounts of a class of course C1 (e.g. Staging sync student tongan.pham+student45@manabie.com)
- Lesson SYNC-L2 (lesson id 90288002) exists in Week 6 of course C1 at 2026-10-12 18:00–19:00 JST
- Student S1 is assigned to lesson SYNC-L2

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student S1 opens the lesson list on Learner Web | SYNC-L2 is listed |  |
| 2 | Tester sends a JPREP Master Registration sync that deletes lesson id 90288002 | The sync is accepted (success response) | action = deleted; lesson id = 90288002; name = SYNC-L2; type = online; course id = 119; week = Week 6; start = 1791795600; end = 1791799200 |
| 3 | JPREP BO Admin opens Course > C1 > Lesson tab | Row Week 6 no longer shows SYNC-L2 |  |
| 4 | Student S1 refreshes the lesson list on Learner Web | SYNC-L2 is no longer listed |  |

**Severity:** major
**Priority:** high

---

### [JPREP] Live Lesson – Sync – Lesson sent without a required field – Sync rejected and no lesson created

**Description:** AC 01.3 — Decision Table — A lesson sent without any one required field is rejected and nothing is stored; run once per missing field.

**Spec sources:**
- [S27] Confluence – How to use API to create JPREP's data for testing — https://manabie.atlassian.net/wiki/spaces/TECH/pages/47087636
- [S29] Code – backend JPREP sync live lesson BDD (create / update / delete / missing field) — https://github.com/manabie-com/backend/blob/develop/features/gandalf/jprep/jprep_sync_live_lesson.feature
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Tester has the JPREP sync Postman collection set to Staging (base URL https://web-api.staging.jprep.manabie.io/jprep) with a valid signature (source S28)
- JPREP BO Admin account is available
- Course C1 = JPREP_COURSE_000000119 (JPREP course id 119) is on the Staging live lesson course whitelist
- Lesson id 90288003 has never been used on Staging

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Tester sends a JPREP Master Registration sync with lesson id 90288003 and removes one required field | The sync is rejected with a bad request error (400) | Base lesson: action = upserted; lesson id = 90288003; name = SYNC-L3; type = online; course id = 119; week = Week 7; start = 1791190800; end = 1791194400. Remove one field per run: action kind | lesson id | lesson name | lesson type | course id | start datetime | end datetime |
| 2 | JPREP BO Admin opens Course > C1 > Lesson tab | No row shows SYNC-L3 |  |
| 3 | JPREP BO Admin searches Lesson Management for SYNC-L3 | No lesson SYNC-L3 is found |  |

**Severity:** minor
**Priority:** medium

---

### [JPREP] Live Lesson – Sync – Student assigned to a lesson – Lesson shown to the student and student listed on the Back Office lesson

**Description:** AC 01.4 — Cross-system — A student assigned to a lesson by the JPREP student lesson sync is listed on the lesson and sees it with Join (regression LT-61156). HTTP 200 only means accepted; the partner log must reach SUCCESS.

**Spec sources:**
- [S27] Confluence – How to use API to create JPREP's data for testing — https://manabie.atlassian.net/wiki/spaces/TECH/pages/47087636
- [S30] Postmortem 2022-06-16 JPREP data sync (lesson members lost) + Jira LT-61156 — https://manabie.atlassian.net/wiki/spaces/TECH/pages/471957547
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Tester uses the Postman request "Synchronize only new data changes ..." of the JPREP sync collection (PUT {{baseUrl}}/user-course), NOT "User Registration"; baseUrl = https://web-api.staging.jprep.manabie.io/jprep (one line, no port, no trailing line break) and the pre-request script signs the body (source S28)
- Teacher T1 = JPREP Staging teacher account jprep.teachertest01 (password: team vault)
- Course C1 = JPREP_COURSE_000000119 (JPREP course id 119) is on the Staging live lesson course whitelist
- Student S1 = JPREP Staging student account nt1818895 (password: team vault), Manabie user ID e9bd33ad-a63e-43b2-ab56-f235c8a7ad14
- Lesson SYNC-L1 (lesson id 90288001) exists in course C1 with teaching medium Online
- Student S1 is not assigned to lesson SYNC-L1

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Tester sends PUT {{baseUrl}}/user-course with the body in Test Data (the pre-request script sets timestamp = now and the JPREP-Signature header) | Response is HTTP 200 (the request is only accepted; students are assigned asynchronously) | URL: PUT https://web-api.staging.jprep.manabie.io/jprep/user-course
Body:
{
  "timestamp": {{now}},
  "payload": {
    "student_lesson": [
      {
        "action_kind": "upserted",
        "student_id": "e9bd33ad-a63e-43b2-ab56-f235c8a7ad14",
        "m_lesson_ids": [
          90288001
        ]
      }
    ]
  }
} |
| 2 | Tester copies the JPREP-Signature header of the previous request from the Postman Console and sends POST {{baseUrl}}/partner-log with it | Response data lists the sync with status = SUCCESS (PROCESSING / PENDING / FAILED means the assignment failed) | Body: {"timestamp": {{now}}, "payload": {"signature": "<JPREP-Signature of the user-course request>"}} |
| 3 | Teacher T1 opens the Teacher Web lesson detail of SYNC-L1 and reads the student list (hard reload) | Student S1 (nt1818895) is listed | URL = https://teacher.staging.jprep.manabie.io/#/liveLessonDetailScreen?course_id=JPREP_COURSE_000000119&lesson_id=JPREP_LESSON_090288001 |
| 4 | Student S1 opens the lesson list on Learner Web | SYNC-L1 is listed with a Join button |  |
| 5 | Student S1 clicks Join after Teacher T1 has started SYNC-L1 | Student S1 enters the live room of SYNC-L1 |  |

**Severity:** critical
**Priority:** high

---

### [JPREP] Live Lesson – Sync – Student synced with several lessons then with one – Student keeps only the lessons of the last sync

**Description:** AC 01.4 — State transition — One upserted sync assigns the student to every listed lesson; a later upserted sync replaces the whole list, so lessons not sent again are removed. An upserted student lesson sync REPLACES the whole lesson list of that student: lessons not listed in m_lesson_ids are removed from the student (backend yasuo).

**Spec sources:**
- [S27] Confluence – How to use API to create JPREP's data for testing — https://manabie.atlassian.net/wiki/spaces/TECH/pages/47087636
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Tester uses the Postman request "Synchronize only new data changes ..." of the JPREP sync collection (PUT {{baseUrl}}/user-course), NOT "User Registration"; baseUrl = https://web-api.staging.jprep.manabie.io/jprep (one line, no port, no trailing line break) and the pre-request script signs the body (source S28)
- Teacher T1 = JPREP Staging teacher account jprep.teachertest01 (password: team vault)
- Course C1 = JPREP_COURSE_000000119 (JPREP course id 119) is on the Staging live lesson course whitelist
- Student S1 = JPREP Staging student account nt1818895 (password: team vault), Manabie user ID e9bd33ad-a63e-43b2-ab56-f235c8a7ad14
- Lessons SYNC-L1 (90288001), SYNC-L4 (90288004) and SYNC-L5 (90288005) exist in course C1 with teaching medium Online

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Tester sends PUT {{baseUrl}}/user-course with the body in Test Data (the pre-request script sets timestamp = now and the JPREP-Signature header) | Response is HTTP 200 (the request is only accepted; students are assigned asynchronously) | URL: PUT https://web-api.staging.jprep.manabie.io/jprep/user-course
Body:
{
  "timestamp": {{now}},
  "payload": {
    "student_lesson": [
      {
        "action_kind": "upserted",
        "student_id": "e9bd33ad-a63e-43b2-ab56-f235c8a7ad14",
        "m_lesson_ids": [
          90288001,
          90288004,
          90288005
        ]
      }
    ]
  }
} |
| 2 | Tester copies the JPREP-Signature header of the previous request from the Postman Console and sends POST {{baseUrl}}/partner-log with it | Response data lists the sync with status = SUCCESS (PROCESSING / PENDING / FAILED means the assignment failed) | Body: {"timestamp": {{now}}, "payload": {"signature": "<JPREP-Signature of the user-course request>"}} |
| 3 | Student S1 opens the lesson list on Learner Web | SYNC-L1, SYNC-L4 and SYNC-L5 are all listed |  |
| 4 | Tester sends PUT {{baseUrl}}/user-course with the body in Test Data (the pre-request script sets timestamp = now and the JPREP-Signature header) | Response is HTTP 200 (the request is only accepted; students are assigned asynchronously) | URL: PUT https://web-api.staging.jprep.manabie.io/jprep/user-course
Body:
{
  "timestamp": {{now}},
  "payload": {
    "student_lesson": [
      {
        "action_kind": "upserted",
        "student_id": "e9bd33ad-a63e-43b2-ab56-f235c8a7ad14",
        "m_lesson_ids": [
          90288004
        ]
      }
    ]
  }
} |
| 5 | Tester copies the JPREP-Signature header of the previous request from the Postman Console and sends POST {{baseUrl}}/partner-log with it | Response data lists the sync with status = SUCCESS (PROCESSING / PENDING / FAILED means the assignment failed) | Body: {"timestamp": {{now}}, "payload": {"signature": "<JPREP-Signature of the user-course request>"}} |
| 6 | Student S1 refreshes the lesson list on Learner Web | Only SYNC-L4 is listed; SYNC-L1 and SYNC-L5 are no longer listed |  |
| 7 | Teacher T1 opens the Teacher Web lesson detail of SYNC-L1 and reads the student list (hard reload) | Student S1 is not listed | URL = https://teacher.staging.jprep.manabie.io/#/liveLessonDetailScreen?course_id=JPREP_COURSE_000000119&lesson_id=JPREP_LESSON_090288001 |

**Severity:** major
**Priority:** high

---

### [JPREP] Live Lesson – Sync – Student lesson sync with action deleted – Request rejected and the student keeps the lesson

**Description:** AC 01.4 — Negative — The student lesson sync only accepts action_kind "upserted"; "deleted" is rejected with HTTP 400 and nothing changes (backend enigma; the Confluence page S27 is outdated on this point).

**Spec sources:**
- [S27] Confluence – How to use API to create JPREP's data for testing — https://manabie.atlassian.net/wiki/spaces/TECH/pages/47087636
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Tester uses the Postman request "Synchronize only new data changes ..." of the JPREP sync collection (PUT {{baseUrl}}/user-course), NOT "User Registration"; baseUrl = https://web-api.staging.jprep.manabie.io/jprep (one line, no port, no trailing line break) and the pre-request script signs the body (source S28)
- Teacher T1 = JPREP Staging teacher account jprep.teachertest01 (password: team vault)
- Course C1 = JPREP_COURSE_000000119 (JPREP course id 119) is on the Staging live lesson course whitelist
- Student S1 = JPREP Staging student account nt1818895 (password: team vault), Manabie user ID e9bd33ad-a63e-43b2-ab56-f235c8a7ad14
- Student S1 is assigned to lesson SYNC-L1 (90288001)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Tester sends PUT {{baseUrl}}/user-course with the body in Test Data (the pre-request script sets timestamp = now and the JPREP-Signature header) | Response is HTTP 400 with error "payload.student_lesson[0].action_kind should be upserted" | URL: PUT https://web-api.staging.jprep.manabie.io/jprep/user-course
Body:
{
  "timestamp": {{now}},
  "payload": {
    "student_lesson": [
      {
        "action_kind": "deleted",
        "student_id": "e9bd33ad-a63e-43b2-ab56-f235c8a7ad14",
        "m_lesson_ids": [
          90288001
        ]
      }
    ]
  }
} |
| 2 | Student S1 refreshes the lesson list on Learner Web | SYNC-L1 is still listed |  |
| 3 | Teacher T1 opens the Teacher Web lesson detail of SYNC-L1 and reads the student list (hard reload) | Student S1 is still listed | URL = https://teacher.staging.jprep.manabie.io/#/liveLessonDetailScreen?course_id=JPREP_COURSE_000000119&lesson_id=JPREP_LESSON_090288001 |

**Severity:** minor
**Priority:** medium

---

### [JPREP] Live Lesson – Sync – Student synced with an empty lesson list – Student removed from all lessons

**Description:** AC 01.4 — Equivalence Partitioning — An upserted student lesson sync with an empty lesson list is the way to remove a student from all lessons. An upserted student lesson sync REPLACES the whole lesson list of that student: lessons not listed in m_lesson_ids are removed from the student (backend yasuo).

**Spec sources:**
- [S27] Confluence – How to use API to create JPREP's data for testing — https://manabie.atlassian.net/wiki/spaces/TECH/pages/47087636
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Tester uses the Postman request "Synchronize only new data changes ..." of the JPREP sync collection (PUT {{baseUrl}}/user-course), NOT "User Registration"; baseUrl = https://web-api.staging.jprep.manabie.io/jprep (one line, no port, no trailing line break) and the pre-request script signs the body (source S28)
- Teacher T1 = JPREP Staging teacher account jprep.teachertest01 (password: team vault)
- Course C1 = JPREP_COURSE_000000119 (JPREP course id 119) is on the Staging live lesson course whitelist
- Student S1 = JPREP Staging student account nt1818895 (password: team vault), Manabie user ID e9bd33ad-a63e-43b2-ab56-f235c8a7ad14
- Student S1 is assigned to lessons SYNC-L1 (90288001) and SYNC-L4 (90288004)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student S1 opens the lesson list on Learner Web | SYNC-L1 and SYNC-L4 are listed |  |
| 2 | Tester sends PUT {{baseUrl}}/user-course with the body in Test Data (the pre-request script sets timestamp = now and the JPREP-Signature header) | Response is HTTP 200 (the request is only accepted; students are assigned asynchronously) | URL: PUT https://web-api.staging.jprep.manabie.io/jprep/user-course
Body:
{
  "timestamp": {{now}},
  "payload": {
    "student_lesson": [
      {
        "action_kind": "upserted",
        "student_id": "e9bd33ad-a63e-43b2-ab56-f235c8a7ad14",
        "m_lesson_ids": []
      }
    ]
  }
} |
| 3 | Tester copies the JPREP-Signature header of the previous request from the Postman Console and sends POST {{baseUrl}}/partner-log with it | Response data lists the sync with status = SUCCESS (PROCESSING / PENDING / FAILED means the assignment failed) | Body: {"timestamp": {{now}}, "payload": {"signature": "<JPREP-Signature of the user-course request>"}} |
| 4 | Student S1 refreshes the lesson list on Learner Web | SYNC-L1 and SYNC-L4 are no longer listed |  |
| 5 | Teacher T1 opens the Teacher Web lesson detail of SYNC-L1 and reads the student list (hard reload) | Student S1 is not listed | URL = https://teacher.staging.jprep.manabie.io/#/liveLessonDetailScreen?course_id=JPREP_COURSE_000000119&lesson_id=JPREP_LESSON_090288001 |

**Severity:** major
**Priority:** high

---

### [JPREP] Live Lesson – Sync – One student re-synced to a lesson – Other students of the lesson are kept

**Description:** AC 01.4 — Data integrity — Re-sending the lessons of one student must not remove other students from the same lesson (regression of the 2022-06-16 lesson member loss). An upserted student lesson sync REPLACES the whole lesson list of that student: lessons not listed in m_lesson_ids are removed from the student (backend yasuo). The re-sync therefore lists every lesson S1 must keep.

**Spec sources:**
- [S27] Confluence – How to use API to create JPREP's data for testing — https://manabie.atlassian.net/wiki/spaces/TECH/pages/47087636
- [S30] Postmortem 2022-06-16 JPREP data sync (lesson members lost) + Jira LT-61156 — https://manabie.atlassian.net/wiki/spaces/TECH/pages/471957547
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Tester uses the Postman request "Synchronize only new data changes ..." of the JPREP sync collection (PUT {{baseUrl}}/user-course), NOT "User Registration"; baseUrl = https://web-api.staging.jprep.manabie.io/jprep (one line, no port, no trailing line break) and the pre-request script signs the body (source S28)
- Teacher T1 = JPREP Staging teacher account jprep.teachertest01 (password: team vault)
- Course C1 = JPREP_COURSE_000000119 (JPREP course id 119) is on the Staging live lesson course whitelist
- Student S1 = JPREP Staging student account nt1818895 (password: team vault), Manabie user ID e9bd33ad-a63e-43b2-ab56-f235c8a7ad14
- Student S2 = a second JPREP Staging student account (password: team vault) whose Manabie user ID is known (Learner Web > DevTools > any web-api request > header "token" > decode JWT > x-hasura-user-id)
- Lesson SYNC-L1 (lesson id 90288001) exists in course C1 with teaching medium Online
- Student S1 and Student S2 are both assigned to lesson SYNC-L1 and to no other lesson

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Tester sends PUT {{baseUrl}}/user-course with the body in Test Data (the pre-request script sets timestamp = now and the JPREP-Signature header); repeat it once more | Both responses are HTTP 200 | URL: PUT https://web-api.staging.jprep.manabie.io/jprep/user-course
Body:
{
  "timestamp": {{now}},
  "payload": {
    "student_lesson": [
      {
        "action_kind": "upserted",
        "student_id": "e9bd33ad-a63e-43b2-ab56-f235c8a7ad14",
        "m_lesson_ids": [
          90288001
        ]
      }
    ]
  }
}
Sent 2 times |
| 2 | Tester copies the JPREP-Signature header of the previous request from the Postman Console and sends POST {{baseUrl}}/partner-log with it (for each of the 2 requests) | Both syncs have status = SUCCESS | Body: {"timestamp": {{now}}, "payload": {"signature": "<JPREP-Signature of the user-course request>"}} |
| 3 | Teacher T1 opens the Teacher Web lesson detail of SYNC-L1 and reads the student list (hard reload) | Student S1 and Student S2 are both listed, each once | URL = https://teacher.staging.jprep.manabie.io/#/liveLessonDetailScreen?course_id=JPREP_COURSE_000000119&lesson_id=JPREP_LESSON_090288001 |
| 4 | Student S2 opens the lesson list on Learner Web | SYNC-L1 is still listed for Student S2 |  |

**Severity:** critical
**Priority:** high

---
