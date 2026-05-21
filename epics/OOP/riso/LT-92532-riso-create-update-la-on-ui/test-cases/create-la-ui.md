# Test Cases: LT-92532 — [Riso] Create Lesson Allocation on UI

## Suite: Create LA – CTA Button & Modal

---

### [Riso] Lesson Allocation – Contact Course Tab – New Lesson Allocation Button – Displayed for HQ/CM user

**Description:** AC 01.1 — Decision Table — Verify "New Lesson Allocation" CTA button is visible under the Require Lesson Allocation table in Contact → Course tab for authorized users.

**Preconditions:**

- Logged in as HQ or CM user
- Navigate to Student detail → Contact → Course tab
- Student has at least one course with `require_allocation = TRUE`

| #   | Action                                        | Expected Result                                           | Test Data |
| --- | --------------------------------------------- | --------------------------------------------------------- | --------- |
| 1   | Navigate to Student detail page               | Student detail page is displayed                          |           |
| 2   | Click on "Contact" tab                        | Contact tab opens                                         |           |
| 3   | Click on "Course" sub-tab                     | Course tab content is shown                               |           |
| 4   | Scroll to the Require Lesson Allocation table | "New Lesson Allocation" button is visible below the table |           |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Contact Course Tab – New Lesson Allocation Button – Click Opens Modal

**Description:** AC 01.1 — State Transition Testing — Verify clicking the "New Lesson Allocation" button opens the New Lesson Allocation modal.

**Preconditions:**

- Logged in as HQ or CM user
- On Student → Contact → Course tab
- "New Lesson Allocation" button is visible

| #   | Action                               | Expected Result                                                                 | Test Data |
| --- | ------------------------------------ | ------------------------------------------------------------------------------- | --------- |
| 1   | Click "New Lesson Allocation" button | New Lesson Allocation modal dialog opens                                        |           |
| 2   | Observe modal header                 | Modal title displays "New Lesson Allocation"                                    |           |
| 3   | Observe modal content                | AY field and Location field are present; course selection table area is visible |           |

**Severity:** normal
**Priority:** medium

---

## Suite: Create LA – Form Pre-fill & Course List

---

### [Riso] Lesson Allocation – New LA Form – Academic Year – Pre-filled with Current AY

**Description:** AC 01.2 — Decision Table — Verify AY field is automatically pre-filled with the current Academic Year when the modal opens.

**Preconditions:**

- Logged in as HQ or CM user
- Current Academic Year exists and is active (e.g., AY 2026)
- New Lesson Allocation modal is open

| #   | Action                           | Expected Result                                                  | Test Data |
| --- | -------------------------------- | ---------------------------------------------------------------- | --------- |
| 1   | Open New Lesson Allocation modal | Modal is displayed                                               |           |
| 2   | Observe AY field                 | AY field is pre-filled with the current active AY (e.g., "2026") | AY: 2026  |

**Severity:** normal
**Priority:** medium

---

### [Riso] Lesson Allocation – New LA Form – Location Field – Pre-filled When Student Has Exactly 1 Active Enrolled Location

**Description:** AC 01.2 — Decision Table — Verify Location is pre-filled when the student has exactly one active enrolled location (status = enrolled).

**Preconditions:**

- Logged in as HQ or CM user
- Student has exactly **1** active enrolled location (e.g., Location A, status = enrolled)
- New Lesson Allocation modal is open

| #   | Action                           | Expected Result                                                                              | Test Data            |
| --- | -------------------------------- | -------------------------------------------------------------------------------------------- | -------------------- |
| 1   | Open New Lesson Allocation modal | Modal is displayed                                                                           |                      |
| 2   | Observe Location field           | Location field is pre-filled with "Location A" (the student's sole active enrolled location) | Location: Location A |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – New LA Form – Location Field – Blank When Student Has 2+ Active Enrolled Locations

**Description:** AC 01.2 — Decision Table — Verify Location field is blank (not pre-filled) when the student has more than one active enrolled location.

**Preconditions:**

- Logged in as HQ or CM user
- Student has **2** active enrolled locations (Location A and Location B, both status = enrolled)
- New Lesson Allocation modal is open

| #   | Action                           | Expected Result                                          | Test Data |
| --- | -------------------------------- | -------------------------------------------------------- | --------- |
| 1   | Open New Lesson Allocation modal | Modal is displayed                                       |           |
| 2   | Observe Location field           | Location field is blank (no pre-filled value)            |           |
| 3   | Click Location dropdown          | Dropdown shows both Location A and Location B as options |           |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – New LA Form – Location Field – Blank When Student Has No Active Enrolled Location

**Description:** AC 01.2 — Decision Table — Verify Location field is blank when the student has no active enrolled location; dropdown shows all locations user has affiliation with.

**Preconditions:**

- Logged in as HQ or CM user who has affiliation with Location A and Location B
- Student has **0** active enrolled locations
- New Lesson Allocation modal is open

| #   | Action                           | Expected Result                                                                             | Test Data |
| --- | -------------------------------- | ------------------------------------------------------------------------------------------- | --------- |
| 1   | Open New Lesson Allocation modal | Modal is displayed                                                                          |           |
| 2   | Observe Location field           | Location field is blank                                                                     |           |
| 3   | Click Location dropdown          | Dropdown shows all locations the current user has affiliation with (Location A, Location B) |           |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – New LA Form – Course List – Not Shown Before AY and Location Are Selected

**Description:** AC 01.2 — Decision Table — Verify course selection table does not load until both AY and Location are selected.

**Preconditions:**

- Logged in as HQ or CM user
- New Lesson Allocation modal is open
- AY is pre-filled; Location is blank

| #   | Action                                                        | Expected Result                                                | Test Data            |
| --- | ------------------------------------------------------------- | -------------------------------------------------------------- | -------------------- |
| 1   | Observe course table area with only AY filled, Location blank | Course list is empty / not loaded                              |                      |
| 2   | Select a Location                                             | Course list loads and shows courses for selected AY + Location | Location: Location A |
| 3   | Clear Location                                                | Course list disappears / resets                                |                      |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – New LA Form – Course List – Shows Course Masters with Course Offering and Location Course

**Description:** AC 01.2 — CRUD Testing — Verify course list only shows Course Masters that have both a Course Offering (for selected AY) and a Location Course (for selected Location).

**Preconditions:**

- Logged in as HQ or CM user
- Course Master "Math" has Course Offering for AY 2026 AND Location Course for Location A
- Course Master "English" has Course Offering for AY 2026 but NO Location Course for Location A
- AY = 2026, Location = Location A selected in modal

| #   | Action                                     | Expected Result                                     | Test Data                      |
| --- | ------------------------------------------ | --------------------------------------------------- | ------------------------------ |
| 1   | Select AY = 2026 and Location = Location A | Course list loads                                   | AY: 2026, Location: Location A |
| 2   | Observe course list                        | "Math" is shown in the list; "English" is NOT shown |                                |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – New LA Form – Course List – Reloads When AY Changes

**Description:** AC 01.2 — State Transition Testing — Verify course list is refreshed when the AY value is changed.

**Preconditions:**

- Logged in as HQ or CM user
- AY 2026 and Location A selected; course list shows Courses A, B
- AY 2025 has a different set of courses for Location A (Course C only)

| #   | Action                                                    | Expected Result                                       | Test Data                      |
| --- | --------------------------------------------------------- | ----------------------------------------------------- | ------------------------------ |
| 1   | Observe course list with AY = 2026, Location = Location A | Courses A and B are shown                             | AY: 2026, Location: Location A |
| 2   | Change AY to 2025                                         | Course list reloads                                   | AY: 2025                       |
| 3   | Observe updated course list                               | Only Course C is shown (reflecting AY 2025 offerings) |                                |

**Severity:** normal
**Priority:** medium

---

### [Riso] Lesson Allocation – New LA Form – Course List – Reloads When Location Changes

**Description:** AC 01.2 — State Transition Testing — Verify course list is refreshed when the Location value is changed.

**Preconditions:**

- Logged in as HQ or CM user
- AY 2026 + Location A selected; course list shows Courses A, B
- Location B has different courses for AY 2026 (Course D only)

| #   | Action                                                    | Expected Result           | Test Data            |
| --- | --------------------------------------------------------- | ------------------------- | -------------------- |
| 1   | Observe course list with AY = 2026, Location = Location A | Courses A and B are shown |                      |
| 2   | Change Location to Location B                             | Course list reloads       | Location: Location B |
| 3   | Observe updated course list                               | Only Course D is shown    |                      |

**Severity:** normal
**Priority:** medium

---

### [Riso] Lesson Allocation – New LA Form – Course Search – JP Partial Match Returns Matching Courses

**Description:** AC 01.2 — Equivalence Partitioning — Verify course search box supports Japanese partial match.

**Preconditions:**

- Logged in as HQ or CM user
- AY and Location selected; courses including "数学コース" and "英語コース" are in the list

| #   | Action                                      | Expected Result                                                       | Test Data      |
| --- | ------------------------------------------- | --------------------------------------------------------------------- | -------------- |
| 1   | Type partial JP string in course search box | Course list filters to show only courses containing the search string | Search: "数学" |
| 2   | Observe results                             | Only "数学コース" is shown; "英語コース" is not shown                 |                |

**Severity:** minor
**Priority:** low

---

## Suite: Create LA – Happy Path

---

### [Riso] Lesson Allocation – Create LA – Single Course – Happy Path – LA Created and Displayed in Table

**Description:** AC 01.3 — CRUD Testing — Verify a single LA can be created with all required fields; user is redirected and LA appears in the table.

**Preconditions:**

- Logged in as HQ or CM user
- Student has 1 active enrolled location (Location A)
- Course "Math" exists for AY 2026 + Location A
- No existing LA for Math / AY 2026 / Location A in the test date range

| #   | Action                                                      | Expected Result                                                                                | Test Data          |
| --- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ------------------ |
| 1   | Open New Lesson Allocation modal                            | Modal opens; AY = 2026 pre-filled; Location = Location A pre-filled                            |                    |
| 2   | Observe selections and click Next / proceed to course table | Course list loads showing "Math"                                                               |                    |
| 3   | Select "Math" from course list                              | "Math" is checked; Next button becomes active                                                  |                    |
| 4   | Click Next to configuration page                            | Configuration form appears with Type, Purchased Slot, Start date, End date fields              |                    |
| 5   | Select Type = "Regular"                                     | Type field shows "Regular"                                                                     | Type: Regular      |
| 6   | Enter Purchased Slot = 10                                   | Purchased Slot shows 10                                                                        | Purchased Slot: 10 |
| 7   | Enter Start date = 2026-04-01                               | Start date = 2026-04-01                                                                        | Start: 2026-04-01  |
| 8   | Enter End date = 2026-09-30                                 | End date = 2026-09-30; no error shown                                                          | End: 2026-09-30    |
| 9   | Click Save / Confirm                                        | User is redirected to Contact page                                                             |                    |
| 10  | Navigate to Student → Contact → Course tab                  | New LA row for "Math" / AY 2026 / Location A is visible in the Require Lesson Allocation table |                    |
| 11  | Open the new LA record                                      | Product details, student course id, package course, order remarks are all empty / no value     |                    |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocation – Create LA – Multiple Courses in One Flow – All LAs Created

**Description:** AC 01.3 — Equivalence Partitioning — Verify selecting multiple courses in one flow creates an LA for each selected course.

**Preconditions:**

- Logged in as HQ or CM user
- AY 2026, Location A selected
- Courses "Math" and "English" both available in the list with no overlapping existing LAs

| #   | Action                                                              | Expected Result                                                           | Test Data                                                                               |
| --- | ------------------------------------------------------------------- | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| 1   | Open New Lesson Allocation modal and proceed to course table        | Course list is loaded                                                     |                                                                                         |
| 2   | Select "Math" and "English"                                         | Both courses are checked                                                  |                                                                                         |
| 3   | Click Next to configuration                                         | Configuration shows 2 rows — one for Math, one for English                |                                                                                         |
| 4   | Fill in Type, Purchased Slot, Start date, End date for both courses | All fields filled with valid values for each row                          | Math: Regular, 10, 2026-04-01, 2026-09-30; English: Seasonal, 5, 2026-04-01, 2026-06-30 |
| 5   | Click Save                                                          | Redirected to Contact page                                                |                                                                                         |
| 6   | Navigate to Course tab                                              | Both LAs (Math and English) appear in the Require Lesson Allocation table |                                                                                         |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Create LA – All Three LA Types – Each Type Can Be Selected

**Description:** AC 01.3 — Equivalence Partitioning — Verify all three LA type options (Regular, Seasonal, Trial) are available and selectable.

**Preconditions:**

- Logged in as HQ or CM user
- New Lesson Allocation modal open, course selected, on configuration page

| #   | Action                    | Expected Result                                        | Test Data      |
| --- | ------------------------- | ------------------------------------------------------ | -------------- |
| 1   | Click Type dropdown       | Dropdown shows three options: Regular, Seasonal, Trial |                |
| 2   | Select "Regular"          | Type field shows "Regular"                             | Type: Regular  |
| 3   | Change Type to "Seasonal" | Type field shows "Seasonal"                            | Type: Seasonal |
| 4   | Change Type to "Trial"    | Type field shows "Trial"                               | Type: Trial    |

**Severity:** normal
**Priority:** medium
