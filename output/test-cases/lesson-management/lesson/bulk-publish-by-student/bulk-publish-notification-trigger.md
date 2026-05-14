# Test Cases: LT-98532 — Bulk Publish Lessons by Student

## Suite: [Riso] Bulk Publish by Student – Notification Trigger

---

### [Riso] Bulk Publish Notification – All Lessons Published Successfully – Notification Sent to All Affected Students and Parents

**Description:** AC 02.1 — State Transition Testing — When the Bulk Publish job completes with full success (all Draft lessons published, no failures), push notifications are sent to all affected students and their linked parents.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- The period contains 2 Draft lessons: Lesson A (Student A) and Lesson B (Student B)
- Student A is linked to Parent A; Student B is linked to Parent B
- All 4 devices (Student A's Learner App, Student B's Learner App, Parent A's Parent App, Parent B's Parent App) are logged in with push notifications enabled
- Bulk Publish modal submitted with "Apply to selected students" activated for Student A and Student B

| #   | Action                                                                  | Expected Result                                          | Test Data             |
| --- | ----------------------------------------------------------------------- | -------------------------------------------------------- | --------------------- |
| 1   | Submit the Bulk Publish request                                         | Success message appears; user redirected to Calendar     | ""                    |
| 2   | Wait for the async job to complete (click Refresh to confirm published) | Calendar shows Lesson A and Lesson B as **"Published"**  | ""                    |
| 3   | On Student A's device, check the Learner App notification inbox         | A push notification is received for the published period | Student A Learner App |
| 4   | On Parent A's device, check the Parent App notification inbox           | A push notification is received for the published period | Parent A Parent App   |
| 5   | On Student B's device, check the Learner App notification inbox         | A push notification is received for the published period | Student B Learner App |
| 6   | On Parent B's device, check the Parent App notification inbox           | A push notification is received for the published period | Parent B Parent App   |

**Severity:** critical
**Priority:** high

---

### [Riso] Bulk Publish Notification – Partial Failure (Completed with Errors) – Notification Sent Only for Successfully Published Students

**Description:** AC 02.1 — Decision Table — When the Bulk Publish job completes with some failures ("Completed with Errors"), notifications are sent only for students whose lessons were successfully published. Students with failed lessons do not receive a notification.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- The period contains 2 Draft lessons:
  - Lesson A (Student A) — will be published successfully
  - Lesson B (Student B) — will fail to publish (simulated via backend/test environment tooling)
- Student A is linked to Parent A; Student B is linked to Parent B
- All 4 devices are logged in with push notifications enabled

| #   | Action                                                          | Expected Result                                                               | Test Data             |
| --- | --------------------------------------------------------------- | ----------------------------------------------------------------------------- | --------------------- |
| 1   | Submit the Bulk Publish request                                 | Success message appears; user redirected to Calendar                          | ""                    |
| 2   | Wait for the job to complete; check Bulk Action Monitoring      | Job Status shows **"Completed with Errors"**; Success = 1, Failed = 1         | ""                    |
| 3   | On Student A's device, check the Learner App notification inbox | Student A **receives** a push notification for the published period           | Student A Learner App |
| 4   | On Parent A's device, check the Parent App notification inbox   | Parent A **receives** a push notification for the published period            | Parent A Parent App   |
| 5   | On Student B's device, check the Learner App notification inbox | Student B does **not** receive a push notification (lesson failed to publish) | Student B Learner App |
| 6   | On Parent B's device, check the Parent App notification inbox   | Parent B does **not** receive a push notification                             | Parent B Parent App   |

**Severity:** critical
**Priority:** high

---

### [Riso] Bulk Publish Notification – All Lessons Already Published – No Notification Sent

**Description:** AC 02.1 — Decision Table + Negative Testing — When the Bulk Publish job is submitted but all lessons in scope are already Published, Completed, or Cancelled (0 Draft lessons), the job skips silently and no push notification is sent.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- The period contains 2 lessons for the selected student, both with status **"Published"** (no Draft lessons)
- Student A is linked to Parent A; both devices have push notifications enabled
- Bulk Publish modal submitted with "Apply to selected students" activated for Student A

| #   | Action                                                                              | Expected Result                                                                  | Test Data             |
| --- | ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | --------------------- |
| 1   | Submit the Bulk Publish request                                                     | Success message appears; user redirected to Calendar                             | ""                    |
| 2   | Wait for the job to complete; check the Calendar after Refresh                      | Lesson statuses remain **"Published"** — no change (no Draft lessons to process) | ""                    |
| 3   | On Student A's device, wait 60 seconds and check the Learner App notification inbox | No new push notification is received for this period                             | Student A Learner App |
| 4   | On Parent A's device, check the Parent App notification inbox                       | No new push notification is received                                             | Parent A Parent App   |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Publish Notification – Cross-Type Dedup – Lesson Already Notified via Individual "Publish and Notify" Is Excluded from Bulk Notification

**Description:** AC 02.1 — Regression Analysis + Decision Table — If a lesson was already published and notified via the individual "Publish and Notify Student" button (LT-96662), it is excluded from the bulk notification batch; the student and parent do not receive a duplicate notification for that lesson.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- The calendar period contains:
  - Lesson A: already published and already notified via the individual "Publish and Notify Student" button (LT-96662 feature)
  - Lesson B: Draft, has NOT been individually notified
- Student A is assigned to both Lesson A and Lesson B; Student A is linked to Parent A
- Both Student A's and Parent A's devices are logged in with push notifications enabled
- Bulk Publish modal submitted for the period with Student A in the filter and checkbox activated

| #   | Action                                                                                       | Expected Result                                                                                                                              | Test Data             |
| --- | -------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| 1   | Use the individual "Publish and Notify Student" button on Lesson A to publish and notify     | Lesson A is Published; Student A and Parent A receive notification via the individual flow                                                   | Lesson A              |
| 2   | Submit the Bulk Publish request for the same period (Lesson A + Lesson B in scope)           | Success message appears                                                                                                                      | ""                    |
| 3   | Wait for the Bulk Publish job to complete                                                    | Bulk job processes the period                                                                                                                | ""                    |
| 4   | On Student A's device, check the Learner App notification inbox after the Bulk job completes | Student A receives **exactly 1 new notification** from the Bulk Publish job — for Lesson B only. **No duplicate notification for Lesson A.** | Student A Learner App |
| 5   | On Parent A's device, check the Parent App notification inbox                                | Parent A receives **exactly 1 new notification** from Bulk job — for Lesson B period. **No duplicate for Lesson A.**                         | Parent A Parent App   |
| 6   | Count total notifications for Lesson A on Student A's device                                 | Student A has received notification for Lesson A exactly **once** (from the individual flow, step 1)                                         | ""                    |

**Severity:** critical
**Priority:** high

---
