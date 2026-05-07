# Test Coverage: LT-96662 — [Renseikai] Receive notifications when a new lesson is published

**Jira:** https://manabie.atlassian.net/browse/LT-96662
**Date:** 2026-04-13

---

## 1. Business Rules Extracted

| #   | AC        | Business Rule                                                                                                                                                                                  |
| --- | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | AC 01.1   | "Publish and notify student" button added to SF Lesson Detail page                                                                                                                             |
| 2   | AC 01.1   | Button visible only when lesson status = Draft OR Published; hidden for all other statuses (Completed, Cancelled, etc.)                                                                        |
| 3   | AC 02.1   | When clicked on Draft lesson: lesson is published (core rules apply) + confirmation modal shown                                                                                                |
| 4   | AC 02.1   | When clicked on Published lesson: no status change + confirmation modal shown                                                                                                                  |
| 5   | AC 02.2   | Confirmation modal message: "Would you like to send notifications about the publishing lesson to all allocated students?" with Send / Don't Send options                                       |
| 6   | AC 02.2   | "Send" → triggers notification flow; "Don't Send" → no notification sent                                                                                                                       |
| 7   | [Gap #6]  | "Don't Send" on a Draft lesson → lesson was already published before modal; lesson remains Published (status NOT reverted)                                                                     |
| 8   | AC 02.1   | Notification recipients = student assigned to lesson + ALL parent contacts linked to that student via Relationship                                                                             |
| 9   | [Gap #3]  | Student has no linked parent → notification sent to student only (expected behavior to confirm with product)                                                                                   |
| 10  | [Gap #4]  | Student/parent has no device token (never logged into app) → notification silently skipped                                                                                                     |
| 11  | AC 02.1   | Notification title: "Lesson Published" (JP: 授業公開のおしらせ)                                                                                                                                |
| 12  | AC 02.1   | Notification body: lesson name + lesson date + start/end time + CTA tap to view lesson details                                                                                                 |
| 13  | AC 02.1   | Notifications sent in real-time (not batched)                                                                                                                                                  |
| 14  | AC 02.3   | Retry on failure: up to 3 automatic attempts with short delay between each                                                                                                                     |
| 15  | AC 02.3   | Idempotent delivery — only one successful notification delivered even if multiple retry attempts succeed                                                                                       |
| 16  | AC 02.3   | Every attempt (success or failure) must be logged for audit                                                                                                                                    |
| 17  | AC 02.3   | If all 3 attempts fail → failure logged clearly (error log / admin dashboard)                                                                                                                  |
| 18  | AC 03.1   | Notification deep-links to the specific Lesson Detail page of the published lesson                                                                                                             |
| 19  | [Gap #11] | User not logged in when tapping notification → redirect flow (confirm with product: login then lesson detail, or app home?)                                                                    |
| 20  | [Gap #10] | Parent viewing Student B, receives notification for Student A → confirm expected behavior: auto-switch context or stay on Student B                                                            |
| 21  | PRD       | Custom permission **"Publish Lesson With Notification"** controls button visibility — added to Renseikai OOP Permission Set (PS) on first release; other partners do not receive it by default |
| 22  | PRD       | Feature enabled for Renseikai only on initial release (OOP PS); future partners considered per request                                                                                         |
| 23  | [Gap #8]  | Button visible to any SF user who already has permission to see/use the existing Publish button (no separate role restriction)                                                                 |

---

## 2. Logic Type Categorization

| AC      | Business Rule # | Logic Type                            |
| ------- | --------------- | ------------------------------------- |
| AC 01.1 | 1, 2            | Conditional logic                     |
| AC 02.1 | 3, 4            | State transition                      |
| AC 02.2 | 5, 6, 7         | Conditional logic, State transition   |
| AC 02.1 | 8, 9, 10        | Data integrity                        |
| AC 02.1 | 11, 12, 13      | Validation logic, Cross-system impact |
| AC 02.3 | 14, 15          | Data integrity                        |
| AC 02.3 | 16, 17          | Data integrity                        |
| AC 03.1 | 18, 19, 20      | Cross-system impact                   |
| PRD     | 21, 22, 23      | Conditional logic, Permission logic   |

---

## 3. Test Technique Selection

| Logic Type          | Applicable Techniques                             |
| ------------------- | ------------------------------------------------- |
| Conditional logic   | Decision Table, Negative Testing                  |
| State transition    | State Transition Testing, Negative Testing        |
| Data integrity      | CRUD Testing, Decision Table, Regression Analysis |
| Validation logic    | Equivalence Partitioning, Negative Testing        |
| Cross-system impact | Regression Analysis, Decision Table               |
| Permission logic    | Permission Matrix                                 |

---

## 4. Structured Coverage Strategy

| AC                  | Business Rule Summary                                                                                 | Logic Type          | Test Technique                        | Risk Level | Coverage Depth |
| ------------------- | ----------------------------------------------------------------------------------------------------- | ------------------- | ------------------------------------- | ---------- | -------------- |
| AC 01.1             | Button exists on SF Lesson Detail page                                                                | Conditional logic   | Decision Table                        | High       | Standard       |
| AC 01.1             | Button visible for Draft/Published; hidden for Completed, Cancelled                                   | Conditional logic   | Decision Table, Negative Testing      | High       | Standard       |
| AC 02.1             | Click on Draft lesson → publishes lesson + shows confirmation modal                                   | State transition    | State Transition Testing              | Critical   | Deep           |
| AC 02.1             | Click on Published lesson → no status change + shows confirmation modal                               | State transition    | State Transition Testing              | High       | Standard       |
| AC 02.2             | Confirmation modal content and options correct (Send / Don't Send)                                    | Validation logic    | Equivalence Partitioning              | High       | Standard       |
| AC 02.2             | Click "Send" → notification flow triggered                                                            | Conditional logic   | Decision Table                        | Critical   | Deep           |
| AC 02.2             | Click "Don't Send" → no notification sent                                                             | Conditional logic   | Decision Table, Negative Testing      | High       | Standard       |
| AC 02.2 / [Gap #6]  | "Don't Send" on Draft lesson → lesson stays Published (not reverted)                                  | State transition    | State Transition Testing              | High       | Standard       |
| AC 02.1             | Recipients: student + ALL linked parent contacts                                                      | Data integrity      | CRUD Testing, Decision Table          | Critical   | Deep           |
| AC 02.1 / [Gap #3]  | No parent linked to student → notification to student only                                            | Data integrity      | Decision Table, Negative Testing      | High       | Standard       |
| AC 02.1 / [Gap #4]  | No device token → notification silently skipped                                                       | Conditional logic   | Decision Table, Negative Testing      | Medium     | Standard       |
| AC 02.1             | Notification content correct (title, body, lesson name, date, time, CTA)                              | Validation logic    | Equivalence Partitioning              | High       | Standard       |
| AC 02.1             | Notification content in JP correct (JP tenant)                                                        | Validation logic    | Equivalence Partitioning              | Medium     | Standard       |
| AC 02.3             | Retry on failure: up to 3 attempts with short delay                                                   | Data integrity      | Negative Testing                      | Medium     | Standard       |
| AC 02.3             | No duplicate notification when retry succeeds                                                         | Data integrity      | Regression Analysis, Negative Testing | High       | Standard       |
| AC 02.3             | All attempts logged (success + failure)                                                               | Data integrity      | Regression Analysis                   | Medium     | Smoke          |
| AC 02.3             | All 3 attempts fail → failure logged clearly                                                          | Data integrity      | Negative Testing                      | Medium     | Standard       |
| AC 03.1             | Notification deep-links to correct Lesson Detail page                                                 | Cross-system impact | Regression Analysis                   | High       | Standard       |
| AC 03.1 / [Gap #11] | User not logged in taps notification → redirect flow (confirm with product)                           | Cross-system impact | Decision Table                        | Medium     | Standard       |
| AC 03.1 / [Gap #10] | Parent on Student B receives notification for Student A → switch/stay behavior (confirm with product) | Cross-system impact | Decision Table                        | High       | Standard       |
| PRD                 | User without custom permission "Publish Lesson With Notification" → button hidden                     | Conditional logic   | Decision Table                        | High       | Standard       |
| PRD                 | User with custom permission (Renseikai OOP PS member); user without permission (other partner)        | Permission logic    | Permission Matrix                     | High       | Standard       |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area                                       | Reason                                                                                                                                                                                                                                                | Recommended Approach                                                                                                                                                                      |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AC 02.1 — Draft → Published via new button | New alternative publish path that must co-exist with the existing Publish button. If broken: lesson doesn't publish OR publishes without modal. Existing TC-1456 / TC-9786–9791 cover only the original publish path — regression risk on both paths. | Test new button path as a distinct state transition. Also run existing Draft→Published TCs to confirm original path is unaffected.                                                        |
| AC 02.1 — Notification recipient lookup    | If relationship query is incorrect, a parent or student may silently miss a notification. No UI feedback on delivery failure makes this hard to detect in QA.                                                                                         | Test with: (a) student + 1 parent, (b) student + multiple parents, (c) student with no parent, (d) multiple students assigned. Inspect recipient list and notification delivery per case. |
| AC 02.2 — Send trigger                     | If modal "Send" does not actually trigger the notification pipeline (e.g. API call omitted), the entire feature silently fails while the UI looks correct.                                                                                            | Verify API call is made and notification arrives on device after clicking Send.                                                                                                           |

### 🟠 High Risk

| Area                                          | Reason                                                                                                                                                                    | Recommended Approach                                                                                                                                                                                        |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AC 01.1 — Button visibility on wrong statuses | If button is shown for Completed/Cancelled lessons, users could accidentally trigger notification for non-active lessons.                                                 | Test all lesson statuses explicitly: Draft ✅, Published ✅, Completed ❌, Cancelled ❌.                                                                                                                    |
| AC 02.2 + Gap #6 — Don't Send on Draft        | AC 02.1 states Draft lesson is published BEFORE modal appears. If "Don't Send" reverts the status or causes an inconsistency, the feature creates a state management bug. | Test click "Don't Send" after Draft publish: verify lesson status = Published, no notification received.                                                                                                    |
| AC 03.1 + Gap #10 — Switch student deep-link  | Parent on Student B tapping Student A's notification must not see Student B's lesson. If app context doesn't switch, parent may believe Student B's lesson was published. | Execute: parent logged into app viewing Student B → receive notification for Student A → tap notification → verify app switches to Student A's lesson detail. Confirm expected behavior with product first. |
| AC 02.3 — No duplicate on retry               | Duplicate notifications are a direct UX complaint risk. If idempotency guard fails on retry success, student/parent receives 2+ notifications for the same lesson.        | Verify idempotency key exists on notification payload or at delivery layer.                                                                                                                                 |
| PRD — Custom Permission                       | If permission assignment fails: Renseikai users lose the button, or users without permission unexpectedly gain it.                                                        | Test: (a) user with "Publish Lesson With Notification" permission → button visible; (b) user without permission → button hidden.                                                                            |

### 🟡 Medium Risk

| Area                                        | Reason                                                                                                                                                 | Recommended Approach                                                                                                                                                 |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AC 02.1 + Gap #4 — No device token          | Expected behavior is silent skip, but if the system throws an error instead, the entire notification flow may break for all recipients in that lesson. | Test with a student/parent account that has never logged into the app; verify no error on SF side and notification still reaches other recipients with valid tokens. |
| AC 02.3 — Retry + logging                   | Audit logging is internal; not visible to QA via UI. Risk is operational (silent failures undetected).                                                 | Verify via backend logs or admin dashboard that entries exist after a simulated failure.                                                                             |
| AC 03.1 + Gap #11 — Not logged in deep-link | Edge case for first-time users. If deep-link sends to unknown route, users may be confused or see a blank screen.                                      | Tap notification on fresh-install state; confirm redirect behavior (login screen → lesson detail, or app home). Confirm expected behavior with product.              |
| AC 02.1 — JP notification content           | Cosmetic but high-visibility for Renseikai (JP-only partner). Wrong translations cause trust issues.                                                   | Verify JP title and body text match the translation table exactly.                                                                                                   |

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area                                                                                     | Existing Test Case                                                | Overlap                                                        | New Coverage Needed                                                              |
| -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------------------------- |
| Button visibility per lesson status                                                          | None                                                              | None                                                           | ✅ New TCs: Draft, Published, Completed, Cancelled                               |
| Click on Draft → publish + modal                                                             | TC-1456, TC-9786–9791 (Draft→Published without notification path) | Partial — existing TCs cover original Publish button path only | ✅ New TC for new button path; existing TCs need regression check                |
| Click on Published → modal only                                                              | None                                                              | None                                                           | ✅ New TC                                                                        |
| Confirmation modal content + Send/Don't Send                                                 | None                                                              | None                                                           | ✅ New TCs                                                                       |
| Don't Send on Draft → lesson stays Published                                                 | None                                                              | None                                                           | ✅ New TC (verify + share with product)                                          |
| Notification recipients: student + parents                                                   | None                                                              | None                                                           | ✅ New TCs (multiple parent cases)                                               |
| No parent linked → student only                                                              | None                                                              | None                                                           | ✅ New TC (verify result + share with product)                                   |
| Multiple students under same parent                                                          | None                                                              | None                                                           | ✅ New TC — confirm each student gets separate notification                      |
| Parent has multiple accounts                                                                 | None                                                              | None                                                           | ✅ New TC — confirm all accounts notified (share expected behavior with product) |
| No device token → silent skip                                                                | None                                                              | None                                                           | ✅ New TC (verify + share with product)                                          |
| Notification content format (EN + JP)                                                        | None                                                              | None                                                           | ✅ New TCs                                                                       |
| Retry on failure (3 attempts)                                                                | None                                                              | None                                                           | ✅ New TC                                                                        |
| No duplicate on retry success                                                                | None                                                              | None                                                           | ✅ New TC                                                                        |
| All attempts logged                                                                          | None                                                              | None                                                           | ✅ New TC (Smoke)                                                                |
| All 3 attempts fail → failure logged                                                         | None                                                              | None                                                           | ✅ New TC                                                                        |
| Deep-link to Lesson Detail                                                                   | None                                                              | None                                                           | ✅ New TCs                                                                       |
| Switch-student: notification for other student                                               | None                                                              | None                                                           | ✅ New TC (verify + share with product)                                          |
| Not logged in + tap notification                                                             | None                                                              | None                                                           | ✅ New TC (verify + share with product)                                          |
| User without "Publish Lesson With Notification" permission → button hidden                   | None                                                              | None                                                           | ✅ New TC                                                                        |
| User with permission (Renseikai OOP PS); user without permission (other partner / no OOP PS) | None                                                              | None                                                           | ✅ New TC (Permission Matrix)                                                    |

---

## 7. Suggested Test Suite Structure

```
output/test-cases/lesson-management/lesson/publish-notify-student/
├── button-visibility.md
│     → AC 01.1 — Button visibility per lesson status (Draft, Published, Completed, Cancelled)
│     → PRD — Custom permission "Publish Lesson With Notification" (with permission / without permission)
│     → PRD — Per-partner flag (Renseikai vs. other)
│
├── send-notification.md
│     → AC 02.1 — Click on Draft lesson: publish + modal flow
│     → AC 02.1 — Click on Published lesson: modal only (no status change)
│     → AC 02.2 — Modal content, Send / Don't Send actions
│     → Gap #6 — Don't Send on Draft: lesson remains Published
│
├── notification-recipients.md
│     → AC 02.1 — Recipients: student + all linked parents
│     → Gap #3 — No parent linked: student only
│     → Gap #4 — No device token: silent skip
│     → Multiple students same parent / parent multiple accounts
│
├── notification-content.md
│     → AC 02.1 — Notification title + body content (EN)
│     → AC 02.1 — Notification title + body content (JP)
│
├── retry-mechanism.md
│     → AC 02.3 — Retry on failure (up to 3 attempts)
│     → AC 02.3 — No duplicate on retry success
│     → AC 02.3 — Audit logging per attempt
│     → AC 02.3 — All 3 attempts fail: failure logged
│
└── deep-link-navigation.md
      → AC 03.1 — Notification deep-links to correct Lesson Detail page
      → Gap #11 — Not logged in: redirect flow
      → Gap #10 — Switch-student: parent on Student B taps Student A notification
```

**Estimated total:** ~25–30 test cases

---

## 8. Notes for Test Case Authors

> **ℹ️ PERMISSION-BASED CONTROL (BR 21, 22):** Button visibility is controlled by the custom permission **"Publish Lesson With Notification"**, which is added to the Renseikai OOP Permission Set (PS) on the first release. Other partners do not receive this permission by default. Test cases for permission-based visibility should verify: (a) user with this permission sees the button, (b) user without this permission does not see the button.

> **⚠️ CONFIRM WITH PRODUCT before creating execution records for:**
>
> - No parent linked → student-only notification (Gap #3)
> - Don't Send on Draft → lesson status after action (Gap #6)
> - Switch-student: parent viewing Student B taps Student A notification (Gap #10)
> - Not logged in + deep-link tap (Gap #11)
>   After testing, share actual behavior to product for confirmation of expected behavior.

> **🔁 REGRESSION RISK:** Existing TCs TC-1456, TC-9786–9791 (Draft→Published via original Publish button) must still pass after this feature is released. Add a regression check step to confirm the original publish button path is unaffected by the new button.
