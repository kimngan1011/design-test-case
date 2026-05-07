# Test Cases: LT-96620 — [Nichibei] Lesson Booking System

## Suite: Cancel Booking

### [Nichibei] Lesson Booking – Cancel Entry Point – Booking List – Cancel button visible for booked lesson

**Description:** AC 04.1 — BR-3: Decision Table: Cancel button must appear on a booked lesson card in the Booking List.

**Preconditions:**
Student user has a booked lesson (Booking_Flag=TRUE) in their Booking List, within the cancellation deadline.

| #   | Action                                                      | Expected Result                        | Test Data |
| --- | ----------------------------------------------------------- | -------------------------------------- | --------- |
| 1   | Login to app as student user and open "Lesson Booking" menu | Booking List screen shown              | —         |
| 2   | View the booked lesson card                                 | "Cancel" button is visible on the card | —         |

---

### [Nichibei] Lesson Booking – Cancel Entry Point – Lesson List – Cancel button visible for booked lesson

**Description:** AC 04.1 — BR-3: Decision Table: Cancel button must appear for a booked lesson (Booking_Flag=TRUE) when viewed in the Lesson List screen.

**Preconditions:**
Student user has a booked lesson (Booking_Flag=TRUE), within the cancellation deadline. Student navigates to the Lesson List view.

| #   | Action                                            | Expected Result                                | Test Data |
| --- | ------------------------------------------------- | ---------------------------------------------- | --------- |
| 1   | Login to app as student user and open Lesson List | Lesson List screen shown                       | —         |
| 2   | Find the booked lesson                            | "Cancel" button is visible on the lesson entry | —         |

---

### [Nichibei] Lesson Booking – Cancel Entry Point – Lesson List – No Cancel button for staff-allocated lesson

**Description:** AC 04.1 — BR-11: Decision Table: Cancel button must NOT appear for staff-allocated lessons (Booking_Flag=OFF) in the Lesson List.

**Preconditions:**
Student user has a staff-allocated lesson (Booking_Flag=FALSE) in the Lesson List.

| #   | Action                                            | Expected Result                                        | Test Data |
| --- | ------------------------------------------------- | ------------------------------------------------------ | --------- |
| 1   | Login to app as student user and open Lesson List | Lesson List screen shown                               | —         |
| 2   | View the staff-allocated lesson card              | No "Cancel" button shown on the staff-allocated lesson | —         |

---

### [Nichibei] Lesson Booking – Cancel Deadline – Within deadline – Cancel button enabled

**Description:** AC 04.2 — BR-22: BVA: Cancel button must be enabled when current time is before the cancellation deadline (lesson start − 2 hours).

**Preconditions:**
Student has booked a lesson. Current time < (lesson start − 2 hours).
Lesson start = 14:00 JST; cancellation deadline = 12:00 JST (2 hours before start); current = 09:00 JST.

| #   | Action                 | Expected Result                       | Test Data                                                                              |
| --- | ---------------------- | ------------------------------------- | -------------------------------------------------------------------------------------- |
| 1   | Open Booking List      | Booked lesson card visible            | —                                                                                      |
| 2   | View the Cancel button | Cancel button is enabled and tappable | Lesson start = 14:00 JST; deadline = 12:00 JST (2 h before start); current = 09:00 JST |

---

### [Nichibei] Lesson Booking – Cancel Deadline – Past deadline – Cancel button disabled with tooltip

**Description:** AC 04.2 — BR-22: BVA: Cancel button must be disabled with tooltip when current time is past the cancellation deadline.

**Preconditions:**
Student has booked a lesson. Current time > (lesson start − 2 hours).
Lesson start = 11:00 JST; cancellation deadline = 09:00 JST (2 hours before start); current = 10:00 JST.

| #   | Action                                  | Expected Result                                                          | Test Data                                                                              |
| --- | --------------------------------------- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------- |
| 1   | Open Booking List                       | Booked lesson card visible                                               | —                                                                                      |
| 2   | View the Cancel button                  | Cancel button is disabled (greyed out)                                   | Lesson start = 11:00 JST; deadline = 09:00 JST (2 h before start); current = 10:00 JST |
| 3   | Tap or hover the disabled Cancel button | Tooltip shown: "Cancellation not available within 2 hours of start time" | —                                                                                      |

---

### [Nichibei] Lesson Booking – Cancel Dialog – Correct content displayed

**Description:** AC 04.3 — Equivalence Partitioning: Cancel confirmation dialog must show the correct title, message, and buttons.

**Preconditions:**
Student has a booked lesson within cancellation deadline.

| #   | Action                                                         | Expected Result                                                                  | Test Data |
| --- | -------------------------------------------------------------- | -------------------------------------------------------------------------------- | --------- |
| 1   | Open Booking List and tap the Cancel button on a booked lesson | Cancellation confirmation dialog opens                                           | —         |
| 2   | View dialog title                                              | Title reads: "Cancel Booking?"                                                   | —         |
| 3   | View dialog message                                            | Message reads: "Are you sure you want to cancel this reservation?"               | —         |
| 4   | View dialog buttons                                            | Two buttons: "×" (secondary / close) and "Cancel Reservation" (destructive, red) | —         |

---

### [Nichibei] Lesson Booking – Cancel Booking – Student Session deleted after cancellation

**Description:** AC 04.4 — BR-23: CRUD Testing: Confirming cancellation must delete the Student Session record from Salesforce.

**Preconditions:**
Student has a booked lesson within cancellation deadline.

| #   | Action                                           | Expected Result                                         | Test Data |
| --- | ------------------------------------------------ | ------------------------------------------------------- | --------- |
| 1   | Open Booking List, tap Cancel on a booked lesson | Cancellation dialog shown                               | —         |
| 2   | Tap "Cancel Reservation"                         | Cancellation processed                                  | —         |
| 3   | Verify in Salesforce                             | Student Session record for (student, lesson) is deleted | —         |
| 4   | Return to Booking List                           | Cancelled lesson is no longer shown in Booking List     | —         |

---

### [Nichibei] Lesson Booking – Cancel Booking – Points refunded to Point LA on cancellation

**Description:** AC 04.4 — BR-23/BR-31: CRUD Testing: When a student cancels a self-booked lesson, the points consumed at booking time must be refunded back to the Point LA (Remaining Points restored, Consumed Points decremented). This mirrors the point-refund behavior on manual staff removal.

**Preconditions:**
Student has booked Lesson 1. At booking time, 2 pts were deducted from Point LA-B (Remaining went from 5 → 3 pts).
Lesson is within the cancellation deadline.

| #   | Action                                                                | Expected Result                                            | Test Data                                           |
| --- | --------------------------------------------------------------------- | ---------------------------------------------------------- | --------------------------------------------------- |
| 1   | Record LA-B Remaining Points in Salesforce before cancellation        | Remaining Points = 3 pts (post-booking balance)            | LA-B Remaining = 3 pts; original Point Cost = 2 pts |
| 2   | Open Booking List → tap Cancel on Lesson 1 → tap "Cancel Reservation" | Cancellation confirmed; Lesson 1 removed from Booking List | —                                                   |
| 3   | Verify LA-B Remaining Points in Salesforce after cancellation         | Remaining Points = 5 pts (3 + 2 refunded)                  | —                                                   |
| 4   | Verify LA-B Consumed Points in Salesforce after cancellation          | Consumed Points decremented by 2 pts from pre-cancel value | —                                                   |

---

### [Nichibei] Lesson Booking – Cancel Booking – Return to Booking List after cancellation

**Description:** AC 04.4 — BR-23: State Transition: After confirming cancellation, app navigates back to Booking List and the lesson is removed.

**Preconditions:**
Student has a booked lesson within cancellation deadline. Booking List has only that 1 lesson.

| #   | Action                                                | Expected Result                                                  | Test Data |
| --- | ----------------------------------------------------- | ---------------------------------------------------------------- | --------- |
| 1   | Open Booking List and tap Cancel on the booked lesson | Cancellation dialog shown                                        | —         |
| 2   | Tap "Cancel Reservation"                              | App returns to updated Booking List                              | —         |
| 3   | View Booking List                                     | The cancelled lesson is no longer in the list; empty state shown | —         |

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

| #   | Action                                              | Expected Result                                                       | Test Data |
| --- | --------------------------------------------------- | --------------------------------------------------------------------- | --------- |
| 1   | Open Booking List and tap Cancel on a booked lesson | Cancellation dialog shown                                             | —         |
| 2   | Tap "×" (close/secondary button)                    | Dialog dismissed                                                      | —         |
| 3   | View Booking List                                   | The lesson is still present in Booking List; no cancellation occurred | —         |
| 4   | Verify in Salesforce                                | Student Session record still exists                                   | —         |

---

## Suite: Cancellation Deadline – Timezone

### [Nichibei] Lesson Booking – Cancel Deadline – Device timezone ahead of lesson timezone – Deadline uses lesson timezone

**Description:** AC 04.2 — BR-26: BVA (Timezone): When the student's device timezone is AHEAD of the lesson's timezone, the cancellation deadline must still be evaluated in the LESSON timezone. If the deadline has not yet passed in the lesson timezone, the Cancel button must remain enabled regardless of what the device clock shows.

**Preconditions:**
Lesson timezone = UTC+9 (JST). Student's device timezone = UTC+11 (AEST, 2 hours ahead).
Lesson start = today at 10:00 JST. Cancellation deadline = 2 hours before start = 08:00 JST.
Current time = 07:30 JST (within deadline) = 09:30 AEST.

| #   | Action                                                                    | Expected Result                                         | Test Data                                                 |
| --- | ------------------------------------------------------------------------- | ------------------------------------------------------- | --------------------------------------------------------- |
| 1   | Confirm current JST time = 07:30 (within 08:00 JST cancellation deadline) | Within cancellation deadline in lesson timezone         | Current time: 07:30 JST / 09:30 AEST; Deadline: 08:00 JST |
| 2   | Open Booking List                                                         | Booked lesson card visible                              | —                                                         |
| 3   | View Cancel button on the lesson card                                     | Cancel button is enabled and tappable                   | —                                                         |
| 4   | Tap Cancel and tap "Cancel Reservation"                                   | Cancellation succeeds; lesson removed from Booking List | —                                                         |

---

### [Nichibei] Lesson Booking – Cancel Deadline – Device timezone behind lesson timezone – Deadline uses lesson timezone

**Description:** AC 04.2 — BR-26: BVA (Timezone): When the student's device timezone is BEHIND the lesson's timezone, the Cancel button must be DISABLED if the cancellation deadline has passed in the lesson timezone, even if the device clock shows the student is still within the deadline.

**Preconditions:**
Lesson timezone = UTC+9 (JST). Student's device timezone = UTC+7 (ICT, 2 hours behind).
Lesson start = today at 10:00 JST. Cancellation deadline = 2 hours before start = 08:00 JST.
Current time = 08:30 JST (past deadline) = 06:30 ICT (device appears to show 1.5h before deadline).

| #   | Action                                                                                          | Expected Result                                                                | Test Data                                                |
| --- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | -------------------------------------------------------- |
| 1   | Confirm current JST time = 08:30 (past 08:00 JST cancellation deadline), device shows 06:30 ICT | Past cancellation deadline in lesson timezone despite device showing otherwise | Current time: 08:30 JST / 06:30 ICT; Deadline: 08:00 JST |
| 2   | Open Booking List                                                                               | Booked lesson card visible                                                     | —                                                        |
| 3   | View Cancel button on the lesson card                                                           | Cancel button is DISABLED (greyed out)                                         | —                                                        |
| 4   | Tap the disabled Cancel button                                                                  | Tooltip shown: "Cancellation not available within 2 hours of start time"       | —                                                        |

---

## Suite: Multi-Account – Session Isolation

### [Nichibei] Lesson Booking – Multi-Account – Student 1 cancels own booking after switch from Student 2 – Correct session removed

**Description:** AC 04.1 — BR-23: Session Isolation: After two students book lessons on the same device, Student 1 switches back and cancels their own booking. Only Student 1’s session must be deleted; Student 2’s booking must remain intact.

**Preconditions:**
Student 1 has booked Lesson 1. Student 2 has booked Lesson 2. Both bookings made on the same device.
Both lessons are within the cancellation deadline.

| #   | Action                                                                                         | Expected Result                                                      | Test Data                                  |
| --- | ---------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | ------------------------------------------ |
| 1   | Confirm Student 1’s Booking List shows Lesson 1; Student 2’s Booking List shows Lesson 2 in SF | Both Student Sessions exist                                          | Student 1 → Lesson 1; Student 2 → Lesson 2 |
| 2   | Login as Student 2 → open Booking List                                                         | Lesson 2 shown in Booking List                                       | Student 2                                  |
| 3   | Switch account to Student 1 on the same device                                                 | Student 1 home screen shown                                          | Student 1                                  |
| 4   | Open Booking List → tap Cancel on Lesson 1 → tap "Cancel Reservation"                          | Cancellation Success; Lesson 1 removed from Student 1’s Booking List | —                                          |
| 5   | Verify in Salesforce: Student Session (Student 1, Lesson 1)                                    | Session deleted                                                      | —                                          |
| 6   | Verify in Salesforce: Student Session (Student 2, Lesson 2)                                    | Session still exists with Booking_Flag=TRUE                          | —                                          |

---

### [Nichibei] Lesson Booking – Multi-Account – Student cancels booking then switches to Parent – Parent cannot cancel

**Description:** AC 04.1 / AC 06.1 — BR-23/BR-29: Session Isolation: After a student cancels a booking and switches to a parent account on the same device, the parent must NOT be able to access cancellation features.

**Preconditions:**
Student has booked Lesson 1 (within cancellation deadline). Parent account is accessible on the same device.

| #   | Action                                                                                   | Expected Result                                                          | Test Data       |
| --- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ | --------------- |
| 1   | Login as Student → open Booking List → tap Cancel on Lesson 1 → tap "Cancel Reservation" | Cancellation succeeds; Lesson 1 removed from Booking List                | Student account |
| 2   | Switch account to Parent on the same device                                              | Parent home screen shown                                                 | Parent account  |
| 3   | Navigate to Lesson Booking menu area                                                     | Lesson Booking menu is NOT visible for Parent                            | —               |
| 4   | Verify in Salesforce: Student Session (Student, Lesson 1)                                | Session deleted (cancelled by Student); no new session created by Parent | —               |

---

## Suite: Manual Remove – Interaction

### [Nichibei] Lesson Booking – Manual Remove – Staff deletes Student Session from SF – Booking List no longer shows lesson

**Description:** AC 01.1 — BR-1: When a staff member deletes a Student Session from Salesforce (manually removes a student from a lesson), the student's Booking List must no longer display that lesson on the next refresh, as it no longer has Booking_Flag=TRUE.

**Preconditions:**
Student A has booked Lesson 1 via app; session exists in SF with Booking_Flag=TRUE.
Student A's Booking List currently shows Lesson 1.

| #   | Action                                                                       | Expected Result                                                     | Test Data           |
| --- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------- | ------------------- |
| 1   | Confirm Student A's Booking List in app shows Lesson 1                       | Lesson 1 visible                                                    | Student A; Lesson 1 |
| 2   | Staff deletes Student Session (Student A, Lesson 1) directly from Salesforce | Session removed from SF                                             | Staff; SF           |
| 3   | Student A refreshes Booking List in app                                      | Lesson 1 no longer appears in Booking List                          | —                   |
| 4   | Verify in Salesforce                                                         | No Student Session with Booking_Flag=TRUE for (Student A, Lesson 1) | —                   |

---

### [Nichibei] Lesson Booking – Manual Remove – Staff-assigned session (Booking_Flag=OFF) not shown in Booking List – Student cannot cancel

**Description:** AC 01.1 / AC 04.1 — BR-1/BR-3: A session created by staff via Salesforce (Booking_Flag=FALSE/blank) must NOT appear in the student's Booking List. Therefore the student has no Cancel button for that session — cancellation via app is not possible for staff-assigned sessions.

**Preconditions:**
Staff has assigned Student A to Lesson 1 via Salesforce (Booking_Flag=FALSE).
No app-booked session exists for (Student A, Lesson 1).

| #   | Action                                                                             | Expected Result                                                                  | Test Data                               |
| --- | ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | --------------------------------------- |
| 1   | Confirm Student Session (Student A, Lesson 1) exists in SF with Booking_Flag=FALSE | Session exists; staff-assigned                                                   | Student A; Lesson 1; Booking_Flag=FALSE |
| 2   | Login as Student A → open Booking List                                             | Lesson 1 is NOT shown in Booking List                                            | —                                       |
| 3   | Verify Student A cannot cancel Lesson 1 via app                                    | No Cancel button or entry for Lesson 1 in Booking List                           | —                                       |
| 4   | Verify in Salesforce                                                               | Student Session for (Student A, Lesson 1) remains intact with Booking_Flag=FALSE | —                                       |
