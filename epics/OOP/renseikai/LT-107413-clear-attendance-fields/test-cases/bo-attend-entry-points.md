# Test Cases: LT-107413 — Clear Attendance Notice and Attendance Reason in Salesforce

## Suite: [Renseikai] Back Office Attend Entry Points

### [Renseikai] Collect Attendance – Lesson – Student selected – Attend clears absence fields

**Description:** AC 03 — Decision Table — The Lesson Collect Attendance form changes one student to Attend and clears the dependent absence fields.

**Preconditions:**

- Logged in as HQ Staff to Back Office.
- Published Lesson `RSK-BO-001` contains Student `Student I` with Attendance Status `Absent`, Attendance Reason `Traffic Issue`, and Attendance Notice `No Contact`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Lesson `RSK-BO-001` and select Collect Attendance. | The form shows Student I with Status `Absent`, Reason `Traffic Issue`, and Notice `No Contact`. | Lesson = RSK-BO-001; Student = Student I |
| 2 | Open Student I's Attendance Status control. | `Attend` is available as a selectable Attendance Status value. | Current Status = Absent |
| 3 | Select `Attend` for Student I. | Student I displays Status `Attend`; Attendance Reason and Attendance Notice each display a blank selection. | Status: Absent → Attend |

**Severity:** major
**Priority:** high

---

### [Renseikai] Collect Attendance – Report – Student selected – Attend clears absence fields

**Description:** AC 03 — Decision Table — The Report Collect Attendance form changes one student to Attend and clears the dependent absence fields.

**Preconditions:**

- Logged in as HQ Staff to Back Office.
- Published Lesson `RSK-BO-002` has an accessible Lesson Report and contains Student `Student J` with Attendance Status `Late`, Attendance Reason `School Event`, and Attendance Notice `On The Day`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open the report for Lesson `RSK-BO-002` and select Collect Attendance. | The form shows Student J with Status `Late`, Reason `School Event`, and Notice `On The Day`. | Lesson = RSK-BO-002; Student = Student J |
| 2 | Open Student J's Attendance Status control. | `Attend` is available as a selectable Attendance Status value. | Current Status = Late |
| 3 | Select `Attend` for Student J. | Student J displays Status `Attend`; Attendance Reason and Attendance Notice each display a blank selection. | Status: Late → Attend |

**Severity:** major
**Priority:** high

---

### [Renseikai] Bulk Collect Attendance – Calendar BO – Two selected students – Attend clears absence fields

**Description:** AC 03 — Decision Table — Bulk Collect Attendance applies Attend and clears dependent absence fields for every selected student.

**Preconditions:**

- Logged in as HQ Staff to Back Office.
- Calendar shows Published Lesson `RSK-BO-003` with Student `Student K` at `Absent`, Reason `Traffic Issue`, Notice `No Contact`; and Student `Student L` at `Leave Early`, Reason `Family Reason`, Notice `In Advance`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open the Calendar BO bulk attendance action for Lesson `RSK-BO-003`. | The form shows Student K with `Absent` / `Traffic Issue` / `No Contact` and Student L with `Leave Early` / `Family Reason` / `In Advance`. | Lesson = RSK-BO-003 |
| 2 | Select Student K and Student L. | Both students are marked as selected in the bulk form. | Selected Students = K, L |
| 3 | Select `Attend` as the bulk Attendance Status. | The bulk Attendance Status control displays `Attend`. | Bulk Status = Attend |
| 4 | Review the selected rows. | Student K and Student L each display `Attend` as the pending Attendance Status; Attendance Reason and Attendance Notice are blank for both rows. | K: Absent → Attend; L: Leave Early → Attend |

**Severity:** major
**Priority:** high

---

### [Renseikai] Bulk Collect Attendance – Calendar BO – Unselected student – Existing status retained

**Description:** AC 03 — Negative Testing — Bulk selection does not stage Attend for a student outside the selected set.

**Preconditions:**

- Logged in as HQ Staff to Back Office.
- Calendar shows Published Lesson `RSK-BO-004` with Student `Student M` at `Absent` and Student `Student N` at `Late`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open the Calendar BO bulk attendance action for Lesson `RSK-BO-004`. | The bulk attendance form shows Student M and Student N as selectable rows. | Lesson = RSK-BO-004 |
| 2 | Select Student M only and select `Attend` as the bulk Attendance Status. | Student M displays `Attend` as the pending value; Student N is not selected. | Selected Student = M; Bulk Status = Attend |
| 3 | Review Student N's row. | Student N continues to display `Late`; no pending `Attend` value is shown for Student N. | Unselected Student = N; Status = Late |

**Severity:** major
**Priority:** high
