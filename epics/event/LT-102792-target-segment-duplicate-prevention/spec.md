---
ticket_id: LT-102792
ticket_url: https://manabie.atlassian.net/browse/LT-102792
title: Prevent selecting duplicate Target Location, Grade, School, and Course values within Target Segments
module: scheduling
bucket: event
status: Ready for QA
internal_uat_date: null
production_release_date: null
last_updated: 2026-09-18
---

# LT-102792: Prevent duplicate Target Segment values

## Summary

This ticket prevents duplicate Target Segment configuration on Event Master. Users must not be able to add the same Target Location, Target Grade, Target School, or Target Course multiple times. Duplicate values should be disabled or hidden in the selection UI, and backend/save validation must still reject duplicates if a stale UI, API, or parallel edit sends duplicate values.

Existing target-segment filtering behavior remains unchanged:

- AND is applied between different Target Segment dimensions.
- OR is applied within the same Target Segment dimension.

## Source Context

- Jira: `LT-102792`
- Related Event Target Segment epic: `LT-73558`
- Existing Qase suite: `Target Segment - Lookup Constraints & Eligibility Engine` (`suite_id=2612`)
- Existing partial related cases:
  - `PX-19067` to `PX-19072` cover positive add/save flows.
  - `PX-21530` and `PX-21555` cover duplicate Target Location prevention for a Renseikai-specific path.
  - No direct case was found for `LT-102792` or duplicate Target Grade/School/Course prevention.

## Acceptance Criteria

### AC 01 - Duplicate Target Segment values are not selectable

- AC 01.1: When a Target Location already exists on the Event Master, the same location is disabled or hidden in the next Target Location selection list.
- AC 01.2: When a Target Grade already exists, the same grade is disabled or hidden in the next Target Grade selection list.
- AC 01.3: When a Target School already exists, the same school is disabled or hidden in the next Target School selection list.
- AC 01.4: When a Target Course already exists, the same course is disabled or hidden in the next Target Course selection list.

### AC 02 - Save/API validation rejects duplicates

- AC 02.1: Saving duplicate Target Location values is blocked and no duplicate child record is created.
- AC 02.2: Saving duplicate Target Grade values is blocked and no duplicate child record is created.
- AC 02.3: Saving duplicate Target School values is blocked and no duplicate child record is created.
- AC 02.4: Saving duplicate Target Course values is blocked and no duplicate child record is created.

### AC 03 - Existing filtering behavior remains unchanged

- AC 03.1: OR matching within one segment dimension still works after duplicate prevention.
- AC 03.2: AND matching between configured dimensions still works after duplicate prevention.
- AC 03.3: Enrollment Status filtering for Target Location remains unchanged while duplicate Target Location values are prevented.

## Business Rules

| # | AC | Rule |
|---|---|---|
| 1 | AC 01.1-01.4 | Existing Target Segment values must not be selectable again in the same Event Master configuration. |
| 2 | AC 02.1-02.4 | Backend/save validation must reject duplicate Target Segment values even if duplicate payloads bypass the UI. |
| 3 | AC 03.1-03.2 | Duplicate prevention must not change AND between dimensions or OR within one dimension. |
| 4 | AC 03.3 | Target Location Enrollment Status filtering must continue to work with duplicate prevention. |

## Assumptions

- "Duplicate Target Location" means the same Target Location value should not be added again for the same Event Master.
- UI behavior may either disable existing values or hide them from the lookup/list; both satisfy the Jira acceptance criteria.
- Validation error text is not specified in Jira; tests assert blocking behavior and no duplicate child record rather than exact copy.

## Requirement Gaps

| Gap | Impact | Test Handling |
|---|---|---|
| Exact error message is not specified. | Automated test should not depend on copy that may change. | Assert a visible validation/error state and zero duplicate records. |
| Jira does not clarify whether duplicate Target Location with a different Enrollment Status is allowed. | Risk of ambiguous Location + Enrollment Status behavior. | Test uses same Target Location duplicate as blocked and keeps Enrollment Status filtering regression separate. |
| API endpoint name is implementation-specific. | Backend test may need to call Apex/REST/UI save depending on automation framework. | Steps describe stale UI/API duplicate payload generically and assert persisted records. |
