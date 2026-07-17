# Test Cases: LT-98533 — Riso | OOP | Contract API (Create/Update via External System)

## Suite: [Riso] LA Aggregation – POST Events (Case C1, C2a)

### [Riso] LA Aggregation – POST Create Linked (C1) – Recalculates all 3 fields

**Description:** AC-POST-7 — Component / Decision Table — Verify creating a new contract linked to an LA triggers recalculation of Total_Session_Count, Start_Date, and End_Date.

**Preconditions:**
- API Client is authenticated with correct scope
- Lesson Allocation `LA_AGG_01` exists with:
  - `Total_Session_Count = 10`
  - `Start_Date = 2026-06-01`
  - `End_Date = 2026-06-15`
- Contract A is currently active on this LA (`start_date = 2026-06-01`, `end_date = 2026-06-15`, `slot = 10`)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send POST request to create Contract B linked to `LA_AGG_01` with `slot = 5`, `start_date = 2026-05-15`, `end_date = 2026-06-20` | API returns HTTP 201 Created | `external_ref_id = NEW_C1_01`, `slot = 5`, `start_date = 2026-05-15`, `end_date = 2026-06-20`, `lesson_allocation_id = LA_AGG_01` |
| 2 | Query `LA_AGG_01` record | The 3 aggregation fields are synchronously updated to reflect the combined active contracts (A + B) | "" |
| 3 | Verify `Total_Session_Count` | `Total_Session_Count` = 15 (Contract A 10 + Contract B 5) | "" |
| 4 | Verify `Start_Date` | `Start_Date` = 2026-05-15 (earliest of 2026-06-01 and 2026-05-15) | "" |
| 5 | Verify `End_Date` | `End_Date` = 2026-06-20 (latest of 2026-06-15 and 2026-06-20) | "" |

**Severity:** critical
**Priority:** high

---

### [Riso] LA Aggregation – POST Create Unlinked (C1) – No aggregation triggered

**Description:** AC-POST-4 / AC-POST-7 — Decision Table — Verify creating an unlinked contract does not trigger any LA aggregation.

**Preconditions:**
- API Client is authenticated with correct scope
- Lesson Allocation `LA_AGG_02` exists with `Total_Session_Count = 5`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send POST request to create Contract C without `lesson_allocation_id` but with `slot = 10` | API returns HTTP 201 Created | `external_ref_id = NEW_C1_02`, `slot = 10`, `lesson_allocation_id` omitted |
| 2 | Query `LA_AGG_02` record and other LAs for the student | No LA aggregation fields are updated. `LA_AGG_02` still has `Total_Session_Count = 5` | "" |

**Severity:** major
**Priority:** high

---

### [Riso] LA Aggregation – POST Upsert (C2a) – Update slot/total – Recalculates Total_Session_Count

**Description:** AC-POST-8 — CRUD / Decision Table — Verify upserting a contract with a new slot value correctly updates the LA's Total_Session_Count.

**Preconditions:**
- API Client is authenticated with correct scope
- Lesson Allocation `LA_AGG_03` exists with `Total_Session_Count = 8`
- Contract D is linked to `LA_AGG_03` with `slot = 8`, `external_ref_id = UPSERT_C2A_01`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send POST request to upsert Contract D with `slot = 12` | API returns success | `external_ref_id = UPSERT_C2A_01`, `slot = 12` |
| 2 | Query `LA_AGG_03` record | `Total_Session_Count` is synchronously updated to 12. Start_Date and End_Date are unchanged. | "" |

**Severity:** critical
**Priority:** high

---

### [Riso] LA Aggregation – POST Upsert (C2a) – Update end_date – Recalculates End_Date

**Description:** AC-POST-8 — CRUD — Verify upserting a contract's end_date correctly updates the LA's End_Date.

**Preconditions:**
- API Client is authenticated with correct scope
- Lesson Allocation `LA_AGG_04` exists with `End_Date = 2026-07-01`
- Contract E is linked to `LA_AGG_04` with `end_date = 2026-07-01`, `external_ref_id = UPSERT_C2A_02`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send POST request to upsert Contract E with `end_date = 2026-07-15` | API returns success | `external_ref_id = UPSERT_C2A_02`, `end_date = 2026-07-15` |
| 2 | Query `LA_AGG_04` record | `End_Date` is synchronously updated to 2026-07-15. Total_Session_Count is unchanged. | "" |

**Severity:** critical
**Priority:** high

---

### [Riso] LA Aggregation – POST Upsert (C2a) – No aggregation fields changed – LA is unchanged

**Description:** AC-POST-8 — Decision Table — Verify upserting non-aggregation fields (e.g. name) does not affect LA aggregation fields.

**Preconditions:**
- API Client is authenticated with correct scope
- Lesson Allocation `LA_AGG_05` exists with `Total_Session_Count = 5`, `End_Date = 2026-08-01`
- Contract F is linked to `LA_AGG_05` with `external_ref_id = UPSERT_C2A_03`, `name = Old Name`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send POST request to upsert Contract F with `name = New Name` (slot, start_date, end_date remain the same) | API returns success | `external_ref_id = UPSERT_C2A_03`, `name = New Name` |
| 2 | Query `LA_AGG_05` record | LA aggregation fields (`Total_Session_Count`, `Start_Date`, `End_Date`) are unchanged | "" |

**Severity:** minor
**Priority:** medium

---

### [Riso] LA Aggregation – Conflict – Total_Session_Count overwrites Purchased_Slot synchronously

**Description:** AC-POST-7 / BR-14 — State Transition — Verify that auto-calculated Total_Session_Count overwrites any manually inputted Purchased_Slot from BO immediately upon contract aggregation.

**Preconditions:**
- API Client is authenticated with correct scope
- Lesson Allocation `LA_AGG_06` exists
- HQ Staff has manually entered `Purchased_Slot = 20` for `LA_AGG_06` via Back Office

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send POST request to create Contract G linked to `LA_AGG_06` with `slot = 5` | API returns HTTP 201 Created | `external_ref_id = NEW_C1_03`, `slot = 5`, `lesson_allocation_id = LA_AGG_06` |
| 2 | Query `LA_AGG_06` record | `Total_Session_Count` is set to 5, overwriting the manual `Purchased_Slot` value | "" |
| 3 | Login to Back Office and view `LA_AGG_06` details | The Purchased Slot / Total Session Count field displays 5 (auto-calculated value) | "" |

**Severity:** critical
**Priority:** high

---
