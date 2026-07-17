# Test Coverage: LT-98533 — Riso | OOP | Contract API (Create/Update via External System)

**Jira:** https://manabie.atlassian.net/browse/LT-98533  
**Date:** 2026-06-19

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|------|---|
| BR-01 | AC-GET-1 | GET LA requires location_id and academic_year as mandatory parameters |
| BR-02 | AC-GET-2 | course_offering_id is optional filter; when provided, only matching LAs returned |
| BR-03 | AC-GET-3 | last_modified_since enables incremental pull |
| BR-04 | AC-GET-4 | LAs with Require Allocation = false excluded from GET LA response |
| BR-05 | AC-GET-4 | Deleted/archived LAs excluded from GET LA response |
| BR-06 | AC-GET-5 | Cursor-based pagination; next_pointer returned when results exceed page size |
| BR-07 | AC-POST-1 | POST with new external_ref_id creates new Contract; external_ref_id must be unique |
| BR-08 | AC-POST-1 | Duplicate POST with same external_ref_id rejected with 409 DUPLICATE_RECORD |
| BR-09 | AC-POST-2 | POST with existing external_ref_id upserts (updates) existing Contract |
| BR-10 | AC-POST-3 | When lesson_allocation_id provided: Contract linked to LA; student existence validated |
| BR-11 | AC-POST-4 | When lesson_allocation_id absent: Contract created unlinked; no LA aggregation triggered |
| BR-12 | AC-POST-5 | Non-existent lesson_allocation_id → 409 DEPENDENCY_MISSING; no record created |
| BR-13 | AC-POST-6 | Bulk POST: partial success mode — per-record results returned |
| BR-14 | AC-POST-7 | New Contract linked to LA → recalculate LA.Total_Session_Count, LA.Start_Date, LA.End_Date |
| BR-15 | AC-POST-8 | Updating Contract slot/total via POST upsert → recalculate LA.Total_Session_Count |
| BR-16 | AC-PATCH-1 | PATCH allows: end_date, lesson_allocation_id, slot, total. Immutable: external_ref_id, student_id, acad_year_id |
| BR-17 | AC-PATCH-2 | PATCH end_date update → LA.End_Date recalculates; LA.Total_Session_Count unchanged unless total changed |
| BR-18 | AC-PATCH-3 | PATCH re-link (LA change) → both old and new LA recalculate all 3 aggregation fields |
| BR-19 | AC-PATCH-4 | PATCH with non-existent external_ref_id → 404 NOT_FOUND |
| BR-20 | AC-DEL-1 | PATCH contract_status = Deleted → logical delete; record NOT physically removed |
| BR-21 | AC-DEL-2 | After logical delete: record in system, deleted_at populated |
| BR-22 | AC-DEL-3 | Linked Contract deleted → recalculate all 3 LA aggregation fields. No negative aggregation. |
| BR-23 | AC-DEL-4 | Unlinked Contract deleted → marked Deleted; no aggregation recalculation |
| BR-24 | AC-DEL-5 | One of multiple contracts on LA deleted → remaining Active Contracts unaffected |
| BR-25 | AC-DEL-6 | Logical delete is idempotent |
| BR-26 | AC-POST-7 | LA.Total_Session_Count = SUM(contract.total) for all Active contracts |
| BR-27 | AC-POST-7 | LA.Start_Date = Earliest start_date among all Active contracts |
| BR-28 | AC-POST-7 | LA.End_Date = Latest end_date among all Active contracts |
| BR-29 | AC-DEL-3 | When LAST Active contract deleted: LA.Total_Session_Count = 0; LA.Start_Date and LA.End_Date retain last known values |
| BR-30 | AC-POST-1 | Contract required fields on POST: 11 fields listed in spec |
| BR-31 | AC-POST-1 | Contract.type: weekly / monthly / one-time — immutable after creation |
| BR-32 | AC-POST-1 | Contract.end_date optional on POST; must be ≥ start_date when provided |
| BR-33 | AC-DEL-1 | contract_status: active (default) / deleted. No 'ended'. No DELETE HTTP endpoint. |
| BR-34 | AC-POST-1 | Riso OOP only — no feature flag; scope isolated from core LA and non-Riso partners |

---

## 2. Logic Type Categorization

| AC | Business Rule(s) | Logic Type |
|---|---|---|
| AC-GET-1 | BR-01 | Validation logic |
| AC-GET-2 | BR-02 | Conditional logic |
| AC-GET-3 | BR-03 | Conditional logic |
| AC-GET-4 | BR-04, BR-05 | Conditional logic, Data integrity |
| AC-GET-5 | BR-06 | Boundary/range logic |
| AC-POST-1 | BR-07, BR-08, BR-30, BR-31, BR-32 | Validation logic, Data integrity |
| AC-POST-2 | BR-09 | State transition, Data integrity |
| AC-POST-3 | BR-10 | Conditional logic, Data integrity |
| AC-POST-4 | BR-11 | Conditional logic |
| AC-POST-5 | BR-12 | Validation logic |
| AC-POST-6 | BR-13 | Data integrity |
| AC-POST-7 | BR-14, BR-26, BR-27, BR-28 | Downstream effects (Data integrity, Cross-system) |
| AC-POST-8 | BR-15 | Downstream effects (Data integrity) |
| AC-PATCH-1 | BR-16 | Validation logic, Data integrity |
| AC-PATCH-2 | BR-17 | Downstream effects (Conditional logic) |
| AC-PATCH-3 | BR-18 | Downstream effects (Data integrity, Cross-system) |
| AC-PATCH-4 | BR-19 | Validation logic |
| AC-DEL-1 | BR-20, BR-33 | State transition, Validation logic |
| AC-DEL-2 | BR-21 | Data integrity |
| AC-DEL-3 | BR-22, BR-29 | Downstream effects (Data integrity) |
| AC-DEL-4 | BR-23 | Conditional logic |
| AC-DEL-5 | BR-24 | Data integrity |
| AC-DEL-6 | BR-25 | Data integrity |
| NFR-04 | BR-34 | Permission logic (scope isolation) |
| Aggregation formulas | BR-26, BR-27, BR-28, BR-29 | Boundary/range logic, Data integrity |
| Immutable fields | BR-31 (type) + BR-16 (external_ref_id, student_id, acad_year_id) | Validation logic |

---

## 3. Test Technique Selection

| Logic Type | Primary Technique | Secondary Technique |
|---|---|---|
| Validation logic | Equivalence Partitioning | Negative |
| Boundary/range logic | Boundary Value Analysis | Negative |
| Conditional logic | Decision Table | Negative |
| State transition | State Transition | CRUD |
| Data integrity | CRUD | Regression, Decision Table |
| Downstream effects | CRUD | Regression |
| Cross-system impact | Regression | CRUD |
| Permission logic | Permission Matrix | Decision Table |

---

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC-GET-1 | GET LA — required params (location_id, academic_year) | Validation | Equivalence Partitioning + Negative | High | Standard |
| AC-GET-2 | GET LA — optional course_offering_id filter | Conditional | Decision Table | Medium | Standard |
| AC-GET-3 | GET LA — incremental pull via last_modified_since | Conditional | Decision Table | Medium | Standard |
| AC-GET-4 | GET LA — exclude Require Allocation=false + deleted/archived LAs | Conditional + Data integrity | Decision Table + Negative | High | Deep |
| AC-GET-5 | GET LA — cursor pagination; next_pointer returned when page exceeded | Boundary/range | BVA | Medium | Standard |
| AC-POST-1 (create) | POST — new contract created; required fields; type values; end_date ≥ start_date | Validation + Data integrity | Equivalence Partitioning + Negative + BVA | Critical | Deep |
| AC-POST-1 (duplicate) | POST — duplicate external_ref_id → 409 DUPLICATE_RECORD | Data integrity | CRUD + Negative | Critical | Deep |
| AC-POST-2 | POST — upsert on existing external_ref_id; no duplicate; previous values auditable | State transition + Data integrity | State Transition + CRUD | Critical | Deep |
| AC-POST-3 | POST — valid lesson_allocation_id links Contract to LA; student validated | Conditional + Data integrity | Decision Table + Negative | Critical | Deep |
| AC-POST-4 | POST — absent lesson_allocation_id; Contract created unlinked; no aggregation | Conditional | Decision Table | High | Standard |
| AC-POST-5 | POST — non-existent lesson_allocation_id → 409 DEPENDENCY_MISSING | Validation | Negative | High | Standard |
| AC-POST-6 | POST bulk — partial success; per-record result; one invalid does not block others | Data integrity | CRUD + Decision Table | High | Deep |
| AC-POST-7 (Case C1) | POST creates contract linked to LA → Total_Session_Count, Start_Date, End_Date recalculate | Downstream effects | CRUD + Regression | Critical | Deep |
| AC-POST-8 (Case C2a) | POST upsert changes slot/total → Total_Session_Count recalculates | Downstream effects | CRUD | Critical | Deep |
| AC-PATCH-1 (allowed) | PATCH — updatable fields updated; immutable fields rejected | Validation | Equivalence Partitioning + Negative | High | Deep |
| AC-PATCH-2 (Case C2b) | PATCH end_date → LA.End_Date recalculates; Total_Session_Count unchanged | Downstream effects + Conditional | Decision Table + CRUD | Critical | Deep |
| AC-PATCH-3 (Case C2c) | PATCH re-link LA → old LA and new LA both recalculate all 3 aggregation fields | Downstream effects + Cross-system | CRUD + Regression | Critical | Deep |
| AC-PATCH-4 | PATCH non-existent external_ref_id → 404 NOT_FOUND; no record created | Validation | Negative | High | Standard |
| AC-DEL-1 | PATCH contract_status = Deleted → logical delete; record retained | State transition | State Transition + Negative | Critical | Deep |
| AC-DEL-2 | Logical delete preserves record; deleted_at populated; auditable | Data integrity | CRUD | High | Standard |
| AC-DEL-3 (Case V1/D1) | Linked contract deleted → all 3 LA aggregation fields recalculate | Downstream effects | CRUD + Regression | Critical | Deep |
| AC-DEL-3 (Case Last Active) | Last Active contract deleted → Total_Session_Count = 0; Start_Date and End_Date retain | Downstream effects + Boundary | BVA + CRUD | Critical | Deep |
| AC-DEL-4 | Unlinked contract deleted → no aggregation triggered | Conditional | Decision Table | Medium | Standard |
| AC-DEL-5 | One of multiple contracts deleted → remaining unaffected; aggregation correct | Data integrity | CRUD + Regression | Critical | Deep |
| AC-DEL-6 | Logical delete idempotent | Data integrity | CRUD | High | Standard |
| NFR-02 | Aggregation always consistent; no stale values after any event; race-condition safe | Cross-system + Data integrity | Regression | Critical | Deep |
| NFR-03 | Auditability: field change history retained; API events timestamped | Data integrity | CRUD | High | Standard |
| NFR-04 | Scope isolation: Riso API does not affect non-Riso LA records | Permission (scope) | Permission Matrix + Regression | High | Standard |
| NFR-05 | POST/PATCH idempotent on external_ref_id | Data integrity | CRUD | High | Standard |
| Case V3 | PATCH end_date earlier (status stays active) → only End_Date recalculates | Conditional + Downstream | Decision Table | High | Standard |
| Unlinked → Linked | PATCH adds LA to unlinked contract → new LA aggregation recalculates | Downstream effects | CRUD | High | Standard |
| Error paths | HTTP 400 (malformed body), 401 (unauthorized), 403 (forbidden), 422 (validation error) | Validation | Negative | Medium | Standard |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| LA aggregation correctness (C1, C2a, C2b, C2c, V1/D1, Last Active, V3) | Incorrect aggregation corrupts LA.Total_Session_Count which SF users and reports depend on. Silent failure — no visible error to user. Stale aggregation = data corruption (NFR-02). | Test every row in the Case Matrix independently. Verify DB state immediately after each event. Include race-condition test (concurrent batch for same LA). |
| POST create/upsert correctness + no duplicate | Creating a duplicate Contract record would double-count Total_Session_Count — direct data corruption. | BVA on external_ref_id: new ID, existing ID (upsert), same payload twice, partial payload update. |
| PATCH re-link (C2c) — both LAs updated | If old LA is not recalculated on re-link, its Total_Session_Count remains inflated permanently. No visible error. | Test: verify old LA decrements AND new LA increments — both, simultaneously. |
| PATCH logical delete — No physical DELETE endpoint | If dev adds a DELETE endpoint later, existing behavior may shift. Currently deletion is PATCH only — must test that raw DELETE verb returns 4xx. | Test DEL verb → 404 or 405. Verify record NOT removed physically. |
| Last Active contract deleted | LA.Total_Session_Count must go to 0; Start_Date and End_Date must retain — not null out. Confirmed behavior must match implementation. | Explicit assertion: TSC = 0, Start_Date = prior value, End_Date = prior value. |
| Scope isolation (NFR-04) | Aggregation on Riso Contract must NOT modify LA records of other partner students (e.g., Nichibei, Aso). Silently breaks other partners if not isolated. | Create test data for non-Riso LA; perform Contract API events on Riso data; assert non-Riso LA is unchanged. |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| GET LA exclusion rules (AC-GET-4) | Riso's nightly batch uses GET LA to identify valid LA IDs before POSTing contracts. Wrong LA IDs returned = contracts linked to wrong LAs. | Test with: Require Allocation = false LA present, deleted LA present, archived LA present — all must be absent from response. |
| POST bulk partial success (AC-POST-6) | One bad item in a batch of 20,000 could silently skip valid records or incorrectly block the whole batch. | Test: valid + invalid items in same batch; assert valid ones succeed, invalid ones return per-record error. |
| PATCH immutable fields rejected (AC-PATCH-1) | If immutable fields (external_ref_id, student_id, acad_year_id) are accidentally accepted, contract data is corrupted. | Test PATCH with each immutable field included — expect 422 or 400. |
| Idempotency (NFR-05, AC-DEL-6) | Nightly batch may retry on failure. Double-send must not double-create or double-aggregate. | Send same POST twice; same PATCH twice; same DELETE twice — verify consistent state each time. |
| Aggregation trigger completeness (5 event types) | Per Nichibei SPO incident: OOP aggregation paths can be missing for some event types. Missing trigger = stale LA forever. | Run the full 5-event-type matrix sequentially on the same LA. Verify aggregation after each. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| GET LA pagination (AC-GET-5) | Riso batch may miss contracts if pagination is broken and next_pointer is not returned. | Test with N LAs where N > page size; navigate all pages; assert all LAs seen. |
| HTTP error paths (400, 401, 403, 422) | Missing auth validation could allow unauthorized contract submissions. | Test each error code: missing token (401), wrong scope (403), malformed body (400), invalid field value (422). |
| Unlinked contract → Linked (PATCH add LA) | If adding LA to previously unlinked contract does not trigger aggregation, LA remains out of sync. | Test: create unlinked contract; PATCH with LA ID; verify new LA aggregation updated. |
| V3: retroactive end_date change (status stays active) | PATCH end_date earlier does not change TSC — but if it was the latest end_date, LA.End_Date must recalculate. | Test with 2 contracts on same LA; contract 2 was the latest; PATCH contract 2 end_date earlier; verify LA.End_Date = contract 1 end_date. |

---

## 6. Downstream Effects Inventory

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Row |
|---|---|---|---|
| POST — new Contract linked to LA (C1) | LA.Total_Session_Count = SUM of all active contract.total | LA record (SF API + SF UI) | TC-POST-AGG-01 |
| POST — new Contract linked to LA (C1) | LA.Start_Date = earliest start_date of active contracts | LA record (SF API + SF UI) | TC-POST-AGG-02 |
| POST — new Contract linked to LA (C1) | LA.End_Date = latest end_date of active contracts | LA record (SF API + SF UI) | TC-POST-AGG-03 |
| POST — upsert changes total (C2a) | LA.Total_Session_Count recalculates; Start_Date and End_Date unchanged | LA record | TC-POST-AGG-04 |
| PATCH end_date (C2b) | LA.End_Date recalculates; LA.Total_Session_Count unchanged | LA record | TC-PATCH-AGG-01 |
| PATCH re-link (C2c) | Old LA: removes contract from aggregation | Old LA record | TC-PATCH-RELINK-01 |
| PATCH re-link (C2c) | New LA: adds contract to aggregation | New LA record | TC-PATCH-RELINK-02 |
| PATCH logical delete (V1/D1) | LA.Total_Session_Count decrements by deleted contract.total | LA record | TC-DEL-AGG-01 |
| PATCH logical delete (V1/D1) | LA.Start_Date recalculates to next earliest | LA record | TC-DEL-AGG-02 |
| PATCH logical delete (V1/D1) | LA.End_Date recalculates to next latest | LA record | TC-DEL-AGG-03 |
| PATCH logical delete — last Active (Last Active) | LA.Total_Session_Count = 0 | LA record | TC-DEL-LAST-01 |
| PATCH logical delete — last Active (Last Active) | LA.Start_Date retains prior value | LA record | TC-DEL-LAST-02 |
| PATCH logical delete — last Active (Last Active) | LA.End_Date retains prior value | LA record | TC-DEL-LAST-03 |
| PATCH logical delete — unlinked (D4) | No LA aggregation change | No LA record touched | TC-DEL-UNLINKED-01 |
| POST create on Riso data | Non-Riso LA records unchanged | Other partner LA records | TC-SCOPE-ISOLATION-01 |
| POST Contract (any event) | deleted_at, created_at, updated_at fields set correctly | Contract record | TC-AUDIT-01 |
| Concurrent batch (NFR-02) | All N simultaneous records processed; aggregation consistent | LA record after batch | TC-CONCURRENCY-01 |

---

## 7. Edge-Case Patterns Checklist (Step 4.5)

**A. Configuration-driven thresholds** — N/A. No config/feature-flag drives behavior. Riso OOP, no flag.

**B. Date / time logic** — YES for start_date/end_date:
- [x] `end_date` must be ≥ `start_date` → BVA: end = start (valid), end = start−1 day (invalid)
- [x] `start_date` in the past — allowed (batch processes historical contracts)
- [x] `end_date` omitted (open-ended) — valid on POST
- [x] Two contracts on same LA with different start/end dates — earliest/latest calculation
- [ ] TZ gap — DST: JST does not observe DST → N/A. All timestamps UTC (ISO 8601) per API PRD.

**C. Concurrent / stale state** — YES:
- [x] Concurrent batch submission of ~20,000 contracts; same LA referenced by multiple records in same batch → aggregation race condition risk (NFR-02, NFR-06)
- [x] Same contract POST submitted twice (retry scenario) → idempotency

**D. Permission & role** — YES (limited):
- [x] Riso integration user (API): full create/update/delete contract access
- [x] Non-Riso API caller: must not have access (401/403)
- [x] SF HQ/CM user: read-only via UI (cannot call Contract API directly)
- [x] Cross-scope isolation: Riso contract API must not affect non-Riso LA data

**E. State transition** — YES:
- [x] `active` → `deleted` (via PATCH): valid, tested
- [x] `deleted` → `active` (reversal): not currently expected; test as blocked (negative)
- [x] `active` → `active` (same status re-sent): idempotent (AC-DEL-6 logic applies)

**F. Cross-system / cross-surface** — YES:
- [x] Contract API event → LA fields updated on SF API
- [x] LA fields updated on SF API → visible on SF Contact → Course tab (if SF UI in scope — see open Q-02 re: SF UI)
- [x] Scope isolation: Riso Contract event must NOT appear in non-Riso partner's LA data

**G. Downstream effects** — YES (filled above in Downstream Effects Inventory — 17 downstream TC rows).

**H. Display completeness** — Limited scope. The Contract API is primarily API-only (no dedicated Contract UI in this ticket — Epic 3 / PBT-1510 handles Contract UI). However, the updated LA fields (Total_Session_Count, Start_Date, End_Date) are visible in the SF Contact → Course tab:

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| SF Contact → Course tab (LA record) | Total_Session_Count (new), Start_Date (updated), End_Date (updated), Purchased_Slot (manual, unchanged) | — | — | Field label: "Total Session Count" (MANAERP__Total_Session_Count__c) |

> ⚠️ Open Q-02 (in Clarification Questions): SF users' view of updated fields is not confirmed by any AC. Test cases for SF UI fields are drafted but marked **conditional on Q-02 answer**.

**H.1 Spec–Figma mismatch** — N/A. No Figma URL in spec.

---

## 8. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| AC-GET-1 through AC-GET-5 (GET LA API) | None found | None | ✅ Full new coverage required |
| AC-POST-1 create (Contract POST create) | None | None | ✅ Full new coverage required |
| AC-POST-2 upsert | None | None | ✅ Full new coverage required |
| AC-POST-3 LA link | None | None | ✅ Full new coverage required |
| AC-POST-4 unlinked create | None | None | ✅ Full new coverage required |
| AC-POST-5 DEPENDENCY_MISSING | None | None | ✅ Full new coverage required |
| AC-POST-6 bulk / partial success | None | None | ✅ Full new coverage required |
| AC-POST-7 aggregation (Total_Session_Count) | `LT-92532/test-cases/la-auto-calculation.md` (6 TCs for Purchased_Slot) | Partial — tests same trigger event types but asserts **Purchased_Slot** not **Total_Session_Count** | ✅ New TCs for Total_Session_Count. Old TCs for Purchased_Slot: mark as pending [CONFLICT Q-01] resolution |
| AC-POST-8 upsert slot/total + aggregation | `LT-92532/test-cases/la-auto-calculation.md` (1 TC — slot update) | Partial — tests slot change on Purchased_Slot | ✅ New TC for total change → Total_Session_Count recalc |
| AC-PATCH-1 through AC-PATCH-4 | None | None | ✅ Full new coverage required |
| AC-DEL-1 through AC-DEL-6 | None | None | ✅ Full new coverage required |
| Case Matrix: C1, C2a, C2b, C2c, V1/D1, Last Active, V3, Unlinked, Unlinked→Linked | `la-auto-calculation.md` covers Purchased_Slot equivalents of some cases | Partial | ✅ New TCs covering Total_Session_Count for all 9 cases |
| NFR-02 race-condition / concurrency | None | None | ✅ New TC (may require perf/load setup — tag as `@performance`) |
| NFR-03 audit / timestamps | None | None | ✅ New TC for created_at, updated_at, deleted_at assertions |
| NFR-04 scope isolation | None | None | ✅ New TC for non-Riso LA not affected |
| NFR-05 idempotency (POST/PATCH) | None | None | ✅ New TCs: same POST twice, same PATCH twice |
| HTTP error paths (400, 401, 403, 422) | None | None | ✅ New negative TCs for each HTTP error code |

---

## 9. Suggested Test Suite Structure

```
epics/OOP/riso/LT-98533-riso-contract-api/test-cases/
├── get-lesson-allocation.md       → AC-GET-1 to AC-GET-5 — GET LA API: required params, filters, exclusion rules, pagination
├── post-contract-create.md        → AC-POST-1, AC-POST-2, AC-POST-6, BR-30 to BR-32 — POST: create, upsert, required fields, bulk/partial success
├── post-contract-la-link.md       → AC-POST-3 to AC-POST-5, BR-10 to BR-12 — POST: LA linking, unlinked create, DEPENDENCY_MISSING
├── la-aggregation-post.md         → AC-POST-7, AC-POST-8, Case C1, C2a — Aggregation triggered by POST events
├── patch-contract.md              → AC-PATCH-1 to AC-PATCH-4, BR-16 to BR-19 — PATCH: field update, immutable rejection, not-found
├── la-aggregation-patch.md        → Case C2b, C2c, V3, Unlinked→Linked — Aggregation triggered by PATCH events
├── contract-logical-delete.md     → AC-DEL-1 to AC-DEL-6, Case V1/D1, Last Active — Logical delete + aggregation
├── error-paths.md                 → HTTP 400, 401, 403, 422, BR-07 duplicate, BR-33 status constraint — All API error cases
├── scope-isolation.md             → NFR-04, BR-34 — Riso scope isolation, non-Riso LA unaffected
└── nfr-idempotency-audit.md       → NFR-03, NFR-05, AC-DEL-6 — Idempotency (POST/PATCH/DELETE), audit timestamps
```

> **Note:** `nfr-concurrency.md` is intentionally omitted from unit-level test cases. NFR-02 concurrent batch testing requires a performance test environment — tag those scenarios as `@performance` within `la-aggregation-post.md` and `contract-logical-delete.md` rather than a standalone file.
