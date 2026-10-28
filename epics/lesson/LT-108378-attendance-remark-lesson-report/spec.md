---
ticket_id: LT-108378
ticket_url: https://manabie.atlassian.net/browse/LT-108378
title: Show Attendance Remark in Lesson Report (BO)
module: lesson report
bucket: lesson
status: in QA
internal_uat_date: null
production_release_date: null
last_updated: 2026-10-09
---

# LT-108378: Show Attendance Remark in Lesson Report (BO)

## Scope

Back Office renders a student's Attendance Remark next to the Attendance Status in the Student List on the two requested report surfaces. The ticket specifies the populated-value format as `Attendance Status (Attendance Remark)`, for example `Absent (school events)`.

## User Story

### US 01 — Read Attendance Remark in report student lists

As HQ or CM Staff, I can see a student's Attendance Remark alongside the Attendance Status while reviewing lesson reports, so I can understand the reason associated with that attendance state.

### Acceptance Criteria

- **AC 01.1 — Lesson Management report tab:** When staff saves an Attendance Note on a Student Session in Salesforce, Back Office at **Lesson > Lesson Management > Lesson Detail > Report tab > Student List** displays that value as Attendance Remark next to Attendance Status, in the format `Attendance Status (Attendance Remark)`.
- **AC 01.2 — Lesson Report detail report tab:** When staff saves an Attendance Note on a Student Session in Salesforce, Back Office at **Lesson > Lesson Report > Lesson Report Detail > Report tab > Student List** displays that value as Attendance Remark next to Attendance Status, in the format `Attendance Status (Attendance Remark)`.
- **AC 01.3 — Update Attendance Remark in BO:** In Back Office Lesson Management, staff can update a student's Attendance Remark and, after saving, the Student List displays the new value next to the unchanged Attendance Status in the format `Attendance Status (Attendance Remark)`.

## Business Rules (Extracted)

| # | AC | Business Rule | Surface |
|---:|---|---|---|
| BR-01 | AC 01.1 | A staff member can save an Attendance Note on a Student Session in Salesforce. | Salesforce Student Session |
| BR-02 | AC 01.1 | The Lesson Management lesson-detail Report tab Student List displays the saved Attendance Status and its Salesforce Attendance Note as Attendance Remark together. | BO Lesson Management > Lesson Detail > Report |
| BR-03 | AC 01.1 | A populated value uses `Attendance Status (Attendance Remark)`; for example, `Absent (school events)`. | BO Lesson Management > Lesson Detail > Report |
| BR-04 | AC 01.2 | A staff member can save an Attendance Note on a Student Session in Salesforce. | Salesforce Student Session |
| BR-05 | AC 01.2 | The Lesson Report Detail Report tab Student List displays the saved Attendance Status and its Salesforce Attendance Note as Attendance Remark together. | BO Lesson Report > Lesson Report Detail > Report |
| BR-06 | AC 01.2 | A populated value uses `Attendance Status (Attendance Remark)`; for example, `Absent (school events)`. | BO Lesson Report > Lesson Report Detail > Report |
| BR-07 | AC 01.1, AC 01.2 | The BO display is read-only: viewing it does not change the saved Salesforce Attendance Status or Attendance Note. | Both BO report surfaces |
| BR-08 | AC 01.3 | A staff member can update a student's Attendance Remark in Back Office Lesson Management and save the changed value. | BO Lesson Management > Lesson Detail > Report |
| BR-09 | AC 01.3 | The same Student List row shows the unchanged Attendance Status and the newly saved Attendance Remark in the required parenthesized format after refresh. | BO Lesson Management > Lesson Detail > Report |

## Scope Notes and Assumptions

- The supplied screenshot confirms that the affected label is the per-student **Attendance Status** in the Student List, not the lesson-level **Remark (Internal Only)** field.
- The user confirmed that **Salesforce Student Session Attendance Note** is the source of the BO **Attendance Remark**.
- The ticket specifies populated-remark rendering only. It does not define how a blank Attendance Remark is represented; blank-value behavior is recorded as a clarification-dependent coverage gap rather than assigned an unconfirmed expected result.
- No Figma URL is provided. The attached screenshot is evidence for the target location only.
