# Test Cases: LT-107411 — Duplicate Lesson Indicator

## Suite: [Riso] TAC — Duplicate Lesson Indicator

### [Riso] TAC – Duplicate Lessons – Two lessons in one timeslot – Consolidated calendar chip shown
**Description:** AC 06 — Decision Table — Two lessons for one student-timeslot use the PBT duplicate chip.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- One student has two lessons in Timeslot `B限` on the same date.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens the calendar date for the duplicated lessons. | The `B限` calendar entry shows a warning and `2授業` instead of two normal lesson entries. | timeslot = B限; lesson_count = 2 |
**Severity:** major
**Priority:** high

### [Riso] TAC – Duplicate Lessons – Two lessons in one timeslot – Sidebar alert shown
**Description:** AC 06 — Cross-surface — The duplicate sidebar alert matches the PBT screenshot.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- One student has two lessons in Timeslot `B限` on the same date.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects Timeslot `B限` in the sidebar. | The sidebar shows `授業が重複しています(2件)` and a lesson detail entry. | timeslot = B限; lesson_count = 2 |
**Severity:** major
**Priority:** high

### [Riso] TAC – Duplicate Lessons – One lesson in one timeslot – Normal display retained
**Description:** AC 06 — Negative — A non-duplicate lesson does not show duplicate warning UI.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- One student has one lesson in Timeslot `A限` on the selected date.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens the calendar date and selects Timeslot `A限`. | The normal lesson display is shown and no duplicate warning is present. | timeslot = A限; lesson_count = 1 |
**Severity:** minor
**Priority:** medium
