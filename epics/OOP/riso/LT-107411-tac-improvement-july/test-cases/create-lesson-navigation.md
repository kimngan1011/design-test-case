# Test Cases: LT-107411 — Create Lesson Navigation

## Suite: [Riso] TAC — Create Lesson Navigation

### [Riso] TAC – Create Lesson – Valid data – Created Schedule detail opened
**Description:** AC 07 — State Transition — Successful creation opens the created Lesson Schedule detail.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- Course `Mathematics` and an available teacher are selected.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff creates a lesson with valid data. | The created Lesson Schedule detail opens and identifies the created schedule. | course = Mathematics; date = 2026-07-01 |
**Severity:** major
**Priority:** high

### [Riso] TAC – Create Lesson – Cancelled form – Calendar remains current
**Description:** AC 07 — Negative — Cancelling creation does not redirect to a new detail page.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- The lesson creation form is open from TAC.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff cancels lesson creation. | The current Calendar remains open and no new Lesson Schedule detail is opened. | action = cancel |
**Severity:** minor
**Priority:** medium

### [Riso] TAC – Create Lesson – Invalid data – Error flow retained
**Description:** AC 07 — Negative — Failed creation does not redirect to a Schedule detail.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- The lesson creation form has no Course selected.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff submits the lesson creation form. | The validation error is shown and no Lesson Schedule detail is opened. | course = empty |
**Severity:** minor
**Priority:** medium
