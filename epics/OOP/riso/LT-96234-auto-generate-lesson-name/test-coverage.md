# Test Coverage: LT-96234 — [Riso] Auto generate Lesson Name

**Jira:** https://manabie.atlassian.net/browse/LT-96234
**Date:** 2026-06-16

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|---|---|
| BR-01 | AC 01.1 | Subject ≠ blank AND Course ≠ blank AND first save (Riso) → Lesson Name = `[Subject] - [Course]` |
| BR-02 | AC 01.2 | Subject ≠ blank AND Course = blank AND first save (Riso) → Lesson Name = `[Subject]` |
| BR-03 | AC 01.3 | Subject = blank AND Course = blank AND first save (Riso) → Lesson Name = `"-"` |
| BR-04 | AC 01.4 | Auto-generation triggers ONLY on first save; subsequent edits do NOT re-trigger generation |
| BR-05 | AC 01.5 | Lesson Name is editable by users at any time after first save |
| BR-06 | AC 02.1 | Bulk Create Lesson CSV (Riso): same generation rule applied row-by-row on import |
| BR-07 | AC 03.1 | Teaching Method = Individual AND org = Riso → Course field shown in lesson creation form |
| BR-08 | AC 03.2 | Course field is optional (not required) for Teaching Method = Individual, Riso |
| BR-09 | AC 04.1 | Feature is Riso-specific; non-Riso client Lesson Name behavior (manual entry) unchanged |
| BR-10 | AC 04.2 | No new permissions; existing create-lesson and edit-name roles unchanged |
| BR-11 | AC 01.1–01.3 | ALL lessons in a recurring chain created on one first save receive the same auto-generated name |
| BR-12 | AC 01.4 | Duplicating a Riso lesson: first save of the duplicate re-triggers auto-generation using the source lesson's Subject and Course values; pre-filled name is overwritten |
| BR-13 | AC 02.1 | Bulk CSV: auto-generation always overrides any Lesson Name value pre-populated in the CSV row |

---

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC 01.1 | BR-01 | Conditional logic |
| AC 01.2 | BR-02 | Conditional logic |
| AC 01.3 | BR-03 | Conditional logic |
| AC 01.4 | BR-04 | State transition |
| AC 01.4 | BR-12 | State transition, Conditional logic |
| AC 01.5 | BR-05 | State transition |
| AC 01.1–01.3 | BR-11 | Recurrence logic, Conditional logic |
| AC 01.1–01.3 | (cross-surface) | Cross-system impact |
| AC 01.4 | (idempotency) | Data integrity |
| AC 02.1 | BR-06 | Conditional logic, Data integrity |
| AC 02.1 | BR-13 | Data integrity |
| AC 03.1 | BR-07 | Display completeness, Conditional logic |
| AC 03.2 | BR-08 | Validation logic |
| AC 03.3 | — | Conditional logic |
| AC 04.1 | BR-09 | Permission logic (tenant-gate) |
| AC 04.2 | BR-10 | Permission logic |

---

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Conditional logic | Decision Table (primary), Negative |
| State transition | State Transition (primary), CRUD |
| Recurrence logic | State Transition (primary), Regression |
| Cross-system impact | Regression (primary), CRUD |
| Data integrity | CRUD (primary), Negative, Regression |
| Display completeness | Component (primary), Negative (field absent) |
| Validation logic | Equivalence Partitioning (primary), Negative |
| Permission logic (tenant-gate) | Regression (primary), Decision Table |

---

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC 01.1 | Both Subject AND Course → Lesson Name = `[Subject] - [Course]` | Conditional logic | Decision Table | Critical | Deep |
| AC 01.2 | Subject only (Course blank) → Lesson Name = `[Subject]` | Conditional logic | Decision Table | Critical | Deep |
| AC 01.3 | Both blank → Lesson Name = `"-"` | Conditional logic | Decision Table | Critical | Deep |
| AC 01.4 | Auto-generation fires ONLY on first save; subsequent edits do NOT re-trigger | State transition | State Transition | Critical | Deep |
| AC 01.4 (BR-12) | Duplicate lesson: first save re-triggers auto-gen from source Subject/Course | State transition, Conditional logic | State Transition | High | Standard |
| AC 01.5 | Lesson Name manually editable post-first-save | State transition | CRUD | Medium | Standard |
| AC 01.1–01.3 (BR-11) | Recurring chain: ALL lessons receive the same auto-generated name | Recurrence logic | State Transition | High | Deep |
| AC 01.1–01.3 (cross-surface) | Auto-generated name visible in BO Lesson Detail and BO Lesson Management | Cross-system impact | Regression | High | Standard |
| AC 01.4 (idempotency) | Rapid double-save / re-submit does not re-trigger auto-generation a second time | Data integrity | CRUD (negative) | High | Standard |
| AC 02.1 (BR-06) | Bulk CSV row-by-row auto-generation (Subject/Course columns) | Conditional logic, Data integrity | Decision Table | High | Deep |
| AC 02.1 (BR-13) | Bulk CSV: auto-generation overrides any pre-populated Lesson Name column value | Data integrity | Negative | High | Standard |
| AC 03.1 | Course field shown in creation form for TM = Individual (Riso) | Display completeness, Conditional logic | Component | Medium | Standard |
| AC 03.1 | Course field NOT shown for TM ≠ Individual (Riso) | Conditional logic | Negative | Medium | Standard |
| AC 03.2 | Course optional for Individual: lesson saves successfully with Course blank | Validation logic | Equivalence Partitioning | Medium | Standard |
| AC 03.3 | Course provided for Individual TM → participates in name generation | Conditional logic | Decision Table | Medium | Standard |
| AC 04.1 | Non-Riso client: Lesson Name behavior unchanged (manual entry, no auto-gen) | Permission logic (tenant-gate) | Regression | High | Standard |
| AC 04.2 | All existing create/edit-name roles work as before; no new permission gate | Permission logic | Permission Matrix | Low | Smoke |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| BR-01/02/03 — Core generation rule (3 conditions) | Incorrect name generation is directly user-visible and affects lesson record data integrity across all surfaces | Decision table with all 4 condition combinations (Subject+Course, Subject only, Course only, both blank); verify name in SF + BO |
| BR-04 — First-save gate | If auto-generation re-runs on subsequent edits, users lose manually corrected names — data integrity failure | State transition: first save → verify name; edit Subject → verify name unchanged; edit Lesson Name manually → verify no revert |
| LT-94698 regression — save without Subject now produces Lesson Name = `"-"` | Existing Riso test cases for "save without Subject" assertions now need to expect Lesson Name = `"-"`; missing update = failing regression | Explicit regression test for AC 01.3 aligned with LT-94698 "blank Subject" scenario |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| BR-11 — Recurring chain name propagation | If only the first lesson in the chain gets the name and others are blank, scheduling data is inconsistent | Create 3-lesson weekly recurring → verify ALL 3 have same auto-generated name |
| BR-06/BR-13 — Bulk CSV auto-generation + override | CSV import is a batch operation; wrong behavior multiplies across all imported rows; override of user-supplied name needs explicit confirmation | Decision table: row with Subject+Course, row with Subject only, row with both blank, row with pre-populated Lesson Name |
| BR-12 — Duplicate first-save behavior | Duplicating is a common staff workflow; if name generation re-runs unexpectedly it could overwrite a corrected name | State transition on duplicate: source with auto-name → duplicate → first save → verify name = auto-gen from source Subject/Course |
| BR-09 — Non-Riso isolation | Any config leak causing auto-generation to trigger for non-Riso orgs is a critical regression | Regression: create lesson on non-Riso org; verify Lesson Name behaves as before (manual entry required, not auto-populated) |
| AC 01.1–01.3 cross-surface | Auto-generated name must be consistent across SF and BO surfaces | After auto-gen on SF, open BO Lesson Detail and BO Lesson Management; verify name is identical |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| BR-07/BR-08 — Course field for Individual TM | New UI field addition; conditional visibility could affect form layout | Verify Course field shown/hidden per TM, and that saving with Course blank does not break lesson creation |
| BR-05 — Manual edit after auto-gen | Users must be able to correct auto-generated names | Edit Lesson Name post-creation; verify updated value persists across subsequent saves |
| Idempotency under rapid re-save | Double-submit on first save should not regenerate name twice | Simulate rapid two saves on create; verify exactly-once generation |

---

## Section G — Downstream Effects Inventory

_Mandatory for every CREATE/UPDATE/DELETE rule._

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner |
|---|---|---|---|
| Create Riso lesson (first save, Subject+Course) | Lesson Name auto-set to `[Subject] - [Course]` | SF Lesson record (Lesson Name field) | TC: auto-gen-both-provided |
| Create Riso lesson (first save, Subject only) | Lesson Name auto-set to `[Subject]` | SF Lesson record | TC: auto-gen-subject-only |
| Create Riso lesson (first save, both blank) | Lesson Name auto-set to `"-"` | SF Lesson record | TC: auto-gen-both-blank |
| Create Riso lesson (first save, Subject+Course) | Lesson Name visible in BO Lesson Detail | BO Lesson Detail page | TC: cross-surface-bo-detail |
| Create Riso lesson (first save, Subject+Course) | Lesson Name visible in BO Lesson Management list | BO Lesson Management | TC: cross-surface-bo-list |
| Edit Riso lesson (subsequent save after first save) | Lesson Name NOT re-generated; value preserved | SF Lesson record | TC: no-regen-on-edit |
| Manually edit Lesson Name post-creation | Lesson Name updated to user-entered value; preserved on next save | SF + BO Lesson Detail | TC: manual-edit-post-gen |
| Create recurring Riso lesson (first save) | ALL lessons in chain get same auto-generated name | SF Lesson records (all chain members) | TC: recurring-chain-all-get-name |
| Duplicate Riso lesson → first save of duplicate | Duplicate's Lesson Name = auto-gen from source Subject/Course (not pre-filled value) | SF Lesson record (new) | TC: duplicate-regen |
| Bulk CSV import (Riso) | Each row's lesson gets auto-generated Lesson Name | SF Lesson records (all imported) | TC: csv-auto-gen |
| Bulk CSV import (Riso, row with pre-populated Lesson Name) | Lesson Name = auto-generated value (overrides CSV value) | SF Lesson record | TC: csv-override |
| Create lesson (non-Riso org) | Lesson Name behavior unchanged; auto-generation does NOT fire | SF Lesson record (non-Riso) | TC: non-riso-isolation |

---

## Section H — Display & Ordering Inventory

_Mandatory for every UI screen/card/list._

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| Lesson creation form (SF, Riso, TM = Individual) | Lesson Name (auto-gen on save), Subject (optional), Course (optional, new) | Course: shown only when TM = Individual AND org = Riso | N/A | N/A |
| Lesson creation form (SF, Riso, TM ≠ Individual) | Lesson Name, Subject | Course: hidden | N/A | N/A |

**H.1 — Spec–Figma Mismatch:** N/A — No Figma URL in spec.

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Auto-generate Lesson Name: Subject+Course → `[Subject] - [Course]` | None | None | ✅ New TC for AC 01.1 (BR-01) |
| Auto-generate Lesson Name: Subject only → `[Subject]` | None | None | ✅ New TC for AC 01.2 (BR-02) |
| Auto-generate Lesson Name: both blank → `"-"` | `LT-94698` "save without Subject" (partial — tests Subject blank as valid, does NOT assert Lesson Name = `"-"`) | Partial — needs Lesson Name assertion added | ✅ New TC for AC 01.3 (BR-03); update LT-94698 test expectations |
| Auto-generation fires only on first save (no re-trigger on edit) | None | None | ✅ New TC for AC 01.4 (BR-04) |
| Manual edit of Lesson Name post-first-save | `LT-90573` Extend Recurring — Lesson Name editable (partial overlap) | Partial — recurring context only | ✅ New TC for AC 01.5 (BR-05) |
| Recurring chain: ALL lessons get auto-generated name | `LT-94698` BR-22 "Create recurring lesson with subject — all lessons get subject" (partial) | Partial — Subject field propagation tested; Lesson Name auto-gen not tested | ✅ New TC for AC 01.1–01.3 + BR-11 |
| Duplicate lesson → auto-gen from source Subject/Course on first save | `LT-94698` BR-30 "Duplicate lesson with subject — Subject pre-filled in create form" | Partial — Subject pre-fill tested; auto-gen name on save not tested | ✅ New TC for BR-12 |
| Bulk CSV auto-generation (Riso) | None | None | ✅ New TCs for AC 02.1 (BR-06, BR-13) |
| Course field shown for TM = Individual (Riso) | None | None | ✅ New TC for AC 03.1 (BR-07) |
| Course optional for Individual TM (Riso) | None | None | ✅ New TC for AC 03.2 (BR-08) |
| Non-Riso isolation | None | None | ✅ New TC for AC 04.1 (BR-09) |
| Auto-generated name visible in BO | None | None | ✅ New TC for cross-surface |
| No new permission gate | None | None | ✅ New smoke TC for AC 04.2 (BR-10) |

---

## 7. Suggested Test Suite Structure

```
epics/OOP/riso/LT-96234-auto-generate-lesson-name/test-cases/
├── auto-generate-lesson-name.md
│     → AC 01.1, 01.2, 01.3 — Core generation rules (3 conditions; Decision Table)
│     → AC 01.4 — First-save gate (no re-trigger on edit; duplicate behavior)
│     → AC 01.5 — Manual edit post-auto-generation
│     → BR-11   — Recurring chain: all lessons get auto-generated name
│     → Cross-surface: auto-generated name visible in BO
│
├── bulk-csv-auto-generate.md
│     → AC 02.1 — CSV row-by-row auto-generation (BR-06)
│     → AC 02.1 — CSV override of pre-populated Lesson Name (BR-13)
│
├── course-field-individual.md
│     → AC 03.1 — Course field visible/hidden per Teaching Method (Riso)
│     → AC 03.2 — Course optional; lesson saves with Course blank
│     → AC 03.3 — Course provided for Individual → participates in name generation
│
└── scope-isolation.md
      → AC 04.1 — Non-Riso client: Lesson Name behavior unchanged
      → AC 04.2 — No new permissions (smoke)
```
