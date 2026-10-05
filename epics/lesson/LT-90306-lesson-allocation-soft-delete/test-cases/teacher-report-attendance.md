# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 1841 — "Assign a teacher with only this lesson in lesson detail"](https://app.qase.io/project/PX?suite=1841) (10 existing cases). Cases 14254 (Submit report for student) and 14256 (Mark attendance for each student) exercise the same per-lesson student roster already covered by `Is_Archived__c = FALSE` filtering elsewhere in the codebase (`LessonReportHandler.cls:320,462,643` and the roster query verified for suite 219), but through the Teacher persona rather than HQ/CM Staff — an entry point not yet covered.

`Lesson_Report_Detail__c` is not a separate object in this system — a "report detail" row is the `Student_Sessions__c` record itself (`modifyLessonReportDetailsInStudentSession` takes `studentSessionId` as the detail identifier), so the same archive formula governs both attendance and report visibility for a student.

## Suite: Assign a teacher with only this lesson in lesson detail

### Lesson Report – Allocated Teacher – Archived Lesson Allocation – Student Row Not Shown for Report Entry

**Description:** Feature Impact (Attendance, Lesson Report, Report Detail) — Decision Table — a student whose Lesson Allocation has been archived must not appear as a row in the allocated teacher's Lesson Report form for that lesson, so the teacher cannot enter or submit a report for them.

**Preconditions:**
- An allocated teacher has lesson TC-TEACH-REPORT with two students assigned.
- Student A's Lesson Allocation has since been archived (Archived_At__c is populated) after its Student Package Order was fully removed, so Student A's Student Session Is_Archived__c = TRUE.
- Student B retains an active Lesson Allocation (Archived_At__c is blank) on the same lesson.
- The lesson report for TC-TEACH-REPORT is in an editable state.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher signs in and opens the Lesson Report form for TC-TEACH-REPORT | Student B's row is visible in the report form | Student B Is_Archived__c = FALSE → shown |
| 2 | Teacher looks for Student A's row in the same report form | Student A's row is absent; the teacher cannot enter a report for Student A | Student A Is_Archived__c = TRUE → hidden |

**Severity:** major
**Priority:** high

---

### Attendance Collection – Allocated Teacher – Archived Lesson Allocation – Student Row Not Shown for Attendance

**Description:** Feature Impact (Attendance, Lesson Report, Report Detail) — Decision Table — a student whose Lesson Allocation has been archived must not appear as a row on the allocated teacher's Attendance Collection screen for that lesson, so the teacher cannot mark their attendance.

**Preconditions:**
- An allocated teacher has lesson TC-TEACH-ATTEND with two students assigned.
- Student A's Lesson Allocation has since been archived (Archived_At__c is populated) after its Student Package Order was fully removed, so Student A's Student Session Is_Archived__c = TRUE.
- Student B retains an active Lesson Allocation (Archived_At__c is blank) on the same lesson.
- Attendance collection is open for TC-TEACH-ATTEND.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher signs in and opens the Attendance Collection screen for TC-TEACH-ATTEND | Student B's row is visible with attendance controls | Student B Is_Archived__c = FALSE → shown |
| 2 | Teacher looks for Student A's row on the same screen | Student A's row is absent; the teacher cannot mark attendance for Student A | Student A Is_Archived__c = TRUE → hidden |

**Severity:** major
**Priority:** high

---

### Lesson Report and Attendance – Allocated Teacher – Lesson Allocation Restored – Student Row Reappears, Report and Attendance Can Be Updated

**Description:** Feature Impact (Attendance, Lesson Report, Report Detail), control case — Decision Table — after a previously archived Lesson Allocation is restored (unarchived, same record Id), the student's row reappears automatically on both the Lesson Report form and the Attendance Collection screen, and the teacher can submit a report and mark attendance for them normally, confirming the exclusion above is fully reversible.

**Preconditions:**
- An allocated teacher has lesson TC-TEACH-RESTORE with Student A assigned.
- Student A's Lesson Allocation was previously archived, then unarchived (same record Id) after a living Student Package Order reappeared for the same Student Course, so Student A's Student Session Is_Archived__c = FALSE again.
- The lesson report for TC-TEACH-RESTORE is in an editable state; attendance collection is open for the lesson.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher signs in and opens the Lesson Report form for TC-TEACH-RESTORE | Student A's row is now visible in the report form | Student A Is_Archived__c = FALSE (restored) → shown |
| 2 | Teacher enters report content for Student A and submits | Input is accepted; report status becomes submitted for Student A | Student A row editable and submittable |
| 3 | Teacher opens the Attendance Collection screen for TC-TEACH-RESTORE | Student A's row is visible with attendance controls | Student A Is_Archived__c = FALSE (restored) → shown |
| 4 | Teacher sets an attendance status for Student A and saves | Attendance status is saved successfully for Student A | Student A row editable and savable |

**Severity:** major
**Priority:** high

---
