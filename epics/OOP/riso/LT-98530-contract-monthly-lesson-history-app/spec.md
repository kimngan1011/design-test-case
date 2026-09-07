---
ticket_id: LT-98530
ticket_url: https://manabie.atlassian.net/browse/LT-98530
title: "[Riso] OOP | Contract and Monthly Lesson history (App)"
module: scheduling/lesson-management
bucket: OOP/riso
status: Ready for QA
internal_uat_date: 2026-08-24
production_release_date: 2026-09-07
last_updated: 2026-08-13
---

# LT-98530: [Riso] OOP | Contract and Monthly Lesson history (App)

## Summary

This ticket adds two new read-only pages to the Riso Learner App (student/parent facing): a **Contract Info** page showing all of a student's active Lesson Allocations (LAs) for the current Academic Year with a month-selectable Total Slot / Lesson Allocated count, and a **Monthly Lesson History** page listing completed lessons per month with date/time/subject/teacher/attendance detail. The Jira ticket itself carries no inline AC — all requirements were sourced from the linked Confluence PRD (2130575378) and cross-referenced against Figma and the original background RFP (No.445), per explicit instruction to focus on the PRD as the source of truth.

The underlying data (Riso Contract records, LA aggregation) is created by a separate API ticket (LT-98533) and also surfaced read-only on SF via a sibling ticket (LT-98531). Clarifications recorded on 2026-08-13 define the App-specific calculation and display scope below.

---

## Acceptance Criteria

### US 01 (PRD: US 01A) — Contract Page
**As a** student or parent, **I want** to view all my contracts when logging in the app **so that** I can keep track of my/my child's learning history.

| ID | Feature | Acceptance Criteria |
|---|---|---|
| AC01.1 | Contract Info under User profile | Header unchanged (student icon + full name, edit icon). Per the PRD Localization table, section header "Contract Info"/"ご契約内容". Month selector (year-month dropdown, EN "MM YYYY" / JP "YYYY年MM月", default = last month of current AY) may select months outside the current AY; when no LA data qualifies for the selected month, no LA data/cards are shown. Info banner re: data update timing. Body = LA list filtered to `require_allocation = TRUE` AND `Academic Year = Current AY`. Each LA card shows Course Master Name (via Location Course → Course Master), Academic Year & Location, Total Slot (契約数) and Lesson Allocated (授業設定数) for the selected month. Sort: LA start date ASC → end date ASC → created_at ASC. |
| AC01.2 | Calculate the Total Slot and Lesson Allocated | **App calculation:** Total Slot = SUM of related Riso Contracts' contributions: `monthly` type → Monthly Slot × elapsed months (Start Month→Selected Month); `one-time` type (called "Seasonal" in the PRD) → full slot if Start Date(month) ≤ Selected Month(EOM), else 0. There is no Trial contract type in Riso. Lesson Allocated = count of Student Sessions where Lesson Date is within AY AND ≤ EOM of selected month AND Lesson Status is NOT Cancelled, EXCLUDING sessions where Attendance = Absent AND Notice is NOT "In Advance". This Riso App rule deliberately follows the current PRD even where the sibling SF report differs. Ref: Riso \| OOP \| RISO Contract API (POST/PATCH) (LT-98533). |

### US 02 (PRD: US 01B) — Lesson History
**As a** student or parent, **I want** to view my/my child's lesson history by month **so that** I can review what lessons have already taken place and stay informed about attendance.

| ID | Feature | Acceptance Criteria |
|---|---|---|
| AC02.1 | Lesson History view page | Page menu "Lesson History"/"授業履歴". Month Navigator defaults to "THIS month" (EN "month year" / JP "YYYY年MM月") and may navigate to any month. "No data" UI is shown if the selected month contains no qualifying lesson. List = all lessons student is allocated to with Status = Completed and Lesson Date(month) = selected month, sorted by Lesson start time ASC. Each row: Lesson Date (EN "Oct 1"-style / JP "10/1" + day of week), Lesson Time (start-end + line-break + Timeslot Name, blank if none), Subject (blank if none), Teacher full name(s) comma-separated (blank if none), Attendance status + Notice on new line if present. |

---

### Localization (PRD Source of Truth)

The **Localization & Messaging (EN / JP)** table in PRD 2130575378 is authoritative over wording elsewhere in the PRD, Figma, or this repository.

| Area | English | Japanese |
|---|---|---|
| Contract header | Full Name | 名前 |
| Contract section | Contract Info | ご契約内容 |
| Contract caption | total at the time | 時点の累計 |
| Contract card labels | Academic Year; Location; Total Slot; Lesson Allocated | 年度; 拠点; 契約数; 授業設定数 |
| Lesson History menu | Lesson History | 授業履歴 |
| Lesson History table labels | Date; Lesson Time; Subject; Teacher; Attendance | 日付; 授業時間; 科目; 講師; 出欠 |

The Contract info-banner text and the Contract/Lesson History month and Lesson Date formats are asserted by the consolidated Translation cases. Logic cases must not assert localized copy.

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---|----|----|---|---|---|
| BR-01 | AC01.1 | Header unchanged: student icon + full name | header | locked | app |
| BR-02 | AC01.1 | Edit icon edits student full name | full_name | editable | app |
| BR-03 | AC01.1 | Section header label "Contract Info"/"ご契約内容" (PRD Localization table) | section_header | locked | app |
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
| BR-16 | AC01.2 | `one-time` Contract.type (called "Seasonal" in the PRD): full slot if Start(month) ≤ Selected(EOM), else 0 | total_slot | auto-calculated | app |
| BR-17 | AC01.2 | Trial is not a valid Riso Contract.type; no Trial calculation or card variant is in scope | total_slot | N/A | app |
| BR-18 | AC01.2 | Lesson Allocated: sessions with Lesson Date within AY | lesson_allocated | auto-calculated | app |
| BR-19 | AC01.2 | AND Lesson Date ≤ EOM of selected month | lesson_allocated | auto-calculated | app |
| BR-20 | AC01.2 | AND Lesson Status is NOT Cancelled | lesson_allocated | auto-calculated | app |
| BR-21 | AC01.2 | EXCLUDE Absent AND Notice NOT "In Advance" | lesson_allocated | auto-calculated | app |
| BR-22 | AC01.2 (note) | Absent+InAdvance is included in Lesson Allocated; Present is also included | lesson_allocated | auto-calculated | app |
| BR-23 | AC01.2 (scope) | This calculation applies to Riso only; do not require parity with the sibling SF report | lesson_allocated | auto-calculated | app |
| BR-24 | AC02.1 | Page menu label "Lesson History"/"授業履歴" | page_menu | locked | app |
| BR-25 | AC02.1 | Month Navigator defaults to "THIS month" | month_navigator | auto-calculated | app |
| BR-26 | AC02.1 | Navigator format EN "month year" / JP "YYYY年MM月" | month_navigator | locked | app |
| BR-27 | AC02.1 | User can navigate back/next without a specified boundary; a selected month with no qualifying lesson shows "No data" | month_navigator | editable | app |
| BR-28 | AC02.1 | "No data" UI if selected month has no completed lessons | lesson_history_list | computed | app |
| BR-29 | AC02.1 | List includes only lessons with Status = Completed | lesson_history_list | computed | app |
| BR-30 | AC02.1 | AND Lesson Date(month) = selected month | lesson_history_list | computed | app |
| BR-31 | AC02.1 | Sort: Lesson start time ASC | lesson_history_list | computed | app |
| BR-32 | AC02.1 | Row: Lesson Date EN "Oct 1"-style / JP "mm/dd" + day of week | lesson_date | auto-calculated | app |
| BR-33 | AC02.1 | Row: Lesson Time "start-end" + line break + Timeslot Name (blank if none) | lesson_time | auto-calculated | app |
| BR-34 | AC02.1 | Row: Subject (blank if none) | subject | optional | app |
| BR-35 | AC02.1 | Row: Teacher name(s) comma-separated (blank if none) | teacher | optional | app |
| BR-36 | AC02.1 | Row: Attendance status + Notice on new line if present | attendance | auto-calculated | app |
| BR-37 | AC01.1 | The selected month may fall outside the current AY; if no data qualifies, show no LA data/cards | la_list | computed | app |
| BR-38 | AC01.1/AC02.1 | Parent must select a linked student before viewing either page; both pages scope data to that selected student | selected_student | computed | app |

---

## Clarification Decisions — 2026-08-13

| # | Topic | Decision | Test/document impact |
|---|---|---|---|
| 1 | Contract type terminology | The PRD's "Seasonal" contract means Riso `Contract.type=one-time`. Monthly remains `monthly`; Trial is not a valid Riso Contract.type. `weekly` has no AC01.2 formula and is outside this ticket's confirmed calculation scope. | Rename Seasonal cases/data to One-Time and remove the Trial placeholder. The App uses AC01.2's month-based formula, not the backend's flat LA aggregation as its display expectation. |
| 2 | Cancelled lessons in Lesson Allocated | Follow the current App specification: Cancelled lessons are excluded. The difference from LT-98531 is deliberate for this App feature and has been raised with PDM. | Keep the exclusion case; remove the alternate SF-report behaviour and any App–SF parity requirement. |
| 3 | Lesson History status | Only `Completed` lessons are listed. | Status decision table is final; remove TBC wording. |
| 4 | Attendance compound rule | This feature applies only to Riso. Present = included; Absent + In Advance = included; Absent + no In Advance notice = excluded. | Keep all three Riso cases; no cross-surface synchronisation assertion is required. |
| 5 | Zero qualifying LA / out-of-AY month | The selector may move outside the current AY. When the selected month has no qualifying data, no LA data/cards are shown. | Assert data/cards are absent, not an unspecified empty-state message. |
| 6 | Lesson History month navigation | Navigation is not bounded. For any selected month, show qualifying Completed lessons; otherwise show "No data". | Replace the boundary placeholder with unbounded-navigation coverage. |
| 7 | Parent with multiple children | A parent must select a student before viewing either page. Data follows the selected student. | Keep the selected-child scope test as a confirmed rule. |
| 8 | Figma caption localisation | The PRD Localization table is authoritative: "total at the time"/"時点の累計". | Cover it in the consolidated Contract Info Translation case; do not add a logic-case assertion. |

### Integration Notes

| Area | App rule | Related-system difference |
|---|---|---|
| Total Slot | Monthly and One-Time contributions use AC01.2's App formula. | LT-98533's flat `LA.Total_Session_Count` aggregation is backend behaviour and is not the expected App value. |
| Lesson Allocated | Exclude Cancelled lessons and apply the three-way Attendance rule. | LT-98531 does not check status. This is an intentional App-only divergence. |

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

## Clarification Log

All ten questions were answered on 2026-08-13. The resulting decisions and their test impact are recorded in [Clarification Decisions — 2026-08-13](#clarification-decisions--2026-08-13). `weekly` remains outside the AC01.2 calculation scope because the PRD provides no formula for it.

## Related Specs

- `epics/OOP/riso/LT-98533-riso-contract-api/spec.md` — Riso Contract API (POST/PATCH); source for the `monthly`/`one-time` Contract.type mapping. Its flat LA aggregation is a backend value, distinct from this App's AC01.2 calculation.
- `epics/OOP/riso/LT-98531-riso-contract-lesson-report/spec.md` — SF-side sibling read surface for the same Contract/LA data. Its status-agnostic Lesson Allocated rule deliberately differs from this App's Cancelled exclusion.
- `epics/OOP/riso/LT-92532-riso-create-update-la-on-ui/spec.md` — Riso manual LA creation; useful background for LA types, which are distinct from Contract.type.

## Related Test Cases

- `epics/OOP/riso/LT-98533-riso-contract-api/test-cases/la-aggregation-post.md` / `la-aggregation-patch.md` — cover backend aggregation; they are not App Total Slot assertions.
- `epics/OOP/riso/LT-98531-riso-contract-lesson-report/test-cases/monthly-report-calculations.md` — covers the sibling SF report's status-agnostic calculation, which is intentionally different from this App.

## QASE Coverage Gaps

- AC01.1 — Contract Info page display, LA list filter/sort, including an out-of-AY selection with no qualifying data.
- AC01.2 — Total Slot / Lesson Allocated calculation for `monthly` and `one-time` contracts; no Trial type is in scope.
- AC02.1 — Lesson History page, unbounded month navigation, Completed-only filter, and row rendering.
