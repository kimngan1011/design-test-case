# Test Cases: LT-101725 — Riso Lesson Publish Notifications to Teachers

## Suite: [Riso] Bulk Publish – Teacher Email

### [Riso] Bulk Publish Email – SF Lesson List bulk publish – Available Full-Time teacher receives email

**Description:** AC-09, BR-16 — State Transition — Bulk publishing Draft lessons from SF Lesson List triggers one email to each Available Full-Time teacher.

**Preconditions:**
- Riso Salesforce org with Lesson Publish Notification config flag = ON
- 2 Draft lessons in SF Lesson List, both assigned to "Tanaka Kenji" (working_status=Available, working_type=Full Time)
- "Tanaka Kenji" has SF-registered email: tanaka@riso.jp
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate to SF Lesson List; select the 2 Draft lessons | 2 lessons selected | surface="SF Lesson List"; teacher="Tanaka Kenji" |
| 2 | Trigger Bulk Publish | Bulk publish job runs | "" |
| 3 | Wait for the bulk publish job to complete | All selected lessons transition to Published status | "" |
| 4 | Check the email inbox for tanaka@riso.jp | 1 email received from the SF system email address | teacher_email=tanaka@riso.jp |

**Severity:** critical
**Priority:** high

---

### [Riso] Bulk Publish Email – SF Lesson Calendar bulk publish – Available Part-Time teacher receives email

**Description:** AC-09, BR-16 — State Transition — Bulk publishing Draft lessons from SF Lesson Calendar triggers one email to each Available Part-Time teacher.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- SF Lesson Calendar view set to June 2026: calendar_start = 2026-06-01, calendar_end = 2026-06-30
- Multiple Draft lessons within the calendar view assigned to "Yamamoto Yuki" (working_status=Available, working_type=Part Time)
- "Yamamoto Yuki" has SF-registered email: yamamoto@riso.jp
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar for June 2026 | Calendar view shows Start Date = 2026-06-01, End Date = 2026-06-30 | calendar_start=2026-06-01; calendar_end=2026-06-30; surface="SF Lesson Calendar" |
| 2 | Trigger Bulk Publish from the calendar view | Bulk publish job runs | "" |
| 3 | Wait for the job to complete | Draft lessons within the calendar period transition to Published | "" |
| 4 | Check the email inbox for yamamoto@riso.jp | 1 email received | teacher_email=yamamoto@riso.jp; working_type=Part Time |

**Severity:** critical
**Priority:** high

---

### [Riso] Bulk Publish Email – BO Lesson Management bulk publish – Available teacher receives email

**Description:** AC-09, BR-16 — State Transition — Bulk publishing Draft lessons from the Back Office Lesson Management page triggers one email to each Available teacher.

**Preconditions:**
- Riso Back Office environment with config flag = ON
- Multiple Draft lessons in BO Lesson Management assigned to "Nakamura Hana" (working_status=Available, working_type=Full Time)
- "Nakamura Hana" has SF-registered email: nakamura@riso.jp
- Logged in as HQ Staff to the Back Office

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate to BO Lesson Management | Lesson list visible | surface="BO Lesson Management" |
| 2 | Select Draft lessons and trigger Bulk Publish | Bulk publish job runs | "" |
| 3 | Wait for the job to complete | Draft lessons transition to Published status | "" |
| 4 | Check the email inbox for nakamura@riso.jp | 1 email received from SF system email | teacher_email=nakamura@riso.jp |

**Severity:** critical
**Priority:** high

---

### [Riso] Bulk Publish Email – Teacher assigned to multiple lessons in batch – Receives exactly one email for the entire batch

**Description:** AC-10, BR-18 — CRUD — One teacher assigned to multiple lessons in the same bulk publish batch receives exactly 1 email (not one email per lesson).

**Preconditions:**
- Riso Salesforce org with config flag = ON
- 5 Draft lessons in SF Lesson List, ALL assigned to "Tanaka Kenji" (Available, Full Time)
- "Tanaka Kenji" has SF-registered email: tanaka@riso.jp
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Select all 5 Draft lessons in SF Lesson List | 5 lessons selected | lesson_count=5; all assigned to Tanaka Kenji |
| 2 | Trigger Bulk Publish | Bulk publish job runs | "" |
| 3 | Wait for the job to complete | All 5 lessons = Published | "" |
| 4 | Check the email inbox for tanaka@riso.jp | Exactly 1 email received (not 5 emails) | expected_email_count=1; actual_lesson_count=5 |

**Severity:** critical
**Priority:** high

---

### [Riso] Bulk Publish Email – Unavailable teacher assigned to lesson in batch – Does not receive email

**Description:** AC-09, BR-04 — Decision Table negative — A Lesson Teacher with working_status=Unavailable is excluded from bulk publish teacher email.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- 3 Draft lessons, each assigned to 2 teachers:
  - "Tanaka Kenji" (working_status=Available, Full Time) — email: tanaka@riso.jp
  - "Sato Hiroshi" (working_status=Unavailable, Full Time) — email: sato@riso.jp
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Bulk publish the 3 Draft lessons from SF Lesson List | All 3 lessons transition to Published status | Teacher A=Available; Teacher B=Unavailable |
| 2 | Check email inbox for tanaka@riso.jp | 1 email received for "Tanaka Kenji" (Available → included) | working_status=Available → receives email |
| 3 | Check email inbox for sato@riso.jp | NO email received for "Sato Hiroshi" (Unavailable → excluded) | working_status=Unavailable → excluded from email |

**Severity:** critical
**Priority:** high

---

### [Riso] Bulk Publish Email – Email content – English subject and body – All required fields rendered

**Description:** AC-09, BR-17, BR-19, BR-21 — Component — The EN email received by the teacher contains the correct subject line, greeting, body text, and period in the correct format.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- today = 2026-06-23; SF Lesson List bulk publish of lessons dated 2026-06-05 to 2026-06-25
- 1 Available teacher "Tanaka Kenji" (Full Time); SF-registered email: tanaka@riso.jp
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Bulk publish lessons (SF Lesson List) dated 2026-06-05 through 2026-06-25 | Lessons = Published | today=2026-06-23; earliest_lesson_date=2026-06-05; latest_lesson_date=2026-06-25 |
| 2 | Open the email received by tanaka@riso.jp | Email opens | "" |
| 3 | Read the email subject line | Subject = "Lesson Schedule Published" | expected EN subject per BR-17 |
| 4 | Read the email greeting | Greeting = "Hi Tanaka Kenji," | teacher_name="Tanaka Kenji" |
| 5 | Read the email body text | Body contains "Lesson schedules for the following period have been published:" | expected EN body per BR-19 |
| 6 | Read the duration line | Duration = "Duration: June 5, 2026 ~ June 25, 2026" | earliest=2026-06-05; latest=2026-06-25; EN date format per BR-21 |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Publish Email – Email content – Japanese subject and body – All required fields rendered

**Description:** AC-09, BR-20, BR-22 — Component — The JP email received by the teacher contains the correct Japanese subject line, greeting, body text, and period in Japanese date format.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- today = 2026-06-23; SF Lesson List bulk publish of lessons dated 2026-06-05 to 2026-06-25
- 1 Available teacher "田中健二" (Full Time); SF-registered email: tanaka@riso.jp
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Bulk publish lessons (SF Lesson List) dated 2026-06-05 through 2026-06-25 | Lessons = Published | today=2026-06-23; earliest=2026-06-05; latest=2026-06-25 |
| 2 | Open the email received by tanaka@riso.jp | Email opens | "" |
| 3 | Read the email subject line | Subject = "授業予定が公開されました" | expected JP subject per BR-20 |
| 4 | Read the email greeting | Greeting = "田中健二様," | teacher_name="田中健二" |
| 5 | Read the email body text | Body contains "下記の期間の授業が公開されました。" | expected JP body per BR-20 |
| 6 | Read the duration line | Duration = "2026年6月5日～2026年6月25日" | earliest=2026-06-05; latest=2026-06-25; JP date format per BR-22 |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Publish Email – SF Lesson Calendar bulk publish period – Email shows calendar view Start and End Date

**Description:** AC-09, BR-23 — Decision Table — When triggered from SF Lesson Calendar, the email period shows the calendar view Start Date and End Date, not the earliest/latest lesson date in the batch.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- SF Lesson Calendar view set to June 2026: calendar_start = 2026-06-01, calendar_end = 2026-06-30
- Only 2 lessons within the view, dated 2026-06-10 and 2026-06-20 (batch min/max differ from calendar view dates)
- 1 Available teacher "Tanaka Kenji"; email: tanaka@riso.jp
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar for June 2026 | Calendar view Start = 2026-06-01, End = 2026-06-30 | calendar_start=2026-06-01; calendar_end=2026-06-30; lesson_dates=2026-06-10, 2026-06-20 |
| 2 | Trigger Bulk Publish from calendar view | Bulk publish runs | surface="SF Lesson Calendar" |
| 3 | Open the email received by tanaka@riso.jp | Email opens | "" |
| 4 | Read the duration in the email | Duration shows "June 1, 2026 ~ June 30, 2026" — the calendar view Start/End Date, NOT the batch min/max (June 10 ~ June 20) | expected: calendar dates (2026-06-01 ~ 2026-06-30); NOT batch min/max (2026-06-10 ~ 2026-06-20) |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Publish Email – SF Lesson List bulk publish period – Email shows earliest and latest lesson date in the batch

**Description:** AC-09, BR-24 — Decision Table — When triggered from SF Lesson List, the email period shows the earliest and latest lesson date across the batch, not a calendar view date.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- SF Lesson List with 3 selected Draft lessons: lesson dates = 2026-06-05, 2026-06-15, 2026-06-25
- 1 Available teacher "Yamamoto Yuki"; email: yamamoto@riso.jp
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Select 3 Draft lessons (dates: 2026-06-05, 2026-06-15, 2026-06-25) in SF Lesson List | 3 lessons selected | lesson_dates=[2026-06-05, 2026-06-15, 2026-06-25]; earliest=2026-06-05; latest=2026-06-25 |
| 2 | Trigger Bulk Publish | Bulk publish runs | surface="SF Lesson List" |
| 3 | Open the email received by yamamoto@riso.jp | Email opens | "" |
| 4 | Read the duration in the email | Duration shows "June 5, 2026 ~ June 25, 2026" (earliest and latest lesson date in the batch) | expected: June 5, 2026 ~ June 25, 2026 |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Publish Email – Single-day bulk publish batch – Email period shows same date as both start and end

**Description:** AC-09, BR-24 — BVA — Boundary case: when all lessons in the bulk publish batch are on the same date, the email period start and end are identical.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- SF Lesson List with 2 Draft lessons, both dated 2026-06-15
- 1 Available teacher "Nakamura Hana"; email: nakamura@riso.jp
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Select 2 Draft lessons (both dated 2026-06-15) in SF Lesson List | 2 lessons selected | lesson_dates=[2026-06-15, 2026-06-15]; earliest=2026-06-15; latest=2026-06-15 |
| 2 | Trigger Bulk Publish | Bulk publish runs | "" |
| 3 | Open the email received by nakamura@riso.jp | Email opens | "" |
| 4 | Read the duration in the email | Duration shows "June 15, 2026 ~ June 15, 2026" (same date for both start and end — single-day boundary) | expected: same date repeated; BVA edge case |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Publish Email – All lessons in batch already Published – No email sent and no error shown to user

**Description:** AC-09, BR-28, F-13 — Decision Table negative — When all lessons in the bulk publish batch are already Published (0 Draft → Published transitions), no email is sent and no error is shown.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- SF Lesson List with 3 lessons ALL in Published status (no Draft lessons)
- 1 teacher "Tanaka Kenji"; email: tanaka@riso.jp
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Select 3 Published lessons in SF Lesson List | All 3 lessons already in Published status | all_lessons_status=Published; zero_draft_transitions=true |
| 2 | Trigger Bulk Publish | Bulk publish action runs | "" |
| 3 | Wait for the bulk publish job to complete | No error message or warning is shown to the staff user — silent completion | "" |
| 4 | Check the email inbox for tanaka@riso.jp | NO email received — silent skip (0 Draft → Published transitions means no notification triggered) | expected: no email; silent skip per BR-28 |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Publish Email – Email delivery failure – Lessons remain Published and failure is logged for debugging

**Description:** AC-11, BR-25 — Negative — An email send failure does not block or roll back lesson publication. The lesson stays Published and the failure is logged.

**Preconditions:**
- Riso Salesforce org with config flag = ON
- Draft lessons available for bulk publish
- 1 Available teacher "Tanaka Kenji" with email configured to an invalid address (simulates send failure)
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Configure "Tanaka Kenji"'s SF registered email to an invalid address | Email configured to invalid address | teacher_email=invalid@nonexistent-domain-xyz.xyz (simulates delivery failure) |
| 2 | Trigger Bulk Publish on the Draft lessons | Bulk publish job runs | "" |
| 3 | Wait for the job to complete | Job completes | "" |
| 4 | Check the status of each lesson in the batch | ALL lessons are in Published status — publication was NOT rolled back by the email failure | expected: lessons = Published regardless of email failure |
| 5 | Check the SF system debug log for email failure | A failure log entry is visible for the email send attempt | expected: failure logged; lesson publish NOT blocked |

**Severity:** critical
**Priority:** high

---

### [Riso] Bulk Publish Email – LT-98532 student push notification – Fires independently when teacher email also triggered

**Description:** AC-09, F-09 — Regression — LT-98532 student push notification and LT-101725 teacher email both fire on the same bulk publish event without interfering with each other.

**Preconditions:**
- Riso Salesforce org with config flag = ON for both LT-101725 (teacher email) and LT-98532 (student push) configurations
- 2 Draft lessons, each assigned to:
  - 1 Available teacher "Tanaka Kenji" (LT-101725 teacher email recipient); email: tanaka@riso.jp
  - 1 student with a parent contact having a mobile device registered (LT-98532 student push recipient)
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Trigger Bulk Publish on the 2 Draft lessons from SF Lesson Calendar | Bulk publish job runs | both LT-98532 and LT-101725 active; surface="SF Lesson Calendar" |
| 2 | Wait for the job to complete | All lessons = Published | "" |
| 3 | Check email inbox for tanaka@riso.jp (teacher email — LT-101725) | Teacher "Tanaka Kenji" receives 1 bulk publish email with correct period | LT-101725 teacher email path |
| 4 | Check the student/parent Mobile app notification inbox (LT-98532) | Student and parent receive push notification for the same bulk publish | LT-98532 student push path |
| 5 | Confirm no cross-interference | Both teacher email (LT-101725) AND student push notification (LT-98532) delivered independently — neither blocked the other | expected: both systems fire independently; no shared failure mode |

**Severity:** critical
**Priority:** high

---
