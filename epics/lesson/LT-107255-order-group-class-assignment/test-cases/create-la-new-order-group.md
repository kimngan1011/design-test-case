# Test Cases: LT-107255 — Order Group Class Assignment

## Suite: Create LA – New Order Group

### Lesson Allocation – Create Order – No Class Selected – LA Created Without Class Member

**Description:** AC-04 — Equivalence Partitioning — A supported no-class order creates the required LA without creating class-based records.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org.
- Student A has active enrollment at Location 1 and a payment method.
- Course A has Require Allocation = True.
- One-Time product for Course A has Availability Set In Order = True.
- today = 2026-08-10; product_start_date = 2026-08-10; product_end_date = 2026-12-31.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Student A, create a New Order Group for Location 1, and save. | A new Order Group is available for product selection. | today = 2026-08-10; location = Location 1 |
| 2 | Add the One-Time product for Course A and enter the product start and end dates without selecting a class. | The product row is valid and no class is selected. | product_type = One-Time; class = blank; start = 2026-08-10; end = 2026-12-31 |
| 3 | Save the draft and submit the order. | The order is submitted without an error. | class = blank |
| 4 | Open Student A's Course tab and locate the Course A Lesson Allocation. | One Course A LA is created with start date 2026-08-10 and end date 2026-12-31. | expected LA duration = 2026-08-10 to 2026-12-31 |
| 5 | Open Class Member history and Course A group lessons. | No Class Member and no class-based Student Session are created for this order. | expected Class Member count = 0; expected auto-assigned Student Session count = 0 |

**Severity:** major
**Priority:** high

---

### Lesson Allocation – Create Order – Same Course with Different Classes and Durations – Each LA Uses Its Matching Class

**Description:** AC-05 — Pairwise — Duplicate course rows with different durations resolve Class A and Class B independently.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org.
- Student A has active enrollment at Location 1 and a payment method.
- Course A has Require Allocation = True; Class A and Class B both belong to Course A.
- Slot-Based product for Course A has Availability Set In Order = True.
- today = 2026-08-10; duration_a = 2026-08-10 to 2026-09-30; duration_b = 2026-10-01 to 2026-12-31.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Student A and create a New Order Group for Location 1. | A new Order Group is available for product selection. | today = 2026-08-10 |
| 2 | Add a Slot-Based Course A row with Class A and duration A. | The first product row shows Course A, Class A, and duration A. | row 1: Course A; Class A; 2026-08-10 to 2026-09-30 |
| 3 | Add a second Slot-Based Course A row with Class B and duration B. | The second product row shows Course A, Class B, and duration B without replacing the first row. | row 2: Course A; Class B; 2026-10-01 to 2026-12-31 |
| 4 | Submit the order. | The order is submitted without an error. | two Course A product rows |
| 5 | Open the Course A Lesson Allocations and their Class Member records. | Two distinct LAs exist: duration A is linked to Class A and duration B is linked to Class B. | LA A = 2026-08-10 to 2026-09-30; LA B = 2026-10-01 to 2026-12-31 |

**Severity:** critical
**Priority:** high

---

### Lesson Allocation – Create Order – Same Course and Class with Different Durations – Separate LAs Retain Both Durations

**Description:** AC-05 — Pairwise — Duplicate course rows may select the same class while retaining independent LA and Class Member durations.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org.
- Student A has active enrollment at Location 1 and a payment method.
- Course A has Require Allocation = True; Class A belongs to Course A.
- Slot-Based product for Course A has Availability Set In Order = True.
- today = 2026-08-10; duration_a = 2026-08-10 to 2026-09-30; duration_b = 2026-10-01 to 2026-12-31.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Student A and create a New Order Group for Location 1. | A new Order Group is available for product selection. | today = 2026-08-10 |
| 2 | Add a Slot-Based Course A row with Class A and duration A. | The first product row shows Course A, Class A, and duration A. | row 1: Course A; Class A; 2026-08-10 to 2026-09-30 |
| 3 | Add a second Slot-Based Course A row with the same Class A and duration B. | The second product row is retained with its own duration. | row 2: Course A; Class A; 2026-10-01 to 2026-12-31 |
| 4 | Submit the order. | The order is submitted without an error. | two Course A product rows |
| 5 | Open the Course A Lesson Allocations and Class A member history. | Two distinct LAs and two Class Member records exist for Class A; each record retains the duration of its matching product row. | expected durations: 2026-08-10 to 2026-09-30 and 2026-10-01 to 2026-12-31 |

**Severity:** critical
**Priority:** high

---

### Lesson Allocation – Create Order – JST and UTC Date Boundary – Class Member Uses the JST Business Date

**Description:** AC-01, AC-02 — Boundary Value Analysis — A class-selected new order preserves the JST business date when the corresponding UTC timestamp is on the previous calendar day.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org using Asia/Tokyo timezone.
- Student A has active enrollment at Location 1 and a payment method.
- Course A has Require Allocation = True; Class A belongs to Course A.
- One-Time product for Course A has Availability Set In Order = True.
- current_time = 2026-08-10 00:30 JST (= 2026-08-09 15:30 UTC); product_start_date = 2026-08-10; product_end_date = 2026-12-31.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Create a New Order Group for Student A while the business date is 2026-08-10 in JST. | The new Order Group uses the JST business date 2026-08-10. | current_time = 2026-08-10 00:30 JST (= 2026-08-09 15:30 UTC) |
| 2 | Add the One-Time product for Course A with Class A and submit the order. | The order is submitted without an error. | class = Class A; start = 2026-08-10; end = 2026-12-31 |
| 3 | Open the Class Member record for Class A. | The Class Member start date displays 2026-08-10, not the prior UTC calendar date 2026-08-09; its end date displays 2026-12-31. | expected start = 2026-08-10 JST; UTC representation = 2026-08-09 15:30 |

**Severity:** major
**Priority:** high
