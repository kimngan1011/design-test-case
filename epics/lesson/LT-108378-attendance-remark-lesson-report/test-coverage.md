# Test Coverage: LT-108378 — Show Attendance Remark in Lesson Report (BO)

**Jira:** https://manabie.atlassian.net/browse/LT-108378  
**Qase targets:** PX / suite 3269 — Update LR; PX / suite 1748 — Lesson Report Detail  
**Date:** 2026-10-09  
**Scope:** Back Office Student List display only; one report view accessed from Lesson Management and one from Lesson Report.

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---:|---|---|
| BR-01 | AC 01.1 | Staff saves an Attendance Note on the Salesforce Student Session for the report student. |
| BR-02 | AC 01.1 | The Lesson Management lesson-detail Report tab Student List displays the saved Attendance Status and Salesforce Attendance Note for the same student. |
| BR-03 | AC 01.1 | A populated row uses the exact structure `Attendance Status (Attendance Remark)`. |
| BR-04 | AC 01.2 | Staff saves an Attendance Note on the Salesforce Student Session for the report student. |
| BR-05 | AC 01.2 | The Lesson Report Detail Report tab Student List displays the saved Attendance Status and Salesforce Attendance Note for the same student. |
| BR-06 | AC 01.2 | A populated row uses the exact structure `Attendance Status (Attendance Remark)`. |
| BR-07 | AC 01.1, AC 01.2 | Opening either read-only BO display does not alter the stored Salesforce Attendance Status or Attendance Note. |
| BR-08 | AC 01.3 | Staff updates a student's Attendance Remark in Back Office Lesson Management and saves the changed value. |
| BR-09 | AC 01.3 | The Student List shows the unchanged Attendance Status and newly saved Attendance Remark after refresh. |

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC 01.1 | BR-01–BR-03 | State transition; Cross-system impact; Display completeness; Data integrity |
| AC 01.2 | BR-04–BR-06 | State transition; Cross-system impact; Display completeness; Data integrity |
| AC 01.1, AC 01.2 | BR-07 | Regression; Data integrity |
| AC 01.3 | BR-08, BR-09 | State transition; Data integrity; Display completeness |

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| State transition | CRUD/readback — save the Salesforce Attendance Note, then read it from the BO report route. |
| Cross-system impact | Regression — validate source-to-target mapping from Salesforce Student Session to BO Attendance Remark. |
| Display completeness | Component — assert the populated Attendance Status and its remark in the same Student List row. |
| Data integrity | Regression — read the same saved values from the two report routes without changing them. |
| Regression | Scenario — use one named student with an exact, pre-saved attendance pair. |

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC 01.1 | Save Attendance Note in Salesforce and show it as a populated remark in the Lesson Management report Student List, with exact parentheses and text. | State transition; Cross-system impact; Display completeness; Data integrity | CRUD/readback; Component; Regression | High | Standard |
| AC 01.2 | Save Attendance Note in Salesforce and show it as a populated remark in the Lesson Report Detail Student List, with exact parentheses and text. | State transition; Cross-system impact; Display completeness; Data integrity | CRUD/readback; Component; Regression | High | Standard |
| AC 01.1, AC 01.2 | Retain the saved Attendance Status and Attendance Remark after each report view is opened and refreshed. | Regression; Data integrity | Regression | Medium | Standard |
| AC 01.3 | Update a populated Attendance Remark in Back Office Lesson Management and show the saved replacement beside the unchanged Attendance Status after refresh. | State transition; Data integrity; Display completeness | CRUD/readback; Component; Regression | High | Standard |

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Salesforce-to-BO mapping | A source-to-target mapping failure shows an outdated or unrelated attendance note beside the student status. | Save a distinctive Salesforce Attendance Note and assert it is the exact BO Attendance Remark on both requested routes. |
| BO update persistence | A BO update can appear in the edit form but fail to persist, overwrite the status, or display an older remark. | Replace a populated remark, then refresh and assert the exact replacement string with the same Attendance Status. |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Source-to-target synchronization | The source field is updated in Salesforce but consumed as a differently named field in BO. | Set a distinctive note in Salesforce, save, open the corresponding BO report route, and assert the exact composed display. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Exact value composition | Status and remark can be sourced from different fields or rendered with an incorrect separator. | Use a non-empty, recognizable Salesforce Attendance Note and assert the complete string `Absent (school events)`. |
| Route consistency | The same Student List component is reachable from two independent Back Office routes. | Cover each user-provided Qase suite with its corresponding route. |
| Read-only regression | Rendering must not overwrite or clear existing attendance data. | Refresh the report and confirm the saved pair remains unchanged. |

## 6. Mandatory Edge-Case Assessment

| Area | Applicability | Coverage decision |
|---|---|---|
| A. Configuration thresholds | N/A | No numeric or tenant configuration is specified. |
| B. Date / time / timezone | N/A | No date or time behavior is introduced. |
| C. Concurrent / stale state | N/A | The ticket does not define shared editing or cache behavior. |
| D. Permission & role | N/A | The ticket defines no role-specific change; use the default authorized HQ or CM Staff actor. |
| E. State transition | Applicable | Cover saving Salesforce Attendance Note and reading its mapped BO representation. |
| F. Cross-system / cross-surface | Applicable | The saved Salesforce Attendance Note is read through two BO report routes; each route receives a dedicated case. |
| G. Downstream effects | Applicable | Saving the Salesforce note must produce a corresponding BO Attendance Remark without altering the saved Attendance Status; each BO surface has its own case. |
| H. Display completeness & ordering | Applicable | Assert the complete populated string in the Student List. No sort, tooltip, pagination, or required blank-state representation is stated. |
| H.1 Spec–Figma mismatch | N/A | No Figma URL is present. |

## G. Downstream Effects Inventory

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner (TC) |
|---|---|---|---|
| HQ or CM Staff saves Attendance Note `school events` for Student A in Salesforce | The same Student Session's BO Lesson Management report row displays `Absent (school events)` and continues to show `Absent` after refresh. | Salesforce Student Session → BO Lesson Management Report tab | `lesson-management-attendance-remark` |
| HQ or CM Staff saves Attendance Note `school events` for Student A in Salesforce | The same Student Session's BO Lesson Report Detail row displays `Absent (school events)` and continues to show `Absent` after refresh. | Salesforce Student Session → BO Lesson Report Detail Report tab | `lesson-report-detail-attendance-remark` |
| HQ or CM Staff updates Student A's Attendance Remark from `school events` to `medical appointment` in BO | The BO Lesson Management Student List shows `Absent (medical appointment)` after save and refresh; Attendance Status remains `Absent`. | BO Lesson Management Report tab | `lesson-management-attendance-remark` |

## H. Display & Ordering Inventory

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| Salesforce Student Session | Attendance Status; editable Attendance Note | Note is saved for the report student | N/A | Attendance Note = `school events` |
| BO Lesson Management > Lesson Detail > Report > Student List | Student name; Attendance Status with saved Attendance Remark | Remark is populated from the Salesforce Attendance Note for the covered student | Not specified | `Absent (school events)` |
| BO Lesson Report > Lesson Report Detail > Report > Student List | Student name; Attendance Status with saved Attendance Remark | Remark is populated from the Salesforce Attendance Note for the covered student | Not specified | `Absent (school events)` |
| BO Lesson Management > Lesson Detail > Report > attendance edit form and Student List | Editable Attendance Remark; Student name; Attendance Status with saved Attendance Remark | Updated remark is persisted and replaces the previous value | Not specified | `Absent (medical appointment)` |

## 7. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Salesforce Attendance Note to Lesson Management Report tab mapping | PX suite 3269 has status, sort, report-state, and broader field-edit coverage; no title or linked Jira case covers `Attendance Status (Attendance Remark)` sourced from Salesforce Attendance Note. | Partial — existing Student List/report coverage does not assert the new mapping or composed display. | ✅ One cross-system component/regression case in suite 3269. |
| Salesforce Attendance Note to Lesson Report Detail mapping | PX suite 1748 has Lesson Report Detail coverage; no linked Jira case or matching composed-display case exists. | Partial — existing detail coverage does not assert the new mapping or composed display. | ✅ One cross-system component/regression case in suite 1748. |
| BO Attendance Remark update persistence | PX suite 3269 has report-update coverage but no case that replaces an Attendance Remark and asserts the exact parenthesized replacement after refresh. | Partial. | ✅ One BO update/readback case in suite 3269. |
| Blank Attendance Remark representation | No ticket acceptance criterion specifies the display when the remark is blank. | None. | Deferred pending product confirmation; do not assume whether parentheses are omitted or shown empty. |

## 8. Suggested Test Suite Structure

```
epics/lesson/LT-108378-attendance-remark-lesson-report/test-cases/
├── lesson-management-attendance-remark.md       → AC 01.1; import under PX suite 3269 (Update LR)
└── lesson-report-detail-attendance-remark.md    → AC 01.2; import under PX suite 1748 (Lesson Report Detail)
```

Each Markdown file will have a matching Qase CSV file. Each case saves `school events` as the Salesforce Attendance Note and then asserts the explicit BO behavior `Absent (school events)`.
