---
ticket_id: LT-61333
ticket_url: https://manabie.atlassian.net/browse/LT-61333
title: "[App] Lesson Report Notification"
module: scheduling
bucket: OOP/renseikai
status: Done
internal_uat_date: null
production_release_date: null
last_updated: 2026-10-19
---

# LT-61333: Lesson Report Notification

## Summary

At 12:00 PM Japan time daily, the system selects qualifying Published Lesson Reports updated in the preceding 24-hour window and sends one localized notification per report to the Student and their Default Parent. Retry must not create duplicate notifications. Selecting the notification must expose **View Report Detail** and open the intended report in the mobile app.

This is distinct from the real-time lesson-publish notification: it is report-triggered, batch-scheduled, and targets the Default Parent rather than all related parents.

---

## Acceptance Criteria

### REQ-01 — Daily selection of published lesson reports

Schedule a job for 12:00 PM daily. Select all Lesson Reports whose status is **Published** and whose updated_at is from 12:00 PM on the prior day until 12:00 PM on the current day.

### REQ-02 — Deliver one notification per published report

For each selected Lesson Report, send a notification to the Student and the Student's Default Parent who has an affiliation with the Student. Each Lesson Report produces a separate notification.

### REQ-03 — Localized notification content

| Locale | Title | Body |
|---|---|---|
| English | Lesson Report ready! | Lesson report for <lesson name> is now available. |
| Japanese | 指導簿が公開されました | <lesson name>の指導簿が公開されました。 |

### REQ-04 — Report-detail navigation

When the recipient selects the notification, display **View Report Detail** and navigate to the lesson-report section of the mobile app.

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---:|---|---|---|---|---|
| 1 | REQ-01 | Run daily at 12:00 PM Japan time. | Schedule | scheduled | System |
| 2 | REQ-01 | Select only Published reports. | Lesson Report status | required status | System |
| 3 | REQ-01 | Begin selection at the previous day's 12:00 PM. | updated_at | time-window filter | System |
| 4 | REQ-01 | End selection at the current day's 12:00 PM. | updated_at | time-window filter | System |
| 5 | REQ-02 | Notify the assigned Student for each selected report. | Student recipient | derived | Learner App |
| 6 | REQ-02 | Notify only the parent whose Student–Parent Relationship has Default = true. | Default Parent recipient | derived | Parent App |
| 7 | REQ-02 | Keep notifications separate per report. | Lesson Report | cardinality | System |
| 8 | REQ-03 | Use the exact localized title strings. | Notification title | fixed localized text | Both apps |
| 9 | REQ-03 | Substitute the lesson name in the English template. | Notification body | localized template | Both apps |
| 10 | REQ-03 | Substitute the lesson name in the Japanese template. | Notification body | localized template | Both apps |
| 11 | REQ-04 | Open the report section through View Report Detail. | View Report Detail | deep link | Both apps |
| 12 | REQ-02 | Deliver only to the intended recipient account that is currently logged in; do not leak to another switched account. | App account | recipient-scoped delivery | Both apps |
| 13 | REQ-04 | If a parent is viewing Student B and selects Student A's notification, switch to Student A before opening Student A's report. | Active student context | automatic context switch | Parent App |

### Cross-epic extension — LT-90306 Lesson Allocation archive

An archived Lesson Allocation makes its Student Session inactive for operational read paths. For this scheduled notification flow, an otherwise eligible Published Lesson Report must therefore create no notification for that student or their Default Parent while the allocation is archived. Once the same allocation is restored, a Lesson Report that becomes eligible afterwards follows the normal delivery rule again. Restore alone must not replay a historical report that was skipped during the archived period; this prevents duplicate or stale notifications.

---

## Conflict & Gap Analysis

### Conflicts with Existing System

_None found. LT-96662 is a distinct lesson-publish notification flow rather than a contradictory requirement._

### Missing in Requirements

| # | Tag | Source | Description |
|---:|---|---|---|
| 1 | [MISSING BEHAVIOR] | LT-61333 REQ-01 | The exact inclusive/exclusive handling at 12:00 PM remains unconfirmed; implement a non-overlapping window and make the boundary observable in logs/tests. |
| 2 | [REGRESSION RISK] | epics/OOP/renseikai/LT-96662-publish-notify-student/test-cases/notification-recipients.md | Resolved: delivery is limited to the intended recipient account that is currently logged in. |
| 3 | [REGRESSION RISK] | epics/OOP/renseikai/LT-96662-publish-notify-student/test-cases/deep-link-navigation.md | Resolved: the Parent App switches from the currently selected student to the notified student before opening the report. |
| 4 | [MISSING BEHAVIOR] | LT-61333 REQ-04 | Logged-out, changed-account, and unavailable-report fallback handling is intentionally out of scope. |
| 5 | [REGRESSION RISK] | epics/OOP/renseikai/LT-96662-publish-notify-student/spec.md | Resolved: this flow is unrelated to lesson-publish notification behavior; test it independently. |
| 6 | [CROSS-EPIC COVERAGE ADDED] | User request, 2026-10-19; LT-90306 AC-3/AC-5 | An archived LA must suppress scheduled Lesson Report notification delivery to both Student and Default Parent. After the same LA is restored, subsequently eligible reports deliver normally; no historical skipped report is replayed solely because of restore. |

### Lesson-Learned Risks

| # | Incident | Date | AC | Risk | Guardrail |
|---:|---|---|---|---|---|
| 1 | Cross-Domain — Incident Prevention Patterns | 2026-09-21 | REQ-01 / REQ-02 / REQ-04 | Scheduled cross-system flows can omit, duplicate, or misroute notifications around time windows, retries, or mobile context changes. | JP timezone and retry idempotency confirmed; test recipient identity and Student-A/Student-B navigation. |

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-01 | One-Time Group Lesson — Full Lifecycle | Published report gains a daily Student/Default-Parent notification and report deep link. | CREATE a notification/context-switch variant. |

### Assumptions Made

- Japan time is confirmed for the schedule; exact inclusion at the 12:00 PM boundary remains unconfirmed.
- A static Jira image was present, but no accessible external Figma URL was provided.
- Qase parent suite 3719 links LT-61333; its Scheduled Report Delivery child suite 3721 contains the baseline delivery cases. Cross-epic archive coverage is maintained in LT-90306 suite 3756.
- Logged-out, changed-account, and unavailable-report fallback handling is out of scope.

---

## Clarification Questions

Answers were confirmed by the user in chat on 2026-10-12. They were **not posted to Jira** at the user's request.

1. The batch uses Japan time; retry must not send a duplicate notification.
2. Default Parent is identified by the Default field on the Student–Parent Relationship. A student can have many parents, but only the Default Parent receives this notification.
3. Send the notification only to the intended account that is currently logged in; do not show it to another switched account.
4. A parent viewing Student B must switch to Student A when opening Student A's notification, then see Student A's exact report.
5. Logged-out, changed-account, and unavailable-report fallback behavior is skipped/out of scope.
6. The feature is unrelated to lesson-publish notifications.

---

## Related Specs

- epics/OOP/renseikai/LT-96662-publish-notify-student/spec.md — analogous mobile-notification, recipient, deep-link, account-switch, and student-context behavior.
- knowledge/domain-knowledge/scheduling/lesson-management/lesson-mobile.md — mobile visibility and notification domain rules.

## Related Test Cases

- epics/OOP/renseikai/LT-96662-publish-notify-student/test-cases/notification-recipients.md — recipient isolation, multiple accounts on one device.
- epics/OOP/renseikai/LT-96662-publish-notify-student/test-cases/deep-link-navigation.md — parent student-context switching and authentication fallback.
- epics/OOP/renseikai/LT-107175-remote-attendance-status-tag/test-cases/app-remote-submission-sync.md — selected-student state isolation in the Learner App.

## QASE Coverage Gaps

- REQ-01 — Exact 12:00 PM boundary handling, repeated runs, and report update/re-publication idempotency.
- REQ-02 — Default-Relationship recipient selection and switch-account delivery isolation.
- REQ-03 — Exact English/Japanese title/body and lesson-name substitution.
- REQ-04 — View Report Detail deep link and parent Student-A/Student-B context switching.
- LT-90306 integration — Archived LA suppresses delivery; a subsequently eligible report delivers normally after restoring the same LA, without replaying a previously skipped report.
