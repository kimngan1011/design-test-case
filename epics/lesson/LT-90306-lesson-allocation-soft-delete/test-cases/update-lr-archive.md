# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 3269 — "Update LR"](https://app.qase.io/project/PX?suite=3269) (12 existing cases, under "Lesson Report under Lesson" parent 427). This suite covers the same underlying Lesson Report Detail / Student Report Detail (SRD) mechanism already fully traced and tested in suite 426 (`lesson-report-detail-bulk-edit-archive.md`) — same `LessonReportHandler.modifyLessonReportDetailsInStudentSession` backend, same `Is_Archived__c = FALSE` filter behavior and silent-skip-on-archived-session gap. This file re-applies those findings against this suite's own baseline case numbers, since it is a distinct Qase suite ID in the test plan.

Code trace (already established): `LessonReportHandler.modifyLessonReportDetailsInStudentSession`'s lookup query filters `WHERE Id IN :lessonReportDetailIds AND Is_Deleted__c = FALSE AND Is_Archived__c = FALSE`. Any submitted `studentSessionId` not in that filtered map is silently skipped (`continue`), with no error and no entry in the results — the REST call still returns success. `Lesson_Report__c`-level fields (Content, CM Note, status) and other students' SRD rows are completely untouched by one student's archive/restore cycle, since no DML ever touches `Lesson_Report__c` as a side effect of archiving.

## Suite: Update LR

### Bulk Edit Individual Report via BO – One Student's Lesson Allocation Archived Mid-Session – That Student's Edit Silently Dropped; Others Saved Normally

**Description:** Gap case — Decision Table, contrasts with the baseline (case 3604, "Bulk Edit Individual Report via BO – Changes Reflected on BO and Mobile") — if a teacher has the Report tab open with Student A and Student B both loaded, and Student A's Lesson Allocation is archived in the background before Save, the bulk edit silently drops Student A's changes with no error while Student B's changes save normally.

**Preconditions:**
- A Draft lesson report exists with Student A and Student B both in the Report tab, both with active (non-archived) Lesson Allocations.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher opens the Report tab with both students loaded | Both students' current SRD values are shown | Student A and Student B Is_Archived__c = FALSE |
| 2 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | Teacher (on the stale page) bulk-edits Understanding = "Good" for both students and saves | No error is shown; the save appears to succeed | modifyLessonReportDetailsInStudentSession's lookup excludes Student A's now-archived session |
| 4 | Teacher refreshes the Report tab | Student B's Understanding shows "Good"; Student A no longer appears in the list at all, with no indication their edit was dropped | Student A Is_Archived__c = TRUE (via formula); Student B's update succeeded independently |

**Severity:** major
**Priority:** medium

---

### Student Report Detail Fields – Archive/Restore Cycle – Values Survive Unchanged

**Description:** Regression / control case — Decision Table, contrasts with the baseline (case 13750, "Edit Individual Report – Fields Updated – Published and Visible on Mobile") — a student's already-saved SRD fields (Understanding, Homework, CM Note, etc.) are hidden while their Lesson Allocation is archived and reappear with the exact same values once restored, since the underlying `Student_Sessions__c` record is only ever hidden by the `Is_Archived__c` formula, never cleared.

**Preconditions:**
- Student A has SRD fields filled in on a Published lesson report: Understanding = "Excellent", Homework Completion = "Done".
- Student A has an active Lesson Allocation.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher/CM confirms Student A's current SRD values on the Report tab | Understanding = "Excellent", Homework Completion = "Done" | Baseline snapshot |
| 2 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | Teacher/CM reopens the Report tab | Student A's row is no longer shown | Is_Archived__c = TRUE (via formula) |
| 4 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id, and the page is reopened | Student A's row reappears with Understanding = "Excellent", Homework Completion = "Done" — unchanged | Is_Archived__c = FALSE (restored); no data loss |

**Severity:** major
**Priority:** high

---

### Report Tab – Student Show/Hide Accuracy Through Archive/Restore Cycle – Other Students Unaffected Throughout

**Description:** Regression / control case — Decision Table, contrasts with the baseline (case 3595, "Student List Sort – Mixed Grades and JP Names") — a student's row on the Report tab disappears exactly when their Lesson Allocation is archived and reappears exactly when restored, with no delay, no stale flash of incorrect data, and no effect whatsoever on other students' rows or sort order at any point in the cycle.

**Preconditions:**
- A lesson report has Student A, Student B, and Student C all listed on the Report tab, correctly sorted by Grade then Name. All three have active Lesson Allocations.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher/CM opens the Report tab and confirms all three students (A, B, C) are listed in the correct sort order | All three appear, correctly sorted | All three Is_Archived__c = FALSE |
| 2 | The Student Package Order behind Student B's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | Teacher/CM refreshes the Report tab | Student B is no longer shown; Student A and Student C still appear, in the same correct relative sort order as before, with no gap or placeholder left where Student B was | Student B Is_Archived__c = TRUE (via formula) → excluded; Student A/C unaffected |
| 4 | A living Student Package Order reappears for Student B's Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 5 | Teacher/CM refreshes the Report tab | Student B reappears, correctly re-inserted into the sort order by Grade/Name (not appended at the end); Student A and Student C remain unaffected and unchanged throughout | Student B Is_Archived__c = FALSE (restored) → included again, sorted correctly alongside A and C |

**Severity:** minor
**Priority:** medium

---
