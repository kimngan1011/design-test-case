---
ticket_id: LT-98533
ticket_url: https://manabie.atlassian.net/browse/LT-98533
title: Riso | OOP | Create/Update Riso_Contract from external system via API
module: scheduling
bucket: OOP/riso
status: Ready for Internal UAT
internal_uat_date: 2026-06-29
production_release_date: 2026-06-29
last_updated: 2026-06-19
---

# LT-98533: Riso | OOP | Create/Update Riso_Contract from external system via API

## Summary

This ticket implements a **Contract API lifecycle integration** between Riso's external ERP system and Manabie under a **1 Lesson Allocation : Many Contracts** model. Riso submits Contract records to Manabie via POST (create/upsert) and PATCH (partial update / logical delete) APIs. Manabie persists Contract records, links them to Lesson Allocations, and automatically aggregates three LA fields (`Total_Session_Count`, `Start_Date`, `End_Date`) from active Contract data.

The feature also exposes a **read-only GET Lesson Allocation API** so Riso can look up LA IDs before submitting Contracts. Scope is strictly Riso OOP — no feature flag needed.

**PRD:** https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2382659626/Riso+OOP+Student+Contracts+UI+API  
**API PRD:** https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2255290379/Riso+OOP+RISO+Contract+APIs+--+Tentative  
**PBT ticket:** https://manabie.atlassian.net/browse/PBT-1812

---

## Acceptance Criteria

### EPIC 1 — Get Lesson Allocation (Read-only API)

_As Riso, I need to retrieve Lesson Allocations from Manabie by specifying Location and Academic Year (and optionally Course), so that I can correctly identify the LA and store its ID before submitting Contracts._

| ID | Feature | Acceptance Criteria |
|---|---|---|
| AC-GET-1 | Retrieve by Location + AY | Given a valid location_id and academic_year, when Riso calls GET /v1/lesson-allocations, then the system returns all matching LA records with required fields |
| AC-GET-2 | Optional Course filter | Given course_offering_id is provided, when the system processes the request, then only LAs matching that Course Offering are returned |
| AC-GET-3 | Incremental pull | Given last_modified_since is provided, when the system processes the request, then only LAs modified on or after that timestamp are returned |
| AC-GET-4 | Exclusion rules | Given an LA has Require Allocation = false or is deleted/archived, when any GET request is processed, then those LAs must be excluded from results |
| AC-GET-5 | Pagination | Given results exceed the page size limit, when the system processes the request, then a next_pointer cursor is returned and subsequent pages are retrievable |

---

### Story 1 — Create / Update Contract (POST)

_As Riso, I need to submit Contract data to Manabie via POST API so that Contract records can be created or updated and linked to the correct Lesson Allocation._

| ID | Feature | Acceptance Criteria |
|---|---|---|
| AC-POST-1 | Create new record | Given a POST with a new external_ref_id, then a new Contract record is created and the external identifier stored uniquely. Duplicate creation for the same external_ref_id must be rejected (409 DUPLICATE_RECORD). |
| AC-POST-2 | Update existing record (upsert) | Given a POST with an existing external_ref_id, then the existing Contract is updated. No duplicate is created. Previous values remain auditable. |
| AC-POST-3 | Link to LA | Given a POST includes a valid lesson_allocation_id, then the Contract is linked to that LA. Student is validated for existence in Manabie. |
| AC-POST-4 | Create unlinked | Given a POST without lesson_allocation_id, then the Contract is created unlinked. No LA aggregation is triggered. |
| AC-POST-5 | LA not found | Given a POST includes a lesson_allocation_id that does not exist in Manabie, then the API returns 409 DEPENDENCY_MISSING. No record is created. |
| AC-POST-6 | Bulk / partial success | Given multiple Contracts in one POST batch, when each item is processed independently (partial success mode), then per-record results (success or error) are returned. |
| AC-POST-7 | LA aggregation on create | Given a new Contract linked to an LA is created, then LA.Total_Session_Count, LA.Start_Date, and LA.End_Date are recalculated based on all Active contracts linked to that LA. |
| AC-POST-8 | LA aggregation on upsert (slot/total change) | Given POST updates an existing Contract's slot/total, then LA.Total_Session_Count is recalculated. No duplicate record is created. |

---

### Story 2 — Update Contract Fields (PATCH)

_As Riso, I need to partially update Contract records so that field changes (date adjustments, LA re-links) are handled cleanly._

| ID | Feature | Acceptance Criteria |
|---|---|---|
| AC-PATCH-1 | Update allowed fields | Given a PATCH with valid updatable fields (end_date, lesson_allocation_id, slot, total), then only those fields are updated. Immutable fields (external_ref_id, student_id, acad_year_id) are rejected if included. |
| AC-PATCH-2 | Aggregation on date change | Given PATCH updates end_date, then LA.End_Date recalculates. LA.Total_Session_Count is unchanged unless total also changed. |
| AC-PATCH-3 | Aggregation on LA re-link | Given PATCH updates lesson_allocation_id, then the old LA recalculates (removing this contract) and the new LA recalculates (adding it). Both LAs update all three aggregation fields. |
| AC-PATCH-4 | Not-found handling | Given the external_ref_id does not exist, then the API returns 404 NOT_FOUND. No record is created. |

---

### Story 3 — Contract Logical Delete (PATCH)

_As Riso, I need to notify Manabie when a Contract is cancelled or no longer valid, so that the record is logically deleted and LA aggregation is updated accordingly._

| ID | Feature | Acceptance Criteria |
|---|---|---|
| AC-DEL-1 | Identify and mark deleted | Given a PATCH with contract_status = Deleted for a valid external_ref_id, then the Contract record is marked Deleted. Record is not physically removed. |
| AC-DEL-2 | Preserve traceability | Given a logical deletion is processed, then the record remains in the system, historical data is recoverable, and the deletion event is timestamped (deleted_at). |
| AC-DEL-3 | Aggregation recalculation | Given a Contract linked to an LA is logically deleted, then LA.Total_Session_Count, LA.Start_Date, and LA.End_Date are recalculated. The deleted contract no longer contributes. No negative aggregation. |
| AC-DEL-4 | Unlinked contract deletion | Given a Contract not linked to any LA is logically deleted, then the Contract is marked Deleted. No aggregation recalculation is required. |
| AC-DEL-5 | Multiple contracts per LA | Given one of multiple Contracts linked to the same LA is logically deleted, then remaining Active Contracts are unaffected. Aggregation reflects only remaining eligible Contracts. |
| AC-DEL-6 | Idempotency | Given the same logical deletion request is sent multiple times, then the system does not produce inconsistent state and aggregation integrity is maintained. |

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---|----|----|---|---|---|
| BR-01 | AC-GET-1 | GET LA requires location_id and academic_year as mandatory parameters | location_id, academic_year | required | [API] |
| BR-02 | AC-GET-2 | course_offering_id is optional filter; when provided, only matching LAs returned | course_offering_id | optional | [API] |
| BR-03 | AC-GET-3 | last_modified_since enables incremental pull; only LAs modified on/after timestamp returned | last_modified_since | optional | [API] |
| BR-04 | AC-GET-4 | LAs with Require Allocation = false excluded from GET LA response | require_allocation | locked (system-derived) | [API] |
| BR-05 | AC-GET-4 | Deleted/archived LAs excluded from GET LA response | la_status | locked (system-derived) | [API] |
| BR-06 | AC-GET-5 | Cursor-based pagination; next_pointer returned when results exceed page size | next_pointer | auto-calculated | [API] |
| BR-07 | AC-POST-1 | POST with new external_ref_id creates new Contract; external_ref_id must be unique | external_ref_id | required, immutable | [API] |
| BR-08 | AC-POST-1 | Duplicate POST with same external_ref_id (not upsert) rejected with 409 DUPLICATE_RECORD | external_ref_id | required, immutable | [API] |
| BR-09 | AC-POST-2 | POST with existing external_ref_id acts as upsert — updates existing Contract, no duplicate created | external_ref_id | required | [API] |
| BR-10 | AC-POST-3 | When lesson_allocation_id provided: Contract linked to LA; student existence validated | lesson_allocation_id | optional, updatable | [API] |
| BR-11 | AC-POST-4 | When lesson_allocation_id absent: Contract created unlinked; no LA aggregation triggered | lesson_allocation_id | optional | [API] |
| BR-12 | AC-POST-5 | lesson_allocation_id that does not exist → 409 DEPENDENCY_MISSING; no record created | lesson_allocation_id | optional | [API] |
| BR-13 | AC-POST-6 | Bulk POST: partial success mode — each item processed independently; per-record results returned | contracts[] | required (array) | [API] |
| BR-14 | AC-POST-7 | Creating new Contract linked to LA → recalculate LA.Total_Session_Count, LA.Start_Date, LA.End_Date | LA.Total_Session_Count, LA.Start_Date, LA.End_Date | auto-calculated | [API] |
| BR-15 | AC-POST-8 | Updating Contract slot/total via POST upsert → recalculate LA.Total_Session_Count | slot, total, LA.Total_Session_Count | updatable / auto-calculated | [API] |
| BR-16 | AC-PATCH-1 | PATCH allows: end_date, lesson_allocation_id, slot, total. Immutable: external_ref_id, student_id, acad_year_id | multiple | updatable / immutable | [API] |
| BR-17 | AC-PATCH-2 | PATCH end_date update → LA.End_Date recalculates; LA.Total_Session_Count unchanged unless total also changed | end_date, LA.End_Date | updatable / auto-calculated | [API] |
| BR-18 | AC-PATCH-3 | PATCH re-link (lesson_allocation_id change) → old LA recalculates (remove), new LA recalculates (add). Both get all 3 aggregation fields updated. | lesson_allocation_id, all LA aggregation fields | updatable / auto-calculated | [API] |
| BR-19 | AC-PATCH-4 | PATCH with non-existent external_ref_id → 404 NOT_FOUND; no record created | external_ref_id | required | [API] |
| BR-20 | AC-DEL-1 | PATCH contract_status = Deleted → logical delete; record NOT physically removed | contract_status | updatable | [API] |
| BR-21 | AC-DEL-2 | After logical delete: record in system, history recoverable, deleted_at populated | deleted_at | auto-calculated | [API] |
| BR-22 | AC-DEL-3 | Linked Contract logical delete → recalculate LA.Total_Session_Count, LA.Start_Date, LA.End_Date. No negative aggregation. | all LA aggregation fields | auto-calculated | [API] |
| BR-23 | AC-DEL-4 | Unlinked Contract logical delete → marked Deleted; no aggregation recalculation | contract_status | updatable | [API] |
| BR-24 | AC-DEL-5 | One of multiple contracts on LA deleted → remaining Active Contracts unaffected; aggregation reflects remaining only | LA.Total_Session_Count | auto-calculated | [API] |
| BR-25 | AC-DEL-6 | Logical delete is idempotent: repeated deletes do not corrupt state or aggregation | contract_status | updatable | [API] |
| BR-26 | AC-POST-7 | LA.Total_Session_Count = SUM(contract.total) for all Active contracts linked to the same LA | LA.Total_Session_Count | auto-calculated | [API] |
| BR-27 | AC-POST-7 | LA.Start_Date = Earliest start_date among all Active contracts linked to the LA | LA.Start_Date | auto-calculated | [API] |
| BR-28 | AC-POST-7 | LA.End_Date = Latest end_date among all Active contracts linked to the LA | LA.End_Date | auto-calculated | [API] |
| BR-29 | AC-DEL-3 | When LAST Active contract deleted: LA.Total_Session_Count = 0. LA.Start_Date and LA.End_Date: **retain their last known values** (confirmed). | LA.Total_Session_Count, LA.Start_Date, LA.End_Date | auto-calculated | [API] |
| BR-30 | AC-POST-1 | Contract required fields on POST: external_ref_id, external_product_code, acad_year_id, location_id, course_offering_id, student_id, type, slot, total, contract_status, start_date | multiple | required | [API] |
| BR-31 | AC-POST-1 | Contract.type must be: weekly, monthly, or one-time. Immutable after creation. | type | required, immutable | [API] |
| BR-32 | AC-POST-1 | Contract.end_date optional on POST; when provided must be ≥ start_date | end_date | optional | [API] |
| BR-33 | AC-DEL-1 | contract_status allowed values: active (default on create), deleted (via PATCH). No 'ended'. No DELETE HTTP endpoint. | contract_status | updatable | [API] |
| BR-34 | AC-POST-1 | Riso OOP only — no feature flag. Contract API scope isolated from core LA and non-Riso partners. | — | — | [API] |

---

## LA Aggregation Rules (applies to all EPIC 2 stories)

> These rules define exactly how `LA.Total_Session_Count`, `LA.Start_Date`, and `LA.End_Date` are derived. They are the primary source of truth for test case design — every aggregation test case must trace back to one of these rules.

### Aggregation Formulas

| Field | Formula | Eligibility |
|---|---|---|
| `LA.Total_Session_Count` | SUM of `contract.total` for all **Active** contracts linked to the same LA | Only `contract_status = active` contracts included |
| `LA.Start_Date` | Earliest `start_date` among all **Active** contracts linked to the LA | Only `contract_status = active` contracts included |
| `LA.End_Date` | Latest `end_date` among all **Active** contracts linked to the LA | Only `contract_status = active` contracts included |
| `LA.Purchased_Slot` | **NOT auto-calculated** — manually entered by SF user. Defaults to 0. Independent of contracts. | — |

> ⚠️ **`Purchased_Slot` vs `Total_Session_Count`**: These are two distinct LA fields. `Purchased_Slot` (`MANAERP__Purchased_Slot__c`) is manually managed by SF users and **not affected by Contract API events**. `Total_Session_Count` (`MANAERP__Total_Session_Count__c`) is the auto-calculated aggregation target for this feature.

### Contract-to-LA Aggregation Case Matrix

This matrix defines the expected state change for each contract event type. **Every row = one or more required test cases.**

| Case | Event | Contract Change | `LA.Total_Session_Count` | `LA.Start_Date` | `LA.End_Date` |
|---|---|---|---|---|---|
| **C1** | New contract linked to LA | POST with `lesson_allocation_id` (new contract) | Add `contract.total`; recalculate SUM | Recalculate: earliest `start_date` | Recalculate: latest `end_date` |
| **C2a** | Update — slot / total change | PATCH `slot` or `total` on existing linked contract | Recalculate SUM of all Active | No change unless dates also changed | No change unless dates also changed |
| **C2b** | Update — end date change | PATCH `end_date` on existing linked contract | No change | No change | Recalculate: latest `end_date` of Active |
| **C2c** | Update — LA reference change (re-link) | PATCH `lesson_allocation_id` to a different LA | Recalculate **both** old LA (remove) and new LA (add) | Recalculate **both** LAs | Recalculate **both** LAs |
| **V1/V2/D1** | Contract soft deleted | PATCH `contract_status = Deleted` (any linked contract) | Recalculate SUM of remaining Active | Recalculate: earliest of remaining Active | Recalculate: latest of remaining Active |
| **V3** | Retroactive cancel — end date moved earlier | PATCH `end_date` (status stays active) | No change | No change | Recalculate if this was previously the latest |
| **Last Active deleted** | Final Active contract on LA is soft deleted | PATCH `contract_status = Deleted` (last one) | Set to **0** | **Retain last known value** | **Retain last known value** |
| **Unlinked create** | New contract, no LA reference | POST without `lesson_allocation_id` | No LA affected | No LA affected | No LA affected |
| **Unlinked → Linked** | Unlinked contract later linked to an LA | PATCH `lesson_allocation_id` (new value, was null) | Add to new LA aggregation | Recalculate new LA | Recalculate new LA |

### Additional Aggregation Notes

- **First-month enrollment pattern:** When Riso sends two contracts for the same LA (one one-time for the first month, one monthly for the remainder), both are included in aggregation independently. Standard summation — no special handling required.
- **Aggregation timing:** Must be re-triggered on **every** relevant contract event. Stale aggregation is not acceptable (NFR-02).
- **Concurrency:** Must handle concurrent batch submissions (~20,000 students/year, daily night batch) without race conditions.
- **Logical deletion permanence:** A logically deleted contract is excluded from aggregation immediately and permanently unless `contract_status` is reversed (not currently expected).
- **No slot consumption hierarchy:** No priority ordering on which contract is consumed first when multiple contracts exist per LA.
- **Monthly type:** `type = monthly` is received and stored only. Not used for any slot calculation logic at this stage.

---

## Technical Design Considerations

> ⚠️ The engineering team must determine the underlying data model before implementation. This section is solution-agnostic — QA must confirm the selected design before writing DB-level verification steps.

### Decision Required: Contract Object Design

| Option | Description | Pros | Cons |
|---|---|---|---|
| **A** (assumed by PRD) | New dedicated **RISO Contract** object | Scalable; decoupled from LA; extensible for other partners | Additional object; similar fields to LA |
| **B** | Reuse existing LA-related object (e.g., SPO) | No new object needed | Coupled to LA lifecycle; harder to extend |
| **C** | Other extensible structure (TBD) | — | — |

### Design Requirements (whichever option is selected)

The selected design **must** support:
1. Multiple Contracts per LA (1:M relationship)
2. API-driven create, update, and logical delete
3. **Audit history** for field changes (`slot`, `status`, `dates`, `LA reference`) — field-level change tracking required
4. Aggregation into `LA.Total_Session_Count`, `LA.Start_Date`, `LA.End_Date`
5. Logical deletion that excludes the record from aggregation immediately
6. Extensibility for future entitlement complexity and other partner use

### QA Implications

- Must verify that **audit history** is preserved after updates (previous values are queryable)
- Must verify that **aggregation recalculation** is triggered immediately (not async/eventual) — especially after logical deletes
- Must verify **scope isolation**: Contract object and aggregation logic must not affect non-Riso LA records or any other partner

---

## Non-Functional Requirements

| ID | Category | Requirement | QA Test Approach |
|---|---|---|---|
| NFR-01 | Performance | GET LA API must return results within acceptable response time for Riso's daily batch. POST Contract bulk must handle concurrent records without timeout. | Load/performance test with realistic volume (~20,000 contracts); verify no timeout at max batch size |
| NFR-02 | Data Consistency | LA aggregation must reflect current state of Active contracts **at all times**. No stale values after any contract event. Race conditions must not cause incorrect aggregation. | Trigger all 5 aggregation event types and immediately verify LA field values. Test concurrent batch POST with overlapping LA references. |
| NFR-03 | Auditability | All Contract records retained after logical deletion. Field change history (`slot`, `status`, `dates`, `LA reference`) must be auditable. API-originated events must be timestamped and traceable. | Verify `deleted_at` populated on logical delete. Verify previous field values remain queryable. Verify `created_at`, `updated_at` timestamps are set correctly. |
| NFR-04 | Scope Isolation | Contract API and aggregation logic must be scoped to Riso. No unintended impact on non-Riso partners or core LA object behavior. | Verify that POST/PATCH Contract on Riso data does not modify LA records of other partner students. Verify core LA lifecycle (order-driven) is not affected. |
| NFR-05 | Idempotency | POST and PATCH operations must be idempotent on `external_ref_id`. Repeated submissions must not create duplicates or corrupt aggregation. | Send same POST payload twice — verify no duplicate record. Send same PATCH twice — verify state unchanged on second call. _(See open Q-04 for clarification on 409 vs silent idempotency)_ |
| NFR-06 | Volume | ~20,000 students/year, at least 2 contracts each (~40,000 records/year). Aggregation recalculation must complete within acceptable time per batch run. | Test with batch of N contracts for same LA (multiple in one night batch); verify all aggregation is consistent after batch completes. |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---|---|---|----|---|
| 1 | [CONFLICT] | epics/OOP/riso/LT-92532-riso-create-update-la-on-ui/test-cases/la-auto-calculation.md | AC-POST-7 (LT-98533) / AC 03.1 (LT-92532) | Existing TCs assert `LA.Purchased_Slot = SUM(Contract.slot)`. PRD LT-98533 states `LA.Total_Session_Count = SUM(Contract.total)` and explicitly says "Purchased Slot is NOT auto-calculated from contracts — it is a separate, manually managed field." These are different fields from different source attributes. Clarification needed on whether both are auto-calculated or only Total_Session_Count. |
| 2 | [REGRESSION RISK] | epics/OOP/riso/LT-92532-riso-create-update-la-on-ui/test-cases/la-auto-calculation.md | AC-POST-7, AC-POST-8 | If Total_Session_Count is the new aggregation target (not Purchased_Slot), existing la-auto-calculation.md TCs may become stale/fail or miss Total_Session_Count coverage entirely after this implementation. |

### Missing in Requirements

| # | Tag | Source | Description |
|---|---|---|---|
| 1 | ~~[MISSING BEHAVIOR]~~ **[RESOLVED]** | Confluence PRD page 2382659626 — Case Matrix | ~~When the LAST Active contract on an LA is logically deleted: LA.Start_Date and LA.End_Date behavior is TBC in the PRD (retain or null).~~ **Confirmed by user: LA.Start_Date and LA.End_Date retain their last known values.** BR-29 updated. |
| 2 | [MISSING BEHAVIOR] | NFR-05 + AC-POST-1, AC-DEL-6 | Idempotency for POST (same new contract twice) is not explicitly covered by any AC. AC-DEL-6 covers logical delete idempotency only. The 409 DUPLICATE_RECORD vs idempotent 201 behavior is contradicted by the text of AC-POST-1 vs NFR-05. |
| 3 | [ROLE GAP] | Confluence PRD 2382659626 — Roles in scope | SF HQ/CM/Centre Staff users who review Lesson Allocations on SF UI will see updated Total_Session_Count, Start_Date, End_Date after Contract API events — but no AC defines what they see in UI or whether field labels are correct after Contract integration. |
| 4 | [UNDOCUMENTED IN AC] | Confluence API PRD page 2255290379 — Common Errors table | API PRD defines HTTP 400 (INVALID_REQUEST), 401 (UNAUTHORIZED), 403 (FORBIDDEN), 422 (VALIDATION_ERROR) error codes. No ACs cover authentication failure, authorization failure, or general validation error paths. |

### Lesson-Learned Risks

| # | Incident | Date | AC | Risk | Guardrail |
|---|---|---|---|---|---|
| 1 | Nichibei — Student Sessions Missing LA → Points Not Deducted | 2026-03-04 | AC-POST-7, AC-POST-8, AC-PATCH-2, AC-PATCH-3, AC-DEL-3 | If any aggregation trigger event type is missing from implementation (e.g., PATCH re-link not triggering aggregation), LA.Total_Session_Count will be silently stale. NFR-02 explicitly prohibits stale aggregation. | Test every aggregation trigger event type independently (POST create, POST upsert, PATCH end_date, PATCH re-link, PATCH logical delete). Include concurrent batch test. |

### E2E Scenario Impact

_None identified. No e2e-scenarios.md found in workspace matching Contract or Riso aggregation scenarios._

### Assumptions Made

- The slug `riso-contract-api` is derived from the ticket title "Riso | OOP | Create/Update Riso_Contract from external system via API" per epic-folder-convention.md.
- Bucket = `OOP/riso` — feature is Riso-only OOP.
- LA.Purchased_Slot (existing Riso field) and LA.Total_Session_Count (new in this ticket) are confirmed as separate fields per PRD text: "Purchased Slot is NOT auto-calculated from contracts. It is a separate, manually managed field."
- No Figma URLs found in the Jira ticket or linked Confluence pages.
- DELETE Contract API was explicitly removed from scope (strikethrough in PBT-1812 description).
- EPIC 3 (Contract UI and Report / Show Contract List) is handled in PBT-1510 — out of scope for LT-98533.

---

## Clarification Questions

1. **[CONFLICT]** Are `LA.Purchased_Slot` and `LA.Total_Session_Count` two distinct fields that are both auto-calculated from contracts independently (Purchased_Slot from Contract.slot, Total_Session_Count from Contract.total)? Or does LT-98533 replace the LT-92532 AC 03.1 spec, and existing la-auto-calculation.md test cases need to be updated to reflect Total_Session_Count?
   _Evidence: LT-92532 test cases assert "LA.Purchased_Slot = SUM(Contract.slot)". PRD 2382659626 states "Purchased Slot is NOT auto-calculated from contracts — it is a separate, manually managed field."_

2. **[ROLE GAP]** After Contract API events update LA.Total_Session_Count, LA.Start_Date, and LA.End_Date on the backend, do SF users (HQ/CM) see these updated values on the Contact → Course tab? Are the SF field labels for these fields confirmed? (MANAERP__Total_Session_Count__c vs MANAERP__Purchased_Slot__c)
   _Evidence: PRD lists "SF users (HQ/CM) who review LAs and Contracts" as in scope users, but no AC defines UI display behavior._

3. **[MISSING BEHAVIOR]** When the exact same POST payload for a brand-new contract is sent twice (true duplicate, not upsert): AC-POST-1 says "rejected" (409 DUPLICATE_RECORD), while NFR-05 says "idempotent — repeated submissions must not create duplicates." Should the second call return 409 (rejected) or 201 with the same record (silently idempotent)?
   _Evidence: AC-POST-1: "Duplicate creation for the same external_ref_id must be rejected." NFR-05: "Repeated submissions must not create duplicates or corrupt aggregation."_

4. **[LESSON-LEARNED RISK]** Aggregation must trigger on 5 distinct event types (POST create, POST upsert slot/total, PATCH end_date, PATCH re-link, PATCH logical delete). Is this implemented as a single trigger point on any Contract write, or as 5 separate event handlers? How can QA verify the trigger is present for all 5 cases?
   _Evidence: Nichibei SPO sync incident — OOP flows can have missing trigger paths vs Core. NFR-02: "Stale aggregation is not acceptable."_

---

## Related Specs

- `epics/OOP/riso/LT-92532-riso-create-update-la-on-ui/spec.md` — Riso manual LA creation on UI. LA.Purchased_Slot auto-calc (US03 deferred to PBT-1812) directly overlaps with this ticket.
- `epics/OOP/riso/LT-94698-subject-in-lesson-detail/spec.md` — Riso subject field on lesson. Different domain, not impacted.

## Related Test Cases

- `epics/OOP/riso/LT-92532-riso-create-update-la-on-ui/test-cases/la-auto-calculation.md` — **DIRECTLY IMPACTED** — existing TCs for Purchased Slot auto-calc reference "pending PBT-1812". Must be reviewed after LT-98533 is confirmed: either superseded by new Total_Session_Count TCs or updated to reflect both fields.

## QASE Coverage Gaps

- AC-GET-1 — No existing Qase test cases found for GET LA API
- AC-GET-2 — No existing Qase test cases found for course filter on GET LA
- AC-GET-3 — No existing Qase test cases found for incremental pull
- AC-GET-4 — No existing Qase test cases found for exclusion rules
- AC-GET-5 — No existing Qase test cases found for pagination
- AC-POST-1 through AC-POST-8 — No existing Qase test cases found for Contract POST API
- AC-PATCH-1 through AC-PATCH-4 — No existing Qase test cases found for Contract PATCH API
- AC-DEL-1 through AC-DEL-6 — No existing Qase test cases found for Contract logical delete
- All aggregation rules (BR-26 through BR-29) — No existing Qase coverage
