# Test Cases: LT-98530 — [Riso] OOP | Contract and Monthly Lesson history (App)

> **Confirmed 2026-08-13:** This Riso App follows AC01.2: Cancelled lessons are excluded. The sibling SF report's status-agnostic calculation is an intentional divergence and is not an alternate expected result here.

- **Academic Year boundary rule:** Student sessions dated before Academic Year start or after Academic Year end do not contribute to Lesson Allocated, even when their dates are on or before the selected month's End-of-Month.

## Suite: [Riso] Lesson Allocated Calculation

### [Riso] Lesson Allocated – Session Date Within Academic Year – Included in Count

**Description:** AC01.2 — BVA — A student session with Lesson Date within the current Academic Year is included in the Lesson Allocated count.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has one student session on 2025-09-10, within AY 2025-04-01 to 2026-03-31, status Completed, Attendance = Present

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the month selector to September 2025 and view the LA card | Lesson Allocated count includes this session (count = 1) | session_date=2025-09-10; AY=2025-04-01 to 2026-03-31; expected=included |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocated – Sessions Outside Academic Year at Both Boundaries – Excluded

**Description:** AC01.2 — BVA (both Academic Year boundaries) — Student sessions dated one day before Academic Year start and one day after Academic Year end are both excluded, even though both are on or before the selected month's End-of-Month.

**Preconditions:**
- The Student is logged in to the Riso Learner App.
- The Lesson Allocation belongs to Academic Year 2025-04-01 to 2026-03-31.
- The Student has two assigned student sessions with Lesson Status=Completed and Attendance=Present: 2025-03-31 and 2026-04-01.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student selects April 2026 in the Contract Info month selector and views the Lesson Allocation card | The Lesson Allocated count does not include either session | academic_year_start=2025-04-01; academic_year_end=2026-03-31; selected_month=2026-04; selected_month_EOM=2026-04-30; session_1=2025-03-31 < AY start; session_2=2026-04-01 > AY end; both ≤ selected_month_EOM; expected=both excluded |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocated – Multiple Assigned Lessons Within Selected Month – Completed, Draft, and Published Counted

**Description:** AC01.2 — Decision Table / Data Integrity — All assigned student sessions in the selected month are counted when their lessons are Completed, Draft, or Published, are within the Academic Year and before the selected-month End-of-Month, and have eligible attendance.

**Preconditions:**
- The Student is logged in to the Riso Learner App.
- The Lesson Allocation belongs to Academic Year 2025-04-01 to 2026-03-31.
- The Student is assigned to three lessons with one Present student session each: Completed on 2025-09-10, Draft on 2025-09-15, and Published on 2025-09-20.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student selects September 2025 in the Contract Info month selector and views the Lesson Allocation card | The Lesson Allocated count shows 3 | selected_month=2025-09; selected_month_EOM=2025-09-30; sessions=[Completed/2025-09-10/Present, Draft/2025-09-15/Present, Published/2025-09-20/Present]; assigned_student=true; expected=3 |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocated – Session at End-of-Month Boundary – Included

**Description:** AC01.2 — BVA (exact boundary) — A session with Lesson Date exactly on the End-of-Month of the selected month is included.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has one student session on 2025-09-30 (EOM of September), status Completed, Attendance = Present

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the month selector to September 2025 and view the LA card | Lesson Allocated count includes this session | session_date=2025-09-30; selected_month_EOM=2025-09-30 (exact boundary); expected=included |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocated – Session One Day After End-of-Month – Excluded

**Description:** AC01.2 — BVA (above boundary) — A session with Lesson Date one day after the End-of-Month of the selected month is excluded.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has one student session on 2025-10-01, status Completed, Attendance = Present

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the month selector to September 2025 and view the LA card | Lesson Allocated count does NOT include this session | session_date=2025-10-01; selected_month_EOM=2025-09-30; 2025-10-01 > 2025-09-30 (above boundary); expected=excluded |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocated – Cancelled Lesson Status – Excluded

**Description:** AC01.2 — Decision Table — A session on a Cancelled-status lesson is excluded from Lesson Allocated for the Riso App.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has one student session on a Cancelled-status lesson, date=2025-09-15, within range, Attendance = Present

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the month selector to September 2025 and view the LA card | Lesson Allocated count does NOT include this session | lesson_status=Cancelled; session_date=2025-09-15; expected=excluded |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocated – Attendance Absent With Notice In Advance – Session Included

**Description:** AC01.2 — Decision Table / Lesson-Learned Risk — A session where the student was Absent but gave advance notice must be INCLUDED in the count (does not consume a "missed" slot).

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has one student session, date=2025-09-12, Completed status, Attendance = Absent, Attendance Notice = "In Advance"

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the month selector to September 2025 and view the LA card | Lesson Allocated count includes this session | attendance=Absent; notice=In Advance; expected=included |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocated – Attendance Absent Without Advance Notice – Session Excluded

**Description:** AC01.2 — Decision Table / Lesson-Learned Risk — A session where the student was Absent with no advance notice must be EXCLUDED from the count.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has one student session, date=2025-09-13, Completed status, Attendance = Absent, Attendance Notice = none

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the month selector to September 2025 and view the LA card | Lesson Allocated count does NOT include this session | attendance=Absent; notice=none; expected=excluded |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocated – Attendance Present – Session Included

**Description:** AC01.2 — Decision Table / Lesson-Learned Risk — A session where the student attended (Present) must be INCLUDED, completing the 3-way compound-condition coverage required by the 2026-03-04 Nichibei incident guardrail.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has one student session, date=2025-09-14, Completed status, Attendance = Present

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the month selector to September 2025 and view the LA card | Lesson Allocated count includes this session | attendance=Present; expected=included |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocated – Month Boundary – Session Time Near Midnight JST vs UTC

**Description:** AC01.2 — BVA (mandatory timezone rule) — Lesson Date-to-month attribution for the Lesson Allocated count must use the JST-displayed date, not the raw UTC-stored value (mirrors the LT-96673 timezone risk pattern).

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has one student session stored as `2025-09-30 15:15 UTC` (= `2025-10-01 00:15 JST`), Completed status, Attendance = Present

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the month selector to October 2025 and view the LA card | Lesson Allocated count includes this session (attributed to October, the JST date) | session_utc=2025-09-30 15:15 UTC; session_jst=2025-10-01 00:15 JST; selected_month=2025-10; expected=included in October (JST) |
| 2 | Set the month selector to September 2025 and view the LA card | Lesson Allocated count does NOT include this session for September | selected_month=2025-09; expected=excluded from September |

**Severity:** major
**Priority:** high

---
