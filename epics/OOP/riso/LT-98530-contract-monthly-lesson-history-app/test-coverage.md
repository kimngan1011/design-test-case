# Test Coverage: LT-98530 — [Riso] OOP | Contract and Monthly Lesson history (App)

**Jira:** https://manabie.atlassian.net/browse/LT-98530
**Date:** 2026-07-27

> **Note:** Per user instruction, 4 CONFLICT-tier and 1 LESSON-LEARNED RISK item from the spec remain unresolved (not yet posted to Jira). This coverage treats the PRD's stated rules as primary/testable-as-written, while marking the disputed rules 🔴 Critical / "pending confirmation" so they are easy to re-scope once the Jira thread resolves.

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|---|---|
| BR-01/02 | AC01.1 | Header unchanged: student icon + full name; edit icon edits full name |
| BR-03 | AC01.1 | Section header label "Contract Info"/"契約情報" |
| BR-04/05 | AC01.1 | Month selector: year-month dropdown, EN/JP format, default = last month of current AY |
| BR-06 | AC01.1 | Info banner re: data update timing |
| BR-07/08 | AC01.1 | LA list filtered to require_allocation=TRUE AND Academic Year=Current AY |
| BR-09/10 | AC01.1 | LA card shows Course Master Name (derived), Academic Year, Location |
| BR-11/12 | AC01.1/.2 | LA card shows Total Slot and Lesson Allocated for selected month |
| BR-13 | AC01.1 | LA list sort: start date ASC → end date ASC → created_at ASC |
| BR-14 | AC01.2 | Total Slot = SUM of related Riso Contracts' slot numbers |
| BR-15 | AC01.2 | Monthly type: slot = Monthly Slot × elapsed months |
| BR-16 | AC01.2 | Seasonal type: full slot if Start(month) ≤ Selected(EOM) else 0 |
| BR-17 | AC01.2 (gap) | Trial-type contract has no Total Slot rule (🔴 disputed) |
| BR-18/19 | AC01.2 | Lesson Allocated: sessions within AY AND ≤ EOM of selected month |
| BR-20 | AC01.2 | AND Lesson Status is NOT Cancelled (🔴 disputed vs sibling report) |
| BR-21/22 | AC01.2 | EXCLUDE Absent AND Notice NOT "In Advance" (🔴 lesson-learned risk) |
| BR-23 | AC01.2 | Same calc as PBT-1510 (cross-surface consistency claim, disputed) |
| BR-24 | AC02.1 | Page menu label "Lesson History" |
| BR-25/26 | AC02.1 | Month Navigator default "THIS month", EN/JP format |
| BR-27 | AC02.1 | Back/next month navigation (no boundary defined — gap) |
| BR-28 | AC02.1 | "No data" UI if no completed lessons in selected month |
| BR-29 | AC02.1 | List = Status = Completed (🔴 PRD's own unresolved "TBC → Cancelled" comment) |
| BR-30 | AC02.1 | AND Lesson Date(month) = selected month |
| BR-31 | AC02.1 | Sort: Lesson start time ASC |
| BR-32/33/34/35/36 | AC02.1 | Row fields: Date, Time+Timeslot, Subject, Teacher, Attendance+Notice (all with conditional blank rules) |

---

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC01.1 | BR-01/02/03/06 | Display completeness |
| AC01.1 | BR-04/05 | Boundary/range + Display completeness |
| AC01.1 | BR-07/08 | Conditional logic |
| AC01.1 | BR-09/10/11/12 | Display completeness + Cross-system impact |
| AC01.1 | BR-13 | Ordering / Sort |
| AC01.2 | BR-14/15/16/17 | Conditional logic + Boundary/range + Data integrity |
| AC01.2 | BR-18/19 | Boundary/range |
| AC01.2 | BR-20/21/22 | Conditional logic |
| AC01.2 | BR-23 | Cross-system impact |
| AC02.1 | BR-24/26 | Display completeness |
| AC02.1 | BR-25/27 | Boundary/range |
| AC02.1 | BR-28 | Display completeness |
| AC02.1 | BR-29/30 | Conditional logic |
| AC02.1 | BR-31 | Ordering / Sort |
| AC02.1 | BR-32-36 | Display completeness (with conditional sub-rules) |
| Cross-cutting | — | Permission logic (Riso partner gate, own-data scope); Date/Time logic (JST month-boundary risk) |

---

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Display completeness | Component (all required fields together), Negative (field absent/blank cases) |
| Boundary/range | Boundary Value Analysis (month edges, AY edges, EOM), Negative |
| Conditional logic | Decision Table (filter combinations), Negative |
| Data integrity | CRUD-adjacent (aggregation correctness across contract writes), Decision Table |
| Cross-system impact | Regression (App vs SF report vs API spec), CRUD |
| Ordering / Sort | Scenario (2+ items differing on sort key) |
| Permission logic | Permission Matrix |
| Date/Time logic | Boundary Value Analysis (TZ, cross-midnight) |

---

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC01.1 | Header unchanged (icon/name/edit) | Display completeness | Component | Low | Smoke |
| AC01.1 | Section header + info banner exact text (EN/JP) | Display completeness | Component | Low | Smoke |
| AC01.1 | Month selector format + default (last month of AY) | Boundary/range + Display completeness | BVA + Component | Medium | Standard |
| AC01.1 | LA list filter: require_allocation=TRUE AND Current AY | Conditional logic | Decision Table | High | Deep |
| AC01.1 | LA card fields: Course Master Name, AY, Location | Display completeness + Cross-system | Component | Medium | Standard |
| AC01.1 | LA card Total Slot / Lesson Allocated value display | Display completeness | Component | High | Standard |
| AC01.1 | LA list sort order (start→end→created_at) | Ordering / Sort | Scenario | Medium | Standard |
| AC01.1 | Empty state — zero qualifying LAs (gap, pending confirmation) | Display completeness | Negative | Medium | Standard |
| AC01.2 | Total Slot = SUM(contract slot) across Active contracts | Data integrity | Decision Table | 🔴 Critical | Deep |
| AC01.2 | Total Slot — Monthly type proration formula (disputed) | Conditional + Boundary/range | BVA + Decision Table | 🔴 Critical | Deep |
| AC01.2 | Total Slot — Seasonal type on/off formula (disputed) | Conditional + Boundary/range | BVA + Decision Table | 🔴 Critical | Deep |
| AC01.2 | Total Slot — Trial type (undocumented, pending) | Conditional logic | Negative (placeholder) | 🔴 Critical | Deep once defined |
| AC01.2 | Lesson Allocated — AY + EOM date range filter | Boundary/range | BVA | High | Deep |
| AC01.2 | Lesson Allocated — Cancelled-status exclusion (disputed vs SF report) | Conditional logic | Decision Table | 🔴 Critical | Deep |
| AC01.2 | Lesson Allocated — compound Attendance exclusion (lesson-learned risk) | Conditional logic | Decision Table | 🔴 Critical | Deep |
| AC01.2 | Cross-surface consistency: App vs SF Monthly report vs Contract API | Cross-system impact | Regression | High | Deep |
| AC02.1 | Month Navigator default ("THIS month") + EN/JP format | Boundary/range + Display completeness | Component | Medium | Standard |
| AC02.1 | Month Navigator back/next boundary (gap, pending confirmation) | Boundary/range | Negative + BVA | Medium | Standard |
| AC02.1 | "No data" empty state | Display completeness | Negative | Medium | Standard |
| AC02.1 | Lesson History status filter: Completed (PRD's own "TBC" comment) | Conditional logic | Decision Table | 🔴 Critical | Deep |
| AC02.1 | Lesson History month filter | Conditional logic | Decision Table | High | Standard |
| AC02.1 | Lesson History sort order (start time ASC) | Ordering / Sort | Scenario | Medium | Standard |
| AC02.1 | Row fields: Date/Time+Timeslot/Subject/Teacher/Attendance, incl. all blank/conditional variants | Display completeness | Component + Negative | High | Deep |
| Cross-cutting | JST month-boundary / cross-midnight date comparisons (Total Slot, Lesson Allocated, Lesson History filters) | Date/Time logic | BVA | High | Deep |
| Cross-cutting | Riso-only partner gate (feature hidden for non-Riso) | Permission logic | Permission Matrix | Medium | Standard |
| Cross-cutting | Own-data-only scope (student/parent sees only own/linked-child data) | Permission logic | Permission Matrix | High | Standard |
| Cross-cutting | Contract-sync staleness (info banner acknowledges eventual consistency) | Data integrity | Scenario | Medium | Standard |

---

## Mandatory Edge-Case Checklist (Step 4.5) — Summary

- **A. Configuration-driven thresholds** — N/A. No tenant-config numeric threshold (advance days, capacity, etc.) exists in this feature; Total Slot inputs come from Contract records, not partner config.
- **B. Date/Time logic** — APPLIES. Covered as the "JST month-boundary / cross-midnight" row above: TZ-behind and TZ-ahead device tests near midnight for lesson-date-to-month attribution (mirrors the documented Monthly Lesson Count timezone risk, LT-96673); EOM boundary tests for Total Slot and Lesson Allocated; "THIS month" default boundary at day 1 / day 1 23:59. DST — N/A (JST does not observe DST).
- **C. Concurrent/stale state** — APPLIES (Medium). Info banner (BR-06) itself acknowledges contract data lag; covered as "Contract-sync staleness" row. Multi-tab/device: Low priority, folded into Standard depth of the same row.
- **D. Permission & role** — APPLIES. Covered as "Riso-only partner gate" and "Own-data-only scope" rows. Feature-flag-off (non-Riso) must gracefully show no Contract Info/Lesson History entry points at all.
- **E. State transition** — APPLIES (folded into Lesson Allocated / Lesson History rows). Documented: Published/Completed count toward Lesson Allocated, only Completed shows in Lesson History, Cancelled/Draft never reach Mobile. Undocumented transition to test as negative: a Draft lesson must never appear in either page (platform-level guarantee, still worth 1 regression check here since it's load-bearing for BR-20/29).
- **F. Cross-system/cross-surface** — APPLIES. Covered as "Cross-surface consistency: App vs SF report vs Contract API" — the single highest-value regression row given 3 of 4 spec conflicts live here.
- **G. Downstream effects** — LARGELY N/A: this ticket has no CREATE/UPDATE/DELETE action of its own (pure read/view feature). The only "downstream" direction is inverted — upstream Contract API writes (LT-98533) and Student Session attendance updates must be correctly reflected here. This is captured by the Cross-system (F) row rather than a Downstream Effects table, since there is no primary write action in this ticket to build that table around.
- **H. Display completeness & ordering** — APPLIES, see Display & Ordering Inventory Table below.
- **H.1 Spec–Figma mismatch** — Applied to the Contract page frame (Figma node 7592:1027; Lesson History page frame not available in the ticket's Figma link, only PRD screenshots). Found 2 mismatch rows (see spec.md Missing in Requirements #6 and Clarification Question #10 — "時点の累計" caption undocumented, and the Trial Lesson card). Per user instruction (2026-07-27), both are deferred rather than blocking — treated as "pending confirmation," PRD text remains primary.

### Display & Ordering Inventory Table

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| Contract Info — LA card | Course Master Name, Academic Year, Location, Total Slot, Lesson Allocated | Trial-type card variant (formula undefined — pending) | LA start ASC → end ASC → created_at ASC | Info banner EN/JP exact text; "時点の累計" caption (pending confirmation, not yet speced) |
| Contract Info — Month selector | Selected month label | — | N/A (single value) | Format strings "MM YYYY" (EN) / "YYYY年MM月" (JP) |
| Contract Info — empty state | Placeholder message | — | N/A | Exact empty-state copy — not specified in PRD, pending confirmation |
| Lesson History — row | Lesson Date, Lesson Time, Subject, Teacher, Attendance | Timeslot Name (blank if none), Subject (blank if none), Teacher (blank if none / comma-sep if multiple), Attendance Notice (new line if present) | Lesson start time ASC | Date/time format strings (EN/JP); exact "No data" empty-state copy — not specified in PRD, pending confirmation |
| Lesson History — Month Navigator | Selected month label | Back/Next enabled state (boundary undefined — pending) | N/A | Format strings "month year" (EN) / "YYYY年MM月" (JP) |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Total Slot formula (Monthly/Seasonal/Trial, BR-14–17) | Directly conflicts with the authoritative Contract API spec (LT-98533), which says monthly-type contracts aren't used in any slot calculation today and aggregation is a flat SUM; Trial-type has no formula at all. Writing test cases against the PRD's literal formula risks being thrown away. | Write test cases against the PRD's stated formula NOW (per user instruction to keep PRD primary), but tag every TC clearly as "pending confirmation — see spec Clarification Q1/Q5" so they are trivially findable for rework once Jira resolves. |
| Lesson Allocated — Cancelled-status exclusion (BR-20) | Conflicts with the sibling SF report's confirmed behavior (no status check at all), despite both claiming the same PBT-1510 formula. | Test both interpretations (with and without Cancelled exclusion) as separate TC variants; tag as "pending confirmation — see spec Clarification Q2." |
| Lesson Allocated — compound Attendance exclusion (BR-21) | Lesson-learned risk: OOP compound conditions have a documented history (Nichibei, 2026-03-04) of partial implementation causing silent miscalculation. | Mandatory 3-way decision table: Absent+InAdvance (INCLUDED), Absent+NoNotice (EXCLUDED), Present (INCLUDED) — no partial credit for 2 of 3 cases. |
| Lesson History status filter (BR-29) | The PRD's own inline comment marks this as unresolved ("TBC → Cancelled"). | Write TCs for Status=Completed-only (the documented + RFP-supported interpretation) as primary, tag as "pending confirmation — see spec Clarification Q3." |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Cross-surface consistency (App vs SF report vs Contract API) | 3 of 4 disputed conflicts live at this boundary; any fix to one surface without the others causes visible cross-surface discrepancies reportable as bugs. | Regression suite that runs the same test data (contract + sessions) through App, SF report (LT-98531), and API aggregation (LT-98533) and diffs the three outputs. |
| Lesson Allocated AY + EOM date-range filter | Two chained boundary conditions (within AY, ≤ EOM); errors here silently over/under count. | BVA at both boundaries independently, plus a combined case straddling both. |
| Lesson History row rendering (BR-32–36) | 5 fields each with distinct conditional/blank rules; a single "happy path" TC would miss most of the real bugs (blank teacher, blank subject, no timeslot, multiple teachers). | One Component TC for the full/no-gaps case, one Negative TC per conditional field showing its blank/edge variant. |
| JST month-boundary / cross-midnight logic | Applies to Total Slot, Lesson Allocated, and Lesson History month filters simultaneously; a timezone bug here would silently miscount across all three. | Reuse the LT-96673 timezone-risk pattern: derive month from UI-local (JST) date, not raw UTC storage; test a lesson at 23:30+ JST near month-end. |
| Own-data-only scope | Financial/contract data — a cross-student leak here is a high-severity data exposure, not just a display bug. | Permission matrix: verify Student A never sees Student B's contracts/lesson history even via API/manipulation, and a parent only sees linked children. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Month selector default + range vs. Current-AY-only LA filter | Gap: unclear if selector can move outside current AY while LA list is hard-filtered to it. | Standard-depth TCs for the documented default; 1 exploratory TC attempting an out-of-AY selection, tagged pending confirmation. |
| Empty states (Contract page zero-LA, Lesson History no-data) | Both lack exact copy in the PRD. | Standard TCs asserting *a* graceful empty state exists (no crash), with placeholder text flagged pending confirmation rather than hard-asserted. |
| Contract-sync staleness banner | Acknowledged eventual-consistency risk; low likelihood of a hard bug, but a real support-ticket generator if the banner text/logic is wrong. | Scenario TC: create a contract via API, verify banner remains until data reflects, no false-negative "no data" flash. |
| Riso-only partner gate | Standard OOP-feature-flag pattern already well-tested elsewhere in this codebase (low novel risk). | 1 Permission Matrix TC confirming non-Riso tenant sees no Contract Info / Lesson History entry point. |

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Contract Info page (display, list, sort, empty state) | None (greenfield App UI) | None | ✅ Full new suite |
| Total Slot calculation (all contract types) | `epics/OOP/riso/LT-98533-riso-contract-api/test-cases/la-aggregation-post.md`, `la-aggregation-patch.md` | Partial — these assert the flat SUM aggregation this ticket's formula conflicts with | ✅ New TCs against PRD formula (tagged pending), plus a cross-reference regression check against the existing aggregation TCs |
| Lesson Allocated calculation (date range, status, attendance) | `epics/OOP/riso/LT-98531-riso-contract-lesson-report/test-cases/monthly-report-calculations.md` | Partial — same compound Attendance rule, but confirmed to differ on Cancelled-status handling | ✅ New TCs, explicitly parameterized to test both status-handling interpretations |
| Lesson History page (display, navigator, filter, sort) | None (greenfield App UI) | None | ✅ Full new suite |
| Cross-surface consistency (App / SF report / API) | None — LT-98531 spec itself notes "No existing E2E scenarios cover Riso Contract List or Monthly Lesson Assignment Report" | None | ✅ New regression suite, first of its kind for this data model |
| Permission / partner scope | Existing Riso permission-matrix rows are all SF-side (HQ/CM); no App-side row exists | None | ✅ New TCs; also flag permission-matrix CSV as missing an App-facing row (documentation gap, out of scope to fix here) |

---

## 7. Suggested Test Suite Structure

```
epics/OOP/riso/LT-98530-contract-monthly-lesson-history-app/test-cases/
├── contract-info-display.md          → AC01.1 — header, static text, LA list filter/fields/sort, empty state
├── total-slot-calculation.md         → AC01.2 — Total Slot formula: Monthly/Seasonal/Trial (🔴 Critical, pending confirmation)
├── lesson-allocated-calculation.md   → AC01.2 — Lesson Allocated: date range, status filter, compound attendance exclusion (🔴 Critical)
├── lesson-history-display.md         → AC02.1 — page menu, month navigator, empty state, row field rendering
├── lesson-history-filter-sort.md     → AC02.1 — status filter (🔴 TBC), month filter, sort order
└── permission-and-scope.md           → Cross-cutting — Riso-only gate, own-data-only scope, JST month-boundary edge cases, contract-sync staleness
```
