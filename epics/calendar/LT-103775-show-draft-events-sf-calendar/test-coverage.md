# Test Coverage: LT-103775 - Show Draft Events in SF Lesson Calendar

## Coverage Strategy

| Area | Business Rules | Logic Type | Technique | Risk | Depth | Cases |
|---|---|---|---|---|---|---:|
| Feature flag visibility | BR-01, BR-02, BR-08 | Conditional logic | Decision Table | Critical | Deep | 3 |
| Calendar rendering | BR-03, BR-05, BR-07 | Display completeness | Component, Regression | High | Deep | 5 |
| Detail drawer | BR-11 | Cross-system impact | Scenario | High | Standard | 2 |
| Status filter | BR-04, BR-05 | Conditional logic | Decision Table | Critical | Deep | 4 |
| Other filters | BR-06, BR-07 | Conditional logic | Pairwise | High | Standard | 4 |
| Drag and drop | BR-08, BR-09, BR-10 | State transition, Data integrity | State Transition, BVA | Critical | Deep | 8 |
| Non-SF downstream guard | BR-12 | Cross-system impact | Regression | Critical | Standard | 3 |

Estimated total: 30 cases.

## High-Risk Notes

- Drag/drop is the highest risk because the edit form loads existing record data asynchronously. `formActivityEvent` must re-apply dropped date/time after hydration; otherwise the modal can silently revert to the old schedule.
- Status filter reuses `lessonStatusMap` for both lessons and Activity Events. A regression could show Draft lessons but still hide Draft events.
- The Draft feature flag is SF-only; non-SF calendar paths return disabled and must not show Draft Activity Events.
- Draft Events must not leak to Learner app, Booking system, or public event APIs.

## Suggested Suite Structure

```
Qase PX > <suite TBD>
  LT-103775 - SF Calendar Draft Activity Events
    - Flag and rendering
    - Detail drawer and filters
    - Drag and drop
    - Downstream visibility regression
```

## Coverage Gaps From Existing LT-96096

| Existing baseline | Covered there | New coverage here |
|---|---|---|
| Draft status picklist and create/edit/delete/duplicate | Yes | Only referenced as precondition |
| Draft hidden from Learner app and Booking | Yes | Regression guard because calendar visibility now exposes Draft on SF |
| Status transitions | Yes | Drag/drop preserves Draft/Published status on Calendar edit |
| Calendar Draft Event visual/detail/filter/drag-drop | No | Full coverage in this suite |
