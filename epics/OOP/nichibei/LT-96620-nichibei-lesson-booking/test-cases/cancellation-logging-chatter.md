# Test Cases: LT-104607 — [Nichibei] Cancellation Logging: Notify CM via Chatter

## Suite: Cancellation Logging – CM Chatter Notification

### [Nichibei] Lesson Booking – Cancellation Logging – Student self-cancels via app – Chatter post created for CM

**Description:** AC 07.1 — CRUD Testing: When a student self-cancels a booking via the app, a Chatter post must be created on Salesforce for the lesson's CM.

**Preconditions:**
Lesson at Location L1; CM1 assigned directly to L1.
Student A has booked the lesson; within cancellation deadline.
No existing Chatter post on the lesson under topic 予約授業のキャンセル.

| #   | Action                                                                    | Expected Result                                                | Test Data |
| --- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------ | --------- |
| 1   | Confirm no existing Chatter post on the lesson under topic 予約授業のキャンセル | 0 posts under this topic for the lesson                            | —         |
| 2   | Student A cancels the booking via app (Cancel → Cancel Reservation)          | Cancellation confirmed; Student Session deleted                    | —         |
| 3   | Check the Lesson's Chatter/Activity tab in Salesforce                        | 1 new Chatter post created, Related To = this Lesson               | —         |

---

### [Nichibei] Lesson Booking – Cancellation Logging – Staff manually removes Student Session via SF – No Chatter post created

**Description:** AC 07.1 — Negative Testing / Regression (mirrors Qase Case 20924 pattern for teacher notifications): Staff-initiated removal of a Student Session via Salesforce must NOT trigger the Chatter post.

**Preconditions:**
Lesson at Location L1; CM1 assigned to L1.
Student A has a Student Session (Booking_Flag=TRUE).
No existing Chatter post on the lesson.

| #   | Action                                                                       | Expected Result                          | Test Data |
| --- | ---------------------------------------------------------------------------------- | -------------------------------------------- | --------- |
| 1   | Confirm no Chatter post on the lesson under topic 予約授業のキャンセル                  | 0 posts                                      | —         |
| 2   | Staff deletes Student Session (Student A) directly from Salesforce (not via app)  | Session removed from Salesforce              | —         |
| 3   | Check the Lesson's Chatter/Activity tab                                           | No new Chatter post created (still 0 posts)  | —         |

---

### [Nichibei] Lesson Booking – Cancellation Logging – Chatter post content – Hardcoded Japanese regardless of CM's language setting

**Description:** AC 07.2 — Equivalence Partitioning: The Chatter post content must be hardcoded in Japanese regardless of the viewing CM's Salesforce language setting.

**Preconditions:**
CM1's Salesforce user profile language = English.
Lesson at Location L1 (CM1 assigned).
Student A has booked the lesson; within cancellation deadline.

| #   | Action                                                        | Expected Result                                                                              | Test Data |
| --- | ---------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | --------- |
| 1   | Confirm CM1's Salesforce user language setting                   | Language = English                                                                                  | —         |
| 2   | Student A cancels the booking via app                            | Cancellation confirmed; Chatter post created                                                       | —         |
| 3   | CM1 opens the Chatter post                                        | Content reads exactly: "[Student Name]が[Lesson Name]をキャンセルしました。" in Japanese, regardless of CM1's English UI language | —         |

---

### [Nichibei] Lesson Booking – Cancellation Logging – Chatter post content – Student Name and Lesson Name are hyperlinked to correct records

**Description:** AC 07.2 — Component: The [Student Name] token must be hyperlinked to the Student's LA record; the [Lesson Name] token must be hyperlinked to the Lesson detail record.

**Preconditions:**
Student A (LA record LA-A) has booked Lesson 1; within cancellation deadline.
CM1 assigned to Lesson 1's location.

| #   | Action                                                     | Expected Result                                            | Test Data |
| --- | -------------------------------------------------------------- | ---------------------------------------------------------------- | --------- |
| 1   | Student A cancels the booking via app                          | Cancellation confirmed; Chatter post created                     | —         |
| 2   | Open the Chatter post and click the Student Name link          | Navigates to Student A's LA record (LA-A)                        | —         |
| 3   | Return to the Chatter post and click the Lesson Name link      | Navigates to Lesson 1's detail record                             | —         |

---

### [Nichibei] Lesson Booking – Cancellation Logging – Chatter post Related To Lesson – Appears in Lesson Detail Activity tab automatically

**Description:** AC 07.3 — CRUD Testing: The Chatter post's "Related To" must be set to the target Lesson record so it surfaces automatically in the Lesson Detail's Chatter/Activity tab, with no extra sync step.

**Preconditions:**
Student A has booked Lesson 1.
CM1 assigned to Lesson 1's location.
Within cancellation deadline.

| #   | Action                                                | Expected Result                                                          | Test Data |
| --- | ---------------------------------------------------------- | ------------------------------------------------------------------------------ | --------- |
| 1   | Student A cancels the booking via app                      | Cancellation confirmed; Chatter post created                                    | —         |
| 2   | Open Lesson 1's detail record in Salesforce                | Lesson detail page opens                                                        | —         |
| 3   | Open the Chatter/Activity tab on the Lesson detail page    | The new Chatter post is shown automatically, with no manual sync/linking step   | —         |

---

### [Nichibei] Lesson Booking – Cancellation Logging – Chatter post grouped under Topic 予約授業のキャンセル

**Description:** AC 07.3 — Equivalence Partitioning: Every cancellation Chatter post must be grouped under the fixed Topic 予約授業のキャンセル.

**Preconditions:**
An existing Chatter post from a prior cancellation is already grouped under topic 予約授業のキャンセル.
Student A has booked Lesson 2 and now cancels it; within cancellation deadline.

| #   | Action                                                              | Expected Result                                                          | Test Data |
| --- | ------------------------------------------------------------------------ | -------------------------------------------------------------------------- | --------- |
| 1   | Student A cancels the booking on Lesson 2 via app                        | Cancellation confirmed; new Chatter post created                           | —         |
| 2   | Open the Topic page for 予約授業のキャンセル in Salesforce                    | Topic page opens                                                            | —         |
| 3   | Verify the new Chatter post appears grouped under this topic, alongside the prior cancellation post | Both posts listed under the 予約授業のキャンセル topic                       | —         |

---

### [Nichibei] Lesson Booking – Cancellation Logging – CM Recipient – CM assigned directly to Location receives Chatter post

**Description:** AC 07.4 — Decision Table (case 1/4): A CM assigned directly to the lesson's Location must receive/be mentioned on the Chatter post.

**Preconditions:**
Location L1 has CM1 assigned directly (no separate Brand-level CM assigned for L1's Brand).
Student A has booked a lesson at L1; within cancellation deadline.

| #   | Action                                                                                | Expected Result                                             | Test Data |
| --- | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------- | --------- |
| 1   | Confirm CM1 is assigned directly to Location L1; no CM assigned at L1's parent Brand       | Location-level CM = CM1; Brand-level CM = none                    | —         |
| 2   | Student A cancels the booking via app                                                      | Cancellation confirmed; Chatter post created                      | —         |
| 3   | Verify the Chatter post recipient/mention                                                  | CM1 is a recipient/mentioned on the post                          | —         |

---

### [Nichibei] Lesson Booking – Cancellation Logging – CM Recipient – CM assigned only at Brand level (not Location) still receives Chatter post

**Description:** AC 07.4 — Decision Table (case 2/4): A CM assigned only at the Brand level (not directly to the Location) must still receive/be mentioned on the Chatter post for lessons at that Brand's locations.

**Preconditions:**
Location L2 belongs to Brand B1.
No CM assigned directly to L2.
CM2 is assigned to Brand B1.
Student A has booked a lesson at L2; within cancellation deadline.

| #   | Action                                                                              | Expected Result                                             | Test Data |
| --- | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------- | --------- |
| 1   | Confirm no CM assigned directly to L2; CM2 assigned at L2's parent Brand B1               | Location-level CM = none; Brand-level CM = CM2                    | —         |
| 2   | Student A cancels the booking via app                                                      | Cancellation confirmed; Chatter post created                      | —         |
| 3   | Verify the Chatter post recipient/mention                                                  | CM2 is a recipient/mentioned on the post                          | —         |

---

### [Nichibei] Lesson Booking – Cancellation Logging – CM Recipient – No CM at Location or Brand level – No Chatter post created

**Description:** AC 07.4 — Decision Table (case 3/4), Negative Testing, Critical risk: When no CM resolves at either the Location or the Brand level, no Chatter post must be created for the cancellation.

**Preconditions:**
Location L3 belongs to Brand B2.
No CM assigned to L3 directly, and no CM assigned to Brand B2.
Student A has booked a lesson at L3; within cancellation deadline.

| #   | Action                                                                    | Expected Result                                       | Test Data |
| --- | -------------------------------------------------------------------------------- | ------------------------------------------------------------ | --------- |
| 1   | Confirm no CM resolves for L3 at either Location or Brand level                  | Location-level CM = none; Brand-level CM = none               | —         |
| 2   | Student A cancels the booking via app                                            | Cancellation confirmed; Student Session deleted                | —         |
| 3   | Check the Lesson's Chatter/Activity tab                                          | No Chatter post is created for this cancellation                | —         |

---

### [Nichibei] Lesson Booking – Cancellation Logging – CM Recipient – CM assigned at both Location and Brand level – Exactly one Chatter post mentioning both CMs

**Description:** AC 07.4 — Decision Table (case 4/4), Critical risk: When a CM is assigned directly to the Location AND a different CM is assigned at the Brand level, exactly ONE Chatter post must be created, mentioning both CMs — not two separate posts.

**Preconditions:**
Location L4 belongs to Brand B3.
CM3 is assigned directly to L4.
CM4 (a different person from CM3) is assigned to Brand B3.
Student A has booked a lesson at L4; within cancellation deadline.

| #   | Action                                                                                    | Expected Result                                             | Test Data |
| --- | ------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------- | --------- |
| 1   | Confirm CM3 assigned directly to L4 and CM4 (different person) assigned to Brand B3              | Location-level CM = CM3; Brand-level CM = CM4                     | —         |
| 2   | Student A cancels the booking via app                                                            | Cancellation confirmed; Student Session deleted                    | —         |
| 3   | Check the Lesson's Chatter/Activity tab                                                          | Exactly ONE new Chatter post is created (not two)                  | —         |
| 4   | Open the Chatter post and check mentions/recipients                                              | Both CM3 and CM4 are mentioned/recipients on the same post          | —         |

---

### [Nichibei] Lesson Booking – Cancellation Logging – Teacher receives no notification and is not mentioned on the CM Chatter post

**Description:** AC 07.4 — Regression Analysis: Confirms the teacher is excluded from both the CM Chatter post AND the (now-removed) SF teacher notification on cancellation — no notification of any kind reaches the teacher.

**Preconditions:**
Lesson has Teacher A assigned and CM1 assigned to its Location.
Student A has booked the lesson; within cancellation deadline.

| #   | Action                                                              | Expected Result                                                                                     | Test Data |
| --- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | --------- |
| 1   | Student A cancels the booking via app                                      | Cancellation confirmed                                                                                   | —         |
| 2   | Check Teacher A's Salesforce notification inbox                            | No notification received by Teacher A (teacher SF notification removed, PM update 2026-07-01)           | —         |
| 3   | Check the Lesson's Chatter/Activity tab                                    | CM1's Chatter post is created                                                                            | —         |
| 4   | Verify Teacher A is NOT a recipient/mention on the Chatter post             | Teacher A is not listed as a recipient or mention on the post                                            | —         |

---

### [Nichibei] Lesson Booking – Cancellation Logging – Chatter post visibility – Mentioned CM without direct Lesson record access can still view the post

**Description:** AC 07.4 — Permission Matrix: Chatter post visibility follows standard Salesforce LBAC — a CM who is @mentioned can view the post even without direct record-sharing access via role hierarchy alone.

**Preconditions:**
CM5 is mentioned on a cancellation Chatter post (via Brand-level assignment).
CM5 does not have direct sharing access to the Lesson record through role hierarchy alone.

| #   | Action                                                     | Expected Result                                            | Test Data |
| --- | ---------------------------------------------------------------- | ------------------------------------------------------------------ | --------- |
| 1   | CM5 logs into Salesforce                                          | Salesforce home shown                                               | —         |
| 2   | CM5 navigates to their Chatter feed / notifications                | CM5 sees the Chatter post they were mentioned in                    | —         |
| 3   | CM5 opens the mentioned Chatter post                                | Post content and the Related-To Lesson link are visible to CM5      | —         |

---
