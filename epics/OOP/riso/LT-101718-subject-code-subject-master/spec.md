---
ticket_id: LT-101718
pbt_id: PBT-3075
qa_ticket_id: LT-110291
ticket_url: https://manabie.atlassian.net/browse/LT-101718
pbt_url: https://manabie.atlassian.net/browse/PBT-3075
title: Riso | Core | Add Subject Code in Subject Master
module: scheduling
bucket: riso
status: Ready for QA
last_updated: 2026-09-18
---

# Spec: LT-101718 / PBT-3075 - Add Subject Code in Subject Master

## Summary

Add optional `Subject Code` / `科目コード` to Subject Master so users can maintain a short code, number, or shortened subject name for compact displays. The field is `MANAERP__Subject_Code__c`, Text(30), optional. Data migration is not required.

The field is consumed by Teacher Available Calendar student lesson display: when a student is selected, existing lesson chips use Subject Code from Subject Master, plus assigned teacher family name when available.

## Source Evidence

- Jira `PBT-3075`: `[Riso] Core | Add Subject Code in Subject Master`, status In Development.
- Jira `LT-101718`: implementation epic, status Ready for QA.
- Jira `LT-110291`: QA ticket to create testcase and test on preprod.
- Confluence PRD `Riso | Core | Teacher Available Calendar`, US02.2: selected student lesson display uses `Slot Name`, `Subject Code`, and teacher family name.
- Dev repo:
  - `erp-salesforce/packages/master/main/default/objects/Subject_Master__c/fields/Subject_Code__c.field-meta.xml`
  - `erp-salesforce/packages/master-ext/main/default/layouts/Subject_Master__c-Subject Master Layout_Ext.layout-meta.xml`
  - `erp-salesforce/packages/master-ext/main/default/flexipages/Subject_Master_Record_Page_Ext.flexipage-meta.xml`
  - `erp-salesforce/packages/master/main/default/objects/Subject_Master__c/listViews/All_Subjects.listView-meta.xml`
  - `erp-salesforce/packages/master/main/default/objects/Subject_Master__c/listViews/Active_Subjects.listView-meta.xml`
  - `erp-salesforce/packages/lesson/main/default/classes/AvailableTeacherHandler.cls`
  - `school-portal-admin/src/squads/calendar/domains/CalendarV2/AvailableTeacherCalendar/hooks/useStudentLessonsForMonth.ts`
  - `school-portal-admin/src/squads/calendar/domains/CalendarV2/AvailableTeacherCalendar/components/CalendarDayCell.tsx`

## Acceptance Criteria

| AC | Requirement |
|---|---|
| AC 01.1 | Subject Master has `Subject Code` / `科目コード` field with API `MANAERP__Subject_Code__c`, Text(30), optional. |
| AC 01.2 | Users with Subject Master edit permission can input, save, edit, and clear Subject Code. |
| AC 01.3 | New and detail/edit Subject Master views show Subject Code in the expected form/detail layout. |
| AC 01.4 | Subject Master list/search relevant views show Subject Code so users can identify subjects in limited space. |
| AC 01.5 | Existing subjects without Subject Code remain valid and usable; no migration is required. |
| AC 02.1 | Teacher Available Calendar selected student lesson chips display Subject Code from the lesson subject's Subject Master. |
| AC 02.2 | When a selected student's lesson has an assigned teacher, the lesson chip displays Subject Code and teacher family name. |
| AC 02.3 | When a selected student's lesson has no assigned teacher, the lesson chip displays Subject Code without a teacher name. |
| AC 02.4 | Subject Code display does not change available teacher count/filter logic, student search, or lesson creation prefill behavior. |
| AC 03.1 | Existing Course Code behavior in Course Master is unchanged. |

## Business Rules

| ID | Rule |
|---|---|
| BR-01 | `Subject_Code__c` is optional; blank values are allowed. |
| BR-02 | `Subject_Code__c` maximum length is 30 characters. |
| BR-03 | No historical data migration is required; old Subject Master records may have blank Subject Code. |
| BR-04 | Subject Code is a display/identification field, not a uniqueness key unless future scope says otherwise. |
| BR-05 | Teacher Available Calendar student lesson overlay sources Subject Code through `Lesson__r.Subject__r.Subject_Code__c`. |
| BR-06 | Teacher Available Calendar assigned-teacher label uses teacher family name; unassigned lessons omit teacher name. |
| BR-07 | Available teacher determination remains based on teacher availability and no duplicate lesson assignment, not Subject Code. |

## Existing Qase / Repo Impact

| Area | Finding | Action |
|---|---|---|
| Qase Subject Code | Read-only Qase search found no existing case for `Subject Code`, `Subject_Code`, `科目コード`, `LT-101718`, or `PBT-3075`. | Create new suite/cases for this epic. |
| Qase Available Teacher Calendar | Existing suites `3011-3014` cover ATC panel, student search/API, and create lesson, but no case title/steps found for selected student lesson Subject Code display. | Add new cases; optionally update `PX-23042`, `PX-23045`, `PX-23046`, `PX-23048` with regression notes. |
| Repo Apex tests | `AvailableTeacherHandlerTest` covers `getStudentLessonsForMonth` happy paths and `hasTeacher`, but does not assert `subjectCode`. | Add Apex assertion for Subject Code mapping. |
| Repo FE tests | No focused FE unit test found for `useStudentLessonsForMonth` mapping or `CalendarDayCell` Subject Code label. | Add FE tests if this area becomes automated. |
| Metadata permissions/layout | Field, layout, flexipage, list view, and permission metadata exist in repo. | Manual QA should validate deployed org behavior. |

## Out of Scope

- Data migration for existing Subject Master records.
- New uniqueness validation for Subject Code.
- Redesign of Teacher Available Calendar beyond Subject Code display path.
- Teacher availability management form unless confirmed by product as part of this epic.
