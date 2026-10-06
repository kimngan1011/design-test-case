---
ticket_id: LT-108376
ticket_url: https://manabie.atlassian.net/browse/LT-108376
title: Add "Not Started" option as default in student filter in Lesson Calendar
module: scheduling
bucket: calendar
status: Ready for Development
internal_uat_date: 2026-10-19
production_release_date: 2026-11-02
last_updated: 2026-10-07
---

# LT-108376: Add "Not Started" option as default in student filter in Lesson Calendar

## Summary

On the Salesforce Lesson Calendar, the Student list (left panel) filter **Student Course Status** currently defaults to **Active** only. Staff cannot see students whose Lesson Allocation (LA) was newly ordered with a future start date. The default changes to **Active + Not Started**, aligned with the Student detail > Course tab where "Active" means Active + Future. Lesson Master keeps the Active-only default.

**Sources:** Jira LT-108376 (epic), PBT-3079 (+ attachment `image-20260417-073947.png`), child LT-108377 [SF] (Done), QA task LT-112367. No Confluence / Figma. Behavior details below come from erp-salesforce code and QA-owner confirmations (2026-10-07).

---

## Acceptance Criteria

### US1 — Lesson Calendar student filter default includes Not Started

| AC | Description |
|---|---|
| AC-01 | Lesson Calendar > Student list > Filter > Student Course Status: default changes from "Active" only to "Active" and "Not Started". |
| AC-02 (derived from Background) | Students whose LA starts in the future (newly ordered) are visible in the Lesson Calendar Student list without changing the filter — consistent with Student detail > Course tab "Active" (= Active + Future). |

**Mockup (PBT-3079 attachment):** filter popover opened from the funnel icon on the Student panel — Location (calendar location chip, not removable), Academic Year (current AY pre-selected), Type (Regular / Seasonal / Trial pre-selected), **Student Course Status (Active ×, Not Started ×)**, Package Type, Course Master, … ; footer Reset / Save.

### Status definition (from code — `LessonMasterHandler.getListAssignStudent`)

| Status | Condition on LA | Default selected |
|---|---|---|
| Active | Start Date Time ≤ TODAY **and** End Date Time ≥ TODAY | ✅ |
| Not Started | Start Date Time > TODAY | ✅ (new) |
| Inactive | End Date Time < TODAY | ❌ |

Multiple statuses are OR-combined; empty selection = no status condition. `TODAY` = Salesforce date literal in the logged-in user's timezone (see Q3).

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---|---|---|---|---|---|
| BR-01 | AC-01 | On first load of Lesson Calendar, Student Course Status filter is pre-selected with Active AND Not Started. | Student Course Status | editable (default value) | [SF] |
| BR-02 | AC-01 | Inactive is NOT pre-selected by default. | Student Course Status | editable | [SF] |
| BR-03 | AC-02 | Default list includes students with an LA where Start Date <= today <= End Date (Active). | Student list | auto-calculated | [SF] |
| BR-04 | AC-02 | Default list includes students with an LA whose Start Date > today (Not Started / future-ordered LA). | Student list | auto-calculated | [SF] |
| BR-05 | AC-02 | Default list excludes students whose only LA ended before today (Inactive). | Student list | auto-calculated | [SF] |
| BR-06 | AC-02 | Boundary: LA starting today is Active (shown); LA starting tomorrow is Not Started (shown); LA ending today is Active (shown); LA ended yesterday is Inactive (hidden by default). 'Today' evaluated in the running user's timezone (SOQL TODAY). ASSUMPTION (accepted by QA owner 2026-10-07, pending PO answer Q3): test against current code behavior — date-level comparison, user timezone. | LA Start/End Date Time | auto-calculated | [SF] |
| BR-07 | AC-01 | Staff can deselect Not Started → list returns to Active-only results (as-is behaviour). | Student Course Status | editable | [SF] |
| BR-08 | AC-01 | Staff can deselect Active keeping only Not Started → only future-LA students shown. | Student Course Status | editable | [SF] |
| BR-09 | AC-01 | Staff can add Inactive → Active + Not Started + Inactive OR-combined. | Student Course Status | editable | [SF] |
| BR-10 | AC-01 | Default Student Course Status combines (AND) with other student filters (Location, Type, Course, Class, Grade, School, Student Classification, Package Type) and keyword search. | Student filter | editable | [SF] |
| BR-11 | AC-01 (code + user confirmation) | Reset in filter popover clears ALL filters (incl. Student Course Status, Academic Year, Type) except the calendar location — confirmed by user 2026-10-07. Student Course Status becomes empty = all statuses incl. Inactive. | Reset button | editable | [SF] |
| BR-12 | AC-01 (code) | Reloading/reopening Lesson Calendar restores default Active + Not Started (no persistence across page loads). | Student Course Status | default | [SF] |
| BR-13 | scope (code) | Lesson Master student list keeps default Active only (unchanged). | Student Course Status (Lesson Master) | default | [SF] |
| BR-14 | AC-02 | A student with both an Inactive LA and a Not Started LA appears by default (via the Not Started LA). | Student list | auto-calculated | [SF] |
| BR-15 | AC-02 | Filter chip/label shows both 'Active' and 'Not Started' in EN and JP. | Filter chips | locked (label) | [SF] |
| BR-16 | undocumented (commit) | Additional Fields on Create/Edit Lesson form (and Lesson Schedule form) appear right after the notes textarea instead of near the bottom (bundled change). — OUT OF GENERATED TCs: QA owner tests manually. | Additional Fields section | layout | [SF] |
| BR-17 | AC-01 (image PBT-3079) | Default chips 'Active' and 'Not Started' are shown in the Student Course Status field of the filter popover, each removable with ×; order Active then Not Started. | Student Course Status chips | editable | [SF] |
| BR-18 | AC-01 (confirmed by user 2026-10-07) | The student list (and its 'N items' count) on first load already reflects Active + Not Started without the user opening the filter or clicking Save. | Student list / item count | auto-calculated | [SF] |
| BR-19 | existing default (user confirmation) | Academic Year filter default = current Academic Year (the AY whose date range contains today) — must stay pre-selected together with the new Student Course Status default. | Academic Year | editable (default value) | [SF] |
| BR-20 | existing default (user confirmation, PX-4637) | Type filter default = all LA types selected (Regular, Seasonal, Trial) — unchanged. | Type | editable (default value) | [SF] |
| BR-21 | AC-02 x BR-19 | Default list = Course Status (Active OR Not Started) AND current AY AND all types AND calendar location. A Not Started LA belonging to the NEXT academic year is therefore NOT shown by default. | Student list | auto-calculated | [SF] |
| BR-22 | AC-01 (user confirmation 2026-10-07) | Changing calendar location or switching view (Daily/Weekly/…) keeps the user's current Student Course Status (and other filter) selection — only the Location chip changes to the new calendar location; the default is NOT re-applied. | Student filter | editable (retained) | [SF] |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description | Status |
|---|---|---|---|---|---|
| F-01 | [REPLACED] | Qase PX-4639 / erp-salesforce listStudentCalendar.js:29 | AC-01 | Default changes from ['Active'] to ['Active','Not Started'] on Lesson Calendar. | Open |
| F-02 | [REGRESSION RISK] | Qase PX-4639 (suite 483) | AC-01 | Existing case asserts Active-only default → will fail after release; must be updated, not duplicated. | DONE — PX-4639 updated in Qase 2026-10-07 (backup in scratchpad) |
| F-03 | [CONFLICT] | Qase PX-13084 last step | BR-11 | Code (popoverFilterStudentListLessonMaster.handleReset → all [] except location) and user confirmation (Reset clears everything) contradict PX-13084, which expects Reset to restore defaults. PX-4653 matches code. | DONE — PX-13084 step 5 updated in Qase 2026-10-07: Reset + Save clears all except location |

### Missing in Requirements

| # | Tag | Source | Description | Status |
|---|---|---|---|---|
| F-05 | [MISSING BEHAVIOR] → resolved (by design) | temp/business_rules.json BR-21 | Background says users cannot see newly ordered future LAs. A future LA in the NEXT academic year (e.g. order in Feb/Mar for April start in JP) is still hidden by the AY default — the business problem is only partly solved. Not addressed in ticket. | Confirmed by user — keep as clarification question to PO |
| F-06 | [MISSING BEHAVIOR] → resolved (expected) | erp-salesforce LessonMasterHandler.getListAssignStudent (FROM Lesson_Allocation__c, one resultItem per LA) | A student with an Active LA and a Not Started LA (e.g. Change Associated Course with future effective date — PX-1774; Add Associated Course future date — PX-1775) now appears TWICE in the default list (one row per LA, each with its own allocated count). Ticket does not say whether this is expected. | Covered by existing PX-1774 / PX-1775 — add both to the epic test run (user 2026-10-07) |
| F-12 | [MISSING BEHAVIOR] | temp/business_rules.json BR-06 | Status boundary uses date-level TODAY in user's timezone while LA Start/End are DateTime. LA starting today 10:00 → Active even before 10:00; staff in a different timezone from the location may see a different split. Not defined. | Accept current code behavior for testing; ask PO (Q3) |
| F-13 | [MISSING BEHAVIOR] | erp-salesforce listStudentCalendar (no persistence) | Not specified whether the user's own selection persists when switching Daily/Weekly view, changing calendar location, or navigating dates. | RESOLVED — selection retained on location/view change; only Location chip changes (BR-22) |
| F-08 | [UNDOCUMENTED IN AC] | erp-salesforce commit 2774d05917 / 7c0d556f46 (formLessonNewLayout.html, formLessonOnLessonScheduleNewLayout.html) | Same commit moves Additional Fields from the end of the 'Location & Course' subsection (after Cancellation Reason, before Bookable Flag) to the end of the 'Basic Information' subsection (right after Lesson Note). Applies to Lesson form and Lesson Schedule form. Only visible when LessonFeatureToggles.isEnableAdditionalField() is ON and Additional_Field_Setting__mdt has active Lesson fields. No ticket covers it; no Qase case found for Lesson-form Additional Fields. | User will test manually — out of generated test cases |
| F-14 | [ROLE GAP] | temp/raw_requirement.json roles | No distinction between HQ (full_access) and Centre staff (center_level_edit); behavior assumed identical. | Confirmed by user — HQ and CM identical |

### Other findings (no question)

| # | Tag | Description | Status |
|---|---|---|---|
| F-04 | [EXTENDED] | New Course Status default co-exists with existing AY (current AY) and Type (all) defaults; list = AND of all defaults. | — |
| F-11 | [EXTENDED] | Lesson Master student list keeps Active-only default. | Confirmed by user |
| F-09 | [REGRESSION RISK] | Feature was reverted because it shipped without a feature flag; re-apply is identical (still no flag). Unknown which build is on staging; Jira LT-108377 = Done while code is not on develop. | Out of QA concern — test that the epic works |
| F-10 | [EXTENDED] | Bulk Publish scope comes from students CHECKED in the list, not from Course Status. Impact is indirect: the header 'select all' now also checks Not Started students → their Draft lessons in the period get published and they/parents get the bulk notification. | NOT APPLICABLE — user: Bulk Publish uses students selected in the calendar GRID filter, not the left Student List |

### Lesson-Learned Risks

| # | Incident | Date | AC | Risk | Guardrail |
|---|---|---|---|---|---|
| 1 | Core — Infinite-Scroll / Paged Lists Stop at ~2,000 Rows (SOQL OFFSET Limit) — notes SF calendar Student List shows first 200 rows by design | 2026-09-29 | AC-02 | At a dense location, adding Not Started LAs can push Active students whose phonetic names sort late beyond row 200 — they silently disappear from the default list (no 'more rows' message), i.e. the change can HIDE active students it was meant to complement. | Test with a location having > 200 LA rows (Active + Not Started) under the current AY: verify the item count, whether an Active student beyond row 200 is still reachable via keyword search, and ask whether the 200 cap is acceptable with the larger default. |
| 2 | Core — Teacher List Filter Fails Silently When Subject + Location + Working Time Are Combined (SOQL 2 Semi-Join Limit) | 2026-09-29 | AC-02 | An empty student list after the default change could mean 'no match' or a silent API error; QA cannot tell from the UI. | When verifying default/combined filters, check getListAssignStudent Aura response state = SUCCESS in DevTools; combine Course Status + Class + Location (2 semi-joins) + Student Classification. |

> Risk #1 (200-row window) is a known Salesforce limitation accepted by the team (QA owner, 2026-10-07) — no question raised.

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-28 | Assign Student — Calendar, BO Platforms & Mobile Verification | Default Student list now also contains Not Started students | UPDATE (note only) |

### Assumptions Made

- Status boundary follows current code (date-only, user timezone) until PO answers Q3.
- Reset clears every filter except the calendar location (Academic Year, Type, Student Course Status become empty) — confirmed by QA owner; matches Qase PX-4653.
- Student list and "N items" count already reflect Active + Not Started on first load, without opening the filter — confirmed.
- Changing calendar location or view keeps the current filter selection; only the Location chip changes — confirmed.
- Academic Year default = current AY; Type default = all types (Regular, Seasonal, Trial) — unchanged, confirmed.
- Lesson Master Student list keeps Active-only default; HQ and CM behave the same — confirmed.
- Additional Fields position change on Create/Edit Lesson + Lesson Schedule forms (bundled in commit 2774d05917) is tested manually by QA owner — not in generated test cases.
- Bulk Publish "Apply to selected students" uses students selected in the calendar grid filter, not this Student list — out of scope.

---

## Clarification Questions

1. ~~**[MISSING BEHAVIOR]** Next-academic-year future LA hidden by the current-AY default~~
   ✅ **Resolved (QA owner, 2026-10-07):** expected by design — the Academic Year filter scopes the list, so an LA of the next AY is only shown when that AY is selected. Not a gap.

2. ~~**[MISSING BEHAVIOR]** Student with an Active LA and a Not Started LA shows two rows~~
   ✅ **Resolved (QA owner, 2026-10-07):** correct — rows are per LA; different LAs = different rows. No uniqueness check on student name.

3. **[MISSING BEHAVIOR]** The ticket does not define how 'Active' and 'Not Started' are decided. The current implementation compares the LA Start/End Date Time with Salesforce TODAY — date only (no time), in the logged-in user's timezone: Active = Start ≤ today ≤ End; Not Started = Start > today; Inactive = End < today. As a result: (a) an LA that starts later today (e.g. 18:00) is already Active from 00:00 today; (b) an LA that ends today stays Active for the whole day; (c) a staff user whose Salesforce timezone differs from the location's timezone (e.g. GMT+7 vs JST) may see a different status around midnight. Can you confirm this date-only, user-timezone rule is intended? If not, which reference should be used — the location's timezone, or the exact date and time?
   _Evidence: LT-108376 / PBT-3079 — only 'Active' and 'Not Started' named, no rule given; erp-salesforce LessonMasterHandler.getListAssignStudent — SOQL TODAY (running user's timezone)_
   > ⏳ Handled by QA owner directly (not posted by the pipeline). Test cases follow current code behavior until answered.

---

## Related Specs

- `epics/calendar/LT-111303-static-student-panel-divider/spec.md` — same Student panel; filters must keep working.
- `epics/calendar/LT-98532-bulk-publish-lessons-by-student/spec.md` — reviewed; not impacted (uses calendar grid student filter).

## Related Test Cases (Qase PX)

- Suite 483 "Student Filter" (parent 469 "Student list"):
  - **PX-4639** Student course status filter — default — ✅ updated 2026-10-07 to Active + Not Started.
  - **PX-13084** AY filter … reset — ✅ step 5 updated 2026-10-07 (Reset + Save clears all except location).
  - PX-4640 (select statuses), PX-4653 (Reset), PX-13083 (current AY default), PX-4637 (LA type default), PX-4652 (combined filters), PX-4631 / PX-4632 (view / search) — regression.
- Suite 2573 "Change Associated Course": **PX-1774** (future effective date → old LA Active + new LA Not Started); **PX-1775** Add Associated Course future effective date — include in the epic test run.

## Qase Import (2026-10-07)

- Suite **3698** "Lesson Calendar – Student List – Student Course Status Default (LT-108376)" under suite 483 — https://app.qase.io/project/PX?suite=3698
- New cases: **PX-29506 → PX-29522** (17)
- Test run **3658** — https://app.qase.io/run/PX/dashboard/3658 — 21 cases: PX-29506..29522 + PX-1774, PX-1775, PX-4639, PX-13084

## QASE Coverage Gaps

- AC-01 — Not Started default chip present on first load; Inactive not pre-selected; list/count on load.
- AC-02 — date boundaries (start today / tomorrow, end today / yesterday); future LA in next AY hidden until that AY is selected; student with Active + Not Started LAs shows one row per LA.
- BR-07..BR-10 — deselect Not Started / only Not Started / add Inactive / combine with other filters + keyword search.
- BR-13 — Lesson Master keeps Active-only default.
- BR-22 — selection retained after changing location / view.
- BR-12 — reload restores default.
