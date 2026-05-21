# Test Coverage: LT-88879 — Improve Course and Class Filter on Calendar

**Jira:** https://manabie.atlassian.net/browse/LT-88879
**Date:** 2026-05-19
**Module:** lesson-management / lesson / calendar-filter
**Platform:** SF Calendar, BO Calendar

---

## 1. Business Rules Extracted

| #   | AC              | Business Rule                                                                                                                                                                           |
| --- | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | AC 01.1         | When course is selected in SF Calendar filter, classes under that course are auto-populated in the class list in UNCHECKED (inactive) state                                             |
| 2   | AC 01.1         | When course is selected in BO Calendar filter, classes under that course are auto-populated in the class list in UNCHECKED (inactive) state                                             |
| 3   | AC 01.1         | Auto-populated classes are NOT active filter criteria — no class filter is applied to the calendar until the user explicitly checks a class                                              |
| 4   | AC 02.1         | User can independently check any auto-populated class to add it as an active class filter criterion alongside the selected course                                                       |
| 5   | AC 02.1         | User can uncheck any checked class to remove it from the active filter while keeping the course selected                                                                                |
| 6   | AC 02.1         | Unchecking a class does NOT deselect the course filter — course remains selected independently                                                                                          |
| 7   | PRIOR: BR-35    | Calendar class filter continues to use ALL-match (AND) logic when multiple classes are checked simultaneously                                                                           |
| 8   | PRIOR: BR-09    | Course filter logic unchanged: Individual lessons → filtered by Student Session course; Group lessons → filtered by lesson's course field                                               |
| 9   | REPLACED        | Old behavior: selecting a course previously auto-added AND auto-checked all classes. This is fully replaced by new unchecked behavior.                                                  |
| 10  | CONFIRMED Q4    | Class filter section is HIDDEN before any course is selected — users cannot see or access the class filter section until a course is chosen first                                       |
| 11  | CONFIRMED Q1    | Class auto-population applies ONLY to Group lessons. Individual lessons do NOT support class filter — class filter section remains hidden regardless of course selection for Individual  |
| 12  | CONFIRMED Q2    | When a course is deselected/cleared, all auto-populated classes are also automatically cleared/deselected from the class list                                                           |
| 13  | CONFIRMED Q3    | Auto-populated class list contains ALL classes system-wide linked to that course — NOT scoped to the current calendar date range or location                                             |
| 14  | CONFIRMED Q5    | For teachers (CPU / bo_teacher login): auto-populated class list shows ALL classes under the selected course, not scoped to that teacher's assigned lessons                             |
| 15  | CONFIRMED Q6 ⚠️ | BREAKING CHANGE: Class filter now REQUIRES course selection first. Users cannot filter by class without first selecting a course. Old behavior (direct class selection) is no longer supported. All 8 existing LT-74136 calendar class filter test cases must be reviewed/updated. |

---

## 2. Logic Type Categorization

| AC / Source     | Business Rule # | Logic Type(s)                                 | Notes                                                                        |
| --------------- | --------------- | --------------------------------------------- | ---------------------------------------------------------------------------- |
| AC 01.1         | 1, 2            | Conditional logic, Cross-system impact        | Course selection triggers class list population on both SF and BO            |
| AC 01.1         | 3               | Conditional logic                             | Checked state = inactive until user action                                   |
| AC 02.1         | 4, 5            | State transition                              | Class transitions: hidden → unchecked → checked → unchecked                  |
| AC 02.1         | 6               | Conditional logic                             | Course/class filter independence                                             |
| PRIOR: BR-35    | 7               | Data integrity, Conditional logic             | AND logic must be preserved with new interaction flow                        |
| PRIOR: BR-09    | 8               | Conditional logic, Cross-system impact        | Course filter logic unchanged; regression check needed                       |
| CONFIRMED Q4    | 10              | Conditional logic, State transition           | Class section visibility gated by course selection                           |
| CONFIRMED Q1    | 11              | Permission logic, Conditional logic           | Lesson type (Group vs Individual) gates class filter section                 |
| CONFIRMED Q2    | 12              | State transition                              | Course deselect → class list state resets to hidden                          |
| CONFIRMED Q3    | 13              | Data integrity                                | Scope rule: system-wide, not date/location-scoped                            |
| CONFIRMED Q5    | 14              | Permission logic                              | Teacher role — same global scope as HQ/CM                                    |
| CONFIRMED Q6    | 15              | Conditional logic, Regression Analysis ⚠️     | Breaking change: class gated behind course; all prior class-only TCs invalid |

---

## 3. Test Technique Selection

| Logic Type              | Applicable Techniques                               | Notes                                                         |
| ----------------------- | --------------------------------------------------- | ------------------------------------------------------------- |
| Conditional logic       | Decision Table, Equivalence Partitioning            | Map course-selected vs not-selected; lesson type conditions   |
| State transition        | State Transition Testing, CRUD Testing              | Class visibility state machine; course deselect path          |
| Cross-system impact     | Regression Analysis, CRUD Testing                   | Verify SF and BO both updated; existing ALL-match TCs re-run  |
| Data integrity          | Decision Table, Regression Analysis                 | ALL-match (AND) must survive interaction flow changes         |
| Permission logic        | Permission Matrix, Decision Table                   | HQ, CM, Teacher roles; Individual vs Group lesson type        |
| Regression Analysis     | Regression Analysis                                 | BR-15 breaking change — 8 existing TCs need flow update       |

---

## 4. Structured Coverage Strategy

| AC / Source  | Business Rule Summary                                                | Logic Type                          | Test Technique                              | Risk Level   | Coverage Depth |
| ------------ | -------------------------------------------------------------------- | ----------------------------------- | ------------------------------------------- | ------------ | -------------- |
| BR-10        | Class section hidden before course selected                          | Conditional, State Transition       | State Transition Testing                    | **High**     | Standard       |
| BR-11        | Class section hidden for Individual lessons (even with course)       | Conditional, Permission             | Decision Table, Equivalence Partitioning    | **High**     | Standard       |
| AC 01.1 BR-1 | [SF] Course selected → class list auto-populated, all unchecked      | Conditional, Cross-system           | Decision Table, CRUD Testing                | **High**     | Deep           |
| AC 01.1 BR-2 | [BO] Course selected → class list auto-populated, all unchecked      | Conditional, Cross-system           | Decision Table, CRUD Testing                | **High**     | Deep           |
| AC 01.1 BR-3 | Auto-populated classes are inactive — calendar not yet filtered      | Conditional                         | Decision Table                              | **Critical** | Deep           |
| AC 01.1 BR-13| Auto-populated list = ALL classes system-wide (not date/location)    | Data Integrity                      | Equivalence Partitioning, Boundary          | **Medium**   | Standard       |
| AC 02.1 BR-4 | User checks class → becomes active filter criterion                  | State Transition                    | State Transition Testing, Decision Table    | **High**     | Deep           |
| AC 02.1 BR-5 | User unchecks class → removed from active filter                     | State Transition                    | State Transition Testing                    | **High**     | Standard       |
| AC 02.1 BR-6 | Uncheck class does NOT deselect course                               | Conditional                         | Decision Table, Negative Testing            | **High**     | Standard       |
| BR-12        | Course deselected → class list auto-clears                           | State Transition                    | State Transition Testing                    | **High**     | Standard       |
| BR-7 (prior) | ALL-match (AND) logic still applies for multi-class filter           | Data Integrity, Regression          | Regression Analysis, Decision Table         | **Critical** | Deep           |
| BR-8 (prior) | Course filter logic unchanged (Individual: SS course, Group: lesson) | Conditional, Regression             | Regression Analysis                         | **Medium**   | Smoke          |
| BR-14        | Teacher (CPU): class list shows ALL classes under course             | Permission                          | Permission Matrix                           | **Medium**   | Standard       |
| BR-15 ⚠️     | BREAKING CHANGE: Class filter requires course first                  | Conditional, Regression             | Regression Analysis, Decision Table         | **Critical** | Deep           |
| Edge case    | Course with 0 associated classes → class section shows empty state   | Boundary, State Transition          | Boundary Value Analysis, Negative Testing   | **Medium**   | Standard       |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
| ---- | ------ | -------------------- |
| BR-3 — Auto-populated classes inactive (calendar not filtered) | If auto-populated classes are accidentally activated, the calendar silently applies a class filter the user never intended. Users would see wrong/missing lessons without any visible indication. Previous behavior auto-checked these classes — regression back to old behavior is a real risk. | Verify calendar shows ALL course lessons after course selection + class auto-population. Verify no class filter is applied. Compare lesson count before/after course selection (should remain the same until a class is manually checked). |
| BR-7 — ALL-match logic preserved | The AND-match logic (BR-35 from LT-74136) must survive the interaction flow change. If the new code path that handles class population accidentally changes filter logic to OR-match, users would see over-inclusive results. Hard to detect without explicit regression. | Re-execute the 2 existing ALL-match decision table tests (SF + BO) with the new flow (select course first → class appears → check two classes → verify AND-match). |
| BR-15 — Class filter requires course selection | This is a breaking behavioral change from LT-74136. If the dependency is not enforced (e.g., class list still shows without course selection in some edge condition), or if the enforcement is too aggressive (breaks existing BO functions), both scenarios produce incorrect behavior. | Verify class section is hidden with no course selected. Verify selecting course reveals class section. Verify directly navigating to class filter section without course selection has no effect. |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
| ---- | ------ | -------------------- |
| BR-1 + BR-2 — Core auto-population behavior on SF + BO | Primary new behavior. If auto-population only works on one platform but not the other, or if classes are populated for the wrong course, filtering will be broken for users. | Test both SF and BO independently. Verify class list contents match the selected course. |
| BR-4 + BR-5 + BR-6 — Check/uncheck class independence | The key UX improvement of this ticket. If unchecking a class also deselects the course (regression to coupled behavior), users lose the course filter unexpectedly. | State transition test: select course → check class → verify filter applied → uncheck class → verify course remains → verify calendar shows all course lessons. |
| BR-12 — Course deselected → class list clears | If class list persists after course is cleared, stale class filters may be silently applied when user selects a new course. Decision: does clearing course also clear checked classes? Test with classes already checked when course is cleared. | Test: select course → check 2 classes → deselect course → verify class list hidden/cleared → re-select course → verify class list resets (no residual checked state). |
| BR-10 + BR-11 — Class section visibility gating | If class section is visible without course selection, users can potentially interact with an undefined state. If Individual lesson type incorrectly shows class section, data integrity is at risk. | Verify initial state (no course): class section hidden. Verify with Group lesson type filter: class section appears on course select. Verify with Individual lesson type: class section stays hidden even after course select. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
| ---- | ------ | -------------------- |
| BR-13 — System-wide class scope | If scope is accidentally restricted to date/location range, users selecting courses for past/future terms won't see expected classes. | Select course that has classes scheduled outside current calendar view — verify those classes still appear in the class filter list. |
| BR-14 — Teacher (CPU) role | Teachers see all classes, not scoped to their own lessons. If scope is incorrectly narrowed, teachers can't filter the calendar properly. | Log in as teacher (CPU). Select a course. Verify all classes system-wide under that course appear in the class list (including classes from lessons not assigned to this teacher). |
| Edge case — Course with 0 classes | If empty state is unhandled, UI may crash, show a loading spinner, or display a confusing blank section. | Select a course that has no associated classes. Verify class section shows an empty state gracefully (e.g., "No classes available" or empty list — no crash, no spinner stuck). |

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area                                                          | Existing Test Case                                                                       | Overlap | New Coverage Needed                                                                                                  |
| ----------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------- |
| BR-10: Class section hidden before course selected                | None                                                                                     | None    | ✅ New TC: Verify class section is hidden when no course is selected (SF + BO)                                        |
| BR-11: Individual lesson → class section hidden even after course | None                                                                                     | None    | ✅ New TC: Select Individual lesson type + select course → class section stays hidden                                 |
| AC 01.1 BR-1/2: Course selected → classes auto-populated unchecked | None                                                                                    | None    | ✅ New TC: Select course → verify class list appears, all unchecked (SF); same for BO                                 |
| AC 01.1 BR-3: Auto-populated classes are NOT active filter criteria | None                                                                                    | None    | ✅ New TC: After course select + class auto-population, verify calendar NOT filtered by class (shows all course lessons)|
| BR-13: Scope = all classes system-wide                            | None                                                                                     | None    | ✅ New TC: Verify classes outside current date/location range are also in the list                                    |
| AC 02.1 BR-4: Check class → active filter                        | `06-ui-filter.md` — "Single Class Selected" (uses OLD flow without course pre-select)    | Partial | ✅ Update existing TC to select course first, THEN check class; verify calendar filters                               |
| AC 02.1 BR-5/6: Uncheck class → course stays active              | None                                                                                     | None    | ✅ New TC: Check class → uncheck → verify course still selected, calendar shows all course lessons                    |
| BR-12: Course deselected → class list clears                     | None                                                                                     | None    | ✅ New TC: Select course → check classes → deselect course → verify class list cleared; re-select course → fresh list  |
| BR-7: ALL-match logic preserved (regression)                     | `06-ui-filter.md` — "Two Classes Selected – ALL-Match" (SF + BO, OLD flow)              | Partial | ✅ Update existing TCs: pre-select course first, THEN check two classes, verify AND-match still works                 |
| BR-14: Teacher (CPU) sees all classes                             | None                                                                                     | None    | ✅ New TC: Teacher login → select course → verify all system-wide classes shown                                       |
| BR-15: Class requires course (breaking change)                   | `06-ui-filter.md` — ALL 8 class filter TCs use direct class selection without course    | BROKEN  | ✅ All 8 existing TCs need flow update: add course selection step before class selection step                          |
| Edge: Course with 0 classes → empty state                        | None                                                                                     | None    | ✅ New TC: Select course with no associated classes → class section visible but empty; no error                       |
| Full user journey (course → class → filter → uncheck)            | None                                                                                     | None    | ✅ New TC: E2E journey test on both SF and BO                                                                         |

---

## 7. Suggested Test Suite Structure

```
output/test-cases/lesson-management/lesson/course-class-filter/
├── 01-class-section-visibility.md
│     → BR-10, BR-11
│     → Class section hidden before course; Group vs Individual gating
│     → Platforms: SF + BO
│
├── 02-course-selection-class-population.md
│     → AC 01.1 (BR-1, BR-2, BR-3, BR-13)
│     → Course selected → class list auto-populated, unchecked, not active
│     → Scope: all classes system-wide; edge case: 0 classes
│     → Platforms: SF + BO
│
├── 03-class-filter-check-uncheck.md
│     → AC 02.1 (BR-4, BR-5, BR-6)
│     → Check class → active filter; uncheck → removed; course unaffected
│     → Full user journey (select course → check → uncheck → recheck)
│     → Platforms: SF + BO
│
├── 04-course-deselect-class-clear.md
│     → BR-12
│     → Deselect course → class list auto-clears
│     → Including: with no classes checked, with classes already checked
│     → Platforms: SF + BO
│
├── 05-all-match-regression.md
│     → BR-7 (BR-35 from LT-74136)
│     → Multi-class AND-match logic preserved with new interaction flow
│     → Update of existing TCs: pre-select course first
│     → Platforms: SF + BO
│
├── 06-class-requires-course-regression.md
│     → BR-15 (BREAKING CHANGE)
│     → Class filter requires course; class section hidden without course
│     → Review and update all 8 existing LT-74136 class filter TCs
│     → Platforms: SF + BO
│
└── 07-teacher-role.md
      → BR-14
      → Teacher (CPU login) class list scope: all classes system-wide
      → Platform: BO only
```

**Total estimated test cases: ~28–32**
- 01: 4 TCs (hidden state + Individual gating on SF + BO)
- 02: 7 TCs (core auto-populate happy path SF+BO; 0-classes edge; inactive verification; scope)
- 03: 6 TCs (check, uncheck, course stays, full journey SF+BO)
- 04: 4 TCs (deselect with no checks, deselect with checks; re-select fresh state SF+BO)
- 05: 4 TCs (ALL-match updated flow SF+BO; 0-result state)
- 06: 6 TCs (class requires course; confirm 8 existing TCs updated in new flow)
- 07: 2 TCs (teacher CPU login SF+BO — BO only per BR-14 platform scope)
