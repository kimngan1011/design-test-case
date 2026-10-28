# Test Cases: LT-61333 — Lesson Report Notification

## Suite: Recipient Resolution and Account Isolation

### [Renseikai] Lesson Report Notification – Recipient – Default Parent – Only default parent notified
**Description:** REQ-02 — Decision Table — The Default Relationship controls parent delivery.
**Preconditions:**
- Report R-201 is eligible for the 2026-10-12 12:00 JST batch.
- Student A is linked to Parent A with Default = true.
- Student A is linked to Parent B with Default = false.
- Student A, Parent A, and Parent B are logged in to their apps.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | System runs the daily report-notification batch. | System creates recipient delivery for Student A and Parent A only. | report=R-201 |
| 2 | Parent A opens the notification inbox. | One notification for R-201 is present. | Default=true |
| 3 | Parent B opens the notification inbox. | No notification for R-201 is present. | Default=false |
**Severity:** major
**Priority:** high

### [Renseikai] Lesson Report Notification – Recipient – No Default Parent – Student delivery retained
**Description:** REQ-02 — Negative — Missing Default Parent does not block the Student notification.
**Preconditions:**
- Report R-202 is eligible for the 2026-10-12 12:00 JST batch.
- Student B has no Parent Relationship with Default = true.
- Student B is logged in to the Learner App.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | System runs the daily report-notification batch. | System creates delivery for Student B and no parent delivery. | report=R-202 |
| 2 | Student B opens the notification inbox. | One notification for R-202 is present. | recipient=Student B |
**Severity:** major
**Priority:** high

### [Renseikai] Lesson Report Notification – Recipient – Unrelated Parent – No report data exposed
**Description:** REQ-02 — Permission Matrix Negative — A parent without the Student relationship receives nothing.
**Preconditions:**
- Report R-203 is eligible for Student C.
- Parent C has Default = true for Student C.
- Parent D has no relationship with Student C.
- Parent D is logged in to the Parent App.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | System runs the daily report-notification batch. | System creates no recipient delivery for Parent D. | report=R-203 |
| 2 | Parent D opens the notification inbox. | No notification or report data for Student C is present. | recipient=Parent D |
**Severity:** critical
**Priority:** high

### [Renseikai] Lesson Report Notification – Switch Account – Intended Student active – Notification visible
**Description:** REQ-02 — Permission Matrix — The intended active Student account receives the report notification.
**Preconditions:**
- Report R-204 is eligible for Student D.
- One device has Student D and Student E accounts available through Switch Account.
- Student D is the currently logged-in account.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | System runs the daily report-notification batch. | System delivers R-204 to Student D's current account. | active=Student D |
| 2 | Student D opens the notification inbox. | One notification for R-204 is present. | report=R-204 |
**Severity:** critical
**Priority:** high

### [Renseikai] Lesson Report Notification – Switch Account – Different Student active – Notification hidden
**Description:** REQ-02 — Permission Matrix Negative — A switched account that is not the recipient does not see the notification.
**Preconditions:**
- Report R-205 is eligible for Student F.
- One device has Student F and Student G accounts available through Switch Account.
- Student G is the currently logged-in account at batch execution.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | System runs the daily report-notification batch. | System creates no visible delivery for Student G. | active=Student G; recipient=Student F |
| 2 | Student G opens the notification inbox. | No notification for R-205 is present. | report=R-205 |
**Severity:** critical
**Priority:** high

### [Renseikai] Lesson Report Notification – Switch Account – Parent account – Recipient role isolated
**Description:** REQ-02 — Permission Matrix — An intended Default Parent account receives its own delivery without exposing it to a switched Student account.
**Preconditions:**
- Report R-206 is eligible for Student H and Default Parent H.
- One device has Student H and Parent H accounts available through Switch Account.
- Parent H is the currently logged-in account.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | System runs the daily report-notification batch. | System delivers R-206 to Parent H's current account. | active=Parent H |
| 2 | Parent H opens the notification inbox. | One notification for R-206 is present. | recipient=Parent H |
| 3 | Student H switches into the account on the same device. | Student H does not see Parent H's notification entry. | switched_account=Student H |
**Severity:** critical
**Priority:** high
