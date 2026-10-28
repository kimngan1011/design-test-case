# Test Cases: LT-108378 — Show Attendance Remark in Lesson Report (BO)

## Suite: Update LR

### Lesson Management – Report Tab Student List – Salesforce Attendance Note – Saved note shown beside Attendance Status

**Description:** AC 01.1 — CRUD/readback; Component; Regression — A Salesforce Student Session Attendance Note is shown as Attendance Remark beside the same student's saved Attendance Status in the Back Office Lesson Management Report tab.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce and Back Office.
- A published lesson named `LT-108378 Lesson A` includes Student A and has a Student Session.
- Student A's Student Session is visible in the Lesson Management lesson-detail Report tab Student List.
- Student A's Attendance Status is `Attend` and Attendance Note is blank before this test.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Student A's Student Session for `LT-108378 Lesson A` in Salesforce. | Student A's Student Session opens and shows the current Attendance Status and Attendance Note. | Lesson=`LT-108378 Lesson A`; Student=`Student A`; initial status=`Attend`; initial note=blank |
| 2 | HQ or CM Staff sets Attendance Status to `Absent`, enters `school events` in Attendance Note, and saves the Student Session. | Salesforce saves Attendance Status=`Absent` and Attendance Note=`school events` for Student A. | Attendance Status=`Absent`; Attendance Note=`school events` |
| 3 | HQ or CM Staff opens `LT-108378 Lesson A` in Back Office through Lesson Management, opens Lesson Detail, and selects the Report tab. | The Report tab displays the Student List containing Student A. | BO route=`Lesson > Lesson Management > Lesson Detail > Report` |
| 4 | HQ or CM Staff reads Student A's Attendance Status in the Student List. | Student A's Attendance Status displays exactly `Absent (school events)`. | Expected display=`Absent (school events)` |
| 5 | HQ or CM Staff refreshes the Report tab and reads Student A's Attendance Status again. | Student A's Attendance Status still displays exactly `Absent (school events)`; no value is changed by viewing the report. | Expected display after refresh=`Absent (school events)` |

**Severity:** major
**Priority:** high

---

### Lesson Management – Report Tab Student List – BO Attendance Remark – Updated note persists beside Attendance Status

**Description:** AC 01.3 — CRUD/readback; Component; Regression — Back Office saves a replacement Attendance Remark and displays it beside the unchanged Attendance Status after refresh.

**Preconditions:**
- HQ or CM Staff is logged in to Back Office.
- A published lesson named `LT-108378 Lesson C` includes Student C and has a Student Session.
- Student C's Attendance Status is `Absent` and Attendance Remark is `school events` before this test.
- Student C is visible in the Lesson Management lesson-detail Report tab Student List.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens `LT-108378 Lesson C` in Back Office through Lesson Management, opens Lesson Detail, and selects the Report tab. | The Report tab displays the Student List containing Student C with Attendance Status `Absent (school events)`. | BO route=`Lesson > Lesson Management > Lesson Detail > Report`; initial display=`Absent (school events)` |
| 2 | HQ or CM Staff opens the attendance edit form for Student C, replaces Attendance Remark with `medical appointment`, and saves the update. | Back Office saves Attendance Remark=`medical appointment` for Student C while Attendance Status remains `Absent`. | Attendance Remark=`medical appointment`; Attendance Status=`Absent` |
| 3 | HQ or CM Staff reads Student C's Attendance Status in the Student List. | Student C's Attendance Status displays exactly `Absent (medical appointment)`. | Expected display=`Absent (medical appointment)` |
| 4 | HQ or CM Staff refreshes the Report tab and reads Student C's Attendance Status again. | Student C's Attendance Status still displays exactly `Absent (medical appointment)`. | Expected display after refresh=`Absent (medical appointment)` |

**Severity:** major
**Priority:** high

---
