# Test Cases: LT-111600 — JPREP Live Lesson

## Suite: [JPREP] Live Lesson – In-room Key Features

_KEY features per Test plan coverage KEY feature for Live Lesson (S18) and JPREP-only behavior from S19: cam/mic, share PDF/image/video, whiteboard, public/private chat, share screen hidden, reconnect._

### [JPREP] Live Lesson – Camera and Mic – Teacher and student toggle on and off – State shown on the other side

**Description:** AC 06.1 — Scenario — Camera/mic toggles of teacher and student are reflected in each other's view.

**Spec sources:**
- [S18] Confluence – Test plan coverage KEY feature for Live Lesson — https://manabie.atlassian.net/wiki/spaces/TECH/pages/2189852681
- [S19] Confluence – Live Lesson Smoke Test Planning on PROD (share screen hidden on JPREP; recording & private chat JPREP only) — https://manabie.atlassian.net/wiki/spaces/LT/pages/411631738
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Student S1 and Student S2 are JPREP student accounts assigned to Lesson L1 (e.g. Staging sync student tongan.pham+student45@manabie.com; UAT jprep-superman62 / jprep-superman63 from source S22)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Teacher T1 started Lesson L1 from BO and is inside the live room
- Student S1 (Learner Web, Chrome) and Student S2 (Learner App, iPad or Android) joined the live room

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 turns camera ON and mic ON | Students S1 and S2 see the teacher video and the teacher mic icon as ON |  |
| 2 | Teacher T1 turns camera OFF and mic OFF | Students see the teacher video replaced by placeholder and mic icon OFF |  |
| 3 | Student S1 turns camera ON and mic ON | Teacher T1 sees S1 video and S1 mic icon ON in the participant list |  |
| 4 | Student S1 turns camera OFF and mic OFF | Teacher T1 sees S1 camera and mic OFF |  |

**Severity:** major
**Priority:** high

---

### [JPREP] Live Lesson – Camera and Mic – Rapid repeated taps – Final state matches last tap and room stays usable

**Description:** AC 06.1 — Negative (monkey) — Spam-clicking the camera and mic buttons must not freeze the room or leave a mismatched state (monkey test in S18).

**Spec sources:**
- [S18] Confluence – Test plan coverage KEY feature for Live Lesson — https://manabie.atlassian.net/wiki/spaces/TECH/pages/2189852681
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Student S1 and Student S2 are JPREP student accounts assigned to Lesson L1 (e.g. Staging sync student tongan.pham+student45@manabie.com; UAT jprep-superman62 / jprep-superman63 from source S22)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Teacher T1 started Lesson L1 from BO and is inside the live room
- Student S1 (Learner Web, Chrome) and Student S2 (Learner App, iPad or Android) joined the live room

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 clicks the mic button 11 times within 5 seconds | Mic ends in the opposite state of the start (odd number of clicks); icon matches the audio actually sent | 11 clicks / 5 s |
| 2 | Teacher T1 clicks the camera button 11 times within 5 seconds | Camera ends in the opposite state; video tile matches icon | 11 clicks / 5 s |
| 3 | Student S1 checks the teacher tile | Student sees the same final mic/camera state as the teacher icon |  |
| 4 | Teacher T1 shares W2_Slides.pdf | Sharing still works (room not frozen) |  |

**Severity:** major
**Priority:** high

---

### [JPREP] Live Lesson – Share PDF – Teacher shares and changes page – All students see the same page and sharing stops for all

**Description:** AC 06.2 — Scenario — Guard for the 2024-03-30 incident where attendees could not see shared material.

**Spec sources:**
- [S18] Confluence – Test plan coverage KEY feature for Live Lesson — https://manabie.atlassian.net/wiki/spaces/TECH/pages/2189852681
- [S26] Confluence – Postmortem 2024-03-30 Room attendees cannot see the sharing material — https://manabie.atlassian.net/wiki/spaces/TECH/pages/937787471
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Student S1 and Student S2 are JPREP student accounts assigned to Lesson L1 (e.g. Staging sync student tongan.pham+student45@manabie.com; UAT jprep-superman62 / jprep-superman63 from source S22)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Teacher T1 started Lesson L1 from BO and is inside the live room
- Student S1 (Learner Web, Chrome) and Student S2 (Learner App, iPad or Android) joined the live room
- W2_Slides.pdf (2 pages) is in the room material list

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 shares W2_Slides.pdf | S1 (web) and S2 (app) both show page 1 within 5 seconds |  |
| 2 | Teacher T1 moves to page 2 | S1 and S2 both show page 2 | page 1 -> 2 |
| 3 | Teacher T1 stops sharing | The PDF disappears for S1 and S2 |  |

**Severity:** major
**Priority:** high

---

### [JPREP] Live Lesson – Share Image – Image with Japanese file name – Displayed to all students

**Description:** AC 06.2 — Scenario — Teacher can share an image material; Japanese file names are shown without broken characters.

**Spec sources:**
- [S18] Confluence – Test plan coverage KEY feature for Live Lesson — https://manabie.atlassian.net/wiki/spaces/TECH/pages/2189852681
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Student S1 and Student S2 are JPREP student accounts assigned to Lesson L1 (e.g. Staging sync student tongan.pham+student45@manabie.com; UAT jprep-superman62 / jprep-superman63 from source S22)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Teacher T1 started Lesson L1 from BO and is inside the live room
- Student S1 (Learner Web, Chrome) and Student S2 (Learner App, iPad or Android) joined the live room
- Image 教材_第2週.png is uploaded to Week 2 materials

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 opens the room material list | File name 教材_第2週.png is shown without garbled characters | file = 教材_第2週.png |
| 2 | Teacher T1 shares 教材_第2週.png | S1 and S2 see the image |  |
| 3 | Teacher T1 stops sharing | Image disappears for students |  |

**Severity:** minor
**Priority:** medium

---

### [JPREP] Live Lesson – Share Video – Brightcove video material – Plays with sound on student side

**Description:** AC 06.2 — Scenario — JPREP live lesson video material is served via Brightcove; shared video plays for students (S24).

**Spec sources:**
- [S18] Confluence – Test plan coverage KEY feature for Live Lesson — https://manabie.atlassian.net/wiki/spaces/TECH/pages/2189852681
- [S24] Slack #draft-discuss-lesson-feature 2026-07-31 – JPREP live lesson uses Brightcove video — https://manabiebiz.slack.com/archives/C0BNPCH3605
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Student S1 and Student S2 are JPREP student accounts assigned to Lesson L1 (e.g. Staging sync student tongan.pham+student45@manabie.com; UAT jprep-superman62 / jprep-superman63 from source S22)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Teacher T1 started Lesson L1 from BO and is inside the live room
- Student S1 (Learner Web, Chrome) and Student S2 (Learner App, iPad or Android) joined the live room
- Video material W2_Video.mp4 (uploaded, stored on Brightcove) is in Week 2 materials

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 shares W2_Video.mp4 and clicks play | Video plays on teacher side |  |
| 2 | Student S1 and Student S2 watch | Video plays on both with sound, no "video unavailable" error |  |
| 3 | Teacher T1 pauses the video | Video pauses for students |  |
| 4 | Teacher T1 stops sharing | Video disappears for students |  |

**Severity:** major
**Priority:** high

---

### [JPREP] Live Lesson – Whiteboard – Teacher draws and allows student annotation – Drawings synced both ways

**Description:** AC 06.3 — Scenario — Teacher and learner can interact on the whiteboard / annotation layer.

**Spec sources:**
- [S18] Confluence – Test plan coverage KEY feature for Live Lesson — https://manabie.atlassian.net/wiki/spaces/TECH/pages/2189852681
- [S19] Confluence – Live Lesson Smoke Test Planning on PROD (share screen hidden on JPREP; recording & private chat JPREP only) — https://manabie.atlassian.net/wiki/spaces/LT/pages/411631738
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Student S1 and Student S2 are JPREP student accounts assigned to Lesson L1 (e.g. Staging sync student tongan.pham+student45@manabie.com; UAT jprep-superman62 / jprep-superman63 from source S22)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Teacher T1 started Lesson L1 from BO and is inside the live room
- Student S1 (Learner Web, Chrome) and Student S2 (Learner App, iPad or Android) joined the live room
- Teacher T1 is sharing W2_Slides.pdf page 1

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 draws a line with the pen tool on page 1 | S1 and S2 see the line at the same position |  |
| 2 | Teacher T1 enables annotation for students | Annotation tools appear on S1 and S2 |  |
| 3 | Student S1 draws a circle | Teacher T1 and S2 see the circle |  |
| 4 | Teacher T1 disables annotation for students | Annotation tools disappear for students; existing drawings remain |  |

**Severity:** minor
**Priority:** medium

---

### [JPREP] Live Lesson – Public Chat – Teacher and student send messages – Every participant sees both messages

**Description:** AC 06.4 — Scenario — Public chat in the JPREP live room (ChatV1 still used by JPREP – S21).

**Spec sources:**
- [S18] Confluence – Test plan coverage KEY feature for Live Lesson — https://manabie.atlassian.net/wiki/spaces/TECH/pages/2189852681
- [S21] Confluence – [ChatV1] cleanup plan (live lesson chat still used by JPREP) — https://manabie.atlassian.net/wiki/spaces/TECH/pages/2627272747
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Student S1 and Student S2 are JPREP student accounts assigned to Lesson L1 (e.g. Staging sync student tongan.pham+student45@manabie.com; UAT jprep-superman62 / jprep-superman63 from source S22)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Teacher T1 started Lesson L1 from BO and is inside the live room
- Student S1 (Learner Web, Chrome) and Student S2 (Learner App, iPad or Android) joined the live room

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 opens Chat > Public and sends "Hello class 1" | Message appears in the teacher chat | text = Hello class 1 |
| 2 | Student S1 and Student S2 open public chat | Both see "Hello class 1" from Teacher T1 |  |
| 3 | Student S1 sends "Hi teacher" | Teacher T1 and S2 see "Hi teacher" from S1 | text = Hi teacher |

**Severity:** minor
**Priority:** medium

---

### [JPREP] Live Lesson – Private Chat – Teacher messages one student – Only that student receives it

**Description:** AC 06.5 — Permission Matrix — Private chat is a JPREP-only feature (S19); a private message is visible only to the teacher and the target student. Needs mock student data (S18).

**Spec sources:**
- [S18] Confluence – Test plan coverage KEY feature for Live Lesson — https://manabie.atlassian.net/wiki/spaces/TECH/pages/2189852681
- [S19] Confluence – Live Lesson Smoke Test Planning on PROD (share screen hidden on JPREP; recording & private chat JPREP only) — https://manabie.atlassian.net/wiki/spaces/LT/pages/411631738
- [S21] Confluence – [ChatV1] cleanup plan (live lesson chat still used by JPREP) — https://manabie.atlassian.net/wiki/spaces/TECH/pages/2627272747
- [S27] Confluence – JPREP Live Lesson Post-mortem (2023, private chat load) — https://manabie.atlassian.net/wiki/spaces/ERP/pages/791511059
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Student S1 and Student S2 are JPREP student accounts assigned to Lesson L1 (e.g. Staging sync student tongan.pham+student45@manabie.com; UAT jprep-superman62 / jprep-superman63 from source S22)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Teacher T1 started Lesson L1 from BO and is inside the live room
- Student S1 (Learner Web, Chrome) and Student S2 (Learner App, iPad or Android) joined the live room
- Private chat is enabled for JPREP in the environment under test (Staging confirmed working 2026-08-19 – S21; PROD status: open question 6)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 opens a private chat with Student S1 and sends "Private to S1" | Message appears in the T1–S1 private conversation | text = Private to S1 |
| 2 | Student S1 opens private chat | S1 sees "Private to S1" from Teacher T1 |  |
| 3 | Student S2 opens public and private chat | S2 does NOT see "Private to S1" anywhere |  |
| 4 | Student S1 replies "Reply from S1" | Teacher T1 sees the reply; S2 does not | text = Reply from S1 |

**Severity:** major
**Priority:** high

---

### [JPREP] Live Lesson – Share Screen – JPREP teacher room – Share screen control not shown

**Description:** AC 06.6 — Negative — Share screen is hidden for JPREP (S19).

**Spec sources:**
- [S19] Confluence – Live Lesson Smoke Test Planning on PROD (share screen hidden on JPREP; recording & private chat JPREP only) — https://manabie.atlassian.net/wiki/spaces/LT/pages/411631738
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Student S1 and Student S2 are JPREP student accounts assigned to Lesson L1 (e.g. Staging sync student tongan.pham+student45@manabie.com; UAT jprep-superman62 / jprep-superman63 from source S22)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Teacher T1 started Lesson L1 from BO and is inside the live room
- Student S1 (Learner Web, Chrome) and Student S2 (Learner App, iPad or Android) joined the live room

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 looks at the room toolbar and the share menu | No Share screen option is displayed | Tenant = JPREP |

**Severity:** trivial
**Priority:** low

---

### [JPREP] Live Lesson – Reconnect – Student loses network and reconnects – Student back in room seeing the current shared page

**Description:** AC 06.7 — State Transition — Network drops (see MANACS-2179 / JPREP-105) must not lock the student out; after reconnect the student sees the current room state.

**Spec sources:**
- [S19] Confluence – Live Lesson Smoke Test Planning on PROD (share screen hidden on JPREP; recording & private chat JPREP only) — https://manabie.atlassian.net/wiki/spaces/LT/pages/411631738
- [S28] Jira MANACS-2179 / JPREP-105 – Students cannot connect to network during live lesson — https://manabie.atlassian.net/browse/MANACS-2179
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Student S1 and Student S2 are JPREP student accounts assigned to Lesson L1 (e.g. Staging sync student tongan.pham+student45@manabie.com; UAT jprep-superman62 / jprep-superman63 from source S22)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, teacher = T1, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Teacher T1 started Lesson L1 from BO and is inside the live room
- Student S1 (Learner Web, Chrome) and Student S2 (Learner App, iPad or Android) joined the live room
- Teacher T1 is sharing W2_Slides.pdf page 1

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student S1 turns off Wi-Fi for 20 seconds | S1 sees a reconnecting indicator; Teacher T1 sees S1 as disconnected | offline 20 s |
| 2 | Teacher T1 moves to page 2 while S1 is offline | S2 sees page 2 |  |
| 3 | Student S1 turns Wi-Fi back on | S1 rejoins the room automatically within 30 seconds without clicking Join again | wait <= 30 s |
| 4 | Student S1 looks at the shared material | S1 sees page 2 (current page), not page 1 |  |

**Severity:** major
**Priority:** high

---
