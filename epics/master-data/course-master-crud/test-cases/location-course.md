# Test Cases: Location Course – CRUD, Import and Sync

## Suite: Location Course – Generate

### Location Course – Generate Courses – Location Selected – Location Course Created and Linked

**Description:** CRUD – Generate (Scenario) – Click Generate Courses on a Course Master, select a Location, and verify a Location Course is created and linked to the Course Master.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master "GenLC_TC" exists with no Location Course for Location_H001
- Location_H001 exists in the system

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the detail page of "GenLC_TC" | Detail page opens; Location Course related list shows 0 items | "" |
| 2 | Click **Generate Courses** | Generate Course dialog opens with Academic Year and Location fields | "" |
| 3 | Leave **Academic Year** empty | Field remains blank | "" |
| 4 | Select "Location_H001" in the **Location** field | Location field shows Location_H001 | "Location_H001" |
| 5 | Click **Add** | Dialog closes; success feedback shown | "" |
| 6 | Click the **Location Course** tab on the Course Master detail page | Location Course list shows 1 item: "GenLC_TC - Location_H001" linked to Account = Location_H001 and Course Master = GenLC_TC | "" |

**Severity:** major
**Priority:** high

---

### Location Course – Generate Courses – Name Auto-Set to Course Master Name – Location Name Format

**Description:** CRUD – Generate (Scenario) – Verify the Location Course name is automatically set to the format `<Course Master Name> - <Location Name>` when generated; it cannot be changed to any other format.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master "NameFormat_TC" exists
- Location "Location_H002" exists

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Click **Generate Courses** on the detail page of "NameFormat_TC" | Generate Course dialog opens | "" |
| 2 | Select "Location_H002" in the **Location** field | Field shows Location_H002 | "Location_H002" |
| 3 | Click **Add** | Location Course is created | "" |
| 4 | Click the **Location Course** tab and open the newly created record | Detail page of Location Course opens; Name = "NameFormat_TC - Location_H002" | "" |

**Severity:** major
**Priority:** high

---

### Location Course – Generate Courses – No Location Selected – Location Course Not Created

**Description:** CRUD – Generate (Negative) – Attempt to generate a Location Course without selecting a Location; verify no Location Course is created.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master "GenNoLoc_TC" exists

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the detail page of "GenNoLoc_TC" | Location Course tab shows 0 items | "" |
| 2 | Click **Generate Courses** | Generate Course dialog opens | "" |
| 3 | Leave both **Academic Year** and **Location** empty | Both fields remain blank | "" |
| 4 | Click **Add** | System shows a validation message or Add button is disabled; dialog does not proceed with empty fields | "" |
| 5 | Close the dialog and check the Location Course tab | Location Course list still shows 0 items for "GenNoLoc_TC" | "" |

**Severity:** minor
**Priority:** medium

---

### Location Course – Generate Courses – Duplicate Location for Same Course Master – Error Shown

**Description:** CRUD – Generate (Negative) – Attempt to generate a Location Course with a Location already linked to the same Course Master; verify the system prevents duplicate creation and shows an error.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master "DupLoc_TC" exists with a Location Course already created for Location_H001

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the detail page of "DupLoc_TC" | Location Course tab shows 1 item for Location_H001 | "" |
| 2 | Click **Generate Courses** | Generate Course dialog opens | "" |
| 3 | Select "Location_H001" in the **Location** field | Field shows Location_H001 | "Location_H001" |
| 4 | Click **Add** | System shows an error indicating a Location Course for Location_H001 already exists for this Course Master; duplicate record is NOT created | "" |
| 5 | Click the **Location Course** tab | Location Course list still shows exactly 1 item for Location_H001 (no duplicate) | "" |

**Severity:** major
**Priority:** high

---

## Suite: Location Course – Read

### Location Course – List View – Name, Account, Course Master Columns Displayed

**Description:** CRUD – Read (Component) – Navigate to the Location Course list and verify the expected columns are present and populated.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- At least one Location Course record exists

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to **Master > Location Course** | Location Course list view loads | "" |
| 2 | Inspect the column headers | Columns displayed: Name, Account, Course Master, Last Modified Date | "" |
| 3 | Inspect the data in the first visible row | Each column shows a non-empty value | "" |

**Severity:** minor
**Priority:** medium

---

### Location Course – Detail View – Active Student, Inactive Student, Classes Tabs Displayed

**Description:** CRUD – Read (Component) – Open a Location Course detail page and verify the Information section, related list tabs, and key fields are displayed correctly.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Location Course "ReadLC_TC - Location_H001" exists linked to Course Master "ReadLC_TC"

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Location Course detail page | Detail page opens showing Name = "ReadLC_TC - Location_H001" | "" |
| 2 | Inspect the action buttons at the top right | **Edit**, **Delete**, **Change Owner** buttons are visible | "" |
| 3 | Inspect the **Information** section | Fields visible: Name, Account, Course Master, Teaching Ratio | "" |
| 4 | Inspect the tabs in the related list area | **Active Student**, **Inactive Student**, **Classes** tabs are displayed | "" |

**Severity:** minor
**Priority:** medium

---

## Suite: Location Course – Update

### Location Course – Edit – Teaching Ratio – Updated Value Saved on Detail Page

**Description:** CRUD – Update (EP) – Edit the Teaching Ratio field of a Location Course and verify the updated value is saved on the detail page.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Location Course "EditLC_TC - Location_H001" exists with Teaching Ratio = (empty)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the detail page of "EditLC_TC - Location_H001" | Detail page shows Teaching Ratio = (empty) | "" |
| 2 | Click **Edit** | Edit form opens; Name, Account, Course Master fields are visible | "" |
| 3 | Enter a value in **Teaching Ratio** | Field shows entered value | "1:2" |
| 4 | Click **Save** | Record saved; detail page shows Teaching Ratio = "1:2" | "" |

**Severity:** minor
**Priority:** medium

---

### Location Course – Edit – Attempt to Change Name to Non-Standard Format – Error Message Shown

**Description:** CRUD – Update (Negative) – Attempt to edit the Name of a Location Course to a value that does not follow the `<Course Master Name> - <Location Name>` format; verify an error is shown and the name is not saved.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Location Course "EditNameLC_TC - Location_H001" exists

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the detail page of "EditNameLC_TC - Location_H001" | Detail page opens; Name = "EditNameLC_TC - Location_H001" | "" |
| 2 | Click **Edit** | Edit form opens | "" |
| 3 | Clear the **Name** field and enter a value that does not follow the required format | Name field shows the non-standard value | "MyCustomName" |
| 4 | Click **Save** | System shows an error: "Location Course's name format should be: <Course Master Name - Location Name>"; record is NOT saved with the new name | "" |
| 5 | Click **Cancel** and return to the detail page | Name still shows "EditNameLC_TC - Location_H001" (unchanged) | "" |

**Severity:** major
**Priority:** high

---

### Location Course – Edit – Attempt to Change Account – Field Not Editable

**Description:** CRUD – Update (Negative) – Attempt to change the Account (Location) field of an existing Location Course; verify the field is not editable or the change is blocked.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Location Course "EditAccLC_TC - Location_H001" exists linked to Account = Location_H001

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the detail page of "EditAccLC_TC - Location_H001" | Detail page shows Account = Location_H001 | "" |
| 2 | Click **Edit** | Edit form opens | "" |
| 3 | Attempt to modify the **Account** field | Account field is not editable, or system shows an error when a different account is entered | "" |
| 4 | Click **Save** (or Cancel) | Account remains = Location_H001 (unchanged) | "" |

**Severity:** major
**Priority:** high

---

## Suite: Location Course – Delete

### Location Course – Delete – No Active Students – Record Removed From List

**Description:** CRUD – Delete – Delete a Location Course with no active students and verify it is removed from the list.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Location Course "DeleteLC_TC - Location_H001" exists with 0 active students

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the detail page of "DeleteLC_TC - Location_H001" | Detail page opens; Active Student tab shows 0 items | "" |
| 2 | Click **Delete** | A confirmation dialog appears | "" |
| 3 | Confirm the deletion | Record is deleted; page redirects to Location Course list | "" |
| 4 | Search for "DeleteLC_TC - Location_H001" in the Location Course list | Record is no longer present | "DeleteLC_TC - Location_H001" |

**Severity:** major
**Priority:** high

---

### Location Course – Delete – Active Students Linked – Deletion Blocked

**Description:** CRUD – Delete (Negative) – Attempt to delete a Location Course that has active student records; verify deletion is blocked and an error is shown.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Location Course "BlockDelLC_TC - Location_H001" exists with at least 1 active student

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the detail page of "BlockDelLC_TC - Location_H001" | Detail page opens; Active Student tab shows at least 1 item | "" |
| 2 | Click **Delete** | A confirmation dialog appears | "" |
| 3 | Confirm the deletion | System shows an error message; record is NOT deleted | "" |
| 4 | Navigate to the Location Course list | "BlockDelLC_TC - Location_H001" is still present in the list | "" |

**Severity:** major
**Priority:** high

---

## Suite: Location Course – Import

### Location Course – Import – Valid CSV – Records Created in List

**Description:** Import – Location Course (Scenario) – Upload a valid CSV file via the Import button on the Location Course list and verify the records are created.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A valid Location Course import CSV is prepared with at least 1 new record following the Name format `<Course Master Name> - <Location Name>` with a valid Account and Course Master

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to **Master > Location Course** | Location Course list view loads | "" |
| 2 | Click **Import** | Import wizard opens | "" |
| 3 | Upload the valid CSV file | File is accepted; field mapping step shown | "valid_location_course_import.csv" |
| 4 | Complete the field mapping and confirm import | Import completes; success summary shown with number of records inserted | "" |
| 5 | Search for the imported record name in the Location Course list | Newly imported records appear with correct Account and Course Master | "" |

**Severity:** minor
**Priority:** medium

---

### Location Course – Import – CSV With Duplicate Location for Same Course Master – Duplicate Rows Rejected

**Description:** Import – Location Course (Negative) – Upload a CSV that contains a Location Course with a Location already linked to the same Course Master; verify duplicates are rejected with an error.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Location Course "ImportDupLC_TC - Location_H001" already exists
- An import CSV is prepared with the same Course Master and Location_H001 combination

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to **Master > Location Course** and click **Import** | Import wizard opens | "" |
| 2 | Upload the CSV containing the duplicate row | File accepted; mapping shown | "dup_location_course_import.csv" |
| 3 | Complete field mapping and confirm import | Import completes; summary shows the duplicate row(s) as failed/rejected with a duplicate or uniqueness error; other valid rows may succeed | "" |
| 4 | Search for "ImportDupLC_TC - Location_H001" in the Location Course list | Only the original record remains; no duplicate was created | "" |

**Severity:** major
**Priority:** high

---

## Suite: Location Course – Sync to BO

### Location Course – Sync Data – New Location Course Synced to BO Course Location After Manual Sync

**Description:** Sync – Manual Sync (Scenario) – Create a new Location Course in SF, trigger Sync Data from the Course Master list, and verify the record appears as a Course Location in the Back Office.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A new Location Course "SyncNewLC_TC - Location_H001" has been created and is not yet synced
- Logged in to the Back Office as HQ Staff
- Auto-sync has not yet run since creation

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Confirm "SyncNewLC_TC - Location_H001" exists in the SF Location Course list | Record is present in SF | "" |
| 2 | In BO, search for the corresponding course location under the related course | Location is NOT yet visible in BO course location | "" |
| 3 | In SF, navigate to the **Course Master** list and click **Sync Data** | Sync is triggered; confirmation or progress indicator shown | "" |
| 4 | Wait for sync to complete | Sync completes without error | "" |
| 5 | In BO, search for the course location linked to "SyncNewLC_TC" | Location_H001 now appears as a location under the corresponding BO course | "" |

**Severity:** critical
**Priority:** high

---

### Location Course – Sync Data – Deleted Location Course Removed from BO Course Location After Manual Sync

**Description:** Sync – Manual Sync (Scenario) – Delete a Location Course in SF, trigger Sync Data, and verify the corresponding location is removed from the BO course.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Location Course "SyncDelLC_TC - Location_H001" exists and is already synced (Location_H001 appears in BO course)
- Logged in to the Back Office as HQ Staff

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Confirm Location_H001 is visible as a course location in BO for the corresponding course | Location present in BO | "" |
| 2 | In SF, delete "SyncDelLC_TC - Location_H001" | Record deleted from SF | "" |
| 3 | In BO, confirm Location_H001 is still visible (sync not yet triggered) | Location still present in BO | "" |
| 4 | In SF, navigate to the **Course Master** list and click **Sync Data** | Sync triggered and completes without error | "" |
| 5 | In BO, check the course locations for the corresponding course | Location_H001 is no longer listed as a course location | "" |

**Severity:** critical
**Priority:** high

---

### Location Course – Auto Sync – Location Course Synced to BO After Configured Interval

**Description:** Sync – Auto Sync (State Transition) – Verify a new Location Course created in SF is automatically synced to the BO course location after the org-configured interval elapses without any manual trigger.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- Org auto-sync interval is configured (X hours per org setup)
- today = 2026-06-16; last_sync_time = known; next_sync_time = last_sync_time + X hours
- A Location Course "AutoSyncLC_TC - Location_H001" was created after the last sync ran
- Logged in to the Back Office as HQ Staff

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Confirm the location is NOT yet visible in BO course location immediately after creation | Location absent from BO | "" |
| 2 | Wait until the next scheduled auto-sync time without clicking Sync Data | System runs the auto-sync job automatically at the configured time | "next_sync_time = last_sync_time + X hours" |
| 3 | After auto-sync completes, check the BO course locations | Location_H001 now appears as a course location for the corresponding BO course | "" |

**Severity:** major
**Priority:** high

---
