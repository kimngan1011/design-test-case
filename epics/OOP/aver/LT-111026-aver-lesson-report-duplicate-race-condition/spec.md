---
ticket_id: LT-111026
ticket_url: https://manabie.atlassian.net/browse/LT-111026
title: Prevent duplicate Aver Lesson Report creation via race condition
module: scheduling
bucket: OOP/aver
status: Ready for QA
internal_uat_date: null
production_release_date: null
last_updated: 2026-09-18
---

# LT-111026: Prevent duplicate Aver Lesson Report creation via race condition

## Summary

This bug fixes duplicate Aver Lesson Report creation when the same lesson is opened and submitted in parallel. The incident showed two active `Lesson_Report__c` records for one lesson, created five seconds apart, which caused the Lesson Report detail to show the published report while Lesson List picked the second draft report and displayed the wrong status.

The fix is backend-side idempotency: before creating a new Aver Lesson Report for a lesson, the system must check whether an active report already exists. If an active report exists, the create flow must return or reuse that existing report instead of inserting another `Lesson_Report__c`.

## Source Context

- Jira: `LT-111026`
- Incident context: `MANACS-2608`
- Related epic: `LT-105354` - Q3 Aver lesson report improvement items
- Slack thread referenced in Jira confirmed two root scenarios:
  - Two staff click `Add New Aver Lesson Report` for the same lesson at nearly the same time.
  - One staff opens the same Lesson Report in two browser tabs and clicks Add/Save in both.
- Local Salesforce code references:
  - `packages/lesson/main/default/lwc/cardLessonReport/cardLessonReport.js`
  - `packages/lesson/main/default/classes/LessonReportHandler.cls`
  - `packages/lesson/main/default/classes/repository/LessonReportRepo.cls`

## Acceptance Criteria

### AC 01 - Duplicate prevention for parallel creation

- AC 01.1: When two create requests are made for the same Aver lesson at nearly the same time, only one active Aver Lesson Report is created.
- AC 01.2: The later request returns or reuses the existing active report instead of creating a second active report.
- AC 01.3: The duplicate prevention works for both same-user multi-tab and different-user concurrent scenarios.

### AC 02 - Existing active report reuse

- AC 02.1: If the lesson already has an active Draft Aver Lesson Report, clicking `Add New Aver Lesson Report` opens or returns that same report.
- AC 02.2: If the lesson already has an active Published Aver Lesson Report, clicking `Add New Aver Lesson Report` does not create a new Draft report.
- AC 02.3: If no active Aver Lesson Report exists for the lesson, the system can create one new active report.

### AC 03 - Status and relationship consistency

- AC 03.1: Lesson List, Lesson Report card, and Lesson Report detail all resolve to the same report and status after the duplicate-prevention flow.
- AC 03.2: Student Session and Lesson Report Detail records remain linked to the single reused or created report.
- AC 03.3: No orphan or inactive duplicate report is introduced by rapid Add/Save retries.

## Business Rules

| # | AC | Rule |
|---|---|---|
| 1 | AC 01.1-01.3 | Aver Lesson Report creation for one lesson must be idempotent under parallel requests. |
| 2 | AC 02.1-02.2 | Existing active Aver Lesson Report wins over a new create attempt, regardless of Draft or Published status. |
| 3 | AC 02.3 | A new Aver Lesson Report is created only when no active report exists for the lesson. |
| 4 | AC 03.1 | List/card/detail status must be derived from the same single report record. |
| 5 | AC 03.2-03.3 | Detail and Student Session relationships must not be split across duplicate reports. |

## Assumptions

- "Active report" follows the Salesforce data model used by the implementation. Tests assert active vs. inactive/deleted behavior from the user-visible and queryable record state.
- The fix is expected from backend logic, so UI double-click prevention alone is not sufficient.
- The system may show an existing report, redirect to it, or return its ID from the create request. Any of these are acceptable if no duplicate active report is created.
- Optimistic locking notifications for parallel edit/save are out of scope unless they are implemented as an add-on; this ticket focuses on duplicate creation prevention.

## Requirement Gaps

| Gap | Impact | Test Handling |
|---|---|---|
| Exact UI response for the reused existing report is not specified. | Test cannot require a specific toast or navigation label. | Assert the stable outcome: one active report and both users/tabs resolve to the same report ID. |
| The exact active/inactive flag is not visible from Jira. | Boundary tests may depend on object fields. | Write the case in terms of product data model state: active existing report vs. no active report. |
| Exact concurrency harness is not specified. | Manual QA may not reproduce true simultaneous requests consistently. | Include both browser-tab reproduction and API/automation-level parallel request validation for automation reuse. |
