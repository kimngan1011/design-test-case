# Test Cases: LT-107411 — Riso | Core | TAC improvement (July)

## Suite: AC-06 — Duplicate Lessons

### AC 06.1 – Duplicate Lessons – Two lessons in same timeslot consolidated to one calendar card

**Description:** AC 06 — Decision Table + CRUD (High Risk) — Multiple lessons (2) in one student's timeslot render as a single consolidated card on Lesson Calendar.

**Preconditions:**
- User role: HQ/CM Staff or Teacher
- Location: Riso TAC (Teacher Availability Calendar)
- Student: "Yamada Taro"
- Two lessons created for Yamada Taro on 2026-07-01 in timeslot 09:00-10:00:
  - Lesson A: Mathematics with Tanaka Yuki
  - Lesson B: Physics with Suzuki Hana
- Calendar view displays Riso TAC

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Riso TAC on 2026-07-01 (July 1st) | TAC page loads showing lessons for that date | date = "2026-07-01" (JST), calendar_timezone = "Asia/Tokyo" |
| 2 | Locate timeslot 09:00-10:00 on calendar | Timeslot cell visible | timeslot = "09:00-10:00" |
| 3 | Verify only ONE consolidated lesson card displayed | Single card shown in timeslot (not two separate cards) | lesson_cards_in_timeslot = 1 |
| 4 | Verify card shows consolidated representation (e.g., count badge or combined label) | Card indicates duplicates (e.g., "2 lessons" or badge with count) | consolidation_indicator = "visible" |

**Severity:** major
**Priority:** high

---

### AC 06.2 – Duplicate Lessons – Three or more lessons in same timeslot consolidated to one calendar card

**Description:** AC 06 — Decision Table + CRUD (Boundary) — Multiple lessons (3+) in one student's timeslot consolidate into a single card.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC
- Student: "Yamada Taro"
- Three lessons created for Yamada Taro on 2026-07-02 in timeslot 10:00-11:00:
  - Lesson A: Mathematics, Lesson B: Physics, Lesson C: English
- Calendar displays Riso TAC for 2026-07-02

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Riso TAC on 2026-07-02 (July 2nd) | TAC page loads | date = "2026-07-02" (JST), calendar_timezone = "Asia/Tokyo" |
| 2 | Locate timeslot 10:00-11:00 on calendar | Timeslot cell visible | timeslot = "10:00-11:00" |
| 3 | Verify only ONE consolidated lesson card displayed | Single card shown (not three separate cards) | lesson_cards_in_timeslot = 1 |
| 4 | Verify card shows count or indicator (e.g., "3 lessons") | Consolidation indicator shows correct count | consolidation_indicator = "3_lessons" |

**Severity:** major
**Priority:** high

---

### AC 06.3 – Duplicate Lessons – Sidebar displays alert for duplicated lessons

**Description:** AC 06 — Component (Display Completeness & High Risk) — Left sidebar displays an alert message when duplicate lessons exist for the selected student.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC
- Student: "Yamada Taro" has two lessons in same timeslot (2026-07-01, 09:00-10:00)
- Left sidebar visible
- Calendar showing duplicates

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Riso TAC with duplicate lessons present | TAC page loads | date = "2026-07-01" |
| 2 | Locate left sidebar below calendar | Sidebar visible with lesson/student information | sidebar_section = "details" |
| 3 | Verify alert message displayed for duplicates | Alert shown (e.g., "Warning: Duplicate lessons detected for Yamada Taro at 09:00") | alert_present = true |
| 4 | Verify alert styling (color, icon, text) | Alert styled correctly per design (warning color, icon visible) | alert_styling = "design_compliant" |
| 5 | Verify alert text matches spec (in JP or EN locale) | Alert text is accurate and localized | alert_text_correct = true |

**Severity:** major
**Priority:** medium

---

### AC 06.4 – Duplicate Lessons – Single lesson displays normally (no duplicate alert)

**Description:** AC 06 — Decision Table (Conditional) — When only one lesson exists in a timeslot, calendar and sidebar display normal (no duplicate alert or consolidation).

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC
- Student: "Yamada Taro"
- ONE lesson created: 2026-07-03, 11:00-12:00, Mathematics with Tanaka Yuki
- Calendar displays Riso TAC for 2026-07-03

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Riso TAC on 2026-07-03 (July 3rd) | TAC page loads | date = "2026-07-03" (JST) |
| 2 | Locate timeslot 11:00-12:00 | Timeslot cell visible | timeslot = "11:00-12:00" |
| 3 | Verify ONE lesson card displayed (normal format, no consolidation badge) | Single lesson card shown in normal format | lesson_cards_in_timeslot = 1, consolidation_indicator = "none" |
| 4 | Verify left sidebar shows lesson details (no duplicate alert) | Sidebar displays lesson info without alert message | alert_present = false |
| 5 | Verify lesson label format | Label shows "Mathematics (Tanaka Yuki)" normally | label_format = "normal" |

**Severity:** minor
**Priority:** medium

---

### AC 06.5 – Duplicate Lessons – Duplicate alert disappears when duplicate is removed

**Description:** AC 06 — Regression + State Transition — When a duplicate lesson is deleted, the duplicate alert in sidebar disappears and calendar returns to normal display.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC
- Student: "Yamada Taro" has two lessons in timeslot (2026-07-01, 09:00-10:00)
- Duplicate alert currently displayed in sidebar
- Calendar showing consolidated card

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Verify current state: duplicate alert visible, consolidated card shown | Starting state confirmed | duplicate_state = "present" |
| 2 | Delete one of the two lessons (e.g., Physics lesson) | Lesson deleted from system | deleted_lesson = "Physics" |
| 3 | Verify calendar refreshes | Calendar updated after deletion | calendar_refresh = "automatic" |
| 4 | Verify only ONE lesson card remains in timeslot | Single card displayed (no consolidation) | lesson_cards_in_timeslot = 1 |
| 5 | Verify duplicate alert disappears from sidebar | Alert message no longer shown | alert_present = false |
| 6 | Verify remaining lesson displays normally | Remaining lesson (Mathematics) shown in normal format | remaining_lesson_display = "normal" |

**Severity:** minor
**Priority:** medium

---

## Test Data Dictionary

- `date`: Date in YYYY-MM-DD format (2026-07-01, 2026-07-02, etc.)
- `calendar_timezone`: Timezone for date/time display (Asia/Tokyo = JST, UTC, etc.)
- `timeslot`: Time range of lesson (09:00-10:00, 10:00-11:00, etc.)
- `lesson_cards_in_timeslot`: Number of distinct lesson cards rendered in timeslot
- `consolidation_indicator`: Indicator showing duplicate count or flag (visible, "2_lessons", "3_lessons", none)
- `sidebar_section`: Sidebar area showing lesson details (details, info, right_panel)
- `alert_present`: Boolean; alert message visible
- `alert_styling`: Design compliance check (design_compliant, styling_correct, colors_match)
- `alert_text_correct`: Boolean; alert message text matches spec and localization
- `label_format`: Lesson label display format (normal, consolidated, null_subject, etc.)
- `duplicate_state`: State of duplicates (present, resolved, none)
- `deleted_lesson`: Name of lesson being deleted or modified
- `calendar_refresh`: Refresh behavior (automatic, manual, delayed)
- `remaining_lesson_display`: How remaining lesson displays (normal, unchanged, error)
