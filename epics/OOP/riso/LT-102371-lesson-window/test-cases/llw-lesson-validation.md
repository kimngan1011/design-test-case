# Test Cases: LT-102371 — [Riso] OOP | Lesson Window

## Suite: [Riso] LLW – Lesson Validation

---

### [Riso] Lesson Creation – LLW Validation – SF Lesson List – Date in Complete LLW – Creation blocked

**Description:** AC-09, BR-02 — Decision Table (negative) — Creating a lesson from the SF Lesson List with a date that falls within a Complete LLW for the same location is blocked.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW exists: Location A, AY = 2026, Start Date = 2026-07-01, End Date = 2026-07-31, Status = **Complete**
- Navigate to the SF Lesson List → New Lesson form

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | In the New Lesson form, set Location = **Location A** and Lesson Date = **2026-07-15** | Fields are filled | today = 2026-07-14; lesson_date = 2026-07-15; llw_start = 2026-07-01; llw_end = 2026-07-31; llw_status = Complete |
| 2 | Fill in other required lesson fields (teacher, time, etc.) and click **Save** | Save is **blocked** | — |
| 3 | Observe the error message | Error reads: **"Selected lesson date is already closed."** | expected_error = "Selected lesson date is already closed." |
| 4 | Confirm no lesson record was created | The lesson does not appear in the Lesson List | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Creation – LLW Validation – Lesson Schedule Detail Page – Date in Complete LLW – Creation blocked

**Description:** AC-09, BR-02 — Decision Table (negative) — Creating a lesson from the Lesson Schedule detail page with a date in a Complete LLW is blocked.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW: Location A, Start = 2026-07-01, End = 2026-07-31, Status = Complete
- Navigate to a Lesson Schedule detail page for Location A → Add Lesson from Schedule

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set Lesson Date = **2026-07-20** for Location A | Date entered | lesson_date = 2026-07-20; location = Location A |
| 2 | Click **Save** | Save is **blocked** | — |
| 3 | Observe the error message | Error: **"Selected lesson date is already closed."** | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Creation – LLW Validation – SF Calendar – Date in Complete LLW – Creation blocked

**Description:** AC-09, BR-02 — Cross-system, Regression (negative) — Creating a lesson via the SF Calendar by clicking a date that falls within a Complete LLW is blocked.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW: Location A, Start = 2026-07-01, End = 2026-07-31, Status = Complete
- Navigate to the SF Calendar view

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Click on **July 18, 2026** on the SF Calendar to create a new lesson for Location A | New lesson creation form opens | lesson_date = 2026-07-18; location = Location A |
| 2 | Fill in lesson details and click **Save** | Save is **blocked** | — |
| 3 | Observe the error | Error: **"Selected lesson date is already closed."** | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Creation – LLW Validation – CSV Import – Date in Complete LLW – Import blocked

**Description:** AC-09, BR-02 — Cross-system, Regression (negative) — Importing a lesson schedule via CSV where the Lesson Date falls within a Complete LLW is blocked.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW: Location A, Start = 2026-07-01, End = 2026-07-31, Status = Complete
- Prepared CSV file with one lesson row: Location = Location A, Lesson Date = **2026-07-25**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the Lesson Schedule CSV import feature | Import form is shown | — |
| 2 | Upload the CSV file with lesson date **2026-07-25** for Location A | File is uploaded | lesson_date = 2026-07-25; llw_range = 2026-07-01 to 2026-07-31 |
| 3 | Start the import | Import is **blocked** or the row is rejected | — |
| 4 | Observe the error feedback | Error indicates the lesson date is in a closed period: **"Selected lesson date is already closed."** | — |
| 5 | Confirm no lesson was created for 2026-07-25 | Lesson does not exist in the system | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Creation – LLW Validation – Recurring Lesson – Date in Complete LLW – Creation blocked

**Description:** AC-09, BR-02 — Decision Table (negative) — Creating a recurring lesson series where the recurrence dates fall within a Complete LLW is blocked.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW: Location A, Start = 2026-07-01, End = 2026-07-31, Status = Complete
- Attempting to create a recurring weekly lesson starting 2026-07-07 for Location A

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the New Recurring Lesson form, set Location = Location A, Start Date = **2026-07-07**, recurrence = weekly | Fields filled | lesson_date = 2026-07-07; recurrence = weekly; location = Location A |
| 2 | Click **Save** | Save is **blocked** | — |
| 3 | Observe the error | Error: **"Selected lesson date is already closed."** | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Creation – LLW Validation – BVA – Lesson Date Equals Start Date of Complete LLW – Blocked (inclusive)

**Description:** AC-09, BR-02 — BVA — A lesson date exactly equal to the Start Date of a Complete LLW is blocked (inclusive boundary).

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW: Location A, Start Date = **2026-07-01**, End Date = 2026-07-31, Status = Complete

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Attempt to create a lesson for Location A with Lesson Date = **2026-07-01** (= Start Date exactly) | Create attempted | today = 2026-07-14; lesson_date = 2026-07-01; llw_start = 2026-07-01 (inclusive boundary) |
| 2 | Click **Save** | Save is **blocked** | — |
| 3 | Observe the error | Error: **"Selected lesson date is already closed."** — start date is inclusive | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Creation – LLW Validation – BVA – Lesson Date Equals End Date of Complete LLW – Blocked (inclusive)

**Description:** AC-09, BR-02 — BVA — A lesson date exactly equal to the End Date of a Complete LLW is blocked (inclusive boundary).

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW: Location A, Start Date = 2026-07-01, End Date = **2026-07-31**, Status = Complete

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Attempt to create a lesson for Location A with Lesson Date = **2026-07-31** (= End Date exactly) | Create attempted | lesson_date = 2026-07-31; llw_end = 2026-07-31 (inclusive boundary) |
| 2 | Click **Save** | Save is **blocked** | — |
| 3 | Observe the error | Error: **"Selected lesson date is already closed."** — end date is inclusive | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Creation – LLW Validation – BVA – Lesson Date One Day Before Start Date – Creation allowed

**Description:** AC-09, BR-02 — BVA — A lesson date one day before the Start Date of a Complete LLW is allowed.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW: Location A, Start Date = **2026-07-01**, End Date = 2026-07-31, Status = Complete

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Attempt to create a lesson for Location A with Lesson Date = **2026-06-30** (= day before Start Date) | Create attempted | lesson_date = 2026-06-30; llw_start = 2026-07-01; gap = lesson_date < llw_start → allowed |
| 2 | Click **Save** | Lesson creation **succeeds** | — |
| 3 | Confirm the lesson is created | Lesson exists in the system with date 2026-06-30 | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Creation – LLW Validation – BVA – Lesson Date One Day After End Date – Creation allowed

**Description:** AC-09, BR-02 — BVA — A lesson date one day after the End Date of a Complete LLW is allowed.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW: Location A, Start Date = 2026-07-01, End Date = **2026-07-31**, Status = Complete

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Attempt to create a lesson for Location A with Lesson Date = **2026-08-01** (= day after End Date) | Create attempted | lesson_date = 2026-08-01; llw_end = 2026-07-31; gap = lesson_date > llw_end → allowed |
| 2 | Click **Save** | Lesson creation **succeeds** | — |
| 3 | Confirm the lesson is created | Lesson exists with date 2026-08-01 | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Creation – LLW Validation – Date Falls Outside All Complete LLW Ranges – Creation allowed

**Description:** AC-09, BR-02 — Equivalence Partitioning — Creating a lesson with a date that does not fall within any Complete LLW for that location succeeds.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW: Location A, July 2026 (2026-07-01–2026-07-31)
- No LLW exists for August 2026 for Location A

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Create a lesson for Location A with Lesson Date = **2026-08-15** (no LLW covers August) | Create attempted | lesson_date = 2026-08-15; no_complete_llw_for_august = true |
| 2 | Click **Save** | Lesson creation **succeeds** | — |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Creation – LLW Validation – Date in Open LLW Range – Creation allowed

**Description:** AC-09, BR-02 — Equivalence Partitioning — A lesson date that falls within an **Open** (not Complete) LLW is NOT blocked.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- LLW exists: Location A, Start = 2026-08-01, End = 2026-08-31, Status = **Open** (not Complete)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Create a lesson for Location A with Lesson Date = **2026-08-10** (within Open LLW) | Create attempted | lesson_date = 2026-08-10; llw_status = Open |
| 2 | Click **Save** | Lesson creation **succeeds** — Open status LLW does not block | — |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Creation – LLW Validation – Date in Complete LLW of Different Location – Creation allowed

**Description:** AC-09, BR-02 — Equivalence Partitioning — A lesson date falling within a Complete LLW of a **different location** does not block creation for the lesson's actual location.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW exists for **Location B**: Start = 2026-07-01, End = 2026-07-31, Status = Complete
- No Complete LLW exists for **Location A** in July 2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Create a lesson for **Location A** with Lesson Date = **2026-07-15** | Create attempted | lesson_date = 2026-07-15; lesson_location = Location A; complete_llw_location = Location B |
| 2 | Click **Save** | Lesson creation **succeeds** — LLW validation is location-specific | — |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Creation – LLW Validation – Error Message – English Text Shown Inline

**Description:** AC-10 — Component — The exact English error message is shown when lesson creation is blocked by a Complete LLW.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW: Location A, July 2026, Status = Complete
- Attempt to create a lesson on 2026-07-15 for Location A

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Fill in the lesson creation form with Lesson Date = 2026-07-15 for Location A and click **Save** | Save is blocked | lesson_date = 2026-07-15 |
| 2 | Observe the error message text | Error reads exactly: **"Selected lesson date is already closed."** | expected_message = "Selected lesson date is already closed." |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Creation – LLW Validation – Error Message – Japanese Text Shown

**Description:** AC-10 — Component — The exact Japanese error message is shown when the Riso org is in Japanese locale.

**Preconditions:**
- Riso SF org is set to Japanese locale (ja-JP)
- Complete LLW: Location A, July 2026, Status = Complete
- Attempt to create a lesson on 2026-07-15 for Location A

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Fill in the lesson creation form with Lesson Date = 2026-07-15 for Location A and click **Save** | Save is blocked | lesson_date = 2026-07-15 |
| 2 | Observe the error message text in Japanese | Error reads exactly: **"選択された授業期間は既に完了済です"** | expected_ja = "選択された授業期間は既に完了済です" |

**Severity:** minor
**Priority:** medium

---

### [Riso] Lesson – LLW Validation – Non-date Fields – Editable when lesson date is in a Complete LLW range

**Description:** AC-11 — Decision Table — Editing non-date fields (teacher, start time, etc.) on an existing lesson whose date falls in a Complete LLW range is not blocked.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW: Location A, Start = 2026-07-01, End = 2026-07-31, Status = Complete
- An existing lesson exists: Location A, Lesson Date = 2026-07-10 (within Complete LLW), Teacher = Teacher A

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the existing lesson (date = 2026-07-10, Location A) and click **Edit** | Edit form opens | lesson_date = 2026-07-10; llw_status = Complete |
| 2 | Change the **Teacher** field from Teacher A to **Teacher B** (do NOT change Lesson Date) | Teacher field is updated | new_teacher = Teacher B |
| 3 | Click **Save** | Save **succeeds** — only lesson date change to a Complete LLW range is blocked, not other fields | — |
| 4 | Confirm the Teacher field shows Teacher B | Record updated correctly | — |

**Severity:** minor
**Priority:** medium

---

### [Riso] Lesson Update – LLW Validation – Edit Form – Date Changed to Complete LLW Range – Update blocked

**Description:** AC-12, BR-06 — Decision Table (negative) — When editing an existing lesson and changing the Lesson Date to a date within a Complete LLW range, the update is blocked.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW: Location A, Start = 2026-07-01, End = 2026-07-31, Status = Complete
- Existing lesson: Location A, Lesson Date = **2026-08-10** (currently outside LLW)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the lesson (Lesson Date = 2026-08-10) and click **Edit** | Edit form opens | original_date = 2026-08-10 |
| 2 | Change Lesson Date to **2026-07-20** (within the Complete LLW range) | Date updated in form | new_date = 2026-07-20; llw_start = 2026-07-01; llw_end = 2026-07-31 |
| 3 | Click **Save** | Save is **blocked** | — |
| 4 | Observe the error message | Error: **"Selected lesson date is already closed."** | — |
| 5 | Confirm the lesson date remains **2026-08-10** | Update was not applied | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Update – LLW Validation – DnD on SF Calendar – Drag to Complete LLW Date – Move blocked

**Description:** AC-12, BR-06 — Cross-system, Regression (negative) — Dragging and dropping a lesson on the SF Calendar to a date within a Complete LLW range is blocked with an error.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW: Location A, Start = 2026-07-01, End = 2026-07-31, Status = Complete
- An existing lesson is scheduled on **2026-08-05** for Location A (outside LLW)
- Navigate to the SF Calendar view showing both July and August

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | On the SF Calendar, drag the lesson from **2026-08-05** and drop it on **2026-07-22** (within the Complete LLW) | DnD operation is attempted | original_date = 2026-08-05; target_date = 2026-07-22; llw_range = 2026-07-01 to 2026-07-31 |
| 2 | Observe the system response | DnD is **blocked** — lesson does not move to July 22 | — |
| 3 | Observe the error message | Error: **"Selected lesson date is already closed."** | — |
| 4 | Confirm the lesson remains on **2026-08-05** | Lesson date was not changed | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Update – LLW Validation – Edit Form – Date Changed from Complete LLW Range to Open Range – Update allowed

**Description:** AC-12 — Equivalence Partitioning — Editing a lesson to move its date FROM a Complete LLW range TO an open date is allowed (update is not blocked when new date is outside all Complete LLWs).

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW: Location A, July 2026 (2026-07-01–2026-07-31), Status = Complete
- No Complete LLW for August 2026 for Location A
- Existing lesson: Location A, Lesson Date = **2026-07-15** (within Complete LLW — but it was created before the LLW existed)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the lesson (date = 2026-07-15) and click **Edit** | Edit form opens | original_date = 2026-07-15 |
| 2 | Change Lesson Date to **2026-08-10** (outside all Complete LLWs) | Date field updated | new_date = 2026-08-10; no_complete_llw_in_aug = true |
| 3 | Click **Save** | Update **succeeds** — new date is not in any Complete LLW range | — |
| 4 | Confirm lesson date is now **2026-08-10** | Update applied | — |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Creation – LLW Validation – Retroactive LLW – Date in Past Complete LLW – Creation blocked

**Description:** AC-04, BR-02 — Decision Table — A LLW created retroactively (with Start Date in the past) blocks new lesson creation for that past date range.

**Preconditions:**
- Logged in as HQ Staff to the Riso Salesforce org
- A new LLW is created with Start Date = **2026-06-01**, End Date = **2026-06-30**, and immediately marked **Complete** (retroactive — June has already passed)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Create LLW: Location A, AY = 2026, Start = 2026-06-01, End = 2026-06-30, Status = Complete | LLW created | today = 2026-07-14; llw_start = 2026-06-01; llw_end = 2026-06-30 |
| 2 | Attempt to create a lesson for Location A with Lesson Date = **2026-06-15** (in the past retroactive LLW) | Create attempted | lesson_date = 2026-06-15 |
| 3 | Click **Save** | Creation is **blocked**: "Selected lesson date is already closed." | — |
| 4 | Confirm existing lessons with date 2026-06-15 (created before the LLW) are unaffected | Existing lessons remain; only new creation is blocked | — |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Creation – LLW Validation – Timezone Boundary – Date at JST Midnight – LLW uses JST date

**Description:** AC-09, BR-02 — BVA, Timezone — Lesson date validation uses JST (Japan Standard Time, UTC+9) for date comparison. A lesson created at 00:30 JST on July 1 falls within the July Complete LLW even though UTC date is still June 30.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW: Location A, AY = 2026, Start Date = **2026-07-01**, End Date = 2026-07-31, Status = Complete
- System/device is set to JST timezone

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Note the timezone context | today (JST) = 2026-07-01 00:30 JST = 2026-06-30 15:30 UTC; llw_start = 2026-07-01 |
| 2 | Attempt to create a lesson for Location A with Lesson Date = **2026-07-01** at 00:30 JST | Create attempted | lesson_date = 2026-07-01 (JST) |
| 3 | Click **Save** | Creation is **blocked** — Lesson Date 2026-07-01 (JST) is within the July Complete LLW | — |
| 4 | Observe the error | Error: **"Selected lesson date is already closed."** | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Creation – LLW vs ACI – Same Date in Both Complete LLW and ACI Closed Date – LLW error shown, ACI silent

**Description:** AC-09, Lesson-Learned Risk — Regression — When a lesson date falls within both a Complete LLW and an ACI closed date, the LLW validation shows an explicit error message; ACI silently skips without its own error.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW: Location A, July 2026, Status = Complete
- ACI Academic Calendar has **2026-07-15** marked as a closed date for Location A
- Attempt to create a lesson on **2026-07-15** for Location A

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Create a lesson: Location A, Lesson Date = **2026-07-15** (in both Complete LLW and ACI closed date) | Create attempted | lesson_date = 2026-07-15; llw_status = Complete; aci_closed = true |
| 2 | Click **Save** | Save is blocked | — |
| 3 | Observe the error message | Exactly **one** error message appears: **"Selected lesson date is already closed."** (from LLW) | expected_errors = 1 |
| 4 | Confirm ACI does NOT add its own separate error message | Only the LLW error is shown; ACI validation runs silently | — |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Update – LLW Validation – Timezone Boundary – Edit Lesson Date to JST Midnight – Blocked by JST Date LLW

**Description:** AC-12, BR-06 — BVA, Timezone — When editing a lesson's date to a timezone boundary date (00:30 JST = still previous UTC calendar date), the LLW validation uses JST date. If the JST date falls within a Complete LLW, the update is blocked.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW: Location A, Start Date = **2026-07-01**, End Date = 2026-07-31, Status = Complete
- Existing lesson: Location A, Lesson Date = **2026-08-10** (currently outside LLW)
- System/device is set to JST timezone

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Note the timezone context | today (JST) = 2026-07-14; editing lesson date to 2026-07-01 (JST) = 2026-06-30 15:30 UTC; llw_start = 2026-07-01 (JST inclusive) |  |
| 2 | Open the lesson (date = 2026-08-10) and click **Edit** | Edit form opens | original_date = 2026-08-10 |
| 3 | Change Lesson Date to **2026-07-01** (= JST date that equals LLW Start Date) | Date updated in form | new_date = 2026-07-01 (JST); UTC equivalent = 2026-06-30 15:30 UTC |
| 4 | Click **Save** | Update is **blocked** — LLW validation uses JST date 2026-07-01 which is within the Complete LLW | — |
| 5 | Observe the error message | Error: **"Selected lesson date is already closed."** | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Update – LLW Validation – Timezone – DnD on SF Calendar to JST Midnight Date – Blocked by JST Date LLW

**Description:** AC-12, BR-06 — BVA, Timezone — Dragging and dropping a lesson to a date that is the first day of a Complete LLW at JST midnight (00:30 JST) is blocked, as the system evaluates the drop target date in JST.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW: Location A, Start Date = **2026-07-01**, End Date = 2026-07-31, Status = Complete
- Existing lesson scheduled on **2026-08-10** for Location A
- SF Calendar is open; device clock is at **2026-07-01 00:30 JST** (= 2026-06-30 15:30 UTC)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Note the timezone context | device_time = 2026-07-01 00:30 JST (= 2026-06-30 15:30 UTC); DnD target = 2026-07-01 (JST calendar cell); llw_start = 2026-07-01 |  |
| 2 | On the SF Calendar, drag the lesson from **2026-08-10** and drop it onto the **July 1** calendar cell | DnD attempted | target_date = 2026-07-01 (JST) |
| 3 | Observe the result | DnD is **blocked** — July 1 (JST) is the Start Date of the Complete LLW (inclusive) | — |
| 4 | Observe the error message | Error: **"Selected lesson date is already closed."** | — |
| 5 | Confirm the lesson remains on **2026-08-10** | Lesson date was not changed | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Creation – LLW Validation – Available Teacher Calendar – Lesson date in Complete LLW – Creation blocked

**Description:** AC-09, BR-02 — Decision Table (negative) — Creating a lesson via the Available Teacher Calendar (select date → select available teacher → select student → select course → click Create Lesson) is blocked when the selected date falls within a Complete LLW for the same location.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW exists: Location = Riso Test, AY = 2026, Start Date = 2026-07-01, End Date = 2026-07-31, Status = **Complete**
- Navigate to the Available Teacher Calendar and set Location = **Riso Test**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | On the calendar, click on **July 15, 2026** | The right panel shows the selected date (7/15 Wed) with Course and Select Available Teachers fields | lesson_date = 2026-07-15; location = Riso Test; llw_range = 2026-07-01 to 2026-07-31; llw_status = Complete |
| 2 | Select an available teacher from the teacher list | Teacher is selected and highlighted | — |
| 3 | Select a student from the **Select Student** field | Student is selected (e.g., Student Riso 01) | student = Student Riso 01 |
| 4 | Select a course | Course is selected | — |
| 5 | Click **+ Create Lesson** | Creation is **blocked** — error message appears | — |
| 6 | Observe the error message | Error: **"Selected lesson date is already closed."** | expected_error = "Selected lesson date is already closed." |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Creation – LLW Validation – Calendar Drag-and-Drop to Create – Lesson date in Complete LLW – Creation blocked

**Description:** AC-09, BR-02 — Decision Table (negative) — Creating a new lesson by clicking and dragging on an empty calendar slot that falls within a Complete LLW is blocked when the user attempts to save.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW exists: Location = Riso Test, AY = 2026, Start Date = 2026-07-01, End Date = 2026-07-31, Status = **Complete**
- Navigate to the SF Calendar view for Location = Riso Test

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | On the SF Calendar, click and drag on an empty slot for **July 15, 2026** to initiate new lesson creation | A lesson creation form or dialog appears with July 15 pre-selected as the lesson date | lesson_date = 2026-07-15; location = Riso Test; llw_range = 2026-07-01 to 2026-07-31; llw_status = Complete |
| 2 | Fill in the required fields (teacher, student, course) in the creation form | Fields are filled | — |
| 3 | Click **Save** or **Create Lesson** | Creation is **blocked** — error message appears | — |
| 4 | Observe the error message | Error: **"Selected lesson date is already closed."** | expected_error = "Selected lesson date is already closed." |
| 5 | Confirm no lesson is created on July 15 for this location | The calendar shows no new lesson on July 15 | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Update – LLW Validation – BO Edit – Lesson date changed to Complete LLW range – Update blocked

**Description:** AC-12, BR-06 — Decision Table (negative) — When editing an existing lesson's date on the Back Office (BO) to a date that falls within a Complete LLW for the same location, the update is blocked.

**Preconditions:**
- Logged in as HQ or CM Staff to the Back Office (BO)
- Complete LLW exists: Location = Riso Test, AY = 2026, Start Date = 2026-07-01, End Date = 2026-07-31, Status = **Complete**
- An existing lesson exists: Location = Riso Test, Lesson Date = **2026-08-10** (currently outside the LLW range)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | On the BO, navigate to the lesson (Lesson Date = 2026-08-10, Location = Riso Test) and click **Edit** | The lesson edit form opens | original_date = 2026-08-10; llw_start = 2026-07-01; llw_end = 2026-07-31 |
| 2 | Change the **Lesson Date** field to **2026-07-20** (within the Complete LLW range) | Lesson Date field updated to 2026-07-20 | new_date = 2026-07-20 |
| 3 | Click **Save** | Update is **blocked** — error message appears | — |
| 4 | Observe the error message | Error: **"Selected lesson date is already closed."** | expected_error = "Selected lesson date is already closed." |
| 5 | Confirm the lesson date remains **2026-08-10** | The lesson was not updated | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Creation – LLW Validation – Complete LLW same location but different Academic Year – Creation allowed

**Description:** AC-09, BR-02 — Equivalence Partitioning — A Complete LLW for the same location but a **different Academic Year** does NOT block lesson creation. Lesson blocking only applies when the Complete LLW matches both the same location AND the same Academic Year as the lesson.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW exists: Location A, **AY = 2025**, Start Date = 2026-01-01, End Date = 2026-01-31, Status = Complete
- No Complete LLW exists for Location A under **AY = 2026** for January 2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Establish test context: the Complete LLW belongs to AY = 2025; the lesson to be created belongs to AY = 2026 | AY mismatch — LLW (AY=2025) and lesson (AY=2026) are under different Academic Years | llw_AY = 2025; lesson_AY = 2026; lesson_date = 2026-01-15; location = Location A |
| 2 | Attempt to create a lesson for Location A with Lesson Date = **2026-01-15** (within the date range of the AY=2025 Complete LLW) | Create attempted | lesson_date = 2026-01-15; llw_start = 2026-01-01; llw_end = 2026-01-31; llw_status = Complete; llw_AY = 2025 ≠ lesson_AY = 2026 |
| 3 | Click **Save** | Lesson creation **succeeds** — the Complete LLW belongs to a different Academic Year and does not block | — |
| 4 | Confirm the lesson is created on 2026-01-15 | Lesson record exists; no error was shown | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Update – LLW Validation – Edit Single Occurrence of Recurring Lesson – Date changed to Complete LLW range – Update blocked

**Description:** AC-12, BR-06 — Decision Table (negative) — When editing a single occurrence of a recurring lesson and changing its date to fall within a Complete LLW for the same location and Academic Year, the update is blocked.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW exists: Location A, AY = 2026, Start Date = 2026-07-01, End Date = 2026-07-31, Status = **Complete**
- A recurring lesson chain exists for Location A: weekly, starting 2026-08-03 (all occurrences are outside the LLW range)
- Open the **single occurrence** for **2026-08-10** to edit (edit only this lesson)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the recurring lesson occurrence on 2026-08-10 and select **Edit this lesson only** | Edit form opens for the single occurrence | original_date = 2026-08-10; recurrence = weekly; location = Location A |
| 2 | Change Lesson Date to **2026-07-20** (within the Complete LLW range) | Lesson Date updated to 2026-07-20 in the form | new_date = 2026-07-20; llw_start = 2026-07-01; llw_end = 2026-07-31; llw_AY = 2026 |
| 3 | Click **Save** | Update is **blocked** — error message appears | — |
| 4 | Observe the error message | Error: **"Selected lesson date is already closed."** | expected_error = "Selected lesson date is already closed." |
| 5 | Confirm the occurrence date remains **2026-08-10** | The single occurrence was not updated; the rest of the recurring chain is unaffected | — |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Update – LLW Validation – Edit This and Following Occurrences of Recurring Lesson – New dates in Complete LLW range – Update blocked

**Description:** AC-12, BR-06 — Decision Table (negative) — When editing "this and following" occurrences of a recurring lesson with a new start date that falls within a Complete LLW for the same location and Academic Year, the update is blocked.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org
- Complete LLW exists: Location A, AY = 2026, Start Date = 2026-07-01, End Date = 2026-07-31, Status = **Complete**
- A recurring lesson chain exists for Location A: weekly, starting 2026-08-03 (all occurrences outside LLW)
- Open the occurrence on **2026-08-10** to edit with **Edit this and following lessons**

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the recurring lesson occurrence on 2026-08-10 and select **Edit this and following lessons** | Edit form opens affecting 2026-08-10 and all subsequent occurrences | original_start_date = 2026-08-10; recurrence = weekly; location = Location A |
| 2 | Change the Lesson Date (new chain start) to **2026-07-14** (within the Complete LLW range) | New start date updated to 2026-07-14 in the form | new_start_date = 2026-07-14; llw_start = 2026-07-01; llw_end = 2026-07-31; llw_AY = 2026 |
| 3 | Click **Save** | Update is **blocked** — error message appears | — |
| 4 | Observe the error message | Error: **"Selected lesson date is already closed."** | expected_error = "Selected lesson date is already closed." |
| 5 | Confirm all occurrences from 2026-08-10 onward remain unchanged | The recurring chain was not modified | — |

**Severity:** critical
**Priority:** high
