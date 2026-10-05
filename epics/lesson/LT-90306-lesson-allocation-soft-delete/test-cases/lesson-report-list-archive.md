# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 1749 — "Lesson Report List"](https://app.qase.io/project/PX?suite=1749) (15 existing cases, under parent 292). None test an archived Lesson Allocation.

Code trace: "Search by Student Name" (case 13716) uses its own filter, `calcSearchTerm` (`school-portal-admin/src/squads/lesson/domains/LessonReport/hooks/useRetrieveLessonReportSFV2/lesson-report-filters.ts:34-67`, plus the Aver-tenant sibling `aver-lesson-report-filters.ts:45-78`) — a separately-implemented function from the Lesson List page's `calcSearch`, but patched in the same commit (`5e9fb50e`, "[LT-111546] filter archived lesson allocation records out of SF queries") with the identical `MANAERP__Is_Archived__c: { eq: false }` filter. Already correct, zero regression coverage.

"Bulk Update Individual Report"/"Bulk Update Group Report" (cases 13725/13726) are the same UI feature and write path — `POST /lessonReports/v1/update` with `isBulkUpdate = true` → `LessonReportHandler.updateLessonReport` → `modifyLessonReport` (`LessonReportHandler.cls:226-303`), a genuinely different Apex method from the already-confirmed `modifyLessonReportDetailsInStudentSession`. `modifyLessonReport` only ever writes `Lesson_Report__c` parent-level fields (Content, Announcement, Remarks, CM Note, etc.) — for **Group** reports, the `Lesson_Report__c` `afterUpdate` trigger separately cascades these fields down to child `Student_Sessions__c` rows via `updateLessonReportDetailInformation` (`LessonReportHandler.cls:435-472`), which correctly filters `WHERE ... Is_Deleted__c = FALSE AND Is_Archived__c = FALSE` (patched in the same commit as the already-confirmed method, `1eee000f`, "[LT-92895] ... Is_Archived__c checks"). For **Individual** reports, no cascade to `Student_Sessions__c` happens at all (the bulk-edited fields live only on the parent), so there is nothing archive-sensitive to check there.

A related observation (not a defect, documented for completeness): the base Lesson Report List query has no `Is_Archived__c` filter of its own outside the search box — but this is expected and consistent with the rest of this epic, since `Lesson_Report__c` is a lesson-level record representing potentially several students, not a single student's record, and should remain visible/editable regardless of any one student's archive state (same principle already locked in for suite 426's "Lesson-Level Report Fields ... Completely Unaffected" case).

## Suite: Lesson Report List

### Search by Student Name – Student's Only Session Archived – Report Excluded from Search Results; Restored – Reappears

**Description:** Regression / control case — Decision Table, contrasts with the baseline (case 13716, "Search by Student Name – Matching Reports Displayed") — searching for a student whose Lesson Allocation is archived returns no matching lesson report, consistent with the shared `Is_Archived__c = false` filter pattern already locked in for the Lesson List page (suite 250).

**Preconditions:**
- A lesson report exists for a lesson where Student A is the only student. Searching "Student A" on the Lesson Report List currently returns this report.
- Student A has an active Lesson Allocation.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff searches "Student A" on the Lesson Report List | The report appears in the results | Student A Is_Archived__c = FALSE → matched |
| 2 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff repeats the search for "Student A" | The report no longer appears in the results | Student A's Student Session Is_Archived__c = TRUE (via formula) → excluded from calcSearchTerm's semi-join |
| 4 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 5 | HQ or CM Staff repeats the search for "Student A" | The report reappears in the results | Is_Archived__c = FALSE (restored) → matched again |

**Severity:** minor
**Priority:** medium

---

### Bulk Update Group Report – One Student in the Group Archived – Cascade Correctly Skips That Student; Lesson-Level Fields and Other Students Update Normally

**Description:** Regression / control case — Decision Table, contrasts with the baseline (case 13726, "Bulk Update Group Report – Content, Homework, Announcement Updated for All Selected") — bulk-updating a Group lesson report that includes a student whose Lesson Allocation is archived still succeeds: the Lesson_Report__c-level Content/Homework/Announcement fields update correctly, and the cascade to Student_Sessions__c correctly skips the archived student's row (via `updateLessonReportDetailInformation`'s `Is_Archived__c = FALSE` filter) while still updating the other, non-archived students' rows normally. This locks in that bulk actions aren't broken or blocked by having one archived student mixed into a multi-student Group report.

**Preconditions:**
- A Group lesson report has Student A (active Lesson Allocation) and Student B (Lesson Allocation archived — Archived_At__c populated) both in the roster. The report is still listed and selectable on the Lesson Report List (not filtered out, since the list isn't scoped to a single student).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff selects this Group report (and others) on the Lesson Report List and uses "Bulk Update" to set Content = "Chapter 6 review", Homework = "Workbook p.30", Announcement = "Test next week" | The bulk update completes with no error | Bulk payload applies to the selected report(s) |
| 2 | HQ or CM Staff opens the Group report's Lesson_Report__c-level fields | Content, Homework, and Announcement all show the new values | Lesson_Report__c fields updated directly, unaffected by any student's archive state |
| 3 | HQ or CM Staff checks Student A's Student Session row for this lesson | Student A's row reflects the cascaded Content/Homework/Announcement update | Student A Is_Archived__c = FALSE → included in updateLessonReportDetailInformation's cascade |
| 4 | HQ or CM Staff checks Student B's Student Session row for this lesson | Student B's row is not found in the active list (archived), and did not receive the cascaded update — consistent with every other archived-session write path in this epic | Student B Is_Archived__c = TRUE → excluded from the cascade's WHERE clause, same as the already-confirmed pattern |

**Severity:** minor
**Priority:** medium

---
