# Test Cases: LT-92536 - Daily Timetable Print Functionality

## Suite: LT-92536 - Daily Timetable Print Functionality

### [Core] Daily Timetable Print - Daily view shows Print Out action

**Description:** AC 01.1 - Print Out action is available from SF Lesson Calendar Daily view.

**Preconditions:**
- Logged in as HQ or CM Staff to Salesforce org.
- User has access to SF Lesson Calendar.
- Calendar location filter is Tokyo Center.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar. | Calendar loads successfully. | location = Tokyo Center |
| 2 | Switch to Daily view. | Daily arrangement table is displayed. | date = 2026-09-14 |
| 3 | Open the toolbar more-actions menu. | Print Out action is visible and enabled. | view = Daily |

**Priority:** high
**Severity:** major
**Tags:** LT-92536;Core;SF Calendar;Print Out

### [Core] Daily Timetable Print - Weekly and Monthly views do not allow Print Out

**Description:** AC 01.1 - Print Out is disabled or unavailable outside Daily view.

**Preconditions:**
- Logged in as HQ or CM Staff.
- SF Lesson Calendar is accessible.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar in Weekly view. | Weekly calendar loads. | view = Weekly |
| 2 | Open the toolbar more-actions menu. | Print Out action is not available or is disabled. |  |
| 3 | Switch to Monthly view and open the more-actions menu. | Print Out action remains unavailable or disabled. | view = Monthly |

**Priority:** high
**Severity:** major
**Tags:** LT-92536;Core;SF Calendar;Print Out

### [Core] Daily Timetable Print - Teacher and Classroom daily views allow Print Out

**Description:** AC 01.1 - Print Out is enabled in both Daily Teacher view and Daily Classroom view.

**Preconditions:**
- Logged in as HQ or CM Staff.
- SF Lesson Calendar Daily view is open.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Select Daily Teacher view. | Teacher daily arrangement table loads. | date = 2026-09-14 |
| 2 | Open the more-actions menu. | Print Out is enabled. |  |
| 3 | Switch to Daily Classroom view and open the more-actions menu. | Print Out is also enabled. |  |

**Priority:** medium
**Severity:** major
**Tags:** LT-92536;Core;SF Calendar;Print Out

### [Core] Daily Timetable Print - Dialog opens with Individual selected by default

**Description:** AC 01.2 - Print Out dialog keeps Individual as default teaching method.

**Preconditions:**
- SF Lesson Calendar Daily view is open.
- Print Out action is enabled.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Click Print Out from the more-actions menu. | Print Out dialog opens. |  |
| 2 | Inspect radio options. | Individual and Group options are shown. |  |
| 3 | Inspect selected radio option. | Individual is selected by default. | default = Individual |

**Priority:** high
**Severity:** major
**Tags:** LT-92536;Core;Dialog;Print Out

### [Core] Daily Timetable Print - Cancel dialog keeps calendar state unchanged

**Description:** AC 01.2 - Cancel returns to the same calendar context without opening a PDF.

**Preconditions:**
- SF Lesson Calendar Daily view is open for Tokyo Center.
- Print Out dialog is open.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Confirm the current date, view, and location filters. | Calendar context is known before cancel. | date = 2026-09-14; location = Tokyo Center |
| 2 | Click Cancel in the Print Out dialog. | Dialog closes. |  |
| 3 | Observe browser tabs and calendar filters. | No new PDF tab opens; date, view, and location filters remain unchanged. |  |

**Priority:** medium
**Severity:** minor
**Tags:** LT-92536;Core;Dialog;Regression

### [Core] Daily Timetable Print - Individual flag enabled opens new timetable PDF tab

**Description:** AC 01.3 - Individual print uses the new Individual timetable PDF when the feature flag is enabled.

**Preconditions:**
- `MANAERP__Enable_Individual_Daily_Timetable_Print__c = true`.
- SF Lesson Calendar Daily view is open for Tokyo Center.
- Print Out dialog is open with Individual selected.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Click Print in the dialog. | A new browser tab opens. | teachingMethod = Individual |
| 2 | Inspect the new tab URL. | URL points to `IndividualTimetablePrintPdf` with `locationId` and `lessonDate` parameters. | date = 2026-09-14 |
| 3 | Wait for the PDF to render. | PDF renders without error message. |  |

**Priority:** high
**Severity:** critical
**Tags:** LT-92536;Core;Individual PDF;Feature Flag

### [Core] Daily Timetable Print - Individual flag disabled falls back to legacy PDF

**Description:** AC 01.16 - Existing print flow remains when the new Individual timetable flag is disabled.

**Preconditions:**
- `MANAERP__Enable_Individual_Daily_Timetable_Print__c = false`.
- SF Lesson Calendar Daily view is open.
- Print Out dialog is open with Individual selected.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Click Print. | A PDF tab opens through the existing CalendarPrintOut flow. | teachingMethod = Individual |
| 2 | Inspect the PDF URL or network request. | Request does not use `IndividualTimetablePrintPdf`. | expected = legacy CalendarPrintOutPdf |
| 3 | Confirm Group/Individual legacy behavior still works. | Existing print behavior is unchanged. |  |

**Priority:** high
**Severity:** major
**Tags:** LT-92536;Core;Feature Flag;Regression

### [Core] Daily Timetable Print - Group selection remains legacy print flow

**Description:** AC 01.16 - Group print is not migrated to the new Individual timetable PDF.

**Preconditions:**
- `MANAERP__Enable_Individual_Daily_Timetable_Print__c = true`.
- Print Out dialog is open.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Select Group in the Print Out dialog. | Group radio is selected. | teachingMethod = Group |
| 2 | Click Print. | PDF opens through existing CalendarPrintOut flow. |  |
| 3 | Inspect new tab URL/network request. | `IndividualTimetablePrintPdf` is not used. |  |

**Priority:** medium
**Severity:** major
**Tags:** LT-92536;Core;Group;Regression

### [Core] Daily Timetable Print - PDF filename uses selected lesson date

**Description:** AC 01.4 - Individual PDF filename is `Schedule [yyyymmdd] - Individual.pdf`.

**Preconditions:**
- Individual timetable flag is enabled.
- Individual PDF tab is opened for selected date.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Print Out dialog from Daily view. | Dialog opens. | date = 2026-09-14 |
| 2 | Click Print with Individual selected. | New PDF tab opens. |  |
| 3 | Download or inspect PDF response filename. | File name is `Schedule 20260914 - Individual.pdf`. | expected filename |

**Priority:** high
**Severity:** major
**Tags:** LT-92536;Core;Individual PDF;Filename

### [Core] Daily Timetable Print - PDF header shows location, lesson date, printing date, page number

**Description:** AC 01.5 - PDF header contains required Japanese date and page metadata.

**Preconditions:**
- Individual timetable PDF is opened for Tokyo Center and 2026-09-14.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Inspect top banner of the PDF. | Location name is displayed in the header banner. | location = Tokyo Center |
| 2 | Inspect lesson date and printing date. | Lesson date uses `yyyy年MM月dd日（weekday）`; printing date uses `yyyy年MM月dd日`. | lesson date = 2026年09月14日（月） |
| 3 | Inspect page number text. | Page number is displayed and increments on later pages. | Page_Number label |

**Priority:** high
**Severity:** critical
**Tags:** LT-92536;Core;Individual PDF;Visual

### [Core] Daily Timetable Print - PDF uses A3 landscape and stamp rectangle

**Description:** AC 01.5 - PDF layout uses A3 landscape and has the stamping area.

**Preconditions:**
- Individual timetable PDF is open.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open browser print preview or inspect PDF page size. | Page size is A3 landscape. | expected = A3 landscape |
| 2 | Inspect bottom-right area of each page. | A rectangle for stamping is displayed. | stamp position = bottom right |
| 3 | Compare page margins and table placement. | Content is not clipped by the page edge or stamp rectangle. |  |

**Priority:** high
**Severity:** critical
**Tags:** LT-92536;Core;Individual PDF;Visual

### [Core] Daily Timetable Print - Published Individual lessons are included

**Description:** AC 01.6 - Published Individual lessons for the selected date/location are shown.

**Preconditions:**
- Published Individual Lesson A exists at Tokyo Center on 2026-09-14.
- Lesson A has classroom Booth A, student Student A, teacher Teacher A, course Course A, subject Math.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF for Tokyo Center on 2026-09-14. | PDF renders. |  |
| 2 | Locate the matching timeslot/time block and Booth A row. | Lesson data is displayed in Booth A row. |  |
| 3 | Verify columns. | Grade, Course, Subject, Student, and Teacher values match Lesson A data. |  |

**Priority:** high
**Severity:** critical
**Tags:** LT-92536;Core;Data Filter;Published

### [Core] Daily Timetable Print - Completed Individual lessons are excluded

**Description:** AC 01.6 - New Individual timetable PDF includes Published lessons only.

**Preconditions:**
- Completed Individual Lesson B exists at Tokyo Center on 2026-09-14.
- Published Individual Lesson A exists in the same location/date.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF for Tokyo Center on 2026-09-14. | PDF renders. |  |
| 2 | Search for Published Lesson A data. | Published Lesson A is displayed. |  |
| 3 | Search for Completed Lesson B data. | Completed Lesson B is not displayed. | status = Completed |

**Priority:** high
**Severity:** critical
**Tags:** LT-92536;Core;Data Filter;Published Only

### [Core] Daily Timetable Print - Draft and Cancelled Individual lessons are excluded

**Description:** AC 01.6 - Non-published Individual lesson statuses are excluded.

**Preconditions:**
- Draft Individual Lesson C and Cancelled Individual Lesson D exist at Tokyo Center on 2026-09-14.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF for Tokyo Center on 2026-09-14. | PDF renders. |  |
| 2 | Search for Draft Lesson C student/teacher data. | Draft lesson data is absent. | status = Draft |
| 3 | Search for Cancelled Lesson D student/teacher data. | Cancelled lesson data is absent. | status = Cancelled |

**Priority:** high
**Severity:** critical
**Tags:** LT-92536;Core;Data Filter;Published Only

### [Core] Daily Timetable Print - Group lessons are excluded from Individual PDF

**Description:** AC 01.6 - Individual PDF includes only Individual teaching method.

**Preconditions:**
- Published Group Lesson G exists at Tokyo Center on 2026-09-14.
- Published Individual Lesson A exists in the same date/location.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF. | PDF renders. | teachingMethod selected = Individual |
| 2 | Search for Individual Lesson A data. | Individual Lesson A is displayed. |  |
| 3 | Search for Group Lesson G class/course data. | Group Lesson G is not displayed. | teachingMethod = Group |

**Priority:** high
**Severity:** critical
**Tags:** LT-92536;Core;Data Filter;Teaching Method

### [Core] Daily Timetable Print - Other date and other location lessons are excluded

**Description:** AC 01.6 - PDF is scoped to selected calendar date and location.

**Preconditions:**
- Published Individual Lesson A exists at Tokyo Center on 2026-09-14.
- Published Individual Lesson E exists at Tokyo Center on 2026-09-15.
- Published Individual Lesson F exists at Osaka Center on 2026-09-14.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF for Tokyo Center on 2026-09-14. | PDF renders. |  |
| 2 | Search for Lesson A data. | Lesson A is displayed. | selected date/location |
| 3 | Search for Lesson E and Lesson F data. | Other-date and other-location lessons are not displayed. |  |

**Priority:** high
**Severity:** critical
**Tags:** LT-92536;Core;Data Filter;Location;Date

### [Core] Daily Timetable Print - Timeslot mode header uses active timeslot name and time

**Description:** AC 01.7 - Timeslot mode block header uses Timeslot Master values.

**Preconditions:**
- `MANAERP__Show_Timeslot_In_Lesson__c = true`.
- Active Timeslot 1 exists with Name = 1, Sequence = 1, Start Time = 09:00, End Time = 10:20.
- Published Individual Lesson A uses Timeslot 1.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF. | PDF renders in timeslot mode. |  |
| 2 | Inspect first block header. | Header shows `1限 09:00 - 10:20`. | Timeslot name + 限 |
| 3 | Verify Lesson A is under the Timeslot 1 block. | Lesson A data is displayed in the correct block. |  |

**Priority:** high
**Severity:** critical
**Tags:** LT-92536;Core;Timeslot;Individual PDF

### [Core] Daily Timetable Print - Timeslot blocks are ordered by sequence

**Description:** AC 01.7 - Timeslot blocks display in Timeslot Master sequence order, not created date or name.

**Preconditions:**
- Active Timeslots exist with sequences 1, 2, 3, 4.
- Each timeslot has at least one Published Individual lesson on selected date/location.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF. | PDF renders. | Timeslot mode = on |
| 2 | Read block headers left to right. | Blocks are ordered by sequence 1, 2, 3, 4. |  |
| 3 | Confirm lesson placement per timeslot. | Each lesson appears under its assigned timeslot block. |  |

**Priority:** high
**Severity:** major
**Tags:** LT-92536;Core;Timeslot;Sorting

### [Core] Daily Timetable Print - AM timeslot pages render before PM pages

**Description:** AC 01.9 - Timeslot pages are split by AM before PM.

**Preconditions:**
- AM active timeslots have start times before 12:00.
- PM active timeslots have start times at or after 12:00.
- Published Individual lessons exist in both AM and PM timeslots.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF. | PDF has multiple pages. |  |
| 2 | Inspect page 1 block headers. | AM timeslots are shown first. | start time < 12:00 |
| 3 | Inspect later page block headers. | PM timeslots appear after all AM pages. | start time >= 12:00 |

**Priority:** high
**Severity:** critical
**Tags:** LT-92536;Core;Timeslot;Pagination

### [Core] Daily Timetable Print - More than four AM timeslots creates next AM page

**Description:** AC 01.9 - Each page contains at most four blocks, and extra AM blocks continue before PM.

**Preconditions:**
- Five AM active timeslots have Published Individual lessons.
- At least one PM timeslot has a Published Individual lesson.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF. | PDF renders at least three pages. | 5 AM + 1 PM block |
| 2 | Inspect page 1. | First four AM blocks are shown. | blocks 1-4 |
| 3 | Inspect page 2 and page 3. | Fifth AM block is on page 2; PM block starts after AM pages. |  |

**Priority:** high
**Severity:** critical
**Tags:** LT-92536;Core;Timeslot;Pagination

### [Core] Daily Timetable Print - Less than four blocks pads blank headers

**Description:** AC 01.9 - A page still keeps four block areas when fewer than four blocks exist.

**Preconditions:**
- Two AM timeslots have Published Individual lessons.
- No other AM timeslot has matching lessons.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF. | AM page renders. |  |
| 2 | Inspect visible block headers. | First two blocks show timeslot headers. |  |
| 3 | Inspect remaining block areas. | Remaining block areas are present with blank headers and classroom rows. | padded blocks |

**Priority:** medium
**Severity:** major
**Tags:** LT-92536;Core;Timeslot;Layout

### [Core] Daily Timetable Print - Unused active timeslots still appear as empty blocks

**Description:** AC 01.4 - PRD expected behavior: timeslot template remains even when no lessons exist for a timeslot.

**Preconditions:**
- Active Timeslots 1, 2, 3, 4 exist.
- Only Timeslot 1 has a Published Individual lesson.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF. | PDF renders. | Timeslot mode = on |
| 2 | Inspect AM page headers. | All active AM timeslot blocks are displayed, including empty timeslots. | expected by PRD |
| 3 | Inspect empty timeslot classroom rows. | Classroom rows are present; lesson data cells are blank. |  |

**Priority:** high
**Severity:** critical
**Tags:** LT-92536;Core;Timeslot;PRD Gap

### [Core] Daily Timetable Print - Lesson without timeslot in timeslot mode is handled safely

**Description:** AC 01.7 - Timeslot mode should not break when a Published Individual lesson has blank Timeslot.

**Preconditions:**
- `MANAERP__Show_Timeslot_In_Lesson__c = true`.
- Published Individual Lesson NoSlot exists with no Timeslot.
- At least one active Timeslot lesson also exists.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF. | PDF renders without error. |  |
| 2 | Inspect timeslot blocks. | Timeslot-assigned lessons appear correctly. |  |
| 3 | Search for Lesson NoSlot data. | Behavior matches confirmed product rule: either excluded from timeslot PDF or shown in a defined no-timeslot/blank area; no broken PDF. | clarification needed |

**Priority:** medium
**Severity:** major
**Tags:** LT-92536;Core;Timeslot;Edge

### [Core] Daily Timetable Print - Manual mode groups by start and end time

**Description:** AC 01.8 - Manual mode groups lessons by distinct start/end pair.

**Preconditions:**
- `MANAERP__Show_Timeslot_In_Lesson__c = false`.
- Published Individual lessons exist with time ranges 09:00-10:00 and 09:00-10:30.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF. | PDF renders in manual mode. |  |
| 2 | Inspect block headers. | Blocks show `09:00 - 10:00` and `09:00 - 10:30`. | no timeslot name/limit suffix |
| 3 | Verify lessons are under matching time range blocks. | Each lesson appears in its corresponding start/end block. |  |

**Priority:** high
**Severity:** critical
**Tags:** LT-92536;Core;Manual Time;Grouping

### [Core] Daily Timetable Print - Manual mode sorts start time then end time

**Description:** AC 01.8 - Manual time blocks are sorted by start time ASC then end time ASC.

**Preconditions:**
- Manual time mode is enabled.
- Lessons exist with 09:00-10:30, 09:00-10:00, 09:30-11:00, and 09:30-11:30.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF. | PDF renders. |  |
| 2 | Read block headers left to right. | Order is 09:00-10:00, 09:00-10:30, 09:30-11:00, 09:30-11:30. |  |
| 3 | Verify no duplicate block is created for same start/end pair. | Lessons sharing same time range are grouped in one block. |  |

**Priority:** high
**Severity:** major
**Tags:** LT-92536;Core;Manual Time;Sorting

### [Core] Daily Timetable Print - Manual mode splits AM and PM pages

**Description:** AC 01.9 - Manual time grouping still renders AM pages before PM pages.

**Preconditions:**
- Manual time mode is enabled.
- Published Individual lessons exist at 10:00-11:00 and 13:00-14:00.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF. | PDF renders with AM and PM sections. |  |
| 2 | Inspect first page. | AM time block appears before PM block. | 10:00-11:00 |
| 3 | Inspect later page/section. | PM time block appears after AM. | 13:00-14:00 |

**Priority:** medium
**Severity:** major
**Tags:** LT-92536;Core;Manual Time;Pagination

### [Core] Daily Timetable Print - Manual mode more than four time ranges paginates

**Description:** AC 01.9 - Manual mode also limits one page to four blocks.

**Preconditions:**
- Manual time mode is enabled.
- Five distinct AM time ranges have Published Individual lessons.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF. | PDF renders multiple AM pages. | 5 distinct AM ranges |
| 2 | Inspect page 1. | First four time ranges are shown. |  |
| 3 | Inspect page 2. | Fifth time range continues on next AM page, with same header layout. |  |

**Priority:** medium
**Severity:** major
**Tags:** LT-92536;Core;Manual Time;Pagination

### [Core] Daily Timetable Print - All classrooms appear even without lessons

**Description:** AC 01.10 - Every block lists all classrooms under the selected location.

**Preconditions:**
- Tokyo Center has Booth A, Booth B, Booth C.
- Only Booth A has a Published Individual lesson in Timeslot 1.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF. | PDF renders. |  |
| 2 | Inspect Timeslot 1 block rows. | Booth A, Booth B, and Booth C are all displayed. | all classroom rows |
| 3 | Inspect Booth B and Booth C cells. | Lesson data cells are blank, not removed. |  |

**Priority:** high
**Severity:** critical
**Tags:** LT-92536;Core;Classroom;Layout

### [Core] Daily Timetable Print - Classroom rows sort by sequence then name

**Description:** AC 01.10 - Classroom row sorting follows Classroom Master sequence then name.

**Preconditions:**
- Classrooms exist: Booth B sequence 2, Booth A sequence 1, Booth C sequence blank.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF. | PDF renders. |  |
| 2 | Inspect classroom row order in any block. | Booth A appears before Booth B. | sequence 1 before 2 |
| 3 | Inspect classrooms with blank sequence. | Blank sequence classrooms appear after sequenced classrooms, sorted by name. | nulls last |

**Priority:** medium
**Severity:** major
**Tags:** LT-92536;Core;Classroom;Sorting

### [Core] Daily Timetable Print - Multiple classrooms on one lesson appear in each classroom row

**Description:** AC 01.10 - A lesson assigned to multiple classrooms is displayed under each associated classroom.

**Preconditions:**
- Published Individual Lesson MultiBooth is assigned to Booth A and Booth B.
- Same lesson has one student and one teacher.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF. | PDF renders. |  |
| 2 | Inspect Booth A row for the lesson block. | Lesson data is shown. |  |
| 3 | Inspect Booth B row for the same block. | Same lesson data is also shown. | multiple classrooms |

**Priority:** medium
**Severity:** major
**Tags:** LT-92536;Core;Classroom;Data

### [Core] Daily Timetable Print - Student, grade, course, subject, teacher columns are populated

**Description:** AC 01.11/01.12 - PDF columns display all required lesson data.

**Preconditions:**
- Published Individual Lesson A has Student A, Grade 5, Course Math Basic, Subject Algebra, Teacher A.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF. | PDF renders. |  |
| 2 | Locate Lesson A row. | Row is in correct classroom and timeslot/time block. |  |
| 3 | Verify displayed columns. | Grade, Course, Subject, Student, Teacher are populated with correct values. |  |

**Priority:** high
**Severity:** critical
**Tags:** LT-92536;Core;PDF Content

### [Core] Daily Timetable Print - Multiple students and teachers are comma-separated

**Description:** AC 01.12 - Multiple related values render together without overwriting each other.

**Preconditions:**
- Published Individual Lesson A has Student A, Student B, Teacher A, and Teacher B.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF. | PDF renders. |  |
| 2 | Inspect Student column for Lesson A. | Student A and Student B are both displayed. | separator = comma |
| 3 | Inspect Teacher column for Lesson A. | Teacher A and Teacher B are both displayed. | separator = comma |

**Priority:** medium
**Severity:** major
**Tags:** LT-92536;Core;PDF Content

### [Core] Daily Timetable Print - Seasonal student course displays star marker

**Description:** AC 01.13 - Seasonal enrollment is marked with star on course display.

**Preconditions:**
- Seasonal Student S has active Seasonal enrollment at Tokyo Center.
- Student S attends Published Individual Lesson A.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF for Tokyo Center. | PDF renders. |  |
| 2 | Locate Student S row. | Student S is displayed in the correct block. |  |
| 3 | Inspect Course column. | Course name has star marker `★`. | seasonal marker |

**Priority:** medium
**Severity:** major
**Tags:** LT-92536;Core;Seasonal;PDF Content

### [Core] Daily Timetable Print - Remarks show other timeslots for same student

**Description:** AC 01.14 - Remarks list other timeslot labels for students with multiple lessons in the day.

**Preconditions:**
- Student A has Published Individual lessons in Timeslot 1 and Timeslot 3 on the selected date/location.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF. | PDF renders. |  |
| 2 | Locate Student A in Timeslot 1 block. | Student A is displayed. | current timeslot = 1 |
| 3 | Inspect Remarks column. | Remarks show the other timeslot label, such as `3限`, and do not repeat current timeslot. | other timeslot = 3 |

**Priority:** high
**Severity:** major
**Tags:** LT-92536;Core;Remarks;Timeslot

### [Core] Daily Timetable Print - Empty date still generates classroom-only timetable

**Description:** AC 01.15 - No matching lessons should not produce a broken PDF.

**Preconditions:**
- Tokyo Center has Classroom Master data.
- No Published Individual lessons exist at Tokyo Center on 2026-09-20.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF for 2026-09-20. | PDF opens successfully. | no lesson date |
| 2 | Inspect PDF body. | Classroom rows are displayed. | all classrooms |
| 3 | Inspect lesson data cells. | Lesson cells are blank or follow confirmed empty-template behavior; no server error or blank browser page occurs. |  |

**Priority:** high
**Severity:** critical
**Tags:** LT-92536;Core;Empty State

### [Core] Daily Timetable Print - No classroom master data does not crash PDF

**Description:** AC 01.15 - Missing Classroom Master rows should be handled gracefully.

**Preconditions:**
- Selected location has no Classroom Master records.
- Published Individual lesson exists at the location/date.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF. | PDF opens without unhandled error. | no classrooms |
| 2 | Inspect PDF body. | PDF follows confirmed no-classroom behavior and does not show a broken table. |  |
| 3 | Verify header and stamp area. | Header metadata and stamp rectangle still render. |  |

**Priority:** medium
**Severity:** major
**Tags:** LT-92536;Core;Empty State;Classroom

### [Core] Daily Timetable Print - Missing locationId or lessonDate returns error message

**Description:** AC 01.17 - Direct PDF request with missing params shows controlled error.

**Preconditions:**
- User is logged in and has access to the Visualforce PDF page.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open `IndividualTimetablePrintPdf` without `locationId`. | Page renders controlled error. | missing locationId |
| 2 | Open `IndividualTimetablePrintPdf` without `lessonDate`. | Page renders controlled error. | missing lessonDate |
| 3 | Check logs/user output. | No unhandled exception page is shown to user. |  |

**Priority:** medium
**Severity:** major
**Tags:** LT-92536;Core;Error Handling

### [Core] Daily Timetable Print - Long JP and Latin text wraps inside fixed columns

**Description:** AC 01.11 - Fixed-width columns wrap long values without overlap.

**Preconditions:**
- Published Individual lesson has long course, subject, student, and teacher names with JP and Latin characters.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF. | PDF renders. | long text fixture |
| 2 | Inspect Course, Subject, Student, Teacher, and Remarks cells. | Text wraps within each cell. | no overflow |
| 3 | Inspect adjacent cells and page boundaries. | Text does not overlap neighboring columns or get clipped. |  |

**Priority:** high
**Severity:** critical
**Tags:** LT-92536;Core;Visual;Wrapping

### [Core] Daily Timetable Print - Table borders and header bar match production PDF style

**Description:** LT-103358 regression - PDF visual style remains stable across environments.

**Preconditions:**
- Individual timetable PDF is generated in preprod/staging.
- A production-style reference PDF or screenshot is available.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Compare header bar rendering. | Header bar is full-width and location title is visible. |  |
| 2 | Compare table border color and thickness. | Borders are light gray and not thick black. |  |
| 3 | Compare fonts, colors, and cell sizing. | Layout is consistent with expected production style. |  |

**Priority:** high
**Severity:** critical
**Tags:** LT-92536;Core;Visual Regression;PDF

### [Core] Daily Timetable Print - Multi-page row chunking repeats headers

**Description:** AC 01.9/01.11 - When classroom rows exceed page height, each physical page repeats the block headers.

**Preconditions:**
- Selected location has enough classrooms or long values to force row chunking across pages.
- Individual timetable PDF has at least two physical pages for the same four blocks.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Individual timetable PDF. | PDF renders multiple physical pages. | dense classroom fixture |
| 2 | Inspect page 1 and page 2. | Block headers and column headers repeat on each physical page. |  |
| 3 | Inspect row continuation. | Classroom rows continue without overlap, duplication, or missing rows. |  |

**Priority:** high
**Severity:** critical
**Tags:** LT-92536;Core;Pagination;Visual

### [Core] Daily Timetable Print - Dialog note does not contradict Published-only rule

**Description:** UI copy regression - Dialog message should align with new Individual PDF filtering rule.

**Preconditions:**
- Print Out dialog is open.
- Individual timetable feature flag is enabled.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Read helper text in the Print Out dialog. | Text does not claim Completed lessons will be printed for the new Individual timetable, or product confirms this copy is intentionally legacy. | expected = Published only |
| 2 | Generate Individual PDF with a Completed lesson fixture. | Completed lesson is excluded. |  |
| 3 | Compare UI copy with PDF behavior. | No user-facing contradiction remains; otherwise raise UI copy bug. |  |

**Priority:** medium
**Severity:** major
**Tags:** LT-92536;Core;Dialog;Copy

### [Core] Daily Timetable Print - Permissioned CM can open Individual PDF

**Description:** Access regression - Center-level edit user has access to controller/page.

**Preconditions:**
- Logged in as CM Staff with center-level edit permission.
- Individual timetable flag is enabled.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar Daily view. | Calendar loads for the CM user's accessible location. | user = CM |
| 2 | Print Individual timetable. | New PDF tab opens. |  |
| 3 | Inspect PDF content. | PDF contains only data from the user's accessible location and no permission error. |  |

**Priority:** medium
**Severity:** major
**Tags:** LT-92536;Core;Permission;CM

### [Core] Daily Timetable Print - Unauthorized or inaccessible location is blocked

**Description:** Access regression - User mode queries must not leak data for inaccessible locations.

**Preconditions:**
- Logged in as a user without access to Osaka Center.
- Osaka Center has Published Individual lessons.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Attempt to open Individual timetable URL for Osaka Center directly. | Access is blocked or PDF shows no inaccessible data. | locationId = inaccessible |
| 2 | Inspect PDF/error output. | No Osaka lesson/student/teacher data is visible. |  |
| 3 | Return to accessible location and print again. | Accessible location still prints normally. |  |

**Priority:** high
**Severity:** critical
**Tags:** LT-92536;Core;Permission;Security

### [Core] Daily Timetable Print - Calendar date selection is passed to PDF

**Description:** Integration - The selected Daily view date is passed as `lessonDate`.

**Preconditions:**
- Individual timetable flag is enabled.
- Calendar has Published Individual lessons on 2026-09-14 and 2026-09-15.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Navigate Daily view to 2026-09-15. | Calendar displays 2026-09-15. |  |
| 2 | Print Individual timetable. | New URL includes `lessonDate=2026-09-15`. |  |
| 3 | Inspect PDF data. | 2026-09-15 lessons appear; 2026-09-14 lessons do not. |  |

**Priority:** high
**Severity:** major
**Tags:** LT-92536;Core;Integration;Date

### [Core] Daily Timetable Print - Calendar location selection is passed to PDF

**Description:** Integration - The selected calendar location is passed as `locationId`.

**Preconditions:**
- Individual timetable flag is enabled.
- Tokyo Center and Osaka Center both have Published Individual lessons on the same date.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Select Osaka Center in the calendar location filter. | Calendar reloads for Osaka Center. |  |
| 2 | Print Individual timetable. | New URL includes Osaka Center locationId. |  |
| 3 | Inspect PDF. | Osaka lessons/classrooms appear; Tokyo lessons/classrooms do not. |  |

**Priority:** high
**Severity:** major
**Tags:** LT-92536;Core;Integration;Location

### [Core] Daily Timetable Print - Direct Apex URL respects feature flag

**Description:** AC 01.16/01.17 - Direct URL generation is blocked when feature flag is off.

**Preconditions:**
- `MANAERP__Enable_Individual_Daily_Timetable_Print__c = false`.
- User has access to calendar.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Trigger `getIndividualTimetableUrl` from the Individual print flow or API console. | Method rejects the request. | flag = false |
| 2 | Inspect error message. | Error indicates feature is not enabled. | Feature_Not_Enabled |
| 3 | Re-enable flag and retry. | URL is returned normally. | flag = true |

**Priority:** medium
**Severity:** major
**Tags:** LT-92536;Core;Feature Flag;API
