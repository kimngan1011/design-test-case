# Test Cases: LT-88879 — Improve Course and Class Filter on Calendar

**Suite:** ALL-Match Logic – Regression
**Qase suite:** lesson-management > lesson > course-class-filter > ALL-Match Logic – Regression
**Epic:** [LT-88879](https://manabie.atlassian.net/browse/LT-88879)
**BRs covered:** BR-7 (prior BR-35 from LT-74136)

**Precondition (all cases):**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- "Course A – Introduction to Math" has 3 classes: **Class Alpha**, **Class Beta**, **Class Gamma**
- The following Group lessons exist on the calendar in the **current week**:
  - **Lesson G1**: Course A, Class Alpha only
  - **Lesson G2**: Course A, Class Alpha + Class Beta
  - **Lesson G3**: Course A, Class Beta only
  - **Lesson G4**: Course A, Class Gamma only
- No lesson under Course A contains both Class Alpha and Class Gamma simultaneously

---

## Suite: ALL-Match Logic – Regression

### Calendar Filter – Multi-Class Filter – SF Calendar – Two Classes Checked After Course Select – Only Lessons With Both Classes Shown

**Description:** BR-7 (BR-35) — Decision Table (Regression) — Confirms the ALL-match (AND logic) class filter still works correctly in the new interaction flow: course must be selected first, then two classes are checked, and only lessons containing BOTH classes are shown.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- Course A has 3 classes; Group lessons G1–G4 exist in the current week
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                        | Expected Result                                                                                                                                             | Test Data                        |
| --- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| 1   | On SF Mana Calendar, select **"Course A – Introduction to Math"** in the Course filter | Class section appears; Class Alpha, Class Beta, Class Gamma all unchecked                                              | Course A – Introduction to Math  |
| 2   | Check **Class Alpha**                                                         | Calendar shows Lesson G1 (Class Alpha only) and Lesson G2 (Class Alpha + Class Beta); G3 and G4 are hidden             |                                  |
| 3   | Also check **Class Beta**                                                     | Calendar shows only **Lesson G2** — the only lesson that contains BOTH Class Alpha AND Class Beta; Lesson G1 (Class Alpha only), G3 (Class Beta only), and G4 (Class Gamma only) are all hidden |         |

**Severity:** critical
**Priority:** high

---

### Calendar Filter – Multi-Class Filter – BO Calendar – Two Classes Checked After Course Select – Only Lessons With Both Classes Shown

**Description:** BR-7 (BR-35) — Decision Table (Regression) — Confirms ALL-match (AND logic) works correctly on BO Calendar with the new course-first interaction flow.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- Course A has 3 classes; Group lessons G1–G4 exist in the current week
- Logged in as HQ or CM Staff to the Back Office

| #   | Action                                                                        | Expected Result                                                                                                                             | Test Data                        |
| --- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| 1   | On BO Calendar, select **"Course A – Introduction to Math"** in the Course filter | Class section appears; all 3 classes unchecked                                                                                          | Course A – Introduction to Math  |
| 2   | Check **Class Alpha**                                                         | Calendar shows Lesson G1 and Lesson G2                                                                                                      |                                  |
| 3   | Also check **Class Beta**                                                     | Calendar shows only **Lesson G2** (AND logic: must contain both Class Alpha AND Class Beta); Lessons G1, G3, G4 hidden                      |                                  |

**Severity:** critical
**Priority:** high

---

### Calendar Filter – Multi-Class Filter – No Lesson Contains Both Selected Classes – Empty Calendar Result Shown

**Description:** BR-7 (BR-35) — Decision Table (Boundary/Negative) — Confirms that when two classes are checked and no lesson in the calendar contains both simultaneously, the calendar shows an empty result without any error.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- Course A has 3 classes; no lesson under Course A contains both Class Alpha AND Class Gamma
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                        | Expected Result                                                                                                                | Test Data                        |
| --- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | -------------------------------- |
| 1   | On SF Mana Calendar, select **"Course A – Introduction to Math"**             | Class section appears; all 3 classes unchecked                                                                                 | Course A – Introduction to Math  |
| 2   | Check **Class Alpha** and **Class Gamma**                                     | Both classes are checked                                                                                                       |                                  |
| 3   | Observe the calendar                                                          | **No lessons** are shown in the current date range — no lesson has both Class Alpha AND Class Gamma; no error message is thrown |                                  |

**Severity:** critical
**Priority:** high

---

### Calendar Filter – Multi-Class Filter – One of Two Checked Classes Unchecked – Broader Lesson Results Shown

**Description:** BR-7, BR-5 — Decision Table — Confirms that unchecking one of two active class filters relaxes the AND condition and displays a broader set of lessons matching only the remaining checked class.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- Course A has 3 classes; Group lessons G1–G4 exist in the current week
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                        | Expected Result                                                                                                              | Test Data                        |
| --- | ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| 1   | On SF Mana Calendar, select **"Course A"**, check Class Alpha and Class Beta  | Calendar shows only Lesson G2 (AND logic: has both Alpha AND Beta)                                                           | Course A – Introduction to Math  |
| 2   | Uncheck **Class Beta**                                                        | Class Beta is unchecked; only Class Alpha remains checked                                                                    |                                  |
| 3   | Observe the calendar                                                          | Calendar now shows **Lesson G1** (Class Alpha only) and **Lesson G2** (Class Alpha + Class Beta) — single-class filter applied |                                 |
| 4   | Confirm Course A is still selected                                            | "Course A – Introduction to Math" remains selected in the Course filter                                                      |                                  |

**Severity:** major
**Priority:** high
