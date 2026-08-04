# Test Cases: LT-98512 — Riso Classroom Reassignment by Student

## Suite: Manual Follow-up

### [Riso] Classroom Adjustment – Manual follow-up – Completed run – Classroom remains editable

**Description:** US03 duplicate AC-17 — State Transition — Staff can correct a classroom after automation.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Classroom Adjustment completed and assigned Student A's 11:00 lesson to Room A; Room B is eligible at 11:00.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Student A's 11:00 lesson after adjustment. | The classroom field is editable. | current room = Room A |
| 2 | Change the classroom to Room B and save. | The lesson shows Room B after save. | new room = Room B |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Manual follow-up – Conflicting room choice – Existing clash safeguard remains active

**Description:** US03 duplicate AC-17 — Regression — Automation does not bypass normal manual clash prevention.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Classroom Adjustment completed; Room A is occupied by another lesson from 11:00 to 12:00; Student A's lesson is 11:00 to 12:00 in Room B.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Attempt to change Student A's classroom from Room B to Room A and save. | The existing clash safeguard blocks the conflicting manual change; Student A remains in Room B. | target = 11:00–12:00; Room A = occupied; current = Room B |

**Severity:** major  
**Priority:** high

---

### [Riso] Classroom Adjustment – Manual follow-up – Corrected room – Print Out reflects the staff change

**Description:** US03 duplicate AC-17, AC-05 — Cross-system — The manual correction survives into the continuing daily flow.

**Preconditions:**
- Logged in as HQ or CM Staff; Optimize Classroom Assignment = ON.
- Location = Riso Shinjuku; lesson_date = 2026-07-23.
- Adjustment completed; Student A's classroom was manually changed to Room B and saved.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Select Print Out from Daily View. | The print flow opens with Student A assigned to Room B. | expected classroom = Room B |

**Severity:** major  
**Priority:** high
