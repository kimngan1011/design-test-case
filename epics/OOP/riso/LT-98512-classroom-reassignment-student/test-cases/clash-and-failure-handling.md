# Test Cases: LT-98512 — Riso Classroom Reassignment by Student

## Suite: Clash, Skip, and Failure Handling

### [Riso] Classroom Adjustment – Classroom clash – Partial time overlap – Overlapping room is excluded

**Description:** AC-11, AC-12 — Regression — Existing Calendar partial-overlap protection applies to automated assignment.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Room A is assigned from 10:00 to 11:00; target Individual lesson is 10:30 to 11:30; Room B Sequence 2 is available.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | The target lesson does not receive Room A and receives Room B when Rule 2 applies. | Room A = 10:00–11:00; target = 10:30–11:30; Room B sequence = 2 |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Per-lesson failure – No room for middle lesson – Later lessons continue

**Description:** AC-14 — Negative — One assignment failure does not stop later processing.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Student A has 09:00 Room A, 11:00 with no eligible room, and 13:00 with Room A available.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | The 11:00 lesson retains its current classroom; processing continues to 13:00. | Room A unavailable at 11:00; Room A available at 13:00 |
| 2 | Inspect the 13:00 lesson. | The 13:00 lesson receives Room A through the applicable Rule 1 history. | expected 13:00 room = Room A |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – No-room outcome – Rule 1 and Rule 2 unavailable – Current classroom is retained

**Description:** AC-15 — Negative — The primary PRD rule preserves the classroom when no eligible room exists.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Target lesson currently has Room C; its Rule 1 room is occupied and no eligible Private classroom is available.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | The target lesson retains Room C and Skipped shows `1`. | current room = Room C; eligible rooms = 0; expected Skipped = 1 |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Two-student lesson – Mixed scope – Two-student classroom is retained

**Description:** AC-16 — Equivalence Partitioning — A two-student lesson is skipped while eligible lessons can continue.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Lesson T has two students and Room C; Lesson I is an eligible one-student lesson with a reassignment fixture.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | Lesson T remains in Room C; Lesson I follows its assignment rule. | Lesson T students = 2; Room C |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Pre-existing clash – One duplicate can move – Lowest sequence replacement is used

**Description:** AC-17 — CRUD — A pre-existing same-room/same-slot duplicate is reconciled.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Lessons 100 and 101 are both in Room A from 10:00 to 11:00; Room B Sequence 2 and Room C Sequence 3 are available.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | One lesson remains in Room A and the other is reassigned to Room B. | duplicate = Lessons 100,101 in Room A; B=2; C=3 |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Pre-existing clash – No replacement room – Duplicate remains unresolved and processing continues

**Description:** AC-18 — Negative — An unresolvable duplicate is retained and does not stop other lessons.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Lessons 100 and 101 duplicate Room A at 10:00; no alternative Private room is available; Student B has an eligible 11:00 lesson with Room B available.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | The duplicated lesson that cannot move retains Room A and Clash unresolved (kept as-is) shows `1`. | duplicate = Room A; alternative rooms = 0; expected Clash unresolved = 1 |
| 2 | Inspect Student B's 11:00 lesson. | Student B's lesson is still processed and receives Room B. | Student B 11:00; Room B available |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Duplicate priority – Different start times – Earlier lesson remains in original room

**Description:** AC-19 — Scenario — Chronological priority selects the preserved duplicate.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Duplicated Room A assignments are Lesson 200 at 09:00 and Lesson 201 at 10:00; Room B Sequence 2 is available for Lesson 201.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | Lesson 200 remains in Room A and Lesson 201 is reassigned to Room B. | Lesson 200 = 09:00; Lesson 201 = 10:00; Room B = 2 |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Duplicate priority – Equal start times – Earlier Lesson ID remains in original room

**Description:** AC-19 — Scenario — Lesson ID is the deterministic tie-breaker for preserved duplicates.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Duplicated Room A assignments are Lesson 100 and Lesson 101 at 10:00; Room B Sequence 2 is available.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | Lesson 100 remains in Room A and Lesson 101 is reassigned to Room B. | start time = 10:00; Lesson IDs = 100,101; Room B = 2 |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Availability – Rule 1 candidate becomes occupied – Rule 2 prevents a clash

**Description:** AC-08, AC-12 — Negative — A previously used room is rejected when it is no longer available for the target slot.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Student A has 09:00 Room A; another lesson occupies Room A at Student A's 11:00 slot; Room B Sequence 2 is available.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | Student A's 11:00 lesson receives Room B and does not clash with the Room A occupant. | Room A occupied at 11:00; Room B = 2 |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Independent students – One student's failure – Other student remains eligible

**Description:** AC-14 — Decision Table — A failure is isolated to its lesson and student.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Student A has a 10:00 lesson with no eligible room; Student B has a 10:00 lesson with Room B available.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | Student A follows the no-room path and Student B is assigned Room B. | Student A eligible rooms = 0; Student B Room B = available |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Result counters – Two-student skip – Skipped outcome is recorded

**Description:** AC-04, AC-16 — Decision Table — A known skipped lesson contributes to the result feedback.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- A two-student Individual lesson is assigned Room C; no other lesson needs adjustment.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment and read the feedback. | The lesson remains Room C and Skipped shows `1`. | students = 2; current room = Room C; expected Skipped = 1 |

**Severity:** major  
**Priority:** high
