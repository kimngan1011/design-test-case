# Test Cases: LT-107664 — Koyu Lesson Quiz and Total Score

## Suite: [Koyu] Per-student Score Detail and Synchronization

### [Koyu] Lesson Report – Total Score – SF save – BO value synchronized

**Description:** AC 2.1.1 — CRUD / Regression — A Total Score saved in SF is read unchanged in Back Office.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- HQ or CM Staff is logged in to the Koyu Back Office.
- The SF Lesson Custom Setting is `ON`.
- The BO internal score setting is `ON`.
- Student A's Total Score is blank.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `-10.5` in Student A's Total Score in Salesforce and saves the report. | Salesforce displays Total Score `-10.5`. | total_score = -10.5; source = SF |
| 2 | HQ or CM Staff opens Student A's same Lesson Report in Back Office. | Back Office displays Total Score `-10.5`. | expected_total_score = -10.5 |

**Severity:** critical
**Priority:** high

---

### [Koyu] Lesson Report – Test Result – BO save – SF value synchronized

**Description:** AC 2.1.1 — CRUD / Regression — A Test Result saved in BO is read unchanged in Salesforce.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- The SF Lesson Custom Setting is `ON`.
- The BO internal score setting is `ON`.
- Student A's Test Result is blank.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `8.5` in Student A's Test Result in Back Office and saves the report. | Back Office displays Test Result `8.5`. | test_result = 8.5; source = BO |
| 2 | HQ or CM Staff opens Student A's same Lesson Report in Salesforce. | Salesforce displays Test Result `8.5`. | expected_test_result = 8.5 |

**Severity:** critical
**Priority:** high

---

### [Koyu] Lesson Report – Score details – Two students – Values remain isolated

**Description:** AC 2.1.1 — Decision Table / Data Integrity — Each student's score detail remains independent in a group lesson.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- The SF Lesson Custom Setting is `ON`.
- A group lesson has Student A and Student B.
- Student A's Total Score and Test Result are blank.
- Student B's Total Score is `100.0`.
- Student B's Test Result is `92.5`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters Total Score `-10.5` and Test Result `8.5` for Student A and saves the report. | Student A's detail displays `-10.5` and `8.5`. | student = A; total_score = -10.5; test_result = 8.5 |
| 2 | HQ or CM Staff opens Student B's detail in the same lesson. | Student B retains Total Score `100.0` and Test Result `92.5`. | student = B; expected_total_score = 100.0; expected_test_result = 92.5 |

**Severity:** critical
**Priority:** high

---

### [Koyu] Lesson Report – Test Result – Single-field update – Other scores retained

**Description:** AC 2.1.1 — CRUD / Regression — Updating Test Result does not change Total Score or inactive Lesson Quiz data.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- The BO internal score setting is `ON`.
- Student A's Lesson Quiz is `80%`.
- Student A's Total Score is `10.0`.
- Student A's Test Result is `8.0`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff changes Student A's Test Result to `9.5` and saves the report. | Test Result displays `9.5`. | test_result = 9.5 |
| 2 | HQ or CM Staff reopens Student A's detail. | Total Score remains `10.0` and the stored Lesson Quiz value remains `80%`. | expected_total_score = 10.0; expected_lesson_quiz = 80% |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Learner App – Student score detail – Published report – SF-originated values displayed

**Description:** AC 2.1.1 / AC 2.1.2 — State Transition / Component — A student sees exact SF-originated values after normal report publication.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- Student A is logged in to the Koyu Learner App.
- The SF Lesson Custom Setting is `ON`.
- The App internal score setting is `ON`.
- Student A's lesson and Lesson Report are published.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff saves Total Score `-20.5` and Test Result `15.0` for Student A in Salesforce. | Salesforce stores the two values. | total_score = -20.5; test_result = 15.0; source = SF |
| 2 | Student A opens the published Lesson Report in the Learner App. | Total Score displays `-20.5` and Test Result displays `15.0`; Lesson Quiz is absent and neither score is editable. | expected_total_score = -20.5; expected_test_result = 15.0 |

**Severity:** critical
**Priority:** high

---

### [Koyu] Learner App – Parent score detail – Published report – BO-originated values displayed

**Description:** AC 2.1.1 / AC 2.1.2 — State Transition / Permission Matrix — A parent sees exact BO-originated values for the selected child.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- Parent A is logged in to the Koyu Learner App and selects Student A.
- The BO internal score setting is `ON`.
- Student A's lesson and Lesson Report are published.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff saves Total Score `50.0` and Test Result `48.5` for Student A in Back Office. | Back Office stores the two values. | total_score = 50.0; test_result = 48.5; source = BO |
| 2 | Parent A opens Student A's published Lesson Report in the Learner App. | Total Score displays `50.0` and Test Result displays `48.5`; neither score is editable. | expected_total_score = 50.0; expected_test_result = 48.5 |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Learner App – Score detail – Report not published – Values not exposed

**Description:** AC 2.1.2 — State Transition / Negative — New score values do not bypass the existing published-report visibility condition.

**Preconditions:**

- Student A is logged in to the Koyu Learner App.
- The App internal score setting is `ON`.
- Student A's Lesson Report Detail has Total Score `50.0` and Test Result `48.5`.
- Student A's Lesson Report is Draft.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student A opens the lesson in the Learner App. | The unpublished Lesson Report score detail is not exposed to Student A. | report_status = Draft |

**Severity:** major
**Priority:** high

---

### [Koyu] Lesson Report – Invalid Total Score – Existing cross-surface values retained

**Description:** AC 2.1.1 — Negative / Data Integrity — A blocked Total Score save does not overwrite the prior synchronized values.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- HQ or CM Staff is logged in to the Koyu Back Office.
- The SF Lesson Custom Setting is `ON`.
- The BO internal score setting is `ON`.
- Student A's Total Score is `10.0` in both staff surfaces.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `10.25` in Student A's Total Score in Salesforce and saves the report. | Save is blocked with the active-locale validation message. | total_score = 10.25 |
| 2 | HQ or CM Staff opens Student A's Lesson Report in Back Office. | Total Score remains `10.0`. | expected_total_score = 10.0 |

**Severity:** critical
**Priority:** high

---

### [Koyu] Lesson Report – Score detail – SF update after BO view – Refreshed value displayed

**Description:** AC 2.1.1 — Regression — Back Office does not retain a stale score after an SF update and refresh.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- HQ or CM Staff opens Student A's Lesson Report in the Koyu Back Office.
- The SF Lesson Custom Setting is `ON`.
- The BO internal score setting is `ON`.
- Student A's Total Score is `10.0`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff changes Student A's Total Score to `11.0` in Salesforce and saves the report. | Salesforce displays Total Score `11.0`. | total_score = 11.0; source = SF |
| 2 | HQ or CM Staff refreshes Student A's open Lesson Report in Back Office. | Back Office displays Total Score `11.0` rather than the earlier `10.0` value. | expected_total_score = 11.0 |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – Independent scores – Total Score changed – Test Result not calculated

**Description:** Scope — Decision Table / Negative — Changing Total Score does not calculate or replace Test Result.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- The SF Lesson Custom Setting is `ON`.
- Student A's Total Score is `100.0`.
- Student A's Test Result is `75.5`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff changes Student A's Total Score to `50.0` and saves the report. | Total Score displays `50.0`. | total_score = 50.0 |
| 2 | HQ or CM Staff reads Student A's Test Result. | Test Result remains `75.5` and no percentage or other calculated value appears. | expected_test_result = 75.5 |

**Severity:** minor
**Priority:** medium
