# Test Cases: LT-107256 — Withus Class Member Past Start Date

## Suite: Order Group Class Member

### [Withus Juku] Class Member – Order Group Class – LA Start Date Entered by Staff – Historical date accepted

**Description:** AC-01 — Decision Table and Boundary Value Analysis — A staff-entered Order Group Class date equal to LA start is accepted for Withus when the setting is enabled.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled.
- Student A has a Course A LA from 2026-08-01 through 2026-12-31; Class A belongs to Course A.
- `today = 2026-08-12`; `target_date = 2026-08-01`; Order Group Class allows staff to enter the Class Member effective date.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Student A's Create Order > Order Group Class flow and select Course A and Class A. | The Class Member effective-date input is available to staff. | today = 2026-08-12; setting = enabled |
| 2 | Enter 2026-08-01 as the Class Member effective date. | The flow accepts the date without the lower-bound error. | target_date = LA start = 2026-08-01 |
| 3 | Save or submit the Order Group Class according to the existing flow and open Class Member history. | The entered Class A Class Member starts 2026-08-01; no old Class Member data is processed by this change. | expected start = 2026-08-01 |

**Severity:** major
**Priority:** high

---

## Product Type Regression Coverage

### [Withus Juku] Class Member – Create Order – One-Time product – Class Member synced to Back Office

**Description:** AC-01 — Regression — A One-Time Create Order creates the expected Class Member and syncs it to Back Office without lesson auto-assignment checks.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled; Course A requires allocation; Class A belongs to Course A.
- `today = 2026-08-12`; `LA_start_date = 2026-08-01`; `LA_end_date = 2026-12-31`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Create a New Order Group for Student A and select the enrolled location. | A new Order Group is available for product selection. | today = 2026-08-12 |
| 2 | Add the One-Time product for Course A, set the LA dates, select Class A, and submit the order. | The order is submitted and a Course A LA is created. | product_type = One-Time; LA = 2026-08-01 to 2026-12-31; class = A |
| 3 | Open the created Class Member. | Class A starts 2026-08-01 and ends 2026-12-31 with linkage to the created LA. | expected Class Member = 2026-08-01 to 2026-12-31 |
| 4 | Open Back Office and view Student A's Course A class information. | The synced Class A membership is visible in Back Office with the same effective dates. | expected BO Class A = 2026-08-01 to 2026-12-31 |

**Severity:** major
**Priority:** high

---

### [Withus Juku] Class Member – Create Order – Slot-Based product – Class Member synced to Back Office

**Description:** AC-01 — Regression — A Slot-Based Create Order creates the expected Class Member and syncs it to Back Office without lesson auto-assignment checks.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled; Course A requires allocation; Class A belongs to Course A.
- `today = 2026-08-12`; `LA_start_date = 2026-08-01`; `LA_end_date = 2026-12-31`; `selected_slots = 12`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Create a New Order Group for Student A and select the enrolled location. | A new Order Group is available for product selection. | today = 2026-08-12 |
| 2 | Add the Slot-Based product for Course A, set the LA dates and 12 slots, select Class A, and submit the order. | The order is submitted and a Course A LA is created. | product_type = Slot-Based; slots = 12; LA = 2026-08-01 to 2026-12-31; class = A |
| 3 | Open the created Class Member. | Class A starts 2026-08-01 and ends 2026-12-31 with linkage to the created LA. | expected Class Member = 2026-08-01 to 2026-12-31 |
| 4 | Open Back Office and view Student A's Course A class information. | The synced Class A membership is visible in Back Office with the same effective dates. | expected BO Class A = 2026-08-01 to 2026-12-31 |

**Severity:** major
**Priority:** high

---

### [Withus Juku] Class Member – Create Order – Schedule product – Class Member synced to Back Office

**Description:** AC-01 — Regression — A Schedule Create Order creates the expected Class Member and syncs it to Back Office without lesson auto-assignment checks.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled; Course A requires allocation; Class A belongs to Course A.
- `today = 2026-08-12`; `LA_start_date = 2026-08-01`; `LA_end_date = 2026-12-31`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Create a New Order Group for Student A and select the enrolled location. | A new Order Group is available for product selection. | today = 2026-08-12 |
| 2 | Add the Schedule product for Course A, set the LA dates, select Class A, and submit the order. | The order is submitted and a Course A LA is created. | product_type = Schedule; LA = 2026-08-01 to 2026-12-31; class = A |
| 3 | Open the created Class Member. | Class A starts 2026-08-01 and ends 2026-12-31 with linkage to the created LA. | expected Class Member = 2026-08-01 to 2026-12-31 |
| 4 | Open Back Office and view Student A's Course A class information. | The synced Class A membership is visible in Back Office with the same effective dates. | expected BO Class A = 2026-08-01 to 2026-12-31 |

**Severity:** major
**Priority:** high

---

### [Withus Juku] Class Member – Create Order – Frequency product – Class Member synced to Back Office

**Description:** AC-01 — Regression — A Frequency Create Order creates the expected Class Member and syncs it to Back Office without lesson auto-assignment checks.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled; Course A requires allocation; Class A belongs to Course A.
- `today = 2026-08-12`; `LA_start_date = 2026-08-01`; `LA_end_date = 2026-12-31`; `selected_slots = 12`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Create a New Order Group for Student A and select the enrolled location. | A new Order Group is available for product selection. | today = 2026-08-12 |
| 2 | Add the Frequency product for Course A, set the LA dates and 12 slots, select Class A, and submit the order. | The order is submitted and a Course A LA is created. | product_type = Frequency; slots = 12; LA = 2026-08-01 to 2026-12-31; class = A |
| 3 | Open the created Class Member. | Class A starts 2026-08-01 and ends 2026-12-31 with linkage to the created LA. | expected Class Member = 2026-08-01 to 2026-12-31 |
| 4 | Open Back Office and view Student A's Course A class information. | The synced Class A membership is visible in Back Office with the same effective dates. | expected BO Class A = 2026-08-01 to 2026-12-31 |

**Severity:** major
**Priority:** high

---

### [Withus Juku] Class Member – Add New Course – One-Time product – Class Member synced to Back Office

**Description:** AC-01 — Regression — Adding a One-Time associated course creates the Class Member and syncs it to Back Office without lesson auto-assignment checks.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled; Student A has an active One-Time product for Course A.
- Course B requires allocation; Class B belongs to Course B; `today = 2026-08-12`; `LA_end_date = 2026-12-31`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Start an update order for Student A's existing One-Time product. | The update-order form opens. | product_type = One-Time; today = 2026-08-12 |
| 2 | Add Course B, select Class B, and submit the update order. | The Course B LA is created with the OGC submission date as its Class Member start. | OGC submission date = 2026-08-12; class = B |
| 3 | Open the Course B Class Member. | Class B starts 2026-08-12 and ends 2026-12-31 with linkage to the Course B LA. | expected Class Member = 2026-08-12 to 2026-12-31 |
| 4 | Open Back Office and view Student A's Course B class information. | The synced Class B membership is visible in Back Office with the same effective dates. | expected BO Class B = 2026-08-12 to 2026-12-31 |

**Severity:** major
**Priority:** high

---

### [Withus Juku] Class Member – Add New Course – Slot-Based product – Class Member synced to Back Office

**Description:** AC-01 — Regression — Adding a Slot-Based associated course creates the Class Member and syncs it to Back Office without lesson auto-assignment checks.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled; Student A has an active Slot-Based product for Course A.
- Course B requires allocation; Class B belongs to Course B; `today = 2026-08-12`; `LA_end_date = 2026-12-31`; `selected_slots = 12`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Start an update order for Student A's existing Slot-Based product. | The update-order form opens. | product_type = Slot-Based; today = 2026-08-12 |
| 2 | Add Course B, select Class B, retain 12 slots, and submit the update order. | The Course B LA is created with the OGC submission date as its Class Member start. | OGC submission date = 2026-08-12; slots = 12; class = B |
| 3 | Open the Course B Class Member. | Class B starts 2026-08-12 and ends 2026-12-31 with linkage to the Course B LA. | expected Class Member = 2026-08-12 to 2026-12-31 |
| 4 | Open Back Office and view Student A's Course B class information. | The synced Class B membership is visible in Back Office with the same effective dates. | expected BO Class B = 2026-08-12 to 2026-12-31 |

**Severity:** major
**Priority:** high

---

### [Withus Juku] Class Member – Add New Course – Schedule product – Class Member synced to Back Office

**Description:** AC-01 — Regression — Adding a Schedule associated course creates the Class Member and syncs it to Back Office without lesson auto-assignment checks.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled; Student A has an active Schedule product for Course A.
- Course B requires allocation; Class B belongs to Course B; `today = 2026-08-12`; `effective_date = 2026-08-20`; `LA_end_date = 2026-12-31`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Start an update order for Student A's existing Schedule product. | The update-order form opens. | product_type = Schedule; today = 2026-08-12 |
| 2 | Add Course B, select Class B, enter 2026-08-20 as the effective date, and submit the update order. | The Course B LA is created with the selected effective date. | effective_date = 2026-08-20; class = B |
| 3 | Open the Course B Class Member. | Class B starts 2026-08-20 and ends 2026-12-31 with linkage to the Course B LA. | expected Class Member = 2026-08-20 to 2026-12-31 |
| 4 | Open Back Office and view Student A's Course B class information. | The synced Class B membership is visible in Back Office with the same effective dates. | expected BO Class B = 2026-08-20 to 2026-12-31 |

**Severity:** major
**Priority:** high

---

### [Withus Juku] Class Member – Add New Course – Frequency product – Class Member synced to Back Office

**Description:** AC-01 — Regression — Adding a Frequency associated course creates the Class Member and syncs it to Back Office without lesson auto-assignment checks.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled; Student A has an active Frequency product for Course A.
- Course B requires allocation; Class B belongs to Course B; `today = 2026-08-12`; `effective_date = 2026-08-20`; `LA_end_date = 2026-12-31`; `selected_slots = 12`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Start an update order for Student A's existing Frequency product. | The update-order form opens. | product_type = Frequency; today = 2026-08-12 |
| 2 | Add Course B, select Class B, enter 2026-08-20 as the effective date, retain 12 slots, and submit the update order. | The Course B LA is created with the selected effective date. | effective_date = 2026-08-20; slots = 12; class = B |
| 3 | Open the Course B Class Member. | Class B starts 2026-08-20 and ends 2026-12-31 with linkage to the Course B LA. | expected Class Member = 2026-08-20 to 2026-12-31 |
| 4 | Open Back Office and view Student A's Course B class information. | The synced Class B membership is visible in Back Office with the same effective dates. | expected BO Class B = 2026-08-20 to 2026-12-31 |

**Severity:** major
**Priority:** high

---

### [Withus Juku] Class Member – Order Group Class – Date Before LA Start – Exact validation message shown

**Description:** AC-01 — Negative and Component — A staff-entered Order Group Class date below LA start is blocked with the required error text.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled.
- Student A has a Course A LA from 2026-08-01 through 2026-12-31; Class A belongs to Course A.
- `today = 2026-08-12`; `LA_start_date = 2026-08-01`; `target_date = 2026-07-31`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Student A's Create Order > Order Group Class flow and select Course A and Class A. | The Class Member effective-date input is available to staff. | today = 2026-08-12; setting = enabled |
| 2 | Enter 2026-07-31 as the Class Member effective date. | The effective-date input shows `Effective date must be from LA start date onwards`. | target_date = 2026-07-31 = LA start minus 1 day |
| 3 | Attempt to continue the flow and open Student A's Class Member history. | The invalid date is blocked and no Class Member history is added or changed. | expected Class Member additions = 0 |

**Severity:** major
**Priority:** high

---

### [Withus Juku] Class Member – Order Group Class – Setting Disabled – Existing current-date lower bound retained

**Description:** AC-01 — Decision Table and Regression — Disabling the Withus setting does not allow an LA-start date that is before today.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = disabled.
- Student A has a Course A LA from 2026-08-01 through 2026-12-31; Class A belongs to Course A.
- `today = 2026-08-12`; `target_date = 2026-08-01`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Student A's Create Order > Order Group Class flow and select Course A and Class A. | The Class Member effective-date input is available to staff. | today = 2026-08-12; setting = disabled |
| 2 | Enter 2026-08-01 as the Class Member effective date and attempt to continue. | The flow does not accept the past date under the existing setting-disabled current-date rule. | target_date = 2026-08-01; target_date < today |
| 3 | Open Student A's Class Member history. | No Class Member is added from the blocked date. | expected Class Member additions = 0 |

**Severity:** major
**Priority:** high

---

### [Withus Juku] Class Member – Order Group Class – Core tenant – Existing past-date baseline retained

**Description:** AC-01 — Regression — The Withus-only setting does not change the existing Core baseline represented by PX-10451 and PX-10454.

**Preconditions:**

- Logged in as HQ or CM Staff to a Core Salesforce org.
- Student A has a Course A LA from 2026-08-01 through 2026-12-31; Class A belongs to Course A.
- `today = 2026-08-12`; `target_date = 2026-08-01`; no Withus custom setting is enabled in Core.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Execute the existing class-selected Core Order Group scenario represented by PX-10451 or PX-10454 with a past product start. | The order flow follows the existing Core behaviour. | today = 2026-08-12; product start = 2026-08-01 |
| 2 | Open the created Core Class Member. | The Class Member start date follows the existing Core current-date baseline and is not changed to the LA start date by the Withus setting. | expected Core start = 2026-08-12; Withus setting = not applicable |

**Severity:** major
**Priority:** high
