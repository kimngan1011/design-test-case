# Test Cases: LT-98533 — Riso | OOP | Contract API (Create/Update via External System)

## Suite: [Riso] LA Aggregation – PATCH Events (C2b, C2c, V3, Unlinked→Linked)

### [Riso] LA Aggregation – PATCH Re-link (C2b/C2c) – Old LA recalculates correctly

**Description:** AC-PATCH-3 — Decision Table — Verify old LA recalculates all 3 aggregation fields when a contract is re-linked away from it.

**Preconditions:**
- API Client is authenticated with correct scope
- Old Lesson Allocation `LA_OLD` has `Total_Session_Count = 20`, `Start_Date = 2026-06-01`, `End_Date = 2026-06-30`
- Contract A (active) is linked to `LA_OLD` (`slot = 10`, `start_date = 2026-06-15`, `end_date = 2026-06-30`)
- Contract B (active) is also linked to `LA_OLD` (`slot = 10`, `start_date = 2026-06-01`, `end_date = 2026-06-15`)
- New Lesson Allocation `LA_NEW` exists

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send PATCH request to update Contract A with `lesson_allocation_id = LA_NEW` | API returns HTTP 200 OK | `external_ref_id = REF_RELINK_01`, `lesson_allocation_id = LA_NEW` |
| 2 | Query the `LA_OLD` record | `LA_OLD` is synchronously updated based only on remaining Contract B | "" |
| 3 | Verify `Total_Session_Count` on `LA_OLD` | `Total_Session_Count` = 10 (Contract B only) | "" |
| 4 | Verify `Start_Date` on `LA_OLD` | `Start_Date` = 2026-06-01 (from Contract B) | "" |
| 5 | Verify `End_Date` on `LA_OLD` | `End_Date` = 2026-06-15 (from Contract B) | "" |

**Severity:** critical
**Priority:** high

---

### [Riso] LA Aggregation – PATCH Re-link (C2b/C2c) – New LA recalculates correctly

**Description:** AC-PATCH-3 — Decision Table — Verify new LA recalculates all 3 aggregation fields when a contract is re-linked to it.

**Preconditions:**
- API Client is authenticated with correct scope
- Contract C is currently linked to `LA_OLD` (`slot = 5`, `start_date = 2026-07-01`, `end_date = 2026-07-31`)
- New Lesson Allocation `LA_NEW` exists with `Total_Session_Count = 5`, `Start_Date = 2026-08-01`, `End_Date = 2026-08-31`
- Contract D (active) is linked to `LA_NEW` (`slot = 5`, `start_date = 2026-08-01`, `end_date = 2026-08-31`)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send PATCH request to update Contract C with `lesson_allocation_id = LA_NEW` | API returns HTTP 200 OK | `external_ref_id = REF_RELINK_02`, `lesson_allocation_id = LA_NEW` |
| 2 | Query the `LA_NEW` record | `LA_NEW` is synchronously updated based on Contracts C and D | "" |
| 3 | Verify `Total_Session_Count` on `LA_NEW` | `Total_Session_Count` = 10 (Contract C 5 + Contract D 5) | "" |
| 4 | Verify `Start_Date` on `LA_NEW` | `Start_Date` = 2026-07-01 (earliest of C and D) | "" |
| 5 | Verify `End_Date` on `LA_NEW` | `End_Date` = 2026-08-31 (latest of C and D) | "" |

**Severity:** critical
**Priority:** high

---

### [Riso] LA Aggregation – PATCH Re-link – Unlinked to Linked – New LA recalculates correctly

**Description:** AC-PATCH-3 — State Transition — Verify linking a previously unlinked contract triggers recalculation on the target LA.

**Preconditions:**
- API Client is authenticated with correct scope
- Contract E exists unlinked (`lesson_allocation_id` is null) with `slot = 8`, `start_date = 2026-09-01`, `end_date = 2026-09-30`
- Target Lesson Allocation `LA_TARGET` exists with `Total_Session_Count = 10`, `Start_Date = 2026-10-01`, `End_Date = 2026-10-31`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send PATCH request to update Contract E with `lesson_allocation_id = LA_TARGET` | API returns HTTP 200 OK | `external_ref_id = REF_RELINK_03`, `lesson_allocation_id = LA_TARGET` |
| 2 | Query the `LA_TARGET` record | `LA_TARGET` is synchronously updated | "" |
| 3 | Verify `Total_Session_Count` on `LA_TARGET` | `Total_Session_Count` = 18 (10 + 8) | "" |
| 4 | Verify `Start_Date` on `LA_TARGET` | `Start_Date` = 2026-09-01 | "" |
| 5 | Verify `End_Date` on `LA_TARGET` | `End_Date` = 2026-10-31 | "" |

**Severity:** critical
**Priority:** high

---

### [Riso] LA Aggregation – PATCH Field Update (V3) – end_date updated – Recalculates End_Date only

**Description:** AC-PATCH-2 — CRUD / Decision Table — Verify updating end_date via PATCH recalculates LA End_Date but leaves Total_Session_Count unaffected.

**Preconditions:**
- API Client is authenticated with correct scope
- Contract F is linked to `LA_UPDATE` with `end_date = 2026-11-15`, `slot = 10`
- `LA_UPDATE` has `End_Date = 2026-11-15`, `Total_Session_Count = 10`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send PATCH request to update Contract F with `end_date = 2026-11-30` | API returns HTTP 200 OK | `external_ref_id = REF_PATCH_01`, `end_date = 2026-11-30` |
| 2 | Query the `LA_UPDATE` record | `LA_UPDATE` is synchronously updated | "" |
| 3 | Verify `End_Date` on `LA_UPDATE` | `End_Date` = 2026-11-30 | "" |
| 4 | Verify `Total_Session_Count` on `LA_UPDATE` | `Total_Session_Count` remains 10 | "" |

**Severity:** major
**Priority:** high

---

### [Riso] LA Aggregation – PATCH Field Update (V3) – slot updated – Recalculates Total_Session_Count

**Description:** AC-PATCH-2 — CRUD — Verify updating slot via PATCH recalculates LA Total_Session_Count.

**Preconditions:**
- API Client is authenticated with correct scope
- Contract G is linked to `LA_UPDATE_2` with `slot = 5`, `start_date = 2026-12-01`
- `LA_UPDATE_2` has `Total_Session_Count = 5`, `Start_Date = 2026-12-01`

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send PATCH request to update Contract G with `slot = 15` | API returns HTTP 200 OK | `external_ref_id = REF_PATCH_02`, `slot = 15` |
| 2 | Query the `LA_UPDATE_2` record | `LA_UPDATE_2` is synchronously updated | "" |
| 3 | Verify `Total_Session_Count` on `LA_UPDATE_2` | `Total_Session_Count` = 15 | "" |
| 4 | Verify `Start_Date` on `LA_UPDATE_2` | `Start_Date` remains 2026-12-01 | "" |

**Severity:** major
**Priority:** high

---
