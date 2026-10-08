# Test Cases: LT-98529 — [Riso] Core | Lesson Note and Timeslot (App)

> Normalized 2026-10-08 to current test-case rules (actor + verb steps, state preconditions, anchored dates, severity/priority mapping). Test intent unchanged.

## Suite: [Riso] Core | Lesson Note and Timeslot (App)

### [Riso] Lesson Note – SF Lesson Form – Show Lesson Note setting ON – Lesson Note shown as optional multi-line field

**Description:** US01.1 — Decision Table (config ON) — SF Lesson create/edit form shows Lesson Note as an optional multi-line text field.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce with Lesson create and edit permission
- Lesson Custom Setting "Show Lesson Note" is ON in Salesforce

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Salesforce Lesson create form | The Lesson form opens | surface = Salesforce; Show Lesson Note = ON |
| 2 | HQ or CM Staff looks at the Basic Information section | A "Lesson Note" multi-line text field is shown | field = Lesson Note |
| 3 | HQ or CM Staff fills all required lesson fields, leaves Lesson Note blank and clicks Save | The lesson is saved; no required-field error is shown for Lesson Note | Lesson Note = (blank) |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Note – SF Lesson Form – Show Lesson Note setting OFF – Lesson Note field hidden and save unaffected

**Description:** US01.1 — Decision Table (config OFF) + Negative — SF does not show Lesson Note when the setting is OFF; saving is not blocked.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce with Lesson create and edit permission
- Lesson Custom Setting "Show Lesson Note" is OFF in Salesforce

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Salesforce Lesson create form | The Lesson form opens | Show Lesson Note = OFF |
| 2 | HQ or CM Staff looks for the Lesson Note field | No "Lesson Note" field is shown | — |
| 3 | HQ or CM Staff fills all required lesson fields and clicks Save | The lesson is saved with no Lesson Note error | Lesson Note = (not shown) |

**Severity:** minor
**Priority:** medium

---

### [Riso] Lesson Note – SF Save – Note of 32,768 characters – Saved in full

**Description:** US01.1 / US01.3 — BVA (max) — Lesson Note accepts the maximum length of 32,768 characters.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce with Lesson create and edit permission
- Lesson Custom Setting "Show Lesson Note" is ON in Salesforce
- Lesson A exists and is editable by HQ or CM Staff
- A plain-text string of exactly 32,768 characters is prepared

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson A edit form in Salesforce | The edit form opens with the Lesson Note field | lesson = Lesson A |
| 2 | HQ or CM Staff pastes the 32,768-character text into Lesson Note | The field shows the pasted text | length = 32768 (max) |
| 3 | HQ or CM Staff clicks Save | The lesson is saved without error | — |
| 4 | HQ or CM Staff reopens Lesson A and copies the Lesson Note value | The Lesson Note value is exactly 32,768 characters and identical to the prepared text | expected length = 32768 |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Note – SF Save – Note of 32,769 characters – Save blocked with error, previous note kept

**Description:** US01.1 — BVA (max + 1) + Negative — A note one character over the limit cannot be saved; the stored value is unchanged.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce with Lesson create and edit permission
- Lesson Custom Setting "Show Lesson Note" is ON in Salesforce
- Lesson A has Lesson Note "Old announcement"
- A plain-text string of exactly 32,769 characters is prepared

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson A edit form in Salesforce | The edit form opens; Lesson Note shows "Old announcement" | lesson = Lesson A |
| 2 | HQ or CM Staff replaces Lesson Note with the 32,769-character text and clicks Save | Save is blocked and an error message is shown; the edit form stays open | length = 32769 (max + 1) |
| 3 | HQ or CM Staff cancels the edit and reopens Lesson A | Lesson Note still shows "Old announcement" | expected = Old announcement |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Note – BO Lesson Form – Feature setting ON – Lesson Note shown as optional multi-line field

**Description:** US01.1 — Decision Table (config ON) — Back Office Lesson form shows an optional Lesson Note field.

**Preconditions:**
- HQ or CM Staff is logged in to the Back Office with Lesson create and edit permission
- Back Office feature setting "Lesson Note" (lesson.lesson_note.is_enabled) is ON

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Back Office Lesson create form | The Lesson form opens | surface = Back Office; feature setting = ON |
| 2 | HQ or CM Staff looks at the form fields | A "Lesson Note" multi-line text field is shown | label EN = Lesson Note |
| 3 | HQ or CM Staff fills all required lesson fields, leaves Lesson Note blank and clicks Save | The lesson is saved; no required-field error is shown for Lesson Note | Lesson Note = (blank) |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Note – BO Lesson Form – Feature setting OFF – Lesson Note field hidden and save unaffected

**Description:** US01.1 — Decision Table (config OFF) + Negative — Back Office does not show Lesson Note when the feature setting is OFF.

**Preconditions:**
- HQ or CM Staff is logged in to the Back Office with Lesson create and edit permission
- Back Office feature setting "Lesson Note" (lesson.lesson_note.is_enabled) is OFF

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Back Office Lesson create form | The Lesson form opens | feature setting = OFF |
| 2 | HQ or CM Staff looks for the Lesson Note field | No "Lesson Note" field is shown | — |
| 3 | HQ or CM Staff fills all required lesson fields and clicks Save | The lesson is saved with no Lesson Note error | Lesson Note = (not shown) |

**Severity:** minor
**Priority:** medium

---

### [Riso] Lesson Note – BO Save – Note entered in Back Office – Stored on the Lesson and shown in Salesforce

**Description:** US01.3 — CRUD (update) — A note saved in the Back Office is stored on the Lesson record.

**Preconditions:**
- HQ or CM Staff is logged in to the Back Office with Lesson create and edit permission
- Back Office feature setting "Lesson Note" (lesson.lesson_note.is_enabled) is ON
- Lesson Custom Setting "Show Lesson Note" is ON in Salesforce
- Lesson A exists with a blank Lesson Note and is assigned to Student A

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson A in Back Office edit mode | The edit form opens with an empty Lesson Note field | lesson = Lesson A |
| 2 | HQ or CM Staff types "Bring workbook A" in Lesson Note and clicks Save | The lesson is saved | note = Bring workbook A |
| 3 | HQ or CM Staff opens Lesson A detail in Salesforce | Lesson Note shows "Bring workbook A" | expected = Bring workbook A |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Note – Permission – Staff with view-only Lesson access – Lesson Note cannot be edited

**Description:** US01.2 — Permission Matrix — Lesson Note follows the existing Lesson object permission.

**Preconditions:**
- Staff User R is logged in to Salesforce with permission to view Lessons but not to edit them
- Lesson Custom Setting "Show Lesson Note" is ON in Salesforce
- Lesson A has Lesson Note "Bring workbook A"

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Staff User R opens Lesson A detail in Salesforce | Lesson A detail opens; Lesson Note shows "Bring workbook A" | role = view-only |
| 2 | Staff User R looks for an Edit action or tries to change Lesson Note | No Edit action is available, or Lesson Note is read-only; the value cannot be changed | permission = no update |

**Severity:** minor
**Priority:** medium

---

### [Riso] Lesson Note – SF Lesson Calendar – Lesson with note – Lesson Note shown in lesson information

**Description:** US01.4 — Component — Salesforce Lesson Calendar lesson information shows the Lesson Note.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce with Lesson create and edit permission
- Lesson Custom Setting "Show Lesson Note" is ON in Salesforce
- Lesson A at Location A is dated 2026-10-21 and has Lesson Note "Bring workbook A"

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson Calendar for Location A on 2026-10-21 | Lesson A is shown on the calendar | lesson_date = 2026-10-21 |
| 2 | HQ or CM Staff clicks Lesson A to open its information panel | The lesson information panel opens | lesson = Lesson A |
| 3 | HQ or CM Staff looks at the Lesson Note area | "Lesson Note" shows "Bring workbook A" | expected = Bring workbook A |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Note – App Calendar Card – Lesson with note – Note-available tag shown

**Description:** US02.1 — Decision Table (note present) — The App Calendar lesson card shows the note-available tag for Student and Parent.

**Preconditions:**
- Lesson A is published, dated 2026-10-21 09:00 - 10:00 and assigned to Student A
- Lesson A has Lesson Note "Bring workbook A"
- Student A's App language is English

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A opens the App Calendar on 2026-10-21 | The Lesson A card is shown | lesson_date = 2026-10-21 |
| 2 | Student A looks at the bottom of the Lesson A card | The tag "Lesson Note Available" is shown | note = Bring workbook A |
| 3 | Parent of Student A logs in, selects Student A and opens the App Calendar on 2026-10-21 | The Lesson A card shows the tag "Lesson Note Available" | viewer = Parent |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Note – App Calendar Card – Lesson with blank note – Note-available tag hidden

**Description:** US02.1 — Decision Table (note blank) + Negative — The App Calendar lesson card has no note tag when the note is blank.

**Preconditions:**
- Student A is logged in to the Learner App
- Lesson B is published, dated 2026-10-21 10:30 - 11:30, assigned to Student A and has a blank Lesson Note

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A opens the App Calendar on 2026-10-21 | The Lesson B card is shown | lesson_date = 2026-10-21 |
| 2 | Student A looks at the bottom of the Lesson B card | No "Lesson Note Available" / "教室からのお知らせあり" tag is shown | note = (blank) |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Note – App Lesson Detail – Lesson with note – Read-only note section shown at the top

**Description:** US02.2 — Component — App Lesson Detail shows the note section at the top with icon, header and content; it is read-only.

**Preconditions:**
- Student A is logged in to the Learner App
- Lesson A is published, dated 2026-10-21 09:00 - 10:00 and assigned to Student A
- Lesson A has Lesson Note "Bring workbook A"
- Student A's App language is English

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A opens the App Calendar on 2026-10-21 and taps the Lesson A card | Lesson A detail opens | lesson_date = 2026-10-21 |
| 2 | Student A looks at the top of Lesson A detail | A Lesson Note section is shown above the basic lesson information | position = top |
| 3 | Student A looks at the section header and content | The header shows the note icon and "Lesson Note"; the content shows "Bring workbook A" | expected = Bring workbook A |
| 4 | Student A taps the note content | No edit control appears; the note cannot be changed | App = view only |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Note – App Lesson Detail – Lesson with blank note – Note section hidden, layout unchanged

**Description:** US02.2 — Decision Table (note blank) + Negative — No empty note block appears on App Lesson Detail.

**Preconditions:**
- Student A is logged in to the Learner App
- Lesson B is published, dated 2026-10-21 10:30 - 11:30, assigned to Student A and has a blank Lesson Note

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A opens Lesson B detail from the App Calendar on 2026-10-21 | Lesson B detail opens | lesson_date = 2026-10-21 |
| 2 | Student A looks at the top of Lesson B detail | No Lesson Note section, header, icon or empty block is shown | note = (blank) |
| 3 | Student A looks at the basic lesson information | Date, time and other lesson information are shown as before, with no blank gap | — |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Note – App Lesson Detail – Note with line breaks and symbols – Shown as plain text on separate lines

**Description:** US02.2 — EP (special content) — The note is shown as plain text; line breaks are kept and symbols are not treated as formatting.

**Preconditions:**
- Student A is logged in to the Learner App
- Lesson A is published, dated 2026-10-21 09:00 - 10:00 and assigned to Student A
- Lesson A has a two-line Lesson Note: line 1 "Bring workbook A", line 2 "Use classroom entrance B <Room 301>"

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A opens Lesson A detail from the App Calendar on 2026-10-21 | Lesson A detail opens | lesson_date = 2026-10-21 |
| 2 | Student A looks at the Lesson Note content | "Bring workbook A" and "Use classroom entrance B <Room 301>" are shown on two separate lines in this order | line 1 / line 2 |
| 3 | Student A looks at the text "<Room 301>" | "<Room 301>" is shown exactly as typed; no formatting is applied and the layout is not broken | plain text only |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Note – App – Note edited in Salesforce – New note shown in App after refresh

**Description:** US01.3 — State Transition (note changed) — A saved note change is shown in the App without any Lesson Report.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce with Lesson create and edit permission
- Lesson Custom Setting "Show Lesson Note" is ON in Salesforce
- Student A is logged in to the Learner App
- Lesson A is published, dated 2026-10-21 09:00 - 10:00 and assigned to Student A
- Lesson A has Lesson Note "Old announcement"
- Lesson A has no published Lesson Report

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson A edit form in Salesforce | Lesson Note shows "Old announcement" | initial = Old announcement |
| 2 | HQ or CM Staff changes Lesson Note to "New announcement" and clicks Save | The lesson is saved | new = New announcement |
| 3 | Student A pulls to refresh the App Calendar on 2026-10-21 | The Lesson A card still shows the note-available tag | lesson_date = 2026-10-21 |
| 4 | Student A opens Lesson A detail | The Lesson Note section shows "New announcement"; "Old announcement" is not shown | expected = New announcement |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Note – App – Note cleared in Salesforce – Tag and note section removed from App

**Description:** US01.3 — State Transition (note cleared) — Clearing the note removes all note UI in the App.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce with Lesson create and edit permission
- Lesson Custom Setting "Show Lesson Note" is ON in Salesforce
- Student A is logged in to the Learner App
- Lesson A is published, dated 2026-10-21 09:00 - 10:00 and assigned to Student A
- Lesson A has Lesson Note "Bring workbook A" and the App shows its note-available tag

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson A edit form in Salesforce, clears Lesson Note and clicks Save | The lesson is saved; Lesson Note is blank on Lesson A detail | note = (cleared) |
| 2 | Student A pulls to refresh the App Calendar on 2026-10-21 | The Lesson A card no longer shows the note-available tag | lesson_date = 2026-10-21 |
| 3 | Student A opens Lesson A detail | No Lesson Note section is shown | expected = hidden |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Note – App – Note containing only spaces and line breaks – Treated as blank, no tag and no section

**Description:** US02.1 / US02.2 — EP (whitespace-only) + Negative — A whitespace-only note behaves like a blank note in the App.

**Preconditions:**
- Student A is logged in to the Learner App
- Lesson C is published, dated 2026-10-21 13:00 - 14:00, assigned to Student A and its Lesson Note contains only spaces and line breaks

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A opens the App Calendar on 2026-10-21 | The Lesson C card is shown | lesson_date = 2026-10-21; note = spaces + line breaks only |
| 2 | Student A looks at the bottom of the Lesson C card | No note-available tag is shown | expected = hidden |
| 3 | Student A opens Lesson C detail | No Lesson Note section or empty block is shown | expected = hidden |

**Severity:** minor
**Priority:** medium

---

### [Riso] Timeslot – App Calendar Card – Timeslot display ON and lesson has Timeslot – Time shown as "Start - End (Timeslot)"

**Description:** US03.1 — Component — The App lesson card shows the Timeslot name after the lesson time.

**Preconditions:**
- Partner config "Show Timeslot In Lesson" is ON
- Student A is logged in to the Learner App
- Lesson A is published, dated 2026-10-21 09:00 - 10:00 and assigned to Student A
- Lesson A has Timeslot "TimeSlot S"

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A opens the App Calendar on 2026-10-21 | The Lesson A card is shown | lesson_date = 2026-10-21 |
| 2 | Student A looks at the time line on the Lesson A card | The time shows "09:00 - 10:00 (TimeSlot S)" | start = 09:00; end = 10:00; timeslot = TimeSlot S |

**Severity:** critical
**Priority:** high

---

### [Riso] Timeslot – App Lesson Detail – Timeslot display ON and lesson has Timeslot – Timeslot row shown under Time

**Description:** US03.2 — Component — App Lesson Detail basic information shows a Timeslot row under Time.

**Preconditions:**
- Partner config "Show Timeslot In Lesson" is ON
- Student A is logged in to the Learner App
- Lesson A is published, dated 2026-10-21 09:00 - 10:00 and assigned to Student A
- Lesson A has Timeslot "TimeSlot S"
- Student A's App language is English

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A opens Lesson A detail from the App Calendar on 2026-10-21 | Lesson A detail opens | lesson_date = 2026-10-21 |
| 2 | Student A looks at the basic information under Time | A "Timeslot" row is shown directly under the Time row | label EN = Timeslot |
| 3 | Student A looks at the Timeslot value | The value is "TimeSlot S"; the Time row still shows "09:00 - 10:00" | expected = TimeSlot S |

**Severity:** critical
**Priority:** high

---

### [Riso] Timeslot – App – Lesson without Timeslot – No empty brackets on card and no Timeslot row in detail

**Description:** US03.1 / US03.2 — Decision Table (no Timeslot) + Negative — A lesson without Timeslot shows no empty Timeslot text.

**Preconditions:**
- Partner config "Show Timeslot In Lesson" is ON
- Student A is logged in to the Learner App
- Lesson B is published, dated 2026-10-21 10:30 - 11:30, assigned to Student A and has no Timeslot

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A opens the App Calendar on 2026-10-21 | The Lesson B card is shown | lesson_date = 2026-10-21 |
| 2 | Student A looks at the time line on the Lesson B card | The time shows "10:30 - 11:30" only, with no "()" or "null" | timeslot = (none) |
| 3 | Student A opens Lesson B detail and looks under Time | No Timeslot row is shown and no empty label appears | expected = hidden |

**Severity:** major
**Priority:** high

---

### [Riso] Timeslot – App – Timeslot display OFF – Timeslot hidden on card and in detail

**Description:** US03.1 / US03.2 — Decision Table (config OFF) + Negative — Timeslot is not shown when the partner config is OFF.

**Preconditions:**
- Partner config "Show Timeslot In Lesson" is OFF
- Student A is logged in to the Learner App
- Lesson A is published, dated 2026-10-21 09:00 - 10:00 and assigned to Student A
- Lesson A has Timeslot "TimeSlot S"

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A opens the App Calendar on 2026-10-21 | The Lesson A card is shown | lesson_date = 2026-10-21; Show Timeslot In Lesson = OFF |
| 2 | Student A looks at the time line on the Lesson A card | The time shows "09:00 - 10:00" without "(TimeSlot S)" | expected = hidden |
| 3 | Student A opens Lesson A detail and looks under Time | No Timeslot row is shown | expected = hidden |

**Severity:** major
**Priority:** high

---

### [Riso] Lesson Note and Timeslot – App – Japanese language – Tag, note header and Timeslot label in Japanese

**Description:** US02.1 / US02.2 / US03.2 — Component (localization) — App labels match the English and Japanese texts.

**Preconditions:**
- Partner config "Show Timeslot In Lesson" is ON
- Student A is logged in to the Learner App
- Lesson A is published, dated 2026-10-21 09:00 - 10:00 and assigned to Student A
- Lesson A has Lesson Note "Bring workbook A" and Timeslot "TimeSlot S"

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A sets the App language to English and opens the App Calendar on 2026-10-21 | The Lesson A card shows the tag "Lesson Note Available" | lesson_date = 2026-10-21; language = English |
| 2 | Student A opens Lesson A detail | The note header shows "Lesson Note"; the basic information label shows "Timeslot" | language = English |
| 3 | Student A sets the App language to Japanese and reopens the App Calendar and Lesson A detail | The tag shows "教室からのお知らせあり"; the note header shows "教室からのお知らせ"; the Timeslot label shows "時限" | language = Japanese |

**Severity:** minor
**Priority:** medium

---

### [Riso] Lesson Note and Timeslot – App – Parent with two children – Each child sees only their own lesson note and Timeslot

**Description:** US02 / US03 — Permission Matrix (child scope) — Note and Timeslot follow the selected child; no data from the other child is shown.

**Preconditions:**
- Partner config "Show Timeslot In Lesson" is ON
- Parent P is linked to Student A and Student B
- Lesson A on 2026-10-21 is assigned to Student A with Lesson Note "Bring workbook A" and Timeslot "TimeSlot S"
- Lesson D on 2026-10-21 is assigned to Student B with Lesson Note "Bring gym clothes" and Timeslot "TimeSlot T"

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Parent P logs in to the Learner App and selects Student A | Student A's view is active | selected child = Student A |
| 2 | Parent P opens the App Calendar on 2026-10-21 | Lesson A is shown with the note-available tag and "(TimeSlot S)"; Lesson D is not shown | lesson_date = 2026-10-21 |
| 3 | Parent P switches to Student B | The calendar reloads for Student B | selected child = Student B |
| 4 | Parent P opens Lesson D detail on 2026-10-21 | Lesson D shows "Bring gym clothes" and Timeslot "TimeSlot T"; nothing from Lesson A is shown | no cross-child data |

**Severity:** critical
**Priority:** high

---

### [Riso] Timeslot – App Lesson History – Completed lesson with Timeslot – Time and Timeslot still shown (regression LT-98530)

**Description:** Regression (LT-98530) — Lesson History still shows the lesson time with the Timeslot name after the LT-98529 App changes.

**Preconditions:**
- Lesson History (LT-98530) is enabled for Student A
- Student A is logged in to the Learner App
- Student A has a completed lesson on 2026-10-14 09:00 - 10:00 with Timeslot "1限"

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A opens App Lesson History for October 2026 | Lesson History opens | month = 2026-10 |
| 2 | Student A looks at the row of the completed lesson on 2026-10-14 | The row shows the lesson time with the Timeslot name "1限" as before; no note tag or other Calendar-only element appears | timeslot = 1限 |

**Severity:** minor
**Priority:** medium

---

### [Riso] Lesson Note – SF Create Recurring Lesson – Note entered on create – Note copied to every occurrence

**Description:** Q4 (answered 2026-10-08) — CRUD (create, recurring) — A note entered when creating a recurring lesson is saved on every created occurrence.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce with Lesson create and edit permission
- Lesson Custom Setting "Show Lesson Note" is ON in Salesforce
- Student A is logged in to the Learner App
- Student A is affiliated with Location A

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Salesforce Lesson create form for Location A | The Lesson form opens with the Lesson Note field | start = 2026-10-21 09:00 - 10:00 |
| 2 | HQ or CM Staff fills all required fields, adds Student A, types "Bring workbook A" in Lesson Note, turns on "Recur this lesson" weekly with end date 2026-11-11 and clicks Save | The recurring lesson is saved; 4 lessons are created on 2026-10-21, 2026-10-28, 2026-11-04 and 2026-11-11 | note = Bring workbook A; occurrences = 4 |
| 3 | HQ or CM Staff opens each of the 4 created lessons in Salesforce | Each lesson shows Lesson Note "Bring workbook A" | expected = 4 / 4 lessons with the note |
| 4 | Student A opens the App Calendar on 2026-10-21 and on 2026-11-11 | The lesson card on both dates shows the note-available tag | first and last occurrence |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Note – SF Edit Recurring Lesson – "This and the following lessons" – Selected and following occurrences updated, earlier occurrence keeps old note

**Description:** Q4 (answered 2026-10-08) — CRUD (update, recurring scope) — Editing the note with "This and the following lessons" changes the selected and later occurrences only.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce with Lesson create and edit permission
- Lesson Custom Setting "Show Lesson Note" is ON in Salesforce
- Student A is logged in to the Learner App
- Recurring weekly lesson R at Location A runs every Wednesday 09:00 - 10:00 on 2026-10-21, 2026-10-28, 2026-11-04 and 2026-11-11, and is assigned to Student A
- All 4 occurrences of lesson R have Lesson Note "Old announcement"

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the 2026-10-28 occurrence of lesson R in Salesforce edit mode | The edit form opens; Lesson Note shows "Old announcement" | selected = 2026-10-28 |
| 2 | HQ or CM Staff changes Lesson Note to "New announcement", clicks Save and chooses "This and the following lessons" | The lessons are saved | save scope = This and the following lessons |
| 3 | HQ or CM Staff opens the occurrences on 2026-10-28, 2026-11-04 and 2026-11-11 | Each of the 3 lessons shows Lesson Note "New announcement" | expected = updated (3 lessons) |
| 4 | HQ or CM Staff opens the occurrence on 2026-10-21 | Lesson Note still shows "Old announcement" | expected = unchanged (earlier occurrence) |
| 5 | Student A opens Lesson R detail in the App for 2026-10-21 and for 2026-11-04 | 2026-10-21 shows "Old announcement"; 2026-11-04 shows "New announcement" | App check |

**Severity:** critical
**Priority:** high

---

### [Riso] Lesson Note – SF Edit Recurring Lesson – "Only this Lesson" – Only the selected occurrence updated

**Description:** Q4 (answered 2026-10-08) — CRUD (update, single scope) + Negative — Editing the note with "Only this Lesson" leaves every other occurrence unchanged.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce with Lesson create and edit permission
- Lesson Custom Setting "Show Lesson Note" is ON in Salesforce
- Recurring weekly lesson R at Location A runs every Wednesday 09:00 - 10:00 on 2026-10-21, 2026-10-28, 2026-11-04 and 2026-11-11, and is assigned to Student A
- All 4 occurrences of lesson R have Lesson Note "Old announcement"

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the 2026-11-04 occurrence of lesson R in Salesforce edit mode | The edit form opens; Lesson Note shows "Old announcement" | selected = 2026-11-04 |
| 2 | HQ or CM Staff changes Lesson Note to "Room changed to 301", clicks Save and chooses "Only this Lesson" | The lesson is saved | save scope = Only this Lesson |
| 3 | HQ or CM Staff opens the 2026-11-04 occurrence | Lesson Note shows "Room changed to 301" | expected = updated |
| 4 | HQ or CM Staff opens the occurrences on 2026-10-21, 2026-10-28 and 2026-11-11 | Each of the 3 lessons still shows Lesson Note "Old announcement" | expected = unchanged (3 lessons) |

**Severity:** major
**Priority:** high

---
