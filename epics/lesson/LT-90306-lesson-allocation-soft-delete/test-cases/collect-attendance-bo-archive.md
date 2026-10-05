# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 326 — "Collect Attendance on BO"](https://app.qase.io/project/PX?suite=326) (10 existing cases). None test an archived Lesson Allocation.

Code trace: the "Collect Attendance" dialog (`DialogsCollectAttendance.tsx`, shared by both `TabStudentSF` and `TabStudentSFV2`) reads its student list via `Lesson_GetStudentSessionAttendance`/`GetListLessonStudentSessions` GraphQL queries, both filtering `MANAERP__Is_Archived__c: { eq: false }` — consistent with the list page, so an archived student is correctly absent from the dialog on a fresh open. The save path (`PUT /studentSessions/v1` → `StudentSessionRestAPI.doPut` → `StudentSessionsHandler.bulkUpdateStudentSessionAttendance`, `StudentSessionsHandler.cls:942-1012`) re-queries `WHERE Id IN :studentSessionIds AND Is_Deleted__c = FALSE AND Is_Archived__c = FALSE` before applying updates — but this is a **silent-drop gap, not a hard gate**: any submitted `studentSessionId` that doesn't match (e.g., archived in the background after the dialog was opened) is simply absent from the query result and its update is skipped, with no error. `doPut()` unconditionally returns HTTP 200 regardless of how many of the submitted rows actually matched. Since this is a **bulk** endpoint (multiple students' attendance submitted in one PUT), this produces a distinct failure mode from the other archive gaps already found in this epic: not a crash, not a complete absence of filtering — a **false-positive success toast masking a silently-dropped partial update** within a batch.

## Suite: Collect Attendance on BO

### Collect Attendance Dialog – Fresh Open – Archived Student Excluded from the List

**Description:** Regression / control case — Decision Table — opening the Collect Attendance dialog for a lesson correctly excludes a student whose Lesson Allocation is archived, consistent with the Student tab's own list filter, since both read queries share the same `Is_Archived__c = false` filter.

**Preconditions:**
- Lesson L1 has Student A and Student B both assigned. Student A's Lesson Allocation is archived (Archived_At__c populated) after its Student Package Order was fully removed.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson L1's Collect Attendance dialog | Only Student B appears in the dialog; Student A is not listed | Student A Is_Archived__c = TRUE (via formula) → excluded from Lesson_GetStudentSessionAttendance's Is_Archived__c = false filter |

**Severity:** minor
**Priority:** medium

---

### Collect Attendance Dialog – Bulk Save – One of Multiple Selected Students Archived Mid-Session – That Student's Update Silently Dropped; Success Toast Still Shown for the Whole Batch

**Description:** Gap case — Decision Table, contrasts with the baseline (case 1919, "Update Attendance Status – All Valid Statuses and Reasons – Saved Correctly") — if a teacher has the Collect Attendance dialog open with Student A and Student B both loaded, sets attendance for both, and Student A's Lesson Allocation is archived in the background before Save is clicked, submitting the bulk update returns HTTP 200 and shows a success toast for the entire batch — but Student A's attendance update is silently dropped, since `bulkUpdateStudentSessionAttendance`'s re-query excludes their now-archived session with no error surfaced for that specific row.

**Preconditions:**
- HQ or CM Staff has Lesson L1's Collect Attendance dialog open with Student A and Student B both loaded, each with current Attendance Status = blank.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff sets Student A's status = Absent (reason = Traffic Issue) and Student B's status = Attend, but does not yet click Save | Both students' form fields show the selected values, unsaved | Dialog still open, no submission yet |
| 2 | In a separate session, the Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff (on the original, stale dialog, without refreshing) clicks "Save" to submit both students' attendance | A success toast is shown for the whole batch ("You have collected the attendance successfully"), with no indication that one student's update was dropped | PUT /studentSessions/v1 returns HTTP 200 unconditionally regardless of how many submitted rows actually matched |
| 4 | HQ or CM Staff opens Student B's Student Session record directly and confirms Attendance Status | Student B's Attendance Status = Attend — correctly saved | Student B Is_Archived__c = FALSE → included in the re-query, updated normally |
| 5 | HQ or CM Staff opens Student A's Student Session record directly and confirms Attendance Status | Student A's Attendance Status is still blank (or whatever it was before step 1) — the Absent/Traffic Issue update from step 1 was never applied, despite the success toast in step 3 | Student A excluded from bulkUpdateStudentSessionAttendance's WHERE Id IN :ids AND Is_Archived__c = FALSE re-query → silently skipped, no DML for this row |

**Severity:** major
**Priority:** medium

---
