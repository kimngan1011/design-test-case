---
ticket_id: LT-108387+LT-101751
ticket_url: "https://manabie.atlassian.net/browse/LT-108387 | https://manabie.atlassian.net/browse/LT-101751"
title: Core Customizable Student Session Table in Lesson Detail
module: scheduling
bucket: lesson
status: "LT-108387: Ready for QA; LT-101751: Done"
internal_uat_date: null
production_release_date: null
last_updated: 2026-09-15
---

# LT-108387 + LT-101751: Core Customizable Student Session Table in Lesson Detail

## Summary

This merged Core feature makes the Salesforce Lesson Detail Student Session table compact and tenant-configurable. It preserves the required field set for Renseikai and EEA while allowing a System Administrator to customize displayed columns through the Lesson Custom Setting **Enable Customizable Table Columns**.

This is a purposeful exception to the one-epic-per-folder convention, requested to keep the two Jira epics and their shared Qase suite (`PX / 3534`) together.

---

## Acceptance Criteria

### LT-108387 — Renseikai

On the Lesson Detail Student Session table, show the following Renseikai fields:

| Displayed field | Jira label |
|---|---|
| Student Name | 生徒名 / Student Name |
| Grade | 学年 / Grade |
| Attendance Response | 出欠連絡 / Attendance Response |
| Attendance Status | 出欠状況 / Attendance Status |
| Attendance Reason | 欠席理由 / Attendance Reason |
| Attendance Note | 備考 / Attendance Note |

Do not show these fields in the Renseikai layout: Risk, Type, Attendance Notice, Reallocate Flag.

### LT-101751 — EEA

EEA collects attendance through the **Salesforce Lesson Detail** page, not BO Lesson Detail. Its Student Session table displays:

| Displayed field |
|---|
| Student Name |
| Grade |
| Type |
| Attendance Status |
| Attendance Reason |
| Reallocate Flag |

### Core configuration

- Lesson Custom Setting includes **Enable Customizable Table Columns**.
- Only **System Administrators** can customize Student Session table columns.
- The mechanism is Core and intended to support partner-specific show/hide choices in future.
- The table is **read-only**; the existing separate Edit function remains the edit path and inline editing is not allowed.
- Configuration is **per tenant**. Only a tenant with the custom setting enabled can customize its Student Session fields.
- A System Administrator can select and reorder **any** Student Session field.
- A saved tenant layout is displayed to other HQ or CM Staff in the same tenant.
- After a System Administrator saves a layout, HQ or CM Staff can still update Student Session values through the separate Edit function.

#### Supported column catalog

The column picker contains exactly these ten fields, based on the supplied configuration screenshot:

| # | Field |
|---:|---|
| 1 | Grade |
| 2 | Risk |
| 3 | Type |
| 4 | Attendance Response |
| 5 | Attendance Status |
| 6 | Attendance Notice |
| 7 | Attendance Reason |
| 8 | Reallocate Flag |
| 9 | Student Name |
| 10 | Attendance Note |

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---:|---|---|---|---|---|
| 1 | LT-108387 | Display Student Name. | Student Name | display-only | Salesforce |
| 2 | LT-108387 | Display Grade. | Grade | display-only | Salesforce |
| 3 | LT-108387 | Display Attendance Response, Attendance Status, Attendance Reason, and Attendance Note. | Attendance fields | display-only | Salesforce |
| 4 | LT-108387 | Hide Risk, Type, Attendance Notice, and Reallocate Flag. | Excluded fields | hidden | Salesforce |
| 5 | LT-101751 | Display Student Name, Grade, Type, Attendance Status, Attendance Reason, and Reallocate Flag. | EEA fields | display-only | Salesforce |
| 6 | LT-101751 | Use Salesforce Lesson Detail for attendance collection; no BO flow is introduced. | Lesson Detail platform | locked | Salesforce |
| 7 | Core configuration | Expose **Enable Customizable Table Columns**. | Lesson Custom Setting | configurable | Salesforce |
| 8 | Core configuration | Only System Administrators can change table columns. | Column configuration | editable | Salesforce |
| 9 | Core configuration | Use a Core dynamic show/hide mechanism for tenant-specific layouts. | Table columns | configurable | Salesforce |
| 10 | User clarification | Keep the table read-only; use the separate Edit function for changes. | Student Session table | read-only | Salesforce |
| 11 | User clarification | Apply custom configuration only to the enabled tenant. | Enable Customizable Table Columns | tenant-scoped configurable | Salesforce |
| 12 | User clarification + configuration screenshot | Allow a System Administrator to select and reorder any of the ten supported fields: Grade, Risk, Type, Attendance Response, Attendance Status, Attendance Notice, Attendance Reason, Reallocate Flag, Student Name, Attendance Note. | Table columns | configurable; reorderable | Salesforce |
| 13 | User request | Show a System Administrator's saved layout to other HQ or CM Staff in the same tenant. | Student Session table | shared tenant layout | Salesforce |
| 14 | User request | Preserve the separate Edit function for HQ or CM Staff after a System Administrator saves a layout. | Student Session values | editable through separate function | Salesforce |
| 15 | LT-108387 + User request | A System Administrator in Japanese locale can customize the Renseikai Student Session table using the Jira-specified Japanese field labels; the saved table renders those selected Japanese headers. | Renseikai Student Session column configuration and table | localized configuration and display | Salesforce |

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---:|---|---|---|---|
| 1 | [EXTENDED] | `epics/OOP/renseikai/LT-107175-remote-attendance-status-tag/spec.md` | LT-108387 | The new table adds a compact view of existing persisted Response, Status, Reason, and Note values. It must not alter their persistence or sync behavior. |
| 2 | [REGRESSION RISK] | `epics/OOP/renseikai/LT-107413-clear-attendance-fields/spec.md` | LT-108387 | A rendering/configuration refactor can bind a stale or wrong attendance field, or mutate a value that is synchronized to BO and Learner App. |
| 3 | [EXTENDED] | LT-101751 Jira description | LT-101751 | EEA's Salesforce layout has a different six-column set and must remain isolated from Renseikai's layout. |

### Missing in Requirements

| # | Tag | Source | Description |
|---:|---|---|---|
| 1 | [EXTENDED] | User clarification 2026-09-15 | Configuration is per tenant and only available when that tenant enables the setting; no configuration may leak to another tenant. |
| 2 | [EXTENDED] | User clarification 2026-09-15 | System Administrators can select and reorder any Student Session field. |
| 3 | [EXTENDED] | User clarification 2026-09-15 | The table is read-only; a separate Edit function is the only edit path. |
| 4 | [EXTENDED] | User-supplied screenshot `SCR-20260915-ppqb.png` | The selectable field catalog is the ten fields listed in **Supported column catalog**. |
| 5 | [EXTENDED] | User request 2026-09-15 | A layout saved by a System Administrator must be visible to other HQ or CM Staff in the same tenant. |
| 6 | [EXTENDED] | User request 2026-09-15 | After a System Administrator customizes columns, HQ or CM Staff must retain the normal separate Edit path for Student Session values. |

### Lesson-Learned Risks

| # | Incident | Date | AC | Risk | Guardrail |
|---:|---|---|---|---|---|
| — | No entity-and-operation match | — | — | All checked incidents involve Student Session create, delete, or assignment flows; this requirement is display/configuration only. | Prove configuration is non-mutating; retain normal attendance and assignment regression coverage. |

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-01 | Lesson Lifecycle — Create, Teach, Report, View | Add a non-mutating display check after attendance is saved. | UPDATE |
| E2E-17 | Renseikai — Attendance & Error Configuration | Add Renseikai six-column display and hidden-column assertions on Salesforce Lesson Detail. | UPDATE |
| E2E-18 | EEA Dual Lesson — Paired Locations | Add the EEA six-column Salesforce display assertion. | UPDATE |

### Assumptions Made

- The table is a read-only display surface. Existing separate Edit behavior remains a regression boundary, including after a System Administrator customizes the tenant layout.
- The Jira screenshots are attachments, not Figma designs; no Figma-specific behavior was extracted.
- The Core design supports tenant-specific layouts. It does not imply that a configuration change should affect other tenants.
- The configuration screenshot defines the supported field catalog, but does not define empty-selection validation, Save/Cancel behavior, or the default column order; these are covered as testable behavior only if implemented.
- Field values retain their existing data behavior; this scope only decides whether a column is visible.

## Clarification Questions

> ✅ Resolved by the user on 2026-09-15. Per instruction, no Jira comment was posted.

## Related Specs

- `epics/OOP/renseikai/LT-107413-clear-attendance-fields/spec.md` — Salesforce attendance-field persistence and BO/Learner App read-back.
- `epics/OOP/renseikai/LT-107175-remote-attendance-status-tag/spec.md` — Student Session Attendance Response, Status, Reason, and Note display semantics.
- `epics/lesson/LT-96152-collect-attendance-entry-points-bo/spec.md` — existing attendance value persistence baseline.
- `epics/OOP/riso/LT-94698-subject-in-lesson-detail/spec.md` — tenant-specific Lesson Detail display isolation pattern.

## Related Test Cases

- `epics/OOP/renseikai/LT-107413-clear-attendance-fields/test-cases/sf-bo-attendance-sync.md` — attendance data read-back regression surface.
- `epics/OOP/renseikai/LT-107175-remote-attendance-status-tag/test-cases/attendance-status-surfaces.md` — attendance field display regression surface.
- Qase `PX / 3534` — target suite exists and has no cases at analysis time.

## QASE Coverage Gaps

- LT-108387 — exact display and absence of all ten stated Renseikai field columns.
- LT-101751 — exact display of all six EEA field columns and absence of Renseikai-only columns.
- Core configuration — setting enablement, System Administrator authorization, tenant isolation, selection/reordering of all ten catalog fields, persistence, excluded-field behavior, and cross-user saved-layout readback.
- Read-only boundary — no inline edit in the table; the separate Edit function remains the only supported edit path after a layout is customized.
- All display paths — populated and blank field values must render without mutating the Student Session or its downstream attendance data.
