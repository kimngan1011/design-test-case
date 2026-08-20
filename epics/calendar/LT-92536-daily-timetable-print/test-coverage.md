# Test Coverage: LT-92536 - Daily Timetable Print Functionality

## Coverage Strategy

| Area | Business Rules | Logic Type | Technique | Risk | Depth | Cases |
|---|---|---|---|---|---|---:|
| Entry point and dialog | BR-01, BR-13, BR-14 | Conditional UI | Decision Table | High | Standard | 8 |
| New PDF URL and filename | BR-01 | Integration | Scenario | High | Standard | 3 |
| Published-only data filter | BR-03, BR-04, BR-05 | Query filter | Decision Table | Critical | Deep | 5 |
| Timeslot-mode grouping | BR-02, BR-07, BR-09, BR-10 | Grouping/sorting | BVA, Pairwise | Critical | Deep | 7 |
| Manual-time grouping | BR-08, BR-09, BR-10 | Grouping/sorting | BVA | High | Deep | 4 |
| PDF layout/content fields | BR-06, BR-11, BR-12 | Display completeness | Component, Visual regression | Critical | Deep | 13 |
| Empty/error states | BR-10, BR-11 | Negative path | Boundary, Error guessing | High | Standard | 3 |
| Regression guards | BR-13, BR-14 | Compatibility | Regression | High | Standard | 3 |

Estimated total: 46 cases.

## High-Risk Notes

- `Status__c = Published` is stricter than the old print dialog copy. Completed lessons must be excluded in the new Individual timetable PDF even if the UI still mentions Completed.
- Timeslot mode uses active Timeslot Masters but current implementation only renders timeslots used by lessons. PRD says empty AM/PM timeslot templates should remain; testcase should detect this mismatch.
- PDF validation needs visual checks: A3 landscape, four blocks per page, bottom-right stamp rectangle, stable borders, headers, wrapping, and no overlap.
- Classroom sorting and all-classroom row generation are important for classroom management. A lesson in only one classroom must not remove other classroom rows.
- Remarks are derived from the same student's other timeslot lessons on the same day/location, so multi-lesson fixtures must be prepared carefully.

## Suggested Suite Structure

```
Qase PX > Manabie Scheduling > CORE FEATURES > Event Master > update testcase > Calendar lesson
  LT-92536 - Daily Timetable Print Functionality
    - Entry point and feature flag
    - Individual PDF data filters
    - Timeslot-mode layout
    - Manual-time layout
    - Visual and edge regressions
```

## Existing Coverage Reused

| Existing area | Existing coverage | New coverage needed |
|---|---|---|
| Baseline Print Out menu/dialog | Existing Calendar Daily View print-out spec and Qase calendar suite | Keep smoke/regression only; focus deeper tests on new Individual PDF. |
| Timeslot Master CRUD | `PBT-2130` / Timeslot Master tests | Treat Timeslot Master records as fixtures; verify print consumption only. |
| Legacy Group PDF | Existing `CalendarPrintOutPdf` behavior | Verify Group still uses legacy flow; do not redesign Group layout here. |
| PDF UI parity bug | `LT-103358` | Add visual regression checks for header bar, borders, page sizing, and layout stability. |

## Test Data Matrix

| Fixture | Purpose |
|---|---|
| Location `Tokyo Center` with classrooms Booth A, Booth B, Booth C sorted by Sequence | Verify all classroom rows and sorting. |
| Active Timeslots 1-5 with AM/PM split and sequence order | Verify timeslot block order, AM/PM split, and page overflow. |
| Published Individual lessons across multiple classrooms and timeslots | Verify included data and grouping. |
| Draft, Completed, Cancelled, Group, other-date, other-location lessons | Verify exclusion filters. |
| Student with two published lessons in different timeslots | Verify Remarks column. |
| Seasonal student enrollment at selected location | Verify course star marker. |
| Long CJK/Latin student/course/teacher values | Verify fixed-width wrapping without overlap. |
