# Test Coverage: LT-96673 — Monthly Lesson Count in Add Teacher Popup & Calendar Teacher Details

**Jira:** https://manabie.atlassian.net/browse/LT-96673
**Partner:** Riso (OOP)
**Date:** 2026-04-16

---

## 1. Business Rules Extracted

| #   | AC                | Business Rule                                                                                                                                                   |
| --- | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | AC 01.1           | New custom field 'Monthly Lesson Count' created on Lesson Teacher SF object                                                                                     |
| 2   | AC 01.2           | New column 'Monthly Lesson Count' (今月の授業数) appears in the Add Teacher popup                                                                               |
| 3   | AC 01.2           | Count = lessons (status: Draft/Published/Completed) teacher is assigned to during selected lesson's month                                                       |
| 4   | AC 01.2           | Cancelled lessons are EXCLUDED from the count                                                                                                                   |
| 5   | AC 01.2           | Count populates when popup opens; NOT updated in real-time; applying filters does NOT refresh the count                                                         |
| 6   | AC 01.2           | Teacher with zero lessons in the month shows 0 (not blank)                                                                                                      |
| 7   | AC 01.2           | Count includes lessons from ALL locations teacher is assigned to (cross-location)                                                                               |
| 8   | AC 01.2           | No role restriction — all SF users who can open the Add Teacher popup see the Monthly Lesson Count column                                                       |
| 9   | AC 01.2           | Monthly Lesson Count column is NOT sortable                                                                                                                     |
| 10  | AC 01.2           | Add Teacher popup count uses SELECTED LESSON's month as reference (not today's month)                                                                           |
| 11  | AC 01.3           | Monthly Lesson Count shown in Teacher Details panel on SF Lesson Calendar (existing UI)                                                                         |
| 12  | AC 01.3           | Calendar Teacher Details count always uses TODAY's month regardless of calendar view month                                                                      |
| 13  | AC 01.3           | Calendar count is static per session — navigation to other months does not change it                                                                            |
| 14  | AC 01.2 + AC 01.3 | Month boundary uses lesson datetime in UI local timezone (NOT raw UTC stored value); lessons near month boundary must be counted in the locally-displayed month |

---

## 2. Logic Type Categorization

| AC                | Business Rule # | Logic Type                              |
| ----------------- | --------------- | --------------------------------------- |
| AC 01.1           | 1               | Data integrity                          |
| AC 01.2           | 2               | Cross-system impact                     |
| AC 01.2           | 3               | Conditional logic, Boundary/range logic |
| AC 01.2           | 4               | Conditional logic                       |
| AC 01.2           | 5               | Conditional logic                       |
| AC 01.2           | 6               | Boundary/range logic                    |
| AC 01.2           | 7               | Conditional logic, Data integrity       |
| AC 01.2           | 8               | Permission logic                        |
| AC 01.2           | 9               | Validation logic                        |
| AC 01.2           | 10              | Conditional logic, Boundary/range logic |
| AC 01.3           | 11              | Cross-system impact                     |
| AC 01.3           | 12              | Conditional logic                       |
| AC 01.3           | 13              | State transition, Conditional logic     |
| AC 01.2 + AC 01.3 | 14              | Boundary/range logic, Data integrity    |

---

## 3. Test Technique Selection

| Logic Type           | Applicable Techniques                      |
| -------------------- | ------------------------------------------ |
| Conditional logic    | Decision Table, Negative Testing           |
| Boundary/range logic | Boundary Value Analysis, Negative Testing  |
| State transition     | State Transition Testing                   |
| Permission logic     | Permission Matrix                          |
| Validation logic     | Equivalence Partitioning, Negative Testing |
| Data integrity       | CRUD Testing, Regression Analysis          |
| Cross-system impact  | Regression Analysis, CRUD Testing          |

---

## 4. Structured Coverage Strategy

| AC                | Business Rule Summary                              | Logic Type                           | Test Technique                            | Risk Level | Coverage Depth |
| ----------------- | -------------------------------------------------- | ------------------------------------ | ----------------------------------------- | ---------- | -------------- |
| AC 01.1           | New field on Lesson Teacher object                 | Data integrity                       | CRUD Testing                              | High       | Standard       |
| AC 01.2           | Column visible in Add Teacher popup                | Cross-system impact                  | Regression Analysis                       | High       | Standard       |
| AC 01.2           | Count = Draft/Published/Completed lessons in month | Conditional logic                    | Decision Table, Equivalence Partitioning  | Critical   | Deep           |
| AC 01.2           | Cancelled lessons excluded from count              | Conditional logic                    | Decision Table, Negative Testing          | High       | Standard       |
| AC 01.2           | Count fixed at popup open; filter does NOT refresh | Conditional logic                    | Decision Table, Negative Testing          | High       | Standard       |
| AC 01.2           | Zero lessons shows 0 (not blank)                   | Boundary/range logic                 | Boundary Value Analysis                   | Medium     | Standard       |
| AC 01.2           | Count across ALL locations (cross-location)        | Conditional logic, Data integrity    | Decision Table                            | High       | Standard       |
| AC 01.2           | No role restriction — all roles see column         | Permission logic                     | Permission Matrix                         | Medium     | Standard       |
| AC 01.2           | Column is NOT sortable                             | Validation logic                     | Negative Testing                          | Low        | Smoke          |
| AC 01.2           | Reference month = selected lesson's month          | Conditional logic, Boundary logic    | Decision Table, Boundary Value Analysis   | High       | Standard       |
| AC 01.3           | Count shown in Calendar Teacher Details panel      | Cross-system impact                  | Regression Analysis                       | High       | Standard       |
| AC 01.3           | Always today's month (not calendar view month)     | Conditional logic                    | Decision Table, State Transition Testing  | High       | Deep           |
| AC 01.3           | Navigation does not change count                   | State transition                     | State Transition Testing                  | High       | Standard       |
| AC 01.2 + AC 01.3 | Month boundary uses local timezone not UTC         | Boundary/range logic, Data integrity | Boundary Value Analysis, Negative Testing | Critical   | Deep           |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area                            | Reason                                                                                                                                                                                                | Recommended Approach                                                                                                                                                            |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Count calculation accuracy (R3) | Core feature value — if count is wrong, staff assign overloaded teachers. Wrong statuses counted or excluded causes silent data inaccuracy                                                            | Decision Table covering all 4 status combinations: (1) only Draft, (2) only Cancelled, (3) Draft+Published+Completed, (4) mixed including Cancelled; verify count value in each |
| Timezone / month boundary (R14) | Lesson stored as UTC in DB; for JST users, a lesson at 11:30pm Jan 31 = Feb 1 UTC. If system uses UTC date, lesson is counted in February (wrong). Silent data accuracy failure with no visible error | BVA: test lesson on last day of month at e.g. 11:30pm local; test lesson on first day of month at e.g. 12:30am local; confirm count uses UI-displayed date, not UTC             |

### 🟠 High Risk

| Area                                         | Reason                                                                                                                                                                                | Recommended Approach                                                                                                                                                            |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Calendar always uses today's month (R12–R13) | UX confusion risk: user navigating to last month in Calendar may expect count to update. If dev accidentally uses calendar view month, count is wrong for the navigated month         | State Transition: open Calendar, navigate to previous month, navigate to next month — verify count value stays unchanged across all nav transitions                             |
| Filter does NOT refresh count (R5)           | AC originally said "may update" — confirmed as NOT updating. If dev implements refresh on filter, the count would change unexpectedly                                                 | Decision Table: apply each filter type (location, working type, subject, working hours) after noting the initial count; verify count is unchanged after each filter application |
| Cross-location scope (R7)                    | If dev accidentally scopes count to current lesson's location only, teachers with cross-location assignments will show lower-than-actual counts, leading to false overwork assessment | Test teacher assigned to 3 lessons at Location A and 2 lessons at Location B; open popup for Location A lesson → count must show 5                                              |
| Selected lesson month reference (R10)        | If dev uses today's month instead of selected lesson's month, a lesson created for a past/future month will show wrong count                                                          | Open popup on a lesson in January; verify count shows January lessons (not current month lessons)                                                                               |
| Regression on TC-1219 (filter)               | New field added to Lesson Teacher object may affect popup load query performance or list behavior                                                                                     | Re-run TC-1219 filter flow; verify filter still works and count is visible after filtering                                                                                      |

### 🟡 Medium Risk

| Area                     | Reason                                                                                                            | Recommended Approach                                                                                    |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Zero-lesson display (R6) | Showing blank instead of 0 would mislead staff into thinking the count was not loaded or the teacher is not valid | EP: teacher with 0 lessons in selected month → verify cell shows "0", not empty                         |
| No role restriction (R8) | If roles were accidentally locked to CM/HQ only (as the US says), Centre Staff would not see the column           | Permission Matrix: log in as Centre Staff (SPU login), open Add Teacher popup, verify column is visible |
| Column not sortable (R9) | Low risk — UI behavior; if sortable it's a minor unintended feature, not a data issue                             | Negative test: click column header, verify list order does not change                                   |

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area                                          | Existing Test Case   | Overlap                                                                          | New Coverage Needed                                                 |
| ------------------------------------------------- | -------------------- | -------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Add Teacher popup — column visible                | TC-1214 (view popup) | Partial — TC-1214 checks popup opens; does not check Monthly Lesson Count column | ✅ New: verify column appears and displays a number                 |
| Count calculation (Draft/Published/Completed)     | None                 | None                                                                             | ✅ New: verify count per status                                     |
| Cancelled lessons excluded                        | None                 | None                                                                             | ✅ New: verify Cancelled not counted                                |
| Count fixed at popup open; filter doesn't refresh | TC-1219 (filter)     | Partial — TC-1219 checks filter affects list; does not check count constancy     | ✅ New: verify count unchanged after each filter type               |
| Zero-lesson shows 0                               | None                 | None                                                                             | ✅ New: verify 0 display                                            |
| Cross-location count                              | None                 | None                                                                             | ✅ New: teacher with cross-location lessons shows combined count    |
| Role access (Centre Staff)                        | None                 | None                                                                             | ✅ New: Centre Staff can see column                                 |
| Not sortable                                      | None                 | None                                                                             | ✅ New: column header click does not sort                           |
| Selected lesson's month reference                 | None                 | None                                                                             | ✅ New: popup on past/future month lesson shows correct month count |
| Calendar Teacher Details — count visible          | None                 | None                                                                             | ✅ New: count shown in calendar panel                               |
| Calendar — always today's month                   | None                 | None                                                                             | ✅ New: navigate to other months; count stays fixed                 |
| Timezone boundary — last day of month             | None                 | None                                                                             | ✅ New: late-night lesson on last day of month counts correctly     |
| Timezone boundary — first day of month            | None                 | None                                                                             | ✅ New: early-morning lesson on first day of month counts correctly |

---

## 7. Suggested Test Suite Structure

```
output/test-cases/lesson-management/lesson-teacher/
├── monthly-lesson-count-popup.md
│   → AC 01.1, AC 01.2 — Add Teacher popup: column display, count calculation,
│     status filtering, zero value, cross-location, filter behavior, role access,
│     sort behavior, reference month selection
│
└── monthly-lesson-count-calendar.md
    → AC 01.3 — Calendar Teacher Details panel: count display, always today's month,
      navigation invariance, zero value
```

> **Note on timezone test cases:** Timezone boundary tests (R14) require a lesson
> created with a specific time near month-end/start. These should be included in
> `monthly-lesson-count-popup.md` as a dedicated "Timezone Boundary" section with
> setup instructions for creating lessons at 11:30pm local time on month-end dates.
