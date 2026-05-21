# Test Cases: LT-86458 — Validate Start time / End time / Duration fields

**Reference:** https://manabie.atlassian.net/browse/LT-86458  
**Custom Settings required:**

- `MANAERP__Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- `MANAERP__Default_Lesson_Duration_Minutes__c` = e.g. 60 (minutes)

---

## Suite: Lesson

### Lesson – Duration Field – "Enable Duration Field" Custom Setting ON – Field visible on lesson form

**Description:** AC — Field Display — Confirm Duration field appears on the lesson create/edit form when the custom setting "Enable Duration Field on Lesson Form" is enabled.

**Preconditions:**

- Admin is logged in with Create Lesson permission
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Navigate to Lesson Management > Lesson List

| #   | Action                               | Expected Result                                                   | Test Data |
| --- | ------------------------------------ | ----------------------------------------------------------------- | --------- |
| 1   | Click "Create Lesson" button         | Lesson creation form opens                                        | ""        |
| 2   | Observe the Time section of the form | "Duration" field is visible alongside "Start Time" and "End Time" | ""        |

**Severity:** normal  
**Priority:** high

---

### Lesson – Duration Field – Default Duration from Custom Setting – Field pre-filled on form open

**Description:** AC — Default Value — Confirm Duration field is pre-filled with the value defined in "Default Lesson Duration Minutes" custom setting when the form opens.

**Preconditions:**

- Admin is logged in with Create Lesson permission
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Custom Setting `Default_Lesson_Duration_Minutes__c` = 60
- Navigate to Lesson Management > Lesson List

| #   | Action                           | Expected Result                                            | Test Data |
| --- | -------------------------------- | ---------------------------------------------------------- | --------- |
| 1   | Click "Create Lesson" button     | Lesson creation form opens                                 | ""        |
| 2   | Observe the Duration field value | Duration field shows "60" (pre-filled from custom setting) | ""        |

**Severity:** normal  
**Priority:** medium

---

### Lesson – Create – All Three Fields Valid (Start + End + Duration match) – Lesson saved

**Description:** AC — Valid Input — Lesson is successfully saved when Start Time, End Time, and Duration are all provided and consistent (Duration = End − Start).

**Preconditions:**

- Admin is logged in with Create Lesson permission
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Lesson form is open

| #   | Action                                                     | Expected Result                                                                                   | Test Data    |
| --- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ------------ |
| 1   | Select lesson date                                         | Lesson date is set                                                                                | "2026-06-01" |
| 2   | Enter Start Time                                           | Start Time field shows "09:00"                                                                    | "09:00"      |
| 3   | Enter End Time                                             | End Time field shows "10:00"                                                                      | "10:00"      |
| 4   | Enter Duration                                             | Duration field shows "60"                                                                         | "60"         |
| 5   | Fill in all other required fields (subject, teacher, etc.) | Required fields populated                                                                         | ""           |
| 6   | Click "Save"                                               | Lesson is saved successfully; lesson appears in list with Start=09:00, End=10:00, Duration=60 min | ""           |

**Severity:** critical  
**Priority:** high

---

### Lesson – Create – Start Time + Duration provided – End Time auto-calculated

**Description:** AC — Auto-calculation — When Start Time and Duration are entered, End Time is automatically calculated as Start + Duration.

**Preconditions:**

- Admin is logged in with Create Lesson permission
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Lesson form is open
- End Time field is empty

| #   | Action                                     | Expected Result                                              | Test Data |
| --- | ------------------------------------------ | ------------------------------------------------------------ | --------- |
| 1   | Enter Start Time                           | Start Time field shows "09:00"                               | "09:00"   |
| 2   | Enter Duration                             | Duration field shows "90" and End Time auto-fills to "10:30" | "90"      |
| 3   | Observe End Time field                     | End Time = "10:30" (Start 09:00 + Duration 90 min)           | ""        |
| 4   | Click "Save" (with required fields filled) | Lesson saved with Start=09:00, End=10:30, Duration=90 min    | ""        |

**Severity:** critical  
**Priority:** high

---

### Lesson – Create – End Time + Duration provided – Start Time auto-calculated

**Description:** AC — Auto-calculation — When End Time and Duration are entered, Start Time is automatically calculated as End − Duration.

**Preconditions:**

- Admin is logged in with Create Lesson permission
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Lesson form is open
- Start Time field is empty

| #   | Action                                     | Expected Result                                                | Test Data |
| --- | ------------------------------------------ | -------------------------------------------------------------- | --------- |
| 1   | Enter End Time                             | End Time field shows "11:00"                                   | "11:00"   |
| 2   | Enter Duration                             | Duration field shows "60" and Start Time auto-fills to "10:00" | "60"      |
| 3   | Observe Start Time field                   | Start Time = "10:00" (End 11:00 − Duration 60 min)             | ""        |
| 4   | Click "Save" (with required fields filled) | Lesson saved with Start=10:00, End=11:00, Duration=60 min      | ""        |

**Severity:** critical  
**Priority:** high

---

### Lesson – Create – Duration mismatched with Start and End – Save blocked

**Description:** AC — Validation — Lesson cannot be saved when Duration value does not match the difference between End Time and Start Time (all 3 fields filled manually with inconsistent values).

**Preconditions:**

- Admin is logged in with Create Lesson permission
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Lesson form is open

| #   | Action                                              | Expected Result                                                        | Test Data |
| --- | --------------------------------------------------- | ---------------------------------------------------------------------- | --------- |
| 1   | Enter Start Time                                    | Start Time = "09:00"                                                   | "09:00"   |
| 2   | Enter End Time                                      | End Time = "10:00"                                                     | "10:00"   |
| 3   | Manually overwrite Duration with a mismatched value | Duration field shows "90" (mismatched: 10:00 − 09:00 = 60 min, not 90) | "90"      |
| 4   | Click "Save"                                        | Validation error displayed; lesson is NOT saved                        | ""        |
| 5   | Observe error message                               | Error message indicates Duration does not match Start/End difference   | ""        |

**Severity:** major  
**Priority:** high

---

### Lesson – Create – Duration = 0 – Validation error shown

**Description:** AC — Boundary Validation — Entering Duration = 0 must trigger a validation error as a lesson cannot have zero duration.

**Preconditions:**

- Admin is logged in with Create Lesson permission
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Lesson form is open

| #   | Action                     | Expected Result                                             | Test Data |
| --- | -------------------------- | ----------------------------------------------------------- | --------- |
| 1   | Enter Start Time           | Start Time = "09:00"                                        | "09:00"   |
| 2   | Clear Duration and enter 0 | Duration field shows "0"                                    | "0"       |
| 3   | Click "Save"               | Validation error displayed: Duration must be greater than 0 | ""        |
| 4   | Lesson is NOT saved        | System remains on form with error highlighted               | ""        |

**Severity:** major  
**Priority:** high

---

### Lesson – Create – Duration = negative number – Validation error shown

**Description:** AC — Boundary Validation — Entering a negative value in the Duration field must be rejected with a validation error.

**Preconditions:**

- Admin is logged in with Create Lesson permission
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Lesson form is open

| #   | Action                           | Expected Result                                              | Test Data |
| --- | -------------------------------- | ------------------------------------------------------------ | --------- |
| 1   | Enter Start Time                 | Start Time = "09:00"                                         | "09:00"   |
| 2   | Enter negative value in Duration | Duration field shows "-30"                                   | "-30"     |
| 3   | Click "Save"                     | Validation error displayed; negative duration is not allowed | ""        |
| 4   | Lesson is NOT saved              | System remains on form with error                            | ""        |

**Severity:** major  
**Priority:** high

---

### Lesson – Create – Duration = decimal number – Validation error shown

**Description:** AC — Input Validation — Duration field only accepts whole numbers (integers); decimal input must be rejected or not allowed.

**Preconditions:**

- Admin is logged in with Create Lesson permission
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Lesson form is open

| #   | Action                           | Expected Result                                                                     | Test Data |
| --- | -------------------------------- | ----------------------------------------------------------------------------------- | --------- |
| 1   | Enter Start Time                 | Start Time = "09:00"                                                                | "09:00"   |
| 2   | Enter decimal number in Duration | Field either rejects input or shows validation error                                | "30.5"    |
| 3   | Click "Save"                     | System shows validation error or does not accept decimal value; lesson is NOT saved | ""        |

**Severity:** normal  
**Priority:** medium

---

### Lesson – Create – Start time after End time – Save blocked

**Description:** AC — Validation — Start Time must be before End Time; entering Start > End must block save with a validation error.

**Preconditions:**

- Admin is logged in with Create Lesson permission
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Lesson form is open

| #   | Action                                    | Expected Result                                                        | Test Data |
| --- | ----------------------------------------- | ---------------------------------------------------------------------- | --------- |
| 1   | Enter Start Time                          | Start Time = "14:00"                                                   | "14:00"   |
| 2   | Enter End Time that is earlier than Start | End Time = "10:00"                                                     | "10:00"   |
| 3   | Click "Save"                              | Validation error: Start time must be before End time; lesson NOT saved | ""        |

**Severity:** major  
**Priority:** high

---

### Lesson – Create – Start time equals End time – Save blocked

**Description:** AC — Boundary Validation — A lesson with Start Time equal to End Time (Duration = 0) must be blocked.

**Preconditions:**

- Admin is logged in with Create Lesson permission
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Lesson form is open

| #   | Action                        | Expected Result                                                           | Test Data |
| --- | ----------------------------- | ------------------------------------------------------------------------- | --------- |
| 1   | Enter Start Time              | Start Time = "10:00"                                                      | "10:00"   |
| 2   | Enter End Time equal to Start | End Time = "10:00"                                                        | "10:00"   |
| 3   | Click "Save"                  | Validation error: Start and End time cannot be the same; lesson NOT saved | ""        |

**Severity:** major  
**Priority:** high

---

### Lesson – Create – End time exceeds midnight of lesson date – Save blocked

**Description:** AC — Boundary Validation — Start time and End time must fall within the same calendar day (00:00–23:59) of the selected lesson date; crossing midnight must be blocked.

**Preconditions:**

- Admin is logged in with Create Lesson permission
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Lesson form is open, date selected

| #   | Action                                           | Expected Result                                                                                 | Test Data |
| --- | ------------------------------------------------ | ----------------------------------------------------------------------------------------------- | --------- |
| 1   | Enter Start Time close to midnight               | Start Time = "23:00"                                                                            | "23:00"   |
| 2   | Enter Duration that would push End past midnight | Duration = "90" (End would be 00:30 next day)                                                   | "90"      |
| 3   | Click "Save"                                     | Validation error: Start/End time must be within the lesson date (00:00–23:59); lesson NOT saved | ""        |

**Severity:** major  
**Priority:** high

---

### Lesson – Duration Field – Default value from custom setting pre-fills on form open

**Description:** AC — Custom Setting — "Default Lesson Duration Minutes" value is applied to Duration field when lesson form is first opened (default duration pre-fill behavior).

**Preconditions:**

- Admin is logged in
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Custom Setting `Default_Lesson_Duration_Minutes__c` = 45
- Navigate to Lesson Management

| #   | Action                                               | Expected Result                                            | Test Data |
| --- | ---------------------------------------------------- | ---------------------------------------------------------- | --------- |
| 1   | Click "Create Lesson"                                | Form opens                                                 | ""        |
| 2   | Observe the Duration field without entering anything | Duration field is pre-filled with "45" from custom setting | ""        |
| 3   | Enter Start Time                                     | End Time auto-calculates as Start + 45 min                 | "09:00"   |
| 4   | Observe End Time                                     | End Time = "09:45"                                         | ""        |

**Severity:** normal  
**Priority:** medium

---

### Lesson – Edit – Duration entered with Start time set – End time auto-calculated

**Description:** AC — Auto-calculation (Edit) — When editing a lesson and entering Duration while Start Time exists, End Time is auto-calculated.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- An existing lesson exists with Start Time = 09:00, End Time = 10:00, Duration = 60
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                           | Expected Result                                                    | Test Data |
| --- | -------------------------------- | ------------------------------------------------------------------ | --------- |
| 1   | Open existing lesson for editing | Edit form opens showing Start=09:00, End=10:00, Duration=60        | ""        |
| 2   | Clear the Duration field         | Duration field is empty                                            | ""        |
| 3   | Re-enter a new Duration value    | Duration = "90"; End Time auto-updates to "10:30" (09:00 + 90 min) | "90"      |
| 4   | Click "Save"                     | Lesson saved with Start=09:00, End=10:30, Duration=90              | ""        |

**Severity:** major  
**Priority:** high

---

### Lesson – Edit – Start time changed with existing Duration – End time auto-updates

**Description:** AC — Auto-calculation (Edit) — When Start Time is changed on an existing lesson that has a Duration, End Time should auto-update to maintain Start + Duration = End.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- Existing lesson: Start=09:00, End=10:00, Duration=60
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                           | Expected Result                                            | Test Data |
| --- | -------------------------------- | ---------------------------------------------------------- | --------- |
| 1   | Open lesson for editing          | Form shows Start=09:00, End=10:00, Duration=60             | ""        |
| 2   | Change Start Time to a new value | Start Time = "10:00"                                       | "10:00"   |
| 3   | Observe End Time                 | End Time auto-updates to "11:00" (10:00 + 60 min Duration) | ""        |
| 4   | Click "Save"                     | Lesson saved with Start=10:00, End=11:00, Duration=60      | ""        |

**Severity:** major  
**Priority:** high

---

### Lesson – Edit – End time changed with existing Duration – Duration auto-updates

**Description:** AC — Auto-calculation (Edit) — When End Time is changed manually on an existing lesson, Duration auto-updates to reflect new End − Start.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- Existing lesson: Start=09:00, End=10:00, Duration=60
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                         | Expected Result                                        | Test Data |
| --- | ------------------------------ | ------------------------------------------------------ | --------- |
| 1   | Open lesson for editing        | Form shows Start=09:00, End=10:00, Duration=60         | ""        |
| 2   | Change End Time to a new value | End Time = "11:00"                                     | "11:00"   |
| 3   | Observe Duration field         | Duration auto-updates to "120" (11:00 − 09:00)         | ""        |
| 4   | Click "Save"                   | Lesson saved with Start=09:00, End=11:00, Duration=120 | ""        |

**Severity:** major  
**Priority:** high

---

### Lesson – Edit – Duration entered with End time set – Start time auto-calculated

**Description:** AC — Auto-calculation (Edit) — When editing a lesson, entering Duration while End Time is set and Start Time is empty causes Start Time to be auto-calculated.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- Existing lesson: End Time = 11:00, Start Time cleared, Duration = blank
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                   | Expected Result                                                    | Test Data |
| --- | ------------------------ | ------------------------------------------------------------------ | --------- |
| 1   | Open lesson for editing  | Form shows End=11:00, Start is empty                               | ""        |
| 2   | Enter Duration           | Duration = "60"; Start Time auto-fills to "10:00" (11:00 − 60 min) | "60"      |
| 3   | Observe Start Time field | Start Time = "10:00"                                               | ""        |
| 4   | Click "Save"             | Lesson saved with Start=10:00, End=11:00, Duration=60              | ""        |

**Severity:** major  
**Priority:** high

---

### Lesson – Edit – Both Start and End times changed manually – Duration auto-updates

**Description:** AC — Auto-calculation (Edit) — When both Start and End times are manually edited, Duration field auto-updates to reflect the new difference.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- Existing lesson: Start=09:00, End=10:00, Duration=60
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                  | Expected Result                                        | Test Data |
| --- | ----------------------- | ------------------------------------------------------ | --------- |
| 1   | Open lesson for editing | Form shows Start=09:00, End=10:00, Duration=60         | ""        |
| 2   | Change Start Time       | Start Time = "08:00"                                   | "08:00"   |
| 3   | Change End Time         | End Time = "10:30"                                     | "10:30"   |
| 4   | Observe Duration field  | Duration auto-updates to "150" (10:30 − 08:00)         | ""        |
| 5   | Click "Save"            | Lesson saved with Start=08:00, End=10:30, Duration=150 | ""        |

**Severity:** major  
**Priority:** high

---

### Lesson – Edit – Duration edited with both Start and End set – End time auto-adjusts

**Description:** AC — Auto-calculation (Edit) — When Duration is changed while both Start and End are set, End Time auto-adjusts to Start + new Duration.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- Existing lesson: Start=09:00, End=10:00, Duration=60
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                         | Expected Result                                        | Test Data |
| --- | ------------------------------ | ------------------------------------------------------ | --------- |
| 1   | Open lesson for editing        | Form shows Start=09:00, End=10:00, Duration=60         | ""        |
| 2   | Change Duration to a new value | Duration = "120"                                       | "120"     |
| 3   | Observe End Time               | End Time auto-adjusts to "11:00" (09:00 + 120 min)     | ""        |
| 4   | Click "Save"                   | Lesson saved with Start=09:00, End=11:00, Duration=120 | ""        |

**Severity:** major  
**Priority:** high

---

### Lesson – Edit – Duration cleared with Start time set – End time cleared

**Description:** AC — Field Interaction — When Duration is cleared while Start Time is set (End Time was auto-calculated), End Time field clears.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- Existing lesson: Start=09:00, Duration=60, End=10:00 (auto-calc)
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                   | Expected Result                                                           | Test Data |
| --- | ------------------------ | ------------------------------------------------------------------------- | --------- |
| 1   | Open lesson for editing  | Form shows Start=09:00, End=10:00, Duration=60                            | ""        |
| 2   | Clear the Duration field | Duration field is empty                                                   | ""        |
| 3   | Observe End Time field   | End Time field is cleared/empty                                           | ""        |
| 4   | Click "Save"             | System prompts for End Time or shows validation that End Time is required | ""        |

**Severity:** normal  
**Priority:** medium

---

### Lesson – Edit – Duration cleared with End time set – Start time cleared

**Description:** AC — Field Interaction — When Duration is cleared while End Time is set (Start Time was auto-calculated), Start Time field clears.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- Existing lesson: End=11:00, Duration=60, Start=10:00 (auto-calc)
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                   | Expected Result                                         | Test Data |
| --- | ------------------------ | ------------------------------------------------------- | --------- |
| 1   | Open lesson for editing  | Form shows Start=10:00, End=11:00, Duration=60          | ""        |
| 2   | Clear the Duration field | Duration field is empty                                 | ""        |
| 3   | Observe Start Time field | Start Time field is cleared/empty                       | ""        |
| 4   | Click "Save"             | System prompts for Start Time or shows validation error | ""        |

**Severity:** normal  
**Priority:** medium

---

### Lesson – Edit – Duration cleared with both Start and End times set – Times remain, Duration blank

**Description:** AC — Field Interaction — When Duration is cleared while both Start and End are set (manually entered), both time fields remain unchanged and Duration stays blank.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- Existing lesson: Start=09:00, End=10:00, Duration=60 (both manually set)
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                            | Expected Result                                                                                      | Test Data |
| --- | --------------------------------- | ---------------------------------------------------------------------------------------------------- | --------- |
| 1   | Open lesson for editing           | Form shows Start=09:00, End=10:00, Duration=60                                                       | ""        |
| 2   | Clear the Duration field          | Duration is empty                                                                                    | ""        |
| 3   | Observe Start and End Time fields | Start=09:00 and End=10:00 remain unchanged                                                           | ""        |
| 4   | Click "Save"                      | Lesson saves with Start=09:00, End=10:00, Duration blank (if Duration is optional when both are set) | ""        |

**Severity:** normal  
**Priority:** medium

---

### Lesson – Edit – Duration cleared and new Duration entered with both Start and End set – End auto-adjusts

**Description:** AC — Field Interaction — When Duration is cleared and a new Duration is entered while Start and End are both set, End Time auto-adjusts to Start + new Duration.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- Existing lesson: Start=09:00, End=10:00, Duration blank (was cleared)
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                                      | Expected Result                                       | Test Data |
| --- | ------------------------------------------- | ----------------------------------------------------- | --------- |
| 1   | Open lesson for editing with blank Duration | Form shows Start=09:00, End=10:00, Duration is blank  | ""        |
| 2   | Enter a new Duration value                  | Duration = "45"                                       | "45"      |
| 3   | Observe End Time                            | End Time auto-adjusts to "09:45" (09:00 + 45 min)     | ""        |
| 4   | Click "Save"                                | Lesson saved with Start=09:00, End=09:45, Duration=45 | ""        |

**Severity:** normal  
**Priority:** medium

---

### Lesson – Edit – Auto-adjust End Time when Duration matches defined value with manual Start/End

**Description:** AC — Auto-adjustment — When user manually sets all three fields and then corrects Duration to the proper value, End Time auto-adjusts to maintain consistency.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- Existing lesson: Start=09:00, End=10:00, Duration=60
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                       | Expected Result                                       | Test Data |
| --- | ---------------------------- | ----------------------------------------------------- | --------- |
| 1   | Open lesson for editing      | Form shows Start=09:00, End=10:00, Duration=60        | ""        |
| 2   | Change Duration to new value | Duration = "30"                                       | "30"      |
| 3   | Observe End Time             | End Time auto-adjusts to "09:30" (09:00 + 30 min)     | ""        |
| 4   | Click "Save"                 | Lesson saved with Start=09:00, End=09:30, Duration=30 | ""        |

**Severity:** normal  
**Priority:** medium

---

### Lesson – Edit Recurring – "Only this lesson" – Only current lesson's time updated

**Description:** AC — Recurring Edit — When editing a recurring lesson time and choosing "Only this lesson", only the selected occurrence is updated; other lessons in the series remain unchanged.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- A recurring lesson series exists (e.g., every Monday, 5 occurrences: L1, L2, L3, L4, L5)
- All lessons have Start=09:00, End=10:00, Duration=60
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                                      | Expected Result                                                         | Test Data |
| --- | ------------------------------------------- | ----------------------------------------------------------------------- | --------- |
| 1   | Open lesson L3 (3rd occurrence) for editing | Edit form opens for L3                                                  | ""        |
| 2   | Change Start Time                           | Start Time = "10:00"                                                    | "10:00"   |
| 3   | Observe Duration                            | Duration = 60; End Time auto-updates to "11:00"                         | ""        |
| 4   | Click "Save"                                | Recurring scope selector appears (Only this / This and following / All) | ""        |
| 5   | Select "Only this lesson"                   | Scope "Only this" selected                                              | ""        |
| 6   | Confirm save                                | L3 saved with Start=10:00, End=11:00                                    | ""        |
| 7   | Open L2 and L4 to verify                    | L2 and L4 still have Start=09:00, End=10:00, Duration=60 (unchanged)    | ""        |

**Severity:** major  
**Priority:** high

---

### Lesson – Edit Recurring – "This and following" – All subsequent lessons updated

**Description:** AC — Recurring Edit — When editing a recurring lesson time and choosing "This and following", the selected lesson and all subsequent occurrences are updated; past lessons remain unchanged.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- A recurring lesson series exists (5 occurrences: L1, L2, L3, L4, L5)
- All lessons have Start=09:00, End=10:00, Duration=60
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                                           | Expected Result                                           | Test Data |
| --- | ------------------------------------------------ | --------------------------------------------------------- | --------- |
| 1   | Open lesson L3 for editing                       | Edit form opens for L3                                    | ""        |
| 2   | Change Start Time                                | Start Time = "10:00"                                      | "10:00"   |
| 3   | Duration remains 60; End auto-updates to "11:00" | End Time = "11:00"                                        | ""        |
| 4   | Click "Save"                                     | Recurring scope selector appears                          | ""        |
| 5   | Select "This and following"                      | Scope selected                                            | ""        |
| 6   | Confirm save                                     | L3, L4, L5 saved with Start=10:00, End=11:00, Duration=60 | ""        |
| 7   | Open L1 and L2 to verify                         | L1 and L2 still have Start=09:00, End=10:00 (unchanged)   | ""        |

**Severity:** major  
**Priority:** high

---

### Lesson – Edit Recurring – Duration mismatch on recurring lesson – Save blocked

**Description:** AC — Recurring Edit Validation — Editing a recurring lesson with a mismatched Duration should trigger a validation error regardless of the scope chosen.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- A recurring lesson exists: Start=09:00, End=10:00, Duration=60
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                                            | Expected Result                                                                  | Test Data |
| --- | ------------------------------------------------- | -------------------------------------------------------------------------------- | --------- |
| 1   | Open recurring lesson for editing                 | Edit form opens                                                                  | ""        |
| 2   | Manually set Start Time                           | Start Time = "09:00"                                                             | "09:00"   |
| 3   | Manually set End Time                             | End Time = "10:00"                                                               | "10:00"   |
| 4   | Manually overwrite Duration with mismatched value | Duration = "90" (mismatch: 10:00 − 09:00 = 60)                                   | "90"      |
| 5   | Click "Save"                                      | Validation error: Duration does not match Start/End difference; lesson NOT saved | ""        |

**Severity:** major  
**Priority:** high

---

## Suite: Calendar

### Calendar – Duration Field – "Enable Duration Field" Custom Setting ON – Field visible on lesson form

**Description:** AC — Field Display — Confirm Duration field appears on the lesson create/edit form when accessed from the Calendar view (SF or BO) and custom setting is enabled.

**Preconditions:**

- Admin is logged in with Create Lesson permission
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Navigate to Calendar (SF or BO)

| #   | Action                                                  | Expected Result                                                   | Test Data |
| --- | ------------------------------------------------------- | ----------------------------------------------------------------- | --------- |
| 1   | Click on a time slot or "Create Lesson" on the Calendar | Lesson creation form opens                                        | ""        |
| 2   | Observe the Time section of the form                    | "Duration" field is visible alongside "Start Time" and "End Time" | ""        |

**Severity:** normal  
**Priority:** high

---

### Calendar – Duration Field – Default Duration from Custom Setting – Field pre-filled on form open

**Description:** AC — Default Value — Duration field is pre-filled with "Default Lesson Duration Minutes" value when lesson form is opened from Calendar.

**Preconditions:**

- Admin is logged in
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Custom Setting `Default_Lesson_Duration_Minutes__c` = 60
- Navigate to Calendar

| #   | Action                                                     | Expected Result                                | Test Data |
| --- | ---------------------------------------------------------- | ---------------------------------------------- | --------- |
| 1   | Click on a Calendar time slot to open lesson creation form | Form opens                                     | ""        |
| 2   | Observe Duration field                                     | Duration = "60" pre-filled from custom setting | ""        |

**Severity:** normal  
**Priority:** medium

---

### Calendar – Create – All Three Fields Valid (Start + End + Duration match) – Lesson saved

**Description:** AC — Valid Input — Lesson created from Calendar is saved when all three time fields are consistent.

**Preconditions:**

- Admin is logged in with Create Lesson permission
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Calendar view is open

| #   | Action                                           | Expected Result                                  | Test Data           |
| --- | ------------------------------------------------ | ------------------------------------------------ | ------------------- |
| 1   | Click on Calendar time slot for 2026-06-01 09:00 | Lesson form opens with Start=09:00 pre-filled    | "2026-06-01, 09:00" |
| 2   | Confirm or enter Start Time                      | Start Time = "09:00"                             | "09:00"             |
| 3   | Enter End Time                                   | End Time = "10:00"                               | "10:00"             |
| 4   | Enter Duration                                   | Duration = "60"                                  | "60"                |
| 5   | Fill required fields and click "Save"            | Lesson saved; appears on Calendar at 09:00–10:00 | ""                  |

**Severity:** critical  
**Priority:** high

---

### Calendar – Create – Start Time + Duration provided – End Time auto-calculated

**Description:** AC — Auto-calculation — When creating a lesson from Calendar with Start Time and Duration, End Time auto-calculates.

**Preconditions:**

- Admin is logged in with Create Lesson permission
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Calendar view is open

| #   | Action                                          | Expected Result                                     | Test Data |
| --- | ----------------------------------------------- | --------------------------------------------------- | --------- |
| 1   | Click on Calendar time slot to open lesson form | Lesson form opens                                   | ""        |
| 2   | Enter Start Time                                | Start Time = "09:00"                                | "09:00"   |
| 3   | Enter Duration                                  | Duration = "90"                                     | "90"      |
| 4   | Observe End Time                                | End Time = "10:30" (09:00 + 90 min) auto-calculated | ""        |
| 5   | Click "Save"                                    | Lesson saved; appears on Calendar at 09:00–10:30    | ""        |

**Severity:** critical  
**Priority:** high

---

### Calendar – Create – End Time + Duration provided – Start Time auto-calculated

**Description:** AC — Auto-calculation — When creating from Calendar with End Time and Duration, Start Time auto-calculates.

**Preconditions:**

- Admin is logged in with Create Lesson permission
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Calendar view is open

| #   | Action                                  | Expected Result                                       | Test Data |
| --- | --------------------------------------- | ----------------------------------------------------- | --------- |
| 1   | Open lesson creation form from Calendar | Form opens                                            | ""        |
| 2   | Enter End Time                          | End Time = "11:00"                                    | "11:00"   |
| 3   | Enter Duration                          | Duration = "60"                                       | "60"      |
| 4   | Observe Start Time                      | Start Time = "10:00" (11:00 − 60 min) auto-calculated | ""        |
| 5   | Click "Save"                            | Lesson saved; appears on Calendar at 10:00–11:00      | ""        |

**Severity:** critical  
**Priority:** high

---

### Calendar – Create – Duration mismatched with Start and End – Save blocked

**Description:** AC — Validation — Duration mismatch blocks save from Calendar lesson creation form.

**Preconditions:**

- Admin is logged in with Create Lesson permission
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Calendar view is open, lesson creation form open

| #   | Action                                   | Expected Result                    | Test Data |
| --- | ---------------------------------------- | ---------------------------------- | --------- |
| 1   | Enter Start Time                         | Start Time = "09:00"               | "09:00"   |
| 2   | Enter End Time                           | End Time = "10:00"                 | "10:00"   |
| 3   | Overwrite Duration with mismatched value | Duration = "90"                    | "90"      |
| 4   | Click "Save"                             | Validation error; lesson NOT saved | ""        |

**Severity:** major  
**Priority:** high

---

### Calendar – Create – Duration = 0 – Validation error shown

**Description:** AC — Boundary Validation — Duration = 0 blocks save from Calendar.

**Preconditions:**

- Admin is logged in with Create Lesson permission
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Lesson form open from Calendar

| #   | Action             | Expected Result                                                     | Test Data |
| --- | ------------------ | ------------------------------------------------------------------- | --------- |
| 1   | Enter Start Time   | Start Time = "09:00"                                                | "09:00"   |
| 2   | Enter Duration = 0 | Duration = "0"                                                      | "0"       |
| 3   | Click "Save"       | Validation error: Duration must be greater than 0; lesson NOT saved | ""        |

**Severity:** major  
**Priority:** high

---

### Calendar – Create – Duration = negative number – Validation error shown

**Description:** AC — Boundary Validation — Negative Duration blocks save from Calendar.

**Preconditions:**

- Admin is logged in
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Lesson form open from Calendar

| #   | Action                  | Expected Result                                                   | Test Data |
| --- | ----------------------- | ----------------------------------------------------------------- | --------- |
| 1   | Enter Start Time        | Start Time = "09:00"                                              | "09:00"   |
| 2   | Enter negative Duration | Duration = "-30"                                                  | "-30"     |
| 3   | Click "Save"            | Validation error: negative duration not allowed; lesson NOT saved | ""        |

**Severity:** major  
**Priority:** high

---

### Calendar – Create – Duration = decimal number – Validation error shown

**Description:** AC — Input Validation — Decimal Duration input is rejected in Calendar lesson form.

**Preconditions:**

- Admin is logged in
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Lesson form open from Calendar

| #   | Action                          | Expected Result                                                          | Test Data |
| --- | ------------------------------- | ------------------------------------------------------------------------ | --------- |
| 1   | Enter Start Time                | Start Time = "09:00"                                                     | "09:00"   |
| 2   | Enter decimal value in Duration | Duration field = "30.5"                                                  | "30.5"    |
| 3   | Click "Save"                    | System shows validation error or rejects decimal input; lesson NOT saved | ""        |

**Severity:** normal  
**Priority:** medium

---

### Calendar – Create – Start time after End time – Save blocked

**Description:** AC — Validation — Start > End blocks save in Calendar lesson creation.

**Preconditions:**

- Admin is logged in with Create Lesson permission
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Lesson form open from Calendar

| #   | Action                            | Expected Result                                              | Test Data |
| --- | --------------------------------- | ------------------------------------------------------------ | --------- |
| 1   | Enter Start Time                  | Start Time = "14:00"                                         | "14:00"   |
| 2   | Enter End Time earlier than Start | End Time = "10:00"                                           | "10:00"   |
| 3   | Click "Save"                      | Validation error: Start must be before End; lesson NOT saved | ""        |

**Severity:** major  
**Priority:** high

---

### Calendar – Create – Start time equals End time – Save blocked

**Description:** AC — Boundary Validation — Start = End time blocks save from Calendar.

**Preconditions:**

- Admin is logged in
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Lesson form open from Calendar

| #   | Action                        | Expected Result                                                      | Test Data |
| --- | ----------------------------- | -------------------------------------------------------------------- | --------- |
| 1   | Enter Start Time              | Start Time = "10:00"                                                 | "10:00"   |
| 2   | Enter End Time equal to Start | End Time = "10:00"                                                   | "10:00"   |
| 3   | Click "Save"                  | Validation error: Start and End cannot be the same; lesson NOT saved | ""        |

**Severity:** major  
**Priority:** high

---

### Calendar – Create – End time exceeds midnight of lesson date – Save blocked

**Description:** AC — Boundary Validation — Start/End time cannot cross midnight from Calendar.

**Preconditions:**

- Admin is logged in
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled
- Lesson form open from Calendar, date selected

| #   | Action                                    | Expected Result                                                       | Test Data |
| --- | ----------------------------------------- | --------------------------------------------------------------------- | --------- |
| 1   | Enter Start Time near midnight            | Start Time = "23:00"                                                  | "23:00"   |
| 2   | Enter Duration that would exceed midnight | Duration = "90" (End = 00:30 next day)                                | "90"      |
| 3   | Click "Save"                              | Validation error: time must stay within lesson date; lesson NOT saved | ""        |

**Severity:** major  
**Priority:** high

---

### Calendar – Edit – Duration entered with Start time set – End time auto-calculated

**Description:** AC — Auto-calculation (Edit via Calendar) — Entering Duration with Start set auto-calculates End.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- Existing lesson on Calendar: Start=09:00, End=10:00, Duration=60
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                                        | Expected Result                                                 | Test Data |
| --- | --------------------------------------------- | --------------------------------------------------------------- | --------- |
| 1   | Click on lesson on Calendar to open edit form | Form shows Start=09:00, End=10:00, Duration=60                  | ""        |
| 2   | Clear Duration and enter new value            | Duration = "90"                                                 | "90"      |
| 3   | Observe End Time                              | End Time auto-updates to "10:30" (09:00 + 90 min)               | ""        |
| 4   | Click "Save"                                  | Lesson saved with new End=10:30; Calendar reflects updated time | ""        |

**Severity:** major  
**Priority:** high

---

### Calendar – Edit – Start time changed with existing Duration – End time auto-updates

**Description:** AC — Auto-calculation (Edit via Calendar) — Changing Start Time with Duration set auto-updates End Time.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- Existing lesson on Calendar: Start=09:00, End=10:00, Duration=60
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                                        | Expected Result                                                      | Test Data |
| --- | --------------------------------------------- | -------------------------------------------------------------------- | --------- |
| 1   | Click on lesson on Calendar to open edit form | Form shows Start=09:00, End=10:00, Duration=60                       | ""        |
| 2   | Change Start Time                             | Start Time = "10:00"                                                 | "10:00"   |
| 3   | Observe End Time                              | End Time auto-updates to "11:00" (10:00 + 60 min)                    | ""        |
| 4   | Click "Save"                                  | Lesson saved with Start=10:00, End=11:00; Calendar reflects new time | ""        |

**Severity:** major  
**Priority:** high

---

### Calendar – Edit – End time changed with existing Duration – Duration auto-updates

**Description:** AC — Auto-calculation (Edit via Calendar) — Changing End Time manually auto-updates Duration.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- Existing lesson on Calendar: Start=09:00, End=10:00, Duration=60
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                                        | Expected Result                                                           | Test Data |
| --- | --------------------------------------------- | ------------------------------------------------------------------------- | --------- |
| 1   | Click on lesson on Calendar to open edit form | Form shows Start=09:00, End=10:00, Duration=60                            | ""        |
| 2   | Change End Time                               | End Time = "11:00"                                                        | "11:00"   |
| 3   | Observe Duration                              | Duration auto-updates to "120" (11:00 − 09:00)                            | ""        |
| 4   | Click "Save"                                  | Lesson saved with End=11:00, Duration=120; Calendar reflects new duration | ""        |

**Severity:** major  
**Priority:** high

---

### Calendar – Edit – Both Start and End changed manually – Duration auto-updates

**Description:** AC — Auto-calculation (Edit via Calendar) — Both Start and End changed manually causes Duration to update.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- Existing lesson on Calendar: Start=09:00, End=10:00, Duration=60
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                       | Expected Result                                        | Test Data |
| --- | ---------------------------- | ------------------------------------------------------ | --------- |
| 1   | Open edit form from Calendar | Form shows Start=09:00, End=10:00, Duration=60         | ""        |
| 2   | Change Start Time            | Start Time = "08:00"                                   | "08:00"   |
| 3   | Change End Time              | End Time = "10:30"                                     | "10:30"   |
| 4   | Observe Duration             | Duration auto-updates to "150"                         | ""        |
| 5   | Click "Save"                 | Lesson saved with Start=08:00, End=10:30, Duration=150 | ""        |

**Severity:** major  
**Priority:** high

---

### Calendar – Edit – Duration cleared with Start time set – End time cleared

**Description:** AC — Field Interaction (Calendar Edit) — Clearing Duration with Start set clears End Time.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- Existing lesson: Start=09:00, End=10:00, Duration=60
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                       | Expected Result                                | Test Data |
| --- | ---------------------------- | ---------------------------------------------- | --------- |
| 1   | Open edit form from Calendar | Form shows Start=09:00, End=10:00, Duration=60 | ""        |
| 2   | Clear Duration field         | Duration = empty                               | ""        |
| 3   | Observe End Time             | End Time field is cleared                      | ""        |
| 4   | Click "Save"                 | Validation or prompt: End Time is required     | ""        |

**Severity:** normal  
**Priority:** medium

---

### Calendar – Edit – Duration cleared with End time set – Start time cleared

**Description:** AC — Field Interaction (Calendar Edit) — Clearing Duration with End set clears Start Time.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- Existing lesson: Start=10:00 (auto-calc), End=11:00, Duration=60
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                       | Expected Result                                | Test Data |
| --- | ---------------------------- | ---------------------------------------------- | --------- |
| 1   | Open edit form from Calendar | Form shows Start=10:00, End=11:00, Duration=60 | ""        |
| 2   | Clear Duration field         | Duration = empty                               | ""        |
| 3   | Observe Start Time           | Start Time field is cleared                    | ""        |
| 4   | Click "Save"                 | Validation or prompt: Start Time is required   | ""        |

**Severity:** normal  
**Priority:** medium

---

### Calendar – Edit – Duration cleared with both Start and End set – Times remain, Duration blank

**Description:** AC — Field Interaction (Calendar Edit) — Clearing Duration when both Start and End are manually set keeps both time fields.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- Existing lesson: Start=09:00, End=10:00, Duration=60 (both manual)
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                       | Expected Result                                | Test Data |
| --- | ---------------------------- | ---------------------------------------------- | --------- |
| 1   | Open edit form from Calendar | Form shows Start=09:00, End=10:00, Duration=60 | ""        |
| 2   | Clear Duration               | Duration = empty                               | ""        |
| 3   | Observe Start and End        | Start=09:00, End=10:00 remain unchanged        | ""        |
| 4   | Click "Save"                 | Lesson saves; Duration field is blank          | ""        |

**Severity:** normal  
**Priority:** medium

---

### Calendar – Edit – Duration cleared, new Duration entered with Start and End set – End auto-adjusts

**Description:** AC — Field Interaction (Calendar Edit) — After clearing Duration and entering a new value with both Start and End set, End auto-adjusts.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- Existing lesson: Start=09:00, End=10:00, Duration blank
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                       | Expected Result                                       | Test Data |
| --- | ---------------------------- | ----------------------------------------------------- | --------- |
| 1   | Open edit form from Calendar | Form shows Start=09:00, End=10:00, Duration blank     | ""        |
| 2   | Enter new Duration           | Duration = "45"                                       | "45"      |
| 3   | Observe End Time             | End Time auto-adjusts to "09:45" (09:00 + 45 min)     | ""        |
| 4   | Click "Save"                 | Lesson saved with Start=09:00, End=09:45, Duration=45 | ""        |

**Severity:** normal  
**Priority:** medium

---

### Calendar – Edit Recurring – "Only this lesson" – Only current occurrence updated

**Description:** AC — Recurring Edit (Calendar) — Editing a recurring lesson from Calendar and choosing "Only this lesson" updates only that occurrence.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- A recurring lesson series on Calendar: 5 occurrences, each Start=09:00, End=10:00, Duration=60
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                                                | Expected Result                                    | Test Data |
| --- | ----------------------------------------------------- | -------------------------------------------------- | --------- |
| 1   | Click on 3rd occurrence on Calendar to open edit form | Edit form opens for occurrence 3                   | ""        |
| 2   | Change Start Time                                     | Start Time = "10:00"                               | "10:00"   |
| 3   | Duration = 60; End = "11:00" auto-updates             | End Time = "11:00"                                 | ""        |
| 4   | Click "Save" → Select "Only this lesson"              | Save with scope "Only this"                        | ""        |
| 5   | Verify occurrence 3 on Calendar                       | Start=10:00, End=11:00                             | ""        |
| 6   | Verify occurrences 2 and 4 on Calendar                | Both still show Start=09:00, End=10:00 (unchanged) | ""        |

**Severity:** major  
**Priority:** high

---

### Calendar – Edit Recurring – "This and following" – All subsequent occurrences updated

**Description:** AC — Recurring Edit (Calendar) — Choosing "This and following" from Calendar updates the selected and all future occurrences.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- A recurring lesson series on Calendar: 5 occurrences, each Start=09:00, End=10:00, Duration=60
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                                     | Expected Result                               | Test Data |
| --- | ------------------------------------------ | --------------------------------------------- | --------- |
| 1   | Click on 3rd occurrence on Calendar        | Edit form opens for occurrence 3              | ""        |
| 2   | Change Start Time                          | Start Time = "10:00"                          | "10:00"   |
| 3   | Duration = 60; End = "11:00"               | End Time = "11:00"                            | ""        |
| 4   | Click "Save" → Select "This and following" | Save with scope                               | ""        |
| 5   | Verify occurrences 3, 4, 5 on Calendar     | All show Start=10:00, End=11:00, Duration=60  | ""        |
| 6   | Verify occurrences 1, 2 on Calendar        | Still show Start=09:00, End=10:00 (unchanged) | ""        |

**Severity:** major  
**Priority:** high

---

### Calendar – Edit Recurring – Duration mismatch on recurring lesson – Save blocked

**Description:** AC — Recurring Edit Validation (Calendar) — Duration mismatch blocks save for recurring lessons edited from Calendar.

**Preconditions:**

- Admin is logged in with Edit Lesson permission
- A recurring lesson on Calendar: Start=09:00, End=10:00, Duration=60
- Custom Setting `Enable_Duration_Field_on_Lesson_Form__c` = Enabled

| #   | Action                                            | Expected Result                                                           | Test Data |
| --- | ------------------------------------------------- | ------------------------------------------------------------------------- | --------- |
| 1   | Click on a recurring lesson on Calendar to edit   | Edit form opens                                                           | ""        |
| 2   | Manually enter Start Time                         | Start Time = "09:00"                                                      | "09:00"   |
| 3   | Manually enter End Time                           | End Time = "10:00"                                                        | "10:00"   |
| 4   | Manually overwrite Duration with mismatched value | Duration = "90"                                                           | "90"      |
| 5   | Click "Save"                                      | Validation error: Duration does not match Start/End difference; NOT saved | ""        |

**Severity:** major  
**Priority:** high
