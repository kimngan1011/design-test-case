# Test Cases: LT-61333 — Lesson Report Notification

## Suite: Localized Notification Content

### [Renseikai] Lesson Report Notification – English Content – Eligible report – Exact title and lesson name
**Description:** REQ-03 — Component — English content contains every required value.
**Preconditions:**
- Report R-301 for lesson Math Addition is eligible for the 2026-10-12 12:00 JST batch.
- Student A is logged in with English selected.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | System runs the daily report-notification batch. | System delivers the English notification to Student A. | locale=English |
| 2 | Student A opens the notification item for R-301. | Title is Lesson Report ready! | title=Lesson Report ready! |
| 3 | Student A reads the notification body. | Body is Lesson report for Math Addition is now available. | lesson=Math Addition |
**Severity:** minor
**Priority:** medium

### [Renseikai] Lesson Report Notification – Japanese Content – Eligible report – Exact title and lesson name
**Description:** REQ-03 — Component — Japanese content contains every required value.
**Preconditions:**
- Report R-302 for lesson 算数の足し算 is eligible for the 2026-10-12 12:00 JST batch.
- Student B is logged in with Japanese selected.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | System runs the daily report-notification batch. | System delivers the Japanese notification to Student B. | locale=Japanese |
| 2 | Student B opens the notification item for R-302. | Title is 指導簿が公開されました. | title=指導簿が公開されました |
| 3 | Student B reads the notification body. | Body is 算数の足し算の指導簿が公開されました。 | lesson=算数の足し算 |
**Severity:** minor
**Priority:** medium

### [Renseikai] Lesson Report Notification – Content Binding – Two reports – Each lesson name retained
**Description:** REQ-03 — Decision Table — Separate notifications retain their own lesson-name values.
**Preconditions:**
- Reports R-303 for Math I and R-304 for Science J are eligible for the 2026-10-12 12:00 JST batch.
- Student C is logged in with English selected.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | System runs the daily report-notification batch. | System creates separate notifications for R-303 and R-304. | reports=R-303,R-304 |
| 2 | Student C opens the notification for R-303. | Body names Math I and does not name Science J. | report=R-303 |
| 3 | Student C opens the notification for R-304. | Body names Science J and does not name Math I. | report=R-304 |
**Severity:** major
**Priority:** high
