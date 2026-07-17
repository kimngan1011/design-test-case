# Test Cases: LT-98533 — Riso | OOP | Contract API (Create/Update via External System)

## Suite: [Riso] POST Contract – Create & Upsert

### [Riso] POST Contract – Create – Valid required fields – New contract created successfully

**Description:** AC-POST-1 — Equivalence Partitioning — Verify successful creation when all required fields are valid.

**Preconditions:**
- API Client is authenticated with correct scope
- A student exists in Manabie with `student_id = STUDENT123`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send POST request to `/v1/contracts` with a new `external_ref_id` and all 11 required fields | API returns HTTP 201 Created | `external_ref_id = NEW_REF_001`, `type = weekly`, `student_id = STUDENT123` |
| 2 | Query the created Contract record in the database | The contract record is created with `contract_status = active` and the submitted field values | "" |

**Severity:** critical
**Priority:** high

---

### [Riso] POST Contract – Create – end_date omitted – Contract created successfully

**Description:** AC-POST-1 / BR-32 — Boundary Value Analysis — Verify creation succeeds when optional end_date is omitted.

**Preconditions:**
- API Client is authenticated with correct scope

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send POST request to `/v1/contracts` with a new `external_ref_id`, all required fields, but omitting `end_date` | API returns HTTP 201 Created | `external_ref_id = NEW_REF_002`, `start_date = 2026-06-01` |
| 2 | Query the created Contract record | The contract is created and `end_date` is null/empty | "" |

**Severity:** major
**Priority:** high

---

### [Riso] POST Contract – Create – end_date before start_date – Returns 422 Validation Error

**Description:** AC-POST-1 / BR-32 — Boundary Value Analysis (Negative) — Verify creation is rejected if end_date is earlier than start_date.

**Preconditions:**
- API Client is authenticated with correct scope
- `start_date = 2026-06-15`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send POST request to `/v1/contracts` with `end_date` set to 1 day before `start_date` | API returns HTTP 422 Validation Error (or 400 Bad Request) | `start_date = 2026-06-15`, `end_date = 2026-06-14` |

**Severity:** critical
**Priority:** high

---

### [Riso] POST Contract – Create – Invalid type value – Returns 422 Validation Error

**Description:** AC-POST-1 / BR-31 — Validation (Negative) — Verify creation is rejected if type is not one of the allowed values.

**Preconditions:**
- API Client is authenticated with correct scope

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send POST request to `/v1/contracts` with `type` set to an invalid string | API returns HTTP 422 Validation Error (or 400 Bad Request) | `type = daily` (valid values: weekly, monthly, one-time) |

**Severity:** major
**Priority:** high

---

### [Riso] POST Contract – Upsert – Existing external_ref_id – Contract updated successfully without duplicate

**Description:** AC-POST-2 — State Transition / CRUD — Verify that POSTing an existing external_ref_id updates the existing record instead of creating a new one.

**Preconditions:**
- API Client is authenticated with correct scope
- Contract exists with `external_ref_id = REF_UPSERT_01`, `slot = 4`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send POST request to `/v1/contracts` with `external_ref_id = REF_UPSERT_01` and `slot = 8` | API returns HTTP 200 OK (or 201 Created indicating upsert success) | `external_ref_id = REF_UPSERT_01`, `slot = 8` |
| 2 | Query the Contract records by `external_ref_id` | Only one record exists. The `slot` field is updated to 8. | "" |
| 3 | Verify audit history of the Contract | Audit history shows the `slot` field changed from 4 to 8 | "" |

**Severity:** critical
**Priority:** high

---

### [Riso] POST Contract – Duplicate – Exact same payload twice – Returns 409 Duplicate Record

**Description:** AC-POST-1 / BR-08 — Data Integrity (Negative) — Verify that sending the exact same POST payload twice is rejected on the second attempt (as per AC-POST-1 contradiction resolved to 409).

**Preconditions:**
- API Client is authenticated with correct scope

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send POST request to `/v1/contracts` with a new `external_ref_id` | API returns HTTP 201 Created | `external_ref_id = REF_DUP_01` |
| 2 | Send the exact same POST request again immediately | API returns HTTP 409 Duplicate Record | `external_ref_id = REF_DUP_01` |
| 3 | Query the Contract records | Only one record was created | "" |

**Severity:** critical
**Priority:** high

---

### [Riso] POST Contract – Bulk Create – Partial success – Returns per-record success and error results

**Description:** AC-POST-6 — CRUD / Decision Table — Verify bulk POST processes each item independently, returning partial success.

**Preconditions:**
- API Client is authenticated with correct scope
- Payload contains 3 contracts:
  - Item 1: Valid new contract
  - Item 2: Invalid contract (missing required field)
  - Item 3: Valid new contract

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send bulk POST request to `/v1/contracts` with the 3 items | API returns HTTP 207 Multi-Status (or 200 OK with detailed body) | Array of 3 contract objects |
| 2 | Inspect the response body | Response indicates Item 1 and Item 3 succeeded, while Item 2 failed with a validation error | "" |
| 3 | Query the Contract records | Contracts for Item 1 and Item 3 are created. Item 2 is not created. | "" |

**Severity:** high
**Priority:** high

---
