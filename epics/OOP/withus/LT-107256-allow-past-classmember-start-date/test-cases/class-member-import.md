# Test Cases: LT-107256 — Withus Class Member Past Start Date

## Suite: Class Member Import

### [Withus Juku] Class Member – Import – LA Start Date – Historical Class Member created

**Description:** AC-01 — Boundary Value Analysis — Import accepts a Class Member date equal to LA start when the Withus setting is enabled.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org with Class Member import access.
- `Allow Class Member Start In The Past` = enabled.
- Student A has Course A LA from 2026-08-01 through 2026-12-31; Class A belongs to Course A; no matching Class Member exists.
- `today = 2026-08-12`; `target_date = 2026-08-01`; import file contains one Class A row for Student A.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open **Import Class Member** and upload the prepared file. | The import preview shows the Student A, Class A, and 2026-08-01 row. | today = 2026-08-12; import rows = 1 |
| 2 | Start the import. | The row completes without the lower-bound error. | target_date = LA start = 2026-08-01 |
| 3 | Open Student A's Class Member history. | One Class A member starts 2026-08-01 and is linked to the Course A LA. | expected start = 2026-08-01 |
| 4 | Open Back Office and view Student A's Course A class information. | The synced Class A membership is visible in Back Office with effective start date 2026-08-01. | expected BO class = Class A; expected BO effective start = 2026-08-01 |

**Severity:** major
**Priority:** high

---

### [Withus Juku] Class Member – Import – Date Before LA Start – Exact validation message shown

**Description:** AC-01 — Negative and Component — Import shows the specified error for an effective date below LA start and does not mutate Class Member history.

**Preconditions:**

- Logged in as HQ or CM Staff to the Withus Juku Salesforce org with Class Member import access.
- `Allow Class Member Start In The Past` = enabled.
- Student A has Course A LA from 2026-08-01 through 2026-12-31; Class A belongs to Course A; no matching Class Member exists.
- `today = 2026-08-12`; `LA_start_date = 2026-08-01`; `target_date = 2026-07-31`; import file contains one Class A row for Student A.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open **Import Class Member** and upload the prepared file. | The import preview shows the submitted row and its effective date. | today = 2026-08-12; import rows = 1 |
| 2 | Start the import. | The invalid row shows `Effective date must be from LA start date onwards`. | target_date = 2026-07-31 = LA start minus 1 day |
| 3 | Open Student A's Class Member history. | No Class Member is created and the existing history is unchanged. | expected Class Member additions = 0 |

**Severity:** major
**Priority:** high
