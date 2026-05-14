# Test Cases: LT-98532 — Bulk Publish Lessons by Student

## Suite: [Riso] Bulk Publish by Student – Publish Modal

---

### [Riso] Bulk Publish Modal – 0 Students in Calendar Filter – "Apply to selected students" checkbox is disabled

**Description:** AC 01.2 — Decision Table — When no student is selected in the Calendar filter before opening the Bulk Publish modal, the "Apply to selected students" checkbox appears but cannot be activated.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- The SF Calendar page is open for a specific period
- No student is selected in the Calendar student filter (filter is empty / "All students")
- At least one Draft lesson exists in the calendar period

| #   | Action                                                                     | Expected Result                                                              | Test Data |
| --- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | --------- |
| 1   | Open the SF Calendar, confirm the student filter shows no selected student | Calendar page is loaded; student filter shows "All students" or no selection | ""        |
| 2   | Click the **Bulk Publish** button                                          | Bulk Publish modal opens                                                     | ""        |
| 3   | Observe the "Apply to selected students" checkbox in the modal             | Checkbox is visible but **disabled** (grayed out, not clickable)             | ""        |
| 4   | Attempt to click the disabled checkbox                                     | Checkbox state does not change; no error shown                               | ""        |

**Severity:** minor
**Priority:** medium

---

### [Riso] Bulk Publish Modal – 0 Students in Filter – Location Field Remains Editable with Multi-Location Support

**Description:** AC 01.2 — Decision Table — When the "Apply to selected students" checkbox is disabled (0 students in filter), the Location field remains editable and the user can select multiple locations.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- SF Calendar is open with no student selected in the filter
- At least 2 locations exist and are accessible to the user

| #   | Action                                                                          | Expected Result                                                                                              | Test Data            |
| --- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | -------------------- |
| 1   | Open the SF Calendar with no student in the filter, then click **Bulk Publish** | Bulk Publish modal opens; "Apply to selected students" checkbox is disabled                                  | ""                   |
| 2   | Observe the Location field in the modal                                         | Location field is **editable** (not locked, not read-only); shows the calendar's current location by default | ""                   |
| 3   | Click the Location field and add a second location                              | Second location is added successfully to the field                                                           | Location: "Branch B" |
| 4   | Confirm both locations are shown in the Location field                          | Location field displays both selected locations                                                              | ""                   |

**Severity:** minor
**Priority:** medium

---

### [Riso] Bulk Publish Modal – 1+ Students in Calendar Filter – Checkbox Appears Enabled and Unchecked by Default

**Description:** AC 01.3 — Decision Table — When at least one student is selected in the Calendar filter before opening the Bulk Publish modal, the "Apply to selected students" checkbox is enabled and unchecked by default.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- SF Calendar is open
- At least 1 student (Student A) is selected in the Calendar student filter
- At least one Draft lesson for Student A exists in the calendar period

| #   | Action                                                     | Expected Result                                                                     | Test Data      |
| --- | ---------------------------------------------------------- | ----------------------------------------------------------------------------------- | -------------- |
| 1   | On the SF Calendar, select Student A in the student filter | Calendar view updates to show Student A's lessons; student filter shows "Student A" | Student A name |
| 2   | Click the **Bulk Publish** button                          | Bulk Publish modal opens                                                            | ""             |
| 3   | Observe the "Apply to selected students" checkbox          | Checkbox is **enabled** (clickable, not grayed out) and **unchecked** by default    | ""             |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Publish Modal – Checkbox Activated – Location Field Locked to Current Calendar Location

**Description:** AC 01.3 — Decision Table — When the user activates the "Apply to selected students" checkbox, the Location field is immediately locked to the calendar's current location and becomes read-only.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- SF Calendar is open; student filter has 1+ students selected
- The calendar's current location is "Hanoi Branch" (a specific named location)
- Bulk Publish modal is open; checkbox is currently unchecked

| #   | Action                                                               | Expected Result                                                                        | Test Data                |
| --- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------ |
| 1   | Open the Bulk Publish modal (checkbox enabled, unchecked)            | Modal is open; Location field shows calendar's current location and is editable        | Location: "Hanoi Branch" |
| 2   | Tick the "Apply to selected students" checkbox                       | Checkbox becomes checked                                                               | ""                       |
| 3   | Observe the Location field immediately after activating the checkbox | Location field is **locked** to "Hanoi Branch"; field shows disabled / read-only state | ""                       |
| 4   | Attempt to click or change the Location field                        | Location field cannot be edited; the value "Hanoi Branch" remains unchanged            | ""                       |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Publish Modal – Checkbox Activated – Cannot Add Extra Locations

**Description:** AC 01.3 — Negative Testing — When the "Apply to selected students" checkbox is activated, the option to add extra locations to the Location field is disabled.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- SF Calendar is open; student filter has 1+ students selected
- Bulk Publish modal is open; the "Apply to selected students" checkbox has been activated (checked)

| #   | Action                                                               | Expected Result                                                                           | Test Data |
| --- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | --------- |
| 1   | Confirm the checkbox is currently checked in the modal               | Checkbox shows checked state; Location field is locked to the calendar's location         | ""        |
| 2   | Attempt to open the Location field dropdown to add a second location | Location field dropdown does not open; the **add location** control is absent or disabled | ""        |
| 3   | Confirm no additional location can be added                          | Only the single locked location is shown in the Location field                            | ""        |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Publish Modal – Checkbox NOT Activated – All Lessons in Period Published (Existing Behavior Preserved)

**Description:** AC 01.3 — Regression Analysis — When the "Apply to selected students" checkbox is NOT activated (even with students in the filter), Bulk Publish works exactly as before LT-98532: all lessons at the selected period and location are published regardless of student.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- SF Calendar is open; 1+ students are selected in the student filter
- Bulk Publish modal is open; "Apply to selected students" checkbox is enabled but **unchecked**
- The period contains 3 Draft lessons: 2 for Student A, 1 for Student B (not in the filter)

| #   | Action                                                                   | Expected Result                                                                                                      | Test Data |
| --- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | Open the Bulk Publish modal with checkbox unchecked                      | Modal is open; checkbox is enabled but unchecked                                                                     | ""        |
| 2   | Complete all required fields and click **Save**                          | Modal closes; success message appears; user is redirected to the calendar view                                       | ""        |
| 3   | Refresh the calendar                                                     | Calendar loads updated lesson statuses                                                                               | ""        |
| 4   | Observe the status of Student A's 2 Draft lessons                        | Both lessons are now **Published**                                                                                   | ""        |
| 5   | Observe the status of Student B's 1 Draft lesson (not in student filter) | Student B's lesson is also **Published** — all lessons in the period were published regardless of the student filter | ""        |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Publish Modal – Student Filter Cannot Be Changed While Modal Is Open

**Description:** AC 01.3 — Decision Table — After the Bulk Publish modal is opened, the Calendar student filter cannot be modified until the modal is closed.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- SF Calendar is open; 1+ students selected in the student filter
- Bulk Publish modal is currently open

| #   | Action                                                                                                | Expected Result                                                                                            | Test Data |
| --- | ----------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | --------- |
| 1   | Open the Bulk Publish modal                                                                           | Modal is open and visible on top of the calendar                                                           | ""        |
| 2   | While the modal is open, attempt to change the Calendar student filter (e.g. add or remove a student) | The student filter **cannot be edited**; it is blocked or the Calendar behind the modal is not interactive | ""        |
| 3   | Close the Bulk Publish modal by clicking **Cancel**                                                   | Modal closes                                                                                               | ""        |
| 4   | Attempt to change the Calendar student filter after the modal is closed                               | Student filter is now **editable** and can be changed                                                      | ""        |

**Severity:** minor
**Priority:** medium

---
