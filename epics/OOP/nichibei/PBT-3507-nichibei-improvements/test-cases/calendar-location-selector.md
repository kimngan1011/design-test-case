# Test Cases: PBT-3507 — [Nichibei] Additional Requirements for Lesson Booking System

## Suite: Calendar Location Selector

### [Nichibei] Calendar – Location Selector – Smartphone Portrait Mode – Selector visible without screen rotation

**Description:** #20 — Smoke — On the BO lesson calendar viewed on a smartphone in portrait orientation, the location selector is visible and tappable without requiring the user to rotate the screen.

**Preconditions:**
- Logged in as HQ or CM Staff to the Back Office (Nichibei org)
- BO lesson calendar page is open on a smartphone (or browser viewport at smartphone width ≤ 430 px)
- At least two locations exist

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open BO lesson calendar on a smartphone in portrait mode | Calendar screen shown in portrait orientation | viewport_orientation = portrait; viewport_width ≤ 430 px |
| 2 | View the top area of the calendar | Location selector UI element is visible on screen without horizontal scrolling or rotation | — |
| 3 | Tap the location selector | Location picker opens | — |
| 4 | Select a different location from the list | Location selector closes and the calendar reloads for the selected location | — |

**Severity:** minor
**Priority:** medium

---

### [Nichibei] Calendar – Location Selector – Smartphone – Selecting location filters calendar lessons

**Description:** #20 — Scenario — After changing the location via the smartphone-accessible selector on the BO calendar, the calendar content updates to show lessons for the selected location only.

**Preconditions:**
- Logged in as HQ or CM Staff to the Back Office (Nichibei org)
- On smartphone viewport (portrait mode)
- Location A and Location B both have published lessons on 2026-07-16

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open BO lesson calendar on smartphone, currently showing Location A | Calendar displays lessons for Location A | location_A = "Location A"; lesson_A_date = 2026-07-16 |
| 2 | Open the location selector and choose Location B | Location B is selected | location_B = "Location B" |
| 3 | View the calendar | Calendar refreshes and shows lessons for Location B; lessons from Location A are not shown | — |

**Severity:** minor
**Priority:** medium

---
