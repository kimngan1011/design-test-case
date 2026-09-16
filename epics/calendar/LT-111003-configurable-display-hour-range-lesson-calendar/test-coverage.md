# Test Coverage: LT-111003 - Configurable Display Hour Range on Lesson Calendar per Partner

## New Test Suite Recommendation

- Qase parent suite: `PX > ... > Calendar lesson` (`suite_id=2717`)
- New child suite suggestion: `Configurable Display Hour Range on Lesson Calendar (LT-111003)`

## Coverage Matrix

| Area | Coverage |
|---|---|
| Default partner behavior | No custom setting keeps 06:00-23:00 visible and hides 00:00-05:59 lessons. |
| Nichibei full-day behavior | 00:00-23:00 setting shows midnight and early-morning lessons in Daily and Weekly views. |
| Boundary values | 00:00, 05:59, 06:00, 22:59, 23:00, 23:59. |
| Data integrity | Changing display range does not change lesson start/end time. |
| Partner isolation | Nichibei setting does not affect Renseikai or other default partners. |
| Timezone | Lesson placement uses partner timezone, not browser timezone. |
| Daily layout | Hour sections, card positions, card width/margins, horizontal scroll, teacher/classroom rows. |
| Weekly layout | Weekly slot labels, scroll-to-first-event/current-time behavior, teacher weekly mode. |
| Calendar filters | Teacher, classroom, location, lesson status, lesson/event type filters still combine with display range. |
| Other-location lessons | Cross-location daily teacher view only shows permitted lessons inside the configured range. |
| DnD/create from calendar | 10-minute grids and dropped/created start times work inside the configured range and reject outside-range drop zones. |
| Configuration validation | Missing/invalid display hour config safely falls back or blocks save according to settings validation. |

## Existing Qase Testcases Likely Impacted

Directly impacted:

- `PX-23774` - Calendar Daily View - BO - Overflow Timeline - Horizontal Scrollbar Visible and Reachable
- `PX-23775` - Calendar Daily View - SF - Non-Overflow Timeline - Content Fully Visible Without Horizontal Scroll
- `PX-23776` - Calendar Daily View - Viewport and Zoom Matrix - Scrollbar Behavior Stays Consistent
- `PX-23784` - Calendar Daily View - SF - Overflow Timeline - Horizontal Scrollbar Visible and Reachable
- `PX-24936` to `PX-24945` - Calendar Weekly Daily-Style View cases
- `PX-25845` to `PX-25848` - 7-Day Teacher Schedule View cases
- `PX-22356` - Teacher View Daily View - Teacher with multiple lessons across locations same day
- `PX-22358` to `PX-22364` - Lesson Card UI Daily/Weekly View layout cases

Near-impact / regression candidates:

- `PX-16122`, `PX-16123`, `PX-17584`, `PX-17585` - Daily 10-minute grid and DnD snap behavior
- `PX-16124` to `PX-16127`, `PX-17581`, `PX-17582` - Weekly DnD/hour block behavior
- `PX-17576`, `PX-17577`, `PX-17592` to `PX-17608` - DnD permission, persistence, clash recalculation
- `PX-17609` to `PX-17611` - DnD Daily View performance with many teachers
- `PX-21253`, `PX-21255`, `PX-21269` - Create Lesson mode controls on SF Calendar
- `PX-22352`, `PX-22354`, `PX-22355` - Teacher daily other-location visibility and permissions

Not direct but worth awareness:

- Draft Activity Event calendar cases under suite `2717` remain behaviorally separate, but `PX-26137` style range-time checks should still pass with the partner-configured range.
- Koyu2 multi-day event cases under suite `3296` are not direct impact because LT-111003 is core partner display-range behavior and multi-day events bypass range-time filtering.

## Notes

- Correct Slack thread `C0BPM7GABDW / 1789107155.218869` was read directly. It confirms MANACS-2599 led to PBT-3939/LT-111003.
- Slack adds/clarifies three key risks already covered in the new cases: current Calendar was observed as showing only until 22:59, lessons starting after 23:59 become early next-day lessons that need 00:00-05:59 sections, and company opening hours must not drive Calendar display range.
- Earlier Slack URL `C0BPM7GABDW / 1789518469.735749` was MANACS-2608 Aver duplicate Lesson Report, unrelated to this epic.
- Current source has an enhanced range constant ending at 22. LT-111003 requires default 06:00-23:00; the new default-range cases intentionally assert the 23:00 section.
