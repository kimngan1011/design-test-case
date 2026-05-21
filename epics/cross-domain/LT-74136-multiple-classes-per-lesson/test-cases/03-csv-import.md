# Test Cases: LT-74136 — Multiple Classes per Lesson

## Suite: CSV Import

---

### Multiple Classes – CSV Import – Group Method – Semicolon-Delimited Classes – Two LSC Records Created

**Description:** AC 01.2 / AC 03.1 — CRUD Testing — Validates that a CSV import with Teaching Method = Group and two semicolon-separated class names results in two Lesson Schedule Class records and the correct Class formula value on the lesson.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- "Class Alpha" and "Class Beta" both exist under "Test Course MC" in SF
- A CSV file is prepared with the following relevant column values: Teaching Method = "Group", Class = "Class Alpha;Class Beta", and all other required lesson fields
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                               | Expected Result                                                                 | Test Data                  |
| --- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------- | -------------------------- |
| 1   | Navigate to the SF Import Wizard (Lesson import)                                     | Import Wizard page is displayed                                                 | ""                         |
| 2   | Select and upload the prepared CSV file                                              | CSV file uploads; column preview is shown                                       | File: lesson-mc-import.csv |
| 3   | Map the CSV columns to SF fields (Teaching Method, Class, and all required fields)   | Column mapping is complete with no errors                                       | ""                         |
| 4   | Click Run Import                                                                     | Import runs; success message is shown with count of created records             | ""                         |
| 5   | Navigate to the newly imported Lesson Schedule record                                | Lesson Schedule Detail page is displayed                                        | ""                         |
| 6   | Open the "Lesson Schedule Class" related list on the Lesson Schedule                 | Related list is visible                                                         | ""                         |
| 7   | Count the LSC records and read their Class values                                    | 2 LSC records exist: one linked to "Class Alpha" and one linked to "Class Beta" | ""                         |
| 8   | Navigate to the Lesson record created by the import and read its Class formula field | Class formula field shows "Class Alpha, Class Beta"                             | ""                         |

**Severity:** major
**Priority:** high

---

### Multiple Classes – CSV Import – Group Method – Two Classes – Students from Both Classes Auto-Assigned After Import

**Description:** AC 01.2 / AC 03.2 — CRUD Testing — Validates that after a multi-class CSV import (Group method), all students enrolled in both imported classes are automatically assigned to the resulting lesson.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- "Class Alpha" has 2 active enrolled students with valid Lesson Allocations
- "Class Beta" has 3 active enrolled students with valid Lesson Allocations
- CSV file prepared: Teaching Method = "Group", Class = "Class Alpha;Class Beta"
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                 | Expected Result                                                                                        | Test Data                  |
| --- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | -------------------------- |
| 1   | Import the multi-class CSV as described above                          | Import succeeds; Lesson Schedule and Lesson are created                                                | File: lesson-mc-import.csv |
| 2   | Wait up to 3 minutes for the auto-assignment batch process to complete | Batch process completes without error                                                                  | ""                         |
| 3   | Navigate to the Lesson created by the import                           | Lesson Detail page is displayed                                                                        | ""                         |
| 4   | Open the Student Session related list                                  | Student Session list is displayed                                                                      | ""                         |
| 5   | Count the Student Sessions and confirm no duplicates                   | Exactly 5 Student Sessions are present (2 from Class Alpha + 3 from Class Beta); no duplicate sessions | ""                         |

**Severity:** major
**Priority:** high

---

### Multiple Classes – CSV Import – Individual Teaching Method – Class Column Ignored – Import Completes Without Class Assignment

**Description:** BR-34 — Negative Testing — Validates that when a CSV is imported with Teaching Method = Individual, the Class field is ignored (hidden for this method), and no Lesson Schedule Class records are created.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- A CSV file is prepared with Teaching Method = "Individual" and Class = "Class Alpha" (class value present in the file)
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                       | Expected Result                                            | Test Data                                         |
| --- | ---------------------------------------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------- |
| 1   | Navigate to the SF Import Wizard (Lesson import)                             | Import Wizard displayed                                    | ""                                                |
| 2   | Upload the CSV with Teaching Method = "Individual" and Class = "Class Alpha" | CSV uploaded; column preview shown                         | Teaching Method = Individual; Class = Class Alpha |
| 3   | Map columns and run the import                                               | Import runs without error; lesson records are created      | ""                                                |
| 4   | Navigate to the Lesson created by the import                                 | Lesson Detail page displayed; Class formula field is empty | ""                                                |
| 5   | Open the "Lesson Schedule Class" related list on the Lesson Schedule         | Related list is empty — no LSC records were created        | ""                                                |

**Severity:** minor
**Priority:** medium

---

### Multiple Classes – CSV Import – Centre Staff Role – Import Access Allowed for All SF Users

**Description:** BR-38 — Permission Matrix — Validates that multi-class CSV import is not restricted to admins; any SF user who can log in (including Centre Staff) can perform the import.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- A user account with "Centre Staff" profile is available (not HQ Admin)
- Valid multi-class CSV prepared: Teaching Method = "Group", Class = "Class Alpha;Class Beta"

| #   | Action                                                                                 | Expected Result                                                                       | Test Data                  |
| --- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- | -------------------------- |
| 1   | Log in to SF using the Centre Staff user account                                       | Successfully logged in as Centre Staff                                                | User: Centre Staff         |
| 2   | Navigate to the SF Import Wizard (Lesson import)                                       | Import Wizard is accessible to Centre Staff (no permission error)                     | ""                         |
| 3   | Upload the multi-class CSV (Teaching Method = Group, Class = "Class Alpha;Class Beta") | CSV uploads without error                                                             | File: lesson-mc-import.csv |
| 4   | Map columns and run the import                                                         | Import completes successfully; Lesson Schedule, 2 LSC records, and Lesson are created | ""                         |

**Severity:** minor
**Priority:** medium

---

### Multiple Classes – CSV Import – New Import Flow – LSC Records Created Between Lesson Schedule and Lesson Steps

**Description:** BR-07 — CRUD Testing — Validates that the updated 5-step import flow creates Lesson Schedule Class records as an intermediate step between the Lesson Schedule and the Lesson, and that the Lesson's Class formula is sourced from those LSC records.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- CSV with Group method, 2 classes (semicolon-separated), teacher username, and student sessions
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                           | Expected Result                                                                                                       | Test Data                  |
| --- | -------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| 1   | Import the multi-class CSV                                                       | Import succeeds with no errors                                                                                        | File: lesson-mc-import.csv |
| 2   | Navigate to the imported Lesson Schedule record                                  | Lesson Schedule Detail page is displayed                                                                              | ""                         |
| 3   | Open the "Lesson Schedule Class" related list                                    | Related list shows 2 LSC records (one for each imported class) — confirming the LSC creation step ran                 | ""                         |
| 4   | Navigate to the Lesson created from this import and read the Class formula field | Class formula field shows the comma-separated class names derived from the 2 LSC records (not from a direct LS field) | ""                         |
| 5   | Open the Lesson Teacher related list on the Lesson                               | Lesson Teacher records exist as imported                                                                              | ""                         |
| 6   | Open the Student Session related list on the Lesson                              | Student Session records exist (auto-assigned via the batch after LSC creation)                                        | ""                         |

**Severity:** major
**Priority:** high
