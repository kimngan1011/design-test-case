# Test Cases: LT-96620 — [Nichibei] Lesson Booking System

## Suite: Lesson Browse

### [Nichibei] Lesson Booking – Browse – No active LA – Empty state shown

**Description:** AC 02.1 — BR-2: Decision Table: When student has no active LA, Browse screen shows an empty state.

**Preconditions:**
Student user has no active Lesson Allocation

| #   | Action                                            | Expected Result                                      | Test Data |
| --- | ------------------------------------------------- | ---------------------------------------------------- | --------- |
| 1   | Login to app as student user                      | Home screen shown                                    | —         |
| 2   | Open "Lesson Booking" menu and tap Browse Lessons | Browse screen shown                                  | —         |
| 3   | View lesson list area                             | Empty state message shown; no lesson cards displayed | —         |

---

### [Nichibei] Lesson Booking – Lesson Visibility – All 4 conditions met – Lesson shown

**Description:** AC 02.2 — BR-4,5,6,7: Decision Table: A lesson meeting all 4 visibility conditions must appear in the Browse list.

**Preconditions:**
Student user has an active LA for Location A.
A lesson exists that:

- Location = Location A (linked to student's active LA)
- Bookable_Flag = TRUE
- Status = Published
- Lesson date = 2026-05-12 (above the 3-day advance booking threshold; threshold = today + 3 days = 2026-05-08)

| #   | Action                                               | Expected Result                               | Test Data |
| --- | ---------------------------------------------------- | --------------------------------------------- | --------- |
| 1   | Login to app as student user and open Browse Lessons | Browse screen with lessons shown              | —         |
| 2   | View the lesson in the list                          | Target lesson is displayed in the Browse list | —         |

---

### [Nichibei] Lesson Booking – Lesson Visibility – Location not linked to student's LA – Lesson hidden

**Description:** AC 02.2 — BR-4: Decision Table: A lesson at a location not linked to the student's active LA must NOT be visible.

**Preconditions:**
Student user has active LA for Location A only.
A lesson exists at Location B (not linked to student's LA). All other conditions (Bookable Flag=TRUE, Published, date = 2026-05-12) are met.

| #   | Action                                               | Expected Result                               | Test Data |
| --- | ---------------------------------------------------- | --------------------------------------------- | --------- |
| 1   | Login to app as student user and open Browse Lessons | Browse screen shown                           | —         |
| 2   | Search or scroll for the lesson at Location B        | Lesson at Location B is NOT shown in the list | —         |

---

### [Nichibei] Lesson Booking – Lesson Visibility – Bookable Flag OFF – Lesson hidden

**Description:** AC 02.2 — BR-5: Decision Table: A lesson with Bookable_Flag=FALSE must NOT appear in Browse list.

**Preconditions:**
Student user has active LA for Location A.
A lesson at Location A exists with Bookable_Flag=FALSE. All other conditions (Published, date = 2026-05-12) are met.

| #   | Action                                               | Expected Result                              | Test Data |
| --- | ---------------------------------------------------- | -------------------------------------------- | --------- |
| 1   | Login to app as student user and open Browse Lessons | Browse screen shown                          | —         |
| 2   | Scroll through the lesson list                       | Lesson with Bookable_Flag=FALSE is NOT shown | —         |

---

### [Nichibei] Lesson Booking – Lesson Visibility – Lesson status Cancelled – Lesson hidden

**Description:** AC 02.2 — BR-6: Decision Table: A lesson with status other than Draft or Published must NOT appear in Browse list.

**Preconditions:**
Student user has active LA for Location A.
A lesson at Location A exists with status = Cancelled. All other conditions (Bookable Flag=TRUE, date = 2026-05-12) are met.

| #   | Action                                               | Expected Result                              | Test Data |
| --- | ---------------------------------------------------- | -------------------------------------------- | --------- |
| 1   | Login to app as student user and open Browse Lessons | Browse screen shown                          | —         |
| 2   | Scroll through the lesson list                       | Cancelled lesson is NOT shown in Browse list | —         |

---

### [Nichibei] Lesson Booking – Lesson Visibility – Lesson status Draft – Lesson shown

**Description:** AC 02.2 — BR-6: Decision Table: A lesson with status = Draft AND Bookable_Flag=TRUE must appear in Browse list (Draft is valid for browsing).

**Preconditions:**
Student user has active LA for Location A.
A lesson at Location A exists with: Status=Draft, Bookable_Flag=TRUE, date = 2026-05-12 (above 3-day threshold).

| #   | Action                                               | Expected Result                                                | Test Data |
| --- | ---------------------------------------------------- | -------------------------------------------------------------- | --------- |
| 1   | Login to app as student user and open Browse Lessons | Browse screen shown                                            | —         |
| 2   | View lesson list                                     | Draft lesson with Bookable_Flag=TRUE is visible in Browse list | —         |

---

### [Nichibei] Lesson Booking – Lesson Visibility – Lesson date within minimum advance days – Lesson hidden

**Description:** AC 02.2 — BR-7: BVA: A lesson with date < 2026-05-08 (today + 3 days) must NOT appear in Browse list.

**Preconditions:**
Student user has active LA for Location A.
A lesson at Location A exists with: Bookable_Flag=TRUE, Published, lesson_date = 2026-05-07 (today + 2 days; 1 day below the 3-day threshold of 2026-05-08).

| #   | Action                                               | Expected Result                            | Test Data                |
| --- | ---------------------------------------------------- | ------------------------------------------ | ------------------------ |
| 1   | Login to app as student user and open Browse Lessons | Browse screen shown                        | —                        |
| 2   | Scroll through the lesson list                       | Lesson with date < 2026-05-08 is NOT shown | lesson_date = 2026-05-07 |

---

### [Nichibei] Lesson Booking – Lesson Visibility – Advance days threshold evaluated in lesson timezone – Device timezone behind

**Description:** AC 02.2 — BR-7 / BR-26: BVA (Timezone): The "today + 3 days" advance booking visibility threshold must be evaluated using the LESSON timezone (JST), not the student's device timezone (ICT). Near midnight JST, the device date (ICT) lags 1 day behind JST — the system must use JST to determine visibility.

**Preconditions:**
Lesson timezone = UTC+9 (JST). Student's device timezone = UTC+7 (ICT).
Current time = 2026-05-06 00:30 JST = 2026-05-05 22:30 ICT (device shows 2026-05-05).
Advance booking threshold = 3 days.
Lesson exists with lesson_date = 2026-05-08.
↳ JST (lesson TZ): min visible date = 2026-05-06 + 3 = 2026-05-09. lesson_date 2026-05-08 < 2026-05-09 → HIDDEN.
↳ ICT (device TZ): min visible date = 2026-05-05 + 3 = 2026-05-08. lesson_date 2026-05-08 >= 2026-05-08 → device WOULD show.

| #   | Action                                                                                              | Expected Result                                      | Test Data                                                                                       |
| --- | --------------------------------------------------------------------------------------------------- | ---------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| 1   | Login to app as student user (device = UTC+7 ICT, device date = 2026-05-05) and open Browse Lessons | Browse screen shown                                  | Device date = 2026-05-05 22:30 ICT; Lesson TZ = JST                                             |
| 2   | Look for the lesson with lesson_date = 2026-05-08                                                   | Lesson is NOT visible (hidden)                       | lesson_date = 2026-05-08; JST threshold = 2026-05-09 → below threshold                          |
| 3   | Confirm that ICT-based calculation would have shown the lesson                                      | System correctly uses lesson TZ (JST), not device TZ | ICT threshold = 2026-05-08; lesson_date = 2026-05-08 → device would show — but system must hide |

---

### [Nichibei] Lesson Booking – Location Filter – Only student's LA locations shown

**Description:** AC 02.3 — BR-8: Decision Table: The Location filter dropdown must only contain locations linked to the student's active LA.

**Preconditions:**
Student user has active LA for Location A only.
System has Location A and Location B available.

| #   | Action                                               | Expected Result                                                    | Test Data |
| --- | ---------------------------------------------------- | ------------------------------------------------------------------ | --------- |
| 1   | Login to app as student user and open Browse Lessons | Browse screen shown                                                | —         |
| 2   | Open the Location filter dropdown                    | Only Location A is shown in the dropdown; Location B is NOT listed | —         |

---

### [Nichibei] Lesson Booking – Filter – Schedule filter by date range restricts list

**Description:** AC 02.3 — Decision Table: Applying a date range on the Schedule filter shows only lessons within that range.

**Preconditions:**
Student user has active LA. Browse list shows multiple lessons on different dates.

| #   | Action                                                          | Expected Result                                                    | Test Data                            |
| --- | --------------------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------ |
| 1   | Open Browse Lessons screen                                      | Multiple lesson cards visible across multiple dates                | —                                    |
| 2   | Apply Schedule filter with date range: 2026-06-01 to 2026-06-07 | Only lessons with date between 2026-06-01 and 2026-06-07 are shown | Date range: 2026-06-01 to 2026-06-07 |
| 3   | Clear the date range filter                                     | All lessons (within visibility rules) are shown again              | —                                    |

---

### [Nichibei] Lesson Booking – Filter – Day of Week filter restricts list

**Description:** AC 02.3 — Decision Table: Applying a day-of-week filter shows only lessons on the selected days.

**Preconditions:**
Student user has active LA. Browse list shows lessons on multiple days of the week.

| #   | Action                                    | Expected Result                          | Test Data    |
| --- | ----------------------------------------- | ---------------------------------------- | ------------ |
| 1   | Open Browse Lessons screen                | Lessons on multiple days of week visible | —            |
| 2   | Apply Schedule filter: select Monday only | Only Monday lessons are shown            | Day = Monday |
| 3   | Clear filter                              | All lessons shown again                  | —            |

---

### [Nichibei] Lesson Booking – Filter – Bookable Only toggle shows only bookable lessons

**Description:** AC 02.3 — Decision Table: Enabling "Bookable Only" toggle shows only lessons that are bookable (not full, within deadline, not already booked).

**Preconditions:**
Student user has active LA. Browse list contains: 1 lesson already full, 1 lesson already booked by student, 1 available bookable lesson.

| #   | Action                         | Expected Result                                                                             | Test Data |
| --- | ------------------------------ | ------------------------------------------------------------------------------------------- | --------- |
| 1   | Open Browse Lessons screen     | All visible lessons shown (full + booked + available)                                       | —         |
| 2   | Enable "Bookable Only" toggle  | Only the available (reservable) lesson is shown; full and already-booked lessons are hidden | —         |
| 3   | Disable "Bookable Only" toggle | All lessons shown again                                                                     | —         |

---

### [Nichibei] Lesson Booking – Filter – Subject filter restricts list

**Description:** AC 02.3 — Decision Table: Applying a Subject filter shows only lessons with the selected subject.

**Preconditions:**
Student user has active LA. Browse list contains lessons for Subject A and Subject B.

| #   | Action                             | Expected Result                             | Test Data |
| --- | ---------------------------------- | ------------------------------------------- | --------- |
| 1   | Open Browse Lessons screen         | Lessons for Subject A and Subject B visible | —         |
| 2   | Select Subject A in Subject filter | Only Subject A lessons are shown            | Subject A |
| 3   | Clear filter                       | All lessons shown again                     | —         |

---

### [Nichibei] Lesson Booking – Filter – Teacher filter restricts list

**Description:** AC 02.3 — Decision Table: Applying a Teacher filter shows only lessons assigned to the selected teacher.

**Preconditions:**
Student user has active LA. Browse list contains lessons assigned to Teacher 1 and Teacher 2.

| #   | Action                             | Expected Result                             | Test Data |
| --- | ---------------------------------- | ------------------------------------------- | --------- |
| 1   | Open Browse Lessons screen         | Lessons for Teacher 1 and Teacher 2 visible | —         |
| 2   | Select Teacher 1 in Teacher filter | Only Teacher 1's lessons shown              | Teacher 1 |
| 3   | Clear filter                       | All lessons shown again                     | —         |

---

### [Nichibei] Lesson Booking – Filter – Lesson Name search restricts list

**Description:** AC 02.3 — Decision Table: Entering a keyword in Lesson Name search shows only matching lessons.

**Preconditions:**
Student user has active LA. Browse list contains "Math Lesson A" and "English Lesson B".

| #   | Action                                   | Expected Result                                     | Test Data        |
| --- | ---------------------------------------- | --------------------------------------------------- | ---------------- |
| 1   | Open Browse Lessons screen               | Both "Math Lesson A" and "English Lesson B" visible | —                |
| 2   | Enter "Math" in Lesson Name search field | Only "Math Lesson A" shown                          | keyword = "Math" |
| 3   | Clear search field                       | Both lessons shown again                            | —                |

---

### [Nichibei] Lesson Booking – Lesson Card Button – Available lesson – Reserve button enabled

**Description:** AC 02.4 — BR-9: Decision Table: Reserve button is enabled when: student not allocated + Bookable_Flag=TRUE + not full + within booking deadline.

**Preconditions:**
Student user has active LA. A bookable lesson exists: not full, within booking deadline, student not yet booked.

| #   | Action                                    | Expected Result                       | Test Data |
| --- | ----------------------------------------- | ------------------------------------- | --------- |
| 1   | Open Browse Lessons screen                | Lesson card visible                   | —         |
| 2   | View the action button on the lesson card | "Reserve" button is shown and enabled | —         |

---

### [Nichibei] Lesson Booking – Lesson Card Button – Lesson full – Reserve button disabled

**Description:** AC 02.4 — BR-10: Decision Table: Reserve button is disabled when lesson has reached maximum capacity.

**Preconditions:**
A bookable lesson exists at student's LA location. Current session count = lesson capacity (lesson is full). Student has not booked this lesson.

| #   | Action                                    | Expected Result                           | Test Data                   |
| --- | ----------------------------------------- | ----------------------------------------- | --------------------------- |
| 1   | Open Browse Lessons screen                | Lesson card visible                       | —                           |
| 2   | View the action button on the lesson card | "Reserve" button is disabled (greyed out) | capacity = current sessions |

---

### [Nichibei] Lesson Booking – Lesson Card Button – Past booking deadline – Reserve button disabled

**Description:** AC 02.4 — BR-10: BVA: Reserve button is disabled when current time is past the booking deadline.

**Preconditions:**
A bookable lesson exists. Current time > (lesson start − booking deadline hours). Student has not booked this lesson.

| #   | Action                                    | Expected Result                                                                       | Test Data |
| --- | ----------------------------------------- | ------------------------------------------------------------------------------------- | --------- |
| 1   | Open Browse Lessons screen                | Lesson card visible                                                                   | —         |
| 2   | View the action button on the lesson card | "Reserve" button is disabled (greyed out) with tooltip explaining deadline has passed | —         |

---

### [Nichibei] Lesson Booking – Lesson Card Button – Staff-allocated lesson – No action button shown

**Description:** AC 02.4 — BR-11: Decision Table: No Reserve or Cancel button is shown for a staff-allocated lesson (Booking_Flag=OFF or blank).

**Preconditions:**
Student user has a staff-allocated lesson (Booking_Flag=FALSE) visible in Browse Lessons.

| #   | Action                                                         | Expected Result                                  | Test Data |
| --- | -------------------------------------------------------------- | ------------------------------------------------ | --------- |
| 1   | Open Browse Lessons screen                                     | Lesson card for staff-allocated lesson visible   | —         |
| 2   | View the action button area on the staff-allocated lesson card | No Reserve button and no Cancel button are shown | —         |

---

### [Nichibei] Lesson Booking – Lesson Card Button – Already booked lesson within deadline – Cancel button enabled

**Description:** AC 02.4 — BR-9: State Transition: Cancel button shown and enabled for a lesson the student has already booked, within the cancellation deadline.

**Preconditions:**
Student user has already booked a lesson. Current time < (lesson start − 2 hours).
Lesson start = 14:00 JST; cancellation deadline = 12:00 JST (2 hours before start); current = 09:00 JST.

| #   | Action                                                   | Expected Result                      | Test Data |
| --- | -------------------------------------------------------- | ------------------------------------ | --------- |
| 1   | Open Browse Lessons screen                               | Lesson card visible                  | —         |
| 2   | View the action button on the already-booked lesson card | "Cancel" button is shown and enabled | —         |

---

### [Nichibei] Lesson Booking – Lesson Card Button – Already booked lesson past deadline – Cancel button disabled

**Description:** AC 02.4 — BR-10/BR-22: BVA: Cancel button shown but disabled for an already-booked lesson when the cancellation deadline has passed.

**Preconditions:**
Student user has already booked a lesson. Current time > (lesson start − 2 hours).
Lesson start = 11:00 JST; cancellation deadline = 09:00 JST (2 hours before start); current = 10:00 JST.

| #   | Action                                                   | Expected Result                                                          | Test Data |
| --- | -------------------------------------------------------- | ------------------------------------------------------------------------ | --------- |
| 1   | Open Browse Lessons screen                               | Lesson card visible                                                      | —         |
| 2   | View the action button on the already-booked lesson card | "Cancel" button is shown but disabled with tooltip                       | —         |
| 3   | Tap the disabled Cancel button                           | Tooltip shown: "Cancellation not available within 2 hours of start time" | —         |
