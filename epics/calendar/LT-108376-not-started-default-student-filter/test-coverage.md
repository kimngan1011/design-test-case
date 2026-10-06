# Test Coverage: LT-108376 — Add "Not Started" option as default in student filter in Lesson Calendar

**Jira:** https://manabie.atlassian.net/browse/LT-108376
**Date:** 2026-10-07
**Spec:** `epics/calendar/LT-108376-not-started-default-student-filter/spec.md`

**Scope notes**
- Surface: Salesforce Lesson Calendar → left **Student** panel → filter popover → **Student Course Status**. SF only.
- Out of generated TCs: Additional Fields position change on Create/Edit Lesson + Lesson Schedule forms (QA owner tests manually); Bulk Publish (uses the calendar grid student filter, not this list); 200-row list window (accepted SF limitation).
- Open question Q3 (TODAY = date-only, user timezone): TCs follow current code behavior (status decided by the **logged-in user's** Salesforce timezone). Timezone-gap TCs CS-15 / CS-16 assert this behavior; re-check them if PO answers Q3 differently.

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|---|---|
| BR-01 | AC-01 | On first load of Lesson Calendar, Student Course Status is pre-selected with **Active** and **Not Started** |
| BR-02 | AC-01 | **Inactive** is not pre-selected |
| BR-03 | AC-02 | Default list includes LAs with Start ≤ today ≤ End (Active) |
| BR-04 | AC-02 | Default list includes LAs with Start > today (Not Started) |
| BR-05 | AC-02 | Default list excludes LAs with End < today (Inactive) |
| BR-06 | AC-02 | Boundaries: start today → Active; start tomorrow → Not Started; end today → Active; end yesterday → Inactive (date only, user timezone — Q3) |
| BR-07 | AC-01 | Deselect Not Started → Active-only results |
| BR-08 | AC-01 | Only Not Started selected → only future-LA rows |
| BR-09 | AC-01 | Add Inactive → all three statuses OR-combined |
| BR-10 | AC-01 | Course Status default AND-combines with other filters + keyword search |
| BR-11 | AC-01 | Reset + Save clears all filters except calendar location (Course Status empty = all statuses) |
| BR-12 | AC-01 | Page reload re-applies default Active + Not Started |
| BR-13 | Scope | Lesson Master Student list keeps Active-only default |
| BR-14 | AC-02 | Student with an Inactive LA and a Not Started LA → only the Not Started LA row is shown by default |
| BR-15 | AC-01 | Labels EN / JP: Active / アクティブ, Not Started / 未来のコース, Inactive / 過去のコース, field "Student Course Status" / 生徒コースのステータス |
| BR-16 | — | Additional Fields position on Lesson forms — **manual by QA owner, not in this suite** |
| BR-17 | AC-01 | Chips shown in order Active, Not Started; each removable (×) |
| BR-18 | AC-01 | List + "N items" count reflect Active + Not Started on first load without opening the filter |
| BR-19 | Existing | Academic Year default = current AY (unchanged, kept with new default) |
| BR-20 | Existing | Type default = all LA types (unchanged) |
| BR-21 | AC-02 | Default list = Course Status (Active ∪ Not Started) ∩ current AY ∩ all types ∩ calendar location → a future LA of the **next** AY is hidden until that AY is selected (by design) |
| BR-22 | AC-01 | Changing calendar location or view keeps the user's filter selection; only the Location chip changes |
| F-06 | AC-02 | A student with an Active LA + a Not Started LA shows **one row per LA** (2 rows) — expected |

---

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC-01 | BR-01, BR-02, BR-17, BR-18 | Display completeness, Conditional |
| AC-02 | BR-03, BR-04, BR-05, BR-14 | Conditional |
| AC-02 | BR-06 | Boundary/range |
| AC-02 | BR-21, BR-19, BR-20 | Conditional |
| AC-02 | F-06 | Data integrity (row per LA), Display completeness |
| AC-01 | BR-07, BR-08, BR-09 | Conditional |
| AC-01 | BR-10 | Conditional (multi-filter) |
| AC-01 | BR-11, BR-12, BR-22 | Conditional (filter state) |
| Scope | BR-13 | Conditional (Lesson Calendar vs Lesson Master), Cross-surface |
| AC-01 | BR-15 | Display completeness (localization) |
| — | Roles HQ / CM | Permission |

---

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Display completeness | Component (chips + list + count in one TC), Negative (Inactive chip absent) |
| Conditional | Decision Table (status × selection), Equivalence Partitioning (Active / Not Started / Inactive LAs) |
| Boundary/range | Boundary Value Analysis on LA Start / End vs today |
| Data integrity | Scenario (student with 2 LAs → 2 rows) |
| Conditional (multi-filter) | Pairwise (Course Status × AY × Course/Class × keyword) |
| Cross-surface | Regression (Lesson Master) |
| Permission | Permission Matrix (HQ, CM) |

---

## 4. Edge-Case Checklist (Step 4.5)

| Section | Result |
|---|---|
| **A. Config thresholds** | N/A — no tenant/partner config or feature flag gates this change (re-applied code has no flag). |
| **B. Date / time** | ✅ Yes — BVA on LA Start/End vs today (start today / tomorrow, end today / yesterday). Every TC declares `today`. ✅ TZ gap — user TZ BEHIND location TZ (ICT GMT+7 vs JST): CS-15. ✅ TZ gap — user TZ AHEAD of location TZ (Australia/Brisbane GMT+10, no DST, vs JST): CS-16. Expected = current code (user timezone), pending Q3. Cross-midnight while UI open: N/A — list is re-queried only on load / filter change; not in AC. DST: N/A (JST). |
| **C. Concurrent / stale** | N/A — read-only list filter, no shared resource. |
| **D. Permission & role** | ✅ HQ (full_access) and CM (center_level_edit) — same behavior (confirmed). Cross-tenant: N/A (filter scoped by calendar location). Feature flag OFF: N/A (no flag). |
| **E. State transition** | N/A — LA status is derived from dates, not a stored transition; date partitions covered in B. |
| **F. Cross-surface** | ✅ Lesson Master shares `listStudentCalendar` → must keep Active-only default (BR-13). BO / Learner App: N/A (SF only). |
| **G. Downstream effects** | N/A — no create/update/delete; filter changes only what is listed. Assigning a listed student to a lesson is existing behavior (E2E-28), unchanged. |
| **H. Display & ordering** | ✅ See inventory below. |
| **H.1 Spec–Figma** | N/A — no Figma URL. PBT-3079 mockup image checked: chips "Active ×", "Not Started ×" in that order; matches code. |

### Display & Ordering Inventory

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Text to Assert |
|---|---|---|---|---|
| Student filter popover — Student Course Status | Label "Student Course Status", chips Active ×, Not Started × | Inactive chip only when selected | Active, Not Started (option order: Active, Not Started, Inactive) | EN: Active / Not Started / Inactive; JP: アクティブ / 未来のコース / 過去のコース; 生徒コースのステータス |
| Student list (left panel) | One row per LA: student name (+ nickname), allocation info; "N items" count | Row present only if LA matches all filters | Phonetic Name ASC → Name ASC → CreatedDate ASC (existing) | "N items" equals number of LA rows |
| Empty state | "0 items", no crash | — | — | — (existing) |
| Pagination | First 200 rows only | — | — | N/A — accepted SF limitation |

---

## 5. Structured Coverage Strategy

| # | AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|---|
| CS-01 | AC-01 | Default chips Active + Not Started, Inactive not selected, chips removable; list + count already filtered on load (BR-01, 02, 17, 18) | Display completeness | Component, Negative | High | Standard |
| CS-02 | AC-02 | Default list shows Active + Not Started LAs, hides Inactive LAs (BR-03, 04, 05) | Conditional | Equivalence Partitioning | High | Deep |
| CS-03 | AC-02 | Date boundaries: start today, start tomorrow, end today, end yesterday (BR-06) | Boundary/range | BVA | High | Deep |
| CS-04 | AC-02 | Student with Inactive LA + Not Started LA → only Not Started row (BR-14) | Conditional | Scenario | Medium | Standard |
| CS-05 | AC-02 | Student with Active LA + Not Started LA (Change / Add Associated Course, future effective date) → 2 rows, one per LA (F-06) | Data integrity | Scenario | Medium | Standard |
| CS-06 | AC-02 | Future LA in next AY hidden with default current AY; shown after adding next AY (BR-19, 21) | Conditional | Decision Table | Medium | Standard |
| CS-07 | AC-01 | Change selection: remove Not Started → Active only; remove Active → Not Started only; add Inactive → all (BR-07, 08, 09) | Conditional | Decision Table | Medium | Standard |
| CS-08 | AC-01 | Default combines with Course / Class / Type and keyword search (BR-10, 20) | Conditional | Pairwise | Medium | Standard |
| CS-09 | AC-01 | Reset + Save clears Course Status (and AY / Type) except location → Inactive LAs and other-AY LAs appear (BR-11) | Conditional | Decision Table | High | Standard |
| CS-10 | AC-01 | Reload re-applies default Active + Not Started after a custom selection (BR-12) | Conditional | Scenario | Medium | Smoke |
| CS-11 | AC-01 | Change calendar location / view → selection kept, only Location chip changes (BR-22) | Conditional | Scenario | Medium | Standard |
| CS-12 | Scope | Lesson Master Student list keeps Active-only default (BR-13) | Cross-surface | Regression | High | Standard |
| CS-13 | AC-01 | JP labels of field and options (BR-15) | Display completeness | Component | Low | Smoke |
| CS-14 | AC-01 | CM (center_level_edit) sees same default as HQ | Permission | Permission Matrix | Low | Smoke |
| CS-15 | AC-02 | TZ gap — user TZ behind location (ICT vs JST): LA starting D+1 00:30 JST shows Active for ICT user / Not Started for JST user; LA ending D 01:00 JST shows Inactive (hidden) for ICT user / Active for JST user (BR-06, Q3) | Boundary/range | BVA, Decision Table | Medium | Standard |
| CS-16 | AC-02 | TZ gap — user TZ ahead of location (Brisbane GMT+10 vs JST): LA starting D 23:30 JST shows Not Started for Brisbane user / Active for JST user (BR-06, Q3) | Boundary/range | BVA, Decision Table | Medium | Standard |

---

## 6. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| — | No data write; a wrong default cannot corrupt data. | — |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Default list content (CS-02, CS-03) | Core of the ticket — staff must see newly ordered future LAs; a wrong date boundary hides or wrongly shows students. | One dataset with 6 LAs (Active, start today, start tomorrow, far future, end today, end yesterday); assert each row and the item count. Declare `today`. |
| Reset behavior (CS-09) | Existing Qase PX-13084 asserted the opposite (restore defaults) until 2026-10-07; easy to mis-test. | Assert every filter field empty except Location, and that Inactive + other-AY rows appear after Save. |
| Lesson Master unchanged (CS-12) | Same component; implementation branches on `isLessonMaster`. A wrong branch changes Lesson Master silently. | Open Lesson Master student list and assert Active-only chip. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Timezone gap (CS-15, CS-16) | Status uses the user's Salesforce timezone (date only); VN QA / staff accounts on GMT+7 can see a different status than JST users for LAs near midnight. Rule not in spec (Q3). | Two users (or switch own user's Time Zone in Personal Settings) — same LA, compare by selecting only Active / only Not Started. Pick LA times so both users are on the same calendar date during the test (avoid running near midnight). |
| Two rows per student (CS-05) | Rows are per LA; users may report as duplicate. Confirmed expected. | Use Change Associated Course with future effective date (PX-1774 data). |
| Next-AY future LA (CS-06) | Business problem only partly solved by design; must behave predictably. | Decision table: AY default vs AY + next AY. |
| Filter state on location / view change (CS-11) | Confirmed: selection kept. Regressions here are easy to miss. | Customize selection, switch view, switch location, assert chips. |

---

## 7. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Default chips (CS-01) | PX-4639 (updated 2026-10-07) | Generic BDD, no data | ✅ New TC with explicit data + count |
| Default list content (CS-02) | PX-4639 | Generic | ✅ New TC (EP dataset) |
| Date boundaries (CS-03) | — | None | ✅ New TC |
| Inactive + Not Started LA (CS-04) | — | None | ✅ New TC |
| Two rows per LA (CS-05) | PX-1774 / PX-1775 create the data (LA side only) | Data setup | ✅ New TC (list side); PX-1774 + PX-1775 added to the run |
| Next-AY future LA (CS-06) | PX-13083 (current AY default) | AY default only | ✅ New TC |
| Change selection (CS-07) | PX-4640 | Generic "select statuses" | ✅ New TC (decision table) |
| Combined filters (CS-08) | PX-4652, PX-13084 steps 2–4 | Partial | ✅ New TC focused on Course Status default × others |
| Reset (CS-09) | PX-4653, PX-13084 step 5 (updated) | Covers clear | ✅ New TC asserting Course Status cleared → Inactive rows appear |
| Reload (CS-10) | — | None | ✅ New TC |
| Location / view change (CS-11) | — | None | ✅ New TC |
| Lesson Master default (CS-12) | — | None | ✅ New TC |
| JP labels (CS-13) | — | None | ✅ New TC |
| CM role (CS-14) | — | None | ✅ Merged into CS-01 TC as a second run role (no separate TC) |
| TZ gap behind (CS-15) | — | None | ✅ New TC |
| TZ gap ahead (CS-16) | — | None | ✅ New TC |
| Additional Fields on Lesson forms | — | — | ❌ Out of suite — manual by QA owner |

**Regression run (existing, unchanged expectations):** PX-4640, PX-4653, PX-13083, PX-4637, PX-4652, PX-4631, PX-4632.
**Updated existing:** PX-4639, PX-13084.
**Impact (requested in run):** PX-1774, PX-1775.

**Test run plan (QA owner, 2026-10-07):** all new LT-108376 TCs + PX-1774 + PX-1775 + PX-4639 + PX-13084.

---

## 8. Suggested Test Suite Structure

```
epics/calendar/LT-108376-not-started-default-student-filter/test-cases/
└── student-course-status-default.md (+ .csv)
      → AC-01, AC-02, Scope — CS-01..CS-16 (~15 TCs; CS-14 merged into CS-01)
```

One file: all cases share the same surface (Lesson Calendar Student list filter) and the same LA dataset.
