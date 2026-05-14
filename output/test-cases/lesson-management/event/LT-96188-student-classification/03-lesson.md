# Test Cases: LT-96188 — Add Student Classification to Event and Lesson Calendar

**Suite:** Student Classification – Lesson
**Coverage file:** output/test-coverages/LT-96188-student-classification-event-lesson-calendar.md
**ACs covered:** AC 02.4
**Precondition (all cases):** PBT-2485 (student_classification field on Contact Object) must be deployed in the Renseikai org before executing any test in this suite.

---

## Suite: Student Classification – Lesson

### [Renseikai] Add Student Filter (Lesson Detail) – Student Classification – Filter Presence – Filter appears below Type filter

**Description:** AC 02.4 — CRUD Testing — Confirms the Student Classification filter is present in the Add Student popup in Lesson Detail, positioned directly below the Type filter.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- A lesson exists in the Lesson Calendar that allows adding students
- The Add Student popup is accessible from the Lesson Detail view

| #   | Action                                                      | Expected Result                                                                           | Test Data |
| --- | ----------------------------------------------------------- | ----------------------------------------------------------------------------------------- | --------- |
| 1   | Navigate to the Lesson Detail page from the Lesson Calendar | Lesson Detail page opens                                                                  |           |
| 2   | Click "Add Student" to open the student search popup        | Add Student popup opens                                                                   |           |
| 3   | Observe the filter fields in the popup                      | Filter fields are visible                                                                 |           |
| 4   | Identify the position of the Student Classification filter  | The "Student Classification" multi-select filter appears directly below the "Type" filter |           |

**Severity:** major
**Priority:** high

---

### [Renseikai] Add Student Filter (Lesson Detail) – Student Classification – Default State – All students returned when no classification selected

**Description:** AC 02.4 — Decision Table — Confirms that with no classification selected in the Add Student filter, all students of all classification types are returned.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- Students of all classification types exist: 在籍生, 元在籍生, 問合生, 季節講習生, and at least one with null
- Add Student popup is open from Lesson Detail

| #   | Action                                                          | Expected Result                                                                                        | Test Data |
| --- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | --------- |
| 1   | Open the Add Student popup from Lesson Detail                   | Popup opens with all filter fields empty                                                               |           |
| 2   | Confirm the Student Classification filter has no value selected | Student Classification filter is empty                                                                 |           |
| 3   | Click "Search"                                                  | Student list returns students of all classification types (在籍生, 元在籍生, 問合生, 季節講習生, null) |           |

**Severity:** minor
**Priority:** medium

---

### [Renseikai] Add Student Filter (Lesson Detail) – Student Classification – Single Value Selected – Only matching students returned

**Description:** AC 02.4 — Decision Table, Equivalence Partitioning — Confirms that selecting one classification value returns only students with that classification.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- Students with "季節講習生" and with "在籍生" exist
- Add Student popup is open from Lesson Detail

| #   | Action                                                   | Expected Result                                                                                                                | Test Data    |
| --- | -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------------ |
| 1   | Open the Add Student popup from Lesson Detail            | Popup opens                                                                                                                    |              |
| 2   | Select "季節講習生" in the Student Classification filter | "季節講習生" is selected                                                                                                       | "季節講習生" |
| 3   | Click "Search"                                           | Student list shows only students with Student Classification = "季節講習生"; students with other classifications are not shown |              |

**Severity:** major
**Priority:** high

---

### [Renseikai] Add Student Filter (Lesson Detail) – Student Classification – Two Values Selected – OR logic returns students of both types

**Description:** AC 02.4 — Decision Table — Confirms that selecting two classification values in the Add Student filter returns students matching either value (OR logic).

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- Students with "在籍生", "季節講習生", and "問合生" exist
- Add Student popup is open from Lesson Detail

| #   | Action                                               | Expected Result                                                                                                                 | Test Data    |
| --- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------ |
| 1   | Open the Add Student popup from Lesson Detail        | Popup opens                                                                                                                     |              |
| 2   | Select "在籍生" in the Student Classification filter | "在籍生" is selected                                                                                                            | "在籍生"     |
| 3   | Also select "季節講習生" in the same filter          | Both "在籍生" and "季節講習生" are shown as selected                                                                            | "季節講習生" |
| 4   | Click "Search"                                       | Student list includes students with "在籍生" AND students with "季節講習生"; students with "問合生" or "元在籍生" are not shown |              |

**Severity:** major
**Priority:** high

---
