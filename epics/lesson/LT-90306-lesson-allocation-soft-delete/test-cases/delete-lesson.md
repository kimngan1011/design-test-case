# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 258 — "Delete lesson"](https://app.qase.io/project/PX?suite=258) (9 existing cases). None of the existing cases distinguish archived vs active Lesson Allocation on the deleted lesson's student sessions.

Code trace: `DeleteLessonHandler.cls:9-32` (`cleanStudentSessionInfo`, called from `beforeDelete`) queries `Student_Sessions__c WHERE Lesson__c IN :deletedLessonIds AND Is_Deleted__c = FALSE AND Is_Archived__c = FALSE` and passes only the result into `StudentSessionsHandler.unassignStudentSessionsFromLesson()`. A session belonging to an **archived** Lesson Allocation is excluded from this call.

`Student_Sessions__c.Lesson__c` is a Lookup field with `deleteConstraint = SetNull` (`objects/Student_Sessions__c/fields/Lesson__c.field-meta.xml`), so Salesforce itself still clears the `Lesson__c` reference automatically regardless of the Apex filter — **no dangling-record risk**. What's actually skipped for an excluded (archived) session is the rest of what `unassignStudentSessionsFromLesson` (`StudentSessionsHandler.cls:470-494`) does: `ReallocationHandler.modifyReallocationAfterUnassignSessions` (for sessions with `Reallocate_Flag__c = true`) and `deleteRelatedMediaAndZoomParticipants` (Lesson Report Media tied to that session). Those two side effects do not run for an archived session's lesson deletion.

## Suite: Delete lesson

### Delete Lesson – Student Session Under Archived Lesson Allocation – Reallocation Request Not Closed, Media Not Cleaned Up

**Description:** Feature Impact / data-integrity gap — Decision Table — when the lesson behind a student session is deleted, a session belonging to an archived Lesson Allocation is excluded from the delete-lesson cascade cleanup, so its linked Reallocation request is not closed and its Lesson Report Media is not deleted, even though its `Lesson__c` field is still cleared automatically by Salesforce.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce with Delete Lesson permission.
- A one-time lesson TC-DEL-archived exists for Course Math 101 at Location Tokyo HQ, status = Draft.
- Student A has a Student Session on TC-DEL-archived with Reallocate_Flag__c = TRUE and an attached Lesson Report Media.
- Student A's Lesson Allocation has since been archived (Archived_At__c is populated), so the session's Is_Archived__c = TRUE.
- An open Reallocation request record exists referencing this Student Session.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff clicks Delete on TC-DEL-archived and confirms | The lesson is deleted; success notification shown | "" |
| 2 | HQ or CM Staff opens Student A's Student Session record directly by its record Id | The Student Session record still exists; its Lesson field is now blank | Lesson__c = null (Salesforce lookup SetNull on parent delete) |
| 3 | HQ or CM Staff opens the Reallocation request linked to this session | The Reallocation request still shows its original pending/open status; it was not closed or updated by the delete | Student A Is_Archived__c = TRUE → excluded from cleanup; status stale |
| 4 | HQ or CM Staff checks the Lesson Report Media attached to this session | The media record still exists; it was not deleted | Student A Is_Archived__c = TRUE → excluded from cleanup |

**Severity:** major
**Priority:** high

---

### Delete Lesson – Student Session Under Active Lesson Allocation – Reallocation Request Closed and Media Cleaned Up

**Description:** Feature Impact / data-integrity gap, control case — Decision Table — the same delete-lesson flow for a student session belonging to an active (non-archived) Lesson Allocation correctly closes the linked Reallocation request and deletes the Lesson Report Media, confirming the gap above is specific to the archived state and not a regression in the normal flow.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce with Delete Lesson permission.
- A one-time lesson TC-DEL-active exists for Course Math 101 at Location Tokyo HQ, status = Draft.
- Student B has a Student Session on TC-DEL-active with Reallocate_Flag__c = TRUE and an attached Lesson Report Media.
- Student B's Lesson Allocation is active (Archived_At__c is blank), so the session's Is_Archived__c = FALSE.
- An open Reallocation request record exists referencing this Student Session.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff clicks Delete on TC-DEL-active and confirms | The lesson is deleted; success notification shown | "" |
| 2 | HQ or CM Staff opens Student B's Student Session record directly by its record Id | The Student Session record still exists; its Lesson field is blank | Lesson__c = null |
| 3 | HQ or CM Staff opens the Reallocation request linked to this session | The Reallocation request is closed/updated by the delete-lesson cleanup | Student B Is_Archived__c = FALSE → included in cleanup |
| 4 | HQ or CM Staff checks the Lesson Report Media attached to this session | The media record has been deleted | Student B Is_Archived__c = FALSE → included in cleanup |

**Severity:** major
**Priority:** medium

---
