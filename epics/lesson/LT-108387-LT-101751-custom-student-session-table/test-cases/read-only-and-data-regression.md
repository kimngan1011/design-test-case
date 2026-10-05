# Test Cases: LT-108387 + LT-101751 — Read-only and Data Regression

## Suite: Read-only and Data Regression

### Student Session Table – Table Cell – Direct interaction – Inline editing unavailable

**Description:** User clarification — Negative UI interaction — The table is read-only and does not expose inline editing controls.

**Preconditions:**

- HQ or CM Staff is logged in to the Renseikai Salesforce tenant.
- The Renseikai **Enable Customizable Table Columns** setting is `ON`.
- The Renseikai layout includes Student Name and Attendance Status.
- A published lesson contains Student A with Attendance Status `Absent`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the published lesson in Salesforce Lesson Detail. | Salesforce Lesson Detail opens with Student A's row. | tenant = Renseikai; setting = ON; Student A Attendance Status = Absent |
| 2 | HQ or CM Staff selects Student A's Attendance Status cell. | The cell displays `Absent` without an inline input, selector, or save control. | target cell = Student A / Attendance Status |
| 3 | HQ or CM Staff attempts to change the Attendance Status value directly in the table. | The table value remains `Absent` and no Student Session update is initiated. | attempted inline value = Attend |

**Severity:** major
**Priority:** high

---

### Student Session Table – Separate Edit Function – Saved attendance update – Table reads current value

**Description:** User clarification — Regression and Readback — The separate Edit function remains the supported update path and the table reads the saved value.

**Preconditions:**

- HQ or CM Staff is logged in to the Renseikai Salesforce tenant.
- The Renseikai **Enable Customizable Table Columns** setting is `ON`.
- The Renseikai layout includes Student Name and Attendance Status.
- A published lesson contains Student A with Attendance Status `Absent`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the separate Edit function for Student A. | The separate Edit function opens with Attendance Status `Absent`. | tenant = Renseikai; setting = ON; initial Attendance Status = Absent |
| 2 | HQ or CM Staff changes Attendance Status to `Attend` in the separate Edit function and saves. | The separate Edit function saves Attendance Status `Attend`. | new Attendance Status = Attend |
| 3 | HQ or CM Staff returns to and refreshes Salesforce Lesson Detail. | Student A's table row displays Attendance Status `Attend`. | expected table value = Attend |

**Severity:** major
**Priority:** high

---

### Student Session Table – Column Configuration – Refresh after save – Separate Edit values retained

**Description:** Core configuration — Regression — Refreshing a saved configuration never changes values maintained by the separate Edit function.

**Preconditions:**

- System Administrator is logged in to the Renseikai Salesforce tenant.
- The Renseikai **Enable Customizable Table Columns** setting is `ON`.
- A published lesson contains Student A with Attendance Status `Absent` and Attendance Reason `Family event`.
- The Renseikai layout includes Student Name, Attendance Status, and Attendance Reason.
- A different HQ or CM Staff user can access the Renseikai Salesforce tenant without the System Administrator role.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | System Administrator opens the Student Session column configuration and saves the order Attendance Reason, Student Name, Attendance Status. | The new Renseikai header order is saved. | tenant = Renseikai; setting = ON; saved order = Attendance Reason → Student Name → Attendance Status |
| 2 | System Administrator refreshes Salesforce Lesson Detail. | The table headers follow Attendance Reason, Student Name, Attendance Status and Student A still displays `Family event` and `Absent`. | expected values = Attendance Reason: Family event; Attendance Status: Absent |
| 3 | A different HQ or CM Staff user opens and refreshes the same published lesson in Salesforce Lesson Detail. | The table headers follow Attendance Reason, Student Name, Attendance Status. | role = non-System Administrator; expected header order = Attendance Reason → Student Name → Attendance Status |
| 4 | System Administrator opens the separate Edit function for Student A. | The separate Edit function still shows Attendance Reason `Family event` and Attendance Status `Absent`. | expected edit values = Attendance Reason: Family event; Attendance Status: Absent |

**Severity:** major
**Priority:** high

---

### Student Session Table – Separate Edit Function – Custom layout saved – Staff value update persists

**Description:** User request — Regression and Readback — After a System Administrator saves a custom Renseikai layout, a different HQ or CM Staff user updates a Student Session value through the separate Edit function.

**Preconditions:**

- System Administrator is logged in to the Renseikai Salesforce tenant.
- The Renseikai **Enable Customizable Table Columns** setting is `ON`.
- A different HQ or CM Staff user can access the Renseikai Salesforce tenant without the System Administrator role.
- A published lesson contains Student A with Grade `7` and Attendance Status `Absent`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | System Administrator selects Student Name, Grade, and Attendance Status in the Student Session column configuration and saves. | The Renseikai saved layout contains exactly Student Name, Grade, and Attendance Status. | tenant = Renseikai; selected fields = Student Name, Grade, Attendance Status |
| 2 | A different HQ or CM Staff user opens and refreshes the published lesson in Salesforce Lesson Detail. | The Student Session table shows exactly Student Name, Grade, and Attendance Status. | role = non-System Administrator; expected headers = Student Name, Grade, Attendance Status |
| 3 | A different HQ or CM Staff user opens the separate Edit function for Student A. | The separate Edit function opens with Attendance Status `Absent`. | initial Attendance Status = Absent |
| 4 | A different HQ or CM Staff user changes Attendance Status to `Attend` in the separate Edit function and saves. | The separate Edit function saves Attendance Status `Attend`. | new Attendance Status = Attend |
| 5 | A different HQ or CM Staff user returns to and refreshes Salesforce Lesson Detail. | The Student Session table keeps exactly Student Name, Grade, and Attendance Status, and Student A displays Attendance Status `Attend`. | expected headers = Student Name, Grade, Attendance Status; expected Attendance Status = Attend |

**Severity:** major
**Priority:** high
