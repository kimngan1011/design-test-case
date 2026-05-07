# Test Cases: LT-96620 — [Nichibei] Lesson Booking System

## Suite: Book a Lesson

### [Nichibei] Lesson Booking – Booking Confirmation Screen – All required fields displayed

**Description:** AC 03.1 — Equivalence Partitioning: Verify the Booking Confirmation Screen shows all required fields: lesson name, date+time, location+classroom, teacher, and optional remarks field.

**Preconditions:**
Student user has active LA. A bookable lesson (Published, available) exists at student's LA location.

| #   | Action                                                       | Expected Result                                                        | Test Data |
| --- | ------------------------------------------------------------ | ---------------------------------------------------------------------- | --------- |
| 1   | Open Browse Lessons and tap "Reserve" on an available lesson | Booking Confirmation Screen opens                                      | —         |
| 2   | View all fields on the screen                                | Lesson Name, Date+Time, Location, Classroom, Teacher are all displayed | —         |
| 3   | View the remarks section                                     | Optional remarks input field is displayed                              | —         |

---

### [Nichibei] Lesson Booking – Book Lesson – Happy path – Student Session created

**Description:** AC 03.2 — BR-12: CRUD Testing: Full booking flow creates a Student Session record with Booking_Flag=TRUE for the correct student and lesson.

**Preconditions:**
Student user has 1 active LA for Location A. A Published, bookable lesson at Location A has available capacity and is within booking deadline.

| #   | Action                                                        | Expected Result                                                              | Test Data |
| --- | ------------------------------------------------------------- | ---------------------------------------------------------------------------- | --------- |
| 1   | Open Browse Lessons and tap "Reserve" on the available lesson | Booking Confirmation Screen opens                                            | —         |
| 2   | Review details and tap "Confirm"                              | Booking submitted                                                            | —         |
| 3   | View the Booking Success Screen                               | Booking success screen is shown with lesson details and action buttons       | —         |
| 4   | Open Booking List                                             | Lesson appears in the student's Booking List with Booking_Flag=TRUE          | —         |
| 5   | Verify in Salesforce                                          | A Student Session record exists for (student, lesson) with Booking_Flag=TRUE | —         |

---

### [Nichibei] Lesson Booking – Book Lesson – Draft lesson auto-published silently on booking

**Description:** AC 03.2 — BR-13/BR-30: State Transition: When a student books a Draft lesson, the lesson status must be automatically set to Published. This auto-publish must NOT trigger any push notification to other students assigned to the lesson.

**Preconditions:**
Student A and Student B are both assigned to a Draft lesson at Location A (Bookable_Flag=TRUE, available capacity, within booking deadline). Student A will perform the booking.

| #   | Action                                                                                  | Expected Result                                               | Test Data |
| --- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------- | --------- |
| 1   | Confirm lesson status = Draft in Salesforce and Student B is assigned                   | Lesson status = Draft; Student B assignment confirmed         | —         |
| 2   | Student A opens Browse Lessons, taps "Reserve" on the Draft lesson, then taps "Confirm" | Booking Success Screen shown                                  | —         |
| 3   | Verify lesson status in Salesforce after booking                                        | Lesson status = Published (auto-published)                    | —         |
| 4   | Check Student B's device for push notifications                                         | No push notification received by Student B                    | —         |
| 5   | Verify no publish notification event logged in system                                   | No notification event created for the auto-publish transition | —         |

---

### [Nichibei] Lesson Booking – Book Lesson – Remarks saved with "Booking Note: " prefix

**Description:** AC 03.2 — BR-14: Equivalence Partitioning: When student enters remarks, the value is saved to Attendance_Response_Remark with "Booking Note: " prefix.

**Preconditions:**
Student user has active LA. A bookable Published lesson exists with available capacity within deadline.

| #   | Action                                                    | Expected Result                                             | Test Data                                 |
| --- | --------------------------------------------------------- | ----------------------------------------------------------- | ----------------------------------------- |
| 1   | Open Browse Lessons, tap "Reserve" on an available lesson | Booking Confirmation Screen opens                           | —                                         |
| 2   | Enter text in the remarks field                           | Text entered successfully                                   | remarks = "Please arrange front row seat" |
| 3   | Tap "Confirm"                                             | Booking Success Screen shown                                | —                                         |
| 4   | Verify Attendance_Response_Remark in Salesforce           | Field value = "Booking Note: Please arrange front row seat" | —                                         |

---

### [Nichibei] Lesson Booking – Book Lesson – Booking without remarks – No prefix added

**Description:** AC 03.2 — BR-14: Equivalence Partitioning: When student leaves remarks empty, Attendance_Response_Remark is not created with any prefix.

**Preconditions:**
Student user has active LA. A bookable Published lesson exists with available capacity within deadline.

| #   | Action                                                    | Expected Result                                           | Test Data |
| --- | --------------------------------------------------------- | --------------------------------------------------------- | --------- |
| 1   | Open Browse Lessons, tap "Reserve" on an available lesson | Booking Confirmation Screen opens                         | —         |
| 2   | Leave the remarks field empty                             | Remarks field is blank                                    | —         |
| 3   | Tap "Confirm"                                             | Booking Success Screen shown                              | —         |
| 4   | Verify Attendance_Response_Remark in Salesforce           | Field is empty or null; no "Booking Note: " entry created | —         |

---

### [Nichibei] Lesson Booking – LA Selection – One active LA – That LA used for booking

**Description:** AC 03.2 — BR-15: Decision Table: When student has exactly one active LA, it is selected for the booking automatically.

**Preconditions:**
Student user has exactly 1 active LA (LA-A). A bookable lesson at LA-A's location is available.

| #   | Action                                        | Expected Result                                      | Test Data |
| --- | --------------------------------------------- | ---------------------------------------------------- | --------- |
| 1   | Book a lesson via app (tap Reserve → Confirm) | Booking Success Screen shown                         | —         |
| 2   | Verify Student Session in Salesforce          | Session is linked to LA-A; points deducted from LA-A | —         |

---

### [Nichibei] Lesson Booking – LA Selection – Location-matching LA prioritized over non-matching

**Description:** AC 03.2 — BR-15: Decision Table (Priority Level 2): When student has 2 active LAs and only one's location matches the lesson location, the location-matching LA is selected.

**Preconditions:**
Student user has 2 active LAs:

- LA-A: location = Location A, active during lesson date
- LA-B: location = Location B, active during lesson date
  Lesson is at Location A.

| #   | Action                                | Expected Result                                              | Test Data |
| --- | ------------------------------------- | ------------------------------------------------------------ | --------- |
| 1   | Book the lesson at Location A via app | Booking Success Screen shown                                 | —         |
| 2   | Verify Student Session in Salesforce  | Session is linked to LA-A (location match); LA-B is not used | —         |

---

### [Nichibei] Lesson Booking – LA Selection – Earliest start date LA selected when locations both match

**Description:** AC 03.2 — BR-15: Decision Table (Priority Level 3): When student has 2 active LAs both with matching location, the LA with the earlier start date is selected.

**Preconditions:**
Student user has 2 active LAs at Location A:

- LA-A: start date = 2026-01-01
- LA-B: start date = 2026-03-01
  Lesson is at Location A. Both LAs are active during lesson date.

| #   | Action                                | Expected Result                                           | Test Data                                        |
| --- | ------------------------------------- | --------------------------------------------------------- | ------------------------------------------------ |
| 1   | Book the lesson at Location A via app | Booking Success Screen shown                              | —                                                |
| 2   | Verify Student Session in Salesforce  | Session is linked to LA-A (earlier start date 2026-01-01) | LA-A start = 2026-01-01; LA-B start = 2026-03-01 |

---

### [Nichibei] Lesson Booking – LA Selection – Earliest created LA selected as final tiebreaker

**Description:** AC 03.2 — BR-15: Decision Table (Priority Level 4): When 2 LAs are equal in location and start date, the LA created earlier is selected.

**Preconditions:**
Student user has 2 active LAs at Location A with the same start date:

- LA-A: created_at = 2026-01-01 09:00
- LA-B: created_at = 2026-01-01 14:00

| #   | Action                               | Expected Result                             | Test Data                                  |
| --- | ------------------------------------ | ------------------------------------------- | ------------------------------------------ |
| 1   | Book a lesson at Location A via app  | Booking Success Screen shown                | —                                          |
| 2   | Verify Student Session in Salesforce | Session is linked to LA-A (created earlier) | LA-A created = 09:00; LA-B created = 14:00 |

---

### [Nichibei] Lesson Booking – Point Consumption – Points deducted from correct Point LA on booking

**Description:** AC 03.2 — BR-31: CRUD Testing: When a student successfully books a lesson, the lesson's Course Category Point_Consumption_Value must be deducted from the selected Point LA (Remaining Points decremented, Consumed Points incremented). Uses the same mechanism as manual staff assignment.

**Preconditions:**
Student has:

- Assignment LA-A: Course = Math, Require_Allocation=TRUE (authorises assignment)
- Point LA-B: Course = General Studies (General_Flag=TRUE), Priority=FALSE, Require_Allocation=FALSE, Remaining Points = 5 pts
  Lesson is at student's LA location, Course = Math. Course Category Point_Consumption_Value = 2 pts.

| #   | Action                                                    | Expected Result                                     | Test Data                                         |
| --- | --------------------------------------------------------- | --------------------------------------------------- | ------------------------------------------------- |
| 1   | Record LA-B Remaining Points in Salesforce before booking | Remaining Points = 5 pts; Consumed Points noted     | LA-B Remaining = 5 pts; Course Point Cost = 2 pts |
| 2   | Book the lesson via app (tap Reserve → Confirm)           | Booking Success Screen shown                        | —                                                 |
| 3   | Verify LA-B Remaining Points in Salesforce after booking  | Remaining Points = 3 pts (5 − 2)                    | —                                                 |
| 4   | Verify LA-B Consumed Points in Salesforce after booking   | Consumed Points incremented by 2 pts from pre-value | —                                                 |

---

### [Nichibei] Lesson Booking – Point Consumption – Priority=TRUE Point LA consumed before Priority=FALSE

**Description:** AC 03.2 — BR-31 / Point Priority Algorithm Step 3: When student has both a Priority=TRUE and a Priority=FALSE Point LA for the same course, the Priority=TRUE LA must be selected and consumed first. The Priority=FALSE LA must remain unchanged.

**Preconditions:**
Student has:

- Assignment LA: Course = Math, Require_Allocation=TRUE
- Point LA-1: Course = Math, Priority=TRUE, Require_Allocation=FALSE, Remaining = 10 pts
- Point LA-3: Course = Math, Priority=FALSE, Require_Allocation=FALSE, Remaining = 8 pts
  Lesson course = Math. Course Category Point_Consumption_Value = 2 pts.

| #   | Action                                                      | Expected Result                                           | Test Data                                       |
| --- | ----------------------------------------------------------- | --------------------------------------------------------- | ----------------------------------------------- |
| 1   | Record LA-1 and LA-3 Remaining Points in Salesforce         | LA-1 Remaining = 10 pts; LA-3 Remaining = 8 pts           | LA-1 = 10 pts; LA-3 = 8 pts; Point Cost = 2 pts |
| 2   | Book the Math lesson via app (tap Reserve → Confirm)        | Booking Success Screen shown                              | —                                               |
| 3   | Verify LA-1 (Priority=TRUE) Remaining Points in Salesforce  | LA-1 Remaining = 8 pts (10 − 2); Priority LA was consumed | —                                               |
| 4   | Verify LA-3 (Priority=FALSE) Remaining Points in Salesforce | LA-3 Remaining = 8 pts unchanged; not consumed            | —                                               |

---

### [Nichibei] Lesson Booking – Validation – Duplicate booking blocked

**Description:** AC 03.3 — BR-16: Negative Testing: Attempting to book a lesson the student is already allocated to must be rejected with the correct error message.

**Preconditions:**
Student user has already booked (or been allocated to) the target lesson. Student attempts to book the same lesson again.

| #   | Action                                                                                            | Expected Result                                            | Test Data |
| --- | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | --------- |
| 1   | Open Browse Lessons                                                                               | The already-booked lesson is visible (Cancel button shown) | —         |
| 2   | Attempt to submit a second booking for the same lesson (e.g., via rapid double-tap or API replay) | Booking rejected                                           | —         |
| 3   | View error message                                                                                | Error shown: "You have already reserved this lesson."      | —         |
| 4   | Verify Student Session count in Salesforce                                                        | Only 1 Student Session exists for (student, lesson)        | —         |

---

### [Nichibei] Lesson Booking – Validation – Lesson full – Booking blocked

**Description:** AC 03.3 — BR-17: BVA: Booking must be rejected when the lesson has reached maximum capacity at submission time.

**Preconditions:**
A bookable lesson with capacity=1. Another student has already booked it (session count = 1 = capacity).

| #   | Action                                                         | Expected Result                                                       | Test Data    |
| --- | -------------------------------------------------------------- | --------------------------------------------------------------------- | ------------ |
| 1   | Open Browse Lessons                                            | Lesson card visible (may show as full)                                | capacity = 1 |
| 2   | Attempt to book the lesson (e.g., race condition or UI bypass) | Booking rejected at submission                                        | —            |
| 3   | View error message                                             | Error shown: "This lesson is now full. Please choose another lesson." | —            |
| 4   | Verify no new Student Session created                          | Session count in SF remains at capacity                               | —            |

---

### [Nichibei] Lesson Booking – Validation – Past booking deadline – Booking blocked

**Description:** AC 03.3 — BR-18: BVA: Booking must be rejected when submitted after the booking deadline has passed.

**Preconditions:**
Current time is past (lesson start − booking deadline hours). Student attempts to submit booking.

| #   | Action                                                             | Expected Result                                                 | Test Data               |
| --- | ------------------------------------------------------------------ | --------------------------------------------------------------- | ----------------------- |
| 1   | Attempt to submit a booking for a lesson past its booking deadline | Booking rejected                                                | deadline already passed |
| 2   | View error message                                                 | Error shown: "The booking deadline has passed for this lesson." | —                       |

---

### [Nichibei] Lesson Booking – Validation – No active LA – Booking blocked

**Description:** AC 03.3 — BR-19: Negative Testing: Booking must be rejected when student has no active Lesson Allocation at submission time.

**Preconditions:**
Student's LA has expired between Browse and Confirmation step (or LA deleted mid-flow).

| #   | Action                                                        | Expected Result                                                      | Test Data |
| --- | ------------------------------------------------------------- | -------------------------------------------------------------------- | --------- |
| 1   | Begin booking flow (Confirmation Screen already open)         | Booking Confirmation Screen shown                                    | —         |
| 2   | Invalidate student's LA (expire or delete) then tap "Confirm" | Booking rejected                                                     | —         |
| 3   | View error message                                            | Error shown: "You are not eligible to reserve lessons at this time." | —         |

---

### [Nichibei] Lesson Booking – Validation – Insufficient points – Booking blocked

**Description:** AC 03.3 — BR-20/BR-31: Negative Testing: Booking must be rejected when the student's remaining LA points are less than the lesson point cost.

**Preconditions:**
Student user has active LA with 0 remaining points. Lesson point cost > 0.

| #   | Action                                                              | Expected Result                                                       | Test Data                             |
| --- | ------------------------------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------- |
| 1   | Open Browse Lessons and tap "Reserve" on a lesson that costs points | Booking Confirmation Screen opens                                     | remaining points = 0; lesson cost > 0 |
| 2   | Tap "Confirm"                                                       | Booking rejected                                                      | —                                     |
| 3   | View error message                                                  | Error shown: "Remaining points are insufficient to book this lesson." | —                                     |

---

### [Nichibei] Lesson Booking – Post-Booking – Booking Success Screen shown

**Description:** AC 03.4 — BR-21: CRUD Testing: After a successful booking, the app navigates to a Booking Success Screen showing lesson details.

**Preconditions:**
Student user has active LA. A bookable Published lesson exists with capacity and within deadline.

| #   | Action                                                   | Expected Result                                                               | Test Data |
| --- | -------------------------------------------------------- | ----------------------------------------------------------------------------- | --------- |
| 1   | Book an available lesson via app (tap Reserve → Confirm) | Booking Success Screen is shown                                               | —         |
| 2   | View the success screen content                          | Lesson name, date+time, location, teacher are displayed on the success screen | —         |

---

### [Nichibei] Lesson Booking – Post-Booking – Lesson appears in Booking List

**Description:** AC 03.4 — BR-1: CRUD Testing: After a successful booking, the lesson appears in the student's Booking List.

**Preconditions:**
Student user has active LA. Booking List is initially empty.

| #   | Action                                       | Expected Result                                                        | Test Data |
| --- | -------------------------------------------- | ---------------------------------------------------------------------- | --------- |
| 1   | Confirm Booking List is empty before booking | Booking List shows empty state                                         | —         |
| 2   | Book an available lesson via app             | Booking Success Screen shown                                           | —         |
| 3   | Navigate to Booking List                     | The newly booked lesson appears in Booking List with Booking_Flag=TRUE | —         |

---

## Suite: Booking Deadline – Timezone

### [Nichibei] Lesson Booking – Booking Deadline – Device timezone ahead of lesson timezone – Deadline uses lesson timezone

**Description:** AC 03.3 — BR-26: BVA (Timezone): When the student's device timezone is AHEAD of the lesson's timezone, the booking deadline must still be evaluated in the LESSON timezone. A student whose device shows the deadline has not passed must be able to book if lesson timezone confirms they are within deadline.

**Preconditions:**
Lesson timezone = UTC+9 (JST). Student's device timezone = UTC+11 (AEST, 2 hours ahead).
Lesson start = today at 10:00 JST. Booking deadline = 2 hours before start = 08:00 JST.
Current time = 07:30 JST (within deadline) = 09:30 AEST.

| #   | Action                                                       | Expected Result                                       | Test Data                                                 |
| --- | ------------------------------------------------------------ | ----------------------------------------------------- | --------------------------------------------------------- |
| 1   | Confirm current JST time = 07:30 (within 08:00 JST deadline) | Within booking deadline in lesson timezone            | Current time: 07:30 JST / 09:30 AEST; Deadline: 08:00 JST |
| 2   | Open Browse Lessons and tap "Reserve" on the lesson          | Booking Confirmation Screen opens                     | —                                                         |
| 3   | Tap "Confirm"                                                | Booking succeeds                                      | —                                                         |
| 4   | View result                                                  | Booking Success Screen shown; Student Session created | —                                                         |

---

### [Nichibei] Lesson Booking – Booking Deadline – Device timezone behind lesson timezone – Deadline uses lesson timezone

**Description:** AC 03.3 — BR-26: BVA (Timezone): When the student's device timezone is BEHIND the lesson's timezone, the booking must be REJECTED if the deadline has passed in the lesson timezone, even if the device clock shows the deadline has not yet passed.

**Preconditions:**
Lesson timezone = UTC+9 (JST). Student's device timezone = UTC+7 (ICT, 2 hours behind).
Lesson start = today at 10:00 JST. Booking deadline = 2 hours before start = 08:00 JST.
Current time = 08:30 JST (past deadline) = 06:30 ICT (device appears to show 1.5h before deadline).

| #   | Action                                                                             | Expected Result                                                           | Test Data                                                |
| --- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------- |
| 1   | Confirm current JST time = 08:30 (past 08:00 JST deadline), device shows 06:30 ICT | Past booking deadline in lesson timezone despite device showing otherwise | Current time: 08:30 JST / 06:30 ICT; Deadline: 08:00 JST |
| 2   | Attempt to submit booking (tap Reserve → Confirm)                                  | Booking rejected                                                          | —                                                        |
| 3   | View error message                                                                 | Error shown: "The booking deadline has passed for this lesson."           | —                                                        |

---

## Suite: Multi-Account – Session Isolation

### [Nichibei] Lesson Booking – Multi-Account – Two students same device – Different lessons – Each session isolated

**Description:** AC 03.2 — BR-12: Session Isolation: When two students use the same device sequentially, each booking must create a Student Session for the correct student only. Switching accounts must not contaminate session ownership.

**Preconditions:**
Student 1 and Student 2 have separate accounts on the same device. Both have active LAs.
Lesson 1 is at Student 1’s LA location (bookable, capacity ≥ 2). Lesson 2 is at Student 2’s LA location (bookable, capacity ≥ 2).

| #   | Action                                                                           | Expected Result                                                               | Test Data           |
| --- | -------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------- |
| 1   | Login as Student 1 → open Browse Lessons → tap Reserve on Lesson 1 → tap Confirm | Booking Success Screen shown for Student 1                                    | Student 1; Lesson 1 |
| 2   | Switch account to Student 2 on the same device                                   | Student 2 home screen shown                                                   | Student 2           |
| 3   | Open Browse Lessons → tap Reserve on Lesson 2 → tap Confirm                      | Booking Success Screen shown for Student 2                                    | Student 2; Lesson 2 |
| 4   | Verify in Salesforce: Student Session for (Student 1, Lesson 1)                  | Session exists with Booking_Flag=TRUE; student = Student 1                    | —                   |
| 5   | Verify in Salesforce: Student Session for (Student 2, Lesson 2)                  | Session exists with Booking_Flag=TRUE; student = Student 2                    | —                   |
| 6   | Verify no cross-contaminated sessions exist                                      | No session for (Student 1, Lesson 2) and no session for (Student 2, Lesson 1) | —                   |

---

### [Nichibei] Lesson Booking – Multi-Account – Two students same device – Same lesson – Two separate sessions created

**Description:** AC 03.2 — BR-12: Session Isolation: When two students use the same device and both book the same lesson, two independent Student Sessions must be created, each linked to the correct student.

**Preconditions:**
Student 1 and Student 2 have separate accounts on the same device. Both have active LAs for the same location.
Lesson 1 is bookable with capacity ≥ 2.

| #   | Action                                                                | Expected Result                                                                                 | Test Data           |
| --- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | ------------------- |
| 1   | Login as Student 1 → open Browse Lessons → Reserve Lesson 1 → Confirm | Booking Success Screen shown for Student 1                                                      | Student 1; Lesson 1 |
| 2   | Switch account to Student 2 on the same device                        | Student 2 home screen shown                                                                     | Student 2           |
| 3   | Open Browse Lessons → Reserve Lesson 1 → Confirm                      | Booking Success Screen shown for Student 2                                                      | Student 2; Lesson 1 |
| 4   | Verify in Salesforce: 2 Student Sessions exist for Lesson 1           | Two separate sessions: one for Student 1, one for Student 2, each with Booking_Flag=TRUE        | capacity ≥ 2        |
| 5   | Verify session ownership                                              | Each session’s student field matches the respective student; no session is shared or duplicated | —                   |

---

### [Nichibei] Lesson Booking – Multi-Account – Student books lesson – Switches to Parent – Parent has no booking access

**Description:** AC 06.1 — BR-29: Session Isolation: After a student books a lesson and switches to a parent account on the same device, the parent must NOT have access to any booking features. The student’s session must remain unaffected.

**Preconditions:**
Student and Parent accounts are both accessible on the same device. Student has active LA.
Lesson 1 is bookable (capacity ≥ 1).

| #   | Action                                                              | Expected Result                                                | Test Data       |
| --- | ------------------------------------------------------------------- | -------------------------------------------------------------- | --------------- |
| 1   | Login as Student → open Browse Lessons → Reserve Lesson 1 → Confirm | Booking Success Screen shown; Student Session created          | Student account |
| 2   | Switch account to Parent on the same device                         | Parent home screen shown                                       | Parent account  |
| 3   | Navigate to Lesson Booking menu area                                | Lesson Booking menu is NOT visible for Parent                  | —               |
| 4   | Verify in Salesforce: Student Session for (Student, Lesson 1)       | Session still exists with Booking_Flag=TRUE; student = Student | —               |

---

### [Nichibei] Lesson Booking – Multi-Account – Parent logged in then switches to Student – Student books lesson correctly

**Description:** AC 06.1 — BR-29: Session Isolation: When a parent is first logged in (with no booking access), then the account is switched to a student on the same device, the student must be able to book normally and the session must be attributed to the student, not the parent.

**Preconditions:**
Parent and Student accounts are both accessible on the same device. Student has active LA.
Lesson 2 is bookable (capacity ≥ 1).

| #   | Action                                                        | Expected Result                                                       | Test Data         |
| --- | ------------------------------------------------------------- | --------------------------------------------------------------------- | ----------------- |
| 1   | Login as Parent → navigate to home screen                     | Parent home screen shown; Lesson Booking menu NOT visible             | Parent account    |
| 2   | Switch account to Student on the same device                  | Student home screen shown                                             | Student account   |
| 3   | Open Browse Lessons → Reserve Lesson 2 → Confirm              | Booking Success Screen shown                                          | Student; Lesson 2 |
| 4   | Verify in Salesforce: Student Session for (Student, Lesson 2) | Session exists with Booking_Flag=TRUE; student = Student (not Parent) | —                 |
| 5   | Verify no Student Session created for Parent account          | No session linked to Parent for any lesson                            | —                 |

---

## Suite: Manual Assignment – Interaction

### [Nichibei] Lesson Booking – Manual Assignment – Staff assigns student via SF first – Student books same lesson via app – Duplicate blocked

**Description:** AC 03.3 — BR-16 / Lesson-Learned Risk #1: When a staff member has already manually assigned a student to a lesson via Salesforce (creating a Student Session with Booking_Flag=FALSE/blank), and the student then tries to book the same lesson via app, the duplicate allocation must be blocked.

**Preconditions:**
Lesson 1 is bookable (Bookable Flag=TRUE, capacity ≥ 1, within booking deadline).
Staff has already created a Student Session for Student A in Lesson 1 via Salesforce (Booking_Flag=FALSE).

| #   | Action                                                                             | Expected Result                                             | Test Data           |
| --- | ---------------------------------------------------------------------------------- | ----------------------------------------------------------- | ------------------- |
| 1   | Confirm Student Session (Student A, Lesson 1) exists in SF with Booking_Flag=FALSE | Session exists; manual assignment confirmed                 | Student A; Lesson 1 |
| 2   | Login as Student A in Learner App → open Browse Lessons                            | Lesson 1 is visible in browse list (Bookable Flag=TRUE)     | —                   |
| 3   | Tap Reserve on Lesson 1 → tap Confirm                                              | App returns error: duplicate allocation                     | —                   |
| 4   | Verify in Salesforce                                                               | No second Student Session created for (Student A, Lesson 1) | —                   |

---

### [Nichibei] Lesson Booking – Manual Assignment – Student books via app while staff simultaneously assigns same student via SF – Only one session created

**Description:** AC 03.3 — BR-16 / Lesson-Learned Risk #1 (Concurrency): Race condition test. Student submits booking via app at the same moment staff creates a Student Session for the same (student, lesson) pair in Salesforce. The read-lock must ensure only one session is committed; no duplicate.

**Preconditions:**
Lesson 1 is bookable. Student A has active LA. No existing session for (Student A, Lesson 1).

| #   | Action                                                                                | Expected Result                                                                                  | Test Data           |
| --- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ------------------- |
| 1   | Student A taps Reserve on Lesson 1 → taps Confirm in app                              | Booking request submitted                                                                        | Student A; Lesson 1 |
| 2   | Simultaneously, staff creates Student Session for (Student A, Lesson 1) in Salesforce | Concurrent write attempted                                                                       | Staff; Lesson 1     |
| 3   | Verify in Salesforce: count of Student Sessions for (Student A, Lesson 1)             | Exactly 1 Student Session exists; no duplicate created                                           | —                   |
| 4   | Verify whichever path succeeded (app or staff)                                        | Either app returns Booking Success OR staff save succeeds — not both; the other returns an error | —                   |

---

### [Nichibei] Lesson Booking – Manual Assignment – App-booked lesson deducts points same as manual staff assignment

**Description:** AC 03.2 — BR-31: Points calculation for a self-booked session must be equivalent to the existing manual staff assignment logic. No special override or bypass.

**Preconditions:**
Student A has a known point balance (e.g. 10 points). Lesson 1 costs 1 point per the existing point deduction logic.

| #   | Action                                                                               | Expected Result                                         | Test Data                       |
| --- | ------------------------------------------------------------------------------------ | ------------------------------------------------------- | ------------------------------- |
| 1   | Record Student A's point balance before booking                                      | Balance = 10 points                                     | Student A; initial balance = 10 |
| 2   | Login as Student A → Browse Lessons → Reserve Lesson 1 → Confirm                     | Booking Success Screen shown                            | Student A; Lesson 1             |
| 3   | Check point balance after booking in Salesforce                                      | Balance = 9 points (deducted 1 point)                   | Expected deduction = 1 point    |
| 4   | Compare with equivalent staff-manual assignment point deduction for same lesson type | Deduction amount is identical to manual assignment path | —                               |
