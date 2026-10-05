# Test Cases: LT-XXXX — Cross-organization account switching

## Suite: Lesson Survey

### Account Switch – Lesson Survey – Cross-org students – Each student submits own survey

**Description:** AC PX-331.01 — Scenario — Students at Renseikai and Asojuku submit separate surveys for their own completed lessons.

**Preconditions:**
- Student Renseikai is logged in to the mobile app.
- Student Asojuku is logged in to the mobile app.
- Student Renseikai has a completed lesson with an available survey.
- Student Asojuku has a completed lesson with an available survey.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Student Renseikai opens the available survey, enters rating `5` and comment `Renseikai survey response`, and submits it. | The app confirms the survey submission for Student Renseikai's completed lesson. | organization = Renseikai; rating = 5 |
| 2 | Student Asojuku opens the available survey, enters rating `4` and comment `Asojuku survey response`, and submits it. | The app confirms the survey submission for Student Asojuku's completed lesson. | organization = Asojuku; rating = 4 |

**Severity:** minor
**Priority:** medium

---

### Account Switch – Survey Response – Cross-org students – Parent sees selected student's survey

**Description:** AC PX-331.02 — Scenario — A parent switches students and views the submitted survey response belonging to each selected student.

**Preconditions:**
- Parent CrossOrg is logged in to the mobile app.
- Parent CrossOrg is linked to Student Renseikai at Renseikai.
- Parent CrossOrg is linked to Student Asojuku at Asojuku.
- Student Renseikai submitted a survey with comment `Renseikai survey response`.
- Student Asojuku submitted a survey with comment `Asojuku survey response`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Parent CrossOrg selects Student Renseikai and opens the submitted lesson survey. | The survey response displays `Renseikai survey response`. | selected student = Student Renseikai |
| 2 | Parent CrossOrg switches to Student Asojuku and opens the submitted lesson survey. | The survey response displays `Asojuku survey response`. | selected student = Student Asojuku |
| 3 | Parent CrossOrg returns to Student Renseikai's submitted lesson survey. | The survey response displays `Renseikai survey response` and does not display the Asojuku response. | selected student = Student Renseikai |

**Severity:** minor
**Priority:** medium
