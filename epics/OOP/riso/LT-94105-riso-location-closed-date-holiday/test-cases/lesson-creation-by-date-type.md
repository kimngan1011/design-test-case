# Test Cases: LT-94105 — Riso Location Closed Date and Holiday

## Suite: Lesson Creation by Date Type

### [Riso] Lesson creation – One-time lesson – Closed Date – Lesson is created

**Description:** AC 02.1 — Decision Table — Confirms one-time creation remains allowed on Closed Date.

**Preconditions:**
- Logged in as HQ or CM Staff for Riso Center A.
- today = `2026-07-01`; `2026-07-13` is Closed Date in Center A 2026.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open one-time lesson creation. | The lesson form opens. | lesson_date = 2026-07-13; Type = Closed Date |
| 2 | Enter a one-time lesson on `2026-07-13` and save. | The lesson saves. | start = 10:00 JST; end = 11:00 JST |
| 3 | Open the saved lesson. | The lesson date is `2026-07-13` and the lesson exists. | expected occurrences = 1 |

**Severity:** major
**Priority:** high

---

### [Riso] Extend Recurrence – Skip Closed Date enabled – Closed Date occurrence is skipped

**Description:** AC 02.1 — Decision Table / Regression — Confirms Extend Recurrence inherits Skip Closed Date and skips only Closed Date occurrences in the extension range.

**Preconditions:**
- Logged in as HQ or CM Staff for Riso Center A.
- A weekly recurring schedule ends on `2026-07-13` with Skip Closed Date enabled and no later occurrences.
- `2026-07-20` is a Closed Date; `2026-07-27` is a normal operating date.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the recurring schedule and select Extend Recurrence. | The extension form shows the saved Skip Closed Date setting as enabled and not editable. | existing end date = 2026-07-13; skip_closed_date = enabled |
| 2 | Set the recurrence end date to `2026-07-27` and confirm the extension. | The extension completes and evaluates the new weekly dates `2026-07-20` and `2026-07-27`. | extension end date = 2026-07-27 |
| 3 | Open the extended lesson chain and search both added dates. | No lesson exists on Closed Date `2026-07-20`; one normal recurring lesson exists on `2026-07-27`. | expected count 07-20 = 0; expected count 07-27 = 1 |

**Severity:** major
**Priority:** high

---

### [Riso] Extend Recurrence – Skip Closed Date enabled – Public Holiday occurrence is created

**Description:** AC 02.1 — Decision Table / Regression — Confirms Extend Recurrence does not suppress a Public Holiday occurrence when the inherited Skip Closed Date setting is enabled.

**Preconditions:**
- Logged in as HQ or CM Staff for Riso Center A.
- A weekly recurring schedule ends on `2026-07-13` with Skip Closed Date enabled and no later occurrences.
- `2026-07-20` is a Public Holiday; `2026-07-27` is a normal operating date.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the recurring schedule and select Extend Recurrence. | The extension form shows the saved Skip Closed Date setting as enabled and not editable. | existing end date = 2026-07-13; skip_closed_date = enabled |
| 2 | Set the recurrence end date to `2026-07-27` and confirm the extension. | The extension completes and evaluates the new weekly dates `2026-07-20` and `2026-07-27`. | extension end date = 2026-07-27 |
| 3 | Open the extended lesson chain and search both added dates. | One normal recurring lesson exists on Public Holiday `2026-07-20` and on `2026-07-27`. | expected count 07-20 = 1; expected count 07-27 = 1 |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson creation – One-time lesson – Public Holiday – Lesson is created

**Description:** AC 02.1 — Decision Table — Confirms one-time creation is allowed on Public Holiday.

**Preconditions:**
- Logged in as HQ or CM Staff for Riso Center A.
- today = `2026-07-01`; `2026-07-14` is Holiday in Center A 2026.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open one-time lesson creation. | The lesson form opens. | lesson_date = 2026-07-14; Type = Public Holiday |
| 2 | Enter a one-time lesson on `2026-07-14` and save. | The lesson saves. | start = 10:00 JST; end = 11:00 JST |
| 3 | Open the saved lesson. | The lesson date is `2026-07-14` and the lesson exists. | expected occurrences = 1 |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson schedule – Manual Add Lesson – Closed Date – Lesson is created

**Description:** AC 02.1 — Decision Table / Regression — Confirms a manually added occurrence remains allowed on Closed Date.

**Preconditions:**
- Logged in as HQ or CM Staff for Riso Center A.
- A recurring schedule exists; `2026-07-15` is Closed Date in Center A 2026.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the recurring schedule and choose Add Lesson. | The Add Lesson form opens. | target_date = 2026-07-15; Type = Closed Date |
| 2 | Add an occurrence on `2026-07-15` at 10:00–11:00 JST. | The occurrence saves. | start = 10:00 JST; end = 11:00 JST |
| 3 | View the schedule occurrences. | One manually added lesson exists on `2026-07-15`. | expected occurrences on date = 1 |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson schedule – Manual Add Lesson – Public Holiday – Lesson is created

**Description:** AC 02.1 — Decision Table / Regression — Confirms a manually added occurrence is allowed on Public Holiday.

**Preconditions:**
- Logged in as HQ or CM Staff for Riso Center A.
- A recurring schedule exists; `2026-07-16` is Holiday in Center A 2026.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the recurring schedule and choose Add Lesson. | The Add Lesson form opens. | target_date = 2026-07-16; Type = Public Holiday |
| 2 | Add an occurrence on `2026-07-16` at 10:00–11:00 JST. | The occurrence saves. | start = 10:00 JST; end = 11:00 JST |
| 3 | View the schedule occurrences. | One manually added lesson exists on `2026-07-16`. | expected occurrences on date = 1 |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson schedule – Recurring generation – Skip Closed Date enabled – Closed Date occurrence is skipped

**Description:** AC 02.1 — State Transition / Regression — Confirms the recurring chain omits a Closed Date occurrence only when Skip Closed Date is enabled.

**Preconditions:**
- Logged in as HQ or CM Staff for Riso Center A.
- today = `2026-07-01`; `2026-07-20` is Closed Date; no other Closed Dates occur on the three weekly target dates; Skip Closed Date is enabled.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Create a weekly recurring schedule starting `2026-07-13` for three Mondays with Skip Closed Date enabled. | The schedule saves with Skip Closed Date enabled. | dates = 2026-07-13, 2026-07-20, 2026-07-27; Type on 07-20 = Closed Date; Skip Closed Date = enabled |
| 2 | Open generated occurrences. | Lessons exist on `2026-07-13` and `2026-07-27`. | expected created dates = 07-13, 07-27 |
| 3 | Search for an occurrence on `2026-07-20`. | No lesson exists on the Closed Date. | expected occurrences on 07-20 = 0 |

**Severity:** major
**Priority:** high

---

### [Riso] Recurring lesson – Legacy Skip Closed Date disabled – Closed Date occurrence – Occurrence is created

**Description:** AC 02.1 — Decision Table / Regression — Confirms a Closed Date occurrence is created normally when Skip Closed Date is disabled.

**Preconditions:**
- Logged in as HQ or CM Staff for Riso Center A.
- `2026-07-20` is Closed Date; the schedule is created with Skip Closed Date disabled.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Create a three-Monday recurring schedule with Skip Closed Date disabled. | The schedule saves with the setting disabled. | dates = 2026-07-13, 07-20, 07-27; skip_closed_date = disabled |
| 2 | Open generated occurrences. | Lessons exist on `2026-07-13`, `2026-07-20`, and `2026-07-27`. | expected created dates = 07-13, 07-20, 07-27 |
| 3 | Open the `2026-07-20` occurrence. | One normal recurring lesson exists on the Closed Date. | expected occurrences on 07-20 = 1; expected origin = recurring schedule |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson schedule – Recurring generation – Public Holiday occurrence – Occurrence is created

**Description:** AC 02.1 — State Transition / Regression — Confirms the recurring chain includes a Public Holiday occurrence.

**Preconditions:**
- Logged in as HQ or CM Staff for Riso Center A.
- today = `2026-07-01`; `2026-07-20` is Holiday; no other Closed Dates occur on the three weekly target dates.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Create a weekly recurring schedule starting `2026-07-13` for three Mondays. | The schedule saves. | dates = 2026-07-13, 2026-07-20, 2026-07-27; Type on 07-20 = Public Holiday |
| 2 | Open generated occurrences. | Lessons exist on all three stated dates. | expected created dates = 07-13, 07-20, 07-27 |
| 3 | Open the `2026-07-20` lesson. | The lesson is a normal schedule occurrence, not a manually added occurrence. | expected origin = recurring schedule |

**Severity:** major
**Priority:** high

---

### [Riso] Recurring lesson – Retry after Holiday creation – Duplicate retry – One schedule chain remains

**Description:** AC 02.1 — Negative / Regression — Confirms an interrupted retry does not duplicate the Holiday occurrence or sequence.

**Preconditions:**
- Logged in as HQ or CM Staff for Riso Center A.
- `2026-07-20` is Holiday; no schedule exists with name `Riso Holiday Retry`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Submit the `Riso Holiday Retry` three-Monday schedule and simulate a client retry. | The service accepts one initial request or prevents the duplicate retry. | dates = 2026-07-13, 07-20, 07-27; retries = 1 |
| 2 | Open all occurrences with the schedule name. | Three occurrences exist, including `2026-07-20`. | expected total = 3 |
| 3 | Inspect occurrence dates and sequence. | Each target date appears once and no duplicated sequence number exists. | expected count per date = 1 |

**Severity:** major
**Priority:** high

---

### [Riso] Recurring lesson – JST and UTC boundary – Holiday occurrence – Generation uses the JST calendar date

**Description:** AC 02.1 — Boundary / Regression — Confirms recurring generation uses the Riso business date across the JST–UTC date boundary.

**Preconditions:**
- Logged in as HQ or CM Staff for Riso Center A.
- generation time = `2026-07-20 00:30 Asia/Tokyo` (`2026-07-19 15:30 UTC`); `2026-07-20` is Holiday.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Create a schedule that generates an occurrence on `2026-07-20`. | The schedule is accepted at the stated JST/UTC boundary. | JST = 2026-07-20 00:30; UTC = 2026-07-19 15:30 |
| 2 | Run or wait for the occurrence generation. | The date is classified as `2026-07-20` Holiday. | target_date = 2026-07-20; Type = Holiday |
| 3 | Open the generated occurrence. | One normal recurring lesson exists on `2026-07-20`. | expected occurrences on 07-20 = 1 |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson schedule – Recurring generation – Public Holiday with Skip Closed Date enabled – Occurrence is created

**Description:** AC 02.1 — Decision Table / Regression — Confirms the ticket's Public Holiday rule overrides legacy Skip Closed Date behavior.

**Preconditions:**
- Logged in as HQ or CM Staff for Riso Center A.
- today = `2026-07-01`; `2026-07-20` is Holiday; the recurring schedule has Skip Closed Date enabled.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Create a weekly recurring schedule starting `2026-07-13` for three Mondays with Skip Closed Date enabled. | The schedule saves with the setting enabled. | skip_closed_date = enabled |
| 2 | Open generated occurrences. | Lessons exist on `2026-07-13`, `2026-07-20`, and `2026-07-27`. | Public Holiday = 2026-07-20 |
| 3 | Open the `2026-07-20` lesson. | The Public Holiday occurrence exists despite Skip Closed Date being enabled. | expected occurrences on 07-20 = 1 |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson creation – JST and UTC boundary – Public Holiday date – One-time lesson uses the JST date

**Description:** AC 02.1 — Boundary / Regression — Confirms lesson creation classifies the date in JST when UTC is the previous calendar day.

**Preconditions:**
- Logged in as HQ or CM Staff for Riso Center A.
- current time = `2026-07-20 00:30 Asia/Tokyo` (`2026-07-19 15:30 UTC`); `2026-07-20` is Holiday.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open one-time lesson creation with the stated clocks. | The business date is treated as `2026-07-20`. | JST = 2026-07-20 00:30; UTC = 2026-07-19 15:30 |
| 2 | Create a lesson for `2026-07-20` at 10:00–11:00 JST. | The lesson saves on `2026-07-20`. | lesson_date = 2026-07-20; Type = Holiday |
| 3 | Open the saved lesson. | The displayed lesson date is `2026-07-20`, not `2026-07-19`. | expected date = 2026-07-20 |

**Severity:** major
**Priority:** high
