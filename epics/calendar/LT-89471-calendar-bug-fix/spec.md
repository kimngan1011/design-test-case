---
ticket_id: LT-89471
ticket_url: https://manabie.atlassian.net/browse/LT-89471
title: Renseikai & Core | Calendar bug fix
module: scheduling
bucket: calendar
status: Done
internal_uat_date: 2025-11-24
production_release_date: 2025-12-08
last_updated: 2026-06-29
---

# LT-89471: Renseikai & Core | Calendar bug fix

## Summary

This epic fixes two calendar-facing regressions in lesson scheduling UX: missing horizontal scrollbar in Daily view under constrained screen sizes and incorrect recurring-until date formatting for Japanese locale.
It also standardizes recurring section label text from Weekly Recurring to Recurring Settings.
The feature primarily impacts calendar usability and recurring metadata readability on lesson detail surfaces.

---

## Acceptance Criteria

### US 01 - Fix horizontal scrolling in Daily view

- AC 01.1: In Lesson Calendar Daily view, horizontal scrollbar is available when content overflows under constrained screen sizes/resolutions so users can access the full calendar width.

### US 02 - Fix recurring metadata wording and date rendering

- AC 02.1: In lesson detail right panel, recurring-until date uses yyyy/mm/dd format when user locale is Japanese.
- AC 02.2: Recurring section label text is changed from Weekly Recurring to Recurring Settings.

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---|----|---|---|---|---|
| 1 | AC 01.1 | Daily view must expose horizontal navigation when timeline overflows viewport width | Daily view timeline container | scrollable | SF/BO |
| 2 | AC 02.1 | Recurring-until date must render as yyyy/mm/dd for Japanese locale users | Recurring until date | formatted | SF/BO |
| 3 | AC 02.1 | Non-Japanese locale formatting remains locale-specific unless explicitly changed | Recurring until date | formatted | SF/BO |
| 4 | AC 02.2 | Weekly Recurring label is replaced with Recurring Settings in recurring section | Recurring section label | display text | SF/BO |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---|---|---|---|---|
| 1 | [REGRESSION RISK] | knowledge/e2e-scenario/e2e-scenarios.md | AC 01.1 | E2E-01 relies on SF calendar visibility. Hidden scrollbar under constrained width can prevent validating full daily timeline content. |

### Missing in Requirements

| # | Tag | Source | Description |
|---|---|---|---|
| 1 | [MISSING BEHAVIOR] | LT-89471 description | Non-Japanese locale output after AC 02.1 fix is not explicitly defined. |
| 2 | [UNDOCUMENTED IN AC] | LT-89471 description | Label rename scope is unclear (right panel only vs other recurring surfaces). |
| 3 | [ROLE GAP] | knowledge/domain-knowledge/scheduling/calendar/calendar-bo.md | Requirement does not state whether BO role-specific views must meet the same scrollbar visibility rule. |

### Lesson-Learned Risks

| # | Incident | Date | AC | Risk | Guardrail |
|---|---|---|---|---|---|
| 1 | No explicit matched incident entry found in lesson-learned files during this run | N/A | AC 01.1, AC 02.1 | Calendar display bugs are sensitive to viewport and locale combinations; risk of partial fix | Add viewport/zoom matrix and locale matrix in coverage and test cases |

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-01 | Lesson Lifecycle - Create, Teach, Report, View | Step 2 calendar verification can fail if overflow is not reachable | UPDATE |
| E2E-02 | Recurring Lesson - Create, Edit Chain, Delete, Calendar Drag | Recurring text/date rendering checks should include locale-aware assertions | UPDATE |

### Assumptions Made

- Jira description and linked Confluence metadata were available, but Confluence requirement tables were not fully extractable from the browser snapshot in this run.
- AC IDs were normalized from issue statements into US/AC structure for traceability.
- Status and release dates were taken from Jira side panel fields.

---

## Clarification Questions

1. **[MISSING BEHAVIOR]** For non-Japanese locales, should recurring-until date continue using existing locale-specific format, or should yyyy/mm/dd apply globally?
   Evidence: ticket description only specifies Locale=Japan behavior.

2. **[ROLE GAP]** Does the Daily-view horizontal scrollbar fix apply to both SF and BO calendar surfaces for all roles (HQ/CM/Teacher), or only specific roles/surfaces?
   Evidence: domain knowledge indicates role-dependent behavior across calendar surfaces.

3. **[UNDOCUMENTED IN AC]** Please confirm the exact scope of label rename to Recurring Settings: lesson detail right panel only, or additional recurring surfaces.
   Evidence: requirement mentions a specific panel but not global scope.

4. **[REGRESSION RISK]** What viewport/zoom baseline should be used as pass criteria for Daily view scrollbar visibility?
   Evidence: issue references specific screen sizes/resolutions but no explicit numeric boundary.

> Posted status: not posted

---

## Related Specs

- epics/calendar/LT-88879-improve-course-class-filter-calendar/spec.md - recent calendar UX/filter behavior changes on SF and BO.
- epics/calendar/LT-XXXX-drag-drop-edit-lesson-time/spec.md - calendar rendering + recurring-related behavior in lesson detail/calendar flows.

## Related Test Cases

- epics/calendar/LT-88879-improve-course-class-filter-calendar/test-cases/01-class-section-visibility.md - UI display-state assertions in calendar panel interactions.
- epics/calendar/LT-88879-improve-course-class-filter-calendar/test-cases/05-all-match-regression.md - regression-oriented calendar assertions.

## QASE Coverage Gaps

- AC 01.1 - viewport-constrained horizontal scrollbar visibility in Daily view.
- AC 02.1 - locale-specific recurring-until formatting (ja-JP vs non-ja behavior).
- AC 02.2 - exact text assertion for Recurring Settings label scope.
