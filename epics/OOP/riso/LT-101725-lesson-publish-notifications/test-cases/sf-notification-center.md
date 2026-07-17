# Test Cases: LT-101725 — Riso Lesson Publish Notifications to Teachers

## Suite: [Riso] SF Notification Center

### [Riso] SF Notification Center – Available @mentioned teacher – Receives notification center alert after lesson published

**Description:** AC-06, BR-13 — State Transition — The teacher @mentioned in the Chatter post receives an SF notification center alert after lesson publish.

**Preconditions:**
- Riso Salesforce org with Lesson Publish Notification config flag = ON
- A Draft lesson "English Class A" with 1 Lesson Teacher: "Tanaka Kenji" (working_status=Available, working_type=Full Time)
- "Tanaka Kenji" has an active Salesforce user account
- Logged in as HQ or CM Staff to the Salesforce org to perform the publish action

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Publish the lesson "English Class A" from SF Lesson Detail (change status Draft → Published) | Status = Published; Chatter post created with "@Tanaka Kenji" | lesson_name="English Class A"; teacher="Tanaka Kenji" |
| 2 | Log out as Staff; log in to Salesforce as "Tanaka Kenji" | Logged in successfully as Tanaka Kenji | actor switches to Tanaka Kenji (teacher) |
| 3 | Open the SF Notification Center (bell icon) | Notification center panel opens | "" |
| 4 | Look for the lesson publish notification | A notification message appears referencing the Chatter post @mention for "English Class A" | expected: 1 notification for the Chatter @mention |

**Severity:** critical
**Priority:** high

---

### [Riso] SF Notification Center – HQ Admin with LBAC access – Can view Chatter post but receives no notification center alert

**Description:** AC-07, BR-14 — Permission Matrix — An HQ Admin with LBAC access to the lesson record can see the Chatter post but does NOT receive a notification center alert because they were not @mentioned.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- A published lesson with a Chatter post visible (1 Available teacher "@Tanaka Kenji" was @mentioned)
- HQ Admin user "Yamada Admin" has LBAC access to the lesson record but is NOT a Lesson Teacher
- Logged in to Salesforce as HQ Admin "Yamada Admin"

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the published lesson in SF Lesson Detail as HQ Admin "Yamada Admin" | Lesson Detail page opens | actor="Yamada Admin" (HQ Admin, LBAC access; not a Lesson Teacher) |
| 2 | Navigate to the Chatter section | Chatter section is visible; the Chatter post created on lesson publish is visible to "Yamada Admin" | LBAC access allows viewing Chatter posts |
| 3 | Open the SF Notification Center (bell icon) | Notification center panel opens | "" |
| 4 | Check for any notification related to this lesson's Chatter post | NO notification alert for "Yamada Admin" — notification center shows no lesson publish alert | HQ Admin was not @mentioned → no notification center alert |

**Severity:** critical
**Priority:** high

---

### [Riso] SF Notification Center – Centre Manager with LBAC access – Can view Chatter post but receives no notification center alert

**Description:** AC-07, BR-14 — Permission Matrix — A Centre Manager with LBAC access to the lesson record can see the Chatter post but does NOT receive a notification center alert.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- A published lesson with a Chatter post visible (1 Available teacher @mentioned)
- Centre Manager "Suzuki CM" has LBAC access to the lesson record but is NOT a Lesson Teacher
- Logged in to Salesforce as Centre Manager "Suzuki CM"

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the published lesson in SF Lesson Detail as "Suzuki CM" | Lesson Detail page opens | actor="Suzuki CM" (Centre Manager, LBAC access; not a Lesson Teacher) |
| 2 | Navigate to the Chatter section | Chatter section is visible; the lesson publish Chatter post is visible | LBAC access allows viewing Chatter posts |
| 3 | Open the SF Notification Center (bell icon) | Notification center panel opens | "" |
| 4 | Check for any notification for this lesson's Chatter post | NO notification alert — notification center shows no lesson publish alert for "Suzuki CM" | Centre Manager was not @mentioned → no notification center alert |

**Severity:** critical
**Priority:** high

---

### [Riso] SF Notification Center – Bulk publish lesson – Teacher does not receive SF notification center alert

**Description:** AC-06, BR-13 — Decision Table negative — Bulk publish triggers teacher email (not SF notification center). No Chatter post or notification center alert is created for bulk-published lessons.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- 3 Draft lessons in SF Lesson List, all assigned to "Tanaka Kenji" (working_status=Available, Full Time)
- "Tanaka Kenji" has an active Salesforce user account
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Bulk publish all 3 Draft lessons from SF Lesson List | All 3 lessons transition to Published status | bulk_publish=true; 3 lessons; teacher="Tanaka Kenji" |
| 2 | Log in to Salesforce as "Tanaka Kenji" | Logged in as Tanaka Kenji | "" |
| 3 | Open the SF Notification Center (bell icon) | Notification center panel opens | "" |
| 4 | Check for any lesson publish @mention notification | NO @mention notification alert in notification center | bulk publish triggers email, NOT SF notification center |
| 5 | Navigate to the Chatter section of each published lesson | No new Chatter posts created by bulk publish | Chatter posts are created only on single publish, not bulk publish |

**Severity:** major
**Priority:** high

---

### [Riso] SF Notification Center – Same lesson single-published then covered by bulk publish – No bulk email sent

**Description:** AC-05, AC-09, F-01 — Cross-type dedup resolved: Bulk publish only sends email when there are Draft → Published transitions. If a batch contains only already-published lessons, no email is sent.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- today = 2026-06-23; lesson_date = 2026-06-30
- A lesson "English Class A" (lesson_date = 2026-06-30) with 1 Available teacher "Tanaka Kenji"
- "Tanaka Kenji" has an active SF account and SF-registered email: tanaka@riso.jp
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Single-publish "English Class A" (change status Draft → Published individually) | Status = Published; Chatter post created with "@Tanaka Kenji"; teacher receives SF notification center alert | today=2026-06-23; lesson_date=2026-06-30 |
| 2 | Bulk-publish a period that includes "English Class A" (select the lesson in SF Lesson List, trigger bulk publish) | Bulk publish action completes; since the lesson was already Published, zero Draft -> Published transitions occur. | "" |
| 3 | Log in as "Tanaka Kenji"; open the SF Notification Center | Notification center shows ONLY the Chatter @mention alert from step 1 | "" |
| 4 | Check teacher email inbox at tanaka@riso.jp | NO bulk publish email is received for "English Class A" | "" |

**Severity:** critical
**Priority:** high

---

### [Riso] SF Notification Center – Teacher Added from SF Lesson Detail – Added teacher receives notification alert

**Description:** AC-01, BR-26, BR-13 — State Transition — A teacher added to a Published lesson via SF Lesson Detail gets @mentioned and receives a notification center alert.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- A lesson in Published status with a future date
- Teacher "Tanaka Kenji" exists in SF
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate to the SF Lesson Detail page of the published lesson | Lesson Detail page opens | lesson_status=Published |
| 2 | Add "Tanaka Kenji" as a Lesson Teacher | "Tanaka Kenji" is added | "" |
| 3 | Log out and log in as "Tanaka Kenji" | Logged in as Tanaka Kenji | "" |
| 4 | Open the SF Notification Center | A notification appears for the Chatter @mention | "" |

**Severity:** critical
**Priority:** high

---

### [Riso] SF Notification Center – Teacher Added from SF Calendar – Added teacher receives notification alert

**Description:** AC-01, BR-26, BR-13 — State Transition — A teacher added to a Published lesson via SF Calendar gets @mentioned and receives a notification center alert.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- A lesson in Published status with a future date
- Teacher "Yamamoto Yuki" exists in SF
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate to the SF Lesson Calendar | Calendar view is displayed | "" |
| 2 | Edit the Published lesson and add "Yamamoto Yuki" | "Yamamoto Yuki" is added | lesson_status=Published |
| 3 | Log out and log in as "Yamamoto Yuki" | Logged in as Yamamoto Yuki | "" |
| 4 | Open the SF Notification Center | A notification appears for the Chatter @mention | "" |

**Severity:** critical
**Priority:** high

---
