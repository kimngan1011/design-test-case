# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 1405 — "Send noti when changing lesson date&time of a published lesson"](https://app.qase.io/project/PX?suite=1405) (9 existing cases). None distinguish archived vs active Lesson Allocation among the lesson's assigned students.

Code trace: `UpdateLessonHandler.sendLessonNotification()` (`UpdateLessonHandler.cls:348-389`, gated on `lessonSource.Status__c == Published`) calls `sendLessonUpdatedNotification()`, which resolves recipients via `StudentSessionsRepo.getStudentSessionByLessonIds()` — the same repository method used by the "Publish and Notify Student" feature (suite 2680) — filtered `Is_Deleted__c = FALSE AND Is_Archived__c = FALSE`. A student whose Lesson Allocation has been archived is correctly excluded from this notification too, but no existing case verifies it.

## Suite: Send noti when changing lesson date&time of a published lesson

### Lesson Notification – Published Lesson Date/Time Changed – Student with Archived Lesson Allocation Not Notified

**Description:** Feature Impact / notification recipients — Decision Table — when a published lesson's date or time is changed, a student whose Lesson Allocation has been archived must not receive the schedule-change push notification, since the recipient list is built from the same `Is_Archived__c = FALSE`-filtered query used by Publish and Notify Student.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce with Update Lesson permission.
- A published lesson TC-NOTI exists for Course Math 101 at Location Tokyo HQ.
- Student A was previously assigned to TC-NOTI; Student A's Lesson Allocation has since been archived (Archived_At__c is populated) after its Student Package Order was fully removed, so the Student Session Is_Archived__c = TRUE.
- Student B remains assigned to TC-NOTI with an active Lesson Allocation (Archived_At__c is blank).
- Student A and Student B are each logged into the Learner App on separate test devices with push notifications enabled.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens TC-NOTI and changes the lesson's date/time to a new valid value, then saves | The lesson's date/time is updated; a schedule-change notification is triggered | New date/time saved |
| 2 | On Student B's device, check the Learner App notification inbox | Student B receives the lesson date/time-change notification | Student B Is_Archived__c = FALSE → included |
| 3 | On Student A's device, check the Learner App notification inbox | Student A does NOT receive any notification for this lesson | Student A Is_Archived__c = TRUE → excluded |

**Severity:** major
**Priority:** high

---
