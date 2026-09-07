# Test Cases: LT-107410 — Auto-delete Student Sessions

## Suite: Withdrawal (Qase 2577)

### Lesson Allocation – Withdrawal – Future individual session – Student is removed from lesson

**Description:** AC-1 — Decision Table — A shortened individual LA removes only the future out-of-range session.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- Student A has an individual LA from `2026-01-01` to `2026-03-31` and three individual sessions: `2026-02-01`, `2026-02-08`, `2026-02-15`.
- `last_attendance_day = 2026-02-08`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Submit a Partial Withdrawal with Last Attendance Day `2026-02-08`. | The LA end date becomes `2026-02-08`. | `last_attendance_day = 2026-02-08` |
| 2 | Open the `2026-02-15` lesson and student assignment. | Student A is removed from the lesson and no longer active in its student list. | `lesson_date = 2026-02-15 > 2026-02-08` |

**Severity:** critical  
**Priority:** high

---

### Lesson Allocation – Withdrawal – Last attendance boundary – Past and boundary sessions retained

**Description:** AC-1, AC-6 — BVA — Sessions before and on the last attendance day remain available.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- Student A has individual sessions on `2026-02-07`, `2026-02-08`, and `2026-02-09`; the `2026-02-07` lesson is completed with attendance recorded.
- `last_attendance_day = 2026-02-08`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Submit a Partial Withdrawal with Last Attendance Day `2026-02-08`. | The withdrawal is completed with the LA ending on `2026-02-08`. | `last_attendance_day = 2026-02-08` |
| 2 | View the three Student Sessions. | Sessions dated `2026-02-07` and `2026-02-08` remain active; only the `2026-02-09` session is deleted. | Boundary: `<`, `=`, `>` `2026-02-08` |

**Severity:** critical  
**Priority:** high

---

### Lesson Allocation – Withdrawal – Lesson Allocation summary – Allocated count and status updated

**Description:** AC-1 — CRUD — Removing two future sessions updates the LA summary.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- Student A has an individual LA with `Lesson Allocated = 3`, status `Fully Assigned`, and sessions on `2026-02-01`, `2026-02-08`, `2026-02-15`.
- `last_attendance_day = 2026-02-08`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Submit a Partial Withdrawal with Last Attendance Day `2026-02-08`. | The future session on `2026-02-15` is removed. | `sessions_before = 3` |
| 2 | Open the student's Lesson Allocation detail. | `Lesson Allocated = 2` and the status reflects the two remaining sessions. | `expected_allocated = 2` |

**Severity:** critical  
**Priority:** high

---

### Lesson Allocation – Withdrawal – Lesson report detail – Removed student detail is deleted

**Description:** AC-1 — CRUD — Session deletion removes the dependent Lesson Report Detail.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce.
- Student A has an individual session and Lesson Report Detail on the `2026-02-15` lesson.
- `last_attendance_day = 2026-02-08`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Submit a Partial Withdrawal with Last Attendance Day `2026-02-08`. | The `2026-02-15` individual session is deleted. | `lesson_date = 2026-02-15` |
| 2 | Open the Lesson Report for the `2026-02-15` lesson. | Student A has no Lesson Report Detail in that lesson. | `student = A` |

**Severity:** critical  
**Priority:** high

---

### Lesson Allocation – Withdrawal – Back Office lesson detail – Student no longer appears

**Description:** AC-1 — Cross-system regression — Deleted session is absent from the BO lesson student list.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce and HQ Staff to Back Office.
- Student A has an individual session on the `2026-02-15` lesson.
- `last_attendance_day = 2026-02-08`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Submit a Partial Withdrawal with Last Attendance Day `2026-02-08`. | The `2026-02-15` individual session is deleted. | `lesson_date = 2026-02-15` |
| 2 | Open the `2026-02-15` lesson in Back Office. | Student A is absent from the lesson student list. | `student = A` |

**Severity:** critical  
**Priority:** high

---

### Lesson Allocation – Withdrawal – Learner App schedule – Removed lesson no longer appears

**Description:** AC-1 — Cross-system regression — Deleted session is absent from the learner schedule.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce and as Student A in the Learner App.
- Student A has an individual session on the `2026-02-15` lesson.
- `last_attendance_day = 2026-02-08`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Submit a Partial Withdrawal with Last Attendance Day `2026-02-08`. | The `2026-02-15` individual session is deleted. | `lesson_date = 2026-02-15` |
| 2 | Open Student A's Learner App schedule for `2026-02-15`. | The removed lesson and its report are not shown. | `student = A` |

**Severity:** critical  
**Priority:** high
