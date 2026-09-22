# Test Cases: LT-107411 — Student Lesson Label

## Suite: [Riso] TAC — Student Lesson Label

### [Riso] TAC – Student Lesson Label – Subject and teacher populated – Subject shown first
**Description:** AC 03 — Component — The student lesson chip uses Subject Name (Teacher Name).
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- A lesson has Subject `中国` and Teacher `山田`.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens the calendar date containing the lesson. | The lesson chip shows `中国 (山田)` with Subject before Teacher. | subject = 中国; teacher = 山田 |
**Severity:** minor
**Priority:** medium

### [Riso] TAC – Student Lesson Label – Long populated values – Teacher remains identifiable
**Description:** AC 03 — Negative — Long Subject and Teacher values retain a usable chip label.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- A lesson has a long Subject Name and long Teacher Name.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens the calendar date containing the lesson. | The chip remains readable and does not overlap adjacent calendar content. | subject = International Mathematics; teacher = Yamada Taro |
**Severity:** minor
**Priority:** medium
