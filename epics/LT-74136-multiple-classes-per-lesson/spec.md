# LT-74136: Multiple Classes per Lesson

**ID:** https://manabie.atlassian.net/browse/LT-74136
**Status:** Done
**Analysis Date:** 2026-05-18
**Partner Scope:** Core (all orgs)
**Module:** lesson-management
**Platform:** SF, BO, Mobile
**Feature Flags:** `Multiple_Classes_In_Lesson__c` (Custom Setting) | `Lesson_BackOffice_LessonSF_MultipleClassesSF` (Unleash)

---

## Summary

LT-74136 extends the Manabie lesson system from a single-class-per-lesson model to a **many-class-per-lesson** model by introducing a new **Lesson Schedule Class** junction object. A lesson (via its Lesson Schedule) can now be linked to multiple classes; students from all assigned classes are auto-assigned to the lesson. The feature ships with a data migration that moves the existing single-class value on Lesson Schedule into Lesson Schedule Class records, and updates the Class formula field on Lesson to derive its value from Lesson Schedule Class. UI updates in SF, BO, and Mobile reflect the new multi-class data source.

---

## Acceptance Criteria

### US 01 — Update Lesson Creation (CRUD & CSV Import) to Support Multiple Classes (SF)

**AC 01.1 — Lesson Creation UI Flow Updates**

1. **Multi-Class Selection:** Users can select multiple classes under the same course when creating a lesson. Class selection field supports multiple entries (changed from single-select).
2. **Recurring Lesson Handling:** When creating a recurring lesson, all selected classes are applied to every lesson in the chain upon generation.
3. **Course & Class Field Lock:** Course and Class fields remain **non-editable** after lesson creation.

**AC 01.2 — Import Lesson Schedule (CSV)**

1. **Multi-Class Import:** Teaching Method = Group: multiple classes separated by semicolon (`;`) supported.
2. **Updated Import Steps (To-Be):**
   - Step 1: Create Lesson Schedule
   - Step 2: Create **Lesson Schedule Class** (linking multiple classes)
   - Step 3: Create Lesson with multiple classes (Class field on Lesson = formula from Lesson Schedule Class)
3. **Was (As-Is):** Step 1 Create Lesson Schedule → Step 2 Create Lesson with single Class.

**AC 01.3 — Auto-Assign Students from Class Membership**
After associating classes with a Lesson Schedule, the system retrieves all students in those classes and allocates them to the lesson (creates Student Session records).

---

### US 02 — Update Lesson Assignment Logic (SF)

**AC 02.1 — Lesson Assignment Flow with Lesson Schedule Class**
When a student is assigned to a class, system auto-retrieves all lessons linked to that class via Lesson Schedule Class and assigns the student to all relevant lessons.

Triggers:

- Bulk Assign Class on UI (Location Course page)
- Individual Assign Class on UI (Contact page)
- Bulk Assign Class by Academic Level (Contact page)
- Class Member Import (Salesforce Import Wizard)

**AC 02.2 — Performance**
Handle 50–100 students per class without degradation. Batch processing / async execution (Master Queue) used for bulk assignments.

---

### US 03 — Update Lesson Import Process (SF)

**AC 03.1 — Import Structure**

- **To-Be:** Lesson Schedule → Lesson → **Lesson Schedule Class** → Lesson Teacher → Lesson Assignment
- After importing a Lesson Schedule with associated classes, system auto-creates corresponding Lesson Schedule Class records.

**AC 03.2 — Post-Import Student Assignment**
After Lesson Schedule Class created (via import), students from assigned classes auto-allocated to appropriate lessons.

---

### US 04 — Migrate Existing Class Data (SF)

**AC 04.1 — Migration to Lesson Schedule Class**

- Migrate all existing Class values from Lesson Schedule → new Lesson Schedule Class object.
- One Lesson Schedule Class record per class per Lesson Schedule.
- After migration: Class field on Lesson Schedule no longer holds data (deprecated).

**AC 04.2 — Update Class Formula Field on Lesson**

- Formula updated to retrieve all classes from Lesson Schedule Class records linked to Lesson's Lesson Schedule.
- Display format: comma-separated class names for multiple classes.

**AC 04.3 — Update Class Schedule Related List on Class Record**

- Related list source changed from Lesson Schedule → Lesson Schedule Class.
- Tab corrected to: **Class Schedule**.
- Columns: Lesson Name, Start Date, End Date, Lesson Schedule hyperlink.

---

### US 05 — Update UI Views & Filtering (SF + BO + Mobile)

**AC 05.1 — SF UI Updates**

- Lesson List view, Lesson detail, Lesson Schedule detail, Compact Layout: display multiple classes from Lesson Schedule Class.
- Mana Calendar filter: supports filtering lessons by class.
- Mana Calendar Lesson Card (Group): shows multiple classes.

**AC 05.2 — BO UI Updates**

- BO Lesson List, Lesson detail: display multiple classes.
- BO Advanced filter + Calendar filter: filter lessons by class.
- BO Calendar Lesson Card (Group): shows multiple classes.

**AC 05.3 — Mobile UI Update**

- Mobile Calendar Lesson detail: displays classes from new Lesson Schedule Class object.

---

## New Object: Lesson Schedule Class

| Field           | Type   | Required | Description                                           |
| --------------- | ------ | -------- | ----------------------------------------------------- |
| Lesson Schedule | Lookup | Yes      | Links to Lesson Schedule when class is associated     |
| Class           | Lookup | Yes      | Links to Class when class is associated with schedule |

**Deprecated Field:** `Class` on `Lesson Schedule` object — marked deprecated post-migration.

---

## Business Rules (Extracted)

| #     | AC           | Business Rule                                                                                                                                                             | Field                                       | Field Behavior                                        | Platform           |
| ----- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- | ----------------------------------------------------- | ------------------ |
| BR-01 | AC 01.1      | Class selection field supports multiple classes under the same course                                                                                                     | Class field (Lesson Creation)               | editable (multi-select) — changed from single-select  | [SF]               |
| BR-02 | AC 01.1      | Recurring lesson: all selected classes applied to every lesson in chain upon generation                                                                                   | Class field (Recurring Lesson)              | auto-propagated to all lessons                        | [SF]               |
| BR-03 | AC 01.1      | Course field remains non-editable after lesson creation                                                                                                                   | Course field                                | locked after save                                     | [SF]               |
| BR-04 | AC 01.1      | Class field remains non-editable after lesson creation                                                                                                                    | Class field                                 | locked after save                                     | [SF]               |
| BR-05 | AC 01.2      | CSV import supports multiple classes per lesson ONLY when Teaching Method = Group                                                                                         | Class column (CSV import)                   | accepts semicolon-delimited multi-value               | [SF]               |
| BR-06 | AC 01.2      | Multiple classes in CSV separated by semicolon (`;`)                                                                                                                      | Class column (CSV import)                   | semicolon-delimited                                   | [SF]               |
| BR-07 | AC 01.2      | New CSV import process: Step 1 Create Lesson Schedule → Step 2 Create Lesson Schedule Class → Step 3 Create Lesson                                                        | Import process steps                        | sequential — new LSC step inserted                    | [SF]               |
| BR-08 | AC 01.2      | Class field in Lesson is a formula derived from Lesson Schedule Class records (not a direct lookup)                                                                       | Class (formula) on Lesson                   | auto-calculated                                       | [SF]               |
| BR-09 | AC 01.3      | After associating classes with a lesson schedule, system auto-retrieves ALL students in those classes and allocates them                                                  | Student Session (auto-create)               | auto-created for all students in all assigned classes | [SF]               |
| BR-10 | AC 02.1      | When a student is assigned to a class, system auto-assigns that student to all lessons linked to the class via Lesson Schedule Class                                      | Student Session (trigger: class assignment) | auto-created via Master Queue                         | [SF]               |
| BR-11 | AC 02.1      | Auto-assignment triggered by: Bulk Assign Class on UI (Location Course page)                                                                                              | Auto-assign trigger                         | trigger                                               | [SF]               |
| BR-12 | AC 02.1      | Auto-assignment triggered by: Individual Assign Class on UI (Contact page)                                                                                                | Auto-assign trigger                         | trigger                                               | [SF]               |
| BR-13 | AC 02.1      | Auto-assignment triggered by: Bulk Assign Class by Academic Level (Contact page)                                                                                          | Auto-assign trigger                         | trigger                                               | [SF]               |
| BR-14 | AC 02.1      | Auto-assignment triggered by: Class Member Import (Salesforce Import Wizard)                                                                                              | Auto-assign trigger                         | trigger                                               | [SF]               |
| BR-15 | AC 02.2      | System must handle class sizes of 50-100 students per class without performance degradation                                                                               | Auto-assignment performance                 | batch/async execution                                 | [SF]               |
| BR-16 | AC 02.2      | Bulk student assignment uses batch processing or asynchronous execution (Master Queue)                                                                                    | Auto-assignment execution                   | async (Master Queue)                                  | [SF]               |
| BR-17 | AC 03.1      | After importing a Lesson Schedule with classes, system auto-creates Lesson Schedule Class records                                                                         | LSC (auto-create on import)                 | auto-created                                          | [SF]               |
| BR-18 | AC 03.1      | Each auto-created LSC correctly references related Lesson Schedule and Class from import data                                                                             | LSC fields                                  | auto-populated from import                            | [SF]               |
| BR-19 | AC 03.2      | After LSC created (via import), students from assigned classes auto-allocated to appropriate lessons                                                                      | Student Session (post-import)               | auto-created via Master Queue                         | [SF]               |
| BR-20 | AC 04.1      | Migration: all existing Class values from Lesson Schedule migrated to new Lesson Schedule Class object                                                                    | LSC (migration)                             | auto-populated by migration                           | [SF]               |
| BR-21 | AC 04.1      | After migration, Class field on Lesson Schedule no longer holds class data (deprecated)                                                                                   | Class field on Lesson Schedule              | deprecated                                            | [SF]               |
| BR-22 | AC 04.2      | Class formula field on Lesson: retrieves all classes from LSC records linked to Lesson's Lesson Schedule                                                                  | Class (formula) on Lesson                   | auto-calculated — comma-separated class names         | [SF]               |
| BR-23 | AC 04.2      | Class formula displays class names in comma-separated format when multiple classes exist                                                                                  | Class (formula display)                     | auto-calculated display                               | [SF]               |
| BR-24 | AC 04.3      | Class Schedule related list on Class record page: pulls data from Lesson Schedule Class                                                                                   | Class Schedule related list                 | read-only display (source = LSC)                      | [SF]               |
| BR-25 | AC 04.3      | Tab name on Class record corrected to 'Class Schedule'                                                                                                                    | Class Schedule tab label                    | display text changed                                  | [SF]               |
| BR-26 | AC 04.3      | Class Schedule related list columns: Lesson Name, Start Date, End Date, Lesson Schedule hyperlink                                                                         | Class Schedule columns                      | display fields defined                                | [SF]               |
| BR-27 | AC 05.1      | SF Lesson List, Lesson detail, Lesson Schedule detail, Compact Layout updated to display multiple classes from LSC                                                        | Class display on SF                         | read-only display (multi-class)                       | [SF]               |
| BR-28 | AC 05.1      | SF Mana Calendar filter updated to support filtering lessons by class (from LSC)                                                                                          | SF Calendar Class filter                    | filterable by class                                   | [SF]               |
| BR-29 | AC 05.2      | BO Lesson List, Lesson detail updated to display multiple classes from LSC                                                                                                | Class display on BO                         | read-only display (multi-class)                       | [BO]               |
| BR-30 | AC 05.2      | BO Advanced filter and Calendar filter updated to filter lessons by class                                                                                                 | BO filter / BO Calendar filter              | filterable by class                                   | [BO]               |
| BR-31 | AC 05.3      | Mobile Calendar Lesson detail updated to display classes from new LSC object                                                                                              | Class display on Mobile                     | read-only display (multi-class)                       | [Mobile]           |
| BR-32 | Q2-CONFIRMED | Staff CAN add/remove Lesson Schedule Class records via the related list on an existing lesson (out-of-scope UI does exist post-creation)                                  | Lesson Schedule Class related list          | editable after lesson creation                        | [SF]               |
| BR-33 | Q2-CONFIRMED | When a class is removed from a lesson's LSC, students from that class are auto-removed from the lesson; when a class is added, students from that class are auto-assigned | Student Session (LSC edit trigger)          | auto-removed/assigned via Master Queue                | [SF]               |
| BR-34 | Q3-CONFIRMED | For CSV import: when Teaching Method = Individual, the Class field is HIDDEN — multi-class input not possible                                                             | Class field (CSV, Individual method)        | hidden when Teaching Method = Individual              | [SF]               |
| BR-35 | Q4-CONFIRMED | Calendar class filter (SF + BO) uses ALL-match logic: a lesson appears only if it contains ALL selected filter classes                                                    | Calendar Class filter                       | ALL-match (AND logic)                                 | [SF] [BO]          |
| BR-36 | Q5-CONFIRMED | Lesson Schedule Class records are cascade-deleted when their parent Lesson Schedule is deleted (Master-Detail relationship)                                               | LSC (cascade delete)                        | auto-deleted with parent LS                           | [SF]               |
| BR-37 | Q6-CONFIRMED | Post-migration, deprecated Class field on Lesson Schedule is migrated at DB level only — NOT shown on any UI surface (SF or BO)                                           | Class field on Lesson Schedule (deprecated) | not visible on UI                                     | [SF] [BO]          |
| BR-38 | Q7-CONFIRMED | Multi-class CSV import is accessible to ALL SF users who can log into SF — not restricted to HQ only                                                                      | CSV import access                           | all SF users                                          | [SF]               |
| BR-39 | Q8-CONFIRMED | When feature flag is OFF, the system reverts to single-class behavior — Class field shows single-select, existing multi-class lessons display as single class             | Feature flag OFF behavior                   | single-class fallback                                 | [SF] [BO] [Mobile] |
| BR-40 | Q9-CONFIRMED | Class Schedule related list update (AC 04.3) applies to BOTH SF and BO Class detail views — not SF-only                                                                   | Class Schedule related list                 | updated on SF and BO                                  | [SF] [BO]          |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

_No direct conflicts detected. The new Lesson Schedule Class junction object is additive. The formula field update replaces the old direct lookup but preserves the same user-visible class name display._

### Missing in Requirements

| #    | Tag                  | Source                        | Description                                                                                              | Status                                                                                                      |
| ---- | -------------------- | ----------------------------- | -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| F-01 | [MISSING BEHAVIOR]   | AC 01.2                       | CSV import: behavior when Teaching Method = Individual but Class column has semicolon-separated values   | ✅ RESOLVED: Class field hidden for Individual teaching method — input not possible                         |
| F-02 | [MISSING BEHAVIOR]   | AC 01.1 + domain_context.json | Feature flag OFF state: Class field UI behavior not defined                                              | ✅ RESOLVED: Flag OFF → system reverts to single-class behavior (BR-39)                                     |
| F-03 | [UNDOCUMENTED IN AC] | AC 04.1                       | Cascade deletion of Lesson Schedule Class records when parent Lesson Schedule is deleted — not specified | ✅ RESOLVED: Master-Detail — LSC cascade-deleted with parent LS (BR-36)                                     |
| F-04 | [UNDOCUMENTED IN AC] | AC 04.1                       | Deprecated Class field on Lesson Schedule — post-migration UI disposition not specified                  | ✅ RESOLVED: DB migration only — not shown on any UI surface (BR-37)                                        |
| F-05 | [MISSING BEHAVIOR]   | AC 01.1 + out-of-scope        | Apparent contradiction: Class field locked vs. edit/remove via related list                              | ✅ RESOLVED: Staff CAN edit via LSC related list; students auto-removed/assigned accordingly (BR-32, BR-33) |
| F-10 | [MISSING BEHAVIOR]   | AC 05.1, AC 05.2              | Calendar class filter match logic for multi-class lessons: ANY-match vs. ALL-match                       | ✅ RESOLVED: ALL-match — lesson must contain ALL selected filter classes (BR-35)                            |
| F-11 | [MISSING BEHAVIOR]   | AC 04.3                       | BO Class detail page equivalent of SF Class Schedule related list update not mentioned                   | ✅ RESOLVED: Both SF and BO updated (BR-40)                                                                 |

### Lesson-Learned Risks

| #    | Incident                                 | Date       | AC                                 | Risk                                                                                                              | Guardrail                                                                                                      | Status                           |
| ---- | ---------------------------------------- | ---------- | ---------------------------------- | ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| F-09 | Aso — Duplicate Student Sessions (LL-01) | 2026-04-13 | AC 01.3, AC 02.1, AC 02.2, AC 03.2 | Student in 2+ classes both on same lesson → 2 auto-assign events for same (student, lesson) → potential duplicate | LT-99546 unique key on (student_id, lesson_id) handles this; multi-class overlap scenario confirmed as handled | ✅ RESOLVED: Handled in LT-99546 |

### Role Gaps

| #    | Tag        | AC      | Description                                                                     | Status                                                                              |
| ---- | ---------- | ------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| F-06 | [ROLE GAP] | AC 01.2 | Centre Manager (center_level_edit) role — CSV import access for multi-class CSV | ✅ RESOLVED: All SF users who can login SF can import — no role restriction (BR-38) |

### Regression Risks

| #    | Tag               | Source                                                               | Description                                                                             |
| ---- | ----------------- | -------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| F-07 | [REGRESSION RISK] | TC-10533, TC-11352, TC-10534, TC-11353, TC-11321, TC-11322, TC-11354 | 7 existing single-class test cases must pass after formula field migration              |
| F-08 | [REGRESSION RISK] | E2E-04                                                               | E2E-04 Step 4 references old data path; Lesson Schedule Class object missing from steps |

### E2E Scenario Impact

| Scenario | Title                                                                         | Impact                                                                                    | Action |
| -------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ------ |
| E2E-04   | Class-Based Student Auto-Assignment — Import, Multiple Classes & Verification | Step 4 data path changes to LSC object; multi-class dedup regression not covered in steps | UPDATE |

### Assumptions Made

_All assumptions below have been confirmed via Q&A with stakeholder (2026-05-18). No open assumptions remain._

- ✅ Teaching Method = Individual → Class field hidden in CSV import (confirmed Q3)
- ✅ LSC editable via related list post-creation; students auto-updated (confirmed Q2)
- ✅ Centre Manager and all SF users have CSV import access (confirmed Q7)
- ✅ Lesson Schedule Class is Master-Detail → cascade delete confirmed (confirmed Q5)

---

## Clarification Questions

> **Jira post status:** ✅ All questions answered directly by stakeholder (2026-05-18) — Jira comment NOT required.

| #   | Tag                 | Question                                                                                                                                         | Answer                                                                              |
| --- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- |
| Q1  | LESSON-LEARNED RISK | Student in Class A + Class B → 2 auto-assign events → duplicate session risk. Has LT-99546 unique-key dedup been tested for multi-class overlap? | ✅ Handled in LT-99546                                                              |
| Q2  | MISSING BEHAVIOR    | Can staff add/remove LSC records via related list post-creation? What happens to students?                                                       | ✅ Yes — Class updated via related list; students auto-removed/assigned accordingly |
| Q3  | MISSING BEHAVIOR    | CSV: Individual Teaching Method + semicolon-separated classes → behavior?                                                                        | ✅ Class field hidden for Individual teaching method — not possible to input        |
| Q4  | MISSING BEHAVIOR    | Calendar class filter: lesson with Class X + Class Y filtered by Class X → shown? ANY or ALL-match?                                              | ✅ ALL-match                                                                        |
| Q5  | UNDOCUMENTED        | Lesson Schedule deleted → LSC cascade-deleted or orphaned?                                                                                       | ✅ Cascade-deleted                                                                  |
| Q6  | UNDOCUMENTED        | Post-migration: deprecated Class field on LS — UI disposition?                                                                                   | ✅ DB migration only — not shown on UI                                              |
| Q7  | ROLE GAP            | Centre Manager: multi-class CSV import permitted?                                                                                                | ✅ All SF users who can login can import                                            |
| Q8  | MISSING BEHAVIOR    | Feature flag OFF: Class field UI? Already-created multi-class lessons?                                                                           | ✅ Reverts to single class                                                          |
| Q9  | MISSING BEHAVIOR    | AC 04.3 Class Schedule related list — SF only or both SF and BO?                                                                                 | ✅ Both SF and BO                                                                   |

---

## Related Specs

- `input/specs/LT-99546: Deduplicate Student and Teacher Assignments/spec.md` — deduplication logic for the same auto-assignment queue used by LT-74136; BR-04 covers 'update lesson schedule class' trigger; multi-class overlap scenario is a regression risk for this spec.

## Related Test Cases

- `output/test-cases/lesson-management/student-session/class-assignment-student-course.md` — 7 single-class assignment test cases (TC-10533, TC-11352, TC-10534, TC-11353, TC-11321, TC-11322, TC-11354); must still pass post-migration (formula field backward compatibility).
- Qase Suite 1385 — Student Session > Class Management > Multiple Classes (8 cases; linked to LT-74136).
- Qase Suite 1462 — Calendar SF > Multiple Classes (8 cases; linked to LT-74136).

## QASE Coverage Gaps

**Negative test surface (Phase 13 anti-shallow check):**

- AC 01.1 NEGATIVE: Attempt to edit Class field after lesson creation → field must remain locked
- AC 01.2 NEGATIVE: Individual Teaching Method + multi-class CSV → Class field hidden; confirm input is blocked
- AC 02.2 NEGATIVE: Auto-assign with class > 100 students → must not time out or corrupt LA count
- AC 05.3 NEGATIVE: Mobile class display when feature flag is OFF → must show single-class fallback only

**Uncovered scenarios (to add as new test cases):**

- AC 01.1 / AC 02.1 — Staff edits lesson class via LSC related list → students auto-removed/assigned (BR-32, BR-33)
- AC 08 — Feature flag OFF: class field reverts to single-select; existing multi-class lessons show single class (BR-39)
- AC 01.3 / AC 02.1 — Multi-class membership overlap dedup (student in 2+ classes on same lesson) — confirmed handled by LT-99546 but regression test recommended
- AC 05.1 / AC 05.2 — Calendar class filter ALL-match logic — explicit test case for multi-class lessons (BR-35)
- AC 04.3 — Class Schedule related list on BO Class detail page (BR-40)
- AC 04.1 — Cascade deletion of LSC when Lesson Schedule deleted (BR-36)
