# Test Cases: LT-107664 — Koyu Lesson Quiz and Total Score

## Suite: [Koyu] Score Validation and Localization

### [Koyu] Lesson Report – Total Score – Blank value – Save accepted

**Description:** AC 2.1.1 — Equivalence Partitioning — An optional Total Score accepts an empty value.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- The SF Lesson Custom Setting is `ON`.
- Student A's Lesson Report Detail has Total Score `10.0`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff clears Total Score and saves Student A's Lesson Report. | The save completes and Total Score remains blank. | total_score = blank |
| 2 | HQ or CM Staff reopens Student A's Lesson Report. | Total Score is blank and Test Result remains unchanged. | expected_total_score = blank |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – Test Result – Blank value – Save accepted

**Description:** AC 2.1.1 — Equivalence Partitioning — An optional Test Result accepts an empty value.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- The BO internal score setting is `ON`.
- Student A's Lesson Report Detail has Test Result `8.0`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff clears Test Result and saves Student A's Lesson Report. | The save completes and Test Result remains blank. | test_result = blank |
| 2 | HQ or CM Staff reopens Student A's Lesson Report. | Test Result is blank and Total Score remains unchanged. | expected_test_result = blank |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – Total Score – Negative one-decimal value – Save accepted

**Description:** AC 2.1.1 — Equivalence Partitioning — Total Score accepts a negative value with one decimal place.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- The SF Lesson Custom Setting is `ON`.
- Student A's Lesson Report Detail is editable.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `-12.5` in Total Score and saves the report. | The save completes and Total Score displays `-12.5`. | total_score = -12.5 |

**Severity:** major
**Priority:** high

---

### [Koyu] Lesson Report – Test Result – Negative one-decimal value – Save accepted

**Description:** AC 2.1.1 — Equivalence Partitioning — Test Result accepts a negative value with one decimal place.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- The BO internal score setting is `ON`.
- Student A's Lesson Report Detail is editable.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `-8.5` in Test Result and saves the report. | The save completes and Test Result displays `-8.5`. | test_result = -8.5 |

**Severity:** major
**Priority:** high

---

### [Koyu] Lesson Report – Total Score – Zero – Save accepted

**Description:** AC 2.1.1 — Boundary Value Analysis — Total Score accepts zero as a valid numeric value.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- The SF Lesson Custom Setting is `ON`.
- Student A's Lesson Report Detail is editable.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `0` in Total Score and saves the report. | The save completes and Total Score displays `0`. | total_score = 0 |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – Test Result – Zero – Save accepted

**Description:** AC 2.1.1 — Boundary Value Analysis — Test Result accepts zero as a valid numeric value.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- The BO internal score setting is `ON`.
- Student A's Lesson Report Detail is editable.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `0` in Test Result and saves the report. | The save completes and Test Result displays `0`. | test_result = 0 |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – Total Score – Two decimal places – English validation displayed

**Description:** AC 2.1.1 — Boundary Value Analysis / Negative — Total Score rejects a value with more than one decimal place in English.

**Preconditions:**

- HQ or CM Staff is logged in to the English Koyu Salesforce organization.
- The SF Lesson Custom Setting is `ON`.
- Student A's stored Total Score is `10.0`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `10.25` in Total Score and saves the report. | Save is blocked and the message `Only single-digit decimal numbers are allowed.` displays. | total_score = 10.25; locale = EN |
| 2 | HQ or CM Staff reopens Student A's Lesson Report. | Total Score remains `10.0`. | expected_total_score = 10.0 |

**Severity:** critical
**Priority:** high

---

### [Koyu] Lesson Report – Test Result – Two decimal places – Japanese validation displayed

**Description:** AC 2.1.1 — Boundary Value Analysis / Negative — Test Result rejects a value with more than one decimal place in Japanese.

**Preconditions:**

- HQ or CM Staff is logged in to the Japanese Koyu Back Office.
- The BO internal score setting is `ON`.
- Student A's stored Test Result is `8.0`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `8.25` in Test Result and saves the report. | Save is blocked and the message `1桁の少数までの数値のみ使用できます` displays. | test_result = 8.25; locale = JP |
| 2 | HQ or CM Staff reopens Student A's Lesson Report. | Test Result remains `8.0`. | expected_test_result = 8.0 |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – Total Score – Alphabetic value – Save blocked

**Description:** AC 2.1.1 — Equivalence Partitioning / Negative — Total Score rejects non-numeric text.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- The SF Lesson Custom Setting is `ON`.
- Student A's stored Total Score is `10.0`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `abc` in Total Score and saves the report. | Save is blocked with the active-locale numeric validation message. | total_score = abc |
| 2 | HQ or CM Staff reopens Student A's Lesson Report. | Total Score remains `10.0`. | expected_total_score = 10.0 |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – Test Result – Repeated sign – Save blocked

**Description:** AC 2.1.1 — Equivalence Partitioning / Negative — Test Result rejects malformed signed input.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- The BO internal score setting is `ON`.
- Student A's stored Test Result is `8.0`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `--8.5` in Test Result and saves the report. | Save is blocked with the active-locale numeric validation message. | test_result = --8.5 |
| 2 | HQ or CM Staff reopens Student A's Lesson Report. | Test Result remains `8.0`. | expected_test_result = 8.0 |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – Total Score – Maximum one-decimal precision – Save accepted

**Description:** AC 2.1.1 — Boundary Value Analysis — Total Score accepts the maximum stored precision of fifteen integer digits and one decimal place.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- The SF Lesson Custom Setting is `ON`.
- Student A's Lesson Report Detail is editable.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `999999999999999.9` in Total Score and saves the report. | The save completes and Total Score retains `999999999999999.9`. | total_score = 999999999999999.9 |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – Test Result – Value beyond stored precision – Save blocked

**Description:** AC 2.1.1 — Boundary Value Analysis / Negative — Test Result rejects a value beyond the configured numeric precision.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- The BO internal score setting is `ON`.
- Student A's stored Test Result is `8.0`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `1000000000000000.0` in Test Result and saves the report. | Save is blocked with a numeric validation message and Test Result is not changed. | test_result = 1000000000000000.0 |
| 2 | HQ or CM Staff reopens Student A's Lesson Report. | Test Result remains `8.0`. | expected_test_result = 8.0 |

**Severity:** critical
**Priority:** high
