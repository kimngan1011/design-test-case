# Test Cases: PBT-3507 — [Nichibei] Additional Requirements for Lesson Booking System

## Suite: Booking Filter Navigation

### [Nichibei] Lesson Booking – Filter Page – Back Button – Navigates to Reservation List

**Description:** #23 — Scenario — In the Lesson Booking System on the learner app, tapping the "<" back button from the Filter page navigates to the Reservation List, not the Bookable Lesson List.

**Preconditions:**
- Logged in as a student to the Nichibei learner app
- Student has navigated to Lesson Booking > Filter page

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Nichibei learner app and navigate to Lesson Booking | Lesson Booking screen shown | — |
| 2 | Open the Filter page (tap Filter button) | Filter page shown | — |
| 3 | Tap the "<" back button without applying any filter | Navigation occurs | — |
| 4 | Observe the destination screen | Reservation List screen is shown (not the Bookable Lesson List) | expected_screen = "Reservation List" |

**Severity:** major
**Priority:** high

---

### [Nichibei] Lesson Booking – Filter Page – Back Button After Selecting Filter – Reservation List shown

**Description:** #23 — Edge — After selecting (but not applying) a filter value on the Filter page and tapping "<" back, the student lands on the Reservation List, not the Bookable Lesson List.

**Preconditions:**
- Logged in as a student to the Nichibei learner app
- Student is on Lesson Booking > Filter page with a filter value selected but not yet applied (e.g. a specific location chosen)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | On the Filter page, select a filter value (e.g. a specific location) | Filter value selected in the UI but not applied | filter_type = location; filter_value = "Location A" |
| 2 | Tap the "<" back button without tapping Apply | Navigation occurs | — |
| 3 | Observe the destination screen | Reservation List screen is shown (not the Bookable Lesson List) | expected_screen = "Reservation List" |

**Severity:** minor
**Priority:** medium

---
