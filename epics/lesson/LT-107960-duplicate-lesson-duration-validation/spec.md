---
ticket_id: LT-107960
ticket_url: https://manabie.atlassian.net/browse/LT-107960
title: Duplicate Lesson Duration field should not show required validation when value exists
module: scheduling
bucket: lesson
status: Need Clarify
internal_uat_date: null
production_release_date: null
last_updated: 2026-09-18
---

# LT-107960: Duplicate Lesson Duration required validation regression

## Summary

When staff duplicates an individual lesson from Lesson Detail or Calendar, the Duplicate Lesson form auto-populates `Duration (minutes)` from Start Time and End Time. The reported staging bug shows `Duration = 60`, but clicking Save still triggers the required validation message `Complete this field.`.

Expected behavior: if Duration already has a valid value, the form must not trigger required validation and the duplicate lesson should save successfully.

## Source Context

- Jira: `LT-107960`
- Existing related Qase cases:
  - `PX-1207` - Duplicate Lesson happy path, but no Duration validation assertion.
  - `PX-20708` - Duration field visible on Lesson form, but not Duplicate Lesson.
  - `PX-20734` - Duration field visible from Calendar create form, but not duplicate validation.
- Related repo coverage:
  - `epics/cross-domain/LT-86458-validate-time-duration` covers Duration validation generally.
  - `epics/lesson/LT-XXXX-create-lesson/test-cases/duplicate-lesson.md` covers Duplicate Lesson broadly.

## Acceptance Criteria

### AC 01 - Duplicate Lesson from Lesson Detail

- AC 01.1: Duplicate Lesson form opens with Duration calculated from source Start Time and End Time.
- AC 01.2: Clicking Save with a valid auto-populated Duration does not show `Complete this field.`
- AC 01.3: The duplicated lesson is created successfully.

### AC 02 - Duplicate Lesson from Calendar

- AC 02.1: Duplicating from Calendar opens the same valid Duration state.
- AC 02.2: Calendar duplicate save does not show required validation when Duration has a value.

### AC 03 - Related form regressions

- AC 03.1: Edit mode with valid Duration does not show false required validation.
- AC 03.2: Extend Recurrence form with prefilled Duration does not show false required validation.
- AC 03.3: Drag-and-drop edit flow with derived Duration does not show false required validation.

## Business Rules

| # | AC | Rule |
|---|---|---|
| 1 | AC 01.1 | Duration is calculated from Start Time and End Time when Duplicate Lesson form opens. |
| 2 | AC 01.2 / AC 02.2 | Required validation must use the current Duration value, not stale empty field state. |
| 3 | AC 01.3 | Valid duplicate lesson data saves successfully. |
| 4 | AC 03.1-03.3 | Shared Duration validation behavior must be consistent across edit, Extend Recurrence, and drag/drop forms. |

## Assumptions

- Exact source lesson from Jira has Start Time `06:40`, End Time `07:40`, Duration `60`.
- Exact validation copy is `Complete this field.`.
- If the implementation changes field label wording, the test should still assert no required validation is shown on the Duration field and save succeeds.
