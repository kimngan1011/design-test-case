# Test Cases: LT-98533 — Riso | OOP | Contract API (Create/Update via External System)

## Suite: [Riso] Scope Isolation (NFR-04)

### [Riso] Contract API – Scope Isolation – GET returns only Riso tenant LAs

**Description:** NFR-04 — Permission Matrix — Verify that a client authenticated for the Riso tenant cannot retrieve Lesson Allocations belonging to other tenants.

**Preconditions:**
- API Client is authenticated with Riso tenant scope
- `LA_RISO` exists in the Riso tenant
- `LA_OTHER` exists in a different tenant (e.g., Nichibei) but shares the same `location_id` and `academic_year`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send GET request to `/v1/lesson-allocations` with valid `location_id` and `academic_year` | API returns HTTP 200 OK | Valid query params for the shared location/academic year |
| 2 | Inspect the returned LAs | Only `LA_RISO` is returned. `LA_OTHER` is strictly excluded. | "" |

**Severity:** critical
**Priority:** high

---

### [Riso] Contract API – Scope Isolation – POST/PATCH across tenant boundary – Returns 403 or 404

**Description:** NFR-04 — Negative — Verify that a client authenticated for the Riso tenant cannot create or update contracts for students/LAs in other tenants.

**Preconditions:**
- API Client is authenticated with Riso tenant scope
- `STUDENT_OTHER` exists only in a different tenant
- `LA_OTHER` exists only in a different tenant

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send POST request to `/v1/contracts` with `student_id = STUDENT_OTHER` | API returns HTTP 403 Forbidden or 404 Not Found (does not create contract) | `student_id = STUDENT_OTHER` |
| 2 | Send POST request to `/v1/contracts` linked to `lesson_allocation_id = LA_OTHER` | API returns HTTP 403 Forbidden or 404 Not Found | `lesson_allocation_id = LA_OTHER` |
| 3 | Send PATCH request to a known `external_ref_id` belonging to another tenant | API returns HTTP 404 Not Found | External Ref ID of other tenant contract |

**Severity:** critical
**Priority:** high

---
