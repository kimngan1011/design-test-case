---
ticket_id: LT-98530
ticket_url: https://manabie.atlassian.net/browse/LT-98530
title: "[Riso] OOP | Contract and Monthly Lesson history (App)"
module: scheduling/lesson-management
bucket: OOP/riso
status: Ready for QA
internal_uat_date: 2026-08-24
production_release_date: 2026-09-07
last_updated: 2026-07-27
---

# LT-98530: [Riso] OOP | Contract and Monthly Lesson history (App)

## Summary

This ticket adds two new read-only pages to the Riso Learner App (student/parent facing): a **Contract Info** page showing all of a student's active Lesson Allocations (LAs) for the current Academic Year with a month-selectable Total Slot / Lesson Allocated count, and a **Monthly Lesson History** page listing completed lessons per month with date/time/subject/teacher/attendance detail. The Jira ticket itself carries no inline AC — all requirements were sourced from the linked Confluence PRD (2130575378) and cross-referenced against Figma and the original background RFP (No.445), per explicit instruction to focus on the PRD as the source of truth.

The underlying data (Riso Contract records, LA aggregation) is created by a separate API ticket (LT-98533) and also surfaced read-only on SF via a sibling ticket (LT-98531). Several calculation rules in this PRD do not agree with those two sibling specs — see Conflict & Gap Analysis below.

---

## Acceptance Criteria

### US 01 (PRD: US 01A) — Contract Page
**As a** student or parent, **I want** to view all my contracts when logging in the app **so that** I can keep track of my/my child's learning history.

| ID | Feature | Acceptance Criteria |
|---|---|---|
| AC01.1 | Contract Info under User profile | Header unchanged (student icon + full name, edit icon). Section header "Contract Info"/"契約情報". Month selector (year-month dropdown, EN "MM YYYY" / JP "YYYY年MM月", default = last month of current AY). Info banner re: data update timing. Body = LA list filtered to `require_allocation = TRUE` AND `Academic Year = Current AY`. Each LA card shows Course Master Name (via Location Course → Course Master), Academic Year & Location, Total Slot (契約数) and Lesson Allocated (授業設定数) for the selected month. Sort: LA start date ASC → end date ASC → created_at ASC. |
| AC01.2 | Calculate the Total Slot and Lesson Allocated | Total Slot = SUM of related Riso Contracts' slot numbers: Monthly type → Monthly Slot × elapsed months (Start Month→Selected Month); Seasonal type → full slot if Start Date(month) ≤ Selected Month(EOM) else 0. Lesson Allocated = count of Student Sessions where Lesson Date is within AY AND ≤ EOM of selected month AND Lesson Status is NOT Cancelled, EXCLUDING sessions where Attendance = Absent AND Notice is NOT "In Advance". Same calc as PBT-1510. Ref: Riso \| OOP \| RISO Contract API (POST/PATCH) (LT-98533). |

### US 02 (PRD: US 01B) — Lesson History
**As a** student or parent, **I want** to view my/my child's lesson history by month **so that** I can review what lessons have already taken place and stay informed about attendance.

| ID | Feature | Acceptance Criteria |
|---|---|---|
| AC02.1 | Lesson History view page | Page menu "Lesson History". Month Navigator defaults to "THIS month" (EN "month year" / JP "YYYY年MM月"), back/next navigation, "No data" UI if no completed lessons. List = all lessons student is allocated to, Status = Completed (see Conflict #3 — PRD carries its own unresolved "TBC → Cancelled" comment on this filter), Lesson Date(month) = selected month, sorted by Lesson start time ASC. Each row: Lesson Date (EN "Oct 1"-style / JP "10/1" + day of week), Lesson Time (start-end + line-break + Timeslot Name, blank if none), Subject (blank if none), Teacher full name(s) comma-separated (blank if none), Attendance status + Notice on new line if present. |

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---|----|----|---|---|---|
| BR-01 | AC01.1 | Header unchanged: student icon + full name | header | locked | app |
| BR-02 | AC01.1 | Edit icon edits student full name | full_name | editable | app |
| BR-03 | AC01.1 | Section header label "Contract Info"/"契約情報" | section_header | locked | app |
| BR-04 | AC01.1 | Month selector: year-month dropdown, EN "MM YYYY" / JP "YYYY年MM月" | month_selector | editable | app |
| BR-05 | AC01.1 | Month selector default = last month of current AY | month_selector | auto-calculated | app |
| BR-06 | AC01.1 | Info banner re: data update timing displayed | info_banner | locked | app |
| BR-07 | AC01.1 | LA list filtered to require_allocation = TRUE | la_list | computed | app |
| BR-08 | AC01.1 | LA list filtered to Academic Year = Current AY | la_list | computed | app |
| BR-09 | AC01.1 | Card shows Course Master Name via LA→Location Course→Course Master | course_master_name | auto-calculated | app |
| BR-10 | AC01.1 | Card shows Academic Year & Location | academic_year_location | auto-calculated | app |
| BR-11 | AC01.1/.2 | Card shows Total Slot (契約数) for selected month | total_slot | auto-calculated | app |
| BR-12 | AC01.1/.2 | Card shows Lesson Allocated (授業設定数) for selected month | lesson_allocated | auto-calculated | app |
| BR-13 | AC01.1 | Sort: LA start date ASC → end date ASC → created_at ASC | la_list | computed | app |
| BR-14 | AC01.2 | Total Slot = SUM of related Riso Contracts' slot numbers | total_slot | auto-calculated | app |
| BR-15 | AC01.2 | Monthly type: slot = Monthly Slot × elapsed months (Start Month→Selected Month) | total_slot | auto-calculated | app |
| BR-16 | AC01.2 | Seasonal type: full slot if Start(month) ≤ Selected(EOM) else 0 | total_slot | auto-calculated | app |
| BR-17 | GAP | [UNDOCUMENTED IN AC] Trial-type contract has no Total Slot rule (Figma shows a Trial card) | total_slot | auto-calculated | app |
| BR-18 | AC01.2 | Lesson Allocated: sessions with Lesson Date within AY | lesson_allocated | auto-calculated | app |
| BR-19 | AC01.2 | AND Lesson Date ≤ EOM of selected month | lesson_allocated | auto-calculated | app |
| BR-20 | AC01.2 | AND Lesson Status is NOT Cancelled | lesson_allocated | auto-calculated | app |
| BR-21 | AC01.2 | EXCLUDE Absent AND Notice NOT "In Advance" | lesson_allocated | auto-calculated | app |
| BR-22 | AC01.2 (note) | Absent+InAdvance does not consume lesson count | lesson_allocated | auto-calculated | app |
| BR-23 | AC01.2 (cross-ref) | Same calc as PBT-1510 (sibling report) | lesson_allocated | auto-calculated | app |
| BR-24 | AC02.1 | Page menu label "Lesson History" | page_menu | locked | app |
| BR-25 | AC02.1 | Month Navigator defaults to "THIS month" | month_navigator | auto-calculated | app |
| BR-26 | AC02.1 | Navigator format EN "month year" / JP "YYYY年MM月" | month_navigator | locked | app |
| BR-27 | AC02.1 | User can navigate back/next by month | month_navigator | editable | app |
| BR-28 | AC02.1 | "No data" UI if selected month has no completed lessons | lesson_history_list | computed | app |
| BR-29 | AC02.1 | [CONFLICT/TBC] List = lessons with Status = Completed (PRD's own inline comment marks this "TBC → Cancelled") | lesson_history_list | computed | app |
| BR-30 | AC02.1 | AND Lesson Date(month) = selected month | lesson_history_list | computed | app |
| BR-31 | AC02.1 | Sort: Lesson start time ASC | lesson_history_list | computed | app |
| BR-32 | AC02.1 | Row: Lesson Date EN "Oct 1"-style / JP "mm/dd" + day of week | lesson_date | auto-calculated | app |
| BR-33 | AC02.1 | Row: Lesson Time "start-end" + line break + Timeslot Name (blank if none) | lesson_time | auto-calculated | app |
| BR-34 | AC02.1 | Row: Subject (blank if none) | subject | optional | app |
| BR-35 | AC02.1 | Row: Teacher name(s) comma-separated (blank if none) | teacher | optional | app |
| BR-36 | AC02.1 | Row: Attendance status + Notice on new line if present | attendance | auto-calculated | app |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---|---|---|---|---|
| 1 | [CONFLICT] | epics/OOP/riso/LT-98533-riso-contract-api/spec.md — LA Aggregation Rules / Additional Aggregation Notes | AC01.2 | AC01.2's month-prorated Total Slot formula for Monthly/Seasonal contracts contradicts LT-98533's flat `SUM(contract.total)` aggregation, which explicitly states monthly-type contracts are "not used for any slot calculation logic at this stage." Same conflict already flagged (unresolved) in sibling ticket LT-98531. |
| 2 | [CONFLICT] | epics/OOP/riso/LT-98533-riso-contract-api/spec.md (BR-31) + knowledge/domain-knowledge/scheduling/partner-rules/riso-lesson-allocation.md | AC01.2 | Contract.type enum is weekly/monthly/one-time (no "Seasonal"); "Seasonal" only exists as an LA.Type value on a different entity. AC01.2 conflates the two. |
| 3 | [CONFLICT] | epics/OOP/riso/LT-98531-riso-contract-lesson-report/spec.md, confirmed answer Q3 (2026-06-22) | AC01.2 | Sibling SF report confirmed it does NOT check lesson status (Cancelled not excluded) despite sharing "the same calculation as PBT-1510"; this ticket's AC01.2 DOES exclude Cancelled. |
| 4 | [CONFLICT] | Confluence PRD 2130575378 — unresolved inline comment on AC02.1 | AC02.1 | PRD's own inline comment marks the Lesson History status filter as "TBC → Cancelled" — unresolved by the PRD's own authors. |

### Missing in Requirements

| # | Tag | Source | Description |
|---|---|---|---|
| 1 | [UNDOCUMENTED IN AC] | Figma node 7592:1027 (体験授業 / Trial Lesson card) | No Total Slot calculation rule exists for Trial-type contracts/LAs, though Figma shows a Trial card with its own numbers. |
| 2 | [MISSING BEHAVIOR] | epics/OOP/riso/LT-98531-riso-contract-lesson-report/spec.md AC-01 (empty state defined there, absent here) | AC01.1 does not define the empty state when the LA list filter returns zero results. |
| 3 | [MISSING BEHAVIOR] | temp/business_rules.json BR-04/05 vs BR-08 | Month selector range vs. the LA list's hard "Current AY" filter is not reconciled — can the selector move outside the current AY? |
| 4 | [MISSING BEHAVIOR] | temp/business_rules.json BR-27 | Lesson History month navigator has no defined back/forward boundary. |
| 5 | [MISSING BEHAVIOR] | raw_requirement.json roles=[student, parent] | Multi-child parent account scoping for this new financial/contract-adjacent data is not explicitly re-confirmed (header reuse assumed). |
| 6 | [UNDOCUMENTED IN AC] | Figma node 7592:1027 (Contract Info card, month badge) | Figma shows a "時点の累計" ("cumulative as of this point") caption under the month/year badge that is not mentioned anywhere in AC01.1's text. Spec–Figma mismatch check (coverage Step H.1) surfaced this; per user instruction (2026-07-27), the PRD text remains primary for now and this is deferred for later review rather than blocking coverage/test-case generation. |

### Lesson-Learned Risks

| # | Incident | Date | AC | Risk | Guardrail |
|---|---|---|---|---|---|
| 1 | Nichibei — Student Sessions Missing LA → Points Not Deducted | 2026-03-04 | AC01.2 | Compound Attendance exclusion (Absent AND Notice != InAdvance) has a documented history of partial implementation in OOP flows causing silent miscalculation. | Test all 3 attendance combinations independently (Absent+InAdvance=INCLUDED, Absent+NoNotice=EXCLUDED, Present=INCLUDED); cross-check against LT-98531 AC-10's confirmed behavior. |

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-19 | Riso — Lesson Allocation & Subject in Detail | Scenario ends at "Student views the lesson on Learner App schedule" (step 11); does not extend into Contract Info or Lesson History pages. | UPDATE — add [Mobile] steps for Contract Info card verification + Lesson History completed-lesson verification. |

### Assumptions Made

- Bucket = `OOP/riso` (Riso-only OOP feature, per epic-folder-convention.md).
- Slug `contract-monthly-lesson-history-app` derived from Jira title, ≤6 words.
- `internal_uat_date` = 2026-08-24 (customfield_10566/10567); `production_release_date` = 2026-09-07 (fixVersion v2026.09.07).
- `status` = "Ready for QA" (Jira status verbatim).
- Per user instruction, the Confluence PRD (2130575378) was treated as the primary/authoritative requirement source over the near-empty Jira description.
- The 4 additional Confluence links posted in a Jira comment (Nichibei Point Consumption, [Riso] PM project management, Scheduling 2026 Q1/Q2 roadmaps) were reviewed by title only — not deep-read — as they are broader planning/roadmap documents, not feature-specific requirement sources. Available on request.
- Figma was fetched for the Contract page frame only (node 7592:1027); the Lesson History page design exists only as PRD screenshot attachments, not independently re-fetched via Figma MCP.

---

## Clarification Questions

1. **[CONFLICT]** AC01.2 defines 'Total Slot' with a month-prorated formula for Monthly contracts and an on/off formula for Seasonal contracts, but the authoritative Contract API spec (LT-98533) defines Contract.type as only weekly/monthly/one-time (no 'Seasonal'), with monthly-type contracts explicitly excluded from any slot-calculation logic today, and LA aggregation is a flat SUM. Is 'Total Slot' meant to be LA.Total_Session_Count as-is (flat sum), or a new app-specific calculation using the real Contract.type values? Please also map each real Contract.type to a Total Slot formula.
   _Evidence: `epics/OOP/riso/LT-98533-riso-contract-api/spec.md` — LA Aggregation Rules table + "Monthly type... not used for any slot calculation logic at this stage."_

2. **[CONFLICT]** AC01.2 excludes Cancelled-status lessons from Lesson Allocated; the sibling SF report (LT-98531), which shares "the same calculation as PBT-1510", was confirmed to NOT check lesson status at all. Should this App feature match the confirmed SF report behavior (drop the Cancelled exclusion), or is a deliberate divergence intended?
   _Evidence: `epics/OOP/riso/LT-98531-riso-contract-lesson-report/spec.md` — "Q3 confirmed: SF report does NOT check lesson status" vs this PRD's "AND Lesson Status is NOT Cancelled."_

3. **[CONFLICT]** AC02.1's Lesson History status filter carries the PRD's own unresolved inline comment: "Status = completed (TBC → Cancelled)". Please confirm definitively whether the filter is Status = Completed only.
   _Evidence: Confluence PRD 2130575378, AC02.1 inline comment; background RFP (Confluence 1424916482): "only completed lesson should be listed... to distinguish from lesson schedule."_

4. **[LESSON-LEARNED RISK]** Per the 2026-03-04 Nichibei incident (partial compound-condition implementation silently under-deducted points), can you confirm the Lesson Allocated compound Attendance rule (Absent AND Notice != In Advance) will be tested for all 3 attendance combinations and kept in sync with LT-98531's confirmed version of the same rule?
   _Evidence: `knowledge/domain-knowledge/scheduling/lesson-learned/oop.md`, 2026-03-04 entry._

5. **[UNDOCUMENTED IN AC]** Figma shows a '体験授業' (Trial Lesson) contract card with its own Total Slot/Lesson Allocated numbers, but AC01.2 defines calculation only for Monthly/Seasonal types. What is the Total Slot formula for Trial-type contracts?
   _Evidence: Figma file MX4KunRlKe4jneEZGgTqmR, node 7592:1027 (Trial Lesson card, 10/10)._

6. **[MISSING BEHAVIOR]** AC01.1 does not define the empty state when the LA list filter (require_allocation=TRUE AND Current AY) returns zero results. What should the Contract page show?
   _Evidence: `temp/business_rules.json` BR-07/BR-08; compare `epics/OOP/riso/LT-98531-riso-contract-lesson-report/spec.md` AC-01, which defines an empty state for its analogous list._

7. **[MISSING BEHAVIOR]** Can the Month selector on the Contract page move outside the current Academic Year, given the LA list itself is hard-filtered to "Current AY"?
   _Evidence: `temp/business_rules.json` BR-04/BR-05 vs BR-08._

8. **[MISSING BEHAVIOR]** Is Lesson History month navigation unbounded (with "No data" for out-of-range months), or bounded to a specific range (e.g. enrollment start through current month)?
   _Evidence: `temp/business_rules.json` BR-27 — no boundary defined._

9. **[MISSING BEHAVIOR]** For a parent linked to multiple children, please confirm both pages simply follow the existing (unchanged) profile header selector with no additional partner-specific restriction on this financial/contract-adjacent data.
   _Evidence: `temp/raw_requirement.json` roles=[student, parent]; AC01.1 says header is "No Change" but does not explicitly re-confirm multi-child scoping._

10. **[UNDOCUMENTED IN AC]** Figma shows a "時点の累計" ("cumulative as of this point") caption under the Contract page's month/year badge that AC01.1 never mentions. What is the intended EN/JP wording and placement of this caption, and is it in scope for this ticket?
    _Evidence: Figma file MX4KunRlKe4jneEZGgTqmR, node 7592:1027 (badge "2025年9月" + caption "時点の累計" directly beneath it); no corresponding text anywhere in AC01.1._

> **Note (2026-07-27):** Per user instruction, these questions are deferred — not yet posted to Jira, PRD text treated as primary source for now. Coverage/test-case generation proceeds using the PRD's stated rules, with disputed items (Q1-3, Q10) flagged as high-risk/pending-confirmation rather than blocking.
> Update this section after questions are posted to Jira:
> _(pending user approval — not yet posted)_

---

## Related Specs

- `epics/OOP/riso/LT-98533-riso-contract-api/spec.md` — Riso Contract API (POST/PATCH); the authoritative source for Contract.type enum and LA aggregation formulas that this ticket's AC01.2 conflicts with.
- `epics/OOP/riso/LT-98531-riso-contract-lesson-report/spec.md` — SF-side sibling read surface for the same Contract/LA data; shares (and diverges from) this ticket's Lesson Allocated calculation.
- `epics/OOP/riso/LT-92532-riso-create-update-la-on-ui/spec.md` — Riso manual LA creation; defines LA.Type (Regular/Seasonal/Trial), the field this PRD's contract-type terminology may be conflating with Contract.type.

## Related Test Cases

- `epics/OOP/riso/LT-98533-riso-contract-api/test-cases/la-aggregation-post.md` / `la-aggregation-patch.md` — assert the flat (non-prorated) aggregation formula this ticket's AC01.2 conflicts with.
- `epics/OOP/riso/LT-98531-riso-contract-lesson-report/test-cases/monthly-report-calculations.md` — assert the confirmed status-agnostic Lesson Allocated rule this ticket's AC01.2 diverges from.

## QASE Coverage Gaps

- AC01.1 — Contract Info page display, LA list filter/sort, empty state (new feature; no existing Qase cases)
- AC01.2 — Total Slot / Lesson Allocated calculation, all contract types incl. Trial (new feature; formula itself is in dispute — see Clarification Questions)
- AC02.1 — Lesson History page, month navigation, row rendering (new feature; no existing Qase cases)
