# Test Cases: LT-92532 — [Riso] Lesson Allocation – Auto-Calculation

> ⚠️ **Note:** US05 is to be implemented together with PBT-1812. Execute these test cases only after PBT-1812 is confirmed in scope and deployed.

---

## Suite: LA – Total Session Count Auto-Calculation

---

### [Riso] Lesson Allocation – Total Session Count – New Contracts Linked – Equals Sum of Active Contract Totals

**Description:** Ac 05.1 — CRUD Testing — LA.Total Session Count equals the sum of Contract.Total for all active contracts linked to the LA (spec scenario: New).

**Preconditions:**

- Logged in as HQ or CM user
- LA 1 exists for student (duration Jan 1–Jun 30)
- Contract 1 (slot=2, type=one-time, total=2, Status=Active) is linked to LA 1
- Contract 2 (slot=4, type=monthly, total=20, Status=Active) is linked to LA 1
- Expected LA 1 Total Session Count = 22

| #   | Action                                     | Expected Result                                                                          | Test Data                                                         |
| --- | ------------------------------------------ | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| 1   | Navigate to Student → Contact → Course tab | Lesson Allocation table is displayed                                                     |                                                                   |
| 2   | Locate LA 1 record in the table            | LA row is found                                                                          |                                                                   |
| 3   | Observe Total Session Count value          | Total Session Count = 22 (Contract 1 total=2 + Contract 2 total=20)                     | Contract 1: slot=2, one-time, total=2; Contract 2: slot=4, monthly, total=20 |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Total Session Count – Contract Cancelled – Excluded from Total Session Count

**Description:** Ac 05.1 — CRUD Testing — When a linked contract is cancelled, LA.Total Session Count is recalculated to exclude the cancelled contract's total.

**Preconditions:**

- Logged in as HQ or CM user
- LA linked to Contract 1 (total=5, Status=Active) and Contract 2 (total=5, Status=Active)
- Current LA Total Session Count = 10

| #   | Action                                  | Expected Result                                                                         | Test Data             |
| --- | --------------------------------------- | --------------------------------------------------------------------------------------- | --------------------- |
| 1   | Cancel Contract 2                       | Contract 2 status = Cancelled                                                           | Contract 2: Cancelled |
| 2   | Navigate to the LA record               | LA Purchased Slot has been recalculated                                                 |                       |
| 3   | Observe Total Session Count value       | Total Session Count = 5 (only Contract 1 active; Contract 2 excluded as Cancelled)      |                       |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Total Session Count – Contract Voided – Excluded from Total Session Count

**Description:** Ac 05.1 — CRUD Testing — When a linked contract is voided, LA.Total Session Count is recalculated to exclude the voided contract's total.

**Preconditions:**

- Logged in as HQ or CM user
- LA linked to Contract 1 (total=5, Status=Active) and Contract 2 (total=5, Status=Active)
- Current LA Total Session Count = 10

| #   | Action                              | Expected Result                                                               | Test Data          |
| --- | ----------------------------------- | ----------------------------------------------------------------------------- | ------------------ |
| 1   | Void Contract 2                     | Contract 2 status = Voided                                                    | Contract 2: Voided |
| 2   | Observe Total Session Count value   | Total Session Count = 5 (Contract 2 excluded as Voided)                       |                    |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Total Session Count – Contract Soft-Deleted – Excluded from Total Session Count

**Description:** Ac 05.1 — CRUD Testing — When a linked contract is soft-deleted (status set to Deleted), LA.Total Session Count is recalculated to exclude it (spec scenario: Soft Delete).

**Preconditions:**

- Logged in as HQ or CM user
- LA 1 (Total Session Count = 22; duration Jan 1–Jun 30)
- Contract 1 (slot=2, one-time, total=2, Status=Active) linked to LA 1
- Contract 2 (slot=4, monthly, total=20, Status=Active) linked to LA 1

| #   | Action                                       | Expected Result                                                                         | Test Data                       |
| --- | -------------------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------- |
| 1   | Set Contract 2 status to Deleted (soft-delete) | Contract 2 status = Deleted                                                           | Contract 2: Status → Deleted    |
| 2   | Navigate to LA 1 record                      | LA table is shown                                                                       |                                 |
| 3   | Observe Total Session Count value            | Total Session Count = 2 (only Contract 1 total=2 counted; Contract 2 excluded)          |                                 |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Total Session Count – New Active Contract Added – Recalculated to Include New Contract Total

**Description:** Ac 05.1 — CRUD Testing — When a new active contract is linked to the LA, LA.Total Session Count is recalculated to include the new contract's total (spec scenario: Another New).

**Preconditions:**

- Logged in as HQ or CM user
- LA 1 (Total Session Count = 2; duration Jan 1–Jun 30)
- Contract 1 (slot=2, one-time, total=2, Status=Active) linked to LA 1
- Contract 2 (slot=4, monthly, total=20, Status=Deleted) linked to LA 1

| #   | Action                                                                              | Expected Result                                                                | Test Data                                  |
| --- | ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------------------------------ |
| 1   | Create Contract 3 (slot=3, type=monthly, total=9, Apr 1–Jun 30) linked to LA 1     | Contract 3 is created with Status=Active                                       | Contract 3: slot=3, monthly, total=9       |
| 2   | Navigate to LA 1 record                                                             | LA table is shown                                                              |                                            |
| 3   | Observe Total Session Count value                                                   | Total Session Count = 11 (Contract 1 total=2 + Contract 3 total=9)             |                                            |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Total Session Count – Active Contract Total Updated – Recalculated on Change

**Description:** Ac 05.1 — CRUD Testing — When an active linked contract's total is updated, LA.Total Session Count is recalculated to reflect the new total (spec scenario: Update).

**Preconditions:**

- Logged in as HQ or CM user
- LA 1 (Total Session Count = 11; duration Jan 1–Jun 30)
- Contract 1 (slot=2, one-time, total=2, Status=Active) linked to LA 1
- Contract 2 (slot=4, monthly, total=20, Status=Deleted) linked to LA 1
- Contract 3 (slot=3, monthly, total=9, Status=Active, Apr 1–Jun 30) linked to LA 1

| #   | Action                                                                          | Expected Result                                                              | Test Data                                      |
| --- | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------- |
| 1   | Update Contract 3: change slot from 3 to 1, type from monthly to weekly, total from 9 to 8, end date to May 30 | Contract 3 updated                                       | Contract 3: slot→1, type→weekly, total→8, end→May 30 |
| 2   | Navigate to LA 1 record                                                         | LA table is shown                                                            |                                                |
| 3   | Observe Total Session Count value                                               | Total Session Count = 10 (Contract 1 total=2 + Contract 3 total=8)           |                                                |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Total Session Count – Multiple LAs per Student – Each Calculated from Its Own Linked Contracts Only

**Description:** Ac 05.1 — CRUD Testing — When a student has multiple LAs (different courses), each LA.Total Session Count is calculated only from contracts linked to that specific LA (isolated by lesson_allocation_id); contracts of one LA do not affect another.

**Preconditions:**

- Logged in as HQ or CM user
- Student has LA 1 (Course A) and LA 2 (Course B); both active
- Contract 1 (total=10, Status=Active) is linked to LA 1 only
- Contract 2 (total=8, Status=Active) is linked to LA 2 only

| #   | Action                                             | Expected Result                                                                                          | Test Data                                               |
| --- | -------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| 1   | Navigate to Student → Contact → Course tab         | LA table is displayed showing LA 1 and LA 2                                                              |                                                         |
| 2   | Observe Total Session Count for LA 1               | Total Session Count = 10 (only Contract 1 counted; Contract 2 belongs to LA 2 and is excluded)           | Contract 1: linked to LA 1, total=10; Contract 2: linked to LA 2, total=8 |
| 3   | Observe Total Session Count for LA 2               | Total Session Count = 8 (only Contract 2 counted; Contract 1 belongs to LA 1 and is excluded)            |                                                         |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Total Session Count – Last Active Contract Soft-Deleted – Total Session Count Becomes Zero; Start Date and End Date Retained

**Description:** Ac 05.1 / Ac 05.2 — CRUD Testing — When the last active contract linked to an LA is soft-deleted, Total Session Count becomes 0 but Start Date and End Date retain their last known values (LT-98533 Logical Deletion rule).

**Preconditions:**

- Logged in as HQ or CM user
- LA has exactly 1 active contract: Contract 1 (start=2026-01-01, end=2026-06-30, total=10, Status=Active)
- LA Total Session Count = 10; LA Start Date = 2026-01-01; LA End Date = 2026-06-30

| #   | Action                                                                    | Expected Result                                                                                  | Test Data                    |
| --- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ---------------------------- |
| 1   | Set Contract 1 status to Deleted (the only active contract)               | Contract 1 status = Deleted                                                                      | Contract 1: Status → Deleted |
| 2   | Navigate to the LA record                                                 | LA is displayed                                                                                  |                              |
| 3   | Observe Total Session Count value                                         | Total Session Count = 0 (no remaining active contracts)                                          |                              |
| 4   | Observe Start Date and End Date values                                    | Start Date = 2026-01-01; End Date = 2026-06-30 (retained from last known state; not reset to null) |                            |

**Severity:** major
**Priority:** high

---

## Suite: LA – Start Date / End Date Auto-Calculation

---

### [Riso] Lesson Allocation – Start Date – Active Contracts Present – Set to Earliest Contract Start Date

**Description:** Ac 05.2 — CRUD Testing — LA.Start_Date equals the earliest start date among all active contracts linked to the LA (LT-98533).

**Preconditions:**

- Logged in as HQ or CM user
- LA linked to Contract 1 (start_date=2026-01-01, Status=Active) and Contract 2 (start_date=2026-04-01, Status=Active)
- Expected LA.Start_Date = 2026-01-01

| #   | Action                            | Expected Result                                                              | Test Data                                                        |
| --- | --------------------------------- | ---------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| 1   | Navigate to the LA record         | LA is displayed                                                              |                                                                  |
| 2   | Observe Start Date value          | Start Date = 2026-01-01 (earliest start date among active contracts)         | Contract 1: start=2026-01-01; Contract 2: start=2026-04-01      |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Start Date – Contract with Earliest Start Date Soft-Deleted – Recalculated to Next Earliest

**Description:** Ac 05.2 — CRUD Testing — When the contract with the earliest start date is soft-deleted, LA.Start_Date recalculates to the next earliest start date among remaining active contracts (LT-98533).

**Preconditions:**

- Logged in as HQ or CM user
- LA linked to Contract 1 (start=2026-01-01, Status=Active) and Contract 2 (start=2026-04-01, Status=Active)
- LA.Start_Date = 2026-01-01 (earliest)

| #   | Action                                                   | Expected Result                                                               | Test Data                            |
| --- | -------------------------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------ |
| 1   | Set Contract 1 status to Deleted (the one with start=2026-01-01) | Contract 1 status = Deleted                                       | Contract 1: Status → Deleted         |
| 2   | Navigate to the LA record                                | LA is displayed                                                               |                                      |
| 3   | Observe Start Date value                                 | Start Date = 2026-04-01 (recalculated to Contract 2's start date, now the only active contract) |                         |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – End Date – Active Contracts Present – Set to Latest Contract End Date

**Description:** Ac 05.2 — CRUD Testing — LA.End_Date equals the latest end date among all active contracts linked to the LA.

**Preconditions:**

- Logged in as HQ or CM user
- LA linked to Contract 1 (end_date=2026-06-30, Status=Active) and Contract 2 (end_date=2026-09-30, Status=Active)
- Expected LA.End_Date = 2026-09-30

| #   | Action                            | Expected Result                                                              | Test Data |
| --- | --------------------------------- | ---------------------------------------------------------------------------- | --------- |
| 1   | Navigate to the LA record         | LA is displayed                                                              |           |
| 2   | Observe End Date value            | End Date = 2026-09-30 (latest end date among active contracts)               |           |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – End Date – Contract with Latest End Date Deleted – LA End Date Recalculates to Past Date

**Description:** Ac 05.2 — CRUD Testing — When the contract with the latest (future) end date is soft-deleted and all remaining active contracts have past end dates, LA.End_Date auto-recalculates to a past date with no validation error (auto-calculated dates bypass the manual-entry future-date restriction).

**Preconditions:**

- Logged in as HQ or CM user
- Today = 2026-06-22
- LA linked to Contract 1 (end=2025-03-31, Status=Active) and Contract 2 (end=2026-09-30, Status=Active)
- LA.End_Date = 2026-09-30 (latest, currently future)

| #   | Action                                                              | Expected Result                                                                                         | Test Data                    |
| --- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | ---------------------------- |
| 1   | Set Contract 2 status to Deleted (the one with end=2026-09-30)      | Contract 2 status = Deleted                                                                             | Contract 2: Status → Deleted |
| 2   | Navigate to the LA record                                           | LA is displayed                                                                                         |                              |
| 3   | Observe End Date value                                              | End Date = 2025-03-31 (recalculated to Contract 1's end date; past date accepted)                       |                              |
| 4   | Verify no validation error is shown for the past End Date           | No error message displayed — auto-recalculated past dates bypass the manual future-date restriction     |                              |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – End Date – Active Contract End Date Updated to Past – LA End Date Recalculates to Past Date

**Description:** Ac 05.2 — CRUD Testing — When the only active contract's end date is updated to a past date, LA.End_Date auto-recalculates to that past date with no validation error.

**Preconditions:**

- Logged in as HQ or CM user
- Today = 2026-06-22
- LA linked to Contract 1 only (end=2026-09-30, Status=Active)
- LA.End_Date = 2026-09-30

| #   | Action                                                                      | Expected Result                                                                                   | Test Data                              |
| --- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | -------------------------------------- |
| 1   | Update Contract 1: change end date from 2026-09-30 to 2025-03-31           | Contract 1 updated with end=2025-03-31                                                            | Contract 1: end → 2025-03-31           |
| 2   | Navigate to the LA record                                                   | LA is displayed                                                                                   |                                        |
| 3   | Observe End Date value                                                      | End Date = 2025-03-31 (recalculated to updated contract end date; past date accepted)             |                                        |
| 4   | Verify no validation error is shown for the past End Date                   | No error message displayed — auto-recalculated past dates bypass the manual future-date restriction |                                      |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – End Date – Contract with Latest End Date Cancelled – Recalculated to Next Latest

**Description:** Ac 05.2 — CRUD Testing — When the contract with the latest end date is cancelled, LA.End_Date recalculates to the next latest end date among remaining active contracts.

**Preconditions:**

- Logged in as HQ or CM user
- LA linked to Contract 1 (end=2026-06-30, Status=Active) and Contract 2 (end=2026-09-30, Status=Active)
- LA.End_Date = 2026-09-30

| #   | Action                                                       | Expected Result                                                               | Test Data |
| --- | ------------------------------------------------------------ | ----------------------------------------------------------------------------- | --------- |
| 1   | Cancel Contract 2 (the one with end=2026-09-30)              | Contract 2 status = Cancelled                                                 |           |
| 2   | Navigate to the LA record                                    | LA is displayed                                                               |           |
| 3   | Observe End Date value                                       | End Date = 2026-06-30 (recalculated to Contract 1's end date)                 |           |

**Severity:** major
**Priority:** high
