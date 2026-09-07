# Test Coverage: LT-107256 — Withus Class Member Past Start Date

**Jira:** https://manabie.atlassian.net/browse/LT-107256  
**Date:** 2026-08-12

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|---|---|
| BR-01 | AC-01 | Withus permits a Class Member effective date from the related LA start date onwards when `Allow Class Member Start In The Past` is enabled. |
| BR-02 | AC-01 | A date before the LA start date is rejected with `Effective date must be from LA start date onwards`. |
| BR-03 | AC-01 | The lower-bound validation applies to Contact > Course individual and bulk assignment. |
| BR-04 | AC-01 | The validation applies to Location Course > Student assignment and LA > Student Session assignment. |
| BR-05 | AC-01 | The validation applies to Import Class Member. |
| BR-06 | AC-01 | The validation applies to a date entered by staff in Create Order > Order Group Class > Class Member; no old-data processing occurs. |
| BR-07 | AC-01 | One LA has at most one active Class Member and one scheduled Class Member; assigning a new class updates the old class effective end date through existing history logic. |
| BR-08 | AC-01 | The change is enabled only for Withus; Core and other tenants retain the existing behaviour. |
| BR-10 | AC-01 | Existing authorization remains unchanged: permitted staff can assign classes; BO teachers remain unable to do so. |

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC-01 | BR-01, BR-02 | Validation logic; Boundary/range logic |
| AC-01 | BR-03, BR-04, BR-05, BR-06 | Cross-system impact; Conditional logic; Display completeness |
| AC-01 | BR-07 | State transition; Data integrity |
| AC-01 | BR-08 | Conditional logic; Permission logic; Cross-system impact |
| AC-01 | BR-10 | Permission logic |

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Validation logic | Equivalence Partitioning; Negative |
| Boundary/range logic | Boundary Value Analysis; Negative |
| Conditional logic | Decision Table; Negative |
| State transition | State Transition; CRUD |
| Permission logic | Permission Matrix; Decision Table |
| Data integrity | CRUD; Regression; Decision Table |
| Cross-system impact | Regression; CRUD |
| Display completeness | Component; Negative |

## G. Downstream Effects Inventory

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner (planned TC) |
|---|---|---|---|
| Create a valid past Class Member | Class Member is created with start date equal to LA start and correct class/LA linkage. | Salesforce Class Member; LA | CM-past-date-01, 04, 07, 10, 13 |
| Create or replace a Class Member at a backdated date | The one active / one scheduled Class Member rule is retained and the old class effective end date is updated by existing history logic. | Salesforce Class Member history | CM-history-01 through 04 |
| Retry a create/import/order action | No duplicate Class Member is created. | Salesforce Class Member | CM-history-04 |
| Submit an invalid past date | The flow shows the exact error and no Class Member or history mutation occurs. | Salesforce records; import/order result | CM-negative-01 through 05 |
| Toggle setting OFF or use a non-Withus tenant | Core/order current-date normalization and non-Withus lower-bound behaviour remain unchanged. | Core and tenant configuration; Order Group Class | CM-isolation-01 through 03 |

## H. Display & Ordering Inventory

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| Contact > Course Assign Class form | Class Member effective-date input | Earliest selectable/accepted date changes only when Withus setting is ON | N/A — no ordering requirement | `Effective date must be from LA start date onwards` |
| Contact > Course Bulk Assign Class form | Effective-date input for each selected assignment | Withus setting ON/OFF validation state | N/A — no ordering requirement | `Effective date must be from LA start date onwards` |
| Location Course > Student Assign Class form | Effective-date input | Withus setting ON/OFF validation state | N/A — no ordering requirement | `Effective date must be from LA start date onwards` |
| LA > Student Session Assign Class form | Effective-date input | Withus setting ON/OFF validation state | N/A — no ordering requirement | `Effective date must be from LA start date onwards` |
| Import Class Member result | Imported effective-date value and validation error | Valid versus invalid row result | N/A — result ordering is not specified | `Effective date must be from LA start date onwards` |
| Create Order > Order Group Class | Staff-entered Class Member effective date | Withus setting ON/OFF and date before LA start | N/A — no ordering requirement | `Effective date must be from LA start date onwards` |

**H.1 — N/A: No Figma URL in the approved spec.**

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC-01 | Withus setting ON accepts a date equal to LA start date. | Boundary/range logic; Conditional logic | BVA; Decision Table | High | Deep |
| AC-01 | Withus setting ON rejects LA start date minus one day with the exact error. | Validation logic; Boundary/range logic; Display completeness | BVA; Negative; Component | High | Deep |
| AC-01 | Withus setting ON accepts a later past date and today/future dates within the LA range. | Equivalence partitioning; Boundary/range logic | Equivalence Partitioning; BVA | High | Deep |
| AC-01 | Individual and bulk Contact > Course assignment enforce the same boundary for each selected student. | Cross-system impact; Data integrity; Display completeness | Decision Table; CRUD; Component | High | Deep |
| AC-01 | Location Course > Student and LA > Student Session assignment enforce the same boundary. | Cross-system impact; Display completeness | Regression; Component; Negative | High | Deep |
| AC-01 | Import shows the lower-bound error for an invalid entered date and leaves the Class Member history unchanged. | Validation logic; Data integrity; Cross-system impact; Display completeness | Equivalence Partitioning; Negative; CRUD; Component | High | Deep |
| AC-01 | Order Group Class validates the date entered by staff against the Withus LA lower bound without processing old data. | Conditional logic; Boundary/range logic; Cross-system impact; Display completeness | Decision Table; BVA; Regression; Component | High | Deep |
| AC-01 | Setting OFF and non-Withus tenants do not receive Withus past-date access. | Conditional logic; Permission logic | Decision Table; Negative; Regression | High | Deep |
| AC-01 | Existing Class Member history retains at most one active and one scheduled record; new assignment updates the old class effective end date. | State transition; Data integrity | State Transition; CRUD; Decision Table | Critical | Deep |
| AC-01 | Existing authorized staff retain access and BO teachers cannot assign classes. | Permission logic | Permission Matrix; Decision Table | Medium | Standard |
| AC-01 | JST business date controls date-only validation at the midnight boundary. | Boundary/range logic; Cross-system impact | BVA; Regression | High | Deep |

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Historical Class Member updates | Backdated inserts must retain the one-active/one-scheduled invariant and update the old class effective end date. | Use state-transition cases for same-date replacement, later replacement, and replacing a scheduled class. |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Five entry-point consistency | Separate Salesforce surfaces can diverge in client validation, server validation, and error text. | Run the LA-start, one-day-before, today, and future partitions in each entry point; assert the verbatim error text. |
| Tenant isolation and Core regression | PX-10451 and PX-10454 assert Core today-normalization for past product starts. | Retain Core cases; add Withus-setting ON/OFF and non-Withus decision-table branches. |
| Date-only timezone boundary | SF/JST date conversion near midnight can move a valid boundary date back one calendar day. | Fix `today` and target dates in every date case; run JST and device TZ-ahead/behind boundary coverage where the application supports it. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Role coverage | Ticket changes no permissions, but assignment entry points have role gates. | Smoke the permitted full-access/centre-level-edit roles and confirm BO teacher denial. |

## 6. Mandatory Edge-Case Assessment

| Area | Assessment | Coverage disposition |
|---|---|---|
| A. Configuration-driven threshold | Yes — setting ON/OFF is the supported configuration; no numeric min/max or config-change visibility rule is specified. | Decision-table cases for Withus ON, Withus OFF, and non-Withus. Numeric config BVA: N/A, not a numeric configuration. |
| B. Date/time | Yes — date-only lower bound. Today, LA start, LA start minus one day, and later past/future dates are applicable. DST: N/A because the business timezone is JST. Cross-midnight/device-TZ scenarios are required. | Deep BVA + JST/TZ regression cases; all cases declare `today` and `target_date`. |
| C. Concurrent/stale state | Applicable to import/order retry and duplicate Class Member risk; seat/deadline scenarios are N/A. | Retry/double-submit and duplicate-Class-Member cases. |
| D. Permission/role | Yes — unchanged role gate and tenant flag must be retained. | Permission matrix and cross-tenant/setting-OFF cases. |
| E. State transition | Yes — Class Member history changes. | State-transition matrix for one-active/one-scheduled history and old-class end-date update. |
| F. Cross-system/cross-surface | Yes — five SF entry points, LA/Class Member history, and order/import outcomes. External-sync outage is N/A: no external asynchronous integration or SLA is specified. | Per-surface validation plus record-level downstream checks. |
| G. Downstream effects | Yes — inventory covers Class Member, history, idempotency, and invalid-write prevention. No inverse delete action is stated; removal/replacement is covered as a history transition. | Each listed effect maps to a planned TC family in Section G. |
| H. Display/ordering | Six ticket-named forms/results have date/error elements. No sort, empty state, pagination, or non-ticket field inventory is specified. | Component rows assert ticket-specific field state and exact error; ordering/empty/pagination: N/A with no spec rule. |
| H.1 Spec–Figma | No Figma URL supplied. | N/A. |

## 7. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Core past product start normalization | Qase PX-10451 / PX-10454; `LT-107255/create-la-new-order-group.md` | Existing baseline asserts start = today for Core. | ✅ Add Withus ON/OFF and non-Withus decision-table regression without replacing Core expectation. |
| Past-date lower-bound validation | `PBT-1859-add-course-past-date.md` | Similar BVA pattern uses product start, not LA start or Class Member. | ✅ Add LA-start exact-boundary and one-day-before cases for all five entry points. |
| Individual/bulk / Location Course / LA Student Session | No identified direct cases in supplied Qase suites. | None. | ✅ Add each surface's valid, invalid, exact-error, and no-write coverage. |
| Import validity and error | `LT-107255/lesson-assignment-update.md` covers a valid current-date import and manual session retention. | Does not cover past LA boundary, invalid data, exact error, or tenant flag. | ✅ Add valid historical import and invalid exact-error/no-history-mutation coverage. |
| Class history update | `LT-107255/lesson-assignment-update.md` covers future/current class changes. | Does not cover the Withus one-active/one-scheduled rule and old-class end-date update. | ✅ Add state-transition cases for the confirmed history rule. |
| Role and tenant isolation | No identified direct test in supplied suites. | None. | ✅ Add permission smoke and Withus/Core/non-Withus flag matrix. |
| Exact error and date-component rendering | No identified direct test in supplied suites. | None. | ✅ Add component assertions for all six named surfaces. |

## 8. Suggested Test Suite Structure

```
epics/OOP/withus/LT-107256-allow-past-classmember-start-date/test-cases/
├── direct-class-assignment.md       → AC-01 — Contact, bulk, Location Course, and LA Student Session boundary/error/role coverage
├── class-member-import.md           → AC-01 — valid/invalid historical import and exact-error/history integrity
├── order-group-class-member.md      → AC-01 — Withus ON/OFF Order Group Class and Core/non-Withus regression
└── class-member-history.md          → AC-01 — one-active/one-scheduled history and old-class effective-end-date updates
```

## 9. Open Requirement Dependencies

All Phase 1 clarification questions were resolved by the stakeholder on 2026-08-12. The cases will assert the confirmed lower-bound/error, staff-entered Order Group Class date, one-active/one-scheduled history rule, and unchanged permissions.
