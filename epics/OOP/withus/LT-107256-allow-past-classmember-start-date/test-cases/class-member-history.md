# Test Cases: LT-107256 — Withus Class Member Past Start Date

## Suite: Class Member History

### [Withus Juku] Class Member – History – Same effective date as active class – Latest class becomes active

**Description:** AC-01 — State Transition — Assigning a new class on the current active start date replaces the active class using the latest-created class.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled.
- Student A has Course A LA from 2026-07-01 through 2026-12-31 and active Class A from 2026-07-01 through 2026-12-31; Class B belongs to Course A.
- `today = 2026-07-27`; `target_date = 2026-07-01`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Student A's Contact > Course record and select **Assign Class** for Course A. | The assignment form opens. | today = 2026-07-27; LA = 2026-07-01 to 2026-12-31; active Class A start = 2026-07-01 |
| 2 | Select Class B, enter 2026-07-01, and save. | The assignment is accepted because the date equals LA start and the existing active Class A start. | target_date = existing active Class A start = LA start = 2026-07-01 |
| 3 | Open Student A's Class Member history. | Class A is deleted; Class B is the active Class Member from 2026-07-01 through 2026-12-31. | expected active class = B; Class B = 2026-07-01 to 2026-12-31; Class A count = 0 |

**Severity:** critical
**Priority:** high

---

### [Withus Juku] Class Member – History – New date before past and active classes – Classes B and C removed

**Description:** AC-01 — State Transition — The exact Jira matrix scenario updates Class A's end date, adds Class D, and removes later Classes B and C.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled.
- Student A has Course A LA from 2026-06-01 through 2026-12-31; existing Class A effective date is 2026-06-01, Class B effective date is 2026-07-01, and Class C effective date is 2026-07-26.
- `today = 2026-07-27`; `target_date = 2026-06-30`; `old_class_A_end_date = 2026-06-29`; Class D belongs to Course A.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Student A's Contact > Course record and select **Assign Class** for Course A. | The assignment form opens. | today = 2026-07-27; LA = 2026-06-01 to 2026-12-31; setting = enabled |
| 2 | Select Class D, enter 2026-06-30 as the effective date, and save. | The assignment is accepted according to the Withus historical Class Member matrix scenario. | target_date = 2026-06-30; Class D |
| 3 | Open Student A's Class Member history. | Class A effective end date is 2026-06-29; Class D effective date is 2026-06-30; Classes B and C are removed. | Class A end = 2026-06-29; Class D effective date = 2026-06-30; Class B count = 0; Class C count = 0 |

**Severity:** critical
**Priority:** high

---

### [Withus Juku] Class Member – History – Later effective date – Old active class ends the prior day

**Description:** AC-01 — State Transition — Assigning a later class date updates the old active class effective end date to one day before the new class starts.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled.
- Student A has Course A LA from 2026-07-01 through 2026-12-31 and active Class A from 2026-07-01 through 2026-12-31; Class B belongs to Course A.
- `today = 2026-07-27`; `target_date = 2026-07-02`; `old_class_end_date = 2026-07-01`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Student A's Contact > Course record and select **Assign Class** for Course A. | The assignment form opens. | today = 2026-07-27; LA = 2026-07-01 to 2026-12-31; active Class A start = 2026-07-01 |
| 2 | Select Class B, enter 2026-07-02, and save. | The assignment is accepted. | target_date = 2026-07-02 |
| 3 | Open Student A's Class Member history. | Class A ends on 2026-07-01 and Class B is active from 2026-07-02 through 2026-12-31. | Class A end = 2026-07-01; Class B = 2026-07-02 to 2026-12-31 |

**Severity:** critical
**Priority:** high

---

### [Withus Juku] Class Member – History – New active class before scheduled class – Scheduled class removed

**Description:** AC-01 — State Transition — Assigning a new active class before a scheduled class updates the active history and removes the scheduled class.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled.
- Student A has Course A LA from 2026-07-01 through 2026-12-31, active Class A from 2026-07-01 through 2026-08-14, and scheduled Class B from 2026-08-15 through 2026-12-31; Class C belongs to Course A.
- `today = 2026-07-27`; `target_date = 2026-07-20`; `old_class_end_date = 2026-07-19`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Student A's Contact > Course record and select **Assign Class** for Course A. | The assignment form opens. | today = 2026-07-27; LA = 2026-07-01 to 2026-12-31; scheduled Class B start = 2026-08-15 |
| 2 | Select Class C, enter 2026-07-20, and save. | The assignment is accepted. | target_date = 2026-07-20; target_date < scheduled Class B start = 2026-08-15 |
| 3 | Open Student A's Class Member history. | Class A ends on 2026-07-19, Class C is active from 2026-07-20 through 2026-12-31, and scheduled Class B is removed. | Class A end = 2026-07-19; Class C = 2026-07-20 to 2026-12-31; Class B count = 0 |

**Severity:** critical
**Priority:** high

---

### [Withus Juku] Class Member – History – New class after scheduled class – Scheduled class retained

**Description:** AC-01 — State Transition — An LA can have sequential scheduled classes. When a new class is assigned, the previous class ends one day before the new class starts.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org.
- `Allow Class Member Start In The Past` = enabled.
- Student A has Course A LA from 2026-08-01 through 2026-12-31, active Class A from 2026-08-01 through 2026-08-20, and scheduled Class B from 2026-08-21 through 2026-12-31; Class C belongs to Course A.
- `today = 2026-08-12`; `target_date = 2026-08-25`; `old_class_end_date = 2026-08-24`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Student A's Contact > Course record and select **Assign Class** for Course A. | The assignment form opens. | today = 2026-08-12; scheduled Class B start = 2026-08-21 |
| 2 | Select Class C, enter 2026-08-25, and save. | The assignment is accepted. | target_date = 2026-08-25; target_date > scheduled Class B start = 2026-08-21 |
| 3 | Open Student A's Class Member history. | Class A remains the prior active membership ending 2026-08-20; Class B is a scheduled membership from 2026-08-21 through 2026-08-24; Class C is scheduled from 2026-08-25 through 2026-12-31. | Class A end = 2026-08-20; Class B = 2026-08-21 to 2026-08-24; Class C = 2026-08-25 to 2026-12-31 |

**Severity:** critical
**Priority:** high
