# Test Coverage: LT-92533 — Riso Compensation Ratio in Lesson Management

**Jira:** https://manabie.atlassian.net/browse/LT-92533  
**Date:** 2026-09-11  
**Scope decision:** PRD wins over the supplied UI screenshots.

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|---|---|
| BR-01 | AC 01.1 | Compensation Ratio is available only for Riso. |
| BR-02 | AC 01.1 | The field label is `Compensation Ratio` and its data type is a Global Picklist. |
| BR-03 | AC 01.1 | `100%` is an allowed value. |
| BR-04 | AC 01.1 | `60%` is an allowed value. |
| BR-05 | AC 01.2 | New Lesson defaults Compensation Ratio to `100%`. |
| BR-06 | AC 01.2 | The field is optional; users can clear and save a blank value. |
| BR-07 | AC 01.2 | Recurring creation applies the first lesson's value to every created occurrence. |
| BR-08 | AC 01.2 | CSV imports valid and blank rows; invalid values reject only that row with a row-level correction/retry outcome. |
| BR-09 | AC 01.2 | A blank or undefined CSV value creates the lesson with `100%`. |
| BR-10 | AC 01.3 | Edit Lesson can update only the selected occurrence. |
| BR-11 | AC 01.3 | This-and-following updates eligible occurrences and skips Completed and Cancelled ones. |
| BR-12 | AC 01.3 | Bulk edit updates eligible selected lessons and skips selected Completed and Cancelled lessons. |
| BR-13 | AC 01.3 | Bulk edit never propagates a changed value to following occurrences. |
| BR-14 | AC 01.4 | Lesson List displays the field; historical lessons display blank. |
| BR-15 | AC 01.4 | Lesson Detail displays the field; historical lessons display blank. |
| BR-16 | AC 01.4 | Calendar detail drawer displays the field; historical lessons display blank. |

---

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC 01.1 | BR-01 | Conditional, Permission |
| AC 01.1 | BR-02–BR-04 | Validation, Display completeness |
| AC 01.2 | BR-05–BR-06 | Validation, Conditional, Data integrity |
| AC 01.2 | BR-07 | Recurrence, Data integrity |
| AC 01.2 | BR-08–BR-09 | Validation, Data integrity, Conditional |
| AC 01.3 | BR-10 | Recurrence, Data integrity |
| AC 01.3 | BR-11 | Recurrence, State transition, Conditional, Data integrity |
| AC 01.3 | BR-12–BR-13 | Conditional, State transition, Data integrity, Recurrence |
| AC 01.4 | BR-14–BR-16 | Display completeness, Cross-system impact, Conditional |

---

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Validation | Equivalence Partitioning; Negative |
| Conditional | Decision Table; Negative |
| Permission | Permission Matrix; Decision Table |
| Data integrity | CRUD; Regression; Decision Table |
| Recurrence | State Transition; Regression |
| State transition | State Transition; CRUD |
| Cross-system impact | Regression; CRUD |
| Display completeness | Component; Negative |

---

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC 01.1 | Riso users can access the field; non-Riso tenants cannot access or persist it. | Conditional, Permission | Permission Matrix, Decision Table | High | Deep |
| AC 01.1 | The UI uses the exact label `Compensation Ratio` and permits `100%`, `60%`, and `発生しない`; `NA` is excluded. | Validation, Display completeness | Equivalence Partitioning, Negative, Component | High | Deep |
| User-directed expansion | Each LT-94111 Lesson Upsert entry point opens the PRD-compliant field; the two BO flows are provisional pending product confirmation. | Entry-point regression, Conditional | Scenario, Component, CRUD | High | Standard |
| AC 01.2 | New Lesson shows `100%` by default; user can retain it, choose `60%` or `発生しない`, or clear and save blank. | Validation, Conditional, Data integrity | Equivalence Partitioning, CRUD | High | Deep |
| AC 01.2 | A recurring series inherits the first lesson's ratio, including a deliberately blank value. | Recurrence, Data integrity | State Transition, Regression | High | Deep |
| AC 01.2 | CSV imports explicit `100%`/`60%` and blank rows; blank values persist as `100%`. | Validation, Data integrity | Equivalence Partitioning, CRUD | Critical | Deep |
| AC 01.2 | CSV mixed files continue valid/blank rows while rejecting each invalid row with a row-level error and correction/retry path. | Validation, Data integrity | Decision Table, Negative, Regression | Critical | Deep |
| AC 01.3 | Editing Only this lesson changes its value without changing adjacent recurring occurrences. | Recurrence, Data integrity | State Transition, Regression | High | Deep |
| AC 01.3 | This-and-following changes eligible selected/following occurrences while retaining prior, Completed, and Cancelled occurrences. | Recurrence, State transition, Conditional | State Transition, Regression | High | Deep |
| AC 01.3 | Bulk edit changes eligible selected lessons and skips selected Completed/Cancelled lessons. | Conditional, State transition, Data integrity | Decision Table, Regression | High | Deep |
| AC 01.3 | Bulk editing a recurring occurrence does not alter unselected following occurrences. | Recurrence, Data integrity | State Transition, Regression | High | Deep |
| AC 01.4 | Lesson List presents `Compensation Ratio` and its persisted value; a legacy lesson presents a blank value. | Display completeness, Conditional | Component, Negative | Medium | Standard |
| AC 01.4 | Lesson Detail presents `Compensation Ratio` and its persisted value; a legacy lesson presents a blank value. | Display completeness, Conditional | Component, Negative | Medium | Standard |
| AC 01.4 | Calendar detail drawer presents `Compensation Ratio` and its persisted value; a legacy lesson presents a blank value. | Display completeness, Conditional | Component, Negative | Medium | Standard |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| CSV import | A row-level validation or continuation failure can create incorrect payroll inputs at scale. | Use a mixed file containing `100%`, `60%`, blank, and invalid values; assert persisted values, rejected row, error, and retry correction. |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Tenant and value restrictions | The supplied UI shows `Compensation Rate` and `NA`, conflicting with Riso's confirmed `Compensation Ratio` and `発生しない` value. | Assert Riso visibility, non-Riso absence, exact label, three allowed values, and absence of `NA`. |
| Recurring edits | An incorrect scope can silently change payroll inputs across a series or alter immutable lesson states. | Cover Only this, This and following, prior occurrence, Completed, Cancelled, and unselected following occurrence. |
| Bulk edit | Bulk action must update only eligible selected records and must not propagate through recurrence. | Use eligible and non-eligible selected lessons plus an unselected following occurrence. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Display surfaces | Incorrect or missing display affects staff's payroll review but does not alter data. | Assert the exact field/value on List, Detail, and Calendar drawer for a populated and a legacy lesson. |

---

## 6. Edge-Case and Downstream-Effects Inventory

### A–F checklist

| Area | Assessment |
|---|---|
| A. Configuration thresholds | N/A — the PRD has fixed picklist values; no adjustable threshold is specified. |
| B. Date/time | N/A — no date-derived field behavior is specified. |
| C. Concurrent/stale state | N/A — no shared-capacity or time-gate behavior is changed. |
| D. Permission/role | Applicable — cover HQ/CM on Riso and a non-Riso tenant. No other role behavior is specified. |
| E. State transition | Applicable — Completed and Cancelled lessons are skipped for following-scope and bulk edits. |
| F. Cross-surface | Applicable — persist and read the value on Lesson List, Lesson Detail, and Calendar detail drawer. Timesheet is explicitly out of scope. |

### G. Downstream Effects Inventory

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner (TC) |
|---|---|---|
| Create a one-time lesson | Persist selected/default/blank ratio on the Lesson record. | SF Lesson record; Lesson List; Lesson Detail; Calendar drawer | Create & Display suite |
| Create a recurring lesson | Persist the first lesson's ratio on every generated occurrence. | SF Lesson recurring occurrences | Create & Recurrence suite |
| Import a CSV row | Persist explicit or blank-defaulted ratio; reject only invalid rows. | Imported Lesson records; CSV row result | CSV Import suite |
| Edit Only this | Update only the selected occurrence; leave adjacent occurrences unchanged. | SF Lesson recurring occurrences | Edit Scope suite |
| Edit This and following | Update eligible selected/following occurrences; leave prior, Completed, and Cancelled records unchanged. | SF Lesson recurring occurrences | Edit Scope suite |
| Bulk edit | Update eligible selected records; skip Completed/Cancelled and do not update unselected following records. | SF Lesson List and recurring occurrences | Bulk Edit suite |

**Inverse action:** N/A — the feature introduces no lesson deletion, unpublish, or compensation-ratio reset rule beyond optional blank editing.

### H. Display & Ordering Inventory

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| New Lesson form | `Compensation Ratio`; options `100%`, `60%`, `発生しない`; default `100%` | Blank is savable | N/A — no sort specified | Exact label `Compensation Ratio` |
| Edit Lesson form | `Compensation Ratio`; options `100%`, `60%`, `発生しない` | Blank is savable | N/A — no sort specified | Exact label `Compensation Ratio` |
| Lesson List | `Compensation Ratio` column and persisted value | Legacy lesson is blank | N/A — no sort specified | Exact label `Compensation Ratio` |
| Lesson Detail | `Compensation Ratio` and persisted value | Legacy lesson is blank | N/A — no sort specified | Exact label `Compensation Ratio` |
| Calendar detail drawer | `Compensation Ratio` and persisted value | Legacy lesson is blank | N/A — no sort specified | Exact label `Compensation Ratio` |

### H.2 Lesson Upsert Entry-Point Inventory

The user requested one dedicated Compensation Ratio case for each of the 13 LT-94111 flows. The LT-92533 PRD remains the oracle; F06 and F13 are recorded as provisional because Back Office is outside the PRD's named SF surfaces and awaits confirmation.

| Flow | Entry point | Coverage status |
|---|---|---|
| F01 | Lesson List SF — New Lesson | Covered |
| F02 | Lesson SF — Edit Lesson | Covered |
| F03 | Lesson Schedule Detail — Add Lesson | Covered |
| F04 | Lesson Schedule Detail — Extend Recurrence | Covered |
| F05 | Lesson SF — Duplicate Lesson | Covered |
| F06 | Back Office — Edit Lesson | Provisional — BO confirmation pending |
| F07 | Calendar SF — New Lesson | Covered |
| F08 | Calendar SF — Drag and drop New Lesson | Covered |
| F09 | Calendar SF — Drag and drop Edit Lesson | Covered |
| F10 | Available Teacher Calendar — New Lesson | Covered |
| F11 | Calendar SF — Edit Lesson | Covered |
| F12 | Calendar SF — Duplicate Lesson | Covered |
| F13 | Back Office Calendar — Edit Lesson | Provisional — BO confirmation pending |

### H.1 PRD–UI Mismatch Report

The supplied PRD screenshots were reviewed in place of Figma. The user explicitly chose **PRD wins**; these are resolved implementation and test expectations.

| Screen / Component | Field | In PRD? | In UI screenshot? | Mismatch Type | Resolution |
|---|---|---|---|---|---|
| New Lesson | Field label | `Compensation Ratio` | `Compensation Rate` | Label mismatch | PRD wins: assert `Compensation Ratio`. |
| Edit Lesson | Field label | `Compensation Ratio` | `Compensation Rate` | Label mismatch | PRD wins: assert `Compensation Ratio`. |
| Lesson List | Field label | `Compensation Ratio` | `Compensation Rate` | Label mismatch | PRD wins: assert `Compensation Ratio`. |
| New/Edit/List | Picklist values | `100%`, `60%`, `発生しない` | `100%`, `60%`, `NA` | User clarification replaces the UI-only `NA` value | Riso clarification wins: offer and persist `発生しない`; do not offer or persist `NA`. |
| Lesson Detail | Read-only display | Required | Not shown in supplied UI | PRD has field, UI evidence absent | PRD wins: test read-only display. |
| Calendar detail drawer | Read-only display | Required | Not shown in supplied UI | PRD has field, UI evidence absent | PRD wins: test drawer display. |

---

## 7. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Riso-only field and exact picklist | None in Qase suite PX/3517 | None | ✅ Tenant isolation, exact label, `100%`/`60%`/`発生しない`, and no `NA`. |
| New Lesson default and optional blank | None in Qase suite PX/3517 | None | ✅ Default, override, blank save, and persistence. |
| Recurring creation and edit scope | Core recurring-edit tests; no ratio coverage | Partial | ✅ Propagation, Only this, This and following, Completed/Cancelled skip. |
| CSV row validation | Existing lesson-import patterns; no ratio coverage | Partial | ✅ Explicit/blank values, invalid row rejection, valid-row continuation, retry. |
| Bulk edit isolation | Existing list behavior; no ratio coverage | Partial | ✅ Eligible/Completed/Cancelled selections and no following-series propagation. |
| Three SF display surfaces | Existing Riso subject-field pattern | Partial | ✅ List, Detail, Calendar drawer, populated and legacy blank values. |
| 13 LT-94111 Lesson Upsert entry points | Entry-point matrix in LT-94111 | Partial | ✅ One dedicated Compensation Ratio case per F01–F13; F06/F13 are provisional pending BO confirmation. |

---

## 8. Suggested Test Suite Structure

```text
epics/OOP/riso/LT-92533-riso-compensation-ratio-lesson/test-cases/
├── compensation-ratio-create-and-configuration.md  → AC 01.1, AC 01.2 UI, recurring creation, and F01/F03–F05/F07–F08/F10/F12
├── compensation-ratio-create-and-configuration.csv → Qase import companion
├── compensation-ratio-csv-import.md                → AC 01.2 CSV validation and row outcomes
├── compensation-ratio-csv-import.csv               → Qase import companion
├── compensation-ratio-edit-and-display.md          → AC 01.3, AC 01.4 edit scope, bulk edit, displays, and F02/F06/F09/F11/F13
└── compensation-ratio-edit-and-display.csv         → Qase import companion
```

## 9. Phase 2 Quality Check

- All 16 business rules have logic types and techniques.
- All four ACs have risk level and coverage depth.
- CRUD/update effects are mapped in the downstream-effects inventory; Timesheet is excluded.
- Every named UI component has display-completeness coverage; no ordering or exact-message behavior beyond the field label is specified.
- The PRD–UI mismatch report is resolved by the user's **PRD wins** decision.
- All 13 LT-94111 entry points have dedicated Compensation Ratio cases; the two BO cases are explicitly provisional pending confirmation.
- Qase suite PX/3517 has no existing coverage; all identified coverage is new.
