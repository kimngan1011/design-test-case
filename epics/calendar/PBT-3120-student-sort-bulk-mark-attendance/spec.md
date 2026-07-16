---
ticket_id: PBT-3120
ticket_url: https://manabie.atlassian.net/browse/PBT-3120
title: "[Renseikai] Core | Student Sort in Bulk Mark Attendance page"
module: scheduling
bucket: calendar
status: In Development
internal_uat_date: null
production_release_date: null
last_updated: 2026-07-02
---

# PBT-3120: [Renseikai] Core | Student Sort in Bulk Mark Attendance page

## Summary

This epic updates student ordering behavior in BO Calendar Bulk Mark Attendance and localizes lesson Type labels to Japanese.
The new ordering requirement is `Grade > Phonetic Name > Student Name > Created at`, aligned with LT-77063 behavior.
It also replaces English Type option labels with Japanese labels for the targeted flow.

---

## Acceptance Criteria

### US 01 - Student ordering in Bulk Mark Attendance

- AC 01.1: In `Lesson Calendar (BO) > Mark Attendance`, students are sorted by `Grade > Phonetic Name > Student Name > Created at`.
- AC 01.2: Sorting behavior follows the same ordering logic used in LT-77063.

### US 02 - Type option localization in Japanese

- AC 02.1: In the target page, Type options are localized to Japanese.
- AC 02.2: Label mapping:
  - `Regular` -> `通常`
  - `Trial` -> `体験`
  - `Seasonal` -> `講習`

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---|---|---|---|---|---|
| 1 | AC 01.1 | Student list order uses Grade as first sort key | Student list | ordered | BO Calendar |
| 2 | AC 01.1 | When Grade is equal, sort by Phonetic Name | Student list | ordered | BO Calendar |
| 3 | AC 01.1 | When Grade and Phonetic Name are equal, sort by Student Name | Student list | ordered | BO Calendar |
| 4 | AC 01.1 | When first three keys are equal, sort by Created at | Student list | ordered | BO Calendar |
| 5 | AC 01.2 | Target flow sorting must match LT-77063 behavior baseline | Student list | consistency | BO Calendar |
| 6 | AC 02.2 | Type labels must render with JP translations 通常 / 体験 / 講習 | Type options | display text | BO Calendar |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---|---|---|---|---|
| 1 | [REGRESSION RISK] | epics/lesson/LT-XXXX-student-assignment/test-cases/student-assignment-lesson-detail.md | AC 01.1 | Existing sorting assertions in lesson student lists can diverge if Bulk Mark Attendance applies different fallback rules for empty phonetic values. |
| 2 | [EXTENDED] | knowledge/domain-knowledge/scheduling/lesson-management/student-session.md | AC 01.1 | Domain rule already defines phonetic-aware sorting; this ticket extends it by introducing Grade-first ordering in a specific screen. |

### Missing in Requirements

| # | Tag | Source | Description |
|---|---|---|---|
| 1 | [MISSING BEHAVIOR] | PBT-3120 description | Sort direction for each key (ASC/DESC) is not explicitly stated. |
| 2 | [MISSING BEHAVIOR] | PBT-3120 description | Handling for null/empty phonetic name in tie-break is not defined. |
| 3 | [UNDOCUMENTED IN AC] | PBT-3120 description | Scope of Type translation is unclear (only Bulk Mark Attendance popup vs all BO lesson surfaces). |
| 4 | [ROLE GAP] | knowledge/domain-knowledge/scheduling/calendar/calendar-bo.md | Requirement does not specify whether ordering/localization is identical for CPU Teacher and SPU CM views. |

### Lesson-Learned Risks

| # | Incident | Date | AC | Risk | Guardrail |
|---|---|---|---|---|---|
| 1 | No directly matching incident found in lesson-learned files during this run | N/A | AC 01.1, AC 02.2 | Sorting and localization changes often fail on null data and mixed-language datasets | Add explicit null-phonetic, mixed-script, and exact-string assertions in coverage and test cases |

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-17 | Renseikai - Attendance & Error Configuration | Bulk Update Attendance flow behavior changes due to new ordering and localized labels | UPDATE |
| E2E-01 | Lesson Lifecycle - Create, Teach, Report, View | BO attendance collection step should assert updated order and label rendering | UPDATE |

### Assumptions Made

- PBT-3120 detail page is the requirement source; linked LT-102402 did not contain a detailed Description block in the captured snapshot.
- This ticket is treated as calendar-domain scope because the impacted entry point is BO Calendar Bulk Mark Attendance.
- Since `Customisation = No` in Jira details, this is modeled as core behavior with Renseikai-driven business priority.

---

## Clarification Questions

1. **[MISSING BEHAVIOR]** For AC 01.1, please confirm the sort direction of each key (Grade, Phonetic Name, Student Name, Created at): all ascending?
   _Evidence: Requirement defines key order only, not direction._

2. **[MISSING BEHAVIOR]** How should records with empty Phonetic Name be ordered when Grade is equal?
   _Evidence: No null/empty rule provided for tie-break handling._

3. **[UNDOCUMENTED IN AC]** Should Type label translations (`通常`, `体験`, `講習`) apply only in Bulk Mark Attendance, or also in other BO lesson views using the same Type values?
   _Evidence: Requirement says "Type options" but does not define exact UI scope._

4. **[ROLE GAP]** Please confirm whether CPU Teacher and SPU CM roles must see identical ordering and Type label translation outcomes.
   _Evidence: BO Calendar access differs by user type in domain knowledge._

> Posted status: not posted

---

## Related Specs

- epics/calendar/LT-89471-calendar-bug-fix/spec.md - calendar BO display-level behavior changes and regression strategy patterns.
- epics/cross-domain/LT-96188-student-classification-event-lesson-calendar/spec.md - JP label assertions in list/filter UIs.

## Related Test Cases

- epics/lesson/LT-XXXX-student-assignment/test-cases/student-assignment-lesson-detail.md - existing phonetic-name ordering assertions for student lists.
- epics/cross-domain/LT-96188-student-classification-event-lesson-calendar/test-cases/02-lesson-calendar.md - calendar list rendering and JP label checks.

## QASE Coverage Gaps

- AC 01.1 - deterministic multi-key sort verification (including null phonetic fallback and final tie on created timestamp).
- AC 01.2 - parity verification against LT-77063 sorting baseline.
- AC 02.2 - exact JP string assertions for all three Type options and absence of untranslated labels.
