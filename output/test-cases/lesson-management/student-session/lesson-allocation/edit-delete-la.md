# Test Cases: LT-92532 — [Riso] Edit & Delete Lesson Allocation

## Suite: Edit LA

---

### [Riso] Lesson Allocation – Edit LA – Start Date – Changed to Date After Original – Update Accepted

**Description:** AC 02.1 — BVA just-above boundary — Verify that editing Start date to a value one day after the original is accepted.

**Preconditions:**

- Logged in as HQ or CM user
- Existing LA: Course "Math", AY 2026, Location A, Start = 2026-04-01, End = 2026-09-30, Type = Regular
- LA edit form is open

| #   | Action                                                   | Expected Result                                                      | Test Data             |
| --- | -------------------------------------------------------- | -------------------------------------------------------------------- | --------------------- |
| 1   | Open edit form for the LA                                | Edit form shows current values: Start = 2026-04-01, End = 2026-09-30 |                       |
| 2   | Change Start date to 2026-04-02 (one day after original) | Start date field shows 2026-04-02; no validation error               | New Start: 2026-04-02 |
| 3   | Click Save                                               | Update is accepted; LA record shows Start = 2026-04-02               |                       |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Edit LA – Start Date – Changed to Same as Original – Blocked

**Description:** AC 02.1 — BVA at boundary — Verify that editing Start date to the same value as the original date is NOT accepted (must be after original).

**Preconditions:**

- Logged in as HQ or CM user
- Existing LA: Start = 2026-04-01, End = 2026-09-30
- LA edit form is open

| #   | Action                                         | Expected Result                                                   | Test Data             |
| --- | ---------------------------------------------- | ----------------------------------------------------------------- | --------------------- |
| 1   | Open edit form                                 | Current Start = 2026-04-01                                        |                       |
| 2   | Set Start date = 2026-04-01 (same as original) | Validation error indicating date must be after the original value | New Start: 2026-04-01 |
| 3   | Confirm Save is blocked                        | Save button is disabled or error persists                         |                       |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Edit LA – Start Date – Changed to Date Before Original – Blocked

**Description:** AC 02.1 — BVA below boundary / Negative Testing — Verify that editing Start date to a value before the original date is rejected.

**Preconditions:**

- Logged in as HQ or CM user
- Existing LA: Start = 2026-04-01, End = 2026-09-30
- LA edit form is open

| #   | Action                                                | Expected Result                                                   | Test Data             |
| --- | ----------------------------------------------------- | ----------------------------------------------------------------- | --------------------- |
| 1   | Open edit form                                        | Current Start = 2026-04-01                                        |                       |
| 2   | Set Start date = 2026-03-31 (one day before original) | Validation error indicating date must be after the original value | New Start: 2026-03-31 |
| 3   | Confirm Save is blocked                               | Save button is disabled or error persists                         |                       |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Edit LA – End Date – Changed to Date After Original – Update Accepted

**Description:** AC 02.1 — BVA just-above boundary — Verify that editing End date to a value one day after the original is accepted.

**Preconditions:**

- Logged in as HQ or CM user
- Existing LA: Start = 2026-04-01, End = 2026-09-30, Type = Regular
- LA edit form is open

| #   | Action                                             | Expected Result                                      | Test Data           |
| --- | -------------------------------------------------- | ---------------------------------------------------- | ------------------- |
| 1   | Open edit form                                     | Current End = 2026-09-30                             |                     |
| 2   | Set End date = 2026-10-01 (one day after original) | End date field shows 2026-10-01; no validation error | New End: 2026-10-01 |
| 3   | Click Save                                         | Update accepted; LA shows End = 2026-10-01           |                     |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Edit LA – End Date – Changed to Date Before Original – Blocked

**Description:** AC 02.1 — BVA below boundary / Negative Testing — Verify that editing End date to a value before the original date is rejected.

**Preconditions:**

- Logged in as HQ or CM user
- Existing LA: Start = 2026-04-01, End = 2026-09-30
- LA edit form is open

| #   | Action                                              | Expected Result                                                       | Test Data           |
| --- | --------------------------------------------------- | --------------------------------------------------------------------- | ------------------- |
| 1   | Open edit form                                      | Current End = 2026-09-30                                              |                     |
| 2   | Set End date = 2026-09-29 (one day before original) | Validation error indicating end date must be after the original value | New End: 2026-09-29 |
| 3   | Confirm Save is blocked                             | Save button is disabled or error persists                             |                     |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Edit LA – Edited Dates Cause Overlap – Error Shown

**Description:** AC 02.1 / AC 01.4 — Negative Testing — Verify that editing dates to create an overlap with another existing LA of the same course triggers the overlap error.

**Preconditions:**

- Logged in as HQ or CM user
- Existing LA 1: Math, AY 2026, Location A, Start = 2026-04-01, End = 2026-06-30
- Existing LA 2 (being edited): Math, AY 2026, Location A, Start = 2026-07-01, End = 2026-09-30

| #   | Action                                                      | Expected Result                                                                                                                                                                     | Test Data             |
| --- | ----------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| 1   | Open edit form for LA 2                                     | Current Start = 2026-07-01                                                                                                                                                          |                       |
| 2   | Change Start date to 2026-06-01 (earlier, overlapping LA 1) | Overlap validation error appears: "The selected course has a duration that overlaps with another instance of the same course created earlier. Please adjust the start or end date." | New Start: 2026-06-01 |
| 3   | Confirm Save is blocked                                     | Save fails                                                                                                                                                                          |                       |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Edit LA – Trial Type – Purchased Slot Increased – Update Accepted

**Description:** AC 02.1 — BVA/Decision Table — Verify that for Trial LA type, Purchased Slot can be edited to a value greater than the original.

**Preconditions:**

- Logged in as HQ or CM user
- Existing LA: Type = Trial, Purchased Slot = 5, Start = 2026-04-01, End = 2026-09-30
- LA edit form is open

| #   | Action                                              | Expected Result                                     | Test Data   |
| --- | --------------------------------------------------- | --------------------------------------------------- | ----------- |
| 1   | Open edit form for Trial LA                         | Purchased Slot field is editable; current value = 5 |             |
| 2   | Change Purchased Slot to 6 (one more than original) | No validation error                                 | New Slot: 6 |
| 3   | Click Save                                          | Update accepted; LA shows Purchased Slot = 6        |             |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Edit LA – Trial Type – Purchased Slot Set to Same Value – Blocked

**Description:** AC 02.1 — BVA at boundary — Verify that setting Purchased Slot to the same value as original (not greater) is rejected.

**Preconditions:**

- Logged in as HQ or CM user
- Existing Trial LA: Purchased Slot = 5
- LA edit form is open

| #   | Action                                    | Expected Result                                                | Test Data   |
| --- | ----------------------------------------- | -------------------------------------------------------------- | ----------- |
| 1   | Open edit form                            | Purchased Slot = 5                                             |             |
| 2   | Set Purchased Slot = 5 (same as original) | Validation error indicating slot must be greater than original | New Slot: 5 |
| 3   | Confirm Save is blocked                   | Save is blocked                                                |             |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Edit LA – Trial Type – Purchased Slot Decreased – Blocked

**Description:** AC 02.1 — Negative Testing — Verify that decreasing Purchased Slot below the original value for a Trial LA is rejected.

**Preconditions:**

- Logged in as HQ or CM user
- Existing Trial LA: Purchased Slot = 5
- LA edit form is open

| #   | Action                                      | Expected Result                                                | Test Data   |
| --- | ------------------------------------------- | -------------------------------------------------------------- | ----------- |
| 1   | Open edit form                              | Purchased Slot = 5                                             |             |
| 2   | Set Purchased Slot = 4 (less than original) | Validation error indicating slot must be greater than original | New Slot: 4 |
| 3   | Confirm Save is blocked                     | Save is blocked                                                |             |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Edit LA – Regular Type – Purchased Slot Field Not Editable

**Description:** AC 02.1 — Decision Table — Verify that Purchased Slot field is NOT editable for Regular LA type.

**Preconditions:**

- Logged in as HQ or CM user
- Existing LA: Type = Regular, Purchased Slot = 10
- LA edit form is open

| #   | Action                        | Expected Result                                             | Test Data |
| --- | ----------------------------- | ----------------------------------------------------------- | --------- |
| 1   | Open edit form for Regular LA | Edit form is displayed                                      |           |
| 2   | Observe Purchased Slot field  | Purchased Slot field is read-only / disabled (not editable) |           |

**Severity:** normal
**Priority:** medium

---

### [Riso] Lesson Allocation – Edit LA – Seasonal Type – Purchased Slot Field Not Editable

**Description:** AC 02.1 — Decision Table — Verify that Purchased Slot field is NOT editable for Seasonal LA type.

**Preconditions:**

- Logged in as HQ or CM user
- Existing LA: Type = Seasonal, Purchased Slot = 8
- LA edit form is open

| #   | Action                         | Expected Result                                             | Test Data |
| --- | ------------------------------ | ----------------------------------------------------------- | --------- |
| 1   | Open edit form for Seasonal LA | Edit form is displayed                                      |           |
| 2   | Observe Purchased Slot field   | Purchased Slot field is read-only / disabled (not editable) |           |

**Severity:** normal
**Priority:** medium

---

## Suite: Delete LA

---

### [Riso] Lesson Allocation – Delete LA – Start Date in Future – Delete Button Enabled and Confirmation Shown

**Description:** AC 02.2 — Decision Table — Verify delete button is enabled and confirmation dialog appears when LA start date is in the future.

**Preconditions:**

- Logged in as HQ or CM user
- Existing LA: Start = 2026-04-01 (future relative to today 2026-03-23), End = 2026-09-30
- On Student → Contact → Course tab

| #   | Action                                   | Expected Result                                                                                                                                                                           | Test Data |
| --- | ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | Locate the LA row with future start date | Delete button is visible and enabled                                                                                                                                                      |           |
| 2   | Click Delete button                      | Confirmation dialog appears: "All allocated lesson (if any) in this course will also be removed. This action cannot be reverted. Are you sure you want to delete this Lesson Allocation?" |           |
| 3   | Observe dialog buttons                   | "Confirm" and "Cancel" buttons are both present                                                                                                                                           |           |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Delete LA – Start Date in Past – Delete Button Disabled

**Description:** AC 02.2 — Decision Table — Verify delete button is disabled when LA start date is in the past (≤ today).

**Preconditions:**

- Logged in as HQ or CM user
- Existing LA: Start = 2026-03-01 (past), End = 2026-09-30
- On Student → Contact → Course tab

| #   | Action                                      | Expected Result                                    | Test Data |
| --- | ------------------------------------------- | -------------------------------------------------- | --------- |
| 1   | Locate the LA row with past start date      | Delete button is present but disabled / greyed out |           |
| 2   | Attempt to click the disabled Delete button | No action triggered; button remains disabled       |           |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Delete LA – Start Date = Today – Delete Button Disabled

**Description:** AC 02.2 — BVA at boundary — Verify delete button is disabled exactly when LA start date = today.

**Preconditions:**

- Logged in as HQ or CM user
- Today = 2026-03-23
- Existing LA: Start = 2026-03-23 (today), End = 2026-09-30

| #   | Action                                    | Expected Result           | Test Data         |
| --- | ----------------------------------------- | ------------------------- | ----------------- |
| 1   | Locate the LA row with start date = today | Delete button is disabled | Start: 2026-03-23 |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Allocation – Delete LA – Confirm Delete – LA Deleted and Allocated Lessons Unlinked

**Description:** AC 02.2 — CRUD Testing / Data Integrity — Verify that confirming delete removes the LA and unlinks all its allocated lessons.

**Preconditions:**

- Logged in as HQ or CM user
- Existing LA: Start = 2026-04-01 (future), with 2 lessons allocated to it
- Delete confirmation dialog is open

| #   | Action                                                         | Expected Result                                                      | Test Data |
| --- | -------------------------------------------------------------- | -------------------------------------------------------------------- | --------- |
| 1   | Click "Confirm" in the delete confirmation dialog              | Dialog closes                                                        |           |
| 2   | Observe the LA table                                           | The deleted LA row is no longer present                              |           |
| 3   | Navigate to Lesson list for the 2 previously allocated lessons | Both lessons no longer reference the deleted LA (LA link is removed) |           |
| 4   | Confirm no orphaned references                                 | No error or broken link exists for those lessons                     |           |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Allocation – Delete LA – Cancel Delete – Nothing Changes

**Description:** AC 02.2 — State Transition Testing — Verify that cancelling the delete confirmation dialog leaves the LA and its lessons unchanged.

**Preconditions:**

- Logged in as HQ or CM user
- Existing LA with future start date and allocated lessons
- Delete confirmation dialog is open

| #   | Action                                           | Expected Result                                       | Test Data |
| --- | ------------------------------------------------ | ----------------------------------------------------- | --------- |
| 1   | Click "Cancel" in the delete confirmation dialog | Dialog closes                                         |           |
| 2   | Observe the LA table                             | The LA row still exists with all original data        |           |
| 3   | Observe allocated lessons                        | All lessons remain linked to the LA                   |           |
| 4   | Observe page state                               | User is on Student → Contact → Course tab (unchanged) |           |

**Severity:** normal
**Priority:** medium
