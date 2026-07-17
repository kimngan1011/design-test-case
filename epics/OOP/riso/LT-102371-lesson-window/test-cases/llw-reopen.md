# Test Cases: LT-102371 — [Riso] OOP | Lesson Window

## Suite: [Riso] LLW – Reopen

---

### [Riso] Location Lesson Window – Reopen – CM Staff – Current Month LLW – Status changes to Open

**Description:** AC-06, BR-03 — State Transition — A CM can reopen a Complete LLW whose month is the current calendar month.

**Preconditions:**
- Logged in as **CM Staff** assigned to Location A
- LLW exists: Location A, AY = 2026, Start Date = **2026-07-01**, End Date = **2026-07-31**, Status = **Complete**
- Navigate to Account detail page for Location A → Lesson Window tab

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Locate the July LLW record (Status = Complete) | Record is visible | today = 2026-07-14; llw_month = July 2026 (= current month) |
| 2 | Click the **Reopen** action on the July LLW | Reopen action is available and triggered | — |
| 3 | Observe the **Status** field | Status changes to **Open** | — |
| 4 | Confirm no error message is shown | Action succeeds without restriction | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Location Lesson Window – Reopen – CM Staff – Preceding Month LLW (BVA) – Status changes to Open

**Description:** AC-06, BR-03 — BVA — A CM can reopen a Complete LLW whose month is the immediately preceding calendar month (boundary: exactly 1 month ago).

**Preconditions:**
- Logged in as **CM Staff** assigned to Location A
- LLW exists: Location A, AY = 2026, Start Date = **2026-06-01**, End Date = **2026-06-30**, Status = **Complete**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to Account detail page for Location A → Lesson Window tab and locate the June LLW | Record is visible | today = 2026-07-14; llw_month = June 2026 (= immediately preceding month) |
| 2 | Click **Reopen** on the June LLW | Action is triggered | — |
| 3 | Observe the **Status** field | Status changes to **Open** | — |
| 4 | Confirm no error message is shown | CM can reopen the preceding month — allowed | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Location Lesson Window – Reopen – CM Staff – First Day of Current Month (BVA) – Preceding Month Reopen Still Allowed

**Description:** AC-06, BR-03 — BVA — On the first day of a new month, the CM can still reopen the previous month's LLW (preceding month rule applies).

**Preconditions:**
- Logged in as **CM Staff** assigned to Location A
- Today is the **first day of the current month** (2026-08-01)
- LLW exists for July 2026 (2026-07-01–2026-07-31), Status = **Complete**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Note that today is the first day of August | today = 2026-08-01; llw_month = July 2026 (= immediately preceding month) |  |
| 2 | Click **Reopen** on the July LLW | Reopen action is triggered | — |
| 3 | Observe the **Status** field | Status changes to **Open** — preceding month rule still allows this | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Location Lesson Window – Reopen – CM Staff – Two Months Ago LLW (BVA) – Reopen blocked

**Description:** AC-07, BR-03 — BVA (negative) — A CM cannot reopen a Complete LLW whose month is 2 months ago (one beyond the allowed boundary).

**Preconditions:**
- Logged in as **CM Staff** assigned to Location A
- LLW exists: Location A, AY = 2026, Start Date = **2026-05-01**, End Date = **2026-05-31**, Status = **Complete** (May = 2 months ago when today = July)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Lesson Window tab and locate the May LLW | Record is visible | today = 2026-07-14; llw_month = May 2026 (= 2 months ago) |
| 2 | Click **Reopen** on the May LLW | Reopen action is attempted | — |
| 3 | Observe the system response | Reopen is **blocked** | — |
| 4 | Observe the error message (English) | Error reads: **"This window can no longer be reopened. Please contact HQ."** | — |
| 5 | Confirm the Status remains **Complete** | Status has not changed | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Location Lesson Window – Reopen – CM Staff – Blocked – English Error Message Content

**Description:** AC-07 — Component — When CM's reopen attempt is blocked, the English error message text is exactly correct.

**Preconditions:**
- Logged in as **CM Staff** assigned to Location A
- Complete LLW exists for a month older than 1 month prior (e.g., May 2026)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Attempt to reopen the old Complete LLW (May 2026) | Reopen is blocked | today = 2026-07-14; llw_month = May 2026 |
| 2 | Observe the exact error message text | Error text is exactly: **"This window can no longer be reopened. Please contact HQ."** | expected_message = "This window can no longer be reopened. Please contact HQ." |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – Reopen – CM Staff – Blocked – Japanese Error Message Content

**Description:** AC-07 — Component — When CM's reopen attempt is blocked, the Japanese error message text is exactly correct.

**Preconditions:**
- Riso SF org is set to Japanese locale (ja-JP)
- Logged in as **CM Staff** assigned to Location A
- Complete LLW exists for May 2026 (older than 1 month prior)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Attempt to reopen the May 2026 Complete LLW | Reopen is blocked | today = 2026-07-14 |
| 2 | Observe the error message in Japanese | Error text is exactly: **"未完了状態に戻すことはできません。本部に連絡してください。"** | expected_ja = "未完了状態に戻すことはできません。本部に連絡してください。" |

**Severity:** minor
**Priority:** medium

---

### [Riso] Location Lesson Window – Reopen – CM Staff – 6 Months Ago – Reopen blocked

**Description:** AC-07, BR-03 — Negative — A CM cannot reopen a Complete LLW from 6 months ago (well beyond the allowed window).

**Preconditions:**
- Logged in as **CM Staff** assigned to Location A
- LLW exists: Start Date = **2026-01-01**, End Date = **2026-01-31**, Status = **Complete** (January = 6 months ago)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Attempt to click **Reopen** on the January 2026 LLW | Reopen is attempted | today = 2026-07-14; llw_month = Jan 2026 (6 months ago) |
| 2 | Observe the system response | Reopen is **blocked** with error: "This window can no longer be reopened. Please contact HQ." | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Location Lesson Window – Reopen – HQ Staff – Current Month LLW – Status changes to Open

**Description:** AC-08, BR-03 — State Transition — HQ Staff can reopen any Complete LLW including the current month.

**Preconditions:**
- Logged in as **HQ Staff** to the Riso Salesforce org
- LLW exists: Location A, July 2026, Status = **Complete**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Click **Reopen** on the July 2026 LLW | Action is triggered | today = 2026-07-14; llw_month = July 2026 |
| 2 | Observe the **Status** field | Status changes to **Open** | — |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – Reopen – HQ Staff – 6 Months Ago LLW – Reopen succeeds (no restriction)

**Description:** AC-08, BR-03 — State Transition — HQ Staff can reopen any Complete LLW regardless of how old the month is.

**Preconditions:**
- Logged in as **HQ Staff** to the Riso Salesforce org
- LLW exists: Location A, January 2026 (6 months ago), Status = **Complete**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Click **Reopen** on the January 2026 LLW | Reopen action is triggered | today = 2026-07-14; llw_month = Jan 2026 (6 months ago) |
| 2 | Observe the system response | Reopen **succeeds** with no error — HQ has no restriction | — |
| 3 | Observe the **Status** field | Status changes to **Open** | — |

**Severity:** major
**Priority:** high

---

### [Riso] Location Lesson Window – Reopen – After Reopen – Lesson Creation in Date Range Immediately Unblocked

**Description:** AC-06, AC-13 — State Transition — After a CM or HQ reopens a Complete LLW, lesson creation in that date range is immediately unblocked with no delay or cache.

**Preconditions:**
- Logged in as HQ Staff to the Riso Salesforce org
- LLW exists: Location A, AY = 2026, Start Date = 2026-07-01, End Date = 2026-07-31, Status = **Complete**
- A lesson creation attempt on 2026-07-15 is currently blocked

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Confirm that creating a lesson on **2026-07-15** for Location A is blocked before reopen | Lesson creation blocked: "Selected lesson date is already closed." | lesson_date = 2026-07-15; location = Location A |
| 2 | Navigate to the LLW record for July 2026 and click **Reopen** | Status changes to **Open** | — |
| 3 | Immediately attempt to create a lesson on **2026-07-15** for Location A (no page refresh delay) | Lesson creation **succeeds** without any blocking error | — |
| 4 | Confirm the lesson is created | Lesson record exists with date 2026-07-15 | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Location Lesson Window – Reopen – Unblocked After Reopen – No Cache or Delay

**Description:** AC-13 — State Transition — The unblocking effect after Reopen is immediate; no cache or server delay prevents lesson creation.

**Preconditions:**
- Logged in as HQ Staff to the Riso Salesforce org
- LLW: Location A, July 2026, just reopened (Status changed from Complete → Open in this same session)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Without closing the browser or navigating away, attempt to create a lesson on **2026-07-22** for Location A | Lesson creation is attempted immediately after reopen | lesson_date = 2026-07-22 |
| 2 | Observe the result | Lesson creation **succeeds** — no error, no delay, no cache hit preventing creation | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Location Lesson Window – Reopen – CM Staff – Previous month window allowed, two months ago window blocked

**Description:** AC-06, AC-07, BR-03 — BVA — The CM reopen restriction has a boundary between M-1 (preceding month, allowed) and M-2 (2 months ago, blocked). LLW only stores Date fields, no timezone involved.

**Preconditions:**
- Logged in as CM Staff assigned to Location A
- today = 2026-07-15; M (current) = July 2026; M-1 (preceding, allowed boundary) = June 2026; M-2 (first blocked) = May 2026
- LLW A: Location A, Start = 2026-06-01, End = 2026-06-30 (June = M-1), Status = Complete
- LLW B: Location A, Start = 2026-05-01, End = 2026-05-31 (May = M-2), Status = Complete

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Establish BVA boundary anchor | Two LLW records exist: June (Complete) and May (Complete) | today = 2026-07-15; M-1 = June 2026 (last allowed month); M-2 = May 2026 (first blocked month) |
| 2 | Click Reopen on LLW A (June 2026, month = M-1 = last allowed boundary) | Reopen succeeds — Status changes to **Open**. June is exactly at the allowed boundary (M-1). | llw_month = June 2026; llw_start = 2026-06-01; llw_end = 2026-06-30 |
| 3 | Click Reopen on LLW B (May 2026, month = M-2 = first blocked boundary) | Reopen is **blocked**. Error: "This window can no longer be reopened. Please contact HQ." May is exactly one month past the allowed boundary. | llw_month = May 2026; llw_start = 2026-05-01; llw_end = 2026-05-31 |
| 4 | Confirm LLW B Status remains Complete | Status = Complete (unchanged) | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Location Lesson Window – Reopen – Lesson creation on window start and end date – Dates unblocked after window reopened

**Description:** AC-06, AC-13, BR-02 — BVA — After a Complete LLW is reopened (Status → Open), lesson dates at the LLW boundary dates (Start_Date and End_Date, both inclusive) become unblocked immediately. LLW stores Date only — no timezone involved.

**Preconditions:**
- Logged in as HQ Staff to the Riso Salesforce org
- LLW exists: Location A, AY = 2026, Start_Date = **2026-07-01**, End_Date = **2026-07-31**, Status = Complete
- No existing lessons on 2026-07-01 and 2026-07-31 for Location A

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Establish BVA boundary anchor: LLW range = [2026-07-01, 2026-07-31] (both inclusive) | LLW is Complete; both boundary dates are blocked | boundary_start = 2026-07-01 (Start_Date, inclusive); boundary_end = 2026-07-31 (End_Date, inclusive); llw_status = Complete |
| 2 | Attempt to create a lesson on **2026-07-01** (= Start_Date boundary) | Creation is **blocked**: "Selected lesson date is already closed." | lesson_date = 2026-07-01 |
| 3 | Attempt to create a lesson on **2026-07-31** (= End_Date boundary) | Creation is **blocked**: "Selected lesson date is already closed." | lesson_date = 2026-07-31 |
| 4 | Reopen the LLW (Status: Complete → Open) | Status changes to **Open** immediately | — |
| 5 | Attempt to create a lesson on **2026-07-01** (= Start_Date boundary) after reopen | Creation **succeeds** — boundary date is now unblocked | lesson_date = 2026-07-01 |
| 6 | Attempt to create a lesson on **2026-07-31** (= End_Date boundary) after reopen | Creation **succeeds** — boundary date is now unblocked | lesson_date = 2026-07-31 |

**Severity:** critical
**Priority:** high
