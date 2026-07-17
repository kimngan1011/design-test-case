# Test Coverage: LT-98531 — [Riso] OOP | Contract vs Lesson Assigned Report

**Jira:** https://manabie.atlassian.net/browse/LT-98531
**Date:** 2026-06-22

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|------|---|
| BR-01 | AC-01 | Contact > Course tab displays contract list for current AY for Riso users |
| BR-02 | AC-01 | Contract list columns: Lesson Allocation, Course, Start Date, End Date, Location, Contract Status |
| BR-03 | AC-01 | Empty state shown (no error) when no contracts exist for the contact |
| BR-04 | AC-01 | Active tab: contracts for current AY |
| BR-05 | AC-01 | Inactive tab: contracts for previous AYs |
| BR-06 | AC-02 | Sort: Location ASC → Course ASC → Start Date ASC; applied on every load/refresh |
| BR-07 | AC-03 | "Not Require Allocation" list hidden for Riso |
| BR-08 | AC-03 | Hiding "Not Require Allocation" list must not affect contract list visibility |
| BR-09 | AC-04 | Contract list and related UI shown only for Riso; non-Riso partners unaffected |
| BR-10 | AC-05 | Lesson Allocation in contract list = the LA record linked to the contract; blank if no linked LA |
| BR-11 | AC-06 | Monthly Lesson Assignment report accessible as standalone; accessible to authorized Riso HQ/CM users |
| BR-12 | AC-06 | Report not exposed to non-Riso partners |
| BR-13 | AC-07 | Filter: Month — single-select |
| BR-14 | AC-07 | Filter: AY — defaults to current AY on first open |
| BR-15 | AC-07 | Filter: Student or Contact ID — multi-select |
| BR-16 | AC-07 | Filter: Location — multi-select, defaults to user's assigned location |
| BR-17 | AC-08 | Report columns: Location, Student Name, Course, Student Course Duration Per Month, Purchased Slot, Lesson Allocated, Diff |
| BR-18 | AC-08 | Rows ordered by: Location, Student Name, Course, Start Date ASC |
| BR-19 | AC-08 | Row with missing field values renders without breaking the report |
| BR-20 | AC-09 | Purchased Slot: if Contract.type = Monthly or Weekly → use Contract.slot |
| BR-21 | AC-09 | Purchased Slot: if Contract.type = One Time → use Contract.total |
| BR-22 | AC-10 | Lesson Allocated = count of lessons for the target monthly context |
| BR-23 | AC-10 | EXCLUDE from count: Attendance = Absent AND Notice != "In Advance" |
| BR-24 | AC-10 | INCLUDE in count: Absent + Notice = "In Advance" (advance-notice absent counts as consumed) |
| BR-25 | AC-11 | Diff = Purchased Slot - Lesson Allocated, per row |
| BR-26 | AC-11 | Diff displays correctly for negative, zero, and positive values |
| BR-27 | AC-12 | Student or Contact ID filter supports multiple values; all matching rows shown |

---

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC-01 | BR-01, BR-02, BR-03, BR-04, BR-05 | Display completeness, Conditional logic |
| AC-02 | BR-06 | Ordering / Sort |
| AC-03 | BR-07, BR-08 | Conditional logic, Data integrity |
| AC-04 | BR-09 | Permission logic |
| AC-05 | BR-10 | Display completeness, Conditional logic |
| AC-06 | BR-11, BR-12 | Permission logic |
| AC-07 | BR-13, BR-14, BR-15, BR-16 | Conditional logic, Validation logic |
| AC-08 | BR-17, BR-18, BR-19 | Display completeness, Ordering / Sort |
| AC-09 | BR-20, BR-21 | Conditional logic, Boundary/range logic |
| AC-10 | BR-22, BR-23, BR-24 | Conditional logic, Boundary/range logic |
| AC-11 | BR-25, BR-26 | Boundary/range logic, Display completeness |
| AC-12 | BR-27 | Validation logic, Display completeness |

---

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Display completeness | Component (enumerate all required fields; one TC asserts all simultaneously), Negative (field absent / blank state) |
| Conditional logic | Decision Table (input combinations → outcomes), Negative (condition not met → alternate branch) |
| Ordering / Sort | Scenario (2+ items differing on sort key; explicit order assertion), Pairwise (multi-criteria: Location × Course × Start Date) |
| Permission logic | Permission Matrix (one row per role × action), Decision Table (Riso vs non-Riso partner gate) |
| Validation logic | Equivalence Partitioning (valid/invalid partition), Negative (empty/null input) |
| Boundary/range logic | Boundary Value Analysis (negative/zero/positive Diff; contract type variants), Decision Table (all contract type branches) |
| Data integrity | Regression (validate existing LT-92532 TCs still pass after AC-03 change), Negative (isolation: contract list unaffected by hiding NRA list) |
| Cross-system impact | Regression (Contact > Course tab still renders correctly after UI change) |

---

## 4. Structured Coverage Strategy

> **Pending questions note:** Q5–Q10 remain open. Rows affected are annotated with ⏳ and coverage is written for what IS defined. Pending items will require additional rows when resolved.

> **H.1 — N/A:** Figma URL in spec is inaccessible (blob URL). Spec–Figma mismatch check cannot be performed. No 🔴/🟡 rows to surface.

### Display & Ordering Inventory

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| Contact > Course tab — Contract List | Lesson Allocation, Course, Start Date, End Date, Location, Contract Status | Active tab (current AY) / Inactive tab (previous AYs); Lesson Allocation blank if no linked LA | Location ASC → Course ASC → Start Date ASC | Empty state message (text TBD — Q pending) |
| Monthly Lesson Assignment Report | Location, Student Name, Course, Student Course Duration Per Month, Purchased Slot, Lesson Allocated, Diff | Purchased Slot: Monthly/Weekly → slot; One Time → total; Diff can be negative/zero/positive; Row with missing values still renders | Location ASC → Student Name ASC → Course ASC → Start Date ASC | None confirmed |

### Downstream Effects Inventory

> This feature is read-only UI — it reads Contract and LA records but does not write/create/delete any entity. No downstream write effects apply. Section G — N/A: No CRUD/state-change actions are initiated by this feature. The only "write-adjacent" risk is AC-03 (hiding NRA list): this is a UI presentation change, not a data write. No counter fields, child records, or flag flips are triggered.

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner |
|---|---|---|---|
| AC-03: Hide NRA list (UI change) | "Not Require Allocation" list no longer rendered | Contact > Course tab (SF) | TC in contract-list.md |
| AC-03: Hide NRA list | Contract list (new) still renders correctly | Contact > Course tab (SF) | TC in contract-list.md (isolation check) |
| AC-03: Hide NRA list | LT-92532 existing TCs that assert NRA list presence may fail | LT-92532 test cases | Regression TCs flagged in gap analysis |

### Coverage Strategy Table

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC-01 | Contract list displayed on Contact > Course tab (Active tab, current AY) | Display completeness | Component | High | Standard |
| AC-01 | Contract list columns: Lesson Allocation, Course, Start Date, End Date, Location, Contract Status — all present simultaneously | Display completeness | Component | High | Deep |
| AC-01 | Empty state: no contracts for contact → empty state shown, no error | Display completeness | Negative | Medium | Standard |
| AC-01 | Active tab shows current-AY contracts only | Conditional logic | Decision Table | Medium | Standard |
| AC-01 | Inactive tab shows previous-AY contracts only | Conditional logic | Decision Table | Medium | Standard |
| AC-01 | Active tab has data, Inactive tab is empty → both tabs render without error; and vice versa | Conditional logic | Negative | Medium | Standard |
| AC-02 | Sort: Location ASC → Course ASC → Start Date ASC — applied on load | Ordering / Sort | Scenario | Medium | Standard |
| AC-02 | Sort tiebreaker: same Location and Course → ordered by Start Date ASC | Ordering / Sort | Pairwise | Medium | Standard |
| AC-02 | Sort applied on refresh (not just initial load) | Ordering / Sort | Scenario | Medium | Standard |
| AC-03 | "Not Require Allocation" list is hidden on Contact > Course tab for Riso | Conditional logic | Decision Table | High | Standard |
| AC-03 | Hiding NRA list does not affect contract list display (isolation) | Data integrity | Negative | High | Standard |
| AC-03 | REGRESSION: Existing LT-92532 TCs asserting Contact > Course tab layout — NRA section no longer present | Data integrity | Regression | High | Standard |
| AC-04 | Contract list and UI changes shown only for Riso partner | Permission logic | Permission Matrix | High | Standard |
| AC-04 | Non-Riso partner: no contract list rendered on Contact > Course tab | Permission logic | Negative | High | Standard |
| AC-04 | ⏳ Pending Q9: Centre Staff (center_level_edit) access to contract list — assumption: same pattern as other Riso features (center_level_edit=TRUE) | Permission logic | Permission Matrix | High | Standard |
| AC-05 | Lesson Allocation column shows the LA record linked to the contract | Display completeness | Component | Medium | Standard |
| AC-05 | Lesson Allocation blank when no LA linked to the contract | Conditional logic | Negative | Medium | Standard |
| AC-06 | Monthly Lesson Assignment report accessible as standalone page for Riso HQ/CM | Permission logic | Permission Matrix | High | Standard |
| AC-06 | Report not accessible for non-Riso partner | Permission logic | Negative | High | Standard |
| AC-06 | ⏳ Pending Q9: Centre Staff access to standalone report (assumption: center_level_edit=TRUE per Riso pattern) | Permission logic | Permission Matrix | High | Standard |
| LBAC | Contract List: staff sees only contracts at their assigned location(s) | Permission logic | Permission Matrix | High | Standard |
| LBAC | Contract List: staff cannot see contracts from unassigned location | Permission logic | Negative | High | Standard |
| LBAC | Monthly Report: report returns only data for user's assigned location | Permission logic | Permission Matrix | High | Standard |
| LBAC | Monthly Report: changing Location filter cannot expose data from unassigned location | Permission logic | Negative | Critical | Deep |
| AC-06 | ⏳ Pending Q8: "Contact > Course shortcut" to report — UI and pre-fill behavior not yet defined; skip shortcut coverage until confirmed | Conditional logic | — | Medium | — |
| AC-07 | Filter: AY defaults to current AY on first open | Conditional logic | Decision Table | Medium | Standard |
| AC-07 | Filter: Location defaults to user's assigned location on first open | Conditional logic | Decision Table | Medium | Standard |
| AC-07 | Filter: Student/Contact ID is multi-select | Validation logic | Equivalence Partitioning | Medium | Standard |
| AC-07 | Filter: Location is multi-select | Validation logic | Equivalence Partitioning | Medium | Standard |
| AC-07 | ⏳ Pending Q6: Month filter default on open not defined; no coverage for Month default until confirmed | Conditional logic | — | Medium | — |
| AC-07 | Filter: changing AY updates report data scope | Conditional logic | Decision Table | Medium | Standard |
| AC-07 | Filter: clearing all students (empty multi-select) — behavior | Validation logic | Negative | Medium | Standard |
| AC-08 | Report columns all present: Location, Student Name, Course, Student Course Duration Per Month, Purchased Slot, Lesson Allocated, Diff | Display completeness | Component | High | Deep |
| AC-08 | Row sort: Location ASC → Student Name ASC → Course ASC → Start Date ASC | Ordering / Sort | Scenario | Medium | Standard |
| AC-08 | Row with missing/null field values renders without breaking the report | Display completeness | Negative | Medium | Standard |
| AC-08 | ⏳ Pending Q7: "Student Course Duration Per Month" column formula not defined; column presence verified by Component TC; calculation coverage deferred |Display completeness | Component | Medium | Smoke |
| AC-09 | Purchased Slot: Contract.type = Monthly → uses Contract.slot | Conditional logic | Decision Table | High | Standard |
| AC-09 | Purchased Slot: Contract.type = Weekly → uses Contract.slot | Conditional logic | Decision Table | High | Standard |
| AC-09 | Purchased Slot: Contract.type = One Time → uses Contract.total | Conditional logic | Decision Table | High | Standard |
| AC-09 | All three contract type branches in one multi-student report view | Conditional logic | Pairwise | High | Deep |
| AC-09 | ⏳ Pending Q5: Mixed contract types (Monthly + One Time on same LA) — behavior not defined; coverage deferred | Conditional logic | — | High | — |
| AC-10 | Lesson Allocated: Attendance = Absent AND Notice != "In Advance" → session EXCLUDED (compound exclusion) | Conditional logic | Decision Table | Critical | Deep |
| AC-10 | Lesson Allocated: Attendance = Absent AND Notice = "In Advance" → session INCLUDED (advance-notice absent) | Conditional logic | Decision Table | Critical | Deep |
| AC-10 | Lesson Allocated: Attendance = Present → session INCLUDED | Conditional logic | Decision Table | Critical | Deep |
| AC-10 | Compound rule: all three attendance combinations tested independently in same report context | Conditional logic | Decision Table | Critical | Deep |
| AC-10 | Cancelled lesson (lesson status = Cancelled) is NOT excluded from Lesson Allocated (Q3 confirmed) | Conditional logic | Negative | High | Standard |
| AC-10 | ⏳ Assumption: Lesson Allocated uses same formula as Mobile App (PBT-1512 AC 01.2); to be confirmed if formula diverges | Conditional logic | — | High | — |
| AC-11 | Diff = Purchased Slot − Lesson Allocated, per row | Boundary/range logic | Boundary Value Analysis | Medium | Standard |
| AC-11 | Diff positive: Purchased Slot > Lesson Allocated | Boundary/range logic | Boundary Value Analysis | Medium | Standard |
| AC-11 | Diff zero: Purchased Slot = Lesson Allocated | Boundary/range logic | Boundary Value Analysis | Medium | Standard |
| AC-11 | Diff negative: Purchased Slot < Lesson Allocated | Boundary/range logic | Boundary Value Analysis | Medium | Standard |
| AC-12 | Student/Contact ID filter: select multiple students → all matching rows shown | Validation logic | Equivalence Partitioning | Medium | Standard |
| AC-12 | Multi-student: rows for each student shown under same filter context; one per student-course combination | Display completeness | Component | Medium | Standard |
| AC-12 | ⏳ Pending Q10: Contract list limited to LAs with Require_Allocation = TRUE only, or all contracts? Coverage for this distinction deferred | Conditional logic | — | Medium | — |
| TZ | AC-10 — Lesson Allocated month-end boundary: session at 23:30 JST on last day of month counted in JST month, not UTC next-day month | Timezone boundary | Boundary Value Analysis | High | Standard |
| TZ | AC-10 — Lesson Allocated month-start boundary: session at 00:00 JST on first day of month counted in new JST month, not prior UTC date | Timezone boundary | Boundary Value Analysis | High | Standard |
| TZ | AC-10 — Session stored in UTC assigned to correct month after JST conversion (UTC ≠ JST date for sessions near midnight) | Timezone boundary | Boundary Value Analysis | High | Standard |
| TZ | AC-07 BR-14 — AY filter default: N/A for time-boundary check — AY is determined by the "Is Current AY" checkbox on the AY record, not by the current date/time; no midnight-boundary TC needed | Timezone boundary | N/A (skip) | — | — |
| TZ | AC-07 BR-13 — Month filter (if defaulted) shows JST month, not UTC month, at midnight JST boundary | Timezone boundary | Boundary Value Analysis | Medium | Standard |
| TZ | AC-01 BR-04/05 — Active/Inactive tab AY classification: N/A for time-boundary check — classification is driven by the "Is Current AY" checkbox, not by current date/time | Timezone boundary | N/A (skip) | — | — |
| TZ | AC-01 BR-02 — Contract Start Date and End Date displayed in JST, not raw UTC; UTC 2025-03-31T15:00Z must show as 2025-04-01 JST | Timezone boundary | Component | High | Standard |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| AC-10 — Lesson Allocated compound exclusion rule (BR-23, BR-24) | Lesson-Learned Risk pattern (Nichibei 2026-03-04): OOP compound filter conditions have historically been implemented with only the primary condition, causing silent miscalculation. If the Notice != "In Advance" check is missing, Absent+InAdvance sessions will be incorrectly excluded, inflating Diff values with no error signal. | Test all three attendance combinations independently: (1) Absent + In Advance → INCLUDED; (2) Absent + no/other notice → EXCLUDED; (3) Present → INCLUDED. Verify all three produce correct Lesson Allocated counts in the same report run. Use a controlled data set with exactly one session per branch. |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| AC-09 — Purchased Slot calculation by contract type (BR-20, BR-21) | Silent calculation error if wrong field used (Contract.slot vs Contract.total). Three contract types must each resolve to correct formula; no UI error if wrong value shown. | Decision Table with all three types (Monthly, Weekly, One Time). Include a pairwise test with all three in one report view. Verify against Contract API data (LT-98533). |
| AC-03 — Hiding "Not Require Allocation" list (BR-07, BR-08) | Regression risk: LT-92532 Contact > Course tab TCs assert NRA section is present. Hiding it for Riso breaks those assertions. Isolation risk: hiding NRA must not remove the new contract list section. | Regression test: open Contact > Course tab as Riso user → NRA list absent, contract list present. Run against LT-92532 TCs to identify which assertions require update. |
| AC-04 / AC-06 — Partner scope gate (BR-09, BR-12) | Non-Riso partners must not see contract list or report page. Partner gate failure exposes Riso-only data to all partners. | Permission Matrix: test at least one non-Riso partner user account. Verify route/page is inaccessible, not just hidden from nav. |
| AC-10 — Cancelled lesson NOT excluded (Q3 confirmed) | SF report does not filter by lesson status. If implementation adds a status filter (common mistake given Mobile App excludes Cancelled), Cancelled lessons would be incorrectly removed, underreporting Lesson Allocated. | Explicit TC: create a Cancelled lesson for the student and month under test; verify Lesson Allocated count includes it. |
| AC-01 — Contract List display completeness (BR-01, BR-02) | All six required columns must be present simultaneously. Missing any column would cause incomplete monitoring data for HQ/CM users. | Component TC asserting all six columns present in a single view; include a row with data for every column. |
| TZ — JST vs UTC boundary gaps (AC-10, AC-07 BR-13, AC-01 BR-02) | Riso is JST (UTC+9). Session timestamps for Lesson Allocated and contract date display are evaluated relative to JST. If the implementation uses raw UTC for month boundary checks, lessons near midnight JST will be counted in the wrong month. AY classification (Active/Inactive tab) and AY filter default are NOT time-based — both are driven by the "Is Current AY" checkbox, so no midnight-boundary risk applies there. Contract Start/End Date display must render in JST. Japan has no DST so only the fixed UTC+9 offset matters. | Use TZ-01 (month-end boundary), TZ-02 (month-start boundary), TZ-03 (UTC storage vs JST display), TZ-06 (Month filter JST boundary if default exists), TZ-08 (contract date display in JST). TZ-04/TZ-05/TZ-07 are N/A and removed. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| AC-07 — Filter defaults on first open (BR-14, BR-16) | If AY or Location defaults are wrong, users see incorrect data scope without noticing. Month filter default is undefined (Q6 pending). | Smoke TC: open report fresh, observe AY = current AY and Location = user's location without any user action. |
| AC-08 — Report column structure (BR-17, BR-19) | Missing column or null-value row crash would break the report for HQ/CM operations monitoring. "Student Course Duration Per Month" formula is still undefined (Q7 pending). | Component TC enumerating all seven columns; negative TC with a student-course row missing optional data fields. |
| AC-11 — Diff formula display (BR-25, BR-26) | Negative Diff values must render correctly (e.g., no absolute value applied, no blank substitution). | BVA: three TCs — positive/zero/negative Diff. Assert sign and value for each. |
| AC-02 — Sort order on every load/refresh (BR-06) | Silent sort bug would cause list to appear shuffled after refresh, degrading usability. | Scenario TC with 3+ contracts differing on Location then Course then Start Date. Refresh and re-verify order. |
| AC-12 — Multi-student filter (BR-27) | Multi-select edge case: large student sets may cause performance or display truncation. | Standard scenario with 2–3 students; ensure all rows appear with correct student-course grouping. |

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| AC-01 — Contract List Display (Contact > Course tab) | None in LT-98531; LT-92532 TCs cover Require Lesson Allocation table only | No overlap | ✅ New: contract list columns, Active/Inactive tab, empty state |
| AC-02 — Contract List Sort Order | None | None | ✅ New: sort scenario with multi-criteria data |
| AC-03 — Hide "Not Require Allocation" list | LT-92532/create-la-ui.md: asserts Require Lesson Allocation table in Contact > Course tab; does NOT assert NRA list presence (no NRA-specific TCs found in LT-92532) | None directly; indirect regression via Contact > Course tab layout assertions | ✅ New: NRA hidden for Riso TC; regression check on LT-92532 TCs that reference Contact > Course tab layout |
| AC-03 — Isolation (contract list unaffected by NRA hide) | None | None | ✅ New: isolation TC |
| AC-04 — Riso-only partner gate (contract list) | None | None | ✅ New: permission matrix TC (Riso user sees list; non-Riso does not) |
| AC-05 — Lesson Allocation value (linked LA) | LT-92532/la-auto-calculation.md: covers Total Session Count auto-calculation from contracts (source understanding) | Indirect only — source data context | ✅ New: contract list shows linked LA name/record; blank if no LA |
| AC-06 — Standalone report access + Riso scope | None | None | ✅ New: report accessible as Riso HQ/CM; inaccessible to non-Riso |
| AC-07 — Filter defaults and behavior | None | None | ✅ New: AY default, Location default, multi-select Student, multi-select Location; Month default deferred (Q6) |
| AC-08 — Report column structure | None | None | ✅ New: Component TC for all seven columns; null-row render TC |
| AC-09 — Purchased Slot by contract type | LT-98533/post-contract-la-link.md and la-aggregation-post.md: cover contract creation; relevant as upstream data setup | Source data context only | ✅ New: Decision Table for Monthly/Weekly/One Time contract type → correct field used |
| AC-10 — Lesson Allocated compound exclusion | None | None | ✅ New: three attendance-branch TCs (Absent+InAdvance INCLUDED; Absent+NoNotice EXCLUDED; Present INCLUDED); Cancelled-lesson-not-excluded TC |
| AC-11 — Diff formula (negative/zero/positive) | None | None | ✅ New: BVA for negative, zero, positive Diff values |
| AC-12 — Multi-student filter | None | None | ✅ New: multi-select scenario with 2–3 students |

---

## 7. Mandatory Edge-Case Checklist Summary

### Section A — Configuration-driven thresholds
**N/A.** No tenant/partner config thresholds (advance days, capacity, cancellation deadline) appear in the BRs. The Riso partner gate is a static feature flag, not a configurable threshold.

### Section B — Date / Time logic
**YES — Covered (revised 2026-06-23):**
- AC-01 "current AY" and AC-07 "current AY default" depend on date context. Every TC involving AY filtering must declare `today = YYYY-MM-DD` in test data.
- Month filter (AC-07, BR-13) involves date context. TCs must specify `target_month = YYYY-MM`.
- **Timezone scope confirmed:** Riso operates in JST (UTC+9). DST does not apply (Japan has no DST). JST vs UTC boundary gaps apply only to time-based calculations:
  - **Lesson Allocated month assignment (AC-10):** A session at 23:30 JST on the last day of a month stores as UTC next calendar day. If month boundary uses UTC instead of JST, the session is miscounted into the wrong month. → Covered by TZ-01 (month-end boundary), TZ-02 (month-start boundary), TZ-03 (UTC storage vs JST display).
  - **AY filter default (AC-07 BR-14):** **N/A for timezone check.** The "current AY" is determined by the **"Is Current AY" checkbox** on the AY record, not by comparing the current date/time against an AY start date. No midnight-boundary risk applies.
  - **Month filter context (AC-07 BR-13):** If a month default is implemented, it must reflect JST month not UTC month. → Covered by TZ-06.
  - **Contract Active/Inactive tab AY classification (AC-01 BR-04/05):** **N/A for timezone check.** Active/Inactive tab classification is driven by the "Is Current AY" checkbox, not by the current date/time. No midnight-boundary risk applies.
  - **Contract Start Date / End Date display (AC-01 BR-02):** Dates must render in JST. → Covered by TZ-08.

### Section C — Concurrent / stale state
**N/A.** This feature is read-only. No bookings, seats, or shared resources are modified. No stale-cache or double-submit risks apply.

### Section D — Permission & role
**YES — covered in Coverage Strategy:**
- AC-04 and AC-06: Riso vs non-Riso partner gate tested (Permission Matrix rows).
- HQ and CM roles: both can access contract list and report (per AC-01, AC-06).
- Centre Staff (center_level_edit): Q9 pending — assumption: TRUE per Riso pattern. TC flagged.
- Cross-tenant: non-Riso user cannot access Riso-only surfaces (covered by non-Riso negative TCs).
- Feature flag OFF: N/A — no feature flag name specified; partner gate is structural.
- **LBAC (Location-Based Access Control):** ✅ Confirmed applies — staff can only view contracts and report data for their assigned location(s). Four TCs added: (1) contract list shows only assigned-location contracts; (2) contract list hides unassigned-location contracts; (3) report returns only assigned-location data; (4) changing Location filter cannot bypass data-layer restriction. Covered in contract-list.md (23254, 23255) and monthly-report-access-filters.md (23256, 23257).

### Section E — State transition
**N/A.** No entity changes state via this feature. Contract Status is displayed read-only; no transitions are triggered.

### Section F — Cross-system / cross-surface
**Partial.** Feature reads from Contract (LT-98533) and LA (LT-92532) records:
- Contract data created via LT-98533 API must surface correctly in the LT-98531 UI → one integration-level TC confirming the pipeline (post contract via API → contract appears in Contact > Course tab).
- No cross-system writes. No Surface 2 sync-fail scenario.

### Section G — Downstream effects
**N/A.** Feature is read-only. No CREATE/UPDATE/DELETE actions. AC-03 (hide NRA list) is a UI presentation change only — no data records written or deleted. Downstream Effects Inventory populated in Section 4 covers the isolated regression risk.

### Section H — Display completeness & ordering
**YES — fully covered:**
- Display & Ordering Inventory completed in Section 4.
- Contract list: Component TC for all 6 columns; Scenario TC for sort; Negative TC for empty state.
- Report: Component TC for all 7 columns; Scenario TC for sort; Negative TC for null-value rows.
- Pagination: N/A — AC does not define pagination limits. If large result sets are discovered during testing, add scroll/pagination TC.

### Section H.1 — Spec–Figma mismatch
**N/A.** Figma URL in spec is inaccessible (blob URL). Spec–Figma mismatch check cannot be performed. No 🔴/🟡 rows surfaced.

---

## 8. Suggested Test Suite Structure

```
epics/OOP/riso/LT-98531-riso-contract-lesson-report/test-cases/
├── contract-list.md
│     → AC-01: Contract list display, columns, Active/Inactive tabs, empty state
│     → AC-02: Contract list sort order (Location → Course → Start Date)
│     → AC-03: NRA list hidden for Riso; isolation (contract list unaffected); regression flag
│     → AC-04: Riso-only partner gate for contract list
│     → AC-05: Lesson Allocation value (linked LA; blank if no LA)
│
├── monthly-report-access-filters.md
│     → AC-06: Standalone report access (Riso HQ/CM); non-Riso blocked
│     → AC-07: Filter defaults (AY, Location); multi-select behavior (Student, Location)
│
├── monthly-report-calculations.md
│     → AC-08: Report column structure; row sort order; null-value row rendering
│     → AC-09: Purchased Slot by contract type (Monthly/Weekly → slot; One Time → total)
│     → AC-10: Lesson Allocated compound exclusion (3 attendance branches); Cancelled lesson included
│     → AC-11: Diff formula (positive/zero/negative values)
│
└── monthly-report-multi-student.md
      → AC-12: Multi-student filter behavior; rows for all matching students shown
```

---

## Open Items (Pending Q5–Q10)

| # | Question | Affected AC/BR | Coverage Impact |
|---|---|---|---|
| Q5 | Mixed contract types (Monthly + One Time on same LA same month) — which Purchased Slot formula applies? | AC-09, BR-20/21 | Additional Decision Table row needed once resolved |
| Q6 | Month filter default on first open — not defined. Auto-apply or Apply button? | AC-07, BR-13 | Month default TC deferred; apply-button flow TC deferred |
| Q7 | "Student Course Duration Per Month (Jan…Dec)" column formula not defined | AC-08, BR-17 | Column presence covered by Component TC; calculation coverage deferred |
| Q8 | "Contact > Course shortcut" — UI, pre-fill behavior, Riso scope not in AC | AC-06 | Shortcut TC deferred until defined |
| Q9 | Centre Staff (center_level_edit) access to contract list and report | AC-04, AC-06 | Permission Matrix rows included with assumption (TRUE); update when confirmed |
| Q10 | Contract list: all contracts for AY, or only those linked to LAs with Require_Allocation = TRUE? | AC-01, BR-01 | Contract list TC currently assumes all contracts for AY; add filter TC if TRUE-only confirmed |
