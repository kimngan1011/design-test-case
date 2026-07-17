# Test Cases: LT-98531 — [Riso] Monthly Lesson Assignment Report – Access & Filters

## Suite: Report Access – Permission Gate

### [Riso] Monthly Lesson Assignment Report – Riso HQ or CM Staff – Report Page Accessible as Standalone

**Description:** AC-06 — Permission Matrix — The Monthly Lesson Assignment report page is accessible as a standalone page to an authorized Riso HQ or CM Staff user.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- The Monthly Lesson Assignment report page URL is known
- today = 2026-06-22

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate directly to the Monthly Lesson Assignment report page (standalone URL) | The report page loads without an error or permission denial | today = 2026-06-22; Riso HQ or CM Staff user |
| 2 | Observe the page content | The report page is fully rendered, showing the filter panel and report area | "" |

**Severity:** major
**Priority:** high

---

### [Riso] Monthly Lesson Assignment Report – Non-Riso Partner – Report Page Not Accessible

**Description:** AC-06 — Negative — A user from a non-Riso partner org cannot access the Monthly Lesson Assignment report page; access is denied or the page is not reachable.

**Preconditions:**
- Logged in as HQ or CM Staff to a **non-Riso** partner Salesforce org
- today = 2026-06-22

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Attempt to navigate to the Monthly Lesson Assignment report page (using the same URL as the Riso standalone report) | The page does not load; user receives an access-denied message, is redirected, or the route is not found | today = 2026-06-22; non-Riso partner user |
| 2 | Observe whether the report content or any data is exposed | No report content or student data is visible to the non-Riso user | "" |

**Severity:** major
**Priority:** high

---

## Suite: Report Filters – Defaults and Behavior

### [Riso] Monthly Lesson Assignment Report – AY Filter – Defaults to Current AY on First Open

**Description:** AC-07 — Decision Table — When the report is opened for the first time in a session, the AY filter defaults to the current Academic Year without any user action.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- The report has not been opened in the current browser session (no cached filter state)
- today = 2026-06-22; current_AY = 2025-2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page | Report page loads | today = 2026-06-22; current_AY = 2025-2026 |
| 2 | Observe the AY filter field without making any selection | The AY filter displays **2025-2026** as the selected value | Expected default: AY = 2025-2026 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Monthly Lesson Assignment Report – Location Filter – Defaults to User's Assigned Location on First Open

**Description:** AC-07 — Decision Table — When the report is opened, the Location filter defaults to the user's assigned location without any user action.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org whose assigned location is "Tokyo Branch"
- The report has not been opened in the current browser session
- today = 2026-06-22; user_location = Tokyo Branch

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page | Report page loads | today = 2026-06-22; user_location = Tokyo Branch |
| 2 | Observe the Location filter field without making any selection | The Location filter displays **Tokyo Branch** as the pre-selected value | Expected default: Location = user's assigned location (Tokyo Branch) |

**Severity:** minor
**Priority:** medium

---

### [Riso] Monthly Lesson Assignment Report – Student or Contact ID Filter – Multi-Select Supported

**Description:** AC-07 — Equivalence Partitioning — The Student or Contact ID filter accepts multiple student selections simultaneously.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- At least three student contacts exist in the system
- today = 2026-06-22; current_AY = 2025-2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page | Report page loads | today = 2026-06-22 |
| 2 | Click the **Student or Contact ID** filter field | A dropdown or search input appears allowing multiple selections | "" |
| 3 | Select Student A from the filter | Student A is added to the filter; field shows Student A as selected | Student A = Contact ID: STU-001 |
| 4 | Select Student B from the same filter without deselecting Student A | Both Student A and Student B are shown as selected in the filter | Student B = Contact ID: STU-002 |
| 5 | Select Student C from the same filter | All three students (A, B, C) are shown as selected simultaneously | Student C = Contact ID: STU-003 |
| 6 | Apply or observe the report data | Report shows rows for all three selected students | "" |

**Severity:** minor
**Priority:** medium

---

### [Riso] Monthly Lesson Assignment Report – Location Filter – Multi-Select Supported

**Description:** AC-07 — Equivalence Partitioning — The Location filter accepts multiple location selections simultaneously.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- At least two locations exist (e.g., Tokyo Branch and Osaka Branch)
- today = 2026-06-22; current_AY = 2025-2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page | Report page loads | today = 2026-06-22 |
| 2 | Click the **Location** filter field | A dropdown appears allowing multiple selections | "" |
| 3 | Select **Tokyo Branch** from the Location filter | Tokyo Branch is added to the filter selection | Location 1: Tokyo Branch |
| 4 | Select **Osaka Branch** from the same Location filter without deselecting Tokyo Branch | Both Tokyo Branch and Osaka Branch are shown as selected in the filter | Location 2: Osaka Branch |
| 5 | Apply or observe the report data | Report shows rows for students from both Tokyo Branch and Osaka Branch | "" |

**Severity:** minor
**Priority:** medium

---

### [Riso] Monthly Lesson Assignment Report – AY Filter Changed – Report Data Scope Updates

**Description:** AC-07 — Decision Table — Changing the AY filter from the current AY to a previous AY causes the report rows to update to reflect the selected AY's data.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Contracts and sessions exist in both AY 2025-2026 and AY 2024-2025
- today = 2026-06-22; current_AY = 2025-2026; previous_AY = 2024-2025

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page | Report loads with AY defaulting to 2025-2026 | today = 2026-06-22; current_AY = 2025-2026 |
| 2 | Note the number of rows shown for AY 2025-2026 | A set of rows is displayed corresponding to AY 2025-2026 data | "" |
| 3 | Change the AY filter to **2024-2025** and apply (or observe auto-apply) | Report rows update to show data for AY 2024-2025; rows for AY 2025-2026 are no longer shown | AY selection: 2024-2025 |
| 4 | Confirm the displayed rows correspond to AY 2024-2025 contracts and sessions | All visible rows have contract data within AY 2024-2025 | "" |

**Severity:** minor
**Priority:** medium

---

### [Riso] Monthly Lesson Assignment Report – Student Filter Cleared – Empty Filter Behavior

**Description:** AC-07 — Negative — When all students are removed from the Student or Contact ID multi-select filter, the report behaves gracefully (either shows all students or shows an empty state).

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- The report is open with one or more students selected in the filter
- today = 2026-06-22; current_AY = 2025-2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page with students pre-selected | Report page loads showing rows for the selected students | today = 2026-06-22; Students pre-selected: STU-001, STU-002 |
| 2 | Remove all selected students from the Student or Contact ID filter | All student selections are cleared from the filter | "" |
| 3 | Observe the report area | Report either shows rows for all available students (no filter = show all) or shows an empty state with no error or crash | "" |

**Severity:** minor
**Priority:** medium

---

## Suite: Report Access – Location-Based Access Control (LBAC)

### [Riso] Monthly Lesson Assignment Report – LBAC – Report Only Shows Data for User's Assigned Location

**Description:** LBAC — Permission Matrix — When the report is loaded, only data for the user's assigned location is returned. A user assigned to Tokyo Branch does not see student-course rows belonging to Osaka Branch, even if Osaka Branch exists in the system.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org whose assigned location is **Tokyo Branch only**
- Contracts and session data exist for students at both Tokyo Branch and Osaka Branch in AY 2025-2026
- today = 2026-06-22; current_AY = 2025-2026; user_assigned_location = Tokyo Branch

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page | Report page loads | today = 2026-06-22; user_assigned_location = Tokyo Branch |
| 2 | Observe all rows in the report without changing any filter | Only rows where Location = **Tokyo Branch** are displayed; no rows for Osaka Branch are shown | Student X at Tokyo Branch; Student Y at Osaka Branch |
| 3 | Confirm that Student Y (Osaka Branch) is absent from the report | No row with Location = Osaka Branch appears in the report data | Expected: Student Y row is not visible to this user |

**Severity:** major
**Priority:** high

---

### [Riso] Monthly Lesson Assignment Report – LBAC – Changing Location Filter Cannot Expose Unassigned Location Data

**Description:** LBAC — Negative — A user assigned to Tokyo Branch cannot retrieve data for Osaka Branch by manually changing the Location filter to Osaka Branch. The system enforces location scope at the data layer, not only via the default filter value.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org whose assigned location is **Tokyo Branch only** (not assigned to Osaka Branch)
- Contracts and session data exist for students at Osaka Branch in AY 2025-2026
- today = 2026-06-22; current_AY = 2025-2026; user_assigned_location = Tokyo Branch

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Monthly Lesson Assignment report page | Report page loads; Location filter defaults to Tokyo Branch | today = 2026-06-22; user_assigned_location = Tokyo Branch |
| 2 | Manually change the Location filter to **Osaka Branch** and apply | The report returns no rows (or only rows within the user's permitted scope); Osaka Branch data is **not** returned | Attempting to filter by Osaka Branch (unassigned location) |
| 3 | Confirm that no Osaka Branch student rows appear | Report area shows empty state or unchanged Tokyo Branch data; no Osaka Branch rows are exposed | Expected: system blocks data access, not just UI filtering |

**Severity:** critical
**Priority:** high

---
