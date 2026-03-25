# Test Cases: LT-94698 — Subject Import, Search, Filter & Exclusions

## Suite: Subject – CSV Import

---

### Lesson Import – CSV with Valid Subject – Lessons Created with Correct Subject

**Description:** AC 02.1 — Equivalence Partitioning — Import lessons via CSV with a valid Subject Master value; confirm lessons are created with the correct subject mapped.

**Preconditions:**

- Logged in as HQ or CM user on SF
- Subject Master has active records (e.g., Math, English, Science)
- CSV file prepared with Subject column containing valid Subject Master names
- Master data is set up (Location, AY, Course, Class)

| #   | Action                                                              | Expected Result                                                      | Test Data              |
| --- | ------------------------------------------------------------------- | -------------------------------------------------------------------- | ---------------------- |
| 1   | Go to Manabie Lesson → Lesson tab → click "Import"                  | Import wizard opens                                                  |                        |
| 2   | Select Lesson Schedule and "Add new record"                         | Import configuration page displayed                                  |                        |
| 3   | Select AY, Account, Class, Location Course, Program Master          | Fields populated                                                     |                        |
| 4   | Upload CSV file with Subject column containing "Math" and "English" | CSV uploaded; preview displayed with Subject column                  | Subject: Math, English |
| 5   | Map columns including Subject → Subject field                       | Column mapping completed                                             |                        |
| 6   | Click "Next" and "Start Import"                                     | Import completes; lessons created                                    |                        |
| 7   | Open imported lessons on SF                                         | Each lesson shows the correct Subject from the CSV (Math or English) |                        |
| 8   | Open imported lessons on BO                                         | Each lesson shows the correct Subject on BO                          |                        |

**Severity:** critical
**Priority:** high

---

### Lesson Import – CSV with Empty Subject Column – Lessons Created Without Subject

**Description:** AC 02.1 / AC 01.2 — Equivalence Partitioning — Import lessons via CSV with Subject column left empty; confirm lessons are created without subject and no error.

**Preconditions:**

- Logged in as HQ or CM user on SF
- CSV file prepared with Subject column empty for all rows
- Master data is set up

| #   | Action                               | Expected Result                               | Test Data   |
| --- | ------------------------------------ | --------------------------------------------- | ----------- |
| 1   | Import CSV with empty Subject column | Import completes without error                | Subject: "" |
| 2   | Open imported lessons on SF          | Lesson detail shows Subject field empty       |             |
| 3   | Open imported lessons on BO          | Lesson detail shows Subject field empty on BO |             |

**Severity:** major
**Priority:** high

---

### Lesson Import – CSV with Invalid Subject Value – Import Error Returned

**Description:** AC 02.1 — Negative Testing — Import lessons via CSV with a Subject value that does not match any Subject Master record; confirm an error is returned.

**Preconditions:**

- Logged in as HQ or CM user on SF
- CSV file prepared with Subject column containing "InvalidSubjectXYZ" (not in Subject Master)
- Master data is set up

| #   | Action                                        | Expected Result                                                                | Test Data                  |
| --- | --------------------------------------------- | ------------------------------------------------------------------------------ | -------------------------- |
| 1   | Import CSV with Subject = "InvalidSubjectXYZ" | Import fails or shows error for rows with invalid subject                      | Subject: InvalidSubjectXYZ |
| 2   | Observe error message                         | Error indicates unrecognized Subject value; no lesson created for invalid rows |                            |

**Severity:** major
**Priority:** high

---

### Lesson Import – CSV with Mixed Valid and Empty Subject – All Lessons Created Correctly

**Description:** AC 02.1 — Equivalence Partitioning — Import CSV where some rows have a valid Subject and others have empty Subject; confirm all lessons created correctly.

**Preconditions:**

- Logged in as HQ or CM user on SF
- CSV prepared with rows: Row 1 Subject = "Math", Row 2 Subject = "", Row 3 Subject = "Science"
- Master data is set up

| #   | Action                               | Expected Result                         | Test Data                                 |
| --- | ------------------------------------ | --------------------------------------- | ----------------------------------------- |
| 1   | Import CSV with mixed Subject values | Import completes; all 3 lessons created | Row 1: Math, Row 2: empty, Row 3: Science |
| 2   | Open lesson from Row 1               | Subject = "Math"                        |                                           |
| 3   | Open lesson from Row 2               | Subject is empty                        |                                           |
| 4   | Open lesson from Row 3               | Subject = "Science"                     |                                           |

**Severity:** major
**Priority:** high

---

## Suite: Subject – Search

---

### Lesson List – SF – Search by Subject Name – Matching Lessons Returned

**Description:** AC 04.1 — Decision Table — Search for lessons by Subject name on SF Lesson list; confirm matching lessons are returned.

**Preconditions:**

- Logged in as HQ or CM user on SF
- At least one lesson exists with Subject = "Math"
- At least one lesson exists with Subject = "English"

| #   | Action                                             | Expected Result                                              | Test Data       |
| --- | -------------------------------------------------- | ------------------------------------------------------------ | --------------- |
| 1   | Navigate to Manabie Lesson → Lesson tab            | Lesson list displayed                                        |                 |
| 2   | Enter "Math" in the search/filter area for Subject | Lessons with Subject = "Math" are shown; others are excluded | Search: Math    |
| 3   | Clear search and enter "English"                   | Lessons with Subject = "English" are shown                   | Search: English |

**Severity:** normal
**Priority:** medium

---

### Lesson List – SF – Search by Non-Existing Subject – No Lessons Returned

**Description:** AC 04.1 — Negative Testing — Search for a subject name that does not exist on any lesson; confirm no results.

**Preconditions:**

- Logged in as HQ or CM user on SF
- No lessons exist with Subject = "NonExistentSubject"

| #   | Action                                       | Expected Result                                     | Test Data                  |
| --- | -------------------------------------------- | --------------------------------------------------- | -------------------------- |
| 1   | Navigate to Manabie Lesson → Lesson tab      | Lesson list displayed                               |                            |
| 2   | Enter "NonExistentSubject" in Subject search | No matching lessons shown; empty result or no match | Search: NonExistentSubject |

**Severity:** minor
**Priority:** low

---

### Lesson List – BO – Search by Subject Name – Matching Lessons Returned

**Description:** AC 04.2 — Decision Table — Search for lessons by Subject name on BO Lesson Management; confirm matching lessons are returned.

**Preconditions:**

- Logged in to Backoffice
- At least one lesson exists with Subject = "Math"

| #   | Action                                   | Expected Result                                              | Test Data    |
| --- | ---------------------------------------- | ------------------------------------------------------------ | ------------ |
| 1   | Navigate to Lesson Management on BO      | Lesson list displayed                                        |              |
| 2   | Enter "Math" in the Subject search field | Lessons with Subject = "Math" are shown; others are excluded | Search: Math |

**Severity:** normal
**Priority:** medium

---

## Suite: Subject – Filter

---

### Lesson Calendar – SF – Filter by Subject – Only Matching Lessons Shown

**Description:** AC 05.1 — Decision Table — Apply Subject filter on SF Calendar; confirm only lessons with the selected subject are displayed.

**Preconditions:**

- Logged in as HQ or CM user on SF
- Lessons exist with Subject = "Math" and Subject = "English" on visible calendar dates

| #   | Action                                 | Expected Result                                              | Test Data    |
| --- | -------------------------------------- | ------------------------------------------------------------ | ------------ |
| 1   | Navigate to SF Calendar view           | Calendar with lessons displayed                              |              |
| 2   | Apply Subject filter and select "Math" | Only lessons with Subject = "Math" are shown on the calendar | Filter: Math |
| 3   | Clear Subject filter                   | All lessons are displayed again regardless of subject        |              |

**Severity:** normal
**Priority:** medium

---

### Lesson Calendar – BO – Filter by Subject – Only Matching Lessons Shown

**Description:** AC 05.2 — Decision Table — Apply Subject filter on BO Calendar; confirm only lessons with the selected subject are displayed.

**Preconditions:**

- Logged in to Backoffice
- Lessons exist with Subject = "Math" and Subject = "English" on visible calendar dates

| #   | Action                                 | Expected Result                                              | Test Data    |
| --- | -------------------------------------- | ------------------------------------------------------------ | ------------ |
| 1   | Navigate to BO Calendar view           | Calendar with lessons displayed                              |              |
| 2   | Apply Subject filter and select "Math" | Only lessons with Subject = "Math" are shown on the calendar | Filter: Math |
| 3   | Clear Subject filter                   | All lessons are displayed again                              |              |

**Severity:** normal
**Priority:** medium

---

### Lesson List – BO – Subject Filter Applied – Only Matching Lessons Shown

**Description:** AC 05.3 — Decision Table — Apply Subject filter on BO Lesson Management list; confirm only lessons with the selected subject are shown.

**Preconditions:**

- Logged in to Backoffice
- Lessons exist with Subject = "Math" and Subject = "English"

| #   | Action                                   | Expected Result                              | Test Data    |
| --- | ---------------------------------------- | -------------------------------------------- | ------------ |
| 1   | Navigate to Lesson Management list on BO | Lesson list displayed                        |              |
| 2   | Apply Subject filter and select "Math"   | Only lessons with Subject = "Math" are shown | Filter: Math |
| 3   | Clear Subject filter                     | All lessons are displayed again              |              |

**Severity:** major
**Priority:** high

---

### Lesson List – BO – Subject Filter Combined with Other Filters – Cross-Field Validation

**Description:** AC 05.3 — Decision Table — Apply Subject filter combined with Location and Course filters; confirm cross-field validation applies correctly.

**Preconditions:**

- Logged in to Backoffice
- Lessons exist with:
  - Lesson A: Subject = "Math", Location = "Location A", Course = "Course X"
  - Lesson B: Subject = "Math", Location = "Location B", Course = "Course Y"
  - Lesson C: Subject = "English", Location = "Location A", Course = "Course X"

| #   | Action                                            | Expected Result                            | Test Data                                     |
| --- | ------------------------------------------------- | ------------------------------------------ | --------------------------------------------- |
| 1   | Apply Subject filter = "Math"                     | Lessons A and B are shown                  | Filter: Subject = Math                        |
| 2   | Additionally apply Location filter = "Location A" | Only Lesson A is shown (Math + Location A) | Filter: Subject = Math, Location = Location A |
| 3   | Clear all filters                                 | All lessons A, B, C are displayed          |                                               |

**Severity:** major
**Priority:** high

---

## Suite: Subject – Exclusions & Constraints

---

### Lesson Detail – Aver Custom Page – Subject Field Absent

**Description:** AC 06.1 — Permission Matrix / Negative Testing — Confirm Subject field does NOT appear on Aver custom lesson page.

**Preconditions:**

- Logged in with Aver tenant credentials
- A lesson exists on Aver custom page

| #   | Action                              | Expected Result                          | Test Data |
| --- | ----------------------------------- | ---------------------------------------- | --------- |
| 1   | Navigate to Aver custom lesson page | Lesson detail page displayed             |           |
| 2   | Observe all fields on lesson detail | Subject field is NOT present on the page |           |

**Severity:** major
**Priority:** high

---

### Lesson Detail – Teacher Assigned Regardless of Subject – No Subject-Teacher Validation

**Description:** AC 06.2 — Permission Matrix — Assign a teacher to a lesson with Subject = "Math" where the teacher has no eligible_subject for Math; confirm no validation error.

**Preconditions:**

- Logged in as HQ or CM user on SF
- A lesson exists with Subject = "Math"
- A teacher exists who does NOT have "Math" in eligible_subject

| #   | Action                                                            | Expected Result                                                | Test Data     |
| --- | ----------------------------------------------------------------- | -------------------------------------------------------------- | ------------- |
| 1   | Open lesson detail with Subject = "Math"                          | Lesson detail displayed                                        | Subject: Math |
| 2   | Click "Add Teacher" and select a teacher without Math eligibility | Teacher is added to the lesson without any validation error    |               |
| 3   | Observe lesson teachers section                                   | Teacher is listed on the lesson regardless of subject mismatch |               |

**Severity:** minor
**Priority:** low

---

### Lesson Detail – Different Subjects on Same-Course Lessons – No Course-Subject Constraint

**Description:** AC 06.3 — CRUD Testing — Create two lessons under the same course with different subjects; confirm no error or constraint.

**Preconditions:**

- Logged in as HQ or CM user on SF
- Course "Course X" exists
- Subject Master has "Math" and "English"

| #   | Action                                                        | Expected Result                                               | Test Data                          |
| --- | ------------------------------------------------------------- | ------------------------------------------------------------- | ---------------------------------- |
| 1   | Create a lesson under Course X with Subject = "Math"          | Lesson created with Subject = "Math"                          | Course: Course X, Subject: Math    |
| 2   | Create another lesson under Course X with Subject = "English" | Lesson created with Subject = "English"; no conflict or error | Course: Course X, Subject: English |
| 3   | Open both lessons                                             | Each lesson shows its own subject independently               |                                    |

**Severity:** minor
**Priority:** low
