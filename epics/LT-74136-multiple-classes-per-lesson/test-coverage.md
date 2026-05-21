# Test Coverage: LT-74136 — Multiple Classes per Lesson

**Jira:** https://manabie.atlassian.net/browse/LT-74136
**Date:** 2026-05-18
**Module:** lesson-management
**Platforms:** SF, BO, Mobile
**Feature Flags:** `Multiple_Classes_In_Lesson__c` | `Lesson_BackOffice_LessonSF_MultipleClassesSF`

---

## 1. Business Rules Extracted

| #     | AC           | Business Rule                                                                                                 |
| ----- | ------------ | ------------------------------------------------------------------------------------------------------------- |
| BR-01 | AC 01.1      | Class selection field supports multiple classes under the same course (multi-select)                          |
| BR-02 | AC 01.1      | Recurring lesson: all selected classes applied to every lesson in chain upon generation                       |
| BR-03 | AC 01.1      | Course field remains non-editable after lesson creation                                                       |
| BR-04 | AC 01.1      | Class field remains non-editable after lesson creation (via lesson form)                                      |
| BR-05 | AC 01.2      | CSV import supports multiple classes ONLY when Teaching Method = Group                                        |
| BR-06 | AC 01.2      | Multiple classes in CSV separated by semicolon (`;`)                                                          |
| BR-07 | AC 01.2      | New import steps: LS → LSC → Lesson → Teacher → Student Sessions                                              |
| BR-08 | AC 01.2      | Class field in Lesson is a formula derived from LSC records (not a direct lookup)                             |
| BR-09 | AC 01.3      | After associating classes with LS, system auto-retrieves ALL students in those classes and allocates them     |
| BR-10 | AC 02.1      | Auto-assignment when student assigned to a class (Lesson Schedule Class trigger)                              |
| BR-11 | AC 02.1      | Trigger: Bulk Assign Class on UI (Location Course page)                                                       |
| BR-12 | AC 02.1      | Trigger: Individual Assign Class (Contact page)                                                               |
| BR-13 | AC 02.1      | Trigger: Bulk Assign Class by Academic Level (Contact page)                                                   |
| BR-14 | AC 02.1      | Trigger: Class Member Import (Salesforce Import Wizard)                                                       |
| BR-15 | AC 02.2      | System handles 50–100 students per class without degradation                                                  |
| BR-16 | AC 02.2      | Auto-assignment uses async batch processing (Master Queue)                                                    |
| BR-17 | AC 03.1      | Import LS with classes → system auto-creates LSC records                                                      |
| BR-18 | AC 03.1      | Each LSC correctly references related LS and Class from import data                                           |
| BR-19 | AC 03.2      | After LSC created via import, students auto-allocated to lessons                                              |
| BR-20 | AC 04.1      | Migration: all existing Class values from LS → new LSC object                                                 |
| BR-21 | AC 04.1      | After migration, Class field on LS no longer holds data (deprecated)                                          |
| BR-22 | AC 04.2      | Class formula on Lesson retrieves all classes from LSC; comma-separated display                               |
| BR-23 | AC 04.2      | Class formula displays comma-separated class names for multiple classes                                       |
| BR-24 | AC 04.3      | Class Schedule related list on Class record: pulls from LSC                                                   |
| BR-25 | AC 04.3      | Tab name on Class record corrected to 'Class Schedule'                                                        |
| BR-26 | AC 04.3      | Class Schedule columns: Lesson Name, Start Date, End Date, LS hyperlink                                       |
| BR-27 | AC 05.1      | SF Lesson List, Detail, LS Detail, Compact Layout display multiple classes from LSC                           |
| BR-28 | AC 05.1      | SF Mana Calendar filter supports filtering lessons by class (from LSC)                                        |
| BR-29 | AC 05.2      | BO Lesson List, Lesson Detail display multiple classes from LSC                                               |
| BR-30 | AC 05.2      | BO Advanced filter + Calendar filter support filtering by class                                               |
| BR-31 | AC 05.3      | Mobile Calendar Lesson detail displays classes from LSC                                                       |
| BR-32 | Q2-CONFIRMED | Staff CAN add/remove LSC records via related list on existing lesson (post-creation)                          |
| BR-33 | Q2-CONFIRMED | LSC edit triggers student auto-remove/assign: remove class → students removed; add class → students assigned  |
| BR-34 | Q3-CONFIRMED | CSV: Teaching Method = Individual → Class field hidden; multi-class input not possible                        |
| BR-35 | Q4-CONFIRMED | Calendar class filter uses ALL-match (AND) logic                                                              |
| BR-36 | Q5-CONFIRMED | LSC cascade-deleted when parent Lesson Schedule is deleted                                                    |
| BR-37 | Q6-CONFIRMED | Deprecated Class field on LS: DB migration only — not shown on any UI                                         |
| BR-38 | Q7-CONFIRMED | Multi-class CSV import: accessible to all SF users who can login                                              |
| BR-39 | Q8-CONFIRMED | Feature flag OFF → system reverts to single-class behavior; existing multi-class lessons show as single class |
| BR-40 | Q9-CONFIRMED | Class Schedule related list update applies to BOTH SF and BO Class detail views                               |

---

## 2. Logic Type Categorization

| AC / BR Group                    | Business Rule #                   | Logic Type(s)                                          |
| -------------------------------- | --------------------------------- | ------------------------------------------------------ |
| AC 01.1 — UI multi-select        | BR-01                             | Conditional logic, Validation logic                    |
| AC 01.1 — Recurring              | BR-02                             | Recurrence logic, Cross-system impact                  |
| AC 01.1 — Field locks (form)     | BR-03, BR-04                      | Validation logic                                       |
| AC 01.1 — LSC edit post-creation | BR-32, BR-33                      | Conditional logic, Data integrity, Cross-system impact |
| AC 01.2 — CSV rules              | BR-05, BR-06, BR-34               | Conditional logic, Validation logic                    |
| AC 01.2 — Import steps           | BR-07, BR-08                      | Data integrity                                         |
| AC 01.2 — Access                 | BR-38                             | Permission logic                                       |
| AC 01.3 — Auto-assign            | BR-09                             | Data integrity, Conditional logic                      |
| AC 02.1 — Triggers               | BR-10, BR-11, BR-12, BR-13, BR-14 | Conditional logic                                      |
| AC 02.2 — Performance            | BR-15, BR-16                      | Boundary/range logic, Data integrity                   |
| AC 03.1 / 03.2 — Import LSC      | BR-17, BR-18, BR-19               | Data integrity, Conditional logic                      |
| AC 04.1 — Migration              | BR-20, BR-21, BR-37               | Data integrity, Cross-system impact                    |
| AC 04.2 — Formula field          | BR-22, BR-23                      | Data integrity, Cross-system impact                    |
| AC 04.3 — Class Schedule RL      | BR-24, BR-25, BR-26, BR-40        | Cross-system impact                                    |
| AC 05.1 — SF display + filter    | BR-27, BR-28, BR-35               | Cross-system impact, Conditional logic                 |
| AC 05.2 — BO display + filter    | BR-29, BR-30                      | Cross-system impact, Conditional logic                 |
| AC 05.3 — Mobile                 | BR-31                             | Cross-system impact                                    |
| Q5/Q8 — Cascade + flag OFF       | BR-36, BR-39                      | State transition, Data integrity                       |

---

## 3. Test Technique Selection

| Logic Type           | Applicable Techniques                             |
| -------------------- | ------------------------------------------------- |
| Conditional logic    | Decision Table, Negative Testing                  |
| Validation logic     | Equivalence Partitioning, Negative Testing        |
| Recurrence logic     | State Transition Testing, Regression Analysis     |
| Data integrity       | CRUD Testing, Regression Analysis, Decision Table |
| Boundary/range logic | Boundary Value Analysis (50, 100, 101 students)   |
| Permission logic     | Permission Matrix                                 |
| Cross-system impact  | Regression Analysis, CRUD Testing                 |
| State transition     | State Transition Testing (flag ON → OFF → ON)     |

---

## 4. Structured Coverage Strategy

| AC              | Business Rule Summary                                                                           | Logic Type                         | Test Technique      | Risk Level | Coverage Depth |
| --------------- | ----------------------------------------------------------------------------------------------- | ---------------------------------- | ------------------- | ---------- | -------------- |
| AC 01.1         | Multi-select class field: select 2 classes on Group lesson creation                             | Conditional logic                  | Decision Table      | High       | Standard       |
| AC 01.1         | Recurring lesson: both classes appear on all lessons in chain                                   | Recurrence logic                   | State Transition    | High       | Standard       |
| AC 01.1         | Course field locked after save                                                                  | Validation logic                   | Negative Testing    | Medium     | Smoke          |
| AC 01.1         | Class field locked after save (via lesson form)                                                 | Validation logic                   | Negative Testing    | Medium     | Smoke          |
| BR-32/33        | Add class via LSC related list → students auto-assigned                                         | Conditional logic + Data integrity | CRUD Testing        | High       | Standard       |
| BR-32/33        | Remove class via LSC related list → students auto-removed                                       | Conditional logic + Data integrity | CRUD Testing        | Critical   | Deep           |
| AC 01.2         | CSV import: Group + 2 classes (semicolon) → LSC created, students assigned                      | Data integrity                     | CRUD Testing        | High       | Standard       |
| AC 01.2         | CSV import: Individual method → class field hidden, import proceeds with no class               | Conditional logic + Validation     | Negative Testing    | Medium     | Standard       |
| AC 01.2         | CSV import: new 5-step process verified (LSC step present)                                      | Data integrity                     | CRUD Testing        | High       | Standard       |
| AC 01.3         | Create lesson with 2 classes → students from both classes auto-assigned                         | Data integrity                     | CRUD Testing        | Critical   | Deep           |
| AC 01.3         | Student in both Class A + B → single session created (dedup via LT-99546)                       | Data integrity                     | Regression Analysis | Critical   | Deep           |
| AC 02.1         | Assign class to student → student auto-assigned to all lessons in LSC chain                     | Conditional logic                  | Decision Table      | High       | Standard       |
| AC 02.1         | All 4 trigger types produce correct student session creation                                    | Conditional logic                  | Decision Table      | High       | Standard       |
| AC 02.2         | 100 students in a class: all auto-assigned within acceptable time                               | Boundary/range                     | BVA                 | High       | Standard       |
| AC 03.1/03.2    | Import LS with 2 classes → LSC records auto-created + students assigned                         | Data integrity                     | CRUD Testing        | High       | Standard       |
| AC 04.1         | Post-migration: deprecated Class field not visible on SF/BO layouts                             | Cross-system                       | Regression Analysis | High       | Standard       |
| AC 04.2         | Class formula on Lesson shows comma-separated class names from LSC                              | Data integrity                     | Regression Analysis | Critical   | Deep           |
| AC 04.2         | Single-class lesson: formula shows single class name (backward compat)                          | Regression Analysis                | Regression Analysis | Critical   | Deep           |
| AC 04.3         | Class Schedule related list on SF Class record: source = LSC, correct columns                   | Cross-system                       | CRUD Testing        | Medium     | Standard       |
| AC 04.3 (BR-40) | Class Schedule related list on BO Class detail view also updated                                | Cross-system                       | CRUD Testing        | Medium     | Standard       |
| AC 05.1         | SF Lesson List / Detail / LS Detail: shows comma-separated classes                              | Cross-system                       | CRUD Testing        | Medium     | Standard       |
| AC 05.1         | SF Calendar filter: filter by [Class X] → shows all lessons containing Class X                  | Conditional logic                  | Decision Table      | High       | Standard       |
| BR-35           | SF Calendar filter ALL-match: filter [Class X, Class Y] → only lessons with BOTH                | Conditional logic                  | Decision Table      | High       | Deep           |
| AC 05.2         | BO Lesson List / Detail: shows comma-separated classes                                          | Cross-system                       | CRUD Testing        | Medium     | Standard       |
| AC 05.2         | BO Calendar filter: filter by class → ALL-match logic same as SF                                | Conditional logic                  | Decision Table      | High       | Standard       |
| AC 05.3         | Mobile Calendar Lesson detail: shows classes from LSC                                           | Cross-system                       | CRUD Testing        | Medium     | Smoke          |
| BR-36           | Delete Lesson Schedule → LSC records cascade-deleted → formula field = empty                    | Data integrity + State transition  | CRUD Testing        | High       | Standard       |
| BR-39           | Feature flag OFF: lesson creation shows single-select; multi-class lesson shows as single class | State transition                   | Decision Table      | High       | Deep           |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area                                                | Reason                                                                                                                                                                              | Recommended Approach                                                                                          |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Auto-assign + dedup (BR-09, BR-33 + LT-99546)       | A student in Class A and Class B both assigned to the same lesson → 2 auto-assign events fire → duplicate session risk. Silent data corruption if dedup fails.                      | Create test with student in 2 classes on same lesson; verify exactly 1 Student Session + LA count = 1         |
| Class formula backward compatibility (BR-22)        | Formula field migration must not break 7 existing single-class test cases. If formula returns wrong data, all class-based filtering and display across SF/BO/Mobile fails silently. | Regression test: single-class lesson formula = original class name; multi-class = comma-separated             |
| Remove class via LSC → student auto-removed (BR-33) | If auto-removal fails, students remain enrolled in a lesson they should not attend. LA count would be inflated. Lesson reports still exist for removed students.                    | Full CRUD test: add class → verify students assigned; remove class → verify students removed + LA decremented |

### 🟠 High Risk

| Area                                             | Reason                                                                                                                                                    | Recommended Approach                                                                                                                |
| ------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| Recurring + multi-class (BR-02)                  | All lessons in a recurring chain must inherit both classes. If propagation fails for any lesson in the chain, student sessions are missing for that date. | Create 3-lesson recurring chain with 2 classes; verify all 3 lessons have both classes and correct student count                    |
| Calendar filter ALL-match (BR-35)                | Wrong match logic (ANY-match instead of ALL-match) would show irrelevant lessons when filtering by multiple classes.                                      | Filter by [Class X only] → lesson with X+Y appears; filter by [X, Y] → only X+Y lessons; filter by [X, Z] → no match for X+Y lesson |
| Feature flag OFF reversion (BR-39)               | If already-created multi-class lessons do not revert to single-class display when flag is OFF, users see inconsistent data.                               | Toggle flag OFF on a multi-class lesson; verify single-class display on SF, BO, Mobile                                              |
| CSV import: semicolon multi-class (BR-05, BR-07) | Incorrect parsing of semicolons would create wrong LSC records or miss classes entirely.                                                                  | Import CSV with `Class A;Class B`; verify 2 LSC records created and both classes appear on lesson                                   |
| Post-migration data integrity (BR-20, BR-37)     | Migration must not miss any existing single-class records. Deprecated field must not interfere with formula.                                              | Verify all pre-migration lessons show correct class via formula; deprecated field not shown on any layout                           |

### 🟡 Medium Risk

| Area                                                            | Reason                                                                                                                                                                | Recommended Approach                                                                                       |
| --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| Cross-platform display consistency (BR-27, BR-29, BR-31, BR-40) | Comma-separated class display must be consistent across SF Lesson List, SF Detail, BO Lesson List, BO Detail, Mobile Calendar, Class Schedule related list (SF + BO). | Spot-check multi-class lesson display on each surface in one regression scenario                           |
| Individual method class field hidden (BR-34)                    | CSV import with Individual method + class column must silently ignore the class (field hidden). If not handled, import might fail with unexpected error.              | Import CSV with Teaching Method=Individual + class value; verify import succeeds and class is empty/hidden |
| Cascade delete LSC (BR-36)                                      | If LSC not cascade-deleted when LS is deleted, orphaned LSC records corrupt the formula field on remaining lessons.                                                   | Delete a LS that has 2 LSC records; verify both LSC records deleted and formula field on lessons = empty   |

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area                                               | Existing Test Case                                         | Overlap                                                                                  | New Coverage Needed                                                               |
| ------------------------------------------------------ | ---------------------------------------------------------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Multi-class lesson creation (2 classes, Group)         | Qase Suite 2843 (8 cases)                                  | Partial — covers student count; does not cover LSC creation flow or formula verification | ✅ New TC: verify LSC records created + formula field value                       |
| Recurring lesson with 2 classes — all lessons in chain | None                                                       | None                                                                                     | ✅ New TC: recurring 3-lesson chain with 2 classes                                |
| LSC edit post-creation — add class                     | None                                                       | None                                                                                     | ✅ New TC: add class via related list → students auto-added                       |
| LSC edit post-creation — remove class                  | None                                                       | None                                                                                     | ✅ New TC: remove class via related list → students auto-removed + LA decremented |
| Student in 2 classes on same lesson — dedup            | None (LT-99546 tested single-trigger, not multi-class)     | None                                                                                     | ✅ New TC: dedup regression for multi-class overlap                               |
| CSV import with semicolons (Group method)              | None                                                       | None                                                                                     | ✅ New TC: CSV import with `Class A;Class B`                                      |
| CSV: Individual method → class hidden                  | None                                                       | None                                                                                     | ✅ New TC: Individual CSV import with class value — confirm ignored               |
| Calendar filter ALL-match (SF + BO)                    | Qase Suite 2844 (8 cases)                                  | Partial — covers Calendar display; does not cover filter logic                           | ✅ New TC: filter by 1 class, filter by 2 classes (ALL-match)                     |
| Feature flag OFF: single-class reversion               | None                                                       | None                                                                                     | ✅ New TC: flag OFF → verify single-class display on SF/BO/Mobile                 |
| Cascade delete LSC on LS deletion                      | None                                                       | None                                                                                     | ✅ New TC: delete LS → LSC cascade-deleted → formula empty                        |
| Post-migration: deprecated field not on UI             | None                                                       | None                                                                                     | ✅ New TC: deprecated Class field absent from SF and BO layouts                   |
| Class Schedule related list on BO Class detail         | None                                                       | None                                                                                     | ✅ New TC: BO Class detail → Class Schedule tab → verify LSC source               |
| Formula backward compatibility — single class          | TC-10533, TC-11352, TC-10534, TC-11353, TC-11321, TC-11322 | Partial — do not verify formula field specifically                                       | ✅ Regression check: formula field correct on single-class lessons post-migration |
| 100-student class auto-assign performance              | None                                                       | None                                                                                     | ✅ New TC: BVA at 100 students; verify async completion                           |

---

## 7. Suggested Test Suite Structure

```
output/test-cases/lesson-management/lesson/multiple-classes/
├── 01-lesson-creation.md
│     AC 01.1 — Create lesson with 2 classes (Group); recurring chain; field lock via form; formula display
│
├── 02-lsc-edit.md
│     BR-32, BR-33 — Add/remove class via LSC related list; student auto-assign/remove; LA update
│
├── 03-csv-import.md
│     AC 01.2, AC 03.1, AC 03.2 — CSV import with semicolons (Group); Individual method class hidden; all SF users access; LSC auto-created
│
├── 04-student-auto-assign.md
│     AC 01.3, AC 02.1, AC 02.2 — Auto-assign triggers (all 4); dedup (student in 2 classes); 100-student BVA
│
├── 05-migration-display.md
│     AC 04.1, AC 04.2, AC 04.3 — Formula backward compat; deprecated field not on UI; Class Schedule RL on SF + BO; cascade delete
│
├── 06-ui-filter.md
│     AC 05.1, AC 05.2, AC 05.3 — SF/BO multi-class display; SF + BO calendar filter ALL-match; Mobile display
│
└── 07-feature-flag.md
      BR-39 — Feature flag OFF: single-class reversion on UI + existing multi-class lessons
```

**Estimated test cases per file:**

| File                      | Estimated TCs | Risk                 |
| ------------------------- | ------------- | -------------------- |
| 01-lesson-creation.md     | 6             | High/Critical        |
| 02-lsc-edit.md            | 5             | Critical/High        |
| 03-csv-import.md          | 5             | High/Medium          |
| 04-student-auto-assign.md | 6             | Critical/High        |
| 05-migration-display.md   | 6             | Critical/High/Medium |
| 06-ui-filter.md           | 7             | High/Medium          |
| 07-feature-flag.md        | 3             | High                 |
| **Total**                 | **~38**       |                      |
