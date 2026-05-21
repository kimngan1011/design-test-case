# Test Cases: LT-92532 — [Riso] Create LA – Validation Rules

## Suite: Create LA – Validation

---

### [Riso] Lesson Allocation – Create LA – Date Range – Start Date Same as End Date – Error Shown

**Description:** AC 01.3 / AC 01.4 — BVA boundary — Verify that setting Start date equal to End date triggers a validation error.

**Preconditions:**

- Logged in as HQ or CM user
- New Lesson Allocation configuration page is open (course selected)
- No existing LA for the same course in this date range

| #   | Action                                      | Expected Result                                                                         | Test Data         |
| --- | ------------------------------------------- | --------------------------------------------------------------------------------------- | ----------------- |
| 1   | Enter Start date = 2026-05-01               | Start date field shows 2026-05-01                                                       | Start: 2026-05-01 |
| 2   | Enter End date = 2026-05-01 (same as start) | Inline error appears under both date fields: "Start date must be earlier than End date" | End: 2026-05-01   |
| 3   | Confirm Save is blocked                     | Save/Confirm button is disabled or submission fails                                     |                   |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocation – Create LA – Date Range – Start Date One Day Before End Date – LA Created

**Description:** AC 01.3 / AC 01.4 — BVA just-inside boundary — Verify that Start date = End date - 1 day is accepted.

**Preconditions:**

- Logged in as HQ or CM user
- Configuration page open; no existing overlap for this course

| #   | Action                        | Expected Result                                | Test Data         |
| --- | ----------------------------- | ---------------------------------------------- | ----------------- |
| 1   | Enter Start date = 2026-05-01 | Start date shows 2026-05-01                    | Start: 2026-05-01 |
| 2   | Enter End date = 2026-05-02   | No validation error shown                      | End: 2026-05-02   |
| 3   | Click Save                    | LA is created successfully; user is redirected |                   |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocation – Create LA – Date Range – Start Date After End Date – Error on Both Fields

**Description:** AC 01.4 — Negative Testing / BVA — Verify that Start date > End date shows an error on both date fields.

**Preconditions:**

- Logged in as HQ or CM user
- Configuration page open

| #   | Action                                     | Expected Result                                                                                            | Test Data         |
| --- | ------------------------------------------ | ---------------------------------------------------------------------------------------------------------- | ----------------- |
| 1   | Enter Start date = 2026-06-01              | Start date shows 2026-06-01                                                                                | Start: 2026-06-01 |
| 2   | Enter End date = 2026-05-31 (before start) | Inline error appears under both Start date and End date fields: "Start date must be earlier than End date" | End: 2026-05-31   |
| 3   | Confirm Save is blocked                    | Save/Confirm button is disabled or submission fails                                                        |                   |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocation – Create LA – Past End Date – End Date = Today – Error Shown

**Description:** AC 01.4 — BVA at today's boundary — Verify that End date = today (not a future date) triggers the "End date must be a future date" error.

**Preconditions:**

- Logged in as HQ or CM user
- Configuration page open
- Today's date = 2026-03-23

| #   | Action                               | Expected Result                                                       | Test Data         |
| --- | ------------------------------------ | --------------------------------------------------------------------- | ----------------- |
| 1   | Enter Start date = 2026-03-01 (past) | Start date shows 2026-03-01                                           | Start: 2026-03-01 |
| 2   | Enter End date = 2026-03-23 (today)  | Inline error appears under End date: "End date must be a future date" | End: 2026-03-23   |
| 3   | Confirm Save is blocked              | Save/Confirm button is disabled or submission fails                   |                   |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocation – Create LA – Past End Date – End Date = Tomorrow – LA Created

**Description:** AC 01.4 — BVA just-above boundary — Verify that End date = tomorrow (future date) is accepted.

**Preconditions:**

- Logged in as HQ or CM user
- Configuration page open
- Today's date = 2026-03-23; no existing overlap for the course

| #   | Action                                 | Expected Result             | Test Data         |
| --- | -------------------------------------- | --------------------------- | ----------------- |
| 1   | Enter Start date = 2026-03-01          | Start date shows 2026-03-01 | Start: 2026-03-01 |
| 2   | Enter End date = 2026-03-24 (tomorrow) | No validation error shown   | End: 2026-03-24   |
| 3   | Click Save                             | LA is created successfully  |                   |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocation – Create LA – Both Dates in Past – Error on End Date

**Description:** AC 01.4 — Negative Testing — Verify that both start and end date in the past triggers enddate error.

**Preconditions:**

- Logged in as HQ or CM user
- Configuration page open
- Today's date = 2026-03-23

| #   | Action                               | Expected Result                                                       | Test Data         |
| --- | ------------------------------------ | --------------------------------------------------------------------- | ----------------- |
| 1   | Enter Start date = 2026-01-01 (past) | Start date shows 2026-01-01                                           | Start: 2026-01-01 |
| 2   | Enter End date = 2026-03-01 (past)   | Inline error appears under End date: "End date must be a future date" | End: 2026-03-01   |
| 3   | Confirm Save is blocked              | Save/Confirm button is disabled or submission fails                   |                   |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocation – Create LA – Overlap – Same AY + Location + Course + Overlapping Dates – Error at Course Section

**Description:** AC 01.4 — Decision Table / Negative Testing — Verify that selecting a course that already has an LA with an overlapping date range shows a course-section error.

**Preconditions:**

- Logged in as HQ or CM user
- Existing LA for student: Course "Math", AY 2026, Location A, Start = 2026-04-01, End = 2026-09-30
- Configuration page open with same AY 2026, Location A, Course "Math" selected

| #   | Action                                               | Expected Result                                                                                                                                                                            | Test Data         |
| --- | ---------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------- |
| 1   | Enter Start date = 2026-05-01 (overlaps existing LA) |                                                                                                                                                                                            | Start: 2026-05-01 |
| 2   | Enter End date = 2026-08-31 (overlaps existing LA)   | Error message appears at course section: "The selected course has a duration that overlaps with another instance of the same course created earlier. Please adjust the start or end date." | End: 2026-08-31   |
| 3   | Confirm Save is blocked                              | Save/Confirm button is disabled or submission fails                                                                                                                                        |                   |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocation – Create LA – Overlap – Same AY + Location + Course + Non-Overlapping Dates – LA Created

**Description:** AC 01.4 — Decision Table / Positive — Verify that same AY + Location + Course with non-overlapping date range does NOT trigger an overlap error.

**Preconditions:**

- Logged in as HQ or CM user
- Existing LA for student: Course "Math", AY 2026, Location A, Start = 2026-04-01, End = 2026-06-30
- Configuration page open with same AY 2026, Location A, Course "Math"

| #   | Action                                                     | Expected Result                    | Test Data         |
| --- | ---------------------------------------------------------- | ---------------------------------- | ----------------- |
| 1   | Enter Start date = 2026-07-01 (day after existing LA ends) | Start date field shows 2026-07-01  | Start: 2026-07-01 |
| 2   | Enter End date = 2026-09-30                                | No overlap error at course section | End: 2026-09-30   |
| 3   | Click Save                                                 | LA is created successfully         |                   |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocation – Create LA – Different Course, Same AY + Location + Overlapping Dates – LA Created

**Description:** AC 01.4 — Decision Table — Verify that overlapping dates for a **different** course do NOT trigger the overlap error (overlap validation is per course).

**Preconditions:**

- Logged in as HQ or CM user
- Existing LA for student: Course "Math", AY 2026, Location A, Start = 2026-04-01, End = 2026-09-30
- New LA being created: Course "English", AY 2026, Location A, same date range

| #   | Action                        | Expected Result                          | Test Data         |
| --- | ----------------------------- | ---------------------------------------- | ----------------- |
| 1   | Select "English" course       | English selected                         |                   |
| 2   | Enter Start date = 2026-04-01 | Start date shows 2026-04-01              | Start: 2026-04-01 |
| 3   | Enter End date = 2026-09-30   | No overlap error (different course)      | End: 2026-09-30   |
| 4   | Click Save                    | LA for "English" is created successfully |                   |

**Severity:** critical
**Priority:** high
