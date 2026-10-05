# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Feature: Calendar bulk-publish-with-student (`Lesson_Custom_Settings__c.Bulk_Publish_With_Student__c`, Apex `LessonHandler.updateToNewLessonStatusByTime` → `LessonBulkMasterQueueExecutor`). No Qase suite identified yet for this feature — these cases are written directly from code and should be filed under whichever suite covers "bulk publish lessons by date range / location / student on Calendar" once located; a new suite is created at import time if none matches.

Code trace: the executor has three distinct selection branches depending on whether a student filter is supplied:
- No student filter → `getLessonsToUpdate()`: every Draft lesson in the date range/location, no student condition at all.
- Student filter = the `__StudentNoneAssigned` sentinel → `getUnassignedLessonsToUpdate()`: Draft lessons with **no** `Student_Sessions__c` row where `Is_Archived__c = FALSE` — a lesson whose only session belongs to an archived Lesson Allocation is treated as unassigned.
- Student filter = a real student Id → the query additionally requires `Lesson_Allocation__r.Student__c = :studentId AND ... AND Is_Archived__c = FALSE` — an archived student simply returns zero eligible lessons.

After publishing, `doFinish` always sends the "bulk_publish_lesson" notification via `sendLessonUpdatedNotification()` → `StudentSessionsRepo.getStudentSessionByLessonIds()` (same `Is_Archived__c = FALSE` filter as the single Publish-and-Notify and date/time-change notifications).

## Suite: Bulk Publish Lesson by Date Range (Calendar – With Student)

### Bulk Publish Lesson by Date Range – Specific Student Selected – Student with Archived Lesson Allocation Has No Lessons Published

**Description:** Negative Testing / Decision Table — when staff runs the Calendar bulk-publish action scoped to a specific student whose Lesson Allocation has been archived, no lesson is published for that student and no error is shown, since the eligibility query requires `Is_Archived__c = FALSE`.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce with access to the Calendar bulk-publish action.
- `Bulk_Publish_With_Student__c` custom setting is enabled.
- Student A has a Draft lesson TC-BULK-A at Location Tokyo HQ within the target date range, assigned via a Student Session whose Lesson Allocation has since been archived (Archived_At__c is populated), so the session's Is_Archived__c = TRUE.
- Student B has a separate Draft lesson TC-BULK-B at the same Location and date range, with an active Lesson Allocation (Archived_At__c is blank).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Calendar bulk-publish action for Location Tokyo HQ, sets the date range to cover 2026-05-18 to 2026-05-22, selects "Apply to selected students", and picks Student A only, then confirms | The action completes with no error | date range = 2026-05-18 to 2026-05-22; student = Student A |
| 2 | HQ or CM Staff opens TC-BULK-A | TC-BULK-A status is still Draft; it was not published | Student A Is_Archived__c = TRUE → excluded, 0 eligible lessons found |
| 3 | HQ or CM Staff repeats the bulk-publish action for the same date range and Location, this time selecting Student B | The action completes with no error | student = Student B |
| 4 | HQ or CM Staff opens TC-BULK-B | TC-BULK-B status is now Published | Student B Is_Archived__c = FALSE → included |

**Severity:** major
**Priority:** high

---

### Bulk Publish Lesson by Date Range – Unassigned-Lesson Scope – Lesson with Only an Archived Student Session Is Published as Unassigned

**Description:** Boundary / Decision Table — when staff runs the Calendar bulk-publish action scoped to "lessons with no assigned student," a Draft lesson whose only Student Session belongs to an archived Lesson Allocation is treated as unassigned and gets published, because the unassigned-lesson query excludes archived sessions when checking for an existing assignment.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce with access to the Calendar bulk-publish action.
- `Bulk_Publish_With_Student__c` custom setting is enabled.
- Draft lesson TC-BULK-UNASSIGNED exists at Location Tokyo HQ within the target date range. Its only Student Session belongs to Student A, whose Lesson Allocation has since been archived (Archived_At__c is populated), so the session's Is_Archived__c = TRUE.
- A second Draft lesson TC-BULK-TRULY-EMPTY exists in the same scope with no Student Session at all.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Calendar bulk-publish action for Location Tokyo HQ, sets the date range to cover both lessons, selects the "no student assigned" scope, and confirms | The action completes with no error | date range covers both TC-BULK-UNASSIGNED and TC-BULK-TRULY-EMPTY |
| 2 | HQ or CM Staff opens TC-BULK-UNASSIGNED | Status is now Published, even though Student A's historical (archived) session is still attached to it | Student A Is_Archived__c = TRUE → not counted as an existing assignment, lesson qualifies as "unassigned" |
| 3 | HQ or CM Staff opens TC-BULK-TRULY-EMPTY | Status is now Published | No session at all → qualifies as unassigned |

**Severity:** minor
**Priority:** medium

---

### Bulk Publish Lesson by Date Range – Notification After Bulk Publish – Student with Archived Lesson Allocation Not Notified

**Description:** Feature Impact / notification recipients — Decision Table — after the Calendar bulk-publish action completes, the follow-up push notification must not be sent to a student whose Lesson Allocation is archived, consistent with the single Publish-and-Notify and date/time-change notification paths.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce with access to the Calendar bulk-publish action.
- `Bulk_Publish_With_Student__c` and the teacher-publish-notification toggle are enabled.
- Draft lesson TC-BULK-NOTI exists at Location Tokyo HQ within the target date range, with two assigned students: Student A (Lesson Allocation archived, Archived_At__c populated, session Is_Archived__c = TRUE) and Student B (active Lesson Allocation, Archived_At__c blank).
- Student A and Student B are each logged into the Learner App on separate test devices with push notifications enabled.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Calendar bulk-publish action for Location Tokyo HQ, sets the date range to cover TC-BULK-NOTI, and confirms without a student filter | TC-BULK-NOTI status becomes Published | date range covers TC-BULK-NOTI |
| 2 | On Student B's device, check the Learner App notification inbox | Student B receives the bulk-publish push notification | Student B Is_Archived__c = FALSE → included |
| 3 | On Student A's device, check the Learner App notification inbox | Student A does NOT receive any notification for this lesson | Student A Is_Archived__c = TRUE → excluded |

**Severity:** major
**Priority:** high

---
