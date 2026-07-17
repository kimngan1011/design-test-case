# Test Cases: LT-98533 — Riso | OOP | Contract API (Create/Update via External System)

## Suite: [Riso] Contract API – Error Paths

### [Riso] Contract API – Type Validation – Start date wrong format – Returns 422

**Description:** NFR-06 — Negative — Verify validation error when start_date format is incorrect.

**Preconditions:**
- API Client is authenticated with correct scope

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send POST request to `/v1/contracts` with `start_date` in `DD-MM-YYYY` format instead of `YYYY-MM-DD` | API returns HTTP 422 Validation Error | `start_date = 15-06-2026` |

**Severity:** major
**Priority:** high

---

### [Riso] Contract API – Type Validation – Total is not integer – Returns 422

**Description:** NFR-06 — Negative — Verify validation error when numeric field receives incorrect type.

**Preconditions:**
- API Client is authenticated with correct scope

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send POST request to `/v1/contracts` with `total` as a string or float | API returns HTTP 422 Validation Error | `total = "ten"` or `10.5` |

**Severity:** major
**Priority:** high

---

### [Riso] Contract API – Authentication – Invalid token – Returns 401 Unauthorized

**Description:** NFR — Negative — Verify endpoints are protected against invalid authentication.

**Preconditions:**
- API Client has an expired or malformed token

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send GET request to `/v1/lesson-allocations` | API returns HTTP 401 Unauthorized | Invalid Bearer token |
| 2 | Send POST request to `/v1/contracts` | API returns HTTP 401 Unauthorized | Invalid Bearer token |

**Severity:** critical
**Priority:** high

---

### [Riso] Contract API – Authentication – Missing required scope – Returns 403 Forbidden

**Description:** NFR — Negative — Verify endpoints enforce correct OAuth scope.

**Preconditions:**
- API Client is authenticated but lacks the specific scope required for writing contracts

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send POST request to `/v1/contracts` with valid payload | API returns HTTP 403 Forbidden | Valid payload, insufficient scope token |

**Severity:** critical
**Priority:** high

---
