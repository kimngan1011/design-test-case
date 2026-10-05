# Test Cases: LT-94111 — Classroom Save Validation and Concurrency

## Suite: Classroom Save Validation and Concurrency

### [Riso] Lesson Save – Classroom overlap – English locale – English error is shown
**Description:** AC 02.1 — Decision Table / Negative — English overlap copy is exact.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org with English locale.
- `Room Error` has a lesson on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects stale `Room Error` for a Lesson on `2026-09-15 10:00–11:00` JST. | The stale selection is present before Save. | target = existing = 10:00–11:00 JST |
| 2 | HQ or CM Staff saves the Lesson. | Save is rejected and shows exactly `Room Error is already in use for another class.` | locale = English |
**Severity:** critical  
**Priority:** high

### [Riso] Lesson Save – Classroom overlap – Japanese locale – Japanese error is shown
**Description:** AC 02.1 — Decision Table / Negative — Japanese overlap copy is exact.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org with Japanese locale.
- `Room Error` has a lesson on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects stale `Room Error` for a Lesson on `2026-09-15 10:00–11:00` JST. | The stale selection is present before Save. | target = existing = 10:00–11:00 JST |
| 2 | HQ or CM Staff saves the Lesson. | Save is rejected and shows exactly `Room Errorは既に他の授業で利用されています`. | locale = Japanese |
**Severity:** critical  
**Priority:** high

### [Riso] Lesson Save – Classroom overlap – Two user sessions – Second save is rejected
**Description:** AC 02.1 — CRUD / Negative — Concurrent saves do not persist two assignments.
**Preconditions:**
- HQ or CM Staff A is logged in to the Riso Salesforce org.
- HQ or CM Staff B is logged in to a separate Riso session.
- `Room Concurrent` is initially vacant on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff A saves a Lesson with `Room Concurrent`. | Staff A's Lesson is saved. | date = 2026-09-15; interval = 10:00–11:00 JST |
| 2 | HQ or CM Staff B saves a stale Lesson with `Room Concurrent`. | Staff B's Save is rejected and no second assignment persists. | second session = stale selector data |
**Severity:** critical  
**Priority:** high

### [Riso] Lesson Save – Classroom overlap – Repeated submit – Only one Lesson persists
**Description:** AC 02.1 — CRUD / Negative — Double submission cannot create duplicate assignments.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room Double Submit` is vacant on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff submits the same Lesson twice without changing its data. | The system processes at most one save request as a new assignment. | date = 2026-09-15; interval = 10:00–11:00 JST |
| 2 | HQ or CM Staff opens the Lesson list. | Exactly one Lesson uses `Room Double Submit` for the interval. | expected count = 1 |
**Severity:** critical  
**Priority:** high

### [Riso] Lesson Save – Classroom overlap – Two browser tabs – Later Save is rejected
**Description:** AC 02.1 — Decision Table / Negative — A stale tab cannot overwrite availability.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org in two browser tabs.
- `Room Multi Tab` is initially vacant on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff saves a Lesson with `Room Multi Tab` in the first tab. | The first-tab Lesson is saved. | tab = 1; date = 2026-09-15; interval = 10:00–11:00 JST |
| 2 | HQ or CM Staff saves a stale Lesson with `Room Multi Tab` in the second tab. | The second-tab Save is rejected and the first assignment remains unchanged. | tab = 2 |
**Severity:** critical  
**Priority:** high
