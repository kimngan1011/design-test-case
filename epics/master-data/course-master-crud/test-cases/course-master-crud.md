# Test Cases: Course Master – CRUD

## Suite: Course Master – Create

### Course Master – Create – Duplicate Partner Internal Id – Validation Error Shown

**Description:** CRUD – Create (Negative) – Attempt to create a Course Master with a Partner Internal Id already used by another record; verify the system shows a duplicate validation error and no new record is created.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master record already exists with Partner Internal Id = pid_existing

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|----------|
| 1 | Click New to open the new Course Master form | New Course Master form opens | "" |
| 2 | Enter a unique value in the Name field | Name field shows TestCourse_DupPID | "TestCourse_DupPID" |
| 3 | Enter the same Partner Internal Id as the existing record | Field shows pid_existing | "pid_existing" |
| 4 | Enter a value in Course Code | Field shows code_dup_pid | "code_dup_pid" |
| 5 | Click Save | System shows a duplicate or uniqueness validation error on the Partner Internal Id field; record is NOT created | "" |

**Severity:** major
**Priority:** high

---

### Course Master – Create – Required Fields Only – Record Saved and Appears in List

**Description:** CRUD – Create (EP) – Create a Course Master with only Name, Partner Internal Id, and Course Code filled in; verify the record is saved and visible in the list.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- Navigated to Master > Course Master list view

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Click the **New** button | New Course Master form opens; Teaching Method defaults to 個別; all other fields are empty | "" |
| 2 | Enter a value in the **Name** field | Name field shows the entered value | "TestCourse_Create_001" |
| 3 | Enter a value in the **Partner Internal Id** field | Partner Internal Id field shows the entered value | "partner_create_001" |
| 4 | Enter a value in the **Course Code** field | Course Code field shows the entered value | "code_create_001" |
| 5 | Leave **Teaching Ratio** and **Sequence Number** empty | Both fields remain blank | "" |
| 6 | Click **Save** | Record is saved; detail page of the new Course Master opens showing all entered values | "" |
| 7 | Navigate back to the Course Master list | Record "TestCourse_Create_001" appears in the list with correct Course Code and Partner Internal Id | "" |

**Severity:** major
**Priority:** high

---

### Course Master – Create – All Fields – All Values Persisted on Detail Page

**Description:** CRUD – Create (EP) – Create a Course Master with all fields filled in and verify every field value is displayed correctly on the detail page.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- Navigated to Master > Course Master list view

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Click **New** | New Course Master form opens | "" |
| 2 | Enter a value in the **Name** field | Name field shows entered value | "TestCourse_AllFields_001" |
| 3 | Enter a value in the **Partner Internal Id** field | Field shows entered value | "partner_all_001" |
| 4 | Enter a value in the **Course Code** field | Field shows entered value | "code_all_001" |
| 5 | Select a value in **Teaching Method** | Field shows selected value | "グループ" |
| 6 | Enter a value in **Teaching Ratio** | Field shows entered value | "3" |
| 7 | Enter a value in **Sequence Number** | Field shows entered value | "10" |
| 8 | Click **Save** | Record saved; detail page opens | "" |
| 9 | Verify all fields in the **Information** section on the detail page | Name = TestCourse_AllFields_001, Partner Internal Id = partner_all_001, Course Code = code_all_001, Teaching Method = グループ, Teaching Ratio = 3, Sequence Number = 10 | "" |

**Severity:** minor
**Priority:** medium

---

### Course Master – Create – Name Missing – Validation Error Shown

**Description:** CRUD – Create (Negative) – Attempt to save a new Course Master without entering the required Name field; expect a field-level validation error and no record created.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- New Course Master form is open

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Leave **Name** empty | Name field remains blank | "" |
| 2 | Enter a value in **Partner Internal Id** | Field shows value | "partner_err_001" |
| 3 | Enter a value in **Course Code** | Field shows value | "code_err_001" |
| 4 | Click **Save** | Validation error appears on the **Name** field ("Complete this field"); record is NOT saved | "" |

**Severity:** major
**Priority:** high

---

### Course Master – Create – Partner Internal Id Missing – Validation Error Shown

**Description:** CRUD – Create (Negative) – Attempt to save a new Course Master without the required Partner Internal Id; expect a validation error and no record created.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- New Course Master form is open

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Enter a value in **Name** | Field shows value | "TestCourse_MissPID" |
| 2 | Leave **Partner Internal Id** empty | Field remains blank | "" |
| 3 | Enter a value in **Course Code** | Field shows value | "code_miss_pid" |
| 4 | Click **Save** | Validation error appears on the **Partner Internal Id** field; record is NOT saved | "" |

**Severity:** major
**Priority:** high

---

### Course Master – Create – Course Code Missing – Validation Error Shown

**Description:** CRUD – Create (Negative) – Attempt to save a new Course Master without the required Course Code; expect a validation error and no record created.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- New Course Master form is open

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Enter a value in **Name** | Field shows value | "TestCourse_MissCode" |
| 2 | Enter a value in **Partner Internal Id** | Field shows value | "partner_miss_code" |
| 3 | Leave **Course Code** empty | Field remains blank | "" |
| 4 | Click **Save** | Validation error appears on the **Course Code** field; record is NOT saved | "" |

**Severity:** major
**Priority:** high

---

### Course Master – Create – Save & New – Current Record Saved and Blank Form Reopens

**Description:** CRUD – Create (Scenario) – Use "Save & New" to save a Course Master and open a fresh empty form in one action.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- New Course Master form is open

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Fill in **Name**, **Partner Internal Id**, **Course Code** | All three required fields are filled | "Name = SaveNew_TC, PID = sn_tc, Code = sn_tc" |
| 2 | Click **Save & New** | Current record is saved; a new, empty Course Master form opens immediately | "" |
| 3 | Confirm the new form is blank | Name, Partner Internal Id, Course Code fields are all empty; Teaching Method defaults to 個別 | "" |
| 4 | Navigate to the Course Master list | Record "SaveNew_TC" appears in the list | "" |

**Severity:** minor
**Priority:** medium

---

### Course Master – Create – Cancel – Form Closed and No Record Created

**Description:** CRUD – Create (Negative) – Click Cancel on the new Course Master form and verify no record is persisted.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- New Course Master form is open

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Enter a value in **Name** | Name field shows value | "TestCourse_Cancel" |
| 2 | Click **Cancel** | Form closes; returns to the Course Master list | "" |
| 3 | Search for "TestCourse_Cancel" in the Course Master list | No record with the name "TestCourse_Cancel" is found | "TestCourse_Cancel" |

**Severity:** trivial
**Priority:** low

---

## Suite: Course Master – Read

### Course Master – List View – Name, Course Code, Partner Internal Id and Last Modified Date Columns Displayed

**Description:** CRUD – Read (Component) – Navigate to the Course Master list and verify the expected columns are present and show data.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- At least one Course Master record exists

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to **Master > Course Master** | Course Master list view loads | "" |
| 2 | Inspect the column headers in the list | Columns displayed: **Name**, **Course Code**, **Partner Internal Id**, **Last Modified Date** | "" |
| 3 | Inspect the data in the first visible row | Each column shows a non-empty value | "" |

**Severity:** minor
**Priority:** medium

---

### Course Master – Detail View – Information Fields and Related Lists Displayed

**Description:** CRUD – Read (Component) – Open a Course Master detail page and verify the Information fields, action buttons, and related list tabs are all displayed correctly.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master record with at least one Location Course linked exists

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Click a Course Master record from the list | Detail page opens | "" |
| 2 | Inspect the **Information** section | Fields visible: Name, Partner Internal Id, Course Code, Teaching Method, Teaching Ratio, Sequence Number | "" |
| 3 | Inspect the action buttons at the top right | **Generate Courses**, **Edit**, and **Clone** buttons are visible | "" |
| 4 | Inspect the related list tabs below the Information section | **Course Offering** and **Location Course** tabs are displayed | "" |
| 5 | Click the **Location Course** tab | Location Course list appears with columns: Account, Name, Last Modified Date | "" |

**Severity:** minor
**Priority:** medium

---

## Suite: Course Master – Update

### Course Master – Edit – Change Name – Updated Value Saved on Detail Page

**Description:** CRUD – Update (EP) – Edit an existing Course Master and change its Name; verify the updated value is saved and reflected on the detail page and list.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master record "EditSource_TC" (Code = edit_src, PID = edit_pid) exists

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the detail page of "EditSource_TC" | Detail page shows Name = EditSource_TC | "" |
| 2 | Click **Edit** | Edit form opens with current values pre-filled | "" |
| 3 | Clear **Name** and enter a new value | Name field shows new value | "EditUpdated_TC" |
| 4 | Click **Save** | Record saved; detail page shows Name = EditUpdated_TC | "EditUpdated_TC" |
| 5 | Navigate to the Course Master list | "EditUpdated_TC" appears in the list; "EditSource_TC" is no longer shown | "" |

**Severity:** major
**Priority:** high

---

### Course Master – Edit – Update Multiple Fields – All Changes Saved on Detail Page

**Description:** CRUD – Update (EP) – Edit Course Code, Teaching Method, Teaching Ratio, and Sequence Number; verify all updated values are persisted on the detail page.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master record exists with Course Code = code_old, Teaching Method = 個別, Teaching Ratio = (empty), Sequence Number = (empty)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Course Master detail page | Course Code = code_old, Teaching Method = 個別, Teaching Ratio and Sequence Number are empty | "" |
| 2 | Click **Edit** | Edit form opens with current values | "" |
| 3 | Clear **Course Code** and enter a new value | Field shows code_new | "code_new" |
| 4 | Select a new value for **Teaching Method** | Field shows グループ | "グループ" |
| 5 | Enter a value in **Teaching Ratio** | Field shows entered value | "4" |
| 6 | Enter a value in **Sequence Number** | Field shows entered value | "7" |
| 7 | Click **Save** | Record saved; detail page shows Course Code = code_new, Teaching Method = グループ, Teaching Ratio = 4, Sequence Number = 7 | "" |

**Severity:** minor
**Priority:** medium

---

### Course Master – Edit – Partner Internal Id Change Attempted – Error Message Shown

**Description:** CRUD – Update (Negative) – Attempt to change the Partner Internal Id of an existing Course Master; verify the system shows an error message and the change is not saved.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master record EditPID_TC exists with Partner Internal Id = pid_original

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|----------|
| 1 | Open the detail page of EditPID_TC | Detail page shows Partner Internal Id = pid_original | "" |
| 2 | Click **Edit** | Edit form opens with current values pre-filled | "" |
| 3 | Clear **Partner Internal Id** and enter a new value | Field accepts the input and shows pid_changed | "pid_changed" |
| 4 | Click **Save** | System shows an error message; record is NOT saved with the new Partner Internal Id | "" |
| 5 | Navigate back to the detail page of EditPID_TC | Partner Internal Id still shows pid_original (unchanged) | "" |

**Severity:** major
**Priority:** high

---

### Course Master – Edit – Name Updated When Location Course and Course Offering Are Linked – Update Succeeds

**Description:** CRUD – Update (Scenario) – Edit the Name of a Course Master that has linked Location Course, Course Offering, and transaction data; verify the update succeeds and the new name is reflected on the detail page and list.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master record LinkedCM_TC exists with:
  - At least 1 linked Location Course
  - At least 1 linked Course Offering
  - At least 1 associated transaction record

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|----------|
| 1 | Open the detail page of LinkedCM_TC | Detail page shows Name = LinkedCM_TC; Location Course and Course Offering related lists show linked records | "" |
| 2 | Click **Edit** | Edit form opens with current values pre-filled | "" |
| 3 | Clear the **Name** field and enter a new value | Name field shows LinkedCM_Updated | "LinkedCM_Updated" |
| 4 | Click **Save** | Record is saved successfully; no error shown; detail page displays Name = LinkedCM_Updated | "" |
| 5 | Verify the Location Course and Course Offering related lists are still present on the detail page | Linked Location Courses and Course Offerings are still visible and unaffected by the name change | "" |
| 6 | Navigate to the Course Master list | Record appears in the list as LinkedCM_Updated; LinkedCM_TC is no longer shown | "" |

**Severity:** major
**Priority:** high

---

## Suite: Course Master – Delete

### Course Master – Delete – Record No Longer Appears in List After Deletion

**Description:** CRUD – Delete (Negative) – Delete a Course Master record using the dropdown action and confirm it is removed from the list.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master record "ToDelete_TC" exists with no active dependencies

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the detail page of "ToDelete_TC" | Detail page opens | "" |
| 2 | Click the dropdown arrow (▼) next to the **Clone** button | Dropdown menu appears with a **Delete** option | "" |
| 3 | Click **Delete** | A confirmation dialog appears | "" |
| 4 | Confirm the deletion in the dialog | Record is deleted; page redirects to the Course Master list | "" |
| 5 | Search for "ToDelete_TC" in the list | "ToDelete_TC" is no longer present in the list | "ToDelete_TC" |

**Severity:** major
**Priority:** high

---

### Course Master – Delete – Record Has Linked Location Course and Course Offering – Deletion Blocked

**Description:** CRUD – Delete (Negative) – Attempt to delete a Course Master that has linked Location Course, Course Offering, and transaction data; verify the system prevents deletion and shows an error.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master record LinkedDelete_TC exists with:
  - At least 1 linked Location Course
  - At least 1 linked Course Offering
  - At least 1 associated transaction record

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|----------|
| 1 | Open the detail page of LinkedDelete_TC | Detail page opens; Location Course and Course Offering related lists show linked records | "" |
| 2 | Click the dropdown arrow (▼) next to the **Clone** button | Dropdown menu appears with a Delete option | "" |
| 3 | Click **Delete** | A confirmation dialog appears | "" |
| 4 | Confirm the deletion in the dialog | System shows an error message indicating the record cannot be deleted because it has linked data; record remains in the system | "" |
| 5 | Navigate to the Course Master list | LinkedDelete_TC is still present in the list | "" |

**Severity:** major
**Priority:** high

---

## Suite: Course Master – Clone

### Course Master – Clone – New Record Pre-Filled with Source Values

**Description:** CRUD – Clone (Scenario) – Clone an existing Course Master; verify the new form is pre-filled with source values and both records coexist after saving.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master record "CloneSource_TC" (Code = clone_src, PID = pid_src, Teaching Method = 個別) exists

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the detail page of "CloneSource_TC" | Detail page opens showing all field values | "" |
| 2 | Click **Clone** | New Course Master form opens pre-filled: Name = CloneSource_TC, Code = clone_src, PID = pid_src, Teaching Method = 個別 | "" |
| 3 | Change **Name** to a unique value | Name field shows the new value | "CloneTarget_TC" |
| 4 | Click **Save** | Cloned record saved; detail page of "CloneTarget_TC" opens | "" |
| 5 | Navigate to the Course Master list | Both "CloneSource_TC" and "CloneTarget_TC" appear in the list | "" |

**Severity:** minor
**Priority:** medium

---
