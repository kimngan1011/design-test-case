---
ticket_id: LT-110579
ticket_url: https://manabie.atlassian.net/browse/LT-110579
title: "[SF] [Lesson calendar] [Prod] Bulk Publish Lesson uses UTC boundaries instead of Salesforce timezone"
module: scheduling
bucket: calendar
status: New
internal_uat_date: null
production_release_date: null
last_updated: 2026-09-09
---

# LT-110579: Bulk Publish Lesson uses UTC boundaries instead of Salesforce timezone

## Summary

Bulk Publish Lesson on SF Lesson Calendar currently filters lessons by UTC day boundaries after users select a date range in the modal. The expected behavior is to evaluate the selected Start Date and End Date as Salesforce local dates, then publish only lessons whose start datetime belongs to that local date range.

Production example from the bug:

- Salesforce timezone is GMT+9.
- User selects Start Date = 2030-09-19 and End Date = 2030-09-19.
- Correct UTC range is `2030-09-18 15:00:00 UTC <= lesson start datetime < 2030-09-19 15:00:00 UTC`.
- Current behavior publishes roughly `2030-09-19 00:00 UTC` through `2030-09-19 22:59 UTC`, which maps to `2030-09-19 09:00` through `2030-09-20 07:59` in Salesforce timezone.

## Acceptance Criteria

### AC 01 - Salesforce timezone boundary is used for Bulk Publish filtering

- Bulk Publish Lesson converts selected Start Date and End Date using Salesforce timezone before filtering lessons.
- Selecting a single local date publishes only Draft lessons whose start datetime is within that Salesforce local date.
- Lessons from the previous or next Salesforce local date are not included.
- Regression coverage is added for GMT+9 boundary cases.

## Business Rules

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---|---|---|---|---|---|
| 1 | AC 01 | Start Date and End Date in Bulk Publish modal are Salesforce local dates, not raw UTC dates | Date range | local-date boundary | SF |
| 2 | AC 01 | For Salesforce timezone GMT+9, selected date `2030-09-19` maps to UTC range `2030-09-18 15:00:00` inclusive to `2030-09-19 15:00:00` exclusive | Lesson start datetime | converted boundary | SF |
| 3 | AC 01 | Draft lessons starting from `2030-09-19 00:00` to `2030-09-19 23:59` in Salesforce timezone are in scope | Lesson status and start datetime | publish eligible | SF |
| 4 | AC 01 | Draft lessons starting on `2030-09-18` or `2030-09-20` in Salesforce timezone are out of scope | Lesson start datetime | excluded | SF |
| 5 | AC 01 | Existing Bulk Publish scope rules still apply after timezone conversion: location scope, selected-student scope, and Draft-only status transition | Publish scope | unchanged | SF |

## Impact Analysis

| Area | Impact | Regression Guardrail |
|---|---|---|
| SF Bulk Publish modal | Existing Start Date, End Date, Location, and Apply to selected students fields remain unchanged | Do not add UI-only cases; verify publish result after submitting the modal |
| Async publish job | Queue/backend filter must preserve the Salesforce local-date boundary instead of truncating to UTC date | Seed lessons at GMT+9 lower and upper boundaries |
| Student-scoped bulk publish | Apply to selected students must use the same timezone conversion as all-student publish | Include selected-student boundary case |
| Notification and monitoring | Only successfully published lessons should feed downstream notification/monitoring | Verify out-of-scope lessons remain Draft and do not appear as published results |

## Related Files

- `epics/calendar/LT-98532-bulk-publish-lessons-by-student/` - existing Bulk Publish behavior, async refresh, selected-student scope, notification and monitoring rules.
- `epics/calendar/LT-102422-publish-lesson-menu-calendar/` - related calendar publish action behavior.
- `knowledge/domain-knowledge/scheduling/calendar/calendar-sf.md` - SF Calendar domain knowledge.
- `erp-salesforce/packages/lesson/main/default/lwc/modalBulkPublishLesson/` - Bulk Publish modal fields and timezone conversion before Apex call.
- `erp-salesforce/packages/lesson/main/default/classes/LessonHandler.cls` and `LessonBulkMasterQueueExecutor.cls` - backend publish scope and date filtering.

## Assumptions Made

- The bug is core SF Calendar behavior because the Jira bug is not tenant-specific and the affected environment is Production ERP SF & BO.
- Japan does not use daylight saving time, so GMT+9 is a fixed offset for the boundary cases.
- Lessons are evaluated by start datetime for inclusion in the publish date range, as stated in the Jira bug.
