# Test Cases: LT-92532 — [Riso] Lesson Allocation – System Integration & Impact

> Source gaps identified from: Confluence Lesson Allocation Flow · Confluence LA Student Allocation Report · Local test cases TC-1261, PX-1517

## Suite: LA – System Integration

---

### [Riso] Lesson Allocation – require_allocation Flag – Set to TRUE on UI Create

**Description:** System integration — Verify that a Lesson Allocation created via the new UI flow automatically sets `require_allocation = TRUE`, which is required for the student to appear in lesson assignment and the Allocation Dashboard.

**Preconditions:**

- Logged in as HQ or CM user
- A student exists with an active enrolled location
- Course Master, Course Offering, and Location Course exist for the target AY and Location
- Student has no existing LA for the selected course

| #   | Action                                                                                              | Expected Result                                                               | Test Data                       |
| --- | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------- |
| 1   | Navigate to Student detail → Contact → Course tab                                                   | Course tab is displayed                                                       |                                 |
| 2   | Click "New Lesson Allocation" → fill all required fields (AY, Location, Course, Type, Dates) → Save | LA is created; user is redirected to Contact page; new LA appears in LA table | Type: Regular, valid date range |
| 3   | Navigate to the created LA record (e.g., via database or detail view)                               | LA record exists                                                              |                                 |
| 4   | Check the `require_allocation` field on the LA record                                               | `require_allocation = TRUE`                                                   |                                 |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocation – Add Students Popup – Student Visible After UI Create

**Description:** End-to-end integration — Verify that after creating a UI-based LA, the student appears in the lesson's "Add Students" popup, filtered by the LA course.

**Preconditions:**

- Logged in as HQ or CM user
- Student has no existing LA
- A published group lesson exists for the same AY, Location, and Course as the LA to be created

| #   | Action                                                                                                   | Expected Result                                                     | Test Data                          |
| --- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- | ---------------------------------- |
| 1   | Create a UI-based LA for Student A: Course = Course X, AY = current AY, Location = Loc A, Type = Regular | LA created; `require_allocation = TRUE` (verified from previous TC) | Date range overlapping lesson date |
| 2   | Navigate to the group lesson detail page (same course/location as the LA)                                | Lesson detail is displayed                                          |                                    |
| 3   | Click "Add Students" button on the Student Sessions section                                              | Add Students popup/modal opens                                      |                                    |
| 4   | Filter by Course X                                                                                       | Student A is visible in the list                                    | Filter: Course X                   |
| 5   | Verify student entry in popup                                                                            | Student A row shows LA info (course, require_allocation indicator)  |                                    |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocation – Allocation Dashboard – LA Appears Immediately After UI Create

**Description:** Integration — Verify that after creating a UI-based LA, the student's course appears in the Allocation Dashboard under Contact → Course tab.

**Preconditions:**

- Logged in as HQ or CM user
- Student has no existing LA for Course X
- Allocation Dashboard section exists on Contact → Course tab

| #   | Action                                                                   | Expected Result                                                                              | Test Data                          |
| --- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------- | ---------------------------------- |
| 1   | Create UI-based LA for Student A: Course X, AY 2026, Loc A, Type Regular | LA created; user redirected to Contact page                                                  | Start: 2026-04-01, End: 2026-12-31 |
| 2   | Navigate back to Contact → Course tab                                    | Course tab is displayed                                                                      |                                    |
| 3   | Scroll to Allocation Dashboard and select Overall filter                 | Dashboard is visible                                                                         |                                    |
| 4   | Locate Course X entry in the dashboard                                   | Course X (2026-04-01 – 2026-12-31) appears in the Allocation Dashboard with correct location |                                    |
| 5   | Verify Total Purchased Slots column                                      | Total Purchased Slots = value entered at creation (from AC 01.3)                             |                                    |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Allocation Dashboard – Sort Order With Multiple LAs

**Description:** Integration — Verify that when a student has multiple UI-created LAs, the Allocation Dashboard displays them sorted by start_date ASC, then end_date ASC, then created_at ASC.

**Preconditions:**

- Logged in as HQ or CM user
- Student has no existing LAs
- Three Course Masters exist, each with Course Offering and Location Course for AY 2026

| #   | Action                                                                   | Expected Result                                                                                                             | Test Data                                    |
| --- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| 1   | Create LA #1 for Course A: Start 2026-06-01, End 2026-12-31              | LA #1 created                                                                                                               |                                              |
| 2   | Create LA #2 for Course B: Start 2026-04-01, End 2026-12-31              | LA #2 created                                                                                                               |                                              |
| 3   | Create LA #3 for Course C: Start 2026-04-01, End 2026-08-31              | LA #3 created                                                                                                               |                                              |
| 4   | Navigate to Contact → Course tab → Allocation Dashboard → Overall filter | Dashboard is displayed                                                                                                      |                                              |
| 5   | Observe the order of rows                                                | Rows appear: LA #3 (Course C, 04-01 to 08-31) first, LA #2 (Course B, 04-01 to 12-31) second, LA #1 (Course A, 06-01) third | Sorted: start ASC → end ASC → created_at ASC |

**Severity:** normal
**Priority:** medium

---

### [Riso] Lesson Allocation – Order Coexistence – UI-Created LA Not Duplicated by Subsequent Order

**Description:** Integration — Verify that submitting an order for the same Course + AY + Location where a UI-created LA already exists does not create a duplicate LA, or triggers the date-overlap validation preventing the duplicate.

**Preconditions:**

- Logged in as HQ or CM user
- A UI-created LA exists for Student A: Course X, AY 2026, Loc A, Start 2026-04-01, End 2026-12-31
- The Riso org has Order module accessible, or this is tested via an integration test scenario

| #   | Action                                                           | Expected Result                                                                       | Test Data                                 |
| --- | ---------------------------------------------------------------- | ------------------------------------------------------------------------------------- | ----------------------------------------- |
| 1   | Note the existing UI-created LA for Student A, Course X          | 1 LA exists for Course X (Start: 2026-04-01, End: 2026-12-31)                         |                                           |
| 2   | Submit a new order for Student A, Course X, same AY and Location | Either: (a) system blocks creation with overlap error, OR (b) no second LA is created | Order for same course / overlapping dates |
| 3   | Navigate to Contact → Course tab and check LA table              | Exactly 1 LA entry for Course X (no duplicate)                                        |                                           |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Assign Student to Lesson – Manual LA

**Description:** End-to-end — Verify that a student with a UI-created LA can be assigned to a lesson via the "Add Students" popup, and that the LA detail (Lesson Allocated, Lesson Allocation Status, Report History) is updated correctly after assignment.

**Preconditions:**

- Logged in as HQ or CM user
- Student A has a UI-created LA: Course X, AY 2026, Loc A, Type = Regular, Start 2026-04-01, End 2026-12-31, `require_allocation = TRUE`
- A published group lesson exists: Course X, Loc A, lesson date within LA date range

| #   | Action                                                                  | Expected Result                                                                                         | Test Data        |
| --- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ---------------- |
| 1   | Navigate to the lesson detail page                                      | Lesson detail is displayed; Student Sessions section is visible                                         |                  |
| 2   | Click "Add Students" → filter by Course X                               | Add Students popup opens; Student A is visible in the list                                              | Filter: Course X |
| 3   | Select Student A → confirm                                              | Student A is added to the lesson; student session row appears in the Student Sessions table             |                  |
| 4   | Navigate to Student A → Contact → Course tab → LA table → LA detail     | LA detail opens                                                                                         |                  |
| 5   | Check Lesson Allocated, Lesson Allocation Status, Report History fields | Lesson Allocated count increased; Lesson Allocation Status updated; Report History shows the assignment |                  |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocation – Unassign Student from Lesson – Manual LA

**Description:** End-to-end — Verify that a student with a UI-created LA can be unassigned from a lesson, and the LA detail is updated to reflect the removal.

**Preconditions:**

- Student A has a UI-created LA: Course X, `require_allocation = TRUE`
- Student A is already assigned to a published group lesson (Course X) — refer to previous TC

| #   | Action                                                         | Expected Result                                                                                       | Test Data |
| --- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | --------- |
| 1   | Navigate to the lesson detail page where Student A is assigned | Student A row is visible in Student Sessions                                                          |           |
| 2   | Select Student A → click Unassign / Remove                     | Confirmation dialog appears (if applicable); student is removed from the lesson                       |           |
| 3   | Verify Student Sessions table                                  | Student A row is no longer present                                                                    |           |
| 4   | Navigate to Student A → LA detail                              | Lesson Allocated count decremented; Lesson Allocation Status updated; Report History reflects removal |           |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – New/Risk Flag – Displayed Correctly on Student Session

**Description:** Integration — Verify that after a student with a UI-created LA is assigned to a lesson, the New flag and Risk flag are displayed correctly in the Student Sessions table based on the student's status.

**Preconditions:**

- Student A has a UI-created LA: Course X, `require_allocation = TRUE`
- Student A is assigned to a published group lesson (Course X)
- At least one student is configured to show the New flag (first time assigned) and another set up for Risk flag conditions

| #   | Action                                                                 | Expected Result                                    | Test Data                            |
| --- | ---------------------------------------------------------------------- | -------------------------------------------------- | ------------------------------------ |
| 1   | Navigate to lesson detail → Student Sessions table                     | Student Sessions table is displayed                |                                      |
| 2   | Locate Student A (newly assigned, no prior lesson attendance)          | New flag is displayed on Student A's row           | Student A: first lesson assignment   |
| 3   | Locate Student B whose risk condition is met (e.g., multiple absences) | Risk flag is displayed on Student B's row          | Student B: risk condition configured |
| 4   | Verify flag translations and column labels                             | New/Risk tags display correctly in the UI language |                                      |

**Severity:** major
**Priority:** medium

---

### [Riso] Lesson Allocation – Reallocate – Student Reallocated from One Lesson to Another

**Description:** Integration — Verify that a student with a UI-created LA can be reallocated from one lesson to another (e.g., different time slot, same course), and the reallocate flag is shown correctly.

**Preconditions:**

- Student A has a UI-created LA: Course X, `require_allocation = TRUE`
- Student A is assigned to Lesson L1 (Course X)
- A second published lesson L2 exists for the same course on a different schedule

| #   | Action                                                          | Expected Result                                                                            | Test Data         |
| --- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ----------------- |
| 1   | Navigate to Lesson L1 detail → Student Sessions → Student A row | Student A is listed; Reallocate action is available                                        |                   |
| 2   | Click Reallocate for Student A → select Lesson L2               | Reallocation dialog/form opens; L2 is selectable                                           | Target lesson: L2 |
| 3   | Confirm reallocation                                            | Student A is removed from L1 and assigned to L2; reallocate flag shown in Student Sessions |                   |
| 4   | Navigate to Lesson L2 → Student Sessions                        | Student A appears in L2's Student Sessions table                                           |                   |
| 5   | Navigate to Student A → LA detail → Report History              | Report History reflects the reallocation event                                             |                   |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Trial LA – Purchased Slot Editable and Student Session Behavior

**Description:** Integration — Verify specific behaviors for Trial LA type: Purchased Slot is editable to a greater value only, and student session and lesson assignment work correctly for Trial type.

**Preconditions:**

- Logged in as HQ or CM user
- Student A has a UI-created LA: Course X, Type = **Trial**, Purchased Slot = 3, Start 2026-04-01, End 2026-06-30
- A published group lesson exists for Course X within the LA date range

| #   | Action                                                                                   | Expected Result                                                                  | Test Data                 |
| --- | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------- |
| 1   | Navigate to Student A → LA detail → edit Trial LA → change Purchased Slot to 5 (greater) | Purchased Slot updated to 5; save succeeds                                       | New slot: 5 (original: 3) |
| 2   | Attempt to edit Purchased Slot to 3 (same as original)                                   | Validation error: must be greater than original                                  | New slot: 3               |
| 3   | Attempt to edit Purchased Slot to 2 (less than original)                                 | Validation error: must be greater than original                                  | New slot: 2               |
| 4   | Navigate to the published lesson → Add Students → filter Course X → add Student A        | Student A (Trial LA) is visible in popup and can be assigned                     |                           |
| 5   | Verify student session row for Student A                                                 | Student session row displays LA type = Trial; Purchased Slot = 5 (updated value) |                           |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Collect Attendance – Student with Manual LA

**Description:** Integration — Verify that attendance can be collected for a student assigned to a lesson via UI-created LA, and the attendance status and note are saved correctly.

**Preconditions:**

- Logged in as HQ or CM user (or teacher with appropriate access)
- Student A has a UI-created LA: Course X, `require_allocation = TRUE`
- Student A is assigned to a published group lesson (Course X); lesson is in progress or past

| #   | Action                                                        | Expected Result                                                                  | Test Data                             |
| --- | ------------------------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------------- |
| 1   | Navigate to the lesson detail page → Student Sessions section | Student A row is listed with Attendance Status = empty / default                 |                                       |
| 2   | Set attendance status for Student A (e.g., Attend)            | Attendance status updated to "Attend"                                            | Status: Attend                        |
| 3   | Set attendance status for Student A (e.g., Absent)            | Attendance status updated to "Absent"; attendance notice fields become available | Status: Absent                        |
| 4   | Enter attendance reason and note                              | Fields accept input; values saved on submit                                      | Reason: Personal; Note: "Out of town" |
| 5   | Submit / save the lesson attendance                           | Attendance saved; lesson status updates accordingly                              |                                       |
| 6   | Navigate to Student A → LA detail → Report History            | Attendance record appears in Report History with correct status and date         |                                       |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Lesson Report – Auto-Created for Student with Manual LA

**Description:** Integration — Verify that a lesson report is automatically created for a student with a UI-created LA when they are added to a lesson, and the report detail is accessible and correct.

**Preconditions:**

- Student A has a UI-created LA: Course X, `require_allocation = TRUE`
- Student A has been assigned to a published group lesson (Course X) and attendance has been submitted

| #   | Action                                                                | Expected Result                                                                                 | Test Data |
| --- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- | --------- |
| 1   | Navigate to the lesson detail page → Student Sessions → Student A row | Lesson report detail link is present on Student A's row                                         |           |
| 2   | Click the lesson report detail link                                   | Lesson report detail page opens for Student A                                                   |           |
| 3   | Verify lesson report fields                                           | Report contains: student name, lesson date, course, attendance status, attendance note (if set) |           |
| 4   | Navigate to Student A → LA detail → Report History tab                | Report History tab shows the lesson with correct lesson date, attendance status                 |           |
| 5   | Login BO → navigate to same lesson → Student Sessions → Student A     | Student A visible in BO lesson detail; lesson report created in BO                              |           |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Class Assignment – Assign Class via LA Detail

**Description:** Integration — Verify that a class can be assigned/changed on the LA detail view for a student with a UI-created LA, consistent with the class assignment flow for order-created LAs.

**Preconditions:**

- Logged in as HQ or CM user
- Student A has a UI-created LA: Course X, Type = Regular, `require_allocation = TRUE`
- A class (Class A) exists for Course X at the same location

| #   | Action                                                                | Expected Result                                                                           | Test Data             |
| --- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | --------------------- |
| 1   | Navigate to Student A → Contact → Course tab → LA detail for Course X | LA detail page opens; Class assignment section is visible                                 |                       |
| 2   | Click assign class → select Class A with effective date = start date  | Class A is assigned; effective date = LA start date                                       | Effective date: today |
| 3   | Verify lessons within the effective date range are updated            | Student A is added to all lessons of Class A within the date range                        |                       |
| 4   | Change class: select Class B with effective date in the future        | Class B is assigned from the future date; Class A assignment remains until effective date | New class: Class B    |
| 5   | Navigate to the affected lessons and verify Student Sessions          | Lessons on or after effective date show Student A in Class B; prior lessons show Class A  |                       |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Lesson Mobile – Student Sees Lesson After Manual LA Assignment

**Description:** Integration — Verify that after a student with a UI-created LA is assigned to a lesson, the student and parent can view the lesson and lesson report on the Mobile app with correct information.

**Preconditions:**

- Student A has a UI-created LA: Course X, `require_allocation = TRUE`
- Student A has been assigned to a published group lesson (Course X)
- Attendance has been submitted for Student A
- Mobile app access is available for student/parent login

| #   | Action                                                    | Expected Result                                                                 | Test Data |
| --- | --------------------------------------------------------- | ------------------------------------------------------------------------------- | --------- |
| 1   | Login to Mobile app as Student A (or Parent of Student A) | Mobile home screen is displayed                                                 |           |
| 2   | Navigate to Lessons / Schedule section                    | The assigned lesson (Course X) appears in the student's lesson schedule         |           |
| 3   | Open the lesson detail on mobile                          | Lesson detail shows: course name, date/time, location, teacher name             |           |
| 4   | Navigate to the lesson report for this lesson             | Lesson report is visible; attendance status is correct (Attend / Absent as set) |           |
| 5   | Verify lesson report information is consistent with SF/BO | Attendance status, note, and lesson date match what was set in SF lesson detail |           |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Calendar – Student List – UI-created LA always visible (Ignore Duration)

**Description:** System integration — Verify that a student with an LA created via the UI always appears on the Student List in the Calendar environment, regardless of the LA duration, because Calendar does not check LA duration limits when filtering students.

**Preconditions:**

- Logged in as HQ or CM user
- A UI-created LA exists for Student A: Course X, Type = Regular, Start 2026-01-01, End 2026-01-15, `require_allocation = TRUE`
- A published group lesson exists for Course X on a date far outside the LA duration (e.g., 2026-05-01)

| #   | Action                                                                   | Expected Result                                                                    | Test Data                                   |
| --- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- | ------------------------------------------- |
| 1   | Navigate to Calendar tab                                                 | Calendar is displayed                                                              |                                             |
| 2   | Select the lesson for Course X on 2026-05-01                             | Lesson details/drawer opens                                                        | Lesson Date: 2026-05-01 (Outside LA effect) |
| 3   | Open the "Add Students" or view the Student List assigning to the lesson | Student list opens allowing searching by Course X                                  |                                             |
| 4   | Search for Student A in the list                                         | Student A still appears successfully in the Student List and is enabled to assign  |                                             |

**Severity:** normal
**Priority:** medium

---

### [Riso] Lesson Allocation – Calendar – Lesson Assignment – Update LA Date does not auto assign/unassign

**Description:** Integration — Verify that extending or modifying an LA’s date on the UI does not trigger any implicit/background processes to auto-assign or auto-unassign the student from their existing lesson events on the Calendar.

**Preconditions:**

- Logged in as HQ or CM user
- Student A has a UI-created LA for Course X: Start 2026-04-01, End 2026-06-30
- Student A has been manually assigned to Lesson L1 (Course X) on 2026-05-15 (within LA range)
- Student A is also assigned to another Lesson L2 (Course X) on 2026-08-01 (outside original LA range, which is allowed by Calendar rules)

| #   | Action                                                                              | Expected Result                                                                                         | Test Data                               |
| --- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | --------------------------------------- |
| 1   | Navigate to Contact → Course tab → Edit LA from the UI                              | LA modal opens with editable Start and End Date fields                                                  |                                         |
| 2   | Extend End Date from 2026-06-30 to 2026-12-31 and save                              | LA saved successfully                                                                                   | End Date update: 2026-12-31             |
| 3   | Navigate to Calendar tab                                                            | Calendar view opens                                                                                     |                                         |
| 4   | Check the participation of Student A in Lesson L1 (2026-05-15)                      | Student A is still assigned to Lesson L1; no background unassign triggered                              | Lesson L1 Date: 2026-05-15              |
| 5   | Check the participation of Student A in Lesson L2 (2026-08-01)                      | Student A is still assigned to Lesson L2; no auto-status updates or removals triggered                  | Lesson L2 Date: 2026-08-01              |

**Severity:** normal
**Priority:** medium

---

### [Riso] Lesson Allocation – Calendar – Delete LA – Synchronous unlinking

**Description:** Integration — Verify that deleting a UI-created LA synchronously removes the student from any calendar lessons they were already assigned to. According to Business Rule 32, the lesson unlinking is immediate.

**Preconditions:**

- Logged in as HQ or CM user
- Student A has a UI-created LA for Course X
- Student A is assigned to two upcoming published group lessons (L1 and L2) for Course X

| #   | Action                                                               | Expected Result                                                                                                            | Test Data |
| --- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | Navigate to Calendar and verify Student A in L1 and L2               | Student A is visible in the Student Sessions list for both L1 and L2                                                       |           |
| 2   | Navigate to Contact → Course tab → Delete the LA for Student A       | Confirmation dialog warns about allocated lessons being removed                                                            |           |
| 3   | Confirm the deletion                                                 | LA is immediately deleted                                                                                                  |           |
| 4   | Navigate back to Calendar and check Student Sessions for L1 and L2   | Student A no longer appears in the sessions for either L1 or L2; synchronous unlinking happened successfully               |           |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocation – Calendar – Student Dots – "Trial Student" label visibility

**Description:** Integration — Verify that a UI-created LA configured as 'Trial' propagates the correct student attribute so the "Trial Student dot" mark appears correctly on lessons in the Calendar view.

**Preconditions:**

- Logged in as HQ or CM user
- Student A has an active UI-created LA: Course X, Type = **Trial**
- Student A is assigned to a published group lesson for Course X

| #   | Action                                                                 | Expected Result                                                                           | Test Data             |
| --- | ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | --------------------- |
| 1   | Navigate to Calendar tab                                               | Calendar view is displayed containing the active lesson event                             |                       |
| 2   | Open or expand the lesson detail for the assigned course               | Student list for the specific lesson opens                                                |                       |
| 3   | Observe the visual indicators next to Student A's name                 | System correctly displays the "Trial Student dot" indicating they are taking a trial      | LA Type used: Trial   |

**Severity:** major
**Priority:** medium

---

### [Riso] Lesson Allocation – Calendar – Student Dots – "New Student" label visibility

**Description:** Integration — Verify that a UI-created LA (as the student's first enrollment) correctly flags the student attribute so the "New Student dot" is indicated at their first lesson in the Calendar view.

**Preconditions:**

- Logged in as HQ or CM user
- Student A has a newly created active UI LA: Course X, Type = **Regular**
- This applies to the very first lesson assigned to Student A upon starting the course

| #   | Action                                                                  | Expected Result                                                                                | Test Data               |
| --- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ----------------------- |
| 1   | Navigate to Calendar tab                                                | Calendar view is displayed                                                                     |                         |
| 2   | Open the detail or drawer of Student A's first assigned lesson event    | Student Sessions list opens                                                                    |                         |
| 3   | Observe the visual indicators next to Student A's name                  | System correctly displays the "New Student dot" to mark the student's very first enrolled date |                         |

**Severity:** major
**Priority:** medium

---

### [Riso] Lesson Allocation – Calendar – Assign Student – One-time lesson

**Description:** Integration — Verify that a student with a UI-created LA can be properly assigned to a One-time lesson, and the LA's Lesson Allocated count updates correctly.

**Preconditions:**

- Logged in as HQ or CM user
- Student A has an active UI-created LA for Course X (`require_allocation = TRUE`)
- A published **One-time** lesson exists for Course X within the LA duration

| #   | Action                                                                    | Expected Result                                                                     | Test Data               |
| --- | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------- |
| 1   | Navigate to the One-time lesson detail page (or drawer)                   | Lesson details are displayed                                                        |                         |
| 2   | Click "Add Students" and search for Student A                             | Student A is listed                                                                 |                         |
| 3   | Select Student A and confirm assignment                                   | Student A is added to the One-time lesson                                           | Target: One-time lesson |
| 4   | Navigate to Contact → Course tab → LA detail for Student A                | Lesson Allocated count increments by 1                                              |                         |
| 5   | Check LA Report History                                                   | The specific one-time lesson is recorded in the history tab                         |                         |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocation – Calendar – Assign Student – Recurring lesson – 'Only this' option

**Description:** Integration — Verify that a student with a UI-created LA can be assigned to a single instance of a recurring lesson using the 'Only this' option.

**Preconditions:**

- Logged in as HQ or CM user
- Student A has an active UI-created LA for Course X
- A published **Recurring** lesson series exists for Course X within the LA duration

| #   | Action                                                                    | Expected Result                                                                     | Test Data               |
| --- | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------- |
| 1   | Navigate to a specific instance of the recurring lesson                   | Lesson details are displayed                                                        |                         |
| 2   | Click "Add Students", select Student A                                    | Options for recurring assignment appear                                             |                         |
| 3   | Choose the "**Only this**" lesson option and confirm                      | Student A is assigned ONLY to the current lesson instance                           | Option: Only this       |
| 4   | Check the next lesson in the recurring series                             | Student A is NOT assigned to subsequent instances                                   |                         |
| 5   | Check LA Report History                                                   | Exactly 1 lesson instance is added to the allocated count and history               |                         |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Calendar – Assign Student – Recurring lesson – 'This and the following' option

**Description:** Integration — Verify that assigning a student with a UI-created LA using 'This and the following' correctly populates all subsequent instances in a recurring lesson series up to the LA end date.

**Preconditions:**

- Logged in as HQ or CM user
- Student A has an active UI-created LA for Course X
- A published **Recurring** lesson series exists for Course X within the LA duration

| #   | Action                                                                    | Expected Result                                                                     | Test Data                  |
| --- | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | -------------------------- |
| 1   | Navigate to a specific instance of the recurring lesson                   | Lesson details are displayed                                                        |                            |
| 2   | Click "Add Students", select Student A                                    | Options for recurring assignment appear                                             |                            |
| 3   | Choose "**This and the following**" option and confirm                    | Student A is assigned to the current and all subsequent instances in the series     | Option: This and following |
| 4   | Check subsequent lessons in the series                                    | Student A is present in all valid future lesson instances within the LA duration    |                            |
| 5   | Check LA Report History                                                   | Lesson Allocated count increments by the total number of newly assigned instances   |                            |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocation – Calendar – Assign Student – Recurring lesson – 'Specific number' option

**Description:** Integration — Verify that assigning a student with a UI-created LA via 'Specific number' correctly assigns them to the exact count of subsequent recurring lessons.

**Preconditions:**

- Logged in as HQ or CM user
- Student A has an active UI-created LA for Course X
- A published **Recurring** lesson series exists for Course X

| #   | Action                                                                    | Expected Result                                                                     | Test Data                  |
| --- | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | -------------------------- |
| 1   | Navigate to a specific instance of the recurring lesson                   | Lesson details are displayed                                                        |                            |
| 2   | Click "Add Students", select Student A                                    | Options for recurring assignment appear                                             |                            |
| 3   | Choose "**Specific number**" option, input '3', and confirm               | Student A is assigned to the current lesson and the next 2 instances (total 3)      | Option: Specific number, 3 |
| 4   | View the 4th consecutive lesson instance                                  | Student A is NOT assigned to the 4th instance                                       |                            |
| 5   | Check LA Report History                                                   | Lesson Allocated count strictly increases by 3                                      |                            |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Calendar – Unassign Student – One-time lesson

**Description:** Integration — Verify that unassigning a student with a UI-created LA from a One-time lesson correctly drops them from the lesson and deducts the allocation count.

**Preconditions:**

- Logged in as HQ or CM user
- Student A is assigned to a published **One-time** lesson via their UI-created LA

| #   | Action                                                                    | Expected Result                                                                     | Test Data               |
| --- | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------- |
| 1   | Navigate to the One-time lesson detail where Student A is assigned        | Student A is visible in Student Sessions                                            |                         |
| 2   | Click Remove/Unassign on Student A's row                                  | Confirmation modal is shown                                                         |                         |
| 3   | Confirm unassignment                                                      | Student A is removed from the lesson                                                |                         |
| 4   | Check LA detail for Student A                                             | Lesson Allocated count decrements by 1; the lesson is removed from Report History   |                         |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocation – Calendar – Unassign Student – Recurring lesson – 'Only this' option

**Description:** Integration — Verify that unassigning a student with a UI-created LA via 'Only this' drops them only from the specific recurring lesson instance selected.

**Preconditions:**

- Logged in as HQ or CM user
- Student A is assigned to multiple instances of a published **Recurring** lesson series via their UI-created LA

| #   | Action                                                                    | Expected Result                                                                     | Test Data               |
| --- | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------- |
| 1   | Navigate to a specific assigned instance of the recurring lesson          | Student A is visible in Student Sessions                                            |                         |
| 2   | Click Remove/Unassign on Student A's row                                  | Modal prompts for unassign scope for recurring lesson                               |                         |
| 3   | Select "**Only this**" lesson option and confirm                          | Student A is removed ONLY from this specific instance                               | Option: Only this       |
| 4   | Navigate to the next instance in the recurring series                     | Student A remains assigned to the subsequent instance                               |                         |
| 5   | Check LA detail for Student A                                             | Lesson Allocated count is decremented by exactly 1                                  |                         |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Calendar – Unassign Student – Recurring lesson – 'This and the following' option

**Description:** Integration — Verify that unassigning a student with a UI-created LA via 'This and the following' drops them from the current and all future instances of the recurring series.

**Preconditions:**

- Logged in as HQ or CM user
- Student A is assigned to multiple instances of a published **Recurring** lesson series via their UI-created LA

| #   | Action                                                                    | Expected Result                                                                     | Test Data                  |
| --- | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | -------------------------- |
| 1   | Navigate to a specific assigned instance of the recurring lesson          | Student A is visible in Student Sessions                                            |                            |
| 2   | Click Remove/Unassign on Student A's row                                  | Modal prompts for unassign scope for recurring lesson                               |                            |
| 3   | Select "**This and the following**" option and confirm                    | Student A is removed from this instance and all future instances in the series      | Option: This and following |
| 4   | Navigate to any subsequent instance in the recurring series               | Student A is no longer assigned to those future lessons                             |                            |
| 5   | Check LA detail for Student A                                             | Lesson Allocated count is decremented by the total number of unassigned instances   |                            |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocation – Calendar – Bulk Collect Attendance – LA student in lesson

**Description:** Integration — Verify that bulk collecting attendance operates correctly for a student assigned to a lesson via a newly created UI LA, seamlessly applying the status to the LA reports.

**Preconditions:**

- Logged in as HQ or CM user
- Student A has a UI-created LA and is assigned to a past/in-progress lesson
- There are multiple students in the lesson

| #   | Action                                                                    | Expected Result                                                                     | Test Data                  |
| --- | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | -------------------------- |
| 1   | Navigate to the lesson detail page (or bulk attendance feature via list)  | Student Sessions are listed                                                         |                            |
| 2   | Check the checkbox to select multiple/all students (including Student A)  | UI indicates multiple students are selected                                         |                            |
| 3   | Click 'Collect Attendance' action and set status to 'Attend'              | Bulk action executes                                                                | Action: Bulk Attendance    |
| 4   | Confirm the bulk attendance submission                                    | Student A's attendance updates to 'Attend' along with the others                    |                            |
| 5   | Check LA Report History for Student A                                     | The updated attendance status ('Attend') reflects correctly inside the LA details   |                            |

**Severity:** major
**Priority:** high
