# Test Cases: LT-88879 — Improve Course and Class Filter on Calendar

**Suite:** Class Requires Course – Regression
**Qase suite:** lesson-management > lesson > course-class-filter > Class Requires Course – Regression
**Epic:** [LT-88879](https://manabie.atlassian.net/browse/LT-88879)
**BRs covered:** BR-15 (BREAKING CHANGE), BR-4

**⚠️ Note:** BR-15 is a breaking behavioral change. The 8 existing class filter test cases in
`output/test-cases/lesson-management/lesson/multiple-classes/06-ui-filter.md` (which used direct class
selection without course pre-selection) must be updated to add a course selection step before the class
selection step. The test cases in this file validate the new required flow and serve as the regression
baseline.

**Precondition (all cases):**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- "Course A – Introduction to Math" has 3 classes: **Class Alpha**, **Class Beta**, **Class Gamma**
- The following Group lessons exist on the calendar in the **current week**:
  - **Lesson G1**: Course A, Class Alpha only
  - **Lesson G2**: Course A, Class Alpha + Class Beta
  - **Lesson G3**: Course A, Class Beta only
  - **Lesson G4**: Course A, Class Gamma only

---

## Suite: Class Requires Course – Regression

### Calendar Filter – Class Section Dependency – SF Calendar – Class Section Not Accessible Without Course Selected

**Description:** BR-15 — Decision Table (Breaking Change) — Confirms that on the SF Calendar, the class filter section is completely inaccessible when no course has been selected, enforcing the new dependency: class filter requires course selection first.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- Logged in as HQ or CM Staff to the Salesforce org
- SF Mana Calendar filter panel is open

| #   | Action                                                                         | Expected Result                                                                                        | Test Data |
| --- | ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------ | --------- |
| 1   | Open the SF Mana Calendar filter panel                                         | The filter panel displays Course, Location, Teacher, and other filter sections                         |           |
| 2   | Do NOT select any course; observe the complete filter panel                    | No class filter section is visible; no class checkboxes, no class list, no "Class" label               |           |
| 3   | Scroll through the entire filter panel                                         | The class section is not present anywhere in the filter panel when no course is selected               |           |

**Severity:** critical
**Priority:** high

---

### Calendar Filter – Class Section Dependency – BO Calendar – Class Section Not Accessible Without Course Selected

**Description:** BR-15 — Decision Table (Breaking Change) — Same as above for BO Calendar: class section is inaccessible without course selection.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- Logged in as HQ or CM Staff to the Back Office
- BO Calendar filter panel is open

| #   | Action                                                                         | Expected Result                                                                     | Test Data |
| --- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------- | --------- |
| 1   | Open the BO Calendar filter panel                                              | Filter panel opens with standard filter sections                                    |           |
| 2   | Do NOT select any course; observe the complete filter panel                    | No class filter section is visible anywhere in the filter panel                     |           |

**Severity:** critical
**Priority:** high

---

### Calendar Filter – Class Section Dependency – Course Deselected After Prior Use – Class Section Hidden Again

**Description:** BR-15 — State Transition Testing — Confirms that after using the class filter (course selected, class checked), clearing the course causes the class section to become inaccessible again — the dependency is enforced consistently across the session.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- Course A has 3 classes; Group lessons G1–G4 exist in the current week
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                              | Expected Result                                                                              | Test Data                        |
| --- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------------- |
| 1   | On SF Mana Calendar, select **"Course A – Introduction to Math"**   | Class section appears with 3 classes unchecked                                               | Course A – Introduction to Math  |
| 2   | Check **Class Alpha**                                               | Calendar is filtered; only Lesson G1 and Lesson G2 are shown                                |                                  |
| 3   | Deselect **"Course A"** from the Course filter                      | Course A is cleared                                                                          |                                  |
| 4   | Observe the filter panel                                            | Class section is hidden; no class list, no class checkboxes visible                          |                                  |
| 5   | Observe the calendar                                                | All lessons are shown (no course filter, no class filter active)                             |                                  |

**Severity:** critical
**Priority:** high

---

### Calendar Filter – Regression – SF Calendar – Single Class Filter With Course Pre-Selection – Correct Lessons Shown

**Description:** BR-15, BR-4 — Regression Analysis — Confirms that the single-class filtering behavior from LT-74136 ("Single Class Selected" test) still produces correct results when using the required new flow: select course first, then check class.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- "Course A" has 3 classes: Class Alpha, Class Beta, Class Gamma
- Group lessons: G1 (Class Alpha only), G2 (Class Alpha + Class Beta), G3 (Class Beta only), G4 (Class Gamma only)
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                        | Expected Result                                                                                                                                          | Test Data                        |
| --- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| 1   | On SF Mana Calendar, select **"Course A – Introduction to Math"** in the Course filter | Class section appears with all 3 classes unchecked                                                                                    | Course A – Introduction to Math  |
| 2   | Check **Class Alpha** in the class filter                                     | Class Alpha checkbox is checked (active)                                                                                                                 |                                  |
| 3   | Observe which lessons appear on the calendar                                  | **Lesson G1** (Class Alpha only) and **Lesson G2** (Class Alpha + Class Beta) are shown; Lesson G3 (Class Beta only) and Lesson G4 (Class Gamma only) are hidden |                             |

**Severity:** critical
**Priority:** high

---

### Calendar Filter – Regression – BO Calendar – Single Class Filter With Course Pre-Selection – Correct Lessons Shown

**Description:** BR-15, BR-4 — Regression Analysis — Same regression check for BO Calendar: the single-class filter from LT-74136 BO test produces correct results in the new course-first flow.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- "Course A" has 3 classes: Class Alpha, Class Beta, Class Gamma
- Group lessons G1–G4 as above exist in the current week
- Logged in as HQ or CM Staff to the Back Office

| #   | Action                                                                        | Expected Result                                                                                                               | Test Data                        |
| --- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| 1   | On BO Calendar, select **"Course A – Introduction to Math"** in the Course filter | Class section appears; all 3 classes unchecked                                                                            | Course A – Introduction to Math  |
| 2   | Check **Class Alpha** in the class filter                                     | Class Alpha is checked (active)                                                                                               |                                  |
| 3   | Observe the calendar                                                          | Lesson G1 and Lesson G2 are shown; Lesson G3 (Class Beta only) and Lesson G4 (Class Gamma only) are hidden                   |                                  |

**Severity:** critical
**Priority:** high
