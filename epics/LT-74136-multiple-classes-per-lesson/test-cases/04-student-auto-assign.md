# Test Cases: LT-74136 — Multiple Classes per Lesson

## Suite: Student Auto-Assignment

---

### Multiple Classes – Student Auto-Assignment – Lesson Created with Two Classes – All Students from Both Classes Assigned

**Description:** AC 01.3 — CRUD Testing — Validates that when a lesson is created with two classes assigned, all students enrolled in both classes are automatically allocated to the lesson after the batch process completes.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- "Class Alpha" has 3 active students (Student A1, A2, A3) with valid Lesson Allocations for "Test Course MC"
- "Class Beta" has 2 active students (Student B1, B2) with valid Lesson Allocations for "Test Course MC"
- None of these 5 students are currently assigned to any lesson
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                                          | Expected Result                                                                                                    | Test Data                                                 |
| --- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------- |
| 1   | Navigate to Lessons in SF and click "New Lesson"                                                | New Lesson form opens                                                                                              | ""                                                        |
| 2   | Set Teaching Method = "Group", Course = "Test Course MC", and select Class Alpha + Class Beta   | Both classes selected                                                                                              | Teaching Method = Group; Class = Class Alpha + Class Beta |
| 3   | Fill in required fields (Name = "Lesson MC-Auto", Date, Time, Location, Academic Year) and save | Lesson saved; Lesson Detail opens                                                                                  | Name = Lesson MC-Auto                                     |
| 4   | Wait up to 2 minutes for the auto-assignment batch process to complete                          | Batch completes without error                                                                                      | ""                                                        |
| 5   | Navigate to the Student Session related list on "Lesson MC-Auto"                                | Student Session list is displayed                                                                                  | ""                                                        |
| 6   | Count the Student Sessions and read the student names                                           | Exactly 5 Student Sessions are present: Student A1, A2, A3 (from Class Alpha) and Student B1, B2 (from Class Beta) | ""                                                        |

**Severity:** critical
**Priority:** high

---

### Multiple Classes – Student Auto-Assignment – Student in Two Assigned Classes – Single Student Session Created (No Duplicate)

**Description:** AC 01.3 / LT-99546 — Regression Analysis — Validates that when a student is a member of both assigned classes, only one Student Session is created (dedup via unique-key constraint), and the Lesson Allocation count increments by only 1.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- "Class Alpha" has Student X and 2 others; "Class Beta" has Student X and 1 other
- A lesson "Lesson MC-Dedup" is created with both Class Alpha and Class Beta
- Auto-assignment batch has run and completed
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                  | Expected Result                                                                                                    | Test Data           |
| --- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------- |
| 1   | Navigate to the Student Session related list on "Lesson MC-Dedup"       | Student Session list is displayed                                                                                  | ""                  |
| 2   | Search for Student X in the Student Session list                        | Student X appears exactly once in the list (no duplicate entry)                                                    | Student = Student X |
| 3   | Count the total Student Sessions on the lesson                          | Total sessions = 4 (Student X + 2 others from Class Alpha + 1 other from Class Beta) — Student X not counted twice | ""                  |
| 4   | Open the Lesson Allocation record for Student X for the lesson's course | Student X's LA record opens                                                                                        | ""                  |
| 5   | Read the "Lesson Allocated" count on Student X's LA                     | "Lesson Allocated" count incremented by exactly 1 (not 2, even though Student X is in both classes)                | ""                  |

**Severity:** critical
**Priority:** high

---

### Multiple Classes – Student Auto-Assignment – Individual Assign on Contact Page – Student Added to Matching Lessons

**Description:** AC 02.1 (BR-12) — Decision Table — Validates that when a class is individually assigned to a student via their Contact page, the student is automatically assigned to all lessons that have that class via an LSC record.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- Lesson "Lesson MC-01" has Class Alpha assigned via LSC
- "Student Y" is not yet a member of Class Alpha; Student Y has an active Lesson Allocation for "Test Course MC"
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                                 | Expected Result                                                  | Test Data           |
| --- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ------------------- |
| 1   | Navigate to Student Y's Contact page in SF                                             | Contact page for Student Y is displayed                          | Student = Student Y |
| 2   | Use the "Assign Class" action on the Contact page to assign Student Y to "Class Alpha" | Class assignment form opens                                      | ""                  |
| 3   | Select "Class Alpha" and save the assignment                                           | Student Y is added to Class Alpha membership                     | Class = Class Alpha |
| 4   | Wait up to 2 minutes for the auto-assignment batch to complete                         | Batch completes                                                  | ""                  |
| 5   | Navigate to the Student Session related list on "Lesson MC-01"                         | Student Session list displayed                                   | ""                  |
| 6   | Search for Student Y in the list                                                       | A Student Session for Student Y is now present on "Lesson MC-01" | ""                  |

**Severity:** major
**Priority:** high

---

### Multiple Classes – Student Auto-Assignment – Bulk Class Assign on Location Course – All Students Assigned to Matching Lessons

**Description:** AC 02.1 (BR-11) — Decision Table — Validates that when 3 students are bulk-assigned to a class via the Location Course page, all 3 are automatically assigned to lessons that have that class linked via LSC.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- Lesson "Lesson MC-02" has "Class Gamma" assigned via LSC
- Students C1, C2, C3 are not yet members of Class Gamma; all have active LAs for the course
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                                     | Expected Result                                                    | Test Data                                  |
| --- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------ | ------------------------------------------ |
| 1   | Navigate to the Location Course page in SF for the relevant location and course            | Location Course page displayed                                     | ""                                         |
| 2   | Use "Bulk Assign Class" to select students C1, C2, and C3 and assign them to "Class Gamma" | Bulk assignment form completed; 3 students assigned to Class Gamma | Students = C1, C2, C3; Class = Class Gamma |
| 3   | Save the bulk assignment                                                                   | Save confirmed; 3 students are now Class Gamma members             | ""                                         |
| 4   | Wait up to 3 minutes for the auto-assignment batch to complete                             | Batch completes                                                    | ""                                         |
| 5   | Navigate to the Student Session related list on "Lesson MC-02"                             | Student Session list displayed                                     | ""                                         |
| 6   | Count the new sessions for C1, C2, C3                                                      | 3 new Student Sessions are present (one for each assigned student) | ""                                         |

**Severity:** major
**Priority:** high

---

### Multiple Classes – Student Auto-Assignment – Class Member Import – Students Assigned to Matching Lessons

**Description:** AC 02.1 (BR-14) — Decision Table — Validates that when class members are imported via the SF Import Wizard, the imported students are automatically assigned to all lessons that have that class linked via LSC.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- Lesson "Lesson MC-03" has "Class Delta" assigned via LSC; Class Delta currently has no members
- A CSV with 3 students (D1, D2, D3) to be imported as Class Delta members; all 3 have active LAs
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                                      | Expected Result                                                       | Test Data                     |
| --- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | ----------------------------- |
| 1   | Use the SF Import Wizard to import 3 Class Members for "Class Delta" using the prepared CSV | Import Wizard runs; 3 Class Member records created for Class Delta    | File: class-members-delta.csv |
| 2   | Wait up to 3 minutes for the auto-assignment batch to complete                              | Batch completes                                                       | ""                            |
| 3   | Navigate to the Student Session related list on "Lesson MC-03"                              | Student Session list displayed                                        | ""                            |
| 4   | Count the sessions for students D1, D2, D3                                                  | 3 Student Sessions present — one for each imported Class Delta member | ""                            |

**Severity:** major
**Priority:** high

---

### Multiple Classes – Student Auto-Assignment – 100-Student Class – All Students Assigned via Async Batch (BVA at Max Boundary)

**Description:** AC 02.2 (BR-15/16) — Boundary Value Analysis — Validates that the auto-assignment batch processes all 100 students from a class without degradation or missed assignments (boundary value at the stated performance maximum).

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- "Class Large" has exactly 100 enrolled active students, all with valid Lesson Allocations for "Test Course MC"
- No lesson currently has Class Large assigned
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                     | Expected Result                                                           | Test Data                          |
| --- | -------------------------------------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------- |
| 1   | Create a new Group lesson with Class Large assigned and save               | Lesson "Lesson MC-BVA" created; batch triggered                           | Class = Class Large (100 students) |
| 2   | Wait up to 5 minutes for the async batch process to complete               | Batch completes without timeout, system error, or partial failure message | ""                                 |
| 3   | Navigate to the Student Session related list on "Lesson MC-BVA"            | Student Session list displayed                                            | ""                                 |
| 4   | Count the total Student Sessions                                           | Exactly 100 Student Sessions are present; no sessions missing             | ""                                 |
| 5   | Spot-check 5 specific students from Class Large and confirm their sessions | Each spot-checked student has a Student Session on the lesson             | Students: D1, D20, D50, D80, D100  |

**Severity:** major
**Priority:** high
