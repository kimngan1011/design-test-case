# Test Coverage: LT-108387 + LT-101751 — Core Customizable Student Session Table in Lesson Detail

**Jira:** https://manabie.atlassian.net/browse/LT-108387 · https://manabie.atlassian.net/browse/LT-101751  
**Qase target:** PX / suite 3534 — Core | Customizable Student Session Table in Lesson Detail page  
**Date:** 2026-09-15  
**Scope:** Salesforce Lesson Detail only; the table is read-only and tenant configuration controls its visible columns and order.

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---:|---|---|
| BR-01 | LT-108387 | Renseikai displays Student Name. |
| BR-02 | LT-108387 | Renseikai displays Grade. |
| BR-03 | LT-108387 | Renseikai displays Attendance Response, Attendance Status, Attendance Reason, and Attendance Note. |
| BR-04 | LT-108387 | Renseikai hides Risk, Type, Attendance Notice, and Reallocate Flag. |
| BR-05 | LT-101751 | EEA displays Student Name, Grade, Type, Attendance Status, Attendance Reason, and Reallocate Flag. |
| BR-06 | LT-101751 | EEA attendance collection uses Salesforce Lesson Detail; no BO Lesson Detail flow is introduced. |
| BR-07 | Core configuration | Lesson Custom Setting exposes **Enable Customizable Table Columns**. |
| BR-08 | Core configuration | Only System Administrators can change table-column configuration. |
| BR-09 | Core configuration | Configuration is Core but scoped to an enabled tenant. |
| BR-10 | User clarification | The Student Session table is read-only; the separate Edit function remains the edit path. |
| BR-11 | User clarification | A tenant can customize fields only when its setting is enabled. |
| BR-12 | User clarification + screenshot | A System Administrator can select and reorder any of the ten catalog fields. |
| BR-13 | User request | A saved tenant column layout is shown to other HQ or CM Staff in that same tenant. |
| BR-14 | User request | After a System Administrator saves a column layout, HQ or CM Staff can still update Student Session values through the separate Edit function. |
| BR-15 | LT-108387 + User request | A System Administrator in Japanese locale selects and saves Renseikai Student Session fields using 生徒名, 学年, 出欠連絡, 出欠状況, 欠席理由, and 備考; the table renders those selected Japanese headers. |

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| LT-108387 | BR-01–BR-04 | Display completeness; Conditional logic; Regression |
| LT-101751 | BR-05–BR-06 | Display completeness; Conditional logic; Regression |
| Core configuration | BR-07, BR-11 | Conditional logic; State transition; Display completeness |
| Core configuration | BR-08 | Permission logic; Negative |
| Core configuration | BR-09 | Conditional logic; Data integrity; Cross-tenant isolation |
| Core configuration | BR-12–BR-13 | State transition; Data integrity; Cross-user readback |
| LT-108387 + User request | BR-15 | Display completeness; State transition; Localization |
| User clarification | BR-10, BR-14 | Permission logic; Regression; Data integrity |
| User clarification + screenshot | BR-12 | Display completeness; Ordering / Sort; State transition; Validation |

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Display completeness | Component inventory; Negative assertion for excluded columns; Empty-value scenario |
| Conditional logic | Decision table for tenant × setting state × role |
| Permission logic | Permission matrix for System Administrator versus non-admin lesson-detail user |
| State transition | Configuration OFF → ON → saved layout and configuration change → refreshed layout |
| Data integrity | Save/readback and tenant-isolation regression; no Student Session mutation |
| Cross-user readback | Save as System Administrator, then open the configured table as a distinct HQ or CM Staff user in the same tenant |
| Localization | Japanese-locale component inventory using Jira-specified label text after administrator saves the selected layout |
| Ordering / Sort | Scenario using at least three selected fields with a non-default order; assert header order explicitly |
| Regression | Existing attendance persistence and separate Edit-function checks |
| Validation | Field-catalog completeness, duplicate/excluded selection behavior, and safe empty-state behavior if supported |

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| LT-108387 | Show all six Renseikai columns simultaneously with populated values. | Display completeness | Component inventory | High | Deep |
| LT-108387 | Hide Risk, Type, Attendance Notice, and Reallocate Flag in the Renseikai layout. | Conditional logic; Negative | Decision table; Negative | High | Deep |
| LT-101751 | Show all six EEA columns simultaneously with populated values. | Display completeness | Component inventory | High | Deep |
| LT-101751 | Keep Renseikai-only columns absent from the EEA layout. | Conditional logic; Negative | Decision table; Negative | High | Deep |
| Core configuration | With setting ON, System Administrator can open **Visible Columns** and sees all ten catalog fields. | Permission logic; Display completeness | Permission matrix; Component inventory | High | Deep |
| Core configuration | With setting OFF, the tenant cannot customize columns and another enabled tenant retains its own configuration. | Conditional logic; Cross-tenant isolation | Decision table; Negative | High | Deep |
| Core configuration | Non-System Administrator cannot access or persist a configuration change. | Permission logic; Negative | Permission matrix; Negative | High | Deep |
| Core configuration | System Administrator selects a subset of fields, saves, and a different HQ or CM Staff user sees exactly that subset after refresh. | State transition; Data integrity; Cross-user readback | CRUD/readback; Decision table | High | Deep |
| Core configuration | System Administrator reorders at least three selected fields and a different HQ or CM Staff user sees the saved relative order. | Ordering / Sort; State transition; Cross-user readback | Scenario | High | Deep |
| Core configuration | System Administrator excludes a field and a different HQ or CM Staff user sees the saved layout without the excluded field. | State transition; Data integrity; Cross-user readback | State transition; Regression | High | Deep |
| LT-108387 + User request | System Administrator customizes a Renseikai layout in Japanese locale; the saved table renders the selected Japanese headers after refresh. | Display completeness; State transition; Localization | Component inventory; CRUD/readback | High | Deep |
| User clarification | Table cells remain non-editable; after a System Administrator saves a layout, the separate Edit function remains the only update path for HQ or CM Staff. | Permission logic; Regression; Data integrity | Negative UI interaction; Regression | High | Deep |
| User clarification + screenshot | Scroll the Visible Columns list and confirm all ten fields are reachable exactly once. | Display completeness; Validation | Component inventory; Scroll scenario | Medium | Standard |

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| None identified | The feature changes column configuration and display only; it has no intended Student Session, attendance, or billing write path. | Confirm non-mutation through readback regression rather than treating UI configuration as a Student Session write. |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Tenant configuration isolation | A Core configuration leak can show the wrong field set to another partner and expose irrelevant data. | Configure Renseikai and EEA differently; refresh and use a second tenant session to prove layouts stay isolated. |
| Exact field completeness | Missing one requested field or retaining one excluded field defeats the compact-table purpose. | One component test per tenant that asserts every required and excluded field in the same table render. |
| System Administrator authorization | A non-admin configuration change would affect all applicable users in a tenant. | Explicit role matrix: System Administrator allowed; representative non-admin denied; configured layout still readable to an authorized viewer. |
| Cross-user layout visibility | A layout may be saved but not rendered for other staff members in the same tenant. | Save a layout as System Administrator, then use a distinct HQ or CM Staff session to assert the selected headers and their order. |
| Reordering persistence | A UI can save selected fields but lose relative order on refresh or render a default order. | Save a deliberately non-default order with three or more columns, reload, and assert the full header sequence. |
| Read-only boundary | Accidental inline editing risks corrupting synchronized attendance data. | Attempt direct cell interaction; edit with the separate function; refresh and confirm only the separate edit changes the persisted value. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Column-list scroll | The tenth field is below the initial viewport. | Scroll to the end and assert all ten unique field labels are accessible. |

## 6. Mandatory Edge-Case Assessment

| Area | Applicability | Coverage decision |
|---|---|---|
| A. Configuration thresholds | N/A | The setting is Boolean enablement with no numeric threshold or supported min/max range. Cover ON and OFF states instead. |
| B. Date / time / timezone | N/A | No new date or time logic is introduced. |
| C. Concurrent / stale state | N/A | The requirement does not state multi-admin concurrency behavior. Do not invent conflict-resolution expectations; retain saved-layout refresh coverage. |
| D. Permission & role | Applicable | System Administrator configures; representative non-admin is denied; cross-tenant access/isolation and setting OFF are covered. |
| E. State transition | Applicable | Cover setting OFF → ON, select/reorder/save → refresh, exclude → re-include, and ON tenant versus other/disabled tenant. |
| F. Cross-system / cross-surface | Applicable as regression | Configuration affects Salesforce Lesson Detail only. Verify no Student Session mutation and no unintended BO/Mobile change after configuration. |
| G. Downstream effects | Applicable to configuration save only | Cover the target tenant table re-render and isolation. Student Session, BO, and Mobile are expected to have **no** write or layout side effect. |
| H. Display completeness & ordering | Applicable | Complete field inventories, conditional layouts, exact text `Visible Columns`, non-default order, blank values, and column-list scroll are covered. |
| H.1 Spec–Figma mismatch | N/A | No Figma URL is present. The supplied screenshot is treated as the field-catalog evidence, not a Figma specification. |

## G. Downstream Effects Inventory

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner (TC) |
|---|---|---|---|
| System Administrator enables the setting for Tenant A | Tenant A exposes column-configuration controls; Tenant B remains unaffected. | Salesforce Lesson Custom Settings; Tenant A/B Lesson Detail | `custom-column-configuration` |
| System Administrator saves Tenant A field selection/order | Tenant A Lesson Detail headers and row cells match the saved list/order after refresh for the System Administrator and a different HQ or CM Staff user. | Salesforce Student Session table | `custom-column-configuration` |
| System Administrator excludes/re-includes a field | The target field disappears/reappears only in Tenant A; the previous configuration is not corrupted. | Salesforce Student Session table | `custom-column-configuration` |
| Any column configuration action | No Student Session, Attendance Status/Response/Reason/Note, BO, or Learner App value is written or changed. | Student Session; BO; Learner App | `read-only-and-data-regression` |
| Non-admin attempts configuration | No configuration is saved and the existing tenant layout remains unchanged. | Salesforce Lesson Custom Settings; Student Session table | `custom-column-configuration` |

## H. Display & Ordering Inventory

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| Renseikai Salesforce Lesson Detail — Student Session table | Student Name, Grade, Attendance Response, Attendance Status, Attendance Reason, Attendance Note | Risk, Type, Attendance Notice, Reallocate Flag absent | No source-defined order; do not assert order | None |
| EEA Salesforce Lesson Detail — Student Session table | Student Name, Grade, Type, Attendance Status, Attendance Reason, Reallocate Flag | Attendance Response, Attendance Note, Risk, Attendance Notice absent | No source-defined order; do not assert order | None |
| System Administrator column picker | Grade, Risk, Type, Attendance Response, Attendance Status, Attendance Notice, Attendance Reason, Reallocate Flag, Student Name, Attendance Note | Available only when target tenant setting is ON and user is System Administrator | Saved selected fields follow administrator-selected relative order | `Visible Columns` |
| Configured Salesforce Student Session table | Saved selected field set and current row values | Excluded fields absent; blank value remains blank; table is read-only | Saved selected field order | None |

## 7. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Renseikai compact field layout | Renseikai attendance status/clear-field cases | Existing cases assert attendance value behavior, not table columns. | ✅ One component case asserts all six required and all four excluded columns. Separate blank-value coverage is intentionally out of scope by user direction. |
| EEA compact field layout | No case in target PX suite 3534; existing EEA work covers different features. | None. | ✅ One component case asserts all six required and Renseikai-only absent columns. Separate BO-boundary coverage is intentionally out of scope by user direction. |
| Visible Columns catalog | No case in target PX suite 3534. | None. | ✅ Assert exact ten-field catalog, `Visible Columns` label, and scroll reachability. |
| Tenant setting and isolation | Existing tenant-specific Lesson Detail specs show isolation patterns only. | Conceptual only. | ✅ Cover ON/OFF behavior and separate Renseikai/EEA tenant layouts. |
| System Administrator authorization | Permission matrix has no custom-column permission case. | None. | ✅ Cover allowed admin and denied representative non-admin. |
| Selection/reorder persistence | No case in target PX suite 3534. | None. | ✅ Cover subset, excluded field, non-default order, save/refresh readback. |
| Cross-user saved-layout readback | No case in target PX suite 3534. | None. | ✅ After each System Administrator layout save, use a different HQ or CM Staff user to confirm the saved field set/order is rendered. |
| Renseikai Japanese custom layout | No Japanese-locale administrator configuration case in target PX suite 3534. | None. | ✅ In Japanese locale, select and save the Renseikai required field set using the six Jira-specified Japanese labels; refresh and assert those headers. |
| Read-only table regression | Existing attendance cases cover separate update flows. | Partial. | ✅ Prove no inline mutation and retained separate Edit path, including an HQ or CM Staff update after a System Administrator saves a custom layout. |
| Blank-value handling | Existing attendance cases cover values, not compact-table rendering. | Partial. | Deferred — user requested one field-layout case per tenant only. |

## 8. Suggested Test Suite Structure

```
epics/lesson/LT-108387-LT-101751-custom-student-session-table/test-cases/
├── tenant-student-session-columns.md         → LT-108387 + LT-101751: one exact field-layout case per tenant
├── custom-column-configuration.md            → Core: setting ON/OFF, System Administrator permission, catalog, selection, reorder, tenant isolation, Japanese custom-layout display
└── read-only-and-data-regression.md          → Core: no inline edit; separate Edit path and non-mutation regression
```

Each Markdown file has a matching Qase CSV in the same directory. Each local suite maps to a child suite under Qase parent `PX / 3534`: `Tenant Student Session Columns` (`3544`), `Custom Column Configuration` (`3543`), and `Read-only and Data Regression` (`3545`).
