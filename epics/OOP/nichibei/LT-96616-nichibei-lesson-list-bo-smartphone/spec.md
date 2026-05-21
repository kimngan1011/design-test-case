# LT-96616: Nichibei Lesson List in BO (Smartphone view)

**ID:** https://manabie.atlassian.net/browse/LT-96616  
**Status:** Ready for QA  
**Analysis Date:** 2026-05-11  
**Scope Note (PM Confirmed 2026-05-11):** Feature reuses the **existing Collect Attendance page UI** — no new column added to the Lesson List. LT-96656 adds the student-submitted remark (Attendance_Response_Remark) as a read-only field per student row **within** the existing Collect Attendance page. LT-96657 adds a new **entry point** from the Lesson List to open that existing page (Published lessons only).

---

## Summary

This Epic optimizes the BO Lesson List for smartphone view (Nichibei partner) with two key behaviors: (1) the Lesson Status filter defaults to "Published" on load (persistent until manually cleared), and (2) a new entry point is added from the Lesson List to the existing Collect Attendance page (Published lessons only), where the student-submitted attendance response (Attendance_Response_Remark) is displayed as a read-only field per student row — reusing the existing Collect Attendance UI without adding a new column to the Lesson List.

---

## Acceptance Criteria

### LT-96655 — Filter Lesson Status Defaults to Published

**AC 01.1:** When a BO user opens the Lesson List, the Lesson Status filter should default to "Published".  
**AC 01.2:** The user can change the Lesson Status filter from the default "Published" to any other available status value.

---

### LT-96656 — Show Student Attendance Response in Collect Attendance Page

**AC 02.1:** Within the existing Collect Attendance page, a read-only field shows the student-submitted attendance response (Attendance_Response_Remark) per student row.  
**AC 02.2:** The remark text is sourced from either the **Booking flow** (prefixed "Booking Note: " per LT-96620) or the **Mobile Submit Attendance flow** — displayed as a single field with no visual distinction between sources.

> **Note:** This reuses the existing Collect Attendance page UI. NO new column is added to the Lesson List. UI confirmed via screenshot (2026-05-11): remark appears inline in the student row (e.g. "Leave Early (Test(Submit))").

---

### LT-96657 — New Entry Point: Lesson List → Collect Attendance Page

**AC 03.1:** A new entry point is added on lesson rows in the BO Lesson List to open the existing Collect Attendance page.  
**AC 03.2:** Entry point is available for **Published lessons only** — hidden/disabled for Draft, Completed, and Cancelled lessons.  
**AC 03.3:** The Collect Attendance page opened from this entry point retains full functionality — staff can record/save attendance (radio buttons + Save); the student-submitted remark field is read-only.

---

## Business Rules (Extracted)

| #   | AC         | Business Rule                                                                                                                                                  | Field                                        | Field Behavior                                   | Platform |
| --- | ---------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- | ------------------------------------------------ | -------- |
| 1   | AC 01.1    | Lesson Status filter defaults to "Published" on Lesson List open                                                                                               | Lesson Status filter                         | auto-set (default = Published on load)           | [BO]     |
| 2   | AC 01.1 ✅ | Filter is PERSISTENT — retains user-selected value across navigation; resets to "Published" only when user manually clears                                     | Lesson Status filter                         | persistent (not reset on navigation away/return) | [BO]     |
| 3   | AC 01.1 ✅ | For Limit Teacher profile: Published default applies together with Limit Teacher scope filter (both active simultaneously — assigned Published lessons only)   | Lesson Status filter + Limit Teacher scope   | Published AND within assigned teacher scope      | [BO]     |
| 4   | AC 01.2    | User can change Lesson Status filter from "Published" to any other status                                                                                      | Lesson Status filter                         | editable                                         | [BO]     |
| 5   | AC 02.1 ✅ | Within Collect Attendance page: student-submitted Attendance_Response_Remark shown as read-only field per student row — NO new column on Lesson List           | Attendance_Response_Remark (within page)     | read-only remark text (inline per student row)   | [BO]     |
| 6   | AC 02.2 ✅ | Single remark field shows data from BOTH sources (Booking flow + Submit Attendance) — no visual distinction; blank when no submission                          | Attendance_Response_Remark                   | read-only (single field); blank if no submission | [BO]     |
| 7   | AC 03.1 ✅ | New entry point on Lesson List row opens existing Collect Attendance page — Published lessons only                                                             | Collect Attendance entry point (Lesson List) | navigable (Published lessons only)               | [BO]     |
| 8   | AC 03.1 ✅ | Entry point hidden/disabled for Draft, Completed, and Cancelled lessons                                                                                        | Collect Attendance entry point (Lesson List) | hidden/disabled                                  | [BO]     |
| 9   | AC 03.3 ✅ | Collect Attendance page (from Lesson List) retains full functionality — staff can record/save attendance; only the student-submitted remark field is read-only | Collect Attendance page                      | editable (attendance); remark = read-only        | [BO]     |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

No conflicts found. The new Published default and attendance response column are additive changes that do not contradict any existing behavior in current spec files or test cases.

---

### Missing in Requirements — All Resolved ✅

| #   | Tag        | AC           | Question                                                                    | PM Answer (2026-05-11)                                                                 |
| --- | ---------- | ------------ | --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| 1   | [RESOLVED] | AC 01.1      | Filter persistence after navigation?                                        | Always keep — resets only when user manually clears                                    |
| 2   | [RESOLVED] | AC 01.1      | Limit Teacher behavior with Published default?                              | Apply together with Limit Teacher filter (Published + assigned scope)                  |
| 3   | [RESOLVED] | AC 02.1/02.2 | Remark display format + empty state within Collect Attendance page?         | Shows remark text inline per student row; blank when no submission                     |
| 4   | [RESOLVED] | AC 03.1      | Which statuses allow entry point from Lesson List?                          | Published only                                                                         |
| 5   | [RESOLVED] | AC 03.2      | Collect Attendance page from Lesson List — full functionality or view-only? | Reuses existing UI with full functionality; only the student remark field is read-only |
| 6   | [RESOLVED] | AC 02.2      | Two sources (Booking + Submit Attendance) — combined or separate?           | Single remark field for both, no visual distinction                                    |

---

### Lesson-Learned Risks

| #   | Incident                               | Date       | AC      | Risk                                                                                                                                                                                                                                                    | Guardrail                                                                                                                                                         |
| --- | -------------------------------------- | ---------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Nichibei — Student Sessions Missing LA | 2026-03-04 | AC 03.2 | Mark Attendance page reads student session data. Past incident: Nichibei LA records can be deleted (SPO sync bugs), leaving Student Sessions with null LA. Null-LA sessions must still render Attendance_Response_Remark correctly — not fail silently. | Verify: Mark Attendance page renders correctly when some student sessions have null LA. Attendance_Response_Remark must be readable regardless of LA association. |

---

### E2E Scenario Impact

| Scenario                      | Title                                                            | Impact                                                                                                 | Action          |
| ----------------------------- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | --------------- |
| E2E — Nichibei Lesson Booking | output/test-cases/lesson-management/oop/nichibei-lesson-booking/ | Booking Note remark (from LT-96620) is now displayed in BO Lesson List column and Mark Attendance page | UPDATE          |
| E2E — BO Lesson List          | output/test-cases/lesson-management/                             | New Published default filter and attendance response column need new E2E coverage                      | CREATE / UPDATE |

---

### Regression Risks

| #   | Tag               | Source                                                                | AC      | Description                                                                                                                                                                                                                             |
| --- | ----------------- | --------------------------------------------------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | [REGRESSION RISK] | LT-96152 spec — Collect Attendance entry points via Lesson Report tab | AC 03.1 | Existing collect attendance entry points (Lesson Report tab per LT-96152, Lesson Detail) must not be affected by the new Lesson List entry point. Same page/component — adding a new navigation path must not change existing behavior. |

---

### Assumptions Made

- The "attendance notice" in the Epic = Attendance_Response_Remark field, as documented in LT-96620 AC 03.2.
- The Submit Attendance flow on Mobile also writes to Attendance_Response_Remark (referenced in Epic; no separate spec for this flow found in workspace).
- Feature is Nichibei-partner-specific; does not apply to other partners unless explicitly enabled.
- LT-98222 (sub-ticket in Epic) is a technical/dependency ticket with no additional AC.

---

## Clarification Questions — All Answered ✅ (PM replied 2026-05-11)

| #   | Question                                                                                       | Answer                                                                                                            |
| --- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| 1   | Filter persistence after navigation?                                                           | Always keep — resets only when user manually clears                                                               |
| 2   | Limit Teacher + Published default interaction?                                                 | Apply together with Limit Teacher filter (Published + assigned teacher scope)                                     |
| 3   | Remark display within Collect Attendance page: what shows when response submitted / when none? | Remark text inline per student row; blank when no submission                                                      |
| 4   | Which lesson statuses allow Collect Attendance entry point from Lesson List?                   | Published only                                                                                                    |
| 5   | Collect Attendance page from Lesson List: full functionality or view-only?                     | Reuses existing UI with full functionality; only the student remark field is read-only (confirmed via screenshot) |
| 6   | Booking Note + Submit Attendance — combined or separate?                                       | Single remark field for both; no visual distinction                                                               |

---

## Related Specs

- `input/specs/LT-96620 Nichibei App - Lesson Booking System/spec.md` — defines Attendance_Response_Remark (booking remarks with "Booking Note: " prefix, BR-14); the data source for the remark field shown in Collect Attendance page
- `input/specs/LT-96152 Core Add Collect Attendance Menu in Lesson Report tab page BO/spec.md` — existing Collect Attendance entry points in BO (Lesson Report tab); LT-96657 adds a second entry point from Lesson List to the same page

## Related Test Cases

- `output/test-cases/lesson-management/oop/nichibei-lesson-booking/book-lesson.md` — booking remark test cases (BR-14); BO-side verification of remark display in Collect Attendance page not yet covered

## Qase Coverage Gaps

- AC 01.1 — No existing test cases for Published default Lesson Status filter (persistent behavior, Limit Teacher interaction)
- AC 02.1 / AC 02.2 — No existing test cases for student-submitted remark field display within Collect Attendance page
- AC 03.1 — No existing test cases for Collect Attendance entry point from Lesson List (Published only)
- AC 03.3 — No existing test cases verifying page retains full functionality (Save/radio) + student remark field is read-only
