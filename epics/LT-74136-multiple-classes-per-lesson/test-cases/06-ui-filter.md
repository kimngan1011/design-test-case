# Test Cases: LT-74136 — Multiple Classes per Lesson

## Suite: UI Display and Filter

---

### Multiple Classes – SF Lesson List – Multi-Class Lesson Row – Comma-Separated Class Names Displayed

**Description:** AC 05.1 (BR-27) — CRUD Testing — Validates that the Class column in the SF Lesson List shows comma-separated class names for a lesson that has two classes assigned.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- Lesson "Lesson MC-01" has 2 LSC records: Class Alpha and Class Beta
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                         | Expected Result                              | Test Data |
| --- | ---------------------------------------------- | -------------------------------------------- | --------- |
| 1   | Navigate to the SF Lessons List                | Lesson List page is displayed                | ""        |
| 2   | Locate the row for "Lesson MC-01"              | "Lesson MC-01" row is visible                | ""        |
| 3   | Read the Class column value for "Lesson MC-01" | Class column shows "Class Alpha, Class Beta" | ""        |

**Severity:** minor
**Priority:** medium

---

### Multiple Classes – SF Lesson Detail – Multi-Class Lesson – Class Field Shows Comma-Separated Names

**Description:** AC 05.1 (BR-27) — CRUD Testing — Validates that the Class field on the SF Lesson Detail page displays all assigned class names, comma-separated.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- Lesson "Lesson MC-01" has Class Alpha and Class Beta assigned via LSC
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                            | Expected Result                             | Test Data |
| --- | ------------------------------------------------- | ------------------------------------------- | --------- |
| 1   | Open the SF Lesson Detail page for "Lesson MC-01" | Lesson Detail page is displayed             | ""        |
| 2   | Read the "Class" field value                      | Class field shows "Class Alpha, Class Beta" | ""        |

**Severity:** minor
**Priority:** medium

---

### Multiple Classes – SF Calendar Filter – Single Class Selected – Lessons Containing That Class Are Shown

**Description:** AC 05.1 (BR-28) — Decision Table — Validates that filtering the SF Mana Calendar by a single class shows all lessons that contain that class, including multi-class lessons that also have other classes.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- 3 lessons exist in the same time range: Lesson 1 (Class Alpha only), Lesson 2 (Class Alpha + Class Beta), Lesson 3 (Class Beta only)
- Logged in as HQ or CM Staff to the Salesforce org; SF Mana Calendar is accessible

| #   | Action                                              | Expected Result                                                                                                     | Test Data           |
| --- | --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ------------------- |
| 1   | Navigate to the SF Mana Calendar                    | Calendar displayed with all 3 lessons visible                                                                       | ""                  |
| 2   | Apply the class filter: select "Class Alpha" only   | Filter is applied                                                                                                   | Filter: Class Alpha |
| 3   | Observe which lessons are displayed on the Calendar | Lesson 1 (Class Alpha only) and Lesson 2 (Class Alpha + Class Beta) are shown; Lesson 3 (Class Beta only) is hidden | ""                  |

**Severity:** major
**Priority:** high

---

### Multiple Classes – SF Calendar Filter – Two Classes Selected – ALL-Match Logic Shows Only Lessons with Both Classes

**Description:** BR-35 — Decision Table (Deep) — Validates that when two classes are selected in the SF Calendar filter, only lessons containing BOTH classes (ALL-match) are displayed, not lessons with only one of the two.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- 3 lessons in the same time range: Lesson 1 (Class Alpha only), Lesson 2 (Class Alpha + Class Beta), Lesson 3 (Class Beta only)
- SF Mana Calendar is accessible

| #   | Action                                                             | Expected Result                                                                                                                                     | Test Data                          |
| --- | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| 1   | Navigate to the SF Mana Calendar                                   | Calendar displayed with all 3 lessons visible                                                                                                       | ""                                 |
| 2   | Apply the class filter: select both "Class Alpha" and "Class Beta" | Both classes are selected as filter criteria                                                                                                        | Filter: Class Alpha AND Class Beta |
| 3   | Observe which lessons are displayed                                | Only Lesson 2 (which contains BOTH Class Alpha and Class Beta) is shown; Lesson 1 (Class Alpha only) and Lesson 3 (Class Beta only) are both hidden | ""                                 |

**Severity:** major
**Priority:** high

---

### Multiple Classes – SF Calendar Filter – Two Classes with No Common Lesson – No Lessons Displayed

**Description:** BR-35 — Decision Table (Deep) — Validates that the ALL-match filter returns no results when no lesson contains all the selected classes simultaneously.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- Lesson 2 has Class Alpha and Class Beta; no lesson has Class Alpha and Class Gamma together
- SF Mana Calendar is accessible

| #   | Action                                                         | Expected Result                                                                                       | Test Data                           |
| --- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------- |
| 1   | Navigate to the SF Mana Calendar                               | Calendar displayed                                                                                    | ""                                  |
| 2   | Apply the class filter: select "Class Alpha" and "Class Gamma" | Both classes selected                                                                                 | Filter: Class Alpha AND Class Gamma |
| 3   | Observe the calendar results                                   | No lessons are shown for the selected range (no lesson has BOTH Class Alpha AND Class Gamma assigned) | ""                                  |

**Severity:** major
**Priority:** high

---

### Multiple Classes – BO Lesson List – Multi-Class Lesson Row – Comma-Separated Class Names Displayed

**Description:** AC 05.2 (BR-29) — CRUD Testing — Validates that the BO Lesson List shows comma-separated class names for a multi-class lesson.

**Preconditions:**

- Unleash flag `Lesson_BackOffice_LessonSF_MultipleClassesSF` is ON
- Lesson "Lesson MC-01" has Class Alpha and Class Beta assigned via LSC
- Logged in as HQ Staff or CM Staff to the Back Office

| #   | Action                                  | Expected Result                              | Test Data |
| --- | --------------------------------------- | -------------------------------------------- | --------- |
| 1   | Navigate to BO Lesson List              | BO Lesson List is displayed                  | ""        |
| 2   | Find "Lesson MC-01" in the list         | Row for "Lesson MC-01" is visible            | ""        |
| 3   | Read the Class column value for the row | Class column shows "Class Alpha, Class Beta" | ""        |

**Severity:** minor
**Priority:** medium

---

### Multiple Classes – BO Calendar Filter – Two Classes Selected – ALL-Match Logic Shows Only Lessons with Both Classes

**Description:** AC 05.2 (BR-30/35) — Decision Table — Validates that the BO Calendar class filter uses the same ALL-match (AND) logic as SF: selecting two classes shows only lessons that have both.

**Preconditions:**

- Unleash flag ON; 3 lessons in the same time range: Lesson 1 (Class Alpha), Lesson 2 (Class Alpha + Class Beta), Lesson 3 (Class Beta)
- Logged in as HQ Staff or CM Staff to the Back Office; BO Calendar is accessible

| #   | Action                                                             | Expected Result                                                                           | Test Data                          |
| --- | ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- | ---------------------------------- |
| 1   | Navigate to the BO Calendar                                        | BO Calendar displayed with all 3 lessons visible                                          | ""                                 |
| 2   | Apply the class filter: select both "Class Alpha" and "Class Beta" | Both classes selected as filter criteria                                                  | Filter: Class Alpha AND Class Beta |
| 3   | Observe which lessons are displayed                                | Only Lesson 2 (with both Class Alpha and Class Beta) is shown; Lessons 1 and 3 are hidden | ""                                 |

**Severity:** major
**Priority:** high

---

### Multiple Classes – Mobile Calendar – Lesson Detail – Class Names from LSC Displayed

**Description:** AC 05.3 (BR-31) — CRUD Testing — Validates that the Lesson detail screen on Mobile (Learner App) shows the class names sourced from the LSC records.

**Preconditions:**

- Unleash flag `Lesson_BackOffice_LessonSF_MultipleClassesSF` is ON
- Lesson "Lesson MC-01" has Class Alpha and Class Beta assigned; status is Published
- A student assigned to the lesson is logged in to the Learner App on a mobile device

| #   | Action                                                           | Expected Result                                                        | Test Data |
| --- | ---------------------------------------------------------------- | ---------------------------------------------------------------------- | --------- |
| 1   | Open the Learner App and navigate to the Calendar view           | Calendar view displayed                                                | ""        |
| 2   | Locate "Lesson MC-01" on the Calendar                            | Lesson is visible on the Calendar for its scheduled date               | ""        |
| 3   | Tap on "Lesson MC-01" to open the Lesson detail screen           | Lesson detail screen opens                                             | ""        |
| 4   | Read the class information displayed on the Lesson detail screen | Class field shows "Class Alpha, Class Beta" — sourced from LSC records | ""        |

**Severity:** minor
**Priority:** medium
