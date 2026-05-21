# Test Cases: LT-92532 — [Riso] Lesson Allocation – Auto-Calculation

> ⚠️ **Note:** US03 is to be implemented together with PBT-1812. Execute these test cases only after PBT-1812 is confirmed in scope and deployed.
> AC 03.2 (End Date auto-calculation) is TBC — test cases are drafted but marked as deferred.

---

## Suite: LA – Purchased Slot Auto-Calculation

---

### [Riso] Lesson Allocation – Purchased Slot – Initial Calculation – Equals Sum of Active Contract Slots

**Description:** AC 03.1 — CRUD Testing — Verify that LA.Purchased_Slot correctly equals the sum of all active (non-cancelled, non-voided, non-deleted) contract slots linked to the LA.

**Preconditions:**

- Logged in as HQ or CM user
- LA exists for student; linked to Contract 1 (slot = 5) and Contract 2 (slot = 5); both contracts are active
- Expected LA.Purchased_Slot = 10

| #   | Action                                     | Expected Result                      | Test Data                              |
| --- | ------------------------------------------ | ------------------------------------ | -------------------------------------- |
| 1   | Navigate to Student → Contact → Course tab | Lesson Allocation table is displayed |                                        |
| 2   | Locate the LA record in the table          | LA row is found                      |                                        |
| 3   | Observe Purchased Slot value               | Purchased Slot = 10 (5 + 5)          | Contract 1: slot=5, Contract 2: slot=5 |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Purchased Slot – Contract Cancelled – Slot Decremented

**Description:** AC 03.1 — CRUD Testing — Verify that when a linked contract is cancelled, LA.Purchased_Slot is recalculated to exclude the cancelled contract's slots.

**Preconditions:**

- LA linked to Contract 1 (slot = 5, active) and Contract 2 (slot = 5, active)
- Current LA.Purchased_Slot = 10

| #   | Action                       | Expected Result                                                                | Test Data             |
| --- | ---------------------------- | ------------------------------------------------------------------------------ | --------------------- |
| 1   | Cancel Contract 2            | Contract 2 status = Cancelled                                                  | Contract 2: Cancelled |
| 2   | Navigate to the LA record    | LA Purchased Slot has been recalculated                                        |                       |
| 3   | Observe Purchased Slot value | Purchased Slot = 5 (only Contract 1 counted; Contract 2 excluded as Cancelled) |                       |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Purchased Slot – Contract Voided – Slot Decremented

**Description:** AC 03.1 — CRUD Testing — Verify that when a linked contract is voided, LA.Purchased_Slot is recalculated to exclude the voided contract's slots.

**Preconditions:**

- LA linked to Contract 1 (slot = 5, active) and Contract 2 (slot = 5, active)
- Current LA.Purchased_Slot = 10

| #   | Action                    | Expected Result                                    | Test Data          |
| --- | ------------------------- | -------------------------------------------------- | ------------------ |
| 1   | Void Contract 2           | Contract 2 status = Voided                         | Contract 2: Voided |
| 2   | Observe LA Purchased Slot | Purchased Slot = 5 (Contract 2 excluded as Voided) |                    |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Purchased Slot – Contract Deleted (delete_flag = on) – Slot Decremented

**Description:** AC 03.1 — CRUD Testing — Verify that when a linked contract has delete_flag = on, it is excluded from LA.Purchased_Slot.

**Preconditions:**

- LA linked to Contract 1 (slot = 5, active) and Contract 2 (slot = 5, delete_flag = on)
- Expected LA.Purchased_Slot = 5 (Contract 2 excluded)

| #   | Action                       | Expected Result                                                   | Test Data                  |
| --- | ---------------------------- | ----------------------------------------------------------------- | -------------------------- |
| 1   | Navigate to the LA record    | LA table is shown                                                 |                            |
| 2   | Observe Purchased Slot value | Purchased Slot = 5 (Contract 2 with delete_flag = on is excluded) | Contract 2: delete_flag=on |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Purchased Slot – New Contract Added – Slot Incremented

**Description:** AC 03.1 — CRUD Testing — Verify that when a new contract is created and linked to the LA, LA.Purchased_Slot is recalculated to include the new contract's slots.

**Preconditions:**

- LA linked to Contract 1 (slot = 5, active) only; LA.Purchased_Slot = 5

| #   | Action                                              | Expected Result                                              | Test Data           |
| --- | --------------------------------------------------- | ------------------------------------------------------------ | ------------------- |
| 1   | Create Contract 3 (slot = 12) linked to the same LA | Contract 3 is created                                        | Contract 3: slot=12 |
| 2   | Navigate to the LA record                           | LA table is shown                                            |                     |
| 3   | Observe Purchased Slot value                        | Purchased Slot = 17 (5 from Contract 1 + 12 from Contract 3) |                     |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Purchased Slot – Existing Contract Updated – Slot Recalculated

**Description:** AC 03.1 — CRUD Testing — Verify that updating an existing linked contract's slot value triggers a recalculation of LA.Purchased_Slot.

**Preconditions:**

- LA linked to Contract 1 (slot = 5) and Contract 2 (slot = 5); LA.Purchased_Slot = 10

| #   | Action                             | Expected Result                                             | Test Data                     |
| --- | ---------------------------------- | ----------------------------------------------------------- | ----------------------------- |
| 1   | Update Contract 1 slot from 5 to 8 | Contract 1 updated                                          | Contract 1: slot updated to 8 |
| 2   | Navigate to the LA record          | LA table is shown                                           |                               |
| 3   | Observe Purchased Slot value       | Purchased Slot = 13 (8 from Contract 1 + 5 from Contract 2) |                               |

**Severity:** major
**Priority:** high

---

## Suite: LA – End Date Auto-Calculation (TBC — Deferred)

> ⏸ The following test cases are drafted based on the TBC spec in AC 03.2. Do NOT execute until AC 03.2 is officially confirmed.

---

### [Riso] Lesson Allocation – End Date – Active Contracts – Set to Latest Contract End Date

**Description:** AC 03.2 (TBC) — CRUD Testing — Verify LA.End_Date equals the latest end date among all active contracts linked to the LA.

**Preconditions:**

- LA linked to Contract 1 (end_date = 2026-06-30, active) and Contract 2 (end_date = 2026-09-30, active)
- Expected LA.End_Date = 2026-09-30

| #   | Action                    | Expected Result                                                | Test Data |
| --- | ------------------------- | -------------------------------------------------------------- | --------- |
| 1   | Navigate to the LA record | LA is displayed                                                |           |
| 2   | Observe End Date value    | End Date = 2026-09-30 (latest end date among active contracts) |           |

**Severity:** normal
**Priority:** medium

---

### [Riso] Lesson Allocation – End Date – Contract with Latest Date Is Cancelled – End Date Recalculated

**Description:** AC 03.2 (TBC) — CRUD Testing — Verify that when the contract with the latest end date is cancelled, LA.End_Date recalculates to the next latest end date among remaining active contracts.

**Preconditions:**

- LA linked to Contract 1 (end = 2026-06-30, active) and Contract 2 (end = 2026-09-30, active)
- LA.End_Date = 2026-09-30

| #   | Action                                            | Expected Result                                               | Test Data |
| --- | ------------------------------------------------- | ------------------------------------------------------------- | --------- |
| 1   | Cancel Contract 2 (the one with end = 2026-09-30) | Contract 2 status = Cancelled                                 |           |
| 2   | Navigate to the LA record                         | LA is displayed                                               |           |
| 3   | Observe End Date value                            | End Date = 2026-06-30 (recalculated to Contract 1's end date) |           |

**Severity:** normal
**Priority:** medium
