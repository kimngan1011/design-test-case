---
ticket_id: LT-94105
ticket_url: https://manabie.atlassian.net/browse/LT-94105
title: Riso | Core | Location Closed Date and Holiday
module: scheduling
bucket: OOP/riso
status: Ready for QA
internal_uat_date: null
production_release_date: null
last_updated: 2026-08-14
---

# LT-94105: Riso | Core | Location Closed Date and Holiday

## Summary

LT-94105 classifies each Riso location Closed Date as either a Closed Date or a Holiday/Public Holiday. The classification changes Learner App calendar presentation and makes recurring lessons skip only Closed Date records while preserving normal one-time and manual lesson creation on both types.

The ticket extends the existing location and Academic-Year-scoped ACI model. Its final schedule behavior depends on clarifying the interaction with the current non-editable `Skip Closed Date` schedule setting and the effective time of Type edits.

---

## Acceptance Criteria

### US 01 — Student/parent visibility of center closed dates and public holidays

#### AC 01.1 — Object - field settings

Create a Type picklist field under the Closed Date object with values Closed Date (JP: `休校日`) and Holiday (JP: `祝日`).

#### AC 01.2 — New closed date creation and view

Add Type to the New Closed Date popup. Default it to Closed Date; a user can change it to Public Holiday during creation and can edit the type of an existing closed date.

#### AC 01.3 — New closed date UI on student/parent app

Update the Learner App calendar and day detail:

| Condition | Required behavior |
|---|---|
| Saturday | Date is blue. |
| Sunday | Date is red (`#295ACB`, recorded exactly as written in the PRD). |
| Holiday | Date is red (`#295ACB`, recorded exactly as written in the PRD). |
| Closed Date | Date is gray with diagonal lines. |
| Selected date | Light-blue (`#DEEBFF`) background; selected Closed Date retains diagonal lines. |
| Today | Bold white text in a blue (`#395AD2`) circle; the specified Today treatment takes precedence when today is a Closed Date or selected. |
| Holiday day detail | Display `祝日` next to the date. |
| Closed Date day detail | No change; the closed-date name in body content stays unchanged. |

Resolve closed dates through: Enrollment Location → Location → current Academic Year → Academic Calendar → Closed Date ACI → Closed Date.Type. Only the Calendar section changes.

### US 02 — CM/HQ scheduling on Public Holiday

#### AC 02.1 — Create lesson with closed date

| Lesson operation | Closed Date | Public Holiday |
|---|---|---|
| One-time lesson | Created normally | Created normally |
| Recurring lesson | Skipped; no lesson created | Created normally |
| Manually added lesson | Created normally | Created normally |

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---|---|---|---|---|---|
| 1 | AC 01.1 | Closed Date has a new Type field. | Closed Date.Type | Editable | Salesforce |
| 2 | AC 01.1 | Type allows Closed Date / `休校日`. | Closed Date.Type | Required picklist value; default Closed Date | Salesforce |
| 3 | AC 01.1 | Type allows Holiday / `祝日`. | Closed Date.Type | Editable picklist value | Salesforce |
| 4 | AC 01.2 | New Closed Date popup shows Type. | Closed Date.Type | Editable; default Closed Date | Salesforce |
| 5 | AC 01.2 | A user may change Type during creation. | Closed Date.Type | Editable | Salesforce |
| 6 | AC 01.2 | A user may edit Type on an existing record. | Closed Date.Type | Editable | Salesforce |
| 7 | AC 01.3 | Saturday dates are blue. | Calendar date | Auto-calculated | Learner App |
| 8 | AC 01.3 | Sunday dates are `#295ACB` (called red in PRD). | Calendar date | Auto-calculated | Learner App |
| 9 | AC 01.3 | Holiday dates are `#295ACB` (called red in PRD). | Calendar date | Auto-calculated | Learner App |
| 10 | AC 01.3 | Closed Dates are gray with diagonal lines. | Calendar date | Auto-calculated | Learner App |
| 11 | AC 01.3 | Selected date is `#DEEBFF`; selected Closed Date retains diagonal lines. | Calendar selection | Auto-calculated | Learner App |
| 12 | AC 01.3 | Today is bold white text in a `#395AD2` circle and takes stated precedence. | Calendar today state | Auto-calculated | Learner App |
| 13 | AC 01.3 | Holiday day detail adds the `祝日` label. | Day-detail holiday label | Auto-calculated | Learner App |
| 14 | AC 01.3 | Closed Date day detail and body closed-date name do not change. | Day-detail Closed Date content | Locked | Learner App |
| 15 | AC 01.3 | Resolve Type through enrollment location, location, current AY, calendar, and Closed Date ACI. | Closed Date lookup | Auto-calculated | Learner App |
| 16 | AC 02.1 | One-time lesson is created on a Closed Date. | Lesson creation | Editable | Salesforce |
| 17 | AC 02.1 | Recurring lesson is skipped on a Closed Date. | Recurring generation | Auto-calculated | Salesforce |
| 18 | AC 02.1 | Manually added lesson is created on a Closed Date. | Lesson Schedule Add Lesson | Editable | Salesforce |
| 19 | AC 02.1 | One-time lesson is created on a Public Holiday. | Lesson creation | Editable | Salesforce |
| 20 | AC 02.1 | Recurring lesson is created on a Public Holiday. | Recurring generation | Auto-calculated | Salesforce |
| 21 | AC 02.1 | Manually added lesson is created on a Public Holiday. | Lesson Schedule Add Lesson | Editable | Salesforce |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---|---|---|---|---|
| 1 | [CONFLICT] | `knowledge/e2e-scenario/e2e-scenarios.md` — E2E-02/E2E-15 | AC 02.1 | Existing recurrence skips closed dates only when the schedule-level Skip Closed Date setting is ON; AC 02.1 says recurring lessons skip every Closed Date without defining the setting interaction. |
| 2 | [CONFLICT] | `knowledge/e2e-scenario/e2e-scenarios.md` — E2E-02/E2E-15 | AC 02.1 | Existing Skip Closed Date = ON has no Type-based holiday exception; AC 02.1 requires normal recurring creation on Public Holiday. |

### Extended Existing Behavior

| # | Tag | Source | AC | Description |
|---|---|---|---|---|
| 1 | [EXTENDED] | `epics/master-data/LT-87693-academic-calendar-closed-date-per-location/spec.md` — AC 02.2 | AC 01.1 | Type extends the existing ACI Closed Date record and must retain location/AY isolation. |
| 2 | [EXTENDED] | `epics/master-data/LT-87693-academic-calendar-closed-date-per-location/spec.md` — AC 04.2 | AC 01.3 | Learner App adds Type at the terminal record of the established enrollment-location → ACI traversal. |
| 3 | [EXTENDED] | `knowledge/domain-knowledge/scheduling/calendar/calendar-sf.md` | AC 02.1 | One-time and Lesson Schedule Add Lesson paths retain their existing permissive behavior on Closed Dates and apply it to Holiday. |

### Missing in Requirements

| # | Tag | Source | AC | Description |
|---|---|---|---|---|
| 1 | [MISSING BEHAVIOR] | `temp/business_rules.json` — BR-01 to BR-03 | AC 01.1 | No backfill/null-handling rule for existing Closed Dates after Type is introduced. |
| 2 | [MISSING BEHAVIOR] | `temp/raw_requirement.json` — AC 01.1 versus AC 01.2/02.1 | AC 01.1 | Picklist says Holiday / `祝日`; later ACs say Public Holiday. Canonical value and label mapping are unspecified. |
| 3 | [ROLE GAP] | `knowledge/domain-knowledge/scheduling/scheduling-feature-permission-matrix.csv` | AC 01.2 | Existing create/edit permissions are full_access and center_level_edit only; the AC says only “a user” and does not define CM/HQ scope or denied roles. |
| 4 | [REGRESSION RISK] | `knowledge/e2e-scenario/e2e-scenarios.md` — E2E-15 steps 6–7 | AC 01.2 | E2E-15 expects closed-date edit/delete recalculation, while domain knowledge says ACI changes are non-retroactive; Type edit effective time is unspecified. |
| 5 | [MISSING BEHAVIOR] | `temp/business_rules.json` — BR-07 to BR-14 | AC 01.3 | Visual precedence is not exhaustive for Saturday Holiday, selected Holiday, or today Holiday. |
| 6 | [UNDOCUMENTED IN AC] | `temp/raw_requirement.json` — Figma source unavailable | AC 01.3 | Figma cannot be checked and the PRD calls `#295ACB` red; the authoritative token and Figma-only states are unverified. |

### Lesson-Learned Risks

No relevant historical incidents found. All three scheduling lesson-learned incidents were assessed with the entity-and-operation overlap test; none involve Closed Date classification, Learner App calendar rendering, or recurrence generation.

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-15 | Academic Calendar & Closed Dates Impact | Add Type creation/edit and Learner App display/label coverage; reconcile its retroactive-recalculation steps with the documented non-retroactive domain rule. | UPDATE |
| E2E-02 | Recurring Lesson — Create, Edit Chain, Delete, Calendar Drag | Add a Type × Skip Closed Date decision matrix and Holiday recurrence branch; retain manual add/drag behavior unless clarified otherwise. | UPDATE |

### Assumptions Made

- The ticket is Riso-specific, so the artifact is placed in `OOP/riso`.
- `status` is `null` because the Jira status was not retained in the valid Phase 1 artifacts; it must be replaced with the Jira status verbatim when available.
- The supplied hex values are recorded exactly as written. No visual interpretation overrides the PRD pending design confirmation.
- No Figma-derived behavior is assumed because the linked design was unavailable for inspection.
- No retroactive recurrence action is assumed for a Type edit; the existing domain context documents ACI create/edit/delete as non-retroactive, while E2E-15 currently conflicts and needs resolution.

---

## Clarification Questions

1. **[CONFLICT]** AC 02.1 says recurring lessons skip Closed Date, while the current system makes skipping conditional on the schedule's non-editable-at-creation Skip Closed Date setting (OFF currently allows an instance). For Closed Date.Type = Closed Date, what is the required result for schedules whose existing Skip Closed Date value is ON and OFF: should the setting be removed/ignored, or should it still control creation?
   _Evidence: `knowledge/e2e-scenario/e2e-scenarios.md, E2E-02/E2E-15` — Skip Closed Date = ON produces no recurring instance; `temp/domain_context.json` — Skip OFF currently allows recurring instances on closed dates._

2. **[CONFLICT]** AC 02.1 requires recurring lessons to be created normally on Public Holiday. If a recurring schedule was created with Skip Closed Date = ON, must it now create an instance whenever the matching ACI record has Type = Holiday/Public Holiday, or does Skip Closed Date still skip it? Please confirm the Type × Skip Closed Date decision matrix.
   _Evidence: `knowledge/e2e-scenario/e2e-scenarios.md, E2E-02/E2E-15` — Skip Closed Date = ON skips a closed-date instance; `AC 02.1` — recurring lessons create normally on Public Holiday._

3. **[REGRESSION RISK]** When a user edits Type on an existing Closed Date (for example Closed Date → Holiday), should previously generated recurring lessons be recalculated, created, deleted, or re-coded, or should the change apply only to future generation? The current E2E scenario expects closed-date edits to recalculate a lesson chain, while current domain knowledge says ACI create/edit/delete is non-retroactive.
   _Evidence: `knowledge/e2e-scenario/e2e-scenarios.md, E2E-15 steps 6–7` — edit recalculates and delete creates a lesson; `temp/domain_context.json` — later ACI create/edit/delete does not retroactively change existing lessons._

4. **[UNDOCUMENTED IN AC]** Should `#295ACB` be treated as the authoritative Sunday/Holiday date color even though AC 01.3 calls it “red”? The linked Figma design could not be inspected, so please confirm the design token and any Figma-defined empty, loading, error, or interaction states that must be implemented.
   _Evidence: `temp/raw_requirement.json, figma_discrepancies` — Figma source unavailable; `AC 01.3` records `#295ACB` as red._

5. **[MISSING BEHAVIOR]** What Type should existing Closed Date records have after deployment, and how should a record with null or invalid Type behave in recurrence and the Learner App calendar? Please specify whether a data migration/backfill sets all existing records to Closed Date and whether null records are blocked, defaulted, or handled another way.
   _Evidence: `temp/business_rules.json, BR-01 to BR-03` — Type and a default are defined for new records only; existing Closed Dates already drive ACI lookup and recurrence._

6. **[MISSING BEHAVIOR]** Is “Holiday / `祝日`” the one stored picklist value and is “Public Holiday” only an English description, or are Holiday and Public Holiday intended to be distinct values? Please confirm the canonical stored value and the Salesforce and Learner App display labels.
   _Evidence: `temp/raw_requirement.json, AC 01.1` — picklist value Holiday / `祝日`; `AC 01.2` and `AC 02.1` — Public Holiday._

7. **[MISSING BEHAVIOR]** Please define the complete visual-precedence matrix for a Saturday Holiday, selected Holiday, and today Holiday: which text color, selected background, today circle, diagonal lines, and Holiday / `祝日` label should each state show? AC 01.3 defines selected Closed Date and today Closed Date/selected behavior but not these Holiday overlaps.
   _Evidence: `temp/business_rules.json, BR-07 to BR-13` — Saturday/Sunday/Holiday/Closed Date/selected/today rules do not define all overlapping states._

8. **[ROLE GAP]** Which permission sets and scope rules may create or edit Closed Date.Type? In particular, should existing full_access and center_level_edit users retain those rights, with bo_teacher denied, and should CM be limited to its affiliated ACI while HQ can edit ACM and location ACIs?
   _Evidence: `knowledge/domain-knowledge/scheduling/scheduling-feature-permission-matrix.csv` — Create/Edit Closed Date allowed for full_access and center_level_edit, denied for bo_teacher; `AC 01.2` only says a user can create/edit Type._

> Questions have not been posted to Jira.

---

## Related Specs

- `epics/master-data/LT-87693-academic-calendar-closed-date-per-location/spec.md` — ACI location/AY ownership, Closed Date isolation, and Learner App traversal baseline.
- `knowledge/domain-knowledge/scheduling/calendar/calendar-sf.md` — current recurring/manual lesson treatment on closed dates.
- `knowledge/e2e-scenario/e2e-scenarios.md` — E2E-02 and E2E-15 recurrence and closed-date baselines.

## Related Test Cases

- `epics/master-data/LT-87693-academic-calendar-closed-date-per-location/test-cases/LT-87693-aci.md` — CM ACI Closed Date add/remove/isolation baseline.
- `epics/master-data/LT-87693-academic-calendar-closed-date-per-location/test-cases/LT-87693-acm.md` — ACM/ACI cloning and post-application Closed Date behavior baseline.
- `epics/master-data/LT-87693-academic-calendar-closed-date-per-location/test-cases/LT-87693-general.md` — existing calendar UI translation and migration baseline.

## QASE Coverage Gaps

No Qase suite or existing Qase cases were provided in Phase 1. Coverage must be added for all ticket ACs, especially:

- AC 01.1 — picklist values, legacy-record Type migration/null handling, and permission enforcement.
- AC 01.2 — default/change/edit flows and confirmed effective-time behavior of a Type edit.
- AC 01.3 — location/AY lookup, complete state-precedence matrix, Holiday label, and unchanged Closed Date body content.
- AC 02.1 — one-time/manual/recurring decision matrix across Type and the existing Skip Closed Date setting, including lesson-code sequencing.
