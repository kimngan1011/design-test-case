# Test Cases: LT-108378 — Show Attendance Remark in Lesson Report (BO)

## Suite: Lesson Report Detail

### Lesson Report Detail – Report Tab Student List – Salesforce Attendance Note – Saved note shown beside Attendance Status

**Description:** AC 01.2 — CRUD/readback; Component; Regression — A Salesforce Student Session Attendance Note is shown as Attendance Remark beside the same student's saved Attendance Status in the Back Office Lesson Report Detail Report tab.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce and Back Office.
- A published lesson named `LT-108378 Lesson B` includes Student B and has a Student Session.
- Student B's Student Session is visible in the Lesson Report Detail Report tab Student List.
- Student B's Attendance Status is `Attend` and Attendance Note is blank before this test.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Student B's Student Session for `LT-108378 Lesson B` in Salesforce. | Student B's Student Session opens and shows the current Attendance Status and Attendance Note. | Lesson=`LT-108378 Lesson B`; Student=`Student B`; initial status=`Attend`; initial note=blank |
| 2 | HQ or CM Staff sets Attendance Status to `Absent`, enters `school events` in Attendance Note, and saves the Student Session. | Salesforce saves Attendance Status=`Absent` and Attendance Note=`school events` for Student B. | Attendance Status=`Absent`; Attendance Note=`school events` |
| 3 | HQ or CM Staff opens `LT-108378 Lesson B` in Back Office through Lesson Report, opens Lesson Report Detail, and selects the Report tab. | The Report tab displays the Student List containing Student B. | BO route=`Lesson > Lesson Report > Lesson Report Detail > Report` |
| 4 | HQ or CM Staff reads Student B's Attendance Status in the Student List. | Student B's Attendance Status displays exactly `Absent (school events)`. | Expected display=`Absent (school events)` |
| 5 | HQ or CM Staff refreshes the Report tab and reads Student B's Attendance Status again. | Student B's Attendance Status still displays exactly `Absent (school events)`; no value is changed by viewing the report. | Expected display after refresh=`Absent (school events)` |

**Severity:** major
**Priority:** high

---
