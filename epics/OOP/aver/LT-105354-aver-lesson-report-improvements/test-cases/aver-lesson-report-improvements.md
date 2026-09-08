# Test Cases: LT-105354 - Aver Lesson Report Improvement Items

## Suite: [Aver] Lesson Report Improvements - PDF Rendering and Layout

### [Aver] Lesson Report PDF - Long textbook name - Japanese text wraps without duplicated characters

**Description:** AC 01.1 - Visual Regression - Long Japanese textbook names are rendered exactly once in the lesson report PDF.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce for the Aver tenant.
- Lesson LSN-105354-01 exists in Lesson Schedule LS-105354-A on 2026-06-10.
- Student A is assigned to LSN-105354-01.
- Lesson report for LSN-105354-01 is Draft.
- Next Week Homework has textbook `大学入試数学落とせない必須101題スタンダードレベル`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the lesson report for LSN-105354-01. | Lesson report detail opens with the Next Week Homework section. | lesson = LSN-105354-01; textbook = 大学入試数学落とせない必須101題スタンダードレベル |
| 2 | HQ or CM Staff generates the lesson report PDF. | PDF file is generated without error. | output = lesson_report_pdf |
| 3 | HQ or CM Staff opens the generated PDF and inspects the textbook name. | The textbook name displays as `大学入試数学落とせない必須101題スタンダードレベル` with no duplicated `1題` text. | forbidden_text = 大学入試数学落とせない必須101題1題スタンダードレベル |

**Severity:** major
**Priority:** high

---

### [Aver] Lesson Report PDF - Multiple long textbook rows - All rows remain readable

**Description:** AC 01.2 / AC 01.3 - Equivalence Partitioning - Multiple long textbook rows keep full text without truncation or repeated fragments.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce for the Aver tenant.
- Lesson LSN-105354-02 exists in Lesson Schedule LS-105354-A on 2026-06-17.
- Lesson report for LSN-105354-02 is Draft.
- Next Week Homework contains three rows with long Japanese textbook names.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the lesson report for LSN-105354-02. | All three homework rows are visible before PDF generation. | textbooks = three long Japanese values |
| 2 | HQ or CM Staff generates the lesson report PDF. | PDF file is generated without error. | output = lesson_report_pdf |
| 3 | HQ or CM Staff searches the PDF for each textbook name. | Each textbook appears once per homework row, and no row contains repeated partial text such as `とれるとれる` or `数学 い理系`. | textbook_1 = 改訂版最短10時間で9割とれる共通テスト古文のスゴ技; textbook_2 = 【改訂第3版】世界一わかりやすい九大の数学 理系数学＋文系数学の前期日程15か年 |

**Severity:** major
**Priority:** high

---

### [Aver] Lesson Report PDF - Next Week Homework - Remark displayed under textbook name

**Description:** AC 03.1 - Component - The Remark value is moved under the textbook name in the PDF next week homework section.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce for the Aver tenant.
- Lesson LSN-105354-03 exists with Next Week Homework.
- Next Week Homework row has textbook `数学テキストA` and Remark `Bring calculator and finish pages 10-12`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff generates the lesson report PDF for LSN-105354-03. | PDF file is generated. | lesson = LSN-105354-03 |
| 2 | HQ or CM Staff opens the PDF and locates the Next Week Homework row. | Textbook `数学テキストA` is displayed in the homework item. | textbook = 数学テキストA |
| 3 | HQ or CM Staff checks the placement of Remark. | Remark `Bring calculator and finish pages 10-12` is displayed under the textbook name, not as a separate right-side column value. | remark = Bring calculator and finish pages 10-12 |

**Severity:** minor
**Priority:** medium

---

### [Aver] Lesson Report PDF - Long textbook and long remark - Same homework item remains aligned

**Description:** AC 03.2 - Visual Regression - Long textbook and long remark values stay readable in the same homework item.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce for the Aver tenant.
- Lesson LSN-105354-04 exists with Next Week Homework.
- Next Week Homework has a long textbook name and a long Remark value.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff generates the lesson report PDF for LSN-105354-04. | PDF file is generated. | lesson = LSN-105354-04 |
| 2 | HQ or CM Staff opens the PDF and inspects the homework item. | The long textbook wraps within the homework item without overlapping the next item. | textbook = 【改訂第3版】世界一わかりやすい九大の数学 理系数学＋文系数学の前期日程15か年 |
| 3 | HQ or CM Staff checks the Remark under that textbook. | The long Remark wraps under the same textbook and remains fully readable. | remark = Review mistakes from mock exam, solve examples 1-8, and prepare questions for next lesson |

**Severity:** minor
**Priority:** medium

---

## Suite: [Aver] Lesson Report Improvements - BO Copy Forward

### [Aver] Breakthrough Test - Next Time - Next lesson Today's Result prefilled

**Description:** AC 02.1 - State Transition - Breakthrough Test `Next Time` from the previous lesson is copied to the next lesson `Today's Result`.

**Preconditions:**
- HQ or CM Staff is logged in to Back Office for the Aver tenant.
- Lesson Schedule LS-105354-A has LSN-105354-05 on 2026-06-10 and LSN-105354-06 on 2026-06-17.
- Student A is assigned to both lessons.
- Lesson report for LSN-105354-05 is editable.
- Lesson report for LSN-105354-06 has empty Breakthrough Test `Today's Result`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Edit Lesson Report for LSN-105354-05. | Edit Lesson Report form opens. | source_lesson = LSN-105354-05; target_lesson = LSN-105354-06 |
| 2 | HQ or CM Staff enters `BT next: Retry unit 3 speed drill` into Breakthrough Test `Next Time` and saves. | Lesson report for LSN-105354-05 is saved. | next_time = BT next: Retry unit 3 speed drill |
| 3 | HQ or CM Staff opens Edit Lesson Report for LSN-105354-06. | Breakthrough Test `Today's Result` is prefilled with `BT next: Retry unit 3 speed drill`. | today's_result_expected = BT next: Retry unit 3 speed drill |

**Severity:** major
**Priority:** high

---

### [Aver] Breakthrough Test - Same student different schedule - Today's Result ignores unrelated lesson

**Description:** AC 02.2 / AC 10.2 - Decision Table - Copy-forward uses same Lesson Schedule only and ignores another schedule for the same student.

**Preconditions:**
- HQ or CM Staff is logged in to Back Office for the Aver tenant.
- Student A is assigned to Lesson Schedule LS-105354-A and Lesson Schedule LS-105354-B.
- LS-105354-B has LSN-105354-07 on 2026-06-12 with Breakthrough Test `Next Time` value `Wrong schedule value`.
- LS-105354-A has LSN-105354-08 on 2026-06-17 with empty Breakthrough Test `Today's Result`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Edit Lesson Report for LSN-105354-08. | Edit Lesson Report form opens for LS-105354-A. | target_lesson = LSN-105354-08; target_schedule = LS-105354-A |
| 2 | HQ or CM Staff reviews Breakthrough Test `Today's Result`. | `Today's Result` is not prefilled with `Wrong schedule value`. | ignored_schedule = LS-105354-B |
| 3 | HQ or CM Staff saves the report without changing Breakthrough Test fields. | The report saves without pulling data from LS-105354-B. | forbidden_value = Wrong schedule value |

**Severity:** major
**Priority:** high

---

### [Aver] Breakthrough Test - Existing Today's Result - Value is not overwritten silently

**Description:** AC 02.3 - Negative - A teacher-entered `Today's Result` on the next lesson is preserved.

**Preconditions:**
- HQ or CM Staff is logged in to Back Office for the Aver tenant.
- Lesson Schedule LS-105354-A has LSN-105354-09 followed by LSN-105354-10.
- LSN-105354-09 Breakthrough Test `Next Time` is `New copied value`.
- LSN-105354-10 Breakthrough Test `Today's Result` already contains `Teacher entered value`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Edit Lesson Report for LSN-105354-10. | Edit Lesson Report form opens. | target_lesson = LSN-105354-10 |
| 2 | HQ or CM Staff reviews Breakthrough Test `Today's Result`. | `Today's Result` still shows `Teacher entered value`. | existing_value = Teacher entered value |
| 3 | HQ or CM Staff saves the report. | Saved report keeps `Teacher entered value` and does not silently replace it with `New copied value`. | copied_candidate = New copied value |

**Severity:** major
**Priority:** high

---

### [Aver] Next Week Homework - Same textbook added to next lesson - Remarks copied

**Description:** AC 04.1 - Decision Table - Same textbook homework added in the next lesson receives the previous lesson Remarks value.

**Preconditions:**
- HQ or CM Staff is logged in to Back Office for the Aver tenant.
- Lesson Schedule LS-105354-A has LSN-105354-11 followed by LSN-105354-12.
- LSN-105354-11 Next Week Homework has textbook `数学テキストA` and Remarks `Show full calculation steps`.
- LSN-105354-12 has no homework row for `数学テキストA`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Edit Lesson Report for LSN-105354-12. | Edit Lesson Report form opens. | target_lesson = LSN-105354-12 |
| 2 | HQ or CM Staff adds a Next Week Homework row with textbook `数学テキストA`. | New homework row is added. | textbook = 数学テキストA |
| 3 | HQ or CM Staff reviews the Remarks field on the new row. | Remarks is prefilled with `Show full calculation steps`. | expected_remarks = Show full calculation steps |

**Severity:** major
**Priority:** high

---

### [Aver] Next Week Homework - Edited remark - Following lesson receives latest value

**Description:** AC 04.2 / AC 04.3 - State Transition - The latest edited remark becomes the source for the following lesson.

**Preconditions:**
- HQ or CM Staff is logged in to Back Office for the Aver tenant.
- Lesson Schedule LS-105354-A has LSN-105354-13, LSN-105354-14, and LSN-105354-15 in date order.
- LSN-105354-13 homework `数学テキストA` has Remarks `Original remark`.
- LSN-105354-14 homework `数学テキストA` exists and is editable.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Edit Lesson Report for LSN-105354-14. | Edit Lesson Report form opens. | source_lesson = LSN-105354-14 |
| 2 | HQ or CM Staff changes Remarks for textbook `数学テキストA` to `Updated remark for lesson 14` and saves. | LSN-105354-14 homework remark is saved with the updated value. | updated_remarks = Updated remark for lesson 14 |
| 3 | HQ or CM Staff opens Edit Lesson Report for LSN-105354-15 and adds textbook `数学テキストA`. | The new homework row Remarks is prefilled with `Updated remark for lesson 14`. | target_lesson = LSN-105354-15 |

**Severity:** major
**Priority:** high

---

### [Aver] Next Week Homework - Different textbook - Remarks not copied

**Description:** AC 04.4 - Negative - Remarks are not copied when the new homework textbook differs from the previous lesson textbook.

**Preconditions:**
- HQ or CM Staff is logged in to Back Office for the Aver tenant.
- Lesson Schedule LS-105354-A has LSN-105354-16 followed by LSN-105354-17.
- LSN-105354-16 homework has textbook `数学テキストA` and Remarks `Do not copy to another book`.
- LSN-105354-17 has no homework row.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Edit Lesson Report for LSN-105354-17. | Edit Lesson Report form opens. | target_lesson = LSN-105354-17 |
| 2 | HQ or CM Staff adds a homework row with textbook `英語テキストB`. | New homework row is added. | new_textbook = 英語テキストB |
| 3 | HQ or CM Staff reviews the Remarks field. | Remarks remains blank and does not show `Do not copy to another book`. | previous_textbook = 数学テキストA |

**Severity:** minor
**Priority:** medium

---

### [Aver] Instructor's Comment 3 - Previous lesson value - Next lesson prefilled and editable

**Description:** AC 07.1 / AC 07.2 - State Transition - Instructor's Comment 3 is copied from the previous lesson and can be edited.

**Preconditions:**
- HQ or CM Staff is logged in to Back Office for the Aver tenant.
- Lesson Schedule LS-105354-A has LSN-105354-18 followed by LSN-105354-19.
- LSN-105354-18 Instructor's Comment 3 is `Keep same pacing next time`.
- LSN-105354-19 Instructor's Comment 3 is empty.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Edit Lesson Report for LSN-105354-19. | Edit Lesson Report form opens. | target_lesson = LSN-105354-19 |
| 2 | HQ or CM Staff reviews Instructor's Comment 3. | Instructor's Comment 3 is prefilled with `Keep same pacing next time`. | expected_comment = Keep same pacing next time |
| 3 | HQ or CM Staff changes Instructor's Comment 3 to `Increase homework volume` and saves. | The edited comment is saved on LSN-105354-19. | edited_comment = Increase homework volume |

**Severity:** minor
**Priority:** medium

---

### [Aver] Instructor's Comment 3 - Edited value - Following lesson uses latest same-schedule comment

**Description:** AC 07.3 / AC 10.3 - State Transition - The most recent edited Instructor's Comment 3 becomes the source for the following lesson.

**Preconditions:**
- HQ or CM Staff is logged in to Back Office for the Aver tenant.
- Lesson Schedule LS-105354-A has LSN-105354-20, LSN-105354-21, and LSN-105354-22.
- LSN-105354-20 Instructor's Comment 3 is `Original comment`.
- LSN-105354-21 Instructor's Comment 3 is `Edited comment`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Edit Lesson Report for LSN-105354-22. | Edit Lesson Report form opens. | target_lesson = LSN-105354-22 |
| 2 | HQ or CM Staff reviews Instructor's Comment 3. | Instructor's Comment 3 is prefilled with `Edited comment`, not `Original comment`. | latest_previous_lesson = LSN-105354-21 |
| 3 | HQ or CM Staff saves the report. | LSN-105354-22 keeps `Edited comment`. | expected_comment = Edited comment |

**Severity:** minor
**Priority:** medium

---

## Suite: [Aver] Lesson Report Improvements - Edit Restrictions and Date Format

### [Aver] Edit Lesson Report - Previous Week Homework - Add and edit controls hidden

**Description:** AC 06.1 - Negative - Previous Week Homework cannot be edited from BO Edit Lesson Report mode.

**Preconditions:**
- HQ or CM Staff is logged in to Back Office for the Aver tenant.
- Lesson LSN-105354-23 has Previous Week Homework rows displayed.
- Lesson report for LSN-105354-23 is editable.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Edit Lesson Report for LSN-105354-23. | Edit Lesson Report form opens. | lesson = LSN-105354-23 |
| 2 | HQ or CM Staff scrolls to Previous Week Homework. | Previous Week Homework rows are displayed. | section = Previous Week Homework |
| 3 | HQ or CM Staff checks available actions in the section. | Add, edit, delete, and inline editable controls are not shown for Previous Week Homework. | expected_controls = hidden |

**Severity:** major
**Priority:** high

---

### [Aver] Edit Lesson Report - Previous Week Homework field - Direct edit is blocked

**Description:** AC 06.2 - Negative - Previous Week Homework field values remain read-only in Edit Lesson Report mode.

**Preconditions:**
- HQ or CM Staff is logged in to Back Office for the Aver tenant.
- Lesson LSN-105354-24 has Previous Week Homework textbook `数学テキストA`.
- Lesson report for LSN-105354-24 is editable.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Edit Lesson Report for LSN-105354-24. | Edit Lesson Report form opens. | lesson = LSN-105354-24 |
| 2 | HQ or CM Staff attempts to focus or type into Previous Week Homework fields. | Previous Week Homework fields do not accept input. | attempted_value = illegal edit |
| 3 | HQ or CM Staff saves the report and reopens it. | Previous Week Homework values remain unchanged. | expected_textbook = 数学テキストA |

**Severity:** major
**Priority:** high

---

### [Aver] Add Homework Dialog - Normal date range - Year hidden in Japanese format

**Description:** AC 08.1 / AC 08.2 - Localization - Homework date range displays month and day only.

**Preconditions:**
- HQ or CM Staff is logged in to Back Office for the Aver tenant.
- Lesson LSN-105354-25 has add homework dialog available.
- The user's language is Japanese.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Add Homework for Next Week Homework. | Add Homework dialog opens. | lesson = LSN-105354-25; locale = ja |
| 2 | HQ or CM Staff selects homework daily range from 2026-06-10 to 2026-06-17. | Date range displays as `06月10日 - 06月17日`. | start_date = 2026-06-10; end_date = 2026-06-17 |
| 3 | HQ or CM Staff checks the displayed range text. | Year `2026` is not shown in the homework date range. | forbidden_text = 2026 |

**Severity:** minor
**Priority:** medium

---

### [Aver] Add Homework Dialog - Cross-year date range - Year still hidden

**Description:** AC 08.3 - Boundary Value Analysis - Cross-year homework range still omits year.

**Preconditions:**
- HQ or CM Staff is logged in to Back Office for the Aver tenant.
- Lesson LSN-105354-26 has add homework dialog available.
- The user's language is Japanese.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Add Homework for Previous Week Homework. | Add Homework dialog opens. | lesson = LSN-105354-26; locale = ja |
| 2 | HQ or CM Staff selects homework daily range from 2026-12-28 to 2027-01-04. | Date range displays as `12月28日 - 01月04日`. | start_date = 2026-12-28; end_date = 2027-01-04 |
| 3 | HQ or CM Staff checks the displayed range text. | Years `2026` and `2027` are not shown in the homework date range. | forbidden_text = 2026, 2027 |

**Severity:** minor
**Priority:** medium

---

## Suite: [Aver] Lesson Report Improvements - Student App PDF Monthly Count

### [Aver] Student App PDF - Second lesson in month - Title shows monthly count

**Description:** AC 05.1 / AC 05.2 - Boundary Value Analysis - Student App PDF title shows the lesson's monthly sequence.

**Preconditions:**
- Student A can log in to Learner App for the Aver tenant.
- Student A has published lesson reports on 2026-06-03, 2026-06-10, and 2026-06-24.
- The 2026-06-10 report is the second lesson report by lesson date in June.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Student A opens Learner App and opens the lesson report for 2026-06-10. | Published lesson report opens. | student = Student A; lesson_date = 2026-06-10 |
| 2 | Student A downloads or opens the student PDF report. | Student PDF report opens. | output = student_pdf |
| 3 | Student A checks the PDF title. | PDF title displays `指導簿 【生徒用・6月2回目】`. | June lessons = 2026-06-03, 2026-06-10, 2026-06-24 |

**Severity:** major
**Priority:** high

---

### [Aver] Student App PDF - First lesson of next month - Monthly count resets

**Description:** AC 05.3 - Boundary Value Analysis - Monthly count resets when the lesson month changes.

**Preconditions:**
- Student A can log in to Learner App for the Aver tenant.
- Student A has published lesson reports on 2026-06-24 and 2026-07-01.
- The 2026-07-01 report is the first lesson report by lesson date in July.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Student A opens Learner App and opens the lesson report for 2026-07-01. | Published lesson report opens. | student = Student A; lesson_date = 2026-07-01 |
| 2 | Student A opens the student PDF report. | Student PDF report opens. | output = student_pdf |
| 3 | Student A checks the PDF title. | PDF title displays `指導簿 【生徒用・7月1回目】`. | July lessons = 2026-07-01 |

**Severity:** major
**Priority:** high

---

### [Aver] Student App PDF - Same date multiple students - Monthly count calculated per student

**Description:** AC 05.2 - Data Integrity - Monthly count is calculated separately for each student.

**Preconditions:**
- Student A and Student B can log in to Learner App for the Aver tenant.
- Student A has lessons on 2026-06-03 and 2026-06-10.
- Student B has only one lesson on 2026-06-10.
- Both 2026-06-10 lesson reports are published.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Student A opens the student PDF report for 2026-06-10. | Student A PDF opens. | student = Student A |
| 2 | Student A checks the PDF title. | Title displays `指導簿 【生徒用・6月2回目】`. | Student A June count = 2 |
| 3 | Student B opens the student PDF report for 2026-06-10. | Student B PDF opens. | student = Student B |
| 4 | Student B checks the PDF title. | Title displays `指導簿 【生徒用・6月1回目】`. | Student B June count = 1 |

**Severity:** major
**Priority:** high

---

## Suite: [Aver] Lesson Report Improvements - Lesson List Next Lesson

### [Aver] Lesson List - Next Lesson column - Column visible and populated

**Description:** AC 09.1 / AC 09.3 - Component - Lesson List displays the same-schedule next lesson date.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce for the Aver tenant.
- Lesson Schedule LS-105354-A has LSN-105354-27 on 2026-06-10 and LSN-105354-28 on 2026-06-17.
- Lesson List view includes lessons from LS-105354-A.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Lesson List. | Lesson List is displayed. | list = Lesson List |
| 2 | HQ or CM Staff locates row LSN-105354-27. | Row LSN-105354-27 is visible. | lesson = LSN-105354-27 |
| 3 | HQ or CM Staff checks the `Next Lesson` column. | `Next Lesson` shows `2026-06-17` as a hyperlink. | expected_next_lesson = 2026-06-17; target = LSN-105354-28 |

**Severity:** major
**Priority:** high

---

### [Aver] Customizable Columns - Next Lesson - Column can be selected

**Description:** AC 09.2 - Component - Customizable Columns includes `Next Lesson`.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce for the Aver tenant.
- Lesson List page is open.
- Customizable Columns is available.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Customizable Columns from Lesson List. | Customizable Columns panel opens. | page = Lesson List |
| 2 | HQ or CM Staff searches for `Next Lesson`. | `Next Lesson` is available in the selectable column list. | column = Next Lesson |
| 3 | HQ or CM Staff enables `Next Lesson` and applies the column setting. | Lesson List displays the `Next Lesson` column. | action = enable_column |

**Severity:** minor
**Priority:** medium

---

### [Aver] Lesson List - Next Lesson hyperlink - Clicking opens next lesson

**Description:** AC 09.3 - Navigation - The hyperlinked Next Lesson date opens the target lesson.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce for the Aver tenant.
- Lesson Schedule LS-105354-A has LSN-105354-29 on 2026-06-10 and LSN-105354-30 on 2026-06-17.
- Lesson List displays `Next Lesson` for LSN-105354-29 as `2026-06-17`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Lesson List and locates LSN-105354-29. | Row LSN-105354-29 is visible. | source_lesson = LSN-105354-29 |
| 2 | HQ or CM Staff clicks the `2026-06-17` value in the `Next Lesson` column. | Lesson detail for LSN-105354-30 opens. | expected_target_lesson = LSN-105354-30 |
| 3 | HQ or CM Staff checks the opened lesson date. | Lesson date is 2026-06-17. | expected_date = 2026-06-17 |

**Severity:** major
**Priority:** high

---

### [Aver] Lesson List - Last lesson in schedule - Next Lesson has no clickable value

**Description:** AC 09.4 - Boundary Value Analysis - The last lesson in a Lesson Schedule does not show a clickable next lesson.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce for the Aver tenant.
- Lesson Schedule LS-105354-A has LSN-105354-31 as its last lesson on 2026-06-24.
- Lesson List displays row LSN-105354-31.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Lesson List and locates LSN-105354-31. | Row LSN-105354-31 is visible. | lesson = LSN-105354-31 |
| 2 | HQ or CM Staff checks the `Next Lesson` column. | `Next Lesson` is blank or has no clickable link. | position = last_lesson |
| 3 | HQ or CM Staff attempts to navigate from the empty Next Lesson value. | No next lesson detail is opened. | expected_target = none |

**Severity:** minor
**Priority:** medium

---

### [Aver] Lesson List - Same student different schedule - Next Lesson uses same Lesson Schedule

**Description:** AC 10.1 / AC 10.2 - Decision Table - Next Lesson column ignores a nearer lesson in another Lesson Schedule.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce for the Aver tenant.
- Student A has LSN-105354-32 in LS-105354-A on 2026-06-10.
- Student A has LSN-105354-33 in LS-105354-B on 2026-06-12.
- LS-105354-A has LSN-105354-34 on 2026-06-17.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Lesson List and locates LSN-105354-32. | Row LSN-105354-32 is visible. | source_lesson = LSN-105354-32 |
| 2 | HQ or CM Staff checks the `Next Lesson` column. | `Next Lesson` shows `2026-06-17`, not `2026-06-12`. | same_schedule_next = LSN-105354-34; other_schedule_lesson = LSN-105354-33 |
| 3 | HQ or CM Staff clicks the Next Lesson hyperlink. | Lesson detail for LSN-105354-34 opens. | expected_target = LSN-105354-34 |

**Severity:** major
**Priority:** high

---

## Suite: [Aver] Lesson Report Improvements - Same Schedule Regression

### [Aver] Previous and Next logic - Homework source - Same Lesson Schedule selected

**Description:** AC 10.1 / AC 10.3 - Regression - Homework previous/next logic uses same Lesson Schedule for copy-forward.

**Preconditions:**
- HQ or CM Staff is logged in to Back Office for the Aver tenant.
- Student A has lessons in LS-105354-A and LS-105354-B during the same week.
- LS-105354-A previous lesson homework Remarks is `Same schedule source`.
- LS-105354-B lesson homework Remarks is `Different schedule source`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the next lesson in LS-105354-A. | Edit Lesson Report form opens for LS-105354-A. | schedule = LS-105354-A |
| 2 | HQ or CM Staff adds homework using the same textbook from the previous LS-105354-A lesson. | Homework row is added. | textbook = 数学テキストA |
| 3 | HQ or CM Staff reviews copied Remarks. | Remarks is `Same schedule source` and not `Different schedule source`. | expected_remarks = Same schedule source |

**Severity:** major
**Priority:** high

---

### [Aver] Previous and Next logic - Lesson Report navigation - Same Lesson Schedule selected

**Description:** AC 10.1 / AC 10.2 - Regression - Previous/next lesson report references ignore other schedules for the same student.

**Preconditions:**
- HQ or CM Staff is logged in to Back Office for the Aver tenant.
- Student A has Lesson Report LR-A1 in LS-105354-A on 2026-06-10.
- Student A has Lesson Report LR-B1 in LS-105354-B on 2026-06-12.
- Student A has Lesson Report LR-A2 in LS-105354-A on 2026-06-17.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Lesson Report LR-A1. | LR-A1 opens. | source_report = LR-A1 |
| 2 | HQ or CM Staff opens the next report from the lesson report surface. | The next report target resolves within LS-105354-A. | same_schedule = LS-105354-A |
| 3 | HQ or CM Staff checks the opened report. | LR-A2 opens, and LR-B1 is not selected. | expected_report = LR-A2; ignored_report = LR-B1 |

**Severity:** major
**Priority:** high

---

### [Aver] Published Lesson Report - Copy-forward source exists - Published edit validation unchanged

**Description:** Regression - Published lesson report edit validation remains unchanged while copy-forward improvements are added.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce for the Aver tenant.
- Lesson report LR-105354-35 is Published.
- LR-105354-35 has Next Lesson Homework and Remarks values.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens LR-105354-35. | Published lesson report opens. | report = LR-105354-35; status = Published |
| 2 | HQ or CM Staff attempts to edit report fields without reverting to Draft. | Salesforce blocks the edit with the published report validation message. | changed_field = Next Lesson Homework |
| 3 | HQ or CM Staff confirms the report values after the blocked save. | Original report values remain unchanged. | expected_status = Published |

**Severity:** major
**Priority:** high

---

