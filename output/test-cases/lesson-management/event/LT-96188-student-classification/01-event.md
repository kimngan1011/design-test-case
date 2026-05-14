# Test Cases: LT-96188 — Add Student Classification to Event and Lesson Calendar

**Suite:** Student Classification – Event
**Coverage file:** output/test-coverages/LT-96188-student-classification-event-lesson-calendar.md
**ACs covered:** AC 01.1, AC 02.1, AC 02.2, AC 03.1, AC 03.2
**Precondition (all cases):** PBT-2485 (student_classification field on Contact Object) must be deployed in the Renseikai org before executing any test in this suite.

---

## Suite: Student Classification – Event

### [Renseikai] Student Classification Column – Event Participant List – Student with Classification Value – Column visible with correct value

**Description:** AC 01.1 — CRUD Testing — Confirms the Student Classification column is present in the Event Participant List and displays the student's classification value when set.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- An Event Master exists with at least one registered participant whose Student Classification = "在籍生" (enrolled)

| #   | Action                                                            | Expected Result                         | Test Data |
| --- | ----------------------------------------------------------------- | --------------------------------------- | --------- |
| 1   | Navigate to the Event Master list view                            | Event Master list view loads            |           |
| 2   | Click on the Event Master to open its detail page                 | Event Master detail page opens          |           |
| 3   | Scroll to the Participant List section                            | Participant List table is visible       |           |
| 4   | Locate the participant with Student Classification = "在籍生"     | The row for that participant is visible |           |
| 5   | Read the Student Classification column value for that participant | The cell shows "在籍生"                 |           |

**Severity:** major
**Priority:** high

---

### [Renseikai] Student Classification Column – Event Participant List – Student with Null Classification – Column displays blank

**Description:** AC 01.1 — Equivalence Partitioning — Confirms the Student Classification column shows a blank cell (not a dash or placeholder) when a participant has no classification set.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- An Event Master exists with at least one registered participant whose Student Classification is null (not set)

| #   | Action                                                         | Expected Result                                            | Test Data |
| --- | -------------------------------------------------------------- | ---------------------------------------------------------- | --------- |
| 1   | Navigate to the Event Master list view                         | Event Master list view loads                               |           |
| 2   | Open the Event Master with the null-classification participant | Event Master detail page opens                             |           |
| 3   | Scroll to the Participant List section                         | Participant List table is visible                          |           |
| 4   | Locate the participant with no Student Classification set      | The row for that participant is visible                    |           |
| 5   | Read the Student Classification column value                   | The cell is blank — no dash, no "N/A", no placeholder text |           |

**Severity:** minor
**Priority:** medium

---

### [Renseikai] Student Classification Column – Activity Event Participant List – Student with Classification Value – Column visible with correct value

**Description:** AC 01.1 — Regression Analysis — Confirms the Student Classification column also appears in the Participant List when accessed from an Activity Event, not only from Event Master.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- An Activity Event (child event under an Event Master) exists with at least one participant whose Student Classification = "問合生" (inquiry)

| #   | Action                                                               | Expected Result                     | Test Data |
| --- | -------------------------------------------------------------------- | ----------------------------------- | --------- |
| 1   | Navigate to the parent Event Master and open a linked Activity Event | Activity Event detail page opens    |           |
| 2   | Scroll to the Participant List section                               | Participant List table is visible   |           |
| 3   | Locate the participant with Student Classification = "問合生"        | Row for that participant is visible |           |
| 4   | Read the Student Classification column value                         | The cell shows "問合生"             |           |

**Severity:** major
**Priority:** high

---

### [Renseikai] Add Master Participant Filter – Student Classification – Filter Presence – Filter appears below Type filter

**Description:** AC 02.1 — CRUD Testing — Confirms the Student Classification filter is visible in the Add Master Participant popup and is positioned directly below the Type filter.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- An Event Master exists

| #   | Action                                                                                 | Expected Result                                                                           | Test Data |
| --- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | --------- |
| 1   | Navigate to the Event Master detail page                                               | Event Master detail page opens                                                            |           |
| 2   | Click the "Add Master Participant" button                                              | Add Master Participant popup opens                                                        |           |
| 3   | Observe the filter fields in the popup                                                 | Filter section is visible                                                                 |           |
| 4   | Identify the position of the Student Classification filter relative to the Type filter | The "Student Classification" multi-select filter appears directly below the "Type" filter |           |

**Severity:** major
**Priority:** high

---

### [Renseikai] Add Master Participant Filter – Student Classification – Default State – All students returned when no classification selected

**Description:** AC 02.1 — Decision Table — Confirms that when the Student Classification filter has no value selected, all students regardless of classification are returned.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- Students with each classification value exist: 在籍生, 元在籍生, 問合生, 季節講習生, and at least one with null
- Add Master Participant popup is open

| #   | Action                                                            | Expected Result                                                                                                            | Test Data |
| --- | ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | Open the Add Master Participant popup                             | Popup opens with all filter fields empty                                                                                   |           |
| 2   | Confirm the Student Classification filter shows no selected value | Student Classification filter is empty                                                                                     |           |
| 3   | Click "Search" without selecting any classification               | Student list returns and includes students with all classification values (在籍生, 元在籍生, 問合生, 季節講習生, and null) |           |

**Severity:** minor
**Priority:** medium

---

### [Renseikai] Add Master Participant Filter – Student Classification – Single Value Selected – Only matching students returned

**Description:** AC 02.1 — Decision Table, Equivalence Partitioning — Confirms that selecting a single classification value returns only students with that classification.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- At least 2 students with Student Classification = "在籍生" exist
- Students with other classifications (元在籍生, 問合生, 季節講習生) also exist
- Add Master Participant popup is open

| #   | Action                                           | Expected Result                                                                                                              | Test Data |
| --- | ------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | Open the Add Master Participant popup            | Popup opens                                                                                                                  |           |
| 2   | Click the Student Classification filter dropdown | Dropdown opens showing picklist values                                                                                       |           |
| 3   | Select "在籍生" from the dropdown                | "在籍生" is selected and shown in the filter                                                                                 | "在籍生"  |
| 4   | Click "Search"                                   | Student list returns only students with Student Classification = "在籍生"; students with other classifications are not shown |           |

**Severity:** major
**Priority:** high

---

### [Renseikai] Add Master Participant Filter – Student Classification – Two Values Selected – OR logic returns students of both types

**Description:** AC 02.1 — Decision Table — Confirms that selecting two classification values returns students matching either value (OR logic), not only students matching both simultaneously.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- At least 2 students with "在籍生", at least 2 with "問合生", and at least 2 with "元在籍生" exist
- Add Master Participant popup is open

| #   | Action                                               | Expected Result                                                                                                                    | Test Data |
| --- | ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | Open the Add Master Participant popup                | Popup opens                                                                                                                        |           |
| 2   | Select "在籍生" in the Student Classification filter | "在籍生" is selected                                                                                                               | "在籍生"  |
| 3   | Also select "問合生" in the same filter              | Both "在籍生" and "問合生" are shown as selected                                                                                   | "問合生"  |
| 4   | Click "Search"                                       | Student list contains students with "在籍生" AND students with "問合生"; students with "元在籍生" or "季節講習生" are not included |           |

**Severity:** major
**Priority:** high

---

### [Renseikai] Add Master Participant Filter – Student Classification – Picklist Dropdown – All defined values shown, no extras

**Description:** AC 02.1 — Equivalence Partitioning — Confirms the filter dropdown shows exactly the values defined in the Student Classification picklist field and no additional or hardcoded values appear.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- The Student Classification picklist (from PBT-2485) has exactly 4 values: 在籍生, 元在籍生, 問合生, 季節講習生
- Add Master Participant popup is open

| #   | Action                                                       | Expected Result                                                                          | Test Data |
| --- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------- | --------- |
| 1   | Open the Add Master Participant popup                        | Popup opens                                                                              |           |
| 2   | Click the Student Classification filter to open its dropdown | Dropdown opens and lists all available values                                            |           |
| 3   | Count and read all values in the dropdown                    | Exactly 4 values are shown: 在籍生, 元在籍生, 問合生, 季節講習生; no other values appear |           |

**Severity:** minor
**Priority:** medium

---

### [Renseikai] Assign to Event Filter (from Event Master) – Student Classification – Filter Presence – Filter appears below Type filter

**Description:** AC 02.2 — CRUD Testing — Confirms the Student Classification filter is visible in the Assign to Event popup when opened from Event Master, positioned directly below the Type filter.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- An Event Master exists

| #   | Action                                                                                 | Expected Result                                                                           | Test Data |
| --- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | --------- |
| 1   | Navigate to the Event Master detail page                                               | Event Master detail page opens                                                            |           |
| 2   | Click "Assign to Event" to open the popup                                              | Assign to Event popup opens                                                               |           |
| 3   | Observe the filter fields in the popup                                                 | Filter section is visible                                                                 |           |
| 4   | Identify the position of the Student Classification filter relative to the Type filter | The "Student Classification" multi-select filter appears directly below the "Type" filter |           |

**Severity:** major
**Priority:** high

---

### [Renseikai] Assign to Event Filter (from Event Master) – Student Classification – Single Value Selected – Only matching students returned

**Description:** AC 02.2 — Decision Table — Confirms that selecting a single classification value in the Event Master Assign to Event popup returns only students with that classification.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- Students with "季節講習生" and with "在籍生" exist
- Assign to Event popup is open from the Event Master detail page

| #   | Action                                                           | Expected Result                                                                                                                | Test Data    |
| --- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------------ |
| 1   | Open the Assign to Event popup from the Event Master detail page | Popup opens with filter fields empty                                                                                           |              |
| 2   | Select "季節講習生" in the Student Classification filter         | "季節講習生" is selected                                                                                                       | "季節講習生" |
| 3   | Click "Search"                                                   | Student list shows only students with Student Classification = "季節講習生"; students with other classifications are not shown |              |

**Severity:** major
**Priority:** high

---

### [Renseikai] Assign to Event Filter (from Activity Event) – Student Classification – Filter Presence – Filter appears below Type filter

**Description:** AC 02.2 — CRUD Testing — Confirms the Student Classification filter is also visible in the Assign to Event popup when opened from an Activity Event, positioned below the Type filter.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- An Activity Event (child event under an Event Master) exists

| #   | Action                                                            | Expected Result                                                                           | Test Data |
| --- | ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | --------- |
| 1   | Navigate to the Activity Event detail page                        | Activity Event detail page opens                                                          |           |
| 2   | Click "Assign to Event" to open the popup from the Activity Event | Assign to Event popup opens in the Activity Event context                                 |           |
| 3   | Observe the filter fields in the popup                            | Filter section is visible                                                                 |           |
| 4   | Identify the position of the Student Classification filter        | The "Student Classification" multi-select filter appears directly below the "Type" filter |           |

**Severity:** major
**Priority:** high

---

### [Renseikai] Assign to Event Filter (from Activity Event) – Student Classification – Single Value Selected – Only matching students returned

**Description:** AC 02.2 — Decision Table — Confirms filtering by a single classification in the Activity Event Assign to Event popup returns only matching students.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- Students with "元在籍生" and with "在籍生" exist
- Assign to Event popup is open from the Activity Event detail page

| #   | Action                                                             | Expected Result                                                                                                              | Test Data  |
| --- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- | ---------- |
| 1   | Open the Assign to Event popup from the Activity Event detail page | Popup opens in Activity Event context                                                                                        |            |
| 2   | Select "元在籍生" in the Student Classification filter             | "元在籍生" is selected                                                                                                       | "元在籍生" |
| 3   | Click "Search"                                                     | Student list shows only students with Student Classification = "元在籍生"; students with other classifications are not shown |            |

**Severity:** major
**Priority:** high

---

### [Renseikai] Assign to Event Filter (from Activity Event) – Student Classification – Two Values Selected – OR logic returns students of both types

**Description:** AC 02.2 — Decision Table — Confirms that selecting two classification values in the Assign to Event popup (Activity Event context) returns students of either type.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- Students with "在籍生", "問合生", and "元在籍生" exist
- Assign to Event popup is open from an Activity Event detail page

| #   | Action                                               | Expected Result                                                                                                                 | Test Data |
| --- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | Open the Assign to Event popup from Activity Event   | Popup opens                                                                                                                     |           |
| 2   | Select "在籍生" in the Student Classification filter | "在籍生" is selected                                                                                                            | "在籍生"  |
| 3   | Also select "問合生" in the same filter              | Both "在籍生" and "問合生" are shown as selected                                                                                | "問合生"  |
| 4   | Click "Search"                                       | Student list includes students with "在籍生" AND students with "問合生"; students with "元在籍生" or "季節講習生" are not shown |           |

**Severity:** major
**Priority:** high

---

### [Renseikai] Student Classification Column – Collect Event Attendance – Student with Classification Value – Column visible with correct value

**Description:** AC 03.1 [dev-missed] — CRUD Testing — Confirms the Student Classification column appears on the Collect Event Attendance page and shows the student's classification value. This behavior was missed during initial development and is expected to be added before release.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- An event has a Collect Event Attendance page with at least one participant whose Student Classification = "元在籍生" (former enrolled)

| #   | Action                                                           | Expected Result                                                 | Test Data |
| --- | ---------------------------------------------------------------- | --------------------------------------------------------------- | --------- |
| 1   | Navigate to the event and open the Collect Event Attendance page | Collect Event Attendance page loads with a list of participants |           |
| 2   | Locate the participant with Student Classification = "元在籍生"  | Row for that participant is visible in the attendance table     |           |
| 3   | Read the Student Classification column value                     | The cell shows "元在籍生"                                       |           |

**Severity:** minor
**Priority:** medium

---

### [Renseikai] Student Classification Column – Collect Event Attendance – Student with Null Classification – Column displays blank

**Description:** AC 03.1 [dev-missed] — Negative Testing — Confirms the Student Classification column shows blank in Collect Event Attendance when the student has no classification set.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- An event has a Collect Event Attendance page with at least one participant whose Student Classification is null

| #   | Action                                                      | Expected Result                       | Test Data |
| --- | ----------------------------------------------------------- | ------------------------------------- | --------- |
| 1   | Navigate to the Collect Event Attendance page for the event | Collect Event Attendance page loads   |           |
| 2   | Locate the participant with no Student Classification set   | Row for that participant is visible   |           |
| 3   | Read the Student Classification column value                | The cell is blank — no dash, no "N/A" |           |

**Severity:** minor
**Priority:** medium

---

### [Renseikai] Student Classification Column – CSV Download Participants – Column present in file with correct value and blank for null

**Description:** AC 03.2 [dev-missed] — CRUD Testing — Confirms the downloaded CSV file from the Event Participant List includes the Student Classification column, shows the correct value for participants with a classification, and shows a blank cell for null classification.

**Preconditions:**

- Logged in as HQ or CM Staff to the Salesforce org
- An Event Master exists with exactly 2 participants:
  - Participant A: Student Classification = "在籍生"
  - Participant B: Student Classification is null

| #   | Action                                                             | Expected Result                                            | Test Data |
| --- | ------------------------------------------------------------------ | ---------------------------------------------------------- | --------- |
| 1   | Navigate to the Event Master detail page                           | Event Master detail page opens                             |           |
| 2   | Scroll to the Participant List section                             | Participant List is visible                                |           |
| 3   | Click the "CSV Download" button                                    | A CSV file is downloaded                                   |           |
| 4   | Open the downloaded CSV file                                       | CSV file opens with column headers in the first row        |           |
| 5   | Locate the "Student Classification" column header                  | A column with the Student Classification header is present |           |
| 6   | Find the row for Participant A (Student Classification = "在籍生") | The Student Classification cell shows "在籍生"             |           |
| 7   | Find the row for Participant B (null classification)               | The Student Classification cell is blank                   |           |

**Severity:** minor
**Priority:** medium

---
