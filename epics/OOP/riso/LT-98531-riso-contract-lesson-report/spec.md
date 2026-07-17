---
ticket_id: LT-98531
ticket_url: https://manabie.atlassian.net/browse/LT-98531
title: "[Riso] OOP | Contract vs Lesson Assigned Report"
module: scheduling
bucket: OOP/riso
status: Ready for QA
internal_uat_date: 2026-06-29
production_release_date: 2026-07-13
last_updated: 2026-06-22
---

# LT-98531: [Riso] OOP | Contract vs Lesson Assigned Report

## Summary

This feature gives Riso HQ/CM users two new tools to monitor lesson allocation efficiency. First, a **Contract List** is added to the Contact > Course tab on SF, showing contract information directly alongside lesson allocations — replacing the existing "Not Require Allocation" list which will be hidden. Second, a **Monthly Lesson Assignment standalone report** is created that compares Purchased Slots (from contract records) against Lesson Allocated (from student sessions) per student per month, with a Diff column to surface under-allocation or mismatches. Both surfaces are Riso-only OOP and accessible by HQ and CM roles.

The contract data displayed is sourced from the Riso Contract model introduced in LT-98533. This ticket covers the read-only UI layer; the underlying Contract API (create/update/delete) is out of scope here.

---

## Acceptance Criteria

### User Story 1: Show Contract List in Contact > Course Tab

**As a** HQ/CM user
**I want** to see the list of contracts directly in Contact > Course
**So that** I can review contract information without checking a separate screen

| ID | Feature | Acceptance Criteria |
|---|---|---|
| AC-01 | Contract List Display | The Contact > Course tab must display a contract list for the current Academic Year. Show only: Lesson Allocation, Course, Start Date, End Date, Location, Contract Status. Empty state shown if no contracts exist for the contact. Display in Active tab (current AY) and Inactive tab (previous AYs). |
| AC-02 | Contract List Sorting | The contract list must be sorted by Location ASC, then Course ASC, then Start Date ASC. Applied consistently on every load or refresh. |
| AC-03 | Hide "Not Require Allocation" List | The existing "Not Require Allocation" list must be hidden from Contact > Course tab for Riso only. Removing it must not affect the new contract list. |
| AC-04 | Riso-only Exposure | The contract list and related UI changes must be shown only for Riso. Non-Riso partners must not see this UI. |
| AC-05 | Lesson Allocation Display | The Lesson Allocation value shown in the contract list must be as specified in the Post Contract API. Keep blank if no data from the API. |

### User Story 2: Create Standalone Monthly Lesson Assignment Report

**As a** HQ/CM user
**I want** a standalone monthly report
**So that** I can check purchased slots versus allocated lessons across one or more students

| ID | Feature | Acceptance Criteria |
|---|---|---|
| AC-06 | Standalone Report Availability | "Monthly Lesson Assignment" report accessible to authorized Riso HQ/CM users independently of the Contact screen. Supports overall checking across multiple students. Must not be exposed to non-Riso partners. |
| AC-07 | Report Filters | Filters: Month, AY (default: current AY on open), Student or Contact ID (multi-select), Location (multi-select, default: user's assigned location). Default on open: current AY, user's assigned location, all students. |
| AC-08 | Report Columns | Columns: Location, Student Name, Course, Student Course Duration Per Month (Jan…Dec), Purchased Slot (label only; source defined in AC-09), Lesson Allocated, Diff (Purchased Slot - Lesson Allocated). Order by Location, Student Name, Course, Start Date ASC. Rows with missing values must still render without breaking the report. |
| AC-09 | Purchased Slot Calculation | Purchased Slot per month: if Contract.type = Monthly or Weekly → use Contract.slot; if Contract.type = One Time → use Contract.total. |
| AC-10 | Lesson Allocated Calculation | Lesson Allocated = count of lessons for the target monthly context. EXCLUDE student sessions where Attendance = Absent AND Attendance Notice is NOT "In Advance". All other sessions (including Absent+InAdvance) are included. Calculation applied consistently for all rows. |
| AC-11 | Diff Formula | Diff = Purchased Slot - Lesson Allocated, per row. Negative, zero, and positive values all display correctly. |
| AC-12 | Multi-student Checking | Student or Contact ID filter supports multiple values. Report shows rows for all matching students under the same filter context. |

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---|----|----|---|---|---|
| BR-01 | AC-01 | Contact > Course tab displays contract list for current AY for Riso users | Contract List | read-only display | SF |
| BR-02 | AC-01 | Contract list columns: Lesson Allocation, Course, Start Date, End Date, Location, Contract Status | Contract List columns | read-only display | SF |
| BR-03 | AC-01 | Empty state shown (no error) when no contracts exist for the contact | Empty state | auto-display | SF |
| BR-04 | AC-01 | Active tab: contracts for current AY | Active tab | filter / display | SF |
| BR-05 | AC-01 | Inactive tab: contracts for previous AYs | Inactive tab | filter / display | SF |
| BR-06 | AC-02 | Sort: Location ASC → Course ASC → Start Date ASC; applied on every load/refresh | Sort order | auto-calculated | SF |
| BR-07 | AC-03 | "Not Require Allocation" list hidden for Riso | Not Require Allocation list | hidden (Riso only) | SF |
| BR-08 | AC-03 | Hiding "Not Require Allocation" list must not affect contract list visibility | Isolation | isolated removal | SF |
| BR-09 | AC-04 | Contract list and related UI shown only for Riso; non-Riso partners unaffected | Partner scope gate | feature/partner gate | SF |
| BR-10 | AC-05 | Lesson Allocation in contract list = the LA record linked to the contract; blank if no linked LA | Lesson Allocation (in contract list) | read-only, LA-linked | SF |
| BR-11 | AC-06 | Monthly Lesson Assignment report accessible as standalone; accessible to authorized Riso HQ/CM users | Standalone report page | read-only display | SF |
| BR-12 | AC-06 | Report not exposed to non-Riso partners | Report page access | partner gate | SF |
| BR-13 | AC-07 | Filter: Month — single-select | Month filter | editable | SF |
| BR-14 | AC-07 | Filter: AY — defaults to current AY on first open | AY filter | editable, default = current AY | SF |
| BR-15 | AC-07 | Filter: Student or Contact ID — multi-select | Student/Contact ID filter | editable, multi-select | SF |
| BR-16 | AC-07 | Filter: Location — multi-select, defaults to user's assigned location | Location filter | editable, multi-select, default = user's location | SF |
| BR-17 | AC-08 | Report columns: Location, Student Name, Course, Student Course Duration Per Month, Purchased Slot, Lesson Allocated, Diff | Report column structure | read-only display | SF |
| BR-18 | AC-08 | Rows ordered by: Location, Student Name, Course, Start Date ASC | Row sort order | auto-calculated | SF |
| BR-19 | AC-08 | Row with missing field values renders without breaking the report | Row rendering with nulls | graceful empty display | SF |
| BR-20 | AC-09 | Purchased Slot: if Contract.type = Monthly or Weekly → use Contract.slot | Purchased Slot (monthly/weekly) | auto-calculated | SF |
| BR-21 | AC-09 | Purchased Slot: if Contract.type = One Time → use Contract.total | Purchased Slot (one-time) | auto-calculated | SF |
| BR-22 | AC-10 | Lesson Allocated = count of lessons for the target monthly context | Lesson Allocated | auto-calculated | SF |
| BR-23 | AC-10 | EXCLUDE from count: Attendance = Absent AND Notice != "In Advance" | Lesson Allocated exclusion | auto-calculated | SF |
| BR-24 | AC-10 | INCLUDE in count: Absent + Notice = "In Advance" (advance notice absent counts as consumed) | Lesson Allocated inclusion for advance-notice | auto-calculated | SF |
| BR-25 | AC-11 | Diff = Purchased Slot - Lesson Allocated, per row | Diff | auto-calculated | SF |
| BR-26 | AC-11 | Diff displays correctly for negative, zero, and positive values | Diff display | read-only display | SF |
| BR-27 | AC-12 | Student or Contact ID filter supports multiple values; all matching rows shown | Student/Contact ID multi-select | editable, multi-select | SF |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---|---|---|---|---|
| 1 | [CONFLICT] | epics/OOP/riso/LT-92532-riso-create-update-la-on-ui/spec.md — AC 01.9 | AC-03 | LT-92532 AC 01.9 documents Contact > Course tab showing "Require Lesson Allocation list" and "Lesson Allocation list". AC-03 of LT-98531 hides the "Not Require Allocation list". It is unclear whether the "Not Require Allocation list" is a third section or the same as one of the two documented sections. The scope of what is hidden needs confirmation against actual UI layout. |

### Missing in Requirements

| # | Tag | Source | Description |
|---|---|---|---|
| 1 | [REGRESSION RISK] | epics/OOP/riso/LT-92532-riso-create-update-la-on-ui/test-cases/create-la-ui.md | Existing TCs for LT-92532 assert the current Contact > Course tab layout for Riso; hiding "Not Require Allocation" list (AC-03) may break these assertions and require TC updates. |
| 2 | [MISSING BEHAVIOR] | Confluence PRD 2445410319 — AC-01 | Active/Inactive tab behavior when one tab has data and the other is empty is not fully specified. Also unclear whether contract list includes only contracts linked to Require_Allocation = TRUE LAs, or all contracts. |
| 3 | [MISSING BEHAVIOR] | Confluence PRD 2445410319 — AC-05 | "Lesson Allocation value from Post Contract API" does not name the specific field (LA.Total_Session_Count, LA.Purchased_Slot, or LA.Lesson_Allocated). Three different fields exist with different values. |
| 4 | [MISSING BEHAVIOR] | Confluence PRD 2445410319 — AC-07 | Month filter default value on first open is not defined. AY, Location, and Student filters have defined defaults; Month does not. Also unclear whether changing Month auto-applies or requires an Apply button. |
| 5 | [MISSING BEHAVIOR] | Confluence PRD 2445410319 — AC-08 | "Student Course Duration Per Month (Jan, Feb, March…)" column has no calculation rule defined. The Figma image in the PRD is inaccessible (blob URL). |
| 6 | [MISSING BEHAVIOR] | Confluence PRD 2445410319 — AC-09 | Mixed contract types (Monthly + One Time on same LA) and partial-month monthly contracts are not addressed. The Mobile App spec (PBT-1512 AC 01.2) has a cumulative monthly calculation rule not reflected in SF report AC-09. |
| 7 | [MISSING BEHAVIOR] | Confluence PRD 2130575378 (PBT-1512) AC 01.2 vs Confluence 2445410319 AC-10 | Mobile App explicitly excludes Cancelled lessons from Lesson Allocated; SF report AC-10 does not mention Cancelled lesson status. May be an omission. |
| 8 | [MISSING BEHAVIOR] | Confluence PRD 2445410319 — Scope section vs AC-06 | Scope says report accessible from "Contact > Course shortcut" but no AC defines the shortcut UI, pre-fill behavior, or partner scope. |
| 9 | [ROLE GAP] | scheduling-feature-permission-matrix.csv | No permission row for "View Contract List" or "Monthly Lesson Assignment Report". AC-01 and AC-06 say "HQ/CM" but Centre Staff (center_level_edit) access is undefined. Consistent with Riso OOP pattern: center_level_edit=TRUE for all existing Riso features. |
| 10 | [UNDOCUMENTED IN AC] | epics/OOP/riso/LT-98533-riso-contract-api/spec.md — LA field definitions | The report column labeled "Purchased Slot" (AC-08/09) sources from Contract records (Contract.slot or Contract.total), but LA.Purchased_Slot is a separately existing manually-entered SF field. These two values may differ. The AC does not explicitly confirm which data source feeds the report column. |

### Lesson-Learned Risks

| # | Incident | Date | AC | Risk | Guardrail |
|---|---|---|---|---|---|
| 1 | Nichibei — Student Sessions Missing LA → Points Not Deducted | 2026-03-04 | AC-10 | AC-10 defines a compound exclusion rule: Absent AND Notice != In Advance. OOP-specific compound filter conditions have historically been missing from implementations (only the primary condition is applied), causing silent miscalculation. If the Notice condition is missing, Absent+InAdvance sessions will be incorrectly excluded, inflating Diff values without any error signal. | Test all three attendance combinations independently: (1) Absent+InAdvance → INCLUDED; (2) Absent+NoNotice → EXCLUDED; (3) Present → INCLUDED. Verify all three produce correct Lesson Allocated counts. |

### E2E Scenario Impact

_None identified. No existing E2E scenarios cover Riso Contract List or Monthly Lesson Assignment Report features. No update or creation required at this time._

### Assumptions Made

- The ticket scope is the SF-side report and contact page update only (PBT-1510). The Learner App contract info and lesson history pages (Confluence 2130575378, PBT-1512) are a separate epic.
- Bucket = `OOP/riso` — Riso-only OOP feature.
- Production release date = 2026-07-13 (from Jira fix version v2026.07.13).
- Internal UAT date = 2026-06-29 (from customfield_10566 / customfield_10567 on ticket).
- Status = "Ready for QA" (Jira status verbatim).
- Report Lesson Allocated calculation uses the same formula as the Mobile App (PBT-1512 AC 01.2), based on the Confluence PRD note: "Same calculation applied in PBT-1510".
- No Figma URLs accessible in the Jira ticket directly (Figma link exists in PBT-1512 Confluence page but is for the Mobile App feature, not this SF ticket).
- Riso OOP partner gate applies to all features in this ticket — no feature flag name was specified in the ticket.

**Confirmed by user on 2026-06-22:**
- Q1 resolved: "Not Require Allocation" list is a separate section; AC-03 correctly hides it for Riso. Conflict resolved.
- Q2 confirmed: Lesson Allocated exclusion requires BOTH conditions (Absent AND Notice != InAdvance). Absent+InAdvance = INCLUDED.
- Q3 confirmed: SF report does NOT check lesson status (Cancelled lessons are NOT excluded; only attendance rule applies).
- Q4 confirmed: "Lesson Allocation" in contract list = the LA record linked to the contract (not a computed field like Total_Session_Count or Purchased_Slot).

---

## Clarification Questions

> Not posted to Jira — user confirmed answers inline on 2026-06-22; remaining items to be confirmed later.

1. **[CONFLICT] ✅ ANSWERED** AC-03 says hide the "Not Require Allocation" list from Contact > Course tab for Riso. Is "Not Require Allocation list" a THIRD section or the same as one of the two documented sections in LT-92532?
   **Answer:** It is a separate section. AC-03 is correct — hide the "Not Require Allocation" list on Riso. Conflict resolved.

2. **[LESSON-LEARNED RISK] ✅ ANSWERED** For a session where Attendance = Absent AND Notice = "In Advance" — is that session included (correct) or excluded?
   **Answer:** BOTH conditions must be met to exclude. Session with Absent + InAdvance = **INCLUDED** (correct). Implementation must apply the AND compound rule.

3. **[MISSING BEHAVIOR] ✅ ANSWERED** Should the SF report also exclude Cancelled lessons from Lesson Allocated?
   **Answer:** No — lesson status is NOT checked. Only the attendance exclusion rule (Absent AND Notice != InAdvance) applies.

4. **[MISSING BEHAVIOR] ✅ ANSWERED** AC-05 Lesson Allocation in contract list — which specific field (LA.Total_Session_Count, LA.Purchased_Slot, or LA.Lesson_Allocated)?
   **Answer:** The Lesson Allocation displayed is the **LA record linked to the contract** (the LA associated with the Contract record, not a derived field).

5. **[MISSING BEHAVIOR] ⏳ PENDING** Mixed contract types (Monthly + One Time on same LA same month) — behavior? And: cumulative formula like Mobile or per-month value?

6. **[MISSING BEHAVIOR] ⏳ PENDING** Month filter default on first open? Auto-apply or requires Apply button?

7. **[MISSING BEHAVIOR] ⏳ PENDING** "Student Course Duration Per Month (Jan…Dec)" column — what data/formula?

8. **[MISSING BEHAVIOR] ⏳ PENDING** "Contact > Course shortcut" — UI details, pre-fill behavior, Riso scope?

9. **[ROLE GAP] ⏳ PENDING** Should Centre Staff (center_level_edit) have access? Riso pattern is center_level_edit=TRUE for all Riso features.

10. **[MISSING BEHAVIOR] ⏳ PENDING** Contract list — all contracts for AY, or only those linked to LAs with Require_Allocation = TRUE?

---

## Related Specs

- `epics/OOP/riso/LT-98533-riso-contract-api/spec.md` — Riso Contract API (POST/PATCH/logical delete); LT-98531 UI reads data created by this API. Contract field definitions and LA aggregation rules in LT-98533 are the authoritative source for understanding what data is displayed in LT-98531.
- `epics/OOP/riso/LT-92532-riso-create-update-la-on-ui/spec.md` — Riso manual LA creation on UI; LT-98531 AC-03 hides the "Not Require Allocation" list which exists on the Contact > Course tab managed by this spec.
- `epics/OOP/riso/LT-96673-monthly-lesson-count-add-teacher-popup/spec.md` — Monthly Lesson Count for teachers on SF; separate from this feature (teacher count vs student lesson allocated count) but shares the "monthly context" concept.

## Related Test Cases

- `epics/OOP/riso/LT-92532-riso-create-update-la-on-ui/test-cases/create-la-ui.md` — **REGRESSION RISK** — TCs that assert Contact > Course tab layout may need updating when "Not Require Allocation" list is hidden for Riso.
- `epics/OOP/riso/LT-92532-riso-create-update-la-on-ui/test-cases/la-auto-calculation.md` — TCs for Total Session Count auto-calculation from contracts; relevant as source of truth for what contract data is available to display.
- `epics/OOP/riso/LT-98533-riso-contract-api/test-cases/post-contract-la-link.md` — Contract creation TCs that generate the data consumed by LT-98531 UI.

## QASE Coverage Gaps

- AC-01 — Contract List Display (new feature; no existing Qase cases)
- AC-01 — Active tab vs Inactive tab distinction (new feature)
- AC-02 — Contract list sort order (new feature)
- AC-03 — "Not Require Allocation" list hidden for Riso; existing tests may need update
- AC-04 — Riso-only scope gate for contract list (non-Riso partners unaffected)
- AC-05 — Lesson Allocation value from API in contract list (new feature)
- AC-06 — Standalone Monthly Lesson Assignment report page (new feature)
- AC-07 — Report filter defaults and behavior (new feature)
- AC-08 — Report column structure including "Student Course Duration Per Month" (new feature; definition unclear — Q7)
- AC-09 — Purchased Slot calculation by contract type (new feature)
- AC-10 — Lesson Allocated calculation with attendance exclusion rule (new feature; lesson-learned risk)
- AC-11 — Diff formula including negative/zero/positive values (new feature)
- AC-12 — Multi-student selection in report (new feature)
