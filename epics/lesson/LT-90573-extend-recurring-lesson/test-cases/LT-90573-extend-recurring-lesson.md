# Test Cases: LT-90573 — Extend Recurring Lesson Settings

## Suite: Extend Recurrence Button

### Extend Recurrence Button – Recurring Lesson (Daily / Weekly / Custom) – Button Visible

**Description:** AC 01.1 / AC 01.3 — Decision Table: Verify button is present for all recurring schedule types (daily, weekly, custom).

**Preconditions:**
Admin user has created:

- A daily recurring lesson schedule
- A weekly recurring lesson schedule
- A custom recurring lesson schedule

| #   | Action                                                          | Expected Result                      | Test Data |
| --- | --------------------------------------------------------------- | ------------------------------------ | --------- |
| 1   | Open Lesson Schedule detail page of the daily recurring lesson  | User sees "Extend Recurrence" button |           |
| 2   | Open Lesson Schedule detail page of the weekly recurring lesson | User sees "Extend Recurrence" button |           |
| 3   | Open Lesson Schedule detail page of the custom recurring lesson | User sees "Extend Recurrence" button |           |

---

### Extend Recurrence Button – One-time Lesson – Button Hidden

**Description:** AC 01.3 — Decision Table: Button must not appear when is_recurring = FALSE (one-time lesson).

**Preconditions:**
Admin user has created a one-time lesson schedule

| #   | Action                                                  | Expected Result                                                 | Test Data |
| --- | ------------------------------------------------------- | --------------------------------------------------------------- | --------- |
| 1   | Open Lesson Schedule detail page of the one-time lesson | User does NOT see "Extend Recurrence" button                    |           |
| 2   | Inspect action buttons area                             | Only applicable action buttons are shown (no Extend Recurrence) |           |

---

### Extend Recurrence Button – Course Schedule Lesson – Button Hidden

**Description:** AC 01.3 — Decision Table: Button must not appear for course schedule lessons.

**Preconditions:**
Admin user has created a course schedule lesson

| #   | Action                                                         | Expected Result                                                 | Test Data |
| --- | -------------------------------------------------------------- | --------------------------------------------------------------- | --------- |
| 1   | Open Lesson Schedule detail page of the course schedule lesson | User does NOT see "Extend Recurrence" button                    |           |
| 2   | Inspect action buttons area                                    | Only applicable action buttons are shown (no Extend Recurrence) |           |

---

### Extend Recurrence Button – Recurring Lesson – Lesson Creation Form Opened

**Description:** AC 01.1 — Verify clicking the button opens the Lesson Creation Form with correct initial state.

**Preconditions:**
Admin user has created a daily recurring lesson schedule

| #   | Action                           | Expected Result                                                                    | Test Data |
| --- | -------------------------------- | ---------------------------------------------------------------------------------- | --------- |
| 1   | Open Lesson Schedule detail page | User sees "Extend Recurrence" button                                               |           |
| 2   | Click "Extend Recurrence" button | Lesson Creation Form opens with fields pre-filled according to the Lesson Schedule |           |

---

## Suite: Extend Recurrence Form

### Extend Recurrence Form – Pre-filled Fields – Sourced from Lesson Schedule and Editable

**Description:** AC 01.2 — Equivalence Partitioning: Verify Start Time, End Time, Duration, Teaching Medium, Lesson Name are pre-filled and editable.

**Preconditions:**
Admin has created a recurring lesson schedule with:

- Start Time = 09:00
- End Time = 10:00
- Duration = 60 min
- Teaching Medium = Offline
- Lesson Name = "Math Recurring"

| #   | Action                                                                                 | Expected Result                                                                                                   | Test Data                                                                      |
| --- | -------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| 1   | Open Lesson Schedule, click "Extend Recurrence                                         | Lesson Creation Form opens                                                                                        |                                                                                |
| 2   | Verify pre-filled values: Start Time, End Time, Duration, Teaching Medium, Lesson Name | Start Time = 09:00, End Time = 10:00, Duration = 60 min, Teaching Medium = Offline, Lesson Name = "Math Recurring | Source: Lesson Schedule                                                        |
| 3   | Edit Start Time to 10:00, End Time to 11:00, Lesson Name to "Math Extended             | Fields accept new values successfully                                                                             | New Start Time = 10:00, New End Time = 11:00, New Lesson Name = "Math Extended |

---

### Extend Recurrence Form – Date Field – Auto-calculated as Current End Date + 7 Days

**Description:** AC 01.2 — BVA: Date field must equal Lesson Schedule current end date + 7 days and be non-editable.

**Preconditions:**
Admin has created a recurring lesson schedule with End Date = 2026-03-10 (Tuesday)

| #   | Action                                         | Expected Result                                | Test Data                                         |
| --- | ---------------------------------------------- | ---------------------------------------------- | ------------------------------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens                     |                                                   |
| 2   | Check the Date field value                     | Date = 2026-03-17 (Tuesday, end date + 7 days) | End Date = 2026-03-10, Expected Date = 2026-03-17 |
| 3   | Attempt to edit the Date field                 | Date field is locked / non-editable            |                                                   |

---

### Extend Recurrence Form – Lesson Code – Auto-calculated as Last Existing Code + 1

**Description:** AC 01.2 — BVA: Lesson Code = last existing lesson code + 1.

**Preconditions:**
Admin has created a recurring lesson schedule with last lesson having lesson code = 10

| #   | Action                                         | Expected Result                     | Test Data                                     |
| --- | ---------------------------------------------- | ----------------------------------- | --------------------------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens          |                                               |
| 2   | Check the Lesson Code field                    | Lesson Code = 11 (last code 10 + 1) | Last existing lesson code = 10, Expected = 11 |

---

### Extend Recurrence Form – Day of Week – Auto-derived from Auto-calculated Date

**Description:** AC 01.2 — Verify Day of the Week is automatically derived from the auto-calculated Date.

**Preconditions:**
Admin has created a recurring lesson schedule with End Date = 2026-03-13 (Friday)

| #   | Action                                         | Expected Result                                | Test Data                      |
| --- | ---------------------------------------------- | ---------------------------------------------- | ------------------------------ |
| 1   | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens, Date = 2026-03-20  | End Date = 2026-03-13 (Friday) |
| 2   | Check Day of the Week field                    | Day of the Week = Friday (matching 2026-03-20) | Expected: Friday               |

---

### Extend Recurrence Form – Lesson Type and Lesson Capacity – Default Values as Design

**Description:** AC 01.2 — Equivalence Partitioning: Lesson Type = Regular (editable), Lesson Capacity = blank (optional).

**Preconditions:**
Admin has created a recurring lesson schedule

| #   | Action                                         | Expected Result                         | Test Data         |
| --- | ---------------------------------------------- | --------------------------------------- | ----------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens              |                   |
| 2   | Check Lesson Type field                        | Lesson Type = Regular                   | Default = Regular |
| 3   | Check Lesson Capacity field                    | Lesson Capacity is blank                | Optional field    |
| 4   | Change Lesson Type to a different value        | Lesson Type field accepts the new value |                   |

---

### Extend Recurrence Form – Classroom – Searchable Dropdown with Available Classrooms

**Description:** AC 01.2 — Verify Classroom field is a searchable dropdown showing available classrooms.

**Preconditions:**
Admin has created a recurring lesson schedule
Multiple classrooms available at the location: Room A, Room B, Room C

| #   | Action                                         | Expected Result                          | Test Data                         |
| --- | ---------------------------------------------- | ---------------------------------------- | --------------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens               |                                   |
| 2   | Click on Classroom dropdown                    | Dropdown shows available classrooms list | Available: Room A, Room B, Room C |
| 3   | Type "Room A" in the search field              | Dropdown filters to show only "Room A    | Search keyword = "Room A          |
| 4   | Select Room A from the filtered result         | Room A is selected as classroom          |                                   |

---

### Extend Recurrence Form – Locked Fields (Location / Academic Year / Course / Class / Teaching Method) – Non-editable

**Description:** AC 01.2 — Negative Testing: Attempt to edit each locked field; all must remain read-only.

**Preconditions:**
Admin has created a recurring lesson schedule with:

- Location = Tokyo
- Academic Year = 2025-2026
- Course = Mathematics
- Class = Class A
- Teaching Method = Group

| #   | Action                                                           | Expected Result                                    | Test Data               |
| --- | ---------------------------------------------------------------- | -------------------------------------------------- | ----------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence                   | Lesson Creation Form opens                         |                         |
| 2   | Verify Location field shows "Tokyo" and attempt to edit          | Location = "Tokyo", field is locked (non-editable) | Source: Lesson Schedule |
| 3   | Verify Academic Year field shows "2025-2026" and attempt to edit | Academic Year = "2025-2026", field is locked       | Source: Lesson Schedule |
| 4   | Verify Course field shows "Mathematics" and attempt to edit      | Course = "Mathematics", field is locked            | Source: Lesson Schedule |
| 5   | Verify Class field shows "Class A" and attempt to edit           | Class = "Class A", field is locked                 | Source: Lesson Schedule |
| 6   | Verify Teaching Method field shows "Group" and attempt to edit   | Teaching Method = "Group", field is locked         | Source: Lesson Schedule |

---

### Extend Recurrence Form – Recurring Settings (Recurrence Type / Days / Skip Closed Dates) – Inherited and Non-editable

**Description:** AC 01.2 — Negative Testing: Recurrence Type, Recurrence Days, and Skip Closed Dates must display saved values and be non-editable.

**Preconditions:**
Admin has created a custom recurring lesson with:

- Recurrence Type = Custom
- Recurrence Days = Monday, Wednesday, Friday
- Skip Closed Dates = checked

| #   | Action                                         | Expected Result                                                       | Test Data               |
| --- | ---------------------------------------------- | --------------------------------------------------------------------- | ----------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens with Recurring Settings section            |                         |
| 2   | Check Recurrence Type field                    | Recurrence Type = Custom (displayed, not editable)                    | Source: Lesson Schedule |
| 3   | Check Recurrence Days field                    | Recurrence Days = Monday, Wednesday, Friday (displayed, not editable) | Source: Lesson Schedule |
| 4   | Check Skip Closed Dates field                  | Skip Closed Dates = checked (displayed, not editable)                 | Source: Lesson Schedule |
| 5   | Attempt to edit Recurrence Type                | Field is locked, cannot be changed                                    |                         |
| 6   | Attempt to edit Skip Closed Dates              | Field is locked, cannot be changed                                    |                         |

---

### Extend Recurrence Form – Recurrence End Date – Later than Current – Accepted

**Description:** AC 01.2 / AC 01.3 — BVA: Verify user can extend End Date to 1 day after current and to far future.

**Preconditions:**
Admin has created a recurring lesson schedule by End Date

- Current Recurrence End Date = 2026-03-31

| #   | Action                                                     | Expected Result                                              | Test Data                     |
| --- | ---------------------------------------------------------- | ------------------------------------------------------------ | ----------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence             | Lesson Creation Form opens, Recurrence End Date = 2026-03-31 | Current End Date = 2026-03-31 |
| 2   | Set Recurrence End Date = 2026-04-01 (1 day after current) | Date accepted by the system                                  | BVA: Boundary + 1 day         |
| 3   | Save the form                                              | New lessons are created successfully                         |                               |
| 4   | Repeat: Set Recurrence End Date = 2026-12-31 (far future)  | Date accepted by the system                                  | BVA: Far future value         |
| 5   | Save the form                                              | New lessons are created successfully                         |                               |

---

### Extend Recurrence Form – Recurrence End Date – Same or Earlier than Current – Rejected

**Description:** AC 01.2 / AC 01.3 — BVA + Negative Testing: System must reject same date and earlier date.

**Preconditions:**
Admin has created a recurring lesson schedule by End Date

- Current Recurrence End Date = 2026-03-31

| #   | Action                                                      | Expected Result                                              | Test Data                          |
| --- | ----------------------------------------------------------- | ------------------------------------------------------------ | ---------------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence              | Lesson Creation Form opens, Recurrence End Date = 2026-03-31 | Current End Date = 2026-03-31      |
| 2   | Set Recurrence End Date = 2026-03-31 (same as current)      | System does not allow or shows validation error              | BVA: Exact boundary (same date)    |
| 3   | Attempt to save                                             | Save is rejected / blocked                                   |                                    |
| 4   | Set Recurrence End Date = 2026-03-15 (earlier than current) | System does not allow or shows validation error              | BVA: Below boundary (earlier date) |
| 5   | Attempt to save                                             | Save is rejected / blocked                                   |                                    |

---

### Extend Recurrence Form – Lesson Count – Greater than Current – Accepted

**Description:** AC 01.2 / AC 01.3 — BVA: Verify user can increase Lesson Count by 1 and by a large amount.

**Preconditions:**
Admin has created a recurring lesson schedule by Lesson Count

- Current Lesson Count = 10

| #   | Action                                         | Expected Result                               | Test Data                 |
| --- | ---------------------------------------------- | --------------------------------------------- | ------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens, Lesson Count = 10 | Current Lesson Count = 10 |
| 2   | Set Lesson Count = 11 (current + 1)            | Value accepted by the system                  | BVA: Boundary + 1         |
| 3   | Save the form                                  | New lessons are created successfully          |                           |
| 4   | Repeat: Set Lesson Count = 50 (large increase) | Value accepted by the system                  | BVA: Large increase       |
| 5   | Save the form                                  | New lessons are created successfully          |                           |

---

### Extend Recurrence Form – Lesson Count – Same or Less than Current – Rejected

**Description:** AC 01.2 / AC 01.3 — BVA + Negative Testing: System must reject same count and lower count.

**Preconditions:**
Admin has created a recurring lesson schedule by Lesson Count

- Current Lesson Count = 10

| #   | Action                                         | Expected Result                                 | Test Data                         |
| --- | ---------------------------------------------- | ----------------------------------------------- | --------------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens, Lesson Count = 10   | Current Lesson Count = 10         |
| 2   | Set Lesson Count = 10 (same as current)        | System does not allow or shows validation error | BVA: Exact boundary (same count)  |
| 3   | Attempt to save                                | Save is rejected / blocked                      |                                   |
| 4   | Set Lesson Count = 5 (less than current)       | System does not allow or shows validation error | BVA: Below boundary (lower count) |
| 5   | Attempt to save                                | Save is rejected / blocked                      |                                   |

---

## Suite: Extend Recurrence Create Lessons

### Extend Recurring – Daily / End Date – New Lessons Added in DRAFT Status

**Description:** AC 01.4 — State Transition: Verify all new lessons have DRAFT status and are added to the same recurring chain.

**Preconditions:**
Admin has created a daily recurring lesson schedule by End Date

- End Date = 2026-03-31
- 5 existing lessons in chain

| #   | Action                                         | Expected Result                                                    | Test Data                                   |
| --- | ---------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens                                         |                                             |
| 2   | Extend Recurrence End Date to 2026-04-15       | Date accepted                                                      | New End Date = 2026-04-15                   |
| 3   | Save the form                                  | New lessons are created                                            |                                             |
| 4   | Check status of all newly created lessons      | All new lessons have DRAFT status                                  | Expected status = DRAFT for all new lessons |
| 5   | Verify lessons are in the same recurring chain | New lessons appear in the same Lesson Schedule as existing lessons |                                             |

---

### Extend Recurring – Weekly / End Date – New Lessons Added in DRAFT Status

**Description:** AC 01.4 — State Transition: Verify for weekly recurrence type.

**Preconditions:**
Admin has created a weekly recurring lesson schedule by End Date

- End Date = 2026-03-31
- Existing lessons in chain

| #   | Action                                         | Expected Result                                               | Test Data                 |
| --- | ---------------------------------------------- | ------------------------------------------------------------- | ------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens                                    |                           |
| 2   | Extend Recurrence End Date to 2026-04-30       | Date accepted                                                 | New End Date = 2026-04-30 |
| 3   | Save the form                                  | New lessons are created                                       |                           |
| 4   | Check status of all newly created lessons      | All new lessons have DRAFT status                             | Expected status = DRAFT   |
| 5   | Verify lesson dates follow weekly pattern      | Lesson dates are 7 days apart following the weekly recurrence |                           |

---

### Extend Recurring – Custom / End Date – New Lessons Added in DRAFT Status on Specified Days

**Description:** AC 01.4 — State Transition: Verify for custom recurrence type with specific days.

**Preconditions:**
Admin has created a custom recurring lesson schedule by End Date

- Recurrence Days = Monday, Wednesday, Friday
- End Date = 2026-03-31

| #   | Action                                                    | Expected Result                                     | Test Data                       |
| --- | --------------------------------------------------------- | --------------------------------------------------- | ------------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence            | Lesson Creation Form opens                          |                                 |
| 2   | Extend Recurrence End Date to 2026-04-30                  | Date accepted                                       | New End Date = 2026-04-30       |
| 3   | Save the form                                             | New lessons are created                             |                                 |
| 4   | Check status of all newly created lessons                 | All new lessons have DRAFT status                   | Expected status = DRAFT         |
| 5   | Verify lesson dates follow custom pattern (Mon, Wed, Fri) | Lesson dates fall only on Monday, Wednesday, Friday | Recurrence Days = Mon, Wed, Fri |

---

### Extend Recurring – Daily / Lesson Count – New Lessons Added in DRAFT Status

**Description:** AC 01.4 — State Transition: Verify new lessons via Lesson Count path.

**Preconditions:**
Admin has created a daily recurring lesson schedule by Lesson Count

- Current Lesson Count = 10

| #   | Action                                         | Expected Result                     | Test Data                          |
| --- | ---------------------------------------------- | ----------------------------------- | ---------------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens          |                                    |
| 2   | Increase Lesson Count to 15                    | Value accepted                      | New Lesson Count = 15 (was 10, +5) |
| 3   | Save the form                                  | New lessons are created             |                                    |
| 4   | Check total number of lessons in the chain     | Total lessons in chain = 15         | Expected total = 15                |
| 5   | Check status of all newly created lessons      | All 5 new lessons have DRAFT status | Expected 5 new DRAFT lessons       |

---

### Extend Recurring – Weekly / Lesson Count – New Lessons Added in DRAFT Status

**Description:** AC 01.4 — State Transition: Verify for weekly recurrence via Lesson Count.

**Preconditions:**
Admin has created a weekly recurring lesson schedule by Lesson Count

- Current Lesson Count = 8

| #   | Action                                         | Expected Result                     | Test Data                         |
| --- | ---------------------------------------------- | ----------------------------------- | --------------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens          |                                   |
| 2   | Increase Lesson Count to 12                    | Value accepted                      | New Lesson Count = 12 (was 8, +4) |
| 3   | Save the form                                  | New lessons are created             |                                   |
| 4   | Check total number of lessons                  | Total lessons = 12                  | Expected total = 12               |
| 5   | Check status of new lessons                    | All 4 new lessons have DRAFT status | Expected 4 new DRAFT lessons      |

---

### Extend Recurring – Custom / Lesson Count – New Lessons Added in DRAFT Status on Specified Days

**Description:** AC 01.4 — State Transition: Verify for custom recurrence via Lesson Count.

**Preconditions:**
Admin has created a custom recurring lesson schedule by Lesson Count

- Recurrence Days = Tuesday, Thursday
- Current Lesson Count = 6

| #   | Action                                                     | Expected Result                                                | Test Data                         |
| --- | ---------------------------------------------------------- | -------------------------------------------------------------- | --------------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence             | Lesson Creation Form opens                                     |                                   |
| 2   | Increase Lesson Count to 10                                | Value accepted                                                 | New Lesson Count = 10 (was 6, +4) |
| 3   | Save the form                                              | New lessons are created                                        |                                   |
| 4   | Check total lessons and verify dates follow custom pattern | Total = 10, new lesson dates fall on Tuesday and Thursday only | Recurrence Days = Tue, Thu        |
| 5   | Check status of new lessons                                | All 4 new lessons have DRAFT status                            | Expected 4 new DRAFT lessons      |

---

### Extend Recurring – Duplicate Date Conflict – Manual Lesson on 1 Date – New Lesson Skipped

**Description:** AC 01.4 — Decision Table + Data Integrity: New lessons must NOT be created on dates that have manually added lessons.

**Preconditions:**
Admin has created a daily recurring lesson schedule by End Date (End Date = 2026-03-20)
Admin has manually added a lesson on 2026-03-25 via "Add Lesson" flow

| #   | Action                                         | Expected Result                                               | Test Data                                         |
| --- | ---------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens                                    |                                                   |
| 2   | Extend Recurrence End Date to 2026-03-31       | Date accepted                                                 | New End Date = 2026-03-31                         |
| 3   | Save the form                                  | New lessons are created                                       |                                                   |
| 4   | Check if a lesson is created on 2026-03-25     | No new lesson created on 2026-03-25 (skipped)                 | Conflict date = 2026-03-25 (manual lesson exists) |
| 5   | Check manually added lesson on 2026-03-25      | Manually added lesson is unchanged                            |                                                   |
| 6   | Count total new lessons created                | Total new lessons = expected count minus 1 (the skipped date) | Expected: total - 1 due to skip                   |

---

### Extend Recurring – Duplicate Date Conflict – Manual Lessons on Multiple Dates – All Conflicting Dates Skipped

**Description:** AC 01.4 — Decision Table: Multiple manual lessons on different dates within extension range, all must be skipped.

**Preconditions:**
Admin has created a weekly recurring lesson schedule by End Date (End Date = 2026-03-20)
Admin has manually added lessons on 2026-03-25 and 2026-04-01 via "Add Lesson" flow

| #   | Action                                         | Expected Result                                                                      | Test Data                               |
| --- | ---------------------------------------------- | ------------------------------------------------------------------------------------ | --------------------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens                                                           |                                         |
| 2   | Extend Recurrence End Date to 2026-04-15       | Date accepted                                                                        | New End Date = 2026-04-15               |
| 3   | Save the form                                  | New lessons are created                                                              |                                         |
| 4   | Check lessons on 2026-03-25 and 2026-04-01     | No new lessons on 2026-03-25 and 2026-04-01 (both skipped), manual lessons unchanged | Conflict dates = 2026-03-25, 2026-04-01 |
| 5   | Count total new lessons created                | Total new lessons = expected count minus 2                                           | Expected: total - 2 due to skips        |

---

### Extend Recurring – Lesson Code – Auto-incremented from Last Existing Code for Each New Lesson

**Description:** AC 01.4 — BVA + CRUD: Verify lesson code is auto-calculated based on the code defined in the extension form.

**Preconditions:**
Admin has created a recurring lesson schedule

- Last existing lesson code = 5
- Extension will create 3 new lessons

| #   | Action                                         | Expected Result                                             | Test Data                                      |
| --- | ---------------------------------------------- | ----------------------------------------------------------- | ---------------------------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens                                  |                                                |
| 2   | Verify Lesson Code = 6 (last + 1)              | Lesson Code = 6                                             | Last existing code = 5, Expected form code = 6 |
| 3   | Extend to create 3 new lessons                 | Settings accepted                                           |                                                |
| 4   | Save the form                                  | New lessons created                                         |                                                |
| 5   | Check lesson codes of all 3 new lessons        | Lesson codes = 6, 7, 8 (auto-incremented from defined code) | Expected: 6, 7, 8                              |

---

### Extend Recurring – New Lessons – No Teacher or Student Auto-allocated

**Description:** AC 01.4 — Negative Testing: Newly created lessons must not auto-inherit teacher/student from existing lessons.

**Preconditions:**
Admin has created a recurring lesson schedule

- Existing lessons have Teacher A and Student B assigned
- Extension creates new lessons

| #   | Action                                                     | Expected Result                                     | Test Data                    |
| --- | ---------------------------------------------------------- | --------------------------------------------------- | ---------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence             | Lesson Creation Form opens                          |                              |
| 2   | Extend and save                                            | New lessons created                                 |                              |
| 3   | Open each newly created lesson detail                      | Lesson detail pages open                            |                              |
| 4   | Check Lesson Teacher section                               | No teacher assigned to new lessons                  | Expected: empty teacher list |
| 5   | Check Student Sessions section                             | No student assigned to new lessons                  | Expected: empty student list |
| 6   | Verify existing lessons still have Teacher A and Student B | Existing lessons still have Teacher A and Student B |                              |

---

### Extend Recurring – Skip Closed Dates – Closed Date in Extension Range – No Lesson Created

**Description:** AC 01.4 — Regression: When Skip Closed Dates = checked, no extended lesson should be created on a closed date.

**Preconditions:**
Admin has created a recurring lesson schedule with Skip Closed Dates = checked

- A closed date (e.g., 2026-04-10) falls within the extension date range

| #   | Action                                                  | Expected Result                                      | Test Data                                            |
| --- | ------------------------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence          | Lesson Creation Form opens                           |                                                      |
| 2   | Verify Skip Closed Dates shows "checked" (non-editable) | Skip Closed Dates = checked, non-editable            | Source: Lesson Schedule, Skip Closed Dates = checked |
| 3   | Extend End Date to cover range including 2026-04-10     | Date accepted                                        | Closed date = 2026-04-10                             |
| 4   | Save the form                                           | New lessons created                                  |                                                      |
| 5   | Check if any lesson is created on 2026-04-10            | No lesson exists on 2026-04-10 (closed date skipped) | Expected: no lesson on closed date                   |

---

### [Nichibei] Extend Recurring – Syllabus Description – Auto-filled for New Lessons Based on Lesson Code

**Description:** AC 01.4 — CRUD + Regression (Nichibei only): Syllabus description auto-filled for new lessons based on lesson code mapping.

**Preconditions:**
Nichibei tenant configuration
Syllabus master associated to course master with syllabus details:

- Code 6 → Description A
- Code 7 → Description B
- Code 8 → Description C
  Recurring lesson schedule created, last lesson code = 5

| #   | Action                                         | Expected Result                      | Test Data              |
| --- | ---------------------------------------------- | ------------------------------------ | ---------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens           |                        |
| 2   | Extend to create 3 new lessons (codes 6, 7, 8) | Settings accepted                    | lesson codes = 6, 7, 8 |
| 3   | Save the form                                  | New lessons created                  |                        |
| 4   | Check syllabus description of lesson code 6    | Syllabus description = Description A | Code 6 → Description A |
| 5   | Check syllabus description of lesson code 7    | Syllabus description = Description B | Code 7 → Description B |
| 6   | Check syllabus description of lesson code 8    | Syllabus description = Description C | Code 8 → Description C |

---

## Suite: Extend Recurrence Schedule Sync

### Extend Recurring – Schedule End Date / End Date Path – Updated Across All 5 Surfaces (SF + BO)

**Description:** AC 01.5 — Cross-system: End Date must update on all 5 surfaces after extending by End Date.

**Preconditions:**
Admin has created a daily recurring lesson schedule by End Date

- Current End Date = 2026-03-31
- Extension End Date = 2026-04-30

| #   | Action                                             | Expected Result                               | Test Data                 |
| --- | -------------------------------------------------- | --------------------------------------------- | ------------------------- |
| 1   | Extend Recurrence End Date to 2026-04-30 and save  | New lessons created successfully              | New End Date = 2026-04-30 |
| 2   | Check SF - Lesson Schedule detail page             | End Date = 2026-04-30                         | SF Lesson Schedule detail |
| 3   | Check SF - Lesson edit form                        | End Date = 2026-04-30                         | SF Lesson edit form       |
| 4   | Check SF - Lesson Calendar Related list            | Lessons visible up to 2026-04-30              | SF Calendar               |
| 5   | Login BO, check Lesson detail - Recurring settings | Recurring settings show End Date = 2026-04-30 | BO Lesson detail          |
| 6   | Check BO - Calendar Related list                   | Lessons visible up to 2026-04-30              | BO Calendar               |

---

### Extend Recurring – Schedule End Date / Lesson Count Path – Updated Across All 5 Surfaces (SF + BO)

**Description:** AC 01.5 — Cross-system: End Date derived from last lesson date must update on all 5 surfaces after extending by Lesson Count.

**Preconditions:**
Admin has created a daily recurring lesson schedule by Lesson Count

- Current Lesson Count = 10
- Extension to Lesson Count = 15

| #   | Action                                                                       | Expected Result                                | Test Data                      |
| --- | ---------------------------------------------------------------------------- | ---------------------------------------------- | ------------------------------ |
| 1   | Extend Lesson Count to 15 and save                                           | New lessons created successfully               | New Lesson Count = 15 (was 10) |
| 2   | Identify the last lesson date in the chain (e.g., 2026-04-20)                | Last lesson date determined (e.g., 2026-04-20) |                                |
| 3   | Check SF - Lesson Schedule detail page                                       | End Date = last lesson date (2026-04-20)       | SF Lesson Schedule detail      |
| 4   | Check SF - Lesson edit form                                                  | End Date = last lesson date                    | SF Lesson edit form            |
| 5   | Check SF - Lesson Calendar Related list                                      | Lessons visible up to last lesson date         | SF Calendar                    |
| 6   | Login BO, check Lesson detail - Recurring settings and Calendar Related list | End Date and Calendar reflect last lesson date | BO Lesson detail + Calendar    |

---

## Suite: Extend Recurrence Edit Following

### Extend Recurring – Apply This and Following – From Before Extension Point – Extended Lessons Updated

**Description:** AC 02.1 — State Transition + Regression: Editing from a lesson BEFORE the extension point must update all extended lessons.

**Preconditions:**
Admin has created a daily recurring lesson schedule with 5 original lessons
Extended by End Date creating 3 new lessons (total 8)
All lessons are in DRAFT or Published status

| #   | Action                                                                          | Expected Result                                                      | Test Data                                           |
| --- | ------------------------------------------------------------------------------- | -------------------------------------------------------------------- | --------------------------------------------------- |
| 1   | Open the 3rd lesson (before extension point)                                    | Lesson detail opens                                                  |                                                     |
| 2   | Click Edit, change lesson name to "Updated Lesson", change classroom to "Room B | Fields updated                                                       | Lesson name = "Updated Lesson", Classroom = "Room B |
| 3   | Select "Apply this and the following                                            | Recurring update option selected                                     |                                                     |
| 4   | Save                                                                            | Save successful                                                      |                                                     |
| 5   | Check lessons 3-5 (original chain after edit)                                   | Lessons 3-5: name = "Updated Lesson", classroom = "Room B            | Verify original chain updated                       |
| 6   | Check lessons 6-8 (extended lessons)                                            | Lessons 6-8 (extended): name = "Updated Lesson", classroom = "Room B | Verify extended chain updated                       |
| 7   | Check lessons 1-2 (before edit point)                                           | Lessons 1-2: unchanged (original values)                             | Verify previous lessons not affected                |

---

### Extend Recurring – Apply This and Following – From Chain Boundary – All Extended Lessons Updated

**Description:** AC 02.1 — State Transition: Edit the LAST lesson of the original chain and verify all extended lessons are updated.

**Preconditions:**
Admin has created a daily recurring lesson schedule with 5 original lessons
Extended by End Date creating 3 new lessons (total 8)

| #   | Action                                                  | Expected Result                      | Test Data                          |
| --- | ------------------------------------------------------- | ------------------------------------ | ---------------------------------- |
| 1   | Open the 5th lesson (last of original chain / boundary) | Lesson detail opens                  | Boundary lesson (last original)    |
| 2   | Click Edit, change lesson time to 14:00-15:00           | Time updated                         | New time = 14:00-15:00             |
| 3   | Select "Apply this and the following                    | Recurring update option selected     |                                    |
| 4   | Save                                                    | Save successful                      |                                    |
| 5   | Check lesson 5                                          | Lesson 5: time = 14:00-15:00         |                                    |
| 6   | Check lessons 6-8 (extended lessons)                    | Lessons 6-8: time = 14:00-15:00      | Verify extended chain updated      |
| 7   | Check lessons 1-4 (before boundary)                     | Lessons 1-4: original time unchanged | Verify previous chain not affected |

---

### Extend Recurring – One-time Lesson Edit – No Cascade to Recurring or Extended Lessons

**Description:** AC 02.1 — Decision Table + Negative Testing: Editing a one-time lesson must only affect that single lesson.

**Preconditions:**
Admin has created a recurring lesson schedule with extended lessons
A one-time lesson exists in the same Lesson Schedule (created via Add Lesson manually)

| #   | Action                                   | Expected Result                                  | Test Data                  |
| --- | ---------------------------------------- | ------------------------------------------------ | -------------------------- |
| 1   | Open the one-time (manual) lesson        | Lesson detail opens                              |                            |
| 2   | Click Edit, change lesson name and time  | Fields updated                                   | Edit name and time         |
| 3   | Save                                     | Save successful without recurring options        |                            |
| 4   | Verify no recurring popup is shown       | No "Apply this and the following" popup shown    |                            |
| 5   | Check all recurring and extended lessons | All recurring and extended lessons are unchanged | Verify no cascading effect |

---

### Extend Recurring – Apply This and Following – Manual Lesson Within Schedule – Isolated and Unchanged

**Description:** AC 02.1 — Negative Testing: Manually created lesson in the schedule must remain unchanged when recurring edit is applied.

**Preconditions:**
Admin has created a daily recurring lesson schedule with 5 lessons
Manually added a lesson (lesson manual) between lesson 3 and 4
Extended by End Date creating 3 new lessons

| #   | Action                                              | Expected Result                                                        | Test Data                                           |
| --- | --------------------------------------------------- | ---------------------------------------------------------------------- | --------------------------------------------------- |
| 1   | Open lesson 2 (before lesson manual)                | Lesson detail opens                                                    |                                                     |
| 2   | Click Edit, change lesson name to "Recurring Update | Name updated                                                           | New name = "Recurring Update                        |
| 3   | Select "Apply this and the following                | Recurring update selected                                              |                                                     |
| 4   | Save                                                | Save successful                                                        |                                                     |
| 5   | Check the manually created lesson                   | Manual lesson: name unchanged, NOT affected by recurring edit          | Manual lesson should be isolated                    |
| 6   | Check lessons 3-5 and extended lessons 6-8          | Lessons 3-8: name = "Recurring Update" (all recurring lessons updated) | All recurring lessons (original + extended) updated |

---

## Suite: Extend Recurrence Student Teacher

### Extend Recurring – Assign Student and Teacher / Apply This and Following – From Before Extension Point – Extended Lessons Included

**Description:** AC 02.2 — Pairwise + Regression: Assign from a lesson before the extension point, verify both old and extended lessons get the assignment.

**Preconditions:**
Admin has created a daily recurring lesson schedule with 5 original lessons
Extended by End Date creating 3 new lessons (total 8)
Student A and Teacher A exist and are eligible

| #   | Action                                              | Expected Result                                            | Test Data             |
| --- | --------------------------------------------------- | ---------------------------------------------------------- | --------------------- |
| 1   | Open lesson 2 (before extension point)              | Lesson detail opens                                        |                       |
| 2   | Assign Student A with "Apply this and the following | Student A assigned                                         | Student = Student A   |
| 3   | Assign Teacher A with "Apply this and the following | Teacher A assigned                                         | Teacher = Teacher A   |
| 4   | Check lessons 2-5 (original chain)                  | Student A and Teacher A assigned to lessons 2-5            | Verify original chain |
| 5   | Check lessons 6-8 (extended lessons)                | Student A and Teacher A assigned to lessons 6-8 (extended) | Verify extended chain |
| 6   | Check lesson 1 (before assignment point)            | Lesson 1: no Student A or Teacher A                        | Not affected          |
| 7   | Student A login Mobile                              | Student A sees lessons 2-8 with correct information        | Mobile verification   |

---

### Extend Recurring – Assign Student and Teacher / Apply This and Following – From Within Extended Range – Following Extended Lessons Included

**Description:** AC 02.2 — Pairwise: Assign from an extended lesson, verify only following extended lessons get the assignment.

**Preconditions:**
Admin has created a recurring lesson schedule
Extended creating 5 new lessons (lessons 6-10)
Student B and Teacher B exist

| #   | Action                                                            | Expected Result                                 | Test Data                                |
| --- | ----------------------------------------------------------------- | ----------------------------------------------- | ---------------------------------------- |
| 1   | Open lesson 7 (2nd extended lesson)                               | Lesson detail opens                             |                                          |
| 2   | Assign Student B and Teacher B with "Apply this and the following | Student B and Teacher B assigned                | Student = Student B, Teacher = Teacher B |
| 3   | Check lessons 7-10 (following extended lessons)                   | Student B and Teacher B present in lessons 7-10 | Verify following extended lessons        |
| 4   | Check lessons 1-6 (original + first extended)                     | Lessons 1-6: no Student B or Teacher B          | Not affected                             |

---

### Extend Recurring – Unassign Student and Teacher / Apply This and Following – Extended Lessons Included, Allocation Data Updated

**Description:** AC 02.2 — Regression: Unassign from before extension point, verify removal in all following lessons including extended.

**Preconditions:**
Admin has created a recurring lesson schedule, extended with new lessons
Student A and Teacher A assigned to all lessons (1-8) via "Apply this and the following"

| #   | Action                                                     | Expected Result                                                                                                                      | Test Data                                                  |
| --- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------- |
| 1   | Open lesson 3                                              | Lesson detail opens                                                                                                                  |                                                            |
| 2   | Unassign Student A with "Apply this and the following      | Student A removed                                                                                                                    | Unassign Student A                                         |
| 3   | Unassign Teacher A with "Apply this and the following      | Teacher A removed                                                                                                                    | Unassign Teacher A                                         |
| 4   | Check lessons 3-8 (original + extended after unassignment) | No Student A or Teacher A in lessons 3-8                                                                                             | Verify removal in all following                            |
| 5   | Check lessons 1-2 (before unassignment point)              | Lessons 1-2: Student A and Teacher A still present                                                                                   | Not affected                                               |
| 6   | Check lesson allocation for Student A                      | Student sessions deleted for affected lessons, Lesson Allocated count decreased, Lesson Allocation Status and Report History updated | Check: Lesson Allocated, Allocation Status, Report History |

---

### Extend Recurring – Assign Student / Apply This and Following – Manual Lesson Within Schedule – Included in Assignment

**Description:** AC 02.2 — CRUD + Regression: Student/teacher assignment via following must also include manually created lesson in the schedule.

**Preconditions:**
Admin has created a recurring lesson schedule with 5 lessons
Manually added a lesson between lesson 3 and 4
Extended creating 3 new lessons (total 9 including manual)
Student C exists

| #   | Action                                                             | Expected Result                                                                      | Test Data                                             |
| --- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------ | ----------------------------------------------------- |
| 1   | Open lesson 2 (before manual lesson)                               | Lesson detail opens                                                                  |                                                       |
| 2   | Assign Student C with "Apply this and the following                | Student C assigned                                                                   | Student = Student C                                   |
| 3   | Check the manually created lesson                                  | Manual lesson: Student C is assigned                                                 | Manual lesson receives assignment                     |
| 4   | Check remaining recurring lessons (3-5) and extended lessons (6-8) | All recurring and extended lessons: Student C is assigned                            | Both original and extended lessons receive assignment |
| 5   | Check lesson allocation for Student C                              | Lesson Allocated count includes all assigned lessons (manual + recurring + extended) | Verify complete allocation data                       |

---

## Suite: Extend After Chain Modification

### Extend Recurring – End Date Path – After Manual Lesson Added Beyond Chain End – Conflict Date Skipped

**Description:** Additional Logic #34 — Regression: After adding a manual lesson with a date beyond the chain's last recurring lesson, extend by end date. Verify extension uses the chain's end date (not manual lesson date) and skips the manual lesson date.

**Preconditions:**
Admin has created a daily recurring lesson schedule by End Date

- End Date = 2026-03-20 (5 lessons in chain, last lesson = 2026-03-20)
- Admin manually added a one-time lesson on 2026-03-25 via "Add Lesson" flow

| #   | Action                                                    | Expected Result                                                | Test Data                                                 |
| --- | --------------------------------------------------------- | -------------------------------------------------------------- | --------------------------------------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence"           | Lesson Creation Form opens                                     |                                                           |
| 2   | Check auto-calculated Date field                          | Date = 2026-03-27 (chain end date 2026-03-20 + 7)              | Chain End Date = 2026-03-20, auto-calculated = 2026-03-27 |
| 3   | Extend Recurrence End Date to 2026-04-15                  | Date accepted                                                  | New End Date = 2026-04-15                                 |
| 4   | Save the form                                             | New lessons created                                            |                                                           |
| 5   | Check if a new lesson is created on 2026-03-25            | No new lesson on 2026-03-25 (skipped — manual lesson exists)   | Conflict date = 2026-03-25                                |
| 6   | Check manually added lesson on 2026-03-25                 | Manual lesson unchanged                                        |                                                           |
| 7   | Check all new lessons status and Lesson Schedule End Date | All new lessons = DRAFT, Lesson Schedule End Date = 2026-04-15 |                                                           |

---

### Extend Recurring – Lesson Count Path – After Manual Lesson Added Beyond Chain End – Conflict Date Skipped

**Description:** Additional Logic #35 — Regression: After adding a manual lesson beyond chain end, extend by lesson count. Verify new lessons follow recurrence pattern and skip the manual lesson date.

**Preconditions:**
Admin has created a daily recurring lesson schedule by Lesson Count

- Current Lesson Count = 5 (last lesson = 2026-03-20)
- Admin manually added a one-time lesson on 2026-03-25 via "Add Lesson" flow

| #   | Action                                                    | Expected Result                                                             | Test Data                         |
| --- | --------------------------------------------------------- | --------------------------------------------------------------------------- | --------------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence"           | Lesson Creation Form opens                                                  |                                   |
| 2   | Increase Lesson Count to 10                               | Value accepted                                                              | New Lesson Count = 10 (was 5, +5) |
| 3   | Save the form                                             | New lessons created                                                         |                                   |
| 4   | Check if a new lesson is created on 2026-03-25            | No new lesson on 2026-03-25 (skipped — manual lesson exists)                | Conflict date = 2026-03-25        |
| 5   | Check total recurring lessons in chain (excluding manual) | Total recurring lessons = 10, skipped date compensated by additional lesson | Expected: 10 recurring + 1 manual |
| 6   | Verify Lesson Schedule End Date updated                   | End Date = last lesson date of the chain                                    | Derived from last new lesson      |

---

### Extend Recurring – End Date Path – After Last Lesson Date Edited Later – Extension Calculates from Updated End Date

**Description:** Additional Logic #36 — Regression: After editing the last lesson's date to a later date, extend by end date. Verify extension calculates from the updated schedule end date.

**Preconditions:**
Admin has created a daily recurring lesson schedule by End Date

- Original End Date = 2026-03-20 (5 lessons)
- Admin edited lesson 5 date from 2026-03-20 to 2026-03-25 with "Only this lesson"
- Schedule End Date now = 2026-03-25

| #   | Action                                          | Expected Result                                     | Test Data                                             |
| --- | ----------------------------------------------- | --------------------------------------------------- | ----------------------------------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence" | Lesson Creation Form opens                          |                                                       |
| 2   | Check auto-calculated Date field                | Date = 2026-04-01 (updated end date 2026-03-25 + 7) | Updated End Date = 2026-03-25, auto Date = 2026-04-01 |
| 3   | Extend Recurrence End Date to 2026-04-30        | Date accepted                                       | New End Date = 2026-04-30                             |
| 4   | Save the form                                   | New lessons created with DRAFT status               |                                                       |
| 5   | Check Lesson Schedule End Date                  | End Date = 2026-04-30                               |                                                       |

---

### Extend Recurring – Lesson Count Path – After Last Lesson Date Edited Later – New Lessons Follow Updated Chain End

**Description:** Additional Logic #37 — Regression: After editing the last lesson date forward, extend by lesson count. Verify new lessons follow from the updated schedule end date.

**Preconditions:**
Admin has created a daily recurring lesson schedule by Lesson Count

- Current Lesson Count = 5 (last lesson = 2026-03-20)
- Admin edited lesson 5 date from 2026-03-20 to 2026-03-25 with "Only this lesson"

| #   | Action                                          | Expected Result                                                  | Test Data                         |
| --- | ----------------------------------------------- | ---------------------------------------------------------------- | --------------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence" | Lesson Creation Form opens                                       |                                   |
| 2   | Increase Lesson Count to 10                     | Value accepted                                                   | New Lesson Count = 10 (was 5, +5) |
| 3   | Save the form                                   | New lessons created with DRAFT status                            |                                   |
| 4   | Check new lesson dates                          | New lessons follow daily pattern starting after updated end date | Start from after 2026-03-25       |
| 5   | Verify Lesson Schedule End Date                 | End Date = last new lesson date                                  |                                   |

---

## Suite: Extend After Last Lesson Status Change

### Extend Recurring – End Date Path – Last Lesson Completed – Completed Lesson Unchanged, New Lessons Added as DRAFT

**Description:** Additional Logic #38 — State Transition: After completing the last lesson, extend by end date. Completed lesson remains completed, new lessons created as DRAFT.

**Preconditions:**
Admin has created a daily recurring lesson schedule by End Date

- End Date = 2026-03-20 (5 lessons)
- Lesson 5 (last, 2026-03-20) status changed to Completed

| #   | Action                                          | Expected Result                               | Test Data                 |
| --- | ----------------------------------------------- | --------------------------------------------- | ------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence" | Lesson Creation Form opens (button available) |                           |
| 2   | Extend Recurrence End Date to 2026-04-15        | Date accepted                                 | New End Date = 2026-04-15 |
| 3   | Save the form                                   | New lessons created                           |                           |
| 4   | Check lesson 5 (completed lesson) status        | Lesson 5 remains Completed                    | Status = Completed        |
| 5   | Check all new lessons status                    | All new lessons = DRAFT                       | Expected: DRAFT           |
| 6   | Verify Lesson Schedule End Date                 | End Date = 2026-04-15                         |                           |

---

### Extend Recurring – Lesson Count Path – Last Lesson Completed – New Lessons Added as DRAFT

**Description:** Additional Logic #39 — State Transition: After completing the last lesson, extend by lesson count. Completed lesson unchanged, new lessons created as DRAFT.

**Preconditions:**
Admin has created a daily recurring lesson schedule by Lesson Count

- Current Lesson Count = 5
- Lesson 5 (last) status = Completed

| #   | Action                                          | Expected Result            | Test Data                         |
| --- | ----------------------------------------------- | -------------------------- | --------------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence" | Lesson Creation Form opens |                                   |
| 2   | Increase Lesson Count to 10                     | Value accepted             | New Lesson Count = 10 (was 5, +5) |
| 3   | Save the form                                   | New lessons created        |                                   |
| 4   | Check lesson 5 status                           | Remains Completed          |                                   |
| 5   | Check all 5 new lessons status                  | All new lessons = DRAFT    | Expected: DRAFT for all 5 new     |
| 6   | Check total lessons count                       | Total = 10                 |                                   |

---

### Extend Recurring – End Date Path – Last Lesson Cancelled – Cancelled Lesson Excluded from Following Edit, New Lessons DRAFT

**Description:** Additional Logic #40 — State Transition: After cancelling the last lesson, extend by end date. Cancelled lesson unchanged, new lessons created as DRAFT.

**Preconditions:**
Admin has created a daily recurring lesson schedule by End Date

- End Date = 2026-03-20 (5 lessons)
- Lesson 5 (last) status = Cancelled

| #   | Action                                                 | Expected Result                                              | Test Data                                            |
| --- | ------------------------------------------------------ | ------------------------------------------------------------ | ---------------------------------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence"        | Lesson Creation Form opens                                   |                                                      |
| 2   | Extend Recurrence End Date to 2026-04-15               | Date accepted                                                | New End Date = 2026-04-15                            |
| 3   | Save the form                                          | New lessons created                                          |                                                      |
| 4   | Check lesson 5 (cancelled) status                      | Lesson 5 remains Cancelled                                   | Status = Cancelled                                   |
| 5   | Check all new lessons status                           | All new lessons = DRAFT                                      |                                                      |
| 6   | Edit from lesson 4 with "Apply this and the following" | Lesson 4 + new lessons updated, lesson 5 skipped (cancelled) | Verify cancelled lesson excluded from following edit |

---

### Extend Recurring – Lesson Count Path – Last Lesson Cancelled – New Lessons Added as DRAFT

**Description:** Additional Logic #41 — State Transition: After cancelling the last lesson, extend by lesson count. New lessons created as DRAFT, cancelled lesson unchanged.

**Preconditions:**
Admin has created a daily recurring lesson schedule by Lesson Count

- Current Lesson Count = 5
- Lesson 5 (last) status = Cancelled

| #   | Action                                          | Expected Result                           | Test Data                         |
| --- | ----------------------------------------------- | ----------------------------------------- | --------------------------------- |
| 1   | Open Lesson Schedule, click "Extend Recurrence" | Lesson Creation Form opens                |                                   |
| 2   | Increase Lesson Count to 10                     | Value accepted                            | New Lesson Count = 10 (was 5, +5) |
| 3   | Save the form                                   | New lessons created                       |                                   |
| 4   | Check lesson 5 status                           | Remains Cancelled                         |                                   |
| 5   | Check all 5 new lessons status                  | All new lessons = DRAFT                   | Expected: DRAFT                   |
| 6   | Check total lessons in chain                    | Total = 10 (including cancelled lesson 5) |                                   |

---

## Suite: BO Operations After Extension

### Extend Recurring – BO Edit / Apply This and Following – After End Date Extension – Original and Extended Lessons Updated

**Description:** Additional Logic #42 — Regression: After extending by end date, edit a recurring lesson on BO. Verify edit propagates to both original and extended lessons, and changes reflect on SF.

**Preconditions:**
Admin has created a daily recurring lesson schedule with 5 original lessons
Extended by End Date creating 3 new lessons (total 8)
All lessons are in DRAFT or Published status

| #   | Action                                                | Expected Result                                                | Test Data                                      |
| --- | ----------------------------------------------------- | -------------------------------------------------------------- | ---------------------------------------------- |
| 1   | Login BO, open lesson 3 detail                        | Lesson detail opens on BO                                      |                                                |
| 2   | Edit lesson name to "BO Updated", time to 14:00-15:00 | Fields updated                                                 | Lesson name = "BO Updated", Time = 14:00-15:00 |
| 3   | Select "Apply this and the following"                 | Recurring update option selected                               |                                                |
| 4   | Save                                                  | Save successful                                                |                                                |
| 5   | Check lessons 3-5 on BO (original chain)              | Lessons 3-5: name = "BO Updated", time = 14:00-15:00           | Verify original chain                          |
| 6   | Check lessons 6-8 on BO (extended lessons)            | Lessons 6-8: name = "BO Updated", time = 14:00-15:00           | Verify extended chain                          |
| 7   | Check lessons 1-2 on BO                               | Lessons 1-2: unchanged                                         | Not affected                                   |
| 8   | Verify changes reflected on SF                        | All changes visible on SF Lesson Schedule and Lesson edit form | Cross-system sync                              |

---

### Extend Recurring – BO Edit / Apply This and Following – After Lesson Count Extension – Original and Extended Lessons Updated

**Description:** Additional Logic #43 — Regression: After extending by lesson count, edit a lesson on BO and verify propagation to extended lessons.

**Preconditions:**
Admin has created a daily recurring lesson schedule by Lesson Count

- Original Lesson Count = 5, Extended to 8 (3 new lessons)

| #   | Action                                                  | Expected Result                                  | Test Data                                        |
| --- | ------------------------------------------------------- | ------------------------------------------------ | ------------------------------------------------ |
| 1   | Login BO, open lesson 2 detail                          | Lesson detail opens on BO                        |                                                  |
| 2   | Edit classroom to "Room C", teaching medium to "Online" | Fields updated                                   | Classroom = "Room C", Teaching Medium = "Online" |
| 3   | Select "Apply this and the following"                   | Recurring update option selected                 |                                                  |
| 4   | Save                                                    | Save successful                                  |                                                  |
| 5   | Check lessons 2-5 (original chain after edit)           | Classroom = "Room C", Teaching Medium = "Online" | Verify original                                  |
| 6   | Check lessons 6-8 (extended lessons)                    | Classroom = "Room C", Teaching Medium = "Online" | Verify extended                                  |
| 7   | Verify changes on SF                                    | All changes reflected on SF                      | Cross-system                                     |

---

### Extend Recurring – BO Assign Student / Apply This and Following – After End Date Extension – Extended Lessons Included

**Description:** Additional Logic #44 — Regression: After extending by end date, assign a student on BO with "Apply this and the following". Verify student assigned to all following lessons including extended.

**Preconditions:**
Admin has created a daily recurring lesson schedule with 5 original lessons
Extended by End Date creating 3 new lessons (total 8)
Student D exists and is eligible

| #   | Action                                               | Expected Result                          | Test Data           |
| --- | ---------------------------------------------------- | ---------------------------------------- | ------------------- |
| 1   | Login BO, open lesson 3 detail                       | Lesson detail opens on BO                |                     |
| 2   | Assign Student D with "Apply this and the following" | Student D assigned                       | Student = Student D |
| 3   | Check lessons 3-5 on BO                              | Student D assigned to lessons 3-5        | Original chain      |
| 4   | Check lessons 6-8 on BO (extended)                   | Student D assigned to lessons 6-8        | Extended chain      |
| 5   | Check lessons 1-2 on BO                              | No Student D                             | Not affected        |
| 6   | Verify Student D session on SF                       | Student sessions created for lessons 3-8 | Cross-system        |

---

### Extend Recurring – BO Assign Student / Apply This and Following – After Lesson Count Extension – Extended Lessons Included

**Description:** Additional Logic #45 — Regression: After extending by lesson count, assign student on BO and verify propagation to extended lessons.

**Preconditions:**
Admin has created a daily recurring lesson schedule by Lesson Count
Extended from 5 to 8 lessons (3 new)
Student E exists and is eligible

| #   | Action                                               | Expected Result                      | Test Data             |
| --- | ---------------------------------------------------- | ------------------------------------ | --------------------- |
| 1   | Login BO, open lesson 2 detail                       | Lesson detail opens                  |                       |
| 2   | Assign Student E with "Apply this and the following" | Student E assigned                   | Student = Student E   |
| 3   | Check lessons 2-8 on BO                              | Student E present in all lessons 2-8 | All following lessons |
| 4   | Check lesson 1                                       | No Student E                         | Not affected          |
| 5   | Verify Lesson Allocated count for Student E          | Student sessions = 7 (lessons 2-8)   | Allocation data       |

---

### Extend Recurring – BO Assign Teacher / Apply This and Following – After End Date Extension – Extended Lessons Included

**Description:** Additional Logic #46 — Regression: After extending by end date, assign teacher on BO and verify propagation to extended lessons.

**Preconditions:**
Admin has created a daily recurring lesson schedule with 5 original lessons
Extended by End Date creating 3 new lessons (total 8)
Teacher B exists and is eligible

| #   | Action                                                 | Expected Result                                         | Test Data           |
| --- | ------------------------------------------------------ | ------------------------------------------------------- | ------------------- |
| 1   | Login BO, open lesson 3 detail                         | Lesson detail opens on BO                               |                     |
| 2   | Assign Teacher B with "Apply this and the following"   | Teacher B assigned                                      | Teacher = Teacher B |
| 3   | Check lessons 3-8 on BO                                | Teacher B assigned to lessons 3-8 (original + extended) |                     |
| 4   | Check lessons 1-2 on BO                                | No Teacher B                                            | Not affected        |
| 5   | Verify on SF — teacher appears in all affected lessons | Teacher B visible on SF lesson details                  | Cross-system        |

---

### Extend Recurring – BO Assign Teacher / Apply This and Following – After Lesson Count Extension – Extended Lessons Included

**Description:** Additional Logic #47 — Regression: After extending by lesson count, assign teacher on BO and verify propagation to extended lessons.

**Preconditions:**
Admin has created a daily recurring lesson schedule by Lesson Count
Extended from 5 to 8 (3 new lessons)
Teacher C exists and is eligible

| #   | Action                                               | Expected Result           | Test Data           |
| --- | ---------------------------------------------------- | ------------------------- | ------------------- |
| 1   | Login BO, open lesson 4 detail                       | Lesson detail opens on BO |                     |
| 2   | Assign Teacher C with "Apply this and the following" | Teacher C assigned        | Teacher = Teacher C |
| 3   | Check lessons 4-8                                    | Teacher C present in all  | All following       |
| 4   | Check lessons 1-3                                    | No Teacher C              | Not affected        |
| 5   | Verify Lesson Teacher section on SF                  | Teacher C visible on SF   | Cross-system        |

---

## Suite: Zoom Link Generation After Extension

### Extend Recurring – Zoom Link – After End Date Extension – Generated for New Lessons on BO

**Description:** Additional Logic #48 — Regression: After extending by end date, generate zoom link on BO. Verify zoom links created for new extended lessons.

**Preconditions:**
Admin has created a daily recurring lesson schedule with Teaching Medium = Online

- 5 original lessons with zoom links generated
- Extended by End Date creating 3 new lessons

| #   | Action                                   | Expected Result                                          | Test Data          |
| --- | ---------------------------------------- | -------------------------------------------------------- | ------------------ |
| 1   | Login BO, navigate to Lesson Schedule    | Schedule shows 8 total lessons (5 original + 3 extended) |                    |
| 2   | Check new lessons (6-8) zoom link status | New lessons have no zoom link (not auto-generated)       | No zoom link       |
| 3   | Generate zoom link for all lessons on BO | Zoom link generation initiated                           |                    |
| 4   | Check new lessons (6-8) zoom links       | Zoom links created for lessons 6-8                       | Zoom links present |
| 5   | Check original lessons (1-5) zoom links  | Original zoom links unchanged                            | Not affected       |

---

### Extend Recurring – Zoom Link – After Lesson Count Extension – Generated for New Lessons on BO

**Description:** Additional Logic #49 — Regression: After extending by lesson count, generate zoom link on BO for new lessons.

**Preconditions:**
Admin has created a daily recurring lesson schedule with Teaching Medium = Online

- Lesson Count = 5 with zoom links generated
- Extended Lesson Count to 8 (3 new lessons)

| #   | Action                                   | Expected Result                          | Test Data          |
| --- | ---------------------------------------- | ---------------------------------------- | ------------------ |
| 1   | Login BO, check new lessons (6-8)        | New lessons exist with no zoom link      |                    |
| 2   | Generate zoom link for new lessons on BO | Zoom link generation initiated           |                    |
| 3   | Check lessons 6-8 zoom links             | Zoom links created for all 3 new lessons | Zoom links present |
| 4   | Check lessons 1-5 zoom links             | Original zoom links unchanged            | Not affected       |

---

## Suite: Apply to Specific Number of Lessons After Extension

### Extend Recurring – Edit / Apply to Specific Number – Count Spans into Extended Range – Exact Count of Lessons Updated

**Description:** AC 02.1 — State Transition: Edit from an original lesson with "Apply to the specific number lessons" where the count spans into the extended range. Verify changes applied to exact count of following lessons.

**Preconditions:**
Admin has created a daily recurring lesson schedule with 5 original lessons
Extended by End Date creating 5 new lessons (total 10)
All lessons are in DRAFT or Published status

| #   | Action                                                                               | Expected Result                  | Test Data                        |
| --- | ------------------------------------------------------------------------------------ | -------------------------------- | -------------------------------- |
| 1   | Open lesson 3 (original chain)                                                       | Lesson detail opens              |                                  |
| 2   | Edit lesson name to "Specific Update", select "Apply to the specific number lessons" | Edit options shown               | Lesson name = "Specific Update"  |
| 3   | Set number of lessons = 5 (spans lessons 3-7, crossing into extended range)          | Value accepted                   | Number = 5, covers lessons 3-7   |
| 4   | Save                                                                                 | Save successful                  |                                  |
| 5   | Check lessons 3-5 (original chain)                                                   | Name = "Specific Update"         | Updated                          |
| 6   | Check lessons 6-7 (first 2 extended lessons)                                         | Name = "Specific Update"         | Updated (within specified count) |
| 7   | Check lessons 8-10 (remaining extended lessons)                                      | Name unchanged (original values) | Not affected (beyond count)      |
| 8   | Check lessons 1-2 (before edit point)                                                | Name unchanged                   | Not affected                     |

---

### Extend Recurring – Assign Student / Apply to Specific Number – Count Spans into Extended Range – Exact Count of Lessons Assigned

**Description:** AC 02.2 — Regression: Assign student from before extension point with a specific number that crosses into extended lessons range.

**Preconditions:**
Admin has created a daily recurring lesson schedule with 5 original lessons
Extended creating 5 new lessons (total 10)
Student F exists and is eligible

| #   | Action                                                                      | Expected Result          | Test Data                      |
| --- | --------------------------------------------------------------------------- | ------------------------ | ------------------------------ |
| 1   | Open lesson 4 (original chain)                                              | Lesson detail opens      |                                |
| 2   | Assign Student F with "Apply to the specific number lessons"                | Assignment options shown | Student = Student F            |
| 3   | Set number of lessons = 4 (spans lessons 4-7, crossing into extended range) | Value accepted           | Number = 4, covers lessons 4-7 |
| 4   | Save                                                                        | Student F assigned       |                                |
| 5   | Check lessons 4-5 (original)                                                | Student F assigned       | Updated                        |
| 6   | Check lessons 6-7 (extended, within count)                                  | Student F assigned       | Updated                        |
| 7   | Check lessons 8-10 (extended, beyond count)                                 | No Student F             | Not affected                   |
| 8   | Check lessons 1-3 (before point)                                            | No Student F             | Not affected                   |

---

### Extend Recurring – Assign Teacher / Apply to Specific Number – Count Spans into Extended Range – Exact Count of Lessons Assigned

**Description:** AC 02.2 — Regression: Assign teacher from before extension point with a specific number that crosses into extended lessons range.

**Preconditions:**
Admin has created a daily recurring lesson schedule with 5 original lessons
Extended creating 5 new lessons (total 10)
Teacher D exists and is eligible

| #   | Action                                                                      | Expected Result          | Test Data                      |
| --- | --------------------------------------------------------------------------- | ------------------------ | ------------------------------ |
| 1   | Open lesson 3 (original chain)                                              | Lesson detail opens      |                                |
| 2   | Assign Teacher D with "Apply to the specific number lessons"                | Assignment options shown | Teacher = Teacher D            |
| 3   | Set number of lessons = 6 (spans lessons 3-8, crossing into extended range) | Value accepted           | Number = 6, covers lessons 3-8 |
| 4   | Save                                                                        | Teacher D assigned       |                                |
| 5   | Check lessons 3-5 (original)                                                | Teacher D assigned       | Updated                        |
| 6   | Check lessons 6-8 (extended, within count)                                  | Teacher D assigned       | Updated                        |
| 7   | Check lessons 9-10 (extended, beyond count)                                 | No Teacher D             | Not affected                   |
| 8   | Check lessons 1-2 (before point)                                            | No Teacher D             | Not affected                   |

---
