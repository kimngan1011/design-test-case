# Test Cases: LT-96673 — Monthly Lesson Count in Calendar Teacher Details

## Suite: [Riso] Monthly Lesson Count – Calendar Teacher Details

---

### [Riso] Calendar Teacher Details – Monthly Lesson Count – Count Shown When Teacher Selected

**Description:** AC 01.3 — Regression Analysis — The Monthly Lesson Count field is visible in the Teacher Details right panel when a teacher is selected on the SF Lesson Calendar.

**Preconditions:**

- Org is Riso OOP
- Today is in **April 2026**
- Teacher A is assigned to **4 lessons** in April 2026 (Published)
- User is logged in as CM or HQ

| #   | Action                                           | Expected Result                                                            | Test Data |
| --- | ------------------------------------------------ | -------------------------------------------------------------------------- | --------- |
| 1   | Navigate to the SF Lesson Calendar               | SF Calendar opens, showing the current month (April 2026)                  | ""        |
| 2   | On the left side teacher panel, select Teacher A | Teacher Details panel opens on the right                                   | ""        |
| 3   | Observe the Teacher Details right panel          | "Monthly Lesson Count" (今月の授業数) field is **visible** and shows **4** | ""        |

**Severity:** major
**Priority:** high

---

### [Riso] Calendar Teacher Details – Monthly Lesson Count – Count Uses Today's Month Not Calendar View Month

**Description:** AC 01.3 — Decision Table — When the calendar is showing a month different from today's month, the Monthly Lesson Count in Teacher Details still reflects today's month count, not the viewed month's count.

**Preconditions:**

- Org is Riso OOP
- Today is in **April 2026**
- Teacher B has:
  - **6 lessons** in **April 2026** (today's month, Published)
  - **2 lessons** in **February 2026** (past month, Published)

| #   | Action                                                                    | Expected Result                                                          | Test Data |
| --- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------ | --------- |
| 1   | Navigate to the SF Lesson Calendar                                        | Calendar opens in April 2026 view                                        | ""        |
| 2   | Select Teacher B in the left panel                                        | Teacher Details displays with Monthly Lesson Count = **6** (April count) | ""        |
| 3   | Navigate the calendar to **February 2026** (click "previous month" twice) | Calendar view changes to show February 2026 lessons                      | ""        |
| 4   | Observe Teacher B's Monthly Lesson Count in Teacher Details               | Count = **6** (still April 2026 count — NOT 2)                           | ""        |

**Severity:** major
**Priority:** high

---

### [Riso] Calendar Teacher Details – Monthly Lesson Count – Navigation to Next Month Does Not Change Count

**Description:** AC 01.3 — State Transition Testing — Navigating forward in the calendar does not change the Monthly Lesson Count in the Teacher Details panel.

**Preconditions:**

- Org is Riso OOP
- Today is in **April 2026**
- Teacher C has:
  - **3 lessons** in **April 2026** (today's month, Published)
  - **7 lessons** in **May 2026** (next month, Published)
- Teacher C is selected in the Calendar left panel; count = 3 is visible

| #   | Action                                                | Expected Result                                               | Test Data |
| --- | ----------------------------------------------------- | ------------------------------------------------------------- | --------- |
| 1   | Open SF Calendar in April 2026 view; select Teacher C | Teacher Details shows Monthly Lesson Count = **3**            | ""        |
| 2   | Click "next month" to navigate to May 2026            | Calendar view changes to May 2026                             | ""        |
| 3   | Observe Teacher C's Monthly Lesson Count              | Count = **3** (April — unchanged; NOT 7 which is May's count) | ""        |
| 4   | Click "next month" again to navigate to June 2026     | Calendar view changes to June 2026                            | ""        |
| 5   | Observe Teacher C's Monthly Lesson Count              | Count = **3** (April — still unchanged)                       | ""        |

**Severity:** major
**Priority:** high

---

### [Riso] Calendar Teacher Details – Monthly Lesson Count – Navigation to Previous Month Does Not Change Count

**Description:** AC 01.3 — State Transition Testing — Navigating backward in the calendar does not change the Monthly Lesson Count in the Teacher Details panel.

**Preconditions:**

- Org is Riso OOP
- Today is in **April 2026**
- Teacher D has:
  - **5 lessons** in **April 2026** (today's month, Published)
  - **1 lesson** in **March 2026** (previous month, Published)
- Teacher D is selected in the Calendar left panel; count = 5 is visible

| #   | Action                                                | Expected Result                                                 | Test Data |
| --- | ----------------------------------------------------- | --------------------------------------------------------------- | --------- |
| 1   | Open SF Calendar in April 2026 view; select Teacher D | Teacher Details shows Monthly Lesson Count = **5**              | ""        |
| 2   | Click "previous month" to navigate to March 2026      | Calendar view changes to March 2026                             | ""        |
| 3   | Observe Teacher D's Monthly Lesson Count              | Count = **5** (April — unchanged; NOT 1 which is March's count) | ""        |

**Severity:** major
**Priority:** high

---

### [Riso] Calendar Teacher Details – Monthly Lesson Count – Zero Lessons in Today's Month Shows 0

**Description:** AC 01.3 — Boundary Value Analysis — A teacher with no lessons in today's month shows "0" in the Monthly Lesson Count panel, not blank.

**Preconditions:**

- Org is Riso OOP
- Today is in **April 2026**
- Teacher E has **no lessons** assigned in April 2026 (no assignments of any status)
- Teacher E has lessons in other months (e.g., March 2026)

| #   | Action                                 | Expected Result                                               | Test Data |
| --- | -------------------------------------- | ------------------------------------------------------------- | --------- |
| 1   | Navigate to SF Lesson Calendar         | Calendar opens                                                | ""        |
| 2   | Select Teacher E in the left panel     | Teacher Details panel opens                                   | ""        |
| 3   | Observe the Monthly Lesson Count field | Count = **0** — the field is not blank, not empty, not a dash | ""        |

**Severity:** normal
**Priority:** medium

---

### [Riso] Calendar Teacher Details – Monthly Lesson Count – Count Includes All Locations

**Description:** AC 01.3 — Decision Table — The count in Calendar Teacher Details includes lessons the teacher is assigned to across all locations, not only the currently viewed calendar location.

**Preconditions:**

- Org is Riso OOP
- Today is in **April 2026**
- Teacher F is assigned to:
  - 3 lessons at **Location A** in April 2026 (Published)
  - 2 lessons at **Location B** in April 2026 (Published)
- User is viewing the SF Calendar scoped to Location A

| #   | Action                                 | Expected Result                                       | Test Data  |
| --- | -------------------------------------- | ----------------------------------------------------- | ---------- |
| 1   | Navigate to SF Calendar for Location A | Calendar opens showing Location A lessons             | Location A |
| 2   | Select Teacher F in the left panel     | Teacher Details panel opens                           | ""         |
| 3   | Observe Monthly Lesson Count           | Count = **5** (3 from Location A + 2 from Location B) | ""         |

**Severity:** major
**Priority:** high

---

### [Riso] Calendar Teacher Details – Monthly Lesson Count – Timezone Boundary Last Day of Month

**Description:** AC 01.3 — Boundary Value Analysis — A lesson on the last day of today's month at late evening local time is counted in today's month (not the next month), even though the UTC stored datetime is the following day.

**Preconditions:**

- Org is Riso OOP (Japan Standard Time, UTC+9)
- Today is in **April 2026**
- Teacher G is assigned to a lesson with:
  - Date: **April 30, 2026**
  - Time: **23:30 JST** (= May 1 00:30 UTC)
  - Status: Published
- Teacher G has no other lessons in April or May 2026

| #   | Action                                | Expected Result                                                        | Test Data |
| --- | ------------------------------------- | ---------------------------------------------------------------------- | --------- |
| 1   | Navigate to SF Calendar in April 2026 | Calendar displays April 2026                                           | ""        |
| 2   | Select Teacher G in the left panel    | Teacher Details panel opens                                            | ""        |
| 3   | Observe Monthly Lesson Count          | Count = **1** (April 30 23:30 JST lesson is counted in April, not May) | ""        |

**Severity:** critical
**Priority:** high

---

### [Riso] Calendar Teacher Details – Monthly Lesson Count – Switch Between Selected Teachers Updates Count

**Description:** AC 01.3 — State Transition Testing — When multiple teachers are selected on the Calendar and the user switches focus between them, the Monthly Lesson Count in Teacher Details updates to reflect the newly focused teacher's count.

**Preconditions:**

- Org is Riso OOP
- Today is in **April 2026**
- Teacher A has **4 lessons** in April 2026 (Published)
- Teacher B has **9 lessons** in April 2026 (Published)
- Both Teacher A and Teacher B are visible in the Calendar left panel

| #   | Action                                             | Expected Result                                                 | Test Data |
| --- | -------------------------------------------------- | --------------------------------------------------------------- | --------- |
| 1   | Navigate to the SF Lesson Calendar                 | Calendar opens in April 2026 view                               | ""        |
| 2   | Select Teacher A in the left panel to view details | Teacher Details panel opens for Teacher A; Count = **4**        | ""        |
| 3   | Select Teacher B in the left panel to view details | Teacher Details panel updates to Teacher B; Count = **9**       | ""        |
| 4   | Select Teacher A again in the left panel           | Teacher Details panel switches back to Teacher A; Count = **4** | ""        |

**Severity:** major
**Priority:** high

---

### [Riso] Calendar Teacher Details – Monthly Lesson Count – Each Teacher's Count Is Independent

**Description:** AC 01.3 — Decision Table — When multiple teachers are active as calendar filters, the Monthly Lesson Count shown for each teacher reflects only that individual teacher's lesson count for today's month, not the combined total.

**Preconditions:**

- Org is Riso OOP
- Today is in **April 2026**
- Teacher A has **4 lessons** in April 2026 (Published)
- Teacher B has **9 lessons** in April 2026 (Published)
- Both Teacher A and Teacher B are selected as calendar filters (their lessons are visible on the calendar grid)

| #   | Action                                                                   | Expected Result                                                             | Test Data |
| --- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------- | --------- |
| 1   | Navigate to SF Calendar; enable both Teacher A and B as calendar filters | Calendar shows lessons from both teachers on the grid                       | ""        |
| 2   | Click on Teacher A's row in the left panel to open details               | Teacher Details shows Teacher A's Monthly Lesson Count = **4** (NOT 4+9=13) | ""        |
| 3   | Click on Teacher B's row in the left panel to open details               | Teacher Details shows Teacher B's Monthly Lesson Count = **9** (NOT 4+9=13) | ""        |

**Severity:** major
**Priority:** high

---

### [Riso] Calendar Teacher Details – Monthly Lesson Count – Deselect Teacher Clears Panel

**Description:** AC 01.3 — State Transition Testing — When the currently viewed teacher is deselected from the Calendar left panel, the Teacher Details panel (and the Monthly Lesson Count) is no longer shown.

**Preconditions:**

- Org is Riso OOP
- Today is in **April 2026**
- Teacher A has **4 lessons** in April 2026 (Published)
- Teacher A is selected and Teacher Details showing count = 4

| #   | Action                                             | Expected Result                                                                  | Test Data |
| --- | -------------------------------------------------- | -------------------------------------------------------------------------------- | --------- |
| 1   | Open SF Calendar; select Teacher A to view details | Teacher Details panel shows Monthly Lesson Count = **4**                         | ""        |
| 2   | Deselect Teacher A from the left panel             | Teacher Details panel closes or hides; Monthly Lesson Count is no longer visible | ""        |

**Severity:** normal
**Priority:** medium
