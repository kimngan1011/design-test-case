# Test Coverage: LT-98530 — [Riso] OOP | Contract and Monthly Lesson history (App)

**Jira:** https://manabie.atlassian.net/browse/LT-98530
**Date:** 2026-08-13

> **Note:** Clarifications were answered on 2026-08-13. This coverage reflects the confirmed Riso App rules: PRD "Seasonal" maps to `Contract.type=one-time`, Cancelled is excluded from Lesson Allocated, Lesson History is Completed-only, and neither a Trial contract type nor App–SF calculation parity is in scope.

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|---|---|
| BR-01/02 | AC01.1 | Header unchanged: student icon + full name; edit icon edits full name |
| BR-03 | AC01.1 | Section header label "Contract Info"/"ご契約内容" (PRD Localization table) |
| BR-04/05 | AC01.1 | Month selector: year-month dropdown, EN/JP format, default = last month of current AY |
| BR-06 | AC01.1 | Info banner re: data update timing |
| BR-07/08 | AC01.1 | LA list filtered to require_allocation=TRUE AND Academic Year=Current AY |
| BR-09/10 | AC01.1 | LA card shows Course Master Name (derived), Academic Year, Location |
| BR-11/12 | AC01.1/.2 | LA card shows Total Slot and Lesson Allocated for selected month |
| BR-13 | AC01.1 | LA list sort: start date ASC → end date ASC → created_at ASC |
| BR-14 | AC01.2 | Total Slot = SUM of related Riso Contracts' slot numbers |
| BR-15 | AC01.2 | `monthly` type: Monthly Slot × elapsed months |
| BR-16 | AC01.2 | `one-time` type (called Seasonal in the PRD): full slot if Start(month) ≤ Selected(EOM), else 0 |
| BR-17 | AC01.2 | Trial is not a valid Riso Contract.type (out of scope) |
| BR-18/19 | AC01.2 | Lesson Allocated: sessions within AY AND ≤ EOM of selected month |
| BR-20 | AC01.2 | AND Lesson Status is NOT Cancelled |
| BR-21/22 | AC01.2 | EXCLUDE Absent AND Notice NOT "In Advance"; Present and Absent+InAdvance are included (🔴 lesson-learned risk) |
| BR-23 | AC01.2 | Riso-only calculation; App–SF parity is not required |
| BR-24 | AC02.1 | Page menu label "Lesson History"/"授業履歴" |
| BR-25/26 | AC02.1 | Month Navigator default "THIS month", EN/JP format |
| BR-27 | AC02.1 | Unbounded back/next month navigation; "No data" where no qualifying lesson exists |
| BR-28 | AC02.1 | "No data" UI if no completed lessons in selected month |
| BR-29 | AC02.1 | List = Status = Completed only |
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
| AC01.1 | Consolidated Contract Info translation: header, section, caption, card labels, info banner (EN/JP) | Display completeness | Component | Low | Smoke |
| AC01.1 | Month selector format + default (last month of AY) | Boundary/range + Display completeness | BVA + Component | Medium | Standard |
| AC01.1 | LA list filter: require_allocation=TRUE AND Current AY | Conditional logic | Decision Table | High | Deep |
| AC01.1 | LA card fields: Course Master Name, AY, Location | Display completeness + Cross-system | Component | Medium | Standard |
| AC01.1 | LA card Total Slot / Lesson Allocated value display | Display completeness | Component | High | Standard |
| AC01.1 | LA list sort order (start→end→created_at) | Ordering / Sort | Scenario | Medium | Standard |
| AC01.1 | Zero qualifying data — no LA cards for selected month, including out-of-AY months | Display completeness | Negative | Medium | Standard |
| AC01.2 | Total Slot = SUM(contract slot) across Active contracts | Data integrity | Decision Table | 🔴 Critical | Deep |
| AC01.2 | Total Slot — Monthly type proration formula | Conditional + Boundary/range | BVA + Decision Table | 🔴 Critical | Deep |
| AC01.2 | Total Slot — One-Time type on/off formula | Conditional + Boundary/range | BVA + Decision Table | 🔴 Critical | Deep |
| AC01.2 | Lesson Allocated — AY + EOM date range filter | Boundary/range | BVA | High | Deep |
| AC01.2 | Lesson Allocated — Cancelled-status exclusion | Conditional logic | Decision Table | 🔴 Critical | Deep |
| AC01.2 | Lesson Allocated — compound Attendance exclusion (lesson-learned risk) | Conditional logic | Decision Table | 🔴 Critical | Deep |
| AC01.2 | Contract API update is reflected in the App | Cross-system impact | Regression | High | Deep |
| AC02.1 | Consolidated Lesson History translation: menu, table labels, Month Navigator and Lesson Date formats (EN/JP) | Boundary/range + Display completeness | Component | Medium | Standard |
| AC02.1 | Month Navigator is unbounded; no-data result for any month without qualifying lessons | Boundary/range | Negative + BVA | Medium | Standard |
| AC02.1 | "No data" empty state | Display completeness | Negative | Medium | Standard |
| AC02.1 | Lesson History status filter: Completed only | Conditional logic | Decision Table | 🔴 Critical | Deep |
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
- **F. Cross-system/cross-surface** — APPLIES. Verify that Contract API updates become visible in the App. Do not assert App–SF or App–API numerical equality because the App has its own confirmed calculation.
- **G. Downstream effects** — LARGELY N/A: this ticket has no CREATE/UPDATE/DELETE action of its own (pure read/view feature). The only "downstream" direction is inverted — upstream Contract API writes (LT-98533) and Student Session attendance updates must be correctly reflected here. This is captured by the Cross-system (F) row rather than a Downstream Effects table, since there is no primary write action in this ticket to build that table around.
- **H. Display completeness & ordering** — APPLIES, see Display & Ordering Inventory Table below.
- **H.1 Spec–Figma mismatch** — Applied to the Contract page frame (Figma node 7592:1027; Lesson History page frame not available in the ticket's Figma link, only PRD screenshots). The Trial card is out of scope because Trial is not a Riso Contract.type. The PRD Localization table defines the caption as "total at the time"/"時点の累計" and it is asserted in the consolidated Contract Info Translation case.

### Display & Ordering Inventory Table

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| Contract Info — LA card | Course Master Name, Academic Year, Location, Total Slot, Lesson Allocated | — | LA start ASC → end ASC → created_at ASC | Consolidated Translation case asserts card labels and info banner EN/JP |
| Contract Info — Month selector | Selected month label | — | N/A (single value) | Format strings "MM YYYY" (EN) / "YYYY年MM月" (JP) |
| Contract Info — no-data result | No LA cards/data for the selected month | — | N/A | No hard-coded copy assertion |
| Lesson History — row | Lesson Date, Lesson Time, Subject, Teacher, Attendance | Timeslot Name (blank if none), Subject (blank if none), Teacher (blank if none / comma-sep if multiple), Attendance Notice (new line if present) | Lesson start time ASC | Consolidated Translation case asserts row labels and date format EN/JP; "No data" when no qualifying lesson exists |
| Lesson History — Month Navigator | Selected month label | Back/Next available without a specified boundary | N/A | Format strings "month year" (EN) / "YYYY年MM月" (JP) |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Total Slot formula (Monthly/One-Time, BR-14–16) | The App's selected-month calculation differs from backend flat aggregation, so the UI calculation can silently regress. | Test the confirmed App formula: Monthly proration and One-Time full-slot boundary. Trial is out of scope. |
| Lesson Allocated — Cancelled-status exclusion (BR-20) | The App intentionally differs from the sibling SF report, so a shared-calculation assumption could remove the exclusion. | Assert only the confirmed App behaviour: Cancelled is excluded. |
| Lesson Allocated — compound Attendance exclusion (BR-21) | Lesson-learned risk: OOP compound conditions have a documented history (Nichibei, 2026-03-04) of partial implementation causing silent miscalculation. | Mandatory 3-way decision table: Absent+InAdvance (INCLUDED), Absent+NoNotice (EXCLUDED), Present (INCLUDED) — no partial credit for 2 of 3 cases. |
| Lesson History status filter (BR-29) | A wrong status filter would expose scheduled or cancelled lessons as history. | Decision-table coverage asserts Completed only. |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Contract API → App propagation | Contract API writes must reach the App, but the App is not required to mirror API aggregation or the SF report's status handling. | Create/update contract test data through the API and assert the App's own confirmed formula after sync. |
| Lesson Allocated AY + EOM date-range filter | Two chained boundary conditions (within AY, ≤ EOM); errors here silently over/under count. | BVA at both boundaries independently, plus a combined case straddling both. |
| Lesson History row rendering (BR-32–36) | 5 fields each with distinct conditional/blank rules; a single "happy path" TC would miss most of the real bugs (blank teacher, blank subject, no timeslot, multiple teachers). | One Component TC for the full/no-gaps case, one Negative TC per conditional field showing its blank/edge variant. |
| JST month-boundary / cross-midnight logic | Applies to Total Slot, Lesson Allocated, and Lesson History month filters simultaneously; a timezone bug here would silently miscount across all three. | Reuse the LT-96673 timezone-risk pattern: derive month from UI-local (JST) date, not raw UTC storage; test a lesson at 23:30+ JST near month-end. |
| Own-data-only scope | Financial/contract data — a cross-student leak here is a high-severity data exposure, not just a display bug. | Permission matrix: verify Student A never sees Student B's contracts/lesson history even via API/manipulation, and a parent only sees linked children. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Month selector default + range vs. Current-AY-only LA filter | The selector is unbounded while the list remains Current-AY scoped. | Standard-depth TC selects an out-of-AY month and asserts no qualifying LA data/cards are shown. |
| Empty/no-data states | Contract page has no-card behaviour; Lesson History shows "No data" when a month has no qualifying Completed lessons. | Assert the confirmed behaviours without inventing Contract-page copy. |
| Contract-sync staleness banner | Acknowledged eventual-consistency risk; low likelihood of a hard bug, but a real support-ticket generator if the banner text/logic is wrong. | Scenario TC: create a contract via API, verify banner remains until data reflects, no false-negative "no data" flash. |
| Riso-only partner gate | Standard OOP-feature-flag pattern already well-tested elsewhere in this codebase (low novel risk). | 1 Permission Matrix TC confirming non-Riso tenant sees no Contract Info / Lesson History entry point. |

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Contract Info page (display, list, sort, empty state) | None (greenfield App UI) | None | ✅ Full new suite |
| Total Slot calculation (Monthly/One-Time) | `epics/OOP/riso/LT-98533-riso-contract-api/test-cases/la-aggregation-post.md`, `la-aggregation-patch.md` | Backend aggregation only; not the App calculation | ✅ App-specific Monthly and One-Time calculation TCs |
| Lesson Allocated calculation (date range, status, attendance) | `epics/OOP/riso/LT-98531-riso-contract-lesson-report/test-cases/monthly-report-calculations.md` | Partial — same compound Attendance rule, but confirmed to differ on Cancelled-status handling | ✅ New TCs, explicitly parameterized to test both status-handling interpretations |
| Lesson History page (display, navigator, filter, sort) | None (greenfield App UI) | None | ✅ Full new suite |
| Contract API → App propagation | None | API write is covered, App presentation is not | ✅ New App propagation regression; no App–SF parity assertion |
| Permission / partner scope | Existing Riso permission-matrix rows are all SF-side (HQ/CM); no App-side row exists | None | ✅ New TCs; also flag permission-matrix CSV as missing an App-facing row (documentation gap, out of scope to fix here) |

---

## 7. Suggested Test Suite Structure

```
epics/OOP/riso/LT-98530-contract-monthly-lesson-history-app/test-cases/
├── contract-info-display.md          → AC01.1 — header, static text, LA list filter/fields/sort, empty state
├── total-slot-calculation.md         → AC01.2 — Total Slot formula: Monthly/One-Time (🔴 Critical)
├── lesson-allocated-calculation.md   → AC01.2 — Lesson Allocated: date range, status filter, compound attendance exclusion (🔴 Critical)
├── lesson-history-display.md         → AC02.1 — page menu, month navigator, empty state, row field rendering
├── lesson-history-filter-sort.md     → AC02.1 — Completed-only status filter, month filter, sort order
└── permission-and-scope.md           → Cross-cutting — Riso-only gate, own-data-only scope, JST month-boundary edge cases, contract-sync staleness
```
