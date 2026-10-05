# Test Coverage: LT-107664 — Koyu Lesson Quiz and Total Score

**Jira:** https://manabie.atlassian.net/browse/LT-107664  
**Date:** 2026-10-05

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---:|---|---|
| 1 | AC 1.1 | With SF configuration OFF, staff see editable Lesson Quiz. |
| 2 | AC 1.1 | With SF configuration OFF, Lesson Quiz retains automatic `%` formatting. |
| 3 | AC 1.1 | With SF configuration OFF, Total Score is hidden. |
| 4 | AC 1.1 | With SF configuration OFF, Test Result is hidden. |
| 5 | AC 1.2 | With App internal configuration OFF, the App shows Lesson Quiz and hides both new fields. |
| 6 | AC 2.1.1 | With SF configuration ON, staff do not see Lesson Quiz. |
| 7 | AC 2.1.1 | With SF configuration ON, staff can edit Total Score. |
| 8 | AC 2.1.1 | Total Score is optional and accepts negative values with at most one decimal place. |
| 9 | AC 2.1.1 | Invalid Total Score blocks Save and displays the locale-appropriate validation message. |
| 10 | AC 2.1.1 | With SF configuration ON, staff can edit Test Result. |
| 11 | AC 2.1.1 | Test Result is optional and accepts negative values with at most one decimal place. |
| 12 | AC 2.1.1 | Invalid Test Result blocks Save and displays the locale-appropriate validation message. |
| 13 | AC 2.1.1 | A successful save is reflected across SF, BO, and the App. |
| 14 | AC 2.1.2 | With App internal configuration ON, students and parents see Total Score and Test Result read-only; Lesson Quiz is hidden. |
| 15 | Localization | Labels and validation messages display in the active EN or JP locale only. |
| 16 | Scope | The two values are independent per-student Lesson Report Detail values; no calculation, migration, analytics change, or Lesson Quiz behavior change is included. |

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---:|---|
| AC 1.1 | 1–4 | Conditional logic; Display completeness; Regression |
| AC 1.1 | 2 | Data integrity; Display completeness |
| AC 1.2 | 5 | Conditional logic; Display completeness; Permission logic |
| AC 2.1.1 | 6, 7, 10 | Conditional logic; Display completeness; Permission logic |
| AC 2.1.1 | 8, 11 | Validation logic; Boundary/range logic |
| AC 2.1.1 | 9, 12 | Validation logic; Negative; Data integrity |
| AC 2.1.1 | 13, 16 | Data integrity; Cross-system impact; CRUD |
| AC 2.1.2 | 14 | Conditional logic; Display completeness; Permission logic; State transition |
| Localization | 15 | Display completeness; Validation logic |
| Scope | 16 | Data integrity; Cross-system impact; Negative |

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Conditional logic | Decision Table; Negative |
| Validation logic | Equivalence Partitioning; Negative |
| Boundary/range logic | Boundary Value Analysis; Negative |
| Permission logic | Permission Matrix; Decision Table |
| Data integrity | CRUD; Regression; Decision Table |
| Cross-system impact | Regression; CRUD; Component |
| Display completeness | Component; Negative |
| State transition | State Transition; Regression |

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC 1.1 | SF config OFF: staff sees only editable Lesson Quiz; automatic `%` behavior is unchanged; new fields are absent. | Conditional; Display completeness; Regression | Decision Table; Component; Regression | High | Deep |
| AC 1.1 | BO config OFF: staff sees only editable Lesson Quiz; new fields are absent. | Conditional; Display completeness; Regression | Decision Table; Component; Regression | High | Deep |
| AC 1.2 | App config OFF: student and parent see only read-only Lesson Quiz in a published report; new fields are absent. | Conditional; Display completeness; Permission | Decision Table; Component; Permission Matrix | High | Deep |
| AC 2.1.1 | SF config ON: staff sees editable Total Score and Test Result, and Lesson Quiz is absent. | Conditional; Display completeness | Decision Table; Component; Negative | High | Deep |
| AC 2.1.1 | BO config ON: staff sees editable Total Score and Test Result, and Lesson Quiz is absent. | Conditional; Display completeness | Decision Table; Component; Negative | High | Deep |
| AC 2.1.1 | Each field accepts blank, zero, positive/negative integers, and positive/negative one-decimal values. | Validation; Boundary/range | Equivalence Partitioning; BVA | High | Deep |
| AC 2.1.1 | Each field rejects more than one decimal, non-numeric input, malformed signs, and values exceeding the configured Salesforce field precision; Save is blocked and the prior values remain. | Validation; Boundary/range; Data integrity | Equivalence Partitioning; BVA; Negative | Critical | Deep |
| AC 2.1.1 | EN and JP validation messages are exact for invalid Total Score and invalid Test Result. | Validation; Display completeness | Negative; Component | Medium | Standard |
| AC 2.1.1 | A staff member saves distinct scores for Student A and Student B in the same group lesson without cross-student overwrite. | Data integrity; Cross-system | CRUD; Decision Table; Regression | Critical | Deep |
| AC 2.1.1 | A value saved from SF is read back in BO and, after the normal published-report condition, App; a value saved in BO is read back in SF and App. | Cross-system; State transition | CRUD; Regression; State Transition | Critical | Deep |
| AC 2.1.1 | Updating one new score preserves the other new score and the inactive Lesson Quiz value. | Data integrity; Regression | CRUD; Regression; Negative | High | Deep |
| AC 2.1.1 | Staff role matrix: every permitted staff role can view/edit the active layout; no unauthorised user gains a write control. | Permission; Conditional | Permission Matrix; Decision Table | High | Standard |
| AC 2.1.2 | App config ON: student and parent see both exact per-student scores read-only, while Lesson Quiz is absent. | Display completeness; Permission; State transition | Component; Permission Matrix; State Transition | High | Deep |
| Localization | EN and JP labels are exact on each active SF, BO, and App score component. | Display completeness | Component; Negative | Medium | Standard |
| Scope | No calculation is made between Total Score and Test Result; an existing record's inactive-layout values are retained across config ON/OFF transitions. | Data integrity; Conditional | Decision Table; Regression | High | Deep |
| Scope | Koyu's SF custom setting and BO/App internal config are independently applied to their stated surfaces without layout leakage to another organization. | Conditional; Permission; Cross-system | Decision Table; Permission Matrix; Regression | High | Deep |

### 4.5 Mandatory edge-case checklist

| Pattern | Applicability | Coverage decision |
|---|---|---|
| A. Configuration-driven thresholds | Yes — binary configuration controls layout rather than a numeric threshold. | Test both ON/OFF states, state change after data exists, preservation of hidden values, and tenant isolation. Numeric min/max threshold tests are N/A. |
| B. Date / time | N/A — this feature introduces no date, time, deadline, or timezone rule. | No date test cases. App read visibility uses the existing published-report condition only. |
| C. Concurrent / stale state | Yes — the same per-student report detail can be opened in SF and BO. | Add a stale-read regression: save a changed score on one staff surface and confirm the other surface/App does not retain an old score after refresh. Double-submit behavior is not specified; do not infer duplicate-write semantics. |
| D. Permission & role | Yes. | Test all defined staff categories, student, and parent; validate no edit controls in App and no cross-tenant Koyu layout leakage. |
| E. State transition | Yes — App visibility follows the established published-report lifecycle. | Verify App score display after publication and absence/non-exposure before the baseline published-report condition. |
| F. Cross-system / cross-surface | Yes. | Verify SF ↔ BO read-back and published App read-back for values saved from each staff surface; confirm invalid save creates no cross-surface partial state. |
| G. Downstream effects | Yes — score update writes a per-student detail and propagates to multiple read surfaces. | See Section G; every non-empty effect maps to coverage strategy rows. |
| H. Display completeness & ordering | Yes — five UI components are affected; no order, pagination, tooltip, or empty-state rule is specified. | See Section H; require component checks with concrete field values and exact validation text. |
| H.1 Spec–Figma mismatch | N/A — PRD-focused scope. The Jira/PRD link to Figma was intentionally not copied into this spec or analyzed. | Do not treat visual details as confirmed; perform a separate Spec–Figma comparison before final visual-design sign-off or if new Figma-derived scope is requested. |

### Downstream Effects Inventory Table (Section G)

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner (TC group) |
|---|---|---|
| Save Total Score for Student A in SF | Only Student A's Lesson Report Detail stores the value; Student B's existing value is unchanged. | Per-student Lesson Report Detail | Per-student isolation and SF-save cases |
| Save Test Result for Student A in BO | Only Student A's Lesson Report Detail stores the value; Student B's existing value is unchanged. | Per-student Lesson Report Detail | Per-student isolation and BO-save cases |
| Valid score save from SF or BO | Exact values are visible on the counterpart staff surface. | SF Lesson Report / BO Lesson Report | Cross-surface read-back cases |
| Valid score save followed by publication | Exact values are visible read-only to the applicable student/parent. | Learner App Lesson Report | Published App cases |
| Invalid score save | No edited field value is persisted or propagated; previous values remain. | Source surface; counterpart surface; App | Invalid-save integrity cases |
| Toggle SF configuration OFF/ON after scores exist | SF swaps layouts but retains stored new scores and existing Lesson Quiz value. | SF Lesson Report Detail | Config preservation cases |
| Toggle BO/App internal configuration OFF/ON after scores exist | BO/App swap layouts but retain stored new scores and existing Lesson Quiz value. | BO Lesson Report; Learner App | Config preservation cases |

No child entity, counter, notification, deletion, or inverse CRUD action is added by this feature. The inverse of configuration ON/OFF is explicitly covered because it changes visibility and may conceal existing data.

### Display & Ordering Inventory Table (Section H)

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| SF Lesson Report tab / Lesson Report page | Active-layout fields: Lesson Quiz **or** Total Score + Test Result | Config OFF/ON; editable staff fields | None | Active-locale validation error: `Only single-digit decimal numbers are allowed.` / `1桁の少数までの数値のみ使用できます` |
| BO Lesson Report | Active-layout fields: Lesson Quiz **or** Total Score + Test Result | Internal config OFF/ON; editable staff fields | None | Same active-locale validation error |
| Learner App Lesson Report — student | Active-layout fields read-only for the student | Internal config OFF/ON; published report | None | EN labels: `Total Score`, `Test Result`; JP labels: `満点`, `テスト結果` |
| Learner App Lesson Report — parent | Active-layout fields read-only for the selected child | Internal config OFF/ON; published report | None | EN labels: `Total Score`, `Test Result`; JP labels: `満点`, `テスト結果` |
| Per-student group-lesson detail | Student A and Student B retain their own exact Total Score/Test Result values | One student changed; peer unchanged | None | None |

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Per-student score isolation | The confirmed storage target is Lesson Report Detail. A lesson-level write or propagation bug could overwrite a peer student's score. | Use a group lesson with two named students and distinct negative/decimal values; save from SF and BO, then read each detail and App identity separately. |
| Invalid-save integrity | A validation gap could persist malformed scoring data or create different values on SF and BO/App. | Partition valid/invalid values for each field and assert Save is blocked with no source/counterpart/App mutation. |
| SF → BO → App synchronization | The feature changes a shared report path; data can be correct at the write source yet stale or misrouted downstream. | Run bidirectional staff save/read-back plus published-report App verification with exact values. |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Configuration layout isolation and preservation | Two controls govern different surfaces. A wrong mapping can expose both layouts, erase hidden data, or affect a non-Koyu organization. | Decision table across SF custom setting × BO/App internal config × data-exists state; verify ON/OFF round trips and tenant isolation. |
| Legacy Lesson Quiz regression | Config OFF must leave a production percentage field untouched. | Use an existing Lesson Quiz value, edit it, assert automatic `%`, and prove both new fields are absent across all applicable surfaces. |
| Published-report App rendering | The App is read-only and only displays report data at the established lifecycle state. | Verify values before/after publication and separately as student and parent. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| EN/JP localization | Wrong labels or bilingual error presentation is user-visible but does not corrupt score data. | Assert exact field labels and the one-language error message under each locale on all stated surfaces. |
| Optional blank values | Clearing a score must not make a retained peer value disappear or replace it with an unintended calculated value. | Save blank for one field/student and assert blank/read-only rendering plus preservation of the other field and other student. |

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Legacy Lesson Quiz/editing and report-detail baseline | `epics/lesson/lesson report/LT-102393-lesson-report/test-coverage.md` — direct group/individual report editing | Partial — baseline editing exists, but no Koyu flag/layout branch or numeric score rules. | ✅ Config OFF preservation and config ON field replacement. |
| Per-student report-detail persistence and cross-surface read-back | `epics/lesson/lesson report/LT-57816-copy-lesson-report-values/test-coverage.md` | Partial — it validates shared values copied to every detail; this change requires values to remain unique per detail. | ✅ Two-student isolation, SF/BO source reads, and published App read-back. |
| Exact score validation | No directly matching local case found for Total Score/Test Result. | None. | ✅ Blank/zero, negative, positive, one-decimal, over-precision, malformed, and schema-range partitions. |
| Koyu configuration mapping | No Koyu Lesson Report configuration case found. | None. | ✅ SF custom-setting versus BO/App internal-config layout matrix and ON/OFF value preservation. |
| Student/parent App read-only layout | Existing domain baseline covers published report visibility only. | Partial — it does not name the new score fields or parent parity. | ✅ Both fields, exact labels/values, no App edit control, student/parent parity. |
| Locale-specific score labels/errors | No direct local case found. | None. | ✅ EN and JP component/text assertions. |

## 7. Suggested Test Suite Structure

```text
epics/OOP/koyu/LT-107664-lesson-quiz-total-score/test-cases/
├── 01-configured-layouts.md              → AC 1.1, 1.2, 2.1.1, 2.1.2 — SF/BO/App ON/OFF decision table and legacy regression
├── 02-score-validation-and-localization.md → AC 2.1.1, Localization — optional numeric partitions, blocked save, exact EN/JP text
├── 03-score-detail-sync.md               → AC 2.1.1, 2.1.2 — per-student detail isolation, SF↔BO↔App propagation, publication state
└── 04-permissions-and-config-isolation.md → AC 1.1–2.1.2 — staff/student/parent matrix, tenant isolation, retained data across toggles
```

Estimated coverage: 30–36 test cases. No test cases have been generated in this phase.
