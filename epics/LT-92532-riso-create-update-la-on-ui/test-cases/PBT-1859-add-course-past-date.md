# Test Cases: PBT-1859 — Add New Course with Past Date (Lesson Allocation)

## Suite: Add New Course with Past Date (PBT-1859)

---

### Lesson Allocation – Add Associated Course – Past Effective Date ≥ Product Start Date – New Course LA Created

**Description:** AC 03.1, AC 03.3 — BVA / Happy Path — Validates that adding a new associated course via an update order with a past effective date (≥ product start date) creates a new LA with start date = effective date, and leaves the existing LA unchanged.

**Preconditions:**

- User has a student with an active enrolled location
- User has created a product offering (package type = Schedule) with Course A added; Require Allocation flag = True
- User has submitted an order for the student with product start date = 2026-01-01; Course A LA exists with start date = 2026-01-01
- User has added Course B to the product offering (Require Allocation = True)
- Current date = 2026-04-02

| #   | Action                                                                                                               | Expected Result                                                                                | Test Data                          |
| --- | -------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------- |
| 1   | Go to Student Detail → Click "New Order Group" button                                                                | New Order Group dialog opens                                                                   | ""                                 |
| 2   | Select the student's location and save                                                                               | Order Group is created                                                                         | Student's active enrolled location |
| 3   | At Order Group Product, click "Manage" button → Select the existing product → Click "Update"                         | Update order form opens showing current product                                                | ""                                 |
| 4   | Click "Add Course" → Select Course B → Enter effective date = 2026-01-10 (past date ≥ product start date 2026-01-01) | Course B row added with effective date field showing 2026-01-10                                | Effective date: 2026-01-10         |
| 5   | Assign a class for Course B                                                                                          | Class assignment saved                                                                         | Valid class for Course B           |
| 6   | Click "Save Draft"                                                                                                   | Order saved as draft with no error message                                                     | ""                                 |
| 7   | Click "Submit"                                                                                                       | Order submitted successfully                                                                   | ""                                 |
| 8   | Navigate to Contact → Course tab → Lesson Allocation list                                                            | New LA for Course B is visible in the list with start date = 2026-01-10                        | ""                                 |
| 9   | Check existing Course A LA                                                                                           | Course A LA still exists with original start date = 2026-01-01 and original end date unchanged | ""                                 |
| 10  | Check new Course B LA teaching method                                                                                | Teaching method on Course B LA = teaching method of Course B's course offering's course master | ""                                 |
| 11  | Check new Course B LA total session count                                                                            | Total session count = 0; no student session auto-created                                       | ""                                 |

**Severity:** major
**Priority:** high

---

### Lesson Allocation – Add Associated Course – Past Effective Date = Product Start Date – Boundary Allowed

**Description:** AC 03.2, AC 03.3 — BVA Boundary — Validates that effective date exactly equal to the product start date is accepted (lower boundary of allowed range).

**Preconditions:**

- User has a student with an active enrolled location
- User has a product offering (package type = Frequency) with Course A; submitted order with product start date = 2026-01-01; Course A LA exists
- User has added Course B to the product offering (Require Allocation = True)
- Current date = 2026-04-02

| #   | Action                                                                                          | Expected Result                                                                | Test Data                  |
| --- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | -------------------------- |
| 1   | Go to Student Detail → Click "New Order Group" → Select location → Save                         | Order Group created                                                            | ""                         |
| 2   | At Order Group Product, click "Manage" → Select product → Click "Update"                        | Update order form opens                                                        | ""                         |
| 3   | Click "Add Course" → Select Course B → Enter effective date = 2026-01-01 (= product start date) | Course B row added with effective date = 2026-01-01; no inline error displayed | Effective date: 2026-01-01 |
| 4   | Click "Save Draft"                                                                              | Order saved as draft with no error                                             | ""                         |
| 5   | Click "Submit"                                                                                  | Order submitted successfully                                                   | ""                         |
| 6   | Navigate to Contact → Course tab → Lesson Allocation list                                       | New LA for Course B visible with start date = 2026-01-01                       | ""                         |

**Severity:** major
**Priority:** high

---

### Lesson Allocation – Add Associated Course – Past Effective Date < Product Start Date – Order Submission Blocked

**Description:** AC 03.2 — Negative Testing — Validates that effective date earlier than the product start date is rejected with the correct EN and JP error messages, and the order cannot be saved or submitted.

**Preconditions:**

- User has a student with an active enrolled location
- User has a product offering with Course A; submitted order with product start date = 2026-01-01; Course A LA exists
- User has added Course B to the product offering (Require Allocation = True)
- Current date = 2026-04-02

| #   | Action                                                                                                     | Expected Result                                                                                                                                                                                                                 | Test Data                  |
| --- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| 1   | Go to Student Detail → Click "New Order Group" → Select location → Save                                    | Order Group created                                                                                                                                                                                                             | ""                         |
| 2   | At Order Group Product, click "Manage" → Select product → Click "Update"                                   | Update order form opens                                                                                                                                                                                                         | ""                         |
| 3   | Click "Add Course" → Select Course B → Enter effective date = 2025-12-01 (< product start date 2026-01-01) | Effective date entered                                                                                                                                                                                                          | Effective date: 2025-12-01 |
| 4   | Click "Save Draft"                                                                                         | Order cannot be saved; inline error displayed under effective date field: "The selected effective date is earlier than the product start date." (EN); "選択された適用開始日は、商品の開始日以降の日付を選択してください。" (JP) | ""                         |
| 5   | Click "Submit" (if accessible)                                                                             | Submission blocked; same error persists                                                                                                                                                                                         | ""                         |
| 6   | Navigate to Contact → Course tab → Lesson Allocation list                                                  | No new LA created for Course B                                                                                                                                                                                                  | ""                         |

**Severity:** critical
**Priority:** high

---

### Lesson Allocation – Void Update Order That Added New Course with Past Effective Date – Added Course LA Deleted, Original Unchanged

**Description:** AC 07.6 — State Transition Testing — Validates that voiding an update order which added a new course using a past effective date deletes only the newly added course LA, and leaves the original course LA intact.

**Preconditions:**

- User has completed the scenario from TC "Add Associated Course – Past Effective Date ≥ Product Start Date" above
- Course A LA exists: start date = 2026-01-01
- Course B LA exists: start date = 2026-01-10 (created via past-date update order)
- The update order adding Course B is in "Submitted" status and visible in the billing tab

| #   | Action                                                                           | Expected Result                                                                                | Test Data |
| --- | -------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | --------- |
| 1   | Go to Student Detail → Billing tab                                               | Billing tab shows the list of order groups including the update order that added Course B      | ""        |
| 2   | Open the update order group that added Course B with effective date = 2026-01-10 | Order group detail opens showing the submitted update order                                    | ""        |
| 3   | Click "Void" on the update order                                                 | Void confirmation dialog appears                                                               | ""        |
| 4   | Confirm void action                                                              | Order status changes to "Voided"                                                               | ""        |
| 5   | Navigate to Contact → Course tab → Lesson Allocation list                        | Course B LA is removed from the list                                                           | ""        |
| 6   | Check Course A LA                                                                | Course A LA still exists with original start date = 2026-01-01 and original end date unchanged | ""        |
| 7   | Check total session count on Course A LA                                         | Total session count on Course A LA is unchanged from before the void                           | ""        |

**Severity:** critical
**Priority:** high
