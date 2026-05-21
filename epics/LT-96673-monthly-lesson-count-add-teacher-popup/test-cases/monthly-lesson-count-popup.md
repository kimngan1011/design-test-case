# Test Cases: LT-96673 — Monthly Lesson Count in Add Teacher Popup

## Suite: [Riso] Monthly Lesson Count – Add Teacher Popup

---

### [Riso] Add Teacher Popup – Monthly Lesson Count Column – Column Visible With Count Value

**Description:** AC 01.2 — Regression Analysis — Monthly Lesson Count column appears in the Add Teacher popup and shows a count value for teachers who have lessons in the selected lesson's month.

**Preconditions:**

- Org is Riso OOP
- A lesson exists in **January 2026** with status = Draft
- Teacher A is assigned to 3 lessons in January 2026 (all status = Published)
- User is logged in as CM or HQ

| #   | Action                                              | Expected Result                                                                        | Test Data                 |
| --- | --------------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------- |
| 1   | Open the January 2026 lesson detail page            | Lesson Detail page displays correctly                                                  | Lesson date: Jan 15, 2026 |
| 2   | On the Lesson Teacher section, click "Add Teachers" | Add Teacher popup opens showing the teacher list                                       | ""                        |
| 3   | Locate Teacher A in the list                        | "Monthly Lesson Count" (今月の授業数) column is visible; Teacher A shows count = **3** | ""                        |

**Severity:** major
**Priority:** high

---

### [Riso] Add Teacher Popup – Monthly Lesson Count – Count Reflects Draft + Published + Completed Only

**Description:** AC 01.2 — Decision Table — Count equals the sum of Draft, Published, and Completed lessons in the selected month; other statuses are ignored.

**Preconditions:**

- Org is Riso OOP
- A lesson exists in **March 2026** (target lesson for popup)
- Teacher B has the following lessons in March 2026:
  - 1 lesson with status = Draft
  - 2 lessons with status = Published
  - 1 lesson with status = Completed
  - 1 lesson with status = Cancelled
- User is logged in as CM

| #   | Action                                   | Expected Result                                                                                                    | Test Data                 |
| --- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------- |
| 1   | Open the March 2026 target lesson detail | Lesson Detail displays for March 2026                                                                              | Lesson date: Mar 10, 2026 |
| 2   | Click "Add Teachers" to open the popup   | Add Teacher popup opens                                                                                            | ""                        |
| 3   | Locate Teacher B in the list             | Monthly Lesson Count for Teacher B = **4** (Draft 1 + Published 2 + Completed 1); Cancelled lesson is NOT included | ""                        |

**Severity:** critical
**Priority:** high

---

### [Riso] Add Teacher Popup – Monthly Lesson Count – Cancelled Lessons Excluded

**Description:** AC 01.2 — Decision Table / Negative Testing — A teacher with only Cancelled lessons in the selected month shows count = 0, not the cancelled count.

**Preconditions:**

- Org is Riso OOP
- A target lesson exists in **February 2026**
- Teacher C has **3 lessons** in February 2026, all with status = **Cancelled**
- Teacher C has no Draft/Published/Completed lessons in February 2026

| #   | Action                                      | Expected Result                                                             | Test Data                |
| --- | ------------------------------------------- | --------------------------------------------------------------------------- | ------------------------ |
| 1   | Open the February 2026 target lesson detail | Lesson Detail displays for February 2026                                    | Lesson date: Feb 5, 2026 |
| 2   | Click "Add Teachers" to open the popup      | Add Teacher popup opens                                                     | ""                       |
| 3   | Locate Teacher C in the list                | Monthly Lesson Count for Teacher C = **0** (Cancelled lessons are excluded) | ""                       |

**Severity:** major
**Priority:** high

---

### [Riso] Add Teacher Popup – Monthly Lesson Count – Zero Lessons Shows 0 Not Blank

**Description:** AC 01.2 — Boundary Value Analysis — A teacher with no lessons at all in the selected month shows "0" in the count column, not an empty cell.

**Preconditions:**

- Org is Riso OOP
- A target lesson exists in **April 2026**
- Teacher D has **no lessons** in April 2026 (no assignments of any status)

| #   | Action                                   | Expected Result                                                                                      | Test Data                 |
| --- | ---------------------------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------- |
| 1   | Open the April 2026 target lesson detail | Lesson Detail displays for April 2026                                                                | Lesson date: Apr 20, 2026 |
| 2   | Click "Add Teachers" to open the popup   | Add Teacher popup opens                                                                              | ""                        |
| 3   | Locate Teacher D in the list             | Monthly Lesson Count cell for Teacher D shows **"0"** — the cell is not blank, not empty, not a dash | ""                        |

**Severity:** normal
**Priority:** medium

---

### [Riso] Add Teacher Popup – Monthly Lesson Count – Cross-Location Count Included

**Description:** AC 01.2 — Decision Table — Count includes lessons from all of the teacher's locations, not only the location of the selected lesson.

**Preconditions:**

- Org is Riso OOP
- Target lesson is at **Location A** in May 2026
- Teacher E is assigned to:
  - 3 lessons at **Location A** in May 2026 (Published)
  - 2 lessons at **Location B** in May 2026 (Published)
- Teacher E is affiliated to both Location A and Location B

| #   | Action                                               | Expected Result                                                                    | Test Data                |
| --- | ---------------------------------------------------- | ---------------------------------------------------------------------------------- | ------------------------ |
| 1   | Open the May 2026 target lesson detail at Location A | Lesson Detail displays for May 2026, Location A                                    | Lesson date: May 8, 2026 |
| 2   | Click "Add Teachers" to open the popup               | Add Teacher popup opens                                                            | ""                       |
| 3   | Locate Teacher E in the list                         | Monthly Lesson Count for Teacher E = **5** (3 from Location A + 2 from Location B) | ""                       |

**Severity:** major
**Priority:** high

---

### [Riso] Add Teacher Popup – Monthly Lesson Count – Count Uses Selected Lesson's Month Not Today's

**Description:** AC 01.2 — Decision Table — When the selected lesson is in a past or future month, the count reflects that lesson's month, not the current month.

**Preconditions:**

- Org is Riso OOP
- Today is in **April 2026**
- A target lesson exists in **January 2026** (past month)
- Teacher F has:
  - 5 lessons in **January 2026** (Published)
  - 2 lessons in **April 2026** (Published)

| #   | Action                                 | Expected Result                                                                          | Test Data                 |
| --- | -------------------------------------- | ---------------------------------------------------------------------------------------- | ------------------------- |
| 1   | Open the January 2026 lesson detail    | Lesson Detail displays for January 2026                                                  | Lesson date: Jan 20, 2026 |
| 2   | Click "Add Teachers" to open the popup | Add Teacher popup opens                                                                  | ""                        |
| 3   | Locate Teacher F in the list           | Monthly Lesson Count for Teacher F = **5** (January count); count is NOT 2 (April count) | ""                        |

**Severity:** major
**Priority:** high

---

### [Riso] Add Teacher Popup – Monthly Lesson Count – Count Fixed After Filter Applied

**Description:** AC 01.2 — Decision Table / Negative Testing — Applying any filter (location, working type, subject, working hours) does not change the Monthly Lesson Count value for any teacher in the list.

**Preconditions:**

- Org is Riso OOP
- Target lesson exists in **June 2026**
- Teacher G has **4 lessons** in June 2026 (Published)
- Teacher G is part-time, affiliated to Location A, has subject "Math"
- Add Teacher popup is open; Teacher G visible with count = 4

| #   | Action                                             | Expected Result                                           | Test Data  |
| --- | -------------------------------------------------- | --------------------------------------------------------- | ---------- |
| 1   | Open popup — note Teacher G's Monthly Lesson Count | Teacher G shows Monthly Lesson Count = **4**              | ""         |
| 2   | Apply filter: Location = Location A                | Teacher list reloads filtered; Teacher G is still visible | Location A |
| 3   | Observe Teacher G's Monthly Lesson Count           | Count = **4** (unchanged by location filter)              | ""         |
| 4   | Apply filter: Working Type = Part-time             | Teacher list reloads                                      | Part-time  |
| 5   | Observe Teacher G's Monthly Lesson Count           | Count = **4** (unchanged by working type filter)          | ""         |
| 6   | Apply filter: Subject = Math                       | Teacher list reloads                                      | Math       |
| 7   | Observe Teacher G's Monthly Lesson Count           | Count = **4** (unchanged by subject filter)               | ""         |

**Severity:** major
**Priority:** high

---

### [Riso] Add Teacher Popup – Monthly Lesson Count Column – Not Sortable

**Description:** AC 01.2 — Negative Testing — Clicking the Monthly Lesson Count column header does not sort the teacher list by count.

**Preconditions:**

- Org is Riso OOP
- Target lesson exists with multiple teachers visible in the popup, each with a different Monthly Lesson Count value
- Note the order of teachers before clicking

| #   | Action                                                                        | Expected Result                                                                     | Test Data |
| --- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | --------- |
| 1   | Open the Add Teacher popup; note the order of teachers and their count values | Teacher list is displayed in the default sort order                                 | ""        |
| 2   | Click the "Monthly Lesson Count" column header                                | The teacher list order does **not change**; no ascending/descending sort is applied | ""        |
| 3   | Click the column header again                                                 | The teacher list order remains unchanged                                            | ""        |

**Severity:** minor
**Priority:** low

---

### [Riso] Add Teacher Popup – Monthly Lesson Count – Centre Staff Can See Column

**Description:** AC 01.2 — Permission Matrix — A Centre Staff (SPU login) user who can open the Add Teacher popup also sees the Monthly Lesson Count column.

**Preconditions:**

- Org is Riso OOP
- User is logged in as **Centre Staff (SPU login)**
- A lesson exists where the Centre Staff has permission to open the Add Teacher dialog

| #   | Action                                 | Expected Result                                             | Test Data            |
| --- | -------------------------------------- | ----------------------------------------------------------- | -------------------- |
| 1   | Log in as Centre Staff (SPU)           | Login successful                                            | Centre Staff account |
| 2   | Navigate to a lesson detail page       | Lesson Detail page displays                                 | ""                   |
| 3   | Click "Add Teachers" to open the popup | Add Teacher popup opens                                     | ""                   |
| 4   | Observe the teacher list columns       | "Monthly Lesson Count" (今月の授業数) column is **visible** | ""                   |

**Severity:** normal
**Priority:** medium

---

### [Riso] Add Teacher Popup – Monthly Lesson Count – Timezone Boundary Last Day of Month

**Description:** AC 01.2 + AC 01.3 — Boundary Value Analysis — A lesson scheduled on the last day of a month at late evening (local time) is counted in that month, not the next month, even though the UTC stored datetime is the following day.

**Preconditions:**

- Org is Riso OOP (Japan Standard Time, UTC+9)
- Teacher H is assigned to a lesson with:
  - Date: **January 31, 2026**
  - Time: **23:30 JST** (= February 1 00:30 UTC)
  - Status: Published
- Teacher H has no other lessons in January or February 2026
- Target lesson is also in **January 2026**

| #   | Action                                     | Expected Result                                                                                              | Test Data                 |
| --- | ------------------------------------------ | ------------------------------------------------------------------------------------------------------------ | ------------------------- |
| 1   | Open the January 2026 target lesson detail | Lesson Detail page displays for January 2026                                                                 | Lesson date: Jan 15, 2026 |
| 2   | Click "Add Teachers" to open the popup     | Add Teacher popup opens                                                                                      | ""                        |
| 3   | Locate Teacher H in the list               | Monthly Lesson Count for Teacher H = **1** (the Jan 31 23:30 JST lesson is counted in January, not February) | ""                        |

**Severity:** critical
**Priority:** high

---

### [Riso] Add Teacher Popup – Monthly Lesson Count – Timezone Boundary First Day of Month

**Description:** AC 01.2 + AC 01.3 — Boundary Value Analysis — A lesson scheduled on the first day of a month at early morning (local time) is counted in that month, not the previous month, even though the UTC datetime differs.

**Preconditions:**

- Org is Riso OOP (Japan Standard Time, UTC+9)
- Teacher I is assigned to a lesson with:
  - Date: **February 1, 2026**
  - Time: **00:30 JST** (= January 31 15:30 UTC)
  - Status: Published
- Teacher I has no other lessons in January or February 2026
- Target lesson is in **February 2026**

| #   | Action                                      | Expected Result                                                                                             | Test Data                 |
| --- | ------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------------- |
| 1   | Open the February 2026 target lesson detail | Lesson Detail page displays for February 2026                                                               | Lesson date: Feb 10, 2026 |
| 2   | Click "Add Teachers" to open the popup      | Add Teacher popup opens                                                                                     | ""                        |
| 3   | Locate Teacher I in the list                | Monthly Lesson Count for Teacher I = **1** (the Feb 1 00:30 JST lesson is counted in February, not January) | ""                        |

**Severity:** critical
**Priority:** high
