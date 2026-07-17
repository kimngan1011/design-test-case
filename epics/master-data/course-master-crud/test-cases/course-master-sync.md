# Test Cases: Course Master – Sync to BO

## Suite: Course Master – Sync to BO

### Course Master – Sync Data – New Record Synced to BO After Manual Sync

**Description:** Sync – Manual Sync (Scenario) – Create a new Course Master in SF, trigger Sync Data, and verify the record appears in the Back Office.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master "SyncNew_TC" has been created in SF (Name = SyncNew_TC, PID = sync_new, Code = sync_new)
- Logged in to the Back Office as HQ Staff
- Auto-sync has not yet run since the record was created

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | In SF, confirm "SyncNew_TC" is visible in the Course Master list | Record exists in SF | "" |
| 2 | In BO, search for "SyncNew_TC" | Record is NOT yet visible in BO | "" |
| 3 | In SF Course Master list, click **Sync Data** | Sync is triggered; a progress indicator or confirmation message is shown | "" |
| 4 | Wait for the sync to complete | Sync completes without error | "" |
| 5 | In BO, search for "SyncNew_TC" again | "SyncNew_TC" is now visible in BO with matching Name, Course Code, and Partner Internal Id | "" |

**Severity:** critical
**Priority:** high

---

### Course Master – Sync Data – Updated Record Reflected in BO After Manual Sync

**Description:** Sync – Manual Sync (Scenario) – Update a Course Master in SF, trigger Sync Data, and verify the updated values are reflected in the Back Office.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master "SyncUpdate_TC" exists and has already been synced to BO
- Logged in to the Back Office as HQ Staff

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | In BO, confirm the current Name of the synced record | BO shows Name = SyncUpdate_TC | "" |
| 2 | In SF, edit "SyncUpdate_TC" and change the Name | Name updated to new value in SF | "SyncUpdated_TC" |
| 3 | In BO, confirm BO still shows the old name | BO still displays "SyncUpdate_TC" (not yet updated) | "" |
| 4 | In SF Course Master list, click **Sync Data** | Sync triggered and completes without error | "" |
| 5 | In BO, search for "SyncUpdated_TC" | BO now displays the updated Name = SyncUpdated_TC | "" |

**Severity:** critical
**Priority:** high

---

### Course Master – Sync Data – Deleted Record Removed from BO After Manual Sync

**Description:** Sync – Manual Sync (Scenario) – Delete a Course Master in SF, trigger Sync Data, and verify the record is removed from the Back Office.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master "SyncDelete_TC" exists and is already synced to BO
- Logged in to the Back Office as HQ Staff

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | In SF, confirm "SyncDelete_TC" is visible in both SF and BO | Record present in both systems | "" |
| 2 | In SF, delete "SyncDelete_TC" | Record is deleted from SF | "" |
| 3 | In BO, confirm "SyncDelete_TC" is still visible | Record still present in BO (sync not yet triggered) | "" |
| 4 | In SF Course Master list, click **Sync Data** | Sync triggered and completes without error | "" |
| 5 | In BO, search for "SyncDelete_TC" | Record is no longer visible in BO | "" |

**Severity:** critical
**Priority:** high

---

### Course Master – Auto Sync – New Record Synced to BO After Configured Interval Elapses

**Description:** Sync – Auto Sync (State Transition) – Verify a new Course Master created in SF is automatically synced to BO after the org-configured sync interval elapses, without any manual trigger.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- Org auto-sync interval is configured (X hours per org setup)
- today = 2026-06-16; last_sync_time = known (e.g., 10:00 JST); next_sync_time = last_sync_time + X hours
- A Course Master "AutoSync_TC" has been created in SF after the last sync ran
- Logged in to the Back Office as HQ Staff

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Confirm "AutoSync_TC" is NOT visible in BO immediately after creation | Record is absent from BO | "" |
| 2 | Wait until the next scheduled auto-sync time (last_sync_time + X hours) without clicking Sync Data | System runs the auto-sync job automatically at the configured time | "next_sync_time = last_sync_time + X hours" |
| 3 | After auto-sync completes, search for "AutoSync_TC" in BO | "AutoSync_TC" is now visible in BO with correct Name, Course Code, and Partner Internal Id | "" |

**Severity:** major
**Priority:** high

---

### Course Master – Sync Data – Button Visible on Course Master List View

**Description:** Sync – Component – Verify the "Sync Data" button is present and accessible on the Course Master list view action bar.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to **Master > Course Master** | Course Master list view loads | "" |
| 2 | Inspect the action bar at the top right of the list | **Sync Data** button is visible alongside New, Import, and Assign Label | "" |

**Severity:** minor
**Priority:** medium

---

### Course Master – Sync Data – Name Field Update Reflected in BO

**Description:** Sync – Field Sync (Scenario) – Update the Name field of an existing Course Master in SF, trigger Sync Data, and verify the updated Name is reflected in the Back Office.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master SyncField_TC exists and has already been synced to BO
- Logged in to the Back Office as HQ Staff

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | In BO, confirm the current Name of the synced record | BO shows Name = SyncField_TC | "" |
| 2 | In SF, edit SyncField_TC and change the **Name** field | SF detail page shows updated Name = SyncName_Updated | "SyncName_Updated" |
| 3 | In SF Course Master list, click **Sync Data** and wait for completion | Sync completes without error | "" |
| 4 | In BO, search for SyncName_Updated | BO shows Name = SyncName_Updated (updated value reflected) | "" |

**Severity:** critical
**Priority:** high

---

### Course Master – Sync Data – Teaching Method Update Reflected in BO

**Description:** Sync – Field Sync (Scenario) – Update the Teaching Method of an existing Course Master in SF, trigger Sync Data, and verify the updated Teaching Method is reflected in the Back Office.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master SyncTM_TC exists with Teaching Method = 個別 and has already been synced to BO
- Logged in to the Back Office as HQ Staff

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | In BO, confirm the Teaching Method of the synced record | BO shows Teaching Method = 個別 | "" |
| 2 | In SF, edit SyncTM_TC and change **Teaching Method** | SF detail page shows updated Teaching Method = グループ | "グループ" |
| 3 | In SF Course Master list, click **Sync Data** and wait for completion | Sync completes without error | "" |
| 4 | In BO, open the detail page of SyncTM_TC | BO shows Teaching Method = グループ (updated value reflected) | "" |

**Severity:** critical
**Priority:** high

---

### Course Master – Sync Data – Partner Internal Id Update Reflected in BO

**Description:** Sync – Field Sync (Scenario) – Update the Partner Internal Id of an existing Course Master in SF, trigger Sync Data, and verify the updated Partner Internal Id is reflected in the Back Office.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master SyncPID_TC exists with Partner Internal Id = pid_sync_old and has already been synced to BO
- Logged in to the Back Office as HQ Staff

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | In BO, confirm the Partner Internal Id of the synced record | BO shows Partner Internal Id = pid_sync_old | "" |
| 2 | In SF, edit SyncPID_TC and update **Partner Internal Id** to a new unique value | SF detail page shows updated Partner Internal Id = pid_sync_new | "pid_sync_new" |
| 3 | In SF Course Master list, click **Sync Data** and wait for completion | Sync completes without error | "" |
| 4 | In BO, open the detail page of SyncPID_TC | BO shows Partner Internal Id = pid_sync_new (updated value reflected) | "" |

**Severity:** critical
**Priority:** high

---

### Course Master – Sync Data – Sequence Number Update Reflected in BO

**Description:** Sync – Field Sync (Scenario) – Update the Sequence Number of an existing Course Master in SF, trigger Sync Data, and verify the updated Sequence Number is reflected in the Back Office.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master SyncSeq_TC exists with Sequence Number = 5 and has already been synced to BO
- Logged in to the Back Office as HQ Staff

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | In BO, confirm the Sequence Number of the synced record | BO shows Sequence Number = 5 | "" |
| 2 | In SF, edit SyncSeq_TC and change **Sequence Number** | SF detail page shows updated Sequence Number = 99 | "99" |
| 3 | In SF Course Master list, click **Sync Data** and wait for completion | Sync completes without error | "" |
| 4 | In BO, open the detail page of SyncSeq_TC | BO shows Sequence Number = 99 (updated value reflected) | "" |

**Severity:** major
**Priority:** high

---

### Course Master – Sync Data – Course Code Update Reflected in BO

**Description:** Sync – Field Sync (Scenario) – Update the Course Code of an existing Course Master in SF, trigger Sync Data, and verify the updated Course Code is reflected in the Back Office.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org
- A Course Master SyncCode_TC exists with Course Code = code_sync_old and has already been synced to BO
- Logged in to the Back Office as HQ Staff

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | In BO, confirm the Course Code of the synced record | BO shows Course Code = code_sync_old | "" |
| 2 | In SF, edit SyncCode_TC and change **Course Code** | SF detail page shows updated Course Code = code_sync_new | "code_sync_new" |
| 3 | In SF Course Master list, click **Sync Data** and wait for completion | Sync completes without error | "" |
| 4 | In BO, open the detail page of SyncCode_TC | BO shows Course Code = code_sync_new (updated value reflected) | "" |

**Severity:** critical
**Priority:** high

---
