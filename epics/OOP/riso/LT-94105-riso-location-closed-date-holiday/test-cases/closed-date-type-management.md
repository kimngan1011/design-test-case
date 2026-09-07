# Test Cases: LT-94105 — Riso Location Closed Date and Holiday

## Suite: Closed Date Type Management

### [Riso] Closed Date – Type field – New record – Closed Date default is shown

**Description:** AC 01.1 — Equivalence Partitioning — Confirms the New Closed Date form exposes the complete Type choice and defaults it deterministically.

**Preconditions:**
- Logged in as HQ Staff with Closed Date create and edit access for Riso Center A.
- Academic Year `2026`; ACI `Riso Center A 2026`; target_date = `2026-07-20`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the New Closed Date form for Riso Center A. | The form opens for ACI `Riso Center A 2026`. | target_date = 2026-07-20 |
| 2 | Open the Type list. | The list contains exactly `Closed Date` and `Holiday`; the Japanese label for Holiday is `祝日`. | allowed values = Closed Date, Holiday / 祝日 |
| 3 | Read the initial Type value. | Type shows `Closed Date`. | expected default = Closed Date |

**Severity:** major
**Priority:** high

---

### [Riso] Closed Date – Type field – Unsupported value – Save is blocked

**Description:** AC 01.1 — Negative — Confirms a Type outside the defined picklist cannot be stored.

**Preconditions:**
- Logged in as HQ Staff with Closed Date create and edit access for Riso Center A.
- Academic Year `2026`; ACI `Riso Center A 2026`; target_date = `2026-07-21`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the New Closed Date form. | The form opens with Type set to `Closed Date`. | target_date = 2026-07-21 |
| 2 | Attempt to set Type to `National Holiday` by using an unsupported submitted value. | The save is rejected and the record is not created. | unsupported Type = National Holiday |
| 3 | Reopen the ACI Closed Dates list. | No Closed Date for `2026-07-21` appears. | expected record count for date = 0 |

**Severity:** major
**Priority:** high

---

### [Riso] Closed Date – Type field – Holiday selected at creation – Value persists in the target ACI

**Description:** AC 01.1 / AC 01.2 — CRUD — Confirms Holiday is saved without changing the location or academic-year scope.

**Preconditions:**
- Logged in as HQ Staff with Closed Date create and edit access for Riso Center A.
- ACI `Riso Center A 2026` exists; target_date = `2026-07-22`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Create a Closed Date in Riso Center A and select `Holiday`. | The record saves with Date `2026-07-22` and Type `Holiday`. | target_date = 2026-07-22; Type = Holiday |
| 2 | Reopen the saved record. | Type remains `Holiday` and the record belongs to `Riso Center A 2026`. | ACI = Riso Center A 2026 |
| 3 | Open Riso Center B's 2026 ACI. | No record for `2026-07-22` is added to Center B. | control ACI = Riso Center B 2026 |
| 4 | Refresh the Learner Calendar for a student enrolled at Riso Center A and open `2026-07-22`. | The date is rendered as Holiday and its day detail contains `祝日`. | expected color = #295ACB; expected label = 祝日 |

**Severity:** major
**Priority:** high

---

### [Riso] Closed Date – Type editing – Closed Date changed to Holiday – Saved value is retained

**Description:** AC 01.2 — State Transition — Confirms an existing record can move from Closed Date to Holiday.

**Preconditions:**
- Logged in as HQ Staff with Closed Date create and edit access for Riso Center A.
- ACI `Riso Center A 2026` contains `2026-07-23` with Type `Closed Date`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the `2026-07-23` Closed Date record. | The record shows Type `Closed Date`. | original Type = Closed Date |
| 2 | Change Type to `Holiday` and save. | The record saves without creating a second record for the same date. | new Type = Holiday |
| 3 | Reopen the record. | Type shows `Holiday` for `2026-07-23`. | expected Type = Holiday |

**Severity:** major
**Priority:** high

---

### [Riso] Closed Date – Type editing – Holiday changed to Closed Date – Saved value is retained

**Description:** AC 01.2 — State Transition — Confirms the reverse Type transition is available and deterministic.

**Preconditions:**
- Logged in as HQ Staff with Closed Date create and edit access for Riso Center A.
- ACI `Riso Center A 2026` contains `2026-07-24` with Type `Holiday`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the `2026-07-24` Closed Date record. | The record shows Type `Holiday`. | original Type = Holiday |
| 2 | Change Type to `Closed Date` and save. | The record saves without altering Date or ACI. | new Type = Closed Date |
| 3 | Reopen the record. | Type shows `Closed Date` for `2026-07-24`. | expected Type = Closed Date |

**Severity:** major
**Priority:** high

---

### [Riso] Closed Date – Centre Manager – Link existing date to own ACI – Link is allowed

**Description:** AC 01.2 — Permission Matrix — Confirms a Centre Manager can link an existing Closed Date to their assigned Riso location's ACI, without creating or editing the Closed Date.

**Preconditions:**
- Logged in as CM Staff for Riso Center A only.
- An existing Closed Date `2026-07-25` was created by HQ and is not yet linked to ACI `Riso Center A 2026`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open ACI `Riso Center A 2026` and choose the action to link an existing Closed Date. | The existing Closed Date selection is available; Closed Date creation and Type editing controls are unavailable. | actor scope = Center A |
| 2 | Select the existing `2026-07-25` Closed Date and save the ACI link. | The Closed Date is linked to Riso Center A's ACI without creating a new Closed Date record. | target_date = 2026-07-25 |
| 3 | Reopen ACI `Riso Center A 2026`. | The linked date is displayed with its existing Type and no editable Type control. | expected link = 2026-07-25 |

**Severity:** major
**Priority:** high

---

### [Riso] Closed Date – Centre Manager – View all dates, create and edit are blocked

**Description:** AC 01.2 — Permission Matrix / Negative — Confirms a Centre Manager can view all Closed Dates but cannot create or edit any Closed Date.

**Preconditions:**
- Logged in as CM Staff for Riso Center A only.
- Existing Closed Dates include Riso Center A and Riso Center B; Riso Center B has `2026-07-26` with Type `Closed Date`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the all Closed Dates list and open Riso Center B's `2026-07-26` record. | The record and its Type are visible to the Centre Manager. | actor scope = Center A; record ACI = Center B |
| 2 | Attempt to change Type to `Holiday` and save. | Editing is unavailable or rejected, and the record remains `Closed Date`. | attempted Type = Holiday |
| 3 | Attempt to create a new Closed Date from the list or by a direct create route. | The create action is unavailable or rejected and no new Closed Date is created. | target_date = 2026-07-27 |

**Severity:** major
**Priority:** high

---

### [Riso] Closed Date – Type access – Denied role – Create and edit actions are unavailable

**Description:** AC 01.2 — Permission Matrix / Negative — Confirms a role without Closed Date rights cannot use Type actions.

**Preconditions:**
- Logged in as a Riso teacher account without Academic Calendar edit access.
- Riso Center A ACI contains `2026-07-27` with Type `Closed Date`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Riso Center A's Closed Dates area. | New Closed Date and edit actions are unavailable. | actor = Riso teacher |
| 2 | Attempt to open the existing record for editing. | The record cannot be edited. | target_date = 2026-07-27 |
| 3 | Read the existing record. | Type remains `Closed Date`. | expected Type = Closed Date |

**Severity:** major
**Priority:** high

---

### [Riso] Closed Date – Creation retry – Repeated save – One record remains

**Description:** AC 01.1 / AC 01.2 — Negative — Confirms repeated submission does not create duplicate Closed Date records.

**Preconditions:**
- Logged in as HQ Staff with Closed Date create and edit access for Riso Center A.
- ACI `Riso Center A 2026` has no record for `2026-07-28`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Enter a new Closed Date with Type `Holiday`. | The form contains Date `2026-07-28` and Type `Holiday`. | target_date = 2026-07-28 |
| 2 | Submit Save twice before the page reloads. | The form reports one completed save or one duplicate prevention response. | submissions = 2 |
| 3 | Open the ACI Closed Dates list. | Exactly one `2026-07-28` record exists and its Type is `Holiday`. | expected record count = 1 |

**Severity:** major
**Priority:** high
