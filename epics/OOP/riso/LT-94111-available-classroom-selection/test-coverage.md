# Test Coverage: LT-94111 — Riso available classroom selection

**Jira:** https://manabie.atlassian.net/browse/LT-94111  
**Primary requirement:** Confluence PRD 2121531393  
**Date:** 2026-09-09 (revised 2026-09-11 — added code-review risk findings)  
**Qase target:** PX suite 3480 (currently empty)

> Scope decision: every one of the 13 confirmed Lesson/Calendar entry points has at least one dedicated test case. AC 01.6 is excluded until LT-102507 is implemented.

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---:|---|---|
| 1 | AC 01.1 | Sequence is optional; supplied values are positive integers only and duplicates are allowed. |
| 2 | AC 01.2 | Classroom has no option until Location, date, start time, and end time are defined. |
| 3 | AC 01.2 | Only classrooms passing the PRD vacant/occupied checks at the selected Japan-local date/time are selectable. |
| 4 | AC 01.2 | An exact time match is occupied and hidden. |
| 5 | AC 01.2 | A same-start/different-end overlap is occupied and hidden. |
| 6 | AC 01.2 | A different-start/same-end overlap is occupied and hidden. |
| 7 | AC 01.2 | A classroom occupied within the selected period is hidden. |
| 8 | AC 01.2 | Sort available classrooms by Sequence ASC, Name ASC, then created date ASC. |
| 9 | AC 01.2 | Prefill the first sorted available Classroom; every confirmed editable role except PT Teacher may adjust it. |
| 10 | AC 01.2 | With no vacancy, leave Classroom unselected and show `No option`. |
| 11 | AC 01.3 | A Location change resets Classroom to blank; the user manually reselects after opening the field. |
| 12 | AC 01.3 | A date, start-time, or end-time change resets Classroom to blank; the user manually reselects after opening the field. |
| 13 | AC 01.4 | For a weekly recurring lesson, evaluate availability only at the selected/first lesson datetime in every confirmed flow. |
| 14 | AC 01.5 | Classroom is required in Riso and optional in Core; PT Teacher cannot edit Classroom. |
| 15 | AC 01.6 | Deferred — test after LT-102507 implementation. |
| 16 | AC 02.1 | Reject an overlapping/duplicate Save and show the exact PRD English/Japanese errors. |
| 17 | Scope | Cover each of the 13 named Lesson/Calendar creation and edit flows with a dedicated case. |

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---:|---|
| AC 01.1 | 1 | Validation logic; Boundary/range logic; Ordering / Sort |
| AC 01.2 | 2 | Conditional logic; Display completeness |
| AC 01.2 | 3–7 | Data integrity; Boundary/range logic; Date/time |
| AC 01.2 | 8–9 | Ordering / Sort; Conditional logic |
| AC 01.2 | 10 | Conditional logic; Display completeness |
| AC 01.3 | 11–12 | State transition; Conditional logic; Data integrity |
| AC 01.4 | 13 | Recurrence logic; Conditional logic; Data integrity |
| AC 01.5 | 14 | Permission logic; Conditional logic; Validation logic |
| AC 01.6 | 15 | N/A — explicitly deferred to LT-102507 |
| AC 02.1 | 16 | Validation logic; Data integrity; Concurrent / stale state |
| Scope | 17 | Cross-system impact; Regression; Conditional logic |

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Validation logic | Equivalence Partitioning; Negative |
| Boundary/range logic | Boundary Value Analysis; Negative |
| Conditional logic | Decision Table; Negative |
| Recurrence logic | State Transition; Regression |
| Permission logic | Permission Matrix; Decision Table |
| Data integrity | CRUD; Regression; Decision Table |
| Cross-system impact | Regression; CRUD |
| Display completeness | Component; Negative |
| Ordering / Sort | Scenario; Pairwise |
| Concurrent / stale state | Decision Table; Negative; CRUD |
| Date/time | Boundary Value Analysis; Decision Table; Regression |

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC 01.1 | Show the optional Classroom Sequence field; accept positive integers, reject supplied zero, negatives, decimals, and nonnumeric input, and allow duplicate positive values. | Validation; Boundary; Ordering; Display completeness | Equivalence Partitioning; BVA; Negative; Component | Medium | Deep |
| AC 01.2 | Keep Classroom at No option until all availability inputs exist. | Conditional; Display completeness | Decision Table; Component | High | Standard |
| AC 01.2 | Hide exact, same-start, same-end, contained, containing, and strict partial-overlap occupied rooms; retain both adjacent non-overlap boundaries. | Data integrity; Boundary | Decision Table; BVA; Regression | Critical | Deep |
| AC 01.2 | Code-review risk (2026-09-11), confirmed as intended: the full lesson-status occupancy matrix — Draft, Published, and Completed all occupy a Classroom; Cancelled is the only excluded status. | Data integrity; Conditional | Decision Table; Negative | Critical | Deep |
| AC 01.2 | Scope the Classroom selector to the Lesson Location; an overlap at another Location must not suppress a vacant Classroom at the selected Location. | Conditional; Data integrity; Display completeness | Decision Table; Regression | Critical | Deep |
| AC 01.2 | Evaluate availability using Japan-local time at the UTC/JPT date boundary. | Date/time; Data integrity | BVA; Regression | High | Deep |
| AC 01.2 | Sort two or more available rooms by Sequence, then Name, then created date; do not assert blank-Sequence rank. | Ordering / Sort | Scenario; Pairwise | Medium | Deep |
| AC 01.2 | Present first available room as the prefilled choice and show exact text `No option` with no vacancy. | Conditional; Display completeness | Decision Table; Component | High | Standard |
| AC 01.2 | Re-evaluate the prefill candidate when availability inputs change; it must follow the first currently available Classroom, not a now-occupied prior candidate. | State transition; Data integrity; Ordering / Sort | State Transition; Regression | Critical | Deep |
| AC 01.3 | Reset existing Classroom to blank after each editable Location/date/start/end change; only suggest the first vacant room after the field opens. | State transition; Data integrity | Decision Table; Regression | High | Deep |
| AC 01.3 | Code-review risk (2026-09-11): a fast Location-then-time change, or repeated rapid edits to the same field, must resolve to the final combined criteria and not display a stale intermediate response. | Concurrent / stale state | Negative; Decision Table | High | Standard |
| AC 01.4 | For each applicable recurring entry flow, evaluate only the selected/first lesson datetime and do not validate later occurrences. | Recurrence; Conditional | State Transition; Regression | High | Deep |
| AC 01.5 | Require Classroom for Riso, retain optional behavior for Core, and make Classroom non-editable for PT Teacher. | Permission; Validation | Permission Matrix; Equivalence Partitioning; Negative | High | Deep |
| AC 01.6 | Defer lowest-Sequence available Private-room auto-assignment until LT-102507 is implemented. | N/A — deferred | N/A — deferred | Low | Deferred |
| AC 02.1 | Reject a normal overlapping or duplicate Save with `<Classroom name> is already in use for another class.` and `<Classroom name>は既に他の授業で利用されています`. | Validation; Data integrity | Decision Table; Negative | Critical | Deep |
| AC 02.1 | Reject stale, concurrent, double-submit, and multi-tab attempts without persisting an overlapping assignment. | Concurrent; Data integrity | Decision Table; CRUD; Negative | Critical | Deep |
| Scope F01 | New Lesson on Lesson List SF applies availability, ordering, Riso requiredness, and overlap rejection. | Cross-surface; Regression | Scenario; Regression | High | Standard |
| Scope F02 | Edit Lesson on SF resets/re-evaluates Classroom after every editable availability input. | Cross-surface; State transition | Scenario; Regression | High | Standard |
| Scope F03 | Add Lesson in Lesson Schedule Detail applies Classroom availability and Save rejection to the added lesson. | Cross-surface; Data integrity | Scenario; Regression | High | Standard |
| Scope F04 | Extend Recurrence in Lesson Schedule Detail asserts the Classroom field state and selected/first-instance scope. | Recurrence; Cross-surface | State Transition; Regression | High | Standard |
| Scope F05 | Duplicate Lesson on SF re-evaluates a prefilled Classroom before Save. | State transition; Data integrity | Scenario; Regression | High | Standard |
| Scope F06 | Edit Lesson on BO honors Classroom editability, requiredness, and overlap rejection. | Permission; Cross-surface | Permission Matrix; Regression | High | Standard |
| Scope F07 | New Lesson on Calendar SF applies availability, ordering, requiredness, and overlap rejection. | Cross-surface; Regression | Scenario; Regression | High | Standard |
| Scope F08 | New Lesson by DnD asserts entry-point availability or locked-field state and conflict protection. | Cross-surface; Data integrity | Scenario; Regression | High | Standard |
| Scope F09 | Edit Lesson by DnD re-evaluates after a date/time change, or asserts locked-field state, then prevents a conflict. | State transition; Data integrity | Scenario; Regression | High | Standard |
| Scope F10 | New Lesson by Available Teacher Calendar applies availability, ordering, requiredness, and overlap rejection. | Cross-surface; Regression | Scenario; Regression | High | Standard |
| Scope F11 | Edit Lesson on Calendar SF re-evaluates a selected Classroom after editable input changes. | State transition; Data integrity | Scenario; Regression | High | Standard |
| Scope F12 | Duplicate Lesson on Calendar SF re-evaluates a prefilled Classroom before Save. | State transition; Data integrity | Scenario; Regression | High | Standard |
| Scope F13 | Edit Lesson on Calendar BO honors Classroom editability, requiredness, and overlap rejection. | Permission; Cross-surface | Permission Matrix; Regression | High | Standard |

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Availability and Save-time overlap protection | Incorrect filtering or a stale Save can persist two lessons in one classroom/time slot. | Run the full overlap matrix, Japan-local-time boundary tests, concurrent two-user/multi-tab tests, and exact EN/JP error assertions. |
| 13-flow parity | An entry point can bypass the shared availability or blocking validation. | One dedicated case per flow plus a traceability matrix; verify editable versus locked fields per entry point. |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Classroom reset | A stale classroom may survive a Location/date/time change and be saved. | Cover each editable availability input and confirm blank state, manual reselection, and post-open suggestion. |
| Recurrence scope | Validating following instances would alter approved behavior; failing to validate the selected instance would permit an immediate clash. | Test selected/first instance and a later conflicting occurrence in every applicable recurrence flow. |
| Tenant/role behavior | Riso-required validation or PT edit restriction can regress Core or BO behavior. | Use an Riso/Core × editable/PT Teacher permission matrix. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Sequence validation and ordering | Invalid values or an incorrect tie-breaker create unexpected classroom selection. | Partition supplied values; use 2+ rooms with duplicate Sequence/Name/created-date tie-break data. |

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Classroom time clash semantics | `LT-98512 .../clash-and-failure-handling.md` | Existing Riso clash coverage is adjacent only; it does not cover lesson-upsert dropdown or all 13 flows. | ✅ PRD occupied matrix, JPT boundary, dropdown filtering, and exact Save error. |
| Lowest-sequence classroom behavior | `LT-98512 .../assignment-rules.md` | Covers reassignment strategy, not lesson-upsert Sequence field validation/sort. | ✅ Positive-integer validation, duplicate Sequence tie-breaker, prefill, and No option. |
| SF lesson upsert | `LT-101769 .../sf-create-lesson-ui.md`, `sf-edit-lesson-ui.md` | Baseline UI only; no new Riso availability behavior. | ✅ F01, F02, F05 flow-specific cases. |
| Schedule detail / recurrence | `LT-90573 .../LT-90573-extend-recurring-lesson.csv` | Existing Classroom dropdown/recurrence coverage predates this availability rule. | ✅ F03, F04 selected-first-instance cases. |
| Calendar / DnD | `LT-XXXX .../Drag and drop to edit Lesson time on Calendar.csv` | Existing DnD time updates do not re-check Classroom availability or Save rejection. | ✅ F07–F13 flow-specific cases. |
| BO lesson/calendar edit | Domain permission matrix | Lists Edit Lesson access only; no Classroom behavior cases. | ✅ F06 and F13 role/editability cases. |
| AC 01.6 | None | Planned implementation is not available. | Deferred — no LT-94111 case until LT-102507 is implemented. |
| Code-review risk findings (2026-09-11) | None — found via `erp-salesforce` source review, not the PRD | Recurrence-scope and JST-conversion risks confirmed as intended by user; DB-level double-booking risk tracked as a separate bug ticket. | ✅ Added: rapid Location/time-change race case, repeated rapid time-edit case (`classroom-reset-and-recurrence.md`), and a full 4-status occupancy matrix — Draft/Published/Completed occupy, Cancelled does not (`classroom-sequence-and-availability.md`). |

## 6.1 Edge-Case Checklist

| Area | Coverage decision |
|---|---|
| A. Configuration / threshold | N/A — the PRD defines no configurable threshold, limit, or feature flag. |
| B. Date / time | Cover all PRD overlap shapes, an adjacent end-equals-next-start non-overlap, contained and containing periods, and Japan-local (UTC+09:00) date-boundary/cross-midnight conversion. |
| C. Data integrity | Cover normal Save, stale selector data, two-user/multi-tab concurrent Save, and repeated submit; only one non-conflicting lesson may persist. |
| D. Permission / tenant | Cover Riso-required versus Core-optional validation; ensure PT Teacher cannot edit Classroom; include permitted SF and BO edit flows. |
| E. State transition | Cover blank reset for every editable Location/date/start/end change, manual re-selection, and first-vacant suggestion only when the selector opens. |
| F. Cross-surface | Cover all F01–F13 Lesson, Schedule Detail, Calendar, DnD, Available Teacher Calendar, SF, and BO paths. |
| G. Downstream effects | Mapped in Section G for create/update/persist/reject behavior. |
| H. Display / ordering | Cover prerequisite/no-vacancy states, `No option`, prefill, exact bilingual errors, and the complete sort tie-breaker. No pagination or responsive requirement is specified. |

## 7. Suggested Test Suite Structure

```text
epics/OOP/riso/LT-94111-available-classroom-selection/test-cases/
├── classroom-sequence-and-availability.md       → AC 01.1–01.2; validation, occupied matrix, JPT, ordering, empty state
├── lesson-upsert-flows.md                       → F01–F06; six Lesson entry-point cases
├── calendar-upsert-flows.md                     → F07–F13; seven Calendar entry-point cases
├── classroom-reset-and-recurrence.md            → AC 01.3–01.4; reset and recurrence-scope cases
├── riso-permission-and-requiredness.md          → AC 01.5; Riso/Core and PT Teacher matrix
└── classroom-save-concurrency.md                → AC 02.1; errors, stale save, double-submit, multi-tab
```

## G. Downstream Effects Inventory

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner (TC) |
|---|---|---|---|
| Create/edit/duplicate lesson with Classroom | Classroom value is persisted only when it remains available. | Lesson record / entry flow | F01–F13 flow cases |
| Update Location/date/start/end | Stale Classroom is cleared before a later Save. | Lesson record / Classroom selector | AC 01.3 reset cases |
| Save an overlapping Classroom | No conflicting lesson assignment is persisted; user receives exact EN/JP error. | Lesson record / Save feedback | AC 02.1 overlap and concurrency cases |
| Update Classroom on SF | Updated Classroom remains visible through SF lesson/calendar surfaces and synced BO lesson/calendar views where applicable. | SF and BO surfaces | F02, F06, F09, F11, F13 regression cases |
| Rapid or concurrent Save | Exactly one non-overlapping assignment can persist. | Persistence layer / two user sessions | AC 02.1 concurrency cases |

N/A: No counter, child-record, notification, or inverse-action rule is defined by this Classroom selection feature.

## H. Display & Ordering Inventory

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| Classroom Master | Sequence | Optional blank / supplied value | N/A | Validation feedback for invalid supplied values, if defined by implementation |
| Lesson/Calendar upsert Classroom selector | Classroom selector, Location, lesson date, start time, end time | No option before prerequisites / no vacancy; PT Teacher non-editable | Sequence ASC → Name ASC → created date ASC | `No option` |
| Save feedback | Classroom name in error | Only on overlap/duplicate | N/A | `<Classroom name> is already in use for another class.`; `<Classroom name>は既に他の授業で利用されています` |

H.1 — N/A: No Figma URL is linked in the Jira ticket, PRD, or reference pages.
