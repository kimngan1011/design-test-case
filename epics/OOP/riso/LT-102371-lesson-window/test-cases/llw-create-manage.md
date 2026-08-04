# Test Cases: LT-102371 — [Riso] OOP | Lesson Window

## Suite: [Riso] LLW – Create & Manage

---

### [Riso] Location Lesson Window – Account Page – Lesson Window Tab – All required columns displayed

**Description:** AC-01.1 — Component — The Lesson Window tab on the Account detail page displays all six required columns for each LLW record.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- At least one `Location_Lesson_Window__c` record exists for this Account (Status = Open, AY = 2026, Start Date = 2026-07-01, End Date = 2026-07-31)
- Navigate to the Account detail page for that location

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Account detail page and click the **Lesson Window** tab | The tab is visible and loads the list of LLW records | Account = Location A |
| 2 | Observe the column headers in the list | Six columns are shown: **Academic Year**, **Start Date**, **End Date**, **Status**, **Last Modified Date**, **Last Modified By** | — |
| 3 | Observe the row values for the existing LLW record | Academic Year = 2026, Start Date = 2026-07-01, End Date = 2026-07-31, Status = Open, Last Modified Date = today, Last Modified By = current user | — |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – Account Page – New Button – Creation form opens with correct auto-filled fields

**Description:** AC-01.1 — Component — Clicking New on the Lesson Window tab opens a form with Academic Year, Status, and Location pre-filled; Month defaults to current month.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Navigate to the Account detail page for Location A
- Click the **Lesson Window** tab

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Click the **New** button on the Lesson Window tab | The LLW creation form opens | today = 2026-07-14 |
| 2 | Observe the **Academic Year** field | Academic Year is auto-filled with the current academic year (2026) | expected_AY = 2026 |
| 3 | Observe the **Status** field | Status defaults to **Open** | — |
| 4 | Observe the **Location** field | Location is pre-filled with **Location A** and is non-editable | — |
| 5 | Observe the **Month** dropdown | Month defaults to the current month (July) | expected_month = July |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – Account Page – Month Selection – Start Date and End Date auto-populated from Academic Year

**Description:** AC-01.1, BR-11a — Decision Table — Selecting a Month in the creation form auto-populates Start Date (first day) and End Date (last day) from the Academic Year calendar range.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- LLW creation form is open (Account = Location A, AY = 2026 auto-filled)
- Academic Year 2026 spans April 2026 – March 2027

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the LLW creation form (New button on the Lesson Window tab) | The creation form opens with AY = 2026 auto-filled | today = 2026-07-15; AY = 2026 (Apr 2026–Mar 2027) |
| 2 | Observe the Month dropdown without changing it | Month dropdown defaults to the current month: **July** | expected_default_month = July (= current calendar month) |
| 3 | Observe the Start Date field (auto-populated from default month) | Start Date is auto-populated as **2026-07-01** (first day of July in AY 2026) | expected_start = 2026-07-01 |
| 4 | Observe the End Date field (auto-populated from default month) | End Date is auto-populated as **2026-07-31** (last day of July) | expected_end = 2026-07-31 |
| 5 | Change the Month dropdown to **January** | Month field updates to January | — |
| 6 | Observe the Start Date field after changing month | Start Date updates to **2027-01-01** (first day of January in AY 2026) | expected_start = 2027-01-01 |
| 7 | Observe the End Date field after changing month | End Date updates to **2027-01-31** (last day of January) | expected_end = 2027-01-31 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – Account Page – Academic Year Cleared – Month and Date fields disabled

**Description:** AC-01.1, BR-11a — Decision Table — Clearing the Academic Year field disables the Month dropdown, Start Date, and End Date fields.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- LLW creation form is open with Academic Year = 2026 auto-filled

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Clear the **Academic Year** field | Academic Year field is empty | — |
| 2 | Observe the **Month** dropdown | Month dropdown is **disabled** (grayed out, not clickable) | — |
| 3 | Observe the **Start Date** field | Start Date field is **disabled** | — |
| 4 | Observe the **End Date** field | End Date field is **disabled** | — |
| 5 | Re-select Academic Year = **2026** | Month, Start Date, End Date fields become enabled again | — |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – Account Page – Manual Date Override – Custom dates retained after auto-population

**Description:** AC-01.1, BR-11a — Negative — After a Month selection auto-populates Start Date and End Date, a user can manually override the dates and the custom values are saved.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- LLW creation form is open; Month = July selected; Start Date = 2026-07-01, End Date = 2026-07-31 auto-populated

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Clear the **Start Date** field and enter **2026-07-10** | Start Date shows 2026-07-10 | manual_start = 2026-07-10 |
| 2 | Clear the **End Date** field and enter **2026-07-20** | End Date shows 2026-07-20 | manual_end = 2026-07-20 |
| 3 | Click **Save** | Record is saved | — |
| 4 | Open the saved LLW record | Start Date = **2026-07-10**, End Date = **2026-07-20** (custom values retained) | — |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – Complete Action – Any Authorized User – Status changes to Complete

**Description:** AC-04, BR-07 — State Transition — Any authorized user (HQ or CM) can mark an Open LLW as Complete at any time without additional validation.

**Preconditions:**
- Logged in as CM Staff to the Riso Salesforce org
- An LLW record exists: Location = Location A, AY = 2026, Start Date = 2026-07-01, End Date = 2026-07-31, Status = **Open**
- Navigate to the Account detail page for Location A → Lesson Window tab

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Click the **Complete** action on the LLW row (Status = Open) | Confirmation prompt or inline action is available | LLW: Start = 2026-07-01, End = 2026-07-31 |
| 2 | Confirm the Complete action | The action succeeds | — |
| 3 | Observe the **Status** field on the LLW record | Status is now **Complete** | — |
| 4 | Verify that no date or content validation was required to complete | No error messages were shown; action completed immediately | — |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – Delete Button – Visible only on Open status records for staff with either delete Permission Set

**Description:** AC-05, BR-09 — Permission Matrix — The Delete button is visible only when the LLW Status = Open and the staff user has **at least one** of `full_access_v2` or `llw_full_access` Permission Sets.

**Preconditions:**
- Staff A has **`full_access_v2` only**; Staff B has **`llw_full_access` only** in the Riso Salesforce org
- Two LLW records exist for Location A: one with Status = **Open**, one with Status = **Complete**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Log in as Staff A, navigate to Account detail page for Location A → Lesson Window tab | Both LLW records are visible | user = Staff A; PS = full_access_v2 only |
| 2 | Observe the record row where Status = **Open** | **Delete button is visible** on this row | — |
| 3 | Repeat steps 1–2 as Staff B | **Delete button is visible** on the Open record | user = Staff B; PS = llw_full_access only |
| 4 | As either staff user, observe the record row where Status = **Complete** | Delete button is **not visible** on this row | — |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – Delete Button – Not shown when staff has neither delete Permission Set

**Description:** AC-05, BR-CRUD — Permission Matrix (negative) — A staff user who has neither `full_access_v2` nor `llw_full_access` does not see the Delete button on an Open LLW record.

**Preconditions:**
- Logged in as staff **without `full_access_v2` and without `llw_full_access`** in the Riso Salesforce org
- One LLW record exists for Location A: Status = **Open**
- Navigate to Account detail page for Location A → Lesson Window tab

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Observe the LLW record row where Status = Open | **No Delete button is shown** | — |
| 2 | Attempt to delete via any available UI action | No delete action is available | — |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – Delete – Open Status, No Linked Records – Deletion succeeds with llw_full_access PS only

**Description:** AC-05, BR-09 — CRUD — A staff user with `llw_full_access` but without `full_access_v2` can delete an LLW record when Status = Open and no linked detail records exist.

**Preconditions:**
- Logged in as staff with `llw_full_access` but **without `full_access_v2`** in the Riso Salesforce org
- LLW record exists: Location A, AY = 2026, Start Date = 2026-06-01, End Date = 2026-06-30, Status = **Open**, no linked child records

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the LLW record (Status = Open) and click **Delete** | Delete confirmation dialog appears | — |
| 2 | Confirm deletion | Record is deleted | — |
| 3 | Return to the Lesson Window tab for Location A | The deleted LLW record no longer appears in the list | — |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – Delete – Open Status, No Linked Records – Deletion succeeds with full_access_v2 PS only

**Description:** AC-05, BR-09 — CRUD — A staff user with `full_access_v2` but without `llw_full_access` can delete an LLW record when Status = Open and no linked detail records exist.

**Preconditions:**
- Logged in as a staff user with `full_access_v2` but **without `llw_full_access`** in the Riso Salesforce org
- LLW record exists: Location A, AY = 2026, Start Date = 2026-06-01, End Date = 2026-06-30, Status = **Open**, no linked child records

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the LLW record (Status = Open) and click **Delete** | Delete confirmation dialog appears | — |
| 2 | Confirm deletion | Record is deleted | — |
| 3 | Return to the Lesson Window tab for Location A | The deleted LLW record no longer appears in the list | — |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – Delete – Complete Status – Delete action unavailable

**Description:** AC-05, BR-09 — State Transition (negative) — A Complete LLW record cannot be deleted; the Delete action is absent.

**Preconditions:**
- Logged in as staff with `full_access_v2` to the Riso Salesforce org
- LLW record exists: Status = **Complete**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Lesson Window tab and locate the record with Status = Complete | Record is visible | — |
| 2 | Observe available actions on the Complete record | **Delete button is not present** | — |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – List View – Multi-location Creation – All locations created when no overlaps exist

**Description:** AC-01.2 — CRUD — Creating a new LLW from the List View with multiple locations selected and no overlapping LLWs creates records for all selected locations.

**Preconditions:**
- Logged in as HQ Staff to the Riso Salesforce org
- Navigate to the Location Lesson Window list view
- No existing LLW records for Location B, Location C, Location D for AY = 2026, July

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Click **New** in the LLW list view | Creation form opens with multi-select Location field | — |
| 2 | Select **Location B**, **Location C**, **Location D** from the Location multi-select | Three locations selected | AY = 2026; Month = July; Start = 2026-07-01; End = 2026-07-31 |
| 3 | Set AY = 2026, Month = July (Start Date = 2026-07-01, End Date = 2026-07-31) | Fields populated | — |
| 4 | Click **Save** | Save succeeds | — |
| 5 | Return to the LLW list view and filter by AY = 2026, Start Date = 2026-07-01 | **Three new LLW records appear** — one for each of Location B, C, D | — |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – List View – Multi-location Creation – Overlapping location skipped, others created

**Description:** AC-01.2, BR-01 — Data Integrity (negative) — When creating LLWs for multiple locations and one location has an overlapping record, that location is skipped silently; other locations are created.

**Preconditions:**
- Logged in as HQ Staff to the Riso Salesforce org
- Location E already has a Complete LLW: AY = 2026, Start Date = 2026-07-01, End Date = 2026-07-31 (overlap)
- Location F and Location G have no LLW for AY = 2026, July

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open LLW list view → click **New** | Creation form opens | — |
| 2 | Select **Location E**, **Location F**, **Location G** | Three locations selected | AY = 2026; Month = July; Start = 2026-07-01; End = 2026-07-31 |
| 3 | Click **Save** | Save proceeds | — |
| 4 | Check LLW records for Location E | No new record created for Location E (overlap skipped) | — |
| 5 | Check LLW records for Location F and Location G | New LLW records created for **Location F** and **Location G** | — |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – List View – Location Column – Renders as clickable link

**Description:** AC-01.2 — Component — The Location column in the LLW List View renders each location as a clickable hyperlink that navigates to the Account detail page.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- At least one LLW record exists; navigate to the LLW list view

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Observe the **Location** column in the LLW list view | Each location name appears as a **clickable hyperlink** | — |
| 2 | Click the location name for an existing LLW record | Browser navigates to the **Account detail page** for that location | — |
| 3 | Confirm the Account detail page shows the Lesson Window tab | The Lesson Window tab is accessible from this navigation | — |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – List View – Complete and Reopen Actions – Not available in List View

**Description:** AC-01.2 — Component (negative) — The Complete and Reopen actions are not available in the LLW List View (Salesforce standard limitation).

**Preconditions:**
- Logged in as HQ Staff to the Riso Salesforce org
- LLW list view is open; records with Status = Open and Status = Complete are present

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Observe the row actions available for an Open LLW record in the list view | **No Complete action** is present in the list view row actions | — |
| 2 | Observe the row actions for a Complete LLW record in the list view | **No Reopen action** is present in the list view row actions | — |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – Uniqueness – Overlapping Date Range, Same Location and Academic Year – Creation blocked

**Description:** AC-02, BR-01 — Equivalence Partitioning (negative) — Creating a new LLW with an overlapping date range for the same Location and Academic Year is blocked with an English error message.

**Preconditions:**
- Logged in as HQ Staff to the Riso Salesforce org
- Existing LLW: Location A, AY = 2026, Start Date = **2026-07-01**, End Date = **2026-07-31**, Status = Open
- Navigate to Location A Account page → Lesson Window tab → New

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | In the creation form, set AY = 2026, Start Date = **2026-07-15**, End Date = **2026-08-15** (overlaps existing July record) | Fields are filled | overlap_start = 2026-07-15; overlap_end = 2026-08-15 |
| 2 | Click **Save** | Save is **blocked** | — |
| 3 | Observe the error message | Error message reads: **"A Lesson Window already exists for this location and period."** | — |
| 4 | Confirm no new LLW record was created | The LLW list still shows only the original record | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Location Lesson Window – Uniqueness – Non-overlapping Date Range, Same Location and Academic Year – Creation allowed

**Description:** AC-02, BR-01 — Equivalence Partitioning — Creating a new LLW with a non-overlapping date range for the same Location and Academic Year succeeds.

**Preconditions:**
- Logged in as HQ Staff to the Riso Salesforce org
- Existing LLW: Location A, AY = 2026, Start Date = 2026-07-01, End Date = 2026-07-31
- Navigate to Location A Account page → Lesson Window tab → New

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set AY = 2026, Start Date = **2026-08-01**, End Date = **2026-08-31** (August — no overlap) | Fields filled | new_start = 2026-08-01; new_end = 2026-08-31 |
| 2 | Click **Save** | Save **succeeds** with no error | — |
| 3 | Observe the Lesson Window tab | Two LLW records now appear: July and August | — |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – Uniqueness – Same Date Range, Different Academic Year – Creation allowed

**Description:** AC-02, BR-10 — Equivalence Partitioning — Two LLW records with identical date ranges but different Academic Years for the same location do not conflict.

**Preconditions:**
- Logged in as HQ Staff to the Riso Salesforce org
- Existing LLW: Location A, AY = **2025**, Start Date = 2026-01-01, End Date = 2026-01-31
- Navigate to Location A → Lesson Window tab → New

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set AY = **2026**, Start Date = 2026-01-01, End Date = 2026-01-31 (same date range, different AY) | Fields filled | AY = 2026; start = 2026-01-01; end = 2026-01-31 |
| 2 | Click **Save** | Save **succeeds** (different AY scope — no conflict) | — |
| 3 | Observe the Lesson Window tab | Both records appear: one under AY 2025, one under AY 2026 | — |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – LBAC Object – BO Teacher – No access to LLW object

**Description:** BR-CRUD — Permission Matrix — A BO Teacher cannot see, access, or interact with the Location Lesson Window object in any way.

**Preconditions:**
- Logged in as **BO Teacher** user to the Riso Salesforce org
- At least one LLW record exists in the org

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Account detail page for any location | The **Lesson Window tab is not visible** | — |
| 2 | Attempt to access the LLW object via navigation/search | No results found; BO Teacher has no object-level access | — |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – LBAC Record – CM at Own Location – Can only view own location's LLW records

**Description:** AC-03, BR-05 — Permission Matrix — A CM can view and manage LLW records only for the location(s) they are assigned to.

**Preconditions:**
- Logged in as **CM Staff** assigned to **Location A** only
- LLW records exist for both Location A and Location B

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Account detail page for **Location A** → Lesson Window tab | LLW records for Location A are **visible** | — |
| 2 | Navigate to the Account detail page for **Location B** → Lesson Window tab | **No LLW records visible** (CM not assigned to Location B) | — |
| 3 | Navigate to the LLW list view | Only records for **Location A** appear; Location B records are not shown | — |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – LBAC Record – CM at Location A – Cannot access Location B's LLW records

**Description:** AC-03, BR-05 — Permission Matrix (negative) — A CM assigned to Location A is blocked from accessing or creating LLW records for Location B.

**Preconditions:**
- Logged in as **CM Staff** assigned to **Location A** only
- Navigate to the LLW list view → New

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | In the creation form, attempt to set Location = **Location B** (not assigned to this CM) | Location B is **not available** in the CM's Location selection — field only shows Location A | — |
| 2 | Confirm the CM cannot save an LLW for Location B | Save attempt for Location B is blocked by LBAC | — |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – LBAC Record – HQ Staff – Views all LLW records across all locations

**Description:** AC-03, BR-05 — Permission Matrix — HQ Staff can view and manage LLW records for all locations without restriction.

**Preconditions:**
- Logged in as **HQ Staff** to the Riso Salesforce org
- LLW records exist for Location A, Location B, Location C

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the LLW list view | LLW records for **all locations** (A, B, C) are visible | — |
| 2 | Open the Account detail page for Location B → Lesson Window tab | Location B's LLW records are visible and manageable | — |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – Edit – Open Status – Editable fields are accessible

**Description:** AC-20, BR-11b — State Transition — When an LLW's Status is Open, the Start Date, End Date, Month, and Status fields are editable.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- LLW record exists: Location A, AY = 2026, Start Date = 2026-08-01, End Date = 2026-08-31, Status = **Open**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the LLW record (Status = Open) and click **Edit** | The edit form opens | — |
| 2 | Observe the **Start Date** field | Start Date is **editable** | — |
| 3 | Observe the **End Date** field | End Date is **editable** | — |
| 4 | Observe the **Month** field | Month is **editable** | — |
| 5 | Change Start Date to **2026-08-05** and click **Save** | Record saves with Start Date = 2026-08-05 | new_start = 2026-08-05 |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – Edit – Complete Status – All fields are read-only

**Description:** AC-20, BR-11b — State Transition (negative) — When an LLW's Status is Complete, all fields are read-only and cannot be edited.

**Preconditions:**
- Logged in as HQ Staff to the Riso Salesforce org
- LLW record exists: Status = **Complete**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the LLW record with Status = Complete | Record detail page is shown | — |
| 2 | Attempt to click **Edit** or use inline edit on any field | **Edit is not available** or fields are shown as read-only | — |
| 3 | Confirm no changes can be made to Start Date, End Date, Month, or Status (except via Reopen) | All fields are locked | — |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – Edit – Academic Year – Always read-only on edit

**Description:** AC-20, BR-11b — Negative — The Academic Year field is read-only on edit even when the LLW Status is Open.

**Preconditions:**
- Logged in as HQ Staff to the Riso Salesforce org
- LLW record exists: Status = **Open**, AY = 2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the LLW record (Status = Open) and click **Edit** | Edit form opens | — |
| 2 | Observe the **Academic Year** field | Academic Year field is **read-only** (cannot be changed) | — |
| 3 | Confirm the help text or field behavior communicates this restriction | Field is grayed out or locked | — |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – Edit – Overlap Validation Fires on Save

**Description:** AC-20, BR-01 — Data Integrity — Saving an edit to an LLW that would create an overlapping date range with another LLW (same Location + AY) is blocked.

**Preconditions:**
- Logged in as HQ Staff to the Riso Salesforce org
- Two LLW records for Location A, AY = 2026: July (2026-07-01–2026-07-31) and August (2026-08-01–2026-08-31), both Status = Open
- Open the August LLW for editing

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | In the edit form, change Start Date to **2026-07-15** (which overlaps the existing July LLW) | Field updated | overlap_start = 2026-07-15 |
| 2 | Click **Save** | Save is **blocked** | — |
| 3 | Observe the error message | Error: **"A Lesson Window already exists for this location and period."** | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Location Lesson Window – Edit Dates Then Complete – New Date Scope Blocks Lessons in Updated Range

**Description:** AC-21 — State Transition — After editing an LLW's date range and marking it Complete, lesson creation is blocked for the new (updated) date range, not the original.

**Preconditions:**
- Logged in as HQ Staff to the Riso Salesforce org
- LLW record: Location A, AY = 2026, Start Date = 2026-07-01, End Date = 2026-07-31, Status = **Open**
- No lessons exist on 2026-07-20 for Location A

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Edit the LLW: change Start Date to **2026-07-15**, End Date to **2026-07-25**, then mark Status = **Complete** | Save succeeds | new_start = 2026-07-15; new_end = 2026-07-25 |
| 2 | Attempt to create a lesson on **2026-07-20** for Location A (within new range) | Lesson creation is **blocked**: "Selected lesson date is already closed." | lesson_date = 2026-07-20 |
| 3 | Attempt to create a lesson on **2026-07-05** for Location A (outside new range — original range but now open) | Lesson creation **succeeds** | lesson_date = 2026-07-05 |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – Audit Trail – Created Date and Created By – Auto-populated on record creation

**Description:** BR-04, NFR-01 — Component — The Created Date and Created By fields are automatically populated when an LLW record is created; they cannot be edited.

**Preconditions:**
- Logged in as HQ Staff (user: "Test HQ User") to the Riso Salesforce org
- Note the current date and time before creating the record

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Create a new LLW record: Location A, AY = 2026, Month = September | Fill in fields | today = 2026-07-14; actor = Test HQ User |
| 2 | Save the record | Record is saved | — |
| 3 | Open the saved record and observe the **Created Date** field | Created Date is auto-populated with today's date and time | expected_date = 2026-07-14 |
| 4 | Observe the **Created By** (or Last Modified By) field | Field shows **Test HQ User** (the logged-in user) | — |
| 5 | Attempt to edit the Created Date or Created By field | Fields are **read-only** and cannot be edited | — |

**Severity:** trivial
**Priority:** low

---

### [Riso] Location Lesson Window – NFR-03 – Uniqueness at Trigger Level – Concurrent creation of duplicate LLW blocked

**Description:** BR-01, NFR-03 — Data Integrity — Uniqueness is enforced at the Salesforce Apex trigger level, not only in the UI. Concurrent or API-level insertion of a duplicate LLW is blocked.

**Preconditions:**
- An LLW record exists: Location A, AY = 2026, Start Date = 2026-07-01, End Date = 2026-07-31
- Tester has access to the Salesforce API or developer console

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Via the Salesforce API (or developer console), attempt to insert a new `Location_Lesson_Window__c` record with Location = A, AY = 2026, Start Date = 2026-07-10, End Date = 2026-07-31 (overlapping) | API insert attempt initiated | overlap_start = 2026-07-10; overlap_end = 2026-07-31 |
| 2 | Observe the API response | The insert is **rejected** with a validation error from the Apex trigger: "A Lesson Window already exists for this location and period." | — |
| 3 | Confirm no duplicate record was created in the database | Only the original July LLW exists for Location A | — |

**Severity:** critical
**Priority:** high


---

### [Riso] Location Lesson Window – Cross-staff Access – CM Staff A Can View LLW Created by CM Staff B at Same Location

**Description:** AC-03, BR-05 — Permission Matrix — Any authorized CM at a location can view LLW records created by other staff at the same location. Records are shared by location, not locked to their creator.

**Preconditions:**
- **CM Staff B** creates a new LLW: Location A, AY = 2026, Month = July, Status = Open
- **CM Staff A** is a different user also assigned to Location A (not the creator)
- Log in as **CM Staff A**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Account detail page for Location A → Lesson Window tab | Lesson Window tab is visible | actor = CM Staff A (not the LLW creator) |
| 2 | Observe the July LLW record created by CM Staff B | LLW record is **visible** to CM Staff A — shared by location, not by creator | llw_creator = CM Staff B; viewer = CM Staff A; same location = Location A |
| 3 | Open the LLW record detail | Record opens without "Access Denied" | — |
| 4 | Observe the **Last Modified By** field | Shows CM Staff B (the original creator) | — |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – Cross-staff Access – CM Staff A Can Edit Open LLW Created by CM Staff B at Same Location

**Description:** AC-20, BR-05 — Permission Matrix — A CM can edit an Open LLW created by a different CM, provided they share the same location.

**Preconditions:**
- LLW exists: Location A, AY = 2026, Start Date = 2026-08-01, End Date = 2026-08-31, Status = **Open**, created by CM Staff B
- Logged in as **CM Staff A** (different user, also assigned to Location A)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the LLW record (created by CM Staff B) and click **Edit** | Edit form opens without access error | creator = CM Staff B; editor = CM Staff A; same location = Location A |
| 2 | Change the **End Date** to **2026-08-25** | End Date field updated | new_end = 2026-08-25 |
| 3 | Click **Save** | Save **succeeds** — edit rights are not locked to the creator | — |
| 4 | Observe **Last Modified By** | Shows **CM Staff A** (updated to the user who made the edit) | — |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – Cross-staff Access – CM Staff A Can Mark Complete on LLW Created by CM Staff B at Same Location

**Description:** AC-04, BR-05 — Permission Matrix — Any authorized CM at a location can mark Complete on an Open LLW created by a different staff member at the same location.

**Preconditions:**
- LLW exists: Location A, AY = 2026, Start Date = 2026-07-01, End Date = 2026-07-31, Status = **Open**, created by CM Staff B
- Logged in as **CM Staff A** (different user, also assigned to Location A)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the July LLW record (created by CM Staff B) | Record is visible | creator = CM Staff B; actor = CM Staff A; same location = Location A |
| 2 | Click the **Complete** action | Action is available | — |
| 3 | Confirm the Complete action | Status changes to **Complete** | — |
| 4 | Observe **Last Modified By** | Shows **CM Staff A** (the user who completed it, not the creator) | — |

**Severity:** major
**Priority:** high
