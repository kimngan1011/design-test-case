# Test Cases: LT-111600 — JPREP Live Lesson

## Suite: [JPREP] Live Lesson – Weekly Materials

_Upload / view / delete weekly live lesson materials in Course > Lesson tab and their availability in the live room. Admin READWRITE, Teacher READ only. Sources: S1, S11, S18._

### [JPREP] Live Lesson – Materials – Admin uploads a PDF to a week – Material listed for the week and for the learner

**Description:** AC 04.1 — CRUD (Create) — JPREP BO Admin uploads a weekly live lesson material in Course > Lesson tab; it is listed for that week and visible to the learner.

**Spec sources:**
- [S1] Confluence – [JPREP] Agora in LMSv2 JPREP (functional spec) — https://manabie.atlassian.net/wiki/spaces/LT/pages/892403790
- [S11] Confluence – [JPREP][External] Role access level for backoffice — https://manabie.atlassian.net/wiki/spaces/LT/pages/969212037
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- JPREP BO Admin account is available
- Course C1 = JPREP_COURSE_000000119 has Week 2 paired with Lesson L1
- File W2_Slides.pdf (2 pages, < 10 MB) is on the tester's computer
- Student S1 and Student S2 are JPREP student accounts assigned to Lesson L1 (e.g. Staging sync student tongan.pham+student45@manabie.com; UAT jprep-superman62 / jprep-superman63 from source S22)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | JPREP BO Admin opens Course > C1 > Lesson tab in JPREP Back Office | Week list is shown |  |
| 2 | JPREP BO Admin opens the materials of row Week 2 and clicks the add/upload material control | File picker opens |  |
| 3 | JPREP BO Admin selects W2_Slides.pdf and saves | Upload finishes without error | file = W2_Slides.pdf |
| 4 | JPREP BO Admin reads the Week 2 material list | W2_Slides.pdf is listed |  |
| 5 | Student S1 opens Lesson L1 on Learner Web | W2_Slides.pdf is listed in L1 materials and opens in preview |  |

**Severity:** minor
**Priority:** medium

---

### [JPREP] Live Lesson – Materials – Teacher opens week materials – Materials visible but add, edit and delete not available

**Description:** AC 04.2 — Permission Matrix — Per the JPREP role matrix, Teacher has READ on Course Mgt – Lesson: can only see live lesson materials, cannot add, update or delete.

**Spec sources:**
- [S11] Confluence – [JPREP][External] Role access level for backoffice — https://manabie.atlassian.net/wiki/spaces/LT/pages/969212037
- [S2c] Jira LT-56316 / LT-56318 – Teacher left menu & page access in JPREP BO — https://manabie.atlassian.net/browse/LT-56318
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Week 2 of course C1 has material W2_Slides.pdf

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 logs in to JPREP Back Office | Left menu shows only the teacher menu items (no Notification tab) | Role matrix S11 / S12 |
| 2 | Teacher T1 opens Course > C1 > Lesson tab > Week 2 materials | W2_Slides.pdf is listed and can be previewed |  |
| 3 | Teacher T1 looks for add / upload, edit and delete controls | No add/upload, edit or delete control is shown (or they are disabled) | Teacher = READ only |

**Severity:** minor
**Priority:** medium

---

### [JPREP] Live Lesson – Materials – Uploaded week material – Available in the live room and shareable

**Description:** AC 04.3 — Regression — A material uploaded in BO for the week appears in the Teacher Web live room material list and can be shared to students.

**Spec sources:**
- [S1] Confluence – [JPREP] Agora in LMSv2 JPREP (functional spec) — https://manabie.atlassian.net/wiki/spaces/LT/pages/892403790
- [S18] Confluence – Test plan coverage KEY feature for Live Lesson — https://manabie.atlassian.net/wiki/spaces/TECH/pages/2189852681
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Student S1 and Student S2 are JPREP student accounts assigned to Lesson L1 (e.g. Staging sync student tongan.pham+student45@manabie.com; UAT jprep-superman62 / jprep-superman63 from source S22)
- Lesson L1 is synced from JPREP with: lesson ID JPREP_LESSON_<L1>, course JPREP_COURSE_000000119 (whitelisted), teaching medium = Online, students = S1 and S2
- Current time (JST) is inside the lesson window of Lesson L1 (lesson start <= now < lesson end)
- Teacher T1 started Lesson L1 from BO and is inside the live room
- Student S1 (Learner Web, Chrome) and Student S2 (Learner App, iPad or Android) joined the live room
- Week 2 (paired with L1) has material W2_Slides.pdf uploaded in BO

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher T1 opens the material list inside the live room | W2_Slides.pdf is listed |  |
| 2 | Teacher T1 selects W2_Slides.pdf and clicks share | PDF page 1 is displayed on the teacher screen |  |
| 3 | Student S1 and Student S2 look at their screens | Both see page 1 of W2_Slides.pdf |  |

**Severity:** major
**Priority:** high

---

### [JPREP] Live Lesson – Materials – Admin deletes a week material – Removed from BO, learner and live room lists

**Description:** AC 04.1 — CRUD (Delete) — Deleting a weekly material removes it everywhere it was listed.

**Spec sources:**
- [S1] Confluence – [JPREP] Agora in LMSv2 JPREP (functional spec) — https://manabie.atlassian.net/wiki/spaces/LT/pages/892403790
- [S11] Confluence – [JPREP][External] Role access level for backoffice — https://manabie.atlassian.net/wiki/spaces/LT/pages/969212037
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Teacher Web https://teacher.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- JPREP BO Admin account is available
- Teacher T1 account is available: Teacher T1 = JPREP teacher account jprep.teachertest01 (password: see source S10 / team vault)
- Student S1 and Student S2 are JPREP student accounts assigned to Lesson L1 (e.g. Staging sync student tongan.pham+student45@manabie.com; UAT jprep-superman62 / jprep-superman63 from source S22)
- Week 2 of course C1 has materials W2_Slides.pdf and W2_Handout.pdf

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | JPREP BO Admin opens Course > C1 > Lesson tab > Week 2 materials and deletes W2_Handout.pdf, confirming the dialog | W2_Handout.pdf disappears from the list; W2_Slides.pdf remains | deleted = W2_Handout.pdf |
| 2 | Student S1 opens Lesson L1 on Learner Web | Only W2_Slides.pdf is listed |  |
| 3 | Teacher T1 starts Lesson L1 and opens the material list in the room | Only W2_Slides.pdf is listed |  |

**Severity:** minor
**Priority:** medium

---

### [JPREP] Live Lesson – Materials – Admin uploads a PDF and a video to the week of a synced lesson – Both files listed for the week and shown in the lesson on Learner Web

**Description:** AC 04.1 / AC 05.1 — CRUD (Create, multiple files) — Materials are attached to the Week (lesson group) of the course, not to the lesson itself; every lesson synced with that week shows them. One upload adds a PDF and a video at once.

**Spec sources:**
- [S1] Confluence – [JPREP] Agora in LMSv2 JPREP (functional spec) — https://manabie.atlassian.net/wiki/spaces/LT/pages/892403790
- [S11] Confluence – [JPREP][External] Role access level for backoffice — https://manabie.atlassian.net/wiki/spaces/LT/pages/969212037
- [S31] Code – school-portal-admin syllabus LessonTab + LessonUploadDialog (Week / Lesson Date / Materials List / Action > Upload file; PDF, video ≤ 1 GB, audio behind a flag, optional Brightcove) — src/squads/syllabus/components/RelatedCourse/
- [SPEC] Local spec – design-test-case/epics/OOP/jprep/LT-111600-jprep-live-lesson/spec.md

**Preconditions:**
- Environment is JPREP Staging: Back Office https://backoffice-mfe.staging.jprep.manabie.io, Learner Web https://learner.staging.jprep.manabie.io
- JPREP BO Admin account is available (a Teacher account cannot upload)
- Course C1 = JPREP_COURSE_000000119 is on the Staging live lesson course whitelist
- Lesson SYNC-L1 (JPREP_LESSON_090288001) is synced into course C1 with week = Week 5, teaching medium Online, 2026-10-05 18:00–19:00 JST (see PX-29032)
- Student S1 = JPREP Staging student account nt1818895 (password: team vault) is assigned to lesson SYNC-L1 (see PX-29036)
- The Materials List of row Week 5 in Course C1 > Lesson tab is empty
- File SYNC_W5_Slides.pdf (2 pages, under 10 MB) is on the tester's computer
- File SYNC_W5_Video.mp4 (under 1 GB, e.g. 20 MB) is on the tester's computer

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | JPREP BO Admin opens Course, searches JPREP_COURSE_000000119, opens it and clicks the Lesson tab | Section "Upload materials" shows a table with columns Week, Lesson Date, Materials List and Action; row Week 5 shows Lesson Date 2026/10/05 | course_id = JPREP_COURSE_000000119; week = Week 5 |
| 2 | JPREP BO Admin clicks the Action menu of row Week 5 and selects "Upload file" | Dialog "Upload materials" opens |  |
| 3 | JPREP BO Admin selects both files in the file picker | SYNC_W5_Slides.pdf and SYNC_W5_Video.mp4 are both listed in the dialog; no file type or size error is shown | files = SYNC_W5_Slides.pdf, SYNC_W5_Video.mp4 (multiple selection) |
| 4 | JPREP BO Admin clicks Save | The dialog closes without error; the Materials List of row Week 5 shows SYNC_W5_Slides.pdf and SYNC_W5_Video.mp4 |  |
| 5 | JPREP BO Admin clicks Lesson Date 2026/10/05 in row Week 5 | The lesson detail of SYNC-L1 opens (the materials belong to the week paired with this lesson) |  |
| 6 | Student S1 opens lesson SYNC-L1 on Learner Web | SYNC_W5_Slides.pdf and SYNC_W5_Video.mp4 are listed in the materials of SYNC-L1; the PDF opens in preview and the video plays |  |

**Severity:** major
**Priority:** high

---
