---
ticket_id: LT-98512
ticket_url: https://manabie.atlassian.net/browse/LT-98512
title: Riso Classroom Reassignment by Student (Classroom Optimization)
module: scheduling
bucket: OOP/riso
status: Ready for QA
internal_uat_date: 2026-09-07
production_release_date: 2026-09-07
last_updated: 2026-08-20
---

# LT-98512: Riso Classroom Reassignment by Student

## Summary

Add a Riso-only Classroom Adjustment action to Salesforce Lesson Calendar Daily View. For the selected Location and Lesson Date, it assigns/reassigns classrooms for Individual lessons student-by-student to maximize room continuity while preventing classroom clashes; users can then review, manually correct, and print the daily plan.

The primary source is [the Confluence PRD](https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2416181249/Riso+OOP+Classroom+Reassignment+by+Student+Classroom+Optimization), current page status Done. The target Qase suite root is `PX` suite 3231, with child suites 3232-3237 for this epic's grouped cases.

---

## Acceptance Criteria

### US01 — Run classroom adjustment from Lesson Calendar

| ID | Requirement |
|---|---|
| AC-01 | Add Classroom Adjustment above the existing Print Out action in Daily View. |
| AC-02 | Show the action only in Daily View. |
| AC-03 | On click, process the current Location and Lesson Date, only where Teaching Method = Individual. |
| AC-04 | After success, show “Classroom adjustment completed” and lightweight counts: Previous room applied, Sequence assigned, Skipped, Clash resolved, Clash unresolved (kept as-is). |
| AC-05 | Preserve the existing Print Out flow after adjustment. |

### US02 — Apply classroom adjustment rules

| ID | Requirement |
|---|---|
| AC-06 | Process only lessons for the selected Location and Lesson Date. |
| AC-07 | Process per student: earlier start time first; equal start times use earlier Lesson ID first. |
| AC-08 | For every lesson after the student’s earliest lesson, first try the classroom from the most recently processed earlier lesson when available for the target slot. |
| AC-09 | If Rule 1 cannot apply, use Rule 2. |
| AC-10 | Rule 2 assigns the available classroom with the lowest Classroom Sequence. |
| AC-11 | Available means selected Location, Classroom Type = Private, and not assigned to another lesson in the same slot. The note about existing selectability/Classroom Status is marked “Later maybe v2.” |
| AC-12 | Do not use a classroom when Rule 1 or Rule 2 would clash. |
| AC-13 | Support 3+ lessons per student and repeat Rules 1/2 in chronological order. |
| AC-14 | Continue processing remaining lessons after one lesson cannot be assigned. |
| AC-15 | If no room is available after Rules 1/2, skip the lesson and retain its current classroom. |
| AC-16 | Skip a lesson with two students and retain its current classroom. |
| AC-17 | At process start, preserve one lesson in each pre-existing same-classroom/same-slot duplicate and reassign the others with Rule 2. |
| AC-18 | If a pre-existing clash cannot be resolved, retain the current classroom, mark it unresolved/skipped, and continue. |
| AC-19 | Preserve the duplicate lesson chosen by chronological priority; break ties with earlier Lesson ID. |

### US03 — Review and manually adjust

The PRD labels this criterion as **AC-17** again: after automation, users can still manually modify classroom assignments. This duplicate ID needs correction.

### NFRs

- Up to 400 lessons/day/location without unacceptable operational delay.
- Restrict processing and updates to the selected Location and Lesson Date.
- Design for up to 100 locations with similar daily patterns.
- Isolate individual failures; preserve data integrity; retain usability and maintainability.
- Handle simultaneous runs safely without inconsistent results.

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Behavior | Platform |
|---:|---|---|---|---|---|
| 1 | AC-01 | Place action above Print Out. | Action | required | SF |
| 2 | AC-02 | Hide action outside Daily View. | Action | locked/hidden | SF |
| 3 | AC-03 | Scope to selected Location/Date and Individual lessons. | Scope | auto-calculated | SF |
| 4 | AC-04 | Show five result counters after success. | Result summary | auto-calculated | SF |
| 5 | AC-05 | Keep Print Out available. | Print Out | required | SF |
| 6–8 | AC-07 | Group per student; sort by start time, then Lesson ID. | Processing order | auto-calculated | SF |
| 9–11 | AC-08–09 | Reuse last processed room for later lessons; otherwise invoke Rule 2. | Assignment strategy | auto-calculated | SF |
| 12 | AC-10 | Choose lowest-sequence eligible classroom. | Classroom | auto-calculated | SF |
| 13–16 | AC-11–12 | Eligible classroom is selected-location, Private, and clash-free. | Availability / Type | required / locked | SF |
| 17–18 | AC-13–14 | Repeat for 3+ lessons and continue after a per-lesson failure. | Process | auto-calculated / required | SF |
| 19–20 | AC-15–16 | Retain classroom for no-room and two-student skips. | Classroom | locked | SF |
| 21–23 | AC-17–19 | Reconcile pre-existing duplicates deterministically using Rule 2 and chronological priority. | Pre-existing clash | auto-calculated / locked | SF |
| 24 | US03 AC-17 | Allow manual classroom edits after the run. | Classroom | editable | SF |
| 25 | Config | Use Optimize Classroom Assignment setting, enabled for Riso only. | Setting | required | SF |
| 26 | NFR-01 | Support Riso workload; SLA is not finalized. | Runtime | required | SF |
| 27 | NFR-08 | Avoid inconsistent concurrent results. | Concurrency | required | SF |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---:|---|---|---|---|
| 1 | [CONFLICT] | Confluence PRD 2416181249 | AC-15 | AC-15 and Tech Consideration retain the current classroom, while embedded Set B/B3 leaves the lesson unassigned. |
| 2 | [REGRESSION RISK] | `epics/calendar/LT-XXXX-drag-drop-edit-lesson-time/Drag and drop to edit Lesson time on Calendar.csv` | AC-11/12 | Existing Calendar tests define a partial same-classroom overlap as a clash. “Same slot” must not be implemented as exact-time equality only. |
| 3 | [IMPLEMENTATION GAP] | `ClassroomReassignmentController.cls` + `LessonRepo.getClassroomsByLocation` | AC-11 | Current code orders classrooms by `Sequence__c ASC NULLS LAST, Name ASC, CreatedDate ASC` for the selected location but does not filter Classroom Type = Private or Classroom Status/selectability. |
| 4 | [IMPLEMENTATION DETAIL] | `individualCalendar.js` | AC-03/04 | FE ignores optimize payloads when teaching method is not Individual or when location/date is missing; no Apex call and no success toast should be produced. |

### Missing in Requirements

| # | Tag | Source | Description |
|---:|---|---|---|
| 1 | [ROLE GAP] | `knowledge/domain-knowledge/scheduling/calendar/calendar-bo.md` | Daily View is available on BO, but BO Calendar is read-only; the PRD must explicitly name the target platform/roles. |
| 2 | [MISSING BEHAVIOR] | PRD AC-04 | Counter categories and their reconciliation are undefined. |
| 3 | [MISSING BEHAVIOR] | PRD AC-08 | No candidate-room rule for an invalid/changed earliest lesson. |
| 4 | [MISSING BEHAVIOR] | PRD AC-11 | V1 use of existing Classroom Type, Classroom Status, and selectability is ambiguous versus the current repository query. |
| 5 | [MISSING BEHAVIOR] | PRD AC-16 | Zero- and 3+-student Individual lesson handling is undefined. |
| 6 | [MISSING BEHAVIOR] | PRD AC-17 | AC-17 is duplicated for two unrelated requirements. |
| 7 | [MISSING BEHAVIOR] | PRD NFR-01 | No approved performance threshold, timeout, or benchmark dataset. |
| 8 | [MISSING BEHAVIOR] | PRD NFR-08 | Concurrency resolution and user-visible outcome are unspecified. |

### Lesson-Learned Risks

No historical incident passed the required two-factor match (same entity and same operation). The three scheduling incidents reviewed concern Student Session creation/assignment or Nichibei LA/point synchronization; this feature only reads student/session context and updates classrooms.

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-19 | Riso — Lesson Allocation & Subject in Detail | Adjacent Riso lesson/student setup only; no Classroom Adjustment coverage. | CREATE dedicated Riso Classroom Adjustment E2E. |

### Assumptions Made

- The Confluence PRD is authoritative over the shorter Jira description when sources differ.
- The target UI is Salesforce unless clarified; BO Calendar cannot update lesson classrooms.
- The feature’s new Riso setting is independent of the existing EEA-only `Enable Calendar Drag And Drop` setting.
- No Figma URL/design is linked in Jira or the PRD.

---

## Clarification Questions

1. **[CONFLICT]** When neither Rule 1 nor Rule 2 can find a room, which outcome is authoritative: retain the current classroom, or leave the lesson without a classroom? Define the summary category too.
   _Evidence: `Confluence PRD 2416181249` — AC-15/Tech Consideration conflict with Set B/B3._

2. **[REGRESSION RISK]** Does “same slot” mean any time overlap is unavailable, including partial overlaps?
   _Evidence: `epics/calendar/LT-XXXX-drag-drop-edit-lesson-time/Drag and drop to edit Lesson time on Calendar.csv` — partial overlap is an existing classroom clash._

3. **[MISSING BEHAVIOR]** How must AC-04 counters handle overlapping categories such as a clash resolved through Rule 2?
   _Evidence: `Confluence PRD 2416181249` — counter categories have no counting rules._

4. **[MISSING BEHAVIOR]** What is Rule 1’s candidate when the earliest lesson is invalid or changed by clash resolution?
   _Evidence: `Confluence PRD 2416181249` — AC-08 has no branch for this case._

5. **[MISSING BEHAVIOR / IMPLEMENTATION GAP]** Does V1 apply Classroom Type = Private, Classroom Status, or selectability rules?
   _Evidence: `Confluence PRD 2416181249` says Private; current `LessonRepo.getClassroomsByLocation` only filters by Account/location._

6. **[MISSING BEHAVIOR]** How are zero- or 3+-student Individual lessons handled?
   _Evidence: `Confluence PRD 2416181249` — AC-16 covers exactly two students only._

7. **[MISSING BEHAVIOR]** Please assign unique IDs to both AC-17 requirements.
   _Evidence: `Confluence PRD 2416181249` — US02 and US03 reuse AC-17._

8. **[MISSING BEHAVIOR]** What approved runtime, timeout/error behavior, and dataset define NFR-01 performance acceptance?
   _Evidence: `Confluence PRD 2416181249` — benchmark figures are notes, not final criteria._

9. **[MISSING BEHAVIOR]** What observable result is required for simultaneous actions or manual edits during processing?
   _Evidence: `Confluence PRD 2416181249` — NFR-08 gives no concurrency outcome._

10. **[ROLE GAP]** Is this Salesforce Daily View only, or also BO Daily View? Which current roles are eligible?
    _Evidence: `knowledge/domain-knowledge/scheduling/calendar/calendar-bo.md` — BO Calendar is read-only._

---

## Related Specs

- `epics/calendar/LT-XXXX-drag-drop-edit-lesson-time/spec.md` — existing Calendar Daily/Classroom View update and clash behavior.
- `epics/calendar/LT-89471-calendar-bug-fix/spec.md` — Daily View horizontal-navigation regression surface.
- `epics/calendar/LT-98532-bulk-publish-lessons-by-student/spec.md` — independent Riso Calendar action/config baseline.
- `/Users/chaut/Documents/Manabie/erp-salesforce/packages/lesson/main/default/classes/ClassroomReassignmentController.cls` — Apex assignment algorithm and summary counters.
- `/Users/chaut/Documents/Manabie/erp-salesforce/packages/lesson/main/default/classes/repository/LessonRepo.cls` — classroom query ordered by sequence/name/created date.
- `/Users/chaut/Documents/Manabie/erp-salesforce/packages/lesson/main/default/lwc/individualCalendar/individualCalendar.js` — LWC Apex call, guard clauses, toast summary, and calendar refresh.
- `/Users/chaut/Documents/Manabie/school-portal-admin/src/squads/calendar/domains/CalendarV2/Calendar/hooks/useCalendarAction/useCalendarAction.ts` — SPA action placement when `VITE_SF` and optimize setting are enabled.

## Related Test Cases

- `epics/calendar/LT-XXXX-drag-drop-edit-lesson-time/Drag and drop to edit Lesson time on Calendar.csv` — manual classroom-change and clash assertions that must remain true.
- `epics/calendar/LT-89471-calendar-bug-fix/test-cases/01-daily-view-scrollbar.md` — Daily View reachability baseline.

## QASE Coverage Gaps

- Qase `PX` suite 3231 is the parent suite for this epic's testcase set; child suites 3232-3237 are used for import grouping.
- Confirmed ACs are covered by new cases for action placement/visibility, scope, Rules 1-2, eligibility/clash semantics, skips, pre-existing clashes, result summary, manual follow-up, Print Out continuity, configuration, performance, and concurrency.
