---
ticket_id: LT-92533
ticket_url: https://manabie.atlassian.net/browse/LT-92533
title: Riso | OOP | Compensation Ratio in the lesson
module: lesson-management
bucket: OOP/riso
status: Ready for QA
internal_uat_date: 2026-02-23
production_release_date: null
last_updated: 2026-09-11
---

# LT-92533: Riso | OOP | Compensation Ratio in the lesson

## Summary

For the Riso organization, add a `Compensation Ratio` lesson field so HQ and CM can record the ratio used for payroll calculation. The confirmed Riso value set is `100%`, `60%`, and `発生しない`; it requires creation, CSV import, recurring propagation, edit, bulk edit, and display behavior on named Salesforce surfaces.

Timesheet synchronization is confirmed out of scope for LT-92533.

---

## Acceptance Criteria

### US 01 — CRUD Lesson with compensation ratio for payroll calculation

As an HQ or CM, I want to be able to CRUD Lesson with compensation ratio so that I can use this data for payroll calculation.

| AC | Feature | Criteria |
|---|---|---|
| AC 01.1 | Compensation Ratio — only apply for Riso | Label: `Compensation Ratio`. Data type: Global Picklist. Picklist values: `100%`, `60%`, `発生しない`. `NA` is not an allowed value. |
| AC 01.2 | Create new lesson with Compensation Ratio | On the SF New Lesson form, show the field with default `100%`; the user can change and save it. For recurring creation, all created lessons receive the first lesson's value. CSV templates can include the field; if its CSV value is not defined, created lessons receive `100%`. |
| AC 01.3 | Edit Compensation Ratio | From Edit Lesson, change the field for Only this lesson or This and following lessons. From Lesson List bulk edit, change multiple lessons; the change applies only to each selected lesson even when it belongs to a recurring series. |
| AC 01.4 | View Compensation Ratio | Display the field in SF Lesson List, SF Lesson Detail, and SF Lesson Calendar detail drawer. |

### Confirmed Clarifications

- **AC 01.2:** Compensation Ratio is optional. A user may clear the UI default and save a blank value.
- **AC 01.1 (user clarification, 2026-09-14):** Riso uses `発生しない` in place of `NA`. `100%`, `60%`, and `発生しない` are allowed picklist values; `NA` is invalid.
- **AC 01.2:** CSV imports process valid (`100%`/`60%`/`発生しない`) and blank rows. Only rows with an invalid Compensation Ratio are rejected, with a row-level error and correction/retry expectation where the import flow supports it.
- **AC 01.3:** This and following must skip Completed and Cancelled lesson occurrences.
- **AC 01.3:** Bulk edit skips selected Completed and Cancelled lessons. No partial-result notification requirement is specified.
- **Out of scope:** No Timesheet synchronization is required for this ticket.
- **AC 01.4:** For lessons created before release, the new field is shown with a blank value; no 100% backfill is required.

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---|---|---|---|---|---|
| BR-01 | AC 01.1 | Field is available only to the Riso organization. | Compensation Ratio | conditional visibility | SF |
| BR-02 | AC 01.1 | Label is `Compensation Ratio`; field is a Global Picklist. | Compensation Ratio | editable | SF |
| BR-03 | AC 01.1 | `100%` is an allowed picklist value. | Compensation Ratio | editable | SF |
| BR-04 | AC 01.1 | `60%` and `発生しない` are allowed picklist values; `NA` is not allowed. | Compensation Ratio | editable | SF |
| BR-05 | AC 01.2 | New Lesson form defaults the field to `100%`. | Compensation Ratio | defaulted, editable | SF |
| BR-06 | AC 01.2 | Field is optional: user can change the UI default, clear it, and save blank. | Compensation Ratio | optional, editable | SF |
| BR-07 | AC 01.2 | Recurring creation applies the first lesson's value to every created occurrence. | Compensation Ratio | inherited | SF |
| BR-08 | AC 01.2 | Valid/blank CSV rows import; only invalid Compensation Ratio rows reject with row-level error and correction/retry expectation where supported. | CSV Compensation Ratio column | optional, row-level validated | SF |
| BR-09 | AC 01.2 | Blank/undefined CSV value defaults created lessons to `100%`. | CSV Compensation Ratio column | optional, defaulted | SF |
| BR-10 | AC 01.3 | Edit Lesson can change the selected occurrence only. | Compensation Ratio | editable | SF |
| BR-11 | AC 01.3 | Edit Lesson changes eligible selected/following occurrences; Completed and Cancelled are skipped. | Compensation Ratio | editable | SF |
| BR-12 | AC 01.3 | Lesson List bulk edit changes eligible selected lessons and skips selected Completed/Cancelled lessons; no partial-result notification is required. | Compensation Ratio | editable | SF |
| BR-13 | AC 01.3 | Bulk edit does not propagate to following occurrences of a selected recurring lesson. | Compensation Ratio | editable | SF |
| BR-14 | AC 01.4 | Show field in SF Lesson List; historical lessons show blank. | Compensation Ratio | visible | SF |
| BR-15 | AC 01.4 | Show field in SF Lesson Detail; historical lessons show blank. | Compensation Ratio | visible | SF |
| BR-16 | AC 01.4 | Show field in SF Lesson Calendar detail drawer; historical lessons show blank. | Compensation Ratio | visible | SF |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

No direct conflict or full replacement was found. The feature extends established Riso lesson-field, CSV-import, and recurring-edit patterns.

| # | Tag | Source | AC | Description |
|---|---|---|---|---|
| F-10 | [EXTENDED] | `epics/lesson/LT-XXXX-edit-lesson/test-cases/edit-lesson-sf.md`, TC-1045 | AC 01.3 | Confirmed: Compensation Ratio follows core recurring-edit behavior and skips Completed and Cancelled occurrences. |
| F-01 | [EXTENDED] | `epics/OOP/riso/LT-94698-subject-in-lesson-detail/test-coverage.md` | AC 01.1 | Riso-only field pattern is extended; verify tenant isolation. |
| F-07 | [EXTENDED] | `epics/OOP/riso/LT-94698-subject-in-lesson-detail/test-coverage.md` | AC 01.2 | Existing Riso Subject recurrence pattern supports applying a field value to all created occurrences. |
| F-09 | [EXTENDED] | `epics/lesson/LT-XXXX-edit-lesson/test-cases/edit-lesson-sf.md` | AC 01.3 | Only this scope extends established recurring-edit isolation. |
| F-11 | [EXTENDED] | `knowledge/domain-knowledge/scheduling/lesson-management/lesson.md` | AC 01.3 | New multi-select bulk edit is explicitly isolated from following-series propagation. |
| F-13 | [EXTENDED] | `epics/OOP/riso/LT-94698-subject-in-lesson-detail/test-cases/LT-94698-subject-in-lesson-detail.md` | AC 01.4 | Requested SF display surfaces follow an existing Riso field pattern, without implying BO/Mobile scope. |

### Resolved Requirement Decisions and Remaining Gaps

No unresolved requirement gaps remain.

| # | Tag | Source | AC | Description |
|---|---|---|---|---|
| F-06 | [EXTENDED] | User clarification (AC 01.2) | AC 01.2 | Confirmed: field is optional; a user can clear the default and save blank. |
| F-08 | [EXTENDED] | User clarification + `knowledge/domain-knowledge/scheduling/lesson-learned/core.md`, 2026-08-18 | AC 01.2 | Valid/blank rows import; only invalid Compensation Ratio rows reject with row-level error and correction/retry expectation where supported. |
| F-12 | [EXTENDED] | User clarification | AC 01.3 | Bulk edit skips selected Completed/Cancelled lessons; no partial-result notification requirement is added. |
| F-14 | [EXTENDED] | User clarification | N/A | Timesheet synchronization is explicitly out of scope; the Jira Approach text does not add a requirement to this PRD-focused feature. |
| F-15 | [EXTENDED] | User clarification (AC 01.4) | AC 01.4 | Confirmed: historical lessons display the new field blank; no 100% backfill is required. |

### Lesson-Learned Review

No open lesson-learned risk remains after the confirmed row-level CSV decision.

| # | Incident | Date | AC | Risk | Guardrail |
|---|---|---|---|---|---|
| F-08 | Renseikai — Published Lesson Missing Student Sessions Due to Salesforce 10,000-Record Bulk Write Limit | 2026-08-18 | AC 01.2 | Resolved: valid/blank rows continue; invalid Compensation Ratio rows reject individually rather than silently defaulting or blocking valid rows. | Preserve row-level error and correction/retry behavior where the import flow supports it. |

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-02 | Recurring Lesson — Create, Edit Chain, Delete, Calendar Drag | Add Compensation Ratio creation and selected/previous/following assertions; verify Completed/Cancelled occurrences are skipped for both following-scope edit and bulk edit. | UPDATE |
| E2E-19 | Riso — Lesson Allocation & Subject in Detail | Closest tenant/field analogue; add Compensation Ratio create, SF display, recurring scope, and tenant-isolation steps. Do not copy Subject-only BO/Mobile assertions. | UPDATE |
| E2E-01 | Lesson Lifecycle — Create, Teach, Report, View | Can smoke-test persisted one-time data on SF Calendar. Timesheet is out of scope. | NO UPDATE REQUIRED |

### Assumptions Made

- PRD acceptance criteria are the primary source of scope; user clarification explicitly excludes Timesheet synchronization.
- The field is scoped to SF only because the PRD names SF surfaces and has no BO or Mobile AC.
- The supplied PRD UI screenshots were reviewed during coverage planning; the user confirmed that the PRD wins where the screenshots differ.
- Qase suite `PX/3517` was fetched and currently has no cases; all ACs therefore have no Qase coverage in that suite.
- `v2026.11.02` is a Jira Fix Version, not a confirmed production-release date.

---

## Clarification Questions

> Status: **not posted — user requested no Jira post**.

### Open

_None — all clarification questions were resolved by the user._

### Resolved by User

1. **AC 01.3:** This and following skips Completed and Cancelled occurrences.
2. **Out of scope:** Timesheet synchronization is not required.
3. **AC 01.2:** Compensation Ratio is optional; a user may save blank after clearing the default.
4. **AC 01.4:** Historical lessons show the new field with a blank value; no 100% backfill.
5. **AC 01.2:** Valid and blank CSV rows import; only invalid Compensation Ratio rows reject with a row-level error and correction/retry expectation where supported.
6. **AC 01.3:** Bulk edit skips selected Completed and Cancelled lessons; no partial-result notification requirement is specified.

## Related Specs

- `epics/OOP/riso/LT-94698-subject-in-lesson-detail/test-coverage.md` — closest Riso lesson-field analogue for SF display, CSV mapping, and recurring scope.
- `epics/OOP/riso/LT-92532-riso-create-update-la-on-ui/spec.md` — Riso tenant and lesson-allocation context.
- `epics/lesson/LT-XXXX-edit-lesson/test-cases/edit-lesson-sf.md` — core recurring edit scope and Completed/Cancelled regression baseline.

## Related Test Cases

- `epics/OOP/riso/LT-94698-subject-in-lesson-detail/test-cases/LT-94698-subject-in-lesson-detail.md` — recurring create/edit and Riso field display pattern.
- `epics/OOP/riso/LT-94698-subject-in-lesson-detail/test-cases/LT-94698-subject-import-search-filter.md` — existing Riso lesson-field CSV pattern.
- `epics/OOP/riso/LT-96234-auto-generate-lesson-name/test-cases/bulk-csv-auto-generate.md` — per-row mixed-input CSV pattern.
- `epics/lesson/LT-XXXX-edit-lesson/test-cases/edit-lesson-sf.md` — recurring edit scope regression coverage.

## QASE Coverage Gaps

- AC 01.1 — No case in Qase suite `PX/3517` covers Riso-only field visibility or the confirmed three-value Global Picklist.
- AC 01.2 — No case covers UI default/override, optional blank save, recurring inheritance, explicit/blank CSV value, or invalid-row rejection with row-level error/retry expectation.
- AC 01.3 — No case covers Only this, This and following with Completed/Cancelled skipped, or bulk-edit isolation with Completed/Cancelled skipped.
- AC 01.4 — No case covers SF Lesson List, Lesson Detail, Calendar detail-drawer display, or blank display for legacy lessons.
