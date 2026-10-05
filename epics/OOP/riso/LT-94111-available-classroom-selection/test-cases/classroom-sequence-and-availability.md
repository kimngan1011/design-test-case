# Test Cases: LT-94111 — Classroom Sequence and Availability

## Suite: Classroom Sequence and Availability

### [Riso] Classroom Master – Sequence – Blank value – Classroom saves
**Description:** AC 01.1 — Equivalence Partitioning — An optional Sequence may be blank.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- A Classroom named `Room Blank` does not exist at `Tokyo Center`.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `Room Blank` without a Sequence. | The form accepts a blank Sequence. | sequence = blank |
| 2 | HQ or CM Staff saves the Classroom. | `Room Blank` is saved with no Sequence value. | location = Tokyo Center |
**Severity:** minor  
**Priority:** medium

### [Riso] Classroom Master – Sequence – Positive integer – Classroom saves
**Description:** AC 01.1 — Equivalence Partitioning — A supplied positive integer is accepted.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters Sequence `12` for `Room Twelve`. | The Sequence field accepts `12`. | sequence = 12 |
| 2 | HQ or CM Staff saves the Classroom. | `Room Twelve` is saved with Sequence `12`. | location = Tokyo Center |
**Severity:** minor  
**Priority:** medium

### [Riso] Classroom Master – Sequence – Zero – Save is blocked
**Description:** AC 01.1 — BVA / Negative — Zero is not a positive integer.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters Sequence `0` for `Room Zero`. | The form rejects `0` as a Sequence value. | sequence = 0 |
| 2 | HQ or CM Staff saves the Classroom. | `Room Zero` is not created with Sequence `0`. | classroom = Room Zero |
**Severity:** minor  
**Priority:** medium

### [Riso] Classroom Master – Sequence – Negative integer – Save is blocked
**Description:** AC 01.1 — BVA / Negative — A negative value is rejected.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters Sequence `-1` for `Room Negative`. | The form rejects `-1` as a Sequence value. | sequence = -1 |
| 2 | HQ or CM Staff saves the Classroom. | `Room Negative` is not created with Sequence `-1`. | classroom = Room Negative |
**Severity:** minor  
**Priority:** medium

### [Riso] Classroom Master – Sequence – Decimal value – Save is blocked
**Description:** AC 01.1 — Equivalence Partitioning / Negative — A decimal is rejected.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters Sequence `1.5` for `Room Decimal`. | The form rejects `1.5` as a Sequence value. | sequence = 1.5 |
| 2 | HQ or CM Staff saves the Classroom. | `Room Decimal` is not created with Sequence `1.5`. | classroom = Room Decimal |
**Severity:** minor  
**Priority:** medium

### [Riso] Classroom Master – Sequence – Alphabetic value – Save is blocked
**Description:** AC 01.1 — Equivalence Partitioning / Negative — Nonnumeric input is rejected.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters Sequence `A1` for `Room Alpha`. | The form rejects `A1` as a Sequence value. | sequence = A1 |
| 2 | HQ or CM Staff saves the Classroom. | `Room Alpha` is not created with Sequence `A1`. | classroom = Room Alpha |
**Severity:** minor  
**Priority:** medium

### [Riso] Classroom Master – Sequence – Duplicate positive value – Classroom saves
**Description:** AC 01.1 — Equivalence Partitioning — Duplicate positive Sequences are allowed.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room Existing` at `Tokyo Center` has Sequence `5`.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters Sequence `5` for `Room Duplicate`. | The form accepts the duplicate positive Sequence. | existing sequence = 5; new sequence = 5 |
| 2 | HQ or CM Staff saves the Classroom. | `Room Duplicate` is saved with Sequence `5`. | location = Tokyo Center |
**Severity:** minor  
**Priority:** medium

### [Riso] Lesson Upsert – Classroom selector – Missing availability input – No option state remains
**Description:** AC 01.2 — Decision Table / Component — A room is unavailable before every prerequisite is set.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room A` is vacant at `Tokyo Center` on `2026-09-15` from `10:00` to `11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff supplies Location, date, and start time without an end time. | The Classroom selector has no selectable Classroom. | date = 2026-09-15; start = 10:00 JST; end = blank |
| 2 | HQ or CM Staff opens the Classroom selector. | The selector shows `No option`. | missing input = end time |
**Severity:** major  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – Selected Location – Only that Location's Classrooms are shown
**Description:** AC 01.2 — Decision Table / Component — The selector is scoped to the Lesson Location.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Tokyo Room` belongs to `Tokyo Center` and is vacant on `2026-09-15 10:00–11:00` JST.
- `Osaka Room` belongs to `Osaka Center` and is vacant on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `Tokyo Center` and `2026-09-15 10:00–11:00` JST for a new Lesson. | The selector evaluates Classrooms for `Tokyo Center`. | lesson location = Tokyo Center |
| 2 | HQ or CM Staff opens the Classroom selector. | `Tokyo Room` is shown and `Osaka Room` is absent. | classroom locations = Tokyo Center / Osaka Center |
**Severity:** critical  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – Same Location occupied – Classroom is hidden
**Description:** AC 01.2 — Decision Table / Negative — An overlap blocks the Classroom at the Lesson Location.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Tokyo Occupied Room` belongs to `Tokyo Center` and has a Lesson on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `Tokyo Center` and `2026-09-15 10:00–11:00` JST for a new Lesson. | The selector evaluates the same Location and interval. | lesson location = Tokyo Center |
| 2 | HQ or CM Staff opens the Classroom selector. | `Tokyo Occupied Room` is absent. | classroom location = Tokyo Center; existing interval = 10:00–11:00 JST |
**Severity:** critical  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – Different Location occupied – Selected Location's vacant Classroom remains shown
**Description:** AC 01.2 — Decision Table / Regression — An overlap in another Location does not suppress a vacant local Classroom.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Tokyo Vacant Room` belongs to `Tokyo Center` and is vacant on `2026-09-15 10:00–11:00` JST.
- `Osaka Occupied Room` belongs to `Osaka Center` and has a Lesson on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `Tokyo Center` and `2026-09-15 10:00–11:00` JST for a new Lesson. | The selector evaluates `Tokyo Center` only. | lesson location = Tokyo Center |
| 2 | HQ or CM Staff opens the Classroom selector. | `Tokyo Vacant Room` is shown and `Osaka Occupied Room` is absent. | selected Location = Tokyo Center; occupied Location = Osaka Center |
**Severity:** critical  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – Exact overlap – Occupied Classroom is hidden
**Description:** AC 01.2 — Decision Table / Negative — Exact overlap is unavailable.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room Exact` has a lesson on `2026-09-15` from `10:00` to `11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters a new Lesson from `10:00` to `11:00` JST. | The availability query uses the entered lesson interval. | date = 2026-09-15; target = 10:00–11:00 JST |
| 2 | HQ or CM Staff opens the Classroom selector. | `Room Exact` is absent. | existing = 10:00–11:00 JST |
**Severity:** critical  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – Same start overlap – Occupied Classroom is hidden
**Description:** AC 01.2 — Decision Table / Negative — Same-start overlap is unavailable.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room Same Start` has a lesson on `2026-09-15` from `10:00` to `10:30` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters a new Lesson from `10:00` to `11:00` JST. | The availability query uses the entered lesson interval. | date = 2026-09-15; target = 10:00–11:00 JST |
| 2 | HQ or CM Staff opens the Classroom selector. | `Room Same Start` is absent. | existing = 10:00–10:30 JST |
**Severity:** critical  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – Same end overlap – Occupied Classroom is hidden
**Description:** AC 01.2 — Decision Table / Negative — Same-end overlap is unavailable.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room Same End` has a lesson on `2026-09-15` from `10:30` to `11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters a new Lesson from `10:00` to `11:00` JST. | The availability query uses the entered lesson interval. | date = 2026-09-15; target = 10:00–11:00 JST |
| 2 | HQ or CM Staff opens the Classroom selector. | `Room Same End` is absent. | existing = 10:30–11:00 JST |
**Severity:** critical  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – Existing lesson inside target – Occupied Classroom is hidden
**Description:** AC 01.2 — Decision Table / Negative — A lesson within the target period makes the room unavailable.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room Inside` has a lesson on `2026-09-15` from `10:20` to `10:40` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters a new Lesson from `10:00` to `11:00` JST. | The availability query uses the entered lesson interval. | date = 2026-09-15; target = 10:00–11:00 JST |
| 2 | HQ or CM Staff opens the Classroom selector. | `Room Inside` is absent. | existing = 10:20–10:40 JST |
**Severity:** critical  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – Target inside existing lesson – Occupied Classroom is hidden
**Description:** AC 01.2 — Boundary / Negative — A containing existing lesson makes the room unavailable.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room Contains` has a lesson on `2026-09-15` from `09:00` to `12:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters a new Lesson from `10:00` to `11:00` JST. | The availability query uses the entered lesson interval. | date = 2026-09-15; target = 10:00–11:00 JST |
| 2 | HQ or CM Staff opens the Classroom selector. | `Room Contains` is absent. | existing = 09:00–12:00 JST |
**Severity:** critical  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – Adjacent interval – Classroom remains selectable
**Description:** AC 01.2 — BVA — A room ending exactly at the target start is vacant.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room Adjacent` has a lesson on `2026-09-15` from `09:00` to `10:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters a new Lesson from `10:00` to `11:00` JST. | The availability query uses the entered lesson interval. | date = 2026-09-15; target = 10:00–11:00 JST |
| 2 | HQ or CM Staff opens the Classroom selector. | `Room Adjacent` is selectable. | existing end = target start = 10:00 JST |
**Severity:** critical  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – Next adjacent interval – Classroom remains selectable
**Description:** AC 01.2 — BVA — A room starting exactly at the target end is vacant.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room Next Adjacent` has a lesson on `2026-09-15` from `11:00` to `12:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters a new Lesson from `10:00` to `11:00` JST. | The availability query uses the entered lesson interval. | date = 2026-09-15; target = 10:00–11:00 JST |
| 2 | HQ or CM Staff opens the Classroom selector. | `Room Next Adjacent` is selectable. | existing start = target end = 11:00 JST |
**Severity:** critical  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – Left partial overlap – Occupied Classroom is hidden
**Description:** AC 01.2 — Decision Table / Negative — A lesson beginning before and ending within the target is unavailable.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room Left Partial` has a lesson on `2026-09-15` from `09:30` to `10:30` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters a new Lesson from `10:00` to `11:00` JST. | The availability query uses the entered lesson interval. | date = 2026-09-15; target = 10:00–11:00 JST |
| 2 | HQ or CM Staff opens the Classroom selector. | `Room Left Partial` is absent. | existing = 09:30–10:30 JST |
**Severity:** critical  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – Right partial overlap – Occupied Classroom is hidden
**Description:** AC 01.2 — Decision Table / Negative — A lesson beginning within and ending after the target is unavailable.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room Right Partial` has a lesson on `2026-09-15` from `10:30` to `11:30` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters a new Lesson from `10:00` to `11:00` JST. | The availability query uses the entered lesson interval. | date = 2026-09-15; target = 10:00–11:00 JST |
| 2 | HQ or CM Staff opens the Classroom selector. | `Room Right Partial` is absent. | existing = 10:30–11:30 JST |
**Severity:** critical  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – JST to UTC date boundary – Availability uses the same instant
**Description:** AC 01.2 — BVA / Regression — Availability works at a JST/UTC calendar boundary.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room Boundary` has a lesson from `2026-09-14 15:30` to `16:30` UTC.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters a Lesson on `2026-09-15` from `00:30` to `01:30` JST. | The entered JST interval maps to `2026-09-14 15:30–16:30` UTC. | JST = 2026-09-15 00:30–01:30; UTC = 2026-09-14 15:30–16:30 |
| 2 | HQ or CM Staff opens the Classroom selector. | `Room Boundary` is absent because both representations describe the same interval. | room = Room Boundary |
**Severity:** major  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – Sort tie breakers – Available Classrooms follow the complete order
**Description:** AC 01.2 — Scenario / Pairwise — Sequence, Name, and created date determine order.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room B` has Sequence `1` and was created `2026-01-02`.
- `Room A New` has Sequence `2` and was created `2026-02-02`.
- `Room A Old` has Sequence `2` and was created `2026-01-01`.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters a vacant Lesson interval at `Tokyo Center`. | The Classroom selector has three available rooms. | date = 2026-09-15; interval = 13:00–14:00 JST |
| 2 | HQ or CM Staff opens the Classroom selector. | The visible order is `Room B`, `Room A Old`, `Room A New`. | Sequence ASC; Name ASC; created date ASC |
**Severity:** minor  
**Priority:** medium

### [Riso] Lesson Upsert – Classroom selector – Available rooms – First sorted Classroom is prefilled
**Description:** AC 01.2 — Decision Table — The first available sorted Classroom is preselected.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room First` has Sequence `1` and is vacant at `Tokyo Center`.
- `Room Second` has Sequence `2` and is vacant at `Tokyo Center`.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff completes Location, date, start time, and end time for a new Lesson. | The Classroom field is populated automatically. | date = 2026-09-15; interval = 13:00–14:00 JST |
| 2 | HQ or CM Staff views the Classroom value. | The value is `Room First`. | first sorted room = Room First |
**Severity:** major  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – First prefilled Classroom becomes occupied – Prefill moves to the next available Classroom
**Description:** AC 01.2 — State Transition / Regression — The prefilled value tracks the current available Classroom list.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room First` has Sequence `1` and `Room Second` has Sequence `2` at `Tokyo Center`.
- Both Classrooms are vacant on `2026-09-15 13:00–14:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff completes a new Lesson at `Tokyo Center` for `2026-09-15 13:00–14:00` JST. | Classroom is prefilled with `Room First`. | initial available order = Room First, Room Second |
| 2 | HQ or CM Staff changes the Lesson interval to `2026-09-15 14:00–15:00` JST where `Room First` is occupied and `Room Second` is vacant. | Classroom is reset and the availability list is re-evaluated. | Room First occupied = 14:00–15:00 JST |
| 3 | HQ or CM Staff opens the Classroom selector. | `Room Second` is the suggested first available Classroom and `Room First` is absent. | expected prefill candidate = Room Second |
**Severity:** critical  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – No vacant room – Classroom remains blank
**Description:** AC 01.2 — Decision Table / Negative — No vacancy leaves the selection blank.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- Every Classroom at `Tokyo Center` overlaps `2026-09-15 13:00–14:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff completes Location, date, start time, and end time for a new Lesson. | The Classroom field remains blank. | date = 2026-09-15; interval = 13:00–14:00 JST |
| 2 | HQ or CM Staff opens the Classroom selector. | No Classroom is selectable. | vacancy count = 0 |
**Severity:** major  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – No vacant room – Exact empty-state text is shown
**Description:** AC 01.2 — Component — The empty state uses the specified text.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- Every Classroom at `Tokyo Center` overlaps `2026-09-15 13:00–14:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff completes a new Lesson for `2026-09-15 13:00–14:00` JST. | The Classroom field remains blank. | location = Tokyo Center |
| 2 | HQ or CM Staff opens the Classroom selector. | The selector shows exactly `No option`. | expected text = No option |
**Severity:** major  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – Draft-status lesson occupies – Classroom is hidden
**Description:** AC 01.2 — Decision Table / Negative — A Draft-status Lesson occupies the Classroom the same as any other non-Cancelled status.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room Draft Block` at `Tokyo Center` has a Draft-status Lesson on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters a new Lesson at `Tokyo Center` from `10:00` to `11:00` JST on `2026-09-15`. | The availability query uses the entered lesson interval. | date = 2026-09-15; target = 10:00–11:00 JST |
| 2 | HQ or CM Staff opens the Classroom selector. | `Room Draft Block` is absent because the Draft-status Lesson still occupies it. | existing lesson status = Draft; existing interval = 10:00–11:00 JST |
**Severity:** critical  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – Published-status lesson occupies – Classroom is hidden
**Description:** AC 01.2 — Decision Table / Negative — A Published-status Lesson occupies the Classroom.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room Published Block` at `Tokyo Center` has a Published-status Lesson on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters a new Lesson at `Tokyo Center` from `10:00` to `11:00` JST on `2026-09-15`. | The availability query uses the entered lesson interval. | date = 2026-09-15; target = 10:00–11:00 JST |
| 2 | HQ or CM Staff opens the Classroom selector. | `Room Published Block` is absent because the Published-status Lesson still occupies it. | existing lesson status = Published; existing interval = 10:00–11:00 JST |
**Severity:** critical  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – Completed-status lesson occupies – Classroom is hidden
**Description:** AC 01.2 — Decision Table / Negative — A Completed-status Lesson still occupies the Classroom for its recorded interval.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room Completed Block` at `Tokyo Center` has a Completed-status Lesson on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters a new Lesson at `Tokyo Center` from `10:00` to `11:00` JST on `2026-09-15`. | The availability query uses the entered lesson interval. | date = 2026-09-15; target = 10:00–11:00 JST |
| 2 | HQ or CM Staff opens the Classroom selector. | `Room Completed Block` is absent because the Completed-status Lesson still occupies it. | existing lesson status = Completed; existing interval = 10:00–11:00 JST |
**Severity:** critical  
**Priority:** high

### [Riso] Lesson Upsert – Classroom selector – Cancelled-status lesson – Classroom remains selectable
**Description:** AC 01.2 — Decision Table — Cancelled is the only lesson status excluded from the occupied check.
**Preconditions:**
- HQ or CM Staff is logged in to the Riso Salesforce org.
- `Room Cancelled Free` at `Tokyo Center` has a Cancelled-status Lesson on `2026-09-15 10:00–11:00` JST.
| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters a new Lesson at `Tokyo Center` from `10:00` to `11:00` JST on `2026-09-15`. | The availability query uses the entered lesson interval. | date = 2026-09-15; target = 10:00–11:00 JST |
| 2 | HQ or CM Staff opens the Classroom selector. | `Room Cancelled Free` is selectable because a Cancelled-status Lesson does not occupy the Classroom. | existing lesson status = Cancelled; existing interval = 10:00–11:00 JST |
**Severity:** critical  
**Priority:** high
