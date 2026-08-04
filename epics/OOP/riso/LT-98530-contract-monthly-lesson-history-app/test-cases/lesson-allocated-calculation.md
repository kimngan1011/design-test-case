# Test Cases: LT-98530 — [Riso] OOP | Contract and Monthly Lesson history (App)

> ⚠️ **Pending Confirmation:** The Cancelled-status exclusion rule (AC01.2) conflicts with the sibling SF report's confirmed behavior (LT-98531 AC-10 — no status check at all). See spec Clarification Question #2. Both interpretations are tested below.

## Suite: [Riso] Lesson Allocated Calculation (Pending Confirmation)

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

### [Riso] Lesson Allocated – Cancelled Lesson Status – Excluded Per PRD (Pending Confirmation)

**Description:** AC01.2 — Decision Table — Per the PRD's literal text, a session on a Cancelled-status lesson is excluded from Lesson Allocated. This conflicts with the sibling SF report's confirmed behavior (spec Clarification Question #2); tested here as the PRD's primary stated rule.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has one student session on a Cancelled-status lesson, date=2025-09-15, within range, Attendance = Present

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the month selector to September 2025 and view the LA card | Lesson Allocated count does NOT include this session | lesson_status=Cancelled; session_date=2025-09-15; expected=excluded (per PRD, pending confirmation) |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocated – Cancelled Lesson Status – Alternate Behavior Matching Confirmed SF Report (Pending Confirmation)

**Description:** AC01.2 — Decision Table — Documents the alternate expected behavior confirmed for the sibling SF report (LT-98531 AC-10: lesson status is NOT checked at all). To be adopted here only if Clarification Question #2 resolves in favor of matching the SF report.

**Preconditions:**
- Logged in as Student to the Riso Learner App
- LA has one student session on a Cancelled-status lesson, date=2025-09-15, within range, Attendance = Present

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Set the month selector to September 2025 and view the LA card | (Alternate expectation, pending) Lesson Allocated count INCLUDES this session, matching LT-98531's confirmed no-status-check behavior | lesson_status=Cancelled; session_date=2025-09-15; expected=included (alternate, pending confirmation) |

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

### [Riso] Lesson Allocated – Cross-Surface Consistency – App Count vs SF Monthly Lesson Assignment Report

**Description:** AC01.2 — Regression — Compares the App's Lesson Allocated count against the confirmed SF Monthly Lesson Assignment report (LT-98531) count for the same student/month, given both claim to share "the same calculation as PBT-1510."

**Preconditions:**
- Logged in as Student to the Riso Learner App and as HQ or CM Staff to the Salesforce org (same student, same month)
- Student has 1 Cancelled-status session and 1 Absent-without-notice session in the selected month, plus 3 Present sessions

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | View Lesson Allocated on the App Contract Info page | App shows 3 (Cancelled excluded per PRD; Absent-without-notice excluded) | app_lesson_allocated = 3 (Present sessions only, per PRD's Cancelled exclusion) |
| 2 | View the Lesson Allocated column on the SF Monthly Lesson Assignment report for the same student/month | SF report shows 4 (Cancelled included per LT-98531 AC-10 confirmed behavior; only Absent-without-notice excluded) — a mismatch vs the App, flagged as pending confirmation | sf_lesson_allocated = 4 (Cancelled included, per confirmed AC-10); discrepancy = 1, pending Clarification Question #2 |

**Severity:** major
**Priority:** high

---
