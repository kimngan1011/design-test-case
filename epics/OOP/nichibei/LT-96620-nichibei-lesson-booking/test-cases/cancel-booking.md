# Test Cases: LT-96620 — [Nichibei] Lesson Booking System

## Suite: Cancel Booking

### [Nichibei] Lesson Booking – Cancel Entry Point – My Lessons – Cancel button visible for booked lesson

**Description:** AC 04.1 — BR-3: Decision Table: Cancel button must appear on a booked lesson card in My Lessons.

**Preconditions:**
Student user has a booked lesson (Booking_Flag=TRUE) in their My Lessons, within the cancellation deadline.

| #   | Action                                                      | Expected Result                        | Test Data |
| --- | ----------------------------------------------------------- | -------------------------------------- | --------- |
| 1   | Login to app as student user and open "Reservation List" menu | My Lessons screen shown                | —         |
| 2   | View the booked lesson card                                 | "Cancel" button is visible on the card | —         |

---

### [Nichibei] Lesson Booking – Cancel Entry Point – Lesson Lists – Cancel button visible for booked lesson

**Description:** AC 04.1 — BR-3: Decision Table: Cancel button must appear for a booked lesson (Booking_Flag=TRUE) when viewed in the Lesson List screen.

**Preconditions:**
Student user has a booked lesson (Booking_Flag=TRUE), within the cancellation deadline. Student navigates to the Lesson List view.

| #   | Action                                            | Expected Result                                | Test Data |
| --- | ------------------------------------------------- | ---------------------------------------------- | --------- |
| 1   | Login to app as student user and open Lesson Lists | Lesson Lists screen shown                       | —         |
| 2   | Find the booked lesson                            | "Cancel" button is visible on the lesson entry | —         |

---

### [Nichibei] Lesson Booking – Cancel Entry Point – Lesson Lists – No Cancel button for staff-allocated lesson

**Description:** AC 04.1 — BR-11: Decision Table: Cancel button must NOT appear for staff-allocated lessons (Booking_Flag=OFF) in the Lesson List.

**Preconditions:**
Student user has a staff-allocated lesson (Booking_Flag=FALSE) in the Lesson List.

| #   | Action                                            | Expected Result                                        | Test Data |
| --- | ------------------------------------------------- | ------------------------------------------------------ | --------- |
| 1   | Login to app as student user and open Lesson Lists | Lesson Lists screen shown                               | —         |
| 2   | View the staff-allocated lesson card              | No "Cancel" button shown on the staff-allocated lesson | —         |

---

### [Nichibei] Lesson Booking – Cancel Deadline – Within deadline – Cancel button enabled

**Description:** AC 04.2 — BR-22: BVA: Cancel button must be enabled when current time is at or before the cancellation deadline (current ≤ lesson start − X hours), where X is the partner-configured cancellation deadline setting.

**Preconditions:**
Partner config: cancellation deadline X = 2 hours.
Lesson date = 2026-05-22; Lesson start = 2026-05-22 14:00 JST; deadline = 2026-05-22 12:00 JST (14:00 − 2h).
Current datetime = 2026-05-22 09:00 JST → 2026-05-22 09:00 ≤ 2026-05-22 12:00 → within deadline.

| #   | Action                 | Expected Result                       | Test Data                                                                                  |
| --- | ---------------------- | ------------------------------------- | ------------------------------------------------------------------------------------------ |
| 1   | Open My Lessons list   | Booked lesson card visible            | —                                                                                          |
| 2   | View the Cancel button | Cancel button is enabled and tappable | X = 2 h; deadline = 2026-05-22 12:00 JST; current = 2026-05-22 09:00 JST → within deadline |

---

### [Nichibei] Lesson Booking – Cancel Deadline – Past deadline – Cancel button disabled with tooltip

**Description:** AC 04.2 — BR-22: BVA: Cancel button must be disabled with tooltip when current time is past the cancellation deadline (current > lesson start − X hours), where X is the partner-configured cancellation deadline setting.

**Preconditions:**
Partner config: cancellation deadline X = 2 hours.
Lesson date = 2026-05-22; Lesson start = 2026-05-22 11:00 JST; deadline = 2026-05-22 09:00 JST (11:00 − 2h).
Current datetime = 2026-05-22 10:00 JST → 2026-05-22 10:00 > 2026-05-22 09:00 → past deadline.

| #   | Action                                  | Expected Result                                                          | Test Data                                                                                |
| --- | --------------------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| 1   | Open My Lessons list                    | Booked lesson card visible                                               | —                                                                                        |
| 2   | View the Cancel button                  | Cancel button is disabled (greyed out)                                   | X = 2 h; deadline = 2026-05-22 09:00 JST; current = 2026-05-22 10:00 JST → past deadline |
| 3   | Tap or hover the disabled Cancel button | Tooltip shown: "Cancellation not available within 2 hours of start time" | X = 2; tooltip text reflects configured X value                                          |

---

### [Nichibei] Lesson Booking – Cancel Dialog – Correct content displayed

**Description:** AC 04.3 — Equivalence Partitioning: Cancel confirmation dialog must show the correct title, message, and buttons.

**Preconditions:**
Student has a booked lesson within cancellation deadline.

| #   | Action                                                            | Expected Result                                                                  | Test Data |
| --- | ----------------------------------------------------------------- | -------------------------------------------------------------------------------- | --------- |
| 1   | Open My Lessons list and tap the Cancel button on a booked lesson | Cancellation confirmation dialog opens                                           | —         |
| 2   | View dialog title                                                 | Title reads: "Cancel Booking?"                                                   | —         |
| 3   | View dialog message                                               | Message reads: "Are you sure you want to cancel this reservation?"               | —         |
| 4   | View dialog buttons                                               | Two buttons: "×" (secondary / close) and "Cancel Reservation" (destructive, red) | —         |

---

### [Nichibei] Lesson Booking – Cancel Booking – Student Session deleted after cancellation

**Description:** AC 04.4 — BR-23: CRUD Testing: Confirming cancellation must delete the Student Session record from Salesforce.

**Preconditions:**
Student has a booked lesson within cancellation deadline.

| #   | Action                                              | Expected Result                                         | Test Data |
| --- | --------------------------------------------------- | ------------------------------------------------------- | --------- |
| 1   | Open My Lessons list, tap Cancel on a booked lesson | Cancellation dialog shown                               | —         |
| 2   | Tap "Cancel Reservation"                            | Cancellation processed                                  | —         |
| 3   | Verify in Salesforce                                | Student Session record for (student, lesson) is deleted | —         |
| 4   | Return to My Lessons list                           | Cancelled lesson is no longer shown in My Lessons list  | —         |

---

### [Nichibei] Lesson Booking – Cancel Booking – Points refunded to Point LA on cancellation

**Description:** AC 04.4 — BR-23/BR-31: CRUD Testing: When a student cancels a self-booked lesson, the points consumed at booking time must be refunded back to the Point LA (Remaining Points restored, Consumed Points decremented). This mirrors the point-refund behavior on manual staff removal.

**Preconditions:**
Student has booked Lesson 1. At booking time, 2 pts were deducted from Point LA-B (Remaining went from 5 → 3 pts).
Lesson is within the cancellation deadline.

| #   | Action                                                                   | Expected Result                                               | Test Data                                           |
| --- | ------------------------------------------------------------------------ | ------------------------------------------------------------- | --------------------------------------------------- |
| 1   | Record LA-B Remaining Points in Salesforce before cancellation           | Remaining Points = 3 pts (post-booking balance)               | LA-B Remaining = 3 pts; original Point Cost = 2 pts |
| 2   | Open My Lessons list → tap Cancel on Lesson 1 → tap "Cancel Reservation" | Cancellation confirmed; Lesson 1 removed from My Lessons list | —                                                   |
| 3   | Verify LA-B Remaining Points in Salesforce after cancellation            | Remaining Points = 5 pts (3 + 2 refunded)                     | —                                                   |
| 4   | Verify LA-B Consumed Points in Salesforce after cancellation             | Consumed Points decremented by 2 pts from pre-cancel value    | —                                                   |

---

### [Nichibei] Lesson Booking – Cancel Booking – Return to My Lessons list after cancellation

**Description:** AC 04.4 — BR-23: State Transition: After confirming cancellation, app navigates back to My Lessons list and the lesson is removed.

**Preconditions:**
Student has a booked lesson within cancellation deadline. My Lessons list has only that 1 lesson.

| #   | Action                                                   | Expected Result                                                  | Test Data |
| --- | -------------------------------------------------------- | ---------------------------------------------------------------- | --------- |
| 1   | Open My Lessons list and tap Cancel on the booked lesson | Cancellation dialog shown                                        | —         |
| 2   | Tap "Cancel Reservation"                                 | App returns to updated My Lessons list                           | —         |
| 3   | View My Lessons list                                     | The cancelled lesson is no longer in the list; empty state shown | —         |

---

### [Nichibei] Lesson Booking – Cancel Booking – Auto-published lesson stays Published after cancellation

**Description:** AC 04.4 — BR-32: State Transition: When a Draft lesson was auto-published via booking (AC 03.2) and the student subsequently cancels, the lesson must remain in Published status — NOT revert to Draft.

**Preconditions:**
A Draft lesson (Bookable_Flag=TRUE) exists. Student books it → lesson auto-published to Published. Student then cancels the booking.

| #   | Action                                                       | Expected Result                                           | Test Data |
| --- | ------------------------------------------------------------ | --------------------------------------------------------- | --------- |
| 1   | Confirm lesson status = Draft before booking                 | Lesson status = Draft in Salesforce                       | —         |
| 2   | Student books the Draft lesson; confirm it is auto-published | Lesson status = Published after booking                   | —         |
| 3   | Student cancels the booking                                  | Cancellation confirmed; Student Session deleted           | —         |
| 4   | Verify lesson status in Salesforce after cancellation        | Lesson status remains = Published (not reverted to Draft) | —         |

---

### [Nichibei] Lesson Booking – Cancel Booking – Dismiss dialog – Booking not cancelled

**Description:** AC 04.3 — Decision Table: Tapping "×" on the cancel dialog dismisses it without cancelling the booking.

**Preconditions:**
Student has a booked lesson within cancellation deadline.

| #   | Action                                                 | Expected Result                                                          | Test Data |
| --- | ------------------------------------------------------ | ------------------------------------------------------------------------ | --------- |
| 1   | Open My Lessons list and tap Cancel on a booked lesson | Cancellation dialog shown                                                | —         |
| 2   | Tap "×" (close/secondary button)                       | Dialog dismissed                                                         | —         |
| 3   | View My Lessons list                                   | The lesson is still present in My Lessons list; no cancellation occurred | —         |
| 4   | Verify in Salesforce                                   | Student Session record still exists                                      | —         |

---

## Suite: Cancellation Deadline – Timezone

### [Nichibei] Lesson Booking – Cancel Deadline – Device timezone ahead of lesson timezone – Deadline uses lesson timezone

**Description:** AC 04.2 — BR-26: BVA (Timezone): When the student's device timezone is AHEAD of the lesson's timezone, the cancellation deadline must still be evaluated in the LESSON timezone. If the deadline has not yet passed in the lesson timezone, the Cancel button must remain enabled regardless of what the device clock shows.

**Preconditions:**
Partner config: cancellation deadline X = 2 hours.
Lesson timezone = UTC+9 (JST). Student's device timezone = UTC+11 (AEST, 2 hours ahead).
Lesson start = 2026-05-22 10:00 JST; deadline = 2026-05-22 08:00 JST (10:00 − 2h).
Current datetime = 2026-05-22 07:30 JST = 2026-05-22 09:30 AEST.

Deadline calculation:

- Lesson TZ (JST): current 2026-05-22 07:30 JST ≤ deadline 2026-05-22 08:00 JST → **within deadline** ✅
- Device TZ (AEST): device clock = 2026-05-22 09:30 AEST; device would calculate differently — but system must use lesson TZ

| #   | Action                                                                                                        | Expected Result                                            | Test Data                                                                                                                                     |
| --- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Confirm current datetime in JST = 2026-05-22 07:30 ≤ deadline 2026-05-22 08:00 — within cancellation deadline | Within cancellation deadline in lesson timezone            | X = 2 h; lesson_start = 2026-05-22 10:00 JST; deadline = 2026-05-22 08:00 JST; current = 2026-05-22 07:30 JST; device = 2026-05-22 09:30 AEST |
| 2   | Open My Lessons list                                                                                          | Booked lesson card visible                                 | —                                                                                                                                             |
| 3   | View Cancel button on the lesson card                                                                         | Cancel button is enabled and tappable                      | —                                                                                                                                             |
| 4   | Tap Cancel and tap "Cancel Reservation"                                                                       | Cancellation succeeds; lesson removed from My Lessons list | —                                                                                                                                             |

---

### [Nichibei] Lesson Booking – Cancel Deadline – Device timezone behind lesson timezone – Deadline uses lesson timezone

**Description:** AC 04.2 — BR-26: BVA (Timezone): When the student's device timezone is BEHIND the lesson's timezone, the Cancel button must be DISABLED if the cancellation deadline has passed in the lesson timezone, even if the device clock shows the student is still within the deadline.

**Preconditions:**
Partner config: cancellation deadline X = 2 hours.
Lesson timezone = UTC+9 (JST). Student's device timezone = UTC+7 (ICT, 2 hours behind).
Lesson start = 2026-05-22 10:00 JST; deadline = 2026-05-22 08:00 JST (10:00 − 2h).
Current datetime = 2026-05-22 08:30 JST = 2026-05-22 06:30 ICT.

Deadline calculation:

- Lesson TZ (JST): current 2026-05-22 08:30 JST > deadline 2026-05-22 08:00 JST → **past deadline** ❌
- Device TZ (ICT): device clock = 2026-05-22 06:30 ICT; device would suggest still within deadline — but system must use lesson TZ

| #   | Action                                                                                                                                         | Expected Result                                                                | Test Data                                                                                                                                    |
| --- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Confirm current datetime in JST = 2026-05-22 08:30 > deadline 2026-05-22 08:00 — past cancellation deadline; device shows 2026-05-22 06:30 ICT | Past cancellation deadline in lesson timezone despite device showing otherwise | X = 2 h; lesson_start = 2026-05-22 10:00 JST; deadline = 2026-05-22 08:00 JST; current = 2026-05-22 08:30 JST; device = 2026-05-22 06:30 ICT |
| 2   | Open My Lessons list                                                                                                                           | Booked lesson card visible                                                     | —                                                                                                                                            |
| 3   | View Cancel button on the lesson card                                                                                                          | Cancel button is DISABLED (greyed out)                                         | —                                                                                                                                            |
| 4   | Tap the disabled Cancel button                                                                                                                 | Tooltip shown: "Cancellation not available within 2 hours of start time"       | X = 2; tooltip text reflects configured X value                                                                                              |

---

## Suite: Multi-Account – Session Isolation

### [Nichibei] Lesson Booking – Multi-Account – Student 1 cancels own booking after switch from Student 2 – Correct session removed

**Description:** AC 04.1 — BR-23: Session Isolation: After two students book lessons on the same device, Student 1 switches back and cancels their own booking. Only Student 1’s session must be deleted; Student 2’s booking must remain intact.

**Preconditions:**
Student 1 has booked Lesson 1. Student 2 has booked Lesson 2. Both bookings made on the same device.
Both lessons are within the cancellation deadline.

| #   | Action                                                                                               | Expected Result                                                         | Test Data                                  |
| --- | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- | ------------------------------------------ |
| 1   | Confirm Student 1's My Lessons list shows Lesson 1; Student 2's My Lessons list shows Lesson 2 in SF | Both Student Sessions exist                                             | Student 1 → Lesson 1; Student 2 → Lesson 2 |
| 2   | Login as Student 2 → open My Lessons list                                                            | Lesson 2 shown in My Lessons list                                       | Student 2                                  |
| 3   | Switch account to Student 1 on the same device                                                       | Student 1 home screen shown                                             | Student 1                                  |
| 4   | Open My Lessons list → tap Cancel on Lesson 1 → tap "Cancel Reservation"                             | Cancellation Success; Lesson 1 removed from Student 1's My Lessons list | —                                          |
| 5   | Verify in Salesforce: Student Session (Student 1, Lesson 1)                                          | Session deleted                                                         | —                                          |
| 6   | Verify in Salesforce: Student Session (Student 2, Lesson 2)                                          | Session still exists with Booking_Flag=TRUE                             | —                                          |

---

### [Nichibei] Lesson Booking – Multi-Account – Student cancels booking then switches to Parent – Parent cannot cancel

**Description:** AC 04.1 / AC 06.1 — BR-23/BR-29: Session Isolation: After a student cancels a booking and switches to a parent account on the same device, the parent must NOT be able to access cancellation features.

**Preconditions:**
Student has booked Lesson 1 (within cancellation deadline). Parent account is accessible on the same device.

| #   | Action                                                                                      | Expected Result                                                          | Test Data       |
| --- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | --------------- |
| 1   | Login as Student → open My Lessons list → tap Cancel on Lesson 1 → tap "Cancel Reservation" | Cancellation succeeds; Lesson 1 removed from My Lessons list             | Student account |
| 2   | Switch account to Parent on the same device                                                 | Parent home screen shown                                                 | Parent account  |
| 3   | Navigate to Reservation List menu area                                                        | Reservation List menu is NOT visible for Parent                            | —               |
| 4   | Verify in Salesforce: Student Session (Student, Lesson 1)                                   | Session deleted (cancelled by Student); no new session created by Parent | —               |

---

## Suite: Manual Remove – Interaction

### [Nichibei] Lesson Booking – Manual Remove – Staff deletes Student Session from SF – My Lessons no longer shows lesson

**Description:** AC 01.1 — BR-1: When a staff member deletes a Student Session from Salesforce (manually removes a student from a lesson), the student's My Lessons must no longer display that lesson on the next refresh, as it no longer has Booking_Flag=TRUE.

**Preconditions:**
Student A has booked Lesson 1 via app; session exists in SF with Booking_Flag=TRUE.
Student A's My Lessons list currently shows Lesson 1.

| #   | Action                                                                       | Expected Result                                                     | Test Data           |
| --- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------- |
| 1   | Confirm Student A's My Lessons list shows Lesson 1                           | Lesson 1 visible                                                    | Student A; Lesson 1 |
| 2   | Staff deletes Student Session (Student A, Lesson 1) directly from Salesforce | Session removed from SF                                             | Staff; SF           |
| 3   | Student A refreshes My Lessons list in app                                   | Lesson 1 no longer appears in My Lessons list                       | —                   |
| 4   | Verify in Salesforce                                                         | No Student Session with Booking_Flag=TRUE for (Student A, Lesson 1) | —                   |

---

### [Nichibei] Lesson Booking – Manual Remove – Staff-assigned session (Booking_Flag=OFF) not shown in My Lessons – Student cannot cancel

**Description:** AC 01.1 / AC 04.1 — BR-1/BR-3: A session created by staff via Salesforce (Booking_Flag=FALSE/blank) must NOT appear in the student's My Lessons. Therefore the student has no Cancel button for that session — cancellation via app is not possible for staff-assigned sessions.

**Preconditions:**
Staff has assigned Student A to Lesson 1 via Salesforce (Booking_Flag=FALSE).
No app-booked session exists for (Student A, Lesson 1).

| #   | Action                                                                             | Expected Result                                                                  | Test Data                               |
| --- | ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | --------------------------------------- |
| 1   | Confirm Student Session (Student A, Lesson 1) exists in SF with Booking_Flag=FALSE | Session exists; staff-assigned                                                   | Student A; Lesson 1; Booking_Flag=FALSE |
| 2   | Login as Student A → open My Lessons list                                          | Lesson 1 is NOT shown in My Lessons list                                         | —                                       |
| 3   | Verify Student A cannot cancel Lesson 1 via app                                    | No Cancel button or entry for Lesson 1 in My Lessons list                        | —                                       |
| 4   | Verify in Salesforce                                                               | Student Session for (Student A, Lesson 1) remains intact with Booking_Flag=FALSE | —                                       |

---

## Suite: Post-Cancellation – Data Integrity

### [Nichibei] Lesson Booking – Cancel Booking – LA Lesson Allocated count decrements by 1 after cancellation

**Description:** AC 04.4 — BR-23: Data Integrity: When a student cancels a self-booked lesson (deleting the Student Session), the linked LA's Lesson_Allocated count must decrement by 1 and the LA status must update accordingly. This mirrors the counter rollback triggered by manual staff removal.

**Preconditions:**
Student A has booked Lesson 1 (Booking_Flag=TRUE). LA-A's Lesson_Allocated = 1; LA Status = "Partial Assigned".
Lesson 1 is within the cancellation deadline.

| #   | Action                                                                                | Expected Result                                                                    | Test Data                               |
| --- | ------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | --------------------------------------- |
| 1   | Record LA-A Lesson_Allocated count in Salesforce before cancellation                  | LA-A Lesson_Allocated = 1; Status = "Partial Assigned"                             | LA-A Lesson_Allocated = 1 before cancel |
| 2   | Student A opens My Lessons list → taps Cancel on Lesson 1 → taps "Cancel Reservation" | Cancellation confirmed; Lesson 1 removed from My Lessons list                      | —                                       |
| 3   | Verify LA-A Lesson_Allocated count in Salesforce after cancellation                   | LA-A Lesson_Allocated = 0 (decremented from 1)                                     | —                                       |
| 4   | Verify LA-A status in Salesforce after cancellation                                   | LA Status updated to "None Assigned" (count = 0) or corresponding status per count | —                                       |

---

### [Nichibei] Lesson Booking – Cancel Booking – Lesson Report Detail deleted after cancellation

**Description:** AC 04.4 — BR-23: Data Integrity: When a student cancels a self-booked lesson (Student Session deleted), the associated Lesson Report Detail record must also be deleted from Salesforce. This ensures the Collect Attendance list for staff accurately reflects only students still assigned to the lesson.

**Preconditions:**
Student A booked Lesson 1; a Lesson Report Detail record exists for (Student A, Lesson 1) in Salesforce.
Lesson 1 is within the cancellation deadline.

| #   | Action                                                                                | Expected Result                                                      | Test Data           |
| --- | ------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | ------------------- |
| 1   | Verify Lesson Report Detail exists for (Student A, Lesson 1) in Salesforce            | Lesson Report Detail record found (created at booking time)          | Student A; Lesson 1 |
| 2   | Student A opens My Lessons list → taps Cancel on Lesson 1 → taps "Cancel Reservation" | Cancellation confirmed; Lesson 1 removed from My Lessons list        | —                   |
| 3   | Verify Lesson Report Detail in Salesforce after cancellation                          | Lesson Report Detail record for (Student A, Lesson 1) is deleted     | —                   |
| 4   | Staff opens BO Collect Attendance for Lesson 1                                        | Student A is no longer listed in the Collect Attendance student list | —                   |

---

## Suite: Cancellation Deadline – Config Change

### [Nichibei] Lesson Booking – Cancel Deadline Config – X decreased (4h→2h) – Previously disabled Cancel button becomes enabled

**Description:** AC 04.2 — BR-22 / Config: When admin decreases the cancellation deadline X from 4 hours to 2 hours, a lesson that was previously past the deadline (Cancel button disabled) must immediately show the Cancel button as enabled after refresh — because the shorter deadline now places the current time within the new window.

**Preconditions:**
Partner config: cancellation deadline X = 4 hours.
Student has booked Lesson A. Lesson A start = 2026-05-22 14:00 JST.
Current datetime = 2026-05-22 11:30 JST.
With X=4: deadline = 2026-05-22 10:00 JST; current 2026-05-22 11:30 > 2026-05-22 10:00 → **past deadline → Cancel DISABLED**.
After config change to X=2: deadline = 2026-05-22 12:00 JST; current 2026-05-22 11:30 ≤ 2026-05-22 12:00 → **within deadline → Cancel ENABLED**.

| #   | Action                                                        | Expected Result                                              | Test Data                                                                                                       |
| --- | ------------------------------------------------------------- | ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| 1   | Open My Lessons list with X=4 config                          | Lesson A Cancel button is DISABLED; tooltip shown on tap     | X = 4 h; Lesson A start = 2026-05-22 14:00 JST; deadline = 2026-05-22 10:00 JST; current = 2026-05-22 11:30 JST |
| 2   | Admin updates partner cancellation deadline config from 4h→2h | Config updated successfully                                  | X changed: 4 → 2; new deadline = 2026-05-22 12:00 JST                                                           |
| 3   | Student refreshes My Lessons list                             | Lesson A Cancel button is now ENABLED and tappable           | current 2026-05-22 11:30 JST ≤ new deadline 2026-05-22 12:00 JST → within deadline                              |
| 4   | Tap Cancel on Lesson A → confirm cancellation                 | Cancellation succeeds; Lesson A removed from My Lessons list | —                                                                                                               |

---

### [Nichibei] Lesson Booking – Cancel Deadline Config – X increased (2h→4h) – Previously enabled Cancel button becomes disabled

**Description:** AC 04.2 — BR-22 / Config: When admin increases the cancellation deadline X from 2 hours to 4 hours, a lesson that was previously within the deadline (Cancel button enabled) must immediately show the Cancel button as disabled with tooltip after refresh — because the longer deadline now places the current time past the new window.

**Preconditions:**
Partner config: cancellation deadline X = 2 hours.
Student has booked Lesson B. Lesson B start = 2026-05-22 14:00 JST.
Current datetime = 2026-05-22 11:30 JST.
With X=2: deadline = 2026-05-22 12:00 JST; current 2026-05-22 11:30 ≤ 2026-05-22 12:00 → **within deadline → Cancel ENABLED**.
After change to X=4: deadline = 2026-05-22 10:00 JST; current 2026-05-22 11:30 > 2026-05-22 10:00 → **past deadline → Cancel DISABLED**.

| #   | Action                                                        | Expected Result                                                          | Test Data                                                                                                       |
| --- | ------------------------------------------------------------- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| 1   | Open My Lessons list with X=2 config                          | Lesson B Cancel button is ENABLED and tappable                           | X = 2 h; Lesson B start = 2026-05-22 14:00 JST; deadline = 2026-05-22 12:00 JST; current = 2026-05-22 11:30 JST |
| 2   | Admin updates partner cancellation deadline config from 2h→4h | Config updated successfully                                              | X changed: 2 → 4; new deadline = 2026-05-22 10:00 JST                                                           |
| 3   | Student refreshes My Lessons list                             | Lesson B Cancel button is now DISABLED (greyed out)                      | current 2026-05-22 11:30 JST > new deadline 2026-05-22 10:00 JST → past deadline                                |
| 4   | Tap the disabled Cancel button                                | Tooltip shown: "Cancellation not available within 4 hours of start time" | X = 4; tooltip text reflects updated X value                                                                    |
