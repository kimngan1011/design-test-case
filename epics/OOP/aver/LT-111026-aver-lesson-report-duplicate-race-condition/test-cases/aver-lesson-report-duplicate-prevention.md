# Test Cases: LT-111026 - Aver Lesson Report duplicate prevention

## Suite: [Aver] Lesson Report Duplicate Prevention

### [Aver] Lesson Report creation - Same staff two browser tabs - Reuse existing active report

**Description:** AC 01.1 / AC 01.2 / AC 01.3 - Race-condition regression - Opening the same lesson in two tabs and submitting Add New Aver Lesson Report twice creates only one active report.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce for the Aver tenant.
- Lesson `LSN-111026-01` exists and has no active Aver Lesson Report.
- Browser Tab 1 and Tab 2 both open the Lesson Report entry point for `LSN-111026-01`.
- QA can verify `Lesson_Report__c` records for the lesson from Salesforce list/API/query.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | In Tab 1, click `Add New Aver Lesson Report`. | The create flow starts for `LSN-111026-01`. | tab = 1 |
| 2 | Without refreshing Tab 2, click `Add New Aver Lesson Report` in Tab 2 within the same test window. | The second create request is accepted for processing or resolves to an existing report without an unhandled error. | tab = 2 |
| 3 | Save or complete both flows. | Both tabs resolve to the same Aver Lesson Report ID. | expected = same_report_id |
| 4 | Query active Aver Lesson Reports for `LSN-111026-01`. | Exactly one active `Lesson_Report__c` exists for the lesson. | active_report_count = 1 |

### [Aver] Lesson Report creation - Two staff create same lesson report concurrently - Single active report

**Description:** AC 01.1 / AC 01.2 / AC 01.3 - Concurrency - Two staff users creating the same Aver Lesson Report at nearly the same time must not create duplicates.

**Preconditions:**
- HQ Staff A and CM Staff B are logged in to Salesforce for the Aver tenant.
- Lesson `LSN-111026-02` exists and has no active Aver Lesson Report.
- Both staff can access the lesson report creation entry point.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Staff A opens `LSN-111026-02` and clicks `Add New Aver Lesson Report`. | Staff A starts report creation. | user = staff_a |
| 2 | Staff B clicks `Add New Aver Lesson Report` for the same lesson at nearly the same time. | Staff B's request does not create an independent active report. | user = staff_b |
| 3 | Complete both create/save flows. | Both users are linked to the same existing or newly-created report record. | expected = one_shared_report |
| 4 | Query active Aver Lesson Reports for `LSN-111026-02`. | Exactly one active report exists; no second Draft report is created. | active_report_count = 1 |

### [Aver] Lesson Report creation - Existing active Draft report - Add action opens existing report

**Description:** AC 02.1 - State transition - When an active Draft report already exists, Add New Aver Lesson Report reuses it instead of creating a duplicate.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce for the Aver tenant.
- Lesson `LSN-111026-03` has active Draft Aver Lesson Report `ALR-111026-DRAFT`.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the Lesson Report entry point for `LSN-111026-03`. | The page/card recognizes the lesson report context. | lesson = LSN-111026-03 |
| 2 | Click `Add New Aver Lesson Report`. | The system opens or returns `ALR-111026-DRAFT`. | existing_report = ALR-111026-DRAFT |
| 3 | Query active Aver Lesson Reports for `LSN-111026-03`. | Only `ALR-111026-DRAFT` exists as active; no new report is inserted. | active_report_count = 1 |

### [Aver] Lesson Report creation - Existing active Published report - No new Draft report

**Description:** AC 02.2 / AC 03.1 - Regression - Existing Published report must be reused and must not be hidden by a new Draft duplicate.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce for the Aver tenant.
- Lesson `LSN-111026-04` has active Published Aver Lesson Report `ALR-111026-PUBLISHED`.
- Lesson List currently displays `Published` for `LSN-111026-04`.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open `LSN-111026-04` and click `Add New Aver Lesson Report`. | The system opens or returns `ALR-111026-PUBLISHED`, or blocks new creation by reusing the active report. | existing_status = Published |
| 2 | Refresh Lesson List and the Lesson Report detail page. | Both surfaces still show the same Published report status. | expected_status = Published |
| 3 | Query active Aver Lesson Reports for `LSN-111026-04`. | Exactly one active report exists and no new Draft report is created. | forbidden_status = duplicate Draft |

### [Aver] Lesson Report creation - No active report exists - Creates one active report

**Description:** AC 02.3 - Boundary - The duplicate-prevention check must still allow one new Aver Lesson Report when no active report exists.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce for the Aver tenant.
- Lesson `LSN-111026-05` has no active Aver Lesson Report.
- Any old report for this lesson is inactive/deleted according to the product data model.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open `LSN-111026-05` and click `Add New Aver Lesson Report`. | A new Aver Lesson Report creation flow starts. | active_report_before = 0 |
| 2 | Save the report. | The report is saved successfully. | action = save |
| 3 | Query active Aver Lesson Reports for `LSN-111026-05`. | Exactly one active report exists for the lesson. | active_report_after = 1 |

### [Aver] Lesson Report status - Publish after duplicate-prevention flow - List/card/detail remain consistent

**Description:** AC 03.1 - End-to-end regression - After the duplicate-prevention path, publishing the single report keeps Lesson List, card, and detail status consistent.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce for the Aver tenant.
- Lesson `LSN-111026-06` has one active Draft Aver Lesson Report created through a duplicate-prevention scenario.
- The report is publishable.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the active Draft report for `LSN-111026-06`. | The Draft report opens with a single report ID. | initial_status = Draft |
| 2 | Publish the report. | The report status changes to Published. | expected_status = Published |
| 3 | Refresh Lesson List, the Lesson Report card, and Lesson Report detail. | All three surfaces resolve to the same report ID and show Published. | surfaces = list, card, detail |
| 4 | Query active Aver Lesson Reports for `LSN-111026-06`. | Exactly one active report exists. | active_report_count = 1 |

### [Aver] Lesson Report data integrity - Details and Student Session remain linked to single report

**Description:** AC 03.2 / AC 03.3 - Data integrity - Duplicate-prevention must not split details or Student Session references across report records.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce for the Aver tenant.
- Lesson `LSN-111026-07` has students and report details available for Aver Lesson Report creation.
- A concurrent create or rapid retry scenario has just been executed for this lesson.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Query the active Aver Lesson Report for `LSN-111026-07`. | Exactly one active report ID is returned. | active_report_count = 1 |
| 2 | Query `Lesson_Report_Detail__c` records for the lesson/report. | All active detail records reference the single active report ID. | expected = one_parent_report |
| 3 | Query `Student_Sessions__c.Lesson_Report__c` for students in the lesson. | Student Session references point to the same report ID where the product flow expects a lesson report link. | expected = no_split_reference |
| 4 | Check for orphan duplicate reports/details. | No extra active report and no orphan active detail record exists. | expected_orphan_count = 0 |

### [Aver] Lesson Report creation - Rapid double-click/retry - Backend remains idempotent

**Description:** AC 01.1 / AC 03.3 - Negative regression - Rapid repeated user action or duplicate network submission must not create multiple active reports.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce for the Aver tenant.
- Lesson `LSN-111026-08` has no active Aver Lesson Report.
- The test can simulate rapid double-click, retry, or duplicate API calls for the same create action.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Trigger `Add New Aver Lesson Report` twice rapidly for `LSN-111026-08`. | The UI may disable the second click, or the backend may receive duplicate requests. | trigger = rapid_retry |
| 2 | Wait for both requests to settle. | No unhandled error is shown; at most one report ID is returned as active. | expected = idempotent_result |
| 3 | Query active Aver Lesson Reports for `LSN-111026-08`. | Exactly one active report exists for the lesson. | active_report_count = 1 |
| 4 | Refresh the page and click `Add New Aver Lesson Report` again. | The same existing report opens or is returned. | expected = same_report_id |
