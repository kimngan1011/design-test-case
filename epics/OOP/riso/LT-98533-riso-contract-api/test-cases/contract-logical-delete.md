# Test Cases: LT-98533 — Riso | OOP | Contract API (Create/Update via External System)

## Suite: [Riso] Contract Logical Delete + Aggregation (V1/D1, Last Active)

### [Riso] Contract Delete – Logical deletion – Record marked as deleted but kept in DB

**Description:** AC-DEL-1 / AC-DEL-2 — CRUD / State Transition — Verify that setting contract_status to Deleted only performs a soft delete.

**Preconditions:**
- API Client is authenticated with correct scope
- Contract exists with `external_ref_id = REF_DEL_01` and `contract_status = Active`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send PATCH request to `/v1/contracts/{external_ref_id}` with `contract_status = Deleted` | API returns HTTP 200 OK | `external_ref_id = REF_DEL_01`, `contract_status = Deleted` |
| 2 | Query the database directly for the contract record | The record exists in the database. `contract_status` is `Deleted` and `deleted_at` is populated with a timestamp. | "" |

**Severity:** critical
**Priority:** high

---

### [Riso] Contract Delete – Unlinked contract (V1) – Record deleted, no aggregation triggered

**Description:** AC-DEL-4 — Decision Table — Verify deleting an unlinked contract has no aggregation side effects.

**Preconditions:**
- API Client is authenticated with correct scope
- Unlinked Contract exists with `external_ref_id = REF_DEL_02` (`lesson_allocation_id` is null)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send PATCH request to `/v1/contracts/{external_ref_id}` with `contract_status = Deleted` | API returns HTTP 200 OK | `external_ref_id = REF_DEL_02`, `contract_status = Deleted` |
| 2 | Query the contract and any system LAs | The contract is marked deleted. No LA data is affected. | "" |

**Severity:** minor
**Priority:** medium

---

### [Riso] LA Aggregation – Contract Delete (D1) – Remaining active contracts – LA recalculates based on remaining

**Description:** AC-DEL-3 / AC-DEL-5 — Decision Table — Verify that when a linked contract is deleted, the LA recalculates aggregation fields using only the remaining active contracts.

**Preconditions:**
- API Client is authenticated with correct scope
- Lesson Allocation `LA_DEL_01` exists
- Contract A (active) is linked to `LA_DEL_01` (`slot = 10`, `start_date = 2026-06-01`, `end_date = 2026-06-15`)
- Contract B (active) is linked to `LA_DEL_01` (`slot = 10`, `start_date = 2026-06-15`, `end_date = 2026-06-30`)
- Current `LA_DEL_01` state: `Total_Session_Count = 20`, `Start_Date = 2026-06-01`, `End_Date = 2026-06-30`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send PATCH request to update Contract B with `contract_status = Deleted` | API returns HTTP 200 OK | Contract B external ref ID |
| 2 | Query `LA_DEL_01` record | `LA_DEL_01` is synchronously updated based on the only remaining active contract (Contract A) | "" |
| 3 | Verify `Total_Session_Count` on `LA_DEL_01` | `Total_Session_Count` = 10 | "" |
| 4 | Verify `Start_Date` on `LA_DEL_01` | `Start_Date` = 2026-06-01 | "" |
| 5 | Verify `End_Date` on `LA_DEL_01` | `End_Date` = 2026-06-15 | "" |
| 6 | Verify Contract A | Contract A is completely unaffected | "" |

**Severity:** critical
**Priority:** high

---

### [Riso] LA Cascade Delete – Last Contract Delete (D1) – All contracts deleted – LA is also soft-deleted

**Description:** AC-DEL-3 — Decision Table / Negative — Verify the critical edge case: when the last active contract linked to an LA is logically deleted, the LA itself is also automatically soft-deleted (cascade delete). The LA should no longer appear as active.

**Preconditions:**
- API Client is authenticated with correct scope
- Lesson Allocation `LA_DEL_LAST` exists
- Contract C is the *only* active contract linked to `LA_DEL_LAST` (`slot = 8`, `start_date = 2026-07-01`, `end_date = 2026-07-31`)
- Current `LA_DEL_LAST` state: `Total_Session_Count = 8`, `Start_Date = 2026-07-01`, `End_Date = 2026-07-31`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send PATCH request to update Contract C with `contract_status = Deleted` (the only active contract linked to `LA_DEL_LAST`) | API returns HTTP 200 OK | Contract C external ref ID |
| 2 | Query `LA_DEL_LAST` record | `LA_DEL_LAST` is also marked as Deleted (cascade delete triggered because no active contracts remain) | "" |
| 3 | Verify `LA_DEL_LAST` status | `LA_DEL_LAST` status = Deleted | "" |
| 4 | Verify `LA_DEL_LAST` does not appear in active LA lists | `LA_DEL_LAST` does NOT appear in any active/available LA listing | "" |
| 5 | Verify `deleted_at` field on `LA_DEL_LAST` | `deleted_at` is populated with a timestamp | "" |

**Severity:** critical
**Priority:** high

---
