# Test Cases: LT-88879 — Improve Course and Class Filter on Calendar

**Suite:** Course Selection – Class Auto-Population
**Qase suite:** lesson-management > lesson > course-class-filter > Course Selection – Class Auto-Population
**Epic:** [LT-88879](https://manabie.atlassian.net/browse/LT-88879)
**BRs covered:** AC 01.1, BR-1, BR-2, BR-3, BR-13

**Precondition (all cases):**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- "Course A – Introduction to Math" has 3 associated classes: **Class Alpha**, **Class Beta**, **Class Gamma**
- "Course C – Empty Course" has **0 associated classes**
- "Class Zeta" is linked to Course A but all its lessons under Course A are scheduled **3 months ago** (outside the current calendar week)
- The following Group lessons exist on the calendar in the **current week**:
  - **Lesson G1**: Course A, Class Alpha only
  - **Lesson G2**: Course A, Class Alpha + Class Beta
  - **Lesson G3**: Course A, Class Beta only
  - **Lesson G4**: Course A, Class Gamma only

---

## Suite: Course Selection – Class Auto-Population

### Calendar Filter – Course Selection – SF Calendar – Classes Auto-Populated in Unchecked State

**Description:** AC 01.1, BR-1 — Decision Table — Confirms that on the SF Mana Calendar, selecting a course auto-populates the class list with all classes under that course, and every class starts in an unchecked (inactive) state.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- "Course A – Introduction to Math" has 3 classes: Class Alpha, Class Beta, Class Gamma
- Group lessons G1–G4 exist in the current week
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                     | Expected Result                                                                                           | Test Data                        |
| --- | -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | -------------------------------- |
| 1   | Open the SF Mana Calendar and open the filter panel                        | Filter panel opens; Class section is not visible                                                          |                                  |
| 2   | Select **"Course A – Introduction to Math"** in the Course filter          | Course A is selected                                                                                      | Course A – Introduction to Math  |
| 3   | Observe the Class filter section                                           | The Class section appears below the Course section; **Class Alpha, Class Beta, and Class Gamma** are listed |                                |
| 4   | Observe the checkbox state of each class in the list                       | All 3 classes are in **unchecked** state — no class checkbox is checked                                   |                                  |

**Severity:** major
**Priority:** high

---

### Calendar Filter – Course Selection – BO Calendar – Classes Auto-Populated in Unchecked State

**Description:** AC 01.1, BR-2 — Decision Table — Confirms that on the BO Calendar, selecting a course auto-populates the class list in unchecked state.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- "Course A – Introduction to Math" has 3 classes: Class Alpha, Class Beta, Class Gamma
- Group lessons G1–G4 exist in the current week
- Logged in as HQ or CM Staff to the Back Office

| #   | Action                                                                     | Expected Result                                                                                           | Test Data                        |
| --- | -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- | -------------------------------- |
| 1   | Open the BO Calendar and open the filter panel                             | Filter panel opens; Class section is not visible                                                          |                                  |
| 2   | Select **"Course A – Introduction to Math"** in the Course filter          | Course A is selected                                                                                      | Course A – Introduction to Math  |
| 3   | Observe the Class filter section                                           | The Class section appears; Class Alpha, Class Beta, and Class Gamma are listed                            |                                  |
| 4   | Observe the checkbox state of each class                                   | All 3 classes are in **unchecked** state                                                                  |                                  |

**Severity:** major
**Priority:** high

---

### Calendar Filter – Course Selection – SF Calendar – Auto-Populated Classes Not Active Until Manually Checked

**Description:** AC 01.1, BR-3 — Decision Table (Critical) — Confirms that after selecting a course and seeing the class list auto-populated, the SF Calendar is NOT filtered by class. All lessons for that course remain visible — no class filter is applied until the user explicitly checks a class.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- "Course A" has 3 classes; Group lessons G1–G4 (all linked to Course A) exist in the current week
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                                     | Expected Result                                                                                                     | Test Data |
| --- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | Open the SF Mana Calendar with no filter applied                                           | All 4 Group lessons for Course A (G1, G2, G3, G4) are visible on the calendar                                      |           |
| 2   | Note the total number of Course A lessons visible: **4 lessons**                           | 4 lessons confirmed visible                                                                                         |           |
| 3   | Select **"Course A – Introduction to Math"** in the Course filter                          | Course A is selected; Class section appears with Class Alpha, Class Beta, Class Gamma — all unchecked               | Course A – Introduction to Math |
| 4   | Observe the calendar without checking any class                                            | Calendar still shows **all 4 Course A lessons** (G1, G2, G3, G4) — the lesson count has NOT decreased              |           |
| 5   | Confirm that all class checkboxes remain unchecked                                         | Class Alpha, Class Beta, Class Gamma are all unchecked; no class filter is active                                   |           |

**Severity:** critical
**Priority:** high

---

### Calendar Filter – Course Selection – BO Calendar – Auto-Populated Classes Not Active Until Manually Checked

**Description:** AC 01.1, BR-3 — Decision Table (Critical) — Confirms the same inactive behavior on BO Calendar: course selection auto-populates classes but does not filter the calendar until a class is manually checked.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- "Course A" has 3 classes; Group lessons G1–G4 exist in the current week
- Logged in as HQ or CM Staff to the Back Office

| #   | Action                                                                                     | Expected Result                                                                                    | Test Data                        |
| --- | ------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- | -------------------------------- |
| 1   | Open the BO Calendar with no filter applied; confirm all 4 Course A lessons are visible    | All 4 Group lessons (G1, G2, G3, G4) visible                                                       |                                  |
| 2   | Select **"Course A – Introduction to Math"** in the Course filter                          | Course A selected; Class section appears with all 3 classes unchecked                              | Course A – Introduction to Math  |
| 3   | Observe the calendar without checking any class                                            | Calendar still shows all 4 Course A lessons — no class filter applied                              |                                  |
| 4   | Confirm all class checkboxes are unchecked                                                 | All 3 classes remain unchecked; no class is active as a filter criterion                           |                                  |

**Severity:** critical
**Priority:** high

---

### Calendar Filter – Course Selection – Class Scope – Classes Outside Current Date Range Listed in Filter

**Description:** BR-13 — Equivalence Partitioning — Confirms the auto-populated class list contains ALL classes system-wide linked to the selected course, including classes whose lessons fall outside the currently displayed calendar date range.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- "Course A – Introduction to Math" has **4 associated classes**: Class Alpha, Class Beta, Class Gamma, **Class Zeta**
- Class Zeta's lessons under Course A are all scheduled 3 months ago (not visible in the current week view)
- Logged in as HQ or CM Staff to the Salesforce org
- SF Mana Calendar is showing the **current week**

| #   | Action                                                                     | Expected Result                                                                                                                                            | Test Data                        |
| --- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| 1   | Open SF Mana Calendar showing the current week                             | Current week is displayed; Class Zeta's lessons are not visible on the calendar                                                                            |                                  |
| 2   | Select **"Course A – Introduction to Math"** in the Course filter          | Course A is selected                                                                                                                                       | Course A – Introduction to Math  |
| 3   | Observe the full class list in the filter panel                            | Class list shows: **Class Alpha, Class Beta, Class Gamma, and Class Zeta** — all 4 classes appear, including Class Zeta whose lessons are not in the current view |                             |

**Severity:** minor
**Priority:** medium

---

### Calendar Filter – Course Selection – Course with No Associated Classes – Empty Class Section Displayed

**Description:** AC 01.1 edge case — Boundary Value Analysis — Confirms that selecting a course that has no associated classes shows an empty class section gracefully, without error or crash.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- "Course C – Empty Course" exists and has **0 associated classes**
- Logged in as HQ or CM Staff to the Salesforce org
- SF Mana Calendar filter panel is open

| #   | Action                                                            | Expected Result                                                                                                       | Test Data             |
| --- | ----------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------- |
| 1   | In the Calendar filter, select **"Course C – Empty Course"**      | Course C is selected                                                                                                  | Course C – Empty Course |
| 2   | Observe the Class section in the filter panel                     | The Class section appears but displays an empty list (e.g., "No classes available" message, or an empty container)   |                       |
| 3   | Confirm no error message, crash, or indefinite loading spinner    | The filter panel remains stable; no error toast, no spinner frozen, no blank page                                     |                       |

**Severity:** minor
**Priority:** medium
