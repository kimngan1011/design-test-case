# Test Cases: LT-74136 — Multiple Classes per Lesson

## Suite: Lesson Creation

---

### Multiple Classes – Lesson Creation – Group Method – Two Classes Selected – Both Classes Visible on Lesson Detail

**Description:** AC 01.1 — Decision Table — Validates that a Group lesson can be created with two classes selected from the same course, and both classes are visible on the Lesson Detail.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- Course "Test Course MC" exists with two classes: "Class Alpha" and "Class Beta"
- Both "Class Alpha" and "Class Beta" are active under "Test Course MC"
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                                                                      | Expected Result                                                                  | Test Data                       |
| --- | --------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ------------------------------- |
| 1   | Navigate to the Lessons tab in SF                                                                                           | Lesson List page is displayed                                                    | ""                              |
| 2   | Click "New Lesson"                                                                                                          | New Lesson creation form opens                                                   | ""                              |
| 3   | Set Teaching Method to "Group"                                                                                              | Teaching Method field shows "Group"                                              | Teaching Method = Group         |
| 4   | Set Course to "Test Course MC"                                                                                              | Course field shows "Test Course MC"; Class field becomes available               | Course = Test Course MC         |
| 5   | Click the Class field and select "Class Alpha", then select "Class Beta"                                                    | Both "Class Alpha" and "Class Beta" appear as selected values in the Class field | Class = Class Alpha, Class Beta |
| 6   | Fill in all remaining required fields (Name = "Lesson MC-01", Date, Start/End Time, Location, Academic Year) and click Save | Lesson is saved; Lesson Detail page for "Lesson MC-01" opens                     | Name = Lesson MC-01             |
| 7   | Locate the Class field on the Lesson Detail page                                                                            | Class field is visible                                                           | ""                              |
| 8   | Read the value of the Class field                                                                                           | Class field shows "Class Alpha, Class Beta" (comma-separated)                    | ""                              |

**Severity:** major
**Priority:** high

---

### Multiple Classes – Lesson Schedule – Recurring Chain – Two Classes Propagated to All Lessons

**Description:** AC 01.1 — State Transition Testing — Validates that when a Lesson Schedule is created with two classes selected, every lesson generated in the recurring chain inherits both classes.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- Course "Test Course MC" with "Class Alpha" and "Class Beta" active
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                                                    | Expected Result                                        | Test Data                                                                          |
| --- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| 1   | Navigate to Lesson Schedules in SF and click "New Lesson Schedule"                                        | New Lesson Schedule form opens                         | ""                                                                                 |
| 2   | Set Teaching Method = "Group", Course = "Test Course MC", and select Class = "Class Alpha" + "Class Beta" | Both classes selected                                  | Teaching Method = Group; Course = Test Course MC; Class = Class Alpha + Class Beta |
| 3   | Set recurrence to Weekly, lesson count = 3, set Start Date and other required fields                      | Recurrence settings configured; form is filled         | Lesson Count = 3                                                                   |
| 4   | Click Save                                                                                                | Lesson Schedule saved; 3 lesson records auto-generated | ""                                                                                 |
| 5   | Navigate to the Lessons related list on the Lesson Schedule Detail                                        | Related list shows 3 lessons                           | ""                                                                                 |
| 6   | Open Lesson 1 and read the Class field                                                                    | Lesson 1 Class field shows "Class Alpha, Class Beta"   | ""                                                                                 |
| 7   | Go back and open Lesson 2 and read the Class field                                                        | Lesson 2 Class field shows "Class Alpha, Class Beta"   | ""                                                                                 |
| 8   | Go back and open Lesson 3 and read the Class field                                                        | Lesson 3 Class field shows "Class Alpha, Class Beta"   | ""                                                                                 |

**Severity:** major
**Priority:** high

---

### Multiple Classes – Lesson Form – Course Field – Non-Editable After Lesson Save

**Description:** AC 01.1 — Negative Testing — Validates that the Course field on a lesson cannot be changed after the lesson has been saved.

**Preconditions:**

- SF org with an existing lesson "Lesson MC-01" that has Course = "Test Course MC"
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                         | Expected Result                                                                   | Test Data |
| --- | ---------------------------------------------- | --------------------------------------------------------------------------------- | --------- |
| 1   | Open the Lesson Detail page for "Lesson MC-01" | Lesson Detail page is displayed                                                   | ""        |
| 2   | Click Edit on the Lesson                       | Lesson edit form opens                                                            | ""        |
| 3   | Attempt to locate and change the Course field  | The Course field is read-only; no dropdown or edit control is available           | ""        |
| 4   | Cancel the edit                                | Edit form closed; Lesson Detail page returns with original Course value unchanged | ""        |

**Severity:** minor
**Priority:** medium

---

### Multiple Classes – Lesson Form – Class Field – Non-Editable via Lesson Form After Save

**Description:** AC 01.1 — Negative Testing — Validates that the Class field on a lesson cannot be changed through the standard lesson edit form after the lesson is saved. Class changes must be made via the LSC related list.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- Existing lesson "Lesson MC-01" with Class Alpha and Class Beta assigned (via LSC records)
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                        | Expected Result                                                                                    | Test Data |
| --- | ------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | --------- |
| 1   | Open the Lesson Detail page for "Lesson MC-01"                | Lesson Detail page displayed; Class field shows "Class Alpha, Class Beta"                          | ""        |
| 2   | Click Edit on the Lesson                                      | Lesson edit form opens                                                                             | ""        |
| 3   | Attempt to locate and modify the Class field on the edit form | The Class field is read-only on the edit form; it cannot be changed or cleared via the lesson form | ""        |
| 4   | Cancel the edit without saving                                | Edit closed; Class field on Lesson Detail still shows "Class Alpha, Class Beta"                    | ""        |

**Severity:** minor
**Priority:** medium

---

### Multiple Classes – Formula Field – Two Classes Assigned – Comma-Separated Names Displayed

**Description:** AC 04.2 — Regression Analysis — Validates that the Class formula field on a Lesson correctly shows comma-separated class names when the lesson has two Lesson Schedule Class (LSC) records.

**Preconditions:**

- SF org post-migration; `Multiple_Classes_In_Lesson__c` flag TRUE
- Lesson "Lesson MC-01" has two LSC records: one for "Class Alpha" and one for "Class Beta"
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                      | Expected Result                                                                                  | Test Data |
| --- | ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | --------- |
| 1   | Navigate to the Lesson Detail page for "Lesson MC-01" in SF | Lesson Detail page is displayed                                                                  | ""        |
| 2   | Locate the "Class" formula field on the Lesson Detail       | Class field is visible                                                                           | ""        |
| 3   | Read the displayed value of the Class field                 | Class field shows "Class Alpha, Class Beta" (comma-separated names matching the two LSC records) | ""        |

**Severity:** critical
**Priority:** high

---

### Multiple Classes – Formula Field – Single-Class Lesson – Single Class Name Displayed (Backward Compatibility)

**Description:** AC 04.2 — Regression Analysis — Validates that the Class formula field on a single-class lesson (migrated from the old model) shows only the single class name with no trailing comma or extra formatting.

**Preconditions:**

- SF org post-migration
- An existing lesson "Lesson MC-Legacy" that was created before the multi-class feature and has been migrated; it has exactly 1 LSC record for "Class Alpha"
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                          | Expected Result                                                                            | Test Data |
| --- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | --------- |
| 1   | Navigate to the Lesson Detail page for "Lesson MC-Legacy" in SF | Lesson Detail page is displayed                                                            | ""        |
| 2   | Locate the "Class" formula field                                | Class field is visible                                                                     | ""        |
| 3   | Read the value of the Class field                               | Class field shows "Class Alpha" only — no trailing comma, no extra space, no empty bracket | ""        |
| 4   | Navigate to BO Lesson Detail for "Lesson MC-Legacy"             | BO Lesson Detail page is displayed                                                         | ""        |
| 5   | Read the Class field value in BO                                | BO Class field shows "Class Alpha" — consistent with SF display                            | ""        |

**Severity:** critical
**Priority:** high
