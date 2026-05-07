# Test Cases: LT-96662 — Publish and Notify Student

## Suite: Publish and Notify Student – Send Notification

### Publish and Notify – Draft Lesson – Button Clicked – Lesson published and confirmation modal shown

**Description:** AC 02.1 — State Transition Testing — Clicking "Publish and notify student" on a Draft lesson publishes the lesson and immediately shows the confirmation modal.

**Preconditions:**

- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- A lesson exists with status = **Draft**, with at least one student assigned
- User is logged into SF with lesson publish permission

| #   | Action                                                    | Expected Result                                                                                                                                                          | Test Data       |
| --- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------- |
| 1   | Navigate to the SF Lesson Detail page of the Draft lesson | Lesson Detail page opens; status label shows "Draft"                                                                                                                     | Draft lesson ID |
| 2   | Click the "Publish and notify student" button             | Button click is registered                                                                                                                                               | ""              |
| 3   | Observe the lesson status immediately after click         | Lesson status changes to **Published**                                                                                                                                   | ""              |
| 4   | Observe the modal dialog that appears                     | Confirmation modal is displayed with title "Send Notification" and message "Would you like to send notifications about the publishing lesson to all allocated students?" | ""              |
| 5   | Observe the modal action buttons                          | Modal contains two buttons: "Send" and "Don't Send"                                                                                                                      | ""              |

**Severity:** critical
**Priority:** high

---

### Publish and Notify – Published Lesson – Button Clicked – Lesson status unchanged and confirmation modal shown

**Description:** AC 02.1 — State Transition Testing — Clicking "Publish and notify student" on a Published lesson does not change its status but shows the confirmation modal.

**Preconditions:**

- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- A lesson exists with status = **Published**, with at least one student assigned
- User is logged into SF with lesson publish permission

| #   | Action                                                                             | Expected Result                                                                                                                                                          | Test Data           |
| --- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------- |
| 1   | Navigate to the SF Lesson Detail page of the Published lesson; note current status | Lesson Detail page opens; status label shows "Published"                                                                                                                 | Published lesson ID |
| 2   | Click the "Publish and notify student" button                                      | Button click is registered                                                                                                                                               | ""                  |
| 3   | Observe the lesson status immediately after click                                  | Lesson status remains **Published** (no change)                                                                                                                          | ""                  |
| 4   | Observe the modal dialog that appears                                              | Confirmation modal is displayed with title "Send Notification" and message "Would you like to send notifications about the publishing lesson to all allocated students?" | ""                  |
| 5   | Observe the modal action buttons                                                   | Modal contains two buttons: "Send" and "Don't Send"                                                                                                                      | ""                  |

**Severity:** major
**Priority:** high

---

### Publish and Notify – Confirmation Modal – All content elements displayed as designed

**Description:** AC 02.2 — Equivalence Partitioning — The confirmation modal displays the correct title, message, and action buttons in both EN and JP.

**Preconditions:**

- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- User is on the SF Lesson Detail page (Published lesson)
- User has clicked "Publish and notify student" and the modal is open

| #   | Action                                                                                 | Expected Result                                                                                                                                                             | Test Data           |
| --- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- |
| 1   | Navigate to SF Lesson Detail (Published lesson) and click "Publish and notify student" | Confirmation modal appears                                                                                                                                                  | Published lesson ID |
| 2   | Observe the modal title                                                                | Modal title displays "Send Notification" (JP: "おしらせ配信")                                                                                                               | ""                  |
| 3   | Observe the modal message body                                                         | Message reads: "Would you like to send notifications about the publishing lesson to all allocated students?" (JP: "授業に参加する生徒へ授業公開のおしらせを配信しますか？") | ""                  |
| 4   | Observe the primary action button                                                      | Button labeled "Send" (JP: "今すぐ送る") is present                                                                                                                         | ""                  |
| 5   | Observe the secondary action button                                                    | Button labeled "Don't Send" (JP: "送らない") is present                                                                                                                     | ""                  |

**Severity:** major
**Priority:** high

---

### Publish and Notify – Published Lesson – Send Clicked – Notification delivered to assigned student and linked parents

**Description:** AC 02.1 + AC 02.2 — Decision Table — Clicking "Send" on the confirmation modal triggers real-time push notification delivery to the student and all linked parents.

**Preconditions:**

- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- A lesson exists with status = **Published**; lesson name: "English Level 3 – Session 1"; lesson date: 2026-04-20; start time: 10:00; end time: 11:00
- Student A is assigned to the lesson and is logged into the Learner App on a test device
- Parent A is linked to Student A via a Relationship record and is logged into the Parent App on a test device
- Both devices have push notifications enabled

| #   | Action                                                                            | Expected Result                                                                                                                                                                                                                      | Test Data                                       |
| --- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------- |
| 1   | Navigate to the SF Lesson Detail page of the Published lesson                     | Lesson Detail page opens; status = "Published"                                                                                                                                                                                       | Published lesson: "English Level 3 – Session 1" |
| 2   | Click "Publish and notify student"                                                | Confirmation modal appears                                                                                                                                                                                                           | ""                                              |
| 3   | Click "Send" in the modal                                                         | Modal closes                                                                                                                                                                                                                         | ""                                              |
| 4   | On Student A's test device, open the Learner App and check the notification inbox | A push notification is received with title "Lesson Published" and body "The schedule for English Level 3 – Session 1 has been published. Lesson Date: 2026-04-20 \| 10:00 - 11:00. Tap the button below to view the lesson details." | Student A Learner App account                   |
| 5   | On Parent A's test device, open the Parent App and check the notification inbox   | A push notification is received with title "Lesson Published" and body "The schedule for English Level 3 – Session 1 has been published. Lesson Date: 2026-04-20 \| 10:00 - 11:00. Tap the button below to view the lesson details." | Parent A Parent App account                     |

**Severity:** critical
**Priority:** high

---

### Publish and Notify – Draft Lesson – Send Clicked – Lesson published and notification delivered to student and parents

**Description:** AC 02.1 + AC 02.2 — State Transition Testing + Decision Table — Clicking "Send" on a Draft lesson publishes the lesson and triggers push notification delivery to the student and all linked parents.

**Preconditions:**

- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- A lesson exists with status = **Draft**; lesson name: "Math Level 2 – Session 5"; lesson date: 2026-04-21; start time: 14:00; end time: 15:00
- Student B is assigned to the lesson and is logged into the Learner App on a test device
- Parent B is linked to Student B via a Relationship record and is logged into the Parent App on a test device
- Both devices have push notifications enabled

| #   | Action                                                               | Expected Result                                                                                                                                              | Test Data                                |
| --- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------- |
| 1   | Navigate to the SF Lesson Detail page of the Draft lesson            | Lesson Detail page opens; status = "Draft"                                                                                                                   | Draft lesson: "Math Level 2 – Session 5" |
| 2   | Click "Publish and notify student"                                   | Lesson status changes to Published; confirmation modal appears                                                                                               | ""                                       |
| 3   | Confirm lesson status in the modal is now Published                  | Lesson is in Published state before modal interaction                                                                                                        | ""                                       |
| 4   | Click "Send" in the modal                                            | Modal closes                                                                                                                                                 | ""                                       |
| 5   | Observe the lesson status on the detail page                         | Lesson status shows "Published"                                                                                                                              | ""                                       |
| 6   | On Student B's test device, check the Learner App notification inbox | Push notification received with title "Lesson Published" and body containing lesson name "Math Level 2 – Session 5", date 2026-04-21, and time 14:00 - 15:00 | Student B Learner App account            |
| 7   | On Parent B's test device, check the Parent App notification inbox   | Push notification received with title "Lesson Published" containing same lesson details                                                                      | Parent B Parent App account              |

**Severity:** critical
**Priority:** high

---

### Publish and Notify – Published Lesson – Don't Send Clicked – No notification sent to student or parents

**Description:** AC 02.2 — Decision Table + Negative Testing — Clicking "Don't Send" in the confirmation modal dismisses it without sending any push notification.

**Preconditions:**

- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- A lesson exists with status = **Published** with Student A assigned
- Student A and Parent A have devices logged into the app with notifications enabled
- No pending notifications for this lesson on either device

| #   | Action                                                                 | Expected Result                                     | Test Data           |
| --- | ---------------------------------------------------------------------- | --------------------------------------------------- | ------------------- |
| 1   | Navigate to the SF Lesson Detail page of the Published lesson          | Lesson Detail page opens; status = "Published"      | Published lesson ID |
| 2   | Click "Publish and notify student"                                     | Confirmation modal appears                          | ""                  |
| 3   | Click "Don't Send" in the modal                                        | Modal closes; no loading or sending indicator shown | ""                  |
| 4   | Wait 30 seconds, then check Student A's Learner App notification inbox | No new notification received for this lesson        | ""                  |
| 5   | Check Parent A's Parent App notification inbox                         | No new notification received for this lesson        | ""                  |

**Severity:** major
**Priority:** high

---

### Publish and Notify – Draft Lesson – Don't Send Clicked – Lesson status remains Published after modal dismissed

**Description:** AC 02.2 + Gap #6 — State Transition Testing — When "Don't Send" is selected after clicking the button on a Draft lesson, the lesson remains Published (status is NOT reverted to Draft).

> ⚠️ **Note:** Expected behavior (lesson stays Published) is to be confirmed with product team. Create this test case, run it, and share the result for confirmation.

**Preconditions:**

- User is logged into SF with the "Publish Lesson With Notification" custom permission (member of the Renseikai OOP Permission Set)
- A lesson exists with status = **Draft** with an assigned student
- User is logged into SF with lesson publish permission

| #   | Action                                                    | Expected Result                                                | Test Data       |
| --- | --------------------------------------------------------- | -------------------------------------------------------------- | --------------- |
| 1   | Navigate to the SF Lesson Detail page of the Draft lesson | Lesson Detail page opens; status = "Draft"                     | Draft lesson ID |
| 2   | Click "Publish and notify student"                        | Lesson status changes to Published; confirmation modal appears | ""              |
| 3   | Click "Don't Send" in the modal                           | Modal closes                                                   | ""              |
| 4   | Observe the lesson status on the detail page              | Lesson status remains **Published** (not reverted to Draft)    | ""              |
| 5   | Navigate away and return to the lesson detail page        | Lesson status persists as "Published"                          | ""              |

**Severity:** major
**Priority:** high

---
