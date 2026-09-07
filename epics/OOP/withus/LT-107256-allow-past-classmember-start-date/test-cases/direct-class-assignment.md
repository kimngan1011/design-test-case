# Test Cases: LT-107256 — Withus Class Member Past Start Date

## Suite: Direct Class Assignment

### [Withus Juku] Class Member – Contact Course Assignment – LA Start Date – Past effective date accepted

**Description:** AC-01 — Boundary Value Analysis — A staff member can assign a class using the exact LA start date when the Withus setting is enabled.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled.
- Student A has Course A LA from 2026-08-01 through 2026-12-31; Class A belongs to Course A.
- `today = 2026-08-12`; `target_date = 2026-08-01`; current time = 2026-08-12 00:30 JST (= 2026-08-11 15:30 UTC).

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Student A's Contact > Course record and select **Assign Class** for Course A. | The assignment form opens with an effective-date input. | today = 2026-08-12; LA start = 2026-08-01; setting = enabled |
| 2 | Select Class A and enter 2026-08-01 as the effective date. | The form accepts 2026-08-01 without the lower-bound error. | target_date = LA start = 2026-08-01 |
| 3 | Save the assignment and open the created Class Member. | One Class A member is created for Student A with effective start date 2026-08-01 and linkage to the Course A LA. | expected start = 2026-08-01; JST timestamp = 2026-08-12 00:30; UTC timestamp = 2026-08-11 15:30 |
| 4 | Open Back Office and view Student A's Course A class information. | The synced Class A membership is visible in Back Office with effective start date 2026-08-01. | expected BO class = Class A; expected BO effective start = 2026-08-01 |

**Severity:** major
**Priority:** high

---

### [Withus Juku] Class Member – Contact Course Assignment – Date Before LA Start – Exact validation message shown

**Description:** AC-01 — Boundary Value Analysis and Component — A date one day before LA start is blocked and the form shows the required error text.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled.
- Student A has Course A LA from 2026-08-01 through 2026-12-31; Class A belongs to Course A; no pending Class A assignment exists.
- `today = 2026-08-12`; `LA_start_date = 2026-08-01`; `target_date = 2026-07-31`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Student A's Contact > Course record and select **Assign Class** for Course A. | The form shows the Class and effective-date inputs. | today = 2026-08-12; LA start = 2026-08-01; setting = enabled |
| 2 | Select Class A and enter 2026-07-31 as the effective date. | The effective-date input remains visible and shows `Effective date must be from LA start date onwards`. | target_date = 2026-07-31 = LA start minus 1 day |
| 3 | Attempt to save the assignment and reopen Class Member history. | Saving is blocked; no Class Member is created and the existing Class Member history is unchanged. | expected Class Member additions = 0 |

**Severity:** major
**Priority:** high

---

### [Withus Juku] Class Member – Bulk Assign Class – Multiple LAs for one student – Each LA assigned

**Description:** AC-01 — Decision Table — Bulk assignment accepts the LA start date for each selected LA belonging to one student.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled.
- Student A has two Course A LAs: LA 1 from 2026-08-01 through 2026-09-30 and LA 2 from 2026-08-01 through 2026-12-31; Class A belongs to Course A.
- `today = 2026-08-12`; `target_date = 2026-08-01`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Student A's Contact > Course record and select the two Course A LAs for **Bulk Assign Class**. | The bulk-assignment form opens for the two selected LAs of Student A. | student = A; selected LAs = LA 1, LA 2; today = 2026-08-12 |
| 2 | Select Class A and enter 2026-08-01 as the effective date. | The form accepts the shared date without the lower-bound error. | target_date = LA start = 2026-08-01 |
| 3 | Save the bulk assignment and open Student A's Class Member history. | Student A has one Class A member for LA 1 and one Class A member for LA 2; both start 2026-08-01 and retain their respective LA linkage and end date. | expected members = 2; LA 1 = 2026-08-01 to 2026-09-30; LA 2 = 2026-08-01 to 2026-12-31 |
| 4 | Open Back Office and view Student A's Course A class information. | Both synced Class A memberships are visible in Back Office with their respective LA end dates. | expected BO memberships = 2; LA 1 end = 2026-09-30; LA 2 end = 2026-12-31 |

**Severity:** major
**Priority:** high

---

### [Withus Juku] Class Member – Bulk Assign Class – Multiple LAs for one student below boundary – Exact validation message shown

**Description:** AC-01 — Negative and Component — Bulk assignment blocks a date below the shared LA start boundary for the selected LAs and shows the required error.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled.
- Student A has two Course A LAs: LA 1 from 2026-08-01 through 2026-09-30 and LA 2 from 2026-08-01 through 2026-12-31; Class A belongs to Course A.
- `today = 2026-08-12`; `LA_start_date = 2026-08-01`; `target_date = 2026-07-31`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Student A's Contact > Course record and select the two Course A LAs for **Bulk Assign Class**. | The bulk-assignment form opens for the two selected LAs of Student A. | student = A; selected LAs = LA 1, LA 2; today = 2026-08-12 |
| 2 | Select Class A and enter 2026-07-31 as the effective date. | The effective-date input shows `Effective date must be from LA start date onwards`. | target_date = 2026-07-31 = LA start minus 1 day |
| 3 | Attempt to save and open Student A's Class Member history. | Saving is blocked; neither selected LA receives a new Class Member and Student A's history is unchanged. | expected Class Member additions = 0 for LA 1 and LA 2 |

**Severity:** major
**Priority:** high

---

### [Withus Juku] Class Member – Location Course Student Assignment – Later past date – Class Member created

**Description:** AC-01 — Equivalence Partitioning — Location Course assignment accepts a past date after LA start.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled.
- Student A has Course A LA from 2026-08-01 through 2026-12-31 at Location 1; Class A belongs to Course A at Location 1.
- `today = 2026-08-12`; `LA_start_date = 2026-08-01`; `target_date = 2026-08-05`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Location 1 > Course A > Student A and select **Assign Class**. | The Location Course assignment form opens with an effective-date input. | today = 2026-08-12; setting = enabled |
| 2 | Select Class A and enter 2026-08-05 as the effective date. | The form accepts the later past date without the lower-bound error. | target_date = 2026-08-05; target_date > LA start |
| 3 | Save and open Student A's Class Member history. | One Class A member starts 2026-08-05 and is linked to the Course A LA. | expected start = 2026-08-05 |
| 4 | Open Back Office and view Student A's Course A class information. | The synced Class A membership is visible in Back Office with effective start date 2026-08-05. | expected BO class = Class A; expected BO effective start = 2026-08-05 |

**Severity:** major
**Priority:** high

---

### [Withus Juku] Class Member – Location Course Student Assignment – Date Before LA Start – Exact validation message shown

**Description:** AC-01 — Negative and Component — Location Course assignment blocks a date below LA start and shows the exact required error.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled.
- Student A has Course A LA from 2026-08-01 through 2026-12-31 at Location 1; Class A belongs to Course A at Location 1.
- `today = 2026-08-12`; `LA_start_date = 2026-08-01`; `target_date = 2026-07-31`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Location 1 > Course A > Student A and select **Assign Class**. | The Location Course assignment form opens with an effective-date input. | today = 2026-08-12; setting = enabled |
| 2 | Select Class A and enter 2026-07-31 as the effective date. | The effective-date input shows `Effective date must be from LA start date onwards`. | target_date = 2026-07-31 = LA start minus 1 day |
| 3 | Attempt to save and open Student A's Class Member history. | Saving is blocked and Class Member history is unchanged. | expected Class Member additions = 0 |

**Severity:** major
**Priority:** high

---

### [Withus Juku] Class Member – LA Student Session Assignment – LA Start Date – Past effective date accepted

**Description:** AC-01 — Boundary Value Analysis — The Learning Area Student Session Assign Class flow accepts an effective date equal to the LA start date when the Withus setting is enabled.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled.
- Student A has Course A LA from 2026-08-01 through 2026-12-31; Class A belongs to Course A; no Class A assignment exists.
- `today = 2026-08-12`; `target_date = 2026-08-01`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Course A LA > Student Session for Student A and select **Assign Class**. | The assignment form opens with Class and effective-date inputs. | today = 2026-08-12; setting = enabled |
| 2 | Select Class A and enter 2026-08-01 as the effective date. | The form accepts 2026-08-01 without the lower-bound error. | target_date = LA start = 2026-08-01 |
| 3 | Save the assignment and open Student A's Class Member history. | One Class A member starts 2026-08-01 and is linked to Course A LA. | expected Class Member start = 2026-08-01 |
| 4 | Open Back Office and view Student A's Course A class information. | The synced Class A membership is visible in Back Office with effective start date 2026-08-01. | expected BO class = Class A; expected BO effective start = 2026-08-01 |

**Severity:** major
**Priority:** high

---

### [Withus Juku] Class Member – LA Student Session Assignment – Date Before LA Start – Exact validation message shown

**Description:** AC-01 — Negative and Component — The LA Student Session flow blocks a date below the LA boundary and renders the exact error.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled.
- Student A has Course A LA from 2026-08-01 through 2026-12-31; Class A belongs to Course A.
- `today = 2026-08-12`; `LA_start_date = 2026-08-01`; `target_date = 2026-07-31`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Course A LA > Student Session for Student A and select **Assign Class**. | The assignment form shows Class and effective-date inputs. | today = 2026-08-12; setting = enabled |
| 2 | Select Class A and enter 2026-07-31 as the effective date. | The effective-date input shows `Effective date must be from LA start date onwards`. | target_date = 2026-07-31 = LA start minus 1 day |
| 3 | Attempt to save and open Student A's Class Member history. | Saving is blocked and no Class Member history is added or changed. | expected Class Member additions = 0 |

**Severity:** major
**Priority:** high

---

### [Withus Juku] Class Member – Assign Class Permission – BO Teacher – Existing access restriction retained

**Description:** AC-01 — Permission Matrix — The tenant-specific logic does not give a BO teacher class-assignment permission.

**Preconditions:**

- Logged in as a BO Teacher in the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled.
- Student A has Course A LA from 2026-08-01 through 2026-12-31.
- `today = 2026-08-12`; `target_date = 2026-08-01`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Student A's Contact > Course record. | The Course A record is visible according to the teacher's existing access. | today = 2026-08-12; role = BO Teacher |
| 2 | Inspect the available actions for Course A. | **Assign Class** is unavailable to the BO Teacher. | setting = enabled; target_date = 2026-08-01 |

**Severity:** minor
**Priority:** medium
