# Test Cases: LT-111600 — JPREP Live Lesson

## Suite: [JPREP] Live Lesson – Student Join & Course Whitelist

_Learner lesson list, Join button gated by the JPREP live lesson course whitelist (incident MANACS-2620 / LT-111600), late member sync, waiting room, end for all. Sources: S1, S13, S14, S16, S17._

### [JPREP] Live Lesson – Learner Schedule – Online lesson card – Name, date, time and materials displayed

**Description:** AC 05.1 — Component — The JPREP learner sees the live lesson in the schedule with lesson name, JST date/time and the week's uploaded materials (same UX as LMSv1).

**Spec sources:**
- [S1] Confluence – [JPREP] Agora in LMSv2 JPREP (functional spec) — https://manabie.atlassian.net/wiki/spaces/LT/pages/892403790
- [S12] Confluence – [QA] Jprep LMSv2 integration test — https://manabie.atlassian.net/wiki/spaces/LT/pages/993427472
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Student S1 and Student S2 are JPREP student accounts assigned to Lesson L1 (e.g. Staging sync student tongan.pham+student45@manabie.com; UAT jprep-superman62 / jprep-superman63 from source S22)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Lesson L1 start = 2026-09-28 10:00 JST, end = 2026-09-28 12:00 JST
- Material "W2_Slides.pdf" is uploaded to the week paired with L1

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student S1 logs in to Learner Web | Learner home is shown | URL = https://learner.staging.jprep.manabie.io |
| 2 | Student S1 opens the lesson schedule / live lesson list | Lesson L1 is listed | today = 2026-09-28 |
| 3 | Student S1 reads the L1 card | Card shows lesson name L1, date 2026-09-28, time 10:00 – 12:00 |  |
| 4 | Student S1 opens L1 detail | Material W2_Slides.pdf is listed and can be opened for preview |  |
| 5 | Student S1 repeats steps 1–4 on the Learner App (iOS or Android) | Same lesson name, date, time and material are shown | Platform = Learner App |

**Severity:** minor
**Priority:** medium

---

### [JPREP] Live Lesson – Join – Course on whitelist and teacher started – Student sees Join button and enters the room

**Description:** AC 05.2 — Equivalence Partitioning (whitelisted) — For a lesson whose course is on the live lesson whitelist, the student sees Join once the teacher has started and can enter the room.

**Spec sources:**
- [S13] Slack #jp_incidents – MANACS-2620 EX240 students cannot join (whitelist root cause, Admin error, waiting room, late sync, end lesson) — https://manabiebiz.slack.com/archives/C0BPM7GABDW/p1789976358320349
- [S16] Slack DM 2026-09-26 – STG live lesson course whitelist (4 courses) — https://manabiebiz.slack.com/archives/D0BNMBRTRNZ/p1790399497452229
- [S17] Confluence – Virtual Classroom Database Tables (whitelist config for JPREP live lessons) — https://manabie.atlassian.net/wiki/spaces/TECH/pages/722468865
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Staging live lesson course whitelist = JPREP_COURSE_000000119, JPREP_COURSE_020240109, JPREP_COURSE_000000122, JPREP_COURSE_000000218 (source S16)
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Student S1 and Student S2 are JPREP student accounts assigned to Lesson L1 (e.g. Staging sync student tongan.pham+student45@manabie.com; UAT jprep-superman62 / jprep-superman63 from source S22)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 starts Lesson L1 from JPREP Back Office (Start Live Lesson) | Teacher T1 is inside the live room | course_id = JPREP_COURSE_000000119 (whitelisted) |
| 2 | Student S1 logs in to Learner Web and opens Lesson L1 | A Join button is displayed on L1 |  |
| 3 | Student S1 clicks Join | Student S1 enters the live room (or waiting room if enabled) |  |
| 4 | Teacher T1 looks at the participant list | Student S1 is shown as joined |  |

**Severity:** critical
**Priority:** high

---

### [JPREP] Live Lesson – Join – Course not on whitelist – Student sees no Join button while teacher can still start

**Description:** AC 05.3 — Equivalence Partitioning (not whitelisted) / Negative — Reproduces the 2026-09-21 EX240 incident: an Online lesson of a course missing from the whitelist can be started by the teacher, but students get no Join button.

**Spec sources:**
- [S13] Slack #jp_incidents – MANACS-2620 EX240 students cannot join (whitelist root cause, Admin error, waiting room, late sync, end lesson) — https://manabiebiz.slack.com/archives/C0BPM7GABDW/p1789976358320349
- [S14] Jira LT-111600 – JPREP check issue live lesson (add course to whitelist) — https://manabie.atlassian.net/browse/LT-111600
- [S16] Slack DM 2026-09-26 – STG live lesson course whitelist (4 courses) — https://manabiebiz.slack.com/archives/D0BNMBRTRNZ/p1790399497452229
- [S17] Confluence – Virtual Classroom Database Tables (whitelist config for JPREP live lessons) — https://manabie.atlassian.net/wiki/spaces/TECH/pages/722468865
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Staging live lesson course whitelist = JPREP_COURSE_000000119, JPREP_COURSE_020240109, JPREP_COURSE_000000122, JPREP_COURSE_000000218 (source S16)
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Student S1 and Student S2 are JPREP student accounts assigned to Lesson L1 (e.g. Staging sync student tongan.pham+student45@manabie.com; UAT jprep-superman62 / jprep-superman63 from source S22)
- Lesson L5 is synced with teaching medium Online, course JPREP_COURSE_000000457 (EX240 – NOT in the Staging whitelist), teacher T1, students S1 and S2
- Current time (JST) is inside the lesson window of L5

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 opens Lesson L5 in JPREP Back Office and clicks Start Live Lesson | Teacher T1 enters the live room (teacher side is not blocked) | course_id = JPREP_COURSE_000000457 (not whitelisted) |
| 2 | Student S1 logs in to Learner Web and opens the lesson schedule | Lesson L5 has NO Join button (or is not listed as a live lesson) | Expected per incident S13 |
| 3 | Student S1 refreshes the page | Still no Join button (not a cache issue) |  |
| 4 | Student S1 repeats on Learner App | No Join button on Learner App either |  |
| 5 | Tester records the result for course JPREP_COURSE_000000457 in the run | Evidence (screenshots of teacher room + student list) attached |  |

**Severity:** critical
**Priority:** high

---

### [JPREP] Live Lesson – Join – Course added to whitelist while lesson exists – Join button appears after student refresh

**Description:** AC 05.4 — State Transition — After dev adds the lesson's course to the whitelist, the student sees Join after refreshing (fix applied in LT-111600).

**Spec sources:**
- [S13] Slack #jp_incidents – MANACS-2620 EX240 students cannot join (whitelist root cause, Admin error, waiting room, late sync, end lesson) — https://manabiebiz.slack.com/archives/C0BPM7GABDW/p1789976358320349
- [S14] Jira LT-111600 – JPREP check issue live lesson (add course to whitelist) — https://manabie.atlassian.net/browse/LT-111600
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Student S1 and Student S2 are JPREP student accounts assigned to Lesson L1 (e.g. Staging sync student tongan.pham+student45@manabie.com; UAT jprep-superman62 / jprep-superman63 from source S22)
- Lesson L5 from the previous case exists (course JPREP_COURSE_000000457 not whitelisted) and Teacher T1 is in the room
- Dev support (Lesson BE) can add JPREP_COURSE_000000457 to the Staging live lesson whitelist and remove it after the run

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student S1 opens Lesson L5 on Learner Web | No Join button | State before = not whitelisted |
| 2 | Dev support adds JPREP_COURSE_000000457 to the Staging live lesson whitelist | Whitelist now contains 5 courses | State after = whitelisted |
| 3 | Student S1 refreshes the lesson schedule | Join button is displayed on L5 |  |
| 4 | Student S1 clicks Join | Student S1 enters the live room of L5 |  |
| 5 | Dev support removes JPREP_COURSE_000000457 from the Staging whitelist after the run | Staging whitelist is back to the 4 courses in source S16 | restore config |

**Severity:** major
**Priority:** high

---

### [JPREP] Live Lesson – Join – Newly whitelisted PROD courses EX240 and EX280 – Student sees Join button

**Description:** AC 05.2 — Regression — Smoke on Production (only with JPREP approval, S15) that courses added after the incident (EX240, EX280) now allow students to join.

**Spec sources:**
- [S13] Slack #jp_incidents – MANACS-2620 EX240 students cannot join (whitelist root cause, Admin error, waiting room, late sync, end lesson) — https://manabiebiz.slack.com/archives/C0BPM7GABDW/p1789976358320349
- [S14] Jira LT-111600 – JPREP check issue live lesson (add course to whitelist) — https://manabie.atlassian.net/browse/LT-111600
- [S15] Slack #draft-discuss-lesson-feature 2026-09-23 – re-test plan + unleash User_Auth_AllowAllRolesToLoginTeacherWeb — https://manabiebiz.slack.com/archives/C0BNPCH3605/p1790133887305919
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Production; JPREP has approved a test lesson (ask via PS – source S15)
- Production live lesson course whitelist (2026-09-25) = ES010 JPREP_COURSE_000000119, ES015 JPREP_COURSE_000000217, ES020 JPREP_COURSE_000000120, ES030 JPREP_COURSE_000000121, ES040 JPREP_COURSE_000000122, EX100 JPREP_COURSE_000000162, EX200 JPREP_COURSE_000000218, EX240 JPREP_COURSE_000000457, EX250 JPREP_COURSE_000000163, EX280 JPREP_COURSE_000000458 (source S13)
- Test lesson L6 is created under EX240 (JPREP_COURSE_000000457) and test lesson L7 under EX280 (JPREP_COURSE_000000458), teaching medium Online, with a Manabie test teacher and a Manabie test student
- Current time (JST) is inside the lesson window of L6 and L7

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Manabie test teacher starts L6 from JPREP Back Office | Teacher enters the live room of L6 | course = EX240 JPREP_COURSE_000000457 |
| 2 | Manabie test student opens Learner App and looks at L6 | Join button is displayed |  |
| 3 | Manabie test student clicks Join | Student enters the room of L6 |  |
| 4 | Manabie test teacher and student repeat steps 1–3 with L7 | Join button displayed and student enters L7 | course = EX280 JPREP_COURSE_000000458 |
| 5 | Manabie test teacher ends both lessons for all | Rooms close; no real JPREP student was affected |  |

**Severity:** critical
**Priority:** high

---

### [JPREP] Live Lesson – Join – Student synced into lesson after start time – Join button appears after refresh

**Description:** AC 05.5 — Scenario — In the incident, lesson members were synced at 15:36 JST after the lesson started; a student added late must see Join after refreshing.

**Spec sources:**
- [S13] Slack #jp_incidents – MANACS-2620 EX240 students cannot join (whitelist root cause, Admin error, waiting room, late sync, end lesson) — https://manabiebiz.slack.com/archives/C0BPM7GABDW/p1789976358320349
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Student S3 is a JPREP student NOT yet assigned to Lesson L1
- Dev/PS support can sync S3 into L1 through the JPREP sync

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 starts Lesson L1 from BO | Teacher T1 is in the room | lesson start = before now |
| 2 | Student S3 logs in to Learner Web and opens the schedule | Lesson L1 is not shown for S3 | S3 not a member |
| 3 | Dev/PS support syncs S3 as a member of L1 | Sync accepted | sync time = after lesson start |
| 4 | Student S3 refreshes the schedule | Lesson L1 is shown with a Join button |  |
| 5 | Student S3 clicks Join | Student S3 enters the room and Teacher T1 sees S3 in the participant list |  |

**Severity:** major
**Priority:** high

---

### [JPREP] Live Lesson – Join – Student not assigned to the lesson – Lesson and Join button not shown

**Description:** AC 05.2 — Permission Matrix / Negative — A JPREP student in the same course but not a member of the lesson must not see or join that live lesson.

**Spec sources:**
- [S1] Confluence – [JPREP] Agora in LMSv2 JPREP (functional spec) — https://manabie.atlassian.net/wiki/spaces/LT/pages/892403790
- [S17] Confluence – Virtual Classroom Database Tables (whitelist config for JPREP live lessons) — https://manabie.atlassian.net/wiki/spaces/TECH/pages/722468865
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Student S4 is a JPREP student of course JPREP_COURSE_000000119 but NOT a member of Lesson L1

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 starts Lesson L1 from BO | Teacher T1 is in the room |  |
| 2 | Student S4 logs in to Learner Web and opens the schedule | Lesson L1 is not listed and no Join button for L1 exists |  |
| 3 | Student S4 opens the live lesson URL of L1 copied from another student | Student S4 cannot enter the room (error or redirect to home); Teacher T1 does not see S4 in the participant list | Negative access |

**Severity:** major
**Priority:** high

---

### [JPREP] Live Lesson – Waiting Room – Teacher enables waiting room – Student waits until teacher turns it off

**Description:** AC 05.6 — State Transition — When the waiting room is on, joining students stay in the waiting room with the message seen in the incident until the teacher turns it off.

**Spec sources:**
- [S13] Slack #jp_incidents – MANACS-2620 EX240 students cannot join (whitelist root cause, Admin error, waiting room, late sync, end lesson) — https://manabiebiz.slack.com/archives/C0BPM7GABDW/p1789976358320349
- [S19] Confluence – Live Lesson Smoke Test Planning on PROD (share screen hidden on JPREP; recording & private chat JPREP only) — https://manabie.atlassian.net/wiki/spaces/LT/pages/411631738
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Student S1 and Student S2 are JPREP student accounts assigned to Lesson L1 (e.g. Staging sync student tongan.pham+student45@manabie.com; UAT jprep-superman62 / jprep-superman63 from source S22)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 starts Lesson L1 from BO and enables the waiting room | Teacher sees the message "Waiting room is now enabled for your students. They will wait until you turn this mode off under class." | Exact text from S13 |
| 2 | Student S1 clicks Join on L1 | Student S1 is placed in the waiting room and does not see the teacher's video or materials | State = Waiting |
| 3 | Teacher T1 turns the waiting room off | Waiting room mode is off |  |
| 4 | Student S1 looks at the screen | Student S1 is moved into the live room automatically and sees the teacher | State = In room |

**Severity:** minor
**Priority:** medium

---

### [JPREP] Live Lesson – End – Teacher ends lesson for all – Students leave the room and Join button no longer shown

**Description:** AC 05.7 — State Transition — After End for all, the lesson is treated as ended: students are removed and cannot rejoin (incident S13 showed EX240 ended by the teacher).

**Spec sources:**
- [S13] Slack #jp_incidents – MANACS-2620 EX240 students cannot join (whitelist root cause, Admin error, waiting room, late sync, end lesson) — https://manabiebiz.slack.com/archives/C0BPM7GABDW/p1789976358320349
- [S19] Confluence – Live Lesson Smoke Test Planning on PROD (share screen hidden on JPREP; recording & private chat JPREP only) — https://manabie.atlassian.net/wiki/spaces/LT/pages/411631738
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Student S1 and Student S2 are JPREP student accounts assigned to Lesson L1 (e.g. Staging sync student tongan.pham+student45@manabie.com; UAT jprep-superman62 / jprep-superman63 from source S22)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Teacher T1, Student S1 and Student S2 are inside the live room of L1

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 clicks End lesson for all and confirms | Teacher Web tab closes |  |
| 2 | Student S1 and Student S2 look at their screens | Both students are taken out of the room with an ended/left message |  |
| 3 | Student S1 refreshes the lesson schedule | Lesson L1 no longer shows a Join button | State = Ended |

**Severity:** major
**Priority:** high

---
