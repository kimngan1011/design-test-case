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

### [Riso] Classroom Adjustment – Eligibility – Foreign location and non-Private rooms – PRD ineligible rooms are excluded

**Description:** AC-11 — Equivalence Partitioning / Gap Detection — The PRD says only selected-location Private rooms can be selected; current repository query must be verified against this requirement.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Eligible Room A is Private at Riso Shinjuku Sequence 3; Room B is Private at Riso Ikebukuro Sequence 1; Room C is Group type at Riso Shinjuku Sequence 2.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment for Riso Shinjuku. | The candidate lesson is assigned Room A; Room B and Room C are not selected. If Room C is selected, log an implementation gap against AC-11 because current code may not filter classroom type. | A = Shinjuku Private; B = Ikebukuro Private; C = Shinjuku Group |

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

---

### [Riso] Classroom Adjustment – Rule 2 ordering – Null sequence rooms are considered last

**Description:** AC-10 — Boundary Value Analysis — Repository ordering places null Classroom Sequence after numeric sequences.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- The candidate lesson needs Rule 2; Room A Sequence is blank, Room B Sequence is 2, and Room C Sequence is 3.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | The lesson receives Room B, not the null-sequence Room A. | Room A sequence = null; Room B = 2; Room C = 3 |
| 2 | Inspect available-room ordering. | Numeric sequence rooms are evaluated before null-sequence rooms; if multiple nulls remain, existing Name/CreatedDate tie-break applies. | order = Sequence ASC NULLS LAST, Name ASC, CreatedDate ASC |

**Severity:** major
**Priority:** high

---

### [Riso] Classroom Adjustment – Rule 2 ordering – Same or null sequence – Name and CreatedDate tie-break are deterministic

**Description:** AC-10 — Pairwise / Sort — When sequence values tie, the same classroom is chosen deterministically based on repository ordering.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Candidate lesson needs Rule 2; Room Alpha and Room Beta have the same Sequence, with Room Alpha alphabetically first.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | Room Alpha is selected before Room Beta. | Room Alpha sequence = 5; Room Beta sequence = 5 |
| 2 | Repeat with two rooms having the same blank Sequence and same Name fixture if supported. | Earlier CreatedDate room is selected first, giving a stable repeatable result. | sequence = null; name tie; created date tie-break |

**Severity:** major
**Priority:** high

---

### [Riso] Classroom Adjustment – Roomless eligible lesson – Available room creates classroom assignment

**Description:** AC-10, AC-15 — CRUD — A lesson with no existing `Lesson_Classroom__c` receives a new classroom junction when Rule 2 finds an available room.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Student A has a valid Individual lesson at 11:00 with no classroom junction; Room A Sequence 1 is available.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Run Classroom Adjustment. | The roomless lesson is assigned Room A and a `Lesson_Classroom__c` record exists for the lesson. | current classroom = none; Room A sequence = 1 |
| 2 | Read the completion summary. | Sequence assigned increments by `1`; Skipped does not increment for this lesson. | expected Sequence assigned = +1 |

**Severity:** major
**Priority:** high
