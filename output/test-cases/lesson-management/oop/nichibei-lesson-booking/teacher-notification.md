# Test Cases: LT-96620 — [Nichibei] Lesson Booking System

## Suite: Teacher Notifications

### [Nichibei] Lesson Booking – Teacher Notification – Booking – SF notification sent within 30s

**Description:** AC 05.1 — BR-21: CRUD Testing: When a student books a lesson via app, the assigned teacher must receive a Salesforce notification within 30 seconds with the correct message.

**Preconditions:**
A bookable Published lesson exists with Teacher A assigned. Student user books the lesson via the app.

| #   | Action                                                            | Expected Result                                            | Test Data                                              |
| --- | ----------------------------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------ |
| 1   | Student books an available lesson via app (tap Reserve → Confirm) | Booking Success Screen shown                               | —                                                      |
| 2   | Check Teacher A's Salesforce notification inbox within 30 seconds | SF notification received by Teacher A                      | —                                                      |
| 3   | Read the notification message                                     | Message reads: "[Student Name] has reserved [Lesson Name]" | Student Name = test student; Lesson Name = test lesson |

---

### [Nichibei] Lesson Booking – Teacher Notification – Cancellation – SF notification sent within 30s

**Description:** AC 05.2 — BR-24: CRUD Testing: When a student cancels a booking via app, the assigned teacher must receive a Salesforce notification within 30 seconds with the correct message.

**Preconditions:**
A lesson has Teacher A assigned. Student user has an existing booking for this lesson and cancels it via the app.

| #   | Action                                                                    | Expected Result                                             | Test Data                                              |
| --- | ------------------------------------------------------------------------- | ----------------------------------------------------------- | ------------------------------------------------------ |
| 1   | Student cancels a booked lesson via app (tap Cancel → Cancel Reservation) | Cancellation confirmed; booking removed from list           | —                                                      |
| 2   | Check Teacher A's Salesforce notification inbox within 30 seconds         | SF notification received by Teacher A                       | —                                                      |
| 3   | Read the notification message                                             | Message reads: "[Student Name] has cancelled [Lesson Name]" | Student Name = test student; Lesson Name = test lesson |

---

### [Nichibei] Lesson Booking – Teacher Notification – Staff SF assignment – No notification sent

**Description:** AC 03.4 — BR-21: Regression Analysis: When staff assigns a student to a lesson via Salesforce (not via app booking), NO SF teacher notification must be triggered.

**Preconditions:**
A lesson with Teacher A assigned. A staff user assigns a student to the lesson via Salesforce Lesson Detail (not via app booking flow).

| #   | Action                                                    | Expected Result                                                      | Test Data |
| --- | --------------------------------------------------------- | -------------------------------------------------------------------- | --------- |
| 1   | Staff user assigns a student to the lesson via Salesforce | Student Session created by staff in SF                               | —         |
| 2   | Check Teacher A's Salesforce notification inbox           | No new notification received by Teacher A                            | —         |
| 3   | Confirm notification log                                  | No booking notification event created for staff-triggered assignment | —         |

---

## Suite: Multi-Account – Notification Isolation

### [Nichibei] Lesson Booking – Multi-Account – Student 1 books – Notification sent to correct teacher – Student 2 books different lesson – Each teacher notified correctly

**Description:** AC 05.1 — BR-24: Notification Isolation: When two students on the same device each book a different lesson (with different teachers), each teacher must receive a notification for their own lesson only. No cross-notification must occur.

**Preconditions:**
Student 1 and Student 2 have separate accounts on the same device. Both have active LAs.
Lesson 1 is assigned to Teacher A. Lesson 2 is assigned to Teacher B.

| #   | Action                                                           | Expected Result                                                                            | Test Data                      |
| --- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------ |
| 1   | Login as Student 1 → Browse Lessons → Reserve Lesson 1 → Confirm | Booking Success Screen shown                                                               | Student 1; Lesson 1; Teacher A |
| 2   | Switch account to Student 2 on the same device                   | Student 2 home screen shown                                                                | Student 2                      |
| 3   | Browse Lessons → Reserve Lesson 2 → Confirm                      | Booking Success Screen shown                                                               | Student 2; Lesson 2; Teacher B |
| 4   | Check Teacher A’s SF notification inbox within 30 seconds        | Teacher A receives: "[Student 1 name] has reserved [Lesson 1 name]"                        | —                              |
| 5   | Check Teacher B’s SF notification inbox within 30 seconds        | Teacher B receives: "[Student 2 name] has reserved [Lesson 2 name]"                        | —                              |
| 6   | Verify no cross-notifications                                    | Teacher A has no notification about Lesson 2; Teacher B has no notification about Lesson 1 | —                              |

---

### [Nichibei] Lesson Booking – Multi-Account – Student cancels booking – Switches to Student 2 who cancels different lesson – Each teacher notified correctly

**Description:** AC 05.2 — BR-24: Notification Isolation: When two students on the same device each cancel a different booking, each teacher must receive a cancellation notification for their own lesson only.

**Preconditions:**
Student 1 has booked Lesson 1 (Teacher A). Student 2 has booked Lesson 2 (Teacher B). Both within cancellation deadline. Both accounts accessible on the same device.

| #   | Action                                                                     | Expected Result                                                                            | Test Data                      |
| --- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------ |
| 1   | Login as Student 1 → Booking List → Cancel Lesson 1 → "Cancel Reservation" | Cancellation Success; Lesson 1 removed                                                     | Student 1; Lesson 1; Teacher A |
| 2   | Switch account to Student 2 on the same device                             | Student 2 home screen shown                                                                | Student 2                      |
| 3   | Booking List → Cancel Lesson 2 → "Cancel Reservation"                      | Cancellation Success; Lesson 2 removed                                                     | Student 2; Lesson 2; Teacher B |
| 4   | Check Teacher A’s SF notification inbox within 30 seconds                  | Teacher A receives: "[Student 1 name] has cancelled [Lesson 1 name]"                       | —                              |
| 5   | Check Teacher B’s SF notification inbox within 30 seconds                  | Teacher B receives: "[Student 2 name] has cancelled [Lesson 2 name]"                       | —                              |
| 6   | Verify no cross-notifications                                              | Teacher A has no notification about Lesson 2; Teacher B has no notification about Lesson 1 | —                              |

---

## Suite: Manual Remove – Notification

### [Nichibei] Lesson Booking – Manual Remove – Staff deletes Student Session from SF – No cancellation notification sent to teacher

**Description:** AC 03.4 / AC 04.4 — BR-21/BR-24: SF teacher notifications are triggered ONLY by app booking/cancellation flows. When a staff member manually deletes a Student Session from Salesforce (removes student), no cancellation notification must be sent to the teacher.

**Preconditions:**
Student A has booked Lesson 1 via app; session exists in SF with Booking_Flag=TRUE.
Teacher A is assigned to Lesson 1.

| #   | Action                                                                       | Expected Result                                                        | Test Data                      |
| --- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------------- | ------------------------------ |
| 1   | Confirm Student Session (Student A, Lesson 1) exists in SF                   | Session present; Teacher A assigned                                    | Student A; Lesson 1; Teacher A |
| 2   | Staff deletes Student Session (Student A, Lesson 1) directly from Salesforce | Session removed from SF by staff                                       | Staff; SF                      |
| 3   | Check Teacher A's SF notification inbox within 30 seconds                    | No new notification received by Teacher A                              | —                              |
| 4   | Confirm notification log                                                     | No cancellation notification event created for staff-triggered removal | —                              |

---

### [Nichibei] Lesson Booking – Manual Add – Staff assigns student via SF – No booking notification sent to teacher

**Description:** AC 03.4 — BR-21: When staff manually assigns a student to a lesson via Salesforce (creating a Student Session directly, not via app booking), no booking notification must be sent to the teacher. Notification is app-booking-triggered only.

**Preconditions:**
Lesson 1 exists with Teacher A assigned. No existing session for Student A.
Staff user has access to Salesforce to create Student Sessions manually.

| #   | Action                                                                              | Expected Result                                                      | Test Data                  |
| --- | ----------------------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------- |
| 1   | Staff user creates Student Session for (Student A, Lesson 1) directly in Salesforce | Student Session created; Booking_Flag=FALSE                          | Staff; Student A; Lesson 1 |
| 2   | Check Teacher A's SF notification inbox within 30 seconds                           | No new notification received by Teacher A                            | —                          |
| 3   | Confirm notification log                                                            | No booking notification event created for staff-triggered assignment | —                          |
