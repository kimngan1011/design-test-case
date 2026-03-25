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

### Lesson Detail – SF Calendar – Lesson Info Popup – Subject Displayed

**Description:** AC 03.2 — Regression Analysis — Confirm Subject appears in SF Calendar lesson info popup.

**Preconditions:**

- Logged in as HQ or CM user on SF
- A lesson exists with Subject = "Math" on a visible calendar date

| #   | Action                                    | Expected Result                            | Test Data     |
| --- | ----------------------------------------- | ------------------------------------------ | ------------- |
| 1   | Navigate to SF Calendar view              | Calendar view loads with lessons displayed |               |
| 2   | Click on the lesson with Subject = "Math" | Lesson info popup opens                    |               |
| 3   | Observe lesson info popup fields          | Subject = "Math" is displayed in the popup | Subject: Math |

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

### Lesson Detail – BO Calendar – Lesson Info Popup – Subject Displayed

**Description:** AC 03.4 — Regression Analysis — Confirm Subject appears in BO Calendar lesson info popup.

**Preconditions:**

- A lesson exists with Subject = "Math" on a visible calendar date
- Logged in to Backoffice

| #   | Action                                    | Expected Result                            | Test Data     |
| --- | ----------------------------------------- | ------------------------------------------ | ------------- |
| 1   | Navigate to BO Calendar view              | Calendar view loads with lessons displayed |               |
| 2   | Click on the lesson with Subject = "Math" | Lesson info popup opens                    |               |
| 3   | Observe lesson info popup fields          | Subject = "Math" is displayed in the popup | Subject: Math |

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
