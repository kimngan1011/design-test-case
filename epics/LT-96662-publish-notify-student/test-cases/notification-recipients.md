# Test Cases: LT-96662 — Publish and Notify Student

## Suite: Publish and Notify Student – Notification Recipients

### Notification Recipients – Student with One Parent – Student and parent both receive notification

**Description:** AC 02.1 — CRUD Testing + Decision Table — When a lesson has one assigned student with one linked parent, both receive the push notification after "Send" is clicked.

**Preconditions:**
- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- A lesson exists with status = **Published**; lesson name: "English Level 3 – Session 1"; lesson date: 2026-04-20; start time: 10:00; end time: 11:00
- **Student A** is assigned to the lesson; Student A's Learner App account is logged in on Device 1 with push notifications enabled
- **Parent A** has a Relationship record linking them to Student A (parent-student type); Parent A is logged into the Parent App on Device 2 with push notifications enabled

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Navigate to the SF Lesson Detail page of the Published lesson | Lesson Detail page opens; status = "Published" | Lesson: "English Level 3 – Session 1" |
| 2   | Click "Publish and notify student" | Confirmation modal appears | "" |
| 3   | Click "Send" | Modal closes | "" |
| 4   | On Device 1, open the Learner App and check the notification inbox | Student A receives a push notification with title "Lesson Published" | Student A account (Device 1) |
| 5   | On Device 2, open the Parent App and check the notification inbox | Parent A receives a push notification with title "Lesson Published" for the same lesson | Parent A account (Device 2) |

**Severity:** critical
**Priority:** high

---

### Notification Recipients – Student with Multiple Parents – Student and all linked parents receive notification

**Description:** AC 02.1 — CRUD Testing + Decision Table — When a student has multiple parent Relationship records, all linked parents receive the push notification.

**Preconditions:**
- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- A lesson exists with status = **Published** with **Student C** assigned
- **Parent C1** and **Parent C2** are both linked to Student C via separate Relationship records (parent-student type)
- Student C is on Device 1 (Learner App, push enabled); Parent C1 is on Device 2 (Parent App, push enabled); Parent C2 is on Device 3 (Parent App, push enabled)

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Navigate to the SF Lesson Detail page of the Published lesson | Lesson Detail page opens; status = "Published" | Lesson ID with Student C assigned |
| 2   | Click "Publish and notify student" and then click "Send" | Modal closes | "" |
| 3   | On Device 1 (Student C), check the Learner App notification inbox | Student C receives push notification with title "Lesson Published" | Student C Learner App account |
| 4   | On Device 2 (Parent C1), check the Parent App notification inbox | Parent C1 receives push notification with title "Lesson Published" | Parent C1 Parent App account |
| 5   | On Device 3 (Parent C2), check the Parent App notification inbox | Parent C2 receives push notification with title "Lesson Published" | Parent C2 Parent App account |

**Severity:** critical
**Priority:** high

---

### Notification Recipients – Student with No Linked Parent – Only student receives notification

**Description:** AC 02.1 + Gap #3 — Decision Table + Negative Testing — When the assigned student has no Relationship records linking any parent Contact, only the student is notified and no error occurs.

> ⚠️ **Note:** Expected behavior (student-only notification, no error) to be confirmed with product team after test execution. Share the result for confirmation.

**Preconditions:**
- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- A lesson exists with status = **Published** with **Student D** assigned
- Student D has **no** linked parent Contacts via any Relationship record
- Student D is logged into the Learner App on Device 1 with push notifications enabled

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Navigate to the SF Lesson Detail page of the Published lesson | Lesson Detail page opens; status = "Published" | Lesson ID with Student D assigned (no parent) |
| 2   | Click "Publish and notify student" | Confirmation modal appears without error | "" |
| 3   | Click "Send" | Modal closes; no error message or warning shown on SF page | "" |
| 4   | On Device 1, check the Learner App notification inbox for Student D | Student D receives push notification with title "Lesson Published" | Student D Learner App account |

**Severity:** major
**Priority:** high

---

### Notification Recipients – Parent/Student Has No Device Token – Notification silently skipped, other recipients still notified

**Description:** AC 02.1 + Gap #4 — Decision Table + Negative Testing — When a recipient (parent) has never logged into the app (no device token), the notification is silently skipped for that recipient without any error, and other recipients with valid tokens still receive it.

**Preconditions:**
- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- A lesson exists with status = **Published** with **Student E** assigned
- **Parent E** is linked to Student E via a Relationship record but **has never logged into the Parent App** (no device token registered)
- Student E is logged into the Learner App on Device 1 with push notifications enabled

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Navigate to the SF Lesson Detail page of the Published lesson | Lesson Detail page opens; status = "Published" | Lesson ID with Student E assigned |
| 2   | Click "Publish and notify student" | Confirmation modal appears | "" |
| 3   | Click "Send" | Modal closes; no error message shown on SF page | "" |
| 4   | On Device 1, check the Learner App notification inbox for Student E | Student E receives push notification with title "Lesson Published" | Student E Learner App account |
| 5   | Confirm Parent E's state (never logged in) and verify no error logged on SF or visible to the operator | No error banner or failure message is shown to the SF user; Parent E simply does not receive a notification | Parent E contact (no app login) |

**Severity:** normal
**Priority:** medium

---

### Notification Recipients – Multiple Students Under Same Parent – Parent receives notification for each student's lesson separately

**Description:** Gap from coverage — Decision Table — When a parent has multiple students, triggering the notification for Student A's lesson sends a notification specific to Student A's lesson only, and does not affect Student B.

> ⚠️ **Note:** Expected behavior to be confirmed with product team after test execution.

**Preconditions:**
- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- **Parent F** is linked to both **Student F1** and **Student F2** via Relationship records
- Lesson X is assigned to **Student F1** only (not Student F2); status = Published
- Parent F is logged into the Parent App on Device 1
- Student F1 is on Device 2 (Learner App)

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Navigate to the SF Lesson Detail page of Lesson X (Published, assigned to Student F1) | Lesson Detail page opens | Lesson X ID — assigned to Student F1 only |
| 2   | Click "Publish and notify student", then click "Send" | Modal closes | "" |
| 3   | On Device 1, check Parent F's Parent App notification inbox | Parent F receives one push notification referencing Lesson X (Student F1's lesson); the notification does not reference Student F2 | Parent F Parent App account |
| 4   | On Device 2, check Student F1's Learner App notification inbox | Student F1 receives push notification with title "Lesson Published" | Student F1 Learner App account |

**Severity:** major
**Priority:** high

---

### Notification Recipients – Multiple Students Switch Account Same Device – Notification delivered only to the account whose student is assigned

**Description:** Gap — Decision Table — When multiple student accounts are logged into the same device via the switch account feature (e.g. Student F1 and Student F2), only the account whose student is assigned to the lesson receives the push notification; the other account does not.

> ⚠️ **Note:** Expected behavior (notification delivered only to the assigned student's registered device token, not to other accounts on the same device) to be confirmed with product team after test execution.

**Preconditions:**
- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- Device 1 has the Learner App installed with **two student accounts** logged in via switch account:
  - **Account 1:** Student F1 (currently active / foreground account)
  - **Account 2:** Student F2
- A lesson exists with status = **Published** and **Student F1** assigned (Student F2 is NOT assigned to this lesson)
- Push notifications enabled for both accounts on Device 1

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Navigate to the SF Lesson Detail page of the Published lesson (assigned to Student F1) | Lesson Detail page opens; status = "Published" | Lesson ID — assigned to Student F1 only |
| 2   | Click "Publish and notify student", then click "Send" | Modal closes | "" |
| 3   | On Device 1, check the notification inbox while **Student F1** is the active account | Student F1's account **receives** a push notification with title "Lesson Published" | Device 1 — Student F1 account active |
| 4   | Switch to Student F2's account on Device 1 and check the notification inbox | Student F2's account does **not** receive a push notification for this lesson | Device 1 — Student F2 account |

**Severity:** major
**Priority:** high

---

### Notification Recipients – Student and Parent Switch Account Same Device – Notification delivered only to the account matching the recipient role

**Description:** Gap — Decision Table — When a student account and a parent account are both logged into the same device via the switch account feature, the "Lesson Published" notification is delivered correctly to each account by role (student's token and parent's token) and does not bleed to unrelated accounts on the device.

> ⚠️ **Note:** Expected behavior to be confirmed with product team after test execution.

**Preconditions:**
- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- Device 1 has both **Student A's Learner App account** and **Parent A's Parent App account** logged in via switch account
- Currently active account on Device 1: Student A
- A lesson exists with status = **Published** with Student A assigned; Parent A is linked to Student A via a Relationship record
- Push notifications enabled for both accounts on Device 1

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | Navigate to the SF Lesson Detail page of the Published lesson | Lesson Detail page opens; status = "Published" | Lesson ID — assigned to Student A |
| 2   | Click "Publish and notify student", then click "Send" | Modal closes | "" |
| 3   | On Device 1, check the notification inbox while **Student A** is the active account | Student A's Learner App account **receives** a push notification with title "Lesson Published" | Device 1 — Student A active |
| 4   | Switch to Parent A's account on Device 1 and check the notification inbox | Parent A's Parent App account **also receives** a push notification with title "Lesson Published" for the same lesson | Device 1 — Parent A account |
| 5   | Confirm notifications are scoped to the correct role; no notification appears on an unrelated third account if present on the device | Each notification is scoped to the correct account; no unexpected notification on unrelated accounts | "" |

**Severity:** major
**Priority:** high

---
