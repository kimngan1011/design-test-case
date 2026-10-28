# Test Cases: LT-108382 — Student Lesson Report with Classroom

## Suite: Attendance Confirmation and Update

### Student Lesson Report – Attendance – Authorized teacher updates Student A – Persists after reload

**Description:** AC 03.1 — State Transition / CRUD-readback — An authorized teacher changes Student A's attendance through the report workflow and reads the saved value after reload.

**Preconditions:**

- Teacher Taro is logged in to Salesforce with permission to update attendance from the Student Lesson Report.
- Student A has Lesson Tokyo 01 in the current academic year.
- Student Session SS-A01 has Attendance Status Present and no Absent Reason before the update.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Teacher Taro opens Student A's Student Lesson Report. | The report shows Student A's Lesson Tokyo 01 row and the available attendance-update control. | Student Session = SS-A01; Initial status = Present |
| 2 | Teacher Taro changes Student A's Attendance Status to Absent and enters Absent Reason `Medical appointment`. | The attendance-update control accepts the specified values. | New status = Absent; Absent Reason = Medical appointment |
| 3 | Teacher Taro saves the attendance update. | Salesforce confirms the save without creating an additional Student Session. | Student Session = SS-A01 |
| 4 | Teacher Taro reloads Student A's Student Lesson Report. | The Lesson Tokyo 01 row shows Attendance Status Absent and Absent Reason Medical appointment. | Expected persisted values = Absent / Medical appointment |

**Severity:** critical
**Priority:** high

---

### Student Lesson Report – Attendance – User without edit permission – Keeps attendance unchanged

**Description:** AC 03.1 — Permission Matrix / Negative — A user without attendance-edit permission cannot change Student A's stored attendance.

**Preconditions:**

- User C is logged in to Salesforce without attendance-edit permission.
- Student A has Lesson Tokyo 01 in the current academic year.
- Student Session SS-A01 has Attendance Status Present and no Absent Reason.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | User C opens Student A's Student Lesson Report. | The report shows the existing attendance values without granting an editable attendance control. | Student Session = SS-A01; Status = Present |
| 2 | User C attempts to change Student A's Attendance Status to Absent. | Salesforce blocks the change or does not offer a way to save it. | Attempted status = Absent |
| 3 | User C reloads the report. | The Lesson Tokyo 01 row still shows Attendance Status Present with no Absent Reason. | Expected unchanged values = Present / blank |

**Severity:** major
**Priority:** high

---

### Student Lesson Report – Attendance – Update Student A – Leaves Student B unchanged

**Description:** AC 03.1 — CRUD-readback / Regression — Updating one report row changes only the selected Student Session.

**Preconditions:**

- Teacher Taro is logged in to Salesforce with permission to update attendance from the Student Lesson Report.
- Student A and Student B each have a current-academic-year session in Lesson Tokyo 01.
- Student Session SS-A01 has Attendance Status Present.
- Student Session SS-B01 has Attendance Status Late and Absent Reason blank.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Teacher Taro opens the Student Lesson Report containing Student A and Student B rows. | The report shows both students with their prepared attendance values. | Student A = Present; Student B = Late |
| 2 | Teacher Taro changes Student A's Attendance Status to Absent and saves the update. | Salesforce saves the update for Student Session SS-A01. | SS-A01 → Absent |
| 3 | Teacher Taro reloads the report and reads Student B's row. | Student B remains Late with an empty Absent Reason. | SS-B01 = Late / blank |

**Severity:** major
**Priority:** high

---

### Student Lesson Report – Attendance – Save retry – Retains one intended attendance value

**Description:** AC 03.1 — Data Integrity / Regression — Retrying the same attendance save leaves one final intended value for the selected Student Session.

**Preconditions:**

- Teacher Taro is logged in to Salesforce with permission to update attendance from the Student Lesson Report.
- Student A has Lesson Tokyo 01 in the current academic year.
- Student Session SS-A01 has Attendance Status Present and no Absent Reason.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Teacher Taro opens Student A's Student Lesson Report and changes SS-A01 to Absent with Absent Reason `Medical appointment`. | The report shows the pending attendance values for Student A. | SS-A01 → Absent / Medical appointment |
| 2 | Teacher Taro saves the attendance update and repeats the same save after the first save response. | Salesforce retains one intended attendance value for SS-A01 and does not create a second Student Session. | Retry payload = Absent / Medical appointment |
| 3 | Teacher Taro reloads the report and opens SS-A01. | Both the report row and SS-A01 detail show Attendance Status Absent and Absent Reason Medical appointment. | Expected final values = Absent / Medical appointment |

**Severity:** major
**Priority:** high
