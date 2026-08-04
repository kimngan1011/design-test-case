# Test Cases: LT-98512 — Riso Classroom Reassignment by Student

## Suite: Student Ordering and Assignment Rules

### [Riso] Classroom Adjustment – Student grouping – Separate students – Each student uses an independent room history

**Description:** AC-07 — Scenario — Processing one student does not use another student's previous room.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Student A has 09:00 Room A and 11:00; Student B has 09:00 Room B and 11:00; both rooms are available at 11:00.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | Student A's 11:00 lesson uses Room A and Student B's 11:00 lesson uses Room B. | A = Room A history; B = Room B history |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Processing order – Different start times – Earlier lesson supplies Rule 1 candidate

**Description:** AC-07, AC-08 — Scenario — Earlier start time is processed first.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Student A has 09:00 Room A and 11:00 unassigned candidate; Room A is available at 11:00.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | The 09:00 lesson is the earlier processed lesson and the 11:00 lesson receives Room A through Rule 1. | 09:00 < 11:00; Room A available at 11:00 |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Processing order – Same start time – Earlier Lesson ID is processed first

**Description:** AC-07 — Scenario — Lesson ID resolves an equal-start-time tie deterministically.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Student A has 10:00 Lesson ID 100 in Room A and 10:00 Lesson ID 101 with no preferred room; Room A is available only for the first processed lesson.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | Lesson ID 100 is processed before Lesson ID 101 when start times are equal. | start time = 10:00; Lesson IDs = 100, 101 |
| 2 | Inspect the room outcome. | The outcome follows Lesson ID 100 as the first tie-break candidate. | tie-break = Lesson ID ascending |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Rule 1 – Previous room available – Later lesson keeps the room

**Description:** AC-08 — Decision Table — The latest processed room is reused when eligible.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Student A has 09:00 Room A, 11:00 and 13:00 lessons; Room A is available for all three slots.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | Student A's 11:00 and 13:00 lessons are assigned Room A through Rule 1. | Room A available at 11:00 and 13:00 |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Rule 1 history – Rule 2 replacement – Later lesson uses replacement room

**Description:** AC-08, AC-09, AC-13 — Scenario — A Rule 2 room becomes the next Rule 1 candidate.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Student A has 09:00 Room A, 11:00, 13:00, and 16:00 lessons; Room A is occupied at 11:00; Room B Sequence 2 is available from 11:00 onward.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | The 11:00 lesson receives Room B through Rule 2. | Room A unavailable at 11:00; Room B sequence = 2 |
| 2 | Inspect the 13:00 and 16:00 lessons. | Both later lessons use Room B through Rule 1. | Room B available at 13:00 and 16:00 |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Rule 1 fallback – Previous room occupied – Lowest sequence room is selected

**Description:** AC-09, AC-10 — Decision Table — Rule 2 applies when Rule 1 cannot use the prior room.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Student A's earlier lesson uses Room A; Room A is occupied at the later slot; Room C Sequence 3 and Room B Sequence 2 are eligible.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | The later lesson is assigned Room B, not Room A or Room C. | Room A = occupied; Room B sequence = 2; Room C sequence = 3 |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Rule 2 ordering – Multiple eligible rooms – Lowest Classroom Sequence wins

**Description:** AC-10 — Scenario — Rule 2 orders eligible rooms by Classroom Sequence ascending.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- The candidate lesson has no reusable prior room; Private rooms C, A, and B are eligible with sequences 30, 10, and 20.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | The lesson is assigned Room A with Sequence 10. | Room A = 10; Room B = 20; Room C = 30 |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Eligibility – Foreign location and non-Private rooms – Ineligible rooms are excluded

**Description:** AC-11 — Equivalence Partitioning — Only selected-location Private rooms can be selected.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Eligible Room A is Private at Riso Shinjuku Sequence 3; Room B is Private at Riso Ikebukuro Sequence 1; Room C is Group type at Riso Shinjuku Sequence 2.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment for Riso Shinjuku. | The candidate lesson is assigned Room A; Room B and Room C are not selected. | A = Shinjuku Private; B = Ikebukuro Private; C = Shinjuku Group |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Eligibility – Room occupied in target slot – Occupied room is excluded

**Description:** AC-11, AC-12 — Negative — A currently assigned room cannot be selected for the same slot.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Room A Sequence 1 is occupied by another lesson from 10:00 to 11:00; Room B Sequence 2 is available; target lesson is 10:00 to 11:00.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | The target lesson receives Room B and never Room A. | target = 10:00–11:00; Room A = occupied; Room B = available |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Repeated evaluation – Four lessons – Each chronological lesson receives a rule outcome

**Description:** AC-13 — Decision Table — Processing continues through more than two lessons for one student.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Student A has lessons at 09:00 Room A, 11:00, 13:00, and 16:00; Room A is unavailable at 11:00 and Room B Sequence 2 is available thereafter.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | The 11:00 lesson gets Room B through Rule 2; the 13:00 and 16:00 lessons get Room B through Rule 1. | lessons = 09:00, 11:00, 13:00, 16:00; Room B sequence = 2 |

**Severity:** major  
**Priority:** high
