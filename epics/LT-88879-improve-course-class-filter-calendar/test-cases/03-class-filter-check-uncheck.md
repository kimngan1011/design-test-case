# Test Cases: LT-88879 — Improve Course and Class Filter on Calendar

**Suite:** Class Filter – Check and Uncheck
**Qase suite:** lesson-management > lesson > course-class-filter > Class Filter – Check and Uncheck
**Epic:** [LT-88879](https://manabie.atlassian.net/browse/LT-88879)
**BRs covered:** AC 02.1, BR-4, BR-5, BR-6

**Precondition (all cases):**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- "Course A – Introduction to Math" has 3 classes: **Class Alpha**, **Class Beta**, **Class Gamma**
- "Course B – English Fundamentals" has lessons on the calendar in the current week
- The following Group lessons exist on the calendar in the **current week**:
  - **Lesson G1**: Course A, Class Alpha only
  - **Lesson G2**: Course A, Class Alpha + Class Beta
  - **Lesson G3**: Course A, Class Beta only
  - **Lesson G4**: Course A, Class Gamma only

---

## Suite: Class Filter – Check and Uncheck

### Calendar Filter – Class Checkbox – SF Calendar – Class Checked – Calendar Shows Only Lessons With That Class

**Description:** AC 02.1, BR-4 — Decision Table — Confirms that checking a class from the auto-populated list applies it as an active filter criterion and the SF Calendar shows only lessons that contain that class.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- Course A has 3 classes; Group lessons G1–G4 exist in the current week
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                    | Expected Result                                                                                                          | Test Data                        |
| --- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | -------------------------------- |
| 1   | On SF Mana Calendar, select **"Course A – Introduction to Math"** in the Course filter | Class section appears; Class Alpha, Class Beta, Class Gamma are all unchecked                  | Course A – Introduction to Math  |
| 2   | Check **Class Alpha** in the class filter                                 | Class Alpha checkbox becomes checked (active filter)                                                                     |                                  |
| 3   | Observe the calendar                                                      | **Lesson G1** (Class Alpha only) and **Lesson G2** (Class Alpha + Class Beta) are shown; Lesson G3 and Lesson G4 are hidden |                                |

**Severity:** major
**Priority:** high

---

### Calendar Filter – Class Checkbox – BO Calendar – Class Checked – Calendar Shows Only Lessons With That Class

**Description:** AC 02.1, BR-4 — Decision Table — Confirms the same behavior on BO Calendar: checking a class filters the calendar to show only lessons containing that class.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- Course A has 3 classes; Group lessons G1–G4 exist in the current week
- Logged in as HQ or CM Staff to the Back Office

| #   | Action                                                                    | Expected Result                                                                                                          | Test Data                        |
| --- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ | -------------------------------- |
| 1   | On BO Calendar, select **"Course A – Introduction to Math"** in the Course filter | Class section appears; all 3 classes unchecked                                                         | Course A – Introduction to Math  |
| 2   | Check **Class Alpha** in the class filter                                 | Class Alpha checkbox is checked (active)                                                                                 |                                  |
| 3   | Observe the calendar                                                      | Lesson G1 and Lesson G2 are shown; Lesson G3 (Class Beta only) and Lesson G4 (Class Gamma only) are hidden              |                                  |

**Severity:** major
**Priority:** high

---

### Calendar Filter – Class Checkbox – Class Unchecked After Being Checked – Calendar Reverts to All Course Lessons

**Description:** AC 02.1, BR-5 — State Transition Testing — Confirms that unchecking a class removes it from the active filter and the calendar reverts to showing all lessons for the selected course.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- Course A has 3 classes; Group lessons G1–G4 exist in the current week
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                    | Expected Result                                                                                        | Test Data                        |
| --- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | -------------------------------- |
| 1   | On SF Mana Calendar, select **"Course A"** and check **Class Alpha**      | Calendar shows only Lesson G1 and Lesson G2 (lessons containing Class Alpha)                          | Course A – Introduction to Math  |
| 2   | Uncheck **Class Alpha**                                                   | Class Alpha checkbox returns to unchecked state                                                        |                                  |
| 3   | Observe the calendar                                                      | All 4 Course A lessons (G1, G2, G3, G4) are displayed again — no class filter is active               |                                  |
| 4   | Confirm Course A is still selected in the Course filter                   | "Course A – Introduction to Math" remains selected in the Course filter                               |                                  |

**Severity:** major
**Priority:** high

---

### Calendar Filter – Course and Class Independence – Class Unchecked – Course Filter Remains Selected

**Description:** AC 02.1, BR-6 — Decision Table — Confirms that unchecking all class checkboxes does NOT deselect the course filter — the course filter remains active independently of the class filter state.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- "Course A" and "Course B" both have Group lessons on the calendar in the current week
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                                        | Expected Result                                                                                                      | Test Data                        |
| --- | --------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| 1   | On SF Mana Calendar, select **"Course A – Introduction to Math"** in the Course filter        | Course A selected; class list appears; Course B lessons are now filtered out of the calendar                         | Course A – Introduction to Math  |
| 2   | Check **Class Alpha**, then immediately uncheck **Class Alpha**                               | Class Alpha is unchecked; all classes are now unchecked                                                              |                                  |
| 3   | Observe the Course filter section                                                             | **"Course A – Introduction to Math"** is still selected in the Course filter — it was NOT deselected                |                                  |
| 4   | Observe the calendar                                                                          | Only Course A lessons are shown (course filter still active); Course B lessons remain hidden; all 4 Course A lessons (G1–G4) are visible (no active class filter) | |

**Severity:** major
**Priority:** high

---

### Calendar Filter – Full Journey – Select Course, Check Two Classes, Uncheck One – Calendar State Correct at Each Step

**Description:** AC 01.1 + AC 02.1 — State Transition Testing — End-to-end validation of the class filter state transitions: course selected → class appears unchecked → classes checked one-by-one → uncheck one → uncheck all → course persists throughout.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- "Course A" has 3 classes: Class Alpha, Class Beta, Class Gamma
- Group lessons G1 (Class Alpha), G2 (Class Alpha + Class Beta), G3 (Class Beta only), G4 (Class Gamma only) exist in the current week
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                    | Expected Result                                                                                                                    | Test Data                        |
| --- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| 1   | Open SF Mana Calendar with no filter applied                              | All 4 Course A lessons are visible on the calendar                                                                                 |                                  |
| 2   | Select **"Course A – Introduction to Math"** in the Course filter         | Course A selected; Class section appears with Class Alpha, Class Beta, Class Gamma — all unchecked; all 4 Course A lessons visible  | Course A – Introduction to Math  |
| 3   | Check **Class Alpha**                                                     | Class Alpha is checked; calendar shows only Lesson G1 and Lesson G2 (lessons containing Class Alpha)                              |                                  |
| 4   | Also check **Class Beta**                                                 | Both Class Alpha and Class Beta are checked; calendar shows only **Lesson G2** (the only lesson with BOTH Class Alpha AND Class Beta) |                                |
| 5   | Uncheck **Class Beta**                                                    | Class Beta unchecked; Class Alpha still checked; calendar reverts to showing Lesson G1 and G2 (all lessons with Class Alpha)       |                                  |
| 6   | Uncheck **Class Alpha**                                                   | All classes unchecked; calendar shows all 4 Course A lessons; no class filter active                                               |                                  |
| 7   | Confirm Course A is still selected in the Course filter                   | "Course A – Introduction to Math" remains selected; Class section still visible with all 3 classes unchecked                       |                                  |

**Severity:** major
**Priority:** high
