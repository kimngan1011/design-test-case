# Test Cases: LT-98530 — [Riso] OOP | Contract and Monthly Lesson history (App)

> **Confirmed 2026-08-13; updated with PdM clarification:** These cases validate the Riso App calculation in AC01.2. PRD "Seasonal" means `Contract.type=one-time`; Trial is not a valid Riso Contract.type. A `one-time` contract uses Contract Total, not Slot Number. For `weekly`, convert Weekly Slot to Monthly Slot by multiplying by 4, then apply the Monthly formula. For both `monthly` and `weekly`, a selected month before Start Month contributes 0 and a selected month after End Month is capped at the full inclusive contract duration. The App's selected-month calculation is intentionally distinct from the backend flat LA aggregation.

- **One-time boundary rule:** Once the selected month reaches the Contract Start Month, the full Contract Total is contributed, including when the selected month is after the Contract End Month.

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

### [Riso] Total Slot – Monthly Contract – Selected Month Before Contract Duration – Zero Counted

**Description:** AC01.2 — BVA (below contract duration) — When the selected month is before Contract Start Month, the contract has not started and contributes zero to Total Slot.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has one Active Monthly-type Riso Contract: start=2026-06, end=2026-08, monthly slot=1

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the month selector to May 2026 (1 month before contract start) and view the LA card | Total Slot shows 0 for this contract | contract_start=2026-06; contract_end=2026-08; selected_month=2026-05; selected_month < contract_start; expected=0 |

**Severity:** critical
**Priority:** high

---

### [Riso] Total Slot – Monthly Contract – Selected Month After Contract Duration – Full Duration Capped at End Month

**Description:** AC01.2 — BVA (above contract duration) — When the selected month is after Contract End Month, the Total Slot includes the complete inclusive contract duration only and does not add months after the End Month.

**Preconditions:**
- The Student is logged in to the Riso Learner App.
- The Lesson Allocation has one Active Monthly-type Riso Contract: start=2026-06, end=2026-08, Monthly Slot=1.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student selects October 2026 in the Contract Info month selector and views the Lesson Allocation card | The Total Slot shows 3 | contract_start=2026-06; contract_end=2026-08; selected_month=2026-10; counted_months=Jun+Jul+Aug=3; monthly_slot=1; expected=1×3=3 |

**Severity:** critical
**Priority:** high

---

### [Riso] Total Slot – Weekly Contract – Start Month – Weekly Slot Converted to Monthly Equivalent

**Description:** AC01.2 — BVA — A Weekly Slot is multiplied by 4 to derive the Monthly Slot before the monthly Total Slot formula is applied. At the contract Start Month, one elapsed month is counted.

**Preconditions:**
- The Student is logged in to the Riso Learner App.
- The Lesson Allocation has one Active Riso Contract: type=`weekly`, start=2025-04, end=2026-02, Weekly Slot=1.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student selects April 2025 in the Contract Info month selector and views the Lesson Allocation card | The Total Slot shows 4 | contract_type=weekly; weekly_slot=1; monthly_slot=1×4=4; contract_start=2025-04; selected_month=2025-04; elapsed_months=1; expected=4×1=4 |

**Severity:** critical
**Priority:** high

---

### [Riso] Total Slot – Weekly Contract – Selected Month Before Contract Duration – Zero Counted

**Description:** AC01.2 — BVA (below contract duration) — A Weekly contract contributes zero when the selected month is before Contract Start Month; Weekly Slot conversion does not create a contribution before the contract starts.

**Preconditions:**
- The Student is logged in to the Riso Learner App.
- The Lesson Allocation has one Active Riso Contract: type=`weekly`, start=2026-06, end=2026-08, Weekly Slot=1.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student selects May 2026 in the Contract Info month selector and views the Lesson Allocation card | The Total Slot shows 0 | contract_type=weekly; weekly_slot=1; monthly_slot=1×4=4; contract_start=2026-06; contract_end=2026-08; selected_month=2026-05; selected_month < contract_start; expected=0 |

**Severity:** critical
**Priority:** high

---

### [Riso] Total Slot – Weekly Contract – Selected Month After Contract Duration – Full Duration Capped at End Month

**Description:** AC01.2 — BVA (above contract duration) — When the selected month is after Contract End Month, a Weekly Slot is first converted to a Monthly Slot and then counted only for the complete inclusive contract duration.

**Preconditions:**
- The Student is logged in to the Riso Learner App.
- The Lesson Allocation has one Active Riso Contract: type=`weekly`, start=2026-06, end=2026-08, Weekly Slot=1.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student selects October 2026 in the Contract Info month selector and views the Lesson Allocation card | The Total Slot shows 12 | contract_type=weekly; weekly_slot=1; monthly_slot=1×4=4; contract_start=2026-06; contract_end=2026-08; selected_month=2026-10; counted_months=Jun+Jul+Aug=3; expected=4×3=12 |

**Severity:** critical
**Priority:** high

---

### [Riso] Total Slot – Weekly Contract – Elapsed Months From Start – Monthly Equivalent Times Month Count

**Description:** AC01.2 — Decision Table — A Weekly Slot is multiplied by 4 first, then the derived Monthly Slot is multiplied by the elapsed-month count, the same calculation used for a Monthly contract.

**Preconditions:**
- The Student is logged in to the Riso Learner App.
- The Lesson Allocation has one Active Riso Contract: type=`weekly`, start=2025-04, end=2026-02, Weekly Slot=1.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student selects September 2025 in the Contract Info month selector and views the Lesson Allocation card | The Total Slot shows 24 | contract_type=weekly; weekly_slot=1; monthly_slot=1×4=4; contract_start=2025-04; selected_month=2025-09; elapsed_months=6; expected=4×6=24 |

**Severity:** critical
**Priority:** high

---

### [Riso] Total Slot – One-Time Contract – Selected Month After Start Month – Contract Total Counted

**Description:** AC01.2 — BVA — For a `one-time` contract (called Seasonal in the PRD), the Contract Total is counted when the selected month (EOM) is after the contract Start Month; Slot Number is not used.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has one Active `one-time` Riso Contract: start=2025-08, end=2025-09, Slot Number=4, Contract Total=100

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the month selector to September 2025 and view the LA card | Total Slot shows 100 | contract_start=2025-08; selected_month(EOM)=2025-09-30; contract_total=100; slot_number=4; 2025-08 <= 2025-09-30 → Contract Total counted; expected=100 |

**Severity:** critical
**Priority:** high

---

### [Riso] Total Slot – One-Time Contract – Selected Month Equals Start Month – Contract Total Counted

**Description:** AC01.2 — BVA (exact boundary) — When the selected month equals a `one-time` contract's Start Month, the Contract Total is counted. Slot Number is not used.

**Preconditions:**
- The Student is logged in to the Riso Learner App.
- The Lesson Allocation has one Active `one-time` Riso Contract: start=2026-06, end=2026-08, Slot Number=4, Contract Total=20.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student selects June 2026 in the Contract Info month selector and views the Lesson Allocation card | The Total Slot shows 20 | contract_type=one-time; contract_start=2026-06; contract_end=2026-08; selected_month=2026-06; contract_total=20; slot_number=4; selected_month = contract_start; expected=20 |

**Severity:** critical
**Priority:** high

---

### [Riso] Total Slot – One-Time Contract – Selected Month After Contract End Month – Contract Total Counted

**Description:** AC01.2 — BVA (above contract duration) — When the selected month is after a `one-time` contract's End Month, the full Contract Total remains counted. Slot Number is not used.

**Preconditions:**
- The Student is logged in to the Riso Learner App.
- The Lesson Allocation has one Active `one-time` Riso Contract: start=2026-06, end=2026-08, Slot Number=4, Contract Total=20.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student selects October 2026 in the Contract Info month selector and views the Lesson Allocation card | The Total Slot shows 20 | contract_type=one-time; contract_start=2026-06; contract_end=2026-08; selected_month=2026-10; selected_month > contract_end; contract_total=20; slot_number=4; expected=20 |

**Severity:** critical
**Priority:** high

---

### [Riso] Total Slot – One-Time Contract – Selected Month Before Start – Zero Counted

**Description:** AC01.2 — BVA (below boundary) — A `one-time` contract contributes zero when the selected month (EOM) is before the contract Start Month.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has one Active `one-time` Riso Contract: start=2025-08, end=2025-09, Slot Number=4, Contract Total=100

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
