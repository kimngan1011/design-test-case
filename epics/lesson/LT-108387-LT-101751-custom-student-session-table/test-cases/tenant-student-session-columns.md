# Test Cases: LT-108387 + LT-101751 — Tenant Student Session Columns

## Suite: Tenant Student Session Columns

### [Renseikai] Student Session Table – Required and Excluded Fields – Saved layout – Requested columns rendered

**Description:** LT-108387 — Component and Negative — The Renseikai Salesforce table renders all six requested fields and excludes the four removed fields.

**Preconditions:**

- System Administrator has enabled **Enable Customizable Table Columns** for the Renseikai tenant.
- System Administrator has saved the Renseikai layout with Student Name, Grade, Attendance Response, Attendance Status, Attendance Reason, and Attendance Note.
- HQ or CM Staff is logged in to the Renseikai Salesforce tenant.
- A published lesson contains Student A with Grade `7`, Attendance Response `Absent (Family event)`, Attendance Status `Absent`, Attendance Reason `Family event`, and Attendance Note `Parent called at 08:15`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the published lesson in Salesforce Lesson Detail. | Salesforce Lesson Detail opens for the published lesson. | tenant = Renseikai; Enable Customizable Table Columns = ON |
| 2 | HQ or CM Staff opens the Student Session table. | The table header contains Student Name, Grade, Attendance Response, Attendance Status, Attendance Reason, and Attendance Note. | required headers = Student Name, Grade, Attendance Response, Attendance Status, Attendance Reason, Attendance Note |
| 3 | HQ or CM Staff reads Student A's row. | Student A's row shows `Student A`, `7`, `Absent (Family event)`, `Absent`, `Family event`, and `Parent called at 08:15` under the matching headers. | Student A values = configured precondition values |
| 4 | HQ or CM Staff inspects the remaining table headers. | Risk, Type, Attendance Notice, and Reallocate Flag are absent from the Renseikai table. | excluded headers = Risk, Type, Attendance Notice, Reallocate Flag |

**Severity:** major
**Priority:** high

---

### [EEA] Student Session Table – Required and Excluded Fields – Saved layout – Requested columns rendered

**Description:** LT-101751 — Component and Negative — The EEA Salesforce table renders all six requested fields and excludes Renseikai-only fields.

**Preconditions:**

- System Administrator has enabled **Enable Customizable Table Columns** for the EEA tenant.
- System Administrator has saved the EEA layout with Student Name, Grade, Type, Attendance Status, Attendance Reason, and Reallocate Flag.
- HQ or CM Staff is logged in to the EEA Salesforce tenant.
- A published lesson contains Student B with Grade `8`, Type `Regular`, Attendance Status `Absent`, Attendance Reason `Illness`, and Reallocate Flag `Yes`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the published lesson in Salesforce Lesson Detail. | Salesforce Lesson Detail opens for the published lesson. | tenant = EEA; Enable Customizable Table Columns = ON |
| 2 | HQ or CM Staff opens the Student Session table. | The table header contains Student Name, Grade, Type, Attendance Status, Attendance Reason, and Reallocate Flag. | required headers = Student Name, Grade, Type, Attendance Status, Attendance Reason, Reallocate Flag |
| 3 | HQ or CM Staff reads Student B's row. | Student B's row shows `Student B`, `8`, `Regular`, `Absent`, `Illness`, and `Yes` under the matching headers. | Student B values = configured precondition values |
| 4 | HQ or CM Staff inspects the remaining table headers. | Attendance Response, Attendance Note, Risk, and Attendance Notice are absent from the EEA table. | excluded headers = Attendance Response, Attendance Note, Risk, Attendance Notice |

**Severity:** major
**Priority:** high
