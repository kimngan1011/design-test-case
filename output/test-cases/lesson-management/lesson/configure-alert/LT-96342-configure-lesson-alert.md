# Test Cases: LT-96342 — [Renseikai] Configure Lesson Student Session Error Message Display

---

## Suite: Configure Alert – Partner Config Flag

---

### [Renseikai] Configure Alert – Partner Config Flag – Out of Duration config disabled – Alert flag recognized by system

**Description:** AC 01.1 — Decision Table — When the "Out of Duration Students" alert config flag is set to disabled for the Renseikai partner, the system recognizes and applies the config.

**Preconditions:**

- Logged in as Renseikai Admin or CM user
- The Renseikai partner has the `show_out_of_duration_alert` config flag set to `FALSE`
- A lesson exists at a Renseikai location with at least one student whose lesson date falls outside their course LA duration

| #   | Action                                                                     | Expected Result                                                                        | Test Data                                 |
| --- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ----------------------------------------- |
| 1   | Open the SF Lesson detail page for the lesson with out-of-duration student | SF Lesson detail page loads                                                            | Lesson with 1 student outside LA duration |
| 2   | Navigate to the Participants tab → Student Sessions section                | Student Sessions section is displayed                                                  |                                           |
| 3   | Observe the alert banners area                                             | The "⚠ Lesson falls outside this student's course duration." banner is **not visible** |                                           |
| 4   | Open the BO Lesson detail page for the same lesson                         | BO Lesson detail page loads                                                            |                                           |
| 5   | Observe the alert banners area on BO                                       | The out-of-duration alert banner is **not visible** on BO either                       |                                           |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Configure Alert – Partner Config Flag – Classroom Capacity config disabled – Alert flag recognized by system

**Description:** AC 01.2 — Decision Table — When the "Classroom Capacity" alert config flag is set to disabled for the Renseikai partner, the system recognizes and applies the config.

**Preconditions:**

- Logged in as Renseikai Admin or CM user
- The Renseikai partner has the `show_classroom_capacity_alert` config flag set to `FALSE`
- A lesson exists at a Renseikai location with Lesson Capacity = 2 and 3 students assigned (capacity exceeded)

| #   | Action                                                          | Expected Result                                                                                           | Test Data                         |
| --- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | --------------------------------- |
| 1   | Open the SF Lesson detail page for the capacity-exceeded lesson | SF Lesson detail page loads                                                                               | Lesson Capacity = 2, Students = 3 |
| 2   | Navigate to the Participants tab → Student Sessions section     | Student Sessions section is displayed                                                                     |                                   |
| 3   | Observe the alert banners area                                  | The "X/Y The number of assigned students exceeded the defined lesson capacity." banner is **not visible** |                                   |
| 4   | Open the BO Lesson detail page for the same lesson              | BO Lesson detail page loads                                                                               |                                   |
| 5   | Observe the alert banners area on BO                            | The classroom capacity alert banner is **not visible** on BO either                                       |                                   |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Configure Alert – Partner Config Flag – Out of Duration disabled, Classroom Capacity enabled – Only capacity alert shown

**Description:** AC 01.3 — Decision Table — The two alert config flags are independent. When Out of Duration is disabled and Classroom Capacity is enabled, only the capacity alert appears.

**Preconditions:**

- Logged in as Renseikai Admin or CM user
- `show_out_of_duration_alert` = `FALSE`, `show_classroom_capacity_alert` = `TRUE`
- A lesson exists with: Lesson Capacity = 1, 2 students assigned, and one student outside their LA duration

| #   | Action                                                      | Expected Result                                                                           | Test Data                                            |
| --- | ----------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| 1   | Open the SF Lesson detail page for the lesson               | SF Lesson detail page loads                                                               | Lesson Capacity = 1, Students = 2, 1 out-of-duration |
| 2   | Navigate to the Participants tab → Student Sessions section | Student Sessions section is displayed                                                     |                                                      |
| 3   | Observe the alert banners                                   | "The number of assigned students exceeded the defined lesson capacity." banner IS visible |                                                      |
| 4   | Observe the alert banners for out-of-duration               | The "⚠ Lesson falls outside this student's course duration." banner is **not visible**    |                                                      |

**Severity:** major
**Priority:** high

---

### [Renseikai] Configure Alert – Partner Config Flag – Both alerts disabled – Neither alert shown

**Description:** AC 01.1, AC 01.2 — Decision Table — When both alert config flags are disabled, neither alert banner appears on the Lesson detail page.

**Preconditions:**

- Logged in as Renseikai Admin or CM user
- `show_out_of_duration_alert` = `FALSE`, `show_classroom_capacity_alert` = `FALSE`
- A lesson exists with: Lesson Capacity = 0, 3 students assigned, and 2 students outside their LA duration (both alert conditions are triggered)

| #   | Action                                                      | Expected Result                                                 | Test Data                                            |
| --- | ----------------------------------------------------------- | --------------------------------------------------------------- | ---------------------------------------------------- |
| 1   | Open the SF Lesson detail page for the lesson               | SF Lesson detail page loads                                     | Lesson Capacity = 0, Students = 3, 2 out-of-duration |
| 2   | Navigate to the Participants tab → Student Sessions section | Student Sessions section is displayed with the list of students |                                                      |
| 3   | Observe the entire alert banners area                       | **No alert banners** are displayed in the Student Sessions area |                                                      |
| 4   | Open the BO Lesson detail page for the same lesson          | BO Lesson detail page loads                                     |                                                      |
| 5   | Observe the alert banners area on BO                        | **No alert banners** are displayed on BO either                 |                                                      |

**Severity:** critical
**Priority:** high

---

## Suite: Configure Alert – SF Out of Duration

---

### [Renseikai] Configure Alert – SF Out of Duration – Config disabled – Out-of-duration banner not displayed

**Description:** AC 02.1 — Decision Table + Negative Testing — When the "Out of Duration Students" config is disabled for Renseikai, the SF Lesson detail page does not show the out-of-duration alert banner even when a student's lesson falls outside their course duration.

**Preconditions:**

- Logged in as Renseikai Admin or CM user on SF
- `show_out_of_duration_alert` = `FALSE` for Renseikai partner
- Student "Student A" is assigned to Lesson L1 (date: 2026-04-10)
- Student A's LA duration is 2026-01-01 to 2026-03-31 (i.e., Lesson L1 is outside their duration)

| #   | Action                                                              | Expected Result                                                                    | Test Data               |
| --- | ------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ----------------------- |
| 1   | Navigate to SF Lesson detail page for Lesson L1                     | SF Lesson detail page opens                                                        | Lesson date: 2026-04-10 |
| 2   | Click the Participants tab                                          | Participants tab content is shown                                                  |                         |
| 3   | Scroll to the Student Sessions section                              | Student Sessions section is visible with Student A listed                          |                         |
| 4   | Inspect the area above the Student Sessions table for alert banners | The "⚠ Lesson falls outside this student's course duration." banner is **absent**  |                         |
| 5   | Confirm the student is still listed in the Student Sessions table   | Student A is shown in the table (record is not removed — only alert is suppressed) |                         |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Configure Alert – SF Out of Duration – Config enabled – Out-of-duration banner displayed

**Description:** AC 02.2 — Decision Table — When the "Out of Duration Students" config is enabled for Renseikai, the SF Lesson detail page shows the out-of-duration alert banner when a student's lesson falls outside their course duration.

**Preconditions:**

- Logged in as Renseikai Admin or CM user on SF
- `show_out_of_duration_alert` = `TRUE` for Renseikai partner
- Student "Student B" is assigned to Lesson L2 (date: 2026-04-15)
- Student B's LA duration is 2026-01-01 to 2026-03-31 (L2 is outside duration)

| #   | Action                                          | Expected Result                                                                  | Test Data               |
| --- | ----------------------------------------------- | -------------------------------------------------------------------------------- | ----------------------- |
| 1   | Navigate to SF Lesson detail page for Lesson L2 | SF Lesson detail page opens                                                      | Lesson date: 2026-04-15 |
| 2   | Click the Participants tab                      | Participants tab content is shown                                                |                         |
| 3   | Scroll to the Student Sessions section          | Student Sessions section is visible with Student B listed                        |                         |
| 4   | Inspect the alert banners area                  | The "⚠ Lesson falls outside this student's course duration." banner IS displayed |                         |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Configure Alert – SF Out of Duration – Config disabled, multiple out-of-duration students – No banner shown

**Description:** AC 02.3 — Equivalence Partitioning — Alert suppression applies regardless of how many students are outside their course duration.

**Preconditions:**

- Logged in as Renseikai Admin or CM user on SF
- `show_out_of_duration_alert` = `FALSE` for Renseikai partner
- A lesson exists with 3 students, all 3 outside their respective LA durations

| #   | Action                                                                | Expected Result                                                                   | Test Data                          |
| --- | --------------------------------------------------------------------- | --------------------------------------------------------------------------------- | ---------------------------------- |
| 1   | Navigate to SF Lesson detail page for the lesson                      | SF Lesson detail page opens                                                       | Lesson with 3 students             |
| 2   | Click the Participants tab                                            | Participants tab shows 3 students in Student Sessions                             |                                    |
| 3   | Inspect the alert banners area                                        | The "⚠ Lesson falls outside this student's course duration." banner is **absent** | All 3 students are out-of-duration |
| 4   | Confirm all 3 students are still listed in the Student Sessions table | All 3 students appear in the table                                                |                                    |

**Severity:** major
**Priority:** high

---

## Suite: Configure Alert – BO Out of Duration

---

### [Renseikai] Configure Alert – BO Out of Duration – Config disabled – Out-of-duration banner not displayed

**Description:** AC 03.1 — Decision Table + Negative Testing — When the "Out of Duration Students" config is disabled for Renseikai, the BO Lesson detail page does not show the out-of-duration alert banner.

**Preconditions:**

- Logged in as Renseikai Admin or CM user on BO
- `show_out_of_duration_alert` = `FALSE` for Renseikai partner
- A lesson exists with at least one student whose lesson date falls outside their LA duration

| #   | Action                                                            | Expected Result                                             | Test Data                   |
| --- | ----------------------------------------------------------------- | ----------------------------------------------------------- | --------------------------- |
| 1   | Navigate to BO Lesson detail page for the lesson                  | BO Lesson detail page opens                                 |                             |
| 2   | Scroll to the Student Sessions section                            | Student Sessions section is visible with the student listed |                             |
| 3   | Inspect the alert banners area                                    | The out-of-duration alert banner is **absent**              | Student outside LA duration |
| 4   | Confirm the student is still listed in the Student Sessions table | Student appears in the table                                |                             |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Configure Alert – BO Out of Duration – Config enabled – Out-of-duration banner displayed

**Description:** AC 03.2 — Decision Table — When the "Out of Duration Students" config is enabled for Renseikai, the BO Lesson detail page shows the out-of-duration alert banner when applicable.

**Preconditions:**

- Logged in as Renseikai Admin or CM user on BO
- `show_out_of_duration_alert` = `TRUE` for Renseikai partner
- A student is assigned to a lesson that falls outside their LA duration

| #   | Action                                           | Expected Result                                   | Test Data |
| --- | ------------------------------------------------ | ------------------------------------------------- | --------- |
| 1   | Navigate to BO Lesson detail page for the lesson | BO Lesson detail page opens                       |           |
| 2   | Scroll to the Student Sessions section           | Student Sessions section is visible               |           |
| 3   | Inspect the alert banners area                   | The out-of-duration alert banner **IS displayed** |           |

**Severity:** major
**Priority:** high

---

## Suite: Configure Alert – SF Classroom Capacity

---

### [Renseikai] Configure Alert – SF Classroom Capacity – Config disabled – Capacity-exceeded banner not displayed

**Description:** AC 04.1 — Decision Table + Negative Testing — When the "Classroom Capacity" config is disabled for Renseikai, the SF Lesson detail page does not show the classroom capacity alert even when assigned students exceed the defined lesson capacity.

**Preconditions:**

- Logged in as Renseikai Admin or CM user on SF
- `show_classroom_capacity_alert` = `FALSE` for Renseikai partner
- A lesson exists with Lesson Capacity = 2 and 3 students assigned

| #   | Action                                                   | Expected Result                                                                                      | Test Data                         |
| --- | -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | --------------------------------- |
| 1   | Navigate to SF Lesson detail page for the lesson         | SF Lesson detail page opens                                                                          | Lesson Capacity = 2, Students = 3 |
| 2   | Click the Participants tab                               | Participants tab content is shown                                                                    |                                   |
| 3   | Scroll to the Student Sessions section                   | Student Sessions section shows 3 students                                                            |                                   |
| 4   | Inspect the alert banners area                           | The "X/Y The number of assigned students exceeded the defined lesson capacity." banner is **absent** |                                   |
| 5   | Observe the Lesson Capacity field in the Details sidebar | Lesson Capacity field still shows 2 (data is intact; only alert display is suppressed)               |                                   |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Configure Alert – SF Classroom Capacity – Config enabled – Capacity-exceeded banner displayed

**Description:** AC 04.2 — Decision Table — When the "Classroom Capacity" config is enabled for Renseikai, the SF Lesson detail page shows the classroom capacity alert when assigned students exceed the lesson capacity.

**Preconditions:**

- Logged in as Renseikai Admin or CM user on SF
- `show_classroom_capacity_alert` = `TRUE` for Renseikai partner
- A lesson exists with Lesson Capacity = 2 and 3 students assigned

| #   | Action                                           | Expected Result                                                                                                   | Test Data                         |
| --- | ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| 1   | Navigate to SF Lesson detail page for the lesson | SF Lesson detail page opens                                                                                       | Lesson Capacity = 2, Students = 3 |
| 2   | Click the Participants tab                       | Participants tab content is shown                                                                                 |                                   |
| 3   | Scroll to the Student Sessions section           | Student Sessions section shows 3 students                                                                         |                                   |
| 4   | Inspect the alert banners area                   | The "3/2 The number of assigned students exceeded the defined lesson capacity." banner **IS displayed** in orange |                                   |

**Severity:** critical
**Priority:** high

---

## Suite: Configure Alert – BO Classroom Capacity

---

### [Renseikai] Configure Alert – BO Classroom Capacity – Config disabled – Capacity-exceeded banner not displayed

**Description:** AC 05.1 — Decision Table + Negative Testing — When the "Classroom Capacity" config is disabled for Renseikai, the BO Lesson detail page does not show the classroom capacity alert even when capacity is exceeded.

**Preconditions:**

- Logged in as Renseikai Admin or CM user on BO
- `show_classroom_capacity_alert` = `FALSE` for Renseikai partner
- A lesson exists with Lesson Capacity = 1 and 2 students assigned

| #   | Action                                           | Expected Result                                               | Test Data                         |
| --- | ------------------------------------------------ | ------------------------------------------------------------- | --------------------------------- |
| 1   | Navigate to BO Lesson detail page for the lesson | BO Lesson detail page opens                                   | Lesson Capacity = 1, Students = 2 |
| 2   | Scroll to the Student Sessions section           | Student Sessions section is visible with both students listed |                                   |
| 3   | Inspect the alert banners area                   | The classroom capacity exceeded alert banner is **absent**    |                                   |

**Severity:** major
**Priority:** high

---

### [Renseikai] Configure Alert – BO Classroom Capacity – Config enabled – Capacity-exceeded banner displayed

**Description:** AC 05.2 — Decision Table — When the "Classroom Capacity" config is enabled for Renseikai, the BO Lesson detail page shows the classroom capacity alert when applicable.

**Preconditions:**

- Logged in as Renseikai Admin or CM user on BO
- `show_classroom_capacity_alert` = `TRUE` for Renseikai partner
- A lesson exists with Lesson Capacity = 1 and 2 students assigned

| #   | Action                                           | Expected Result                                               | Test Data                         |
| --- | ------------------------------------------------ | ------------------------------------------------------------- | --------------------------------- |
| 1   | Navigate to BO Lesson detail page for the lesson | BO Lesson detail page opens                                   | Lesson Capacity = 1, Students = 2 |
| 2   | Scroll to the Student Sessions section           | Student Sessions section shows both students                  |                                   |
| 3   | Inspect the alert banners area                   | The classroom capacity exceeded alert banner **IS displayed** |                                   |

**Severity:** major
**Priority:** high

---

## Suite: Configure Alert – Default Behavior

---

### Lesson Detail – Alert Default Behavior – Partner without config – Both alerts displayed as before

**Description:** AC 06.1 — Regression Analysis — For partners without an explicit alert config, the default behavior is preserved: both "Out of Duration" and "Classroom Capacity" alerts are shown when the respective conditions are met.

**Preconditions:**

- Logged in as a non-Renseikai partner Admin (e.g., a core/default partner)
- The partner has **no** alert config flags set
- A lesson exists at this partner with: Lesson Capacity = 1, 2 students assigned, and 1 student outside their LA duration

| #   | Action                                           | Expected Result                                                                                 | Test Data                     |
| --- | ------------------------------------------------ | ----------------------------------------------------------------------------------------------- | ----------------------------- |
| 1   | Navigate to SF Lesson detail page for the lesson | SF Lesson detail page opens                                                                     | Non-Renseikai partner lesson  |
| 2   | Click the Participants tab                       | Participants tab content is shown                                                               |                               |
| 3   | Scroll to the Student Sessions section           | Student Sessions section is visible                                                             |                               |
| 4   | Inspect the alert banners area                   | The "The number of assigned students exceeded the defined lesson capacity." banner IS displayed | Capacity = 1, Students = 2    |
| 5   | Inspect for the out-of-duration banner           | The "⚠ Lesson falls outside this student's course duration." banner IS displayed                | 1 student outside LA duration |

**Severity:** critical
**Priority:** high

---

### Lesson Detail – Alert Default Behavior – Renseikai config disabled, other partner – Other partner alerts unaffected

**Description:** AC 06.2 — Regression Analysis — Disabling alert configs for the Renseikai partner does not affect alert display for other partners.

**Preconditions:**

- Renseikai partner has `show_out_of_duration_alert` = `FALSE` and `show_classroom_capacity_alert` = `FALSE`
- A second (non-Renseikai) partner has no config flags set
- A lesson at the non-Renseikai partner has: Lesson Capacity = 2, 3 students assigned, and 1 student outside their LA duration

| #   | Action                                                             | Expected Result                                                                                     | Test Data                         |
| --- | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------- | --------------------------------- |
| 1   | Logged in as non-Renseikai partner Admin on SF                     | Login successful                                                                                    | Non-Renseikai partner credentials |
| 2   | Navigate to SF Lesson detail page for the capacity-exceeded lesson | SF Lesson detail page opens                                                                         | Lesson Capacity = 2, Students = 3 |
| 3   | Click the Participants tab → scroll to Student Sessions section    | Both students and alerts area visible                                                               |                                   |
| 4   | Inspect the alert banners area                                     | The "The number of assigned students exceeded the defined lesson capacity." banner **IS displayed** |                                   |
| 5   | Inspect for the out-of-duration banner                             | The "⚠ Lesson falls outside this student's course duration." banner **IS displayed**                |                                   |

**Severity:** critical
**Priority:** high
