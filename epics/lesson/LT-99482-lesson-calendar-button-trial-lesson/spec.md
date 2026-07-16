---
ticket_id: LT-99482
ticket_url: https://manabie.atlassian.net/browse/LT-99482
title: Add Lesson Calendar button to Trial Lesson page
module: scheduling
bucket: lesson
status: Ready for Internal UAT
internal_uat_date: null
production_release_date: null
last_updated: 2026-07-03
---

# LT-99482: Add Lesson Calendar button to Trial Lesson page

## Summary

This epic adds a Lesson Calendar navigation button on the Trial Lesson detail page in Salesforce so staff can move directly to the calendar from a trial lesson context.
The expected outcome is faster lesson-slot assignment by opening calendar with the trial lesson student already selected.

---

## Acceptance Criteria

### US 01 - Add calendar entry point on Trial Lesson detail

- AC 01.1: On Trial Lesson detail page (SF), a `Lesson Calendar` button is available.
- AC 01.2: When user clicks `Lesson Calendar`, system navigates to Lesson Calendar.
- AC 01.3: Lesson Calendar opens with the student from Trial Lesson already checked/selected in calendar student context.
- AC 01.4: From the opened calendar context, user can continue lesson-slot assignment flow without manually re-selecting the same student.
- AC 01.5: Scope is SF for this entry point; non-SF surfaces are unchanged.

Source baseline: LT-99482 description + linked PBT-3048 description and implementation ticket LT-99483.

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---|---|---|---|---|---|
| 1 | AC 01.1 | Trial Lesson detail shows Lesson Calendar button | Lesson Calendar button | visible | SF |
| 2 | AC 01.2 | Clicking Lesson Calendar button opens Lesson Calendar page | Navigation action | enabled | SF |
| 3 | AC 01.3 | Student tied to Trial Lesson is pre-selected in opened calendar context | Student selection context | auto-selected | SF |
| 4 | AC 01.4 | User can proceed with assignment flow from opened calendar context without re-searching same student | Assignment continuation | preserved context | SF |
| 5 | AC 01.5 | Button entry point is limited to SF scope for this feature | Surface scope | restricted | SF |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---|---|---|---|---|
| 1 | [EXTENDED] | PBT-2058 / PBT-3048 | AC 01.1-01.4 | Extends existing open-calendar behavior by adding Trial Lesson detail as a new entry point. |
| 2 | [REGRESSION RISK] | epics/calendar/LT-102422-publish-lesson-menu-calendar/spec.md | AC 01.2-01.4 | Additional navigation into calendar may affect current calendar state initialization and context behavior. |
| 3 | [REGRESSION RISK] | epics/cross-domain/LT-96188-student-classification-event-lesson-calendar/spec.md | AC 01.3-01.4 | Student-filter and student-session context behavior can regress when entry points change. |

### Missing in Requirements

| # | Tag | Source | Description |
|---|---|---|---|
| 1 | [MISSING BEHAVIOR] | LT-99482 / PBT-3048 text | No explicit behavior for trial lesson with missing/inactive student at click time. |
| 2 | [MISSING BEHAVIOR] | LT-99482 / PBT-3048 text | No explicit expected message or fallback behavior when calendar page load fails. |
| 3 | [ROLE GAP] | LT-99482 fields | Roles allowed to see and use the button are not explicitly listed. |
| 4 | [UNDOCUMENTED IN AC] | LT-99482 text | No explicit assertion for exact navigation target (calendar view mode, left panel state, and whether other filters reset). |

### Lesson-Learned Risks

| # | Incident | Date | AC | Risk | Guardrail |
|---|---|---|---|---|---|
| 1 | Entry-point additions often regress pre-filled context state on destination pages | N/A | AC 01.3-01.4 | Calendar opens but student context is not retained, causing wrong assignment target | Add deterministic context-transfer test cases with student ID assertions |

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-01 | Trial Lesson to Calendar assignment flow | New shortcut entry point from Trial Lesson detail | UPDATE |
| E2E-02 | Lesson Calendar student-context initialization | Additional route into calendar context | UPDATE |

### Assumptions Made

- The new button reuses existing open-calendar behavior currently used in application-related flows.
- Trial Lesson student context should map to calendar student selection directly.
- Scope is SF because implementation ticket LT-99483 is SF-scoped and no BO/mobile scope was specified.

---

## Clarification Questions

1. **[ROLE GAP]** Which exact roles can view and click `Lesson Calendar` on Trial Lesson detail?
   _Evidence: requirement text does not include role matrix._

2. **[MISSING BEHAVIOR]** What is expected behavior when Trial Lesson has no active student at click time?
   _Evidence: student-context pre-select rule exists, but no fallback rule for missing/inactive student._

3. **[UNDOCUMENTED IN AC]** Which calendar surface state is required after navigation (view mode, selected date, left panel filter retention)?
   _Evidence: requirement specifies destination page but not destination state contract._

> Posted status: not posted

---

## Related Specs

- epics/calendar/LT-102422-publish-lesson-menu-calendar/spec.md - recent calendar entry-point and menu behavior changes on SF calendar.
- epics/cross-domain/LT-96188-student-classification-event-lesson-calendar/spec.md - student filter and display context rules in SF calendar.

## Related Test Cases

- epics/calendar/LT-102422-publish-lesson-menu-calendar/test-cases/02-publish-action-execution.md - navigation and state assertion patterns on calendar surface.
- epics/cross-domain/LT-96188-student-classification-event-lesson-calendar/test-cases/02-lesson-calendar.md - student filter/context assertions in calendar.

## QASE Coverage Gaps

- AC 01.1: visibility of Lesson Calendar button on Trial Lesson detail in SF.
- AC 01.2: navigation target and route behavior from Trial Lesson detail to Lesson Calendar.
- AC 01.3: student pre-selection context transfer from Trial Lesson to calendar.
- AC 01.4: assignment continuation from transferred context without manual re-selection.
- AC 01.5: non-SF surface regression coverage.
