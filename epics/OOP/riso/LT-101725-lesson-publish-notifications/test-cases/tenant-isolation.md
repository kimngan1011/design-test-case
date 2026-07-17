# Test Cases: LT-101725 — Riso Lesson Publish Notifications to Teachers

## Suite: [Riso] Tenant Isolation – Config Flag

### [Riso] Tenant Isolation – Riso org with config flag ON – Chatter post created on lesson publish

**Description:** AC-03, BR-27 — Permission Matrix — When the Lesson Publish Notification config flag is ON (Riso org), publishing a lesson creates a Chatter post as expected.

**Preconditions:**
- Riso Salesforce org with Lesson Publish Notification config flag = ON
- A Draft lesson with 1 Lesson Teacher "Tanaka Kenji" (working_status=Available, working_type=Full Time)
- Logged in as HQ or CM Staff to the Riso Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open a Draft lesson in the Riso SF org | Lesson status = Draft | config_flag=ON (Riso org) |
| 2 | Change the lesson status to Published | Status = Published | "" |
| 3 | Navigate to the Chatter section | Exactly 1 Chatter post created with "@Tanaka Kenji" @mention | Riso org with flag ON → Chatter post triggered |

**Severity:** critical
**Priority:** high

---

### [Riso] Tenant Isolation – Non-Riso org with config flag OFF – No Chatter post created on lesson publish

**Description:** AC-03, BR-27, F-10 — Permission Matrix negative — When the Lesson Publish Notification config flag is OFF (non-Riso org), publishing a lesson does NOT create a Chatter post or send any teacher notification.

**Preconditions:**
- A non-Riso Salesforce org (e.g., Renseikai or Nichibei) with Lesson Publish Notification config flag = OFF
- A Draft lesson with 1 Available Lesson Teacher assigned in that org
- Logged in as HQ or CM Staff to the non-Riso Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open a Draft lesson in the non-Riso SF org | Lesson status = Draft | config_flag=OFF (non-Riso org) |
| 2 | Note the Chatter section baseline (any pre-existing posts) | Baseline Chatter post count recorded | "" |
| 3 | Change the lesson status to Published | Status = Published | "" |
| 4 | Navigate to the Chatter section | Chatter post count is unchanged — NO new Chatter post created | config_flag=OFF → no Chatter post; non-Riso org must not be affected |

**Severity:** critical
**Priority:** high

---

### [Riso] Tenant Isolation – Non-Riso org bulk publish – No teacher email sent

**Description:** AC-03, BR-27, F-10 — Permission Matrix negative — Bulk publishing lessons in a non-Riso org with config flag = OFF does not trigger any teacher email notification.

**Preconditions:**
- A non-Riso Salesforce org with config flag = OFF
- Multiple Draft lessons available for bulk publish; 1 Available teacher assigned with a valid email address
- Logged in as HQ or CM Staff to the non-Riso Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Trigger Bulk Publish on Draft lessons in the non-Riso SF org | Bulk publish job runs | config_flag=OFF (non-Riso org) |
| 2 | Wait for the job to complete | Draft lessons transition to Published status | "" |
| 3 | Check the teacher's email inbox | NO teacher email received — config flag OFF prevents teacher email notification in non-Riso orgs | expected: no email; non-Riso org must not be affected by LT-101725 |

**Severity:** critical
**Priority:** high

---
