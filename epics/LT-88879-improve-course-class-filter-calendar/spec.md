# LT-88879: Improve Course and Class Filter on Calendar SF and BO

**ID:** https://manabie.atlassian.net/browse/LT-88879
**Status:** Done
**Analysis Date:** 2026-05-18
**Module:** lesson-management
**Platform:** SF, BO
**Labels:** NonFunctional

---

## Summary

LT-88879 improves the UX of the course and class filter on the Salesforce (SF) and Back Office (BO) Lesson Calendar. Previously, selecting a course in the Calendar filter would automatically add **and check** all classes belonging to that course — forcing class filter to be active whenever a course was selected. The new behavior auto-populates the class list when a course is selected but leaves all classes **unchecked** (inactive), giving users full control over whether to apply a class filter. Additionally, users can now uncheck individual classes while keeping the course filter active — previously, class and course selections were coupled.

---

## Acceptance Criteria

_Note: This ticket has no formal US/AC format. The following ACs are inferred from the 2-bullet description, Confluence documentation, and domain knowledge._

### AC 01.1 — Class Auto-Population (Unchecked) on Course Selection

When a user selects a course in the Calendar filter:
- All classes belonging to that course are **automatically added to the class filter list** in an **UNCHECKED** (inactive) state.
- These auto-populated classes do **not** apply as active filter criteria until the user explicitly checks them.
- Platform: **SF Calendar** and **BO Calendar**.

### AC 02.1 — Independent Class Uncheck While Course Remains

When a course is selected in the Calendar filter and some classes are checked (active):
- User can **uncheck any individual class** to remove it from the active filter criteria.
- Unchecking a class does **not** deselect or clear the course filter — the course remains selected.
- The course filter and the class filter are now independently controllable.
- Platform: **SF Calendar** and **BO Calendar**.

---

## Business Rules (Extracted)

| #   | AC           | Business Rule                                                                                                                                           | Field                         | Field Behavior                        | Platform    |
| --- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- | ------------------------------------- | ----------- |
| 1   | AC 01.1      | When course is selected in Calendar filter (SF), classes under that course are auto-populated in the class list in UNCHECKED state                      | Class filter list             | auto-populated, unchecked by default  | [SF]        |
| 2   | AC 01.1      | When course is selected in Calendar filter (BO), classes under that course are auto-populated in the class list in UNCHECKED state                      | Class filter list             | auto-populated, unchecked by default  | [BO]        |
| 3   | AC 01.1      | Auto-populated classes are NOT active filter criteria — no class filter is applied until user explicitly checks a class                                  | Class filter checkbox         | inactive (unchecked = no filter)      | [SF] [BO]   |
| 4   | AC 02.1      | User can independently check any auto-populated class to add it as an active class filter criterion alongside the selected course                        | Class filter checkbox         | editable (checkable)                  | [SF] [BO]   |
| 5   | AC 02.1      | User can uncheck any checked class to remove it from the active filter while keeping the course selected                                                 | Class filter checkbox         | editable (uncheckable independently)  | [SF] [BO]   |
| 6   | AC 02.1      | Unchecking a class does NOT deselect the course filter                                                                                                  | Course filter selection       | persistent (unaffected by class state)| [SF] [BO]   |
| 7   | PRIOR: BR-35 | Calendar class filter continues to use ALL-match (AND) logic when multiple classes are checked simultaneously                                            | Class filter (multi-check)    | ALL-match (AND logic)                 | [SF] [BO]   |
| 8   | PRIOR: BR-09 | Course filter logic unchanged: Individual lessons → filtered by Student Session course; Group lessons → filtered by lesson's course field                | Course filter behavior        | unchanged from existing               | [SF] [BO]   |
| 9   | INFERRED     | Old behavior (REPLACED): selecting a course previously auto-added AND auto-checked all classes — classes were immediately active as filter criteria      | Class filter (OLD behavior)   | replaced by new unchecked behavior    | [SF] [BO]   |
| 10  | CONFIRMED    | Class filter list is HIDDEN before any course is selected — users cannot see or access the class filter section until a course is chosen first          | Class filter section          | hidden until course selected          | [SF] [BO]   |
| 11  | CONFIRMED    | Class auto-population applies ONLY to Group lessons; Individual lessons do NOT support class filter — class filter section remains hidden for Individual | Class filter section          | hidden for Individual lessons         | [SF] [BO]   |
| 12  | CONFIRMED    | When a course is deselected/cleared, all auto-populated classes are also automatically cleared/deselected from the class list                            | Class list on course clear    | auto-clear on course deselect         | [SF] [BO]   |
| 13  | CONFIRMED    | Auto-populated class list contains ALL classes system-wide linked to that course — NOT scoped to current calendar date range or location                 | Class filter list scope       | all classes globally under course     | [SF] [BO]   |
| 14  | CONFIRMED    | For teachers (CPU/bo_teacher login): auto-populated class list shows ALL classes under the selected course, not scoped to teacher's assigned lessons     | Class filter list (teacher)   | all classes under course, not scoped  | [BO]        |
| 15  | CONFIRMED ⚠️ | BREAKING CHANGE: Class filter now REQUIRES course selection first — users cannot filter by class without first selecting a course. This replaces the old behavior where class could be filtered independently without course selection. All 8 existing class filter TCs (LT-74136) must be updated. | Class filter dependency | class requires course (new) | [SF] [BO]   |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag              | Source                                              | AC       | Description |
|---|------------------|-----------------------------------------------------|----------|-------------|
| 1 | [REPLACED]       | LT-74136 BR-28 / LT-88879 AC 01.1                  | AC 01.1  | Old behavior (auto-checked classes on course selection) is fully superseded by new behavior (auto-populated unchecked). Existing test cases that assumed auto-checked behavior must be reviewed. |

### Missing in Requirements

| # | Tag                  | Source                                              | Description |
|---|----------------------|-----------------------------------------------------|-------------|
| 1 | ✅ RESOLVED [UNDOCUMENTED IN AC] | Confluence 2539618322 | **Q1 CONFIRMED:** Class auto-population applies to **Group lessons ONLY**. Individual lessons do not support class filter — class filter section is hidden for Individual lessons. Added as BR-11. |
| 2 | ✅ RESOLVED [MISSING BEHAVIOR]   | Ticket description    | **Q2 CONFIRMED:** When a course is deselected, auto-populated classes also auto-clear from the class list. Added as BR-12. |
| 3 | ✅ RESOLVED [MISSING BEHAVIOR]   | Ticket description    | **Q3 CONFIRMED:** Auto-populated class list = ALL classes system-wide linked to that course (not scoped to date range/location). Added as BR-13. |
| 4 | ✅ RESOLVED [MISSING BEHAVIOR]   | Ticket description    | **Q4 CONFIRMED:** Class filter section is HIDDEN before any course is selected. Added as BR-10. |
| 5 | [MISSING BEHAVIOR]   | Ticket description    | **UNRESOLVED:** Edge case — course with 0 associated classes selected; expected UI not confirmed. Test case should handle empty class list state. |
| 6 | ✅ RESOLVED [ROLE GAP]           | scheduling-feature-permission-matrix.csv | **Q5 CONFIRMED:** Teacher (CPU login) sees ALL classes under the selected course — not scoped to teacher's assigned lessons. Added as BR-14. |
| 7 | ✅ RESOLVED [REGRESSION RISK] ⚠️ | output/test-cases/…/06-ui-filter.md | **Q6 CONFIRMED — BREAKING CHANGE:** Class filter NOW REQUIRES course selection first. Direct class selection without course is no longer supported. All 8 existing class filter TCs from LT-74136 must be reviewed and updated. Added as BR-15. |

### Lesson-Learned Risks

_No directly applicable lesson-learned incidents found. The two incidents on file (Aso duplicate sessions; Nichibei LA sync) are unrelated to Calendar filter UX behavior._

### E2E Scenario Impact

| Scenario | Title                                          | Impact | Action |
|----------|------------------------------------------------|--------|--------|
| NEW      | Calendar Filter: Course + Class interaction    | NEW    | CREATE — no existing E2E scenario covers course → class auto-population → filter interaction on SF or BO |

### Assumptions Made

- LT-88879 is a pure UX change — no changes to the underlying ALL-match filter logic (BR-35 unchanged)
- Mobile Calendar is out of scope (ticket title explicitly says "SF and BO")
- Feature flag `Multiple_Classes_In_Lesson__c` must be ON for class auto-population to work (same flag governing multi-class lessons)
- Old behavior (auto-checked) is fully replaced; no configuration to revert to auto-checked

---

## Clarification Questions

_Status: **NOT POSTED** — user confirmed answers directly; no Jira comment needed._

**All questions resolved with confirmed answers (2026-05-19):**

1. **[RESOLVED]** Does class auto-population apply to Group AND Individual lessons, or only Group?
   ✅ **Answer: Group lessons ONLY.** Individual lessons do not support class filter. → BR-11

2. **[RESOLVED]** When a course is deselected, does the auto-populated class list also clear?
   ✅ **Answer: Yes — class list auto-clears when course is deselected.** → BR-12

3. **[RESOLVED]** Scope of auto-populated classes — system-wide or scoped to current calendar date/location range?
   ✅ **Answer: ALL classes system-wide under that course** (not scoped). → BR-13

4. **[RESOLVED]** Initial state of class filter before any course is selected?
   ✅ **Answer: Class filter section is HIDDEN** until a course is selected. → BR-10

5. **[RESOLVED]** For teachers (CPU login): all classes under course, or only teacher's assigned classes?
   ✅ **Answer: ALL classes under the course** (not scoped to teacher's assigned lessons). → BR-14

6. **[RESOLVED — BREAKING CHANGE ⚠️]** Can users filter by class WITHOUT selecting a course first?
   ✅ **Answer: NO — class filter REQUIRES course selection first.** Direct class selection without course is no longer supported. All 8 existing LT-74136 class filter test cases must be reviewed and updated. → BR-15

---

## Related Specs

- `input/specs/LT-74136 Multiple Classes per Lesson/spec.md` — defines calendar class filter behavior (BR-28, BR-30, BR-35); ALL-match logic; course filter by lesson type. LT-88879 changes HOW classes appear in the filter but retains all underlying logic from this spec.

## Related Test Cases

- `output/test-cases/lesson-management/lesson/multiple-classes/06-ui-filter.md` — 8 existing calendar class filter test cases (single class, ALL-match, BO filter). These tests may need updates if class filter now requires course selection first (Q6).

## QASE Coverage Gaps

**New test cases required (none exist):**
- AC 01.1 [SF] — Course selected → class section appears with all classes unchecked (Group lessons only)
- AC 01.1 [BO] — Course selected → class section appears with all classes unchecked (Group lessons only)
- AC 01.1 [SF] — Course with 0 associated classes → class section appears empty (or "no classes" message)
- AC 01.1 + BR-11 — Individual lesson type selected → class filter section remains hidden
- AC 01.1 + BR-12 — Course deselected → class list auto-clears
- AC 01.1 + BR-13 — Auto-populated class list shows ALL classes system-wide for that course (not date/location-scoped)
- AC 01.1 + BR-14 [BO Teacher] — Teacher (CPU login) selects course → class list shows all classes under course
- AC 02.1 [SF] — Uncheck individual class → course filter remains active, calendar re-filters
- AC 02.1 [BO] — Uncheck individual class → course filter remains active
- AC 01.1 + AC 02.1 [SF] — Full user journey: select course → class section appears → check one class → calendar filtered → uncheck class → calendar reverts to course-only filter
- BR-15 [REGRESSION] — Class filter requires course selection first: attempting to access class filter without course selection → class section hidden (verify all 8 LT-74136 existing TCs still valid after this change)
