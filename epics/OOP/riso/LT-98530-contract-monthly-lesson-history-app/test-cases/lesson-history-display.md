# Test Cases: LT-98530 — [Riso] OOP | Contract and Monthly Lesson history (App)

## Suite: [Riso] Lesson History — Display & Navigation

### [Riso] Lesson History – Page Menu – Label Displayed

**Description:** AC02.1 — Component — The page menu entry shows the label "Lesson History".

**Preconditions:**
- Logged in as Student to the Riso Learner App

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the app main menu | Menu entry "Lesson History" is shown per the latest Figma icon | "" |

**Severity:** trivial
**Priority:** low

---

### [Riso] Lesson History – Month Navigator – Default Value – Current Month on Page Load

**Description:** AC02.1 — BVA — The Month Navigator defaults to "THIS month" (the current calendar month) when the page is first opened.

**Preconditions:**
- Logged in as Student to the Riso Learner App

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Lesson History page for the first time in the session | Month Navigator shows "July 2026" | today = 2026-07-27; expected default = 2026-07 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Lesson History – Month Navigator – Format Displayed – EN and JP Formats Rendered

**Description:** AC02.1 — Component — Month Navigator renders the exact EN "month year" and JP "YYYY年MM月" formats.

**Preconditions:**
- Logged in as Student to the Riso Learner App

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the Lesson History page in English locale, month = December 2025 | Month Navigator shows "December 2025" | locale = EN; month = 2025-12 |
| 2 | Switch to Japanese locale | Month Navigator shows "2025年12月" | locale = JP; month = 2025-12 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Lesson History – Month Navigator – Navigate to Previous and Next Month (Pending Confirmation on Boundary)

**Description:** AC02.1 — Boundary / Negative — User can move back and forward one month at a time; exact navigation boundary is undefined (spec Clarification Question #8), so this TC only asserts adjacent-month navigation works, not the far boundary.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Lesson History page open at July 2026

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Tap "Previous" | Month Navigator shows "June 2026" and the list updates to June's completed lessons | current=2026-07; expected after back=2026-06 |
| 2 | Tap "Next" twice | Month Navigator shows "August 2026" and the list updates to August's completed lessons | expected after 2x next from 2026-06 = 2026-08 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Lesson History – Empty State – No Completed Lessons in Selected Month (Pending Confirmation)

**Description:** AC02.1 — Negative — When the selected month has zero completed lessons, a "No data" placeholder is shown instead of an empty list. Exact copy is pending confirmation (spec gap).

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Student has zero completed lessons in November 2025

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate the Month Navigator to November 2025 | "No data" placeholder is shown (no crash, no blank list); exact copy pending confirmation | completed_lesson_count(2025-11) = 0 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Lesson History – Row Fields – All Required Fields Displayed Together for a Complete Lesson

**Description:** AC02.1 — Component — A single lesson row simultaneously shows Lesson Date, Lesson Time + Timeslot Name, Subject, Teacher, and Attendance.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Student has a Completed lesson on 2025-09-10 (Wednesday), 09:00-10:20, Timeslot "1限", Subject "Math", Teacher "John Smith", Attendance = Present

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson History for September 2025 and view the row | Row shows: Date "Sep 10 (Wed)", Time "09:00 - 10:20" + "1限", Subject "Math", Teacher "John Smith", Attendance "Present" — all together | date=2025-09-10 (Wed); time=09:00-10:20; timeslot=1限; subject=Math; teacher=John Smith; attendance=Present |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson History – Row Fields – Lesson With No Timeslot – Timeslot Portion Shown Blank

**Description:** AC02.1 — Negative (conditional field) — When a lesson has no Timeslot associated, only the start-end time is shown; the Timeslot Name portion is blank.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Student has a Completed lesson on 2025-09-11, 14:00-15:00, no Timeslot associated

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson History for September 2025 and view the row | Row shows Time "14:00 - 15:00" with no Timeslot Name line beneath it | timeslot=none; expected=time shown, timeslot line blank |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson History – Row Fields – Lesson With No Subject – Subject Shown Blank

**Description:** AC02.1 — Negative (conditional field) — When a lesson has no Subject set, the Subject field is shown blank.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Student has a Completed lesson on 2025-09-12 with no Subject set

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson History for September 2025 and view the row | Subject field is blank | subject=none; expected=blank |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson History – Row Fields – Lesson With Multiple Teachers – Names Comma-Separated

**Description:** AC02.1 — Negative (conditional field) — When a lesson has more than one teacher assigned, names are shown comma-separated.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Student has a Completed lesson on 2025-09-13 with 2 teachers assigned: "John Smith" and "Jane Doe"

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson History for September 2025 and view the row | Teacher field shows "John Smith, Jane Doe" | teachers=[John Smith, Jane Doe]; expected="John Smith, Jane Doe" |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson History – Row Fields – Lesson With No Teacher – Teacher Field Shown Blank

**Description:** AC02.1 — Negative (conditional field) — When a lesson has no teacher assigned, the Teacher field is shown blank.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Student has a Completed lesson on 2025-09-14 with no teacher assigned

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson History for September 2025 and view the row | Teacher field is blank | teachers=[]; expected=blank |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson History – Row Fields – Attendance With Notice – Notice Shown on New Line

**Description:** AC02.1 — Component (conditional field) — When an Attendance Notice exists, it is displayed on a new line below the Attendance status.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Student has a Completed lesson on 2025-09-15, Attendance = Absent, Attendance Notice = "In Advance"

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson History for September 2025 and view the row | Row shows "Absent" with "In Advance" on the line below | attendance=Absent; notice=In Advance; expected=2-line display |

**Severity:** major
**Priority:** high

---
