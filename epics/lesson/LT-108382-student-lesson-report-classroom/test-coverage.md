# Test Coverage: LT-108382 — Student Lesson Report with Classroom

**Jira:** https://manabie.atlassian.net/browse/LT-108382  
**Qase target:** PX / suite 3713 — EEA \| Core \| Student's Lesson Report or Lesson Classroom info in Lesson object  
**Date:** 2026-10-12  
**Scope:** Core Salesforce report, opened from Student detail; report display, Lesson Classroom derivation, Student Session navigation, and teacher attendance workflow.

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---:|---|---|
| BR-01 | AC 01.1 | Centre Staff can open the Student Lesson Report from the Student detail page. |
| BR-02 | AC 02.1 | The report contains the selected student's past and future lessons in the current academic year. |
| BR-03 | AC 02.2 | The report displays all specified lesson, attendance, and Student Session columns. |
| BR-04 | AC 02.3 | Lesson Classroom is a new display column derived from the Lesson's related Classroom. |
| BR-05 | AC 02.4 | Student Session is a link to its detail page. |
| BR-06 | AC 03.1 | A teacher can confirm and update a student's attendance through the report workflow. |
| BR-07 | AC 01.1 | The report-link provision/configuration scope is not specified despite core scope. |

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC 01.1 | BR-01, BR-07 | Permission logic; Conditional logic; Display completeness |
| AC 02.1 | BR-02 | Conditional logic; Boundary/range logic; Display completeness |
| AC 02.2 | BR-03 | Display completeness; Data integrity |
| AC 02.3 | BR-04 | Data integrity; Display completeness; Cross-system impact |
| AC 02.4 | BR-05 | Data integrity; Navigation; Display completeness |
| AC 03.1 | BR-06 | Permission logic; State transition; Data integrity; Cross-system impact |

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Permission logic | Permission Matrix; Decision Table |
| Conditional logic | Decision Table; Negative |
| Boundary/range logic | Boundary Value Analysis; Negative |
| Display completeness | Component; Negative (field absent) |
| Data integrity | CRUD; Regression |
| Cross-system impact | Regression; CRUD/readback |
| Navigation | Scenario; Regression |
| State transition | State Transition; CRUD/readback |

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC 01.1 | An authorized Centre Staff user opens the selected student's report from the Student detail page and receives that student's report context. | Permission logic; Display completeness | Permission Matrix; Component | High | Standard |
| AC 01.1 | An unauthorized role and a user outside the student's permitted location cannot use the link to obtain the student's report data. | Permission logic; Conditional logic | Permission Matrix; Negative | High | Deep |
| AC 01.1 | The report-link configuration branch is verified once product confirms whether the core feature provisions it or a partner manages it. | Conditional logic | Decision Table | Medium | Deferred pending clarification |
| AC 02.1 | The current-AY report includes one past and one future lesson for the selected student and excludes a lesson outside the current AY. | Conditional logic; Boundary/range logic | Decision Table; Boundary Value Analysis | High | Deep |
| AC 02.1 | The report has a defined, stable empty state when the selected student has no lessons in the current AY. | Display completeness; Negative | Component; Negative | Medium | Deferred pending clarification |
| AC 02.2 | One report row/component simultaneously displays Student Name, Lesson Date, Location, Start Time, End Time, Lesson Name, Lesson Teacher, Lesson Classroom, Attendance Status, Absent Reason, and Student Session. | Display completeness | Component | High | Deep |
| AC 02.3 | A Lesson with a related Classroom shows that exact Classroom value in the corresponding report row and does not use another lesson's classroom. | Data integrity; Cross-system impact; Display completeness | CRUD/readback; Regression; Component | High | Deep |
| AC 02.3 | A Lesson without a related Classroom renders the product-approved blank/placeholder behavior without breaking the report. | Conditional logic; Display completeness | Decision Table; Negative | Medium | Deferred pending clarification |
| AC 02.4 | Selecting a Student Session value opens the detail for the same Student Session represented by the row. | Data integrity; Navigation | Scenario; Regression | Medium | Standard |
| AC 03.1 | An authorized teacher confirms existing attendance and updates the product-defined attendance fields, then sees the saved values after reload. | Permission logic; State transition; Data integrity | Permission Matrix; CRUD/readback; State Transition | Critical | Deep |
| AC 03.1 | A user without teacher attendance-edit permission cannot change attendance through the report workflow. | Permission logic; Conditional logic | Permission Matrix; Negative | High | Deep |
| AC 03.1 | A save/retry does not create duplicate Student Session attendance records or overwrite a different student's attendance. | Data integrity; Cross-system impact | CRUD/readback; Regression | High | Deep |

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Teacher attendance update | An incorrect update can write the wrong student's attendance or leave staff with a false confirmation of saved data. | Use two students with distinct initial statuses; update one as an authorized teacher; reload and reconcile both records. Repeat the save/retry path. |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Student-scoped access | A report link or filter leak can expose another student's lesson/attendance data. | Cover permitted Centre Staff, restricted-location user, teacher with valid access, and unauthorized role. |
| Current-AY filtering | Incorrect boundaries can omit usable lessons or include past/future years in a customer-facing report. | Prepare lessons immediately inside and outside the defined AY and assert inclusion/exclusion. |
| Lesson Classroom mapping | The Classroom lives on a different object; an incorrect join can show blank or mismatched classroom data. | Use at least two lessons with distinct classrooms and compare each exact row mapping. |
| Required report fields | Missing/misaligned fields make the report unusable for communication and attendance work. | One component case asserts every required field in a single row. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Student Session navigation | A wrong or broken link disrupts follow-up and can open another student's data. | Open the link and compare the destination ID/student/lesson with the source row. |
| Undefined empty/sort behavior | The ticket leaves empty results, empty classroom, and ordering undefined. | Keep cases blocked until product supplies exact expected behavior; do not infer it. |

## 6. Mandatory Edge-Case Assessment

| Area | Applicability | Coverage decision |
|---|---|---|
| A. Configuration thresholds | N/A | No numeric threshold or supported configuration value is specified. Link ownership/configuration is a clarification item, not a threshold. |
| B. Date / time / timezone | Applicable | Current-AY membership is date-driven. Cover only values immediately inside/outside the confirmed AY boundary. Timezone and cross-midnight behavior are N/A unless the product defines a date evaluation time. |
| C. Concurrent / stale state | Applicable | Attendance is a mutable shared Student Session value. Cover save/retry/readback and confirm that another student's record is unchanged. |
| D. Permission & role | Applicable | Cover authorized Centre Staff, authorized teacher attendance editing, and roles/users that must not view or edit. Cross-tenant/feature-flag checks are N/A until link configuration is defined. |
| E. State transition | Applicable | Cover an allowed attendance change and blocked editing for a role without permission. Lesson-status transitions are N/A because the ticket does not change lesson state. |
| F. Cross-system / cross-surface | Applicable | Validate source Lesson/Student Session relationships against the Salesforce report row and the Student Session destination. No BO/Mobile change is in scope. |
| G. Downstream effects | Applicable | Attendance update readback, record isolation, and report-row freshness each receive a dedicated case. Classroom display is read-only; it creates no downstream entity. |
| H. Display completeness & ordering | Applicable | Assert all required fields together, distinct classroom mapping, Student Session link, and product-approved empty states. Sorting and pagination are not specified; coverage is deferred rather than assumed. |
| H.1 Spec–Figma mismatch | N/A | No Figma URL is present in the approved spec. |

## G. Downstream Effects Inventory

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner (TC) |
|---|---|---|---|
| Teacher saves attendance for Student A from the report workflow | The same Student A Student Session stores the updated attendance and shows it after report reload. | Salesforce Student Session → Student Lesson Report | `attendance-update-persistence` |
| Teacher saves attendance for Student A from the report workflow | Student B's Student Session and attendance remain unchanged. | Salesforce Student Session | `attendance-update-isolation` |
| Teacher retries/submits the same attendance update | The report and Student Session retain one final intended value; no duplicate/extra attendance record is introduced. | Salesforce Student Session → Student Lesson Report | `attendance-update-idempotency` |

Inverse action: N/A. The ticket specifies attendance confirmation/update, not an inverse create/delete operation.

## H. Display & Ordering Inventory

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| Salesforce Student detail | Student Lesson Report entry point | Visibility/configuration by authorized role or partner setup is unspecified | N/A | `生徒別授業一覧` if retained as the configured link label; exact label requires confirmation |
| Student Lesson Report row | Student Name; Lesson Date; Location; Start Time; End Time; Lesson Name; Lesson Teacher; Lesson Classroom; Attendance Status; Absent Reason; Student Session | Lesson Classroom empty behavior; report empty state | Not specified | N/A |
| Student Session detail destination | Same Student Session, Student, and Lesson represented by source row | N/A | N/A | N/A |
| Attendance update control | Product-defined editable attendance fields; save feedback; persisted row values | Availability by teacher permission | N/A | Exact labels/save feedback not specified |

## 7. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Open report from Student detail with student-scoped authorization | Qase PX suite 3713 has 0 cases. | None | ✅ Authorized Centre Staff entry and unauthorized/restricted-access cases. |
| Current-AY inclusion/exclusion and empty state | Qase PX suite 3713 has 0 cases. | None | ✅ Boundary case once current-AY rule is confirmed; empty-state case once UI contract is confirmed. |
| Required report fields and Classroom mapping | Qase PX suite 3713 has 0 cases. | None | ✅ Component completeness case and distinct-classroom mapping case. |
| Student Session link integrity | Qase PX suite 3713 has 0 cases. | None | ✅ Navigate from a row and reconcile the destination Student Session. |
| Teacher attendance update, authorization, and persistence | Qase PX suite 3713 has 0 cases. Related LT-108378 only covers a separate BO Attendance Remark surface. | Partial, cross-feature only. | ✅ Create Salesforce report-workflow cases; do not reuse BO-only assertions as target coverage. |
| Report ordering/pagination, missing Classroom, link ownership | Ticket has no defined expected behavior. | None. | Deferred pending answers to clarification questions 1, 2, 4, and 5. |

## 8. Suggested Test Suite Structure

```text
epics/lesson/LT-108382-student-lesson-report-classroom/test-cases/
├── report-entry-and-access.md             → AC 01.1: entry point, student scope, role access
├── report-current-ay-and-display.md       → AC 02.1, AC 02.2: current-AY boundaries and full report row
├── classroom-and-session-navigation.md    → AC 02.3, AC 02.4: classroom mapping and Student Session link
└── attendance-confirmation-and-update.md  → AC 03.1: permission, update, persistence, retry/isolation
```

Each Markdown file will have a matching Qase CSV file. Cases depending on undefined behavior remain explicitly blocked until the corresponding clarification answer is available.
