# Test Coverage: LT-61333 — Lesson Report Notification

**Jira:** https://manabie.atlassian.net/browse/LT-61333  
**Date:** 2026-10-19

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---:|---|---|
| 1 | REQ-01 | Run at 12:00 PM Japan time daily. |
| 2 | REQ-01 | Select Published reports only. |
| 3 | REQ-01 | Window begins at 12:00 PM on the previous Japan-time day. |
| 4 | REQ-01 | Window ends at 12:00 PM on the current Japan-time day. |
| 5 | REQ-02 | Notify the assigned Student. |
| 6 | REQ-02 | Notify only the parent whose Relationship Default field is true. |
| 7 | REQ-02 | Generate distinct notifications per eligible Lesson Report. |
| 8 | REQ-03 | Render the exact localized title. |
| 9 | REQ-03 | Render the English body with the report lesson name. |
| 10 | REQ-03 | Render the Japanese body with the report lesson name. |
| 11 | REQ-04 | Show View Report Detail and open the report section. |
| 12 | REQ-02 | Deliver only to the intended currently logged-in recipient account. |
| 13 | REQ-04 | Switch a parent from Student B to Student A before opening Student A's report. |
| 14 | LT-90306 AC-5 / REQ-01 / REQ-02 | An otherwise eligible Published report creates no notification while the student's Lesson Allocation is archived. |
| 15 | LT-90306 AC-3 / REQ-01 / REQ-02 | After the same Lesson Allocation is restored, a subsequently eligible report delivers once to the Student and Default Parent; restore does not replay a historical skipped report. |

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| REQ-01 | 1–4 | Recurrence; Boundary/range; Conditional; Data integrity |
| REQ-02 | 5–7, 12 | Conditional; Permission; Data integrity; Cross-system impact |
| REQ-03 | 8–10 | Display completeness; Conditional |
| REQ-04 | 11, 13 | Cross-system impact; Conditional; State transition; Display completeness |
| LT-90306 AC-5 / REQ-01 / REQ-02 | 14 | Conditional; Negative; Cross-system impact |
| LT-90306 AC-3 / REQ-01 / REQ-02 | 15 | State transition; Regression; Data integrity |

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Recurrence | State Transition; Regression |
| Boundary/range | Boundary Value Analysis; Negative |
| Conditional | Decision Table; Negative |
| Permission | Permission Matrix; Decision Table |
| Data integrity | CRUD; Regression; Decision Table |
| Cross-system impact | Regression; CRUD |
| Display completeness | Component; Negative |
| State transition | State Transition; CRUD |

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| REQ-01 | Job runs once at 12:00 PM JST and selects Published reports in the intended window. | Recurrence; Boundary/range; Conditional | State Transition; BVA; Decision Table | Critical | Deep |
| REQ-01 | Cover 11:59:59, 12:00:00, 12:00:01 JST; make the non-overlapping boundary implementation observable. | Boundary/range; Data integrity | BVA; Regression | Critical | Deep |
| REQ-01 | Retry/replay never creates duplicate notification records or inbox entries. | Data integrity; Recurrence | Decision Table; Regression | Critical | Deep |
| REQ-01 / REQ-02 | A 1,000-report batch for 500 students delivers every report notification to each Student and their Default Parent. | Data integrity; Cross-system impact | Scenario; Decision Table | Critical | Deep |
| REQ-01 | Device timezones ahead/behind JST do not alter server-side selection. | Boundary/range; Cross-system impact | BVA; Negative | High | Deep |
| REQ-02 | Student receives one notification per eligible report; Default=true parent alone receives the parent notification. | Conditional; Permission; Cross-system impact | Decision Table; Permission Matrix | High | Deep |
| REQ-02 | Multiple reports create separate correctly linked notifications. | Data integrity; Display completeness | Decision Table; Component | High | Deep |
| REQ-02 | Shared-device Switch Account exposes notification only to the intended currently logged-in account. | Permission; Data integrity | Permission Matrix; Negative | Critical | Deep |
| REQ-02 | Non-default, unrelated, inactive switched accounts and ineligible reports receive no notification. | Conditional; Permission | Decision Table; Negative | High | Deep |
| LT-90306 AC-5 / REQ-01 / REQ-02 | An otherwise eligible Published report sends no notification while the student's Lesson Allocation is archived. | Conditional; Cross-system impact | Decision Table; Negative | Critical | Standard |
| LT-90306 AC-3 / REQ-01 / REQ-02 | A subsequently eligible report sends once to Student and Default Parent after the same Lesson Allocation is restored; no skipped historical report is replayed. | State transition; Data integrity | State Transition; Regression | Critical | Standard |
| REQ-03 | Exact EN and JP title/body with each report's lesson name. | Display completeness; Conditional | Component; Negative | Medium | Standard |
| REQ-03 | Two reports with different lesson names retain correct locale and data binding. | Data integrity; Display completeness | Decision Table; Component | High | Deep |
| REQ-04 | Notification displays exact View Report Detail text and opens the selected report section. | Display completeness; Cross-system impact | Component; Regression | High | Deep |
| REQ-04 | Parent active on Student B taps Student A's notification, switches to Student A, and opens Student A's report. | Conditional; State transition; Cross-system impact | State Transition; Decision Table | Critical | Deep |
| REQ-04 | Multiple Students in one lesson retain separate Homework Completion, Total Score, Test Result, and Understanding values in both apps. | Data integrity; Display completeness; Cross-system impact | Decision Table; State Transition | Critical | Deep |
| REQ-02 / REQ-04 | Multiple Students across multiple lessons map every notification to the exact Student, lesson, and four report-field values. | Data integrity; Display completeness; Cross-system impact | Decision Table; State Transition | Critical | Deep |
| REQ-04 | A stale or changed context cannot open another student's report. | Permission; Data integrity | Permission Matrix; Negative | Critical | Deep |

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Batch window and retry | Boundary/replay errors omit or duplicate user-facing notifications. | Freeze server time in JST; test before/exact/after 12 PM and retry/replay; verify exactly one entry per recipient/report. |
| Recipient account isolation | Shared-device accounts can expose report data to an unrelated user. | Use Student A, Student B, and Parent A; prove only the intended active account sees the notification. |
| Parent child-context switch | A deep link can open Student A data while Student B remains active. | Begin on Student B, tap Student A notification, assert active child then exact report identity. |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Default Parent resolution | Incorrect Relationship filtering discloses the report to the wrong parent. | Decision table: Default true/false, multiple parents, no default, unrelated parent. |
| Report eligibility | Draft, Submitted, old, and later-updated reports must not enter the batch. | Status × updated_at decision table using two reports around the boundary. |
| Cross-surface navigation | Report notification must not reuse the legacy Lesson Detail route. | Validate inbox item, CTA, active student, report identity, and lesson name end to end. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Localized static content | Wrong EN/JP text reduces clarity. | Assert every title/body string and lesson-name substitution. |

## G. Downstream Effects Inventory

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner (TC) |
|---|---|---|---|
| Batch selects an eligible report | One notification record and inbox item per Student. | Notification service; Learner App | scheduled-delivery |
| Batch selects an eligible report | One notification record and inbox item per Default Parent. | Notification service; Parent App | recipient-isolation |
| Batch retries/replays | No extra record, badge, or inbox entry. | Notification service; both apps | scheduled-delivery |
| Batch selects 1,000 eligible reports for 500 students | Every Student and Default Parent receives the two notifications associated with that student's reports. | Notification service; Learner App; Parent App | scheduled-delivery |
| Batch excludes a report | No notification record/inbox item for Draft, Submitted, old, or out-of-window report. | Notification service; both apps | scheduled-delivery |
| Batch selects an otherwise eligible report while the student's LA is archived | No notification record or inbox item is created for Student or Default Parent. | Notification service; both apps | scheduled-delivery / LT-90306 archive suite |
| LA is restored, then a new report becomes eligible | One notification record and inbox item are created for Student and Default Parent; the report skipped while archived is not replayed. | Notification service; both apps | scheduled-delivery / LT-90306 archive suite |
| Recipient taps notification | View Report Detail opens the intended report. | Learner/Parent App report section | report-deep-link |
| Parent taps Student A notification while Student B active | Active child changes to Student A before report load; Student B remains inaccessible through the link. | Parent App context/report | report-deep-link |
| Multiple Students share one lesson or have multiple lessons | Each app renders the exact Homework Completion, Total Score, Test Result, and Understanding values for the notified Student/report. | Learner App; Parent App report section | report-deep-link |

**Inverse action:** N/A — no revoke/unpublish/delete notification action is specified. Negative coverage proves excluded reports create no notification.

## H. Display & Ordering Inventory

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| Student notification item | Localized title, localized body, lesson name, View Report Detail | EN/JP locale | None specified | Lesson Report ready!; Lesson report for <lesson name> is now available.; View Report Detail |
| Parent notification item | Localized title, localized body, lesson name, View Report Detail | Student B to Student A switch | None specified | 指導簿が公開されました; <lesson name>の指導簿が公開されました。; View Report Detail |
| Report destination | Notified report identity; active student identity | Parent selected-student switch | None specified | N/A |

**H.1 — N/A:** No accessible Figma URL is present in the approved spec.

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Daily 12 PM JST selection, boundaries, retry idempotency | Qase suite 3719 — 0 cases | None | ✅ Scheduler, status/window partitions, exact boundary, timezone, replay/retry |
| High-volume Student and Default Parent delivery | Qase suite 3719 — 0 cases | None | ✅ 1,000 reports / 500-student completeness and duplicate-free delivery |
| Student and Default Parent resolution | LT-96662 notification recipient cases | Different trigger and all-parent audience | ✅ Default Relationship decision table, report-specific delivery |
| Switch Account isolation | LT-96662 account-switch cases | Analogous pattern only | ✅ Current-account delivery rule |
| EN/JP content | Qase suite 3719 — 0 cases | None | ✅ Exact content and data-binding |
| Parent Student-A/Student-B report navigation | LT-96662 deep-link cases | Analogous route opens Lesson Detail | ✅ Report route and active-child switch |
| Logged-out/changed-account fallback | Approved spec says out of scope | N/A | No new test case |
| Archived LA suppresses scheduled report notification | None — archive dimension is absent from the 8 existing Scheduled Report Delivery cases | None | ✅ Added in LT-90306 Qase suite 3756, case #30024 |
| Restored LA resumes normal delivery for a subsequently eligible report | None — archive/restore transition is absent from the 8 existing Scheduled Report Delivery cases | None | ✅ Added in LT-90306 Qase suite 3756, case #30025 |

## 7. Suggested Test Suite Structure

~~~
epics/OOP/renseikai/LT-61333-lesson-report-notification/test-cases/
├── scheduled-delivery.md       → REQ-01 — JST scheduling, eligibility, retry idempotency
├── recipient-isolation.md      → REQ-02 — Student/Default Parent and Switch Account isolation
├── notification-content.md     → REQ-03 — exact EN/JP content and report binding
└── report-deep-link.md         → REQ-04 — View Report Detail and selected-student switch
~~~
