# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 2680 — "Publish and Notify Student – Notification Recipients"](https://app.qase.io/project/PX?suite=2680) (7 existing cases, Renseikai OOP). None test a student whose Lesson Allocation has been archived.

Code trace: `LessonHandler.publishLessonWithNotification()` → `UpdateLessonHandler.sendLessonUpdatedNotification()` → `StudentSessionsRepo.getStudentSessionByLessonIds()`, filtered `Is_Deleted__c = FALSE AND Is_Archived__c = FALSE`. Parent recipients are resolved only from the same filtered `studentIds` set, so an archived student's linked parent is excluded too.

## Suite: Publish and Notify Student – Notification Recipients

### [Renseikai] Notification Recipients – Student with Archived Lesson Allocation – Student and Linked Parent Not Notified

**Description:** AC 02.1 (Notification Recipients) — Decision Table — a student whose Lesson Allocation has been archived must not receive the "Publish and notify student" push notification, and their linked parent must not receive it either, since the parent lookup is keyed off the same archived-filtered student set.

**Preconditions:**
- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set).
- A lesson exists with status = Published; Student A was previously assigned with a Student Session.
- Student A's Lesson Allocation has since been archived (Archived_At__c is populated) after its Student Package Order was fully removed, so the Student Session Is_Archived__c = TRUE.
- Student B remains assigned to the same lesson with an active Lesson Allocation (Archived_At__c is blank).
- Student A and Student B are each logged into the Learner App on separate test devices with push notifications enabled; Parent A (linked to Student A via a Relationship record) is logged into the Parent App with push notifications enabled.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the SF Lesson Detail page of the Published lesson and click "Publish and notify student" | Confirmation modal appears | "" |
| 2 | Click "Send" in the modal | Modal closes | "" |
| 3 | On Student B's device, check the Learner App notification inbox | Student B receives a push notification with title "Lesson Published" | Student B Is_Archived__c = FALSE → included |
| 4 | On Student A's device, check the Learner App notification inbox | Student A does NOT receive any notification for this lesson | Student A Is_Archived__c = TRUE → excluded |
| 5 | On Parent A's device, check the Parent App notification inbox | Parent A does NOT receive any notification for this lesson either | Student A excluded → linked parent also excluded from the recipient set |

**Severity:** major
**Priority:** high

---
