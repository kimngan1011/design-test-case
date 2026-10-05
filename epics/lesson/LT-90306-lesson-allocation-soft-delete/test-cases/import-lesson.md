# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 220 — "Import Lesson"](https://app.qase.io/project/PX?suite=220) (28 existing cases). "Import Lesson" has no dedicated Apex batch class — it inserts `Lesson__c`/`Lesson_Schedule__c` directly, so it runs through the same `LessonScheduleHandler.afterInsert → CREATE_LESSON Master Queue → CreateLessonBatchable → getActiveLessonAllocationIdsByClassIds (Is_Archived__c = FALSE)` path already verified for suites 218 and 2374 — not a separate code path. Only case 1033 ("Group with enrolled students") touches this mechanism; the other 27 cases (recurring patterns, closed dates, CSV validation, boundary values) are unrelated to `Archived_At__c`/`Is_Archived__c`.

## Suite: Import Lesson

### Import Lesson – Group with Archived Class Member – Student Not Auto-Assigned

**Description:** Feature Impact (Class Assignment / Master Queue) — Decision Table — importing a Group lesson CSV for a Class with an enrolled student whose Lesson Allocation has been archived must not auto-assign that student to the imported lesson, since the import path reuses the same create-lesson flow as manual creation.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce with Import Lesson permission.
- Class A exists, linked to Course Math 101 and Location Tokyo HQ.
- Student A has a Class Member record on Class A whose Lesson Allocation has been archived (Archived_At__c is populated) after its Student Package Order was fully removed, so Class Member Is_Archived__c = TRUE.
- Student B has a Class Member record on Class A with an active Lesson Allocation (Archived_At__c is blank), so Class Member Is_Archived__c = FALSE.
- CSV prepared: teaching_method=Group, class=Class A, is_recurring=false, lesson_date=2026-05-20.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff imports the CSV for the Group lesson on Class A | The lesson is created on SF and BO with Draft status | class = Class A; lesson_date = 2026-05-20 |
| 2 | HQ or CM Staff opens the imported lesson's Student Sessions related list and looks for Student B | Student B's Student Session is listed, auto-assigned | Student B Class Member Is_Archived__c = FALSE → included |
| 3 | HQ or CM Staff looks for Student A in the same related list | Student A's Student Session is absent; Student A was not auto-assigned | Student A Class Member Is_Archived__c = TRUE → excluded |

**Severity:** critical
**Priority:** high

---

### Import Lesson – Group Lesson – Lesson Allocation Archived Then Restored – Student Session Reappears, Re-Assignable on Next Import

**Description:** AC-3 / AC-5 (unarchive rebuild + read-path filtering) — State Transition — after a student's Lesson Allocation is archived and later restored (unarchived, same record Id), their existing Student Session on the originally imported lesson reappears automatically with no resync job needed (pure formula flip on `Is_Archived__c`), and the student is auto-assignable again when a new lesson is imported for the same Class.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce with Import Lesson permission.
- Class A exists, linked to Course Math 101 and Location Tokyo HQ.
- Student A has a Class Member record on Class A with an active Lesson Allocation (Archived_At__c is blank).
- CSV prepared for a one-time Group lesson on Class A, lesson_date = 2026-05-20.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff imports the CSV for the Group lesson on 2026-05-20 | The lesson is created with Draft status, and Student A is auto-assigned — a Student Session is listed for Student A | lesson_date = 2026-05-20; Student A Is_Archived__c = FALSE → included |
| 2 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp (archive #1) |
| 3 | HQ or CM Staff reopens the lesson on 2026-05-20's Student Sessions related list | Student A no longer appears; the Student Session record still exists | Student A Is_Archived__c = TRUE → hidden; session not deleted |
| 4 | A living Student Package Order reappears for the same Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 5 | HQ or CM Staff reopens the same lesson on 2026-05-20's Student Sessions related list, without re-importing or reassigning anything | Student A reappears automatically in the list — the same original Student Session, not a new one | Student A Is_Archived__c = FALSE (restored) → shown again; Student Session Id unchanged from step 1 |
| 6 | HQ or CM Staff imports a new CSV for a second one-time Group lesson on Class A, lesson_date = 2026-05-27 | The new lesson is created, and Student A is auto-assigned to it as well | lesson_date = 2026-05-27; Student A Is_Archived__c = FALSE → included again |

**Severity:** critical
**Priority:** high

---
