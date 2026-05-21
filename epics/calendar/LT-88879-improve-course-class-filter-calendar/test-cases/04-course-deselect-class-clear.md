# Test Cases: LT-88879 — Improve Course and Class Filter on Calendar

**Suite:** Course Deselection – Class List Clear
**Qase suite:** lesson-management > lesson > course-class-filter > Course Deselection – Class List Clear
**Epic:** [LT-88879](https://manabie.atlassian.net/browse/LT-88879)
**BRs covered:** BR-12

**Precondition (all cases):**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- "Course A – Introduction to Math" has 3 classes: **Class Alpha**, **Class Beta**, **Class Gamma**
- Group lessons G1 (Class Alpha), G2 (Class Alpha + Class Beta), G3 (Class Beta), G4 (Class Gamma) exist in the current week

---

## Suite: Course Deselection – Class List Clear

### Calendar Filter – Course Deselection – SF Calendar – No Classes Checked – Class Section Hidden

**Description:** BR-12 — State Transition Testing — Confirms that deselecting a course when no classes are checked causes the class filter section to completely disappear.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- Logged in as HQ or CM Staff to the Salesforce org
- SF Mana Calendar filter panel is open

| #   | Action                                                              | Expected Result                                                                           | Test Data                        |
| --- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | -------------------------------- |
| 1   | In the SF Mana Calendar filter, select **"Course A – Introduction to Math"** | Course A is selected; Class section appears with 3 classes unchecked            | Course A – Introduction to Math  |
| 2   | Do NOT check any class; deselect / clear **"Course A"** from the Course filter | Course A is deselected                                                          |                                  |
| 3   | Observe the filter panel                                            | The **Class section is no longer visible** — the entire class list has been hidden        |                                  |
| 4   | Observe the calendar                                                | All lessons are shown (no active course filter, no class filter)                          |                                  |

**Severity:** major
**Priority:** high

---

### Calendar Filter – Course Deselection – BO Calendar – No Classes Checked – Class Section Hidden

**Description:** BR-12 — State Transition Testing — Confirms the same course deselection behavior on BO Calendar: class section disappears when course is cleared.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- Logged in as HQ or CM Staff to the Back Office
- BO Calendar filter panel is open

| #   | Action                                                              | Expected Result                                                               | Test Data                        |
| --- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------- | -------------------------------- |
| 1   | In the BO Calendar filter, select **"Course A – Introduction to Math"** | Course A selected; Class section appears with 3 classes unchecked         | Course A – Introduction to Math  |
| 2   | Deselect **"Course A"** from the Course filter                      | Course A is cleared                                                           |                                  |
| 3   | Observe the filter panel                                            | Class section disappears; no class list visible                               |                                  |

**Severity:** major
**Priority:** high

---

### Calendar Filter – Course Deselection – Classes Already Checked – All Checked Classes Also Cleared

**Description:** BR-12 — State Transition Testing (boundary) — Confirms that when a course is deselected while one or more classes are already checked (active filter), the class list is fully cleared including the checked state — not just hidden with stale checked classes preserved in memory.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- Course A has 3 classes; Group lessons G1–G4 exist in the current week
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                        | Expected Result                                                                                          | Test Data                        |
| --- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | -------------------------------- |
| 1   | On SF Mana Calendar, select **"Course A"** in the Course filter               | Class section appears with 3 classes unchecked                                                           | Course A – Introduction to Math  |
| 2   | Check **Class Alpha** and **Class Beta**                                      | Both classes are checked; calendar shows only Lesson G2 (has both Class Alpha AND Class Beta)            |                                  |
| 3   | Deselect **"Course A"** from the Course filter                                | Course A is deselected                                                                                   |                                  |
| 4   | Observe the filter panel                                                      | Class section disappears; the class filter state is fully cleared — no class checkboxes visible          |                                  |
| 5   | Observe the calendar                                                          | All lessons are shown — no course filter and no class filter active                                      |                                  |

**Severity:** major
**Priority:** high

---

### Calendar Filter – Course Reselection – After Deselect and Reselect – Class List Resets to Unchecked State

**Description:** BR-12 — State Transition Testing — Confirms that after deselecting a course (which clears the class list) and then reselecting the same course, the class list is populated fresh with all classes unchecked — no residual checked state from the previous selection.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- "Course A" has 3 classes: Class Alpha, Class Beta, Class Gamma
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                              | Expected Result                                                                                                | Test Data                        |
| --- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| 1   | On SF Mana Calendar, select **"Course A"** in the Course filter     | Class section appears; 3 classes unchecked                                                                     | Course A – Introduction to Math  |
| 2   | Check **Class Alpha**                                               | Class Alpha is checked (active filter applied)                                                                 |                                  |
| 3   | Deselect **"Course A"** from the Course filter                      | Course A cleared; Class section disappears                                                                     |                                  |
| 4   | Reselect **"Course A – Introduction to Math"**                      | Class section reappears with Class Alpha, Class Beta, and Class Gamma listed                                   | Course A – Introduction to Math  |
| 5   | Observe the checkbox state of all classes                           | **All 3 classes are unchecked** — Class Alpha is NOT checked; the previous selection is not carried over        |                                  |

**Severity:** major
**Priority:** high
