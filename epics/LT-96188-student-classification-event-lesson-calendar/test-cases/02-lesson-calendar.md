# Test Cases: LT-96188 — Add Student Classification to Event and Lesson Calendar

**Suite:** Student Classification – Lesson Calendar
**Coverage file:** output/test-coverages/LT-96188-student-classification-event-lesson-calendar.md
**ACs covered:** AC 01.2, AC 02.3
**Precondition (all cases):** PBT-2485 (student_classification field on Contact Object) must be deployed in the Renseikai org before executing any test in this suite.

---

## Suite: Student Classification – Lesson Calendar

### [Renseikai] Student Classification Column – Lesson Calendar Student Session List – Student with Classification Value – Column visible with correct value

**Description:** AC 01.2 — CRUD Testing — Confirms the Student Classification column is present in the Lesson Calendar Student Session list and displays the student's classification value.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- At least one student session is visible in the Lesson Calendar for a student whose Student Classification = "季節講習生" (seasonal)

| #   | Action                                                                                        | Expected Result                                      | Test Data |
| --- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------- | --------- |
| 1   | Navigate to the Lesson Calendar page in Salesforce                                            | Lesson Calendar page loads                           |           |
| 2   | Locate a date with a student session for a student with Student Classification = "季節講習生" | The student session entry is visible on the calendar |           |
| 3   | Open or expand the Student Session list for that entry                                        | Student Session list is displayed                    |           |
| 4   | Read the Student Classification column value for that student                                 | The cell shows "季節講習生"                          |           |

**Severity:** major
**Priority:** high

---

### [Renseikai] Student Classification Column – Lesson Calendar Student Session List – Student with Null Classification – Column displays blank

**Description:** AC 01.2 — Negative Testing — Confirms the Student Classification column shows a blank cell in the Lesson Calendar when a student's classification is null.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- At least one student session is visible in the Lesson Calendar for a student whose Student Classification is null

| #   | Action                                                                    | Expected Result                                            | Test Data |
| --- | ------------------------------------------------------------------------- | ---------------------------------------------------------- | --------- |
| 1   | Navigate to the Lesson Calendar page                                      | Lesson Calendar page loads                                 |           |
| 2   | Locate a student session for a student with no Student Classification set | The student session entry is visible                       |           |
| 3   | Open or expand the Student Session list                                   | Student Session list is displayed                          |           |
| 4   | Read the Student Classification column value for that student             | The cell is blank — no dash, no "N/A", no placeholder text |           |

**Severity:** minor
**Priority:** medium

---

### [Renseikai] Lesson Calendar Student List Filter – Student Classification – Filter Presence – Filter appears below Type filter in left panel

**Description:** AC 02.3 — CRUD Testing — Confirms the Student Classification filter is present in the Lesson Calendar Student List Filter (left panel) and is positioned directly below the Type filter.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- The Lesson Calendar page is accessible and has student sessions to display

| #   | Action                                                                                 | Expected Result                                                                                 | Test Data |
| --- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | --------- |
| 1   | Navigate to the Lesson Calendar page                                                   | Lesson Calendar page loads                                                                      |           |
| 2   | Open the Student List Filter panel on the left side                                    | Student List Filter panel opens with multiple filter fields                                     |           |
| 3   | Observe the filter fields in the panel                                                 | Filter fields are visible                                                                       |           |
| 4   | Identify the position of the Student Classification filter relative to the Type filter | The "Student Classification" multi-select filter field appears directly below the "Type" filter |           |

**Severity:** major
**Priority:** high

---

### [Renseikai] Lesson Calendar Student List Filter – Student Classification – Default State – All students shown when no classification selected

**Description:** AC 02.3 — Decision Table — Confirms that when no Student Classification value is selected, student sessions for all classification types remain visible.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- Lesson Calendar has visible sessions for students with all classification types: 在籍生, 元在籍生, 問合生, 季節講習生, and null
- Student List Filter panel is open with no classification selected

| #   | Action                                                          | Expected Result                                                                                               | Test Data |
| --- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | Open the Lesson Calendar page                                   | Lesson Calendar loads showing student sessions                                                                |           |
| 2   | Open the Student List Filter panel                              | Filter panel opens                                                                                            |           |
| 3   | Confirm the Student Classification filter has no value selected | Student Classification filter is empty                                                                        |           |
| 4   | Apply the filter (or confirm the default view)                  | Student sessions for all classification types (在籍生, 元在籍生, 問合生, 季節講習生, and null) remain visible |           |

**Severity:** minor
**Priority:** medium

---

### [Renseikai] Lesson Calendar Student List Filter – Student Classification – Single Value Selected – Only matching students shown

**Description:** AC 02.3 — Decision Table, Equivalence Partitioning — Confirms that selecting one classification value hides sessions for all other classification types.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- Lesson Calendar has visible sessions for students with "在籍生" and "問合生"
- Student List Filter panel is open

| #   | Action                                                    | Expected Result                                                                                                                                                                         | Test Data |
| --- | --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | Open the Student List Filter panel in the Lesson Calendar | Filter panel opens                                                                                                                                                                      |           |
| 2   | Select "在籍生" in the Student Classification filter      | "在籍生" is selected in the filter                                                                                                                                                      | "在籍生"  |
| 3   | Apply the filter                                          | The calendar and student list show only sessions for students with Student Classification = "在籍生"; sessions for students with "問合生", "元在籍生", "季節講習生", or null are hidden |           |

**Severity:** major
**Priority:** high

---

### [Renseikai] Lesson Calendar Student List Filter – Student Classification – Two Values Selected – OR logic returns students of both types

**Description:** AC 02.3 — Decision Table — Confirms that selecting two classification values shows sessions for students matching either value (OR logic).

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- Lesson Calendar has visible sessions for students with "在籍生", "問合生", and "元在籍生"
- Student List Filter panel is open

| #   | Action                                                    | Expected Result                                                                                                                                             | Test Data |
| --- | --------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | Open the Student List Filter panel in the Lesson Calendar | Filter panel opens                                                                                                                                          |           |
| 2   | Select "在籍生" in the Student Classification filter      | "在籍生" is selected                                                                                                                                        | "在籍生"  |
| 3   | Also select "問合生" in the same filter                   | Both "在籍生" and "問合生" are shown as selected                                                                                                            | "問合生"  |
| 4   | Apply the filter                                          | The calendar shows sessions for students with "在籍生" AND sessions for students with "問合生"; sessions for "元在籍生" or "季節講習生" students are hidden |           |

**Severity:** major
**Priority:** high

---
