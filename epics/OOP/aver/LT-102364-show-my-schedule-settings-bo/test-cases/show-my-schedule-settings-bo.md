# LT-102364 Test Cases - Show my schedule settings in BO

## LT-102364-TC-001 - Calendar default remains ON when remove-default flag is OFF

Preconditions:
- Logged in to BO as an Aver user with access to Lesson Calendar.
- `lesson.lessonmgmt_sf.is_enabled = true`.
- `lesson.remove_default_teacher_filter.is_enabled = false`.
- `lesson.limit_teacher_access_other_lessons.is_enabled = false`.
- Browser/reactive storage for Calendar filters is cleared.
- Calendar has one lesson assigned to the logged-in teacher and one lesson assigned to another teacher in an accessible location.

Steps:
1. Open BO Lesson Calendar.
2. Open the Calendar filter panel.
3. Observe `Show my schedule`.
4. Inspect the active teacher filter/request or the visible lessons.

Expected:
1. Calendar loads in BO-calling-SF mode.
2. Filter panel opens successfully.
3. `Show my schedule` is visible and checked by default.
4. Current teacher id is included in the active teacher filter; only schedules assigned to the logged-in teacher are shown.

## LT-102364-TC-002 - Calendar default becomes OFF when remove-default flag is ON

Preconditions:
- Logged in to BO as an Aver staff/teacher user with Calendar access.
- `lesson.lessonmgmt_sf.is_enabled = true`.
- `lesson.remove_default_teacher_filter.is_enabled = true`.
- `lesson.limit_teacher_access_other_lessons.is_enabled = false`.
- Browser/reactive storage for Calendar filters is cleared.
- Calendar has schedules assigned to the logged-in teacher and another teacher in an accessible location.

Steps:
1. Open BO Lesson Calendar.
2. Open the Calendar filter panel.
3. Observe `Show my schedule`.
4. Inspect the active teacher filter/request.
5. Compare visible schedules.

Expected:
1. Calendar loads in BO-calling-SF mode.
2. Filter panel opens successfully.
3. `Show my schedule` is visible and unchecked by default.
4. Current teacher id is not auto-included in active teacher ids.
5. Schedules are not restricted to only the logged-in teacher; other accessible schedules remain visible according to existing location/access filters.

## LT-102364-TC-003 - Calendar limit teacher access keeps default ON

Preconditions:
- Logged in to BO as an Aver teacher or part-time teacher.
- `lesson.lessonmgmt_sf.is_enabled = true`.
- `lesson.remove_default_teacher_filter.is_enabled = true`.
- `lesson.limit_teacher_access_other_lessons.is_enabled = true`.
- Browser/reactive storage for Calendar filters is cleared.
- Calendar has schedules assigned to the logged-in teacher and another teacher.

Steps:
1. Open BO Lesson Calendar.
2. Open the Calendar filter panel.
3. Observe `Show my schedule`.
4. Inspect the active teacher filter/request.

Expected:
1. Calendar loads successfully.
2. Filter panel opens successfully.
3. `Show my schedule` is checked by default because limited teacher access overrides the remove-default flag.
4. Current teacher id is included in the active teacher filter and non-assigned schedules are not exposed through default view.

## LT-102364-TC-004 - Show my schedule hidden outside BO-calling-SF

Preconditions:
- User can access Calendar in either pure SF app mode or BO mode with `lesson.lessonmgmt_sf.is_enabled = false`.
- Calendar filter panel is available.

Steps:
1. Open Calendar in the non BO-calling-SF context.
2. Open the filter panel.
3. Search for the `Show my schedule` filter row.
4. Inspect the request/filter state.

Expected:
1. Calendar opens successfully.
2. Filter panel opens successfully.
3. `Show my schedule` is not rendered.
4. No current teacher id is auto-added by the hidden control.

## LT-102364-TC-005 - Manual toggle ON appends current teacher under default OFF

Preconditions:
- Same setup as LT-102364-TC-002.
- `Show my schedule` is currently unchecked.

Steps:
1. Open the Calendar filter panel.
2. Check `Show my schedule`.
3. Apply/close the filter panel if required by the UI.
4. Inspect the active teacher filter/request.
5. Compare visible schedules.

Expected:
1. Filter panel opens successfully.
2. Checkbox becomes checked.
3. Filter state updates without clearing date/location/type filters.
4. Current teacher id is appended once to active teacher ids.
5. Calendar narrows to schedules assigned to the logged-in teacher.

## LT-102364-TC-006 - Manual toggle OFF removes auto teacher filtering

Preconditions:
- Same setup as LT-102364-TC-001.
- `Show my schedule` is currently checked by default.
- Date/location/course/class filters have selected values.

Steps:
1. Open the Calendar filter panel.
2. Uncheck `Show my schedule`.
3. Apply/close the filter panel if required by the UI.
4. Inspect the active teacher filter/request.
5. Inspect the other selected filters.

Expected:
1. Filter panel opens successfully.
2. Checkbox becomes unchecked.
3. Current teacher id is removed from the auto teacher filter.
4. Calendar is no longer restricted to only the logged-in teacher unless the user explicitly selected a teacher elsewhere.
5. Date/location/course/class filters remain unchanged.

## LT-102364-TC-007 - Activity events are not incorrectly limited by current teacher when default OFF

Preconditions:
- Same setup as LT-102364-TC-002.
- Calendar event type filter includes Activity Event.
- Activity Event A is assigned to another teacher in an accessible location.
- Activity Event B is assigned to the logged-in teacher.

Steps:
1. Open BO Lesson Calendar.
2. Ensure `Show my schedule` is unchecked by default.
3. Enable Activity Event scope if it is not already enabled.
4. Observe visible activity events.

Expected:
1. Calendar loads successfully.
2. `Show my schedule` remains unchecked.
3. Activity Event scope is active.
4. Activity events are not filtered to only the logged-in teacher; accessible events assigned to other teachers can be displayed.

## LT-102364-TC-008 - Legacy Calendar path honors remove-default behavior

Preconditions:
- Legacy BO Calendar path is reachable in the environment.
- `lesson.lessonmgmt_sf.is_enabled = true`.
- `lesson.remove_default_teacher_filter.is_enabled = true`.
- `lesson.limit_teacher_access_other_lessons.is_enabled = false`.
- Calendar reactive storage is cleared.

Steps:
1. Open the legacy BO Calendar surface.
2. Open the filter panel.
3. Observe `Show my schedule`.
4. Inspect active teacher ids.

Expected:
1. Legacy Calendar opens successfully if still supported.
2. Filter panel opens successfully.
3. `Show my schedule` is unchecked by default.
4. Current teacher id is not auto-added.

Note:
- Current code review found regression risk in `CalendarFilterProvider.tsx`: it defaults `showMySchedule` to true when BO calls SF and does not read `lesson.remove_default_teacher_filter.is_enabled`.

## LT-102364-TC-009 - Lesson List default keeps current teacher when remove-default flag is OFF

Preconditions:
- Logged in to BO Lesson List as an Aver user.
- `lesson.remove_default_teacher_filter.is_enabled = false`.
- `lesson.limit_teacher_access_other_lessons.is_enabled = false`.
- `LESSON_SF_LESSON_FILTER` storage is absent or has `isFilterDirty = false`.
- Lessons exist for the logged-in teacher and another teacher.

Steps:
1. Open BO Lesson List.
2. Open advanced filters.
3. Inspect the Teachers field/chip.
4. Apply the default filters.
5. Inspect the list results/request.

Expected:
1. Lesson List loads successfully.
2. Advanced filters open.
3. Teachers field contains the logged-in teacher by default.
4. Default filters apply successfully.
5. Lesson List is filtered by the logged-in teacher.

## LT-102364-TC-010 - Lesson List default removes current teacher when remove-default flag is ON

Preconditions:
- Logged in to BO Lesson List as an Aver staff/teacher user without limited teacher access.
- `lesson.remove_default_teacher_filter.is_enabled = true`.
- `lesson.limit_teacher_access_other_lessons.is_enabled = false`.
- `LESSON_SF_LESSON_FILTER` storage is absent or has `isFilterDirty = false`.
- Lessons exist for the logged-in teacher and another teacher in accessible scope.

Steps:
1. Open BO Lesson List.
2. Open advanced filters.
3. Inspect the Teachers field/chip.
4. Apply the default filters.
5. Inspect the list results/request.

Expected:
1. Lesson List loads successfully.
2. Advanced filters open.
3. Teachers field is empty by default.
4. Default filters apply successfully.
5. Lesson List request does not auto-send the logged-in teacher id; accessible lessons for other teachers are not removed by the default teacher filter.

## LT-102364-TC-011 - Lesson List limited teacher access forces current teacher on reset and delete

Preconditions:
- Logged in to BO Lesson List as an Aver teacher or part-time teacher.
- `lesson.remove_default_teacher_filter.is_enabled = true`.
- `lesson.limit_teacher_access_other_lessons.is_enabled = true`.
- Advanced filters are open.

Steps:
1. Observe the Teachers field default.
2. Click Reset filters.
3. Try deleting the logged-in teacher filter chip.
4. Apply filters.

Expected:
1. Teachers field contains the logged-in teacher.
2. Reset keeps or restores the logged-in teacher.
3. Deleting the chip restores the logged-in teacher because limited teacher access is active.
4. List remains restricted to the logged-in teacher.

## LT-102364-TC-012 - Lesson List dirty saved filters are respected

Preconditions:
- Logged in to BO Lesson List.
- `lesson.remove_default_teacher_filter.is_enabled = true`.
- `lesson.limit_teacher_access_other_lessons.is_enabled = false`.
- User previously applied a filter with Teacher X selected so `LESSON_SF_LESSON_FILTER.isFilterDirty = true`.

Steps:
1. Reload BO Lesson List.
2. Open advanced filters.
3. Inspect the Teachers field/chip.
4. Apply filters without changing teacher.

Expected:
1. Lesson List reloads successfully.
2. Advanced filters open.
3. Previously selected Teacher X remains selected; the defaulting logic does not replace it with empty teachers or current user.
4. Request uses Teacher X as the user-saved filter.

## LT-102364-TC-013 - Tenant config switch changes default after storage is cleared

Preconditions:
- Same BO user can test both config states.
- Calendar and Lesson List filter storages are cleared between config changes.

Steps:
1. Set `lesson.remove_default_teacher_filter.is_enabled = false` and open Calendar/Lesson List.
2. Record default `Show my schedule` and Teachers field.
3. Clear Calendar and Lesson List filter storage.
4. Set `lesson.remove_default_teacher_filter.is_enabled = true` with limited teacher access inactive.
5. Reopen Calendar/Lesson List and inspect defaults.

Expected:
1. Old/default config opens with current teacher filtering active.
2. Calendar shows `Show my schedule` checked and Lesson List has current teacher selected.
3. Storage is cleared so saved filters do not mask defaults.
4. New config is active.
5. Calendar shows `Show my schedule` unchecked and Lesson List Teachers field is empty.

## LT-102364-TC-014 - Other Calendar filters remain stable when Show my schedule changes

Preconditions:
- BO Calendar is in BO-calling-SF mode.
- `lesson.remove_default_teacher_filter.is_enabled = true`.
- Date, location, course/class, lesson status, and type filters have selected values.

Steps:
1. Open Calendar filter panel.
2. Toggle `Show my schedule` ON.
3. Toggle `Show my schedule` OFF.
4. Inspect the other selected filters after each toggle.
5. Inspect the resulting Calendar data.

Expected:
1. Filter panel opens successfully.
2. Only `Show my schedule` and active teacher ids change.
3. Only `Show my schedule` and active teacher ids change again.
4. Date, location, course/class, lesson status, and type filters remain selected.
5. Calendar data changes only by teacher filtering within the same date/location/type scope.
