---
ticket_id: LT-102367
ticket_url: https://manabie.atlassian.net/browse/LT-102367
title: Event - Bulk Collect Attendance improvement
module: scheduling / event calendar
bucket: calendar
status: Ready for QA
analysis_date: 2026-09-14
---

# LT-102367: Event - Bulk Collect Attendance improvement

## Summary

LT-102367 improves bulk collect attendance around Event Calendar attendance flows. Jira itself has no detailed description, so this analysis uses the feature inventory and merged local implementation behavior from `erp-salesforce` and `school-portal-admin`.

The confirmed product scope from Confluence is Event Calendar `US 37` / BO Calendar `US 37.2`: collect attendance with bulk mark attendance. The code impact also shows a shared/adjacent BO Calendar lesson attendance implementation using bulk student-session attendance APIs, so the testcase set covers both the visible Event Participant collect-attendance flow and implementation-only regressions in the bulk update contract.

## Sources Read

- Jira: `LT-102367` - `Event - Bulk Collect Attendance improvement`
- Jira: `LT-108102` - QA task for this epic
- Confluence: `Event Scope Feature Inventory`, Event Calendar `US 37`, BO Calendar `US 37.2`
- Rovo search result: related private PR candidate `manabie-com/student-app#13917` / `LT-102398 Implement submit multiple event attendance` could not be read through the available GitHub connector because it returned 404
- `school-portal-admin/src/squads/calendar/domains/CalendarV2/Calendar/components/DetailSections/DetailSectionEventParticipant/DetailSectionEventParticipant.tsx`
- `school-portal-admin/src/squads/calendar/domains/CalendarV2/Calendar/components/Dialogs/DialogCollectAttendanceEventParticipant/DialogCollectAttendanceEventParticipant.tsx`
- `school-portal-admin/src/squads/calendar/domains/CalendarV2/Calendar/components/Forms/FormCollectAttendance/FormCollectAttendance.tsx`
- `school-portal-admin/src/squads/calendar/domains/CalendarV2/Calendar/components/Forms/FormCollectAttendance/FormItemCollectAttendance.tsx`
- `school-portal-admin/src/squads/calendar/domains/CalendarV2/Calendar/components/DetailSections/DetailSectionEventParticipant/EventParticipant.tsx`
- `school-portal-admin/src/squads/calendar/domains/CalendarV2/Calendar/hooks/useCalendarAction/useCalendarAction.ts`
- `school-portal-admin/src/squads/calendar/domains/CalendarV2/Calendar/components/Dialogs/DialogCollectAttendance/DialogCollectAttendance.tsx`
- `school-portal-admin/src/squads/calendar/domains/CalendarV2/Calendar/hooks/useControlBulkUpdateStudentSessionAttendance.ts`
- `erp-salesforce/packages/event/main/default/classes/EventParticipantRestAPI.cls`
- `erp-salesforce/packages/event/main/default/classes/EventParticipantHandler.cls`
- `erp-salesforce/packages/event/main/default/classes/restapi/tests/EventRestAPITest.cls`
- `erp-salesforce/packages/lesson/main/default/classes/StudentSessionRestAPI.cls`
- `erp-salesforce/packages/lesson/main/default/classes/StudentSessionsHandler.cls`
- Existing related coverage: `epics/calendar/PBT-3120-student-sort-bulk-mark-attendance`
- Existing related coverage: `epics/lesson/LT-96152-collect-attendance-entry-points-bo`

## Acceptance Criteria

### US 01 - Collect attendance for Activity Event participants from Calendar

- AC 01.1: Activity Event detail shows a `Collect Attendance` action in the Event Participant section.
- AC 01.2: Clicking `Collect Attendance` opens a bulk collect-attendance dialog containing all loaded Event Participants.
- AC 01.3: Each participant can be marked `Attend` or `Absent`.
- AC 01.4: Selecting `Absent` opens a remark dialog; saving stores the remark with that participant.
- AC 01.5: Selecting `Attend` clears the attendance remark for that participant.
- AC 01.6: The edit remark action is disabled until a participant has an attendance status.
- AC 01.7: Saving submits the selected participant attendance statuses and notes, shows success feedback, closes the dialog, and refreshes Event Participant display.

### US 02 - Bulk actions and validation

- AC 02.1: `Mark all as Attend` applies only to participants without an existing attendance status.
- AC 02.2: `Mark all as Absent` applies only to participants without an existing attendance status.
- AC 02.3: Existing participant attendance statuses are not overwritten by bulk mark-all actions.
- AC 02.4: Saving with no participant attendance selected is blocked with the configured empty-participant attendance error.
- AC 02.5: API failure keeps the dialog open and shows the generic error snackbar.

### US 03 - Persist event participant attendance through Salesforce API

- AC 03.1: The Calendar FE payload sends `eventParticipants` containing only the participant Id, attendance status, and attendance note needed by the API.
- AC 03.2: Salesforce `POST /eventParticipants/v1/collectAttendance` upserts multiple `Event_Participant__c` records and returns 200.
- AC 03.3: Empty or null event participant payloads are rejected by the backend with the existing `No_Selected_Participant` guard.

### US 04 - Guard adjacent BO Calendar lesson attendance regression

- AC 04.1: BO Calendar `Mark Attendance` bulk action is visible only when BO is not calling SF and `Calendar_IndividualCalendar_BulkUpdateAttendance` is enabled; it is disabled when location is missing.
- AC 04.2: Lesson collect-attendance dialog pre-fills attendance status from saved attendance status or from attendance response text.
- AC 04.3: Lesson collect-attendance dialog requires every student session row to have attendance status before save.
- AC 04.4: Lesson bulk update payload sends attendance reason for non-Attend, attendance notice and reallocate flag only for Absent, and always sends attendance note.
- AC 04.5: Salesforce bulk student-session attendance update marks reallocation only when status changes to Absent with reallocate on, and unflags reallocation when an already reallocated session is changed to reallocate off.

## Business Rules

| # | AC | Business Rule | Source |
|---|---|---|---|
| 1 | AC 01.1 | Event Participant section always includes `Collect Attendance` action with `Download Participant List`. | `DetailSectionEventParticipant.tsx` |
| 2 | AC 01.2 | Dialog default form values are the event participant list passed from the detail drawer. | `DialogCollectAttendanceEventParticipant.tsx` |
| 3 | AC 01.3 | Event participant attendance choices are limited to `Attend` and `Absent`. | `EventParticipantAttendanceStatus` |
| 4 | AC 01.4 | Selecting Absent opens the remark dialog before applying status/note. | `FormItemCollectAttendance.tsx` |
| 5 | AC 01.5 | Selecting Attend calls `onSelectAttendance(status, "")`, clearing the note. | `FormItemCollectAttendance.tsx` |
| 6 | AC 01.6 | Edit icon is disabled when current attendance status is empty. | `FormItemCollectAttendance.tsx` |
| 7 | AC 02.1/02.2 | Mark-all changes only rows where `Attendance_Status__c` is empty. | `FormCollectAttendance.tsx` |
| 8 | AC 02.4 | Form is valid when at least one participant has attendance status, otherwise shows `collectAttendanceEmptyParticipant`. | `DialogCollectAttendanceEventParticipant.tsx` |
| 9 | AC 03.1 | Payload maps to `eventParticipants[{Id, Attendance_Status__c, Attendance_Note__c}]`. | `toCollectAttendancePayload` |
| 10 | AC 03.2 | Backend REST route is `POST /eventParticipants/v1/collectAttendance`. | `EventParticipantRestAPI.cls` |
| 11 | AC 03.3 | `EventParticipantHandler.upsertEventParticipants` rejects null/empty payloads. | `EventParticipantHandler.cls` |
| 12 | AC 04.1 | BO Calendar bulk Mark Attendance is hidden in SF mode, gated by feature flag, and disabled without `locationId`. | `useCalendarAction.ts` |
| 13 | AC 04.2 | Lesson collect-attendance derives default status from `attendanceStatus` or parsed `attendanceResponse`. | `DialogCollectAttendance.tsx` |
| 14 | AC 04.3 | Lesson collect-attendance save is valid only when every student session has a status. | `DialogCollectAttendance.tsx` |
| 15 | AC 04.4 | FE omits reason for Attend; notice/reallocate are sent only for Absent. | `useControlBulkUpdateStudentSessionAttendance.ts` |
| 16 | AC 04.5 | Backend bulk student-session update batches mark/unflag reallocation around DML. | `StudentSessionsHandler.cls` |

## Conflict & Gap Analysis

| # | Tag | Source | Description |
|---|---|---|---|
| 1 | SPEC GAP | Jira LT-102367 | Jira has no description or AC details. Test cases must rely on Confluence feature inventory and source code behavior. |
| 2 | PR GAP | GitHub connector | Related private PR candidate `student-app#13917` returned 404, so mobile PR diff could not be inspected. |
| 3 | IMPLEMENTATION RISK | `FormCollectAttendance.tsx` | Mark-all intentionally does not overwrite rows that already have attendance status; this is not visible in spec. |
| 4 | DATA LOSS RISK | `FormItemCollectAttendance.tsx` | Switching a participant to Attend clears attendance note; Absent cancel must not apply a partial change. |
| 5 | VALIDATION DIFFERENCE | Event vs lesson attendance dialogs | Event attendance requires at least one selected participant; lesson attendance requires every student row to have status. |
| 6 | API RISK | `EventParticipantRestAPI.cls` | Backend upserts the provided records; wrong payload shape or empty list can break all selected participants. |
| 7 | ADJACENT REGRESSION | `StudentSessionRestAPI.cls`, `StudentSessionsHandler.cls` | Shared attendance update semantics can regress reallocation, reason/notice clearing, and attendance note persistence. |

## Related Existing Cases

- `PBT-3120` covers student ordering and JP type labels in Bulk Mark Attendance; LT-102367 should not duplicate sort-only coverage.
- `LT-96152` covers new BO Lesson Report collect-attendance entry points; LT-102367 reuses the collect-attendance persistence baseline but adds event participant bulk behavior and payload semantics.

## QASE Coverage Target

- Parent suite: `Calendar lesson` (`suite_id=2717`, `suite_parent_id=2628`) because the impacted UI is Calendar V2.
- Imported child suite: `Event Bulk Collect Attendance` (`suite_id=3528`, `suite_parent_id=2717`).
- Imported cases: `PX-28127` to `PX-28142`.
- Test run: `PX-3536` — https://app.qase.io/run/PX/dashboard/3536.
- Existing impacted regression cases were intentionally skipped from the run per request.
