# Test Cases: LT-98512 — Riso Classroom Reassignment by Student

## Suite: Concurrency and Performance

### [Riso] Classroom Adjustment – Concurrent run – Same Location and date – One consistent final assignment set

**Description:** NFR-08 — Decision Table — Two staff actions on the same scope cannot leave inconsistent rooms.

**Preconditions:**
- Logged in as HQ or CM Staff in two browser sessions.
- Optimize Classroom Assignment = ON; Location = Riso Shinjuku; lesson_date = 2026-07-23.
- The scope contains competing Individual lessons with a deterministic Room A/Room B fixture.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Start Classroom Adjustment from both sessions for the same scope. | The scope has one committed adjustment result with no duplicate or conflicting room assignment. | session 1 and session 2; same Location/date |
| 2 | Refresh Daily View in both sessions. | Both sessions show the same final classroom for every lesson. | expected final data set = identical in both sessions |

**Severity:** critical  
**Priority:** high

---

### [Riso] Classroom Adjustment – Rapid trigger – Double click – Exactly one adjustment result is applied

**Description:** NFR-08 — Negative — A rapid retry does not produce two sets of writes.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23; fixture has a deterministic single reassignment to Room A.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Trigger Classroom Adjustment twice without waiting for the first response. | The final lesson assignment equals one valid adjustment run; no duplicate or contradictory update is present. | trigger count = 2; expected effective runs = 1 |

**Severity:** critical  
**Priority:** high

---

### [Riso] Classroom Adjustment – Concurrent edit – Staff changes room during run – Final state is explainable

**Description:** NFR-08 — Decision Table — A manual edit racing with the run produces the approved consistent outcome.

**Preconditions:**
- Logged in as HQ or CM Staff in two browser sessions.
- Optimize Classroom Assignment = ON; Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Student A's 11:00 lesson is in the adjustment scope; Room A and Room B are eligible.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Start Classroom Adjustment in session 1. | The run begins for the selected scope. | session 1 = adjustment |
| 2 | In session 2, change Student A's classroom to Room B while the run is in progress. | Student A has one saved classroom value and no classroom clash after both operations finish. | session 2 edit = Room B |

**Severity:** critical  
**Priority:** high

---

### [Riso] Classroom Adjustment – Concurrent runs – Different locations – Each scope remains isolated

**Description:** NFR-08, AC-06 — Decision Table — Parallel work at separate locations does not cross-write.

**Preconditions:**
- Logged in as HQ or CM Staff in two browser sessions.
- Optimize Classroom Assignment = ON; lesson_date = 2026-07-23.
- Riso Shinjuku and Riso Ikebukuro each have a deterministic reassignment fixture.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment for Riso Shinjuku in session 1 and Riso Ikebukuro in session 2. | Each run changes only its selected location. | session 1 = Shinjuku; session 2 = Ikebukuro |
| 2 | Compare classrooms in both locations. | Each location has its expected local result and no cross-location write. | expected scope = location-local |

**Severity:** critical  
**Priority:** high

---

### [Riso] Classroom Adjustment – Performance workload – 400 daily lessons – Run records complete results

**Description:** NFR-01 — Boundary Value Analysis — The documented maximum daily volume completes without an incomplete result set.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Seed 400 Individual lessons across up to 50 Private classrooms and up to 8 slots per classroom; record the approved performance target before execution.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment and record elapsed runtime. | Every in-scope lesson receives its deterministic assignment, skip, or unresolved outcome; runtime is recorded against the approved release target. | lessons = 400; classrooms = 50; slots/classroom = 8; lesson_date = 2026-07-23 |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Performance failure – Runtime threshold exceeded – Scope remains consistent

**Description:** NFR-01, AC-14 — Negative — A timeout or processing error cannot leave an unexplained partial result.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Use the approved error/timeout fixture once NFR-01 limits are confirmed; record original classrooms for all fixture lessons.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment with the approved timeout or error fixture. | The system displays an error result and every affected lesson has one saved classroom value with no classroom clash. | timeout/error fixture = approved release value; original classrooms recorded |
| 2 | Compare all affected lessons with the reported outcome. | Each changed classroom is listed in the result, and every unlisted lesson retains its recorded original classroom. | original classrooms recorded before run |

**Severity:** major  
**Priority:** high
