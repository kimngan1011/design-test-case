---
ticket_id: LT-96234
ticket_url: https://manabie.atlassian.net/browse/LT-96234
title: "[Riso] Auto generate Lesson Name"
module: scheduling
bucket: OOP/riso
status: Ready for QA
internal_uat_date: 2026-06-22
production_release_date: null
last_updated: 2026-06-16
---

# LT-96234: [Riso] Auto generate Lesson Name

## Summary

For Riso only, auto-generate the Lesson Name field on the **first save** of a lesson, so staff do not need to manually enter it. The generation rule uses the Subject and Course fields of the lesson: `[Subject] - [Course]` when both are provided, `[Subject]` when only Subject is provided, and `"-"` when both are blank. After the first save, Lesson Name remains fully editable and auto-generation does not re-run on subsequent edits. Additionally, the Course field is newly added (shown and optional) to the lesson form for Teaching Method = Individual.

---

## Acceptance Criteria

### US-01 — Auto-generate Lesson Name on first save

**AC 01.1** — For Riso, when a lesson is first saved with both Subject AND Course provided:
- Lesson Name is auto-generated as `[Subject] - [Course]`
- Applies to: normal lesson creation (UI form)

**AC 01.2** — For Riso, when a lesson is first saved with Subject provided but Course is blank:
- Lesson Name is auto-generated as `[Subject]`

**AC 01.3** — For Riso, when a lesson is first saved with both Subject AND Course blank:
- Lesson Name is auto-generated as `"-"` (a dash character)

**AC 01.4** — Auto-generation triggers **only once** — on the first save. Lesson Name is NOT re-generated on subsequent edits regardless of changes to Subject or Course.

**AC 01.5** — Lesson Name is editable after creation. Users can manually change it at any time after the first save.

### US-02 — Bulk Create Lesson CSV support

**AC 02.1** — For Riso, when importing lessons via Bulk Create Lesson CSV, Lesson Name is auto-generated using the same rule (based on Subject/Course column values in each CSV row). Import counts as the "first save".

### US-03 — Course field for Teaching Method = Individual

**AC 03.1** — For Riso, when Teaching Method = Individual is selected in the lesson creation/edit form, the **Course field is shown on the UI** (currently this field is hidden for Individual method).

**AC 03.2** — For Riso, Teaching Method = Individual: Course field is **optional** (not required to save the lesson).

**AC 03.3** — If Course is provided for an Individual lesson, it participates in the Lesson Name generation rule on first save.

### US-04 — Scope and permissions

**AC 04.1** — Auto-generate Lesson Name applies to **Riso only**. Non-Riso clients are unaffected — their Lesson Name behavior (manual entry) is unchanged.

**AC 04.2** — No new permissions introduced. Existing lesson-creation and lesson-name-edit permissions are unchanged.

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---|----|----|---|---|---|
| BR-01 | AC 01.1 | Subject ≠ blank AND Course ≠ blank AND first save (Riso) → Lesson Name = `[Subject] - [Course]` | Lesson Name | auto-calculated (first save only) | [SF] |
| BR-02 | AC 01.2 | Subject ≠ blank AND Course = blank AND first save (Riso) → Lesson Name = `[Subject]` | Lesson Name | auto-calculated (first save only) | [SF] |
| BR-03 | AC 01.3 | Subject = blank AND Course = blank AND first save (Riso) → Lesson Name = `"-"` | Lesson Name | auto-calculated (first save only) | [SF] |
| BR-04 | AC 01.4 | Auto-generation triggers only on first save; NOT on subsequent edits | Lesson Name | auto-calculated (first save only) | [SF] |
| BR-05 | AC 01.5 | Lesson Name is editable post-creation; manual overrides allowed at any time | Lesson Name | editable (post first save) | [SF] |
| BR-06 | AC 02.1 | Bulk Create Lesson CSV (Riso): same generation rule applied row-by-row on import | Lesson Name | auto-calculated (import = first save) | [SF] |
| BR-07 | AC 03.1 | Teaching Method = Individual AND org = Riso → Course field shown in lesson form | Course | optional (shown for Individual, Riso) | [SF] |
| BR-08 | AC 03.2 | Teaching Method = Individual AND org = Riso → Course is optional (not required) | Course | optional | [SF] |
| BR-09 | AC 04.1 | org ≠ Riso → Lesson Name behavior unchanged (manual entry, no auto-generation) | Lesson Name | manual (non-Riso unchanged) | [SF] |
| BR-10 | AC 04.2 | No new permissions; HQ Admin / Centre Manager / Centre Staff can create/edit as before | — | — | [SF] |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---|---|---|----|----|
| 1 | [CONFLICT] | `epics/OOP/riso/LT-94698-subject-in-lesson-detail/test-coverage.md` | AC 01.3 | LT-94698 tests saving a lesson without Subject as a valid scenario. After this feature, Riso lessons saved without Subject AND Course now get Lesson Name = `"-"`. Existing LT-94698 test assertions for the "save without Subject" scenario (which previously had no impact on Lesson Name) may need updating to also verify Lesson Name = `"-"`. |

### Missing in Requirements

| # | Tag | Source | Description |
|---|---|---|---|
| 1 | [MISSING BEHAVIOR] | LT-96234 description + PBT-2320 Out of Scope (RED) | Scope discrepancy: LT-96234 lists Bulk CSV as in-scope; PBT-2320 PRD marks it as "v2 if big effort". Needs confirmation before UAT. |
| 2 | [MISSING BEHAVIOR] | LT-96234 description (AC 02.1) | For Bulk CSV: if a row already contains a Lesson Name value, does auto-generation override it or skip it? Not specified. |
| 3 | [MISSING BEHAVIOR] | `knowledge/domain-knowledge/scheduling/lesson-management/lesson.md` | For recurring lesson creation (all lessons created on one first save): do ALL lessons in the chain get the auto-generated name, or only the first lesson? |
| 4 | [MISSING BEHAVIOR] | `epics/OOP/riso/LT-94698-subject-in-lesson-detail/test-coverage.md` | When duplicating a Riso lesson (which has an auto-generated name), does the duplicate's first save re-trigger generation (potentially overwriting pre-filled name) or preserve the pre-filled value? |
| 5 | [MISSING BEHAVIOR] | `knowledge/domain-knowledge/scheduling/lesson-management/class-assignment.md` | Course field is locked post-creation (existing rule). For Individual Riso lessons saved without Course → name = `"-"` or `[Subject]` → users must manually edit Lesson Name (cannot retroactively set Course to fix name). Is this the intended UX? |
| 6 | [UNDOCUMENTED IN AC] | LT-96234 description ("satisfying the system/Salesforce name requirement") | Maximum character length for auto-generated Lesson Name not specified. Very long Subject + Course combination could potentially exceed SF field limits. No error handling documented. |
| 7 | [ROLE GAP] | LT-96234 + `scheduling-feature-permission-matrix.csv` | No Riso-specific role mapping documented. "No new permission" confirmed, but baseline of which Riso roles trigger auto-generation is not explicitly stated. Assumed: HQ Admin, Centre Manager, Centre Staff. |

### Lesson-Learned Risks

| # | Incident | Date | AC | Risk | Guardrail |
|---|---|---|---|---|---|
| — | No relevant incidents found | — | — | Core.md: Aso duplicate sessions (unrelated). OOP.md: Nichibei SPO sync (unrelated). | No lesson-learned guardrails apply. |

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-01 | Lesson Lifecycle — Create, Teach, Report, View | Step 1 creates lesson with manually entered name. For Riso, name is now auto-generated. E2E needs a Riso variant (or note) for Step 1. | UPDATE |
| E2E-02 | Recurring Lesson — Create, Edit Chain | Step 1 creates recurring lesson (implies name entry). Step 4 edits name via "This and following". For Riso: Step 1 should verify auto-generation; Step 4 verifies post-auto edit works. | UPDATE |

### Assumptions Made

- No Figma designs linked in LT-96234 or Confluence PRD page 2424111121 (only table-based PRD content found).
- Subject field (prerequisite) is delivered via LT-94698 / PBT-1924 which is marked "In Development" — assuming delivered before this feature's UAT.
- The Confluence PRD (page 2424111121) confirmed the same generation rules and scope as described in LT-96234. Content aligns; no discrepancies other than the CSV scope note.
- LT-96234 status is "Ready for QA" — implementation is complete; UAT planned for 2026-06-22.
- "First save" is interpreted as the lesson record creation event (not a separate confirmation step).
- For Teaching Method = Individual: Course is currently hidden (inferred from `class-assignment.md` documenting that Class is hidden for Individual, and the ticket's phrasing "show the Course field").

---

## Clarification Questions

> ✅ Answered directly on 2026-06-16 — not posted to Jira.

| # | Question | Answer |
|---|---|---|
| Q-01 | Is Bulk Create Lesson CSV in scope or v2? | **In scope** for this delivery. |
| Q-02 | For Bulk CSV: if a row already has a Lesson Name, does auto-generation override it? | **Yes — auto-generation always applies** by the same Subject/Course rule; any pre-existing Lesson Name value is overridden. |
| Q-03 | For recurring creation: do ALL lessons in the chain get the auto-generated name? | **Yes — all lessons** in the chain receive the same auto-generated name. |
| Q-04 | When duplicating a Riso lesson, does first save re-trigger auto-generation? | **Yes — auto-generates using Subject and Course of the source (duplicated) lesson.** Pre-filled name is overwritten by auto-generation on first save. |
| Q-05 | Is there a max character length constraint on auto-generated Lesson Name? | **No limit.** |
| Q-06 | Do LT-94698 test cases need updating to expect Lesson Name = `"-"` when Subject is blank? | **Yes — update** LT-94698 test cases to assert Lesson Name = `"-"` for save-without-subject scenarios. |
| Q-07 | For Individual lesson with Course=blank: intended UX is Lesson Name = `[Subject]`? | **Yes — Lesson Name = `[Subject]`** (BR-02 applies; Course remains locked; this is the intended UX). |

### Additional Business Rules (confirmed via Q&A)

| # | AC | Business Rule (Clarified) | Field | Field Behavior | Platform |
|---|---|---|---|---|---|
| BR-11 | AC 01.1–01.3 | ALL lessons in a recurring chain created on one first save receive the same auto-generated name | Lesson Name | auto-calculated (first save, all chain members) | [SF] |
| BR-12 | AC 01.4 | When duplicating a Riso lesson, the duplicate's first save re-triggers auto-generation using the source lesson's Subject and Course values — pre-filled name is overwritten | Lesson Name | auto-calculated (first save of duplicate) | [SF] |
| BR-13 | AC 02.1 | Bulk CSV: auto-generation always applies per row regardless of whether a Lesson Name value is pre-populated in the CSV — auto-generated value overrides any supplied value | Lesson Name | auto-calculated (import = first save, always overrides) | [SF] |

---

## Related Specs

- `epics/OOP/riso/LT-94698-subject-in-lesson-detail/test-coverage.md` — Subject field (prerequisite for name generation); Subject-related test cases may need updates post this feature
- `epics/OOP/riso/LT-92532-riso-create-update-la-on-ui/spec.md` — Riso LA creation flow; background for Riso lesson creation context
- `epics/OOP/riso/LT-96673-monthly-lesson-count-add-teacher-popup/spec.md` — Another Riso OOP feature for context

## Related Test Cases

- `epics/OOP/riso/LT-94698-subject-in-lesson-detail/test-cases/` — Subject in Lesson Detail test cases; "save without subject" assertions may now produce Lesson Name = `"-"` and need verification
- `epics/lesson/LT-90573-extend-recurring-lesson/test-cases/` — Extend Recurring includes Lesson Name pre-fill tests; Riso-specific behavior for extended lessons needs clarification

## QASE Coverage Gaps

- AC 01.1 — No existing Qase test case for Riso auto-generated `[Subject] - [Course]` on lesson create
- AC 01.2 — No existing test case for Riso auto-generated `[Subject]` when Course=blank
- AC 01.3 — No existing test case for Riso auto-generated `"-"` when both blank
- AC 01.4 — No existing test case verifying auto-generation does NOT re-run on edit
- AC 01.5 — No existing test case verifying Lesson Name is manually editable post-generation
- AC 02.1 — No existing test case for Bulk CSV auto-generation (if in scope)
- AC 03.1 — No existing test case for Course field shown for Individual teaching method (Riso)
- AC 03.2 — No existing test case for Course optional for Individual (Riso)
- AC 04.1 — No existing test case verifying non-Riso clients are unaffected
