# Test Cases: LT-90573 — Extend Recurring Lesson Settings

## Suite: Extend Recurrence Button

###  Admin verifies Extend Recurrence button visible on recurring lesson schedule

**Description:** AC 01.1 / AC 01.3 — Decision Table: Verify button is present for all recurring schedule types (daily, weekly, custom).

**Preconditions:**
Admin user has created:
- A daily recurring lesson schedule
- A weekly recurring lesson schedule
- A custom recurring lesson schedule

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule detail page of the daily recurring lesson | User sees "Extend Recurrence" button |  |
| 2 | Open Lesson Schedule detail page of the weekly recurring lesson | User sees "Extend Recurrence" button |  |
| 3 | Open Lesson Schedule detail page of the custom recurring lesson | User sees "Extend Recurrence" button |  |

---

###  Extend Recurrence button hidden for one-time lesson schedule

**Description:** AC 01.3 — Decision Table: Button must not appear when is_recurring = FALSE (one-time lesson).

**Preconditions:**
Admin user has created a one-time lesson schedule

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule detail page of the one-time lesson | User does NOT see "Extend Recurrence" button |  |
| 2 | Inspect action buttons area | Only applicable action buttons are shown (no Extend Recurrence) |  |

---

###  Extend Recurrence button hidden for course schedule lesson

**Description:** AC 01.3 — Decision Table: Button must not appear for course schedule lessons.

**Preconditions:**
Admin user has created a course schedule lesson

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule detail page of the course schedule lesson | User does NOT see "Extend Recurrence" button |  |
| 2 | Inspect action buttons area | Only applicable action buttons are shown (no Extend Recurrence) |  |

---

###  Click Extend Recurrence button opens Lesson Creation Form

**Description:** AC 01.1 — Verify clicking the button opens the Lesson Creation Form with correct initial state.

**Preconditions:**
Admin user has created a daily recurring lesson schedule

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule detail page | User sees "Extend Recurrence" button |  |
| 2 | Click "Extend Recurrence" button | Lesson Creation Form opens with fields pre-filled according to the Lesson Schedule |  |

---

## Suite: Extend Recurrence Form

###  Verify pre-filled editable fields from Lesson Schedule

**Description:** AC 01.2 — Equivalence Partitioning: Verify Start Time, End Time, Duration, Teaching Medium, Lesson Name are pre-filled and editable.

**Preconditions:**
Admin has created a recurring lesson schedule with:
- Start Time = 09:00
- End Time = 10:00
- Duration = 60 min
- Teaching Medium = Offline
- Lesson Name = "Math Recurring"

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens |  |
| 2 | Verify pre-filled values: Start Time, End Time, Duration, Teaching Medium, Lesson Name | Start Time = 09:00, End Time = 10:00, Duration = 60 min, Teaching Medium = Offline, Lesson Name = "Math Recurring | Source: Lesson Schedule |
| 3 | Edit Start Time to 10:00, End Time to 11:00, Lesson Name to "Math Extended | Fields accept new values successfully | New Start Time = 10:00, New End Time = 11:00, New Lesson Name = "Math Extended |

---

###  Verify Date auto-calculated as current end date + 7 days

**Description:** AC 01.2 — BVA: Date field must equal Lesson Schedule current end date + 7 days and be non-editable.

**Preconditions:**
Admin has created a recurring lesson schedule with End Date = 2026-03-10 (Tuesday)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens |  |
| 2 | Check the Date field value | Date = 2026-03-17 (Tuesday, end date + 7 days) | End Date = 2026-03-10, Expected Date = 2026-03-17 |
| 3 | Attempt to edit the Date field | Date field is locked / non-editable |  |

---

###  Verify Lesson Code auto-calculated as last existing code + 1

**Description:** AC 01.2 — BVA: Lesson Code = last existing lesson code + 1.

**Preconditions:**
Admin has created a recurring lesson schedule with last lesson having lesson code = 10

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens |  |
| 2 | Check the Lesson Code field | Lesson Code = 11 (last code 10 + 1) | Last existing lesson code = 10, Expected = 11 |

---

###  Verify Day of Week auto-calculated from Date

**Description:** AC 01.2 — Verify Day of the Week is automatically derived from the auto-calculated Date.

**Preconditions:**
Admin has created a recurring lesson schedule with End Date = 2026-03-13 (Friday)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens, Date = 2026-03-20 | End Date = 2026-03-13 (Friday) |
| 2 | Check Day of the Week field | Day of the Week = Friday (matching 2026-03-20) | Expected: Friday |

---

###  Verify Lesson Type defaults to Regular and Lesson Capacity is blank

**Description:** AC 01.2 — Equivalence Partitioning: Lesson Type = Regular (editable), Lesson Capacity = blank (optional).

**Preconditions:**
Admin has created a recurring lesson schedule

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens |  |
| 2 | Check Lesson Type field | Lesson Type = Regular | Default = Regular |
| 3 | Check Lesson Capacity field | Lesson Capacity is blank | Optional field |
| 4 | Change Lesson Type to a different value | Lesson Type field accepts the new value |  |

---

###  Verify Classroom is searchable dropdown

**Description:** AC 01.2 — Verify Classroom field is a searchable dropdown showing available classrooms.

**Preconditions:**
Admin has created a recurring lesson schedule
Multiple classrooms available at the location: Room A, Room B, Room C

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens |  |
| 2 | Click on Classroom dropdown | Dropdown shows available classrooms list | Available: Room A, Room B, Room C |
| 3 | Type "Room A" in the search field | Dropdown filters to show only "Room A | Search keyword = "Room A |
| 4 | Select Room A from the filtered result | Room A is selected as classroom |  |

---

###  Verify locked fields cannot be edited (Location, Academic Year, Course, Class, Teaching Method)

**Description:** AC 01.2 — Negative Testing: Attempt to edit each locked field; all must remain read-only.

**Preconditions:**
Admin has created a recurring lesson schedule with:
- Location = Tokyo
- Academic Year = 2025-2026
- Course = Mathematics
- Class = Class A
- Teaching Method = Group

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens |  |
| 2 | Verify Location field shows "Tokyo" and attempt to edit | Location = "Tokyo", field is locked (non-editable) | Source: Lesson Schedule |
| 3 | Verify Academic Year field shows "2025-2026" and attempt to edit | Academic Year = "2025-2026", field is locked | Source: Lesson Schedule |
| 4 | Verify Course field shows "Mathematics" and attempt to edit | Course = "Mathematics", field is locked | Source: Lesson Schedule |
| 5 | Verify Class field shows "Class A" and attempt to edit | Class = "Class A", field is locked | Source: Lesson Schedule |
| 6 | Verify Teaching Method field shows "Group" and attempt to edit | Teaching Method = "Group", field is locked | Source: Lesson Schedule |

---

###  Verify Recurring Settings inherited and non-editable (Recurrence Type, Days, Skip Closed Dates)

**Description:** AC 01.2 — Negative Testing: Recurrence Type, Recurrence Days, and Skip Closed Dates must display saved values and be non-editable.

**Preconditions:**
Admin has created a custom recurring lesson with:
- Recurrence Type = Custom
- Recurrence Days = Monday, Wednesday, Friday
- Skip Closed Dates = checked

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens with Recurring Settings section |  |
| 2 | Check Recurrence Type field | Recurrence Type = Custom (displayed, not editable) | Source: Lesson Schedule |
| 3 | Check Recurrence Days field | Recurrence Days = Monday, Wednesday, Friday (displayed, not editable) | Source: Lesson Schedule |
| 4 | Check Skip Closed Dates field | Skip Closed Dates = checked (displayed, not editable) | Source: Lesson Schedule |
| 5 | Attempt to edit Recurrence Type | Field is locked, cannot be changed |  |
| 6 | Attempt to edit Skip Closed Dates | Field is locked, cannot be changed |  |

---

###  Extend Recurrence End Date to a later date - accepted

**Description:** AC 01.2 / AC 01.3 — BVA: Verify user can extend End Date to 1 day after current and to far future.

**Preconditions:**
Admin has created a recurring lesson schedule by End Date
- Current Recurrence End Date = 2026-03-31

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens, Recurrence End Date = 2026-03-31 | Current End Date = 2026-03-31 |
| 2 | Set Recurrence End Date = 2026-04-01 (1 day after current) | Date accepted by the system | BVA: Boundary + 1 day |
| 3 | Save the form | New lessons are created successfully |  |
| 4 | Repeat: Set Recurrence End Date = 2026-12-31 (far future) | Date accepted by the system | BVA: Far future value |
| 5 | Save the form | New lessons are created successfully |  |

---

###  Reject Recurrence End Date equal to or earlier than current

**Description:** AC 01.2 / AC 01.3 — BVA + Negative Testing: System must reject same date and earlier date.

**Preconditions:**
Admin has created a recurring lesson schedule by End Date
- Current Recurrence End Date = 2026-03-31

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens, Recurrence End Date = 2026-03-31 | Current End Date = 2026-03-31 |
| 2 | Set Recurrence End Date = 2026-03-31 (same as current) | System does not allow or shows validation error | BVA: Exact boundary (same date) |
| 3 | Attempt to save | Save is rejected / blocked |  |
| 4 | Set Recurrence End Date = 2026-03-15 (earlier than current) | System does not allow or shows validation error | BVA: Below boundary (earlier date) |
| 5 | Attempt to save | Save is rejected / blocked |  |

---

###  Increase Lesson Count above current value - accepted

**Description:** AC 01.2 / AC 01.3 — BVA: Verify user can increase Lesson Count by 1 and by a large amount.

**Preconditions:**
Admin has created a recurring lesson schedule by Lesson Count
- Current Lesson Count = 10

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens, Lesson Count = 10 | Current Lesson Count = 10 |
| 2 | Set Lesson Count = 11 (current + 1) | Value accepted by the system | BVA: Boundary + 1 |
| 3 | Save the form | New lessons are created successfully |  |
| 4 | Repeat: Set Lesson Count = 50 (large increase) | Value accepted by the system | BVA: Large increase |
| 5 | Save the form | New lessons are created successfully |  |

---

###  Reject Lesson Count equal to or less than current

**Description:** AC 01.2 / AC 01.3 — BVA + Negative Testing: System must reject same count and lower count.

**Preconditions:**
Admin has created a recurring lesson schedule by Lesson Count
- Current Lesson Count = 10

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens, Lesson Count = 10 | Current Lesson Count = 10 |
| 2 | Set Lesson Count = 10 (same as current) | System does not allow or shows validation error | BVA: Exact boundary (same count) |
| 3 | Attempt to save | Save is rejected / blocked |  |
| 4 | Set Lesson Count = 5 (less than current) | System does not allow or shows validation error | BVA: Below boundary (lower count) |
| 5 | Attempt to save | Save is rejected / blocked |  |

---

## Suite: Extend Recurrence Create Lessons

###  Extend daily lesson by End Date - new lessons created in DRAFT status

**Description:** AC 01.4 — State Transition: Verify all new lessons have DRAFT status and are added to the same recurring chain.

**Preconditions:**
Admin has created a daily recurring lesson schedule by End Date
- End Date = 2026-03-31
- 5 existing lessons in chain

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens |  |
| 2 | Extend Recurrence End Date to 2026-04-15 | Date accepted | New End Date = 2026-04-15 |
| 3 | Save the form | New lessons are created |  |
| 4 | Check status of all newly created lessons | All new lessons have DRAFT status | Expected status = DRAFT for all new lessons |
| 5 | Verify lessons are in the same recurring chain | New lessons appear in the same Lesson Schedule as existing lessons |  |

---

###  Extend weekly lesson by End Date - new lessons created in DRAFT status

**Description:** AC 01.4 — State Transition: Verify for weekly recurrence type.

**Preconditions:**
Admin has created a weekly recurring lesson schedule by End Date
- End Date = 2026-03-31
- Existing lessons in chain

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens |  |
| 2 | Extend Recurrence End Date to 2026-04-30 | Date accepted | New End Date = 2026-04-30 |
| 3 | Save the form | New lessons are created |  |
| 4 | Check status of all newly created lessons | All new lessons have DRAFT status | Expected status = DRAFT |
| 5 | Verify lesson dates follow weekly pattern | Lesson dates are 7 days apart following the weekly recurrence |  |

---

###  Extend custom lesson by End Date - new lessons created in DRAFT status

**Description:** AC 01.4 — State Transition: Verify for custom recurrence type with specific days.

**Preconditions:**
Admin has created a custom recurring lesson schedule by End Date
- Recurrence Days = Monday, Wednesday, Friday
- End Date = 2026-03-31

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens |  |
| 2 | Extend Recurrence End Date to 2026-04-30 | Date accepted | New End Date = 2026-04-30 |
| 3 | Save the form | New lessons are created |  |
| 4 | Check status of all newly created lessons | All new lessons have DRAFT status | Expected status = DRAFT |
| 5 | Verify lesson dates follow custom pattern (Mon, Wed, Fri) | Lesson dates fall only on Monday, Wednesday, Friday | Recurrence Days = Mon, Wed, Fri |

---

###  Extend daily lesson by Lesson Count - new lessons created in DRAFT status

**Description:** AC 01.4 — State Transition: Verify new lessons via Lesson Count path.

**Preconditions:**
Admin has created a daily recurring lesson schedule by Lesson Count
- Current Lesson Count = 10

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens |  |
| 2 | Increase Lesson Count to 15 | Value accepted | New Lesson Count = 15 (was 10, +5) |
| 3 | Save the form | New lessons are created |  |
| 4 | Check total number of lessons in the chain | Total lessons in chain = 15 | Expected total = 15 |
| 5 | Check status of all newly created lessons | All 5 new lessons have DRAFT status | Expected 5 new DRAFT lessons |

---

###  Extend weekly lesson by Lesson Count - new lessons created in DRAFT status

**Description:** AC 01.4 — State Transition: Verify for weekly recurrence via Lesson Count.

**Preconditions:**
Admin has created a weekly recurring lesson schedule by Lesson Count
- Current Lesson Count = 8

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens |  |
| 2 | Increase Lesson Count to 12 | Value accepted | New Lesson Count = 12 (was 8, +4) |
| 3 | Save the form | New lessons are created |  |
| 4 | Check total number of lessons | Total lessons = 12 | Expected total = 12 |
| 5 | Check status of new lessons | All 4 new lessons have DRAFT status | Expected 4 new DRAFT lessons |

---

###  Extend custom lesson by Lesson Count - new lessons created in DRAFT status

**Description:** AC 01.4 — State Transition: Verify for custom recurrence via Lesson Count.

**Preconditions:**
Admin has created a custom recurring lesson schedule by Lesson Count
- Recurrence Days = Tuesday, Thursday
- Current Lesson Count = 6

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens |  |
| 2 | Increase Lesson Count to 10 | Value accepted | New Lesson Count = 10 (was 6, +4) |
| 3 | Save the form | New lessons are created |  |
| 4 | Check total lessons and verify dates follow custom pattern | Total = 10, new lesson dates fall on Tuesday and Thursday only | Recurrence Days = Tue, Thu |
| 5 | Check status of new lessons | All 4 new lessons have DRAFT status | Expected 4 new DRAFT lessons |

---

###  Skip date with existing manually added lesson during extension

**Description:** AC 01.4 — Decision Table + Data Integrity: New lessons must NOT be created on dates that have manually added lessons.

**Preconditions:**
Admin has created a daily recurring lesson schedule by End Date (End Date = 2026-03-20)
Admin has manually added a lesson on 2026-03-25 via "Add Lesson" flow

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens |  |
| 2 | Extend Recurrence End Date to 2026-03-31 | Date accepted | New End Date = 2026-03-31 |
| 3 | Save the form | New lessons are created |  |
| 4 | Check if a lesson is created on 2026-03-25 | No new lesson created on 2026-03-25 (skipped) | Conflict date = 2026-03-25 (manual lesson exists) |
| 5 | Check manually added lesson on 2026-03-25 | Manually added lesson is unchanged |  |
| 6 | Count total new lessons created | Total new lessons = expected count minus 1 (the skipped date) | Expected: total - 1 due to skip |

---

###  Skip consecutive dates with multiple manually added lessons during extension

**Description:** AC 01.4 — Decision Table: Multiple manual lessons on different dates within extension range, all must be skipped.

**Preconditions:**
Admin has created a weekly recurring lesson schedule by End Date (End Date = 2026-03-20)
Admin has manually added lessons on 2026-03-25 and 2026-04-01 via "Add Lesson" flow

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens |  |
| 2 | Extend Recurrence End Date to 2026-04-15 | Date accepted | New End Date = 2026-04-15 |
| 3 | Save the form | New lessons are created |  |
| 4 | Check lessons on 2026-03-25 and 2026-04-01 | No new lessons on 2026-03-25 and 2026-04-01 (both skipped), manual lessons unchanged | Conflict dates = 2026-03-25, 2026-04-01 |
| 5 | Count total new lessons created | Total new lessons = expected count minus 2 | Expected: total - 2 due to skips |

---

###  Lesson code auto-incremented correctly for extended lessons

**Description:** AC 01.4 — BVA + CRUD: Verify lesson code is auto-calculated based on the code defined in the extension form.

**Preconditions:**
Admin has created a recurring lesson schedule
- Last existing lesson code = 5
- Extension will create 3 new lessons

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens |  |
| 2 | Verify Lesson Code = 6 (last + 1) | Lesson Code = 6 | Last existing code = 5, Expected form code = 6 |
| 3 | Extend to create 3 new lessons | Settings accepted |  |
| 4 | Save the form | New lessons created |  |
| 5 | Check lesson codes of all 3 new lessons | Lesson codes = 6, 7, 8 (auto-incremented from defined code) | Expected: 6, 7, 8 |

---

###  Extended lessons have no teacher and no student allocated

**Description:** AC 01.4 — Negative Testing: Newly created lessons must not auto-inherit teacher/student from existing lessons.

**Preconditions:**
Admin has created a recurring lesson schedule
- Existing lessons have Teacher A and Student B assigned
- Extension creates new lessons

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens |  |
| 2 | Extend and save | New lessons created |  |
| 3 | Open each newly created lesson detail | Lesson detail pages open |  |
| 4 | Check Lesson Teacher section | No teacher assigned to new lessons | Expected: empty teacher list |
| 5 | Check Student Sessions section | No student assigned to new lessons | Expected: empty student list |
| 6 | Verify existing lessons still have Teacher A and Student B | Existing lessons still have Teacher A and Student B |  |

---

###  Extended lessons respect Skip Closed Dates setting from original schedule

**Description:** AC 01.4 — Regression: When Skip Closed Dates = checked, no extended lesson should be created on a closed date.

**Preconditions:**
Admin has created a recurring lesson schedule with Skip Closed Dates = checked
- A closed date (e.g., 2026-04-10) falls within the extension date range

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens |  |
| 2 | Verify Skip Closed Dates shows "checked" (non-editable) | Skip Closed Dates = checked, non-editable | Source: Lesson Schedule, Skip Closed Dates = checked |
| 3 | Extend End Date to cover range including 2026-04-10 | Date accepted | Closed date = 2026-04-10 |
| 4 | Save the form | New lessons created |  |
| 5 | Check if any lesson is created on 2026-04-10 | No lesson exists on 2026-04-10 (closed date skipped) | Expected: no lesson on closed date |

---

###  Nichibei: Syllabus description updated for extended lessons based on lesson code

**Description:** AC 01.4 — CRUD + Regression (Nichibei only): Syllabus description auto-filled for new lessons based on lesson code mapping.

**Preconditions:**
Nichibei tenant configuration
Syllabus master associated to course master with syllabus details:
- Code 6 → Description A
- Code 7 → Description B
- Code 8 → Description C
Recurring lesson schedule created, last lesson code = 5

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson Schedule, click "Extend Recurrence | Lesson Creation Form opens |  |
| 2 | Extend to create 3 new lessons (codes 6, 7, 8) | Settings accepted | lesson codes = 6, 7, 8 |
| 3 | Save the form | New lessons created |  |
| 4 | Check syllabus description of lesson code 6 | Syllabus description = Description A | Code 6 → Description A |
| 5 | Check syllabus description of lesson code 7 | Syllabus description = Description B | Code 7 → Description B |
| 6 | Check syllabus description of lesson code 8 | Syllabus description = Description C | Code 8 → Description C |

---

## Suite: Extend Recurrence Schedule Sync

###  Verify Lesson Schedule End Date updated on SF and BO after extending by End Date

**Description:** AC 01.5 — Cross-system: End Date must update on all 5 surfaces after extending by End Date.

**Preconditions:**
Admin has created a daily recurring lesson schedule by End Date
- Current End Date = 2026-03-31
- Extension End Date = 2026-04-30

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Extend Recurrence End Date to 2026-04-30 and save | New lessons created successfully | New End Date = 2026-04-30 |
| 2 | Check SF - Lesson Schedule detail page | End Date = 2026-04-30 | SF Lesson Schedule detail |
| 3 | Check SF - Lesson edit form | End Date = 2026-04-30 | SF Lesson edit form |
| 4 | Check SF - Lesson Calendar Related list | Lessons visible up to 2026-04-30 | SF Calendar |
| 5 | Login BO, check Lesson detail - Recurring settings | Recurring settings show End Date = 2026-04-30 | BO Lesson detail |
| 6 | Check BO - Calendar Related list | Lessons visible up to 2026-04-30 | BO Calendar |

---

###  Verify Lesson Schedule End Date updated on SF and BO after extending by Lesson Count

**Description:** AC 01.5 — Cross-system: End Date derived from last lesson date must update on all 5 surfaces after extending by Lesson Count.

**Preconditions:**
Admin has created a daily recurring lesson schedule by Lesson Count
- Current Lesson Count = 10
- Extension to Lesson Count = 15

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Extend Lesson Count to 15 and save | New lessons created successfully | New Lesson Count = 15 (was 10) |
| 2 | Identify the last lesson date in the chain (e.g., 2026-04-20) | Last lesson date determined (e.g., 2026-04-20) |  |
| 3 | Check SF - Lesson Schedule detail page | End Date = last lesson date (2026-04-20) | SF Lesson Schedule detail |
| 4 | Check SF - Lesson edit form | End Date = last lesson date | SF Lesson edit form |
| 5 | Check SF - Lesson Calendar Related list | Lessons visible up to last lesson date | SF Calendar |
| 6 | Login BO, check Lesson detail - Recurring settings and Calendar Related list | End Date and Calendar reflect last lesson date | BO Lesson detail + Calendar |

---

## Suite: Extend Recurrence Edit Following

###  Edit recurring lesson with "Apply this and the following" updates extended lessons

**Description:** AC 02.1 — State Transition + Regression: Editing from a lesson BEFORE the extension point must update all extended lessons.

**Preconditions:**
Admin has created a daily recurring lesson schedule with 5 original lessons
Extended by End Date creating 3 new lessons (total 8)
All lessons are in DRAFT or Published status

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the 3rd lesson (before extension point) | Lesson detail opens |  |
| 2 | Click Edit, change lesson name to "Updated Lesson", change classroom to "Room B | Fields updated | Lesson name = "Updated Lesson", Classroom = "Room B |
| 3 | Select "Apply this and the following | Recurring update option selected |  |
| 4 | Save | Save successful |  |
| 5 | Check lessons 3-5 (original chain after edit) | Lessons 3-5: name = "Updated Lesson", classroom = "Room B | Verify original chain updated |
| 6 | Check lessons 6-8 (extended lessons) | Lessons 6-8 (extended): name = "Updated Lesson", classroom = "Room B | Verify extended chain updated |
| 7 | Check lessons 1-2 (before edit point) | Lessons 1-2: unchanged (original values) | Verify previous lessons not affected |

---

###  Edit at original/extended boundary with "Apply this and the following" updates all extended lessons

**Description:** AC 02.1 — State Transition: Edit the LAST lesson of the original chain and verify all extended lessons are updated.

**Preconditions:**
Admin has created a daily recurring lesson schedule with 5 original lessons
Extended by End Date creating 3 new lessons (total 8)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the 5th lesson (last of original chain / boundary) | Lesson detail opens | Boundary lesson (last original) |
| 2 | Click Edit, change lesson time to 14:00-15:00 | Time updated | New time = 14:00-15:00 |
| 3 | Select "Apply this and the following | Recurring update option selected |  |
| 4 | Save | Save successful |  |
| 5 | Check lesson 5 | Lesson 5: time = 14:00-15:00 |  |
| 6 | Check lessons 6-8 (extended lessons) | Lessons 6-8: time = 14:00-15:00 | Verify extended chain updated |
| 7 | Check lessons 1-4 (before boundary) | Lessons 1-4: original time unchanged | Verify previous chain not affected |

---

###  One-time lesson edit does not cascade to extended recurring chain

**Description:** AC 02.1 — Decision Table + Negative Testing: Editing a one-time lesson must only affect that single lesson.

**Preconditions:**
Admin has created a recurring lesson schedule with extended lessons
A one-time lesson exists in the same Lesson Schedule (created via Add Lesson manually)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the one-time (manual) lesson | Lesson detail opens |  |
| 2 | Click Edit, change lesson name and time | Fields updated | Edit name and time |
| 3 | Save | Save successful without recurring options |  |
| 4 | Verify no recurring popup is shown | No "Apply this and the following" popup shown |  |
| 5 | Check all recurring and extended lessons | All recurring and extended lessons are unchanged | Verify no cascading effect |

---

###  Manual lesson not affected by recurring "Apply this and the following" edit after extension

**Description:** AC 02.1 — Negative Testing: Manually created lesson in the schedule must remain unchanged when recurring edit is applied.

**Preconditions:**
Admin has created a daily recurring lesson schedule with 5 lessons
Manually added a lesson (lesson manual) between lesson 3 and 4
Extended by End Date creating 3 new lessons

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson 2 (before lesson manual) | Lesson detail opens |  |
| 2 | Click Edit, change lesson name to "Recurring Update | Name updated | New name = "Recurring Update |
| 3 | Select "Apply this and the following | Recurring update selected |  |
| 4 | Save | Save successful |  |
| 5 | Check the manually created lesson | Manual lesson: name unchanged, NOT affected by recurring edit | Manual lesson should be isolated |
| 6 | Check lessons 3-5 and extended lessons 6-8 | Lessons 3-8: name = "Recurring Update" (all recurring lessons updated) | All recurring lessons (original + extended) updated |

---

## Suite: Extend Recurrence Student Teacher

###  Assign student and teacher with "Apply this and the following" propagates to extended lessons

**Description:** AC 02.2 — Pairwise + Regression: Assign from a lesson before the extension point, verify both old and extended lessons get the assignment.

**Preconditions:**
Admin has created a daily recurring lesson schedule with 5 original lessons
Extended by End Date creating 3 new lessons (total 8)
Student A and Teacher A exist and are eligible

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson 2 (before extension point) | Lesson detail opens |  |
| 2 | Assign Student A with "Apply this and the following | Student A assigned | Student = Student A |
| 3 | Assign Teacher A with "Apply this and the following | Teacher A assigned | Teacher = Teacher A |
| 4 | Check lessons 2-5 (original chain) | Student A and Teacher A assigned to lessons 2-5 | Verify original chain |
| 5 | Check lessons 6-8 (extended lessons) | Student A and Teacher A assigned to lessons 6-8 (extended) | Verify extended chain |
| 6 | Check lesson 1 (before assignment point) | Lesson 1: no Student A or Teacher A | Not affected |
| 7 | Student A login Mobile | Student A sees lessons 2-8 with correct information | Mobile verification |

---

###  Assign student and teacher with "Apply this and the following" from within extended range

**Description:** AC 02.2 — Pairwise: Assign from an extended lesson, verify only following extended lessons get the assignment.

**Preconditions:**
Admin has created a recurring lesson schedule
Extended creating 5 new lessons (lessons 6-10)
Student B and Teacher B exist

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson 7 (2nd extended lesson) | Lesson detail opens |  |
| 2 | Assign Student B and Teacher B with "Apply this and the following | Student B and Teacher B assigned | Student = Student B, Teacher = Teacher B |
| 3 | Check lessons 7-10 (following extended lessons) | Student B and Teacher B present in lessons 7-10 | Verify following extended lessons |
| 4 | Check lessons 1-6 (original + first extended) | Lessons 1-6: no Student B or Teacher B | Not affected |

---

###  Unassign student and teacher with "Apply this and the following" propagates to extended lessons

**Description:** AC 02.2 — Regression: Unassign from before extension point, verify removal in all following lessons including extended.

**Preconditions:**
Admin has created a recurring lesson schedule, extended with new lessons
Student A and Teacher A assigned to all lessons (1-8) via "Apply this and the following"

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson 3 | Lesson detail opens |  |
| 2 | Unassign Student A with "Apply this and the following | Student A removed | Unassign Student A |
| 3 | Unassign Teacher A with "Apply this and the following | Teacher A removed | Unassign Teacher A |
| 4 | Check lessons 3-8 (original + extended after unassignment) | No Student A or Teacher A in lessons 3-8 | Verify removal in all following |
| 5 | Check lessons 1-2 (before unassignment point) | Lessons 1-2: Student A and Teacher A still present | Not affected |
| 6 | Check lesson allocation for Student A | Student sessions deleted for affected lessons, Lesson Allocated count decreased, Lesson Allocation Status and Report History updated | Check: Lesson Allocated, Allocation Status, Report History |

---

###  Assign student and teacher to manually created lesson with "Apply this and the following"

**Description:** AC 02.2 — CRUD + Regression: Student/teacher assignment via following must also include manually created lesson in the schedule.

**Preconditions:**
Admin has created a recurring lesson schedule with 5 lessons
Manually added a lesson between lesson 3 and 4
Extended creating 3 new lessons (total 9 including manual)
Student C exists

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open lesson 2 (before manual lesson) | Lesson detail opens |  |
| 2 | Assign Student C with "Apply this and the following | Student C assigned | Student = Student C |
| 3 | Check the manually created lesson | Manual lesson: Student C is assigned | Manual lesson receives assignment |
| 4 | Check remaining recurring lessons (3-5) and extended lessons (6-8) | All recurring and extended lessons: Student C is assigned | Both original and extended lessons receive assignment |
| 5 | Check lesson allocation for Student C | Lesson Allocated count includes all assigned lessons (manual + recurring + extended) | Verify complete allocation data |

---

