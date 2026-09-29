# Test Cases: LT-107411 — Riso | Core | TAC improvement (July)

## Suite: AC-05 — Course and Sidebar Layout

### AC 05.1 – Course Required – Creation blocked when course field is null

**Description:** AC 05 — Equivalence Partitioning (Critical Risk) — Lesson creation is blocked when required Course field is null or not selected.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC (Teacher Availability Calendar)
- Create Lesson form is open
- Course field is visible and marked as required
- Courses available in system: ["Course A", "Course B", "Course C"]

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Riso TAC and click "Create Lesson" button | Create Lesson form opens with empty Course field | form_state = "empty" |
| 2 | Verify Course field is empty/null | Course field shows no value selected | course_value = null |
| 3 | Attempt to submit form without selecting Course | Form submission rejected or blocked | submit_action = "click_save" |
| 4 | Verify validation error message displayed | Error message shown (e.g., "Course is required") or create button disabled | error_message_present = true |
| 5 | Verify lesson is NOT created in database | Query lesson table; no orphaned record created | lesson_count_after = 0 |

**Severity:** critical
**Priority:** high

---

### AC 05.2 – Course Required – Creation allowed when course field is populated

**Description:** AC 05 — Equivalence Partitioning (Boundary) — Lesson creation is allowed when Course field is populated with a valid value.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC
- Create Lesson form is open
- Course field is required and visible
- Courses configured: ["Course A", "Course B", "Course C"]

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Riso TAC and click "Create Lesson" button | Create Lesson form opens | form_state = "empty" |
| 2 | Select "Course A" from Course dropdown | Course field populated with "Course A" | course_value = "Course A" |
| 3 | Fill other required fields (Subject, Teacher, Date/Time, Location) | Form populated with valid values | form_complete = true |
| 4 | Submit form by clicking Save/Create button | Form submission accepted | submit_action = "click_save" |
| 5 | Verify lesson created in database and displayed on calendar | Lesson record exists; visible on TAC | lesson_created = true |

**Severity:** critical
**Priority:** high

---

### AC 05.3 – Course Sticky Positioning – Header remains visible during Timeslot scroll (5 timeslots)

**Description:** AC 05 — Boundary Value Analysis — Course field header remains fixed/sticky while Timeslot content scrolls in left sidebar (5 rows).

**Preconditions:**
- User role: HQ/CM Staff or Teacher
- Location: Riso TAC with left sidebar visible
- Sidebar contains Course section + Timeslot section (scrollable)
- Timeslots displayed: 5 rows (e.g., 09:00, 10:00, 11:00, 12:00, 13:00)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Riso TAC on desktop/tablet | TAC loads with sidebar layout visible | device = "desktop" |
| 2 | Verify Course section visible at top of sidebar | Course field/header displayed | sidebar_section = "course" |
| 3 | Verify Timeslot section below Course with 5 rows | 5 timeslot rows visible | timeslot_count = 5 |
| 4 | Scroll down in Timeslot section (vertical scroll) | Timeslot content scrolls | scroll_action = "scroll_down" |
| 5 | Verify Course section header remains visible (sticky) | Course header does NOT scroll out of view; fixed position maintained | course_position = "sticky" |

**Severity:** minor
**Priority:** medium

---

### AC 05.4 – Course Sticky Positioning – Header remains visible during Timeslot scroll (20 timeslots)

**Description:** AC 05 — Boundary Value Analysis (Extended) — Course field header remains fixed/sticky while Timeslot content scrolls (20 rows, high-volume test).

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC with left sidebar
- Sidebar with Course section + Timeslot section (scrollable)
- High-volume timeslots: 20 rows (e.g., 06:00 through 21:00, hourly)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Riso TAC with 20 timeslots displayed | TAC loads with extended timeslot list | timeslot_count = 20 |
| 2 | Verify Course section visible at top | Course header displayed | sidebar_section = "course" |
| 3 | Scroll down through Timeslot section to bottom | Scroll through full timeslot range | scroll_distance = "full_height" |
| 4 | Verify Course header remains sticky and visible | Course does NOT scroll out of view during timeslot scroll | course_position = "sticky_at_20_rows" |
| 5 | Verify no overlap or collision between Course and Timeslot content | Layout remains clean, Course and Timeslot content separated | layout_integrity = "no_overlap" |

**Severity:** minor
**Priority:** medium

---

### AC 05.5 – Japanese Date Format – Calendar displays date as 7月1日 (no slash)

**Description:** AC 05 — Component + Validation — Japanese date format in calendar uses 7月1日 format without slash (/) separator.

**Preconditions:**
- User role: HQ/CM Staff or Teacher
- Location: Riso TAC
- Locale set to Japanese (JP)
- Calendar showing lessons with dates
- Date range includes July 1st, 2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Riso TAC with JP locale | TAC page loads with Japanese language settings | locale = "JP", date_today = "2026-07-01" |
| 2 | Verify calendar header or date display | Calendar shows dates in Japanese format | calendar_section = "header_or_timeslot" |
| 3 | Locate a date entry (e.g., July 1st) | Date visible on calendar | target_date = "2026-07-01" |
| 4 | Verify date format is "7月1日" (no slash) | Date displays exactly as "7月1日" (not "7/1" or "7月1日/") | expected_format = "7月1日" |
| 5 | Verify no slash character present | Format validation: slash count = 0 | slash_count = 0 |

**Severity:** trivial
**Priority:** low

---

## Test Data Dictionary

- `form_state`: State of Create Lesson form (empty, populated, submitted, etc.)
- `course_value`: Value in Course field (null, "Course A", "Course B", etc.)
- `submit_action`: Action to submit form (click_save, click_create, enter_key)
- `error_message_present`: Boolean indicating if validation error shown
- `lesson_count_after`: Number of lessons in database after attempted creation
- `form_complete`: Boolean; all required fields filled
- `lesson_created`: Boolean; lesson record exists in database
- `device`: Device type (desktop, tablet, mobile)
- `sidebar_section`: Sidebar section being tested (course, timeslot, filter)
- `timeslot_count`: Number of timeslot rows displayed
- `scroll_action`: Type of scroll (scroll_down, scroll_up, scroll_to_bottom)
- `course_position`: Positioning behavior (sticky, fixed, scrollable)
- `scroll_distance`: How far scrolled (partial_height, full_height, etc.)
- `layout_integrity`: Layout quality check (no_overlap, no_collision, clean_separation)
- `locale`: Language/region setting (JP = Japanese)
- `date_today`: Current or test date (YYYY-MM-DD format)
- `calendar_section`: Calendar area showing date (header, timeslot, cell)
- `target_date`: Date being validated (YYYY-MM-DD)
- `expected_format`: Expected date string format ("7月1日")
- `slash_count`: Number of slash (/) characters in formatted date (should be 0)
