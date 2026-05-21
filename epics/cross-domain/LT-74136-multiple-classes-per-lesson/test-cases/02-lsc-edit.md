# Test Cases: LT-74136 — Multiple Classes per Lesson

## Suite: LSC Edit (Post-Creation Class Management)

---

### Multiple Classes – LSC Related List – Add Class After Creation – Students from New Class Auto-Assigned to Lesson

**Description:** BR-32/33 — CRUD Testing — Validates that adding a new Lesson Schedule Class record via the related list on an existing lesson automatically assigns all students from that class to the lesson.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- Lesson "Lesson MC-01" exists and has one LSC record for "Class Alpha" (3 students currently assigned)
- "Class Beta" has 3 enrolled active students with valid Lesson Allocations for the lesson's course; none are currently assigned to "Lesson MC-01"
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                    | Expected Result                                                                                           | Test Data          |
| --- | ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | ------------------ |
| 1   | Open the Lesson Detail page for "Lesson MC-01"                            | Lesson Detail page displayed; Class field shows "Class Alpha"                                             | ""                 |
| 2   | Navigate to the "Lesson Schedule Class" related list on the Lesson Detail | Related list is visible with 1 existing LSC record for "Class Alpha"                                      | ""                 |
| 3   | Click "New" to create a new LSC record                                    | New LSC record creation form opens                                                                        | ""                 |
| 4   | Select "Class Beta" in the Class field and save the new LSC record        | New LSC record saved; related list now shows 2 records (Class Alpha and Class Beta)                       | Class = Class Beta |
| 5   | Wait up to 2 minutes for the auto-assignment batch process to complete    | Batch process completes without error                                                                     | ""                 |
| 6   | Navigate to the Student Session related list on "Lesson MC-01"            | Student Session list displayed                                                                            | ""                 |
| 7   | Count the Student Sessions and identify the new ones from Class Beta      | Exactly 3 new Student Sessions from Class Beta are present (one per enrolled student); total sessions = 6 | ""                 |

**Severity:** major
**Priority:** high

---

### Multiple Classes – LSC Related List – Remove Class After Creation – Students Auto-Removed and LA Decremented

**Description:** BR-32/33 — CRUD Testing — Validates that deleting a Lesson Schedule Class record from an existing lesson automatically removes all students from that class and decrements their Lesson Allocation count.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- Lesson "Lesson MC-01" has 2 LSC records: "Class Alpha" (3 students assigned) and "Class Beta" (3 students assigned); total 6 Student Sessions
- "Student B1" is a member of "Class Beta" only; their LA "Lesson Allocated" count is 1 for this lesson
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                                   | Expected Result                                                                                                   | Test Data |
| --- | ---------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | Open the Lesson Detail page for "Lesson MC-01"                                           | Lesson Detail displayed; Class field shows "Class Alpha, Class Beta"                                              | ""        |
| 2   | Navigate to the "Lesson Schedule Class" related list                                     | Related list shows 2 LSC records: Class Alpha and Class Beta                                                      | ""        |
| 3   | Open the LSC record for "Class Beta"                                                     | LSC record detail for Class Beta opens                                                                            | ""        |
| 4   | Delete the LSC record for "Class Beta"                                                   | LSC for Class Beta is deleted; related list now shows only 1 record (Class Alpha)                                 | ""        |
| 5   | Wait up to 2 minutes for the auto-removal batch process to complete                      | Batch process completes                                                                                           | ""        |
| 6   | Navigate to the Student Session related list on "Lesson MC-01"                           | Student Session list displayed                                                                                    | ""        |
| 7   | Count the remaining Student Sessions                                                     | Only 3 Student Sessions remain (Class Alpha students); all 3 Class Beta sessions are removed                      | ""        |
| 8   | Open the Lesson Allocation record for "Student B1" and read the "Lesson Allocated" count | "Student B1"'s LA "Lesson Allocated" count is decremented by 1 (back to the value before the lesson was assigned) | ""        |

**Severity:** critical
**Priority:** high

---

### Multiple Classes – LSC Related List – Add Class Then Remove – Student Sessions Updated After Each Operation

**Description:** BR-32/33 — CRUD Testing — Validates the full lifecycle of adding then removing a class via the LSC related list, confirming that student sessions are correctly updated after each operation.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- Lesson "Lesson MC-01" has 1 LSC record for "Class Alpha" (3 students assigned)
- "Class Beta" has 2 enrolled active students not currently assigned to "Lesson MC-01"
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                    | Expected Result                                                                                                            | Test Data          |
| --- | ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ------------------ |
| 1   | On "Lesson MC-01" LSC related list, add a new LSC record for "Class Beta" | LSC record for Class Beta created; related list shows 2 records                                                            | Class = Class Beta |
| 2   | Wait up to 2 minutes for auto-assignment; then open Student Session list  | 5 Student Sessions total (3 from Class Alpha + 2 from Class Beta); Class field shows "Class Alpha, Class Beta"             | ""                 |
| 3   | Delete the LSC record for "Class Beta" from the related list              | LSC for Class Beta deleted; related list shows 1 record (Class Alpha only)                                                 | ""                 |
| 4   | Wait up to 2 minutes for auto-removal to complete                         | Batch process completes                                                                                                    | ""                 |
| 5   | Open the Student Session related list on "Lesson MC-01"                   | Only 3 Student Sessions remain (Class Alpha students); 2 Class Beta sessions removed; Class field shows "Class Alpha" only | ""                 |

**Severity:** major
**Priority:** high

---

### Multiple Classes – LSC Related List – Remove One Class – Student in Both Classes Remains Assigned via Remaining Class

**Description:** BR-32/33 — CRUD Testing — Validates that when a class is removed from a lesson via the LSC related list, a student who belongs to both the removed class and a remaining class keeps their Student Session (not incorrectly removed).

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- Lesson "Lesson MC-01" has 2 LSC records: "Class Alpha" and "Class Beta"
- "Student X" is a member of both "Class Alpha" and "Class Beta"
- "Student X" has exactly 1 Student Session on "Lesson MC-01" (deduplicated)
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                        | Expected Result                                                                                                                         | Test Data |
| --- | ----------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | Open the "Lesson Schedule Class" related list on "Lesson MC-01"               | Related list shows 2 LSC records: Class Alpha and Class Beta                                                                            | ""        |
| 2   | Delete the LSC record for "Class Beta"                                        | LSC for Class Beta deleted; only Class Alpha remains                                                                                    | ""        |
| 3   | Wait up to 2 minutes for the auto-removal batch to complete                   | Batch process completes                                                                                                                 | ""        |
| 4   | Navigate to the Student Session related list on "Lesson MC-01"                | Student Session list is displayed                                                                                                       | ""        |
| 5   | Find "Student X" in the Student Session list and confirm their session status | "Student X" still has an active Student Session on the lesson (not removed, because they remain in Class Alpha which is still assigned) | ""        |

**Severity:** critical
**Priority:** high

---

### Multiple Classes – LSC Related List – Add Class via SF – BO Lesson Detail Shows Updated Class Names

**Description:** BR-32 — CRUD Testing — Validates that after adding a class via the SF LSC related list, the Back Office Lesson Detail reflects the updated comma-separated class list after sync.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag TRUE and Unleash flag `Lesson_BackOffice_LessonSF_MultipleClassesSF` is ON
- Lesson "Lesson MC-01" has 1 LSC record for "Class Alpha"; BO Lesson Detail shows "Class Alpha"
- Logged in as HQ or CM Staff to SF and BO

| #   | Action                                                                  | Expected Result                                                                | Test Data          |
| --- | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ------------------ |
| 1   | On SF, open the "Lesson Schedule Class" related list for "Lesson MC-01" | Related list shows 1 LSC record for Class Alpha                                | ""                 |
| 2   | Add a new LSC record for "Class Beta" and save                          | LSC record saved; SF Lesson Detail Class field shows "Class Alpha, Class Beta" | Class = Class Beta |
| 3   | Wait 1–2 minutes for SF-to-BO sync to complete                          | Sync completes                                                                 | ""                 |
| 4   | Navigate to BO Lesson Detail for "Lesson MC-01"                         | BO Lesson Detail page is displayed                                             | ""                 |
| 5   | Read the Class field value in BO Lesson Detail                          | BO shows "Class Alpha, Class Beta" — consistent with SF                        | ""                 |

**Severity:** major
**Priority:** high
