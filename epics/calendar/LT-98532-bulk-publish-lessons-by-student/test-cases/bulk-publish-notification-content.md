# Test Cases: LT-98532 — Bulk Publish Lessons by Student

## Suite: [Riso] Bulk Publish by Student – Notification Content

---

### [Riso] Bulk Publish Notification – Title and Body Line 1 Display Correct Fixed Text

**Description:** AC 02.2 — Equivalence Partitioning — The push notification sent after Bulk Publish has a fixed title "Lesson Schedule has been Published" and a fixed body Line 1 "Lesson schedules for the following period have been published".

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- A Draft lesson for Student A exists in the period May 1–31, 2026
- Student A is linked to Parent A; Student A's Learner App is logged in (EN locale) with push notifications enabled
- Bulk Publish submitted for the period with Student A in filter and checkbox activated; job completed successfully

| #   | Action                                                                                | Expected Result                                                                           | Test Data |
| --- | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | --------- |
| 1   | On Student A's device, open the Learner App and expand the received push notification | Notification is displayed                                                                 | ""        |
| 2   | Read the notification title                                                           | Title is exactly: **"Lesson Schedule has been Published"**                                | ""        |
| 3   | Read the notification body, Line 1                                                    | Line 1 reads exactly: **"Lesson schedules for the following period have been published"** | ""        |

**Severity:** minor
**Priority:** medium

---

### [Riso] Bulk Publish Notification – Body Line 2 Shows Period in Correct Date Format

**Description:** AC 02.2 — Equivalence Partitioning — Notification body Line 2 shows the published period in the format "Month Day, Year ~ Month Day, Year" with the correct start and end dates.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- The Bulk Publish period is set to May 1, 2026 ~ May 31, 2026
- Student A is linked to Parent A; Student A's Learner App is logged in with push notifications enabled
- Bulk Publish job completed successfully

| #   | Action                                                     | Expected Result                                        | Test Data              |
| --- | ---------------------------------------------------------- | ------------------------------------------------------ | ---------------------- |
| 1   | On Student A's device, open the received push notification | Notification is displayed                              | ""                     |
| 2   | Read the notification body, Line 2                         | Line 2 reads exactly: **"May 1, 2026 ~ May 31, 2026"** | Period: May 1–31, 2026 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Bulk Publish Notification – Body Line 2 Period Format – Same Day Start and End Date

**Description:** AC 02.2 — Boundary Value Analysis — When the Bulk Publish period spans exactly 1 day (start date = end date), the notification body Line 2 shows the same date on both sides of the "~" separator.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- The Bulk Publish period is set to a single day: May 15, 2026 ~ May 15, 2026
- Student A is linked to Parent A; Student A's Learner App is logged in with push notifications enabled
- Bulk Publish job completed successfully

| #   | Action                                                     | Expected Result                                         | Test Data               |
| --- | ---------------------------------------------------------- | ------------------------------------------------------- | ----------------------- |
| 1   | On Student A's device, open the received push notification | Notification is displayed                               | ""                      |
| 2   | Read the notification body, Line 2                         | Line 2 reads exactly: **"May 15, 2026 ~ May 15, 2026"** | Period: May 15–15, 2026 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Bulk Publish Notification – Body Line 2 Period Format – Cross-Month Period

**Description:** AC 02.2 — Boundary Value Analysis — When the Bulk Publish period spans two different months, the notification body Line 2 correctly shows both months using the "Month Day, Year ~ Month Day, Year" format.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- The Bulk Publish period spans April 25, 2026 ~ May 5, 2026 (crossing a month boundary)
- Student A is linked to Parent A; Student A's Learner App is logged in with push notifications enabled
- Bulk Publish job completed successfully

| #   | Action                                                     | Expected Result                                          | Test Data                    |
| --- | ---------------------------------------------------------- | -------------------------------------------------------- | ---------------------------- |
| 1   | On Student A's device, open the received push notification | Notification is displayed                                | ""                           |
| 2   | Read the notification body, Line 2                         | Line 2 reads exactly: **"April 25, 2026 ~ May 5, 2026"** | Period: Apr 25 – May 5, 2026 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Bulk Publish Notification – Body Line 2 Period Format – Cross-Year Period

**Description:** AC 02.2 — Boundary Value Analysis — When the Bulk Publish period spans two different years, the notification body Line 2 correctly shows both years in the format.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- The Bulk Publish period spans December 28, 2026 ~ January 5, 2027 (crossing a year boundary)
- Student A is linked to Parent A; Student A's Learner App is logged in with push notifications enabled
- Bulk Publish job completed successfully

| #   | Action                                                     | Expected Result                                                 | Test Data                          |
| --- | ---------------------------------------------------------- | --------------------------------------------------------------- | ---------------------------------- |
| 1   | On Student A's device, open the received push notification | Notification is displayed                                       | ""                                 |
| 2   | Read the notification body, Line 2                         | Line 2 reads exactly: **"December 28, 2026 ~ January 5, 2027"** | Period: Dec 28, 2026 – Jan 5, 2027 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Bulk Publish Notification – Body Line 2 Shows Set Filter Period, Not Individual Lesson Dates

**Description:** AC 02.2 — Data Integrity — The notification body Line 2 shows the exact filter period configured in the Calendar when Bulk Publish was triggered, not a date range dynamically computed from the individual lesson dates within that period.

**Preconditions:**

- User is logged into SF as a Riso HQ Admin
- Calendar filter period is set to May 1, 2026 ~ May 31, 2026
- Two Draft lessons exist within the period: Lesson A on May 8, 2026 and Lesson B on May 22, 2026 (neither date is the filter start or end date)
- Student A is allocated to both Lesson A and Lesson B; Student A is linked to Parent A
- Student A's Learner App is logged in (EN locale) with push notifications enabled
- Bulk Publish submitted with "Apply to selected students" activated for Student A; job completed successfully

| #   | Action                                                     | Expected Result                                                                                                                                                          | Test Data                                                  |
| --- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------- |
| 1   | On Student A's device, open the received push notification | Notification is displayed                                                                                                                                                | ""                                                         |
| 2   | Read the notification body, Line 2                         | Line 2 reads exactly: **"May 1, 2026 ~ May 31, 2026"** (the set filter period). Line 2 does **NOT** show "May 8, 2026 ~ May 22, 2026" (the individual lesson date range) | Filter period: May 1–31, 2026; Lesson dates: May 8, May 22 |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Publish Notification – Deep-Link – Logged-In Student Taps Notification – Calendar Opens at Correct Month

**Description:** AC 02.2 — Regression Analysis — When a logged-in student taps the Bulk Publish push notification, the app opens the Calendar page at the month of the published period's start date, with the start date selected.

**Preconditions:**

- Student A is logged into the Learner App on Device 1
- The Bulk Publish period start date is May 1, 2026
- Student A has received the Bulk Publish push notification in their Learner App

| #   | Action                                                                         | Expected Result                                                                  | Test Data |
| --- | ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------- | --------- |
| 1   | On Device 1, tap the Bulk Publish push notification from the notification tray | Learner App opens                                                                | ""        |
| 2   | Observe the screen that opens                                                  | The **Calendar page** is displayed at **May 2026** (the month of the start date) | ""        |
| 3   | Observe which date is selected / highlighted on the calendar                   | The start date **May 1, 2026** is selected or highlighted                        | ""        |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Publish Notification – Deep-Link – Logged-In Parent Taps Notification – Calendar Opens at Correct Month

**Description:** AC 02.2 — Regression Analysis — When a logged-in parent taps the Bulk Publish push notification, the app opens the Calendar page at the month of the published period's start date.

**Preconditions:**

- Parent A is logged into the Parent App on Device 2
- The Bulk Publish period start date is May 1, 2026
- Parent A has received the Bulk Publish push notification in their Parent App

| #   | Action                                                                         | Expected Result                                                                  | Test Data |
| --- | ------------------------------------------------------------------------------ | -------------------------------------------------------------------------------- | --------- |
| 1   | On Device 2, tap the Bulk Publish push notification from the notification tray | Parent App opens                                                                 | ""        |
| 2   | Observe the screen that opens                                                  | The **Calendar page** is displayed at **May 2026** (the month of the start date) | ""        |
| 3   | Observe which date is selected / highlighted on the calendar                   | The start date **May 1, 2026** is selected or highlighted                        | ""        |

**Severity:** major
**Priority:** high

---

### [Riso] Bulk Publish Notification – Deep-Link – User Not Logged In Taps Notification – Redirected to Login, Then Calendar

**Description:** AC 02.2 — Regression Analysis — When a user who is not currently logged in taps the Bulk Publish push notification, the app shows the login screen first and then redirects to the Calendar page at the correct month after successful login.

**Preconditions:**

- Student A is **logged out** from the Learner App on Device 1 (app installed but not logged in)
- Student A has a pending Bulk Publish push notification in the device notification tray

| #   | Action                                                                         | Expected Result                                                                          | Test Data             |
| --- | ------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- | --------------------- |
| 1   | On Device 1, tap the Bulk Publish push notification from the notification tray | Learner App opens; **Login screen** is displayed                                         | ""                    |
| 2   | Enter valid credentials and log in as Student A                                | Login succeeds                                                                           | Student A credentials |
| 3   | Observe the screen after successful login                                      | App navigates to the **Calendar page** at the month of the published period's start date | ""                    |

**Severity:** minor
**Priority:** medium

---

### [Riso] Bulk Publish Notification – Deep-Link – Parent Viewing Different Student's Calendar – Tapping Notification Switches to Correct Student's Calendar

**Description:** AC 02.2 — Regression Analysis — When a parent who manages multiple student accounts taps a Bulk Publish notification sent for Student A, the app switches the view to Student A's calendar (even if the parent was previously viewing Student B's calendar).

**Preconditions:**

- Parent A manages two student accounts: Student A and Student B in the Parent App
- Parent A is currently viewing **Student B's** Calendar in the Parent App on Device 1
- A Bulk Publish notification for **Student A** is pending in the notification tray

| #   | Action                                                                                                | Expected Result                                                                                                      | Test Data |
| --- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | While viewing Student B's calendar in the Parent App, tap the Bulk Publish notification for Student A | App responds to the tap                                                                                              | ""        |
| 2   | Observe which student's data is displayed                                                             | The app **switches to Student A's context** and opens Student A's **Calendar** at the published period's start month | ""        |
| 3   | Confirm it is Student A's calendar and not Student B's                                                | Student A's name is shown as the active student; Student A's calendar data is displayed                              | ""        |

**Severity:** major
**Priority:** high

---
