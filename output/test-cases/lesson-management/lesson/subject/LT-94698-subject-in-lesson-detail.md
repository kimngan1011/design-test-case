# Test Cases: LT-94698 — Subject in Lesson Detail

## Suite: Subject – Set & Display

---

### Lesson Detail – SF – Create One-Time Lesson with Subject – Subject Saved and Displayed

**Description:** AC 01.1 — Equivalence Partitioning — Create a one-time lesson on SF with a subject selected from Subject Master lookup; confirm subject is saved and displayed correctly.

**Preconditions:**

- Logged in as HQ or CM user on SF
- Subject Master has at least one active record (e.g., Math, English)
- User has created master data (Location, AY, Course, Class)

| #   | Action                                                          | Expected Result                                          | Test Data     |
| --- | --------------------------------------------------------------- | -------------------------------------------------------- | ------------- |
| 1   | Go to Manabie Lesson → Lesson tab → click "New"                 | Create lesson form opens                                 |               |
| 2   | Fill in required lesson fields for a one-time individual lesson | All required fields populated                            |               |
| 3   | Click on Subject field                                          | Subject Master lookup opens with searchable list         |               |
| 4   | Select a subject from the lookup                                | Subject field shows the selected subject name            | Subject: Math |
| 5   | Click "Save"                                                    | Lesson created; redirected to lesson detail page         |               |
| 6   | Observe Subject field on lesson detail                          | Subject displays "Math" and is positioned above Location |               |

**Severity:** critical
**Priority:** high

---

### Lesson Detail – SF – Edit Subject to Different Value – Subject Updated on Detail Page

**Description:** AC 01.1 — Equivalence Partitioning — Edit an existing lesson's subject to a different Subject Master value; confirm the new subject is saved.

**Preconditions:**

- Logged in as HQ or CM user on SF
- A one-time lesson exists with Subject = "Math"

| #   | Action                                                | Expected Result                                     | Test Data        |
| --- | ----------------------------------------------------- | --------------------------------------------------- | ---------------- |
| 1   | Open existing lesson detail page                      | Lesson detail with Subject = "Math" displayed       |                  |
| 2   | Click "Edit"                                          | Lesson enters edit mode                             |                  |
| 3   | Click on Subject field and select a different subject | Subject field updated to the new value              | Subject: English |
| 4   | Click "Save"                                          | Lesson saved; detail page shows Subject = "English" |                  |

**Severity:** major
**Priority:** high

---

### Lesson Detail – SF – Clear Subject from Lesson – Lesson Saved Without Subject

**Description:** AC 01.1 / AC 01.2 — Equivalence Partitioning — Clear the subject from a lesson that has one; confirm lesson saves without error.

**Preconditions:**

- Logged in as HQ or CM user on SF
- A lesson exists with Subject = "English"

| #   | Action                                         | Expected Result                                     | Test Data |
| --- | ---------------------------------------------- | --------------------------------------------------- | --------- |
| 1   | Open lesson detail page                        | Lesson detail with Subject = "English" displayed    |           |
| 2   | Click "Edit"                                   | Lesson enters edit mode                             |           |
| 3   | Clear the Subject field (remove current value) | Subject field is empty                              |           |
| 4   | Click "Save"                                   | Lesson saved; Subject field is empty on detail page |           |

**Severity:** major
**Priority:** high

---

### Lesson Detail – SF – Create Lesson Without Subject – Lesson Saved with Empty Subject

**Description:** AC 01.2 — Equivalence Partitioning — Create a lesson without selecting any subject; confirm lesson saves without error.

**Preconditions:**

- Logged in as HQ or CM user on SF
- User has created master data (Location, AY, Course, Class)

| #   | Action                                                    | Expected Result                                          | Test Data |
| --- | --------------------------------------------------------- | -------------------------------------------------------- | --------- |
| 1   | Go to Manabie Lesson → Lesson tab → click "New"           | Create lesson form opens                                 |           |
| 2   | Fill in all required fields but leave Subject field empty | All required fields populated; Subject is blank          |           |
| 3   | Click "Save"                                              | Lesson created without error; Subject is empty on detail |           |

**Severity:** normal
**Priority:** medium

---

### Lesson Detail – SF – Subject Field – Single-Select Behavior – Only One Subject Selectable

**Description:** AC 01.3 — Equivalence Partitioning — Confirm Subject field is single-select; selecting a new value replaces the old value.

**Preconditions:**

- Logged in as HQ or CM user on SF
- Subject Master has at least two records (e.g., Math, English)
- A lesson exists without a subject

| #   | Action                                         | Expected Result                                                   | Test Data        |
| --- | ---------------------------------------------- | ----------------------------------------------------------------- | ---------------- |
| 1   | Open lesson detail → click "Edit"              | Lesson enters edit mode                                           |                  |
| 2   | Click Subject field and select "Math"          | Subject field shows "Math"                                        | Subject: Math    |
| 3   | Click Subject field again and select "English" | Subject field shows "English" (replaces "Math", not multi-select) | Subject: English |
| 4   | Click "Save"                                   | Lesson saved with Subject = "English"                             |                  |

**Severity:** normal
**Priority:** medium

---

### Lesson Detail – SF – Subject Displayed Above Location on Detail Page

**Description:** AC 03.1 — Regression Analysis — Confirm Subject field is positioned above Location on SF Lesson Detail page.

**Preconditions:**

- Logged in as HQ or CM user on SF
- A lesson exists with Subject = "Math" and Location assigned

| #   | Action                                    | Expected Result                            | Test Data     |
| --- | ----------------------------------------- | ------------------------------------------ | ------------- |
| 1   | Open lesson detail page                   | Lesson detail page loads                   |               |
| 2   | Observe field order in lesson information | Subject field appears above Location field | Subject: Math |

**Severity:** major
**Priority:** high

---

### Lesson Detail – SF Calendar – Lesson Detail Drawer – Subject Displayed

**Description:** AC 03.2 — Regression Analysis — Confirm Subject appears in SF Calendar Lesson Detail Drawer.

**Preconditions:**

- Logged in as HQ or CM user on SF
- A lesson exists with Subject = "Math" on a visible calendar date

| #   | Action                                    | Expected Result                             | Test Data     |
| --- | ----------------------------------------- | ------------------------------------------- | ------------- |
| 1   | Navigate to SF Calendar view              | Calendar view loads with lessons displayed  |               |
| 2   | Click on the lesson with Subject = "Math" | Lesson Detail Drawer opens on the right     |               |
| 3   | Observe lesson detail drawer fields       | Subject = "Math" is displayed in the drawer | Subject: Math |

**Severity:** normal
**Priority:** medium

---

### Lesson Detail – BO – Subject Displayed Above Location on Detail Page

**Description:** AC 03.3 — Regression Analysis — Confirm Subject field appears above Location on BO Lesson Detail page.

**Preconditions:**

- A lesson exists with Subject = "Math"
- Logged in to Backoffice

| #   | Action                                          | Expected Result                                            | Test Data     |
| --- | ----------------------------------------------- | ---------------------------------------------------------- | ------------- |
| 1   | Navigate to Lesson Management → open the lesson | Lesson detail page loads on BO                             |               |
| 2   | Observe lesson information fields               | Subject = "Math" displayed above Location on lesson detail | Subject: Math |

**Severity:** major
**Priority:** high

---

### Lesson Detail – BO Calendar – Lesson Detail Drawer – Subject Displayed

**Description:** AC 03.4 — Regression Analysis — Confirm Subject appears in BO Calendar Lesson Detail Drawer.

**Preconditions:**

- A lesson exists with Subject = "Math" on a visible calendar date
- Logged in to Backoffice

| #   | Action                                    | Expected Result                             | Test Data     |
| --- | ----------------------------------------- | ------------------------------------------- | ------------- |
| 1   | Navigate to BO Calendar view              | Calendar view loads with lessons displayed  |               |
| 2   | Click on the lesson with Subject = "Math" | Lesson Detail Drawer opens                  |               |
| 3   | Observe lesson detail drawer fields       | Subject = "Math" is displayed in the drawer | Subject: Math |

**Severity:** normal
**Priority:** medium

---

### Lesson Detail – Mobile Learning App – Student Views Lesson with Subject – Subject Displayed

**Description:** AC 03.5 — Regression Analysis — Confirm Subject is visible to students on Mobile Learning App.

**Preconditions:**

- A lesson exists with Subject = "Math" and a student assigned
- Student has Mobile Learning App access

| #   | Action                                         | Expected Result                                    | Test Data     |
| --- | ---------------------------------------------- | -------------------------------------------------- | ------------- |
| 1   | Student logs into Mobile Learning App          | Student dashboard loads                            |               |
| 2   | Student opens the lesson with Subject = "Math" | Lesson detail displayed on mobile                  |               |
| 3   | Observe lesson information                     | Subject = "Math" is displayed in the lesson detail | Subject: Math |

**Severity:** major
**Priority:** high

---

### Lesson Detail – Mobile Learning App – Lesson Without Subject – No Subject Shown

**Description:** AC 03.5 / AC 01.2 — Regression Analysis — Confirm that lessons without a subject do not show an empty or broken Subject field on Mobile.

**Preconditions:**

- A lesson exists without a subject and a student assigned
- Student has Mobile Learning App access

| #   | Action                                     | Expected Result                                                | Test Data |
| --- | ------------------------------------------ | -------------------------------------------------------------- | --------- |
| 1   | Student logs into Mobile Learning App      | Student dashboard loads                                        |           |
| 2   | Student opens the lesson without a subject | Lesson detail displayed on mobile                              |           |
| 3   | Observe lesson information                 | Subject field is either empty or hidden; no broken UI elements |           |

**Severity:** normal
**Priority:** medium

---

### Calendar SF – Create Lesson – Subject Field Present and Saved Correctly

**Description:** AC 01.1 — Equivalence Partitioning — Create a lesson directly from SF Calendar; confirm Subject field is available in the create form and the selected subject is saved and displayed correctly.

**Preconditions:**

- Logged in as HQ or CM user on SF
- Subject Master has at least one active record (e.g., Math, English)
- User has created master data (Location, AY, Course, Class)

| #   | Action                                                               | Expected Result                                                      | Test Data     |
| --- | -------------------------------------------------------------------- | -------------------------------------------------------------------- | ------------- |
| 1   | Navigate to SF Calendar view                                         | Calendar view loads                                                  |               |
| 2   | Click on an empty time slot to create a new lesson from the calendar | Create lesson form opens (inline or as a drawer/modal from calendar) |               |
| 3   | Fill in required lesson fields                                       | All required fields populated                                        |               |
| 4   | Click on Subject field and select a subject from the lookup          | Subject field shows the selected subject name                        | Subject: Math |
| 5   | Click "Save"                                                         | Lesson created and appears on calendar                               |               |
| 6   | Click on the newly created lesson in the calendar                    | Lesson Detail Drawer opens                                           |               |
| 7   | Observe Subject field in the drawer                                  | Subject = "Math" is displayed correctly                              | Subject: Math |

**Severity:** major
**Priority:** high

---

### Calendar SF – Lesson Detail Drawer – Edit Subject – Subject Updated

**Description:** AC 01.1 — Equivalence Partitioning — Edit a lesson's subject directly from the SF Calendar Lesson Detail Drawer; confirm the subject change is saved and reflected on the drawer and lesson detail page.

**Preconditions:**

- Logged in as HQ or CM user on SF
- A lesson exists with Subject = "Math" on a visible calendar date
- User has lesson edit permission

| #   | Action                                                   | Expected Result                                                        | Test Data        |
| --- | -------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------- |
| 1   | Navigate to SF Calendar view                             | Calendar view loads with lessons displayed                             |                  |
| 2   | Click on the lesson with Subject = "Math"                | Lesson Detail Drawer opens; Subject = "Math" is visible                |                  |
| 3   | Click "Edit" in the Lesson Detail Drawer                 | Lesson enters edit mode in the drawer                                  |                  |
| 4   | Click on Subject field and select a different subject    | Subject field updated to new value                                     | Subject: English |
| 5   | Click "Save"                                             | Lesson saved; Lesson Detail Drawer shows Subject = "English"           |                  |
| 6   | Navigate to the SF Lesson Detail page of the same lesson | Lesson Detail page opens                                               |                  |
| 7   | Observe Subject field on the detail page                 | Subject = "English" is shown (consistent with change made on calendar) |                  |

**Severity:** major
**Priority:** high

---

### Calendar BO – Lesson Detail Drawer – Edit Subject – Subject Updated

**Description:** AC 01.1 — Equivalence Partitioning — Edit a lesson's subject directly from the BO Calendar Lesson Detail Drawer; confirm the subject change is saved and reflected on the drawer and BO lesson detail page.

**Preconditions:**

- Logged in to Backoffice
- A lesson exists with Subject = "Math" on a visible calendar date
- User has lesson edit permission

| #   | Action                                                   | Expected Result                                                        | Test Data        |
| --- | -------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------- |
| 1   | Navigate to BO Calendar view                             | Calendar view loads with lessons displayed                             |                  |
| 2   | Click on the lesson with Subject = "Math"                | Lesson Detail Drawer opens; Subject = "Math" is visible                |                  |
| 3   | Click "Edit" in the Lesson Detail Drawer                 | Lesson enters edit mode in the drawer                                  |                  |
| 4   | Click on Subject field and select a different subject    | Subject field updated to new value                                     | Subject: Science |
| 5   | Click "Save"                                             | Lesson saved; Lesson Detail Drawer shows Subject = "Science"           |                  |
| 6   | Navigate to the BO Lesson Detail page of the same lesson | Lesson Detail page opens                                               |                  |
| 7   | Observe Subject field on the detail page                 | Subject = "Science" is shown (consistent with change made on calendar) |                  |

**Severity:** major
**Priority:** high

---

### Lesson Detail – BO – Edit Subject – Subject Updated on Detail Page

**Description:** AC 01.1 — Equivalence Partitioning — Edit an existing lesson's subject to a different Subject Master value via BO Lesson Detail page; confirm the new subject is saved.

**Preconditions:**

- Logged in to Backoffice
- A lesson exists with Subject = "Math"
- User has lesson edit permission

| #   | Action                                                 | Expected Result                                      | Test Data        |
| --- | ------------------------------------------------------ | ---------------------------------------------------- | ---------------- |
| 1   | Navigate to Lesson Management → open the lesson detail | Lesson Detail page loads; Subject = "Math" displayed |                  |
| 2   | Click "Edit"                                           | Lesson enters edit mode                              |                  |
| 3   | Click on Subject field and select a different subject  | Subject field updated to new value                   | Subject: English |
| 4   | Click "Save"                                           | Lesson saved; detail page shows Subject = "English"  |                  |

**Severity:** major
**Priority:** high

---

## Suite: Subject – Recurring Lesson Behavior

---

### Recurring Lesson – Create with Subject – All Lessons in Chain Display Subject

**Description:** AC 01.1 — Equivalence Partitioning — Create a recurring lesson with a subject selected; confirm all generated lessons in the chain store and display that subject correctly.

**Preconditions:**

- Logged in as HQ or CM user on SF
- Subject Master has at least one active record (e.g., Math)
- User has created master data (Location, AY, Course, Class)

| #   | Action                                                                      | Expected Result                                              | Test Data                    |
| --- | --------------------------------------------------------------------------- | ------------------------------------------------------------ | ---------------------------- |
| 1   | Go to Manabie Lesson → Lesson tab → click "New"                             | Create lesson form opens                                     |                              |
| 2   | Fill in required fields; set Recurrence = Weekly, End After = 5 occurrences | All required fields populated                                | Recurrence: Weekly, Count: 5 |
| 3   | Select Subject = "Math" from the lookup                                     | Subject field shows "Math"                                   | Subject: Math                |
| 4   | Click "Save"                                                                | Lesson Schedule created with 5 lessons; redirected to detail |                              |
| 5   | Open lesson 1 in SF Lesson Detail                                           | Subject = "Math" displayed                                   |                              |
| 6   | Open lessons 2 through 5 in SF Lesson Detail                                | Each lesson shows Subject = "Math"                           |                              |
| 7   | Open each lesson in BO Lesson Detail                                        | Subject = "Math" displayed on each lesson in BO              |                              |

**Severity:** critical
**Priority:** high

---

### Recurring Lesson – Edit Subject – "Only This Lesson" – Other Lessons Unchanged

**Description:** AC 01.1 — Equivalence Partitioning — Edit the subject of one lesson in a recurring chain using "Only this lesson" scope; confirm only the selected lesson is updated.

**Preconditions:**

- Logged in as HQ or CM user on SF
- A recurring Lesson Schedule with 5 lessons exists; all have Subject = "Math"

| #   | Action                                    | Expected Result                                      | Test Data        |
| --- | ----------------------------------------- | ---------------------------------------------------- | ---------------- |
| 1   | Open lesson 3 from the recurring chain    | Lesson Detail opens; Subject = "Math"                |                  |
| 2   | Click "Edit"                              | Edit modal/form opens with recurrence scope selector |                  |
| 3   | Select "Only this lesson"                 | Scope confirmed; only lesson 3 will be edited        |                  |
| 4   | Change Subject to "English"               | Subject field shows "English"                        | Subject: English |
| 5   | Click "Save"                              | Lesson 3 saved; page returns to detail               |                  |
| 6   | Verify Subject on lesson 3                | Subject = "English"                                  |                  |
| 7   | Open lesson 2 and lesson 4 from the chain | Both show Subject = "Math" (unchanged)               |                  |

**Severity:** critical
**Priority:** high

---

### Recurring Lesson – Edit Subject – "This and Following" – Following Lessons Updated

**Description:** AC 01.1 — Equivalence Partitioning — Edit subject via "This and the following lessons" scope; confirm selected and all following lessons are updated while previous lessons are unchanged.

**Preconditions:**

- Logged in as HQ or CM user on SF
- A recurring Lesson Schedule with 5 lessons exists; all have Subject = "Math"

| #   | Action                                                 | Expected Result                                       | Test Data        |
| --- | ------------------------------------------------------ | ----------------------------------------------------- | ---------------- |
| 1   | Open lesson 3 from the recurring chain                 | Lesson Detail opens; Subject = "Math"                 |                  |
| 2   | Click "Edit" → select "This and the following lessons" | Edit applies to lesson 3 and lessons 4, 5             |                  |
| 3   | Change Subject to "English"                            | Subject field shows "English"                         | Subject: English |
| 4   | Click "Save"                                           | Lessons 3, 4, 5 saved with new subject                |                  |
| 5   | Open lessons 3, 4, 5                                   | Each shows Subject = "English"                        |                  |
| 6   | Open lessons 1 and 2                                   | Both show Subject = "Math" (prior lessons unaffected) |                  |

**Severity:** critical
**Priority:** high

---

### Recurring Lesson – Edit Subject – "This and Following" – Completed and Cancelled Lessons Skipped

**Description:** AC 01.1 — Regression Analysis — Confirm that "This and following" subject edit skips Completed and Cancelled lessons, consistent with edit scope rules for all lesson fields.

**Preconditions:**

- Logged in as HQ or CM user on SF
- A recurring chain of 5 lessons exists; all have Subject = "Math"
- Lesson 2 is set to Completed; lesson 4 is set to Cancelled

| #   | Action                                                 | Expected Result                                                | Test Data        |
| --- | ------------------------------------------------------ | -------------------------------------------------------------- | ---------------- |
| 1   | Open lesson 1 from the chain                           | Lesson Detail opens; Subject = "Math"                          |                  |
| 2   | Click "Edit" → select "This and the following lessons" | Edit modal confirms scope                                      |                  |
| 3   | Change Subject to "English" → click "Save"             | Save proceeds                                                  | Subject: English |
| 4   | Open lesson 1                                          | Subject = "English"                                            |                  |
| 5   | Open lesson 2 (Completed)                              | Subject = "Math" (not updated — Completed lessons are skipped) |                  |
| 6   | Open lesson 3                                          | Subject = "English"                                            |                  |
| 7   | Open lesson 4 (Cancelled)                              | Subject = "Math" (not updated — Cancelled lessons are skipped) |                  |
| 8   | Open lesson 5                                          | Subject = "English"                                            |                  |

**Severity:** major
**Priority:** high

---

### Lesson Schedule – Add Lesson Manually – Subject Field is Blank by Default

**Description:** AC 01.1 — Regression Analysis — When adding a lesson manually from the Lesson Schedule Detail, the Subject field is blank by default (not inherited from other lessons in the chain).

**Preconditions:**

- Logged in as HQ or CM user on SF
- A recurring Lesson Schedule with existing lessons that all have Subject = "Math"

| #   | Action                                                 | Expected Result                                                                | Test Data |
| --- | ------------------------------------------------------ | ------------------------------------------------------------------------------ | --------- |
| 1   | Open the Lesson Schedule Detail page                   | Lesson Schedule detail opens with list of lessons                              |           |
| 2   | Click "Add Lesson"                                     | Create lesson form opens; Location, AY, Course, Class pre-filled from schedule |           |
| 3   | Observe the Subject field                              | Subject field is **blank** (not pre-filled with "Math" from existing lessons)  |           |
| 4   | Fill in remaining required fields; leave Subject blank | Form valid with empty Subject                                                  |           |
| 5   | Click "Save"                                           | New lesson created and added to the schedule                                   |           |
| 6   | Open the newly added lesson detail                     | Subject field is empty; existing lessons in chain still show Subject = "Math"  |           |

**Severity:** major
**Priority:** high

---

### Lesson Schedule – Add Lesson Manually – Set Subject on Manually Added Lesson

**Description:** AC 01.1 — Equivalence Partitioning — When adding a lesson manually from the Lesson Schedule Detail, user can set a subject; the subject is saved correctly without affecting other lessons in the chain.

**Preconditions:**

- Logged in as HQ or CM user on SF
- A recurring Lesson Schedule with existing lessons that all have Subject = "Math"

| #   | Action                                                    | Expected Result                                                                                   | Test Data        |
| --- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | ---------------- |
| 1   | Open the Lesson Schedule Detail page → click "Add Lesson" | Create lesson form opens with blank Subject field                                                 |                  |
| 2   | Fill in required lesson fields                            | All required fields populated                                                                     |                  |
| 3   | Click Subject field and select "Science"                  | Subject field shows "Science"                                                                     | Subject: Science |
| 4   | Click "Save"                                              | New lesson created and added to the schedule                                                      |                  |
| 5   | Open the newly added lesson detail                        | Subject = "Science" displayed correctly                                                           |                  |
| 6   | Open the other lessons in the chain                       | Existing lessons still show Subject = "Math" (manually added lesson's subject does not propagate) |                  |

**Severity:** major
**Priority:** high

---

### Recurring Lesson – Extend Recurring – Newly Extended Lessons Have Blank Subject

**Description:** AC 01.1 — Regression Analysis — When extending a recurring lesson schedule, newly created lessons do not inherit the subject from the existing chain; subject is blank on all extended lessons.

**Preconditions:**

- Logged in as HQ or CM user on SF
- A recurring Lesson Schedule with 5 lessons; all have Subject = "Math"
- At least one of the 5 existing lessons is in Draft or Published status

| #   | Action                                                                 | Expected Result                                                              | Test Data |
| --- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------------- | --------- |
| 1   | Open the Lesson Schedule Detail page                                   | Schedule detail loads showing end date of existing chain                     |           |
| 2   | Click "Extend Recurrence" → set new end date (later than current last) | Extension form shows; new start date auto-filled = current end date + 7 days |           |
| 3   | Confirm the extension                                                  | New lessons (DRAFT) created beyond current end date                          |           |
| 4   | Open the first newly extended lesson detail                            | Subject field is **blank** (not inherited from existing lessons)             |           |
| 5   | Open additional newly extended lessons                                 | All extended lessons have blank Subject                                      |           |
| 6   | Open original lessons in the chain                                     | Original lessons still show Subject = "Math" (unchanged)                     |           |

**Severity:** major
**Priority:** high

---

### Recurring Lesson – Extend Recurring – Set Subject on Extended Lessons

**Description:** AC 01.1 — Equivalence Partitioning — After extending a recurring lesson schedule, user can set subject on the newly extended lessons using "This and following" edit; existing lessons are unaffected.

**Preconditions:**

- Logged in as HQ or CM user on SF
- A recurring Lesson Schedule with 5 existing lessons (Subject = "Math") has been extended to add 3 more lessons (Subject = blank)

| #   | Action                                                 | Expected Result                                                                | Test Data        |
| --- | ------------------------------------------------------ | ------------------------------------------------------------------------------ | ---------------- |
| 1   | Open the first newly extended lesson (lesson 6)        | Lesson Detail opens; Subject field is blank                                    |                  |
| 2   | Click "Edit" → select "This and the following lessons" | Edit applies to lessons 6, 7, 8                                                |                  |
| 3   | Select Subject = "Science"                             | Subject field shows "Science"                                                  | Subject: Science |
| 4   | Click "Save"                                           | Lessons 6, 7, 8 updated                                                        |                  |
| 5   | Open lessons 6, 7, 8                                   | All show Subject = "Science"                                                   |                  |
| 6   | Open original lessons 1–5                              | Still show Subject = "Math" (prior lessons not affected by edit from lesson 6) |                  |

**Severity:** major
**Priority:** high

---

### Recurring Lesson – Duplicate Lesson with Subject – Subject Pre-filled in Create Form

**Description:** AC 01.1 — Equivalence Partitioning — Duplicate a lesson that has a subject; confirm the Subject field is pre-filled from the source lesson in the create form.

**Preconditions:**

- Logged in as HQ or CM user on SF
- A lesson exists with Subject = "Math"

| #   | Action                                                    | Expected Result                                                     | Test Data     |
| --- | --------------------------------------------------------- | ------------------------------------------------------------------- | ------------- |
| 1   | Open the lesson detail for a lesson with Subject = "Math" | Lesson Detail page loads                                            |               |
| 2   | Click "Duplicate"                                         | Create lesson form opens pre-filled from the source lesson          |               |
| 3   | Observe the Subject field                                 | Subject = "Math" is pre-filled from the source lesson               | Subject: Math |
| 4   | Save without modifying Subject                            | New lesson created; Subject = "Math" on the duplicate lesson detail |               |
| 5   | Verify the original lesson is unchanged                   | Original lesson still shows Subject = "Math"                        |               |

**Severity:** normal
**Priority:** medium
