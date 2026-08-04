# Test Cases: LT-98530 — [Riso] OOP | Contract and Monthly Lesson history (App)

## Suite: [Riso] Contract Info — Display & List

### [Riso] Contract Info – Header – Student Selected – Icon and Full Name Displayed

**Description:** AC01.1 — Component — Header remains unchanged, showing the selected student's icon and full name.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Student "Yuki Tanaka" is the currently selected profile

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contract Info page from User Profile | Header shows the student's icon and the full name "Yuki Tanaka" | student = Yuki Tanaka |

**Severity:** trivial
**Priority:** low

---

### [Riso] Contract Info – Header – Edit Icon Tapped – Full Name Edit Field Opens

**Description:** AC01.1 — Component — Tapping the edit icon opens the existing full-name edit flow (unchanged behavior).

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Student "Yuki Tanaka" is the currently selected profile

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contract Info page | Header shows edit icon in the top-right corner | "" |
| 2 | Tap the edit icon | The full-name edit field opens pre-filled with "Yuki Tanaka" | student = Yuki Tanaka |

**Severity:** trivial
**Priority:** low

---

### [Riso] Contract Info – Static Text – Section Label and Info Banner Displayed

**Description:** AC01.1 — Component — Section header label and the data-timing info banner display the exact PRD-specified EN/JP text.

**Preconditions:**
- Logged in as Student to the Riso Learner App, English locale

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contract Info page | Section header shows "Contract Info" | locale = EN |
| 2 | View the info banner below the month selector | Banner shows "Due to the timing of data updates, new contract details may not be reflected immediately." | locale = EN |
| 3 | Switch app locale to Japanese and reopen the page | Section header shows "契約情報" and banner shows "データ更新のタイミングにより、新規ご契約内容が即座に反映されない場合がございます。" | locale = JP |

**Severity:** trivial
**Priority:** low

---

### [Riso] Contract Info – Month Selector – Default Value – Last Month of Current Academic Year

**Description:** AC01.1 — BVA — Month selector defaults to the last month of the current Academic Year on first page load.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Current Academic Year runs 2025-04-01 to 2026-03-31

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contract Info page for the first time in the session | Month selector defaults to "Mar 2026" | today = 2026-07-27; AY = 2025-04-01 to 2026-03-31; expected default = 2026-03 (last month of AY) |

**Severity:** minor
**Priority:** medium

---

### [Riso] Contract Info – Month Selector – Format Displayed – EN and JP Formats Rendered

**Description:** AC01.1 — Component — Month selector renders the exact EN "MM YYYY" and JP "YYYY年MM月" formats.

**Preconditions:**
- Logged in as Student to the Riso Learner App

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contract Info page in English locale, month = September 2025 | Month selector shows "Sep 2025" | locale = EN; month = 2025-09 |
| 2 | Switch to Japanese locale | Month selector shows "2025年9月" | locale = JP; month = 2025-09 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Contract Info – LA List – Filter Applied – Only Require-Allocation-True LAs in Current AY Shown

**Description:** AC01.1 — Decision Table — The LA list includes only Lesson Allocations with require_allocation = TRUE and Academic Year = Current AY.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Student has 3 LAs: LA-1 (require_allocation=TRUE, AY=Current), LA-2 (require_allocation=FALSE, AY=Current), LA-3 (require_allocation=TRUE, AY=Previous)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contract Info page | Only LA-1's card is displayed | LA-1: require_allocation=TRUE, AY=Current; expected = shown |
| 2 | Inspect the LA list for LA-2 and LA-3 | LA-2 and LA-3 are NOT displayed | LA-2: require_allocation=FALSE → hidden; LA-3: AY=Previous → hidden |

**Severity:** major
**Priority:** high

---

### [Riso] Contract Info – LA Card – All Required Fields Displayed Together

**Description:** AC01.1 — Component — A single LA card simultaneously shows Course Master Name, Academic Year, Location, Total Slot, and Lesson Allocated.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA-1 links to Location Course "Essential Course" (Course Master "Essential Course"), Academic Year = 2025, Location = "Location Name 01", Total Slot = 50, Lesson Allocated = 52 for the selected month

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contract Info page and view LA-1's card | Card shows all 5 fields together: "Essential Course", "2025", "Location Name 01", Total Slot "50", Lesson Allocated "52" | course=Essential Course; AY=2025; location=Location Name 01; total_slot=50; lesson_allocated=52 |

**Severity:** major
**Priority:** high

---

### [Riso] Contract Info – LA List – Sort Order – Ordered by Start Date, End Date, Created Date

**Description:** AC01.1 — Scenario — Multiple LA cards are ordered by LA start date ASC, then end date ASC, then created_at ASC.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Student has 3 qualifying LAs: LA-A (start=2025-04-01, end=2026-03-31, created=2025-03-01), LA-B (start=2025-04-01, end=2025-09-30, created=2025-03-05), LA-C (start=2025-06-01, end=2026-03-31, created=2025-05-01)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contract Info page | Cards appear in order: LA-B, LA-A, LA-C | LA-A: start=2025-04-01,end=2026-03-31; LA-B: start=2025-04-01,end=2025-09-30; LA-C: start=2025-06-01,end=2026-03-31; expected order = B (same start, earlier end), A, C (later start) |

**Severity:** minor
**Priority:** medium

---

### [Riso] Contract Info – LA List – Empty State – No Qualifying LA (Pending Confirmation)

**Description:** AC01.1 — Negative — When no LA matches the filter (require_allocation=TRUE AND Current AY), the page shows a graceful empty state. Exact copy is pending PM confirmation (spec Clarification Question #6); this TC asserts a placeholder is shown, not the literal text.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Student has zero LAs with require_allocation=TRUE for the Current AY

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Contract Info page | An empty-state placeholder is shown (no crash, no blank white screen); exact copy pending confirmation | qualifying_LA_count = 0 |

**Severity:** minor
**Priority:** medium

---
