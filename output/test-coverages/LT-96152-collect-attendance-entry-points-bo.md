# Test Coverage: LT-96152 — Collect Attendance Entry Points on Lesson Report BO

**Jira:** https://manabie.atlassian.net/browse/LT-96152
**Date:** 2026-04-14

---

## 1. Business Rules Extracted

| #   | AC      | Business Rule                                                                                                                                         |
| --- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | AC 01.1 | Collect Attendance action is shown on BO Lesson Detail -> Report tab.                                                                                 |
| 2   | AC 01.2 | Collect Attendance action is shown on BO Lesson Report Detail.                                                                                        |
| 3   | AC 01.3 | Clicking either new entry point opens the existing collect attendance popup.                                                                          |
| 4   | AC 01.4 | Draft lessons remain unavailable for attendance update on the new surfaces.                                                                           |
| 5   | AC 01.4 | Completed lessons remain unavailable for attendance update on the new surfaces.                                                                       |
| 6   | AC 01.4 | Attendance-eligible lessons keep the new entry points enabled.                                                                                        |
| 7   | AC 01.5 | Saving from the Report tab updates the same student-session data as the current collect-attendance flow.                                              |
| 8   | AC 01.5 | Saving from Lesson Report Detail updates lesson allocation/report-history and Mobile-facing attendance data with the same values as the current flow. |
| 9   | AC 01.5 | Reopening the popup from the new entry points shows the previously saved attendance values.                                                           |

---

## 2. Logic Type Categorization

| AC      | Business Rule # | Logic Type                             |
| ------- | --------------- | -------------------------------------- |
| AC 01.1 | 1, 3, 6         | Conditional logic, Cross-system impact |
| AC 01.2 | 2, 3, 6         | Conditional logic, Cross-system impact |
| AC 01.4 | 4, 5            | Conditional logic, State transition    |
| AC 01.5 | 7, 8            | Data integrity, Cross-system impact    |
| AC 01.5 | 9               | Validation logic, Regression Analysis  |

---

## 3. Test Technique Selection

| Logic Type          | Applicable Techniques                         |
| ------------------- | --------------------------------------------- |
| Conditional logic   | Decision Table, Negative Testing              |
| State transition    | State Transition Testing, Negative Testing    |
| Data integrity      | CRUD Testing, Regression Analysis             |
| Cross-system impact | Regression Analysis, Decision Table           |
| Validation logic    | Equivalence Partitioning, Regression Analysis |

---

## 4. Structured Coverage Strategy

| AC      | Business Rule Summary                                                                                    | Logic Type                             | Test Technique                                | Risk Level | Coverage Depth |
| ------- | -------------------------------------------------------------------------------------------------------- | -------------------------------------- | --------------------------------------------- | ---------- | -------------- |
| AC 01.1 | Report tab shows Collect Attendance and opens the existing popup on attendance-eligible lesson           | Conditional logic, Cross-system impact | Decision Table, Regression Analysis           | High       | Standard       |
| AC 01.2 | Lesson Report Detail shows Collect Attendance and opens the existing popup on attendance-eligible lesson | Conditional logic, Cross-system impact | Decision Table, Regression Analysis           | High       | Standard       |
| AC 01.4 | Draft and Completed lessons keep Collect Attendance unavailable from the new report surfaces             | Conditional logic, State transition    | Decision Table, Negative Testing              | High       | Standard       |
| AC 01.5 | Save from Report tab preserves current student-session and Mobile update flow                            | Data integrity, Cross-system impact    | CRUD Testing, Regression Analysis             | Critical   | Deep           |
| AC 01.5 | Save from Lesson Report Detail preserves lesson allocation/report-history and Mobile update flow         | Data integrity, Cross-system impact    | CRUD Testing, Regression Analysis             | Critical   | Deep           |
| AC 01.5 | Reopen from new surfaces shows previously saved reason, notice, and note values                          | Validation logic, Regression Analysis  | Equivalence Partitioning, Regression Analysis | Medium     | Standard       |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area                           | Reason                                                                                                                                                              | Recommended Approach                                                                                                      |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Save from Report tab           | If the new entry point bypasses the existing save pipeline, student-session, lesson-allocation, and Mobile values can diverge.                                      | Run end-to-end save verification with status, reason, notice, and note; confirm BO and Mobile parity.                     |
| Save from Lesson Report Detail | This surface is closer to report data than student-session data; wiring to the wrong mutation path can update report UI without updating source attendance records. | Save from Lesson Report Detail, then confirm student-session row, report history, and Mobile all reflect the same result. |

### 🟠 High Risk

| Area                  | Reason                                                                                                                       | Recommended Approach                                                       |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Disabled state parity | Existing suite 326 already guards Draft and Completed lessons. The new report-surface buttons must not create a bypass path. | Explicitly test Draft and Completed on the two new surfaces.               |
| Popup parity          | If the new buttons open a duplicated popup, saved remarks, localization, or student ordering can regress.                    | Compare popup structure and saved-value prefill against the existing flow. |

### 🟡 Medium Risk

| Area                     | Reason                                                                                           | Recommended Approach                                                                        |
| ------------------------ | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| Reopen with saved values | Easy to miss during implementation if the new surfaces do not refresh from the same data source. | Save attendance first, reopen from the new surface, and confirm saved values are prefilled. |

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area                                          | Existing Test Case                                     | Overlap                                                                    | New Coverage Needed                                           |
| ------------------------------------------------- | ------------------------------------------------------ | -------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Collect Attendance on Lesson Detail -> Report tab | Qase PX suite 326                                      | None                                                                       | ✅ New coverage for visibility and popup open                 |
| Collect Attendance on Lesson Report Detail        | Qase PX suite 326; LA system integration               | Partial — Lesson Report Detail exists but not as an attendance entry point | ✅ New coverage for visibility and popup open                 |
| Disabled-state parity on new surfaces             | Qase PX suite 326 — User cannot update attendance info | Partial — current disabled logic covered only on the existing surface      | ✅ New coverage for Draft and Completed from report surfaces  |
| Save parity from Report tab                       | Qase PX suite 326 — User updates the attendance info   | Partial — save logic exists, report-tab launch path not covered            | ✅ New coverage for end-to-end save from Report tab           |
| Save parity from Lesson Report Detail             | Qase PX suite 326; LA system integration               | Partial — report detail exists, save from this new entry path not covered  | ✅ New coverage for end-to-end save from Lesson Report Detail |
| Saved-value prefill from new surfaces             | Qase PX suite 326 — remark persistence                 | Partial — persistence exists, new surfaces not covered                     | ✅ New coverage for reopen/prefill                            |

---

## 7. Suggested Test Suite Structure

```
output/test-cases/lesson-management/lesson-report/collect-attendance-entry-points/
├── LT-96152-collect-attendance-entry-points.md
│     → AC 01.1 / AC 01.2 — Report-tab and lesson-report-detail entry points
│     → AC 01.4 — Disabled-state parity on Draft and Completed lessons
│     → AC 01.5 — Save-path regression and saved-value prefill
```
