# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 257 — "Duplicate lesson"](https://app.qase.io/project/PX?suite=257) (14 existing cases). The Duplicate button opens the same Create Lesson form pre-filled from the source lesson (confirmed by case 1207's own expected result) — no separate Apex controller was found, so Duplicate is treated as another entry point into the same `LessonScheduleHandler.afterInsert → CREATE_LESSON Master Queue → CreateLessonBatchable → getActiveLessonAllocationIdsByClassIds (Is_Archived__c = FALSE)` path already verified for suites 218, 2374, and 220 — inferred with high confidence from the UI pattern, not traced to a dedicated Duplicate controller class. The other 12 cases (recurrence/count/day pre-fill, closed date override, and the 4 recent LT-107960 Duration-field regression cases) are unrelated to `Archived_At__c`/`Is_Archived__c`.

## Suite: Duplicate lesson

### Duplicate Lesson – Group with Class – Class Member Archived – Student Not Auto-Assigned

**Description:** Feature Impact (Class Assignment / Master Queue) — Decision Table — duplicating a lesson into a new Group lesson tied to a Class must not auto-assign a student whose Class Member / Lesson Allocation has been archived, since Duplicate submits through the same Create Lesson flow as manual creation and CSV import.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- A one-time lesson TC-DUP-source exists for Course Math 101 at Location Tokyo HQ.
- Class A exists, linked to Course Math 101.
- Student A has a Class Member record on Class A whose Lesson Allocation has been archived (Archived_At__c is populated) after its Student Package Order was fully removed, so Class Member Is_Archived__c = TRUE.
- Student B has a Class Member record on Class A with an active Lesson Allocation (Archived_At__c is blank), so Class Member Is_Archived__c = FALSE.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff clicks Duplicate on TC-DUP-source, changes Teaching Method to Group with Class A, then saves | The duplicate lesson is created with Draft status, Teaching Method = Group, Class = A | class = Class A |
| 2 | HQ or CM Staff opens the duplicated lesson's Student Sessions related list and looks for Student B | Student B's Student Session is listed, auto-assigned | Student B Class Member Is_Archived__c = FALSE → included |
| 3 | HQ or CM Staff looks for Student A in the same related list | Student A's Student Session is absent; Student A was not auto-assigned | Student A Class Member Is_Archived__c = TRUE → excluded |

**Severity:** critical
**Priority:** high

---

### Duplicate Lesson – Group with Class – Lesson Allocation Restored – Student Auto-Assigned on Next Duplicate

**Description:** Feature Impact (Class Assignment / Master Queue) — Decision Table — after a previously archived Lesson Allocation is restored (unarchived, same Class Member record returns to Is_Archived = FALSE), the student is auto-assigned normally when a new lesson is created via Duplicate, confirming the archive filter does not permanently block a restored student on this entry point either.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- A one-time lesson TC-DUP-source-2 exists for Course Math 101 at Location Tokyo HQ.
- Class A exists, linked to Course Math 101.
- Student A's Class Member on Class A was previously archived, then unarchived after a living Student Package Order reappeared for the same Student Course, so the same Class Member record now has Is_Archived__c = FALSE.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff clicks Duplicate on TC-DUP-source-2, changes Teaching Method to Group with Class A, then saves | The duplicate lesson is created with Draft status, Teaching Method = Group, Class = A | class = Class A |
| 2 | HQ or CM Staff opens the duplicated lesson's Student Sessions related list and looks for Student A | Student A's Student Session is listed, auto-assigned | Student A Class Member Is_Archived__c = FALSE (restored) → included |

**Severity:** major
**Priority:** high

---
