# Test Cases: LT-94111 — Classroom Reset and Recurrence

## Suite: Classroom Reset and Recurrence

### [Riso] Lesson Upsert – Classroom – Changed Location – Classroom resets to blank
**Description:** AC 01.3 — State Transition — Location change clears a selected Classroom.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- An editable Lesson at `Tokyo Center` has `Room Reset` on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff changes Location to `Osaka Center`. | The Classroom field becomes blank. | original location = Tokyo Center; updated location = Osaka Center |
| 2 | HQ or CM Staff views the Classroom field. | `Room Reset` is not retained. | classroom = blank |
**Severity:** major  
**Priority:** high

### [Riso] Lesson Upsert – Classroom – Changed lesson date – Classroom resets to blank
**Description:** AC 01.3 — State Transition — Date change clears a selected Classroom.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- An editable Lesson has `Room Reset` on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff changes the lesson date to `2026-09-16`. | The Classroom field becomes blank. | original date = 2026-09-15; updated date = 2026-09-16 |
| 2 | HQ or CM Staff views the Classroom field. | `Room Reset` is not retained. | classroom = blank |
**Severity:** major  
**Priority:** high

### [Riso] Lesson Upsert – Classroom – Changed start time – Classroom resets to blank
**Description:** AC 01.3 — State Transition — Start-time change clears a selected Classroom.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- An editable Lesson has `Room Reset` on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff changes start time to `11:00` JST. | The Classroom field becomes blank. | original = 10:00–11:00 JST; updated start = 11:00 JST |
| 2 | HQ or CM Staff views the Classroom field. | `Room Reset` is not retained. | classroom = blank |
**Severity:** major  
**Priority:** high

### [Riso] Lesson Upsert – Classroom – Changed end time – Classroom resets to blank
**Description:** AC 01.3 — State Transition — End-time change clears a selected Classroom.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- An editable Lesson has `Room Reset` on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff changes end time to `12:00` JST. | The Classroom field becomes blank. | original = 10:00–11:00 JST; updated end = 12:00 JST |
| 2 | HQ or CM Staff views the Classroom field. | `Room Reset` is not retained. | classroom = blank |
**Severity:** major  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – Opened after reset – First vacant Classroom is suggested
**Description:** AC 01.3 — Decision Table — Reset does not auto-select until the selector opens.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- An editable Lesson has been reset by changing its end time to `12:00` JST.
- `Room Suggest` is the first sorted vacant Classroom at the updated interval.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff views the Classroom field before opening it. | The Classroom field remains blank. | date = 2026-09-15; interval = 10:00–12:00 JST |
| 2 | HQ or CM Staff opens the Classroom selector. | `Room Suggest` is suggested as the first vacant Classroom. | first vacant = Room Suggest |
**Severity:** major  
**Priority:** high

### [Riso] Weekly Recurrence – Classroom selector – First occurrence vacant – Later conflict does not block selection
**Description:** AC 01.4 — State Transition / Regression — Availability evaluates only the selected first occurrence.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- A weekly recurrence starts `2026-09-15 10:00–11:00` JST.
- `Room Weekly` is vacant on `2026-09-15` and occupied on `2026-09-22 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff creates the weekly recurrence and opens the Classroom selector. | `Room Weekly` is selectable. | selected = 2026-09-15 10:00–11:00 JST; later = 2026-09-22 10:00–11:00 JST |
| 2 | HQ or CM Staff saves the recurrence with `Room Weekly`. | The later occupied occurrence does not block this save. | recurrence = weekly |
**Severity:** major  
**Priority:** high

### [Riso] Weekly Recurrence – Classroom selector – First occurrence occupied – Classroom is unavailable
**Description:** AC 01.4 — State Transition / Negative — A clash at the selected first occurrence blocks selection.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room Weekly First` is occupied on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff creates a weekly recurrence starting `2026-09-15 10:00–11:00` JST. | The selector uses the first occurrence. | first occurrence = 2026-09-15 10:00–11:00 JST |
| 2 | HQ or CM Staff opens the Classroom selector. | `Room Weekly First` is absent. | room = Room Weekly First |
**Severity:** major  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – Location then time changed quickly – Selector reflects the latest Location
**Description:** AC 01.3 — Negative / Concurrent-stale-state — A fast Location-then-time change must not let a stale response overwrite the latest criteria.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Tokyo Room` belongs to `Tokyo Center` and is vacant on `2026-09-15 10:00–11:30` JST.
- `Osaka Room` belongs to `Osaka Center` and is vacant on `2026-09-15 10:00–11:30` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff changes Location from `Tokyo Center` to `Osaka Center`, then immediately changes the end time from `11:00` to `11:30` JST before the Classroom selector finishes loading. | Both changes are submitted in quick succession. | location change = Tokyo Center → Osaka Center; end-time change = 11:00 → 11:30 JST (immediate) |
| 2 | HQ or CM Staff opens the Classroom selector. | The selector shows only `Osaka Room` for `10:00–11:30` JST at `Osaka Center`; `Tokyo Room` is absent. | expected location = Osaka Center; expected interval = 10:00–11:30 JST |
**Severity:** major  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – Repeated rapid time edits – Selector settles on the final interval only
**Description:** AC 01.3 — Negative / Concurrent-stale-state — Multiple rapid edits to the same field must not leave a stale intermediate result displayed.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room Mid` at `Tokyo Center` is vacant only during `10:00–10:30` JST and occupied from `10:30` JST onward on `2026-09-15`.
- `Room Final` at `Tokyo Center` is vacant during `10:00–11:00` JST on `2026-09-15`.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters end time `10:30`, then `10:45`, then `11:00` JST in quick succession without pausing between edits. | Each edit is submitted before the previous request necessarily returns. | end-time sequence = 10:30 → 10:45 → 11:00 JST (rapid) |
| 2 | HQ or CM Staff opens the Classroom selector. | The selector reflects only the final `10:00–11:00` JST interval: `Room Mid` is absent and `Room Final` is shown. | final interval = 10:00–11:00 JST |
**Severity:** minor  
**Priority:** medium
