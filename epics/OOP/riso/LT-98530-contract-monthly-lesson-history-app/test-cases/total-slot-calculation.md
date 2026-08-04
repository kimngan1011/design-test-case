# Test Cases: LT-98530 — [Riso] OOP | Contract and Monthly Lesson history (App)

> ⚠️ **Pending Confirmation:** Every test case in this suite validates the PRD's stated Total Slot formula (AC01.2), which conflicts with the authoritative Contract API spec (LT-98533 — flat SUM aggregation, no proration) and has an undefined formula for Trial-type contracts. See spec Clarification Questions #1 and #5. These test cases are written against the PRD as primary per user instruction, and are expected to require rework once the Jira thread resolves.

## Suite: [Riso] Total Slot Calculation (Pending Confirmation)

### [Riso] Total Slot – Monthly Contract – Elapsed Months From Start – Slot Times Month Count

**Description:** AC01.2 — BVA — Total Slot for a Monthly-type contract equals Monthly Slot multiplied by the number of elapsed months from Contract Start Month to Selected Month.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has one Active Monthly-type Riso Contract: start=2025-04, end=2026-02, monthly slot=4

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the Contract Info month selector to September 2025 and view the LA card | Total Slot shows 24 | contract_start=2025-04; monthly_slot=4; selected_month=2025-09; elapsed_months=6; expected=4×6=24 |

**Severity:** critical
**Priority:** high

---

### [Riso] Total Slot – Monthly Contract – Selected Month Equals Start Month – Boundary of One Elapsed Month

**Description:** AC01.2 — BVA (exact boundary) — When the selected month equals the contract start month, the elapsed-month count is 1, not 0.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has one Active Monthly-type Riso Contract: start=2025-04, end=2026-02, monthly slot=4

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the month selector to April 2025 (= contract start month) and view the LA card | Total Slot shows 4 | contract_start=2025-04; selected_month=2025-04; elapsed_months=1 (boundary); expected=4×1=4 |

**Severity:** critical
**Priority:** high

---

### [Riso] Total Slot – Monthly Contract – Selected Month Before Start Month – Zero Counted

**Description:** AC01.2 — BVA (below boundary) — When the selected month is before the contract start month, this contract contributes zero to Total Slot.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has one Active Monthly-type Riso Contract: start=2025-04, monthly slot=4

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the month selector to March 2025 (1 month before contract start) and view the LA card | Total Slot shows 0 for this contract | contract_start=2025-04; selected_month=2025-03 (below boundary); expected=0 |

**Severity:** critical
**Priority:** high

---

### [Riso] Total Slot – Seasonal Contract – Selected Month Within Range – Full Slot Counted

**Description:** AC01.2 — BVA — For a Seasonal-type contract, the full slot value is counted once the selected month (EOM) is on or after the contract start month.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has one Active Seasonal-type Riso Contract: start=2025-08, end=2025-09, total slot=100

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the month selector to September 2025 and view the LA card | Total Slot shows 100 | contract_start=2025-08; selected_month(EOM)=2025-09-30; 2025-08 <= 2025-09-30 → full slot; expected=100 |

**Severity:** critical
**Priority:** high

---

### [Riso] Total Slot – Seasonal Contract – Selected Month Before Start – Zero Counted

**Description:** AC01.2 — BVA (below boundary) — A Seasonal-type contract contributes zero when the selected month (EOM) is before the contract start month.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has one Active Seasonal-type Riso Contract: start=2025-08, end=2025-09, total slot=100

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the month selector to May 2025 and view the LA card | Total Slot shows 0 for this contract | contract_start=2025-08; selected_month(EOM)=2025-05-31; 2025-08 > 2025-05-31 → zero; expected=0 |

**Severity:** critical
**Priority:** high

---

### [Riso] Total Slot – Multiple Active Contracts on Same LA – Sum of All Contributions

**Description:** AC01.2 — Decision Table / Data Integrity — Total Slot sums the contributions of every Active Riso Contract linked to the LA.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has 2 Active Riso Contracts for the selected month (Sep 2025): Contract-1 (Monthly, contributes 24), Contract-2 (Seasonal, contributes 100)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the month selector to September 2025 and view the LA card | Total Slot shows 124 | contract_1_contribution=24; contract_2_contribution=100; expected sum=124 |

**Severity:** critical
**Priority:** high

---

### [Riso] Total Slot – Logically Deleted Contract – Excluded From Sum

**Description:** AC01.2 — Negative — A logically deleted (contract_status=Deleted) Riso Contract must not contribute to Total Slot.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has Contract-1 (Active, Monthly, contributes 24) and Contract-2 (logically Deleted, would have contributed 100)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the month selector to September 2025 and view the LA card | Total Slot shows 24 (Contract-2 excluded) | contract_1=24 (Active); contract_2=100 (Deleted, excluded); expected=24 |

**Severity:** critical
**Priority:** high

---

### [Riso] Total Slot – Trial Contract Type – No Confirmed Calculation Formula (Pending Confirmation)

**Description:** AC01.2 — Negative / Placeholder — Figma shows a Trial-type LA card with its own Total Slot value, but no calculation rule is defined anywhere in the PRD, domain knowledge, or sibling specs. This TC documents the gap rather than asserting a formula (spec Clarification Question #5).

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA is of Trial type with an Active Riso Contract

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the month selector to any month and view the Trial-type LA card | A Total Slot value is displayed without crashing; exact formula is pending PM confirmation and must be re-validated once defined | la_type=Trial; formula=undefined (pending) |

**Severity:** critical
**Priority:** high

---

### [Riso] Total Slot – Month Boundary – Contract Comparison Near Midnight JST vs UTC

**Description:** AC01.2 — BVA (mandatory timezone rule) — Month/date comparisons used in the Total Slot formula (Start Month, Selected Month EOM) must be derived from the JST-displayed date, not the raw UTC-stored value.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has one Active Monthly-type Riso Contract with start_date stored as `2025-08-31 15:30 UTC` (= `2025-09-01 00:30 JST`)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the month selector to September 2025 and view the LA card | Contract Start Month is treated as September 2025 (JST date), not August 2025 (UTC date) | contract_start_utc=2025-08-31 15:30 UTC; contract_start_jst=2025-09-01 00:30 JST; selected_month=2025-09; expected start month = 2025-09 (JST) |

**Severity:** critical
**Priority:** high

---

### [Riso] Total Slot – Cross-Surface Consistency – App Value vs Contract API Aggregation

**Description:** AC01.2 — Regression — Compares the App's computed Total Slot against the backend's LA.Total_Session_Count (flat SUM aggregation per LT-98533) for the same LA to surface the known formula conflict (spec Clarification Question #1).

**Preconditions:**
- Logged in as Student to the Riso Learner App and as HQ or CM Staff to the Salesforce org (same student's LA)
- LA has one Active Monthly-type Riso Contract: start=2025-04, monthly slot=4, selected month=Sep 2025

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | View Total Slot on the App Contract Info page | App shows 24 (per PRD's month-prorated formula) | app_total_slot = 4×6 = 24 |
| 2 | View LA.Total_Session_Count for the same LA on Salesforce | SF shows the flat SUM of contract.total (per LT-98533), which will differ from the App's 24 unless the contract's total field is separately set to 24 | sf_total_session_count = SUM(contract.total); expected mismatch flagged as pending confirmation, not a pass/fail assertion |

**Severity:** critical
**Priority:** high

---
