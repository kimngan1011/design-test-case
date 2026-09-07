---
ticket_id: LT-107256
ticket_url: https://manabie.atlassian.net/browse/LT-107256
title: Withus Juku | Allowing past dates for Classmember start date
module: scheduling
bucket: OOP/withus
status: Ready for QA
internal_uat_date: 2026-07-27
production_release_date: 2026-09-07
last_updated: 2026-08-12
---

# LT-107256: Allow Past Class Member Start Date

## Summary

For Withus Juku only, Salesforce will permit a Class Member start/effective date in the past when it is not earlier than the related Lesson Allocation (LA) start date. The setting replaces the current lower bound of today for the listed Class Member creation/assignment entry points, while Core and other partners remain unchanged.

---

## Acceptance Criteria

### AC-01 — Withus-only Class Member past-date lower boundary

- Current behavior: Class Member start date can only be selected from today onward.
- Updated behavior: when `SF Custom Setting > Lesson Custom Setting > Allow Class Member Start In The Past` is enabled for Withus Juku, the earliest valid start/effective date is the related LA start date.
- A date equal to the LA start date is valid; a date earlier than it is invalid.
- Invalid error message: `Effective date must be from LA start date onwards`.
- In-scope Salesforce entry points:
  1. Contact > Course > Assign Class / Bulk Assign Class
  2. Location Course > Student > Assign Class
  3. LA > Student session > Assign Class
  4. Import Class Member
  5. Create Order > Order Group Class > Class Member
- Scope is Withus Juku only. The ticket explicitly excludes Core and other partners.

### Jira matrix cases

| Case | Required behavior from Jira | Open detail |
|---|---|---|
| New class start = current active class | Given LA 2026/07/01–12/31 and Class A effective 2026/07/01, add Class B effective 2026/07/01. Delete A and make B active; use the latest-created class. | Exact Jira matrix row. |
| New class start > current active class | Given LA 2026/07/01–12/31 and Class A effective 2026/07/01, add Class B effective 2026/07/02. Update A end date to 2026/07/01 and make B active 2026/07/02–12/31. | Exact Jira matrix row. |
| New class start < today < scheduled class | Given LA 2026/07/01–12/31, Class A effective 2026/07/01, and Class B scheduled 2026/08/15, add Class C effective 2026/07/20. Update A end date to 2026/07/19, create C through 2026/12/31, and remove B. | Exact Jira matrix row. |
| New class start < past class and active class | Given LA 2026/06/01–12/31; Class A 2026/06/01, B 2026/07/01, C 2026/07/26; add Class D 2026/06/30. Update Class A end date to 2026/06/29, add D from 2026/06/30, and remove B and C. | Matrix data corrected: LA start is 2026/06/01; no historical lesson-assignment processing is required. |

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---|---|---|---|---|---|
| 1 | AC-01 | Withus may select a past Class Member start date when it is `>= LA start date`. | Class Member start/effective date | Editable with tenant-configured lower-bound validation | SF |
| 2 | AC-01 | A date `< LA start date` is invalid. | Class Member start/effective date | Validated | SF |
| 3 | AC-01 | Invalid entry shows the specified error string. | Effective date validation message | System-generated error | SF |
| 4 | AC-01 | Validation applies to Contact > Course individual and bulk assignment. | Class Member start/effective date | Validated | SF |
| 5 | AC-01 | Validation applies to Location Course > Student assignment. | Class Member start/effective date | Validated | SF |
| 6 | AC-01 | Validation applies to LA > Student session assignment. | Class Member start/effective date | Validated | SF |
| 7 | AC-01 | Validation applies to imported Class Member start dates. | Imported Class Member start date | Validated import field | SF |
| 8 | AC-01 | Validation applies to a Class Member date entered by staff in Order Group Class; no old-data processing occurs. | OGC / Class Member start date | Staff-entered and validated | SF |
| 9 | AC-01 | One LA has at most one active Class Member and one scheduled Class Member; assigning a new class updates the old class effective end date using existing history logic. | Class Member history | System-updated | SF |
| 10 | AC-01 | Feature is isolated to Withus by `Allow Class Member Start In The Past`. | Custom setting | Tenant configuration | SF |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---|---|---|---|---|
| 1 | [REPLACED] | `epics/lesson/LT-107255-order-group-class-assignment/spec.md` | AC-01 | Core behavior starts a Class Member today when a product start is in the past. Withus replaces that lower bound with LA start date only when the setting is enabled. |
| 2 | [REGRESSION RISK] | Qase PX suite 2570: PX-10451, PX-10454 | AC-01 | Existing core cases assert today-normalization for past product starts; order-generated Withus behavior must be flag-isolated. |
| 3 | [EXTENDED] | `epics/OOP/riso/LT-92532-riso-create-update-la-on-ui/test-cases/PBT-1859-add-course-past-date.md` | AC-01 | Existing past-date validation accepts the lower boundary and blocks below it; this extends the pattern using LA start date for Withus Class Members. |

### Missing in Requirements

| # | Tag | Source | Description |
|---|---|---|---|
| 1 | [RESOLVED] | Stakeholder response on 2026-08-12 | One LA has at most one active class and one scheduled class; assigning a new class updates the old class effective end date using existing history logic. |
| 2 | [RESOLVED] | Stakeholder response on 2026-08-12 | All five in-scope flows show `Effective date must be from LA start date onwards` when the entered date is before LA start. |
| 3 | [RESOLVED] | Stakeholder response on 2026-08-12 | This is business-logic improvement only; existing permissions are unchanged. |

### Lesson-Learned Risks

| # | Incident | Date | AC | Risk | Guardrail |
|---|---|---|---|---|---|
| 1 | Aso — Duplicate Student Sessions from Manual Assign + Auto Assign | 2026-04-13 | AC-01 | Not applicable: Withus Juku does not use lesson assignment, so this change must not initiate historical lesson/session reconciliation. | Confirm no lesson-assignment processing is invoked by any in-scope flow. |

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-03 | Class-Based Student Auto-Assignment — Setup & Effective Date Logic | No update: Withus Juku does not use lesson assignment. | N/A |
| E2E-04 | Class-Based Student Auto-Assignment — Import, Multiple Classes & Verification | No update: Withus Juku does not use lesson assignment. | N/A |
| E2E-09 | Lesson Allocation — New Order, Change Course & Void | Add Withus OGC branch; retain core current-date normalization branch. | UPDATE |
| E2E-10 | Lesson Allocation — LOA, Add Course & Lesson Assignment | Verify matching LA/Class Member duration remains intact. | UPDATE |
| E2E-31 | Modify & Unassign Student — Lesson Schedule, Order, Calendar & BO Removals | No update: Withus Juku does not use lesson assignment. | N/A |

### Assumptions Made

- `internal_uat_date` is Jira custom date `2026-07-27`; `production_release_date` is the linked fix version release date `2026-09-07`.
- “Withus Juku” maps to `OOP/withus` for artifact organization, although this tenant is not listed in the convention’s example tenant set.
- The custom setting controls validation only for authorized existing users; no role change is inferred.
- No Figma or Confluence source was linked in the Jira ticket.
- The stakeholder responses below were received on 2026-08-12 and resolve the prior questions.

---

## Clarification Questions

**Jira post status: answered by stakeholder in the QA workflow on 2026-08-12; not posted to Jira.**

1. **[RESOLVED — LESSON-LEARNED RISK]** Withus Juku does not use lesson assignment. Historical eligible lessons and Student Sessions are not reconciled by this change.

2. **[RESOLVED — REGRESSION RISK]** Order Group Class uses a date entered by staff. The change does not process old data; that staff-entered date is subject to the Withus LA-start lower bound.

3. **[RESOLVED — MISSING BEHAVIOR]** One LA has one active class and one scheduled class. When a new class is assigned, existing class-history logic updates the old class effective end date.

4. **[RESOLVED — MISSING BEHAVIOR]** Every in-scope flow shows `Effective date must be from LA start date onwards` for a date before LA start.

5. **[RESOLVED — ROLE GAP]** This improves Withus Class Member business logic only and does not change permissions.

## Related Specs

- `epics/lesson/LT-107255-order-group-class-assignment/spec.md` — current Core Order Group Class and Class Member date baseline.

## Related Test Cases

- `epics/lesson/LT-107255-order-group-class-assignment/test-cases/create-la-new-order-group.md` — OGC/current-date and date-boundary coverage.
- `epics/lesson/LT-107255-order-group-class-assignment/test-cases/lesson-assignment-update.md` — class-history reconciliation and manual-session preservation.
- `epics/lesson/LT-107255-order-group-class-assignment/test-cases/add-associated-course.md` — existing product-type Class Member date rules.
- `epics/OOP/riso/LT-92532-riso-create-update-la-on-ui/test-cases/PBT-1859-add-course-past-date.md` — lower-bound past-date validation pattern.

## QASE Coverage Gaps

- AC-01 — No Qase coverage for the Withus custom-setting ON/OFF boundary across all five entry points.
- AC-01 — No Qase coverage for a Class Member date equal to LA start date, or one day before it, in individual, bulk, LA, import, and order flows.
- AC-01 — No Qase coverage for the Withus one-active/one-scheduled Class Member history rule and old-class effective-end-date update.
- AC-01 — Qase PX-2570 expectations for Core today-normalization require tenant-isolation regression coverage.
- AC-01 — Qase PX-1289 has no direct cases despite its class-management data-model description.
