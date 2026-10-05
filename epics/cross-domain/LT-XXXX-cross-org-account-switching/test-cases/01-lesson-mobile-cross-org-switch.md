# Test Cases: LT-XXXX — Cross-organization account switching

## Suite: Lesson Mobile

### Account Switch – Lesson Details – Cross-org students – Each student's lesson is isolated

**Description:** AC PX-320.01 — Scenario — A parent switches between Renseikai and Asojuku students and sees each student's own lesson details.

**Preconditions:**
- Parent CrossOrg is logged in to the mobile app.
- Parent CrossOrg is linked to Student Renseikai at Renseikai.
- Parent CrossOrg is linked to Student Asojuku at Asojuku.
- Student Renseikai has lesson `Renseikai Math`.
- Student Asojuku has lesson `Asojuku English`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Parent CrossOrg selects Student Renseikai and opens the lesson list. | The lesson list contains `Renseikai Math` and does not contain `Asojuku English`. | selected student = Student Renseikai; organization = Renseikai |
| 2 | Parent CrossOrg opens `Renseikai Math`. | The lesson detail shows Student Renseikai's lesson information. | lesson = Renseikai Math |
| 3 | Parent CrossOrg switches to Student Asojuku and opens the lesson list. | The lesson list contains `Asojuku English` and does not contain `Renseikai Math`. | selected student = Student Asojuku; organization = Asojuku |
| 4 | Parent CrossOrg opens `Asojuku English`. | The lesson detail shows Student Asojuku's lesson information. | lesson = Asojuku English |

**Severity:** minor
**Priority:** medium

---

### Account Switch – Lesson Report – Cross-org students – Each student's report is isolated

**Description:** AC PX-320.02 — Scenario — A parent switches students and reads the lesson report belonging to each selected student.

**Preconditions:**
- Parent CrossOrg is logged in to the mobile app.
- Parent CrossOrg is linked to Student Renseikai at Renseikai.
- Parent CrossOrg is linked to Student Asojuku at Asojuku.
- Student Renseikai has a completed lesson with report `Renseikai feedback`.
- Student Asojuku has a completed lesson with report `Asojuku feedback`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Parent CrossOrg selects Student Renseikai and opens the completed lesson report. | The report displays `Renseikai feedback` for Student Renseikai. | selected student = Student Renseikai |
| 2 | Parent CrossOrg switches to Student Asojuku and opens the completed lesson report. | The report displays `Asojuku feedback` for Student Asojuku. | selected student = Student Asojuku |
| 3 | Parent CrossOrg returns to Student Renseikai's completed lesson report. | The report still displays `Renseikai feedback` and does not show Asojuku feedback. | selected student = Student Renseikai |

**Severity:** minor
**Priority:** medium

---

### Account Switch – Attendance – Cross-org students – Submission is recorded for selected student

**Description:** AC PX-320.03 — Scenario — A parent switches students and submits attendance separately for their respective lessons.

**Preconditions:**
- Parent CrossOrg is logged in to the mobile app.
- Parent CrossOrg is linked to Student Renseikai at Renseikai.
- Parent CrossOrg is linked to Student Asojuku at Asojuku.
- Student Renseikai has an attendance request for `Renseikai Math`.
- Student Asojuku has an attendance request for `Asojuku English`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Parent CrossOrg selects Student Renseikai and submits attendance for `Renseikai Math`. | Attendance is submitted for Student Renseikai and the confirmation identifies `Renseikai Math`. | selected student = Student Renseikai; attendance = Present |
| 2 | Parent CrossOrg switches to Student Asojuku and submits attendance for `Asojuku English`. | Attendance is submitted for Student Asojuku and the confirmation identifies `Asojuku English`. | selected student = Student Asojuku; attendance = Present |
| 3 | Parent CrossOrg returns to Student Renseikai's attendance screen. | Student Renseikai's submitted attendance remains displayed and is not replaced by Student Asojuku's submission. | selected student = Student Renseikai |

**Severity:** minor
**Priority:** medium
