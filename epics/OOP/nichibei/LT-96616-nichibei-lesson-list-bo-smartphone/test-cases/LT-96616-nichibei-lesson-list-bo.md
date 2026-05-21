# Test Cases: LT-96616 — [Nichibei] Lesson List in BO (Smartphone View)

---

## Suite: [Nichibei] Lesson List – Status Filter Default

### [Nichibei] Lesson List – Status Filter – First Page Load – "Published" is the default value

**Description:** AC 01.1 — Decision Table: On every load of the Lesson List, the Status filter is pre-set to "Published" without any user action.

**Preconditions:**

- Logged into BO as a Nichibei staff user on the Smartphone (non-Limit Teacher)
- At least one Published lesson and one Draft lesson exist for the accessible location

| #   | Action                                                                                 | Expected Result                                                                                    | Test Data |
| --- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | --------- |
| 1   | Navigate to the Lesson List page                                                       | Lesson List page loads                                                                             | —         |
| 2   | Observe the value shown in the Lesson Status filter dropdown without changing anything | The Lesson Status filter shows **"Published"** as the selected value; only Published lessons shown | —         |

**Severity:** major
**Priority:** high

---

### [Nichibei] Lesson List – Status Filter – Return After Opening Lesson Detail – Filter retains user-selected value

**Description:** AC 01.1 — Decision Table: After the user changes the filter to "Draft" and navigates to a Lesson Detail page, returning to the Lesson List shows "Draft" (not reset to "Published").

**Preconditions:**

- Logged into BO as a Nichibei staff user on the Smartphone
- At least one Draft lesson and one Published lesson exist for the accessible location
- Lesson List is open; Status filter currently shows "Published"

| #   | Action                                                                              | Expected Result                                                                           | Test Data |
| --- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | --------- |
| 1   | Change the Status filter to **"Draft"**                                             | Filter updates to "Draft"; lesson list refreshes to show only Draft lessons               | Draft     |
| 2   | Click on a Draft lesson row to open its detail page                                 | Lesson detail page opens for the selected lesson                                          | —         |
| 3   | Click the back button or use the navigation breadcrumb to return to the Lesson List | Lesson List page loads                                                                    | —         |
| 4   | Observe the Lesson Status filter value                                              | Status filter still shows **"Draft"** — it was not reset to "Published" by the navigation | —         |

**Severity:** major
**Priority:** high

---

### [Nichibei] Lesson List – Status Filter – Manual Clear – Filter resets to "Published"

**Description:** AC 01.1 — Decision Table (Negative): When the user manually clears the Status filter, it resets to the "Published" default.

**Preconditions:**

- Logged into BO as a Nichibei staff user on the Smartphone
- Lesson List is open; Status filter currently shows "Draft" (user had previously changed it)

| #   | Action                                                                        | Expected Result                                                                                       | Test Data |
| --- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | --------- |
| 1   | Observe the current value in the Status filter                                | Status filter shows "Draft"                                                                           | —         |
| 2   | Click the clear (×) icon on the Status filter to remove the current selection | Filter selection is cleared                                                                           | —         |
| 3   | Observe the Status filter value after clearing                                | Status filter automatically shows **"Published"**; lesson list updates to show only Published lessons | —         |

**Severity:** major
**Priority:** high

---

## Suite: [Nichibei] Lesson List – Status Filter Changeability

### [Nichibei] Lesson List – Status Filter – Changed to "Draft" – Lesson list shows only Draft lessons

**Description:** AC 01.2 — Equivalence Partitioning: When the user selects "Draft" from the Status filter, only Draft lessons are displayed in the list.

**Preconditions:**

- Logged into BO as a Nichibei staff user on the Smartphone
- At least one Draft lesson and one Published lesson exist for the accessible location
- Lesson List is open; Status filter = "Published"

| #   | Action                                  | Expected Result                                                                                  | Test Data |
| --- | --------------------------------------- | ------------------------------------------------------------------------------------------------ | --------- |
| 1   | Click the Lesson Status filter dropdown | Dropdown opens and shows available status options                                                | —         |
| 2   | Select **"Draft"** from the options     | Filter changes to "Draft"                                                                        | Draft     |
| 3   | Observe the lesson rows in the list     | Only Draft lessons are shown; the previously visible Published lessons are no longer in the list | —         |

**Severity:** normal
**Priority:** medium

---

### [Nichibei] Lesson List – Status Filter – Changed to "Completed" – Lesson list shows only Completed lessons

**Description:** AC 01.2 — Equivalence Partitioning: When the user selects "Completed" from the Status filter, only Completed lessons are displayed in the list.

**Preconditions:**

- Logged into BO as a Nichibei staff user on the Smartphone
- At least one Completed lesson exists for the accessible location
- Lesson List is open; Status filter = "Published"

| #   | Action                                  | Expected Result                                   | Test Data |
| --- | --------------------------------------- | ------------------------------------------------- | --------- |
| 1   | Click the Lesson Status filter dropdown | Dropdown opens and shows available status options | —         |
| 2   | Select **"Completed"** from the options | Filter changes to "Completed"                     | Completed |
| 3   | Observe the lesson rows in the list     | Only Completed lessons are shown in the list      | —         |

**Severity:** normal
**Priority:** medium

---

## Suite: [Nichibei] Lesson List – Limit Teacher – Published Default

### [Nichibei] Lesson List – Limit Teacher – Page Load – Only assigned Published lessons shown

**Description:** AC 01.1 — Permission Matrix: For a Limit Teacher profile, the Lesson List defaults to "Published" AND shows only lessons the teacher is assigned to (both filters active simultaneously).

**Preconditions:**

- The Limit Teacher feature is enabled in Nichibei partner settings
- Teacher A is set up with a **Limit Teacher** profile
- **Published Lesson 1** exists — Teacher A **is assigned**
- **Draft Lesson 2** exists — Teacher A **is assigned**
- **Published Lesson 3** exists — Teacher A **is NOT assigned**

| #   | Action                                           | Expected Result                                                                                               | Test Data             |
| --- | ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- | --------------------- |
| 1   | Login to BO as Teacher A (Limit Teacher profile) | Login successful; BO home page shown                                                                          | Teacher A credentials |
| 2   | Navigate to the Lesson List page                 | Lesson List page loads                                                                                        | —                     |
| 3   | Observe the value in the Lesson Status filter    | Status filter shows **"Published"** as the default                                                            | —                     |
| 4   | Observe which lesson rows appear in the list     | **Only "Published Lesson 1"** is visible; "Draft Lesson 2" and "Published Lesson 3" are not shown in the list | —                     |

**Severity:** major
**Priority:** high

---

### [Nichibei] Lesson List – Limit Teacher – Assigned Draft Lesson – Not visible under default Published filter

**Description:** AC 01.1 — Decision Table: A Draft lesson that is assigned to the Limit Teacher does NOT appear in the list when the Status filter defaults to "Published".

**Preconditions:**

- The Limit Teacher feature is enabled
- Teacher A (Limit Teacher profile) is assigned to **Draft Lesson 2**
- Lesson List is open as Teacher A; Status filter = "Published" (default)

| #   | Action                                                                 | Expected Result                                                    | Test Data                |
| --- | ---------------------------------------------------------------------- | ------------------------------------------------------------------ | ------------------------ |
| 1   | Observe the Lesson List with the default "Published" filter active     | Only Published lessons assigned to Teacher A are shown in the list | —                        |
| 2   | Search or scroll to find **Draft Lesson 2** by its lesson name or date | Draft Lesson 2 does **not** appear anywhere in the list            | Draft Lesson 2 name/date |

**Severity:** major
**Priority:** high

---

### [Nichibei] Lesson List – Limit Teacher – Unassigned Published Lesson – Not visible in list

**Description:** AC 01.1 — Decision Table: A Published lesson that is NOT assigned to the Limit Teacher is not visible even though the Status filter matches "Published".

**Preconditions:**

- The Limit Teacher feature is enabled
- Teacher A (Limit Teacher profile) is logged in
- **Published Lesson 3** exists at Teacher A's location; Teacher A is **NOT assigned** to it
- Status filter = "Published" (default)

| #   | Action                                                                     | Expected Result                                                                              | Test Data                    |
| --- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | ---------------------------- |
| 1   | Observe the Lesson List with the default "Published" filter active         | Only Teacher A's assigned Published lessons are shown                                        | —                            |
| 2   | Search or scroll to find **Published Lesson 3** by its lesson name or date | Published Lesson 3 does **not** appear in the list (Limit Teacher scope excludes unassigned) | Published Lesson 3 name/date |

**Severity:** major
**Priority:** high

---

### [Nichibei] Lesson List – Limit Teacher – Filter Changed to "Draft" – Only assigned Draft lessons visible

**Description:** AC 01.1 + AC 01.2 — Decision Table: When a Limit Teacher changes the filter to "Draft", only their assigned Draft lessons are shown (Limit Teacher scope continues to apply; unassigned Draft lessons remain hidden).

**Preconditions:**

- The Limit Teacher feature is enabled
- Teacher A (Limit Teacher profile) is assigned to **Draft Lesson 2** and **Published Lesson 1**
- **Draft Lesson 4** exists; Teacher A is **NOT assigned** to it
- Lesson List is open as Teacher A; Status filter currently = "Published"

| #   | Action                                                   | Expected Result                                                                                                                  | Test Data |
| --- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | Change the Status filter from "Published" to **"Draft"** | Filter updates to "Draft"                                                                                                        | Draft     |
| 2   | Observe which lesson rows appear in the list             | Only **Draft Lesson 2** (assigned to Teacher A) is visible; "Draft Lesson 4" (unassigned) and "Published Lesson 1" are not shown | —         |

**Severity:** major
**Priority:** high

---

## Suite: [Nichibei] Lesson List – Collect Attendance Entry Point

### [Nichibei] Lesson List – Collect Attendance – Published Lesson – Entry point opens Collect Attendance page

**Description:** AC 03.1 — State Transition Testing: For a Published lesson row, the Collect Attendance entry point is visible and navigates to the existing Collect Attendance page for that lesson.

**Preconditions:**

- Logged into BO as a Nichibei staff user on the Smartphone with permission to collect attendance
- A Published lesson (**Lesson X**) exists with at least one student assigned
- Lesson List is open; Status filter = "Published"

| #   | Action                                                       | Expected Result                                                                             | Test Data |
| --- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------- | --------- |
| 1   | Locate **Lesson X** (Published) in the Lesson List           | Lesson X row is visible in the list                                                         | —         |
| 2   | Observe the action area on the Lesson X row                  | A **Collect Attendance** entry point (button, icon, or link) is visible on the row          | —         |
| 3   | Click the Collect Attendance entry point on the Lesson X row | Navigation action is triggered                                                              | —         |
| 4   | Observe the page that loads                                  | The **Collect Attendance page** opens, displaying the list of students assigned to Lesson X | —         |

**Severity:** major
**Priority:** high

---

### [Nichibei] Lesson List – Collect Attendance – Draft Lesson – Entry point not available

**Description:** AC 03.1 — Negative Testing: For a Draft lesson row, the Collect Attendance entry point is not visible or is disabled — staff cannot open Collect Attendance from a Draft lesson.

**Preconditions:**

- Logged into BO as a Nichibei staff user on the Smartphone
- A Draft lesson (**Draft Lesson Y**) exists with at least one student assigned
- Lesson List is open; Status filter is changed to "Draft"

| #   | Action                                            | Expected Result                                                                   | Test Data |
| --- | ------------------------------------------------- | --------------------------------------------------------------------------------- | --------- |
| 1   | Change the Status filter to **"Draft"**           | Filter updates to "Draft"; Draft lessons appear in the list                       | Draft     |
| 2   | Locate **Draft Lesson Y** in the list             | Draft Lesson Y row is visible                                                     | —         |
| 3   | Inspect the action area on the Draft Lesson Y row | No Collect Attendance entry point is visible or available on the Draft lesson row | —         |

**Severity:** major
**Priority:** high

---

### [Nichibei] Lesson List – Collect Attendance – Completed Lesson – Entry point not available

**Description:** AC 03.1 — Negative Testing: For a Completed lesson row, the Collect Attendance entry point is not visible or is disabled.

**Preconditions:**

- Logged into BO as a Nichibei staff user on the Smartphone
- A Completed lesson (**Completed Lesson Z**) exists
- Lesson List is open; Status filter is changed to "Completed"

| #   | Action                                                | Expected Result                                                                       | Test Data |
| --- | ----------------------------------------------------- | ------------------------------------------------------------------------------------- | --------- |
| 1   | Change the Status filter to **"Completed"**           | Filter updates to "Completed"; Completed lessons appear in the list                   | Completed |
| 2   | Locate **Completed Lesson Z** in the list             | Completed Lesson Z row is visible                                                     | —         |
| 3   | Inspect the action area on the Completed Lesson Z row | No Collect Attendance entry point is visible or available on the Completed lesson row | —         |

**Severity:** major
**Priority:** high

---

### [Nichibei] Lesson List – Collect Attendance – Cancelled Lesson – Entry point not available

**Description:** AC 03.1 — Negative Testing: For a Cancelled lesson row, the Collect Attendance entry point is not visible or is disabled.

**Preconditions:**

- Logged into BO as a Nichibei staff user on the Smartphone
- A Cancelled lesson (**Cancelled Lesson W**) exists
- Lesson List is open; Status filter is changed to "Cancelled"

| #   | Action                                                | Expected Result                                                                       | Test Data |
| --- | ----------------------------------------------------- | ------------------------------------------------------------------------------------- | --------- |
| 1   | Change the Status filter to **"Cancelled"**           | Filter updates to "Cancelled"; Cancelled lessons appear in the list                   | Cancelled |
| 2   | Locate **Cancelled Lesson W** in the list             | Cancelled Lesson W row is visible                                                     | —         |
| 3   | Inspect the action area on the Cancelled Lesson W row | No Collect Attendance entry point is visible or available on the Cancelled lesson row | —         |

**Severity:** major
**Priority:** high

---

## Suite: [Nichibei] Collect Attendance – Attendance Remark – Booking Flow Source

### [Nichibei] Collect Attendance – Attendance Remark – Student Booked with Remark – "Booking Note:" prefix shown read-only in student row

**Description:** AC 02.1 + AC 02.2 — Decision Table: When a student submitted a remark through the Lesson Booking flow, the Collect Attendance page shows that remark as a read-only inline field in the student's row, prefixed with "Booking Note: ".

**Preconditions:**

- Nichibei Lesson Booking feature is enabled
- **Student A** has booked **Published Lesson X** and entered the booking remark: `"Please arrange front row seat"`
- The remark is saved in the system with the "Booking Note: " prefix
- Lesson X is in **Published** status
- Staff is logged into BO with permission to collect attendance

| #   | Action                                                                             | Expected Result                                                                                                           | Test Data |
| --- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | From the Lesson List, click the **Collect Attendance** entry point on **Lesson X** | Collect Attendance page opens, showing the list of students assigned to Lesson X                                          | —         |
| 2   | Locate **Student A's** row in the student list                                     | Student A's row is visible                                                                                                | —         |
| 3   | Observe the remark area in Student A's row                                         | A read-only text field shows: **"Booking Note: Please arrange front row seat"** — displayed inline within Student A's row | —         |
| 4   | Attempt to click or interact with the remark text in Student A's row               | No text cursor appears; the remark area does not become an input field; the text remains unchanged                        | —         |

**Severity:** major
**Priority:** high

---

## Suite: [Nichibei] Collect Attendance – Attendance Remark – Submit Attendance Source

### [Nichibei] Collect Attendance – Attendance Remark – Student Submitted via Mobile Attendance – Remark shown read-only without prefix

**Description:** AC 02.1 + AC 02.2 — Decision Table: When a student submitted a remark via the Mobile Submit Attendance flow (not the Booking flow), the remark appears read-only in the student's row without the "Booking Note: " prefix.

**Preconditions:**

- **Student B** has submitted attendance for **Published Lesson X** via the Mobile app and entered the remark: `"Will arrive 10 minutes late"`
- The remark is saved from the Submit Attendance flow (no "Booking Note: " prefix)
- Staff is logged into BO with permission to collect attendance

| #   | Action                                                                             | Expected Result                                                                                                            | Test Data |
| --- | ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | From the Lesson List, click the **Collect Attendance** entry point on **Lesson X** | Collect Attendance page opens, showing the student list                                                                    | —         |
| 2   | Locate **Student B's** row in the student list                                     | Student B's row is visible                                                                                                 | —         |
| 3   | Observe the remark area in Student B's row                                         | A read-only text field shows: **"Will arrive 10 minutes late"** — no "Booking Note: " prefix — displayed inline in the row | —         |
| 4   | Attempt to click or interact with the remark text in Student B's row               | No text cursor appears; the remark area does not become an input field                                                     | —         |

**Severity:** major
**Priority:** high

---

## Suite: [Nichibei] Collect Attendance – Attendance Remark – Empty and Edge Cases

### [Nichibei] Collect Attendance – Attendance Remark – No Student Submission – Remark area is blank

**Description:** AC 02.2 — Equivalence Partitioning: When a student has not submitted any attendance remark from either the Booking or Mobile Attendance flow, the remark area in their row is blank — no placeholder text, no error message, no loading indicator.

**Preconditions:**

- **Student C** is assigned to **Published Lesson X**
- Student C has **not** submitted any attendance remark through any flow
- Staff is logged into BO

| #   | Action                                                                             | Expected Result                                                                                       | Test Data |
| --- | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | --------- |
| 1   | From the Lesson List, click the **Collect Attendance** entry point on **Lesson X** | Collect Attendance page opens                                                                         | —         |
| 2   | Locate **Student C's** row in the student list                                     | Student C's row is visible                                                                            | —         |
| 3   | Observe the remark area in Student C's row                                         | The remark area is **blank** — no text, no error message, no placeholder such as "No remark" or "N/A" | —         |

**Severity:** major
**Priority:** high

---

## Suite: [Nichibei] Collect Attendance – Page Functionality – Lesson List Entry

### [Nichibei] Collect Attendance – Lesson List Entry – Attendance Radio Buttons – All options available and respond to selection

**Description:** AC 03.3 — Regression Analysis: After opening Collect Attendance from the Lesson List entry point, all attendance radio button options are present for each student row and respond to selection.

**Preconditions:**

- Logged into BO as a Nichibei staff user on the Smartphone with permission to collect attendance
- **Published Lesson X** exists with **Student A** and **Student B** both assigned
- No attendance has been recorded for either student yet
- Staff opens Collect Attendance from the Lesson List entry point on Lesson X

| #   | Action                                                                             | Expected Result                                                                                            | Test Data |
| --- | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | --------- |
| 1   | From the Lesson List, click the **Collect Attendance** entry point on **Lesson X** | Collect Attendance page opens; student list is visible                                                     | —         |
| 2   | Observe the attendance options available in **Student A's** row                    | Radio buttons for **Attend**, **Absent**, **Late**, and **Leave Early** are all visible in Student A's row | —         |
| 3   | Select **"Absent"** for Student A's row                                            | The "Absent" radio button is highlighted/selected for Student A; no error shown                            | Absent    |
| 4   | Select **"Late"** for Student B's row                                              | The "Late" radio button is highlighted/selected for Student B; no error shown                              | Late      |

**Severity:** major
**Priority:** high

---

### [Nichibei] Collect Attendance – Lesson List Entry – Save Button – Attendance record saved and persisted

**Description:** AC 03.3 — Regression Analysis: After selecting attendance options and clicking Save via the Lesson List entry point, the attendance data is saved and persists when the Collect Attendance page is re-opened.

**Preconditions:**

- Logged into BO as a Nichibei staff user on the Smartphone with permission to collect attendance
- **Published Lesson X** exists with **Student A** assigned
- No attendance has been recorded for Lesson X yet

| #   | Action                                                                                | Expected Result                                                                              | Test Data |
| --- | ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | --------- |
| 1   | From the Lesson List, click the **Collect Attendance** entry point on **Lesson X**    | Collect Attendance page opens with the student list                                          | —         |
| 2   | Select **"Attend"** for **Student A's** row                                           | "Attend" radio button is selected for Student A                                              | Attend    |
| 3   | Click the **Save** button at the bottom of the page                                   | A success confirmation is shown (or the page updates without an error message)               | —         |
| 4   | Navigate away from the Collect Attendance page (e.g. back to the Lesson List)         | Lesson List page loads                                                                       | —         |
| 5   | Re-open the Collect Attendance page for **Lesson X** from the Lesson List entry point | Collect Attendance page opens                                                                | —         |
| 6   | Observe Student A's attendance status                                                 | Student A's attendance shows **"Attend"** — the previously saved selection has been retained | —         |

**Severity:** major
**Priority:** high
