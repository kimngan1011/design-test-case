# Test Cases: LT-61333 — Lesson Report Notification

## Suite: Scheduled Report Delivery

### [Renseikai] Lesson Report Notification – Daily Batch – Eligible Published Report – One notification per recipient
**Description:** REQ-01 — Decision Table — An eligible Published report is processed by the noon JST batch.
**Preconditions:**
- The scheduler time is 2026-10-12 12:00 JST.
- Report R-101 for Math A is Published with updated_at = 2026-10-11 13:00 JST.
- Student A and Default Parent A are logged in to their apps.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | System runs the daily report-notification batch. | System selects R-101 once. | run=2026-10-12 12:00 JST |
| 2 | Student A opens the notification inbox. | One notification for Math A is present. | recipient=Student A |
| 3 | Parent A opens the notification inbox. | One notification for Math A is present. | recipient=Default Parent A |
**Severity:** critical
**Priority:** high

### [Renseikai] Lesson Report Notification – Daily Batch – High-volume Delivery – 500 Students and Default Parents notified
**Description:** REQ-01 and REQ-02 — Scenario — A 1,000-report batch delivers every report to its Student and Default Parent without omissions or duplicates.
**Preconditions:**
- The scheduler time is 2026-10-12 12:00 JST.
- 1,000 Lesson Reports are Published with updated_at values between 2026-10-11 12:00 JST and 2026-10-12 11:59:59 JST.
- The 1,000 reports belong to 500 Students, with exactly two reports per Student.
- Each Student has one Default Parent identified by Relationship Default = true.
- All 500 Students and 500 Default Parents are logged in to their respective apps.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | System runs the daily report-notification batch. | System selects all 1,000 eligible reports once. | run=2026-10-12 12:00 JST; reports=1000; students=500 |
| 2 | System displays the batch delivery audit. | Audit records 2,000 completed recipient deliveries with no failed, omitted, or duplicate delivery. | 1000 reports × 2 recipients = 2000 |
| 3 | Each Student opens the notification inbox. | Every one of the 500 Students has exactly two notifications for their own reports. | Student notifications=1000; 2 per Student |
| 4 | Each Default Parent opens the notification inbox. | Every one of the 500 Default Parents has exactly two notifications for their linked Student's reports. | Parent notifications=1000; 2 per Default Parent |
**Severity:** critical
**Priority:** high

### [Renseikai] Lesson Report Notification – Daily Batch – Pre-window Report – No notification created
**Description:** REQ-01 — BVA Negative — A report updated before the prior noon boundary is excluded.
**Preconditions:**
- The scheduler time is 2026-10-12 12:00 JST.
- Report R-102 is Published with updated_at = 2026-10-11 11:59:59 JST.
- Student A and Default Parent A are logged in to their apps.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | System runs the daily report-notification batch. | System does not select R-102. | window_start=2026-10-11 12:00:00 JST |
| 2 | Student A opens the notification inbox. | No notification for R-102 is present. | report=Math B |
| 3 | Parent A opens the notification inbox. | No notification for R-102 is present. | report=Math B |
**Severity:** critical
**Priority:** high

### [Renseikai] Lesson Report Notification – Daily Batch – Noon Boundary – No duplicate or omission
**Description:** REQ-01 — BVA — A report at the 12:00 JST boundary belongs to exactly one non-overlapping batch.
**Preconditions:**
- Report R-103 is Published with updated_at = 2026-10-12 12:00:00 JST.
- Student A and Default Parent A are logged in to their apps.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | System runs the batch ending at 2026-10-12 12:00 JST. | Batch audit assigns R-103 to exactly one named batch run. | boundary=2026-10-12 12:00:00 JST |
| 2 | System runs the next daily batch. | Across both runs, R-103 has exactly one delivery decision. | next_run=2026-10-13 12:00 JST |
| 3 | Student A opens the notification inbox. | At most one notification for R-103 is present; it is not omitted by both runs. | report=Math C |
**Severity:** critical
**Priority:** high

### [Renseikai] Lesson Report Notification – Daily Batch – Non-published Report – No notification created
**Description:** REQ-01 — Decision Table Negative — Statuses other than Published are excluded.
**Preconditions:**
- The scheduler time is 2026-10-12 12:00 JST.
- Reports R-104 and R-105 are updated in the batch window with statuses Draft and Submitted.
- Student A is logged in to the Learner App.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | System runs the daily report-notification batch. | System selects neither R-104 nor R-105. | statuses=Draft,Submitted |
| 2 | Student A opens the notification inbox. | No notification for either report is present. | reports=Math D,Math E |
**Severity:** major
**Priority:** high

### [Renseikai] Lesson Report Notification – Daily Batch – Retry – One delivery retained
**Description:** REQ-01 — Regression — Retrying an eligible report delivery does not duplicate it.
**Preconditions:**
- The scheduler time is 2026-10-12 12:00 JST.
- Report R-106 is Published with updated_at = 2026-10-12 09:00 JST.
- A transient delivery failure can be simulated after the first send attempt.
- Student A is logged in to the Learner App.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | System runs the batch with the first delivery attempt failing. | System records the failed attempt and retries R-106. | report=R-106 |
| 2 | Student A opens the notification inbox after retry completes. | Exactly one notification for R-106 is present. | recipient=Student A |
| 3 | System displays the delivery audit for R-106. | Audit shows retry activity without duplicate completed delivery. | expected_completed_deliveries=1 |
**Severity:** critical
**Priority:** high

### [Renseikai] Lesson Report Notification – Daily Batch – JST and UTC Date Boundary – Eligible report selected
**Description:** REQ-01 — BVA — Server selection uses JST despite a different UTC calendar date.
**Preconditions:**
- The scheduler time is 2026-10-12 12:00 JST.
- Report R-107 is Published with updated_at = 2026-10-11 00:30 JST (= 2026-10-10 15:30 UTC).
- Student A is logged in to the Learner App.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | System runs the daily report-notification batch. | System selects R-107 using its JST timestamp. | JST=2026-10-11 00:30; UTC=2026-10-10 15:30 |
| 2 | Student A opens the notification inbox. | One notification for R-107 is present. | report=Math F |
**Severity:** high
**Priority:** high

### [Renseikai] Lesson Report Notification – Daily Batch – Two eligible reports – Separate notifications retained
**Description:** REQ-01 and REQ-02 — Decision Table — Each eligible report creates its own notification.
**Preconditions:**
- The scheduler time is 2026-10-12 12:00 JST.
- R-108 for Math G and R-109 for Science H are Published in the batch window.
- Student A is logged in to the Learner App.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | System runs the daily report-notification batch. | System selects R-108 and R-109 once each. | reports=R-108,R-109 |
| 2 | Student A opens the notification inbox. | Separate notifications for Math G and Science H are present. | expected_count=2 |
**Severity:** high
**Priority:** high

### [Renseikai] Lesson Report Notification – Archived Lesson Allocation – Eligible Report Sends No Notification
**Description:** LT-90306 AC-5 and REQ-01/REQ-02 — Decision Table. An otherwise eligible Published Lesson Report is excluded from scheduled delivery while the student's Lesson Allocation is archived.
**Preconditions:**
- The scheduler time is 2026-10-12 12:00 JST.
- Report R-201 for Math Archive is Published with updated_at = 2026-10-12 09:00 JST.
- Student A's sole Lesson Allocation is archived after its Student Package Order is fully removed.
- Student A and Default Parent A are logged in to their apps.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | System runs the daily report-notification batch. | System does not select R-201 and creates no delivery for either recipient. | run=2026-10-12 12:00 JST; report=R-201; allocation=archived |
| 2 | Student A opens the Learner App notification inbox. | No notification for Math Archive is present. | recipient=Student A |
| 3 | Default Parent A opens the Parent App notification inbox. | No notification for Math Archive is present. | recipient=Default Parent A |
**Severity:** critical
**Priority:** high

### [Renseikai] Lesson Report Notification – Restored Lesson Allocation – Subsequent Eligible Report Sends Normally
**Description:** LT-90306 AC-3/AC-5 and REQ-01/REQ-02 — State Transition. After restore, a subsequently eligible Published Lesson Report is delivered once to the Student and Default Parent; restore does not replay the report skipped while archived.
**Preconditions:**
- Student A's Lesson Allocation was archived, then restored on the same record after a living Student Package Order reappeared.
- Report R-202 for Math Restore is Published with updated_at = 2026-10-12 09:00 JST, after the allocation is restored.
- The scheduler time is 2026-10-12 12:00 JST.
- Student A and Default Parent A are logged in to their apps.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | System runs the daily report-notification batch. | System selects R-202 once and creates one delivery for each intended recipient. | run=2026-10-12 12:00 JST; report=R-202; allocation=restored |
| 2 | Student A opens the Learner App notification inbox. | Exactly one notification for Math Restore is present. | recipient=Student A; expected_count=1 |
| 3 | Default Parent A opens the Parent App notification inbox. | Exactly one notification for Math Restore is present. | recipient=Default Parent A; expected_count=1 |
**Severity:** critical
**Priority:** high
