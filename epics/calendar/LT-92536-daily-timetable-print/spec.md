---
ticket_id: LT-92536
ticket_url: https://manabie.atlassian.net/browse/LT-92536
title: Riso | Core | Daily Timetable Print Functionality for Audit Trail and Classroom Management
module: scheduling
bucket: calendar
status: Ready for QA
target_uat_date: 2026-03-02
production_release_date: 2026-09-07
last_updated: 2026-08-19
---

# Spec: LT-92536 - Daily Timetable Print Functionality

## Summary

Improve SF Lesson Calendar daily timetable printing for Individual lessons. A CM/HQ user opens Daily view, chooses Print Out, keeps Individual selected, and opens a new PDF tab using the new Individual timetable template when `MANAERP__Enable_Individual_Daily_Timetable_Print__c` is enabled. The PDF is A3 landscape, named `Schedule [yyyymmdd] - Individual.pdf`, grouped by active Timeslot Master when Timeslot mode is enabled, or by distinct lesson start/end time when Timeslot mode is disabled. Only Published Individual lessons for the selected location and date are included.

## Source Evidence

- Jira `LT-92536`: Core daily timetable print functionality, status Ready for QA, release `v2026.09.07`.
- Linked PBT `PBT-1500`: daily timetable print for audit trail and classroom management; blocked by Timeslot Master `PBT-2130`.
- PRD: `Riso | Core | SF | Daily Timetable Printing for Infdividual lessons`, Confluence page `2130673665`.
- Baseline print dialog spec: `Calendar| Arrangement Table| Print out function on Daily view`, Confluence page `548438017`.
- Timeslot Master PRD: `RISO | Core | Timeslot`, Confluence page `2310668310`.
- Dev repo:
  - `erp-salesforce/packages/lesson/main/default/classes/IndividualTimetablePrintController.cls`
  - `erp-salesforce/packages/lesson/main/default/pages/IndividualTimetablePrintPdf.page`
  - `erp-salesforce/packages/lesson/main/default/classes/repository/LessonRepo.cls`
  - `erp-salesforce/packages/lesson/main/default/lwc/individualCalendar/individualCalendar.js`
  - `erp-salesforce/packages/lesson/main/default/classes/LessonFeatureToggles.cls`
  - `school-portal-admin/src/squads/calendar/domains/CalendarV2/Calendar/components/Dialogs/DialogPrintOut/DialogPrintOut.tsx`

## Acceptance Criteria

| AC | Requirement |
|---|---|
| AC 01.1 | Print Out remains available only from Daily view; it is available in Teacher view and Classroom view, and unavailable from Weekly/Monthly views. |
| AC 01.2 | Print Out dialog remains the current dialog: Individual/Group radio options, Individual default, Confirm opens PDF in a new tab, Cancel returns to calendar unchanged. |
| AC 01.3 | When Individual is selected and Individual timetable flag is enabled, use the new Individual timetable PDF path, not the legacy CalendarPrintOut PDF. |
| AC 01.4 | PDF file name is `Schedule [yyyymmdd] - Individual.pdf`. |
| AC 01.5 | PDF page setup is A3 landscape with location header, lesson date `yyyy年MM月dd日（weekday）`, printing date `yyyy年MM月dd日`, page number, and stamping rectangle at bottom right. |
| AC 01.6 | PDF includes only Published Individual lessons for the selected location and selected lesson date. Draft, Completed, Cancelled, Group lessons, other dates, and other locations are excluded. |
| AC 01.7 | Timeslot mode groups by active Timeslot Master used by matching lessons. Block header is `Timeslot name + 限 Start time - End time`; blocks are ordered by Timeslot sequence. |
| AC 01.8 | Manual time mode groups by distinct lesson Start Date Time and End Date Time, sorted by start time ASC then end time ASC. |
| AC 01.9 | AM blocks render before PM blocks. Each physical page has up to 4 blocks; overflow creates additional pages while preserving header layout. |
| AC 01.10 | Every block lists all classrooms under the selected location, sorted by classroom sequence ASC, then name ASC. |
| AC 01.11 | Each classroom row shows Attendance, Booth, Grade, Course, Subject, Student, Teacher, and Remarks columns with fixed widths and text wrapping. |
| AC 01.12 | Student, grade, course, subject, and teacher data are populated from published lessons, student sessions, allocations, course offerings, subjects, and lesson teachers. |
| AC 01.13 | Seasonal students show a star marker on course display. |
| AC 01.14 | Remarks show other timeslot numbers/labels for students who have multiple published lessons on the same day/location. |
| AC 01.15 | Empty data scenarios still generate a usable timetable with classroom rows and blank lesson cells, without rendering broken or blank PDFs. |
| AC 01.16 | If the new Individual timetable flag is disabled or the selected teaching method is Group, the existing legacy print flow remains unchanged. |
| AC 01.17 | Missing or invalid PDF request parameters show an error instead of server crash. |

## Business Rules

| ID | Rule |
|---|---|
| BR-01 | New Individual timetable PDF is gated by `MANAERP__Enable_Individual_Daily_Timetable_Print__c`. |
| BR-02 | Timeslot grouping is gated by `MANAERP__Show_Timeslot_In_Lesson__c`. |
| BR-03 | Backend query filters lessons by `Status__c = Published` and `Teaching_Method__c = Individual`. |
| BR-04 | Backend query filters by selected lesson date using `Start_Date_Time__c >= startOfDay` and `< startOfNextDay`. |
| BR-05 | Backend query filters by selected calendar location through `Lesson_Schedule__r.Account__c`. |
| BR-06 | Classroom rows come from Classroom Master under selected location and are ordered by `Sequence__c ASC NULLS LAST, Name ASC, CreatedDate ASC`. |
| BR-07 | Timeslot mode uses active Timeslot Masters and lesson `Timeslot__c`; lessons without Timeslot are not mapped into a Timeslot block. |
| BR-08 | Manual mode uses unique start/end pairs; header is time range only. |
| BR-09 | AM/PM split uses noon boundary: start hour `< 12` = AM, otherwise PM. |
| BR-10 | Each page has four blocks. Missing blocks are padded with blank headers and classroom-only rows. |
| BR-11 | If a classroom has no matching lesson in a block, lesson data cells are blank. |
| BR-12 | Text wrapping is intentional for long CJK/Latin strings so values do not overflow fixed columns. |
| BR-13 | Group print remains legacy `CalendarPrintOutPdf` behavior. |
| BR-14 | Feature flag disabled for Individual print falls back to legacy print behavior from the existing print dialog. |

## Implementation Risks / Clarifications

| Risk | Evidence | QA Action |
|---|---|---|
| PRD says no lessons for AM/PM timeslot master should still retain AM and PM timeslot templates, but current controller comments/code render one classroom-only page when no block has a lesson and skip unused timeslots. | `IndividualTimetablePrintController.buildTimeslotBlockSpecs`, `buildPages` | Keep tests written to PRD expected behavior; raise if implementation returns fewer pages or hides expected empty timeslot blocks. |
| Old dialog copy says "Only Published or Completed lesson will be printed out", while new backend filters Published only. | `DialogPrintOut.tsx`, `LessonRepo.getPublishedIndividualLessons` | Test both backend data exclusion and UI copy mismatch. |
| Timeslot mode drops Published Individual lessons with blank `Timeslot__c`; PRD focuses timeslot master operation but manual override/no-timeslot behavior may need confirmation. | `mapLessonsByTimeslotKey` | Include regression case for no-timeslot lessons under Timeslot mode. |

## Out of Scope

- Timeslot Master CRUD and CSV import are covered by `PBT-2130`.
- Group timetable PDF redesign is not part of LT-92536; Group continues existing print flow.
- Automated next-morning print queue generation is mentioned in background but not part of current SF click-to-print scope.
