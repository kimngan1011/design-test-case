# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 2374 — "Extend Recurring Lesson"](https://app.qase.io/project/PX?suite=2374) (65 existing cases, child of suite 219, feature LT-90573). Only the gap introduced by the Lesson Allocation archive refactor is covered here. Cases 17282 / 17284 / 17573 already prove the happy-path "extend lesson with Class auto-assigns active students" behavior via the same `CreateLessonBatchable` → `getActiveLessonAllocationIdsByClassIds` path — the archived-student dimension of that same path is what's new here.

## Suite: Extend Recurring Lesson

### Extend Recurring – Extend Lesson with Class – Class Member Archived – Student Not Auto-Assigned

**Description:** Feature Impact (Class Assignment / Master Queue) — Decision Table — extending a recurring Group lesson schedule for a Class must not auto-assign a student whose Class Member / Lesson Allocation has been archived by the Lesson Allocation soft-delete, even though the class membership's own effective date range would otherwise cover the newly created lessons.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- A recurring Group lesson schedule exists for Class A, linked to Course Math 101 and Location Tokyo HQ, with current End Date = 2026-05-15.
- Student A has a Class Member record on Class A with Effective_End_Date_Time__c = 2026-12-30, but its Lesson Allocation has been archived (Archived_At__c is populated) after the Student Package Order was fully removed, so Class Member Is_Archived__c = TRUE.
- Student B has a Class Member record on Class A with Effective_End_Date_Time__c = 2026-12-30 and an active Lesson Allocation (Archived_At__c is blank), so Class Member Is_Archived__c = FALSE.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Lesson Schedule detail for Class A and clicks Extend Recurrence | The Lesson Creation Form opens, pre-filled with the current End Date | current_end_date = 2026-05-15 |
| 2 | HQ or CM Staff sets the new End Date to 2026-05-29 and saves | New lessons are created in Draft status for 2026-05-16 through 2026-05-29 | new_end_date = 2026-05-29 |
| 3 | HQ or CM Staff opens one of the newly created lessons' Student Sessions related list and looks for Student B | Student B's Student Session is listed, auto-assigned | Student B Class Member Is_Archived__c = FALSE → included |
| 4 | HQ or CM Staff looks for Student A in the same related list | Student A's Student Session is absent; Student A was not auto-assigned | Student A Class Member Is_Archived__c = TRUE → excluded |

**Severity:** critical
**Priority:** high

---

### Extend Recurring – Extend Lesson with Class – Lesson Allocation Unarchived Before Extension – Student Auto-Assigned Going Forward, No Retroactive Backfill

**Description:** Feature Impact (Class Assignment / Master Queue) — Decision Table — after a previously archived Lesson Allocation is unarchived (Class Member returns to Is_Archived = FALSE on the same record), the student is auto-assigned to lessons created by a later Extend Recurrence, but lessons that already existed before the unarchive are not retroactively backfilled, since unarchiving a Lesson Allocation does not re-trigger the class-member assignment job.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- A recurring Group lesson schedule exists for Class A, linked to Course Math 101 and Location Tokyo HQ, with current End Date = 2026-06-15.
- Student A's Class Member on Class A was previously archived, then unarchived after a living Student Package Order reappeared for the same Student Course, so the same Class Member record now has Is_Archived__c = FALSE and Effective_End_Date_Time__c = 2026-12-30.
- A lesson created on 2026-06-10, before Student A's unarchive, currently has no Student Session for Student A.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Lesson Schedule detail for Class A and clicks Extend Recurrence | The Lesson Creation Form opens, pre-filled with the current End Date | current_end_date = 2026-06-15 |
| 2 | HQ or CM Staff sets the new End Date to 2026-06-29 and saves | New lessons are created in Draft status for 2026-06-16 through 2026-06-29 | new_end_date = 2026-06-29 |
| 3 | HQ or CM Staff opens one of the newly created lessons (2026-06-16 to 2026-06-29) and checks its Student Sessions related list for Student A | Student A's Student Session is listed, auto-assigned | Student A Class Member Is_Archived__c = FALSE (restored) → included |
| 4 | HQ or CM Staff opens the lesson on 2026-06-10, created before the unarchive | Student A's Student Session is still absent from that earlier lesson | Lesson predates unarchive timestamp → not retroactively backfilled |

**Severity:** major
**Priority:** high

---
