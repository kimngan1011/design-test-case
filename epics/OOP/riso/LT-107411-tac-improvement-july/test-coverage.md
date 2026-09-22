# Test Coverage: LT-107411 — Riso | Core | TAC improvement (July)

**Jira:** https://manabie.atlassian.net/browse/LT-107411
**Date:** 2026-09-22

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---:|---|---|
| 1 | AC 01 | Empty Subject search shows no options; entered text enables normal search and selection. |
| 2 | AC 02 | Teacher search matches name, phonetic name, and external user ID; placeholders are localized exactly. |
| 3 | AC 03 | Student calendar chip displays Subject Name (Teacher Name). |
| 4 | AC 04 | Location is within the collapsible filter area and retains its selected filtering. |
| 5 | AC 05 | Course is required and fixed; only Available Teachers/Timeslot content scrolls; JP date excludes `/`. |
| 6 | AC 06 | Two duplicate lessons use the documented calendar chip and sidebar alert; one lesson remains normal. |
| 7 | AC 07 | Create success opens the created Lesson Schedule detail; cancel/error stay in their existing flow. |

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---:|---|
| AC 01 | 1 | Conditional, Display completeness |
| AC 02 | 2 | Equivalence partitioning, Display completeness |
| AC 03 | 3 | Display completeness |
| AC 04 | 4 | Conditional, Data integrity |
| AC 05 | 5 | Validation, Display completeness, Localization |
| AC 06 | 6 | Conditional, Display completeness, Cross-surface |
| AC 07 | 7 | State transition, Regression |

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Conditional | Decision Table, Negative |
| Validation | Equivalence Partitioning, Negative |
| Display completeness | Component, Regression |
| Data integrity | Regression |
| State transition | State Transition, Negative |
| Localization | Component |

## 4. Edge-Case Checklist Application

| Area | Applicability | Notes |
|---|---|---|
| A. Configuration thresholds | N/A | No partner-config threshold is specified. |
| B. Date/time | N/A | Display-format only; no calculation or timezone rule. |
| C. Concurrent/stale state | N/A | The changed paths do not reserve capacity or update shared data. |
| D. Permission & role | Yes | Test with HQ or CM Staff, the repository default actor for this staff workflow. |
| E. State transition | Yes | Successful creation changes route from form to the created Schedule detail. |
| F. Cross-surface | Yes | Duplicate state must agree between Calendar and sidebar. |
| G. Downstream effects | Yes | Create success must identify the created Schedule detail; no new entity behavior is introduced. |
| H. Display & ordering | Yes | Subject/Teacher labels, filters, Course, scrolling, JP date, duplicate chip, and warning text are visual contracts. |
| H.1 Spec–Figma mismatch | PBT resolved | PBT attachment screenshots are used as approved visual evidence because the linked Figma frame is inaccessible. |

### Downstream Effects Inventory Table

| Primary Action | Downstream Effect | Affected Surface | Verification Owner |
|---|---|---|---|
| Create Lesson | Route shows the created Lesson Schedule identity | SF Schedule detail | `create-lesson-navigation` |
| Open duplicated timeslot | Calendar duplicate chip and sidebar duplicate alert agree | SF Calendar + sidebar | `duplicate-lesson-indicator` |

### Display & Ordering Inventory Table

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| Teacher filter | EN/JP placeholder | Search matches 3 fields | N/A | `Search Teacher Name, External User ID`; `講師名、外部IDで検索` |
| Left sidebar | Date, `Course *`, Course selector | Scrollbar when list overflows | N/A | `7月1日` (no slash) |
| Duplicate sidebar | Timeslot, warning, lesson entry | Only when duplicate exists | N/A | `授業が重複しています(2件)` |

## 5. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC 01 | Empty Subject search shows no partial suggestions | Conditional | Decision Table, Negative | Medium | Standard |
| AC 01 | Typed Subject search and selection continue to filter | Regression | Equivalence Partitioning | High | Standard |
| AC 02 | Teacher Name, Phonetic Name, and External User ID each find the same teacher | Conditional | Equivalence Partitioning | High | Deep |
| AC 02 | EN and JP placeholders are exact | Display completeness | Component | Medium | Standard |
| AC 03 | Populated Subject and Teacher form one usable chip label | Display completeness | Component, Negative | Medium | Standard |
| AC 04 | Location hides/restores and selection persists | Conditional, Data integrity | State Transition, Regression | High | Standard |
| AC 05 | Missing Course blocks creation | Validation | Equivalence Partitioning, Negative | High | Standard |
| AC 05 | Course remains fixed while only list content scrolls | Display completeness | Component | Medium | Standard |
| AC 05 | JP date excludes slash | Localization | Component | Medium | Standard |
| AC 06 | Two duplicates use the documented chip and alert across both surfaces | Conditional, Cross-surface | Decision Table, Regression | High | Deep |
| AC 06 | One lesson remains normal | Conditional | Negative | Medium | Standard |
| AC 07 | Success reaches the created Schedule detail | State transition | State Transition, Regression | High | Standard |
| AC 07 | Cancel/error does not redirect to Calendar | State transition | Negative | Medium | Standard |

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Subject filter opening | LT-94698 subject filter | Partial | ✅ Empty-search behavior without partial suggestions |
| Teacher search fields | None identified | None | ✅ Name, phonetic name, external ID partitions |
| Student chip format | None identified | None | ✅ Subject-first label and truncation |
| Collapsible Location | Generic calendar filters | Partial | ✅ Hide/restore with selection retention |
| Fixed Course sidebar | None identified | None | ✅ Required validation, fixed position, scroll isolation, JP date |
| Duplicate lesson rendering | Existing duplicate-lesson creation cases | None | ✅ Calendar `2授業` chip and sidebar alert |
| Post-create route | E2E-01 Calendar view | Partial | ✅ Schedule-detail destination and cancel/error regression |

## 7. Suggested Test Suite Structure

```text
epics/OOP/riso/LT-107411-tac-improvement-july/test-cases/
|- subject-teacher-filters.md -> AC 01–02, 8 TCs
|- student-lesson-label.md -> AC 03, 2 TCs
|- filter-accordion.md -> AC 04, 3 TCs
|- course-timeslot-sidebar.md -> AC 05, 4 TCs
|- duplicate-lesson-indicator.md -> AC 06, 3 TCs
|- create-lesson-navigation.md -> AC 07, 3 TCs
```
