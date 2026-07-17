# Test Cases: LT-98531 — [Riso] Contract List (Contact > Course Tab)

## Suite: Contract List – Display & Columns

### [Riso] Contract List – Contact > Course Tab – Active Tab with Current-AY Contracts – Contract List Rendered

**Description:** AC-01 — Component — Contract list is rendered on the Contact > Course Active tab for a Riso user when current-AY contracts exist.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- A student (Contact) exists with at least one contract in Academic Year 2025-2026
- today = 2026-06-22; current_AY = 2025-2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contact record for the student | Contact record page loads | today = 2026-06-22; current_AY = 2025-2026 |
| 2 | Click the **Course** tab on the Contact record | Course tab is displayed | "" |
| 3 | Observe the Active tab content | A Contract List section is visible, containing at least one contract row for AY 2025-2026 | "" |

**Severity:** major
**Priority:** high

---

### [Riso] Contract List – Contact > Course Tab – All 6 Columns Present Simultaneously

**Description:** AC-01 — Component (Deep) — All six required columns (Lesson Allocation, Course, Start Date, End Date, Location, Contract Status) are present simultaneously in the contract list.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- A student (Contact) exists with one contract in AY 2025-2026 that has data for all six columns: linked Lesson Allocation record, Course name, Start Date, End Date, Location, and Contract Status
- today = 2026-06-22; current_AY = 2025-2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contact record for the student and click the **Course** tab | Course tab displays, Active tab shown | today = 2026-06-22; current_AY = 2025-2026 |
| 2 | Locate the Contract List section on the Active tab | Contract List section is visible | "" |
| 3 | Observe the column headers of the Contract List | The following six columns are all present: **Lesson Allocation**, **Course**, **Start Date**, **End Date**, **Location**, **Contract Status** | Expected columns: Lesson Allocation, Course, Start Date, End Date, Location, Contract Status |
| 4 | Observe the data row for the test contract | The row displays a non-empty value under each of the six columns | "" |

**Severity:** major
**Priority:** high

---

### [Riso] Contract List – Contact > Course Tab – No Contracts Exist – Empty State Displayed

**Description:** AC-01 — Negative — When a contact has no contracts for the current AY, an empty state is displayed without an error.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- A student (Contact) exists with no contracts in AY 2025-2026
- today = 2026-06-22; current_AY = 2025-2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contact record for the student and click the **Course** tab | Course tab loads | today = 2026-06-22; current_AY = 2025-2026 |
| 2 | Observe the Active tab Contract List area | An empty state indicator is shown (e.g., placeholder message or empty table); no error or crash occurs | "" |

**Severity:** minor
**Priority:** medium

---

### [Riso] Contract List – Active Tab – Current-AY Contracts Shown; Prior-AY Contracts Not Shown

**Description:** AC-01 — Decision Table — Active tab shows only current-AY (2025-2026) contracts; a contract from a prior AY (2024-2025) does not appear on Active tab.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Student (Contact) has two contracts: one in AY 2025-2026 (active) and one in AY 2024-2025 (prior)
- today = 2026-06-22; current_AY = 2025-2026; previous_AY = 2024-2025

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contact record and click the **Course** tab | Course tab loads showing the Active tab | today = 2026-06-22; current_AY = 2025-2026; previous_AY = 2024-2025 |
| 2 | Observe the rows in the Contract List on the Active tab | Only the AY 2025-2026 contract is listed; the AY 2024-2025 contract is not present | AY 2025-2026 contract: Start Date = 2025-04-01; AY 2024-2025 contract: Start Date = 2024-04-01 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Contract List – Inactive Tab – Previous-AY Contracts Shown; Current-AY Contracts Not Shown

**Description:** AC-01 — Decision Table — Inactive tab shows only previous-AY (2024-2025) contracts; the current-AY contract does not appear on the Inactive tab.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Student (Contact) has contracts in both AY 2025-2026 and AY 2024-2025
- today = 2026-06-22; current_AY = 2025-2026; previous_AY = 2024-2025

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contact record and click the **Course** tab | Course tab loads | today = 2026-06-22; current_AY = 2025-2026; previous_AY = 2024-2025 |
| 2 | Click the **Inactive** tab in the Contract List section | Inactive tab is displayed | "" |
| 3 | Observe the rows in the Contract List on the Inactive tab | Only the AY 2024-2025 contract is listed; the AY 2025-2026 contract is not present | AY 2025-2026 contract: Start Date = 2025-04-01; AY 2024-2025 contract: Start Date = 2024-04-01 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Contract List – Active Tab Has Data, Inactive Tab Empty – Both Tabs Render Without Error

**Description:** AC-01 — Negative — When Active tab has contracts but Inactive tab has none, both tabs render without error; and vice versa.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Scenario A: Student has a contract in AY 2025-2026 only (no prior-AY contracts)
- Scenario B: Student has a contract in AY 2024-2025 only (no current-AY contracts)
- today = 2026-06-22; current_AY = 2025-2026; previous_AY = 2024-2025

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | (Scenario A) Open the Contact with only a current-AY contract; click **Course** tab | Active tab shows one contract row | today = 2026-06-22; Scenario A: contact has AY 2025-2026 contract only |
| 2 | (Scenario A) Click the **Inactive** tab | Inactive tab shows an empty state without error | "" |
| 3 | (Scenario B) Open the Contact with only a prior-AY contract; click **Course** tab | Active tab shows an empty state without error | Scenario B: contact has AY 2024-2025 contract only |
| 4 | (Scenario B) Click the **Inactive** tab | Inactive tab shows one contract row; no error | "" |

**Severity:** minor
**Priority:** medium

---

## Suite: Contract List – Sort Order

### [Riso] Contract List – Sort Order – Location ASC then Course ASC then Start Date ASC on Load

**Description:** AC-02 — Scenario — Contract list rows are sorted by Location ASC, then Course ASC, then Start Date ASC when the page first loads.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Student (Contact) has three contracts in AY 2025-2026 with different Location and Course values (see test data)
- today = 2026-06-22; current_AY = 2025-2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contact record and click the **Course** tab | Course tab loads with the Active tab visible | today = 2026-06-22; Contracts: (A) Location=Tokyo, Course=Math, Start=2025-05-01; (B) Location=Osaka, Course=English, Start=2025-04-01; (C) Location=Tokyo, Course=English, Start=2025-04-01 |
| 2 | Observe the row order in the Contract List | Rows appear in the following order from top to bottom: (1) Osaka–English–2025-04-01, (2) Tokyo–English–2025-04-01, (3) Tokyo–Math–2025-05-01 | Expected order: Osaka < Tokyo (Location ASC); within Tokyo: English < Math (Course ASC) |

**Severity:** minor
**Priority:** medium

---

### [Riso] Contract List – Sort Order – Same Location and Course, Ordered by Start Date ASC

**Description:** AC-02 — Pairwise — When two contracts share the same Location and Course, the tiebreaker is Start Date ASC.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Student (Contact) has two contracts in AY 2025-2026 with identical Location and Course but different Start Dates
- today = 2026-06-22; current_AY = 2025-2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contact record and click the **Course** tab | Course tab loads with the Active tab visible | today = 2026-06-22; Contract X: Location=Tokyo, Course=English, Start=2025-04-01; Contract Y: Location=Tokyo, Course=English, Start=2025-07-01 |
| 2 | Observe the two contract rows in the Contract List | Contract X (Start=2025-04-01) appears above Contract Y (Start=2025-07-01) | Expected: 2025-04-01 before 2025-07-01 (Start Date ASC tiebreaker) |

**Severity:** minor
**Priority:** medium

---

### [Riso] Contract List – Sort Order – Sort Re-applied After Page Refresh

**Description:** AC-02 — Scenario — The sort order (Location ASC → Course ASC → Start Date ASC) is preserved after the page is refreshed.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Student (Contact) has three contracts with different Location and Course values (same as sort-on-load test data)
- today = 2026-06-22; current_AY = 2025-2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contact record and click the **Course** tab; note the order of the three contract rows | Rows appear in correct sorted order: Osaka–English, Tokyo–English, Tokyo–Math | today = 2026-06-22; Contracts: (A) Tokyo/Math/2025-05-01; (B) Osaka/English/2025-04-01; (C) Tokyo/English/2025-04-01 |
| 2 | Refresh the browser page | Page reloads | "" |
| 3 | Return to the Contact **Course** tab and observe the row order | Rows appear in the same sorted order as before: (1) Osaka–English–2025-04-01, (2) Tokyo–English–2025-04-01, (3) Tokyo–Math–2025-05-01 | Expected: sort order is identical after refresh |

**Severity:** minor
**Priority:** medium

---

## Suite: Contract List – Not Require Allocation (NRA) List

### [Riso] Contract List – NRA List – Hidden on Contact > Course Tab for Riso

**Description:** AC-03 — Decision Table — The "Not Require Allocation" list section is not rendered on the Contact > Course tab when logged in as a Riso user.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- The Contact has at least one LA record with Require Allocation = FALSE (to confirm there is data that would appear in the NRA list if it were shown)
- today = 2026-06-22

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open a Contact record and click the **Course** tab | Course tab loads | today = 2026-06-22; Riso org user |
| 2 | Inspect all sections rendered on the Course tab | No section labeled "Not Require Allocation" (or equivalent) is present on the page | "" |

**Severity:** major
**Priority:** high

---

### [Riso] Contract List – NRA List Hidden – Contract List Section Still Displayed (Isolation)

**Description:** AC-03 — Negative — Hiding the "Not Require Allocation" list does not remove or break the Contract List section on the same tab.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- A student (Contact) has at least one contract in AY 2025-2026
- today = 2026-06-22; current_AY = 2025-2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contact record and click the **Course** tab | Course tab loads | today = 2026-06-22; current_AY = 2025-2026 |
| 2 | Observe all sections on the Active tab | The "Not Require Allocation" section is absent; the Contract List section is present and shows the expected contract rows | "" |
| 3 | Confirm the contract row data is complete and not corrupted | All six columns (Lesson Allocation, Course, Start Date, End Date, Location, Contract Status) display correct values | "" |

**Severity:** major
**Priority:** high

---

### [Riso] Contract List – REGRESSION LT-92532 – Contact > Course Tab No Longer Shows NRA Section

**Description:** AC-03 — Regression — Following the LT-98531 change, the Contact > Course tab for a Riso user no longer shows the "Not Require Allocation" list that was present under LT-92532. This TC guards against the NRA section re-appearing after future deployments.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- The Contact has LA records covering both Require Allocation = TRUE and Require Allocation = FALSE (to simulate pre-LT-98531 data)
- today = 2026-06-22

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contact record and click the **Course** tab | Course tab loads; page does not throw an error | today = 2026-06-22; Riso org; Contact has both Require=TRUE and Require=FALSE LA records |
| 2 | Review all visible sections on the Course tab | Only the Require Allocation list (and the new Contract List) are present; the "Not Require Allocation" section is absent | "" |
| 3 | Confirm the Require Allocation list section is still rendered correctly | Require Allocation list section is present with its rows intact | "" |

**Severity:** major
**Priority:** high

---

## Suite: Contract List – Partner Scope Gate

### [Riso] Contract List – Riso Partner – Contract List Rendered on Contact > Course Tab

**Description:** AC-04 — Permission Matrix — A Riso HQ or CM user sees the Contract List section on the Contact > Course tab.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- A student (Contact) exists with at least one contract in AY 2025-2026
- today = 2026-06-22; current_AY = 2025-2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contact record for the student and click the **Course** tab | Course tab loads | today = 2026-06-22; Riso HQ or CM user |
| 2 | Observe the Active tab | A Contract List section is visible and shows contract rows | "" |

**Severity:** major
**Priority:** high

---

### [Riso] Contract List – Non-Riso Partner – Contract List Not Rendered

**Description:** AC-04 — Negative — A user from a non-Riso partner org does not see the Contract List section on the Contact > Course tab.

**Preconditions:**
- Logged in as HQ or CM Staff to a **non-Riso** partner Salesforce org
- A student (Contact) exists on that org
- today = 2026-06-22

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contact record and click the **Course** tab | Course tab loads | today = 2026-06-22; non-Riso partner user |
| 2 | Observe all sections on the Course tab | No Contract List section is present; the tab layout reflects the non-Riso configuration | "" |

**Severity:** major
**Priority:** high

---

## Suite: Contract List – Lesson Allocation Display

### [Riso] Contract List – Lesson Allocation Column – Linked LA Record Displayed

**Description:** AC-05 — Component — The Lesson Allocation column in the contract list shows the name or identifier of the LA record linked to the contract.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- A student (Contact) has a contract in AY 2025-2026 that is linked to a Lesson Allocation (LA) record
- today = 2026-06-22; current_AY = 2025-2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contact record and click the **Course** tab | Course tab loads with the Active tab | today = 2026-06-22; Contract linked to LA record named "LA-2025-001" |
| 2 | Locate the contract row in the Contract List | The **Lesson Allocation** column displays the linked LA record identifier (e.g., "LA-2025-001") | Expected Lesson Allocation value: the linked LA record name |

**Severity:** minor
**Priority:** medium

---

### [Riso] Contract List – Lesson Allocation Column – Blank When No LA Linked

**Description:** AC-05 — Negative — The Lesson Allocation column is blank for a contract that has no linked LA record.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- A student (Contact) has a contract in AY 2025-2026 with no linked Lesson Allocation record
- today = 2026-06-22; current_AY = 2025-2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contact record and click the **Course** tab | Course tab loads with the Active tab | today = 2026-06-22; Contract with no linked LA record |
| 2 | Locate the contract row in the Contract List | The **Lesson Allocation** column cell is blank (empty, no value) for that contract row | "" |

**Severity:** minor
**Priority:** medium

---

## Suite: Contract List – Location-Based Access Control (LBAC)

### [Riso] Contract List – LBAC – Staff Sees Only Contracts for Their Assigned Location

**Description:** LBAC — Permission Matrix — A staff user assigned to Tokyo Branch can only see contracts belonging to Tokyo Branch in the Contract List on the Contact > Course tab. Contracts from other locations (e.g., Osaka Branch) are not visible regardless of which Contact is opened.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org whose assigned location is **Tokyo Branch only**
- A student (Contact) has two contracts in AY 2025-2026: one at Tokyo Branch and one at Osaka Branch
- today = 2026-06-22; current_AY = 2025-2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contact record for the student and click the **Course** tab | Course tab loads with the Active tab | today = 2026-06-22; user_assigned_location = Tokyo Branch only |
| 2 | Observe the rows in the Contract List | Only the Tokyo Branch contract row is displayed; the Osaka Branch contract row is **not** visible | Contract A: Location = Tokyo Branch; Contract B: Location = Osaka Branch |
| 3 | Confirm the Osaka Branch contract is absent from the list | No row with Location = Osaka Branch appears in the contract list | Expected: only Contract A (Tokyo Branch) is shown |

**Severity:** major
**Priority:** high

---

### [Riso] Contract List – LBAC – Staff Cannot View Contracts from Unassigned Location

**Description:** LBAC — Negative — A staff user who is **not** assigned to Osaka Branch cannot see any contracts at Osaka Branch in the Contract List, even if the Contact has active contracts there.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org whose assigned location is **Tokyo Branch only** (not assigned to Osaka Branch)
- A student (Contact) has at least one contract in AY 2025-2026 at **Osaka Branch** and no contract at Tokyo Branch
- today = 2026-06-22; current_AY = 2025-2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contact record for the student and click the **Course** tab | Course tab loads with the Active tab | today = 2026-06-22; user_assigned_location = Tokyo Branch; student has only Osaka Branch contract |
| 2 | Observe the Contract List on the Active tab | The Contract List is empty (empty state shown) or the Osaka Branch contract row is not visible | Expected: no contract rows displayed; the Osaka Branch contract is not accessible to this user |

**Severity:** major
**Priority:** high

---
