# Test Cases: LT-107411 — Course & Timeslot Sidebar

## Suite: [Riso] TAC — Course & Timeslot Sidebar

### [Riso] TAC – Create Lesson – Course empty – Creation blocked
**Description:** AC 05 — Negative — Course is mandatory for lesson creation.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- A lesson date and available teacher are selected.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff leaves Course empty and selects Create Lesson. | Lesson creation is blocked and Course is identified as required. | course = empty |
**Severity:** major
**Priority:** high

### [Riso] TAC – Create Lesson – Course selected – Creation available
**Description:** AC 05 — Equivalence Partitioning — A selected Course satisfies the mandatory field.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- Course `Mathematics` is available.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects Course `Mathematics`. | The Course selector shows `Mathematics` and Create Lesson is available. | course = Mathematics |
**Severity:** major
**Priority:** high

### [Riso] TAC – Left Sidebar – Overflowing teacher list – Course remains fixed
**Description:** AC 05 — Component — Only the Available Teachers/Timeslot area scrolls.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- The selected Course has enough Available Teachers to overflow the list.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff scrolls the Available Teachers/Timeslot area. | The list scrolls while the Course label and selected Course remain visible. | course = Mathematics; list = overflowing |
**Severity:** minor
**Priority:** medium

### [Riso] TAC – Left Sidebar – Japanese locale – Date has no slash
**Description:** AC 05 — Component — Japanese date follows the PBT format.
**Preconditions:**
- HQ or CM Staff is logged in with Japanese locale.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens the sidebar for July 1. | The date shows `7月1日` and does not show `7月/1日`. | locale = ja; date = 2026-07-01 |
**Severity:** minor
**Priority:** medium
