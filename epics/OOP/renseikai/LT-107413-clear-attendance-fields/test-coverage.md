# Test Coverage: LT-107413 — Clear Attendance Notice and Attendance Reason in Salesforce

**Jira:** https://manabie.atlassian.net/browse/LT-107413  
**Date:** 2026-08-13

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---:|---|---|
| 1 | AC 01 | Changing Absent to Attend clears the displayed Attendance Notice and Attendance Reason selections in Salesforce. |
| 2 | AC 01 | Changing Late to Attend clears the displayed Attendance Notice and Attendance Reason selections in Salesforce. |
| 3 | AC 01 | Changing Leave Early to Attend clears the displayed Attendance Notice and Attendance Reason selections in Salesforce. |
| 4 | AC 01 | Clearing Attendance Status after Absent clears the displayed Attendance Notice and Attendance Reason selections. |
| 5 | AC 01 | Clearing Attendance Status after Late clears the displayed Attendance Notice and Attendance Reason selections. |
| 6 | AC 01 | Clearing Attendance Status after Leave Early clears the displayed Attendance Notice and Attendance Reason selections. |
| 7 | AC 02 | A selected Attendance Status has an x icon that clears its displayed value. |
| 8 | AC 02 | A selected Attendance Reason has an x icon that clears its displayed value. |
| 9 | AC 02 | A selected Attendance Notice has an x icon that clears its displayed value. |
| 10 | AC 03 | BO Collect Attendance in Lesson changes one student's Status to Attend and clears displayed Notice and Reason. |
| 11 | AC 03 | BO Collect Attendance in Report changes one student's Status to Attend and clears displayed Notice and Reason. |
| 12 | AC 03 | BO Bulk Collect Attendance in Calendar changes selected students' Status to Attend and clears displayed Notice and Reason for every selected student. |
| 13 | AC 04 | Saving a Salesforce correction from Absent, Late, or Leave Early to Attend synchronizes Attend, blank Notice, and blank Reason to BO. |
| 14 | AC 04 | Saving a cleared Salesforce Attendance Status synchronizes blank Status, blank Notice, and blank Reason to BO. |
| 15 | AC 04 | A saved Salesforce status correction synchronizes the resulting Attendance Status to Learner App for the same student and lesson. |

---

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC 01 | 1–6 | Conditional logic; State transition; Display completeness |
| AC 02 | 7–9 | Display completeness; Conditional logic |
| AC 03 | 10–12 | Display completeness; Conditional logic; State transition |
| AC 04 | 13–15 | State transition; Data integrity; Cross-system impact |

---

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Conditional logic | Decision Table; Negative Testing |
| State transition | State Transition Testing; CRUD Testing |
| Display completeness | Component Testing; Negative Testing |
| Data integrity | CRUD Testing; Regression Analysis |
| Cross-system impact | Regression Analysis; CRUD Testing |

---

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC 01 | Each absence state (Absent, Late, Leave Early) changed to Attend clears both dependent fields in the SF form. | Conditional logic; State transition; Display completeness | Decision Table; Component | High | Deep |
| AC 01 | Each absence state has its Status cleared; the SF form clears both dependent fields. | Conditional logic; State transition; Display completeness | Decision Table; Component | High | Deep |
| AC 01 | A non-qualifying change between absence statuses does not invoke the new clear behavior. | Conditional logic | Negative Testing | High | Standard |
| AC 02 | All three selected attendance controls expose an x icon, and clearing each control changes only that control unless AC 01's qualified status condition applies. | Display completeness; Conditional logic | Component; Negative Testing | Medium | Standard |
| AC 03 | Collect Attendance in Lesson changes one student to Attend and clears the displayed Notice and Reason. | Display completeness; Conditional logic; State transition | Component; Decision Table | High | Standard |
| AC 03 | Collect Attendance in Report changes one student to Attend and clears the displayed Notice and Reason. | Display completeness; Conditional logic; State transition | Component; Decision Table | High | Standard |
| AC 03 | Bulk Collect Attendance in Calendar BO changes every selected student to Attend and clears the displayed Notice and Reason for each. | Display completeness; Conditional logic; State transition | Component; Decision Table | High | Deep |
| AC 04 | A saved SF transition from every absence status to Attend is read back in BO as Attend with blank Notice and Reason, and in Learner App as Attend. | State transition; Data integrity; Cross-system impact | Decision Table; CRUD; Regression | Critical | Deep |
| AC 04 | A saved SF-cleared status is read back in BO with blank Status, Notice, and Reason, and in Learner App with blank Status. | State transition; Data integrity; Cross-system impact | Decision Table; CRUD; Regression | Critical | Deep |
| AC 04 | A failed or unsaved SF edit does not create a partial BO or Learner App update. | Data integrity; Cross-system impact | Negative Testing; Regression | High | Standard |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| SF-to-BO and Learner App synchronization | A stale absence value in BO or an incorrect Attendance Status in Learner App after an SF correction gives users contradictory attendance information. | For every source absence status and for cleared Status, save in SF; assert all three resulting values in BO and the resulting Attendance Status in Learner App. |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Conditional SF auto-clear | The behavior is conditional on both the previous and the newly selected status; missing one source state leaves stale absence information. | Decision table: Absent/Late/Leave Early × Attend/blank; assert both dependent fields after each selection. |
| Bulk Calendar BO selection | A bulk action can leave some selected students unchanged or apply the wrong visible value. | Use two selected students with different original absence statuses; choose Attend once; assert Attend is selected for both before saving. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Clear affordances and individual BO entry points | Missing x icons or an unavailable Attend option block the correction workflow, but do not themselves create cross-system data inconsistency. | Component coverage for the three SF controls and each named BO surface. |

---

## 6. Mandatory Edge-Case Assessment

| Pattern | Applicability | Coverage decision |
|---|---|---|
| A. Configuration-driven thresholds | N/A | No threshold or tenant configuration is specified. |
| B. Date / time logic | N/A | No date or time behavior is specified. |
| C. Concurrent / stale state | N/A | No shared-capacity or time-gated behavior is specified; this is revisited only as a partial-update check for AC 04. |
| D. Permission & role | N/A | The ticket introduces no role or permission change. |
| E. State transition | Yes | Cover each documented source absence status to Attend and blank; cover a non-qualifying absence-to-absence change as a negative case. |
| F. Cross-system / cross-surface | Yes | Save in SF and read all resulting field values in BO; include unsaved/failed-edit no-partial-update coverage. |
| G. Downstream effects | Yes | AC 04 writes a Student Session and affects BO Collect Attendance; inventory below maps both effects to coverage. No inverse action, counter, child-record, peer-surface, or notification behavior is specified. |
| H. Display completeness & ordering | Yes | Inventory below maps each SF and BO form/control. No sort, exact tooltip/error text, empty-state, or pagination behavior is specified. |
| H.1 Spec–Figma mismatch | N/A | No Figma URL is present in the approved spec. |

### G. Downstream Effects Inventory

| Primary Action | Downstream Effect | Affected Entity / Surface | Coverage Strategy Row |
|---|---|---|---|
| Save SF status change to Attend | Student Session stores Attend with cleared Notice and Reason. | Salesforce Student Session | AC 04 — SF transition to Attend read-back |
| Save SF status change to Attend | BO shows Attend with blank Notice and Reason for the same student and lesson. | BO Collect Attendance | AC 04 — SF transition to Attend read-back |
| Save SF status change to Attend | Learner App shows Attend for the same student and lesson. | Learner App lesson attendance | AC 04 — SF transition to Attend read-back |
| Save SF-cleared Status | Student Session stores blank Status, Notice, and Reason. | Salesforce Student Session | AC 04 — SF-cleared Status read-back |
| Save SF-cleared Status | BO shows blank Status, Notice, and Reason for the same student and lesson. | BO Collect Attendance | AC 04 — SF-cleared Status read-back |
| Save SF-cleared Status | Learner App shows blank Attendance Status for the same student and lesson. | Learner App lesson attendance | AC 04 — SF-cleared Status read-back |
| Cancel or failed SF edit | No partial values appear in BO or Learner App. | BO Collect Attendance; Learner App lesson attendance | AC 04 — unsaved/failed edit no-partial-update |

### H. Display & Ordering Inventory

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| Salesforce Edit Student Session | Attendance Status, Attendance Reason, Attendance Notice | x icon appears for each selected value; changing Status to Attend/blank clears Notice and Reason | None | None specified |
| BO Collect Attendance in Lesson | Attendance Status control with Attend option | N/A | None | None specified |
| BO Collect Attendance in Report | Attendance Status control with Attend option | N/A | None | None specified |
| BO Bulk Collect Attendance in Calendar | Attendance Status bulk control with Attend option | Applies to selected students | None | None specified |
| BO Collect Attendance read-back | Attendance Status, Attendance Notice, Attendance Reason | Values depend on saved SF correction | None | None specified |
| Learner App lesson attendance | Attendance Status | Value depends on saved SF correction | None | None specified |

---

## 7. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| SF auto-clear after Absent/Late/Leave Early becomes Attend | PX-1379 sets attendance values; PX-13061 syncs a selected reason from SF to BO. | Existing cases set values; they do not clear dependent fields after a status correction. | ✅ Decision-table coverage for all three source statuses. |
| SF auto-clear after Status becomes blank | PX-9743 cancels an Attendance Reason change. | Cancel behavior exists; clearing Status and dependent form values does not. | ✅ Decision-table coverage for all three source statuses. |
| SF x icon for Status, Reason, and Notice | None in suite 274. | None. | ✅ Component coverage with one selected value in each field. |
| BO Attend in Lesson / Report / Calendar bulk collection | PX-12665 and PX-13061 cover single-flow reason updates; suite 274 has no named Report or Calendar bulk Attend coverage. | Partial for attendance context only. | ✅ One coverage path per BO entry point; bulk path uses at least two selected students. |
| SF correction synchronized to BO and Learner App | PX-9742 and PX-13061 verify a selected SF Attendance Reason is visible in BO. | They do not verify Attend/blank triad from SF or a Learner App Attendance Status read-back. | ✅ Cross-system read-back for status-to-Attend and status-cleared variants. |
| No partial BO or Learner App update before a successful SF save | PX-9743 covers Cancel for Reason only. | Partial cancel concept; no SF-to-BO or Learner App assertion. | ✅ Cancel/failed-save regression coverage for BO and Learner App read-back. |

---

## 8. Suggested Test Suite Structure

```text
epics/OOP/renseikai/LT-107413-clear-attendance-fields/test-cases/
├── sf-attendance-clearing.md      → AC 01 / AC 02 — SF status decision table and clear-icon components
├── bo-attend-entry-points.md      → AC 03 — Lesson, Report, and Calendar BO bulk Attend selection
└── sf-bo-attendance-sync.md       → AC 04 — saved SF correction read-back and no-partial-update regression
```
