# Test Coverage: LT-110579 - Bulk Publish Lesson timezone boundary

## Scope

Validate that SF Lesson Calendar Bulk Publish uses Salesforce local-date boundaries when filtering lessons by Start Date and End Date. The main regression risk is silent data corruption: lessons early in the selected local day can be missed, and lessons early in the next local day can be published incorrectly.

## Requirement Mapping

| ID | Requirement | Risk | Coverage |
|---|---|---|---|
| R1 | Date range is converted using Salesforce timezone before lesson filtering | Critical | TC-01, TC-02, TC-03, TC-04 |
| R2 | Single local date publishes only lessons whose start datetime belongs to that local date | Critical | TC-01, TC-02, TC-03 |
| R3 | Lessons from previous or next Salesforce local date are not included | Critical | TC-01, TC-02, TC-03, TC-04 |
| R4 | Existing location, selected-student, and Draft-only scope rules remain unchanged | High | TC-01, TC-02, TC-04 |

## Test Design

| Case ID | Title | Technique | Depth | Priority |
|---|---|---|---|---|
| TC-01 | Bulk Publish Lesson - Single Local Date GMT+9 - All Lessons Within Salesforce Date Are Published | Boundary Value Analysis | Deep | High |
| TC-02 | Bulk Publish Lesson - Single Local Date GMT+9 - Lessons On Next Salesforce Date Remain Draft | Boundary Value Analysis + Negative Testing | Deep | High |
| TC-03 | Bulk Publish Lesson - Exact GMT+9 Boundaries - Lower Inclusive And Upper Exclusive Rule Applied | Boundary Value Analysis | Deep | High |
| TC-04 | Bulk Publish Lesson - Selected Students GMT+9 Range - Student And Timezone Scope Both Applied | Decision Table + Boundary Value Analysis | Deep | High |

## Boundary Data

| Salesforce local time | UTC stored time | Expected when selected date is 2030-09-19 |
|---|---|---|
| 2030-09-18 23:59 GMT+9 | 2030-09-18 14:59 UTC | Excluded |
| 2030-09-19 00:00 GMT+9 | 2030-09-18 15:00 UTC | Included |
| 2030-09-19 08:59 GMT+9 | 2030-09-18 23:59 UTC | Included |
| 2030-09-19 23:59 GMT+9 | 2030-09-19 14:59 UTC | Included |
| 2030-09-20 00:00 GMT+9 | 2030-09-19 15:00 UTC | Excluded |
| 2030-09-20 07:59 GMT+9 | 2030-09-19 22:59 UTC | Excluded |

## Regression Notes

- Bulk Publish remains asynchronous; cases must refresh Calendar after job completion before asserting lesson status.
- Only Draft lessons are eligible for Draft to Published transition.
- Location scope remains active for all-student publish.
- When Apply to selected students is activated, only lessons for selected students at the locked Calendar location are eligible.

## Suggested Test Suite Structure

| Suite | Parent Suite | Purpose |
|---|---|---|
| Bulk Publish Lesson - Salesforce Timezone Boundary | Calendar lesson | Core SF regression suite for LT-110579 GMT+9 date-boundary filtering |
