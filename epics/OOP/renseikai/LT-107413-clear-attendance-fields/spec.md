---
ticket_id: LT-107413
ticket_url: https://manabie.atlassian.net/browse/LT-107413
title: Renseikai | SF Core | Enable clearing of Attendance Notice and Attendance Reason in Salesforce
module: scheduling
bucket: OOP/renseikai
status: Ready for QA
internal_uat_date: null
production_release_date: 2026-09-07
last_updated: 2026-08-13
---

# LT-107413: Clear Attendance Notice and Attendance Reason in Salesforce

## Summary

Scope covers the Renseikai attendance forms in Salesforce and Back Office, plus synchronization of the corrected Attendance Status to Back Office and Learner App. The Salesforce Lesson > Student Session > Edit form must let staff clear selected Attendance Status, Attendance Reason, and Attendance Notice values through an x icon; when a previously absent attendance status becomes Attend or blank, the two dependent absence fields must appear blank in the form. The Back Office attendance UI must also support changing a student's Attendance Status to Attend from the three stated collection entry points.

Per user direction, this analysis is deliberately limited to the stated form interactions and the Salesforce-to-Back Office read-back; it excludes broader database, Mobile, permission, and regression analysis. **Present means Attend.**

---

## Acceptance Criteria

- **AC 01 — Automatic UI clearing for a status correction**
  - Given Attendance Status is **Absent**, **Late**, or **Leave Early**, and Attendance Notice and Attendance Reason have selected values.
  - When the user changes Attendance Status to **Attend** (also referred to as Present) or clears the Attendance Status selection.
  - Then the form clears the displayed selections for Attendance Notice and Attendance Reason.

- **AC 02 — Clear affordances**
  - The Salesforce form provides an x icon for each selected value in Attendance Status, Attendance Reason, and Attendance Notice.
  - Selecting an x icon clears that field's displayed selection.

- **AC 03 — Set Attendance Status to Attend in Back Office collection flows**
  - In **Collect Attendance in Lesson**, a user can change a student's Attendance Status to **Attend**; the form clears the displayed Attendance Notice and Attendance Reason selections.
  - In **Collect Attendance in Report**, a user can change a student's Attendance Status to **Attend**; the form clears the displayed Attendance Notice and Attendance Reason selections.
  - In **Bulk Collect Attendance in Calendar BO**, a user can change the selected student or students' Attendance Status to **Attend**; the form clears the displayed Attendance Notice and Attendance Reason selections for every selected student.

- **AC 04 — Salesforce correction synchronizes to Back Office and Learner App**
  - When a user changes Attendance Status in Salesforce from **Absent**, **Late**, or **Leave Early** to **Attend**, then saves the Student Session, Back Office Collect Attendance for the same student and lesson displays **Attendance Status = Attend**, **Attendance Notice = blank**, and **Attendance Reason = blank**.
  - For the same saved correction, Learner App for that student and lesson displays **Attendance Status = Attend**.
  - When a user clears Attendance Status in Salesforce, then saves the Student Session, Back Office Collect Attendance for the same student and lesson displays **Attendance Status = blank**, **Attendance Notice = blank**, and **Attendance Reason = blank**.
  - For the same saved clear, Learner App for that student and lesson displays a **blank Attendance Status**.

- **Out of scope**
- Save/cancel behavior other than the Save needed for the Salesforce-to-Back Office read-back in AC 04.
- Learner App fields other than the explicit Attendance Status read-back in AC 04.
  - Role/permission changes and non-UI behavior.

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---:|---|---|---|---|---|
| 1 | AC 01 | Selecting Attend after Absent clears the displayed Attendance Notice and Attendance Reason selections. | Attendance Notice; Attendance Reason | auto-cleared in form | Salesforce |
| 2 | AC 01 | Selecting Attend after Late clears the displayed Attendance Notice and Attendance Reason selections. | Attendance Notice; Attendance Reason | auto-cleared in form | Salesforce |
| 3 | AC 01 | Selecting Attend after Leave Early clears the displayed Attendance Notice and Attendance Reason selections. | Attendance Notice; Attendance Reason | auto-cleared in form | Salesforce |
| 4 | AC 01 | Clearing Attendance Status after Absent clears the displayed Attendance Notice and Attendance Reason selections. | Attendance Status; Attendance Notice; Attendance Reason | status clear triggers dependent clear | Salesforce |
| 5 | AC 01 | Clearing Attendance Status after Late clears the displayed Attendance Notice and Attendance Reason selections. | Attendance Status; Attendance Notice; Attendance Reason | status clear triggers dependent clear | Salesforce |
| 6 | AC 01 | Clearing Attendance Status after Leave Early clears the displayed Attendance Notice and Attendance Reason selections. | Attendance Status; Attendance Notice; Attendance Reason | status clear triggers dependent clear | Salesforce |
| 7 | AC 02 | A selected Attendance Status has an x icon that clears its displayed value. | Attendance Status | clearable | Salesforce |
| 8 | AC 02 | A selected Attendance Reason has an x icon that clears its displayed value. | Attendance Reason | clearable | Salesforce |
| 9 | AC 02 | A selected Attendance Notice has an x icon that clears its displayed value. | Attendance Notice | clearable | Salesforce |
| 10 | AC 03 | Collect Attendance in Lesson changes one student's Status to Attend and clears displayed Notice and Reason. | Attendance Status; Attendance Notice; Attendance Reason | selectable; dependent fields auto-cleared | Back Office |
| 11 | AC 03 | Collect Attendance in Report changes one student's Status to Attend and clears displayed Notice and Reason. | Attendance Status; Attendance Notice; Attendance Reason | selectable; dependent fields auto-cleared | Back Office |
| 12 | AC 03 | Bulk Collect Attendance in Calendar BO changes selected students' Status to Attend and clears displayed Notice and Reason for each selected student. | Attendance Status; Attendance Notice; Attendance Reason | selectable in bulk; dependent fields auto-cleared | Back Office |
| 13 | AC 04 | Saving an SF change from Absent, Late, or Leave Early to Attend synchronizes Attend, blank Attendance Notice, and blank Attendance Reason to BO Collect Attendance. | Attendance Status; Attendance Notice; Attendance Reason | persisted and synchronized | Salesforce → Back Office |
| 14 | AC 04 | Saving an SF-cleared Attendance Status synchronizes blank Attendance Status, blank Attendance Notice, and blank Attendance Reason to BO Collect Attendance. | Attendance Status; Attendance Notice; Attendance Reason | persisted and synchronized | Salesforce → Back Office |
| 15 | AC 04 | A saved SF status correction synchronizes the resulting Attendance Status to Learner App for the same student and lesson. | Attendance Status | persisted and synchronized | Salesforce → Learner App |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---:|---|---|---|---|
| 1 | [EXTENDED] | Qase PX suite 274 — Collect Attendance | AC 01 / AC 02 / AC 03 / AC 04 | The existing suite covers setting attendance values and a cancel path, but does not cover the newly requested Salesforce clear affordances, dependent UI clearing, the specified Back Office Attend update paths, or SF-to-BO synchronization of a cleared absence record. |

### Missing in Requirements

| # | Tag | Source | Description |
|---:|---|---|---|
| — | — | User direction | No deep-analysis gaps assessed because this epic is constrained to UI/UX-only scope. |

### Lesson-Learned Risks

| # | Incident | Date | AC | Risk | Guardrail |
|---:|---|---|---|---|---|
| — | — | — | — | Not assessed; the user excluded deep analysis. | UI-only validation only. |

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-17 | Renseikai — Attendance & Error Configuration | Add a Salesforce correction from an absence status to Attend/blank, then read the same Student Session in BO Collect Attendance and Learner App. | UPDATE |

### Assumptions Made

- “Present” and “Attend” are the same Attendance Status value.
- The x icons are visible only when their corresponding fields currently have selected values.
- The Back Office scope is limited to the visible selection of Attend in the three named collection entry points.
- Synchronization scope is limited to the explicit Back Office three-field and Learner App Attendance Status read-backs in AC 04; other downstream surfaces are out of scope.

---

## Clarification Questions

None. The scoped UI and Salesforce-to-Back Office synchronization behavior, plus terminology, have been explicitly confirmed by the user; questions were not posted to Jira.

> Not posted to Jira — no deep analysis or Jira update requested.

## Related Specs

- `epics/lesson/LT-96152-collect-attendance-entry-points-bo/spec.md` — documents the existing collect-attendance domain and its lifecycle boundaries; it is not an extension target for this UI-only scope.

## Related Test Cases

- Qase PX suite 274 — Collect Attendance — eight existing cases cover setting attendance values and one Cancel path; none covers clearing Attendance Status, Attendance Reason, or Attendance Notice in the Salesforce form.

## QASE Coverage Gaps

- AC 01 — No existing target-suite case covers the visible clearing of Attendance Notice and Attendance Reason when Attendance Status changes to Attend or blank.
- AC 02 — No existing target-suite case covers the x icon for each of the three attendance fields.
- AC 03 — No existing target-suite case covers changing Attendance Status to Attend from Collect Attendance in Lesson, Collect Attendance in Report, and Bulk Collect Attendance in Calendar BO.
- AC 04 — Existing suite cases synchronize a selected Attendance Reason between SF and BO, but none verifies that an SF correction to Attend or blank clears and synchronizes the required values to BO and the resulting Attendance Status to Learner App.
