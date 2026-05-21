# Test Cases: LT-88879 — Improve Course and Class Filter on Calendar

**Suite:** Teacher Role
**Qase suite:** lesson-management > lesson > course-class-filter > Teacher Role
**Epic:** [LT-88879](https://manabie.atlassian.net/browse/LT-88879)
**BRs covered:** BR-14
**Platform:** BO only

**Precondition (all cases):**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- "Course A – Introduction to Math" has 3 associated classes: **Class Alpha**, **Class Beta**, **Class Gamma**
- The following Group lessons exist on the calendar in the **current week**:
  - **Lesson G1**: Course A, Class Alpha only — **Teacher T1 is assigned**
  - **Lesson G2**: Course A, Class Alpha + Class Beta — Teacher T2 only (Teacher T1 NOT assigned)
  - **Lesson G3**: Course A, Class Beta only — Teacher T2 only
  - **Lesson G4**: Course A, Class Gamma only — Teacher T2 only
- **Teacher T1** has a CPU login (bo_teacher role) in the Back Office

---

## Suite: Teacher Role

### Calendar Filter – Teacher Role – BO Calendar – Course Selected – All System-Wide Classes Listed

**Description:** BR-14 — Permission Matrix — Confirms that when a teacher (CPU login) selects a course on the BO Calendar, the auto-populated class list shows ALL classes linked to that course system-wide — not scoped to only the classes from that teacher's assigned lessons.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- Course A has 3 classes: Class Alpha, Class Beta, Class Gamma
- Lesson G1 (Class Alpha, Teacher T1 assigned), G2/G3/G4 (Teacher T2 only) exist in the current week
- Logged in as **Teacher T1** (CPU login / bo_teacher role) to the Back Office

| #   | Action                                                                                    | Expected Result                                                                                                                                                                         | Test Data                        |
| --- | ----------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| 1   | Log in as Teacher T1 (CPU login) to the BO Calendar                                      | BO Calendar shows only **Lesson G1** (the lesson assigned to Teacher T1); G2, G3, G4 are not visible due to teacher scope                                                               | Teacher T1                       |
| 2   | Open the filter panel and select **"Course A – Introduction to Math"** in the Course filter | Course A is selected; Class section appears                                                                                                                                          | Course A – Introduction to Math  |
| 3   | Observe the full class list in the filter panel                                           | The class list shows **Class Alpha, Class Beta, and Class Gamma** — all 3 classes are listed, not just Class Alpha (which is the only class from Teacher T1's assigned lesson, Lesson G1) |                                 |

**Severity:** minor
**Priority:** medium

---

### Calendar Filter – Teacher Role – BO Calendar – Class Checked – Calendar Filtered Correctly for Teacher

**Description:** BR-14, BR-4 — Decision Table — Confirms that when a teacher checks a class in the filter, the calendar applies both the class filter AND the teacher scope: only that teacher's lessons that also contain the selected class are shown.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- Course A has 3 classes; Lesson G1 (Class Alpha, Teacher T1), G2 (Class Alpha + Class Beta, Teacher T2 only), G3 (Class Beta, Teacher T2 only), G4 (Class Gamma, Teacher T2 only)
- Logged in as **Teacher T1** (CPU login) to the Back Office

| #   | Action                                                                    | Expected Result                                                                                                                                                                           | Test Data                        |
| --- | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| 1   | Log in as Teacher T1 and open BO Calendar                                 | Only **Lesson G1** is visible (teacher scope: Teacher T1's assigned lessons only)                                                                                                         | Teacher T1                       |
| 2   | Select **"Course A – Introduction to Math"** in the Course filter         | Class section appears; Class Alpha, Class Beta, and Class Gamma are listed (all system-wide)                                                                                              | Course A – Introduction to Math  |
| 3   | Check **Class Alpha**                                                     | Class Alpha is checked (active filter)                                                                                                                                                    |                                  |
| 4   | Observe the calendar                                                      | **Lesson G1** is shown (it has Class Alpha AND is assigned to Teacher T1); Lesson G2 is NOT shown (also has Class Alpha but Teacher T1 is not assigned — teacher scope still applied) |                                  |

**Severity:** minor
**Priority:** medium
