# Test Cases: LT-108382 — Student Lesson Report with Classroom

## Suite: Current AY and Report Display

### Student Lesson Report – Academic Year – Current-year lessons – Includes in-year past and future lessons only

**Description:** AC 02.1 — Decision Table / Boundary Value Analysis — The report includes the selected student's lessons inside the academic-year range and excludes an outside-range lesson.

**Preconditions:**

- Centre Staff A is logged in to Salesforce with access to Student A.
- The report's configured current academic year is AY 2026, from 2026-04-01 through 2027-03-31.
- Student A has Lesson Past on 2026-05-15.
- Student A has Lesson Future on 2027-02-15.
- Student A has Lesson Outside AY on 2026-03-31.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Centre Staff A opens Student A's Student Lesson Report. | The report opens for Student A using the current academic-year filter. | AY start = 2026-04-01; AY end = 2027-03-31 |
| 2 | Centre Staff A locates Lesson Past and Lesson Future in the report. | The report shows both Lesson Past and Lesson Future. | Past = 2026-05-15; Future = 2027-02-15 |
| 3 | Centre Staff A searches the report rows for Lesson Outside AY. | The report does not show Lesson Outside AY. | Outside AY = 2026-03-31 |

**Severity:** major
**Priority:** high

---

### Student Lesson Report – Lesson Date – JST/UTC date boundary – Applies the intended Japan date and AY scope

**Description:** AC 02.1 — Boundary Value Analysis / Regression — A lesson at the JST↔UTC calendar-date boundary remains in the intended Japan academic-year scope.

**Preconditions:**

- Centre Staff A is logged in to Salesforce with access to Student A.
- The report's configured current academic year is AY 2026, from 2026-04-01 through 2027-03-31 in Japan Standard Time.
- Student A has Boundary Lesson scheduled for 2026-04-01 00:30 JST, which is 2026-03-31 15:30 UTC.
- Student A has Outside Boundary Lesson scheduled for 2026-03-31 23:30 JST, which is 2026-03-31 14:30 UTC.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Centre Staff A opens Student A's Student Lesson Report. | The report opens with AY 2026 scope evaluated for Japan Standard Time. | AY start = 2026-04-01 JST; Boundary Lesson = 2026-04-01 00:30 JST (= 2026-03-31 15:30 UTC) |
| 2 | Centre Staff A locates Boundary Lesson in the report. | The report shows Boundary Lesson with Lesson Date 2026-04-01 and places it in AY 2026. | Display date = 2026-04-01 JST |
| 3 | Centre Staff A searches the report rows for Outside Boundary Lesson. | The report does not show Outside Boundary Lesson in AY 2026. | Outside date = 2026-03-31 23:30 JST (= 2026-03-31 14:30 UTC) |

**Severity:** major
**Priority:** high

---

### Student Lesson Report – Report row – Populated lesson – Shows every required field together

**Description:** AC 02.2 — Component — A populated lesson row presents the complete field set required for communication and attendance work.

**Preconditions:**

- Centre Staff A is logged in to Salesforce with access to Student A.
- Student A has Lesson Tokyo 01 in the current academic year.
- Lesson Tokyo 01 has Location Tokyo Center, Start Time 09:00, End Time 10:00, Teacher Taro, Classroom Room A, Attendance Status Present, and a linked Student Session.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Centre Staff A opens Student A's Student Lesson Report. | The report opens for Student A. | Student = Student A; Lesson = Lesson Tokyo 01 |
| 2 | Centre Staff A reads the Lesson Tokyo 01 row. | The same row shows Student Name, Lesson Date, Location, Start Time, End Time, Lesson Name, Lesson Teacher, Lesson Classroom, Attendance Status, Absent Reason, and Student Session. | Location = Tokyo Center; Time = 09:00–10:00; Teacher = Taro; Classroom = Room A; Status = Present |

**Severity:** major
**Priority:** high
