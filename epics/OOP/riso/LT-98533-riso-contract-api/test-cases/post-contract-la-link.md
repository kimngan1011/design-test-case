# Test Cases: LT-98533 — Riso | OOP | Contract API (Create/Update via External System)

## Suite: [Riso] POST Contract – LA Linking

### [Riso] POST Contract – LA Link – Valid LA – Contract linked successfully

**Description:** AC-POST-3 — Equivalence Partitioning — Verify contract is linked to LA when a valid lesson_allocation_id is provided and student matches.

**Preconditions:**
- API Client is authenticated with correct scope
- Lesson Allocation exists with `id = LA_001` and `student_id = STUDENT_X`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send POST request to `/v1/contracts` with `student_id = STUDENT_X` and `lesson_allocation_id = LA_001` | API returns HTTP 201 Created | `student_id = STUDENT_X`, `lesson_allocation_id = LA_001` |
| 2 | Query the created Contract record | Contract is created and successfully linked to `LA_001` | "" |

**Severity:** critical
**Priority:** high

---

### [Riso] POST Contract – LA Link – Student mismatch – Returns 422 Validation Error

**Description:** AC-POST-3 — Decision Table (Negative) — Verify creation is rejected if the LA belongs to a different student.

**Preconditions:**
- API Client is authenticated with correct scope
- Lesson Allocation exists with `id = LA_001` and `student_id = STUDENT_Y`
- Student exists with `student_id = STUDENT_X`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send POST request to `/v1/contracts` with `student_id = STUDENT_X` and `lesson_allocation_id = LA_001` | API returns HTTP 422 Validation Error | `student_id = STUDENT_X`, `lesson_allocation_id = LA_001` |
| 2 | Query the Contract records | Contract is NOT created | "" |

**Severity:** major
**Priority:** high

---

### [Riso] POST Contract – Unlinked – lesson_allocation_id absent – Contract created unlinked

**Description:** AC-POST-4 — Equivalence Partitioning — Verify contract is created as unlinked when lesson_allocation_id is not provided.

**Preconditions:**
- API Client is authenticated with correct scope
- Student exists with `student_id = STUDENT_X`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send POST request to `/v1/contracts` with `student_id = STUDENT_X` and omit `lesson_allocation_id` | API returns HTTP 201 Created | `student_id = STUDENT_X` |
| 2 | Query the created Contract record | Contract is created with `lesson_allocation_id` as null | "" |

**Severity:** major
**Priority:** medium

---

### [Riso] POST Contract – LA Link – Non-existent LA – Returns 409 Dependency Missing

**Description:** AC-POST-5 — Negative — Verify creation is rejected if the provided lesson_allocation_id does not exist.

**Preconditions:**
- API Client is authenticated with correct scope
- Student exists with `student_id = STUDENT_X`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send POST request to `/v1/contracts` with `student_id = STUDENT_X` and a non-existent `lesson_allocation_id` | API returns HTTP 409 Dependency Missing | `student_id = STUDENT_X`, `lesson_allocation_id = INVALID_LA_999` |
| 2 | Query the Contract records | Contract is NOT created | "" |

**Severity:** critical
**Priority:** high

---
