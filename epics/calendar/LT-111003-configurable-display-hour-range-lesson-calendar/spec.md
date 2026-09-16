# LT-111003 - Configurable Display Hour Range on Lesson Calendar per Partner

## Sources

- Jira: https://manabie.atlassian.net/browse/LT-111003
- Related Jira/tech review: PBT-3939
- Baseline PRD for fixed range: Confluence page `2226913367` - Lesson Calendar Display Time Limit / PBT-1987
- Slack source read directly: `C0BPM7GABDW / 1789107155.218869` - MANACS-2599 / PBT-3939 discussion that led to LT-111003.
- Earlier Slack URL `C0BPM7GABDW / 1789518469.735749` was a different incident about duplicate Aver Lesson Reports and is not used for this epic.

## Objective

Allow each partner to configure which hour sections are shown on the Lesson Calendar instead of forcing one fixed range for every partner.

## Current Behavior

- Previous Renseikai requirement limited the Lesson Calendar view to 06:00-23:00 to avoid empty overnight slots.
- Slack clarification says the current visible Calendar behavior was observed as "showing until 22:59 only", so 23:00-23:59 visibility is an explicit regression risk.
- Lessons/events outside the visible display window are hidden from the calendar view without changing lesson data.
- Current Calendar V2 code generates hour sections from `rangeTime.startHour` to `rangeTime.endHour`.
- Calendar filtering compares the item's start hour with `rangeTime.startHour <= startHour <= rangeTime.endHour`.
- Multi-day events intentionally bypass the range-time filter because they are shown as spanning bars.

## New Behavior

- Partner-level setting controls Lesson Calendar display range:
  - `startHour`
  - `endHour`
- Default for partners with no custom setting remains 06:00-23:00.
- Nichibei must be configurable to 00:00-23:00.
- The original adjustment request extended lesson end time to 23:59, but that does not solve lessons starting after 23:59; those become 00:00-05:59 next-day starts and need full-day hour sections.
- Daily and weekly Lesson Calendar views use the same configured range.
- Lessons starting 00:00-05:59 become visible for partners configured to 00:00-23:00.
- Lessons starting 23:00-23:59 appear in the 23:00 section.
- Changing the setting updates the calendar display without changing existing lesson start/end data.
- Display range is not derived from company opening hours because opening hours can differ by day.
- Timezone remains partner timezone.

## Source Code Impact Notes

- `createHoursSectionList(startHour, endHour)` renders each visible hour section inclusively.
- `filterEvent` uses the visible range to hide single-day items whose start hour is outside the configured range.
- Other-location lessons in `useGetLessonsOnCalendarSF` are also filtered by `rangeTime` when lesson enhancement is enabled.
- Daily teacher/classroom tables, lesson width/margin calculation, weekly teacher view, DnD slots, and scroll-to-first-event behavior all consume `startHour` and `endHour`.
- Existing code constants include both 00:00-23:00 and enhanced 06:00-22:00 values; LT-111003 acceptance requires default 06:00-23:00, so test coverage must catch any 23:00 section regression.

## Out of Scope

- Changing lesson start/end data.
- Deriving calendar display range from operating/opening hours.
- Blocking lesson creation outside the displayed range in other modules.
- Changing public learner calendar or timetable PDF behavior unless those screens reuse the Lesson Calendar view state.
