# Test Cases: LT-96620 — [Nichibei] Lesson Booking System

## Suite: Lesson Lists

### [Nichibei] Lesson Booking – Lesson Lists – No active LA – Empty state shown

**Description:** AC 02.1 — BR-2: Decision Table: When student has no active LA, Lesson Lists screen shows an empty state.

**Preconditions:**
Student user has no active Lesson Allocation

| #   | Action                                            | Expected Result                                      | Test Data |
| --- | ------------------------------------------------- | ---------------------------------------------------- | --------- |
| 1   | Login to app as student user                      | Home screen shown                                    | —         |
| 2   | Open "Reservation List" menu and tap Lesson Lists | Lesson Lists screen shown                            | —         |
| 3   | View lesson list area                             | Empty state message shown; no lesson cards displayed | —         |

---

### [Nichibei] Lesson Booking – Lesson Visibility – All 4 conditions met – Lesson shown

**Description:** AC 02.2 — BR-4,5,6,7: Decision Table: A lesson meeting all 4 visibility conditions must appear in Lesson Lists.

**Preconditions:**
Student user has an active LA for Location A.
A lesson exists that:

- Location = Location A (linked to student's active LA)
- Bookable_Flag = TRUE
- Status = Published
- Lesson date = 2026-05-26 (above the 3-day advance booking threshold; threshold = today + 3 days = 2026-05-22)

| #   | Action                                             | Expected Result                            | Test Data                                                                      |
| --- | -------------------------------------------------- | ------------------------------------------ | ------------------------------------------------------------------------------ |
| 1   | Login to app as student user and open Lesson Lists | Lesson Lists screen with lessons shown     | today = 2026-05-19; lesson_date = 2026-05-26                                   |
| 2   | View the lesson in the list                        | Target lesson is displayed in Lesson Lists | threshold = 2026-05-22 (today+3); lesson_date 2026-05-26 ≥ threshold → visible |

---

### [Nichibei] Lesson Booking – Lesson Visibility – Location not linked to student's LA – Lesson hidden

**Description:** AC 02.2 — BR-4: Decision Table: A lesson at a location not linked to the student's active LA must NOT be visible.

**Preconditions:**
Student user has active LA for Location A only.
A lesson exists at Location B (not linked to student's LA). All other conditions (Bookable Flag=TRUE, Published, date = 2026-05-26) are met.

| #   | Action                                             | Expected Result                               | Test Data                                    |
| --- | -------------------------------------------------- | --------------------------------------------- | -------------------------------------------- |
| 1   | Login to app as student user and open Lesson Lists | Lesson Lists screen shown                     | today = 2026-05-19; lesson_date = 2026-05-26 |
| 2   | Search or scroll for the lesson at Location B      | Lesson at Location B is NOT shown in the list | Location B ≠ student LA location → hidden    |

---

### [Nichibei] Lesson Booking – Lesson Visibility – Bookable Flag OFF – Lesson hidden

**Description:** AC 02.2 — BR-5: Decision Table: A lesson with Bookable_Flag=FALSE must NOT appear in Lesson Lists.

**Preconditions:**
Student user has active LA for Location A.
A lesson at Location A exists with Bookable_Flag=FALSE. All other conditions (Published, date = 2026-05-26) are met.

| #   | Action                                             | Expected Result                              | Test Data                                    |
| --- | -------------------------------------------------- | -------------------------------------------- | -------------------------------------------- |
| 1   | Login to app as student user and open Lesson Lists | Lesson Lists screen shown                    | today = 2026-05-19; lesson_date = 2026-05-26 |
| 2   | Scroll through the lesson list                     | Lesson with Bookable_Flag=FALSE is NOT shown | Bookable_Flag = FALSE → hidden               |

---

### [Nichibei] Lesson Booking – Lesson Visibility – Lesson status Cancelled – Lesson hidden

**Description:** AC 02.2 — BR-6: Decision Table: A lesson with status other than Draft or Published must NOT appear in Lesson Lists.

**Preconditions:**
Student user has active LA for Location A.
A lesson at Location A exists with status = Cancelled. All other conditions (Bookable Flag=TRUE, date = 2026-05-26) are met.

| #   | Action                                             | Expected Result                               | Test Data                                    |
| --- | -------------------------------------------------- | --------------------------------------------- | -------------------------------------------- |
| 1   | Login to app as student user and open Lesson Lists | Lesson Lists screen shown                     | today = 2026-05-19; lesson_date = 2026-05-26 |
| 2   | Scroll through the lesson list                     | Cancelled lesson is NOT shown in Lesson Lists | status = Cancelled → hidden                  |

---

### [Nichibei] Lesson Booking – Lesson Visibility – Lesson status Draft – Lesson shown

**Description:** AC 02.2 — BR-6: Decision Table: A lesson with status = Draft AND Bookable_Flag=TRUE must appear in Lesson Lists (Draft is valid for browsing).

**Preconditions:**
Student user has active LA for Location A.
A lesson at Location A exists with: Status=Draft, Bookable_Flag=TRUE, date = 2026-05-26 (above 3-day threshold).

| #   | Action                                             | Expected Result                                                 | Test Data                                      |
| --- | -------------------------------------------------- | --------------------------------------------------------------- | ---------------------------------------------- |
| 1   | Login to app as student user and open Lesson Lists | Lesson Lists screen shown                                       | today = 2026-05-19; lesson_date = 2026-05-26   |
| 2   | View lesson list                                   | Draft lesson with Bookable_Flag=TRUE is visible in Lesson Lists | status = Draft; Bookable_Flag = TRUE → visible |

---

### [Nichibei] Lesson Booking – Lesson Visibility – Lesson date within minimum advance days – Lesson hidden

**Description:** AC 02.2 — BR-7: BVA: A lesson with date < 2026-05-22 (today + 3 days) must NOT appear in Lesson Lists.

**Preconditions:**
Student user has active LA for Location A.
A lesson at Location A exists with: Bookable_Flag=TRUE, Published, lesson_date = 2026-05-21 (today + 2 days; 1 day below the 3-day threshold of 2026-05-22).

| #   | Action                                             | Expected Result                            | Test Data                                                                     |
| --- | -------------------------------------------------- | ------------------------------------------ | ----------------------------------------------------------------------------- |
| 1   | Login to app as student user and open Lesson Lists | Lesson Lists screen shown                  | today = 2026-05-19; lesson_date = 2026-05-21                                  |
| 2   | Scroll through the lesson list                     | Lesson with date < 2026-05-22 is NOT shown | threshold = 2026-05-22 (today+3); lesson_date 2026-05-21 < threshold → hidden |

---

### [Nichibei] Lesson Booking – Lesson Visibility – Advance days threshold evaluated in lesson timezone – Device timezone behind

**Description:** AC 02.2 — BR-7 / BR-26: BVA (Timezone): The "today + 3 days" advance booking visibility threshold must be evaluated using the LESSON timezone (JST), not the student's device timezone (ICT). Near midnight JST, the device date (ICT) lags 1 day behind JST — the system must use JST to determine visibility.

**Preconditions:**
Lesson timezone = UTC+9 (JST). Student's device timezone = UTC+7 (ICT).
Current time = 2026-05-20 00:30 JST = 2026-05-19 22:30 ICT (device shows 2026-05-19).
Advance booking threshold = 3 days.
Lesson exists with lesson_date = 2026-05-22.
↳ JST (lesson TZ): min visible date = 2026-05-20 + 3 = 2026-05-23. lesson_date 2026-05-22 < 2026-05-23 → HIDDEN.
↳ ICT (device TZ): min visible date = 2026-05-19 + 3 = 2026-05-22. lesson_date 2026-05-22 >= 2026-05-22 → device WOULD show.

| #   | Action                                                                                            | Expected Result                                      | Test Data                                                                                         |
| --- | ------------------------------------------------------------------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| 1   | Login to app as student user (device = UTC+7 ICT, device date = 2026-05-19) and open Lesson Lists | Lesson Lists screen shown                            | today (JST/server) = 2026-05-20; today (ICT/device) = 2026-05-19; lesson_date = 2026-05-22; X = 3 |
| 2   | Look for the lesson with lesson_date = 2026-05-22                                                 | Lesson is NOT visible (hidden)                       | threshold (JST) = 2026-05-23 (today+3); lesson_date 2026-05-22 < threshold → hidden               |
| 3   | Confirm that ICT-based calculation would have shown the lesson                                    | System correctly uses lesson TZ (JST), not device TZ | threshold (ICT) = 2026-05-22 (today+3); lesson_date 2026-05-22 = threshold → device would show    |

---

### [Nichibei] Lesson Booking – Location Filter – Only student's LA locations shown

**Description:** AC 02.3 — BR-8: Decision Table: The Location filter dropdown must only contain locations linked to the student's active LA.

**Preconditions:**
Student user has active LA for Location A only.
System has Location A and Location B available.

| #   | Action                                             | Expected Result                                                    | Test Data |
| --- | -------------------------------------------------- | ------------------------------------------------------------------ | --------- |
| 1   | Login to app as student user and open Lesson Lists | Lesson Lists screen shown                                          | —         |
| 2   | Open the Location filter dropdown                  | Only Location A is shown in the dropdown; Location B is NOT listed | —         |

---

### [Nichibei] Lesson Booking – Filter – Schedule filter by date range restricts list

**Description:** AC 02.3 — Decision Table: Applying a date range on the Schedule filter shows only lessons within that range.

**Preconditions:**
Student user has active LA. Lesson Lists shows multiple lessons on different dates.

| #   | Action                                                          | Expected Result                                                    | Test Data                            |
| --- | --------------------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------ |
| 1   | Open Lesson Lists screen                                        | Multiple lesson cards visible across multiple dates                | —                                    |
| 2   | Apply Schedule filter with date range: 2026-06-01 to 2026-06-07 | Only lessons with date between 2026-06-01 and 2026-06-07 are shown | Date range: 2026-06-01 to 2026-06-07 |
| 3   | Clear the date range filter                                     | All lessons (within visibility rules) are shown again              | —                                    |

---

### [Nichibei] Lesson Booking – Filter – Day of Week filter restricts list

**Description:** AC 02.3 — Decision Table: Applying a day-of-week filter shows only lessons on the selected days.

**Preconditions:**
Student user has active LA. Lesson Lists shows lessons on multiple days of the week.

| #   | Action                                    | Expected Result                          | Test Data    |
| --- | ----------------------------------------- | ---------------------------------------- | ------------ |
| 1   | Open Lesson Lists screen                  | Lessons on multiple days of week visible | —            |
| 2   | Apply Schedule filter: select Monday only | Only Monday lessons are shown            | Day = Monday |
| 3   | Clear filter                              | All lessons shown again                  | —            |

---

### [Nichibei] Lesson Booking – Filter – available lessons only toggle shows only bookable lessons

**Description:** AC 02.3 — Decision Table: Enabling "available lessons only" toggle shows only lessons that are bookable (not full, within deadline, not already booked).

**Preconditions:**
Student user has active LA. Lesson Lists contains: 1 lesson already full, 1 lesson already booked by student, 1 available bookable lesson.

| #   | Action                                  | Expected Result                                                                             | Test Data |
| --- | --------------------------------------- | ------------------------------------------------------------------------------------------- | --------- |
| 1   | Open Lesson Lists screen                | All visible lessons shown (full + booked + available)                                       | —         |
| 2   | Enable "available lessons only" toggle  | Only the available (reservable) lesson is shown; full and already-booked lessons are hidden | —         |
| 3   | Disable "available lessons only" toggle | All lessons shown again                                                                     | —         |

---

### [Nichibei] Lesson Booking – Filter – Subject filter restricts list

**Description:** AC 02.3 — Decision Table: Applying a Subject filter shows only lessons with the selected subject.

**Preconditions:**
Student user has active LA. Lesson Lists contains lessons for Subject A and Subject B.

| #   | Action                             | Expected Result                             | Test Data |
| --- | ---------------------------------- | ------------------------------------------- | --------- |
| 1   | Open Lesson Lists screen           | Lessons for Subject A and Subject B visible | —         |
| 2   | Select Subject A in Subject filter | Only Subject A lessons are shown            | Subject A |
| 3   | Clear filter                       | All lessons shown again                     | —         |

---

### [Nichibei] Lesson Booking – Filter – Teacher filter restricts list

**Description:** AC 02.3 — Decision Table: Applying a Teacher filter shows only lessons assigned to the selected teacher.

**Preconditions:**
Student user has active LA. Lesson Lists contains lessons assigned to Teacher 1 and Teacher 2.

| #   | Action                             | Expected Result                             | Test Data |
| --- | ---------------------------------- | ------------------------------------------- | --------- |
| 1   | Open Lesson Lists screen           | Lessons for Teacher 1 and Teacher 2 visible | —         |
| 2   | Select Teacher 1 in Teacher filter | Only Teacher 1's lessons shown              | Teacher 1 |
| 3   | Clear filter                       | All lessons shown again                     | —         |

---

### [Nichibei] Lesson Booking – Filter – Lesson Name search restricts list

**Description:** AC 02.3 — Decision Table: Entering a keyword in Lesson Name search shows only matching lessons.

**Preconditions:**
Student user has active LA. Lesson Lists contains "Math Lesson A" and "English Lesson B".

| #   | Action                                   | Expected Result                                     | Test Data        |
| --- | ---------------------------------------- | --------------------------------------------------- | ---------------- |
| 1   | Open Lesson Lists screen                 | Both "Math Lesson A" and "English Lesson B" visible | —                |
| 2   | Enter "Math" in Lesson Name search field | Only "Math Lesson A" shown                          | keyword = "Math" |
| 3   | Clear search field                       | Both lessons shown again                            | —                |

---

### [Nichibei] Lesson Booking – Lesson Lists Card – Fields – Lesson Lists card displays all required fields

**Description:** AC 02.4 — Display Testing: Each lesson card in Lesson Lists must display the core information fields a student needs to identify and decide whether to book: lesson name, date, start+end time, center (location), and teacher name.

**Preconditions:**
Student has active LA for Location A. At least 1 bookable Published lesson is visible in Lesson Lists with known data:
lesson name = "Math Lesson", lesson_date = 2026-05-25, start = 10:00 JST, end = 11:00 JST, center = "Center A", teacher = "Teacher A".

| #   | Action                                    | Expected Result                         | Test Data                                                                                    |
| --- | ----------------------------------------- | --------------------------------------- | -------------------------------------------------------------------------------------------- |
| 1   | Open Lesson Lists screen                  | Lesson card for "Math Lesson" visible   | lesson_date = 2026-05-25; start = 10:00; end = 11:00; center = Center A; teacher = Teacher A |
| 2   | Observe lesson name on the card           | "Math Lesson" is displayed              | —                                                                                            |
| 3   | Observe date on the card                  | Date "2026-05-25" is displayed          | —                                                                                            |
| 4   | Observe start and end time on the card    | "10:00" and "11:00" (JST) are displayed | —                                                                                            |
| 5   | Observe center/location field on the card | "Center A" is displayed                 | —                                                                                            |
| 6   | Observe teacher name on the card          | "Teacher A" is displayed                | —                                                                                            |

---

### [Nichibei] Lesson Booking – Lesson Card – Sort Order – Start time ASC, group lessons before individual at same time

**Description:** AC 02.4 — Sorting: Lesson cards in Lesson Lists are sorted by start time ascending. When two lessons share the same start time, group lessons appear before individual lessons. Lesson ID ASC is the final tiebreaker within the same time and type.

**Preconditions:**
Student has active LA. 3 bookable Published lessons visible:

- Lesson A: group lesson, start = 09:00 JST
- Lesson B: individual lesson, start = 09:00 JST (same time as A, individual)
- Lesson C: any type, start = 10:00 JST

| #   | Action                                                                                 | Expected Result                                                                     | Test Data                                  |
| --- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------ |
| 1   | Open Lesson Lists screen                                                               | All 3 lesson cards visible                                                          | A=09:00 group; B=09:00 individual; C=10:00 |
| 2   | Observe position of Lesson C (10:00) vs A and B (09:00)                                | Lessons A and B (09:00) appear before Lesson C (10:00) — earlier start time first   | —                                          |
| 3   | Observe position of Lesson A (group) vs Lesson B (individual) at same 09:00 start time | Lesson A (group) appears before Lesson B (individual) — group > individual ordering | —                                          |

---

### [Nichibei] Lesson Booking – Lesson Card Button – Available lesson – Reserve button enabled

**Description:** AC 02.4 — BR-9: Decision Table: Reserve button is enabled when: student not allocated + Bookable_Flag=TRUE + not full + within booking deadline.

**Preconditions:**
Student user has active LA. A bookable lesson exists: not full, within booking deadline, student not yet booked.

| #   | Action                                    | Expected Result                       | Test Data |
| --- | ----------------------------------------- | ------------------------------------- | --------- |
| 1   | Open Lesson Lists screen                  | Lesson card visible                   | —         |
| 2   | View the action button on the lesson card | "Reserve" button is shown and enabled | —         |

---

### [Nichibei] Lesson Booking – Lesson Card Button – Lesson full – Reserve button disabled with tooltip

**Description:** AC 02.4 — BR-10: Decision Table: Reserve button is disabled with tooltip when lesson has reached maximum capacity (session count = capacity).

**Preconditions:**
A bookable lesson exists at student's LA location. Session count = capacity (lesson is full). Student has not booked this lesson.

| #   | Action                                    | Expected Result                                     | Test Data                                 |
| --- | ----------------------------------------- | --------------------------------------------------- | ----------------------------------------- |
| 1   | Open Lesson Lists screen                  | Lesson card visible                                 | capacity = 1; current_sessions = 1 (full) |
| 2   | View the action button on the lesson card | "Reserve" button is disabled (greyed out)           | —                                         |
| 3   | Tap or hover the disabled Reserve button  | Tooltip shown indicating lesson is at full capacity | —                                         |

---

### [Nichibei] Lesson Booking – Lesson Card Button – Past booking deadline – Reserve button disabled with tooltip

**Description:** AC 02.4 — BR-10: BVA: Reserve button is disabled with tooltip when current time is past the booking deadline (current_time > lesson_start − booking_deadline_hours).

**Preconditions:**
A bookable lesson exists. Current time is past the booking deadline (current_time > lesson_start − booking_deadline_hours).
today = 2026-05-20; lesson_date = 2026-05-20; lesson_start = 10:00 JST; booking_deadline = 08:00 JST (= lesson_start − 2h); current_time = 09:00 JST.
Student has not booked this lesson.

| #   | Action                                    | Expected Result                                                   | Test Data                                                                                                                             |
| --- | ----------------------------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Open Lesson Lists screen                  | Lesson card visible                                               | today = 2026-05-20; lesson_date = 2026-05-20; lesson_start = 10:00 JST; booking_deadline = 08:00 JST; current_time = 09:00 JST (past) |
| 2   | View the action button on the lesson card | "Reserve" button is disabled (greyed out)                         | —                                                                                                                                     |
| 3   | Tap or hover the disabled Reserve button  | Tooltip shown: "The booking deadline has passed for this lesson." | —                                                                                                                                     |

---

### [Nichibei] Lesson Booking – Lesson Card Button – Staff-allocated lesson – No action button shown

**Description:** AC 02.4 — BR-11: Decision Table: No Reserve or Cancel button is shown for a staff-allocated lesson (Booking_Flag=OFF or blank).

**Preconditions:**
Student user has a staff-allocated lesson (Booking_Flag=FALSE) visible in Lesson Lists.

| #   | Action                                                         | Expected Result                                  | Test Data |
| --- | -------------------------------------------------------------- | ------------------------------------------------ | --------- |
| 1   | Open Lesson Lists screen                                       | Lesson card for staff-allocated lesson visible   | —         |
| 2   | View the action button area on the staff-allocated lesson card | No Reserve button and no Cancel button are shown | —         |

---

### [Nichibei] Lesson Booking – Lesson Card Button – Already booked lesson within deadline – Cancel button enabled

**Description:** AC 02.4 — BR-9: State Transition: Cancel button shown and enabled for a lesson the student has already booked, within the cancellation deadline.

**Preconditions:**
Partner config: cancellation deadline X = 2 hours.
Lesson date = 2026-05-22; Lesson start = 2026-05-22 14:00 JST; deadline = 2026-05-22 12:00 JST (14:00 − 2h).
Current datetime = 2026-05-22 09:00 JST → 2026-05-22 09:00 ≤ 2026-05-22 12:00 → within deadline.

| #   | Action                                                   | Expected Result                      | Test Data |
| --- | -------------------------------------------------------- | ------------------------------------ | --------- |
| 1   | Open Lesson Lists screen                                 | Lesson card visible                  | —         |
| 2   | View the action button on the already-booked lesson card | "Cancel" button is shown and enabled | —         |

---

### [Nichibei] Lesson Booking – Lesson Card Button – Already booked lesson past cancellation deadline – Cancel button disabled

**Description:** AC 02.4 — BR-10/BR-22: BVA: Cancel button shown but disabled for an already-booked lesson when current time is past the cancellation deadline (current > lesson start − X hours, BR-22). X is the partner-configured cancellation deadline setting. This is independent of the booking deadline.

**Preconditions:**
Partner config: cancellation deadline X = 2 hours.
today = 2026-05-20; lesson_date = 2026-05-20; Lesson start = 2026-05-20 11:00 JST; deadline = 2026-05-20 09:00 JST (11:00 − 2h).
Current datetime = 2026-05-20 10:00 JST → 2026-05-20 10:00 > 2026-05-20 09:00 → past deadline.

| #   | Action                                                   | Expected Result                                                          | Test Data                                                                                                                                                                            |
| --- | -------------------------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | Open Lesson Lists screen                                 | Lesson card visible                                                      | today = 2026-05-20; lesson_date = 2026-05-20; lesson_start = 2026-05-20 11:00 JST; deadline = 2026-05-20 09:00 JST; current_time = 2026-05-20 10:00 JST → past cancellation deadline |
| 2   | View the action button on the already-booked lesson card | "Cancel" button is shown but disabled with tooltip                       | —                                                                                                                                                                                    |
| 3   | Tap the disabled Cancel button                           | Tooltip shown: "Cancellation not available within 2 hours of start time" | —                                                                                                                                                                                    |

---

## Suite: Advance Days Threshold – BVA (X=1)

### [Nichibei] Lesson Booking – Advance Days BVA – Lesson date = today – Lesson hidden (X=1)

**Description:** AC 02.2 — BR-7: BVA (lower bound violation): When partner setting X=1, a lesson scheduled for today (2026-05-19) must NOT appear in Lesson Lists, because "at least 1 day in the future" means lesson_date must be strictly > today.

**Preconditions:**
Partner config: advance days X = 1. Today = 2026-05-19.
Student has active LA for Location A.
Lesson at Location A: Bookable_Flag=TRUE, status=Published, lesson_date=2026-05-19 (today). All other visibility conditions met.

| #   | Action                                                 | Expected Result                                                                       | Test Data                                                                     |
| --- | ------------------------------------------------------ | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| 1   | Login to app as student user and open Lesson Lists     | Lesson Lists screen shown                                                             | today = 2026-05-19; lesson_date = 2026-05-19; X = 1                           |
| 2   | Scroll through the lesson list for today's date        | Lesson with lesson_date=2026-05-19 is NOT shown (today does not satisfy today+1 rule) | threshold = 2026-05-20 (today+1); lesson_date 2026-05-19 < threshold → hidden |
| 3   | Confirm no lesson card with date 2026-05-19 is visible | Zero lesson cards for 2026-05-19 displayed                                            | —                                                                             |

---

### [Nichibei] Lesson Booking – Advance Days BVA – Lesson date = today+1 – Lesson visible (X=1, exact boundary)

**Description:** AC 02.2 — BR-7: BVA (exact lower bound): When partner setting X=1, a lesson scheduled for 2026-05-20 (today+1) is the minimum valid date and must appear in Lesson Lists.

**Preconditions:**
Partner config: advance days X = 1. Today = 2026-05-19.
Student has active LA for Location A.
Lesson at Location A: Bookable_Flag=TRUE, status=Published, lesson_date=2026-05-20 (today+1). All other visibility conditions met.

| #   | Action                                             | Expected Result                                                            | Test Data                                                                      |
| --- | -------------------------------------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| 1   | Login to app as student user and open Lesson Lists | Lesson Lists screen shown                                                  | today = 2026-05-19; lesson_date = 2026-05-20; X = 1                            |
| 2   | View the lesson list                               | Lesson with lesson_date=2026-05-20 IS displayed (exact boundary satisfied) | threshold = 2026-05-20 (today+1); lesson_date 2026-05-20 = threshold → visible |
| 3   | Confirm the Reserve button is shown on the card    | Reserve button is enabled (or disabled only if capacity/deadline reason)   | —                                                                              |

---

### [Nichibei] Lesson Booking – Advance Days BVA – Lesson date = yesterday – Lesson hidden (past date)

**Description:** AC 02.2 — BR-7: BVA (past date): A lesson scheduled for 2026-05-18 (yesterday) must NOT appear in Lesson Lists regardless of X value. Past lessons are never bookable.

**Preconditions:**
Partner config: advance days X = 1. Today = 2026-05-19.
Student has active LA for Location A.
Lesson at Location A: Bookable_Flag=TRUE, status=Published, lesson_date=2026-05-18 (yesterday). All other visibility conditions met.

| #   | Action                                              | Expected Result                                                     | Test Data                                           |
| --- | --------------------------------------------------- | ------------------------------------------------------------------- | --------------------------------------------------- |
| 1   | Login to app as student user and open Lesson Lists  | Lesson Lists screen shown                                           | today = 2026-05-19; lesson_date = 2026-05-18; X = 1 |
| 2   | Scroll through the lesson list                      | Lesson with lesson_date=2026-05-18 is NOT shown (past date, hidden) | lesson_date 2026-05-18 < today → past date → hidden |
| 3   | Confirm no lesson card with date 2026-05-18 visible | Zero lesson cards for 2026-05-18 displayed                          | —                                                   |

---

## Suite: Advance Days Threshold – Config Change

### [Nichibei] Lesson Booking – Advance Days Config – X decreased (3→1) – Previously hidden lessons become visible

**Description:** AC 02.2 — BR-7 / Config: When admin decreases advance days X from 3 to 1, lessons that were hidden (date was between today+1 and today+2) must immediately become visible after refresh.

**Preconditions:**
Partner config: advance days X = 3. Today = 2026-05-19.
Lesson A: lesson_date=2026-05-20 (today+1) — currently hidden (threshold = today+3 = 2026-05-22).
Lesson B: lesson_date=2026-05-22 (today+3) — currently visible.
Both lessons: Bookable_Flag=TRUE, Published, at student's LA location.

| #   | Action                                                    | Expected Result                                                           | Test Data                                                                                                                         |
| --- | --------------------------------------------------------- | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Open Lesson Lists with X=3 config                         | Lesson A (2026-05-20) is NOT visible; Lesson B (2026-05-22) IS visible    | today = 2026-05-19; Lesson A lesson_date = 2026-05-20; Lesson B lesson_date = 2026-05-22; X = 3; threshold = 2026-05-22 (today+3) |
| 2   | Admin updates partner advance days config from X=3 to X=1 | Config updated successfully                                               | X changed: 3 → 1; new threshold = today+1 = 2026-05-20                                                                            |
| 3   | Student refreshes Lesson Lists                            | Lesson A (2026-05-20) now IS visible (2026-05-20 >= today+1 = 2026-05-20) | —                                                                                                                                 |
| 4   | Confirm Lesson B still visible                            | Lesson B (2026-05-22) still visible                                       | —                                                                                                                                 |

---

### [Nichibei] Lesson Booking – Advance Days Config – X increased (1→3) – Previously visible lessons become hidden

**Description:** AC 02.2 — BR-7 / Config: When admin increases advance days X from 1 to 3, lessons that were visible (date was between today+1 and today+2) must immediately disappear from Lesson Lists after refresh.

**Preconditions:**
Partner config: advance days X = 1. Today = 2026-05-19.
Lesson C: lesson_date=2026-05-21 (today+2) — currently visible (threshold = today+1 = 2026-05-20).
Both Bookable_Flag=TRUE, Published, at student's LA location.

| #   | Action                                                    | Expected Result                                                                | Test Data                                                                                      |
| --- | --------------------------------------------------------- | ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| 1   | Open Lesson Lists with X=1 config                         | Lesson C (2026-05-21) IS visible (2026-05-21 >= today+1 = 2026-05-20)          | today = 2026-05-19; Lesson C lesson_date = 2026-05-21; X = 1; threshold = 2026-05-20 (today+1) |
| 2   | Admin updates partner advance days config from X=1 to X=3 | Config updated successfully                                                    | X changed: 1 → 3; new threshold = today+3 = 2026-05-22                                         |
| 3   | Student refreshes Lesson Lists                            | Lesson C (2026-05-21) is NO LONGER visible (2026-05-21 < today+3 = 2026-05-22) | —                                                                                              |

---

## Suite: Advance Days Threshold – Timezone Gap

### [Nichibei] Lesson Booking – Advance Days Timezone – Device ahead of lesson timezone – Server date used correctly

**Description:** AC 02.2 — BR-7 / BR-26: BVA (Timezone): When the student's device timezone is AHEAD of the lesson timezone, "today" for threshold calculation must use the lesson timezone (server-side). A lesson that is above the X-day threshold in lesson TZ must be shown — even if the device's local date makes the lesson appear to fall short of the threshold.

**Preconditions:**
Lesson timezone = UTC+9 (JST). Student's device timezone = UTC+12 (NZST, 3 hours ahead).
Current time = 2026-05-19 22:30 JST = 2026-05-20 01:30 NZST (device shows date = 2026-05-20).
Partner config: X = 1. Lesson at student's LA location: lesson_date = 2026-05-20, Bookable_Flag=TRUE, Published.

Threshold calculation:

- Lesson TZ (JST): today = 2026-05-19 → threshold = 2026-05-20 → lesson_date 2026-05-20 ≥ 2026-05-20 → **VISIBLE** ✅
- Device TZ (NZST): today = 2026-05-20 → threshold = 2026-05-21 → lesson_date 2026-05-20 < 2026-05-21 → device would hide ❌

| #   | Action                                                                                          | Expected Result                                                           | Test Data                                                                                          |
| --- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| 1   | Login to app (device TZ = NZST, device date = 2026-05-20) and open Lesson Lists                 | Lesson Lists screen shown                                                 | today (JST/server) = 2026-05-19; today (NZST/device) = 2026-05-20; lesson_date = 2026-05-20; X = 1 |
| 2   | Look for lesson with lesson_date=2026-05-20                                                     | Lesson IS visible (system uses lesson TZ “today” = 2026-05-19)            | threshold (JST) = 2026-05-20 (today+1); lesson_date 2026-05-20 = threshold → visible               |
| 3   | Confirm that if device TZ calculation were used instead, the lesson would be incorrectly hidden | System correctly shows the lesson using server/lesson TZ, not device date | threshold (NZST) = 2026-05-21 (today+1); lesson_date 2026-05-20 < threshold → device would hide    |

---

## Suite: Stale Lesson Lists Data

### [Nichibei] Lesson Booking – Stale Lesson Lists – Lesson reaches capacity while Lesson Lists open – Tap Reserve – Server rejects

**Description:** AC 02.4 — BR-17 / Stale UI: When a student has Lesson Lists open (UI shows Reserve enabled on a lesson), and another student fills the last seat before the first student taps Reserve, the server must reject the booking with "lesson full" error even though the UI cache still shows the button as enabled.

**Preconditions:**
Today = 2026-05-19. Student A has Lesson Lists open; Lesson X shows Reserve button enabled (capacity=1, 0 sessions at load time).
Student B has not yet booked the lesson.

| #   | Action                                                                         | Expected Result                                                            | Test Data                                                  |
| --- | ------------------------------------------------------------------------------ | -------------------------------------------------------------------------- | ---------------------------------------------------------- |
| 1   | Student A opens Lesson Lists; Lesson X shows Reserve button enabled            | Reserve button is enabled (capacity=1, 0 bookings at time of page load)    | today = 2026-05-19; lesson_date = 2026-05-26; capacity = 1 |
| 2   | Student B books Lesson X → last seat taken (session count = 1 = capacity)      | Student B's booking succeeds; Lesson X is now full                         | —                                                          |
| 3   | Student A does NOT refresh Lesson Lists (stale UI still shows Reserve enabled) | Reserve button still appears enabled on Student A's screen (stale cache)   | —                                                          |
| 4   | Student A taps Reserve on Lesson X → Confirmation Screen opens → taps Confirm  | Booking request submitted to server                                        | —                                                          |
| 5   | View server response                                                           | Booking rejected: "This lesson is now full. Please choose another lesson." | —                                                          |
| 6   | Verify no Student Session created for Student A                                | No duplicate session in Salesforce for Student A and Lesson X              | —                                                          |
