# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suites reviewed: [PX suite 426 — "Lesson Report Detail"](https://app.qase.io/project/PX?suite=426) (16 existing cases, incl. case 3165 "Bulk Edit SRD"), plus suites 401 ("Lesson Report under Lesson") and 425 ("Lesson Report List"). Suites 401 and 425 test lesson-level report status transitions (Draft/Submitted/Published) and list filtering/bulk status actions — none of their scenarios involve per-student archive state, and no impact was found: their queries operate on `Lesson_Report__c` (one row per lesson) or lesson-level status fields, not on which students are visible. **No test cases were written for 401/425.**

Suite 426 does have per-student impact. Code trace: the save/bulk-edit backend for Student Report Detail (SRD) fields is `LessonReportHandler.modifyLessonReportDetailsInStudentSession` (exposed via REST at `/services/apexrest/MANAERP/lessonReports/v1/update`, not a direct LWC Aura call). Its lookup query (`LessonReportHandler.cls:316-323`) filters `WHERE Id IN :lessonReportDetailIds AND Is_Deleted__c = FALSE AND Is_Archived__c = FALSE`. Any submitted `studentSessionId` not found in that filtered map is **silently skipped via `continue`** (`LessonReportHandler.cls:331-333`) — no error is added, no entry appears in the `results` array for that student, and the REST call still returns HTTP 200. This creates a genuine "stale open tab" gap: if a teacher has the Report Detail page open with a student already loaded, and that student's Lesson Allocation gets archived by HQ/CM staff in the background before the teacher clicks Save, the bulk-edit silently drops that one student's changes with no visible error, while the rest of the batch saves normally. (Note: the page's own initial list/read query that populates the SRD grid could not be located in this repo — it likely lives in an external BO frontend consuming this REST API — so this test case focuses on the confirmed save-path behavior.)

## Suite: Lesson Report Detail

### Lesson Report Detail – Bulk Edit SRD – One Student's Lesson Allocation Archived Mid-Session (Stale Tab) – That Student's Edits Silently Dropped; Other Students Saved Normally, No Error Shown

**Description:** Gap case — Decision Table, contrasts with the baseline (case 3165, "Bulk Edit SRD – Selected students' fields updated; non-selected fields unchanged"): if a teacher has the Lesson Report Detail page open with Student A and Student B both loaded, and Student A's Lesson Allocation gets archived by staff in the background, submitting a bulk edit for both students silently drops Student A's changes with no error — the REST call still returns success, and nothing in the response distinguishes "archived and skipped" from "saved".

**Preconditions:**
- A Draft lesson report exists for a Published lesson with Student A and Student B both in Student Report Detail.
- Teacher has the Lesson Report Detail page open in SF, with both students' current SRD field values loaded (Student A and Student B both have active, non-archived Lesson Allocations at page-load time).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | While the teacher's page remains open, the Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated; Student A's Student Session flips to archived via the Is_Archived__c formula | Archived_At__c = current timestamp |
| 2 | Without refreshing the page, the teacher selects both Student A and Student B, uses Bulk Edit to set Understanding = "Good" for both, and clicks Save | The bulk-edit REST call (`/lessonReports/v1/update`) returns HTTP 200 with no error message shown to the teacher | modifyLessonReportDetailsInStudentSession's lookup query excludes Student A's now-archived session (Is_Archived__c = FALSE filter) |
| 3 | The teacher refreshes the Lesson Report Detail page | Student B's Understanding field shows "Good" (saved successfully); Student A no longer appears in the student list at all — their row (and whatever Understanding value it had before) is simply gone, with no indication the save for Student A was silently skipped | Student A's studentSessionId was not in the filtered map → silently `continue`d, no entry in the update results; Student A Is_Archived__c = TRUE |
| 4 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id, and the teacher reopens the Lesson Report Detail page | Student A reappears in Student Report Detail, with Understanding still showing its original pre-archive value (NOT "Good") — confirming the bulk-edit from step 2 never actually applied to Student A | Student A Is_Archived__c = FALSE (restored); Understanding__c unchanged from before step 2, since that update was silently dropped |

**Severity:** major
**Priority:** medium

---

### Lesson Report Detail – Student's Lesson Allocation Archived or Restored – Lesson-Level Report Fields and Other Students' Rows Completely Unaffected

**Description:** Regression / control case — Decision Table — `Lesson_Report__c` has no rollup/summary field derived from `Student_Sessions__c` (confirmed by field-level review: all 23 fields are either plain text/picklist/date or formulas pulling only from the parent `Lesson__r`), and archiving/restoring a Lesson Allocation performs no DML on `Lesson_Report__c` at all — only the archived student's own `Student_Sessions__c` row's `Is_Archived__c` formula changes. This case locks in that the lesson-level report (status, Content, Homework, CM Note) and every other student's SRD row are completely unaffected when one student's Lesson Allocation is archived or restored — only that one student's row appears/disappears.

**Preconditions:**
- A Draft lesson report exists for a Published lesson with Student A and Student B in Student Report Detail. The report has Content = "Chapter 3 review", CM Note = "Good progress", and status = Draft.
- Student A and Student B both have active (non-archived) Lesson Allocations.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff/Teacher records the current lesson-level report fields (Content, CM Note, status) and both students' SRD values | Content = "Chapter 3 review", CM Note = "Good progress", status = Draft; Student A and Student B both show their current SRD values | Baseline snapshot before archive |
| 2 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff/Teacher reopens the Lesson Report Detail page | Lesson-level fields (Content, CM Note, status) are unchanged from step 1; Student B's row and SRD values are unchanged; only Student A's row is now absent from the student list | No DML ever occurs on the Lesson_Report__c record itself — only Student A's Student_Sessions__c row's Is_Archived__c formula flips, excluding it from the query |
| 4 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id, and the page is reopened | Lesson-level fields (Content, CM Note, status) are still unchanged; Student A reappears with their original pre-archive SRD values intact; Student B's row is still unchanged | Archived_At__c = null (restored); Student A Is_Archived__c = FALSE → row reappears unmodified, since the underlying Student_Sessions__c record was never touched by any DML during the archive/restore cycle |

**Severity:** minor
**Priority:** medium

---

### Lesson Report Detail – Student Report Detail (SRD) Fields Survive Archive/Restore Unchanged – Hidden While Archived, Restored with Original Values Intact

**Description:** Regression / control case — Decision Table, contrasts with the baseline (case 3160, "Submitted Lesson Report – All SRD fields (Understanding, Quiz, Homework, CM Note, Remark) editable and saved correctly"): once a student's own SRD fields are filled in and the report is Submitted, archiving that student's Lesson Allocation hides the student's row entirely from Student Report Detail — not just the status field, but all five SRD fields together — and restoring the Lesson Allocation brings the exact same row back with every field value untouched, since the underlying `Student_Sessions__c` record is only ever hidden by the `Is_Archived__c` formula, never cleared or re-created.

**Preconditions:**
- A Submitted lesson report exists for a Published lesson with Student A in Student Report Detail. Student A's SRD fields are filled in: Understanding = "Excellent", In-lesson Quiz = "8/10", Homework Completion = "Done", CM Note = "Needs more practice on fractions", Remark = "Quiet today".
- Student A has an active (non-archived) Lesson Allocation.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff/Teacher opens Student Report Detail and records Student A's five SRD field values | Understanding = "Excellent", In-lesson Quiz = "8/10", Homework Completion = "Done", CM Note = "Needs more practice on fractions", Remark = "Quiet today" | Baseline snapshot before archive |
| 2 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff/Teacher reopens Student Report Detail | Student A's row — and all five SRD field values together — is no longer shown anywhere on the page; the report's own Submitted status is unaffected | Student A's Student_Sessions__c Is_Archived__c = TRUE (via formula) → row excluded from every SRD query |
| 4 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id, and the page is reopened | Student A's row reappears in Student Report Detail with all five SRD fields showing their exact original values — Understanding = "Excellent", In-lesson Quiz = "8/10", Homework Completion = "Done", CM Note = "Needs more practice on fractions", Remark = "Quiet today" — none reset to blank or default | Archived_At__c = null (restored); Student A Is_Archived__c = FALSE → the same Student_Sessions__c record reappears, field values unchanged since no DML ever cleared them during the archive/restore cycle |

**Severity:** major
**Priority:** high

---
