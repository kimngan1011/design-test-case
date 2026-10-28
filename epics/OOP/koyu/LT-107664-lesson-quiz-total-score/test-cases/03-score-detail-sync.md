# Test Cases: LT-107664 — Koyu Lesson Quiz and Total Score

## Suite: [Koyu] Per-student Score Detail and Synchronization

### [Koyu] Lesson Report – SF Report under Lesson to BO Report under Lesson – Total Score synchronized

**Description:** AC 2.1.1 — CRUD / Regression — A Total Score saved in the Salesforce Report under Lesson screen is read unchanged in the Back Office Report under Lesson screen.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- HQ or CM Staff is logged in to the Koyu Back Office.
- The SF Lesson Custom Setting is `ON`.
- The BO internal score setting is `ON`.
- Student A's Total Score is blank.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `-10.5` in Student A's Total Score in Salesforce Report under Lesson and saves the report. | Salesforce Report under Lesson displays Total Score `-10.5`. | total_score = -10.5; source_screen = SF Report under Lesson |
| 2 | HQ or CM Staff opens Student A's same report in Back Office Report under Lesson. | Back Office Report under Lesson displays Total Score `-10.5`. | target_screen = BO Report under Lesson; expected_total_score = -10.5 |

**Severity:** critical
**Priority:** high

---

### [Koyu] Lesson Report – BO Report under Lesson to SF Report under Lesson – Test Result synchronized

**Description:** AC 2.1.1 — CRUD / Regression — A Test Result saved in the Back Office Report under Lesson screen is read unchanged in the Salesforce Report under Lesson screen.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- The SF Lesson Custom Setting is `ON`.
- The BO internal score setting is `ON`.
- Student A's Test Result is blank.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `8.5` in Student A's Test Result in Back Office Report under Lesson and saves the report. | Back Office Report under Lesson displays Test Result `8.5`. | test_result = 8.5; source_screen = BO Report under Lesson |
| 2 | HQ or CM Staff opens Student A's same report in Salesforce Report under Lesson. | Salesforce Report under Lesson displays Test Result `8.5`. | target_screen = SF Report under Lesson; expected_test_result = 8.5 |

**Severity:** critical
**Priority:** high

---

### [Koyu] Lesson Report – SF Lesson Report Detail – Two students – Values remain isolated

**Description:** AC 2.1.1 — Decision Table / Data Integrity — Each student's score detail remains independent in a group lesson on Salesforce Lesson Report Detail.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- The SF Lesson Custom Setting is `ON`.
- A group lesson has Student A and Student B.
- Student A's Total Score and Test Result are blank.
- Student B's Total Score is `100.0`.
- Student B's Test Result is `92.5`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters Total Score `-10.5` and Test Result `8.5` for Student A in Salesforce Lesson Report Detail and saves the report. | Salesforce Lesson Report Detail for Student A displays `-10.5` and `8.5`. | screen = SF Lesson Report Detail; student = A; total_score = -10.5; test_result = 8.5 |
| 2 | HQ or CM Staff opens Student B's Salesforce Lesson Report Detail in the same lesson. | Salesforce Lesson Report Detail for Student B retains Total Score `100.0` and Test Result `92.5`. | screen = SF Lesson Report Detail; student = B; expected_total_score = 100.0; expected_test_result = 92.5 |

**Severity:** critical
**Priority:** high

---

### [Koyu] Lesson Report – BO Lesson Report Detail – Test Result update – Other scores retained

**Description:** AC 2.1.1 — CRUD / Regression — Updating Test Result in Back Office Lesson Report Detail does not change Total Score or inactive Lesson Quiz data.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- The BO internal score setting is `ON`.
- Student A's Lesson Quiz is `80%`.
- Student A's Total Score is `10.0`.
- Student A's Test Result is `8.0`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff changes Student A's Test Result to `9.5` in Back Office Lesson Report Detail and saves the report. | Back Office Lesson Report Detail displays Test Result `9.5`. | screen = BO Lesson Report Detail; test_result = 9.5 |
| 2 | HQ or CM Staff reopens Student A's Back Office Lesson Report Detail. | Total Score remains `10.0` and the stored Lesson Quiz value remains `80%`. | screen = BO Lesson Report Detail; expected_total_score = 10.0; expected_lesson_quiz = 80% |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – SF Lesson Report Detail to BO Lesson Report Detail – Exact scores synchronized

**Description:** AC 2.1.1 — CRUD / Regression — Both saved score values from Salesforce Lesson Report Detail are read unchanged in Back Office Lesson Report Detail.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- HQ or CM Staff is logged in to the Koyu Back Office.
- The SF Lesson Custom Setting is `ON`.
- The BO internal score setting is `ON`.
- Student A's Total Score and Test Result are blank.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters Total Score `-10.5` and Test Result `8.5` for Student A in Salesforce Lesson Report Detail and saves the report. | Salesforce Lesson Report Detail displays Total Score `-10.5` and Test Result `8.5`. | source_screen = SF Lesson Report Detail; total_score = -10.5; test_result = 8.5 |
| 2 | HQ or CM Staff opens Student A's Back Office Lesson Report Detail. | Back Office Lesson Report Detail displays Total Score `-10.5` and Test Result `8.5`. | target_screen = BO Lesson Report Detail; expected_total_score = -10.5; expected_test_result = 8.5 |

**Severity:** critical
**Priority:** high

---

### [Koyu] Lesson Report – BO Lesson Report Detail to SF Lesson Report Detail – Exact scores synchronized

**Description:** AC 2.1.1 — CRUD / Regression — Both saved score values from Back Office Lesson Report Detail are read unchanged in Salesforce Lesson Report Detail.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- The SF Lesson Custom Setting is `ON`.
- The BO internal score setting is `ON`.
- Student A's Total Score and Test Result are blank.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters Total Score `20.0` and Test Result `18.5` for Student A in Back Office Lesson Report Detail and saves the report. | Back Office Lesson Report Detail displays Total Score `20.0` and Test Result `18.5`. | source_screen = BO Lesson Report Detail; total_score = 20.0; test_result = 18.5 |
| 2 | HQ or CM Staff opens Student A's Salesforce Lesson Report Detail. | Salesforce Lesson Report Detail displays Total Score `20.0` and Test Result `18.5`. | target_screen = SF Lesson Report Detail; expected_total_score = 20.0; expected_test_result = 18.5 |

**Severity:** critical
**Priority:** high

---

### [Koyu] Lesson Report – SF Student Sessions Bulk Edit to BO Report under Lesson – Selected students synchronized

**Description:** AC 2.1.1 — CRUD / Data Integrity — Scores saved for selected students in Salesforce Student Sessions Bulk Edit appear on the matching Back Office Report under Lesson rows without cross-student overwrite.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- HQ or CM Staff is logged in to the Koyu Back Office.
- The SF Lesson Custom Setting is `ON`.
- The BO internal score setting is `ON`.
- A group lesson has Student A and Student B with blank score values.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects Student A and Student B in Salesforce Student Sessions Bulk Edit, enters their distinct scores, and saves. | Salesforce Student Sessions Bulk Edit saves Student A's Total Score `-10.5` and Test Result `8.5`, and Student B's Total Score `20.0` and Test Result `18.5`. | source_screen = SF Student Sessions Bulk Edit; Student A = -10.5, 8.5; Student B = 20.0, 18.5 |
| 2 | HQ or CM Staff opens the group lesson's Back Office Report under Lesson. | Student A and Student B rows show their respective saved Total Score and Test Result values. | target_screen = BO Report under Lesson; Student A = -10.5, 8.5; Student B = 20.0, 18.5 |

**Severity:** critical
**Priority:** high

---

### [Koyu] Lesson Report – BO Bulk Update to SF Report under Lesson – Selected students synchronized

**Description:** AC 2.1.1 — CRUD / Data Integrity — Scores saved for selected students in the Back Office Bulk Update dialog appear on the matching Salesforce Report under Lesson rows without cross-student overwrite.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- The SF Lesson Custom Setting is `ON`.
- The BO internal score setting is `ON`.
- A group lesson has Student A and Student B with blank score values.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff selects Student A and Student B in the Back Office Bulk Update dialog, enters their distinct scores, and saves. | Back Office Bulk Update saves Student A's Total Score `-20.5` and Test Result `15.0`, and Student B's Total Score `30.0` and Test Result `28.5`. | source_screen = BO Bulk Update; Student A = -20.5, 15.0; Student B = 30.0, 28.5 |
| 2 | HQ or CM Staff opens the group lesson's Salesforce Report under Lesson. | Student A and Student B rows show their respective saved Total Score and Test Result values. | target_screen = SF Report under Lesson; Student A = -20.5, 15.0; Student B = 30.0, 28.5 |

**Severity:** critical
**Priority:** high

---

### [Koyu] Lesson Report – SF LA Detail Report History – Published score snapshot displayed

**Description:** AC 2.1.1 — Regression / Component — Salesforce Report History in Lesson Allocation Detail shows the exact score snapshot of a published report.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- The SF Lesson Custom Setting is `ON`.
- Student A has a published Lesson Report history entry with Total Score `50.0` and Test Result `48.5`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student A's Report History in Salesforce Lesson Allocation Detail. | Salesforce Report History opens the published Lesson Report snapshot for Student A. | screen = SF LA Detail Report History; report_status = Published |
| 2 | HQ or CM Staff reads the score values in the history snapshot. | The history snapshot displays Total Score `50.0` and Test Result `48.5` as read-only values. | expected_total_score = 50.0; expected_test_result = 48.5; editability = read-only |

**Severity:** major
**Priority:** high

---

### [Koyu] Lesson Report – BO Report under Lesson History – Published score snapshot displayed

**Description:** AC 2.1.1 — Regression / Component — Back Office Report History opened from Report under Lesson shows the exact score snapshot of a published report.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- The BO internal score setting is `ON`.
- Student A has a published Lesson Report history entry with Total Score `50.0` and Test Result `48.5`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student A's Report History from Back Office Report under Lesson. | Back Office Report History opens the published Lesson Report snapshot for Student A. | entry_screen = BO Report under Lesson; report_status = Published |
| 2 | HQ or CM Staff reads the score values in the history snapshot. | The history snapshot displays Total Score `50.0` and Test Result `48.5` as read-only values. | target_screen = BO Report History; expected_total_score = 50.0; expected_test_result = 48.5; editability = read-only |

**Severity:** major
**Priority:** high

---

### [Koyu] Lesson Report – BO Lesson Report Detail History – Published score snapshot displayed

**Description:** AC 2.1.1 — Regression / Component — Back Office Report History opened from Lesson Report Detail shows the exact score snapshot of a published report.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- The BO internal score setting is `ON`.
- Student A has a published Lesson Report history entry with Total Score `50.0` and Test Result `48.5`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student A's Report History from Back Office Lesson Report Detail. | Back Office Report History opens the published Lesson Report snapshot for Student A. | entry_screen = BO Lesson Report Detail; report_status = Published |
| 2 | HQ or CM Staff reads the score values in the history snapshot. | The history snapshot displays Total Score `50.0` and Test Result `48.5` as read-only values. | target_screen = BO Report History; expected_total_score = 50.0; expected_test_result = 48.5; editability = read-only |

**Severity:** major
**Priority:** high

---

### [Koyu] Learner App – Student Lesson Report – Published report – SF Lesson Report Detail values displayed

**Description:** AC 2.1.1 / AC 2.1.2 — State Transition / Component — A student sees exact values from Salesforce Lesson Report Detail after normal report publication.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- Student A is logged in to the Koyu Learner App.
- The SF Lesson Custom Setting is `ON`.
- The App internal score setting is `ON`.
- Student A's lesson and Lesson Report are published.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff saves Total Score `-20.5` and Test Result `15.0` for Student A in Salesforce Lesson Report Detail. | Salesforce Lesson Report Detail stores the two values. | source_screen = SF Lesson Report Detail; total_score = -20.5; test_result = 15.0 |
| 2 | Student A opens the published Student Lesson Report in the Learner App. | Student Lesson Report displays Total Score `-20.5` and Test Result `15.0`; Lesson Quiz is absent and neither score is editable. | target_screen = Learner App Student Lesson Report; expected_total_score = -20.5; expected_test_result = 15.0 |

**Severity:** critical
**Priority:** high

---

### [Koyu] Learner App – Parent Lesson Report – Published report – BO Lesson Report Detail values displayed

**Description:** AC 2.1.1 / AC 2.1.2 — State Transition / Permission Matrix — A parent sees exact values from Back Office Lesson Report Detail for the selected child.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- Parent A is logged in to the Koyu Learner App and selects Student A.
- The BO internal score setting is `ON`.
- Student A's lesson and Lesson Report are published.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff saves Total Score `50.0` and Test Result `48.5` for Student A in Back Office Lesson Report Detail. | Back Office Lesson Report Detail stores the two values. | source_screen = BO Lesson Report Detail; total_score = 50.0; test_result = 48.5 |
| 2 | Parent A opens Student A's published Parent Lesson Report in the Learner App. | Parent Lesson Report displays Total Score `50.0` and Test Result `48.5`; neither score is editable. | target_screen = Learner App Parent Lesson Report; expected_total_score = 50.0; expected_test_result = 48.5 |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Learner App – Student Lesson Report – Draft report – Values not exposed

**Description:** AC 2.1.2 — State Transition / Negative — New score values do not bypass the existing published-report visibility condition on Student Lesson Report.

**Preconditions:**

- Student A is logged in to the Koyu Learner App.
- The App internal score setting is `ON`.
- Student A's Lesson Report Detail has Total Score `50.0` and Test Result `48.5`.
- Student A's Lesson Report is Draft.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student A opens the Student Lesson Report in the Learner App. | The unpublished Student Lesson Report score detail is not exposed to Student A. | screen = Learner App Student Lesson Report; report_status = Draft |

**Severity:** major
**Priority:** high

---

### [Koyu] Lesson Report – SF Report under Lesson – Invalid Total Score – BO Report under Lesson retains value

**Description:** AC 2.1.1 — Negative / Data Integrity — A blocked Total Score save in Salesforce Report under Lesson does not overwrite the prior value in Back Office Report under Lesson.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- HQ or CM Staff is logged in to the Koyu Back Office.
- The SF Lesson Custom Setting is `ON`.
- The BO internal score setting is `ON`.
- Student A's Total Score is `10.0` in both staff surfaces.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff enters `10.25` in Student A's Total Score in Salesforce Report under Lesson and saves the report. | Salesforce Report under Lesson blocks save with the active-locale validation message. | source_screen = SF Report under Lesson; total_score = 10.25 |
| 2 | HQ or CM Staff opens Student A's report in Back Office Report under Lesson. | Back Office Report under Lesson retains Total Score `10.0`. | target_screen = BO Report under Lesson; expected_total_score = 10.0 |

**Severity:** critical
**Priority:** high

---

### [Koyu] Lesson Report – SF Lesson Report Detail to BO Lesson Report Detail – Refreshed value displayed

**Description:** AC 2.1.1 — Regression — Back Office Lesson Report Detail does not retain a stale score after a Salesforce Lesson Report Detail update and refresh.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- HQ or CM Staff opens Student A's Back Office Lesson Report Detail.
- The SF Lesson Custom Setting is `ON`.
- The BO internal score setting is `ON`.
- Student A's Total Score is `10.0`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff changes Student A's Total Score to `11.0` in Salesforce Lesson Report Detail and saves the report. | Salesforce Lesson Report Detail displays Total Score `11.0`. | source_screen = SF Lesson Report Detail; total_score = 11.0 |
| 2 | HQ or CM Staff refreshes Student A's open Back Office Lesson Report Detail. | Back Office Lesson Report Detail displays Total Score `11.0` rather than the earlier `10.0` value. | target_screen = BO Lesson Report Detail; expected_total_score = 11.0 |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – SF Lesson Report Detail – Total Score changed – Test Result not calculated

**Description:** Scope — Decision Table / Negative — Changing Total Score in Salesforce Lesson Report Detail does not calculate or replace Test Result.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- The SF Lesson Custom Setting is `ON`.
- Student A's Total Score is `100.0`.
- Student A's Test Result is `75.5`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff changes Student A's Total Score to `50.0` in Salesforce Lesson Report Detail and saves the report. | Salesforce Lesson Report Detail displays Total Score `50.0`. | screen = SF Lesson Report Detail; total_score = 50.0 |
| 2 | HQ or CM Staff reads Student A's Test Result in Salesforce Lesson Report Detail. | Test Result remains `75.5` and no percentage or other calculated value appears. | screen = SF Lesson Report Detail; expected_test_result = 75.5 |

**Severity:** minor
**Priority:** medium
