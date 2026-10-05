---
ticket_id: LT-94111
ticket_url: https://manabie.atlassian.net/browse/LT-94111
title: Riso | Core | Selectable Booths: Enable selection of only available; unassigned booths/classrooms.
module: scheduling
bucket: OOP/riso
status: Ready for QA
internal_uat_date: 2026-06-15
production_release_date: null
last_updated: 2026-09-11
---

# LT-94111: Riso available classroom selection

## Summary

For Riso lesson upsert, classroom selection must expose only rooms available at the lesson's location and time, sort them deterministically, and clear a stale choice when the availability inputs change. The feature also makes Classroom required for Riso, adds a Sequence sort key, and requires Save-time prevention of duplicate/overlapping assignments. It applies to 13 confirmed Lesson and Calendar entry points across SF and BO; each entry point requires a dedicated test case. AC 01.6 auto-assignment remains deferred until LT-102507 is implemented.

The [Confluence PRD](https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2121531393/Riso+Core+Enable+only+available+classroom+on+Lesson+upsert+form) is the primary source. Jira provides only the objective and links to the PRD; the legacy Classroom page is reference-only.

---

## Acceptance Criteria

### US 01 — Select only an available classroom

| ID | Feature | Requirement |
|---|---|---|
| AC 01.1 | Classroom — New field | `Sequence` is optional. When supplied, it accepts a positive integer only; duplicate values are allowed. |
| AC 01.2 | One-time availability | Before Location and full lesson date/time are defined, Classroom shows No option. Afterwards, apply the PRD's Classroom vacant/occupied checks at Japan local time (JPT/JST, UTC+09:00); sort by Sequence ASC, Classroom Name ASC, then created date ASC; prefill the first option. With no vacancy, leave Classroom unselected and show No option in search. |
| AC 01.3 | Classroom reset | Changing Location, lesson date, start time, or end time resets Classroom to blank. The user must select a new Classroom; the vacant first classroom is suggested only when the user opens the field. |
| AC 01.4 | Recurrence scope | A weekly recurring lesson can save even when following occurrences would use an occupied classroom; availability is evaluated only for the selected/first lesson datetime. Apply this rule to every confirmed entry-point flow. |
| AC 01.5 | Riso requiredness | Classroom is required for Riso and remains optional in Core. PT Teacher is the only confirmed role that cannot edit Classroom. |
| AC 01.6 | Create auto-assignment | **Testing later — deferred until [LT-102507](https://manabie.atlassian.net/browse/LT-102507) is implemented.** That planned epic defines auto-assignment only after Location and date/time are set with no overlap; it selects the lowest-Sequence Private classroom and remains user-editable. |

### US 02 — Prevent duplicate assignment from concurrent users

| ID | Feature | Requirement |
|---|---|---|
| AC 02.1 | Overlap/duplicate validation | On Save, validate the Classroom + Location + date/time for overlap or duplication. Reject the Save on conflict and show: `<Classroom name> is already in use for another class.` Japanese: `<Classroom name>は既に他の授業で利用されています`. |

### User-confirmed entry-point scope (2026-09-09)

The available-classroom behavior applies to all flows below. Phase 3 must create **at least one dedicated test case per flow**, with its own entry point and expected field state; reusable setup is allowed, but a generic case cannot substitute for a flow-specific case. For an input that a flow locks or does not expose, the case must assert that constraint rather than attempt an inapplicable reset.

| # | Area | Flow | Minimum coverage focus |
|---:|---|---|---|
| 1 | Lesson | New Lesson on Lesson List SF | Availability, ordering, requiredness, Save overlap rejection |
| 2 | Lesson | Edit Lesson on SF | Existing selection, reset after editable availability inputs, Save overlap rejection |
| 3 | Lesson | Add Lesson in Lesson Schedule Detail | Availability and Save overlap rejection for the added lesson |
| 4 | Lesson | Extend Recurrence in Lesson Schedule Detail | Classroom field state and first/new-instance availability scope; assert locked inputs where applicable |
| 5 | Lesson | Duplicate Lesson on SF | Prefilled Classroom re-evaluation, reset/availability, Save overlap rejection |
| 6 | Lesson | Edit Lesson on BO | Classroom field/editability and Riso-required/overlap behavior |
| 7 | Calendar | New Lesson on Calendar SF | Availability, ordering, requiredness, Save overlap rejection |
| 8 | Calendar | New Lesson by DnD | Entry-point availability or locked-field behavior, plus post-action conflict protection |
| 9 | Calendar | Edit Lesson by DnD | Date/time change re-evaluation or locked-field behavior, plus post-action conflict protection |
| 10 | Calendar | New Lesson by Available Teacher Calendar | Availability, ordering, requiredness, Save overlap rejection |
| 11 | Calendar | Edit Lesson on Calendar SF | Existing selection, reset after editable availability inputs, Save overlap rejection |
| 12 | Calendar | Duplicate Lesson on Calendar SF | Prefilled Classroom re-evaluation, reset/availability, Save overlap rejection |
| 13 | Calendar | Edit Lesson on Calendar BO | Classroom field/editability and Riso-required/overlap behavior |

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---:|---|---|---|---|---|
| 1 | AC 01.1 | Sequence is optional; supplied values are positive integers only; duplicate values are allowed. | Classroom Sequence | Optional positive integer | SF |
| 2 | AC 01.2 | Do not offer a room until Location, date, start, and end are defined. | Classroom | Locked/no option before prerequisites | SF / BO |
| 3 | AC 01.2 | Only classrooms passing the PRD vacant/occupied checks at the selected Japan-local date/time are selectable. | Classroom | Filtered using JPT/JST | SF / BO |
| 4 | AC 01.2 | Exact time match is occupied and hidden. | Availability | Computed | SF |
| 5 | AC 01.2 | Same start with a different end is occupied and hidden. | Availability | Computed | SF |
| 6 | AC 01.2 | Different start with the same end is occupied and hidden. | Availability | Computed | SF |
| 7 | AC 01.2 | A room occupied within the selected time period is hidden. | Availability | Computed | SF |
| 8 | AC 01.2 | Sort available rooms by Sequence, Name, then created date, ascending. | Classroom list | Auto-calculated sort | SF |
| 9 | AC 01.2 | Prefill the first available sorted room; every confirmed editable role except PT Teacher can adjust it. | Classroom | Auto-calculated then editable | SF / BO |
| 10 | AC 01.2 | With no vacancy, keep no selection and show No option. | Classroom | Empty state | SF |
| 11 | AC 01.3 | Location change resets Classroom to blank; user manually reselects after opening the field. | Classroom | Reset to blank | SF / BO |
| 12 | AC 01.3 | Date/start/end change resets Classroom to blank; user manually reselects after opening the field. | Classroom | Reset to blank | SF / BO |
| 13 | AC 01.4 | Check availability only at the selected/first weekly occurrence across every confirmed flow. | Availability | Computed recurrence scope | SF / BO |
| 14 | AC 01.5 | Classroom is required in Riso and optional in Core; PT Teacher cannot edit it. | Classroom | Organization- and role-gated | SF / BO |
| 15 | AC 01.6 | Testing deferred until LT-102507; its planned behavior auto-assigns the lowest-Sequence available Private room only after Location/date/time are set with no overlap. | Classroom | Deferred; planned auto-calculated then editable | SF |
| 16 | AC 02.1 | Reject an overlapping/duplicate Classroom Save and show the exact PRD EN/JP errors. | Save validation | Blocking validation | SF / BO |
| 17 | User-confirmed scope | Apply available-classroom behavior to all 13 named Lesson/Calendar entry points; design one dedicated case per flow. | Classroom availability / Save validation | In scope per flow; AC 01.6 deferred | SF / BO |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---:|---|---|---|---|
| 1 | [EXTENDED] | Jira LT-102507 | AC 01.6 | AC 01.6 testing is deliberately deferred. LT-102507 resolves the trigger as Location plus date/time with no overlap before Private-room auto-assignment. |
| 2 | [EXTENDED] | PRD AC 01.2 + confirmed clarification | AC 01.2 | Use the PRD Classroom vacant/occupied checks and Japan-local time (JPT/JST) as the availability oracle. |
| 3 | [EXTENDED] | Confirmed clarification | AC 01.4 | Selected/first-occurrence-only availability applies to every confirmed entry-point flow. |
| 4 | [REPLACED] | Confirmed clarification | AC 02.1 | Use the PRD English and Japanese error copy; do not use LT-102507's alternate English text as this suite's oracle. |
| 5 | [EXTENDED] | User-confirmed scope, 2026-09-09 | Scope | All 13 named Lesson and Calendar upsert flows, including BO flows, are in scope and need their own test case. |

### Missing in Requirements

| # | Tag | Source | Description |
|---:|---|---|---|
| 1 | [MISSING BEHAVIOR] | PRD AC 01.1 + confirmed clarification | Sequence is optional, but the PRD does not prescribe where blank Sequence ranks; do not assert a blank-value rank until confirmed. |
| 2 | [RESOLVED 2026-09-11] | PRD AC 01.2 + code-review finding + user confirmation | Previously flagged as missing a lesson-status inclusion/exclusion matrix. Source code review (`GetLessonData.cls`) confirmed only `Cancelled` is excluded from the occupied check — Draft, Published, and Completed lessons all occupy a Classroom. User confirmed on 2026-09-11 that since the PRD defines no status exclusion, this all-non-Cancelled-statuses-occupy behavior is the intended oracle. Four dedicated status cases (Draft/Published/Completed occupy; Cancelled does not) are added to `classroom-sequence-and-availability.md`. |

### Lesson-Learned Risks

No historical incident met the required entity-and-operation match. All five scheduling lesson-learned incidents concern Student Session/LA assignment, deletion, or bulk writes rather than Classroom availability selection or overlap validation.

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-02 | Recurring Lesson — Create, Edit Chain, Delete, Calendar Drag | It exercises recurrence/date-time edits but has no Classroom reset or availability assertion. | CREATE a Riso classroom-selection E2E scenario; keep E2E-02 as a recurrence regression reference. |

### Assumptions Made

- The Confluence PRD is authoritative where it differs from the short Jira description and LT-102507 error-copy variant.
- All 13 user-provided SF and BO Lesson/Calendar entry points are in scope; PT Teacher is the only confirmed non-editable role.
- Sequence stays optional. If blank, its rank relative to positive Sequence values is intentionally not asserted until confirmed.
- Availability cases use Japan local time (JPT/JST, UTC+09:00). Status-specific inclusion/exclusion is intentionally not asserted until confirmed.
- Strike-through text in the PRD is treated as superseded, so the active AC 02.1 Save validation is used.
- No Figma URL/design is linked in Jira, the PRD, or the two reference pages.

---

## Clarification Questions

All review questions were resolved by the user on 2026-09-09. The decisions are incorporated in the Acceptance Criteria and Business Rules above.

> Not posted to Jira, per user instruction.

### Code-review risk findings — decisions (2026-09-11)

A source-code review of `erp-salesforce` (Apex/LWC) surfaced additional risks beyond the original AC gaps. User decisions on 2026-09-11:

| # | Finding | Decision | Action |
|---:|---|---|---|
| 1 | Recurring lessons: occurrences 2+ get no vacancy check at all (`CreateLessonBatchable.cls` copies the first-occurrence Classroom to every later occurrence with no re-query). | **Confirmed intended.** PdM confirmed only the first/selected occurrence needs validation — matches existing AC 01.4 / Business Rule 13. | No spec change; no new test case (already covered by AC 01.4 cases in `classroom-reset-and-recurrence.md`). |
| 2 | Vacancy check converts the entered date/time using the logged-in user's own Salesforce profile timezone (`@salesforce/i18n/timeZone`), not a hardcoded JST constant. | **Confirmed acceptable.** Users are expected to operate the Riso org in JST. | No spec change; no new test case. |
| 3 | No database-level safeguard (validation rule/trigger/unique index) against two concurrent Saves double-booking a Classroom. | Bug ticket already created by the user. | Tracked outside this spec; `classroom-save-concurrency.md` cases already assert the expected (currently unmet) blocking behavior. |
| 4 | Changing Location fires two overlapping async availability calls (`handleOnChangeField` + `afterChangeFormField`); no request-ordering/sequence guard exists in `formLesson.js` or `lookupClassroomOnLesson.js`, so a stale response can render after a newer one. | **New test case requested.** | Added: `classroom-reset-and-recurrence.md` — "Location then time changed quickly" case. |
| 5 | The occupied-classroom query re-runs on every field edit with no debounce and no lower time bound. | **New test case requested.** | Added: `classroom-reset-and-recurrence.md` — "Repeated rapid time edits" case. |
| 6 | Only `Cancelled` status is excluded from the occupied check; Draft/Published/Completed all block a Classroom. | **Confirmed intended** — see Conflict & Gap Analysis → Missing in Requirements #2. Cover the full status matrix, not just Draft. | Added: `classroom-sequence-and-availability.md` — one case per status (Draft/Published/Completed occupy; Cancelled does not). |

> Not posted to Jira, per user instruction (consistent with the 2026-09-09 clarifications).

## Related Specs

- `epics/OOP/riso/LT-98512-classroom-reassignment-student/spec.md` — Riso classroom eligibility, sequence ordering, and clash semantics.
- `epics/calendar/LT-XXXX-drag-drop-edit-lesson-time/spec.md` — Calendar date/time editing regression surface.
- `epics/lesson/LT-101769-lesson-popup-ui/test-cases/sf-create-lesson-ui.md` — Lesson upsert UI baseline; noted for detailed regression review.

## Related Test Cases

- `epics/OOP/riso/LT-98512-classroom-reassignment-student/test-cases/clash-and-failure-handling.md` — existing classroom clash assertions.
- `epics/OOP/riso/LT-98512-classroom-reassignment-student/test-cases/assignment-rules.md` — existing lowest-sequence Riso assignment strategy.

## QASE Coverage Gaps

- Qase project `PX`, suite `3480` is linked to LT-94111 and currently contains 0 cases.
- New coverage is needed for AC 01.1–01.5 and AC 02.1: the negative/boundary overlap matrix, reset flows, recurrence scope, tenant-requiredness, and concurrent Save rejection.
- The approved minimum is **13 new flow-specific cases**, one for each entry point in the User-confirmed entry-point scope matrix; Phase 3 may add shared-boundary cases beyond this minimum.
- **AC 01.6 is excluded from this suite for now and must be designed/tested after LT-102507 is implemented.**
