## Suite: Lesson Summary Page

### Lesson Report – List View – Component – User views lesson report list – Display standard items
**Description:** AC1 Component - Verify standard display items on the list view.
**Preconditions:**
- Actor: HQ or CM Staff
- Existing lesson report with explicit `lesson_name = "Math 101"`, `lesson_date = "2026-06-25"`, `teacher_name = "John Doe"`, `content = "Algebra"`, `next_lesson_homework = "Page 10"`, `next_lesson_announcement = "Test next week"`, `understanding = "Good"`, `in_lesson_quiz = "8/10"`, `homework_completion = "Done"`, and `remarks = "Good job"`.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Navigate to the lesson report list view | The list view is loaded | `""` |
| 2 | Observe the columns for the lesson report | The list view displays the columns for Lesson name, Lesson date, Teacher name, Content, Next Lesson - Homework, Next Lesson - Announcement, Understanding, In-lesson Quiz, Homework Completion, and Remarks matching the expected data | `""` |

**Severity:** minor
**Priority:** medium

### Lesson Report – List View – Component – User selects direct edit on group report – Allow inline editing of group lesson report
**Description:** AC2 CRUD - Verify direct editing functionality of a group lesson report.
**Preconditions:**
- Actor: HQ or CM Staff
- Existing lesson report with multiple students.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Navigate to the lesson report list view | The list view is loaded | `""` |
| 2 | Select Record > Edit for the target group lesson report | The inline edit mode or edit popup is displayed | `""` |
| 3 | Update the general group lesson report details and save | The group lesson report is successfully updated and changes are reflected in the list view | `updated_details = "Updated group notes"` |

**Severity:** major
**Priority:** high

### Lesson Report – List View – Component – User selects direct edit on individual report – Allow inline editing of individual lesson report
**Description:** AC2 CRUD - Verify direct editing functionality of an individual lesson report (Lesson Report Detail).
**Preconditions:**
- Actor: HQ or CM Staff
- Existing lesson report with student sessions.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Navigate to the lesson report list view | The list view is loaded | `""` |
| 2 | Select Record > Edit for the target individual lesson report detail (student specific) | The inline edit mode or edit popup for the specific student is displayed | `""` |
| 3 | Update the individual report details (e.g. attendance, score) and save | The individual lesson report is successfully updated and changes are reflected in the list view | `attendance_status = "Attended", student_score = "90"` |

**Severity:** major
**Priority:** high

### Lesson Report – List View – Component – User cancels direct edit – Discard changes
**Description:** AC2 CRUD - Verify direct editing functionality of lesson records (Cancel).
**Preconditions:**
- Actor: HQ or CM Staff
- Existing lesson report.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Navigate to the lesson report list view | The list view is loaded | `""` |
| 2 | Select Record > Edit for a target lesson report | The inline edit mode or edit popup is displayed | `""` |
| 3 | Modify details but select Cancel | The edit mode is closed and the original data remains unchanged | `updated_details = "Discarded notes"` |

**Severity:** major
**Priority:** high

### Lesson Report – List View – Component – User adjusts display – Display settings are applied
**Description:** AC3 CRUD - Verify adjusting lesson report display.
**Preconditions:**
- Actor: HQ or CM Staff
- Existing lesson report in the list view.

| # | Action | Expected Result | Test Data |
| --- | --- | --- | --- |
| 1 | Navigate to the lesson report list view | The list view is loaded | `""` |
| 2 | Open display settings or adjust lesson report display option | Display settings are shown | `""` |
| 3 | Modify display preferences (e.g. toggle columns) and apply | The list view updates to reflect the new display preferences | `column_toggle = "Hide Teacher Name"` |
