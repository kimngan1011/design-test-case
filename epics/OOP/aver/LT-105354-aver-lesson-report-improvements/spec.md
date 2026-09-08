---
ticket_id: LT-105354
ticket_url: https://manabie.atlassian.net/browse/LT-105354
title: Q3 | Aver lesson report improvement items
module: scheduling
bucket: OOP/aver
status: Ready for QA
internal_uat_date: null
production_release_date: null
last_updated: 2026-09-08
---

# LT-105354: Q3 | Aver Lesson Report Improvement Items

## Summary

This epic improves Aver lesson report workflows across Salesforce, Back Office, generated PDFs, and Student App PDF output. The main business goal is to reduce repeated teacher input, improve long Japanese textbook rendering in PDFs, align homework remarks placement, expose next lesson date on Lesson List, and update previous/next lesson lookup logic to use the same Lesson Schedule only.

The linked Google Sheet cannot be read with the current Google Drive permission, so this spec is derived from the Jira description plus local Salesforce and BO implementation references:
- `Lesson_Report__c` and `Lesson_Report_Detail__c` support `Content`, `Next Lesson Homework`, `Next Lesson Announcement`, `Remarks`, `CM Note`, `Homework Completion`, `In-lesson Quiz`, and `Understanding`.
- Published lesson reports cannot be edited until reverted to Draft.
- Lesson Report is connected to Lesson and Student Session, and syncs SF -> BO -> Mobile.
- Aver is modeled as an OOP tenant-specific scheduling customization in this repo.

## Acceptance Criteria

### US 01 - PDF renders long textbook names without broken or duplicated text

- AC 01.1: Lesson report PDF displays long Japanese textbook names without duplicated characters or broken wrapping.
- AC 01.2: Textbook names longer than five rendered lines keep the full original value and do not repeat partial text.
- AC 01.3: PDF remains readable when multiple homework rows each contain long textbook names.

### US 02 - Breakthrough Test Next Time is copied to the next lesson Today's Result

- AC 02.1: When a lesson report is saved with Breakthrough Test `Next Time`, the next lesson in the same Lesson Schedule pre-fills `Today's Result` with that value.
- AC 02.2: The next lesson is resolved by same Lesson Schedule only, not by Student Lesson Allocation.
- AC 02.3: If the next lesson already has `Today's Result`, the existing value is not overwritten silently.

### US 03 - PDF moves homework Remark under textbook name

- AC 03.1: In the next week's homework section of the PDF, `Remark` appears under the textbook name.
- AC 03.2: Long textbook and long remark values remain readable and aligned within the same homework item.

### US 04 - BO copies Next Week Homework Remarks to the next lesson homework

- AC 04.1: When BO staff adds new homework in the next lesson with the same textbook as the previous lesson, `Remarks` is copied from the previous lesson homework.
- AC 04.2: The copied remark uses the most recent previous lesson value in the same Lesson Schedule.
- AC 04.3: If the current lesson remark is edited, the edited value becomes the source for the following lesson.
- AC 04.4: If the textbook differs, no remark is copied.
- AC 04.5: If no previous same-schedule lesson exists, no remark is copied.

### US 05 - Student App PDF report title shows monthly lesson count

- AC 05.1: Student App PDF title uses the format `指導簿 【生徒用・MM月X回目】`.
- AC 05.2: `X` is calculated as the lesson's order within the same month for that student, sorted by lesson date.
- AC 05.3: The monthly count resets when the lesson month changes.

### US 06 - Previous Week Homework is read-only in Edit Lesson Report mode

- AC 06.1: In BO Edit Lesson Report mode, Previous Week Homework does not show add or edit controls.
- AC 06.2: Previous Week Homework fields are read-only and cannot be changed from Edit Lesson Report mode.

### US 07 - Instructor's Comment 3 copies from previous to next lesson

- AC 07.1: `Instructor's Comment 3` is copied from the previous lesson to the next lesson in the same Lesson Schedule.
- AC 07.2: The copied comment remains editable on the next lesson.
- AC 07.3: An edited comment becomes the source for the following lesson.

### US 08 - Homework daily range hides year in add homework dialog

- AC 08.1: In BO Aver add homework dialogs for next and previous homework, homework date ranges display without year.
- AC 08.2: Japanese date format displays as `MM月DD日`.
- AC 08.3: Cross-year ranges still omit year in the date range display.

### US 09 - Lesson List shows Next Lesson column

- AC 09.1: Lesson List includes a new `Next Lesson` column.
- AC 09.2: Customizable Columns includes `Next Lesson`.
- AC 09.3: `Next Lesson` value is the next lesson date from the same Lesson Schedule and is hyperlinked to that lesson.
- AC 09.4: The last lesson in a Lesson Schedule shows blank or no link for `Next Lesson`.

### US 10 - Previous/Next lesson logic uses same Lesson Schedule only

- AC 10.1: Previous and next lesson logic for Homework, Lesson Report, and Lesson uses only lessons in the same Lesson Schedule.
- AC 10.2: Lessons from the same Student Lesson Allocation but a different Lesson Schedule are ignored.
- AC 10.3: Copy-forward behavior for homework remarks and Instructor's Comment 3 follows the same Lesson Schedule-only rule.

## Business Rules

| # | AC | Rule |
|---|---|---|
| 1 | AC 01.1-01.3 | PDF rendering must preserve long Japanese textbook strings exactly and wrap without duplicated characters. |
| 2 | AC 02.1-02.3 | Breakthrough Test copy-forward targets the next lesson's Today's Result in the same Lesson Schedule and must not overwrite existing content silently. |
| 3 | AC 03.1-03.2 | Next Week Homework PDF layout places Remark under textbook name. |
| 4 | AC 04.1-04.5 | Next lesson homework Remarks auto-copy only when the added homework has the same textbook as the previous same-schedule lesson. |
| 5 | AC 05.1-05.3 | Student App PDF title includes monthly lesson count by student and month. |
| 6 | AC 06.1-06.2 | Previous Week Homework is read-only in Edit Lesson Report mode. |
| 7 | AC 07.1-07.3 | Instructor's Comment 3 copy-forward follows same Lesson Schedule and remains editable. |
| 8 | AC 08.1-08.3 | Homework daily range in BO add homework dialog hides year and uses Japanese month/day format. |
| 9 | AC 09.1-09.4 | Lesson List and Customizable Columns expose a hyperlinked Next Lesson date derived from same Lesson Schedule. |
| 10 | AC 10.1-10.3 | Existing previous/next references must ignore same-student lessons in different Lesson Schedules. |

## Assumptions

- `Today's Result`, `Next Time`, and `Instructor's Comment 3` are Aver-specific lesson report fields shown by tenant form configuration even if their labels are not visible in the shared metadata search.
- The phrase "next lesson" always means the nearest future lesson within the same `Lesson Schedule`.
- Published report edit validation remains unchanged; tests that modify report fields use Draft or editable report status unless checking the validation.
- Student App PDF is verified after the lesson report is published and visible to the student.

## Requirement Gaps

| Gap | Impact | Test Handling |
|---|---|---|
| Google Sheet spec is not accessible from the connector. | Some UI screenshots and exact field ordering may be missing. | Testcases assert observable business rules from Jira and local repo logic. |
| Exact overwrite behavior for copied Today's Result is not explicitly stated. | Silent overwrite could destroy teacher input. | Include a non-overwrite regression case. |
| Exact blank display for last lesson Next Lesson column is not specified. | Could be blank, dash, or disabled link. | Test expects no clickable next lesson link and accepts blank/no link wording. |

