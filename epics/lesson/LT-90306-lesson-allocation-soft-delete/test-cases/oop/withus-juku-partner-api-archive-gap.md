# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 561 — "Lesson/Course Management & API update"](https://app.qase.io/project/PX?suite=561) (9 existing cases, LT-80592, OOP FEATURES → Withus Juku, parent 555). Two cases are LA-relevant: #5863 "[A07] Get all lesson allocation API includes new columns in response" and #6007 "[A21] Get Class Member API supports filtering and ordering by LastModifiedDate". This is a concrete instance of spec.md's already-documented Missing in Requirements #8 ("Partner REST API consumers... query with partner-owned queries that don't filter archived rows. We can only update sample Postman requests and notify partners — cannot force a fix").

**Code-trace confirmation — structurally unfixable server-side, exactly as spec already states.** Neither A07 nor A21 corresponds to a Manabie-owned Apex `@RestResource`. The only LA-related Apex REST endpoints in the repo (`LessonAllocationRestAPI.cls`, `LessonAllocationRestAPITransport.cls`) expose narrow internal-UI actions only, not a bulk "get all" export matching A07. No Apex REST resource exists for `Class_Member__c` at all. What exists instead is `outside-packages/connections/main/default/connectedApps/Manabie_Open_API.connectedApp-meta.xml` — a Connected App granting generic OAuth `Api` scope via client-credentials flow, consistent with WithUs Juku authenticating once and then issuing its own raw SOQL against `Lesson_Allocation__c`/`Class_Member__c` with a partner-constructed WHERE clause. There is no Manabie Apex code in between to inject an archive filter.

**These are verification/documentation artifacts, not pass/fail code tests** — there is no fixable code path on Manabie's side for a test to hold accountable. They exist to give the `[SF] Check Partner REST API / Postman collection` ticket owner concrete, current-state evidence (current unfiltered query result vs. the corrected query the partner's sample Postman collection should be updated to) to support the "update sample Postman requests and notify partners" mitigation already named in spec.

## Suite: Lesson/Course Management & API update

### [WithUs Juku] A07 Get All Lesson Allocation API – Current Partner Query Returns Archived LA Rows

**Description:** AC-5 (out-of-package, confirmed unfixable) — Negative. Contrasts with existing baseline (#5863, which only verifies the new column list, no archive dimension). Documents the current behavior for the partner-notification effort: WithUs Juku's own query against this generic Salesforce API endpoint has no reason to exclude archived LA unless their Postman collection is explicitly updated to add the filter.

**Preconditions:**
- A WithUs Juku Lesson Allocation record exists, archived (`Archived_At__c` populated, via its order group being fully removed).
- WithUs Juku's existing sample Postman request for A07 is available, using whatever WHERE clause their current collection defines (per spec's framing, likely date-range/LastModifiedDate-based only, with no archive filter).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send WithUs Juku's current A07 request as-is against an org containing the archived LA | [Documents current state] The archived LA record is returned in the response, indistinguishable from an active one — confirmed structurally unfixable server-side, since Manabie has no Apex layer to filter this partner-constructed query | Current query has no Archived_At__c filter |
| 2 | Re-send the same request with `AND MANAERP__Archived_At__c = null` added to the WHERE clause | The archived LA record is correctly excluded from the response | Corrected query for the Postman collection update |
| 3 | Hand off: recommend the corrected WHERE clause from step 2 as the sample Postman collection update, and flag WithUs Juku for direct partner notification per the existing `[SF] Check Partner REST API / Postman collection` ticket | Ticket owner has a concrete before/after query pair to act on | No server-side fix possible — partner must adopt the corrected query themselves |

**Severity:** major
**Priority:** high

---

### [WithUs Juku] A21 Get Class Member API – Current Partner Query Returns Archived Class Member Rows

**Description:** AC-5 (out-of-package, confirmed unfixable) — Negative. Contrasts with existing baseline (#6007, no archive dimension). Same structural gap as A07, for `Class_Member__c` — directly relevant since this epic's spec already flags `Class_Member__c.Is_Archived__c` propagation as a critical architecture gap (Core impact table: "Native backend Class_Member sync... Backend currently syncs Class_Member by DeletedAt only, with no is_archived concept").

**Preconditions:**
- A Class Member record exists whose parent Lesson Allocation is archived, so `Is_Archived__c = TRUE` via formula.
- WithUs Juku's existing sample Postman request for A21 is available (filtered/ordered by LastModifiedDate, per #6007's description, with no archive filter).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Send WithUs Juku's current A21 request as-is against an org containing the archived-parent Class Member | [Documents current state] The Class Member record is returned, still appearing active to the partner's integration, despite the underlying LA being archived | Current query has no Is_Archived__c filter |
| 2 | Re-send the same request with `AND MANAERP__Is_Archived__c = false` added to the WHERE clause | The Class Member record is correctly excluded from the response | Corrected query for the Postman collection update |
| 3 | Hand off: recommend the corrected WHERE clause from step 2 as the sample Postman collection update, flagged alongside A07 for the same partner-notification ticket | Ticket owner has a concrete before/after query pair to act on | No server-side fix possible — partner must adopt the corrected query themselves |

**Severity:** major
**Priority:** high

---
