# Test Coverage: LT-96188 — Add Student Classification to Event and Lesson Calendar

**Jira:** https://manabie.atlassian.net/browse/LT-96188
**Spec:** input/specs/LT-96188: Add Student Classification to Event and Lesson Calendar/spec.md
**Date:** 2026-05-14
**Platform:** Salesforce (SF only)
**Partner:** Renseikai (Renseikai_Recovery)
**Dependency:** PBT-2485 (student_classification field) must be deployed before testing

---

## 1. Business Rules Extracted

| #   | AC                | Business Rule                                                                                                          |
| --- | ----------------- | ---------------------------------------------------------------------------------------------------------------------- |
| 1   | AC 01.1           | `student_classification` displayed in Event Participant List as a read-only column                                     |
| 2   | AC 01.1           | When `student_classification` is null, the column displays **blank** (empty cell)                                      |
| 3   | AC 01.2           | `student_classification` displayed in Lesson Calendar Student Session list as a read-only column                       |
| 4   | AC 01.2           | When `student_classification` is null in Lesson Calendar, displays **blank**                                           |
| 5   | AC 02.1           | `student_classification` multi-select picklist filter added to Add Master Participant popup, below Type filter         |
| 6   | AC 02.1–02.4      | Filter default state: empty (no selection = show all students)                                                         |
| 7   | AC 02.1–02.4      | Multi-select filter uses **OR logic** — returns students matching ANY selected value                                   |
| 8a  | AC 02.2           | `student_classification` filter added to **Event Master → Assign to Event** popup, below Type filter                   |
| 8b  | AC 02.2           | `student_classification` filter added to **Activity Event → Assign to Event** popup, below Type filter                 |
| 9   | AC 02.3           | `student_classification` filter added to Lesson Calendar Student List Filter (left panel), below Type filter           |
| 10  | AC 02.4           | `student_classification` filter added to Add Student Filter in Lesson Detail, below Type filter                        |
| 11  | AC 03.1 [comment] | `student_classification` column shown in Collect Event Attendance page (dev missed; in scope for test)                 |
| 12  | AC 03.2 [comment] | `student_classification` column included in CSV Download Participants (dev missed; in scope for test)                  |
| 13  | AC 02.1–02.4      | Filter picklist values sourced **dynamically** from `student_classification` picklist field definition (not hardcoded) |
| 14  | AC 02.1–02.4      | Type filter already exists in all 4 filter surfaces; classification filter placed directly below it                    |

---

## 2. Logic Type Categorization

| AC      | Business Rule #  | Logic Type                             |
| ------- | ---------------- | -------------------------------------- |
| AC 01.1 | 1, 2             | Conditional logic, Cross-system impact |
| AC 01.2 | 3, 4             | Conditional logic, Cross-system impact |
| AC 02.1 | 5, 6, 7, 13, 14  | Conditional logic, Validation logic    |
| AC 02.2 | 8a, 8b, 6, 7     | Conditional logic, Permission logic    |
| AC 02.3 | 9, 6, 7, 13, 14  | Conditional logic, Validation logic    |
| AC 02.4 | 10, 6, 7, 13, 14 | Conditional logic, Validation logic    |
| AC 03.1 | 11               | Cross-system impact, Validation logic  |
| AC 03.2 | 12               | Cross-system impact, Validation logic  |

---

## 3. Test Technique Selection

| Logic Type          | Applicable Techniques                                      |
| ------------------- | ---------------------------------------------------------- |
| Conditional logic   | Decision Table, Equivalence Partitioning, Negative Testing |
| Validation logic    | Equivalence Partitioning, Negative Testing                 |
| Cross-system impact | Regression Analysis, CRUD Testing                          |
| Permission logic    | Permission Matrix                                          |

---

## 4. Structured Coverage Strategy

| AC      | Business Rule Summary                                                         | Logic Type                | Test Technique                             | Risk Level | Coverage Depth |
| ------- | ----------------------------------------------------------------------------- | ------------------------- | ------------------------------------------ | ---------- | -------------- |
| AC 01.1 | Column shown in Event Participant List with value                             | Conditional, Cross-system | CRUD Testing, Equivalence Partitioning     | High       | Standard       |
| AC 01.1 | Column blank when student_classification = null                               | Conditional               | Equivalence Partitioning, Negative Testing | Medium     | Standard       |
| AC 01.2 | Column shown in Lesson Calendar Student Session with value                    | Conditional, Cross-system | CRUD Testing, Equivalence Partitioning     | High       | Standard       |
| AC 01.2 | Column blank when student_classification = null (Lesson Calendar)             | Conditional               | Equivalence Partitioning, Negative Testing | Medium     | Standard       |
| AC 02.1 | Filter appears in Add Master Participant popup below Type filter              | Validation, Conditional   | CRUD Testing                               | High       | Standard       |
| AC 02.1 | Filter default = empty → all students returned                                | Conditional               | Decision Table                             | Medium     | Standard       |
| AC 02.1 | Single value selected → correct students returned                             | Conditional               | Decision Table, Equivalence Partitioning   | High       | Standard       |
| AC 02.1 | Multiple values selected → OR logic (union of matches)                        | Conditional               | Decision Table                             | High       | Standard       |
| AC 02.1 | Filter values are dynamic from picklist field (not hardcoded)                 | Validation                | Equivalence Partitioning                   | Medium     | Smoke          |
| AC 02.2 | Filter appears in Event Master → Assign to Event popup below Type filter      | Validation, Conditional   | CRUD Testing                               | High       | Standard       |
| AC 02.2 | Filter appears in Activity Event → Assign to Event popup below Type filter    | Validation, Conditional   | CRUD Testing                               | High       | Standard       |
| AC 02.2 | OR logic applies in both Assign to Event surfaces                             | Conditional               | Decision Table                             | High       | Standard       |
| AC 02.3 | Filter appears in Lesson Calendar Student List Filter (left panel) below Type | Validation, Conditional   | CRUD Testing                               | High       | Standard       |
| AC 02.3 | Filter in Lesson Calendar: single value → correct students shown              | Conditional               | Decision Table, Equivalence Partitioning   | High       | Standard       |
| AC 02.3 | Filter in Lesson Calendar: multiple values → OR logic                         | Conditional               | Decision Table                             | High       | Standard       |
| AC 02.4 | Filter appears in Add Student Filter in Lesson Detail below Type filter       | Validation, Conditional   | CRUD Testing                               | High       | Standard       |
| AC 02.4 | Filter in Add Student: single value → correct students shown                  | Conditional               | Decision Table, Equivalence Partitioning   | High       | Standard       |
| AC 02.4 | Filter in Add Student: multiple values → OR logic                             | Conditional               | Decision Table                             | High       | Standard       |
| AC 03.1 | student_classification column shown in Collect Event Attendance page          | Cross-system, Validation  | CRUD Testing, Equivalence Partitioning     | Medium     | Standard       |
| AC 03.1 | Column blank when student_classification = null (Collect Event Attendance)    | Conditional               | Negative Testing                           | Medium     | Smoke          |
| AC 03.2 | student_classification column present in CSV Download Participants            | Cross-system, Validation  | CRUD Testing                               | Medium     | Standard       |
| AC 03.2 | CSV column blank when student_classification = null                           | Conditional               | Negative Testing                           | Medium     | Smoke          |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

_None_ — this feature is purely additive (display + filter). No data writes, state transitions, or financial operations introduced.

### 🟠 High Risk

| Area                                                                         | Reason                                                                                                                                                                                                        | Recommended Approach                                                                                            |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| OR logic across all 4 filter surfaces (AC 02.1–02.4)                         | A mis-implementation of AND logic would silently return zero results for any multi-select query. Since each student has exactly one classification, AND = always empty. Hard to detect without explicit test. | Decision Table: test with 2 values selected covering enrolled + inquiry; verify both student types are returned |
| Event Master → Assign to Event vs Activity Event → Assign to Event (AC 02.2) | Same popup but 2 different parent contexts. Filter may be added to one surface but missed on the other.                                                                                                       | Test filter independently from both parent pages                                                                |
| Dynamic picklist values (AC 02.1–02.4)                                       | If values are hardcoded rather than pulled from the picklist field, future picklist changes won't be reflected. Any hardcoded list that misses or misspells a value causes wrong filter options.              | Verify that all current picklist values appear in the filter dropdown; verify none extra appear                 |
| Column in Event Participant List (AC 01.1)                                   | Event Participant List is shared across multiple contexts (Event Master detail, Activity Event detail). Column must appear in all relevant list views, not just one.                                          | Test from both Event Master participant list and Activity Event participant list                                |

### 🟡 Medium Risk

| Area                                                | Reason                                                                                                                                                                            | Recommended Approach                                                                          |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Null display = blank (AC 01.1, 01.2, 03.1, 03.2)    | PBT-2485 is still In Development — most students will have null classification during initial testing. If null shows '-' or 'N/A' instead of blank, the display spec is violated. | Ensure at least one test student has null classification and verify empty cell                |
| CSV column inclusion (AC 03.2)                      | CSV export column order is fragile. If new column is inserted in an unexpected position or uses a wrong header label, downstream data consumers may break.                        | Download CSV and verify: column exists, header label matches design, blank row for null value |
| Collect Event Attendance column (AC 03.1)           | This is a dev-missed item — higher chance of being deprioritized or implemented inconsistently.                                                                                   | Explicit test case with expected behavior documented; flag as "dev missed" in Qase            |
| Filter placement "below Type filter" (AC 02.1–02.4) | Visual regression — if the filter appears above or in wrong position, the spec is violated but the function still works. Easy to overlook.                                        | Screenshot-based or manual visual check for filter order                                      |

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area                                                                   | Existing Test Case                                                                                          | Overlap                                | New Coverage Needed                                                     |
| -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | -------------------------------------- | ----------------------------------------------------------------------- |
| student_classification column in Event Participant List (AC 01.1)          | `LT-94674-cancel-booked-event-update.csv` — covers participant list columns (Response, cancellation status) | None for student_classification        | ✅ New case: column visible with value / blank when null                |
| student_classification column in Lesson Calendar Student Session (AC 01.2) | No existing coverage in `output/test-cases/lesson-management/`                                              | None                                   | ✅ New case: column visible with value / blank when null                |
| Filter in Add Master Participant popup (AC 02.1)                           | `create-event-master.csv` — covers Add Master Participant flow, not filter behavior                         | None for classification filter         | ✅ New cases: filter visible, single-value, multi-value OR, empty-state |
| Filter in Event Master → Assign to Event (AC 02.2)                         | None                                                                                                        | None                                   | ✅ New cases: filter visible, single-value, multi-value OR              |
| Filter in Activity Event → Assign to Event (AC 02.2)                       | None                                                                                                        | None                                   | ✅ New cases: filter visible, single-value, multi-value OR              |
| Filter in Lesson Calendar left panel (AC 02.3)                             | None in `output/test-cases/lesson-management/`                                                              | None                                   | ✅ New cases: filter visible, single-value, multi-value OR              |
| Filter in Add Student Filter in Lesson Detail (AC 02.4)                    | No existing coverage for student filter in lesson detail                                                    | None                                   | ✅ New cases: filter visible, single-value, multi-value OR              |
| Column in Collect Event Attendance (AC 03.1)                               | None                                                                                                        | None                                   | ✅ New case: column visible / blank when null                           |
| Column in CSV Download Participants (AC 03.2)                              | `LT-94674-cancel-booked-event-update.csv` — covers CSV download from participant list                       | None for student_classification column | ✅ New case: column in CSV, blank when null                             |
| Dynamic picklist values                                                    | None                                                                                                        | None                                   | ✅ New case: verify filter dropdown reflects picklist field definition  |
| OR logic multi-select                                                      | None                                                                                                        | None                                   | ✅ New case: select 2 values, verify both student types returned        |

---

## 7. Suggested Test Suite Structure

```
output/test-cases/lesson-management/event/
└── LT-96188-student-classification/
    ├── 01-event.md
    │   → AC 01.1 — student_classification column in Event Participant List (with value / null / Activity Event)
    │   → AC 02.1 — Filter in Add Master Participant popup (visible, placement, single-value, multi-value OR, dynamic picklist)
    │   → AC 02.2 — Filter in Event Master → Assign to Event popup (visible, placement, single-value)
    │   → AC 02.2 — Filter in Activity Event → Assign to Event popup (visible, placement, single-value, multi-value OR)
    │   → AC 03.1 — student_classification column in Collect Event Attendance (with value / null)
    │   → AC 03.2 — student_classification column in CSV Download Participants (column present / blank for null)
    │
    ├── 02-lesson-calendar.md
    │   → AC 01.2 — student_classification column in Lesson Calendar Student Session (with value / null)
    │   → AC 02.3 — Filter in Lesson Calendar Student List Filter (visible, placement, single-value, multi-value OR)
    │
    └── 03-lesson.md
        → AC 02.4 — Filter in Add Student Filter in Lesson Detail (visible, placement, single-value, multi-value OR)
```

**Total test cases:** 26

- `01-event.md`: 16 cases
- `02-lesson-calendar.md`: 6 cases
- `03-lesson.md`: 4 cases
