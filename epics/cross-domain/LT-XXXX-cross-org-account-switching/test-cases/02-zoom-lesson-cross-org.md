# Test Cases: LT-XXXX — Cross-organization account switching

## Suite: View and join lesson zoom

### Account Switch – Zoom Lesson – Cross-org students – Each student joins own Zoom lesson

**Description:** AC PX-1507.01 — Scenario — Each student at Renseikai and Asojuku opens and joins the Zoom lesson assigned to that student.

**Preconditions:**
- Student Renseikai is logged in to the mobile app.
- Student Asojuku is logged in to the mobile app.
- Student Renseikai has a joinable Zoom lesson `Renseikai Zoom`.
- Student Asojuku has a joinable Zoom lesson `Asojuku Zoom`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Student Renseikai opens `Renseikai Zoom` and selects the join action. | Student Renseikai is directed to the Zoom meeting for `Renseikai Zoom`. | organization = Renseikai; lesson = Renseikai Zoom |
| 2 | Student Asojuku opens `Asojuku Zoom` and selects the join action. | Student Asojuku is directed to the Zoom meeting for `Asojuku Zoom`. | organization = Asojuku; lesson = Asojuku Zoom |

**Severity:** minor
**Priority:** medium
