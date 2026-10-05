# Test Cases: LT-107664 — Koyu Lesson Quiz and Total Score

## Suite: [Koyu] Configured Score Layouts

### [Koyu] Lesson Report – SF layout – Setting OFF – Lesson Quiz

**Description:** AC 1.1 — Decision Table / Regression — SF retains the existing percentage-based layout when its custom setting is OFF.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- A published group lesson has Student A's Lesson Quiz value `80%`.
- The SF Lesson Custom Setting is `OFF`.
- Student A's stored Total Score is `-10.5`.
- Student A's stored Test Result is `8.5`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student A's Lesson Report in Salesforce. | The Lesson Report opens with Lesson Quiz visible and Total Score and Test Result absent. | sf_custom_setting = OFF |
| 2 | HQ or CM Staff enters `85` in Lesson Quiz and saves the report. | Lesson Quiz displays and stores `85%`; the two score fields remain absent. | lesson_quiz = 85 |

**Severity:** minor
**Priority:** medium

---

### [Koyu] Lesson Report – BO layout – Internal setting OFF – Lesson Quiz

**Description:** AC 1.1 — Decision Table / Regression — Back Office retains the legacy layout when its internal setting is OFF.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- A published group lesson has Student A's Lesson Quiz value `70%`.
- The BO internal score setting is `OFF`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student A's Lesson Report in Back Office. | Lesson Quiz is visible and Total Score and Test Result are absent. | bo_internal_setting = OFF |
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

### [Koyu] Lesson Report – SF layout – Setting ON – Both new score fields displayed

**Description:** AC 2.1.1 — Decision Table / Component — SF presents the active score layout to staff.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Salesforce organization.
- A group lesson has Student A's Lesson Report Detail.
- The SF Lesson Custom Setting is `ON`.
- Student A's Total Score is `-10.5`.
- Student A's Test Result is `8.5`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student A's Lesson Report in Salesforce. | Total Score and Test Result display with `-10.5` and `8.5`; Lesson Quiz is absent. | sf_custom_setting = ON |
| 2 | HQ or CM Staff selects each new score field. | Both fields accept staff input. | actor = HQ or CM Staff |

**Severity:** major
**Priority:** high

---

### [Koyu] Lesson Report – BO layout – Internal setting ON – Both new score fields displayed

**Description:** AC 2.1.1 — Decision Table / Component — Back Office presents the active score layout to staff.

**Preconditions:**

- HQ or CM Staff is logged in to the Koyu Back Office.
- A group lesson has Student A's Lesson Report Detail.
- The BO internal score setting is `ON`.
- Student A's Total Score is `-10.5`.
- Student A's Test Result is `8.5`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff opens Student A's Lesson Report in Back Office. | Total Score and Test Result display with `-10.5` and `8.5`; Lesson Quiz is absent. | bo_internal_setting = ON |
| 2 | HQ or CM Staff selects each new score field. | Both fields accept staff input. | actor = HQ or CM Staff |

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
