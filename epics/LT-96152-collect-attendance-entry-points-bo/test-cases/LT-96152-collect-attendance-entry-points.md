# Test Cases: LT-96152 — Collect Attendance Entry Points on Lesson Report BO

## Suite: Collect Attendance Entry Points

---

### Lesson Report BO – Report Tab – Published lesson – Collect Attendance popup opens

**Description:** AC 01.1 / AC 01.3 — Decision Table — Confirm the Lesson Detail -> Report tab exposes Collect Attendance and opens the existing popup for an attendance-eligible lesson.

**Preconditions:**

- Logged in to BO as a user who can already collect attendance
- A published lesson exists with at least one student session and an auto-created lesson report
- The same lesson can already open Collect Attendance from the existing BO flow

| #   | Action                                             | Expected Result                                                                         | Test Data                |
| --- | -------------------------------------------------- | --------------------------------------------------------------------------------------- | ------------------------ |
| 1   | Open the lesson on BO and switch to the Report tab | Report tab is displayed for the selected lesson                                         | Lesson Status: Published |
| 2   | Observe the action area on the Report tab          | Collect Attendance button is visible and enabled                                        |                          |
| 3   | Click Collect Attendance                           | The existing Collect Attendance popup opens                                             |                          |
| 4   | Observe the popup content                          | Student list and attendance fields match the current collect-attendance popup structure |                          |

**Severity:** major
**Priority:** high

---

### Lesson Report BO – Lesson Report Detail – Published lesson – Collect Attendance popup opens

**Description:** AC 01.2 / AC 01.3 — Decision Table — Confirm Lesson Report Detail exposes Collect Attendance and opens the existing popup for an attendance-eligible lesson.

**Preconditions:**

- Logged in to BO as a user who can already collect attendance
- A published lesson exists with at least one student session and an accessible Lesson Report Detail page

| #   | Action                                                        | Expected Result                                                                     | Test Data                |
| --- | ------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------ |
| 1   | Open Lesson Report Detail for a student in a published lesson | Lesson Report Detail is displayed                                                   | Lesson Status: Published |
| 2   | Observe the action area on Lesson Report Detail               | Collect Attendance button is visible and enabled                                    |                          |
| 3   | Click Collect Attendance                                      | The existing Collect Attendance popup opens                                         |                          |
| 4   | Observe the popup content                                     | Popup shows the same attendance fields and editable controls as the current BO flow |                          |

**Severity:** major
**Priority:** high

---

### Lesson Report BO – Report Tab – Draft lesson – Collect Attendance button disabled

**Description:** AC 01.4 — Negative Testing — Confirm the new Report tab entry point does not bypass the current Draft-state guard.

**Preconditions:**

- Logged in to BO as a user who can already collect attendance
- A draft lesson exists with a lesson report visible on the Report tab

| #   | Action                                                   | Expected Result                                        | Test Data            |
| --- | -------------------------------------------------------- | ------------------------------------------------------ | -------------------- |
| 1   | Open the draft lesson on BO and switch to the Report tab | Report tab is displayed                                | Lesson Status: Draft |
| 2   | Observe the Collect Attendance action                    | Collect Attendance button is visible but disabled      |                      |
| 3   | Attempt to click the disabled button                     | No popup opens and lesson attendance remains unchanged |                      |

**Severity:** major
**Priority:** high

---

### Lesson Report BO – Lesson Report Detail – Completed lesson – Collect Attendance button disabled

**Description:** AC 01.4 — Negative Testing — Confirm the new Lesson Report Detail entry point does not bypass the current Completed-state guard.

**Preconditions:**

- Logged in to BO as a user who can already collect attendance
- A completed lesson exists with an accessible Lesson Report Detail page

| #   | Action                                                        | Expected Result                                       | Test Data                |
| --- | ------------------------------------------------------------- | ----------------------------------------------------- | ------------------------ |
| 1   | Open Lesson Report Detail for a student in a completed lesson | Lesson Report Detail is displayed                     | Lesson Status: Completed |
| 2   | Observe the Collect Attendance action                         | Collect Attendance button is visible but disabled     |                          |
| 3   | Attempt to click the disabled button                          | No popup opens and saved attendance data is unchanged |                          |

**Severity:** major
**Priority:** high

---

### Lesson Report BO – Report Tab – Absent attendance saved – Student session and mobile updated

**Description:** AC 01.5 — Regression Analysis — Confirm saving attendance from Lesson Detail -> Report tab uses the same persistence and sync flow as the current collect-attendance path.

**Preconditions:**

- Logged in to BO as a user who can already collect attendance
- A published lesson exists with at least one student session and an auto-created lesson report
- Student A can log in to Mobile and view the lesson

| #   | Action                                                                        | Expected Result                                                             | Test Data                                                                      |
| --- | ----------------------------------------------------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| 1   | Open the lesson on BO, switch to the Report tab, and click Collect Attendance | Collect Attendance popup opens                                              | Lesson Status: Published                                                       |
| 2   | Set Attendance Status to Absent                                               | Absent-dependent fields become available                                    | Attendance Status: Absent                                                      |
| 3   | Select Attendance Reason, Attendance Notice, and enter Attendance Note        | Values are accepted in the popup                                            | Reason: Traffic Issue; Notice: No Contact; Note: Student absent due to traffic |
| 4   | Click Save                                                                    | Success message is shown and the popup closes                               |                                                                                |
| 5   | View the student row on BO lesson detail                                      | Student session shows Absent, Traffic Issue, No Contact, and the saved note |                                                                                |
| 6   | Open Mobile and view the same lesson                                          | Mobile shows the updated attendance status for the student                  |                                                                                |

**Severity:** critical
**Priority:** high

---

### Lesson Report BO – Lesson Report Detail – Late attendance saved – Lesson allocation and report detail updated

**Description:** AC 01.5 — Regression Analysis — Confirm saving attendance from Lesson Report Detail updates the same downstream records as the current collect-attendance path.

**Preconditions:**

- Logged in to BO as a user who can already collect attendance
- A published lesson exists with at least one student session, lesson allocation history, and an accessible Lesson Report Detail page

| #   | Action                                                                     | Expected Result                                                      | Test Data                                                                       |
| --- | -------------------------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| 1   | Open Lesson Report Detail and click Collect Attendance                     | Collect Attendance popup opens                                       | Lesson Status: Published                                                        |
| 2   | Set Attendance Status to Late                                              | Late-dependent fields become available                               | Attendance Status: Late                                                         |
| 3   | Select Attendance Reason and Attendance Notice, then enter Attendance Note | Values are accepted in the popup                                     | Reason: School Event; Notice: On The Day; Note: Arrived late after school event |
| 4   | Click Save                                                                 | Success message is shown and the popup closes                        |                                                                                 |
| 5   | Refresh Lesson Report Detail                                               | Lesson Report Detail shows the updated Late attendance information   |                                                                                 |
| 6   | Open the student's lesson allocation report history                        | Report history reflects the updated attendance values for the lesson |                                                                                 |

**Severity:** critical
**Priority:** high

---

### Lesson Report BO – Lesson Report Detail – Existing attendance record – Saved values prefilled on reopen

**Description:** AC 01.5 — Equivalence Partitioning — Confirm reopening Collect Attendance from the new surface preserves previously saved reason, notice, and note values.

**Preconditions:**

- Logged in to BO as a user who can already collect attendance
- A published lesson exists with attendance already saved for the selected student
- Saved attendance includes status, reason, notice, and note

| #   | Action                                                             | Expected Result                                                   | Test Data                                 |
| --- | ------------------------------------------------------------------ | ----------------------------------------------------------------- | ----------------------------------------- |
| 1   | Open Lesson Report Detail for the student with existing attendance | Lesson Report Detail is displayed                                 | Existing Attendance: Leave Early          |
| 2   | Click Collect Attendance                                           | Collect Attendance popup opens                                    |                                           |
| 3   | Observe the prefilled attendance values                            | Status, reason, notice, and note show the previously saved values | Reason: Family Reason; Notice: In Advance |
| 4   | Close and reopen the popup from the same page                      | The same saved values remain prefilled                            | Note: Left early due to family emergency  |

**Severity:** normal
**Priority:** medium
