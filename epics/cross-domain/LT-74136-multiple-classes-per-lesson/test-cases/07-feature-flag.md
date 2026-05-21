# Test Cases: LT-74136 — Multiple Classes per Lesson

## Suite: Feature Flag

---

### Multiple Classes – Feature Flag OFF – Lesson Creation – Class Field Shows Single-Select Only

**Description:** BR-39 — Decision Table (Deep) — Validates that when the Multiple Classes feature flag is disabled, the lesson creation form reverts to a single-select Class field and multi-class selection is not possible.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` set to FALSE (flag OFF)
- Course "Test Course MC" has multiple classes available
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                      | Expected Result                                                                        | Test Data                                        |
| --- | ----------------------------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------ |
| 1   | Navigate to the SF Lessons tab and click "New Lesson"       | New Lesson creation form opens                                                         | ""                                               |
| 2   | Set Teaching Method = "Group" and Course = "Test Course MC" | Teaching Method and Course set                                                         | Teaching Method = Group; Course = Test Course MC |
| 3   | Locate the Class field                                      | Class field is present as a single-select field (not a multi-select)                   | ""                                               |
| 4   | Attempt to select more than one class                       | Only one class can be selected at a time; the field does not allow multiple selections | ""                                               |
| 5   | Select one class and save the lesson                        | Lesson saved with a single class; no multi-class configuration is shown                | Class = Class Alpha                              |

**Severity:** major
**Priority:** high

---

### Multiple Classes – Feature Flag OFF – Existing Multi-Class Lesson – Displays as Single Class

**Description:** BR-39 — Decision Table (Deep) — Validates that when the feature flag is turned OFF after a multi-class lesson was created, the lesson reverts to showing a single class on SF Lesson Detail and BO Lesson Detail.

**Preconditions:**

- SF org and BO with flags initially ON
- Lesson "Lesson MC-Flag" has 2 LSC records: Class Alpha and Class Beta; SF and BO both show "Class Alpha, Class Beta"
- The flag `Multiple_Classes_In_Lesson__c` can be toggled by an admin

| #   | Action                                                                                   | Expected Result                                                                                  | Test Data  |
| --- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ---------- |
| 1   | With flag ON, navigate to SF Lesson Detail for "Lesson MC-Flag" and read the Class field | Class field shows "Class Alpha, Class Beta" (multi-class display is active)                      | ""         |
| 2   | Turn the flag `Multiple_Classes_In_Lesson__c` to FALSE (disabled)                        | Flag is now OFF                                                                                  | Flag = OFF |
| 3   | Navigate to SF Lesson Detail for "Lesson MC-Flag"                                        | SF Lesson Detail is displayed                                                                    | ""         |
| 4   | Read the Class field value                                                               | Class field shows a single class (the first/primary class only); multi-class display is reverted | ""         |
| 5   | Navigate to BO Lesson Detail for "Lesson MC-Flag"                                        | BO Lesson Detail is displayed                                                                    | ""         |
| 6   | Read the Class field value in BO                                                         | BO Class field also shows a single class (consistent with SF)                                    | ""         |

**Severity:** major
**Priority:** high

---

### Multiple Classes – Feature Flag Cycle – Flag ON Then OFF Then ON – Multi-Class Lesson Restores Full Display

**Description:** BR-39 — State Transition Testing — Validates that the multi-class display is fully restored after the feature flag is toggled from ON to OFF and back to ON, confirming the data is not permanently lost when the flag is disabled.

**Preconditions:**

- SF org with `Multiple_Classes_In_Lesson__c` flag currently ON
- Lesson "Lesson MC-Flag" has 2 LSC records: Class Alpha and Class Beta
- Flags can be toggled by an admin

| #   | Action                                                                                      | Expected Result                                                                                                                                     | Test Data  |
| --- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| 1   | With flag ON, confirm SF Lesson Detail for "Lesson MC-Flag" shows "Class Alpha, Class Beta" | Class field shows "Class Alpha, Class Beta"                                                                                                         | ""         |
| 2   | Turn the flag OFF                                                                           | Flag is now OFF                                                                                                                                     | Flag = OFF |
| 3   | Navigate to SF Lesson Detail for "Lesson MC-Flag"                                           | Class field shows single class (reverted)                                                                                                           | ""         |
| 4   | Turn the flag back ON                                                                       | Flag is now ON                                                                                                                                      | Flag = ON  |
| 5   | Navigate to SF Lesson Detail for "Lesson MC-Flag"                                           | Lesson Detail page is displayed                                                                                                                     | ""         |
| 6   | Read the Class field value                                                                  | Class field shows "Class Alpha, Class Beta" again — both classes are restored (the LSC records were never deleted; only the display was suppressed) | ""         |

**Severity:** major
**Priority:** high
