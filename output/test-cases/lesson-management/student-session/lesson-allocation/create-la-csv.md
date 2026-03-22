# Test Cases: LT-92532 — [Riso] Create LA – CSV Bulk Import

## Suite: Create LA – CSV Import

---

### [Riso] Lesson Allocation – CSV Import – Valid CSV – All LAs Created

**Description:** AC 01.5 — Equivalence Partitioning (valid partition) — Verify that a valid CSV file with correct data creates all LAs successfully.

**Preconditions:**

- Logged in as HQ or CM user
- Valid CSV file prepared with columns: student_id, AY, location, course, type, purchased_slot, start_date, end_date
- All rows contain valid, non-overlapping future end dates and start < end
- No existing LAs that would trigger overlap errors

| #   | Action                                                       | Expected Result                                                                            | Test Data                |
| --- | ------------------------------------------------------------ | ------------------------------------------------------------------------------------------ | ------------------------ |
| 1   | Navigate to the SF CSV import function for Lesson Allocation | Import page is displayed                                                                   |                          |
| 2   | Upload the valid CSV file                                    | File is accepted; preview shows all rows without errors                                    | CSV: valid_la_import.csv |
| 3   | Click Import / Confirm                                       | Import completes successfully                                                              |                          |
| 4   | Navigate to affected students' Contact → Course tab          | All LA records from the CSV are displayed in the Require Lesson Allocation table           |                          |
| 5   | Inspect each created LA record                               | Product details, student course id, package course, order remarks are all empty / no value |                          |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – CSV Import – Overlapping Dates Row – Import Fails for That Row

**Description:** AC 01.5 — Negative Testing — Verify that a CSV row with overlapping dates for the same AY + Location + Course triggers an error for that row.

**Preconditions:**

- Logged in as HQ or CM user
- Existing LA: Course "Math", AY 2026, Location A for student S1, Start = 2026-04-01, End = 2026-09-30
- CSV file has 2 rows: Row 1 (valid, different student), Row 2 (student S1, Math, AY 2026, Location A, overlapping dates 2026-05-01 to 2026-08-31)

| #   | Action                                                 | Expected Result                                                 | Test Data |
| --- | ------------------------------------------------------ | --------------------------------------------------------------- | --------- |
| 1   | Upload CSV file with one valid and one overlapping row | File is accepted for parsing                                    |           |
| 2   | Observe validation results                             | Row 2 shows error: overlap error message for the course section |           |
| 3   | Check import result                                    | Row 1 LA is created; Row 2 LA is NOT created                    |           |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – CSV Import – Past End Date Row – Import Fails for That Row

**Description:** AC 01.5 — Negative Testing — Verify that a CSV row where both start and end dates are in the past triggers an end date error for that row.

**Preconditions:**

- Logged in as HQ or CM user
- Today = 2026-03-23
- CSV file has Row 1 (valid) and Row 2 (start = 2026-01-01, end = 2026-03-01; both in past)

| #   | Action                     | Expected Result                                     | Test Data |
| --- | -------------------------- | --------------------------------------------------- | --------- |
| 1   | Upload CSV file            | File accepted                                       |           |
| 2   | Observe validation results | Row 2 shows error: "End date must be a future date" |           |
| 3   | Check import result        | Row 1 LA is created; Row 2 LA is NOT created        |           |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – CSV Import – Start Date After End Date Row – Import Fails for That Row

**Description:** AC 01.5 — Negative Testing — Verify that a CSV row where start_date > end_date triggers a date order error for that row.

**Preconditions:**

- Logged in as HQ or CM user
- CSV file has Row 1 (valid) and Row 2 (start = 2026-09-01, end = 2026-06-30)

| #   | Action                     | Expected Result                                               | Test Data |
| --- | -------------------------- | ------------------------------------------------------------- | --------- |
| 1   | Upload CSV file            | File accepted                                                 |           |
| 2   | Observe validation results | Row 2 shows error: "Start date must be earlier than End date" |           |
| 3   | Check import result        | Row 1 LA is created; Row 2 LA is NOT created                  |           |

**Severity:** major
**Priority:** high
