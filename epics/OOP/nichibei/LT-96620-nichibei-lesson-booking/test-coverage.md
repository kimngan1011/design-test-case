# Test Coverage: LT-96620 — [Nichibei] Lesson Booking System

**Jira:** https://manabie.atlassian.net/browse/LT-96620
**Date:** 2026-05-05

---

## 1. Business Rules Extracted

| #   | AC         | Business Rule                                                                              |
| --- | ---------- | ------------------------------------------------------------------------------------------ |
| 1   | AC 01.1    | Booking List shows ONLY Booking Flag=TRUE sessions, lesson_date >= today                   |
| 2   | AC 01.1    | Browse Lessons (+) button visible ONLY when student has active LA                          |
| 3   | AC 01.1    | Cancel button ENABLED within deadline; DISABLED with tooltip past deadline                 |
| 4   | AC 02.2    | Lesson visible: location linked to student's active LA                                     |
| 5   | AC 02.2    | Lesson visible: Bookable Flag = TRUE                                                       |
| 6   | AC 02.2    | Lesson visible: status = Draft OR Published                                                |
| 7   | AC 02.2    | Lesson visible: date >= today + X days (partner config)                                    |
| 8   | AC 02.3    | Location filter shows only student's active LA locations                                   |
| 9   | AC 02.4    | Reserve button ENABLED: not allocated + bookable + not full + within deadline              |
| 10  | AC 02.4    | Reserve button DISABLED: lesson full OR past deadline                                      |
| 11  | AC 02.4    | No button shown for staff-allocated lessons (Booking Flag OFF/blank)                       |
| 12  | AC 03.2    | Booking is ATOMIC: validate → create session → save remarks → auto-publish                 |
| 13  | AC 03.2    | Draft lesson → auto-Published (silent, no notification) when booked                        |
| 14  | AC 03.2    | Remarks prefixed "Booking Note: " on Attendance_Response_Remark field                      |
| 15  | AC 03.2    | LA selection priority: active → location match → earliest start → earliest created         |
| 16  | AC 03.3    | Duplicate allocation blocked: "You have already reserved this lesson."                     |
| 17  | AC 03.3    | Capacity full blocked: "This lesson is now full. Please choose another lesson."            |
| 18  | AC 03.3    | Past booking deadline blocked: "The booking deadline has passed for this lesson."          |
| 19  | AC 03.3    | No active LA blocked: "You are not eligible to reserve lessons at this time."              |
| 20  | AC 03.3    | Insufficient points blocked: "Remaining points are insufficient to book this lesson."      |
| 21  | AC 03.4    | SF notification to assigned teacher within 30s on booking (app-only)                       |
| 22  | AC 04.2    | Cancel button ENABLED within X hours before lesson start; DISABLED + tooltip past deadline |
| 23  | AC 04.4    | Cancel is ATOMIC: delete session → remove from Booking List → notify teacher               |
| 24  | AC 04.4    | SF notification to assigned teacher within 30s on cancellation (app-only)                  |
| 25  | AC 06.1    | Bookable Flag OFF: existing Student Sessions are unaffected (no cascading deletion)        |
| 26  | PRD/Tech   | Deadline evaluation uses LESSON timezone, not user device timezone                         |
| 27  | PRD/Tech   | Capacity check uses optimistic locking (re-validated at submission time)                   |
| 28  | PRD/Config | Feature disabled by default; Lesson Booking menu hidden when disabled                      |
| 29  | Confirmed  | Parent users CANNOT access Lesson Booking — Student scope only                             |
| 30  | Confirmed  | Auto-publish on booking is SILENT — no push notification triggered                         |
| 31  | Confirmed  | Points calculation = same as existing Nichibei manual assignment mechanism                 |
| 32  | Confirmed  | Auto-published lesson stays Published after all bookings cancelled — no revert to Draft    |

---

## 2. Logic Type Categorization

| AC         | Business Rule #    | Logic Type                                                    |
| ---------- | ------------------ | ------------------------------------------------------------- |
| AC 01.1    | 1                  | Conditional logic, Data integrity                             |
| AC 01.1    | 2                  | Conditional logic, Permission logic                           |
| AC 01.1    | 3                  | Boundary/range logic, State transition                        |
| AC 02.2    | 4, 5, 6, 7         | Conditional logic (ALL conditions must be met simultaneously) |
| AC 02.3    | 8                  | Conditional logic, Permission logic                           |
| AC 02.4    | 9, 10, 11          | Conditional logic, State transition                           |
| AC 03.2    | 12                 | Data integrity, State transition                              |
| AC 03.2    | 13                 | State transition, Conditional logic                           |
| AC 03.2    | 14                 | Validation logic                                              |
| AC 03.2    | 15                 | Conditional logic (priority chain)                            |
| AC 03.3    | 16, 17, 18, 19, 20 | Validation logic, Boundary/range logic                        |
| AC 03.4    | 21                 | Cross-system impact                                           |
| AC 04.2    | 22                 | Boundary/range logic, State transition                        |
| AC 04.4    | 23                 | Data integrity, State transition                              |
| AC 04.4    | 24                 | Cross-system impact                                           |
| AC 05.1/2  | 21, 24             | Cross-system impact                                           |
| AC 06.1    | 25                 | Data integrity, Conditional logic                             |
| PRD/Tech   | 26                 | Boundary/range logic                                          |
| PRD/Tech   | 27                 | Data integrity                                                |
| PRD/Config | 28                 | Permission logic, Conditional logic                           |
| Confirmed  | 29                 | Permission logic                                              |
| Confirmed  | 30                 | State transition                                              |
| Confirmed  | 31                 | Validation logic                                              |
| Confirmed  | 32                 | State transition                                              |

---

## 3. Test Technique Selection

| Logic Type           | Applicable Techniques                      |
| -------------------- | ------------------------------------------ |
| Conditional logic    | Decision Table, Negative Testing           |
| Boundary/range logic | Boundary Value Analysis, Negative Testing  |
| State transition     | State Transition Testing, CRUD Testing     |
| Validation logic     | Equivalence Partitioning, Negative Testing |
| Data integrity       | CRUD Testing, Regression Analysis          |
| Permission logic     | Permission Matrix                          |
| Cross-system impact  | Regression Analysis, CRUD Testing          |

---

## 4. Structured Coverage Strategy

| AC         | Business Rule Summary                                                                          | Logic Type                             | Test Technique                   | Risk Level | Coverage Depth |
| ---------- | ---------------------------------------------------------------------------------------------- | -------------------------------------- | -------------------------------- | ---------- | -------------- |
| AC 01.1    | Booking List — filter: Booking Flag=TRUE + date >= today                                       | Conditional logic                      | Decision Table                   | High       | Standard       |
| AC 01.1    | Browse Lessons button — visible with active LA, hidden without                                 | Conditional logic, Permission logic    | Decision Table                   | Medium     | Standard       |
| AC 01.1    | Cancel button on Booking List — enabled/disabled by deadline                                   | Boundary/range logic, State transition | BVA                              | High       | Deep           |
| AC 02.1    | No active LA → empty state; active LA → show list                                              | Conditional logic                      | Decision Table                   | Medium     | Standard       |
| AC 02.2    | Lesson visibility: all 4 conditions must be met                                                | Conditional logic                      | Decision Table                   | High       | Deep           |
| AC 02.3    | Location filter restricted to student's LA locations                                           | Conditional logic                      | Decision Table, Negative Testing | Medium     | Standard       |
| AC 02.3    | All filter types work independently and in combination                                         | Conditional logic                      | Pairwise Testing                 | Medium     | Standard       |
| AC 02.4    | Reserve button — 5 distinct states (enabled/disabled/no button/cancel-enabled/cancel-disabled) | State transition, Conditional logic    | Decision Table                   | High       | Deep           |
| AC 03.1    | Booking Confirmation Screen — all required fields shown                                        | Validation logic                       | Equivalence Partitioning         | Medium     | Standard       |
| AC 03.2    | Booking atomic flow — happy path (validate → session → remarks → publish)                      | Data integrity, State transition       | CRUD Testing                     | Critical   | Deep           |
| AC 03.2    | Draft → Published auto-transition on booking (silent, no notification)                         | State transition, Conditional logic    | State Transition Testing         | Critical   | Deep           |
| AC 03.2    | Remarks saved with "Booking Note: " prefix                                                     | Validation logic                       | Equivalence Partitioning         | Medium     | Standard       |
| AC 03.2    | LA selection priority chain (4-level rule)                                                     | Conditional logic                      | Decision Table                   | High       | Deep           |
| AC 03.3    | Duplicate allocation blocked (correct error message)                                           | Validation logic                       | Negative Testing                 | Critical   | Deep           |
| AC 03.3    | Capacity full blocked                                                                          | Boundary/range logic                   | BVA, Negative Testing            | Critical   | Deep           |
| AC 03.3    | Past booking deadline blocked                                                                  | Boundary/range logic                   | BVA, Negative Testing            | High       | Deep           |
| AC 03.3    | No active LA blocked                                                                           | Validation logic                       | Negative Testing                 | High       | Standard       |
| AC 03.3    | Insufficient points blocked                                                                    | Validation logic                       | Negative Testing                 | High       | Standard       |
| AC 03.4    | Post-booking: success screen + Booking List updated + teacher notified                         | Cross-system impact                    | CRUD Testing                     | High       | Standard       |
| AC 03.4    | Teacher SF notification within 30s (app booking only, not SF assignment)                       | Cross-system impact                    | Regression Analysis              | High       | Standard       |
| AC 04.1    | Cancel entry points: Booking List + Lesson List (Booking Flag=TRUE only)                       | Conditional logic                      | Decision Table                   | Medium     | Standard       |
| AC 04.2    | Cancel deadline — enabled/disabled + tooltip                                                   | Boundary/range logic, State transition | BVA                              | High       | Deep           |
| AC 04.3    | Cancel confirmation dialog — correct UI content                                                | Validation logic                       | Equivalence Partitioning         | Low        | Smoke          |
| AC 04.4    | Cancel atomic flow — session deleted + list updated + teacher notified                         | Data integrity, State transition       | CRUD Testing                     | Critical   | Deep           |
| AC 04.4    | Auto-published lesson stays Published after cancellation                                       | State transition                       | State Transition Testing         | High       | Standard       |
| AC 05.1    | Teacher notified within 30s on booking                                                         | Cross-system impact                    | CRUD Testing                     | High       | Standard       |
| AC 05.2    | Teacher notified within 30s on cancellation                                                    | Cross-system impact                    | CRUD Testing                     | High       | Standard       |
| AC 06.1    | Bookable Flag ON/OFF — existing sessions unaffected when turned OFF                            | Data integrity, Conditional logic      | CRUD Testing, Negative Testing   | High       | Standard       |
| PRD/Tech   | Deadline uses lesson timezone, not device timezone                                             | Boundary/range logic                   | BVA                              | High       | Standard       |
| PRD/Config | Feature disabled → Lesson Booking menu hidden                                                  | Permission logic                       | Decision Table                   | Medium     | Standard       |
| Confirmed  | Parent cannot access Lesson Booking                                                            | Permission logic                       | Permission Matrix                | High       | Standard       |
| Confirmed  | Auto-publish silent (no notification triggered)                                                | State transition                       | State Transition Testing         | High       | Standard       |
| Confirmed  | Points calc = Nichibei existing mechanism                                                      | Validation logic                       | Regression Analysis              | High       | Standard       |
| Confirmed  | Lesson stays Published after all bookings cancelled                                            | State transition                       | State Transition Testing         | High       | Standard       |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area                                        | Reason                                                                                                                                                                                                         | Recommended Approach                                                                                             |
| ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| AC 03.2 — Booking atomic flow               | Creating a Student Session is a data write that also triggers auto-publish and remarks. Partial failure (session created, publish failed) or reverse order could corrupt state.                                | CRUD Testing with network interruption simulation; verify all side-effects either all complete or all roll back. |
| AC 03.2 — Draft → Published auto-transition | Auto-publish is silent (confirmed). If notification is erroneously triggered, it affects ALL assigned students, not just the booking student. Must verify lesson publish event does not trigger LT-96662 flow. | State Transition Testing: book a Draft lesson; verify Published; verify no push notification sent to any device. |
| AC 03.3 — Duplicate allocation              | A student booking twice (race condition or double-tap) could create duplicate Student Sessions. Given 2026-04-13 Aso incident (1,655 duplicates), this is a known systemic risk.                               | Negative Testing with rapid double-submission; verify only one session created and second attempt returns error. |
| AC 03.3 — Capacity full                     | Optimistic locking means two students can hit "Reserve" simultaneously on the last seat. The second must be rejected cleanly.                                                                                  | BVA at capacity boundary (capacity=1, 2 students submit at same time); verify only one succeeds.                 |
| AC 04.4 — Cancel atomic flow                | Cancellation deletes a Student Session. If deletion succeeds but notification fails, teacher is unaware. If deletion fails but UI shows "cancelled", student believes booking is gone but it persists.         | CRUD Testing: verify session physically deleted in SF after cancel. Verify Booking List no longer shows lesson.  |

### 🟠 High Risk

| Area                                       | Reason                                                                                                                                                                                    | Recommended Approach                                                                                                          |
| ------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| AC 02.2 — All 4 visibility conditions      | All conditions must be met simultaneously. A lesson could appear incorrectly if any single condition check has a bug (e.g., Draft lesson shown to a student with no LA at that location). | Decision Table: test each condition violated individually while others pass; verify lesson hidden.                            |
| AC 02.4 — Reserve button states            | 5 distinct states depend on: allocated status, Bookable Flag, capacity, deadline. Wrong button state could allow double-booking or block eligible students.                               | Decision Table: each of the 5 states tested independently with exact preconditions.                                           |
| AC 03.2 — LA selection priority            | When student has multiple active LAs, wrong LA selection leads to incorrect point deduction from wrong LA. 4-level priority chain must be tested exhaustively.                            | Decision Table: test each priority level — when two LAs have same priority at level N, verify level N+1 breaks tie correctly. |
| AC 03.3 — Past booking deadline (timezone) | Deadline evaluation uses LESSON timezone. A student in a different timezone could see different button state than expected if device timezone is used by mistake.                         | BVA: test at exact deadline boundary using lesson timezone; verify correct rejection.                                         |
| AC 06.1 — Bookable Flag OFF non-cascading  | Turning OFF Bookable Flag must not delete existing Student Sessions. Critical for data integrity — existing bookings must be preserved.                                                   | CRUD: create sessions → turn OFF Bookable Flag → verify sessions still exist in SF.                                           |
| Confirmed — Auto-published stays Published | After last booking cancelled, lesson remains Published. Staff must manually manage this. If lesson erroneously reverts to Draft, it becomes invisible on Mobile.                          | State Transition: book Draft lesson → auto-publish → cancel booking → verify lesson still Published.                          |

### 🟡 Medium Risk

| Area                              | Reason                                                                                                                                                                                   | Recommended Approach                                                                                               |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| AC 02.3 — Filters                 | Filter combinations (location + date + bookable-only + teacher) could interact incorrectly, especially "Bookable Only" toggle which checks capacity + student allocation simultaneously. | Pairwise Testing: combine Bookable Only toggle with Location and Date filters; verify correct lesson subset shown. |
| AC 01.1 — Cancel button tooltip   | Tooltip text must appear when Cancel is disabled past deadline. Missing tooltip leaves student with no feedback.                                                                         | BVA at cancellation deadline boundary; verify tooltip content matches exact spec text.                             |
| PRD/Config — Feature disabled     | When feature is disabled, Lesson Booking menu must not appear at all in app navigation.                                                                                                  | Decision Table: disabled partner config → verify menu absent; enabled → verify menu present.                       |
| Confirmed — Parent access blocked | Parent user accessing the app must not see Lesson Booking menu.                                                                                                                          | Permission Matrix: login as parent → verify no Lesson Booking menu; login as student → verify menu present.        |

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area                                    | Existing Test Case                                                                       | Overlap | New Coverage Needed                                               |
| ------------------------------------------- | ---------------------------------------------------------------------------------------- | ------- | ----------------------------------------------------------------- |
| AC 01.1 — Booking List display              | None                                                                                     | None    | ✅ Booking List with bookings / empty state / no-LA state         |
| AC 01.1 — Browse button visibility          | None                                                                                     | None    | ✅ With active LA (visible) / no active LA (inactive)             |
| AC 01.1 — Cancel button state (deadline)    | None                                                                                     | None    | ✅ Within deadline (enabled) / past deadline (disabled + tooltip) |
| AC 02.1 — Prerequisites gate                | None                                                                                     | None    | ✅ No active LA → empty state message                             |
| AC 02.2 — All 4 visibility conditions       | None                                                                                     | None    | ✅ Each condition violated individually                           |
| AC 02.3 — Filter functionality              | None                                                                                     | None    | ✅ Each filter type + combinations                                |
| AC 02.4 — Reserve button 5 states           | None                                                                                     | None    | ✅ Each of the 5 states independently                             |
| AC 03.1 — Booking Confirmation Screen       | None                                                                                     | None    | ✅ All fields shown correctly                                     |
| AC 03.2 — Happy path booking                | None                                                                                     | None    | ✅ Full booking flow end-to-end                                   |
| AC 03.2 — Auto-publish Draft lesson         | None                                                                                     | None    | ✅ Draft → Published on booking + silent (no notification)        |
| AC 03.2 — Remarks saved with prefix         | None                                                                                     | None    | ✅ With remarks / without remarks                                 |
| AC 03.2 — LA selection priority             | Partial: `nichibei-assign-student-lesson-number.md` (manual assignment — different flow) | Partial | ✅ All 4 priority levels for app-booking LA selection             |
| AC 03.3 — All 5 validation errors           | None                                                                                     | None    | ✅ Each error individually with exact error message               |
| AC 03.4 — Post-booking state                | None                                                                                     | None    | ✅ Success screen + Booking List update                           |
| AC 03.4 — Teacher SF notification           | None                                                                                     | None    | ✅ Notification content + timing                                  |
| AC 04.1 — Cancel entry points               | None                                                                                     | None    | ✅ From Booking List / from Lesson List                           |
| AC 04.2 — Cancel deadline (BVA)             | None                                                                                     | None    | ✅ Within / at / past cancellation deadline                       |
| AC 04.3 — Cancel dialog content             | None                                                                                     | None    | ✅ Dialog title, message, button labels                           |
| AC 04.4 — Cancel flow + stays Published     | None                                                                                     | None    | ✅ Session deleted + list updated + lesson stays Published        |
| AC 04.4 — Teacher SF notification on cancel | None                                                                                     | None    | ✅ Notification content + timing                                  |
| AC 05.1/05.2 — SF notifications             | None                                                                                     | None    | ✅ Booking + cancel notifications (app-only, not SF assignment)   |
| AC 06.1 — Bookable Flag CRUD                | None                                                                                     | None    | ✅ ON/OFF toggle + non-cascading behavior                         |
| PRD/Tech — Timezone boundary                | None                                                                                     | None    | ✅ Deadline at lesson timezone boundary                           |
| PRD/Config — Feature disabled               | None                                                                                     | None    | ✅ Menu hidden when disabled                                      |
| Confirmed — Parent access blocked           | None                                                                                     | None    | ✅ Parent cannot see/access Lesson Booking                        |
| Confirmed — Auto-publish silent             | None                                                                                     | None    | ✅ No notification triggered on auto-publish                      |
| Confirmed — Lesson stays Published          | None                                                                                     | None    | ✅ Post-cancellation Published state persists                     |

---

## 7. Suggested Test Suite Structure

```
output/test-cases/lesson-management/oop/nichibei-lesson-booking/
├── booking-list.md
│   → AC 01.1 — Booking List screen display, browse button visibility,
│                cancel button state on booking cards
│
├── lesson-browse.md
│   → AC 02.1, AC 02.2, AC 02.3, AC 02.4
│     — Prerequisites gate, lesson visibility conditions,
│       filter functionality, lesson card action button states
│
├── book-lesson.md
│   → AC 03.1, AC 03.2, AC 03.3, AC 03.4
│     — Confirmation screen, booking atomic flow, validation errors,
│       auto-publish, LA selection, remarks, post-booking state
│
├── cancel-booking.md
│   → AC 04.1, AC 04.2, AC 04.3, AC 04.4
│     — Cancel entry points, deadline constraints, confirm dialog,
│       cancel atomic flow, lesson stays Published
│
├── teacher-notification.md
│   → AC 05.1, AC 05.2
│     — SF teacher notifications on booking and cancellation
│
└── bookable-flag-config.md
    → AC 06.1, PRD/Config, Confirmed (parent, feature-disabled)
      — Bookable Flag ON/OFF, feature enable/disable, parent access guard
```
