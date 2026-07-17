# Test Cases: LT-103679 — [EEA] Core | Weekly Calendar view in Daily-view style

**Suite:** Weekly Calendar in Daily-view style
**Qase suite:** PX > Calendar > suite 2717
**Epic:** https://manabie.atlassian.net/browse/LT-103679

---

## Suite: Weekly Calendar in Daily-view style

### Calendar Weekly Daily-Style View - Mode Visibility - New weekly daily-style mode is available

**Description:** Core availability — Staff can access the new weekly calendar mode that renders a 7-day range in Daily View layout.

**Preconditions:**
- Logged in as staff user with calendar access.
- Calendar feature build includes LT-103679.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Lesson Calendar. | Calendar landing page is displayed. | surface = lesson_calendar |
| 2 | Open the view mode selector. | Existing calendar view options are shown. | action = open_view_selector |
| 3 | Observe the available modes. | A new weekly daily-style view option is visible and selectable. | expected_mode = weekly_daily_style |

**Severity:** critical
**Priority:** high

---

### Calendar Weekly Daily-Style View - Teacher Filter Required - Selecting a teacher loads the 7-day schedule

**Description:** Core flow — After selecting a teacher, the calendar shows that teacher's 7-day schedule in Daily View layout.

**Preconditions:**
- Logged in as staff user with calendar access.
- Weekly daily-style mode is available.
- Teacher T1 has lessons in the target week.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Switch the calendar to weekly daily-style mode. | Mode switches successfully. | mode = weekly_daily_style |
| 2 | Select Teacher T1 in the teacher filter. | Teacher T1 is applied as active filter. | teacher = T1 |
| 3 | Wait for calendar data to load. | The schedule for Teacher T1 is displayed across 7 days in daily-style layout. | week = current |

**Severity:** critical
**Priority:** high

---

### Calendar Weekly Daily-Style View - Seven Consecutive Days - Calendar displays one full week in date order

**Description:** Layout integrity — The view shows 7 consecutive days sorted by date from the selected week.

**Preconditions:**
- Weekly daily-style mode is open.
- Teacher T1 is selected.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open weekly daily-style view for a known week. | Calendar renders the weekly board. | teacher = T1 |
| 2 | Read the day/date headers from left to right. | Exactly 7 day columns are shown. | expected_days = 7 |
| 3 | Compare header order. | Headers are arranged in chronological order for the selected week. | expected_order = ascending_by_date |

**Severity:** critical
**Priority:** high

---

### Calendar Weekly Daily-Style View - Actual Lesson Duration - Lesson cards reflect real time length

**Description:** Visual accuracy — Lessons are rendered with height/length matching their actual scheduled duration, similar to Daily View.

**Preconditions:**
- Weekly daily-style mode is open.
- Teacher T1 has at least 2 lessons with different durations in the same week.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the weekly daily-style view for Teacher T1. | Teacher T1 schedule is displayed. | teacher = T1 |
| 2 | Locate Lesson A and Lesson B with different durations. | Both lesson cards are visible in the grid. | duration_A != duration_B |
| 3 | Compare visual block lengths against scheduled times. | Longer lesson occupies visibly more vertical space/time range than shorter lesson, consistent with actual duration. | sample_durations = 30m_vs_90m |

**Severity:** critical
**Priority:** high

---

### Calendar Weekly Daily-Style View - Multi-location Visibility - Teacher lessons from different locations are shown in one weekly surface

**Description:** Cross-location visibility — Staff can review the selected teacher's lessons from different locations in the same weekly daily-style schedule.

**Preconditions:**
- Weekly daily-style mode is open.
- Teacher T1 has lessons in the selected week across multiple locations.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open weekly daily-style view for Teacher T1. | Schedule grid loads. | teacher = T1 |
| 2 | Locate lessons from Location A and Location B in the week. | Lessons from both locations are present in the weekly view. | locations = A_and_B |
| 3 | Inspect lesson labels/details. | Each lesson shows the correct location context without requiring a different view mode. | expected_location_display = correct |

**Severity:** major
**Priority:** high

---

### Calendar Weekly Daily-Style View - Teacher Scope - Only selected teacher's lessons are shown

**Description:** Filter correctness — The view is scoped to the selected teacher and does not mix in lessons from other teachers.

**Preconditions:**
- Weekly daily-style mode is open.
- Teacher T1 and Teacher T2 both have lessons in the same week.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Select Teacher T1 in weekly daily-style view. | Filter is applied. | teacher = T1 |
| 2 | Review visible lesson cards for the week. | Only lessons assigned to Teacher T1 are shown. | expected_teacher_scope = T1_only |
| 3 | Switch filter to Teacher T2 and reload the week. | View refreshes to show only Teacher T2 lessons; Teacher T1 lessons are no longer visible. | teacher = T2 |

**Severity:** critical
**Priority:** high

---

### Calendar Weekly Daily-Style View - Empty-day Handling - Days with no lessons remain visible with empty timeline

**Description:** Negative layout — A day without lessons still appears in the 7-day range and does not collapse the weekly board.

**Preconditions:**
- Weekly daily-style mode is open.
- Selected teacher has no lessons on at least one day in the target week.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open weekly daily-style view for a week containing at least one no-lesson day. | Weekly grid loads. | teacher = T1 |
| 2 | Locate the day column with no lessons. | The day column is still rendered. | expected_empty_day = visible |
| 3 | Observe the empty timeline area. | No lesson cards are shown for that day, but the day header and timeline remain intact. | empty_state = no_cards |

**Severity:** major
**Priority:** medium

---

### Calendar Weekly Daily-Style View - Week Navigation - Previous and next week keep mode and teacher filter

**Description:** Navigation flow — Moving between weeks keeps the selected mode and teacher context while refreshing data to the new 7-day range.

**Preconditions:**
- Weekly daily-style mode is open.
- Teacher T1 is selected.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | In weekly daily-style view, click Next Week. | Calendar moves to the next 7-day range. | nav = next_week |
| 2 | Observe active controls after navigation. | Weekly daily-style mode and Teacher T1 filter remain selected. | expected_state = mode_and_teacher_persist |
| 3 | Click Previous Week to return. | Original week reloads with the same mode and teacher filter intact. | nav = previous_week |

**Severity:** major
**Priority:** high

---

### Calendar Weekly Daily-Style View - Dense schedule readability - Overlapping or adjacent lessons remain distinguishable

**Description:** Readability — When a teacher has a busy week/day, lesson cards remain distinguishable and usable in the daily-style weekly layout.

**Preconditions:**
- Weekly daily-style mode is open.
- Teacher T1 has multiple lessons on the same day, including adjacent or close time slots.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open weekly daily-style view for the dense-schedule day. | The target day column is visible. | teacher = T1 |
| 2 | Inspect adjacent lesson cards in the same day. | Cards do not visually merge incorrectly; boundaries between lessons remain clear. | density = adjacent_lessons |
| 3 | Click each lesson card in sequence. | Each card is individually selectable and opens the correct lesson detail/interaction target. | action = open_lesson |

**Severity:** major
**Priority:** medium

---

### Calendar Weekly Daily-Style View - Regression - Existing calendar views remain unchanged

**Description:** Regression — Adding the new weekly daily-style mode does not break existing daily view and standard weekly view behavior.

**Preconditions:**
- Logged in as staff user with calendar access.
- Existing daily view and weekly view are available.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open existing Daily View and verify normal rendering. | Daily View behaves as baseline. | view = daily |
| 2 | Switch to standard Weekly View and verify rendering. | Standard Weekly View behaves as baseline. | view = weekly_standard |
| 3 | Return to weekly daily-style mode. | New mode remains available without affecting the other view modes. | view = weekly_daily_style |

**Severity:** major
**Priority:** high
