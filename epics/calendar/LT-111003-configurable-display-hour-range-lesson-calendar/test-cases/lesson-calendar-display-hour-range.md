# Test Cases: LT-111003 - Configurable Display Hour Range on Lesson Calendar per Partner

## Suite: Calendar lesson > Configurable Display Hour Range on Lesson Calendar (LT-111003)

### [Core] Lesson Calendar display range - Default partner keeps 06:00-23:00 in Daily view

**Description:** AC 01 - Regression - Partners without a custom display-hour setting keep the existing 06:00-23:00 Daily view.

**Preconditions:**
- Login as HQ/CM staff with access to a non-Nichibei partner/location.
- Partner has no custom Lesson Calendar display range setting.
- Lessons exist on the same date at 05:30-06:00, 06:00-06:30, 23:00-23:30, and 23:30-23:59 in partner timezone.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Daily view for the target location/date. | Calendar loads successfully. | partner = default/no custom config |
| 2 | Inspect visible hour labels. | The first visible hour is 06:00 and the last visible hour is 23:00. | expected range = 06:00-23:00 inclusive |
| 3 | Search the calendar surface for the 05:30 lesson. | The 05:30 lesson is not displayed and no error is shown. | start = 05:30 |
| 4 | Inspect the 06:00 and 23:00 sections. | The 06:00 lesson appears in 06:00; the 23:00 and 23:30 lessons appear in the 23:00 section. | start = 06:00, 23:00, 23:30 |

**Severity:** critical
**Priority:** high

---

### [Core] Lesson Calendar display range - Default partner keeps 06:00-23:00 in Weekly view

**Description:** AC 01 - Regression - Weekly view uses the same default 06:00-23:00 range as Daily view.

**Preconditions:**
- Same partner has no custom Lesson Calendar display range setting.
- Weekly calendar contains lessons at 05:59, 06:00, 22:59, and 23:30 across different days.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Weekly view for the target week. | Weekly view loads. | week includes target lessons |
| 2 | Inspect visible time labels/slots. | 06:00 through 23:00 are visible; 00:00-05:00 are not visible. | expected range = 06:00-23:00 |
| 3 | Inspect lessons in boundary sections. | 06:00, 22:59, and 23:30 lessons are visible in their correct day/time sections. | starts = 06:00, 22:59, 23:30 |
| 4 | Search for the 05:59 lesson card. | 05:59 lesson is hidden because its start hour is outside the default range. | start = 05:59 |

**Severity:** critical
**Priority:** high

---

### [Core][Nichibei] Lesson Calendar display range - Full-day Daily view shows 00:00-23:00

**Description:** AC 02 - Scenario - Nichibei 00:00-23:00 setting exposes midnight and early-morning lessons in Daily view.

**Preconditions:**
- Login as HQ/CM staff with access to Nichibei location.
- Nichibei Lesson Calendar display range is configured to startHour = 0, endHour = 23.
- Lessons exist at 00:00-00:30, 00:30-01:00, 05:59-06:29, and 23:30-23:59 in partner timezone.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Daily view for the Nichibei location/date. | Calendar loads successfully. | partner = Nichibei |
| 2 | Inspect visible hour labels. | Calendar starts at 00:00 and ends at 23:00. | config = 00:00-23:00 |
| 3 | Inspect 00:00 and 05:00 sections. | 00:00, 00:30, and 05:59 lessons are visible in the correct hour sections. | starts = 00:00, 00:30, 05:59 |
| 4 | Inspect 23:00 section. | 23:30 lesson is visible in the 23:00 section. | start = 23:30 |

**Severity:** critical
**Priority:** high

---

### [Core][Nichibei] Lesson Calendar display range - Full-day Weekly view shows early-morning lessons

**Description:** AC 02 - Scenario - Weekly view honors Nichibei 00:00-23:00 setting for lessons on every day of the week.

**Preconditions:**
- Nichibei display range is configured to 00:00-23:00.
- Weekly data includes early-morning lessons at 00:15, 03:00, and 05:45 on different days.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Weekly view for the target week. | Weekly view loads with seven day columns. | partner = Nichibei |
| 2 | Inspect visible hour labels. | 00:00, 01:00, 02:00, 03:00, 04:00, 05:00, and 23:00 sections are visible. | config = 00:00-23:00 |
| 3 | Inspect each early-morning lesson's day column. | Each lesson appears on its correct day and hour section. | starts = 00:15, 03:00, 05:45 |
| 4 | Change to another week and return. | The same configured display range is preserved after navigation. | navigation = next week then previous week |

**Severity:** critical
**Priority:** high

---

### [Core] Lesson Calendar display range - Partner setting change updates visibility without changing lesson data

**Description:** AC 03 - State Transition - Existing early-morning lessons appear after range expansion and retain their saved datetime.

**Preconditions:**
- Partner initially uses default 06:00-23:00 display range.
- Lesson `Overseas Morning Lesson A` exists at 02:30-03:00 in partner timezone.
- Admin user can update partner-level Lesson Calendar display range.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Daily view before changing the setting. | `Overseas Morning Lesson A` is hidden. | initial range = 06:00-23:00 |
| 2 | Update partner display range to 00:00-23:00 and refresh/open the same Daily view. | `Overseas Morning Lesson A` appears in the 02:00 section. | new range = 00:00-23:00 |
| 3 | Open the lesson detail/edit form. | Start Date Time remains 02:30 and End Date Time remains 03:00. | expected data unchanged |
| 4 | Change range back to 06:00-23:00 and refresh/open the same view. | The lesson is hidden again, with no data update or warning. | restored range = 06:00-23:00 |

**Severity:** critical
**Priority:** high

---

### [Core] Lesson Calendar display range - Partner isolation between Nichibei and default partner

**Description:** AC 04 - Regression - A full-day setting for Nichibei must not alter other partners' default range.

**Preconditions:**
- Nichibei is configured to 00:00-23:00.
- Renseikai or another default partner has no custom display range setting.
- Each partner has a lesson at 01:00 and another lesson at 10:00.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Nichibei Daily view. | 00:00-23:00 labels are visible; both 01:00 and 10:00 lessons appear. | partner = Nichibei |
| 2 | Switch location/partner to default partner. | Calendar reloads for the selected partner. | partner = default |
| 3 | Inspect visible labels and cards. | 06:00-23:00 labels are visible; 10:00 lesson appears and 01:00 lesson is hidden. | expected isolation = true |
| 4 | Return to Nichibei. | Nichibei still shows 00:00-23:00 without requiring reconfiguration. | config preserved |

**Severity:** critical
**Priority:** high

---

### [Core] Lesson Calendar display range - 23:00 boundary remains visible by default

**Description:** AC 01 - BVA - A lesson starting from 23:00 to 23:59 must be visible in the default range.

**Preconditions:**
- Partner has no custom display range.
- Lessons exist at 22:59-23:29, 23:00-23:30, and 23:59-24:00.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Daily view for the date. | Calendar shows default range. | range = 06:00-23:00 |
| 2 | Inspect the 22:00 and 23:00 sections. | 22:59 is shown in 22:00; 23:00 and 23:59 are shown in 23:00. | starts = 22:59, 23:00, 23:59 |
| 3 | Open Weekly view for the same date. | The same three lessons are visible in the correct weekly slots. | view = weekly |

**Severity:** critical
**Priority:** high

---

### [Core] Lesson Calendar display range - Timezone uses partner timezone, not browser timezone

**Description:** AC 05 - Timezone - Early-morning lesson placement is based on partner timezone.

**Preconditions:**
- Nichibei display range is 00:00-23:00.
- Browser/device timezone is different from partner timezone.
- Lesson exists at 00:30 partner timezone.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Set browser/device timezone to a different timezone from partner timezone. | Session remains logged in and calendar can be opened. | browser timezone != partner timezone |
| 2 | Open Nichibei Daily view for the lesson date. | Calendar renders using partner timezone. | partner timezone = org/location timezone |
| 3 | Inspect the lesson card placement and detail. | Lesson appears in 00:00 section and detail shows 00:30 start time. | start = 00:30 partner timezone |

**Severity:** major
**Priority:** high

---

### [Core] Lesson Calendar display range - Scroll lands near useful content in full-day range

**Description:** Risk Coverage - Full-day view should not leave users stranded at empty early-morning sections when lessons are later in the day.

**Preconditions:**
- Nichibei display range is 00:00-23:00.
- Target day has no lessons from 00:00-08:59 and has the first lesson at 09:30.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Daily view for the target date. | Calendar loads without layout jump. | first lesson = 09:30 |
| 2 | Observe initial scroll/focus position after loading. | User can immediately find the current time or first lesson without manually scrolling through only empty 00:00-08:00 slots. | expected = scroll to first lesson/current time behavior |
| 3 | Click/open a lesson detail from a deep link or drawer state. | Calendar scrolls to the selected lesson if it is visible in the configured range. | selected lesson = 09:30 |

**Severity:** major
**Priority:** medium

---

### [Core] Lesson Calendar display range - Other-location lessons respect configured range and permissions

**Description:** Regression - Teacher daily cross-location view combines permission, location, and display range correctly.

**Preconditions:**
- Teacher has lessons at current location and another permitted location.
- Partner display range is 00:00-23:00.
- Other-location lessons exist at 01:00 and 10:00.
- User has permission for the other location.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Teacher Daily view for the current location. | Teacher row displays lessons according to selected filters. | view = teacher daily |
| 2 | Inspect other-location lessons. | Both 01:00 and 10:00 other-location lessons appear with basic/other-location styling. | config = 00:00-23:00 |
| 3 | Change partner display range to 06:00-23:00 and reload. | 01:00 other-location lesson is hidden; 10:00 remains visible. | config = 06:00-23:00 |
| 4 | Remove permission for the other location and reload. | Other-location lessons are hidden regardless of display range. | permission = no access |

**Severity:** major
**Priority:** high

---

### [Core] Lesson Calendar display range - DnD grid supports early-morning slots in full-day range

**Description:** Regression - Drag-and-drop 10-minute grid is generated for early-morning visible hours.

**Preconditions:**
- Nichibei display range is 00:00-23:00.
- DnD custom setting is ON.
- A draggable lesson exists at 06:00.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Weekly view and enter drag mode for the 06:00 lesson. | Calendar shows 10-minute drop slots for visible hours. | source start = 06:00 |
| 2 | Drag the lesson to 00:20 on the same day. | Drop target is available and snaps to 00:20. | target = 00:20 |
| 3 | Confirm/open Edit Lesson modal. | Modal shows updated Start Time = 00:20 and same lesson duration. | expected start = 00:20 |
| 4 | Cancel the modal. | Original lesson time remains unchanged. | action = cancel |

**Severity:** major
**Priority:** high

---

### [Core] Lesson Calendar display range - DnD rejects drop outside configured visible range

**Description:** Negative - Drop zones outside the configured display range must not update lesson time.

**Preconditions:**
- Default partner display range is 06:00-23:00.
- DnD custom setting is ON.
- A draggable lesson exists at 10:00.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Weekly view and enter drag mode for the 10:00 lesson. | 06:00-23:00 grid is visible. | source start = 10:00 |
| 2 | Attempt to drop the lesson into a non-visible/outside-calendar 05:30 area. | Drop is rejected or no valid target is available. | target = 05:30 |
| 3 | Reopen/inspect the lesson. | Lesson Start Time is still 10:00 and no save API is triggered for 05:30. | expected unchanged |

**Severity:** major
**Priority:** high

---

### [Core] Lesson Calendar display range - Create lesson from calendar uses visible full-day time

**Description:** Risk Coverage - Create Lesson modal opened from calendar preserves selected early-morning time under full-day config.

**Preconditions:**
- Nichibei display range is 00:00-23:00.
- User has permission to create lessons from SF Calendar.
- Calendar is in create lesson mode.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Daily or Weekly view for Nichibei. | 00:00-23:00 sections are visible. | partner = Nichibei |
| 2 | Select/create a lesson from the 02:10 time slot. | Create Lesson form/modal opens. | selected slot = 02:10 |
| 3 | Inspect Date, Start Time, End Time, Location, and Teacher/Classroom if selected. | Start Time is 02:10, Date is the selected calendar date, and context fields are prefilled correctly. | expected start = 02:10 |
| 4 | Save with required fields completed. | Lesson is created and appears in the 02:00 section after refresh. | expected card section = 02:00 |

**Severity:** critical
**Priority:** high

---

### [Core] Lesson Calendar display range - Calendar filters combine with configured range

**Description:** Regression - Teacher/status/type filters must narrow results without overriding the display-hour filter.

**Preconditions:**
- Nichibei display range is 00:00-23:00.
- Lessons exist for Teacher A at 01:00 and 10:00.
- Lessons exist for Teacher B at 01:00.
- Activity event exists at 01:00 if event filter is enabled for the tenant.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Calendar Weekly view with all teachers/types visible. | Early-morning lessons/events appear because they are inside the configured range. | range = 00:00-23:00 |
| 2 | Filter by Teacher A. | Teacher A's 01:00 and 10:00 lessons remain; Teacher B's lesson is hidden. | teacher = A |
| 3 | Filter by Lesson only. | Lesson cards remain; event card is hidden. | type = Lesson |
| 4 | Change range to 06:00-23:00 and reload with the same filters. | Teacher A's 10:00 lesson remains; Teacher A's 01:00 lesson is hidden. | range = 06:00-23:00 |

**Severity:** major
**Priority:** high

---

### [Core] Lesson Calendar display range - Invalid or missing config is handled safely

**Description:** Negative - Missing/invalid partner configuration must not break Calendar loading.

**Preconditions:**
- Admin or backend test fixture can create/update partner display range configuration.
- Calendar has normal lessons at 10:00 and 23:30.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Remove the partner display range config and open Calendar Daily view. | Calendar falls back to 06:00-23:00 and loads normally. | config = missing |
| 2 | Try to save startHour outside 0-23. | Save is blocked with validation error or invalid value is not accepted by API. | startHour = -1 or 24 |
| 3 | Try to save endHour outside 0-23. | Save is blocked with validation error or invalid value is not accepted by API. | endHour = -1 or 24 |
| 4 | Try to save startHour greater than endHour. | Save is blocked or Calendar safely falls back to default without blank/negative layout. | startHour = 23, endHour = 6 |

**Severity:** critical
**Priority:** high

---

### [Core] Lesson Calendar display range - Multi-day event remains visible regardless of start hour

**Description:** Regression - Multi-day events bypass single-day range filtering and should remain visible as spanning bars.

**Preconditions:**
- Tenant has multi-day activity events enabled.
- Partner display range is 06:00-23:00.
- Multi-day activity event exists from 00:30 Day 1 to 10:00 Day 2.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Weekly view for the event week. | Weekly view loads with default range. | range = 06:00-23:00 |
| 2 | Inspect multi-day event band area. | Multi-day event appears as a spanning bar even though its start hour is 00:30. | event start = 00:30 |
| 3 | Turn Event type filter off. | Multi-day event is hidden by type filter. | type filter = Lesson only |
| 4 | Turn Event type filter on again. | Multi-day event returns. | type filter = Lesson + Event |

**Severity:** major
**Priority:** medium

