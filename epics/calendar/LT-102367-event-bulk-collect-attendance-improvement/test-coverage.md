# Test Coverage: LT-102367 - Event Bulk Collect Attendance Improvement

**Jira:** https://manabie.atlassian.net/browse/LT-102367  
**Date:** 2026-09-14  
**Module:** scheduling / event calendar  
**Platform:** BO Calendar, Salesforce REST API

## Business Rules Extracted

| # | Rule |
|---|---|
| 1 | Event Participant section exposes Collect Attendance from Activity Event detail. |
| 2 | Bulk attendance dialog loads all currently loaded event participants. |
| 3 | Event participant attendance choices are limited to Attend and Absent. |
| 4 | Absent opens remark dialog and persists the note. |
| 5 | Attend clears participant attendance note. |
| 6 | Edit remark is disabled before attendance status exists. |
| 7 | Mark-all Attend/Absent fills only rows with empty attendance status. |
| 8 | Save requires at least one selected event participant attendance status. |
| 9 | Successful save closes dialog, refreshes participant display, and shows success snackbar. |
| 10 | API failure keeps dialog open and shows generic error snackbar. |
| 11 | Backend route `/eventParticipants/v1/collectAttendance` upserts multiple event participants. |
| 12 | Backend rejects null/empty event participant payload. |
| 13 | Adjacent BO Calendar Mark Attendance action is flag-gated and location-gated. |
| 14 | Lesson collect attendance pre-fills from status or attendance response text. |
| 15 | Lesson collect attendance requires every student session to have status. |
| 16 | Lesson bulk payload conditionally includes reason, notice, and reallocate flag. |
| 17 | Student-session bulk update marks/unflags reallocation correctly. |

## Structured Coverage Strategy

| Area | Rules | Technique | Risk | Coverage Depth |
|---|---|---|---|---|
| Event participant entry point | 1, 2 | Scenario | High | Standard |
| Participant status selection | 3, 4, 5, 6 | Decision Table / State Transition | High | Deep |
| Mark-all behavior | 7 | Decision Table / Negative | High | Deep |
| Validation and error handling | 8, 10, 12 | Negative | High | Deep |
| Success persistence | 9, 11 | CRUD / API Contract | Critical | Deep |
| Display after save | 9 | Regression | High | Standard |
| Adjacent lesson attendance action | 13 | Feature Flag Matrix | Medium | Standard |
| Adjacent lesson attendance form | 14, 15, 16, 17 | Contract / Regression | High | Deep |

## Coverage Matrix

| Case | Title | AC / Rules | Source |
|---|---|---|---|
| TC-01 | Activity Event detail opens bulk collect attendance dialog | AC 01.1-01.2 / Rules 1-2 | `DetailSectionEventParticipant.tsx` |
| TC-02 | Mark one participant Attend and save | AC 01.3, 01.5, 01.7, 03.1-03.2 / Rules 3, 5, 9, 11 | FE form + REST API |
| TC-03 | Mark one participant Absent with remark and save | AC 01.3-01.4, 01.7, 03.1-03.2 / Rules 3, 4, 9, 11 | FE form + REST API |
| TC-04 | Cancel Absent remark dialog does not change row | AC 01.4 / Rules 4, 6 | `FormItemCollectAttendance.tsx` |
| TC-05 | Edit remark disabled until status exists | AC 01.6 / Rule 6 | `FormItemCollectAttendance.tsx` |
| TC-06 | Edit existing Absent remark pre-fills previous note | AC 01.4, 01.7 / Rules 4, 9 | `FormItemCollectAttendance.tsx` |
| TC-07 | Mark all as Attend only fills empty rows | AC 02.1, 02.3 / Rule 7 | `FormCollectAttendance.tsx` |
| TC-08 | Mark all as Absent only fills empty rows and does not force remarks | AC 02.2-02.3 / Rule 7 | `FormCollectAttendance.tsx` |
| TC-09 | Save with no selected attendance is blocked | AC 02.4 / Rule 8 | `DialogCollectAttendanceEventParticipant.tsx` |
| TC-10 | API failure keeps dialog open and shows error | AC 02.5 / Rule 10 | `DialogCollectAttendanceEventParticipant.tsx` |
| TC-11 | Backend rejects empty event participant payload | AC 03.3 / Rule 12 | `EventParticipantHandler.cls` |
| TC-12 | BO Calendar Mark Attendance action follows flag/location gating | AC 04.1 / Rule 13 | `useCalendarAction.ts` |
| TC-13 | Lesson collect attendance pre-fills status from attendance response | AC 04.2 / Rule 14 | `DialogCollectAttendance.tsx` |
| TC-14 | Lesson collect attendance blocks save until every row has status | AC 04.3 / Rule 15 | `DialogCollectAttendance.tsx` |
| TC-15 | Lesson bulk payload sends reason/notice/reallocate conditionally | AC 04.4 / Rule 16 | `useControlBulkUpdateStudentSessionAttendance.ts` |
| TC-16 | Student-session bulk update marks/unflags reallocation | AC 04.5 / Rule 17 | `StudentSessionsHandler.cls` |

## High-Risk Areas

| Area | Reason | Recommended Approach |
|---|---|---|
| Multi-record event upsert | One failed payload shape affects every selected participant. | Verify FE payload and REST 200/readback for multiple participants. |
| Mark-all non-overwrite behavior | Users may expect mark-all to overwrite, but code intentionally preserves existing status. | Explicitly assert existing statuses are untouched. |
| Remark data loss | Attend clears note and Absent cancel should not write a half-edited note. | Include state-transition tests around status switch and modal cancel/save. |
| Validation difference from lesson attendance | Event flow requires at least one selected attendance; lesson flow requires all rows. | Keep separate event and lesson validation cases. |
| Reallocation side effect | Lesson adjacent bulk attendance can create/remove reallocation records. | Assert backend mark/unflag behavior, not just UI status. |

## Existing Coverage Impact

| Existing Area | Existing Case Set | Overlap | LT-102367 Action |
|---|---|---|---|
| Student order and Type labels | `PBT-3120-student-sort-bulk-mark-attendance` | Sort/localization only | Do not duplicate; keep as regression reference. |
| BO lesson collect attendance entry points | `LT-96152-collect-attendance-entry-points-bo` | Entry-point parity and save baseline | Extend with Event Participant bulk flow and API payload behavior. |
| Activity Event detail participant display | Event calendar existing cases | Display-only partial overlap | Add action/save/readback tests. |

## Gaps / Assumptions

- Mobile PR diff for `student-app#13917` was not readable through the available GitHub connector, so mobile-specific multiple event attendance submission cases are marked as out-of-repo evidence gap rather than asserted from source.
- Jira LT-102367 has no AC body; tests are intentionally implementation-informed.
- If Qase import is requested, create or reuse a child suite under `PX` suite `2717` named `Event Bulk Collect Attendance`.
