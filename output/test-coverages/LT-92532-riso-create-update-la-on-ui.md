# Test Coverage: LT-92532 — Riso | Create/Update LA on UI

**Jira:** https://manabie.atlassian.net/browse/LT-92532
**Qase:** https://app.qase.io/project/PX?suite=18
**Date:** 2026-03-23

---

## 1. Business Rules Extracted

| #   | AC      | Business Rule                                                                                                          |
| --- | ------- | ---------------------------------------------------------------------------------------------------------------------- |
| 1   | AC 01.1 | "New Lesson Allocation" button appears under Require Lesson Allocation table in Contact → Course tab                   |
| 2   | AC 01.1 | Clicking button opens the New Lesson Allocation modal                                                                  |
| 3   | AC 01.2 | AY field is pre-filled with the current Academic Year                                                                  |
| 4   | AC 01.2 | Location pre-filled if student has exactly 1 active enrolled location; otherwise blank                                 |
| 5   | AC 01.2 | Location dropdown shows all active enrolled locations or all locations user has affiliation with                       |
| 6   | AC 01.2 | Course list loads only after AY and Location are both selected                                                         |
| 7   | AC 01.2 | Course list shows all Course Masters with Course Offering (by AY) and Location Course (by Location)                    |
| 8   | AC 01.2 | Course list reloads when AY or Location changes                                                                        |
| 9   | AC 01.2 | Course search supports JP partial match                                                                                |
| 10  | AC 01.3 | User can select multiple courses to create multiple LAs in one flow                                                    |
| 11  | AC 01.3 | LA Type options: Regular, Seasonal, Trial                                                                              |
| 12  | AC 01.3 | Start date must be earlier than End date                                                                               |
| 13  | AC 01.3 | On save: user redirected to Contact page and LA appears in LA table                                                    |
| 14  | AC 01.3 | LA created without order-related fields (product details, student course id, package course, order remarks = no value) |
| 15  | AC 01.4 | Overlapping dates for same AY + Location + Course → error at course section                                            |
| 16  | AC 01.4 | Both start and end date in the past → inline error under End date: "End date must be a future date"                    |
| 17  | AC 01.4 | Start date > End date → inline error under both date fields: "Start date must be earlier than End date"                |
| 18  | AC 01.5 | CSV bulk import respects same validation and data rules as UI creation                                                 |
| 19  | AC 02.1 | Edit: Start date and End date can only be changed to a date after the original value                                   |
| 20  | AC 02.1 | Edited dates must pass all validations in AC 01.4                                                                      |
| 21  | AC 02.1 | Trial LA type: Purchased Slot editable to a value greater than the original only                                       |
| 22  | AC 02.2 | Delete only allowed when LA start date > today                                                                         |
| 23  | AC 02.2 | Delete confirmation dialog must be shown before deletion                                                               |
| 24  | AC 02.2 | On confirm delete: LA deleted, allocated lessons unlinked                                                              |
| 25  | AC 02.2 | Delete button disabled when LA start date ≤ today                                                                      |
| 26  | AC 03.1 | LA.Purchased_Slot = sum of Contract.Slot (excluding Cancelled, Voided, delete_flag = on)                               |
| 27  | AC 03.1 | LA.Purchased_Slot recalculated when contract updated or new contract added for same LA                                 |
| 28  | AC 03.2 | LA.End_Date = latest end date from linked contracts (excluding Cancelled/Voided/deleted) — TBC                         |

---

## 2. Logic Type Categorization

| #   | AC      | Logic Type(s)                           |
| --- | ------- | --------------------------------------- |
| 1   | AC 01.1 | Conditional logic, Permission logic     |
| 2   | AC 01.1 | State transition                        |
| 3   | AC 01.2 | Conditional logic                       |
| 4   | AC 01.2 | Conditional logic (decision on count)   |
| 5   | AC 01.2 | Conditional logic                       |
| 6   | AC 01.2 | Conditional logic                       |
| 7   | AC 01.2 | Data integrity, Cross-system impact     |
| 8   | AC 01.2 | State transition                        |
| 9   | AC 01.2 | Validation logic                        |
| 10  | AC 01.3 | Validation logic                        |
| 11  | AC 01.3 | Validation logic (enum)                 |
| 12  | AC 01.3 | Boundary/range logic, Validation logic  |
| 13  | AC 01.3 | State transition, Cross-system impact   |
| 14  | AC 01.3 | Data integrity                          |
| 15  | AC 01.4 | Data integrity, Validation logic        |
| 16  | AC 01.4 | Boundary/range logic, Validation logic  |
| 17  | AC 01.4 | Boundary/range logic, Validation logic  |
| 18  | AC 01.5 | Validation logic, Data integrity        |
| 19  | AC 02.1 | Boundary/range logic, Validation logic  |
| 20  | AC 02.1 | Validation logic                        |
| 21  | AC 02.1 | Boundary/range logic, Conditional logic |
| 22  | AC 02.2 | Conditional logic                       |
| 23  | AC 02.2 | State transition                        |
| 24  | AC 02.2 | Data integrity, Cross-system impact     |
| 25  | AC 02.2 | Conditional logic                       |
| 26  | AC 03.1 | Data integrity                          |
| 27  | AC 03.1 | Data integrity, Cross-system impact     |
| 28  | AC 03.2 | Data integrity (TBC)                    |

---

## 3. Test Techniques per Logic Type

| Logic Type           | Primary Technique        | Secondary Technique |
| -------------------- | ------------------------ | ------------------- |
| Validation logic     | Equivalence Partitioning | Negative Testing    |
| Boundary/range logic | Boundary Value Analysis  | Negative Testing    |
| Conditional logic    | Decision Table           | Negative Testing    |
| State transition     | State Transition Testing | CRUD Testing        |
| Permission logic     | Permission Matrix        | Decision Table      |
| Data integrity       | CRUD Testing             | Regression Analysis |
| Cross-system impact  | Regression Analysis      | CRUD Testing        |

---

## 4. Coverage Strategy Table

| AC      | Business Rule Summary                                   | Logic Type                          | Test Technique                     | Risk Level | Coverage Depth |
| ------- | ------------------------------------------------------- | ----------------------------------- | ---------------------------------- | ---------- | -------------- |
| AC 01.1 | CTA button visibility in Require LA table               | Conditional logic, Permission logic | Decision Table, Permission Matrix  | High       | Standard       |
| AC 01.1 | Button click opens modal                                | State transition                    | State Transition Testing           | Medium     | Smoke          |
| AC 01.2 | AY pre-filled with current AY                           | Conditional logic                   | Decision Table                     | Medium     | Standard       |
| AC 01.2 | Location pre-fill: 1 location → pre-filled, else blank  | Conditional logic                   | Decision Table                     | High       | Deep           |
| AC 01.2 | Location dropdown options                               | Conditional logic                   | Decision Table                     | Medium     | Standard       |
| AC 01.2 | Course list loads only after AY + Location selected     | Conditional logic                   | Decision Table                     | High       | Standard       |
| AC 01.2 | Course list filters by AY + Location (Course Offering)  | Data integrity, Cross-system impact | CRUD Testing, Regression Analysis  | High       | Standard       |
| AC 01.2 | Course list reloads on AY/Location change               | State transition                    | State Transition Testing           | Medium     | Standard       |
| AC 01.2 | JP partial search by course name                        | Validation logic                    | Equivalence Partitioning           | Low        | Smoke          |
| AC 01.3 | Multi-course selection creates multiple LAs             | Validation logic                    | Equivalence Partitioning           | High       | Standard       |
| AC 01.3 | LA Type enum: Regular / Seasonal / Trial                | Validation logic                    | Equivalence Partitioning           | Medium     | Standard       |
| AC 01.3 | Start date < End date enforced                          | Boundary/range logic                | Boundary Value Analysis            | High       | Deep           |
| AC 01.3 | Save → redirect + LA appears in table                   | State transition, Cross-system      | State Transition Testing           | High       | Standard       |
| AC 01.3 | No order-related fields on created LA                   | Data integrity                      | CRUD Testing                       | High       | Standard       |
| AC 01.4 | Overlap same AY+Location+Course → error message         | Data integrity, Validation logic    | Decision Table, Negative Testing   | Critical   | Deep           |
| AC 01.4 | Both dates in past → end date error                     | Boundary/range logic                | Boundary Value Analysis, Negative  | Critical   | Deep           |
| AC 01.4 | Start date > End date → error both fields               | Boundary/range logic                | Boundary Value Analysis, Negative  | Critical   | Deep           |
| AC 01.5 | CSV import: same validation + data rules as UI          | Validation logic, Data integrity    | Equivalence Partitioning, Negative | High       | Standard       |
| AC 02.1 | Edit Start/End date: only forward (after original)      | Boundary/range logic                | Boundary Value Analysis            | High       | Deep           |
| AC 02.1 | Edited dates re-validated per AC 01.4                   | Validation logic                    | Equivalence Partitioning, Negative | High       | Standard       |
| AC 02.1 | Trial: Purchased Slot editable to greater value only    | Boundary/range logic, Conditional   | BVA, Decision Table                | High       | Deep           |
| AC 02.2 | Delete allowed only when start date > today             | Conditional logic                   | Decision Table                     | High       | Deep           |
| AC 02.2 | Delete confirmation dialog shown                        | State transition                    | State Transition Testing           | Medium     | Standard       |
| AC 02.2 | Confirm delete: LA deleted + allocated lessons unlinked | Data integrity, Cross-system        | CRUD Testing, Regression Analysis  | Critical   | Deep           |
| AC 02.2 | Delete button disabled for past-start-date LAs          | Conditional logic                   | Decision Table, Negative Testing   | High       | Standard       |
| AC 03.1 | Purchased Slot = sum of active contracts                | Data integrity                      | CRUD Testing                       | High       | Deep           |
| AC 03.1 | Recalculated on contract create/update                  | Data integrity, Cross-system        | CRUD Testing, Regression Analysis  | High       | Deep           |
| AC 03.2 | End Date = max end date of active contracts (TBC)       | Data integrity (TBC)                | CRUD Testing                       | Medium     | Standard       |

---

## 5. High-Risk Areas

### 🔴 Critical Risk

**AC 01.4 — Overlap validation (BR 15)**

- Risk: If overlap is not detected, duplicate LA entries for the same course/AY/location period will be created, corrupting student allocation data and causing incorrect billing or lesson assignment.
- Approach: Decision table with all combinations — same AY same location same course with overlapping / non-overlapping / adjacent date ranges. Include edge cases where start/end of new LA exactly matches start/end of existing LA.

**AC 01.4 — Past date validation (BR 16)**

- Risk: If past-end-date LAs are created, students can be allocated to already-completed lessons, producing invalid system state.
- Approach: BVA at today's date boundary — end date = today (should fail), end date = tomorrow (should pass), start date in past with future end date (should pass based on current spec).

**AC 01.4 — Start > End date validation (BR 17)**

- Risk: LA with invalid date range would be created, breaking allocation logic and potentially causing system errors downstream.
- Approach: BVA — start = end (boundary, check if error), start = end - 1 day (valid), start = end + 1 day (invalid).

**AC 02.2 — Confirm delete unlinks allocated lessons (BR 24)**

- Risk: If allocated lessons are not properly unlinked, orphaned lesson-allocation references remain in the system, causing data integrity failures and potentially blocking future LA creation for the same course.
- Approach: CRUD — create LA, allocate lessons, delete LA, verify all lesson links are removed and no orphaned references exist.

---

### 🟠 High Risk

**AC 01.2 — Location pre-fill decision (BR 4)**

- Risk: If the pre-fill logic is wrong (pre-filling when there are multiple enrolled locations, or not pre-filling when there is exactly one), users will be confused and create LAs under the wrong location.
- Approach: Decision table with 3 conditions — 0 active enrolled locations, exactly 1 active enrolled location, 2+ active enrolled locations. Verify field value and dropdown behavior in each case.

**AC 01.3 — LA appears in table after save with correct data (BR 13, 14)**

- Risk: If the redirect fails or the LA is not shown in the table, or if order-related fields are populated when they shouldn't be, the creation flow is broken and data is incorrect.
- Approach: CRUD — create LA, verify redirect, verify LA row in table, inspect LA record fields to confirm no order-related values.

**AC 02.1 — Date edit forward-only constraint (BR 19)**

- Risk: If backward date edits are accepted, existing lesson allocations and student assignments may become invalid over time ranges that have already passed.
- Approach: BVA — attempt to set new start date = original start date (boundary, should fail or succeed depending on clarification), new start date = original - 1 day (should fail), new start date = original + 1 day (should pass).

**AC 02.1 — Trial Purchased Slot edit constraint (BR 21)**

- Risk: If Purchased Slot can be decreased, it may conflict with already-allocated lesson counts, causing data inconsistency.
- Approach: BVA — edit to original value (boundary), edit to original - 1 (should fail), edit to original + 1 (should pass). Decision table for LA type: Regular and Seasonal → Purchased Slot not editable; Trial → editable to greater value only.

**AC 02.2 — Delete button state based on start date (BR 22, 25)**

- Risk: If delete is enabled for past-start-date LAs, historical data can be destroyed; if disabled for future LAs, valid delete operations are blocked.
- Approach: Decision table — start date in past, start date = today, start date in future. Verify button state and behavior in each case.

**AC 03.1 — Purchased Slot auto-calc on contract events (BR 26, 27)**

- Risk: If contracts are not properly excluded (Cancelled/Voided/deleted), the slot count will be inflated and students over-allocated. If recalculation doesn't trigger on contract update/create, the count will be stale.
- Approach: CRUD — create LA, link contracts, cancel a contract, verify slot total updates; add a new contract, verify slot recalculates; mark contract as deleted, verify exclusion.

---

### 🟡 Medium Risk

**AC 01.2 — Course list reload on AY/Location change (BR 8)**

- Risk: If stale course data is displayed after changing AY or Location, users may inadvertently select courses not valid for the new AY/Location.
- Approach: State transition — select AY+Location → course list appears; change AY → course list reloads; change Location → course list reloads. Verify list reflects new selection.

**AC 01.5 — CSV bulk import (BR 18)**

- Risk: If CSV validation differs from UI validation, inconsistent LAs can be bulk-imported that would fail UI creation validation.
- Approach: EP — valid CSV (happy path), CSV with overlapping dates, CSV with past end date, CSV with start > end. Verify each row error is reported.

**AC 02.2 — Delete confirmation dialog and cancel (BR 23)**

- Risk: If cancel does not restore state, user loses data or is unexpectedly navigated away.
- Approach: State transition — trigger delete → dialog appears → cancel → verify nothing changed; trigger delete → dialog appears → confirm → verify LA deleted.

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area                                   | Existing Test Case | Overlap | New Coverage Needed                                 |
| ------------------------------------------ | ------------------ | ------- | --------------------------------------------------- |
| AC 01.1 — CTA button + modal               | None               | None    | ✅ New TC: button visibility and modal open         |
| AC 01.2 — AY/Location pre-fill logic       | None               | None    | ✅ New TC: 3 location scenarios (0, 1, 2+)          |
| AC 01.2 — Course list load/reload          | None               | None    | ✅ New TC: load after AY+Location, reload on change |
| AC 01.3 — Create LA happy path (single)    | None               | None    | ✅ New TC: single course, all LA types              |
| AC 01.3 — Create LA multi-course           | None               | None    | ✅ New TC: multi-course selection in one flow       |
| AC 01.4 — Overlap validation               | None               | None    | ✅ New TC: all overlap scenarios + error message    |
| AC 01.4 — Past date validation             | None               | None    | ✅ New TC: BVA at today boundary                    |
| AC 01.4 — Start > End validation           | None               | None    | ✅ New TC: BVA start vs end                         |
| AC 01.5 — CSV bulk import                  | None               | None    | ✅ New TC: valid CSV + each validation failure      |
| AC 02.1 — Edit date forward-only           | None               | None    | ✅ New TC: BVA original date as boundary            |
| AC 02.1 — Trial Purchased Slot edit        | None               | None    | ✅ New TC: edit Trial vs Regular/Seasonal           |
| AC 02.2 — Delete future vs past start date | None               | None    | ✅ New TC: decision table by start date             |
| AC 02.2 — Delete confirmation + unlink     | None               | None    | ✅ New TC: confirm delete, verify lesson unlink     |
| AC 03.1 — Purchased Slot auto-calc         | None               | None    | ✅ New TC: contract cancel/add/update triggers      |
| AC 03.2 — End Date auto-calc (TBC)         | None               | None    | ⏸ Defer until AC 03.2 is confirmed                  |

---

## 7. Suggested Test Suite Structure

```
output/test-cases/lesson-management/student-session/lesson-allocation/
  ├── create-la-ui.md            → AC 01.1, 01.2, 01.3 — Create LA via UI (CTA, form, happy path)
  ├── create-la-validation.md    → AC 01.4 — Validation rules (overlap, past date, start > end)
  ├── create-la-csv.md           → AC 01.5 — CSV bulk import (valid + all failure scenarios)
  ├── edit-delete-la.md          → AC 02.1, 02.2 — Edit date/slot, delete with guard conditions
  └── la-auto-calculation.md     → AC 03.1, 03.2 — Purchased Slot + End Date auto-calc (pending PBT-1812)
```

> ℹ️ All test cases in this suite are **[Riso]-prefixed** as this is a tenant-specific feature.
> US03 test cases are drafted but should be executed only after PBT-1812 is confirmed in scope.
