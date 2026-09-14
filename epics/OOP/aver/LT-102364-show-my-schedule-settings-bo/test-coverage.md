# LT-102364 Test Coverage

## Coverage Matrix

| Case ID | Area | AC | Risk Covered |
|---|---|---|---|
| LT-102364-TC-001 | Calendar | AC 01.2 | Existing default behavior remains ON when remove-default-teacher-filter is OFF. |
| LT-102364-TC-002 | Calendar | AC 01.3 | Configured tenant can default OFF and avoid applying current teacher automatically. |
| LT-102364-TC-003 | Calendar | AC 01.4 | Limit teacher access overrides the remove-default setting. |
| LT-102364-TC-004 | Calendar | AC 01.1 | Show my schedule is hidden outside BO-calling-SF context. |
| LT-102364-TC-005 | Calendar | AC 01.5 | Manual toggle ON appends current user and narrows schedule. |
| LT-102364-TC-006 | Calendar | AC 01.5 | Manual toggle OFF removes auto teacher filtering without clearing unrelated filters. |
| LT-102364-TC-007 | Calendar | AC 01.3 | Activity events are not incorrectly filtered by current teacher when default OFF. |
| LT-102364-TC-008 | Calendar legacy | AC 01.3 | Legacy Calendar provider gap/regression check for the new flag. |
| LT-102364-TC-009 | Lesson List | AC 02.1 | Existing default teacher filter remains for tenants without the new config. |
| LT-102364-TC-010 | Lesson List | AC 02.2 | New config removes default teacher filter from Lesson List. |
| LT-102364-TC-011 | Lesson List | AC 02.3 | Teacher access limit forces current teacher on reset/delete. |
| LT-102364-TC-012 | Lesson List | AC 02.4 | Dirty saved user filters are not overwritten by default logic. |
| LT-102364-TC-013 | Calendar + Lesson List | AC 01.3, AC 02.2 | Tenant switch changes defaults after clearing local storage/session state. |
| LT-102364-TC-014 | Calendar | AC 01.5 | Search/date/location/course/class filters remain stable when Show my schedule changes. |

## Automation Notes

- Use controlled feature-setting fixtures for:
  - `lesson.lessonmgmt_sf.is_enabled`
  - `lesson.remove_default_teacher_filter.is_enabled`
  - `lesson.limit_teacher_access_other_lessons.is_enabled`
- Use at least three teachers:
  - `T_CURRENT`: logged-in teacher
  - `T_OTHER_1`: teacher in same accessible location
  - `T_OTHER_2`: teacher outside accessible location
- Use at least three schedule records:
  - Lesson assigned to `T_CURRENT`
  - Lesson assigned to `T_OTHER_1`
  - Activity event assigned to `T_OTHER_1`
- Clear reactive storage before default-state cases:
  - Calendar: `FILTER_LESSON`, `ACTIVE_FILTER_LESSON`
  - Lesson List: `LESSON_SF_LESSON_FILTER`
- For request-level automation, assert teacher filters rather than only UI row counts:
  - Default ON: current teacher id included
  - Default OFF: current teacher id not auto-included
  - Limit teacher access: current teacher id restored after reset/delete

## Regression Guardrails

- Do not assert the Event Master form has start date/end date; this epic affects Calendar/Lesson List filters only.
- Do not mix LT-101770 auto-location behavior from the same release note page.
- Validate both visible checkbox state and downstream filter/query behavior.
- Validate Lesson List separately from Calendar because it uses a different plugin path.
