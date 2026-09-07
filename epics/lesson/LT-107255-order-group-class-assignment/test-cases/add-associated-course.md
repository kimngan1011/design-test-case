# Test Cases: LT-107255 — Order Group Class Assignment

## Suite: Add Associated Course

### Lesson Allocation – Add Associated Course – One-Time with Class – LA and Class Member Created from OGC Date

**Description:** AC-03, AC-06 — Decision Table — A One-Time added course with a selected class uses the OGC submission date because no effective date is entered.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org.
- Student A has an active One-Time product for Course A starting 2026-08-01 and ending 2026-12-31.
- Course B has Require Allocation = True; Class B belongs to Course B.
- today = 2026-08-10; existing_product_start = 2026-08-01; existing_product_end = 2026-12-31.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Student A's existing product and start an update order. | The update-order form opens. | product_type = One-Time; today = 2026-08-10 |
| 2 | Add Course B and select Class B. | Course B and Class B are added; no effective-date input is requested. | course = Course B; class = Class B; effective_date = system default |
| 3 | Submit the update order. | The update order is submitted without an error. | OGC submission date = 2026-08-10 |
| 4 | Open the new Course B LA and Class Member record. | The Course B LA is created and its Class Member starts on 2026-08-10, the OGC submission date. | expected Class Member start = 2026-08-10 |

**Severity:** major
**Priority:** high

---

### Lesson Allocation – Add Associated Course – Slot-Based with Class – LA and Class Member Created from OGC Date

**Description:** AC-03, AC-06 — Decision Table — A Slot-Based added course with a selected class uses the OGC submission date because no effective date is entered.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org.
- Student A has an active Slot-Based product for Course A starting 2026-08-01 and ending 2026-12-31.
- Course B has Require Allocation = True; Class B belongs to Course B.
- today = 2026-08-10; existing_product_start = 2026-08-01; existing_product_end = 2026-12-31; selected_slots = 12.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Student A's existing product and start an update order. | The update-order form opens. | product_type = Slot-Based; today = 2026-08-10 |
| 2 | Add Course B, select Class B, and retain the selected slots. | Course B and Class B are added; no effective-date input is requested. | course = Course B; class = Class B; slots = 12 |
| 3 | Submit the update order. | The update order is submitted without an error. | OGC submission date = 2026-08-10 |
| 4 | Open the new Course B LA and Class Member record. | The Course B LA is created and its Class Member starts on 2026-08-10, the OGC submission date. | expected Class Member start = 2026-08-10 |

**Severity:** major
**Priority:** high

---

### Lesson Allocation – Add Associated Course – Schedule with Class – LA and Class Member Use Effective Date

**Description:** AC-03, AC-06 — Decision Table — A Schedule added course with a selected class uses the staff-selected effective date.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org.
- Student A has an active Schedule product for Course A starting 2026-08-01 and ending 2026-12-31.
- Course B has Require Allocation = True; Class B belongs to Course B.
- today = 2026-08-10; effective_date = 2026-09-01; product_end_date = 2026-12-31.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Student A's existing product and start an update order. | The update-order form opens. | product_type = Schedule; today = 2026-08-10 |
| 2 | Add Course B, select Class B, and enter the effective date. | Course B is added with the selected class and effective date. | course = Course B; class = Class B; effective_date = 2026-09-01 |
| 3 | Submit the update order. | The update order is submitted without an error. | effective_date = 2026-09-01 |
| 4 | Open the new Course B LA and Class Member record. | The Course B LA and Class Member both start on 2026-09-01 and end on 2026-12-31. | expected duration = 2026-09-01 to 2026-12-31 |

**Severity:** major
**Priority:** high

---

### Lesson Allocation – Add Associated Course – No Class Selected – LA Created Without Class Member

**Description:** AC-04 — Equivalence Partitioning — An added course without a class creates its LA but no class-based records.

**Preconditions:**
- Logged in as HQ or CM Staff to the Salesforce org.
- Student A has an active Schedule product for Course A starting 2026-08-01 and ending 2026-12-31.
- Course B has Require Allocation = True.
- today = 2026-08-10; effective_date = 2026-09-01; product_end_date = 2026-12-31.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Open Student A's existing product and start an update order. | The update-order form opens. | product_type = Schedule |
| 2 | Add Course B, enter effective date 2026-09-01, and leave the class unselected. | Course B is valid with no class selected. | course = Course B; class = blank; effective_date = 2026-09-01 |
| 3 | Submit the update order. | The update order is submitted without an error. | class = blank |
| 4 | Open the Course B LA, Class Member history, and Course B group lessons. | Course B LA starts on 2026-09-01; no Class Member and no class-based Student Session are created. | expected Class Member count = 0; expected auto-assigned Student Session count = 0 |

**Severity:** major
**Priority:** high
