# Test Cases: LT-98533 — Riso | OOP | Contract API (Create/Update via External System)

## Suite: [Riso] NFR – Idempotency & Audit Timestamps

### [Riso] Contract API – Idempotency – Safe retries on POST/PATCH updates – Same state maintained

**Description:** NFR-03 — State Transition — Verify that repeating a state-mutating request with the exact same valid payload (upsert or update) is idempotent and does not cause unexpected side effects or errors.

**Preconditions:**
- API Client is authenticated with correct scope
- Contract exists with `external_ref_id = REF_IDEMP_01`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send POST request to `/v1/contracts` (upsert) or PATCH to `/v1/contracts/{external_ref_id}` with valid changes | API returns HTTP 200 OK (or 201 for upsert) and applies changes | `external_ref_id = REF_IDEMP_01`, `slot = 10` |
| 2 | Send the exact same request again immediately | API returns HTTP 200 OK (or 201). No error is thrown. | Same payload |
| 3 | Query the database | Contract state is exactly as it was after step 1. No duplicate records. | "" |
| 4 | Query LA aggregation fields (if linked) | LA aggregation fields remain unchanged after the second identical request | "" |

**Severity:** major
**Priority:** medium

---

### [Riso] Contract API – Audit Columns – Auto-populated on Create – created_at, updated_at set

**Description:** NFR-05 — Component — Verify standard audit columns are populated automatically upon record creation.

**Preconditions:**
- API Client is authenticated with correct scope

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send POST request to `/v1/contracts` to create a new contract | API returns HTTP 201 Created | `external_ref_id = REF_AUDIT_01` |
| 2 | Query the database for the new contract | System populated `created_at`, `updated_at`, and `resource_path` correctly | "" |

**Severity:** minor
**Priority:** medium

---

### [Riso] Contract API – Audit Columns – Auto-updated on PATCH – updated_at changes, created_at unchanged

**Description:** NFR-05 — Component — Verify updated_at changes on modification while created_at remains the same.

**Preconditions:**
- API Client is authenticated with correct scope
- Contract exists with `external_ref_id = REF_AUDIT_02`
- Wait for at least 1 second since creation

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Record current `created_at` and `updated_at` timestamps of the contract | Timestamps noted | "" |
| 2 | Send PATCH request to `/v1/contracts/{external_ref_id}` with `slot = 20` | API returns HTTP 200 OK | `external_ref_id = REF_AUDIT_02`, `slot = 20` |
| 3 | Query the database for the contract | `updated_at` is newer than the previously recorded value. `created_at` is exactly the same as before. | "" |

**Severity:** minor
**Priority:** medium

---
