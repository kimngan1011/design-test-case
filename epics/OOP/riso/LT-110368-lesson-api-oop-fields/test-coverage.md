# Test Coverage: LT-110368 — Riso Lesson API OOP Fields and Related Change Sync

**Jira:** https://manabie.atlassian.net/browse/LT-110368  
**Date:** 2026-09-29

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|---|---|
| 1 | AC-01 | A valid Riso lesson request returns only Lessons in the required status, date, and location scope, with the finalized response shape. |
| 2 | AC-02 | Status, start date, end date, and location are required; the end date is inclusive and cannot precede the start date. |
| 3 | AC-02 | `last_updated_since` returns Lessons with `SystemModstamp` at or after the supplied UTC watermark. |
| 4 | AC-02 | Pagination uses `limitQuery` and `paging.next_pointer`; a full page supplies the final Lesson Id and a non-full page returns `null`. |
| 5 | AC-03 | Riso OOP fields serialize as strings; a configured field with no record value returns `null`, without failing the response. |
| 6 | AC-04 | The response `last_updated_at` is exactly the parent Lesson's `LastModifiedDate`, not the internal related-change field. |
| 7 | AC-04 | Create, update, or delete of each confirmed related object touches every affected Lesson, which becomes eligible for the incremental pull. |
| 8 | AC-05 | Teacher, classroom, and student collections reflect active related data; deleted or archived Student Sessions are excluded. |
| 9 | AC-01, AC-03 | The response includes all finalized core, OOP, teacher, classroom, and student fields with correct source values. |
| 10 | AC-01, AC-04 | Riso always receives the `compensation_ratio` key; it contains the Lesson value or `null`. |
| 11 | AC-01, AC-04 | Course partner codes derive from all schedule classes, sort deterministically, and join with semicolons. |
| 12 | AC-02 | Invalid/missing required parameters and invalid date formats return `400`; invalid status, page size, or cursor returns `422`. |

---

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC-01 | 1, 9, 10 | Cross-system impact; Display completeness; Data integrity |
| AC-02 | 2, 12 | Validation; Boundary/range |
| AC-02 | 3 | Conditional; Boundary/range; Cross-system impact |
| AC-02 | 4 | Boundary/range; Data integrity |
| AC-03 | 5 | Conditional; Cross-system impact |
| AC-04 | 6 | Data integrity; Cross-system impact |
| AC-04 | 7 | CRUD; Data integrity; Cross-system impact |
| AC-05 | 8 | Conditional; Data integrity; Cross-system impact |
| AC-01 | 11 | Ordering / Sort; Data integrity |

---

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Validation | Equivalence Partitioning; Boundary Value Analysis; Negative |
| Boundary/range | Boundary Value Analysis; Negative |
| Conditional | Decision Table; Negative |
| CRUD | CRUD; Regression |
| Data integrity | CRUD; Decision Table; Regression |
| Cross-system impact | Regression; CRUD; Component |
| Display completeness | Component; Negative |
| Ordering / Sort | Scenario; Pairwise |

---

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC-01 | Return the complete finalized response for a populated Lesson, including teacher, classroom, student, and Riso fields | Cross-system; Display completeness | Component | High | Deep |
| AC-01 | Always return `compensation_ratio`; preserve a populated value and a null value | Conditional; Data integrity | Decision Table | High | Standard |
| AC-01 | Aggregate multiple class partner codes in sorted semicolon-separated order | Ordering/Sort; Data integrity | Scenario | High | Standard |
| AC-01 | Convert a Lesson at a JST/UTC date boundary to the correct UTC response timestamps | Boundary/range; Cross-system | BVA; Regression | High | Deep |
| AC-02 | Accept each supported status, requested date range, and matching location | Validation; Conditional | Equivalence Partitioning; Decision Table | Medium | Standard |
| AC-02 | Reject missing required input, malformed dates, reversed date range, unsupported status, invalid page size, and invalid cursor | Validation; Boundary/range | Equivalence Partitioning; BVA; Negative | High | Deep |
| AC-02 | Return a Lesson whose update watermark exactly equals `last_updated_since`; exclude one before it | Boundary/range; Data integrity | BVA; Decision Table | Critical | Deep |
| AC-02 | Retrieve every Lesson exactly once across full and final cursor pages | Boundary/range; Data integrity | BVA; Regression | High | Deep |
| AC-03 | Return null for an empty optional Riso field without error or an omitted key | Conditional; Cross-system | Decision Table; Negative | High | Standard |
| AC-04 | Return direct Lesson edits in the incremental pull and map its modified timestamp to `last_updated_at` | Data integrity; Cross-system | CRUD; Component | Critical | Deep |
| AC-04 | Lesson Teacher create/update/delete changes the parent timestamp and active teacher collection | CRUD; Cross-system | CRUD; Regression | Critical | Deep |
| AC-04 | Lesson Classroom create/update/delete changes the parent timestamp and active classroom collection | CRUD; Cross-system | CRUD; Regression | Critical | Deep |
| AC-04 | Student Session create/update/delete changes the parent timestamp and active student collection | CRUD; Cross-system | CRUD; Regression | Critical | Deep |
| AC-04 | Lesson Report create/update/delete changes the parent timestamp | CRUD; Cross-system | CRUD; Regression | Critical | Deep |
| AC-04 | Lesson Survey Response create/update/delete changes the parent timestamp | CRUD; Cross-system | CRUD; Regression | Critical | Deep |
| AC-04 | Lesson Schedule create/update/delete affects every Lesson in the schedule's incremental result | CRUD; Data integrity; Cross-system | CRUD; Regression | Critical | Deep |
| AC-04 | Lesson Schedule Class create/update/delete affects every Lesson in the schedule and recomputes class partner codes | CRUD; Data integrity; Cross-system | CRUD; Regression | Critical | Deep |
| AC-05 | Exclude deleted Student Sessions from the returned student collection while still returning the changed parent Lesson | Conditional; Data integrity | Decision Table; Regression | Critical | Deep |
| AC-05 | Exclude archived Student Sessions from the returned student collection while still returning the changed parent Lesson | Conditional; Data integrity | Decision Table; Regression | Critical | Deep |

### 4.5 Mandatory edge-case checklist

| Pattern | Applicability | Coverage decision |
|---|---|---|
| A. Configuration thresholds | N/A | The PRD has no configurable threshold. `limitQuery` is a request input, covered as a validation and pagination boundary instead. |
| B. Date/time and timezone | Yes | Cover an exact incremental watermark boundary, inclusive date range, and a Lesson at `2026-10-01 00:30 JST = 2026-09-30T15:30:00Z`; all API timestamps are UTC. DST is N/A because JST has no DST. |
| C. Concurrent/stale state | Yes | Page through a stable multi-record result and assert no duplicate/missing Lesson at the cursor boundary. No request-side write exists; double-submit is N/A. |
| D. Permission and role | Partial | The API authentication contract is not specified. No role matrix can be designed without its expected 401/403 behavior; retain as an open dependency. Riso tenant/OOP field behavior is covered. |
| E. State transition | N/A | This is a read-only API; Lesson status is a filter, not a state transition implemented by this epic. |
| F. Cross-system | Yes | Assert source Lesson/related data and returned payload together for each related-object event. |
| G. Downstream effects | Yes | Every related-object create/update/delete has a separate case that verifies Lesson timestamp update, incremental eligibility, and relevant returned collection. |
| H. Display/ordering | Yes for API data | Use one populated response component case for all required fields; use a separate scenario for ordered class partner codes. UI inventory is N/A because the feature has no UI. |
| H.1 Spec–Figma | N/A | The spec has no Figma URL. |

### Downstream Effects Inventory

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner (TC group) |
|---|---|---|---|
| Direct Lesson update | Parent modified timestamp advances; Lesson appears in incremental result | Lesson record; Riso API | Direct Lesson timestamp cases |
| Create/update/delete Lesson Teacher | Parent modified timestamp advances; active teacher collection changes | Lesson record; `teachers` response collection | Lesson Teacher lifecycle cases |
| Create/update/delete Lesson Classroom | Parent modified timestamp advances; active classroom collection changes | Lesson record; `classrooms` response collection | Lesson Classroom lifecycle cases |
| Create/update/delete Student Session | Parent modified timestamp advances; eligible student collection changes | Lesson record; `students` response collection | Student Session lifecycle cases |
| Create/update/delete Lesson Report | Parent modified timestamp advances | Lesson record; Riso API | Lesson Report lifecycle cases |
| Create/update/delete Lesson Survey Response | Parent modified timestamp advances | Lesson record; Riso API | Survey Response lifecycle cases |
| Create/update/delete Lesson Schedule | Every lesson in the schedule has an advanced timestamp and is in incremental results | All Lessons under one schedule; Riso API | Lesson Schedule fan-out lifecycle cases |
| Create/update/delete Lesson Schedule Class | Every schedule Lesson has an advanced timestamp; class partner codes reflect the resulting set | All Lessons under one schedule; Riso API | Lesson Schedule Class fan-out lifecycle cases |
| Delete/archive Student Session | Session absent from `students`; parent remains visible through incremental result | Student collection; Riso API | Student exclusion cases |

### Display & Ordering Inventory

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| Riso Lesson API populated response | Response envelope; core Lesson details; timestamps; compensation ratio; teacher, classroom, and student collections | Empty optional values are `null`; student records are excluded when deleted/archived | Class partner codes sort before joining | None |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Related-object timestamp propagation | A missed parent update means Riso's incremental job permanently misses changed information. | Individually exercise create/update/delete for all seven objects; compare source parent timestamp and incremental response. |
| Lesson Schedule / Schedule Class fan-out | One changed schedule can affect many Lessons. Updating only one instance creates silent partial synchronization. | Use one schedule with at least two Lessons and assert every affected Lesson returns. |
| Watermark boundary | An exclusive comparison or timezone conversion error drops records from a nightly synchronization run. | Test exact equality, one record before the watermark, and a JST/UTC date boundary. |
| Deleted/archived Student Session filtering | Historical or invalid students in JStaff cause incorrect operational data. | Test deletion and archival independently, while asserting the parent Lesson is still returned as changed. |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Finalized response mapping | Wrong identifiers or OOP values break downstream JStaff upsert/reporting. | Compare every populated response field against known Salesforce source data in a single complete component case. |
| Class code aggregation | Incorrect ordering or delimiter produces a false course/class association. | Use three classes with non-alphabetical creation order and assert sorted semicolon-delimited output after each Schedule Class lifecycle event. |
| Cursor pagination | Missing or repeated records cause an incomplete downstream sync. | Test exact page size and a final partial page, then compare the unique IDs with the source set. |
| Invalid query handling | Weak validation can produce an unintentionally broad or misleading data extraction. | Partition by error status: malformed/missing query input = 400; invalid business value/cursor/page size = 422. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Empty optional Riso values | A null value must not become an omitted property or API error. | Use a configured field with no record value and assert the key is present with `null`. |
| Status/location/date filtering | Incorrect filtering returns an unexpected operational scope. | Use distinguishable Lessons covering each supported status, adjacent dates, and two locations. |

---

## 6. Coverage Gaps vs. Existing Test Cases

Existing local cases: none for LT-110368. Existing Qase parent suite **PX / Get Lesson API (3005)** contains 14 older baseline cases and is the import destination.

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Basic successful request without cursor | Qase 22995: Get Lesson Without Pointer - Success | Partial — older response uses `updated_at` and does not assert finalized mappings | ✅ Complete finalized payload and `last_updated_at` mapping. |
| Cursor request | Qase 23000: Get Lesson With Pointer - Success | Partial — no deterministic page-boundary/data-integrity assertion | ✅ Full-page/final-page cursor traversal with unique Lesson IDs. |
| Direct Lesson status/date edits | Qase 23001–23003 | Partial — no current timestamp-source assertion | ✅ Direct Lesson timestamp mapping and incremental watermark boundary. |
| Location filter | Qase 23004 | Partial — no response mapping/current contract assertion | ✅ Covered inside populated response and scope decision cases. |
| `last_updated_since` basic request | Qase 23005 and 23014 | Partial — no equality boundary, related-object propagation, or `LastModifiedDate` assertion | ✅ Watermark boundary and all related-object lifecycle cases. |
| Default page size | Qase 23013 | Full for default-value behavior | No new standalone default-page-size case. |
| Missing required parameters | Qase 23007, 23009, 23011, 23012 | Full for the four missing-parameter variants | No duplicate missing-parameter cases; add malformed date, reversed range, unsupported status, invalid page size, and invalid cursor only. |
| OOP fields / compensation ratio | None | None | ✅ Populated and null-value response coverage, including always-present compensation ratio key. |
| Nested related collections | Qase 22995 | Partial — one static sample only | ✅ Active teacher/classroom/student data and Student Session exclusion coverage. |
| All seven related objects | None | None | ✅ Create/update/delete lifecycle matrix with timestamp propagation and schedule fan-out. |
| Class partner-code ordering | None | None | ✅ Sorted, semicolon-delimited aggregation coverage. |

---

## 7. Suggested Test Suite Structure

```
epics/OOP/riso/LT-110368-lesson-api-oop-fields/test-cases/
└── lesson-api-oop-fields.md
    → AC-01 to AC-05 — finalized response contract, validation and pagination deltas,
      direct Lesson incremental behavior, and the 7 × create/update/delete related-change matrix
```

**Proposed Qase suite:** `[Riso] Get Lesson API – OOP Fields & Related Change Sync` as a child of **PX / Get Lesson API (3005)**.

### Estimated test cases

| Area | Estimated cases |
|---|---:|
| Finalized response, explicit Lesson/Teacher/Student OOP mapping, filtering, validation, watermark, and pagination deltas | 18 |
| Lesson Teacher lifecycle | 3 |
| Lesson Classroom lifecycle | 3 |
| Student Session lifecycle plus deleted/archived exclusions | 5 |
| Lesson Report lifecycle | 3 |
| Lesson Survey Response lifecycle | 3 |
| Lesson Schedule fan-out lifecycle | 3 |
| Lesson Schedule Class fan-out and class-code lifecycle | 3 |
| **Total** | **41** |

## Open dependency

Authentication and authorization behavior is not defined in the PRD/current epic
comment. This design intentionally does not infer 401/403 outcomes. Add those
cases only after the integration-authentication contract is confirmed.
