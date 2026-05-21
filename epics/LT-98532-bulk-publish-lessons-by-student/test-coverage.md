# Test Coverage: LT-98532 — Bulk Publish Lessons by Student

**Jira:** https://manabie.atlassian.net/browse/LT-98532
**Date:** 2026-05-12
**Partner scope:** Riso only
**Platforms:** SF + Mobile App

---

## 1. Business Rules Extracted

| #   | AC      | Business Rule                                                                                                                                                                                                                       |
| --- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | AC 01.2 | "Apply to selected students" checkbox is DISABLED when Calendar filter has 0 students                                                                                                                                               |
| 2   | AC 01.2 | When checkbox disabled: user can select calendar default location OR add multiple locations                                                                                                                                         |
| 3   | AC 01.3 | "Apply to selected students" checkbox is ENABLED (unchecked by default) when 1+ students in Calendar filter                                                                                                                         |
| 4   | AC 01.3 | When checkbox activated: Location field locked to calendar's current location (disabled, read-only)                                                                                                                                 |
| 5   | AC 01.3 | When checkbox activated: user cannot add extra locations (multi-location selection disabled)                                                                                                                                        |
| 6   | AC 01.3 | When checkbox NOT activated (students in filter): all lessons at period published (existing behavior)                                                                                                                               |
| 7   | AC 01.3 | Student filter cannot be modified while Bulk Publish modal is open; user must close modal first                                                                                                                                     |
| 8   | AC 01.4 | Success message: "Bulk publish lesson request has been submitted successfully. Changes will be applied shortly"                                                                                                                     |
| 9   | AC 01.4 | User redirected to previous calendar view after submission                                                                                                                                                                          |
| 10  | AC 01.4 | Job runs asynchronously — calendar must be manually refreshed to see updated status                                                                                                                                                 |
| 11  | AC 01.4 | Only Draft lessons are updated to Published; Published/Completed/Cancelled lessons unaffected                                                                                                                                       |
| 12  | AC 02.1 | Notification sent after job completes — only for successfully published lessons                                                                                                                                                     |
| 13  | AC 02.1 | Partial failure ("Completed with Errors"): notifications sent for successfully published students only                                                                                                                              |
| 14  | AC 02.1 | 0 Draft lessons in scope: job skips silently, no notification fired                                                                                                                                                                 |
| 15  | AC 02.1 | Cross-type dedup: if lesson was already published+notified via LT-96662, it is excluded from bulk notification                                                                                                                      |
| 16  | AC 02.1 | Notification recipients: all students allocated to published lessons, deduplicated (1 notification per student)                                                                                                                     |
| 17  | AC 02.1 | Notification recipients: all parents of deduplicated students (1 notification per parent)                                                                                                                                           |
| 18  | AC 02.1 | Student with no Parent Contact → student skipped entirely (no notification sent)                                                                                                                                                    |
| 19  | AC 02.2 | Notification title: "Lesson Schedule has been Published"                                                                                                                                                                            |
| 20  | AC 02.2 | Notification body Line 1: "Lesson schedules for the following period have been published"                                                                                                                                           |
| 21  | AC 02.2 | Notification body Line 2: period format "Month Day, Year ~ Month Day, Year"                                                                                                                                                         |
| 22  | AC 02.2 | Deep-link: opens Mobile Calendar at month of published start date, start date selected                                                                                                                                              |
| 23  | AC 03.1 | Bulk Action Monitoring gated by config (ON = Riso) and permission (HQ Admin or CM only)                                                                                                                                             |
| 24  | AC 03.1 | Bulk Publish: 1 monitoring record per student+location pairing; records from same batch grouped                                                                                                                                     |
| 24a | AC 03.2 | Fields per job record: Job ID / Batch ID, ID, Action, Job Status, Location, Student (Bulk Publish only), Lesson Start/End Date, Total Lessons, Processed Count, Success, Failed, Created By, Created Time, Completed Time, Run Time |
| 25  | AC 03.3 | Job statuses: Pending → Processing → Completed / Completed with Errors / Failed                                                                                                                                                     |
| 26  | AC 03.3 | Processed Count = Success + Failed (auto-calculated)                                                                                                                                                                                |
| 27  | AC 03.4 | Job Status = "Completed with Errors" when Failed > 0 AND all lessons processed                                                                                                                                                      |
| 28  | AC 03.4 | Job Status = "Failed" when system error terminates job before completion                                                                                                                                                            |
| 29  | AC 03.5 | All job records purged after 2 weeks                                                                                                                                                                                                |
| 30  | AC 03.6 | Filters: Action (all), Job Status (all), Created Date (this week), Location (user's assigned)                                                                                                                                       |

---

## 2. Logic Type Categorization

| #   | AC      | Business Rule Summary                                          | Logic Type                             |
| --- | ------- | -------------------------------------------------------------- | -------------------------------------- |
| 1   | AC 01.2 | Checkbox DISABLED when 0 students in filter                    | Conditional logic                      |
| 2   | AC 01.2 | Location editable + multi-location when checkbox disabled      | Conditional logic                      |
| 3   | AC 01.3 | Checkbox ENABLED unchecked by default when 1+ students         | Conditional logic, State transition    |
| 4   | AC 01.3 | Location locked when checkbox activated                        | Conditional logic, State transition    |
| 5   | AC 01.3 | Extra locations disabled when checkbox activated               | Conditional logic                      |
| 6   | AC 01.3 | Existing behavior retained when checkbox not activated         | Conditional logic, Regression          |
| 7   | AC 01.3 | Filter locked while modal is open                              | Conditional logic                      |
| 8   | AC 01.4 | Success message on submit                                      | Validation logic                       |
| 9   | AC 01.4 | Redirect to previous calendar view                             | State transition                       |
| 10  | AC 01.4 | Async job — calendar requires manual Refresh                   | State transition, Cross-system impact  |
| 11  | AC 01.4 | Only Draft → Published; others unaffected                      | State transition, Data integrity       |
| 12  | AC 02.1 | Notification fires after job completes (full success)          | State transition, Conditional logic    |
| 13  | AC 02.1 | Partial failure → notify successful students only              | Conditional logic, Data integrity      |
| 14  | AC 02.1 | 0 Draft lessons → silent skip                                  | Conditional logic, Data integrity      |
| 15  | AC 02.1 | Cross-type dedup with LT-96662                                 | Data integrity, Conditional logic      |
| 16  | AC 02.1 | Student recipients deduplicated across LS                      | Data integrity                         |
| 17  | AC 02.1 | Parent recipients deduplicated per parent                      | Data integrity                         |
| 18  | AC 02.1 | Student with no parent → skipped entirely                      | Conditional logic, Data integrity      |
| 19  | AC 02.2 | Notification title fixed text                                  | Validation logic                       |
| 20  | AC 02.2 | Notification body Line 1 fixed text                            | Validation logic                       |
| 21  | AC 02.2 | Notification body Line 2 date period format                    | Validation logic, Boundary/range logic |
| 22  | AC 02.2 | Deep-link to Calendar at correct month                         | Cross-system impact, State transition  |
| 23  | AC 03.1 | Monitoring config gate + permission gate                       | Permission logic, Conditional logic    |
| 24  | AC 03.1 | 1 record per student+location; batch grouping                  | Data integrity                         |
| 24a | AC 03.2 | Fields per job record: all required fields present and correct | Validation logic                       |
| 25  | AC 03.3 | Job status lifecycle                                           | State transition                       |
| 26  | AC 03.3 | Processed Count auto-calculated                                | Validation logic, Data integrity       |
| 27  | AC 03.4 | Status = "Completed with Errors" on partial failure            | State transition, Conditional logic    |
| 28  | AC 03.4 | Status = "Failed" on system error                              | State transition                       |
| 29  | AC 03.5 | Records purged after 2 weeks                                   | Data integrity, Boundary/range logic   |
| 30  | AC 03.6 | Filters in monitoring view                                     | Conditional logic, Validation logic    |

---

## 3. Test Techniques per Logic Type

| Logic Type           | Primary Technique        | Secondary Technique                 |
| -------------------- | ------------------------ | ----------------------------------- |
| Conditional logic    | Decision Table           | Negative Testing                    |
| State transition     | State Transition Testing | CRUD Testing                        |
| Validation logic     | Equivalence Partitioning | Negative Testing                    |
| Boundary/range logic | Boundary Value Analysis  | Negative Testing                    |
| Data integrity       | CRUD Testing             | Regression Analysis, Decision Table |
| Cross-system impact  | Regression Analysis      | CRUD Testing                        |
| Permission logic     | Permission Matrix        | Decision Table                      |

---

## 4. Coverage Strategy Table

| AC      | Business Rule Summary                                          | Logic Type                       | Test Technique                      | Risk Level | Coverage Depth |
| ------- | -------------------------------------------------------------- | -------------------------------- | ----------------------------------- | ---------- | -------------- |
| AC 01.2 | Checkbox DISABLED / location editable when 0 students          | Conditional                      | Decision Table                      | Medium     | Standard       |
| AC 01.3 | Checkbox ENABLED unchecked by default when 1+ students         | Conditional, State transition    | Decision Table, State Transition    | High       | Standard       |
| AC 01.3 | Location locked when checkbox activated                        | Conditional, State transition    | Decision Table                      | High       | Standard       |
| AC 01.3 | Extra locations disabled when checkbox activated               | Conditional                      | Decision Table, Negative            | High       | Standard       |
| AC 01.3 | Existing behavior retained when checkbox NOT activated         | Conditional, Regression          | Regression Analysis                 | High       | Standard       |
| AC 01.3 | Filter locked while modal open                                 | Conditional                      | Decision Table, Negative            | Medium     | Smoke          |
| AC 01.4 | Success message + redirect after submit                        | Validation, State transition     | Equivalence Partitioning            | Medium     | Smoke          |
| AC 01.4 | Async job — calendar not updated until Refresh                 | State transition, Cross-system   | State Transition Testing            | High       | Standard       |
| AC 01.4 | Only Draft → Published; others unaffected                      | State transition, Data integrity | State Transition Testing, Negative  | Critical   | Deep           |
| AC 02.1 | Notification fires on full success                             | State transition, Conditional    | State Transition Testing            | Critical   | Deep           |
| AC 02.1 | Partial failure → notify successful students only              | Conditional, Data integrity      | Decision Table, Negative            | Critical   | Deep           |
| AC 02.1 | 0 Draft lessons → silent skip (no notification)                | Conditional, Data integrity      | Decision Table, Negative            | High       | Standard       |
| AC 02.1 | Cross-type dedup with LT-96662                                 | Data integrity, Conditional      | Regression Analysis, Decision Table | Critical   | Deep           |
| AC 02.1 | Student recipients deduplicated across LS                      | Data integrity                   | CRUD Testing, Decision Table        | Critical   | Deep           |
| AC 02.1 | Parent recipients deduplicated per parent                      | Data integrity                   | Decision Table                      | High       | Standard       |
| AC 02.1 | Student with no parent → skipped entirely                      | Conditional, Data integrity      | Decision Table, Negative            | High       | Standard       |
| AC 02.2 | Notification title fixed text                                  | Validation                       | Equivalence Partitioning            | Medium     | Smoke          |
| AC 02.2 | Notification body Line 1 fixed text                            | Validation                       | Equivalence Partitioning            | Medium     | Smoke          |
| AC 02.2 | Notification body Line 2 period date format                    | Validation, Boundary             | BVA, Equivalence Partitioning       | Medium     | Standard       |
| AC 02.2 | Deep-link to Calendar at correct month                         | Cross-system, State transition   | Regression Analysis                 | High       | Standard       |
| AC 03.1 | Monitoring config gate + permission gate                       | Permission, Conditional          | Permission Matrix, Decision Table   | High       | Standard       |
| AC 03.1 | 1 record per student+location; batch grouping                  | Data integrity                   | CRUD Testing                        | High       | Standard       |
| AC 03.2 | All required fields present and populated correctly per record | Validation logic                 | Equivalence Partitioning            | Medium     | Standard       |
| AC 03.3 | Job status lifecycle (Pending → ... → Completed)               | State transition                 | State Transition Testing            | High       | Standard       |
| AC 03.3 | Processed Count = Success + Failed                             | Validation, Data integrity       | Equivalence Partitioning            | Medium     | Smoke          |
| AC 03.4 | Status = "Completed with Errors" on partial failure            | State transition, Conditional    | Decision Table, State Transition    | High       | Standard       |
| AC 03.4 | Status = "Failed" on system error                              | State transition                 | Negative Testing                    | Medium     | Smoke          |
| AC 03.5 | Records purged after 2 weeks                                   | Data integrity, Boundary         | Boundary Value Analysis             | Low        | Smoke          |
| AC 03.6 | Filters in monitoring view                                     | Conditional, Validation          | Decision Table                      | Medium     | Standard       |

---

## 5. High-Risk Areas

### 🔴 Critical Risk

| Area                                                           | Reason                                                                                                                                                                                          | Recommended Approach                                                                                                                                                 |
| -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| BR-11: Publish scope — only Draft → Published                  | Incorrect scope (publishing non-Draft lessons or publishing wrong student's lessons) would cause data corruption visible to students and parents                                                | State Transition + Negative: verify Published/Completed/Cancelled lessons are NOT changed; verify student-scoped publish only affects the filtered students' lessons |
| BR-12 + BR-13: Notification trigger on full/partial success    | Silent failure (no notification when there should be one, or notification when there shouldn't be) directly impacts students and parents receiving lesson information                           | Decision Table: full success, partial failure, all-fail scenarios; cross-check notification counts against lesson publish counts                                     |
| BR-15: Cross-type dedup with LT-96662                          | Same student receiving duplicate notifications (bulk + individual) is the exact pattern that caused the Aso 2026-04-13 incident; confirmed required by PM. Failure = silent double notification | Regression test: publish 1 lesson via LT-96662 "Publish and Notify", then run bulk publish for same period → verify 0 duplicate notification for that lesson         |
| BR-16: Student recipient deduplication across Lesson Schedules | Student in 3 LS in the same batch must receive exactly 1 notification. Failure = notification spam, user confusion                                                                              | Decision Table: student in 1 LS, 2 LS, 3 LS → always 1 notification                                                                                                  |

### 🟠 High Risk

| Area                                                          | Reason                                                                                                                                                  | Recommended Approach                                                                                                                             |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| BR-3 / BR-4 / BR-5: Checkbox state + location lock            | Checkbox state determines publish scope; wrong state = wrong scope = wrong students notified                                                            | Decision Table: 3 checkbox states (disabled / enabled-unchecked / enabled-checked) × location field state                                        |
| BR-6: Existing behavior retained when checkbox not activated  | Regression risk: if new checkbox code breaks the non-activated path, all non-student-filtered bulk publishes break                                      | Regression Analysis: run existing Bulk Publish flow with students in filter but checkbox unchecked → same result as before LT-98532              |
| BR-10: Async job + manual Refresh required                    | If tester/user expects synchronous update, test assertions fail or users think publish failed                                                           | State Transition: immediately after submit → calendar shows Draft; after Refresh → Published                                                     |
| BR-18: Student with no parent → skipped entirely              | Confirmed by PM: student with no parent is skipped entirely (not just parent-only notification). Wrong implementation = student silently never notified | Decision Table: student with 0 parents, 1 parent, 2 parents                                                                                      |
| BR-22: Deep-link to Calendar at correct month                 | LT-96662 already has deep-link tests (deep-link-navigation.md) — reuse pattern but verify month navigation vs. lesson detail navigation difference      | Regression: same pattern as LT-96662 deep-link but target = Calendar monthly view at start date                                                  |
| BR-23: Monitoring config + permission gate                    | Riso-only config off by default; wrong config = monitoring visible to all partners                                                                      | Permission Matrix: HQ with permission ✅ / HQ without permission ✗ / CM with permission ✅ / CM without ✗ / Riso partner ✅ / non-Riso partner ✗ |
| BR-24: 1 record per student+location pairing + batch grouping | Incorrect record granularity (1 per batch instead of 1 per student) or missing batch grouping = monitoring unusable                                     | CRUD: trigger bulk for 3 students → verify 3 records, same Batch ID, grouped                                                                     |

### 🟡 Medium Risk

| Area                                                         | Reason                                                                                                       | Recommended Approach                                                                        |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| BR-14: 0 Draft lessons → silent skip                         | Edge case — no user warning. Risk: user thinks publish succeeded but nothing happened                        | Negative: all lessons already Published → submit → verify 0 status changes, 0 notifications |
| BR-21: Notification body period date format                  | Format "Month Day, Year ~ Month Day, Year" — localization/boundary: start date = end date, cross-year period | BVA: same-day period, cross-month, cross-year                                               |
| BR-25/26: Job status lifecycle + Processed Count calculation | UI count accuracy; Processed Count must stay = Success + Failed during live processing                       | State Transition: check count at Pending (0/0), mid-processing (partial), Completed         |
| BR-30: Monitoring filters defaults + behavior                | Default filter "Created Date = this week" + location scoped to user's locations                              | Equivalence Partitioning: default state, custom date range, location filter                 |

---

## 6. Coverage Gaps vs. Existing Test Cases

**Existing related test cases read:**

- `output/test-cases/lesson-management/lesson/publish-notify-student/` (LT-96662) — 6 files covering button visibility, send notification, notification content, notification recipients, retry mechanism, deep-link navigation
- `output/test-cases/PX-2026-04-13.json` — Qase cases 4624–4626, 4751–4753: existing Bulk Publish from Calendar (no checkbox, no async, no notification)

| Gap Area                                                   | Existing Test Case                                                                                                              | Overlap                             | New Coverage Needed                               |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------- | ------------------------------------------------- |
| Checkbox DISABLED when 0 students in filter                | None                                                                                                                            | None                                | ✅ New: `bulk-publish-modal.md`                   |
| Checkbox ENABLED unchecked by default when 1+ students     | None                                                                                                                            | None                                | ✅ New: `bulk-publish-modal.md`                   |
| Location locked when checkbox activated                    | None                                                                                                                            | None                                | ✅ New: `bulk-publish-modal.md`                   |
| Extra locations disabled when checkbox activated           | None                                                                                                                            | None                                | ✅ New: `bulk-publish-modal.md`                   |
| Existing behavior retained when checkbox NOT activated     | Qase 4624–4626, 4751–4753 (partial — no checkbox guard)                                                                         | Partial                             | ✅ New regression case in `bulk-publish-modal.md` |
| Filter locked while modal open                             | None                                                                                                                            | None                                | ✅ New: `bulk-publish-modal.md`                   |
| Success message + redirect (async)                         | Qase 4624–4626 (partial — pre-async behavior)                                                                                   | Partial                             | ✅ New: `bulk-publish-async-job.md`               |
| Calendar not updated until Refresh                         | None                                                                                                                            | None                                | ✅ New: `bulk-publish-async-job.md`               |
| Only Draft → Published; others unaffected (student-scoped) | Qase 4624, lesson-status.md TC-1469–1476 (partial — no student scope)                                                           | Partial                             | ✅ New: `bulk-publish-async-job.md`               |
| Notification fires on full success                         | publish-notify-student/send-notification.md (LT-96662 pattern, different trigger)                                               | Partial — different feature         | ✅ New: `bulk-publish-notification-trigger.md`    |
| Partial failure → notify successful students only          | None                                                                                                                            | None                                | ✅ New: `bulk-publish-notification-trigger.md`    |
| 0 Draft lessons → silent skip                              | None                                                                                                                            | None                                | ✅ New: `bulk-publish-notification-trigger.md`    |
| Cross-type dedup with LT-96662                             | publish-notify-student/send-notification.md (covers LT-96662 side only)                                                         | Partial — no cross-test             | ✅ New: `bulk-publish-notification-trigger.md`    |
| Student recipients deduplicated across LS                  | notification-recipients.md (LT-96662 single-lesson dedup, different scope)                                                      | Partial — different scope           | ✅ New: `bulk-publish-notification-recipients.md` |
| Parent recipients deduplicated per parent                  | notification-recipients.md (partial — same pattern)                                                                             | Partial                             | ✅ New: `bulk-publish-notification-recipients.md` |
| Student with no parent → skipped entirely                  | notification-recipients.md has "student-only" case for LT-96662, but LT-98532 behavior differs (skip entirely vs. student-only) | Partial — different expected result | ✅ New: `bulk-publish-notification-recipients.md` |
| Notification title + body content                          | notification-content.md (LT-96662 — different content format)                                                                   | None — completely different content | ✅ New: `bulk-publish-notification-content.md`    |
| Notification body period date format (boundary)            | None                                                                                                                            | None                                | ✅ New: `bulk-publish-notification-content.md`    |
| Deep-link to Calendar at correct month                     | deep-link-navigation.md (LT-96662 — navigates to Lesson Detail, not Calendar monthly)                                           | None — different deep-link target   | ✅ New: `bulk-publish-notification-content.md`    |
| Monitoring config gate + permission gate                   | None                                                                                                                            | None                                | ✅ New: `bulk-action-monitoring.md`               |
| 1 record per student+location; batch grouping              | None                                                                                                                            | None                                | ✅ New: `bulk-action-monitoring.md`               |
| All required record fields present and populated (AC 03.2) | None                                                                                                                            | None                                | ✅ New: `bulk-action-monitoring.md`               |
| Job status lifecycle                                       | None                                                                                                                            | None                                | ✅ New: `bulk-action-monitoring.md`               |
| Processed Count calculation                                | None                                                                                                                            | None                                | ✅ New: `bulk-action-monitoring.md`               |
| Completed with Errors status                               | None                                                                                                                            | None                                | ✅ New: `bulk-action-monitoring.md`               |
| Failed status on system error                              | None                                                                                                                            | None                                | ✅ New: `bulk-action-monitoring.md`               |
| Data retention 2 weeks                                     | None                                                                                                                            | None                                | ✅ New: `bulk-action-monitoring.md` (smoke only)  |
| Filters in monitoring view                                 | None                                                                                                                            | None                                | ✅ New: `bulk-action-monitoring.md`               |

**Key reuse notes from LT-96662 publish-notify-student:**

| LT-96662 Test Case Pattern                                   | Applicability to LT-98532                                                                                | Adaptation Required                                                                                  |
| ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `notification-recipients.md` — Student + parent both receive | Reuse pattern: same recipient resolution logic                                                           | Adapt trigger (job completion vs. button click); adapt dedup scope (across all LS vs. single lesson) |
| `notification-recipients.md` — Multiple parents per student  | Reuse pattern: same BR                                                                                   | Adapt trigger only                                                                                   |
| `notification-recipients.md` — Student with no parent        | **Different expected result**: LT-96662 = student-only notification; LT-98532 = student skipped entirely | Must create new TC; do NOT copy LT-96662 expected result                                             |
| `notification-recipients.md` — No device token               | Applicable pattern                                                                                       | Adapt trigger                                                                                        |
| `deep-link-navigation.md` — Logged-in user taps notification | Partially applicable                                                                                     | Deep-link target is Calendar (monthly view) not Lesson Detail — new TC required                      |
| `deep-link-navigation.md` — User not logged in               | Applicable pattern                                                                                       | Adapt target screen                                                                                  |
| `deep-link-navigation.md` — Parent switch student context    | Applicable pattern                                                                                       | Adapt target screen                                                                                  |
| `retry-mechanism.md`                                         | **Not applicable** — LT-98532 uses async job queue, not per-notification retry. Different failure model. | Do not reuse                                                                                         |
| `send-notification.md` — "Don't Send" flow                   | **Not applicable** — LT-98532 has no confirmation modal                                                  | Do not reuse                                                                                         |
| `notification-content.md` — Title and body format            | Different content entirely                                                                               | New TCs required; same verification approach                                                         |

---

## 7. Suggested Test Suite Structure

```
output/test-cases/lesson-management/lesson/bulk-publish-by-student/
├── bulk-publish-modal.md
│   → AC 01.2, AC 01.3 — Checkbox states (disabled/enabled/activated), location lock,
│     extra locations disabled, filter lock while modal open, existing behavior regression
│
├── bulk-publish-async-job.md
│   → AC 01.4 — Success message, redirect, async job behavior, Refresh required,
│     Draft-only publish scope, student-scoped vs. all-lesson publish
│
├── bulk-publish-notification-trigger.md
│   → AC 02.1 (trigger conditions) — Full success trigger, partial failure (Completed with Errors),
│     0 Draft lessons silent skip, cross-type dedup with LT-96662
│
├── bulk-publish-notification-recipients.md
│   → AC 02.1 (recipients) — Student dedup across LS, parent dedup per parent,
│     student in multiple LS (1 notification only), student with no parent (skipped entirely),
│     no device token (graceful skip)
│
├── bulk-publish-notification-content.md
│   → AC 02.2 — Notification title, body line 1, body line 2 (period format BVA),
│     deep-link to Calendar at correct month (logged-in, not logged-in, switch student context)
│
└── bulk-action-monitoring.md
    → AC 03.1, AC 03.2, AC 03.3, AC 03.4, AC 03.5, AC 03.6 — Config gate, permission gate,
      1 record per student+location, batch grouping, all fields, status lifecycle,
      Processed Count calculation, Completed with Errors, Failed, data retention, filters
```
