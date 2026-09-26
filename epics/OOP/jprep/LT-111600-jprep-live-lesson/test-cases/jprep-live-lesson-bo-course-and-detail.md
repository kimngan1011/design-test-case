# Test Cases: LT-111600 — JPREP Live Lesson

## Suite: [JPREP] Live Lesson – BO Course Lesson Tab & Lesson Detail

_Course > Lesson tab (Week ↔ paired live lesson), lesson detail Start Live Lesson button by teaching medium, sync-driven changes. Sources: S1, S2, S3._

### [JPREP] Live Lesson – Course Lesson Tab – Week List – Paired lesson name shown for every week

**Description:** AC 02.1 — Component — In JPREP Back Office, the Lesson tab of a course lists every Week together with the name of the live lesson paired to that week.

**Spec sources:**
- [S1] Confluence – [JPREP] Agora in LMSv2 JPREP (functional spec) — https://manabie.atlassian.net/wiki/spaces/LT/pages/892403790
- [S2a] Jira LT-56315 – Add Lesson column in Course detail > Lesson tab — https://manabie.atlassian.net/browse/LT-56315
- [S2b] Jira LT-54446 – Design: join live lesson through BO (Lesson tab per Week + Start button) — https://manabie.atlassian.net/browse/LT-54446
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- JPREP BO Admin (HQ Staff) account is available and has Course Management access
- Course C1 = JPREP_COURSE_000000119 has Week 1, Week 2 and Week 3 synced from JPREP
- Week 1 is paired with lesson "L-W1", Week 2 with lesson "L-W2", Week 3 with lesson "L-W3"

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | JPREP BO Admin logs in to JPREP Back Office | Back Office home page is shown with the left-side menu | URL = https://backoffice-mfe.staging.jprep.manabie.io |
| 2 | JPREP BO Admin clicks Course in the left-side menu | Course list is shown |  |
| 3 | JPREP BO Admin searches for course C1 and clicks its name | Course detail page of C1 is shown with its tabs | course_id = JPREP_COURSE_000000119 |
| 4 | JPREP BO Admin clicks the Lesson tab | The Lesson tab shows a table of Weeks with a Lesson column |  |
| 5 | JPREP BO Admin reads the Week and Lesson columns of every row | Row Week 1 shows lesson name L-W1; row Week 2 shows L-W2; row Week 3 shows L-W3; no row has an empty lesson name | Week 1 -> L-W1; Week 2 -> L-W2; Week 3 -> L-W3 |

**Severity:** minor
**Priority:** medium

---

### [JPREP] Live Lesson – Course Lesson Tab – Click Lesson Name – Lesson detail of the paired lesson opens

**Description:** AC 02.2 — Scenario — Clicking the lesson name in a Week row redirects the BO user to the lesson detail page of the paired live lesson.

**Spec sources:**
- [S1] Confluence – [JPREP] Agora in LMSv2 JPREP (functional spec) — https://manabie.atlassian.net/wiki/spaces/LT/pages/892403790
- [S2a] Jira LT-56315 – Add Lesson column in Course detail > Lesson tab — https://manabie.atlassian.net/browse/LT-56315
- [S2b] Jira LT-54446 – Design: join live lesson through BO (Lesson tab per Week + Start button) — https://manabie.atlassian.net/browse/LT-54446
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Course C1 = JPREP_COURSE_000000119 has Week 2 paired with Lesson L1
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 logs in to JPREP Back Office | Back Office home page is shown | username = jprep.teachertest01 |
| 2 | Teacher T1 opens Course > course C1 > Lesson tab | Lesson tab lists the Weeks of course C1 | course_id = JPREP_COURSE_000000119 |
| 3 | Teacher T1 clicks the lesson name L1 in row Week 2 | Browser navigates to the lesson detail page of Lesson L1 |  |
| 4 | Teacher T1 reads the page header, lesson date/time and course on the detail page | Lesson name = L1, course = C1, date/time equals the synced start/end of L1 in JST |  |
| 5 | Teacher T1 reads the browser address bar | URL contains /lesson/lesson_management/JPREP_LESSON_<L1>/show | Expected path pattern: /lesson/lesson_management/<lesson_id>/show |

**Severity:** minor
**Priority:** medium

---

### [JPREP] Live Lesson – Lesson Detail – Teaching Medium Online – Start Live Lesson button shown and enabled

**Description:** AC 03.1 — Decision Table — When the synced lesson is Online, the lesson detail page shows an enabled Start Live Lesson button.

**Spec sources:**
- [S1] Confluence – [JPREP] Agora in LMSv2 JPREP (functional spec) — https://manabie.atlassian.net/wiki/spaces/LT/pages/892403790
- [S3] Jira LT-57917 – Hide Start Lesson when teaching medium is Offline — https://manabie.atlassian.net/browse/LT-57917
- [S2] Jira LT-54444 – [LMS 2.0][JPREP] Launch Live Lesson on BO (epic + child tickets) — https://manabie.atlassian.net/browse/LT-54444
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 logs in to JPREP Back Office | Back Office home page is shown | username = jprep.teachertest01 |
| 2 | Teacher T1 opens the lesson detail page of Lesson L1 (Lesson Management > L1) | Lesson detail page of L1 is shown | teaching_medium = Online |
| 3 | Teacher T1 reads the Teaching Medium field | Teaching Medium shows Online |  |
| 4 | Teacher T1 looks for the Start Live Lesson button | Start Live Lesson button is visible and enabled (clickable) | Decision: Online -> button shown + enabled |

**Severity:** major
**Priority:** high

---

### [JPREP] Live Lesson – Lesson Detail – Teaching Medium Offline – Start Live Lesson button not available

**Description:** AC 03.1 — Decision Table / Negative — When the synced lesson is Offline, the Start Live Lesson button is hidden or disabled so no live room can be opened.

**Spec sources:**
- [S3] Jira LT-57917 – Hide Start Lesson when teaching medium is Offline — https://manabie.atlassian.net/browse/LT-57917
- [S1] Confluence – [JPREP] Agora in LMSv2 JPREP (functional spec) — https://manabie.atlassian.net/wiki/spaces/LT/pages/892403790
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Lesson L2 is synced from JPREP with teaching medium = Offline, course JPREP_COURSE_000000119, teacher = T1

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 logs in to JPREP Back Office | Back Office home page is shown | username = jprep.teachertest01 |
| 2 | Teacher T1 opens the lesson detail page of Lesson L2 | Lesson detail page of L2 is shown | teaching_medium = Offline |
| 3 | Teacher T1 reads the Teaching Medium field | Teaching Medium shows Offline |  |
| 4 | Teacher T1 looks for the Start Live Lesson button | Start Live Lesson button is not displayed, or is displayed disabled and cannot be clicked | Decision: Offline -> button hidden/disabled |
| 5 | Teacher T1 tries to click the area of the Start Live Lesson button (if displayed disabled) | Nothing happens: no new browser tab, no Teacher Web page opens |  |

**Severity:** major
**Priority:** high

---

### [JPREP] Live Lesson – Lesson Sync – Offline changed to Online by JPREP – Start Live Lesson button becomes available

**Description:** AC 01.2 — State Transition — An irregular lesson switched from Offline to Online by JPREP sync (e.g. typhoon day) shows the Start Live Lesson button after the sync.

**Spec sources:**
- [S13] Slack #jp_incidents – MANACS-2620 EX240 students cannot join (whitelist root cause, Admin error, waiting room, late sync, end lesson) — https://manabiebiz.slack.com/archives/C0BPM7GABDW/p1789976358320349
- [S3] Jira LT-57917 – Hide Start Lesson when teaching medium is Offline — https://manabie.atlassian.net/browse/LT-57917
- [S1] Confluence – [JPREP] Agora in LMSv2 JPREP (functional spec) — https://manabie.atlassian.net/wiki/spaces/LT/pages/892403790
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Lesson L3 exists with teaching medium = Offline, course JPREP_COURSE_000000119, teacher = T1
- Dev/PS support can re-send the JPREP sync payload for L3 with lesson_type = online (same payload shape as source S13: m_lesson with lesson_type, start_datetime, end_datetime, m_course_name_id)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 opens the lesson detail page of Lesson L3 in JPREP Back Office | Teaching Medium shows Offline and the Start Live Lesson button is not available | State before = Offline |
| 2 | Dev/PS support sends the JPREP sync for L3 with lesson_type = online | Sync request is accepted (no error returned) | lesson_type: offline -> online |
| 3 | Teacher T1 reloads the lesson detail page of L3 | Teaching Medium shows Online | State after = Online |
| 4 | Teacher T1 looks for the Start Live Lesson button | Start Live Lesson button is visible and enabled |  |

**Severity:** major
**Priority:** high

---

### [JPREP] Live Lesson – Lesson Time – Lesson at 00:30 JST – BO and Learner show the JST date, not the UTC date

**Description:** AC 01.1 — Boundary Value Analysis (timezone) — JPREP sends lesson times as Unix time (UTC); a lesson at 00:30 JST must appear on the JST calendar date in BO and Learner, not on the previous UTC date.

**Spec sources:**
- [S13] Slack #jp_incidents – MANACS-2620 EX240 students cannot join (whitelist root cause, Admin error, waiting room, late sync, end lesson) — https://manabiebiz.slack.com/archives/C0BPM7GABDW/p1789976358320349
- [S1] Confluence – [JPREP] Agora in LMSv2 JPREP (functional spec) — https://manabie.atlassian.net/wiki/spaces/LT/pages/892403790
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Student S1 is assigned to the lesson
- Lesson L4 is synced with start_datetime = 1790609400 and end_datetime = 1790614800 (= 2026-09-29 00:30–02:00 JST = 2026-09-28 15:30–17:00 UTC), teaching medium Online, course JPREP_COURSE_000000119
- Browser and device time zone of the tester is Asia/Tokyo

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 opens the lesson detail page of Lesson L4 in JPREP Back Office | Lesson date shows 2026-09-29 and time 00:30 – 02:00 | start = 2026-09-29 00:30 JST (= 2026-09-28 15:30 UTC); end = 2026-09-29 02:00 JST (= 2026-09-28 17:00 UTC) |
| 2 | Teacher T1 reads the lesson date again | Lesson date is NOT 2026-09-28 and time is NOT 15:30 | UTC date 2026-09-28 must not be displayed |
| 3 | Student S1 logs in to Learner Web and opens the lesson schedule | Lesson L4 is listed under 2026-09-29 with time 00:30 – 02:00 | Learner time zone = Asia/Tokyo |
| 4 | Tester changes device time zone to UTC and Student S1 reloads the lesson schedule | The lesson start/end shown still equals the same instant (00:30 JST = 15:30 UTC); the app does not shift it twice | device TZ = UTC; record the displayed value as evidence |

**Severity:** minor
**Priority:** medium

---
