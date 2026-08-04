# Test Cases: LT-98530 — [Riso] OOP | Contract and Monthly Lesson history (App)

> ⚠️ **Pending Confirmation:** The status-filter test cases below validate the PRD's stated "Status = Completed" rule, which the PRD's own inline comment marks as unresolved ("TBC → Cancelled"). See spec Clarification Question #3.

## Suite: [Riso] Lesson History — Filter & Sort (Pending Confirmation)

### [Riso] Lesson History – Status Filter – Completed Lesson Included

**Description:** AC02.1 — Decision Table — A lesson with Status = Completed is included in the Lesson History list.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Student has a lesson on 2025-09-05 with Status = Completed

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson History for September 2025 | The lesson on 2025-09-05 is shown in the list | lesson_status=Completed; expected=included |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson History – Status Filter – Published Lesson Not Yet Occurred – Excluded

**Description:** AC02.1 — Decision Table / Negative — A lesson with Status = Published (scheduled but not yet completed) must NOT appear in Lesson History, since only Completed lessons belong in past-lesson history.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Student has a future lesson on 2025-09-25 with Status = Published

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson History for September 2025 | The lesson on 2025-09-25 is NOT shown in the list | lesson_status=Published; expected=excluded |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson History – Status Filter – Cancelled Lesson – Excluded (Pending Confirmation)

**Description:** AC02.1 — Decision Table / Negative — A Cancelled-status lesson is excluded from Lesson History, per the PRD's background RFP intent ("only completed lesson should be listed"). The PRD's own inline comment marks this as unresolved ("TBC → Cancelled") — spec Clarification Question #3.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Student has a lesson on 2025-09-08 with Status = Cancelled

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson History for September 2025 | The lesson on 2025-09-08 is NOT shown in the list (pending confirmation this remains correct) | lesson_status=Cancelled; expected=excluded (pending confirmation) |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson History – Month Filter – Lesson Date Outside Selected Month – Excluded

**Description:** AC02.1 — Decision Table — A Completed lesson whose date falls outside the selected month is excluded from the list.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Student has a Completed lesson on 2025-08-30 and another on 2025-10-01

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson History for September 2025 | Neither the 2025-08-30 nor the 2025-10-01 lesson is shown | selected_month=2025-09; lesson_dates=[2025-08-30, 2025-10-01]; expected=both excluded |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson History – Sort Order – Same-Day Lessons Ordered by Start Time Ascending

**Description:** AC02.1 — Scenario — Multiple Completed lessons on the same day are ordered by Lesson start time ascending.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Student has 2 Completed lessons on 2025-09-10: Lesson-A (14:00-15:00) and Lesson-B (09:00-10:00)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson History for September 2025 | Lesson-B (09:00) appears before Lesson-A (14:00) | Lesson-A start=14:00; Lesson-B start=09:00; expected order = B, A |

**Severity:** minor
**Priority:** medium

---

### [Riso] Lesson History – Month Boundary – Lesson Time Near Midnight JST vs UTC

**Description:** AC02.1 — BVA (mandatory timezone rule) — Lesson Date-to-month attribution for the Lesson History filter must use the JST-displayed date, not the raw UTC-stored value.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- Student has a Completed lesson stored as `2025-08-31 15:05 UTC` (= `2025-09-01 00:05 JST`)

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Lesson History for September 2025 | The lesson appears in September's list (JST date) | lesson_utc=2025-08-31 15:05 UTC; lesson_jst=2025-09-01 00:05 JST; selected_month=2025-09; expected=included in September (JST) |
| 2 | Open Lesson History for August 2025 | The lesson does NOT appear in August's list | selected_month=2025-08; expected=excluded from August |

**Severity:** major
**Priority:** high

---
