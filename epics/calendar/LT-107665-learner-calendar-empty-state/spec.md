---
ticket_id: LT-107665
ticket_url: https://manabie.atlassian.net/browse/LT-107665
implementation_ticket: PBT-1290
title: Core | Learner app | Change "No lesson/event" text
module: learner-app-calendar
bucket: calendar
status: Ready for QA
last_updated: 2026-09-10
---

# Spec: LT-107665 - Learner App Calendar Empty-State Messages

## Summary

Replace the misleading Live Lesson-only empty state in the Learner App Calendar with a message that describes the selected tab. This is a UI and localization change only: it must not change calendar queries, filtering, date selection, lesson/event visibility, or record data.

## Source Evidence

- Jira `LT-107665` and linked implementation epic `PBT-1290` define the required English and Japanese copy.
- `PBT-1290` is linked as the implementation work item and is currently `Ready for Development`; no merged PR or commit is linked to either Jira item.
- The local `erp-salesforce` checkout has no source match or commit for the required Learner App strings. The Salesforce static-resource bundles are not treated as source-of-truth for this Learner App text change.

## Acceptance Criteria

| AC | Selected tab | English empty-state message | Japanese empty-state message |
|---|---|---|---|
| AC-01 | All | There are no items scheduled for this date. | この日の予定はありません。 |
| AC-02 | Lesson | There are no lessons scheduled for this date. | この日の授業はありません。 |
| AC-03 | Event | There are no events scheduled for this date. | この日のイベントはありません。 |

## Business Rules

| ID | Rule |
|---|---|
| BR-01 | The empty state is selected from the active Calendar tab, not from the calendar date alone. |
| BR-02 | `All` is empty only when no visible lesson or event exists for the learner on the selected date. |
| BR-03 | `Lesson` can be empty while the same date has an Event; the message must still say `lessons`. |
| BR-04 | `Event` can be empty while the same date has a Lesson; the message must still say `events`. |
| BR-05 | Copy changes must not hide, create, or alter any calendar item. |
| BR-06 | Switching app language updates the empty-state string for the same selected tab and date. |

## Out Of Scope

- Salesforce Calendar, Back Office Calendar, Activity Event CRUD, event booking, and Live Lesson join behavior.
- Changes to event/lesson filtering, query endpoints, notification content, or access control.
