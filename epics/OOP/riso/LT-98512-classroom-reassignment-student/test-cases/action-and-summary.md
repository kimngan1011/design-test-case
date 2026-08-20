# Test Cases: LT-98512 — Riso Classroom Reassignment by Student

## Suite: Daily Action and Result Summary

### [Riso] Classroom Adjustment – Daily View menu – Flag enabled – Action appears above Print Out

**Description:** AC-01 — Component — Riso staff can find the adjustment action in its required menu position.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org.
- Optimize Classroom Assignment = ON for Riso.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Lesson Calendar Daily View for Riso Shinjuku on 2026-07-23. | The Daily View action menu is available. | location = Riso Shinjuku; lesson_date = 2026-07-23 |
| 2 | Open the action menu. | Classroom Adjustment is shown immediately above Print Out. | menu order = Classroom Adjustment, Print Out |

**Severity:** minor
**Priority:** medium

---

### [Riso] Classroom Adjustment – Calendar views – Non-Daily View – Action remains hidden

**Description:** AC-02 — Decision Table — The Riso action is limited to Daily View.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org.
- Optimize Classroom Assignment = ON for Riso.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Lesson Calendar Week View for 2026-07-23. | Classroom Adjustment is not shown in the action menu. | view = Week; lesson_date = 2026-07-23 |
| 2 | Open Lesson Calendar Month View for July 2026. | Classroom Adjustment is not shown in the action menu. | view = Month; month = 2026-07 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Classroom Adjustment – Completion summary – One reassignment – Required message and counters appear

**Description:** AC-04 — Component — A completed adjustment presents the specified feedback.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org.
- Optimize Classroom Assignment = ON; Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Student A has Individual lessons at 09:00 and 11:00; Room A is available for both lessons.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Daily View and run Classroom Adjustment. | The adjustment completes for the selected scope. | lesson_date = 2026-07-23; Student A: 09:00 Room A, 11:00 unassigned candidate |
| 2 | Read the completion feedback. | The message is `Classroom adjustment completed`; Previous room applied, Sequence assigned, Skipped, Clash resolved, and Clash unresolved (kept as-is) are all displayed. | expected text = Classroom adjustment completed |

**Severity:** major
**Priority:** high

---

### [Riso] Classroom Adjustment – Completion summary – No eligible lessons – Zero-update result appears

**Description:** AC-04 — Negative — A valid empty scope still returns readable completion feedback.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org.
- Optimize Classroom Assignment = ON; Location = Riso Shinjuku; lesson_date = 2026-07-24.
- The selected scope has no Individual lessons.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment from Daily View. | The run completes without changing any lesson. | location = Riso Shinjuku; lesson_date = 2026-07-24; Individual lessons = 0 |
| 2 | Read the completion feedback. | `Classroom adjustment completed` is displayed with all required counter labels and zero updates. | expected updated lessons = 0 |

**Severity:** major
**Priority:** high

---

### [Riso] Classroom Adjustment – Print flow – Completed reassignment – Print Out remains available

**Description:** AC-05 — Regression — Adjustment does not block the existing Daily PDF flow.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org.
- Optimize Classroom Assignment = ON; Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Student A has a confirmed reassignment from Room B to Room A after adjustment.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment and dismiss the completion feedback. | Daily View remains available after the run. | Student A = Room B to Room A |
| 2 | Select Print Out. | The existing Print Out flow opens and includes Student A with Room A. | expected classroom in print flow = Room A |

**Severity:** major
**Priority:** high

---

### [Riso] Classroom Adjustment – Completion summary – Pre-existing clash resolved – Clash result is surfaced

**Description:** AC-04, AC-17 — Decision Table — A corrected duplicate is represented in the summary.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org.
- Optimize Classroom Assignment = ON; Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Two Individual lessons at 10:00 are assigned to Room A; Room B is an available Private classroom with Sequence 2.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | One duplicated lesson is reassigned to Room B and the other remains in Room A. | 10:00 duplicate = Lesson 100 in Room A, Lesson 101 in Room A; Room B sequence = 2 |
| 2 | Read the completion feedback. | Clash resolved shows `1` for the resolved duplicate. | expected Clash resolved = 1 |

**Severity:** major
**Priority:** high

---

### [Riso] Classroom Adjustment – Invalid trigger payload – Missing location or lesson date – Apex is not called

**Description:** AC-03, AC-04 — Negative — The Calendar LWC guard must not run classroom adjustment without required Daily View context.

**Preconditions:**
- Logged in as HQ or CM Staff to the Riso Salesforce org.
- Optimize Classroom Assignment = ON.
- Test harness can observe the `ClassroomReassignmentController.reassign` Apex call or network request.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Trigger `optimizeClassroomAssignment` with `teachingMethod = Individual` and blank `locationId`. | The action returns without calling Apex and no success summary is shown. | locationId = blank; lessonDate = 2026-07-23 |
| 2 | Trigger `optimizeClassroomAssignment` with `teachingMethod = Individual` and blank `lessonDate`. | The action returns without calling Apex and no classroom records are changed. | locationId = Riso Shinjuku SF Id; lessonDate = blank |
| 3 | Trigger `optimizeClassroomAssignment` with `teachingMethod = Group`. | The action returns without calling Apex. | teachingMethod = Group |

**Severity:** major
**Priority:** high
