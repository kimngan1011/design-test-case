# Test Cases: Course Offering – CRUD, Import and Sync

## Suite: Course Offering – Generate

### Course Offering – Generate Courses – Academic Year Selected – Course Offering Created and Linked

**Description:** CRUD – Generate (Scenario) – Click Generate Courses on a Course Master, select an Academic Year, and verify a Course Offering is created and linked to the Course Master.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master "GenCO_TC" exists with no Course Offering for Academic Year 2026
- Academic Year 2026 exists in the system

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the detail page of "GenCO_TC" | Detail page opens; Course Offering related list shows 0 items | "" |
| 2 | Click **Generate Courses** | Generate Course dialog opens with Academic Year and Location fields | "" |
| 3 | Select "2026" in the **Academic Year** field | Academic Year field shows 2026 | "2026" |
| 4 | Leave **Location** empty | Location field remains blank | "" |
| 5 | Click **Add** | Dialog closes; success feedback is shown | "" |
| 6 | Click the **Course Offering** tab on the Course Master detail page | Course Offering list shows 1 item: "[2026] GenCO_TC" linked to Academic Year 2026 | "" |
| 7 | Click the newly created Course Offering record | Detail page opens; Course Master = GenCO_TC, Academic Year = 2026, Name = [2026] GenCO_TC | "" |

**Severity:** major
**Priority:** high

---

### Course Offering – Generate Courses – Academic Year and Location Selected – Both Records Created

**Description:** CRUD – Generate (Scenario) – Select both Academic Year and Location in Generate Courses; verify both a Course Offering and a Location Course are created.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master "GenBoth_TC" exists with no linked records
- Academic Year 2026 and Location "Location_H001" exist in the system

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the detail page of "GenBoth_TC" | Course Offering and Location Course related lists both show 0 items | "" |
| 2 | Click **Generate Courses** | Generate Course dialog opens | "" |
| 3 | Select "2026" in the **Academic Year** field | Field shows 2026 | "2026" |
| 4 | Select "Location_H001" in the **Location** field | Field shows Location_H001 | "Location_H001" |
| 5 | Click **Add** | Dialog closes; success feedback shown | "" |
| 6 | Click the **Course Offering** tab | Course Offering list shows 1 item: "[2026] GenBoth_TC" | "" |
| 7 | Click the **Location Course** tab | Location Course list shows 1 item: "GenBoth_TC - Location_H001" | "" |

**Severity:** major
**Priority:** high

---

### Course Offering – Generate Courses – No Academic Year Selected – Course Offering Not Created

**Description:** CRUD – Generate (Negative) – Attempt to generate courses without selecting an Academic Year; verify no Course Offering is created.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master "GenNoAY_TC" exists

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the detail page of "GenNoAY_TC" | Course Offering tab shows 0 items | "" |
| 2 | Click **Generate Courses** | Generate Course dialog opens | "" |
| 3 | Leave **Academic Year** empty | Field remains blank | "" |
| 4 | Click **Add** | System shows a validation message; dialog does not close; or Add button is disabled until at least one field is filled | "" |
| 5 | Close the dialog and check the Course Offering tab | Course Offering list still shows 0 items for "GenNoAY_TC" | "" |

**Severity:** minor
**Priority:** medium

---

### Course Offering – Generate Courses – Duplicate Academic Year for Same Course Master – Error Shown

**Description:** CRUD – Generate (Negative) – Attempt to generate a Course Offering with an Academic Year already linked to the same Course Master; verify the system prevents duplicate creation and shows an error.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master "DupAY_TC" exists with a Course Offering already created for Academic Year 2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the detail page of "DupAY_TC" | Course Offering tab shows 1 item for Academic Year 2026 | "" |
| 2 | Click **Generate Courses** | Generate Course dialog opens | "" |
| 3 | Select "2026" in the **Academic Year** field | Field shows 2026 | "2026" |
| 4 | Click **Add** | System shows an error or warning indicating a Course Offering for Academic Year 2026 already exists for this Course Master; duplicate record is NOT created | "" |
| 5 | Click the **Course Offering** tab | Course Offering list still shows exactly 1 item for Academic Year 2026 (no duplicate) | "" |

**Severity:** major
**Priority:** high

---

## Suite: Course Offering – Read

### Course Offering – List View – Name, Course Master, Academic Year, Program Master Columns Displayed

**Description:** CRUD – Read (Component) – Navigate to the Course Offering list and verify the expected columns are present and populated.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- At least one Course Offering record exists

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to **Master > Course Offering** | Course Offering list view loads | "" |
| 2 | Inspect the column headers | Columns displayed: Name, Course Master, Academic Year, Program Master, Last Modified Date | "" |
| 3 | Inspect the data in the first visible row | Each column shows a non-empty value (except Program Master which may be empty) | "" |

**Severity:** minor
**Priority:** medium

---

### Course Offering – Detail View – Name, Academic Year, Course Master Fields Are Read-Only

**Description:** CRUD – Read (Component) – Open a Course Offering detail page and verify that Name, Academic Year, and Course Master fields cannot be edited.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Offering record "[2026] ReadOnly_TC" exists

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the detail page of "[2026] ReadOnly_TC" | Detail page shows Name, Academic Year, Course Master, Course Name for Customer, Program Master in the Details section | "" |
| 2 | Click **Edit** | Edit form opens | "" |
| 3 | Inspect the **Name** field | Name field is not editable (read-only, greyed out, or no input available) | "" |
| 4 | Inspect the **Academic Year** field | Academic Year field is not editable | "" |
| 5 | Inspect the **Course Master** field | Course Master field is not editable | "" |
| 6 | Inspect the **Course Name for Customer** field | Field is editable | "" |

**Severity:** minor
**Priority:** medium

---

## Suite: Course Offering – Update

### Course Offering – Edit – Course Name for Customer – Updated Value Saved on Detail Page

**Description:** CRUD – Update (EP) – Edit the Course Name for Customer field of a Course Offering and verify the updated value is saved on the detail page.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Offering "[2026] EditCO_TC" exists with Course Name for Customer = (empty)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the detail page of "[2026] EditCO_TC" | Detail page shows Course Name for Customer = (empty) | "" |
| 2 | Click **Edit** | Edit form opens with current values | "" |
| 3 | Enter a value in **Course Name for Customer** | Field shows entered value | "English Course 2026" |
| 4 | Click **Save** | Record saved; detail page shows Course Name for Customer = "English Course 2026" | "" |

**Severity:** minor
**Priority:** medium

---

### Course Offering – Edit – Program Master – Updated Value Saved on Detail Page

**Description:** CRUD – Update (EP) – Edit the Program Master field of a Course Offering and verify the updated value is saved.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Offering "[2026] EditPM_TC" exists with Program Master = (empty)
- A Program Master record "PM_Test" exists

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the detail page of "[2026] EditPM_TC" | Detail page shows Program Master = (empty) | "" |
| 2 | Click **Edit** | Edit form opens | "" |
| 3 | Select a value in the **Program Master** field | Field shows "PM_Test" | "PM_Test" |
| 4 | Click **Save** | Record saved; detail page shows Program Master = "PM_Test" | "" |

**Severity:** minor
**Priority:** medium

---

### Course Offering – Edit – Attempt to Change Name – Field Not Editable

**Description:** CRUD – Update (Negative) – Attempt to edit the Name field of a Course Offering; verify the field is read-only and cannot be changed.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Offering "[2026] ReadOnlyName_TC" exists

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the detail page of "[2026] ReadOnlyName_TC" | Detail page shows Name = [2026] ReadOnlyName_TC | "" |
| 2 | Click **Edit** | Edit form opens | "" |
| 3 | Attempt to modify the **Name** field | Name field is not editable; input is not accepted or field is visually locked | "" |
| 4 | Click **Save** (or Cancel) | If saved, Name remains "[2026] ReadOnlyName_TC" unchanged | "" |

**Severity:** major
**Priority:** high

---

## Suite: Course Offering – Delete

### Course Offering – Delete – No Active Student Allocation – Record Removed From List

**Description:** CRUD – Delete – Delete a Course Offering with no active student allocations and verify it is removed from the list.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Offering "[2026] DeleteCO_TC" exists with 0 active student allocations

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the detail page of "[2026] DeleteCO_TC" | Detail page opens; Active Student tab shows 0 items | "" |
| 2 | Click **Delete** | A confirmation dialog appears | "" |
| 3 | Confirm the deletion | Record is deleted; page redirects to Course Offering list | "" |
| 4 | Search for "[2026] DeleteCO_TC" in the Course Offering list | Record is no longer present in the list | "[2026] DeleteCO_TC" |

**Severity:** major
**Priority:** high

---

### Course Offering – Delete – Active Student Allocation Exists – Deletion Blocked

**Description:** CRUD – Delete (Negative) – Attempt to delete a Course Offering that has active student allocations; verify deletion is blocked and an error is shown.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Offering "[2026] BlockDelete_TC" exists with at least 1 active student allocation

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the detail page of "[2026] BlockDelete_TC" | Detail page opens; Active Student tab shows at least 1 item | "" |
| 2 | Click **Delete** | A confirmation dialog appears | "" |
| 3 | Confirm the deletion | System shows an error message; record is NOT deleted | "" |
| 4 | Navigate to the Course Offering list | "[2026] BlockDelete_TC" is still present | "" |

**Severity:** major
**Priority:** high

---

## Suite: Course Offering – Import

### Course Offering – Import – Valid CSV – Records Created in List

**Description:** Import – Course Offering (Scenario) – Upload a valid CSV file via the Import button on the Course Offering list and verify the records are created.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A valid Course Offering import CSV file is prepared with at least 1 new record (unique Name + Course Master + Academic Year combination)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to **Master > Course Offering** | Course Offering list view loads | "" |
| 2 | Click **Import** | Import wizard opens (SF standard import dialog) | "" |
| 3 | Upload the valid CSV file | File is accepted; field mapping step shown | "valid_course_offering_import.csv" |
| 4 | Complete the field mapping and confirm import | Import completes; success summary shown with number of records inserted | "" |
| 5 | Search for the imported record name in the Course Offering list | Newly imported records appear in the list with correct Course Master and Academic Year | "" |

**Severity:** minor
**Priority:** medium

---

### Course Offering – Import – CSV With Duplicate Academic Year for Same Course Master – Duplicate Rows Rejected

**Description:** Import – Course Offering (Negative) – Upload a CSV that contains a Course Offering with an Academic Year already linked to the same Course Master; verify duplicates are rejected with an error and existing records are unchanged.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Offering "[2026] ImportDup_TC" already exists
- An import CSV is prepared with the same Course Master and Academic Year 2026 combination

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to **Master > Course Offering** and click **Import** | Import wizard opens | "" |
| 2 | Upload the CSV containing the duplicate row | File accepted; mapping shown | "dup_course_offering_import.csv" |
| 3 | Complete field mapping and confirm import | Import completes; summary shows the duplicate row(s) as failed/rejected with a duplicate error; other valid rows may succeed | "" |
| 4 | Search for "[2026] ImportDup_TC" in the Course Offering list | Only the original record remains; no duplicate was created | "" |

**Severity:** major
**Priority:** high

---

## Suite: Course Offering – Sync to Manabie DB

### Course Offering – Sync Data – New Course Offering Synced to sf-course-offering After Manual Sync

**Description:** Sync – Manual Sync (Scenario) – Create a new Course Offering in SF, trigger Sync Data from the Course Master list, and verify the record appears in the sf-course-offering table in Manabie DB.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A new Course Offering "[2026] SyncNew_CO" has been created and is not yet synced
- Access to Manabie DB sf-course-offering table is available for verification
- Auto-sync has not yet run since creation

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Confirm "[2026] SyncNew_CO" exists in the SF Course Offering list | Record is present in SF | "" |
| 2 | Confirm the record does NOT yet exist in the sf-course-offering table | Record absent from Manabie DB | "" |
| 3 | Navigate to the **Course Master** list in SF and click **Sync Data** | Sync is triggered; confirmation or progress indicator shown | "" |
| 4 | Wait for sync to complete | Sync completes without error | "" |
| 5 | Check the sf-course-offering table in Manabie DB | "[2026] SyncNew_CO" record is present with correct Course Master reference and Academic Year | "" |

**Severity:** critical
**Priority:** high

---

### Course Offering – Sync Data – Deleted Course Offering Removed from sf-course-offering After Manual Sync

**Description:** Sync – Manual Sync (Scenario) – Delete a Course Offering in SF, trigger Sync Data, and verify the record is removed from the sf-course-offering table.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Offering "[2026] SyncDel_CO" exists and is already synced (present in sf-course-offering table)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Confirm "[2026] SyncDel_CO" exists in both SF and sf-course-offering table | Record present in both systems | "" |
| 2 | In SF, delete "[2026] SyncDel_CO" | Record deleted from SF | "" |
| 3 | Confirm the record is still in sf-course-offering table (sync not yet triggered) | Record still present in Manabie DB | "" |
| 4 | Navigate to the **Course Master** list and click **Sync Data** | Sync triggered and completes without error | "" |
| 5 | Check the sf-course-offering table | "[2026] SyncDel_CO" is no longer present | "" |

**Severity:** critical
**Priority:** high

---

### Course Offering – Auto Sync – Course Offering Synced to sf-course-offering After Configured Interval

**Description:** Sync – Auto Sync (State Transition) – Verify a new Course Offering is automatically synced to the sf-course-offering table after the org-configured interval elapses without any manual trigger.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- Org auto-sync interval is configured (X hours per org setup)
- today = 2026-06-16; last_sync_time = known; next_sync_time = last_sync_time + X hours
- A Course Offering "[2026] AutoSync_CO" was created after the last sync ran

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Confirm "[2026] AutoSync_CO" is NOT yet in sf-course-offering table immediately after creation | Record absent from Manabie DB | "" |
| 2 | Wait until next scheduled auto-sync time without clicking Sync Data | System runs the auto-sync job at the configured time | "next_sync_time = last_sync_time + X hours" |
| 3 | After auto-sync completes, check the sf-course-offering table | "[2026] AutoSync_CO" is now present with correct fields | "" |

**Severity:** major
**Priority:** high

---
