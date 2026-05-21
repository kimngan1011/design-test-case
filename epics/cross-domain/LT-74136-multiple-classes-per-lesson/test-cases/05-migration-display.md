# Test Cases: LT-74136 — Multiple Classes per Lesson

## Suite: Migration and Display

---

### Multiple Classes – Migration – Deprecated Class Field – Not Visible on SF Lesson Schedule Layout

**Description:** AC 04.1 (BR-21/37) — Regression Analysis — Validates that after migration, the deprecated Class field that was on the Lesson Schedule object is no longer shown on any SF layout (Detail or Edit).

**Preconditions:**

- SF org post-migration (Lesson Schedule Class records migrated from old Class field on LS)
- At least one Lesson Schedule exists that had a class assigned before migration
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                                         | Expected Result                                                                                                                 | Test Data |
| --- | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | Navigate to any Lesson Schedule record in SF                                                   | Lesson Schedule Detail page is displayed                                                                                        | ""        |
| 2   | Scan the Lesson Schedule Detail layout for a standalone "Class" field (the old LS-level field) | No standalone "Class" field is present on the Lesson Schedule Detail layout — only the LSC related list shows class information | ""        |
| 3   | Click Edit on the Lesson Schedule                                                              | Lesson Schedule edit form opens                                                                                                 | ""        |
| 4   | Scan the edit form for a "Class" field                                                         | No "Class" input field is present on the Lesson Schedule edit form                                                              | ""        |
| 5   | Cancel the edit                                                                                | Lesson Schedule Detail page returns unchanged                                                                                   | ""        |

**Severity:** major
**Priority:** high

---

### Multiple Classes – Migration – Deprecated Class Field – Not Visible on BO Lesson Detail Layout

**Description:** AC 04.1 (BR-37) — Regression Analysis — Validates that the deprecated LS-level Class field is not displayed on the Back Office Lesson Detail or Lesson List pages after migration.

**Preconditions:**

- SF org and BO post-migration; Unleash flag `Lesson_BackOffice_LessonSF_MultipleClassesSF` is ON
- Logged in as HQ Staff or CM Staff to the Back Office

| #   | Action                                                                             | Expected Result                                                                                                         | Test Data |
| --- | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | --------- |
| 1   | Navigate to BO Lesson List                                                         | BO Lesson List page is displayed                                                                                        | ""        |
| 2   | Scan the column headers for a deprecated "Class (LS)" or raw LS-level class column | No deprecated LS-level class column appears in the list; only the formula-derived class value (from LSC) is shown       | ""        |
| 3   | Click on any lesson to open BO Lesson Detail                                       | BO Lesson Detail page opens                                                                                             | ""        |
| 4   | Scan the Lesson Detail fields for the deprecated LS-level Class field              | No deprecated LS-level Class field is shown; only the formula-derived Class value (sourced from LSC records) is visible | ""        |

**Severity:** major
**Priority:** high

---

### Multiple Classes – Formula Field – Single-Class Lesson – Single Class Name Displayed Without Extra Formatting (Backward Compatibility)

**Description:** AC 04.2 (BR-22) — Regression Analysis — Validates that the Class formula field on a single-class lesson (migrated) shows exactly the class name with no trailing comma, extra space, or unwanted separator.

**Preconditions:**

- SF org post-migration
- Lesson "Lesson MC-Legacy" was created before the multi-class feature and migrated; it has exactly 1 LSC record pointing to "Class Alpha"
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                              | Expected Result                                                                                      | Test Data |
| --- | --------------------------------------------------- | ---------------------------------------------------------------------------------------------------- | --------- |
| 1   | Navigate to SF Lesson Detail for "Lesson MC-Legacy" | Lesson Detail page is displayed                                                                      | ""        |
| 2   | Read the value of the "Class" formula field         | Class formula field shows "Class Alpha" only — no trailing comma, no parentheses, no empty separator | ""        |
| 3   | Navigate to BO Lesson Detail for "Lesson MC-Legacy" | BO Lesson Detail page is displayed                                                                   | ""        |
| 4   | Read the Class field value on BO                    | BO Class field shows "Class Alpha" — matches the SF display exactly                                  | ""        |

**Severity:** critical
**Priority:** high

---

### Multiple Classes – Formula Field – Two Classes Assigned – Comma-Separated Names Displayed on SF and BO

**Description:** AC 04.2 (BR-22/23) — Regression Analysis — Validates that when a lesson has two LSC records, the Class formula field displays both class names separated by a comma on both SF and BO.

**Preconditions:**

- SF org post-migration; `Multiple_Classes_In_Lesson__c` flag TRUE; BO Unleash flag ON
- Lesson "Lesson MC-Multi" has 2 LSC records: "Class Alpha" and "Class Beta"
- Logged in as HQ or CM Staff to SF and BO

| #   | Action                                                                     | Expected Result                                             | Test Data |
| --- | -------------------------------------------------------------------------- | ----------------------------------------------------------- | --------- |
| 1   | Navigate to SF Lesson Detail for "Lesson MC-Multi"                         | SF Lesson Detail page displayed                             | ""        |
| 2   | Read the "Class" formula field                                             | Class field shows "Class Alpha, Class Beta"                 | ""        |
| 3   | Navigate to BO Lesson Detail for "Lesson MC-Multi"                         | BO Lesson Detail page displayed                             | ""        |
| 4   | Read the Class field in BO                                                 | BO Class field shows "Class Alpha, Class Beta" — same as SF | ""        |
| 5   | Navigate to the SF Lesson Schedule Detail that generated "Lesson MC-Multi" | Lesson Schedule Detail page is displayed                    | ""        |
| 6   | Read the Class value visible on the Lesson in the related list             | Class column shows "Class Alpha, Class Beta"                | ""        |

**Severity:** critical
**Priority:** high

---

### Multiple Classes – Class Schedule Related List – SF Class Record – Tab Label and Columns Are Correct

**Description:** AC 04.3 (BR-24/25/26) — CRUD Testing — Validates that the Class Schedule related list on an SF Class record shows the correct tab label ("Class Schedule"), sources data from LSC records, and displays the required columns.

**Preconditions:**

- SF org post-migration
- A Class record "Class Alpha" has at least 2 LSC records linking it to different Lesson Schedules
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                     | Expected Result                                                                                             | Test Data           |
| --- | -------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ------------------- |
| 1   | Navigate to the "Class Alpha" record in SF                                 | Class record Detail page is displayed                                                                       | Class = Class Alpha |
| 2   | Find the related list tab for lesson schedules/classes on the Class record | A related list tab is visible                                                                               | ""                  |
| 3   | Read the tab label                                                         | Tab label reads "Class Schedule" (not an older label like "Lesson Schedules")                               | ""                  |
| 4   | Inspect the column headers in the related list                             | Columns shown: Lesson Name, Start Date, End Date, and a hyperlink column for Lesson Schedule                | ""                  |
| 5   | Verify that the entries in the list match the LSC records for Class Alpha  | The rows in the list correspond to lessons linked to Class Alpha via LSC (not the old LS-level Class field) | ""                  |
| 6   | Click the Lesson Schedule hyperlink in one row                             | Navigates to the correct Lesson Schedule record                                                             | ""                  |

**Severity:** minor
**Priority:** medium

---

### Multiple Classes – Class Schedule Related List – BO Class Record – Related List Updated from LSC Source

**Description:** AC 04.3 (BR-40) — CRUD Testing — Validates that the Class Schedule related list on the Back Office Class detail page is also updated to source data from LSC records and shows consistent information with SF.

**Preconditions:**

- BO Unleash flag `Lesson_BackOffice_LessonSF_MultipleClassesSF` is ON
- "Class Alpha" has at least 1 LSC record linking it to a lesson
- Logged in as HQ Staff or CM Staff to the Back Office

| #   | Action                                                                          | Expected Result                                                                                                       | Test Data           |
| --- | ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | ------------------- |
| 1   | Navigate to the Class detail page for "Class Alpha" in BO                       | BO Class detail page is displayed                                                                                     | Class = Class Alpha |
| 2   | Locate the Class Schedule related list or tab on the Class detail               | Class Schedule section is visible                                                                                     | ""                  |
| 3   | Read the tab label                                                              | Tab label reads "Class Schedule"                                                                                      | ""                  |
| 4   | Read the entries in the related list                                            | List shows lessons where "Class Alpha" is linked via LSC — same lessons that appear in SF Class Schedule related list | ""                  |
| 5   | Add a new LSC record for "Class Alpha" on a new lesson via SF and wait for sync | After sync, the new lesson appears in the BO Class Schedule related list for Class Alpha                              | ""                  |

**Severity:** minor
**Priority:** medium

---

### Multiple Classes – LSC Cascade Delete – Lesson Schedule Deleted – LSC Records Removed and Class Formula Shows Empty

**Description:** BR-36 — CRUD Testing — Validates that when a Lesson Schedule is deleted, its child Lesson Schedule Class records are cascade-deleted, and the Class formula field on associated lessons becomes empty.

**Preconditions:**

- SF org has `Multiple_Classes_In_Lesson__c` flag set to TRUE
- Lesson Schedule "LS-Delete-01" exists with 2 LSC records (Class Alpha and Class Beta) and 1 associated Lesson
- The associated Lesson's Class formula currently shows "Class Alpha, Class Beta"
- Logged in as HQ or CM Staff to the Salesforce org

| #   | Action                                                                                          | Expected Result                                                                                            | Test Data         |
| --- | ----------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | ----------------- |
| 1   | Navigate to "LS-Delete-01" in SF and open the Lesson Schedule Detail                            | Lesson Schedule Detail is displayed; LSC related list shows 2 records                                      | LS = LS-Delete-01 |
| 2   | Note the record IDs of the 2 LSC records from the related list                                  | Both LSC record IDs recorded for later verification                                                        | ""                |
| 3   | Click Delete on "LS-Delete-01" and confirm the deletion                                         | "LS-Delete-01" is deleted; no longer appears in Lesson Schedule list                                       | ""                |
| 4   | Search SF for both noted LSC record IDs                                                         | Neither LSC record exists — both are cascade-deleted with the parent Lesson Schedule (no orphaned records) | ""                |
| 5   | If the Lesson record still exists, navigate to its Detail page and read the Class formula field | Class formula field is empty (no LSC records left to drive the formula)                                    | ""                |

**Severity:** major
**Priority:** high
