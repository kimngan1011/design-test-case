# Test Cases: LT-107411 — Riso | Core | TAC improvement (July)

## Suite: AC-04 — Location Filter Accordion

### AC 04.1 – Location Filter – Included in collapsible filter accordion

**Description:** AC 04 — CRUD — Location filter control is present and functional within the collapsible filter accordion.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC (Teacher Availability Calendar)
- Filter accordion visible on page
- Location list exists: ["Room A", "Room B", "Room C"]

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Riso TAC | TAC page loads with filter accordion visible | page = "Riso TAC" |
| 2 | Expand filter accordion (if collapsed) | Accordion expands showing filter controls | accordion_state = "expanded" |
| 3 | Verify Location filter control is present | Location filter input or dropdown visible in accordion | filter_type = "location" |
| 4 | Click on Location filter dropdown | Dropdown opens showing available locations | locations = ["Room A", "Room B", "Room C"] |
| 5 | Select "Room A" | Location filter applied to calendar | selected_location = "Room A" |
| 6 | Observe calendar | Calendar now shows only lessons in Room A | expected_display = "filtered_by_room_a" |

**Severity:** minor
**Priority:** low

---

### AC 04.2 – Location Filter – Selection persists after accordion collapse and expand

**Description:** AC 04 — Regression + State Transition — Location filter selection retains its value when filter accordion is collapsed and re-expanded.

**Preconditions:**
- User role: HQ/CM Staff
- Location: Riso TAC
- Location list exists: ["Room A", "Room B", "Room C"]
- Filter accordion expanded; Location filter available

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Select Location filter to "Room B" | Location filter applied; "Room B" shown as active | selected_location = "Room B" |
| 2 | Verify calendar displays only Room B lessons | Calendar filtered correctly | display_state = "filtered_by_room_b" |
| 3 | Collapse filter accordion (click collapse button/icon) | Accordion collapses; Location filter remains applied to calendar | accordion_state = "collapsed" |
| 4 | Expand filter accordion again (click expand button/icon) | Accordion expands; Location filter shows "Room B" still selected | accordion_state = "expanded" |
| 5 | Verify calendar display unchanged | Calendar still shows only Room B lessons; no filter reset | expected_display = "still_filtered_by_room_b" |

**Severity:** minor
**Priority:** medium

---

## Test Data Dictionary

- `page`: Current page or feature (Riso TAC, Lesson Schedule, etc.)
- `accordion_state`: State of filter accordion (expanded, collapsed)
- `filter_type`: Type of filter control (location, subject, teacher, date, etc.)
- `locations`: Array of available location options
- `selected_location`: Location chosen by user
- `expected_display`: Expected calendar display after filter applied (filtered_by_room_a, etc.)
- `display_state`: Current state of calendar display after filter action
