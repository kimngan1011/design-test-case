# Test Cases: LT-98532 — Bulk Publish Lessons by Student

## Suite: [Riso] Bulk Publish by Student – Notification Recipients

---

### [Riso] Bulk Publish Notification Recipients – Student in Multiple Lesson Schedules in One Batch – Receives Exactly 1 Notification

**Description:** AC 02.1 — Decision Table — When a student is allocated to multiple lesson schedules published in a single Bulk Publish batch, the student receives exactly 1 push notification (deduplicated), not one per lesson schedule.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- The period contains 3 Draft Lesson Schedules (LS-1, LS-2, LS-3), all assigned to Student A
- Student A is linked to Parent A
- Both Student A's Learner App and Parent A's Parent App are logged in with push notifications enabled
- Bulk Publish modal submitted for the period with Student A in the filter and checkbox activated

| #   | Action                                                          | Expected Result                                                                       | Test Data             |
| --- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------- | --------------------- |
| 1   | Submit the Bulk Publish request for the period                  | Success message appears; user redirected to Calendar                                  | ""                    |
| 2   | Wait for the job to complete; click Refresh                     | LS-1, LS-2, and LS-3 are all **"Published"**                                          | ""                    |
| 3   | On Student A's device, check the Learner App notification inbox | Student A has received **exactly 1** push notification — not 3 separate notifications | Student A Learner App |
| 4   | On Parent A's device, check the Parent App notification inbox   | Parent A has received **exactly 1** push notification for Student A                   | Parent A Parent App   |

**Severity:** critical
**Priority:** high

---

### [Riso] Bulk Publish Notification Recipients – Student with 2 Parents – Both Parents Receive Notification

**Description:** AC 02.1 — Decision Table — When a student is linked to 2 parent contacts, both parents receive a push notification after the Bulk Publish job completes.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- Student A is linked to Parent A and Parent B (two separate Parent Contact records)
- A Draft lesson for Student A exists in the period
- Both Parent A's and Parent B's Parent Apps are logged in with push notifications enabled
- Bulk Publish submitted with Student A in the filter and checkbox activated

| #   | Action                                                                    | Expected Result                                                    | Test Data           |
| --- | ------------------------------------------------------------------------- | ------------------------------------------------------------------ | ------------------- |
| 1   | Submit the Bulk Publish request                                           | Success message appears                                            | ""                  |
| 2   | Wait for job completion; confirm Lesson status is "Published" via Refresh | Lesson is Published                                                | ""                  |
| 3   | On Parent A's device, check the Parent App notification inbox             | Parent A **receives** a push notification for the published period | Parent A Parent App |
| 4   | On Parent B's device, check the Parent App notification inbox             | Parent B **receives** a push notification for the published period | Parent B Parent App |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Publish Notification Recipients – Two Students Share the Same Parent – Parent Receives Exactly 1 Notification

**Description:** AC 02.1 — Decision Table — When a single parent is linked to two students who are both published in the same Bulk Publish batch, the parent receives exactly 1 notification (not 2).

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- Parent A is linked to both Student A and Student B as a parent contact
- The period contains:
  - Lesson A (Draft) assigned to Student A
  - Lesson B (Draft) assigned to Student B
- Both students are selected in the Calendar student filter
- Parent A's Parent App is logged in with push notifications enabled

| #   | Action                                                                     | Expected Result                                                             | Test Data           |
| --- | -------------------------------------------------------------------------- | --------------------------------------------------------------------------- | ------------------- |
| 1   | Submit the Bulk Publish request with Student A and Student B in the filter | Success message appears                                                     | ""                  |
| 2   | Wait for job completion; confirm both lessons are Published via Refresh    | Lesson A and Lesson B are both **"Published"**                              | ""                  |
| 3   | On Parent A's device, check the Parent App notification inbox              | Parent A has received **exactly 1** push notification — not 2 separate ones | Parent A Parent App |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Publish Notification Recipients – Student with No Linked Parent – Student Skipped Entirely (No Notification Sent)

**Description:** AC 02.1 — Decision Table + Negative Testing — When a student has no linked Parent Contact (0 Relationship records), that student is skipped entirely and receives no push notification. Their linked lessons do not trigger any notification.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- Student A has **no linked Parent Contact** (0 Relationship records for Student A)
- A Draft lesson for Student A exists in the period
- Student A is selected in the Calendar student filter
- Student A's Learner App is logged in with push notifications enabled

| #   | Action                                                                              | Expected Result                                                                                                    | Test Data             |
| --- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------- |
| 1   | Submit the Bulk Publish request with Student A in the filter and checkbox activated | Success message appears                                                                                            | ""                    |
| 2   | Wait for job completion; confirm lesson status via Refresh                          | Lesson may be Published (the publish step may succeed); the publish step and the notification step are independent | ""                    |
| 3   | On Student A's device, wait 60 seconds and check the Learner App notification inbox | Student A does **not** receive any push notification for this period                                               | Student A Learner App |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Publish Notification Recipients – Student Has No Device Token – Student Silently Skipped, Other Recipients Still Notified

**Description:** AC 02.1 — Negative Testing — When a student has no registered device token (app not installed or logged out), they are silently skipped for notification delivery. Other students and parents in the same batch still receive their notifications.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- The period contains:
  - Lesson A (Draft) for Student A — Student A has **no device token** (device not registered)
  - Lesson B (Draft) for Student B — Student B is logged in with push notifications enabled; Parent B is linked and logged in
- Both students are in the Calendar filter and checkbox is activated

| #   | Action                                                                             | Expected Result                                                       | Test Data             |
| --- | ---------------------------------------------------------------------------------- | --------------------------------------------------------------------- | --------------------- |
| 1   | Submit the Bulk Publish request                                                    | Success message appears                                               | ""                    |
| 2   | Wait for job completion; confirm both lessons Published via Refresh                | Lesson A and Lesson B are **"Published"**                             | ""                    |
| 3   | Check Student A's accounts — no notification received (expected — no device token) | No notification for Student A (expected behavior, no error in system) | Student A (no device) |
| 4   | On Student B's device, check the Learner App notification inbox                    | Student B **receives** a push notification                            | Student B Learner App |
| 5   | On Parent B's device, check the Parent App notification inbox                      | Parent B **receives** a push notification                             | Parent B Parent App   |

**Severity:** major
**Priority:** high

---
