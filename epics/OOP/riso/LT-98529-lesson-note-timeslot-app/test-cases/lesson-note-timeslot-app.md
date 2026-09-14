# Test Cases: LT-98529 - [Riso] Core | Lesson Note and Timeslot (App)

## Suite: [Riso] Lesson Note & Timeslot (App)

### [Riso] Lesson Note & Timeslot App - SF Lesson Form - Lesson Note visible when setting ON

**Description:** US01.1 - Config/component - SF Lesson create/edit screen shows Lesson Note as optional long text when `Show_Lesson_Note__c` is enabled.

**Preconditions:**
- Logged in as SF user with Lesson create/edit permission.
- `Lesson_Custom_Settings__c.Show_Lesson_Note__c = true`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson create or edit form. | Lesson form opens. | surface = SF |
| 2 | Inspect the general/basic information section. | Field `Lesson Note` is visible as a multi-line text area. | field = `Lesson_Note__c` |
| 3 | Leave the field blank and inspect required validation. | No required-marker validation is shown for Lesson Note. | optional = true |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Note & Timeslot App - SF Lesson Form - Lesson Note hidden when setting OFF

**Description:** US01.1 - Negative/config - SF must not expose Lesson Note when `Show_Lesson_Note__c` is disabled.

**Preconditions:**
- Logged in as SF user with Lesson create/edit permission.
- `Lesson_Custom_Settings__c.Show_Lesson_Note__c = false`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson create or edit form. | Lesson form opens. | surface = SF |
| 2 | Inspect the form for Lesson Note. | `Lesson Note` field is not displayed. | config = OFF |
| 3 | Save a lesson without Lesson Note. | Lesson saves through the existing flow; no Lesson Note validation blocks save. | note = blank |

**Severity:** major
**Priority:** medium

---

### [Riso] Lesson Note & Timeslot App - SF Save - 32768 character note is accepted

**Description:** US01.1 / US01.3 - Boundary value - `Lesson_Note__c` accepts the max Long Text Area length.

**Preconditions:**
- `Show_Lesson_Note__c = true`.
- SF user can edit Lesson A.
- Test data generator can create a 32,768-character plain text note.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Lesson A edit form in SF. | Edit form opens. | lesson = Lesson A |
| 2 | Enter a 32,768-character note into Lesson Note. | Field accepts the value. | length = 32768 |
| 3 | Save the lesson. | Save succeeds and record stores the full note. | field = `Lesson_Note__c` |
| 4 | Reopen the lesson detail. | Lesson Note value is still present and not truncated below 32,768 characters. | expected length = 32768 |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Note & Timeslot App - SF Save - 32769 character note is rejected or constrained

**Description:** US01.1 - Negative boundary - Values above the field max cannot be saved silently.

**Preconditions:**
- `Show_Lesson_Note__c = true`.
- SF user can edit Lesson A.
- Test data generator can create a 32,769-character plain text note.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Lesson A edit form in SF. | Edit form opens. | lesson = Lesson A |
| 2 | Enter a 32,769-character note. | UI prevents entry beyond max length or allows edit until save validation. | length = 32769 |
| 3 | Save the lesson. | Save is blocked with validation, or value is explicitly constrained to 32,768 characters; no silent corrupted value is stored. | max = 32768 |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Note & Timeslot App - BO Lesson Form - Lesson Note visible when feature setting ON

**Description:** US01.1 - BO component/config - BO Lesson form shows Lesson Note when `lesson.lesson_note.is_enabled` is enabled.

**Preconditions:**
- Logged in to BO as HQ/CM user with Lesson create/edit permission.
- `lesson.lesson_note.is_enabled = true`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open BO Lesson create or edit form. | Lesson form opens. | surface = BO |
| 2 | Inspect Lesson form fields. | `Lesson Note` field is visible as multiline text area. | i18n EN = Lesson Note |
| 3 | Leave Lesson Note blank and save a valid lesson. | Save succeeds; field is optional. | note = blank |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Note & Timeslot App - BO Save - Created or edited note is stored on Lesson

**Description:** US01.3 - Integration - BO sends `lessonNote` and stores it on the Lesson record.

**Preconditions:**
- Logged in to BO as HQ/CM user with Lesson edit permission.
- `lesson.lesson_note.is_enabled = true`.
- Lesson A exists and is assigned to Student A.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Lesson A in BO edit mode. | Edit form opens with Lesson Note field. | lesson = Lesson A |
| 2 | Enter `Bring workbook A` in Lesson Note. | Text is entered. | note = Bring workbook A |
| 3 | Save the lesson. | Save succeeds. | payload field = lessonNote |
| 4 | Reopen Lesson A in BO/SF detail or query the record. | `Lesson_Note__c` equals `Bring workbook A`. | expected record value |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Note & Timeslot App - Permissions - Read-only lesson user cannot edit Lesson Note

**Description:** US01.2 - Permission - Lesson Note follows existing Lesson object/field permissions.

**Preconditions:**
- User has permission to view Lesson Detail but not update Lesson.
- Lesson A has Lesson Note populated.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Log in as read-only/restricted lesson user. | User logs in successfully. | role = view-only |
| 2 | Open Lesson A detail. | Lesson detail is accessible according to existing Lesson permission. | lesson = Lesson A |
| 3 | Try to edit Lesson Note. | Edit action is unavailable or Lesson Note is read-only/disabled; user cannot save changes. | permission = no update |

**Severity:** major
**Priority:** medium

---

### [Riso] Lesson Note & Timeslot App - SF Calendar information shows Lesson Note

**Description:** US01.4 - Calendar display - Lesson Calendar information includes Lesson Note when the lesson has a note.

**Preconditions:**
- SF Calendar is accessible.
- `Show_Lesson_Note__c = true`.
- Lesson A exists on the selected date with Lesson Note `Bring workbook A`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open SF Lesson Calendar for Lesson A date/location. | Calendar loads and Lesson A is visible. | date/location = Lesson A |
| 2 | Open Lesson A calendar information/detail panel. | Lesson information panel opens. | card = Lesson A |
| 3 | Inspect Lesson Note area. | `Lesson Note` is displayed with value `Bring workbook A`. | expected note |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Note & Timeslot App - App Calendar Card shows note available tag

**Description:** US02.1 - App component - Calendar lesson card shows note-available tag when Lesson Note is entered.

**Preconditions:**
- Logged in to Learner App as Student A or Parent of Student A.
- Lesson A is assigned to Student A and has Lesson Note.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open App Calendar for Lesson A date. | Calendar opens. | student = Student A |
| 2 | Locate Lesson A card. | Lesson card is visible. | lesson = Lesson A |
| 3 | Inspect the bottom of the card. | Tag `Lesson Note Available` is shown in EN locale or `教室からのお知らせあり` in JP locale. | note exists |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Note & Timeslot App - App Calendar Card hides note tag for blank note

**Description:** US02.1 - Negative - Calendar lesson card hides note tag when Lesson Note is blank.

**Preconditions:**
- Logged in to Learner App as Student A or Parent of Student A.
- Lesson B is assigned to Student A and has blank Lesson Note.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open App Calendar for Lesson B date. | Calendar opens. | student = Student A |
| 2 | Locate Lesson B card. | Lesson card is visible. | lesson = Lesson B |
| 3 | Inspect the bottom of the card. | `Lesson Note Available` / `教室からのお知らせあり` tag is not shown. | note = blank |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Note & Timeslot App - App Lesson Detail shows note section at top

**Description:** US02.2 - App detail - Lesson Detail shows dedicated note section above/basic info when note exists.

**Preconditions:**
- Logged in to Learner App as Student A.
- Lesson A has Lesson Note `Bring workbook A`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open App Calendar and tap Lesson A. | Lesson Detail opens. | lesson = Lesson A |
| 2 | Inspect top of Lesson Detail. | Dedicated Lesson Note section is displayed near the top before normal lesson information. | placement = top |
| 3 | Inspect section header and content. | Header shows note icon + `Lesson Note` / `教室からのお知らせ`; content shows `Bring workbook A`. | expected note |
| 4 | Try to edit the note from App. | No edit control is available; note is read-only. | app = view only |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Note & Timeslot App - App Lesson Detail hides note section for blank note

**Description:** US02.2 - Negative - Blank Lesson Note does not leave an empty section on App Lesson Detail.

**Preconditions:**
- Logged in to Learner App as Student A.
- Lesson B is assigned to Student A and has blank Lesson Note.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Lesson B detail from App Calendar. | Lesson Detail opens. | lesson = Lesson B |
| 2 | Inspect the top area and Basic Info. | No Lesson Note section/header/icon/empty block is shown. | note = blank |
| 3 | Confirm existing Lesson Detail content. | Existing lesson information remains aligned and unchanged. | regression = layout |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Note & Timeslot App - App preserves plain text line breaks and escapes symbols

**Description:** US02.2 - Data format/security - App displays note as plain text with line breaks reflected.

**Preconditions:**
- Lesson A note is `Bring workbook A\nUse classroom entrance B <Room 301>`.
- Lesson A is assigned to Student A.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Lesson A detail in App. | Lesson Detail opens. | lesson = Lesson A |
| 2 | Inspect Lesson Note content. | Two lines are displayed in the same order. | line1/line2 |
| 3 | Inspect `<Room 301>` rendering. | Symbols are displayed as plain text; no HTML rendering or broken layout occurs. | plain text only |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Note & Timeslot App - Editing note is reflected in App immediately

**Description:** US01.3 / US02 - State transition - Saved note changes are visible in App without Lesson Report dependency.

**Preconditions:**
- Lesson A is assigned to Student A.
- Lesson A initial note is `Old announcement`.
- No published Lesson Report is required for this lesson.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Lesson A in SF or BO edit mode. | Edit form opens. | initial note = Old announcement |
| 2 | Change Lesson Note to `New announcement`. | Value is changed. | new note |
| 3 | Save the lesson. | Save succeeds. | source = SF/BO |
| 4 | Refresh App Calendar and Lesson Detail for Lesson A. | Card still shows note tag and detail shows `New announcement`, not the old note. | no Lesson Report required |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Note & Timeslot App - Clearing note removes App tag and detail section

**Description:** US01.3 / US02 - State transition - Clearing Lesson Note removes all App note UI.

**Preconditions:**
- Lesson A has Lesson Note and is visible in App for Student A.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Lesson A in SF or BO edit mode. | Edit form opens. | note exists |
| 2 | Clear Lesson Note and save. | Save succeeds and `Lesson_Note__c` is blank. | note = empty |
| 3 | Refresh App Calendar for Lesson A date. | Lesson A card no longer shows note-available tag. | card tag hidden |
| 4 | Open Lesson A detail. | Lesson Note section is hidden. | detail section hidden |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Note & Timeslot App - App Calendar Card displays timeslot in PRD format

**Description:** US03.1 - App component - Calendar card time includes Timeslot name after lesson time when enabled.

**Preconditions:**
- `Show_Timeslot_In_Lesson__c = true`.
- Lesson A is assigned to Student A.
- Lesson A time = 09:00-10:00 and Timeslot = `TimeSlot S`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open App Calendar for Lesson A date. | Calendar opens. | student = Student A |
| 2 | Locate Lesson A card. | Lesson card is visible. | lesson = Lesson A |
| 3 | Inspect the time line on the card. | Time displays `09:00 - 10:00 (TimeSlot S)`. | expected PRD format |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Note & Timeslot App - App Lesson Detail displays Timeslot under Time

**Description:** US03.2 - App detail - Lesson Detail Basic Info shows Timeslot label and value under Time.

**Preconditions:**
- `Show_Timeslot_In_Lesson__c = true`.
- Lesson A is assigned to Student A.
- Lesson A has Timeslot `TimeSlot S`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open Lesson A detail in App. | Lesson Detail opens. | lesson = Lesson A |
| 2 | Inspect Basic Info section under Time. | Row/field `Timeslot` / `時限` is displayed. | label |
| 3 | Inspect Timeslot value. | Value shows `TimeSlot S` without breaking the existing Time display. | expected timeslot |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Note & Timeslot App - Lesson without timeslot hides timeslot UI safely

**Description:** US03.1 / US03.2 - Negative - No-timeslot lesson does not show empty parentheses or empty row.

**Preconditions:**
- `Show_Timeslot_In_Lesson__c = true`.
- Lesson B is assigned to Student A.
- Lesson B has no Timeslot.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open App Calendar for Lesson B date. | Lesson card is visible. | lesson = Lesson B |
| 2 | Inspect Lesson B card time. | Time shows only start-end time; no empty `()` or `null` Timeslot text appears. | timeslot = blank |
| 3 | Open Lesson B detail. | Detail opens. |  |
| 4 | Inspect Basic Info. | Timeslot row is hidden or blank-safe per PRD; no empty label/value pair distorts layout. | no timeslot |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Note & Timeslot App - Timeslot hidden when partner config OFF

**Description:** US03.1 / US03.2 - Config - Timeslot display respects partner config.

**Preconditions:**
- `Show_Timeslot_In_Lesson__c = false`.
- Lesson A is assigned to Student A and has Timeslot `TimeSlot S`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open App Calendar for Lesson A date. | Lesson card is visible. | config = OFF |
| 2 | Inspect Lesson A card time. | Card does not display `(TimeSlot S)`; existing start-end time remains visible. | expected hidden |
| 3 | Open Lesson A detail. | Detail opens. |  |
| 4 | Inspect Basic Info. | Timeslot row/value is not displayed. | expected hidden |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Note & Timeslot App - Localization for Note and Timeslot labels

**Description:** US02.1 / US02.2 / US03.2 - i18n - App labels match EN/JP localization.

**Preconditions:**
- Lesson A has note and Timeslot.
- Student A can switch App locale between EN and JP.
- `Show_Timeslot_In_Lesson__c = true`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open App Calendar in English. | Note card tag shows `Lesson Note Available`. | locale = EN |
| 2 | Open Lesson A detail in English. | Note header shows `Lesson Note`; Basic Info label shows `Timeslot`. | locale = EN |
| 3 | Switch to Japanese and reopen Calendar/detail. | Tag shows `教室からのお知らせあり`; note header shows `教室からのお知らせ`; Timeslot label shows `時限`. | locale = JP |

**Severity:** major
**Priority:** medium

---

### [Riso] Lesson Note & Timeslot App - Student and parent only see assigned child's lesson note

**Description:** US02 / US03 - Access scope - Notes/timeslots respect existing App lesson visibility and selected child.

**Preconditions:**
- Parent account has Student A and Student B.
- Lesson A is assigned to Student A and has note/timeslot.
- Lesson D is assigned to Student B and has different note/timeslot.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Log in as parent and select Student A. | Student A context is active. | selected child = Student A |
| 2 | Open App Calendar for shared date. | Lesson A is visible with its note tag/timeslot; Lesson D is not shown in Student A context. | access scope |
| 3 | Switch to Student B. | Calendar refreshes to Student B context. | selected child = Student B |
| 4 | Inspect the same date. | Lesson D is visible with its own note/timeslot; Lesson A is not shown in Student B context. | no cross-child leak |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Note & Timeslot App - Existing Lesson History timeslot display is not regressed

**Description:** Regression - LT-98530 Lesson History still shows time + Timeslot name after LT-98529 App Calendar/detail changes.

**Preconditions:**
- LT-98530 Lesson History is enabled.
- Student A has a completed lesson with Timeslot `1限`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open App Lesson History for the completed lesson month. | Lesson History opens. | source = LT-98530 |
| 2 | Inspect the completed lesson row. | Row still shows Lesson Time plus Timeslot name on the expected line; no duplicate note tag or Calendar-only UI appears. | timeslot = 1限 |

**Severity:** major
**Priority:** medium

---

### [Riso] Lesson Note & Timeslot App - BO Lesson Form - Lesson Note hidden when feature setting OFF

**Description:** US01.1 - Negative/config - BO does not expose Lesson Note when `lesson.lesson_note.is_enabled` is disabled.

**Preconditions:**
- Logged in to BO as HQ/CM user with Lesson create/edit permission.
- `lesson.lesson_note.is_enabled = false`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open BO Lesson create or edit form. | Lesson form opens. | surface = BO |
| 2 | Inspect Lesson form fields. | `Lesson Note` field is not displayed. | config = OFF |
| 3 | Save a valid lesson without note. | Save succeeds through existing flow; no hidden Lesson Note validation blocks save. | note = blank |

**Severity:** major
**Priority:** medium

---

### [Riso] Lesson Note & Timeslot App - Whitespace-only note is treated as blank in App

**Description:** US02.1 / US02.2 - Negative blank handling - Whitespace-only note should not create an empty tag or note section.

**Preconditions:**
- Lesson C is assigned to Student A.
- Lesson C `Lesson_Note__c` contains only spaces/newlines.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open App Calendar for Lesson C date. | Lesson C card is visible. | note = whitespace-only |
| 2 | Inspect the bottom of the card. | Note-available tag is hidden. | expected blank behavior |
| 3 | Open Lesson C detail. | Lesson Detail opens. | lesson = Lesson C |
| 4 | Inspect the top note area. | Lesson Note section is hidden; no empty announcement block appears. | expected hidden |

**Severity:** major
**Priority:** medium
