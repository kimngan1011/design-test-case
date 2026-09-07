# Test Cases: LT-98530 — [Riso] OOP | Contract and Monthly Lesson history (App)

> **Confirmed 2026-08-13:** These cases validate the Riso App calculation in AC01.2. PRD "Seasonal" means `Contract.type=one-time`; Trial is not a valid Riso Contract.type. The App's selected-month calculation is intentionally distinct from the backend flat LA aggregation.

## Suite: [Riso] Total Slot Calculation

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

### [Riso] Total Slot – One-Time Contract – Selected Month Within Range – Full Slot Counted

**Description:** AC01.2 — BVA — For a `one-time` contract (called Seasonal in the PRD), the full slot value is counted once the selected month (EOM) is on or after the contract start month.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has one Active `one-time` Riso Contract: start=2025-08, end=2025-09, total slot=100

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the month selector to September 2025 and view the LA card | Total Slot shows 100 | contract_start=2025-08; selected_month(EOM)=2025-09-30; 2025-08 <= 2025-09-30 → full slot; expected=100 |

**Severity:** critical
**Priority:** high

---

### [Riso] Total Slot – One-Time Contract – Selected Month Before Start – Zero Counted

**Description:** AC01.2 — BVA (below boundary) — A `one-time` contract contributes zero when the selected month (EOM) is before the contract start month.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has one Active `one-time` Riso Contract: start=2025-08, end=2025-09, total slot=100

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
- LA has 2 Active Riso Contracts for the selected month (Sep 2025): Contract-1 (Monthly, contributes 24), Contract-2 (`one-time`, contributes 100)

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
