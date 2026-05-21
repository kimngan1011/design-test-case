# Test Cases: LT-88879 — Improve Course and Class Filter on Calendar

**Suite:** Class Section Visibility
**Qase suite:** lesson-management > lesson > course-class-filter > Class Section Visibility
**Epic:** [LT-88879](https://manabie.atlassian.net/browse/LT-88879)
**BRs covered:** BR-10, BR-11

**Precondition (all cases):**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE in the Salesforce org
- "Course A – Introduction to Math" has 3 associated classes: **Class Alpha**, **Class Beta**, **Class Gamma**
- At least one Group lesson and one Individual lesson linked to Course A exist on the calendar in the current week

---

## Suite: Class Section Visibility

### Calendar Filter – Class Section – SF Calendar – No Course Selected – Class Section Not Visible

**Description:** BR-10 — State Transition Testing — Confirms that the class filter section is completely hidden on the SF Mana Calendar when no course has been selected in the filter panel.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- At least one Group lesson exists on the calendar in the current week
- Logged in as HQ or CM Staff to the Salesforce org
- SF Mana Calendar is open

| #   | Action                                                                    | Expected Result                                                                              | Test Data |
| --- | ------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- | --------- |
| 1   | Open the SF Mana Calendar and open the filter panel                       | The filter panel opens; Course, Location, Teacher and other sections are visible             |           |
| 2   | Observe the filter panel without selecting any course                     | The **Class** filter section is NOT visible in the filter panel                              |           |
| 3   | Scroll through the entire filter panel to confirm no class section exists | No class list, no class checkboxes, and no "Class" section label is found anywhere           |           |

**Severity:** major
**Priority:** high

---

### Calendar Filter – Class Section – BO Calendar – No Course Selected – Class Section Not Visible

**Description:** BR-10 — State Transition Testing — Confirms that the class filter section is completely hidden on the BO Calendar when no course has been selected.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- At least one Group lesson exists on the calendar in the current week
- Logged in as HQ or CM Staff to the Back Office
- BO Calendar filter panel is accessible

| #   | Action                                                                    | Expected Result                                                                 | Test Data |
| --- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | --------- |
| 1   | Open the BO Calendar and open the filter panel                            | The filter panel opens with standard filter sections visible                    |           |
| 2   | Observe the filter panel without selecting any course                     | The **Class** filter section is NOT visible                                     |           |
| 3   | Scroll through the entire filter panel to confirm no class section exists | No class list, no class checkboxes, and no "Class" label is found anywhere      |           |

**Severity:** major
**Priority:** high

---

### Calendar Filter – Class Section – Individual Lesson Type – Course Selected – Class Section Remains Hidden

**Description:** BR-11 — Decision Table — Confirms that when the lesson type filter is set to "Individual", selecting a course does NOT reveal the class filter section. Individual lessons do not support class filtering.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- At least one Individual lesson linked to "Course A – Introduction to Math" exists on the calendar (via Student Session course)
- Logged in as HQ or CM Staff to the Salesforce org
- SF Mana Calendar filter panel is open

| #   | Action                                                                        | Expected Result                                                                                    | Test Data                        |
| --- | ----------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- | -------------------------------- |
| 1   | In the Calendar filter, set the lesson type to **Individual**                 | "Individual" lesson type is selected; only Individual lessons appear on the calendar               |                                  |
| 2   | In the Course filter, select **"Course A – Introduction to Math"**            | Course A is selected                                                                               | Course A – Introduction to Math  |
| 3   | Observe the filter panel                                                      | The **Class** filter section is still NOT visible — no class list appears                          |                                  |
| 4   | Confirm the Individual lesson linked to Course A is shown on the calendar     | The Individual lesson is visible on the calendar (course filter applies; no class filter expected) |                                  |

**Severity:** major
**Priority:** high

---

### Calendar Filter – Class Section – Group Lesson Type – Course Selected – Class Section Becomes Visible

**Description:** BR-10, BR-11 — State Transition Testing — Confirms that selecting a course when the lesson type is "Group" (or "All") makes the class filter section appear, populated with all classes under that course.

**Preconditions:**
- Feature flag `Multiple_Classes_In_Lesson__c` is set to TRUE
- "Course A – Introduction to Math" has 3 classes: Class Alpha, Class Beta, Class Gamma
- At least one Group lesson linked to Course A exists on the calendar
- Logged in as HQ or CM Staff to the Salesforce org
- SF Mana Calendar filter panel is open; lesson type is set to **Group** or **All**

| #   | Action                                                          | Expected Result                                                                           | Test Data                        |
| --- | --------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | -------------------------------- |
| 1   | In the Calendar filter, confirm lesson type is **Group** or **All** | Lesson type is Group or All                                                           |                                  |
| 2   | In the Course filter, select **"Course A – Introduction to Math"** | Course A is selected                                                                   | Course A – Introduction to Math  |
| 3   | Observe the filter panel below the Course section               | The **Class** filter section appears; a list of classes under Course A is displayed       |                                  |
| 4   | Observe the classes listed and their checkbox states            | Class Alpha, Class Beta, and Class Gamma are all listed; all 3 are in **unchecked** state |                                  |

**Severity:** major
**Priority:** high
