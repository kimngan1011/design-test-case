# Test Coverage: LT-96616 — Nichibei Lesson List in BO (Smartphone view)

**Jira:** https://manabie.atlassian.net/browse/LT-96616  
**Date:** 2026-05-11  
**Partner Scope:** Nichibei only  
**Platform:** BO (Back Office)

---

## 1. Business Rules Extracted

| #   | AC      | Business Rule                                                                                                                                                            |
| --- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| BR1 | AC 01.1 | Lesson Status filter defaults to "Published" on every Lesson List page load                                                                                              |
| BR2 | AC 01.1 | Filter is PERSISTENT — retains user-selected value across navigation; resets to "Published" only when user manually clears                                               |
| BR3 | AC 01.1 | For Limit Teacher profile: Published default applies together with Limit Teacher scope (both active simultaneously — teacher sees only their assigned Published lessons) |
| BR4 | AC 01.2 | User can change Lesson Status filter from "Published" to any other available status                                                                                      |
| BR5 | AC 02.1 | Within existing Collect Attendance page: student-submitted Attendance_Response_Remark shown as read-only inline field per student row (no new column on Lesson List)     |
| BR6 | AC 02.2 | Single remark field shows data from BOTH sources (Booking flow + Submit Attendance); blank when no submission; no visual distinction between sources                     |
| BR7 | AC 03.1 | New entry point on Lesson List row opens existing Collect Attendance page — Published lessons only                                                                       |
| BR8 | AC 03.1 | Entry point is hidden/disabled for Draft, Completed, and Cancelled lessons                                                                                               |
| BR9 | AC 03.3 | Collect Attendance page from Lesson List retains full functionality (radio buttons + Save); only student-submitted remark field is read-only                             |

---

## 2. Logic Type Categorization

| AC      | BR  | Logic Type                          |
| ------- | --- | ----------------------------------- |
| AC 01.1 | BR1 | Conditional logic, State transition |
| AC 01.1 | BR2 | Conditional logic                   |
| AC 01.1 | BR3 | Permission logic, Conditional logic |
| AC 01.2 | BR4 | Validation logic                    |
| AC 02.1 | BR5 | Conditional logic, Data integrity   |
| AC 02.2 | BR6 | Conditional logic, Data integrity   |
| AC 03.1 | BR7 | Conditional logic, Permission logic |
| AC 03.1 | BR8 | Conditional logic, State transition |
| AC 03.3 | BR9 | Data integrity, Regression Analysis |

---

## 3. Test Technique Selection

| Logic Type          | Applicable Techniques                                      |
| ------------------- | ---------------------------------------------------------- |
| Conditional logic   | Decision Table, Equivalence Partitioning, Negative Testing |
| State transition    | State Transition Testing, Negative Testing                 |
| Permission logic    | Permission Matrix, Decision Table                          |
| Validation logic    | Equivalence Partitioning, Negative Testing                 |
| Data integrity      | CRUD Testing, Regression Analysis                          |
| Regression Analysis | Regression Analysis, CRUD Testing                          |

---

## 4. Structured Coverage Strategy

| AC      | Business Rule Summary                                               | Logic Type                          | Test Technique                           | Risk Level | Coverage Depth |
| ------- | ------------------------------------------------------------------- | ----------------------------------- | ---------------------------------------- | ---------- | -------------- |
| AC 01.1 | BR1: Filter defaults to "Published" on page load                    | Conditional logic                   | Decision Table, Equivalence Partitioning | High       | Standard       |
| AC 01.1 | BR2: Filter is persistent (manual clear only)                       | Conditional logic                   | Decision Table, Negative Testing         | High       | Standard       |
| AC 01.1 | BR3: Limit Teacher + Published default (both active simultaneously) | Permission logic, Conditional       | Permission Matrix, Decision Table        | High       | Deep           |
| AC 01.2 | BR4: User can change filter to any other status                     | Validation logic                    | Equivalence Partitioning                 | Medium     | Standard       |
| AC 02.1 | BR5: Remark shown read-only per student row in Collect Attendance   | Conditional logic, Data integrity   | Decision Table, Equivalence Partitioning | High       | Deep           |
| AC 02.2 | BR6: Single remark field — both sources; blank when no submission   | Conditional logic, Data integrity   | Decision Table, Equivalence Partitioning | High       | Deep           |
| AC 03.1 | BR7: Entry point from Lesson List — Published only                  | Conditional logic, State transition | Decision Table, State Transition Testing | High       | Standard       |
| AC 03.1 | BR8: Entry point hidden/disabled for non-Published statuses         | Conditional logic, State transition | Decision Table, Negative Testing         | High       | Standard       |
| AC 03.3 | BR9: Page retains full functionality; only remark is read-only      | Data integrity, Regression          | Regression Analysis, CRUD Testing        | High       | Deep           |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area                                   | Reason                                                                                                                                                                                                                                                           | Recommended Approach                                                                                                                                                                             |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| BR5 + BR6: Remark field data integrity | Attendance_Response_Remark is sourced from two separate flows (Booking + Submit Attendance). If either source is incorrectly displayed or overwritten, the BO staff receives incorrect student attendance information — impacting attendance recording accuracy. | Test each source independently; verify combined single-field display; verify no overwrite between sources; verify null-LA student sessions do not cause rendering failure (lesson-learned risk). |
| BR9: Page functionality preserved      | If adding the new entry point or the read-only remark field accidentally disables Save/radio buttons, existing attendance collection is broken for Nichibei — affects lesson reporting and downstream billing.                                                   | Regression test: verify Save and all radio button options remain fully functional after the new entry point is added.                                                                            |

### 🟠 High Risk

| Area                                        | Reason                                                                                                                                                                                                           | Recommended Approach                                                                                                                   |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| BR2: Filter persistence                     | If the filter resets on navigation, BO staff on smartphones must manually re-apply the filter every page visit — high friction for the primary smartphone UX goal of this Epic.                                  | Test navigation away and return (via Lesson Detail, Dashboard, Calendar) — verify filter persists; test browser refresh separately.    |
| BR3: Limit Teacher + Published default      | Two independent filter scopes must apply simultaneously. If one overrides the other, Limit Teachers either see lessons outside their scope or see all statuses.                                                  | Decision table covering: Limit Teacher viewing assigned Published / assigned Draft / unassigned Published — verify correct visibility. |
| BR7 + BR8: Entry point visibility by status | Entry point must appear on Published and be hidden on Draft / Completed / Cancelled. If guard is incorrect, staff can open Collect Attendance for lessons in wrong state, or cannot access it for valid lessons. | State transition test: for each status (Draft, Published, Completed, Cancelled) verify entry point visibility.                         |
| BR1: Published default on first load        | If default is only applied on session start (not per-page-load), staff who visit from different pages see wrong filter. This is the primary UX requirement for smartphone optimization.                          | Verify: fresh page load, return from detail, return after filter change — all should show Published as default on load.                |

### 🟡 Medium Risk

| Area                                           | Reason                                                                                                                                                          | Recommended Approach                                                                                                          |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| BR4: Filter changeability                      | Standard dropdown behavior; low risk but must confirm Published can be replaced with Draft / Completed / Cancelled.                                             | Equivalence partitioning: one test per valid status value.                                                                    |
| BR6: Blank state when no submission            | If the remark field shows an error or unexpected text when no student has submitted, it creates confusion for staff.                                            | Verify blank/empty state renders cleanly (no error text, no placeholder artifact).                                            |
| Null-LA student sessions (lesson-learned risk) | Past Nichibei incident (2026-03-04): SPO sync bugs can delete LA records, leaving Student Sessions with null LA. Remark field rendering must not fail silently. | Verify: Collect Attendance page renders student row correctly when session has null LA; remark field shows blank (not error). |

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area                                              | Existing Test Case                                                                                                                                                                           | Overlap                                                                                         | New Coverage Needed                                                                                                 |
| ----------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| BR1: Published default filter on load                 | `lesson-status.md` (TC-1456, TC-9786…) — covers status transitions, NOT list filter defaults                                                                                                 | None                                                                                            | ✅ New TC: verify filter = Published on Lesson List load (Nichibei BO)                                              |
| BR2: Filter persistence across navigation             | None found                                                                                                                                                                                   | None                                                                                            | ✅ New TC: navigate away/return → filter retains value; browser refresh → resets to Published                       |
| BR3: Limit Teacher + Published default                | `teacher-view-lesson-different-location.md` — covers Limit Teacher lesson visibility, NOT combined filter default                                                                            | Partial (Limit Teacher scope covered, Published default + simultaneous interaction not covered) | ✅ New TC: Limit Teacher opens Lesson List → Published default + assigned-only scope both active                    |
| BR4: Filter changeability                             | None for Lesson List filter                                                                                                                                                                  | None                                                                                            | ✅ New TC: change filter to Draft / Completed → list updates correctly                                              |
| BR5: Remark field displayed read-only per student row | `book-lesson.md` (BR-14) — covers SAVING remark during booking; `LT-96152-collect-attendance-entry-points.md` — covers entry point and saving attendance from Report tab, NOT remark display | Partial (remark save on Mobile covered; BO display in Collect Attendance page not covered)      | ✅ New TC: open Collect Attendance from Lesson List → remark shown read-only inline per student row                 |
| BR6: Single field — both sources + blank when none    | `book-lesson.md` — covers "Booking Note: " prefix save; Submit Attendance source has no existing test                                                                                        | Partial (booking source covered; Submit Attendance + combined display not covered)              | ✅ New TC: remark from Submit Attendance source; remark from Booking flow; blank state when no submission           |
| BR7: Entry point visible for Published lessons only   | `LT-96152-collect-attendance-entry-points.md` — covers Lesson Report tab entry point, NOT Lesson List entry point                                                                            | None (different entry point)                                                                    | ✅ New TC: Published lesson → entry point visible; click → Collect Attendance page opens                            |
| BR8: Entry point hidden for non-Published statuses    | `LT-96152-collect-attendance-entry-points.md` — covers Draft/Completed guards for Report tab entry point                                                                                     | Partial (same page behavior, different entry point guards not tested)                           | ✅ New TC: Draft / Completed / Cancelled lesson rows → entry point hidden/disabled                                  |
| BR9: Page retains full functionality                  | `LT-96152-collect-attendance-entry-points.md` (TC-5 Regression) — covers save from Report tab entry point                                                                                    | Partial (save functionality regression covered for Report tab; not for Lesson List entry point) | ✅ New TC: open Collect Attendance from Lesson List → Save + radio buttons functional; remark field is not editable |
| Null-LA student session rendering                     | None                                                                                                                                                                                         | None                                                                                            | ✅ New TC: Collect Attendance page loads correctly when a student session has null LA                               |

---

## 7. Suggested Test Suite Structure

```
output/test-cases/lesson-management/oop/nichibei-lesson-list/
├── filter-default-published.md
│   → AC 01.1 (BR1, BR2) — Published default on load; filter persistence across navigation;
│     reset behavior on manual clear
│
├── filter-limit-teacher.md
│   → AC 01.1 (BR3) — Limit Teacher profile: Published default + assigned scope simultaneous;
│     decision table per Limit Teacher + status combination
│
├── LT-96616-collect-attendance-lesson-list-entry.md
│   → AC 03.1 (BR7, BR8) — Entry point visibility per lesson status (Published/Draft/Completed/Cancelled);
│     navigation to Collect Attendance page from Lesson List
│
├── LT-96616-attendance-response-remark-display.md
│   → AC 02.1 + AC 02.2 (BR5, BR6) — Remark field read-only per student row;
│     Booking flow source (with prefix); Submit Attendance source; blank state; null-LA edge case
│
├── LT-96616-collect-attendance-page-functionality.md
│   → AC 03.3 (BR9) — Regression: Save button + radio buttons functional after new entry point added;
│     remark field is read-only (not editable by staff)
```

> **Note:** All files are placed under `oop/nichibei-lesson-list/` as these are Nichibei-specific behaviors.
