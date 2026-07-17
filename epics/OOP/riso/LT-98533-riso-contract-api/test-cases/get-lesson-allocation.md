# Test Cases: LT-98533 — Riso | OOP | Contract API (Create/Update via External System)

## Suite: [Riso] GET Lesson Allocation API

### [Riso] GET Lesson Allocation – Required Params – Valid location and academic year – Returns matching LAs

**Description:** AC-GET-1 — Equivalence Partitioning — Verify successful retrieval when both mandatory parameters are provided.

**Preconditions:**
- API Client is authenticated with correct scope
- At least one Lesson Allocation exists in the system with `location_id = LOC123`, `academic_year = 2025`, `require_allocation = true`, and status is active

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send GET request to `/v1/lesson-allocations` with parameters `location_id` and `academic_year` | API returns HTTP 200 OK with a list of Lesson Allocations matching the parameters | `location_id = LOC123`, `academic_year = 2025` |
| 2 | Inspect the response body | Response contains the expected Lesson Allocations with required fields | "" |

**Severity:** major
**Priority:** high

---

### [Riso] GET Lesson Allocation – Required Params – Missing location – Returns 400 Bad Request

**Description:** AC-GET-1 — Negative — Verify request fails when mandatory location_id is missing.

**Preconditions:**
- API Client is authenticated with correct scope

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send GET request to `/v1/lesson-allocations` with parameter `academic_year` only | API returns HTTP 400 Bad Request (or 422 Validation Error) | `academic_year = 2025` |

**Severity:** major
**Priority:** high

---

### [Riso] GET Lesson Allocation – Required Params – Missing academic year – Returns 400 Bad Request

**Description:** AC-GET-1 — Negative — Verify request fails when mandatory academic_year is missing.

**Preconditions:**
- API Client is authenticated with correct scope

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send GET request to `/v1/lesson-allocations` with parameter `location_id` only | API returns HTTP 400 Bad Request (or 422 Validation Error) | `location_id = LOC123` |

**Severity:** major
**Priority:** high

---

### [Riso] GET Lesson Allocation – Course Filter – Valid course_offering_id – Returns only matching LAs

**Description:** AC-GET-2 — Decision Table — Verify filtering by course_offering_id returns correct subset of LAs.

**Preconditions:**
- API Client is authenticated with correct scope
- Multiple Lesson Allocations exist for `location_id = LOC123`, `academic_year = 2025`
- Some LAs belong to `course_offering_id = COURSE999`, others belong to `course_offering_id = COURSE888`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send GET request to `/v1/lesson-allocations` including parameters `location_id`, `academic_year`, and `course_offering_id` | API returns HTTP 200 OK | `location_id = LOC123`, `academic_year = 2025`, `course_offering_id = COURSE999` |
| 2 | Inspect the returned LAs | All returned LAs have the specified course_offering_id. LAs with other course offering IDs are not returned. | `course_offering_id = COURSE999` |

**Severity:** minor
**Priority:** medium

---

### [Riso] GET Lesson Allocation – Incremental Pull – Valid last_modified_since – Returns recently modified LAs

**Description:** AC-GET-3 — Decision Table — Verify incremental pull filters LAs by last_modified_since timestamp.

**Preconditions:**
- API Client is authenticated with correct scope
- LAs exist for the target location and academic year
- `today = 2026-06-19T00:00:00Z`
- LA-A was modified at `2026-06-18T10:00:00Z`
- LA-B was modified at `2026-06-19T05:00:00Z`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send GET request to `/v1/lesson-allocations` including parameters `location_id`, `academic_year`, and `last_modified_since` | API returns HTTP 200 OK | `location_id = LOC123`, `academic_year = 2025`, `last_modified_since = 2026-06-19T00:00:00Z` (today) |
| 2 | Inspect the returned LAs | Only LA-B is returned. LA-A is excluded. | `last_modified_since = 2026-06-19T00:00:00Z` |

**Severity:** minor
**Priority:** medium

---

### [Riso] GET Lesson Allocation – Exclusion Rules – Require Allocation is false – LA is excluded from response

**Description:** AC-GET-4 — Decision Table / Negative — Verify LAs with Require Allocation = false are implicitly excluded.

**Preconditions:**
- API Client is authenticated with correct scope
- LA-C exists with `location_id = LOC123`, `academic_year = 2025`, status active, but `require_allocation = false`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send GET request to `/v1/lesson-allocations` with valid `location_id` and `academic_year` | API returns HTTP 200 OK | `location_id = LOC123`, `academic_year = 2025` |
| 2 | Inspect the returned LAs | LA-C is NOT present in the response | "" |

**Severity:** major
**Priority:** high

---

### [Riso] GET Lesson Allocation – Exclusion Rules – LA status is deleted or archived – LA is excluded from response

**Description:** AC-GET-4 — Decision Table / Negative — Verify deleted or archived LAs are implicitly excluded.

**Preconditions:**
- API Client is authenticated with correct scope
- LA-D exists with `location_id = LOC123`, `academic_year = 2025`, `require_allocation = true`, but status is `deleted`
- LA-E exists with same params but status is `archived`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send GET request to `/v1/lesson-allocations` with valid `location_id` and `academic_year` | API returns HTTP 200 OK | `location_id = LOC123`, `academic_year = 2025` |
| 2 | Inspect the returned LAs | LA-D and LA-E are NOT present in the response | "" |

**Severity:** major
**Priority:** high

---

### [Riso] GET Lesson Allocation – Pagination – Results exceed page size – Returns next_pointer and correct page size

**Description:** AC-GET-5 — Boundary Value Analysis — Verify cursor pagination works when total results exceed default/requested page size.

**Preconditions:**
- API Client is authenticated with correct scope
- The system has 105 active, eligible LAs for `location_id = LOC123`, `academic_year = 2025`
- API has a default page size limit of 100

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send GET request to `/v1/lesson-allocations` with valid `location_id` and `academic_year` | API returns HTTP 200 OK | `location_id = LOC123`, `academic_year = 2025` |
| 2 | Inspect the response body | Response contains exactly 100 LAs and a `next_pointer` cursor string | "" |
| 3 | Send a second GET request including the `next_pointer` | API returns HTTP 200 OK | `location_id = LOC123`, `academic_year = 2025`, `pointer = <next_pointer>` |
| 4 | Inspect the second response | Response contains the remaining 5 LAs | "" |

**Severity:** minor
**Priority:** medium

---
