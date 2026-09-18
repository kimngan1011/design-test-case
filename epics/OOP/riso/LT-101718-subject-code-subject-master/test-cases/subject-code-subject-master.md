# Test Cases: LT-101718 / PBT-3075 - Add Subject Code in Subject Master

## Suite: Add Subject Code in Subject Master (LT-101718 / PBT-3075)

### [Riso] Subject Master - Create subject with Subject Code

**Description:** AC 01.1 / AC 01.2 - Verify Subject Code can be entered when creating a Subject Master record.

**Preconditions:**
- Logged in as HQ or CM Staff with Subject Master create/edit permission.
- Salesforce Master app is accessible.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Subject Master tab and click New. | New Subject Master form opens. | object = Subject_Master__c |
| 2 | Fill required fields and Subject Code. | Subject Code field is visible and editable. | Name = 国語; Subject Code = JP01 |
| 3 | Save the record. | Record is saved successfully. |  |
| 4 | Open the created record detail page. | Subject Code displays `JP01`. | expected = JP01 |

**Priority:** high
**Severity:** critical
**Tags:** LT-101718;PBT-3075;Subject Master;Subject Code;Create

### [Riso] Subject Master - Subject Code is optional

**Description:** AC 01.1 / AC 01.5 - Verify Subject Master can be created and used when Subject Code is blank.

**Preconditions:**
- Logged in as HQ or CM Staff with Subject Master create/edit permission.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Subject Master tab and click New. | New form opens. |  |
| 2 | Fill all required fields and leave Subject Code blank. | No client-side required marker or validation blocks blank Subject Code. | Subject Code = blank |
| 3 | Save the record. | Record is saved successfully. |  |
| 4 | Open detail/edit page for the record. | Subject Code remains blank and record can still be edited. |  |

**Priority:** high
**Severity:** major
**Tags:** LT-101718;PBT-3075;Subject Master;Optional;No Migration

### [Riso] Subject Master - Subject Code accepts maximum 30 characters

**Description:** AC 01.1 / BR-02 - Verify Text(30) boundary behavior for Subject Code.

**Preconditions:**
- Logged in as HQ or CM Staff with Subject Master create/edit permission.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open a Subject Master create or edit form. | Form is editable. |  |
| 2 | Enter a 30-character Subject Code. | Value is accepted in the field. | Subject Code = SUBCODE123456789012345678901 |
| 3 | Save the record. | Save succeeds and the 30-character value persists. | length = 30 |
| 4 | Edit the record and attempt to enter 31 characters. | Salesforce prevents or rejects the value according to Text(30) behavior; saved value never exceeds 30 characters. | length = 31 |

**Priority:** high
**Severity:** major
**Tags:** LT-101718;PBT-3075;Subject Master;Boundary

### [Riso] Subject Master - Edit and clear Subject Code

**Description:** AC 01.2 / AC 01.5 - Verify users can update and clear Subject Code after creation.

**Preconditions:**
- Subject Master record exists with Subject Code `JP01`.
- User has edit permission.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the Subject Master detail page. | Existing Subject Code is displayed. | current = JP01 |
| 2 | Click Edit and change Subject Code. | Field accepts the new value. | new value = JPN |
| 3 | Save and refresh the record. | Detail page displays `JPN`. | expected = JPN |
| 4 | Edit again, clear Subject Code, and save. | Save succeeds; Subject Code becomes blank. | new value = blank |

**Priority:** high
**Severity:** major
**Tags:** LT-101718;PBT-3075;Subject Master;Edit

### [Riso] Subject Master - New/detail layouts show Subject Code

**Description:** AC 01.3 - Verify Subject Code appears in the expected Subject Master form and record page layout.

**Preconditions:**
- Logged in as HQ or CM Staff.
- Subject Master record exists.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Subject Master New form. | Subject Code field is visible near Subject Name according to layout. | label = Subject Code / 科目コード |
| 2 | Open an existing Subject Master detail page. | Subject Code field is visible on record detail page. |  |
| 3 | Switch user language to Japanese if supported and reload. | Field label shows Japanese translation `科目コード`. | language = Japanese |

**Priority:** medium
**Severity:** major
**Tags:** LT-101718;PBT-3075;Subject Master;Layout;i18n

### [Riso] Subject Master - List views include Subject Code

**Description:** AC 01.4 - Verify Subject Code is visible in relevant Subject Master list views.

**Preconditions:**
- At least two Subject Master records exist, one active with Subject Code and one blank.
- User can access Subject Master list views.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open All Subjects list view. | Subject Code column is displayed. | list = All Subjects |
| 2 | Confirm record with Subject Code. | The configured Subject Code value is visible in the row. | expected = JP01 |
| 3 | Open Active Subjects list view. | Subject Code column is displayed for active records. | list = Active Subjects |
| 4 | Confirm blank Subject Code record behavior. | Blank values render as empty cells without layout issue. | expected = blank cell |

**Priority:** medium
**Severity:** major
**Tags:** LT-101718;PBT-3075;Subject Master;List View

### [Riso] Subject Master - Permission set allows Subject Code access

**Description:** AC 01.2 - Verify users with configured Subject Master permissions can read/edit Subject Code and read-only users cannot edit it.

**Preconditions:**
- One editable user and one read-only/view user are available.
- Subject Master record exists with Subject Code.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Log in as editable user and open Subject Master record. | Subject Code is readable and editable. | permission = edit |
| 2 | Update Subject Code and save. | Update succeeds. | new value = EDIT01 |
| 3 | Log in as view-only user and open the same record. | Subject Code is readable. | permission = view |
| 4 | Try to edit Subject Code. | Edit is unavailable or blocked by permission. | expected = no edit |

**Priority:** medium
**Severity:** major
**Tags:** LT-101718;PBT-3075;Subject Master;Permission

### [Riso] ATC - Selected student lesson with assigned teacher shows Subject Code and family name

**Description:** AC 02.1 / AC 02.2 - Verify Teacher Available Calendar selected student lesson chip uses Subject Code and teacher family name.

**Preconditions:**
- Available Teacher Calendar is accessible for a Riso location.
- Student `田中花子` has a published lesson in the selected month and location.
- Lesson subject has Subject Code `中国`.
- Lesson has assigned teacher with LastName `佐藤`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Available Teacher Calendar for the target location/month. | Calendar loads with timeslots. | location = Riso Test |
| 2 | Search and select student `田中花子`. | Student is selected and lesson overlay is displayed. | student = 田中花子 |
| 3 | Locate the student's lesson timeslot on the calendar. | Lesson chip is highlighted as teacher assigned. | status = assigned |
| 4 | Inspect the lesson chip text. | Chip shows Subject Code and teacher family name as `中国 (佐藤)`; it does not show full Subject Name in place of Subject Code. | expected = 中国 (佐藤) |

**Priority:** high
**Severity:** critical
**Tags:** LT-101718;PBT-3075;Available Teacher Calendar;Subject Code;Student Lesson

### [Riso] ATC - Selected student lesson without assigned teacher shows Subject Code only

**Description:** AC 02.1 / AC 02.3 - Verify unassigned lesson chip omits teacher name and still displays Subject Code.

**Preconditions:**
- Student has a published lesson in the selected month/location.
- Lesson subject has Subject Code `MATH`.
- Lesson has no Lesson Teacher assigned.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Available Teacher Calendar. | Calendar loads. |  |
| 2 | Search and select the student. | Student lesson overlay is displayed. |  |
| 3 | Locate the unassigned lesson chip. | Chip is highlighted as teacher unassigned. | status = unassigned |
| 4 | Inspect the lesson chip text. | Chip shows `MATH` only; no blank parentheses or teacher placeholder is displayed. | expected = MATH |

**Priority:** high
**Severity:** critical
**Tags:** LT-101718;PBT-3075;Available Teacher Calendar;Subject Code;Unassigned

### [Riso] ATC - Blank Subject Code does not break selected student lesson display

**Description:** AC 01.5 / AC 02.4 - Verify old/no-migration subject data with blank Subject Code does not break ATC.

**Preconditions:**
- Student has a published lesson whose Subject Master has blank Subject Code.
- Lesson is in the selected month/location.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Available Teacher Calendar and select the student. | Student lessons are loaded without error. | Subject Code = blank |
| 2 | Locate the lesson chip for the blank-code subject. | Calendar remains stable; no `undefined`, `null`, or broken placeholder is displayed. |  |
| 3 | Open the selected date/right panel if applicable. | Student lesson and available teacher sections still render normally. |  |

**Priority:** high
**Severity:** major
**Tags:** LT-101718;PBT-3075;Available Teacher Calendar;Blank Handling;No Migration

### [Riso] ATC - Subject Code display does not affect available teacher counts

**Description:** AC 02.4 / BR-07 - Verify Subject Code only changes student lesson display and does not change availability calculation.

**Preconditions:**
- Available Teacher Calendar has known available teacher counts for a date/timeslot.
- Student has lessons with Subject Code values in the same month.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Available Teacher Calendar without selected student and record teacher count for a date/timeslot. | Baseline count is visible. | count = N |
| 2 | Select a student whose lesson subject has Subject Code. | Student lesson overlay appears. |  |
| 3 | Re-check the same date/timeslot teacher count. | Available teacher count remains based on teacher availability/filter conditions, not Subject Code display. | expected = N unless normal filters changed |
| 4 | Apply/clear teacher filters. | Filtering behavior remains unchanged. | filters = subject/gender/name/tag |

**Priority:** high
**Severity:** major
**Tags:** LT-101718;PBT-3075;Available Teacher Calendar;Regression

### [Riso] ATC - Lesson creation from ATC remains unchanged with Subject Code

**Description:** AC 02.4 - Verify lesson creation prefill/override behavior still works when student lesson overlay includes Subject Code.

**Preconditions:**
- Available Teacher Calendar has at least one available teacher.
- Student with Subject Code lesson overlay is selected.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Select an available date/timeslot and teacher. | Create Lesson action is enabled. |  |
| 2 | Click Create Lesson. | Lesson creation modal opens. |  |
| 3 | Inspect prefilled fields. | Teacher, lesson date/time, location, and selected student/course behavior follow existing ATC spec. |  |
| 4 | Save or cancel according to test environment policy. | Existing ATC lesson creation flow is not broken by Subject Code display. |  |

**Priority:** high
**Severity:** major
**Tags:** LT-101718;PBT-3075;Available Teacher Calendar;Create Lesson;Regression

### [Riso] Regression - Course Master Course Code behavior is unchanged

**Description:** AC 03.1 - Verify adding Subject Code does not alter existing Course Code behavior.

**Preconditions:**
- Course Master record exists with Course Code.
- Subject Master records exist with Subject Code.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Course Master create/edit form. | Course Code field remains available with existing behavior. |  |
| 2 | Create or edit Course Code. | Course Code saves according to existing validation. |  |
| 3 | Open related lesson/calendar flow that uses Course Code. | Course Code display remains unchanged and is not replaced by Subject Code. |  |

**Priority:** medium
**Severity:** major
**Tags:** LT-101718;PBT-3075;Course Master;Course Code;Regression

### [Riso] Repo regression - Apex student lesson payload includes Subject Code

**Description:** Repo test recommendation - Verify `AvailableTeacherHandler.getStudentLessonsForMonth` returns `subjectCode` from `Lesson__r.Subject__r.Subject_Code__c`.

**Preconditions:**
- Apex test data creates Subject Master with Subject Code.
- Lesson references that Subject Master and has a Student Session in the requested month/location.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Execute `AvailableTeacherHandler.getStudentLessonsForMonth` with student, month, and location request. | Response contains the student's lesson. | method = getStudentLessonsForMonth |
| 2 | Inspect first `StudentLesson.subjectCode`. | `subjectCode` equals the configured Subject Master Subject Code. | expected = configured code |
| 3 | Repeat with a blank Subject Code subject. | `subjectCode` is null or blank according to implementation and no exception is thrown. | expected = blank-safe |

**Priority:** high
**Severity:** major
**Tags:** LT-101718;PBT-3075;Repo Test;Apex;Subject Code
