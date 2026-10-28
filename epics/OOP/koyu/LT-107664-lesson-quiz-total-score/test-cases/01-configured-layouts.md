# Test Cases: LT-107664 — Koyu Lesson Quiz and Total Score

## Suite: [Koyu] Configured Score Layouts

### [Koyu] Lesson Report – SF Report under Lesson – Setting OFF – Lesson Quiz

**Description:** AC 1.1 — Decision Table / Regression — SF retains the existing percentage-based layout when its custom setting is OFF.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- A published group lesson has Student A's Lesson Quiz value `80%`.
- The SF Lesson Custom Setting is `OFF`.
- Student A's stored Total Score is `-10.5`.
- Student A's stored Test Result is `8.5`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student A's report under the lesson in Salesforce. | The report under the lesson opens with Lesson Quiz visible and Total Score and Test Result absent. | sf_custom_setting = OFF |
| 2 | HQ or CM Staff enters `85` in Lesson Quiz and saves the report. | Lesson Quiz displays and stores `85%`; the two score fields remain absent. | lesson_quiz = 85 |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – BO Report under Lesson – Internal setting OFF – Lesson Quiz

**Description:** AC 1.1 — Decision Table / Regression — Back Office retains the legacy layout when its internal setting is OFF.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- A published group lesson has Student A's Lesson Quiz value `70%`.
- The BO internal score setting is `OFF`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student A's report under the lesson in Back Office. | The report under the lesson shows Lesson Quiz and does not show Total Score or Test Result. | bo_internal_setting = OFF |
| 2 | HQ or CM Staff enters `75` in Lesson Quiz and saves the report. | Lesson Quiz displays and stores `75%`; neither new score field appears. | lesson_quiz = 75 |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Learner App – Student layout – Internal setting OFF – Lesson Quiz

**Description:** AC 1.2 — Decision Table / Component — A student sees only the legacy score in the published report while the internal setting is OFF.

**Preconditions:**

- Student A is logged in to the Koyu Learner App.
- Student A has a published lesson and published Lesson Report.
- Student A's Lesson Quiz value is `65%`.
- The App internal score setting is `OFF`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Student A opens the published Lesson Report. | Lesson Quiz displays `65%`; Total Score and Test Result do not display. | app_internal_setting = OFF |
| 2 | Student A views the score area. | No editable score control is available. | actor = Student A |

**Severity:** trivial
**Priority:** low

---

### [Koyu] Learner App – Parent layout – Internal setting OFF – Lesson Quiz

**Description:** AC 1.2 — Decision Table / Permission Matrix — A parent has the same read-only OFF layout for the selected child.

**Preconditions:**

- Parent A is logged in to the Koyu Learner App.
- Parent A selects Student A.
- Student A has a published lesson and published Lesson Report with Lesson Quiz `65%`.
- The App internal score setting is `OFF`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Parent A opens Student A's published Lesson Report. | Lesson Quiz displays `65%`; Total Score and Test Result do not display. | app_internal_setting = OFF |
| 2 | Parent A views the score area. | No editable score control is available. | actor = Parent A |

**Severity:** trivial
**Priority:** low

---

### [Koyu] Lesson Report – SF Report under Lesson – Setting ON – Both new score fields displayed

**Description:** AC 2.1.1 — Decision Table / Component — SF presents the active score layout to staff.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- A group lesson has Student A's Lesson Report Detail.
- The SF Lesson Custom Setting is `ON`.
- Student A's Total Score is `-10.5`.
- Student A's Test Result is `8.5`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student A's report under the lesson in Salesforce. | The report under the lesson displays Total Score `-10.5` and Test Result `8.5`; Lesson Quiz is absent. | sf_custom_setting = ON |
| 2 | HQ or CM Staff selects each new score field. | Both fields accept staff input. | actor = HQ or CM Staff |

**Severity:** major
**Priority:** high

---

### [Koyu] Lesson Report – BO Report under Lesson – Internal setting ON – Both new score fields displayed

**Description:** AC 2.1.1 — Decision Table / Component — Back Office presents the active score layout to staff.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- A group lesson has Student A's Lesson Report Detail.
- The BO internal score setting is `ON`.
- Student A's Total Score is `-10.5`.
- Student A's Test Result is `8.5`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student A's report under the lesson in Back Office. | The report under the lesson displays Total Score `-10.5` and Test Result `8.5`; Lesson Quiz is absent. | bo_internal_setting = ON |
| 2 | HQ or CM Staff selects each new score field. | Both fields accept staff input. | actor = HQ or CM Staff |

**Severity:** major
**Priority:** high

---

### [Koyu] Lesson Report – SF Lesson Report Detail – Setting OFF – Lesson Quiz

**Description:** AC 1.1 — Decision Table / Regression — The Salesforce Lesson Report Detail retains the legacy score layout when the custom setting is OFF.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- A group lesson has Student A's Lesson Report Detail with Lesson Quiz `80%`.
- The SF Lesson Custom Setting is `OFF`.
- Student A's stored Total Score is `-10.5`.
- Student A's stored Test Result is `8.5`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student A's Lesson Report Detail in Salesforce. | The Lesson Report Detail shows Lesson Quiz `80%` and does not show Total Score or Test Result. | sf_custom_setting = OFF |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – SF Lesson Report Detail – Setting ON – Both new score fields displayed

**Description:** AC 2.1.1 — Decision Table / Component — The Salesforce Lesson Report Detail presents the active score layout when the custom setting is ON.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- A group lesson has Student A's Lesson Report Detail.
- The SF Lesson Custom Setting is `ON`.
- Student A's Total Score is `-10.5`.
- Student A's Test Result is `8.5`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student A's Lesson Report Detail in Salesforce. | The Lesson Report Detail displays Total Score `-10.5` and Test Result `8.5`; Lesson Quiz is absent. | sf_custom_setting = ON |

**Severity:** major
**Priority:** high

---

### [Koyu] Lesson Report – SF LA Detail Report History – Setting OFF – Lesson Quiz

**Description:** AC 1.1 — Decision Table / Regression — Report History in the Salesforce Lesson Allocation Detail retains the legacy score layout when the custom setting is OFF.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- Student A's Lesson Allocation Detail has a Report History entry with Lesson Quiz `80%`.
- The SF Lesson Custom Setting is `OFF`.
- Student A's stored Total Score is `-10.5`.
- Student A's stored Test Result is `8.5`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student A's Report History in the Lesson Allocation Detail. | The Report History entry shows Lesson Quiz `80%` and does not show Total Score or Test Result. | sf_custom_setting = OFF |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – SF LA Detail Report History – Setting ON – Both new score fields displayed

**Description:** AC 2.1.1 — Decision Table / Component — Report History in the Salesforce Lesson Allocation Detail presents the active score layout when the custom setting is ON.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- Student A's Lesson Allocation Detail has a Report History entry.
- The SF Lesson Custom Setting is `ON`.
- Student A's Total Score is `-10.5`.
- Student A's Test Result is `8.5`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student A's Report History in the Lesson Allocation Detail. | The Report History entry displays Total Score `-10.5` and Test Result `8.5`; Lesson Quiz is absent. | sf_custom_setting = ON |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – BO Lesson Report Detail – Internal setting OFF – Lesson Quiz

**Description:** AC 1.1 — Decision Table / Regression — The Back Office Lesson Report Detail retains the legacy score layout when the internal setting is OFF.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- A group lesson has Student A's Lesson Report Detail with Lesson Quiz `70%`.
- The BO internal score setting is `OFF`.
- Student A's stored Total Score is `-10.5`.
- Student A's stored Test Result is `8.5`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student A's Lesson Report Detail in Back Office. | The Lesson Report Detail shows Lesson Quiz `70%` and does not show Total Score or Test Result. | bo_internal_setting = OFF |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – BO Lesson Report Detail – Internal setting ON – Both new score fields displayed

**Description:** AC 2.1.1 — Decision Table / Component — The Back Office Lesson Report Detail presents the active score layout when the internal setting is ON.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- A group lesson has Student A's Lesson Report Detail.
- The BO internal score setting is `ON`.
- Student A's Total Score is `-10.5`.
- Student A's Test Result is `8.5`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student A's Lesson Report Detail in Back Office. | The Lesson Report Detail displays Total Score `-10.5` and Test Result `8.5`; Lesson Quiz is absent. | bo_internal_setting = ON |

**Severity:** major
**Priority:** high

---

### [Koyu] Lesson Report – BO Bulk Update dialog – Internal setting OFF – Lesson Quiz

**Description:** AC 1.1 — Decision Table / Regression — The Back Office Bulk Update dialog retains the legacy score layout when the internal setting is OFF.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- A group lesson has selected Student A and Student B Lesson Report Details for bulk update.
- Both selected students have Lesson Quiz values.
- The BO internal score setting is `OFF`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Bulk Update for the selected Lesson Report Details. | The Bulk Update dialog shows the editable Lesson Quiz field and does not show Total Score or Test Result. | bo_internal_setting = OFF |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – BO Bulk Update dialog – Internal setting ON – Both new score fields displayed

**Description:** AC 2.1.1 — Decision Table / Component — The Back Office Bulk Update dialog presents the active score layout when the internal setting is ON.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- A group lesson has selected Student A and Student B Lesson Report Details for bulk update.
- The BO internal score setting is `ON`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Bulk Update for the selected Lesson Report Details. | The Bulk Update dialog shows editable Total Score and Test Result fields and does not show Lesson Quiz. | bo_internal_setting = ON |

**Severity:** major
**Priority:** high

---

### [Koyu] Lesson Report – BO Report under Lesson History dialog – Internal setting OFF – Lesson Quiz

**Description:** AC 1.1 — Decision Table / Regression — Report History opened from the Back Office report under the lesson retains the legacy score layout when the internal setting is OFF.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- Student A has a Report History record accessible from the report under the lesson.
- The Report History record has Lesson Quiz `80%`.
- The BO internal score setting is `OFF`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student A's Report History from the report under the lesson. | The Report History dialog shows Lesson Quiz `80%` and does not show Total Score or Test Result. | bo_internal_setting = OFF |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – BO Report under Lesson History dialog – Internal setting ON – Both new score fields displayed

**Description:** AC 2.1.1 — Decision Table / Component — Report History opened from the Back Office report under the lesson presents the active score layout when the internal setting is ON.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- Student A has a Report History record accessible from the report under the lesson.
- The Report History record has Total Score `-10.5` and Test Result `8.5`.
- The BO internal score setting is `ON`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student A's Report History from the report under the lesson. | The Report History dialog displays Total Score `-10.5` and Test Result `8.5`; Lesson Quiz is absent. | bo_internal_setting = ON |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – BO Lesson Report Detail History dialog – Internal setting OFF – Lesson Quiz

**Description:** AC 1.1 — Decision Table / Regression — Report History opened from the Back Office Lesson Report Detail retains the legacy score layout when the internal setting is OFF.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- Student A has a Report History record accessible from the Lesson Report Detail.
- The Report History record has Lesson Quiz `80%`.
- The BO internal score setting is `OFF`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student A's Report History from the Lesson Report Detail. | The Report History dialog shows Lesson Quiz `80%` and does not show Total Score or Test Result. | bo_internal_setting = OFF |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – BO Lesson Report Detail History dialog – Internal setting ON – Both new score fields displayed

**Description:** AC 2.1.1 — Decision Table / Component — Report History opened from the Back Office Lesson Report Detail presents the active score layout when the internal setting is ON.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- Student A has a Report History record accessible from the Lesson Report Detail.
- The Report History record has Total Score `-10.5` and Test Result `8.5`.
- The BO internal score setting is `ON`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student A's Report History from the Lesson Report Detail. | The Report History dialog displays Total Score `-10.5` and Test Result `8.5`; Lesson Quiz is absent. | bo_internal_setting = ON |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – SF Student Sessions Bulk Edit – Setting OFF – Lesson Quiz

**Description:** AC 1.1 — Decision Table / Regression — Salesforce Student Sessions Bulk Edit follows the legacy score layout when the custom setting is OFF.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- Student A and Student B Student Session records are selected for Bulk Edit.
- The SF Lesson Custom Setting is `OFF`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student Sessions Bulk Edit. | Bulk Edit shows editable Lesson Quiz and does not show Total Score or Test Result. | sf_custom_setting = OFF |

**Severity:** major
**Priority:** high

---

### [Koyu] Lesson Report – SF Student Sessions Bulk Edit – Setting ON – Both new score fields displayed

**Description:** AC 2.1.1 — Decision Table / Regression — Salesforce Student Sessions Bulk Edit follows the active score layout when the custom setting is ON.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- Student A and Student B Student Session records are selected for Bulk Edit.
- The SF Lesson Custom Setting is `ON`.
- Student A's Total Score is `-10.5`.
- Student A's Test Result is `8.5`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student Sessions Bulk Edit. | Bulk Edit shows editable Total Score and Test Result and does not show Lesson Quiz. | sf_custom_setting = ON |

**Severity:** major
**Priority:** high

---

### [Koyu] Lesson Report – SF layout – Setting changed OFF then ON – Stored values retained

**Description:** Scope — Decision Table / Regression — Switching the SF layout hides values without deleting either layout's data.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- Student A's Lesson Quiz is `90%`.
- Student A's Total Score is `-12.5`.
- Student A's Test Result is `11.0`.
- The SF Lesson Custom Setting is `ON`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff sets the SF Lesson Custom Setting to `OFF` and opens Student A's Lesson Report. | Lesson Quiz displays `90%`; both new score fields are hidden. | sf_custom_setting = OFF |
| 2 | HQ or CM Staff sets the SF Lesson Custom Setting to `ON` and reopens the report. | Total Score displays `-12.5` and Test Result displays `11.0`; Lesson Quiz is hidden. | sf_custom_setting = ON |

**Severity:** major
**Priority:** high

---

### [Koyu] Lesson Report – BO and App layouts – Internal setting changed OFF then ON – Stored values retained

**Description:** Scope — Decision Table / Regression — The BO/App internal setting preserves data across its OFF/ON layout transition.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- Student A is logged in to the Koyu Learner App.
- Student A has a published Lesson Report.
- Student A's Lesson Quiz is `90%`.
- Student A's Total Score is `-12.5`.
- Student A's Test Result is `11.0`.
- The BO/App internal score setting is `ON`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff sets the BO/App internal score setting to `OFF`. | BO shows Lesson Quiz `90%`; the App shows Lesson Quiz `90%`; both new fields are hidden on both surfaces. | internal_setting = OFF |
| 2 | HQ or CM Staff sets the BO/App internal score setting to `ON`. | BO and the App show Total Score `-12.5` and Test Result `11.0`; Lesson Quiz is hidden. | internal_setting = ON |

**Severity:** major
**Priority:** high
