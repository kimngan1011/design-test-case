# Test Cases: LT-96620 — [Nichibei] Lesson Booking System

## Suite: Booking List

### [Nichibei] Lesson Booking – Booking List – Student with booked lessons – All shown

**Description:** AC 01.1 — BR-1: Decision Table: Booking List shows only Booking_Flag=TRUE sessions with lesson_date >= today. Verify booked lessons are displayed.

**Preconditions:**
Student user has:

- Active Lesson Allocation (LA)
- 2 booked lessons with Booking_Flag=TRUE and lesson_date >= today
- 1 staff-allocated lesson with Booking_Flag=FALSE

| #   | Action                       | Expected Result                                                                                         | Test Data |
| --- | ---------------------------- | ------------------------------------------------------------------------------------------------------- | --------- |
| 1   | Login to app as student user | Home screen shown                                                                                       | —         |
| 2   | Open "Lesson Booking" menu   | Booking List screen shown                                                                               | —         |
| 3   | View lesson cards displayed  | Only 2 booked lessons (Booking_Flag=TRUE, date >= today) are shown; staff-allocated lesson is NOT shown | —         |

---

### [Nichibei] Lesson Booking – Booking List – No bookings – Empty state shown

**Description:** AC 01.1 — BR-1: Decision Table: Verify empty state is shown when student has no booked lessons.

**Preconditions:**
Student user has an active LA but no booked lessons (Booking_Flag=TRUE)

| #   | Action                       | Expected Result                                         | Test Data |
| --- | ---------------------------- | ------------------------------------------------------- | --------- |
| 1   | Login to app as student user | Home screen shown                                       | —         |
| 2   | Open "Lesson Booking" menu   | Booking List screen shown                               | —         |
| 3   | View lesson list area        | Empty state message is shown; no lesson cards displayed | —         |

---

### [Nichibei] Lesson Booking – Booking List – Past booked lesson – Not shown

**Description:** AC 01.1 — BR-1: Boundary Value Analysis: A booked lesson with lesson_date < today must NOT appear in the Booking List.

**Preconditions:**
Student user has:

- 1 booked lesson with lesson_date = yesterday (past)
- 1 booked lesson with lesson_date = today

| #   | Action                                                      | Expected Result                                                                 | Test Data                                                   |
| --- | ----------------------------------------------------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| 1   | Login to app as student user and open "Lesson Booking" menu | Booking List screen shown                                                       | —                                                           |
| 2   | View lesson cards displayed                                 | Only the lesson with lesson_date = today is shown; the past lesson is NOT shown | lesson_date(past) = yesterday; lesson_date(present) = today |

---

### [Nichibei] Lesson Booking – Browse Lessons Button – Student has active LA – Button visible

**Description:** AC 01.1 — BR-2: Decision Table: Browse Lessons (+) button must be visible when student has an active Lesson Allocation.

**Preconditions:**
Student user has 1 active Lesson Allocation

| #   | Action                             | Expected Result                | Test Data |
| --- | ---------------------------------- | ------------------------------ | --------- |
| 1   | Login to app as student user       | Home screen shown              | —         |
| 2   | Open "Lesson Booking" menu         | Booking List screen shown      | —         |
| 3   | View the Browse Lessons button (+) | Button is visible and tappable | —         |

---

### [Nichibei] Lesson Booking – Browse Lessons Button – Student has no active LA – Button hidden

**Description:** AC 01.1 — BR-2: Decision Table: Browse Lessons (+) button must NOT be visible when student has no active Lesson Allocation.

**Preconditions:**
Student user has no active Lesson Allocation (expired or never created)

| #   | Action                            | Expected Result                          | Test Data |
| --- | --------------------------------- | ---------------------------------------- | --------- |
| 1   | Login to app as student user      | Home screen shown                        | —         |
| 2   | Open "Lesson Booking" menu        | Booking List screen shown                | —         |
| 3   | View the Booking List header area | Browse Lessons (+) button is NOT visible | —         |

---

### [Nichibei] Lesson Booking – Booking List Cancel Button – Within cancellation deadline – Button enabled

**Description:** AC 01.1 — BR-3 / BR-22: BVA: Cancel button on a booking card must be enabled when current time is before the cancellation deadline.

**Preconditions:**
Student user has a booked lesson where current time < (lesson start − 2 hours).
Lesson start = 14:00 JST; cancellation deadline = 12:00 JST (2 hours before start); current = 09:00 JST.

| #   | Action                                                      | Expected Result                       | Test Data                                                                              |
| --- | ----------------------------------------------------------- | ------------------------------------- | -------------------------------------------------------------------------------------- |
| 1   | Login to app as student user and open "Lesson Booking" menu | Booking List screen shown             | —                                                                                      |
| 2   | View the Cancel button on the booked lesson card            | Cancel button is enabled and tappable | Lesson start = 14:00 JST; deadline = 12:00 JST (2 h before start); current = 09:00 JST |

---

### [Nichibei] Lesson Booking – Booking List Cancel Button – Past cancellation deadline – Button disabled with tooltip

**Description:** AC 01.1 — BR-3 / BR-22: BVA: Cancel button on a booking card must be disabled with tooltip when current time is past the cancellation deadline.

**Preconditions:**
Student user has a booked lesson where current time > (lesson start − 2 hours).
Lesson start = 11:00 JST; cancellation deadline = 09:00 JST (2 hours before start); current = 10:00 JST.

| #   | Action                                                      | Expected Result                                                          | Test Data                                                                              |
| --- | ----------------------------------------------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| 1   | Login to app as student user and open "Lesson Booking" menu | Booking List screen shown                                                | —                                                                                      |
| 2   | View the Cancel button on the booked lesson card            | Cancel button is disabled (greyed out)                                   | Lesson start = 11:00 JST; deadline = 09:00 JST (2 h before start); current = 10:00 JST |
| 3   | Tap or hover the disabled Cancel button                     | Tooltip shown: "Cancellation not available within 2 hours of start time" | —                                                                                      |
