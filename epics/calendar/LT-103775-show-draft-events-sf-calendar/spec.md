---
ticket_id: LT-103775
ticket_url: https://manabie.atlassian.net/browse/LT-103775
title: Koyu| Core | Show Draft Events in SF's Lesson Calendar
module: scheduling
bucket: calendar
status: Ready for QA
internal_uat_date: 2026-06-15
production_release_date: 2026-09-07
last_updated: 2026-08-12
---

# Spec: LT-103775 - Show Draft Events in SF's Lesson Calendar

## Summary

Show Activity Events with Event Status = Draft in Salesforce Lesson Calendar when the Draft Activity Event feature is enabled. Draft Event cards must follow the Draft Lesson visual pattern but use event green styling. Clicking a Draft Event opens the Activity Event detail drawer. Calendar Status filter uses the same status values for Lessons and Activity Events, so selecting Draft shows both Draft Lessons and Draft Events. Drag and drop is allowed for single-day Activity Events with status Draft or Published only; after drop, the Edit Event UI opens with Date, Start Time, End Time, and Classrooms derived from the drop tile, and saving moves the event card to the drop area.

## Source Evidence

- Jira `LT-103775`: Show Draft Events in SF Lesson Calendar, detail drawer, status filter, drag/drop edit.
- Linked PBT `PBT-2218`: Draft Activity Event baseline rules: Draft/Pubished create options, default Published, Draft to Published allowed, Draft to Completed blocked, Draft to Cancelled allowed, Draft hidden from Learner app and Booking system.
- Dev repo:
  - `school-portal-admin/src/squads/calendar/domains/CalendarV2/Calendar/hooks/useDraftEventEnabledSF.ts`
  - `school-portal-admin/src/squads/calendar/domains/CalendarV2/CalendarSF/IndividualCalendar.tsx`
  - `school-portal-admin/src/squads/calendar/domains/CalendarV2/Calendar/hooks/useDragDropCalendar.ts`
  - `school-portal-admin/src/squads/calendar/component-v2/ActivityEvent/ActivityEvent.tsx`
  - `school-portal-admin/src/squads/calendar/component-v2/ActivityEvent/MultiDayEventBar.tsx`
  - `erp-salesforce/packages/event/main/default/lwc/formActivityEvent/formActivityEvent.js`

## Acceptance Criteria

| AC | Requirement |
|---|---|
| AC 01 | SF Lesson Calendar shows Draft Activity Events when Draft Activity Event feature is enabled. |
| AC 02 | Draft Activity Event card uses Draft Lesson visual pattern with event green styling. |
| AC 03 | Clicking a Draft Activity Event opens the Activity Event detail drawer on the right side. |
| AC 04 | Calendar Status filter with Draft selected shows both Draft Lesson cards and Draft Event cards. |
| AC 05 | Drag and drop is allowed for single-day Activity Events whose status is Draft or Published. |
| AC 06 | Drag and drop opens Edit Event UI with Date, Start Time, End Time, and Classrooms from the drop tile. |
| AC 07 | Saving the Edit Event UI after drag/drop moves the Activity Event card to the drop area. |
| AC 08 | Draft Activity Events remain hidden when the Draft Activity Event feature flag is disabled or when not on SF calendar. |
| AC 09 | Draft Activity Events must not leak to Learner app Calendar or Booking system. |

## Business Rules

| ID | Rule |
|---|---|
| BR-01 | Draft Event visibility is controlled by `MANAERP__Enable_Draft_Status_On_Activity_Event__c` on SF Calendar. |
| BR-02 | When the flag is off, Draft Activity Events are filtered out; Published, Completed, and Cancelled Activity Events remain eligible. |
| BR-03 | Draft Event card styling is white background with green border; Published Event uses green filled styling. |
| BR-04 | Status filter applies to both Lesson status and Activity Event status. |
| BR-05 | Default calendar status filter selects Published and Completed, not Draft or Cancelled. |
| BR-06 | Event type filter still controls Activity Event visibility independent of status. |
| BR-07 | Teacher, student, capacity, range time, and date/view filters still apply to Draft Events like other Activity Events. |
| BR-08 | Only single-day Draft or Published Activity Events are draggable. Completed, Cancelled, and multi-day Activity Events are not draggable. |
| BR-09 | Drag/drop recalculates Start Date Time and End Date Time from the target tile; timeslot mode uses timeslot master start/end when available. |
| BR-10 | Drag/drop edit must preserve Activity Event Status unless the user changes it in the edit form. |
| BR-11 | Clicking a Draft Event must open Activity Event detail (`objectType = ACTIVITY`), not Lesson detail. |
| BR-12 | Draft Events are hidden from Learner app Calendar, Booking system, and public event APIs that only return Published events. |

## Out of Scope

- Creating Draft status itself is covered by `PBT-2218` / `LT-96096`.
- Activity Event CRUD outside SF Lesson Calendar is covered by Draft Activity Event baseline test suites.
- Migration of old Activity Events is not required.

