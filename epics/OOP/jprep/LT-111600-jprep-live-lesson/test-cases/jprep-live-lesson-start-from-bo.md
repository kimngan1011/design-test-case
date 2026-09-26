# Test Cases: LT-111600 — JPREP Live Lesson

## Suite: [JPREP] Live Lesson – Start from BO

_Start Live Lesson from JPREP BO → Teacher Web live room (SSO, URL, account, refresh, leave/end, role, recording dialog). Sources: S2, S4–S10, S13, S15, S20, S23._

### [JPREP] Live Lesson – Start – Teacher clicks Start Live Lesson – Live room opens in a new tab without login and BO tab stays

**Description:** AC 03.2 — Scenario — The JPREP teacher starts the live lesson from BO; Teacher Web opens the live room in a new tab with the same account and no extra login.

**Spec sources:**
- [S1] Confluence – [JPREP] Agora in LMSv2 JPREP (functional spec) — https://manabie.atlassian.net/wiki/spaces/LT/pages/892403790
- [S2] Jira LT-54444 – [LMS 2.0][JPREP] Launch Live Lesson on BO (epic + child tickets) — https://manabie.atlassian.net/browse/LT-54444
- [S4] Jira LT-56380 – Single sign-on when opening Teacher Web from BO — https://manabie.atlassian.net/browse/LT-56380
- [S13] Slack #jp_incidents – MANACS-2620 EX240 students cannot join (whitelist root cause, Admin error, waiting room, late sync, end lesson) — https://manabiebiz.slack.com/archives/C0BPM7GABDW/p1789976358320349
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Teacher T1 is NOT logged in to Teacher Web in this browser (clear Teacher Web session first)
- Browser allows camera and microphone for the Teacher Web domain

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 logs in to JPREP Back Office | Back Office home page is shown | username = jprep.teachertest01 |
| 2 | Teacher T1 opens the lesson detail page of Lesson L1 | Start Live Lesson button is visible and enabled |  |
| 3 | Teacher T1 clicks Start Live Lesson once | A new browser tab opens on the Teacher Web domain; the BO tab stays on the lesson detail page of L1 | Expected new tab domain = teacher.staging.jprep.manabie.io |
| 4 | Teacher T1 looks at the new tab | No login screen is shown; Teacher Web goes straight to the live lesson room of L1 (or its lesson screen with the room loading) | SSO: no username/password prompt |
| 5 | Teacher T1 reads the teacher name shown in the room / participant list | The teacher shown is T1 (jprep.teachertest01) |  |
| 6 | Teacher T1 switches back to the BO tab | BO lesson detail page of L1 is still displayed and usable |  |

**Severity:** critical
**Priority:** high

---

### [JPREP] Live Lesson – Start URL – ImproveSSO flag OFF – URL has single slash, course_id before lesson_id and the teacher user_id

**Description:** AC 03.3 — Decision Table — With User_Authentication_ImproveSSO OFF, the Teacher Web URL uses the JPREP liveStreamScreen structure fixed in LT-91604 and carries user_id (LT-98048).

**Spec sources:**
- [S7] Jira LT-88036 – Live lesson redirect URL + unleash User_Authentication_ImproveSSO — https://manabie.atlassian.net/browse/LT-88036
- [S8] Jira LT-91604 – Fix JPREP live lesson URL (no double slash, course_id first) — https://manabie.atlassian.net/browse/LT-91604
- [S9] Jira LT-98048 – Attach user_id to JPREP live lesson URL — https://manabie.atlassian.net/browse/LT-98048
- [S23] Confluence – Live Lesson - Launch Live lesson from BO (JPREP URL structure) — https://manabie.atlassian.net/wiki/spaces/TECH/pages/953253916
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Unleash flag User_Authentication_ImproveSSO = OFF for JPREP Staging
- Teacher T1 user ID is known (from BO Staff detail or dev support) = <T1_user_id>

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 logs in to JPREP Back Office and opens the lesson detail page of Lesson L1 | Start Live Lesson button is enabled | User_Authentication_ImproveSSO = OFF |
| 2 | Teacher T1 clicks Start Live Lesson | A new Teacher Web tab opens |  |
| 3 | Teacher T1 copies the full URL of the new tab | URL = https://teacher.staging.jprep.manabie.io/#/liveStreamScreen?course_id=JPREP_COURSE_000000119&lesson_id=JPREP_LESSON_<L1>&user_id=<T1_user_id> | Reference PROD example: https://teacher.prod.jprep.manabie.io/#/liveStreamScreen?course_id=JPREP_COURSE_000000122&lesson_id=JPREP_LESSON_010198766 |
| 4 | Teacher T1 inspects the URL path after # | Path contains exactly one slash before liveStreamScreen ("#/liveStreamScreen"), never "#//" or "#////" | Regression of LT-91604 |
| 5 | Teacher T1 inspects the query parameter order and values | Parameter course_id comes first, then lesson_id, then user_id; user_id is present, is NOT empty and equals <T1_user_id> |  |

**Severity:** major
**Priority:** high

---

### [JPREP] Live Lesson – Start URL – ImproveSSO flag ON – URL uses redirect format with JPREP live lesson data

**Description:** AC 03.3 — Decision Table — With User_Authentication_ImproveSSO ON, Start Live Lesson opens <teacher domain>/redirect?data=<base64>, where data decodes to organization_name=jprep, empty access_level, context=live_lesson and the lesson ID.

**Spec sources:**
- [S7] Jira LT-88036 – Live lesson redirect URL + unleash User_Authentication_ImproveSSO — https://manabie.atlassian.net/browse/LT-88036
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Unleash flag User_Authentication_ImproveSSO = ON for the JPREP environment under test (confirm env with dev – open question 7)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 logs in to JPREP Back Office and opens the lesson detail page of Lesson L1 | Start Live Lesson button is enabled | User_Authentication_ImproveSSO = ON |
| 2 | Teacher T1 clicks Start Live Lesson | A new Teacher Web tab opens |  |
| 3 | Teacher T1 copies the URL of the new tab before it redirects (or from browser history) | URL = https://teacher.staging.jprep.manabie.io/#/redirect?data=<base64 value> |  |
| 4 | Tester decodes the data value from Base64 | Decoded text = organization_name=jprep&access_level=&context=live_lesson&lesson_id=JPREP_LESSON_<L1> | access_level must be empty for JPREP |
| 5 | Teacher T1 waits for Teacher Web to finish redirecting | Live lesson room of L1 is opened as Teacher T1 without a login prompt |  |

**Severity:** major
**Priority:** high

---

### [JPREP] Live Lesson – Start – BO account switched from Teacher T1 to Teacher T2 – Live room opens as Teacher T2

**Description:** AC 03.4 — Scenario — After logging out T1 and logging in T2 in the same browser, Start Live Lesson must enter the room as T2, not the cached T1 session (LT-98050).

**Spec sources:**
- [S10] Jira LT-98050 – Switch teacher account BO -> Teacher Web (JPREP) — https://manabie.atlassian.net/browse/LT-98050
- [S9] Jira LT-98048 – Attach user_id to JPREP live lesson URL — https://manabie.atlassian.net/browse/LT-98048
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Teacher T2 account is available: Teacher T2 = JPREP teacher account jprep.teachertest02 (password: see source S10 / team vault)
- Lesson L1 is synced with teaching medium Online and teachers T1 and T2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 logs in to JPREP Back Office and clicks Start Live Lesson on Lesson L1 | Teacher Web tab opens the room as Teacher T1 | account 1 = jprep.teachertest01 |
| 2 | Teacher T1 closes the Teacher Web tab | Only the BO tab remains |  |
| 3 | Teacher T1 logs out of JPREP Back Office | BO login page is shown |  |
| 4 | Teacher T2 logs in to JPREP Back Office in the same browser | BO home page is shown for T2 | account 2 = jprep.teachertest02 |
| 5 | Teacher T2 opens Lesson L1 and clicks Start Live Lesson | A new Teacher Web tab opens |  |
| 6 | Teacher T2 reads the teacher name in the room and the user_id in the URL | Room shows Teacher T2; URL user_id = <T2_user_id>; T1 is NOT shown as the current user | Bug before fix: room opened as T1 |

**Severity:** major
**Priority:** high

---

### [JPREP] Live Lesson – In Room – Teacher refreshes the live lesson page – Teacher stays in the live room

**Description:** AC 03.5 — State Transition — Refreshing the Teacher Web live lesson page keeps the teacher in the live room instead of going back to lesson detail (LT-56381).

**Spec sources:**
- [S5] Jira LT-56381 – Keep staying in live lesson after refresh — https://manabie.atlassian.net/browse/LT-56381
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Teacher T1 has started Lesson L1 from BO and is inside the live room
- Student S1 is inside the live room

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 presses the browser refresh button (F5) on the live room tab | Page reloads |  |
| 2 | Teacher T1 waits up to 30 seconds | Teacher T1 is back inside the live room of L1 (not on lesson detail, not on login) | wait <= 30 s |
| 3 | Student S1 looks at the participant list | Teacher T1 appears in the room again |  |

**Severity:** minor
**Priority:** medium

---

### [JPREP] Live Lesson – Leave – Teacher leaves or ends the lesson – Teacher Web browser tab closes

**Description:** AC 03.6 — State Transition — When the teacher leaves or ends the lesson, the Teacher Web tab opened from BO closes (LT-56382); the BO tab remains.

**Spec sources:**
- [S6] Jira LT-56382 – Close browser tab when leaving / ending live lesson — https://manabie.atlassian.net/browse/LT-56382
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Teacher T1 opened the live room of L1 from BO (Teacher Web tab opened by Start Live Lesson)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 clicks the Leave button in the live room and confirms Leave (not End for all) | Teacher Web tab closes automatically | Action = Leave |
| 2 | Teacher T1 looks at the remaining tabs | BO lesson detail tab of L1 is still open |  |
| 3 | Teacher T1 clicks Start Live Lesson again and, in the room, clicks End lesson for all and confirms | Teacher Web tab closes automatically | Action = End for all |

**Severity:** minor
**Priority:** medium

---

### [JPREP] Live Lesson – Role – JPREP Admin clicks Start Live Lesson with AllowAllRoles flag OFF – "Account is not registered" shown and no room entered

**Description:** AC 03.7 — Permission Matrix — In JPREP only teachers can enter the live room; an Admin gets the error seen in the 2026-09-21 incident when User_Auth_AllowAllRolesToLoginTeacherWeb is OFF.

**Spec sources:**
- [S13] Slack #jp_incidents – MANACS-2620 EX240 students cannot join (whitelist root cause, Admin error, waiting room, late sync, end lesson) — https://manabiebiz.slack.com/archives/C0BPM7GABDW/p1789976358320349
- [S15] Slack #draft-discuss-lesson-feature 2026-09-23 – re-test plan + unleash User_Auth_AllowAllRolesToLoginTeacherWeb — https://manabiebiz.slack.com/archives/C0BNPCH3605/p1790133887305919
- [S11] Confluence – [JPREP][External] Role access level for backoffice — https://manabie.atlassian.net/wiki/spaces/LT/pages/969212037
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- JPREP BO Admin (non-teacher) account is available
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Unleash flag User_Auth_AllowAllRolesToLoginTeacherWeb = OFF for the JPREP environment under test

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | JPREP BO Admin logs in to JPREP Back Office and opens the lesson detail page of Lesson L1 | Start Live Lesson button is visible | role = Admin; flag = OFF |
| 2 | JPREP BO Admin clicks Start Live Lesson | A Teacher Web tab opens |  |
| 3 | JPREP BO Admin reads the Teacher Web tab | Error popup "Account is not registered" is shown; the live room is not entered | Exact text from incident: "Account is not registered" |
| 4 | Teacher T1 (in another browser) opens the room of L1 | Admin does not appear in the participant list |  |

**Severity:** major
**Priority:** high

---

### [JPREP] Live Lesson – Role – JPREP Admin clicks Start Live Lesson with AllowAllRoles flag ON – Admin enters the live room

**Description:** AC 03.7 — Permission Matrix — Per dev note (S15), turning ON User_Auth_AllowAllRolesToLoginTeacherWeb allows the Admin to join. Expected result must be confirmed with PM (open question 2).

**Spec sources:**
- [S15] Slack #draft-discuss-lesson-feature 2026-09-23 – re-test plan + unleash User_Auth_AllowAllRolesToLoginTeacherWeb — https://manabiebiz.slack.com/archives/C0BNPCH3605/p1790133887305919
- [S13] Slack #jp_incidents – MANACS-2620 EX240 students cannot join (whitelist root cause, Admin error, waiting room, late sync, end lesson) — https://manabiebiz.slack.com/archives/C0BPM7GABDW/p1789976358320349
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- JPREP BO Admin (non-teacher) account is available
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Unleash flag User_Auth_AllowAllRolesToLoginTeacherWeb = ON for the JPREP environment under test

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | JPREP BO Admin logs in to JPREP Back Office and opens the lesson detail page of Lesson L1 | Start Live Lesson button is visible | role = Admin; flag = ON |
| 2 | JPREP BO Admin clicks Start Live Lesson | A Teacher Web tab opens without "Account is not registered" |  |
| 3 | JPREP BO Admin waits for the page to load | Admin is inside the live room of L1 and shown with the Admin's own name |  |
| 4 | JPREP BO Admin sets the flag back to OFF with dev support after the run | Flag state restored to the environment default | restore flag |

**Severity:** major
**Priority:** high

---

### [JPREP] Live Lesson – Start – Recording confirmation dialog – Cancel enters the room without recording

**Description:** AC 03.8 — Decision Table — If the recording confirmation dialog appears when starting from BO, Cancel must be clickable and let the teacher enter the room without recording (MANACS-2343).

**Spec sources:**
- [S20] Jira MANACS-2343 – [JPREP] Unable to start online lesson from BO (recording dialog Cancel) — https://manabie.atlassian.net/browse/MANACS-2343
- [S19] Confluence – Live Lesson Smoke Test Planning on PROD (share screen hidden on JPREP; recording & private chat JPREP only) — https://manabie.atlassian.net/wiki/spaces/LT/pages/411631738
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Recording feature is enabled for JPREP (JPREP-only feature per S19)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 logs in to JPREP Back Office and clicks Start Live Lesson on Lesson L1 | Teacher Web tab opens and the recording confirmation dialog is shown |  |
| 2 | Teacher T1 clicks Cancel in the recording dialog | Dialog closes on the first click (button is clickable) | Choice = Cancel |
| 3 | Teacher T1 looks at the room | Teacher T1 is inside the live room; no recording indicator is shown |  |
| 4 | Student S1 joins the room from Learner Web | Student S1 sees the room; no recording indicator is shown to the student |  |

**Severity:** major
**Priority:** high

---

### [JPREP] Live Lesson – Start – Recording confirmation dialog – Start recording enters the room with recording on

**Description:** AC 03.8 — Decision Table — Choosing Start recording in the dialog enters the room and starts recording; the teacher is not left on an error screen (MANACS-2343).

**Spec sources:**
- [S20] Jira MANACS-2343 – [JPREP] Unable to start online lesson from BO (recording dialog Cancel) — https://manabie.atlassian.net/browse/MANACS-2343
- [S19] Confluence – Live Lesson Smoke Test Planning on PROD (share screen hidden on JPREP; recording & private chat JPREP only) — https://manabie.atlassian.net/wiki/spaces/LT/pages/411631738
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Recording feature is enabled for JPREP

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 logs in to JPREP Back Office and clicks Start Live Lesson on Lesson L1 | Recording confirmation dialog is shown |  |
| 2 | Teacher T1 clicks Start recording | Dialog closes | Choice = Start recording |
| 3 | Teacher T1 looks at the room | Teacher T1 is inside the live room and a recording indicator is shown; no error screen |  |
| 4 | Teacher T1 stops the recording (or ends the lesson) | Recording stops without error |  |

**Severity:** major
**Priority:** high

---
