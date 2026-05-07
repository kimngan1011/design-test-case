# Test Cases: LT-96662 — Publish and Notify Student

## Suite: Publish and Notify Student – Deep-link Navigation

### Notification Deep-link – Logged-in Student – Tap notification opens correct Lesson Detail page in app

**Description:** AC 03.1 — Regression Analysis — When a logged-in student taps the push notification, the Learner App deep-links directly to the Lesson Detail page of the published lesson with up-to-date information.

**Preconditions:**
- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- A lesson exists with status = **Published**; lesson name: "English Level 3 – Session 1"; lesson date: 2026-04-20; start time: 10:00; end time: 11:00
- Student A is assigned to the lesson and is logged into the Learner App on Device 1 with push notifications enabled
- Student A has received the "Lesson Published" push notification for this lesson

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | On Device 1, locate the "Lesson Published" push notification for "English Level 3 – Session 1" in the notification tray | Push notification is visible with correct title and lesson name | Student A's device notification tray |
| 2   | Tap the push notification (or the CTA "view lesson details" button within it) | Learner App opens (if not already open) | "" |
| 3   | Observe the screen that loads | App navigates to the **Lesson Detail page** of "English Level 3 – Session 1" | "" |
| 4   | Observe the lesson details displayed on the page | Lesson name = "English Level 3 – Session 1"; lesson date = 2026-04-20; start time = 10:00; end time = 11:00; status = Published | "" |

**Severity:** major
**Priority:** high

---

### Notification Deep-link – Logged-in Parent – Tap notification opens correct Lesson Detail page in app

**Description:** AC 03.1 — Regression Analysis — When a logged-in parent taps the push notification, the Parent App deep-links directly to the correct Lesson Detail page.

**Preconditions:**
- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- A lesson exists with status = **Published**; lesson name: "English Level 3 – Session 1"; lesson date: 2026-04-20; start time: 10:00; end time: 11:00
- Student A is assigned to the lesson; Parent A is linked to Student A via a Relationship record and is logged into the Parent App on Device 2 with push notifications enabled
- Parent A has received the "Lesson Published" push notification for this lesson

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | On Device 2, locate the "Lesson Published" push notification in the notification tray | Push notification is visible with title "Lesson Published" and lesson name | Parent A's device notification tray |
| 2   | Tap the push notification | Parent App opens (if not already open) | "" |
| 3   | Observe the screen that loads | App navigates to the **Lesson Detail page** of "English Level 3 – Session 1" within Student A's context | "" |
| 4   | Observe the lesson details displayed | Lesson name = "English Level 3 – Session 1"; date = 2026-04-20; start time = 10:00; end time = 11:00; status = Published | "" |

**Severity:** major
**Priority:** high

---

### Notification Deep-link – User Not Logged In – Tap notification redirects to login then Lesson Detail page

**Description:** AC 03.1 + Gap #11 — Decision Table — When a user who is NOT currently logged into the app taps the push notification, they are taken to the login screen and then redirected to the Lesson Detail page after successful login.

> ⚠️ **Note:** Expected redirect behavior (login → lesson detail) is to be **confirmed with product team** after test execution. If behavior differs (e.g., app home), share the actual result.

**Preconditions:**
- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- A Published lesson with Student A assigned; "Lesson Published" notification has been sent to Student A
- Device 1 has the Learner App installed but Student A is **not currently logged in** (logged out state)
- The push notification is still present in Device 1's notification tray

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | On Device 1 (not logged in), locate the "Lesson Published" push notification in the notification tray | Push notification is visible | Student A's device (logged out) |
| 2   | Tap the push notification | Learner App opens to the **login screen** (session is not active) | "" |
| 3   | Log in with Student A's credentials | Login succeeds | Student A credentials |
| 4   | Observe the screen after successful login | App navigates to the **Lesson Detail page** of the notified lesson (not the app home screen) | "" |

**Severity:** normal
**Priority:** medium

---

### Notification Deep-link – Parent Viewing Different Student Context – Tap Student A notification shows Student A lesson detail

**Description:** AC 03.1 + Gap #10 — Decision Table — When a parent is currently viewing Student B in the app and receives and taps a notification for Student A's lesson, the app switches context to Student A and shows Student A's Lesson Detail page.

> ⚠️ **Note:** Expected switching behavior is to be **confirmed with product team** after test execution. If the app does NOT switch context, share the actual result so the team can define the expected behavior.

**Preconditions:**
- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- **Parent F** has two students: **Student A** and **Student B** via Relationship records
- A lesson for **Student A** has been published and "Lesson Published" notification sent to Parent F
- Parent F is logged into the Parent App on Device 1 and is currently **viewing Student B's context** (Student B selected as active student)

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | On Device 1, confirm the Parent App is open and Student B's context is currently active | Parent App shows Student B's information | Parent F account; Student B context active |
| 2   | Locate the "Lesson Published" push notification for **Student A's** lesson in the notification tray | Push notification is visible with Student A's lesson name | Student A's lesson notification |
| 3   | Tap the push notification | App responds to the tap | "" |
| 4   | Observe the active student context after navigation | App switches to **Student A's context** (Student A shown as active student) | "" |
| 5   | Observe the screen that loads | App navigates to the **Lesson Detail page** of Student A's published lesson — not Student B's lesson | Student A's lesson detail |

**Severity:** major
**Priority:** high

---
