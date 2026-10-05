# Test Cases: LT-94111 — Riso Permission and Requiredness

## Suite: Riso Permission and Requiredness

### [Riso] Lesson Upsert – Classroom – Blank value – Save is blocked
**Description:** AC 01.5 — Equivalence Partitioning / Negative — Classroom is mandatory in Riso.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- A new Lesson has `Tokyo Center`, `2026-09-15`, `10:00`, and `11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff leaves Classroom blank. | The form identifies Classroom as required or keeps Save unavailable. | classroom = blank |
| 2 | HQ or CM Staff saves the Lesson. | The Riso Lesson is not saved without a Classroom. | date = 2026-09-15; interval = 10:00–11:00 JST |
**Severity:** major  
**Priority:** high

### Core Lesson Upsert – Classroom – Blank value – Save is allowed
**Description:** AC 01.5 — Equivalence Partitioning — Classroom remains optional in Core.
**Preconditions:**
- HQ or CM Staff is logged in to a Core Salesforce org.
- A new Lesson has `Tokyo Center`, `2026-09-15`, `10:00`, and `11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff leaves Classroom blank. | The form permits a blank Classroom. | classroom = blank |
| 2 | HQ or CM Staff saves the Lesson. | The Core Lesson is saved without a Classroom. | date = 2026-09-15; interval = 10:00–11:00 JST |
**Severity:** major  
**Priority:** high

### [Riso] Lesson Upsert – Classroom – PT Teacher – Editing is unavailable
**Description:** AC 01.5 — Permission Matrix / Negative — PT Teacher cannot edit Classroom.
**Preconditions:**
- A PT Teacher is logged in to the Riso Salesforce org.
- An editable Lesson displays `Room PT` on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | PT Teacher opens the Lesson edit form. | The current Classroom is visible but not editable. | classroom = Room PT |
| 2 | PT Teacher attempts to change Classroom to `Room Other`. | The Classroom value remains `Room PT`. | requested classroom = Room Other |
**Severity:** major  
**Priority:** high
