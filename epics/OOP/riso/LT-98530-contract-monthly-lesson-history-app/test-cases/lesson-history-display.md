# Test Cases: LT-98530 — [Riso] OOP | Contract and Monthly Lesson history (App)

## Suite: [Riso] Lesson History — Display & Navigation

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

### [Riso] Translation – Lesson History – Menu – Labels and Date Formats

**Description:** AC02.1 — Translation — Lesson History menu, table labels, Month Navigator and Lesson Date formats follow the PRD Localization table.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Student has a Completed lesson on 2025-10-01 (Wednesday)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open the app main menu in English | Menu entry shows "Lesson History" | locale = EN |
| 2 | Open Lesson History in English for October 2025 | Month Navigator shows "October 2025"; labels show "Date", "Lesson Time", "Subject", "Teacher", and "Attendance"; the lesson date uses the "Oct 1"-style format followed by its day of week | locale = EN; month = 2025-10 |
| 3 | Switch to Japanese locale | Menu entry shows "授業履歴"; Month Navigator shows "2025年10月"; labels show "日付", "授業時間", "科目", "講師", and "出欠"; the lesson date uses the "10/1"-style format followed by its day of week | locale = JP; month = 2025-10 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Lesson History – Month Navigator – Navigate to Previous and Next Month

**Description:** AC02.1 — Boundary / Negative — User can move back and forward one month at a time without a specified navigation boundary. Each selected month displays qualifying Completed lessons or "No data".

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

### [Riso] Lesson History – Empty State – No Completed Lessons in Selected Month

**Description:** AC02.1 — Negative — When the selected month has zero Completed lessons, "No data" is shown.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Student has zero completed lessons in November 2025

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate the Month Navigator to November 2025 | "No data" is shown | completed_lesson_count(2025-11) = 0 |

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
| 1 | Open Lesson History for September 2025 and view the row | Row shows the lesson date, time with Timeslot Name, Subject, Teacher, and Attendance together | date=2025-09-10 (Wed); time=09:00-10:20; timeslot=1限; subject=Math; teacher=John Smith; attendance=Present |

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
