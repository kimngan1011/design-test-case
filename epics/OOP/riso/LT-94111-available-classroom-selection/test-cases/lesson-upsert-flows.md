# Test Cases: LT-94111 — Lesson Upsert Flows

## Suite: Lesson Upsert Flows

### [Riso] Lesson List SF – New Lesson – Vacant Classroom – Available Classroom is saved
**Description:** Scope F01 / AC 01.2 — Scenario — New Lesson on Lesson List SF uses availability.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room F01` is vacant at `Tokyo Center` on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff creates a new Lesson from Lesson List SF with `Room F01`. | `Room F01` is selectable. | date = 2026-09-15; interval = 10:00–11:00 JST |
| 2 | HQ or CM Staff saves the Lesson. | The saved Lesson displays `Room F01`. | flow = F01 |
**Severity:** major  
**Priority:** high

### [Riso] Lesson SF – Edit Lesson – Changed start time – Classroom resets to blank
**Description:** Scope F02 / AC 01.3 — State Transition — SF edit clears stale Classroom.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- An editable Lesson has `Room F02` on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff changes the Lesson start time to `11:00` in SF. | The Classroom field becomes blank. | original = 10:00–11:00 JST; updated start = 11:00 JST |
| 2 | HQ or CM Staff saves without selecting another Classroom. | Riso requiredness prevents saving without a Classroom. | flow = F02 |
**Severity:** major  
**Priority:** high

### [Riso] Lesson Schedule Detail – Add Lesson – Occupied Classroom – Classroom is unavailable
**Description:** Scope F03 / AC 01.2 — Scenario / Negative — Added lessons use availability.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room F03` has a lesson on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff adds a Lesson from Lesson Schedule Detail for `10:00–11:00` JST. | The Classroom selector is available for the added Lesson. | date = 2026-09-15 |
| 2 | HQ or CM Staff opens the Classroom selector. | `Room F03` is absent. | flow = F03; existing interval = 10:00–11:00 JST |
**Severity:** major  
**Priority:** high

### [Riso] Lesson Schedule Detail – Extend Recurrence – First occurrence vacant – Classroom can be selected
**Description:** Scope F04 / AC 01.4 — State Transition — Recurrence entry uses the selected instance.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- A weekly schedule can be extended from `2026-09-15 10:00–11:00` JST.
- `Room F04` is vacant for the selected occurrence.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Extend Recurrence and selects `2026-09-15 10:00–11:00` JST. | `Room F04` is selectable. | first occurrence = 2026-09-15 10:00–11:00 JST |
| 2 | HQ or CM Staff saves the extension with `Room F04`. | The extended lesson uses `Room F04`. | flow = F04 |
**Severity:** major  
**Priority:** high

### [Riso] Lesson SF – Duplicate Lesson – Duplicated Classroom conflicts – Save is rejected
**Description:** Scope F05 / AC 02.1 — Regression / Negative — Duplicate flow cannot retain a conflict.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- The source Lesson uses `Room F05`.
- Another Lesson uses `Room F05` on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff duplicates the source Lesson to `2026-09-15 10:00–11:00` JST. | The duplicate cannot retain `Room F05` as an available selection. | flow = F05 |
| 2 | HQ or CM Staff saves with `Room F05` selected from stale data. | Save is rejected with `Room F05 is already in use for another class.` | classroom = Room F05 |
**Severity:** major  
**Priority:** high

### [Riso] Back Office – Edit Lesson – Vacant Classroom – Updated Classroom persists
**Description:** Scope F06 / AC 01.2 — Permission Matrix / Regression — BO edit supports a permitted user.
**Preconditions:**
- HQ Staff is logged in to Back Office with Classroom edit permission.
- An editable Lesson exists at `Tokyo Center`.
- `Room F06` is vacant on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ Staff selects `Room F06` while editing the Lesson in Back Office. | `Room F06` is selectable. | flow = F06; date = 2026-09-15; interval = 10:00–11:00 JST |
| 2 | HQ Staff saves the Lesson. | The Back Office Lesson displays `Room F06`. | classroom = Room F06 |
**Severity:** major  
**Priority:** high
