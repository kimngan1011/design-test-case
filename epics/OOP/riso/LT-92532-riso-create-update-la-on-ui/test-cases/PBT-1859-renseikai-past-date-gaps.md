# Test Cases: PBT-1859 — Renseikai Past-Date Gaps (Groups B, C, D)

## Suite: Lesson Allocation

---

### Lesson Allocation – Cancel Order with Past Effective Date – Slot-Based – LA Deleted

**Description:** AC 06.2, AC 06.6 — State Transition / BVA — Validates that cancelling a Slot-Based product order with an effective date in the past deletes the LA entirely (not just updates end date), consistent with cancel behavior for Slot-Based product type.

**Preconditions:**

- User has created an order with product type = Slot-Based; Require Allocation flag = True; order start date < current date (e.g. 2026-01-01)
- LA exists for the student with start date = 2026-01-01
- User has created an individual lesson and added this student to the lesson

| #   | Action                                                                                  | Expected Result                                             | Test Data                  |
| --- | --------------------------------------------------------------------------------------- | ----------------------------------------------------------- | -------------------------- |
| 1   | Go to Student Detail → Click "New Order Group" → Select location → Save                 | Order Group created                                         | ""                         |
| 2   | At Order Group Product, click "Manage" → Select the Slot-Based product → Click "Cancel" | Cancel order form opens                                     | ""                         |
| 3   | Enter effective date = 2026-03-01 (past date; < current date 2026-04-02)                | Effective date field shows 2026-03-01; no inline error      | Effective date: 2026-03-01 |
| 4   | Click "Save Draft"                                                                      | Order saved as draft with no error                          | ""                         |
| 5   | Click "Submit"                                                                          | Order submitted successfully                                | ""                         |
| 6   | Navigate to Contact → Course tab → Lesson Allocation list                               | LA for this Slot-Based product is deleted; no entry visible | ""                         |
| 7   | Check lesson assignment                                                                 | Student is removed from lessons that were linked to this LA | ""                         |

**Severity:** major
**Priority:** high

---

### Lesson Allocation – Cancel Order with Past Effective Date – One-Time – LA Deleted

**Description:** AC 06.2, AC 06.6 — State Transition / BVA — Validates that cancelling a One-Time product order with a past effective date deletes the LA entirely.

**Preconditions:**

- User has created an order with product type = One-Time; Require Allocation flag = True; order start date < current date (e.g. 2026-01-01)
- LA exists for the student with start date = 2026-01-01
- User has created an individual lesson and added this student to the lesson

| #   | Action                                                                                | Expected Result                                           | Test Data                  |
| --- | ------------------------------------------------------------------------------------- | --------------------------------------------------------- | -------------------------- |
| 1   | Go to Student Detail → Click "New Order Group" → Select location → Save               | Order Group created                                       | ""                         |
| 2   | At Order Group Product, click "Manage" → Select the One-Time product → Click "Cancel" | Cancel order form opens                                   | ""                         |
| 3   | Enter effective date = 2026-03-01 (past date; < current date 2026-04-02)              | Effective date field shows 2026-03-01; no inline error    | Effective date: 2026-03-01 |
| 4   | Click "Save Draft"                                                                    | Order saved as draft with no error                        | ""                         |
| 5   | Click "Submit"                                                                        | Order submitted successfully                              | ""                         |
| 6   | Navigate to Contact → Course tab → Lesson Allocation list                             | LA for this One-Time product is deleted; no entry visible | ""                         |
| 7   | Check lesson assignment                                                               | Student is removed from lessons linked to this LA         | ""                         |

**Severity:** major
**Priority:** high

---

### Lesson Allocation – Enrollment Order with Past Start Date – LA Created with Past Start Date

**Description:** AC 02.2 — CRUD Testing — Validates that creating an enrollment application with a past start date results in an LA being created with start date = the past date, following the same LA creation rules as a standard order.

**Preconditions:**

- User has created a product offering with package types = One-Time, Schedule, Frequency, and Slot-Based; each product has Course A added with Require Allocation flag = True
- User has created a student with a grade and location = product offering
- User has created a recurring group lesson with class
- Current date = 2026-04-02

| #   | Action                                                                                                                          | Expected Result                                                    | Test Data                              |
| --- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | -------------------------------------- |
| 1   | Go to Student Detail → Click "Create Enrollment Application" button                                                             | Enrollment application form opens                                  | ""                                     |
| 2   | At Order Group Product, click "Manage" → Click "Add Product" → Select the product offering and course offering → Assign a class | Product and course selected; class assigned                        | Product with Require Allocation = True |
| 3   | Enter start date = 2026-01-15 (past date < current date 2026-04-02)                                                             | Start date field shows 2026-01-15; no inline error                 | Start date: 2026-01-15                 |
| 4   | Click "Save Draft"                                                                                                              | Enrollment saved as draft with no error                            | ""                                     |
| 5   | Click "Submit Enrollment"                                                                                                       | Enrollment submitted successfully                                  | ""                                     |
| 6   | Navigate to Contact → Course tab → Require Lesson Allocation and Lesson Allocation lists                                        | LAs are created for each product type with start date = 2026-01-15 | ""                                     |
| 7   | Check LA duration on one of the created LAs                                                                                     | Start date = 2026-01-15; end date = order end date                 | ""                                     |
| 8   | Check total session count                                                                                                       | Total session count = 0; no student session auto-created           | ""                                     |
| 9   | Check class assignment                                                                                                          | Class member created with start date & end date = LA duration      | ""                                     |

**Severity:** major
**Priority:** high

---

### Lesson Allocation – Update Slot – Past Effective Date – Purchased Slot Updated, Duration Unchanged

**Description:** AC 05.1, AC 05.2, AC 05.3, AC 05.6 — BVA — Validates that updating the slot/week on a Frequency product with an effective date in the past updates the purchased slot and recalculates total session count, while leaving the LA duration unchanged.

**Preconditions:**

- User has created an order with product type = Frequency; Require Allocation flag = True; order start date = 2026-01-01
- LA exists; current purchased slot/week = 2
- User has assigned the student to a group lesson by class
- Current date = 2026-04-02

| #   | Action                                                                                                   | Expected Result                                                           | Test Data                           |
| --- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ----------------------------------- |
| 1   | Go to Student Detail → Click "New Order Group" → Select location → Save                                  | Order Group created                                                       | ""                                  |
| 2   | At Order Group Product, click "Manage" → Select the Frequency product → Click "Update"                   | Update order form opens                                                   | ""                                  |
| 3   | Increase slot/week from 2 to 3 → Enter effective date = 2026-02-01 (past date < current date 2026-04-02) | Slot/week field shows 3; effective date shows 2026-02-01; no inline error | Slot: 3; Effective date: 2026-02-01 |
| 4   | Click "Save Draft"                                                                                       | Order saved as draft with no error                                        | ""                                  |
| 5   | Click "Submit"                                                                                           | Order submitted successfully                                              | ""                                  |
| 6   | Navigate to Contact → Course tab → Lesson Allocation                                                     | Purchased slot on LA updated to 3/week                                    | ""                                  |
| 7   | Check LA duration                                                                                        | LA start date and end date are unchanged from original order              | ""                                  |
| 8   | Check total session count                                                                                | Total session count recalculated based on new slot/week value             | ""                                  |
| 9   | Check student session                                                                                    | No new student session auto-created                                       | ""                                  |

**Severity:** major
**Priority:** high

---

### Lesson Allocation – Update Slot – Today Effective Date – Purchased Slot Updated, Duration Unchanged

**Description:** AC 05.1, AC 05.2, AC 05.3, AC 05.6 — BVA — Validates slot update with effective date = current date (today boundary).

**Preconditions:**

- User has created an order with product type = Frequency; Require Allocation flag = True; order start date = 2026-01-01
- LA exists; current purchased slot/week = 2
- User has assigned the student to a group lesson by class
- Current date = 2026-04-02

| #   | Action                                                                              | Expected Result                                                   | Test Data                           |
| --- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------- |
| 1   | Go to Student Detail → Click "New Order Group" → Select location → Save             | Order Group created                                               | ""                                  |
| 2   | At Order Group Product, click "Manage" → Select Frequency product → Click "Update"  | Update order form opens                                           | ""                                  |
| 3   | Increase slot/week from 2 to 3 → Enter effective date = 2026-04-02 (= current date) | Slot/week = 3; effective date = 2026-04-02; no inline error       | Slot: 3; Effective date: 2026-04-02 |
| 4   | Click "Save Draft" → Click "Submit"                                                 | Order submitted successfully                                      | ""                                  |
| 5   | Navigate to Contact → Course tab → Lesson Allocation                                | Purchased slot on LA updated to 3/week                            | ""                                  |
| 6   | Check LA duration                                                                   | LA start date and end date unchanged                              | ""                                  |
| 7   | Check total session count                                                           | Total session count recalculated; no student session auto-created | ""                                  |

**Severity:** major
**Priority:** high

---

### Lesson Allocation – Update Slot – Future Effective Date – Purchased Slot Updated, Duration Unchanged

**Description:** AC 05.1, AC 05.2, AC 05.3, AC 05.6 — BVA — Validates slot update with effective date in the future.

**Preconditions:**

- User has created an order with product type = Frequency; Require Allocation flag = True; order start date = 2026-01-01
- LA exists; current purchased slot/week = 2
- User has assigned the student to a group lesson by class
- Current date = 2026-04-02

| #   | Action                                                                                          | Expected Result                                                   | Test Data                           |
| --- | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------- |
| 1   | Go to Student Detail → Click "New Order Group" → Select location → Save                         | Order Group created                                               | ""                                  |
| 2   | At Order Group Product, click "Manage" → Select Frequency product → Click "Update"              | Update order form opens                                           | ""                                  |
| 3   | Increase slot/week from 2 to 3 → Enter effective date = 2026-05-01 (future date > current date) | Slot/week = 3; effective date = 2026-05-01; no inline error       | Slot: 3; Effective date: 2026-05-01 |
| 4   | Click "Save Draft" → Click "Submit"                                                             | Order submitted successfully                                      | ""                                  |
| 5   | Navigate to Contact → Course tab → Lesson Allocation                                            | Purchased slot on LA updated to 3/week                            | ""                                  |
| 6   | Check LA duration                                                                               | LA start date and end date unchanged                              | ""                                  |
| 7   | Check total session count                                                                       | Total session count recalculated; no student session auto-created | ""                                  |

**Severity:** major
**Priority:** high
