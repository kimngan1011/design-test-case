# Test Cases: LT-96620 — [Nichibei] Lesson Booking System

## Suite: My Lessons

### [Nichibei] Lesson Booking – My Lessons Card – Fields – Card displays all required fields

**Description:** AC 01.1 — Display Testing: Each booked lesson card in My Lessons must display the core information fields: lesson name, date, start time, center (location), and teacher name, so the student can identify their booking at a glance.

**Preconditions:**
Student has 1 booked lesson (Booking_Flag=TRUE, lesson_date >= today) with known data:
lesson name = "Math Lesson", lesson_date = 2026-05-25, start = 10:00 JST, end = 11:00 JST, center = "Center A", teacher = "Teacher A".

| #   | Action                                    | Expected Result                          | Test Data                                                                                    |
| --- | ----------------------------------------- | ---------------------------------------- | -------------------------------------------------------------------------------------------- |
| 1   | Open "Reservation List" menu                | My Lessons screen shown with lesson card | lesson_date = 2026-05-25; start = 10:00; end = 11:00; center = Center A; teacher = Teacher A |
| 2   | Observe lesson name on the card           | "Math Lesson" is displayed               | —                                                                                            |
| 3   | Observe date on the card                  | Date "2026-05-25" is displayed           | —                                                                                            |
| 4   | Observe start time on the card            | "10:00" (JST) is displayed               | —                                                                                            |
| 5   | Observe center/location field on the card | "Center A" is displayed                  | —                                                                                            |
| 6   | Observe teacher name on the card          | "Teacher A" is displayed                 | —                                                                                            |

---

### [Nichibei] Lesson Booking – My Lessons – Student with booked lessons – All shown

**Description:** AC 01.1 — BR-1: Decision Table: My Lessons shows only Booking_Flag=TRUE sessions with lesson_date >= today. Verify booked lessons are displayed.

**Preconditions:**
Student user has:

- Active Lesson Allocation (LA)
- 2 booked lessons with Booking_Flag=TRUE and lesson_date >= 2026-05-19 (today): lesson A = 2026-05-19, lesson B = 2026-05-26
- 1 staff-allocated lesson with Booking_Flag=FALSE

| #   | Action                       | Expected Result                                                                                        | Test Data                                    |
| --- | ---------------------------- | ------------------------------------------------------------------------------------------------------ | -------------------------------------------- |
| 1   | Login to app as student user | Home screen shown                                                                                      | today = 2026-05-19                           |
| 2   | Open "Reservation List" menu   | My Lessons screen shown                                                                                | —                                            |
| 3   | View lesson cards displayed  | Only 2 booked lessons (dates 2026-05-19 and 2026-05-26) are shown; staff-allocated lesson is NOT shown | lesson A = 2026-05-19; lesson B = 2026-05-26 |

---

### [Nichibei] Lesson Booking – My Lessons – No bookings – Empty state shown

**Description:** AC 01.1 — BR-1: Decision Table: When student has an active LA but no upcoming booked lessons, the My Lessons screen must show the exact empty state message "You have no upcoming bookings".

**Preconditions:**
Student user has an active LA but no booked lessons (Booking_Flag=TRUE)

| #   | Action                       | Expected Result                                                               | Test Data |
| --- | ---------------------------- | ----------------------------------------------------------------------------- | --------- |
| 1   | Login to app as student user | Home screen shown                                                             | —         |
| 2   | Open "Reservation List" menu   | My Lessons screen shown                                                       | —         |
| 3   | View lesson list area        | Empty state message "You have no upcoming bookings" is shown; no lesson cards | —         |

---

### [Nichibei] Lesson Booking – My Lessons – Past booked lesson – Not shown

**Description:** AC 01.1 — BR-1: Boundary Value Analysis: A booked lesson with lesson_date < today must NOT appear in My Lessons.

**Preconditions:**
Student user has:

- 1 booked lesson with lesson_date = 2026-05-18 (yesterday, past)
- 1 booked lesson with lesson_date = 2026-05-19 (today)

| #   | Action                                                      | Expected Result                                                                      | Test Data                                                         |
| --- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------ | ----------------------------------------------------------------- |
| 1   | Login to app as student user and open "Reservation List" menu | My Lessons screen shown                                                              | today = 2026-05-19                                                |
| 2   | View lesson cards displayed                                 | Only the lesson with lesson_date = 2026-05-19 is shown; the past lesson is NOT shown | lesson_date(past) = 2026-05-18; lesson_date(present) = 2026-05-19 |

---

### [Nichibei] Lesson Booking – Lesson Lists Button – Student has active LA – Button visible

**Description:** AC 01.1 — BR-2: Decision Table: Lesson Lists (+) button must be visible when student has an active Lesson Allocation.

**Preconditions:**
Student user has 1 active Lesson Allocation

| #   | Action                             | Expected Result                | Test Data |
| --- | ---------------------------------- | ------------------------------ | --------- |
| 1   | Login to app as student user       | Home screen shown              | —         |
| 2   | Open "Reservation List" menu         | My Lessons screen shown        | —         |
| 3   | View the Lesson Lists button (+) | Button is visible and tappable | —         |

---

### [Nichibei] Lesson Booking – Lesson Lists Button – Student has no active LA – Button hidden

**Description:** AC 01.1 — BR-2: Decision Table: Lesson Lists (+) button must NOT be visible when student has no active Lesson Allocation.

**Preconditions:**
Student user has no active Lesson Allocation (expired or never created)

| #   | Action                          | Expected Result                          | Test Data |
| --- | ------------------------------- | ---------------------------------------- | --------- |
| 1   | Login to app as student user    | Home screen shown                        | —         |
| 2   | Open "Reservation List" menu      | My Lessons screen shown                  | —         |
| 3   | View the My Lessons header area | Lesson Lists (+) button is NOT visible | —         |

---

### [Nichibei] Lesson Booking – My Lessons Cancel Button – Within cancellation deadline – Button enabled

**Description:** AC 01.1 — BR-3 / BR-22: BVA: Cancel button on a booking card must be enabled when current time is before the cancellation deadline.

**Preconditions:**
Student user has a booked lesson where current time < (lesson start − 2 hours).
Lesson start = 14:00 JST; cancellation deadline = 12:00 JST (2 hours before start); current = 09:00 JST.

| #   | Action                                                      | Expected Result                       | Test Data                                                                              |
| --- | ----------------------------------------------------------- | ------------------------------------- | -------------------------------------------------------------------------------------- |
| 1   | Login to app as student user and open "Reservation List" menu | My Lessons screen shown               | —                                                                                      |
| 2   | View the Cancel button on the booked lesson card            | Cancel button is enabled and tappable | Lesson start = 14:00 JST; deadline = 12:00 JST (2 h before start); current = 09:00 JST |

---

### [Nichibei] Lesson Booking – My Lessons Cancel Button – Past cancellation deadline – Button disabled with tooltip

**Description:** AC 01.1 — BR-3 / BR-22: BVA: Cancel button on a booking card must be disabled with tooltip when current time is past the cancellation deadline.

**Preconditions:**
Student user has a booked lesson where current time > (lesson start − 2 hours).
Lesson start = 11:00 JST; cancellation deadline = 09:00 JST (2 hours before start); current = 10:00 JST.

| #   | Action                                                      | Expected Result                                                          | Test Data                                                                              |
| --- | ----------------------------------------------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| 1   | Login to app as student user and open "Reservation List" menu | My Lessons screen shown                                                  | —                                                                                      |
| 2   | View the Cancel button on the booked lesson card            | Cancel button is disabled (greyed out)                                   | Lesson start = 11:00 JST; deadline = 09:00 JST (2 h before start); current = 10:00 JST |
| 3   | Tap or hover the disabled Cancel button                     | Tooltip shown: "Cancellation not available within 2 hours of start time" | —                                                                                      |

---

### [Nichibei] Lesson Booking – My Lessons – Sort Order – Start time ASC, group lessons before individual at same time

**Description:** AC 01.1 — Sorting: Booked lesson cards on the My Lessons screen are sorted by start time ascending. When two lessons share the same start time, group lessons appear before individual lessons. Lesson ID ASC is the final tiebreaker within the same time and type.

**Preconditions:**
Student has 3 booked lessons (all Booking_Flag=TRUE, lesson_date >= today):

- Lesson A: group lesson, start = 09:00 JST
- Lesson B: individual lesson, start = 09:00 JST (same time as A)
- Lesson C: any type, start = 10:00 JST

| #   | Action                                                                                 | Expected Result                                                                      | Test Data                                  |
| --- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------ |
| 1   | Open "Reservation List" menu                                                             | All 3 booked lesson cards visible in My Lessons list                                 | A=09:00 group; B=09:00 individual; C=10:00 |
| 2   | Observe position of Lesson C (10:00) vs Lessons A and B (09:00)                        | Lessons A and B (09:00) appear before Lesson C (10:00) — earlier start time first    | —                                          |
| 3   | Observe position of Lesson A (group) vs Lesson B (individual) at same 09:00 start time | Lesson A (group) appears before Lesson B (individual) — group before individual rule | —                                          |

---

### [Nichibei] Lesson Booking – My Lessons – No active LA – "No courses available for booking" shown

**Description:** AC 01.1 — Decision Table: When student has no active Lesson Allocation, the My Lessons screen must show the exact empty state message "No courses available for booking" and the Lesson Lists button must be inactive.

**Preconditions:**
Student user has no active Lesson Allocation (expired or never created).

| #   | Action                             | Expected Result                                              | Test Data |
| --- | ---------------------------------- | ------------------------------------------------------------ | --------- |
| 1   | Login to app as student user       | Home screen shown                                            | —         |
| 2   | Open "Reservation List" menu         | My Lessons screen shown                                      | —         |
| 3   | View the empty state message       | "No courses available for booking" is displayed              | —         |
| 4   | View the Lesson Lists (+) button | Lesson Lists button is inactive (disabled or not tappable) | —         |
