# Test Cases: LT-96620 — [Nichibei] Lesson Booking System

## Suite: Bookable Flag & Access Control

### [Nichibei] Lesson Booking – Bookable Flag – New lesson – Default OFF

**Description:** AC 06.1 — CRUD Testing: When creating a new lesson in Salesforce, the Bookable Flag checkbox must default to OFF (unchecked).

**Preconditions:**
Staff user with Lesson edit permission is creating a new lesson in Salesforce.

| #   | Action                                              | Expected Result                                      | Test Data |
| --- | --------------------------------------------------- | ---------------------------------------------------- | --------- |
| 1   | Open Salesforce and navigate to create a new Lesson | Lesson creation form opened                          | —         |
| 2   | View the Bookable Flag field                        | Bookable Flag checkbox is unchecked (OFF) by default | —         |

---

### [Nichibei] Lesson Booking – Bookable Flag – Turned ON – Lesson appears in Browse

**Description:** AC 06.1 — BR-5: State Transition: After turning Bookable Flag ON for a lesson, it becomes visible in the student's Browse Lessons list (assuming all other visibility conditions are met).

**Preconditions:**
A lesson at student's LA location (Published, date = 2026-05-12) has Bookable_Flag=FALSE. Student cannot see it in Browse.

| #   | Action                                                                | Expected Result                         | Test Data |
| --- | --------------------------------------------------------------------- | --------------------------------------- | --------- |
| 1   | Confirm lesson is NOT visible in Browse Lessons (Bookable_Flag=FALSE) | Lesson not shown in Browse              | —         |
| 2   | Staff turns Bookable Flag ON for the lesson in Salesforce             | Flag updated to TRUE                    | —         |
| 3   | Student refreshes Browse Lessons                                      | Lesson is now visible in Browse Lessons | —         |

---

### [Nichibei] Lesson Booking – Bookable Flag – Turned OFF – Existing sessions unaffected

**Description:** AC 06.1 — BR-25: CRUD Testing / Negative Testing: When staff turns Bookable Flag OFF for a lesson that already has booked Student Sessions, the existing sessions must NOT be deleted.

**Preconditions:**
A lesson has Bookable_Flag=TRUE and 2 existing Student Sessions (2 students have booked).

| #   | Action                                                        | Expected Result                                          | Test Data |
| --- | ------------------------------------------------------------- | -------------------------------------------------------- | --------- |
| 1   | Confirm 2 Student Sessions exist in Salesforce for the lesson | Sessions present with Booking_Flag=TRUE                  | —         |
| 2   | Staff turns Bookable Flag OFF for the lesson in Salesforce    | Flag updated to FALSE                                    | —         |
| 3   | Verify Student Sessions in Salesforce after flag change       | Both Student Sessions still exist; no sessions deleted   | —         |
| 4   | Verify Booking List for affected students                     | Both students still see the lesson in their Booking List | —         |

---

### [Nichibei] Lesson Booking – Bookable Flag – Turned OFF – Lesson no longer shown in Browse

**Description:** AC 06.1 — BR-5: State Transition: After turning Bookable Flag OFF, the lesson must NOT appear in new Browse searches.

**Preconditions:**
A lesson at student's LA location (Published, date = 2026-05-12) has Bookable_Flag=TRUE and is visible in Browse.

| #   | Action                                                           | Expected Result                               | Test Data |
| --- | ---------------------------------------------------------------- | --------------------------------------------- | --------- |
| 1   | Confirm lesson IS visible in Browse Lessons (Bookable_Flag=TRUE) | Lesson shown in Browse                        | —         |
| 2   | Staff turns Bookable Flag OFF in Salesforce                      | Flag updated to FALSE                         | —         |
| 3   | Student refreshes Browse Lessons                                 | Lesson is no longer visible in Browse Lessons | —         |

---

### [Nichibei] Lesson Booking – Bookable Flag – Flag change history tracked in Salesforce

**Description:** AC 06.1 — CRUD Testing: Changes to the Bookable Flag field must be tracked via Salesforce field history.

**Preconditions:**
A lesson exists with Bookable_Flag=FALSE.

| #   | Action                                                       | Expected Result                                                                 | Test Data |
| --- | ------------------------------------------------------------ | ------------------------------------------------------------------------------- | --------- |
| 1   | Turn Bookable Flag ON for the lesson in Salesforce           | Flag updated to TRUE                                                            | —         |
| 2   | Turn Bookable Flag OFF for the lesson in Salesforce          | Flag updated to FALSE                                                           | —         |
| 3   | Open Salesforce field history for the lesson's Bookable Flag | History log shows both changes (FALSE→TRUE, TRUE→FALSE) with timestamp and user | —         |

---

### [Nichibei] Lesson Booking – Access Control – Feature disabled – Lesson Booking menu hidden

**Description:** PRD/Config — BR-28: Decision Table: When the Lesson Booking feature is disabled for the partner, the Lesson Booking menu must NOT appear in the student's app navigation.

**Preconditions:**
Lesson Booking feature flag is set to DISABLED for the Nichibei partner org.

| #   | Action                                                          | Expected Result                            | Test Data               |
| --- | --------------------------------------------------------------- | ------------------------------------------ | ----------------------- |
| 1   | Login to app as a student user (Nichibei org, feature disabled) | App home screen shown                      | Feature flag = disabled |
| 2   | View app navigation / main menu                                 | "Lesson Booking" menu entry is NOT visible | —                       |

---

### [Nichibei] Lesson Booking – Access Control – Feature enabled – Lesson Booking menu visible

**Description:** PRD/Config — BR-28: Decision Table: When the Lesson Booking feature is enabled for the partner, the Lesson Booking menu must appear in the student's app navigation.

**Preconditions:**
Lesson Booking feature flag is set to ENABLED for the Nichibei partner org.

| #   | Action                                                         | Expected Result                        | Test Data              |
| --- | -------------------------------------------------------------- | -------------------------------------- | ---------------------- |
| 1   | Login to app as a student user (Nichibei org, feature enabled) | App home screen shown                  | Feature flag = enabled |
| 2   | View app navigation / main menu                                | "Lesson Booking" menu entry IS visible | —                      |

---

### [Nichibei] Lesson Booking – Access Control – Parent user – Lesson Booking menu not accessible

**Description:** Confirmed — BR-29: Permission Matrix: Parent users must NOT have access to the Lesson Booking feature. The menu must not appear for parent accounts.

**Preconditions:**
Lesson Booking feature is enabled. A parent user account is linked to a student.

| #   | Action                                                        | Expected Result                                       | Test Data      |
| --- | ------------------------------------------------------------- | ----------------------------------------------------- | -------------- |
| 1   | Login to app as a parent user (Nichibei org, feature enabled) | App home screen shown                                 | Role = Parent  |
| 2   | View app navigation / main menu                               | "Lesson Booking" menu entry is NOT visible for parent | —              |
| 3   | Login to app as the linked student user                       | App home screen shown                                 | Role = Student |
| 4   | View app navigation / main menu                               | "Lesson Booking" menu entry IS visible for student    | —              |
