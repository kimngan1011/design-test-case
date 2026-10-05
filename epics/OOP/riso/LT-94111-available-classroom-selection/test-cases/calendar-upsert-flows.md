# Test Cases: LT-94111 — Calendar Upsert Flows

## Suite: Calendar Upsert Flows

### [Riso] Calendar SF – New Lesson – Vacant Classroom – Available Classroom is saved
**Description:** Scope F07 / AC 01.2 — Scenario — New Calendar lesson uses availability.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room F07` is vacant at `Tokyo Center` on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff creates a Lesson from Calendar SF and selects `Room F07`. | `Room F07` is selectable. | flow = F07; date = 2026-09-15; interval = 10:00–11:00 JST |
| 2 | HQ or CM Staff saves the Lesson. | The Calendar lesson displays `Room F07`. | classroom = Room F07 |
**Severity:** major  
**Priority:** high

### [Riso] Calendar SF – Drag and drop new Lesson – Occupied Classroom – Conflict is blocked
**Description:** Scope F08 / AC 02.1 — Scenario / Negative — DnD create cannot assign an occupied room.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room F08` has a lesson on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff drags to create a Calendar Lesson for `10:00–11:00` JST. | The new Lesson form uses the dragged date and time. | flow = F08; date = 2026-09-15 |
| 2 | HQ or CM Staff opens the Classroom selector. | `Room F08` is absent. | existing interval = 10:00–11:00 JST |
**Severity:** major  
**Priority:** high

### [Riso] Calendar SF – Drag and drop edit – Changed time – Classroom resets to blank
**Description:** Scope F09 / AC 01.3 — State Transition — DnD edit clears a stale Classroom.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- A Calendar Lesson uses `Room F09` on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff drags the Lesson to `2026-09-15 11:00–12:00` JST. | The Classroom field becomes blank before Save. | flow = F09; updated interval = 11:00–12:00 JST |
| 2 | HQ or CM Staff opens the edited Lesson. | The user must select a Classroom again. | classroom = blank |
**Severity:** major  
**Priority:** high

### [Riso] Available Teacher Calendar – New Lesson – Vacant Classroom – Available Classroom is saved
**Description:** Scope F10 / AC 01.2 — Scenario — Available Teacher Calendar applies Classroom availability.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room F10` is vacant at `Tokyo Center` on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff creates a Lesson from Available Teacher Calendar and selects `Room F10`. | `Room F10` is selectable. | flow = F10; date = 2026-09-15; interval = 10:00–11:00 JST |
| 2 | HQ or CM Staff saves the Lesson. | The saved Lesson displays `Room F10`. | classroom = Room F10 |
**Severity:** major  
**Priority:** high

### [Riso] Available Teacher Calendar – New Lesson – Occupied Classroom – Classroom is unavailable
**Description:** Scope F10 / AC 01.2 — Scenario / Negative — Available Teacher Calendar filters an occupied Classroom.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room F10 Occupied` has a lesson on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff creates a Lesson from Available Teacher Calendar for `2026-09-15 10:00–11:00` JST. | The Classroom selector uses the entered Lesson interval. | flow = F10; target = 10:00–11:00 JST |
| 2 | HQ or CM Staff opens the Classroom selector. | `Room F10 Occupied` is absent. | existing = 10:00–11:00 JST |
**Severity:** major  
**Priority:** high

### [Riso] Calendar SF – Edit Lesson – Changed date – Classroom resets to blank
**Description:** Scope F11 / AC 01.3 — State Transition — Calendar edit clears stale Classroom.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- A Calendar Lesson uses `Room F11` on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff changes the Lesson date to `2026-09-16` in Calendar SF. | The Classroom field becomes blank. | flow = F11; original date = 2026-09-15; updated date = 2026-09-16 |
| 2 | HQ or CM Staff saves without selecting another Classroom. | Riso requiredness prevents saving without a Classroom. | classroom = blank |
**Severity:** major  
**Priority:** high

### [Riso] Calendar SF – Duplicate Lesson – Duplicated Classroom conflicts – Save is rejected
**Description:** Scope F12 / AC 02.1 — Regression / Negative — Calendar duplicate cannot retain a conflict.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- The source Calendar Lesson uses `Room F12`.
- Another Lesson uses `Room F12` on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff duplicates the Calendar Lesson to `2026-09-15 10:00–11:00` JST. | The duplicate re-evaluates `Room F12`. | flow = F12 |
| 2 | HQ or CM Staff saves with stale selection `Room F12`. | Save is rejected with `Room F12 is already in use for another class.` | classroom = Room F12 |
**Severity:** major  
**Priority:** high

### [Riso] Back Office Calendar – Edit Lesson – Vacant Classroom – Updated Classroom persists
**Description:** Scope F13 / AC 01.2 — Permission Matrix / Regression — BO Calendar edit supports a permitted user.
**Preconditions:**
- HQ Staff is logged in to Back Office with Classroom edit permission.
- `Room F13` is vacant at `Tokyo Center` on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ Staff selects `Room F13` while editing a Calendar Lesson in Back Office. | `Room F13` is selectable. | flow = F13; date = 2026-09-15; interval = 10:00–11:00 JST |
| 2 | HQ Staff saves the Lesson. | The Back Office Calendar Lesson displays `Room F13`. | classroom = Room F13 |
**Severity:** major  
**Priority:** high

### [Riso] Back Office Calendar – Edit Lesson – Occupied Classroom – Classroom is unavailable
**Description:** Scope F13 / AC 01.2 — Permission Matrix / Negative — Permitted BO Calendar edit filters an occupied Classroom.
**Preconditions:**
- HQ Staff is logged in to Back Office with Classroom edit permission.
- `Room F13 Occupied` has a lesson on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ Staff edits a Calendar Lesson for `2026-09-15 10:00–11:00` JST. | The Classroom selector uses the edited Lesson interval. | flow = F13; target = 10:00–11:00 JST |
| 2 | HQ Staff opens the Classroom selector. | `Room F13 Occupied` is absent. | existing = 10:00–11:00 JST |
**Severity:** major  
**Priority:** high
