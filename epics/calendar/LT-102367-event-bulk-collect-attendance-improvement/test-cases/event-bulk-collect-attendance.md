# Test Cases: LT-102367 - Event Bulk Collect Attendance Improvement

## Suite: Event Bulk Collect Attendance

### [LT-102367] Event detail - Collect Attendance action - Opens participant bulk attendance dialog

**Description:** AC 01.1-01.2 - Scenario - Activity Event detail exposes Collect Attendance and opens the bulk dialog with loaded participants.

**Preconditions:**
- Logged in to BO Calendar as HQ or CM Staff with Activity Event detail access.
- Activity Event EVT-102367-A is visible on Calendar and has at least 3 Event Participants.
- Event Participant section is loaded in the Activity Event detail drawer.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Activity Event EVT-102367-A from Calendar. | Activity Event detail drawer opens. | event = EVT-102367-A |
| 2 | Locate the Event Participant section. | Event Participant section displays participant count and action menu. | participants >= 3 |
| 3 | Click Collect Attendance. | DialogCollectAttendanceEventParticipant opens. | action = Collect Attendance |
| 4 | Count participant rows in the dialog. | Dialog shows all loaded Event Participants from the detail section. | expected rows = loaded participants |

**Severity:** major  
**Priority:** high

---

### [LT-102367] Event attendance - Single participant Attend - Save updates status and clears note

**Description:** AC 01.3, AC 01.5, AC 01.7, AC 03.1-03.2 - State Transition - Attend can be selected and saved, and Attend clears the participant attendance note.

**Preconditions:**
- Activity Event EVT-102367-B has Participant A with Attendance Status blank and Attendance Note blank.
- Activity Event EVT-102367-B has Participant B with existing Attendance Status = Absent and Attendance Note = "Needs follow-up".

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Collect Attendance for EVT-102367-B. | Participant A and Participant B are listed. |  |
| 2 | Select Attend for Participant A. | Participant A row shows Attend selected without opening the remark dialog. | status = Attend |
| 3 | Select Attend for Participant B. | Participant B row changes to Attend and its note becomes empty in the dialog. | previous note = Needs follow-up |
| 4 | Click Save. | Save succeeds, dialog closes, and success snackbar is shown. | expected snackbar = Attendance marked successfully |
| 5 | Refresh Activity Event detail and inspect Participants A and B. | Both participants show Attend; Participant B attendance note is empty. | expected API fields = Attendance_Status__c Attend; Attendance_Note__c empty |

**Severity:** critical  
**Priority:** high

---

### [LT-102367] Event attendance - Single participant Absent with remark - Save updates status and note

**Description:** AC 01.3-01.4, AC 01.7, AC 03.1-03.2 - CRUD - Absent opens remark dialog and persists note through Event Participant REST upsert.

**Preconditions:**
- Activity Event EVT-102367-C has Participant A with Attendance Status blank.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Collect Attendance for EVT-102367-C. | Participant A is listed with no attendance status selected. |  |
| 2 | Select Absent for Participant A. | Remark dialog opens with title Absent. | status = Absent |
| 3 | Enter remark and save the remark dialog. | Participant A row shows Absent and displays the entered remark. | remark = "Sick leave" |
| 4 | Click Save in the Collect Attendance dialog. | FE submits participant Id, Attendance_Status__c, and Attendance_Note__c; API returns success. | expected payload row = Id + Absent + Sick leave |
| 5 | Refresh Activity Event detail. | Participant A shows Absent with the saved remark. | expected readback = Absent / Sick leave |

**Severity:** critical  
**Priority:** high

---

### [LT-102367] Event attendance - Cancel Absent remark dialog - Row remains unchanged

**Description:** AC 01.4 - Negative - Cancelling the Absent remark dialog must not apply a partial attendance status or note.

**Preconditions:**
- Activity Event EVT-102367-D has Participant A with Attendance Status blank and no note.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Collect Attendance for EVT-102367-D. | Participant A is listed with no status. |  |
| 2 | Select Absent for Participant A. | Remark dialog opens. |  |
| 3 | Enter a temporary remark and click Cancel. | Remark dialog closes. | temporary remark = "Do not save" |
| 4 | Inspect Participant A row. | Participant A still has no attendance status and no attendance note. | expected status = blank; expected note = blank |
| 5 | Click Save without selecting any other participant. | Save is blocked by empty attendance validation. | expected error = collectAttendanceEmptyParticipant |

**Severity:** major  
**Priority:** high

---

### [LT-102367] Event attendance - Edit remark icon - Disabled until status exists

**Description:** AC 01.6 - Component - The edit remark action cannot be used before a participant has attendance status.

**Preconditions:**
- Activity Event EVT-102367-E has Participant A with blank attendance status.
- Participant B has Attendance Status = Absent and Attendance Note = "Original note".

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Collect Attendance for EVT-102367-E. | Participant rows are visible. |  |
| 2 | Inspect Participant A edit icon. | Edit icon is disabled. | Participant A status = blank |
| 3 | Inspect Participant B edit icon. | Edit icon is enabled. | Participant B status = Absent |
| 4 | Click Participant B edit icon. | Remark dialog opens with existing note prefilled. | expected note = Original note |

**Severity:** major  
**Priority:** medium

---

### [LT-102367] Event attendance - Edit existing Absent remark - Saved note replaces previous note

**Description:** AC 01.4, AC 01.7 - State Transition - Editing an existing Absent remark pre-fills and persists the replacement note.

**Preconditions:**
- Activity Event EVT-102367-F has Participant A with Attendance Status = Absent and Attendance Note = "Original note".

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Collect Attendance for EVT-102367-F. | Participant A row shows Absent and "Original note". |  |
| 2 | Click Participant A edit icon. | Remark dialog opens and pre-fills "Original note". |  |
| 3 | Replace the note and save the remark dialog. | Participant A row shows Absent and the replacement note. | new note = "Updated note" |
| 4 | Click Save and refresh Activity Event detail. | Participant A readback shows Absent and "Updated note". | expected final note = Updated note |

**Severity:** major  
**Priority:** high

---

### [LT-102367] Event attendance - Mark all as Attend - Only empty rows are filled

**Description:** AC 02.1, AC 02.3 - Decision Table - Mark all as Attend does not overwrite existing participant statuses.

**Preconditions:**
- Activity Event EVT-102367-G has Participant A blank, Participant B = Absent with note, Participant C = Attend.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Collect Attendance for EVT-102367-G. | Three participants are shown with prepared statuses. | A blank; B Absent; C Attend |
| 2 | Click Mark all as Attend. | Only Participant A changes to Attend. |  |
| 3 | Inspect Participant B and C rows. | Participant B remains Absent with its note; Participant C remains Attend. | existing statuses must not overwrite |
| 4 | Save and refresh Activity Event detail. | Readback keeps A Attend, B Absent, C Attend. | expected final = A Attend / B Absent / C Attend |

**Severity:** critical  
**Priority:** high

---

### [LT-102367] Event attendance - Mark all as Absent - Only empty rows are filled without forcing remarks

**Description:** AC 02.2-02.3 - Decision Table - Mark all as Absent applies only to empty rows and does not force remark entry.

**Preconditions:**
- Activity Event EVT-102367-H has Participant A blank, Participant B = Attend, Participant C = Absent with note.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Collect Attendance for EVT-102367-H. | Prepared participant rows are displayed. | A blank; B Attend; C Absent |
| 2 | Click Mark all as Absent. | Only Participant A changes to Absent; no remark dialog opens for mark-all. |  |
| 3 | Inspect existing rows. | Participant B remains Attend; Participant C remains Absent with original note. | no overwrite |
| 4 | Save and refresh Activity Event detail. | Participant A is saved as Absent with empty note; existing rows are unchanged. | expected A note = empty |

**Severity:** critical  
**Priority:** high

---

### [LT-102367] Event attendance - Save with no selected participant status - Validation error shown

**Description:** AC 02.4 - Negative - Save is blocked when every event participant attendance status is blank.

**Preconditions:**
- Activity Event EVT-102367-I has at least one Event Participant and all attendance statuses are blank.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Collect Attendance for EVT-102367-I. | All participant rows are blank. |  |
| 2 | Click Save without selecting any status. | Dialog remains open and no API request is sent. |  |
| 3 | Observe snackbar. | Error message `There is no participant to collect attendance` is shown. | i18n key = collectAttendanceEmptyParticipant |

**Severity:** major  
**Priority:** high

---

### [LT-102367] Event attendance - API failure - Dialog remains open and generic error appears

**Description:** AC 02.5 - Negative - API failure is visible to the user and does not close the dialog.

**Preconditions:**
- Activity Event EVT-102367-J has Participant A available.
- Backend/API can be mocked or forced to return an error for collect attendance.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Collect Attendance for EVT-102367-J. | Dialog opens. |  |
| 2 | Select Attend for Participant A. | Participant A row shows Attend. |  |
| 3 | Trigger Save while API returns error. | Dialog remains open and Save becomes available again after request completes. | API = error |
| 4 | Observe snackbar. | Generic error snackbar is shown. | expected key = ra.manabie-error.unknown |
| 5 | Refresh Activity Event detail. | Participant A attendance is not changed by the failed request. | expected DB unchanged |

**Severity:** critical  
**Priority:** high

---

### [LT-102367] Event Participant API - Empty payload - Backend rejects request

**Description:** AC 03.3 - API Negative - Backend prevents empty event participant upsert.

**Preconditions:**
- User/API token has access to Salesforce Event Participant REST API.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Send POST `/services/apexrest/MANAERP/eventParticipants/v1/collectAttendance` with an empty eventParticipants list. | Request is rejected by backend guard. | body = `{ "eventParticipants": [] }` |
| 2 | Send POST with null eventParticipants. | Request is rejected by backend guard. | body = `{ "eventParticipants": null }` |
| 3 | Query Event_Participant__c records from the fixture. | No participant attendance value is changed. | expected writes = 0 |

**Severity:** critical  
**Priority:** high

---

### [LT-102367] BO Calendar - Mark Attendance bulk action - Feature flag and location gating

**Description:** AC 04.1 - Feature Flag Matrix - Adjacent BO Calendar bulk attendance action remains gated correctly.

**Preconditions:**
- BO Calendar is running in Back Office context, not direct SF context.
- Test accounts can toggle `Calendar_IndividualCalendar_BulkUpdateAttendance`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open BO Calendar with feature flag ON and selected location. | Mark Attendance action is visible and enabled. | flag = ON; locationId present |
| 2 | Clear selected location. | Mark Attendance action remains visible but is disabled. | locationId missing |
| 3 | Turn feature flag OFF and reload BO Calendar. | Mark Attendance action is hidden. | flag = OFF |
| 4 | Open direct SF Calendar context. | Mark Attendance BO bulk action is not shown. | VITE_SF = true |

**Severity:** major  
**Priority:** medium

---

### [LT-102367] Lesson collect attendance - Attendance response pre-fills status

**Description:** AC 04.2 - Regression - Student-session collect attendance derives empty status from attendance response text.

**Preconditions:**
- Published lesson LES-102367-A has Student A with Attendance_Status__c blank and Attendance_Response__c containing a known Attend/Absent/Late/Leave Early label.
- Lesson detail Collect Attendance action is available.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Lesson detail from BO Calendar. | Lesson detail drawer opens. | lesson = LES-102367-A |
| 2 | Click Collect Attendance. | Collect Attendance dialog opens. |  |
| 3 | Inspect Student A attendance radio state. | Status is prefilled from Attendance_Response__c when Attendance_Status__c is blank. | response contains status label |
| 4 | Save without changing Student A. | Save succeeds if all rows have derived or explicit status. | expected no validation error |

**Severity:** major  
**Priority:** high

---

### [LT-102367] Lesson collect attendance - Missing status in any row blocks save

**Description:** AC 04.3 - Negative - Lesson attendance dialog requires every student session row to have attendance status.

**Preconditions:**
- Published lesson LES-102367-B has Student A with Attend and Student B with blank Attendance_Status__c and no parseable Attendance_Response__c.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Open Lesson detail Collect Attendance dialog. | Student A and Student B are listed. |  |
| 2 | Leave Student B status blank and click Save. | Save is blocked; no bulk update request is submitted. | Student B status = blank |
| 3 | Select a status for Student B. | Save button becomes available. |  |
| 4 | Click Save. | Save succeeds. | expected all rows have status |

**Severity:** major  
**Priority:** high

---

### [LT-102367] Lesson collect attendance payload - Status-dependent fields are sent correctly

**Description:** AC 04.4 - Contract - FE payload includes reason, notice, reallocate flag, and note according to status.

**Preconditions:**
- Published lesson LES-102367-C has three student sessions.
- Network request can be inspected or mocked.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Set Student A to Attend with a note. | Payload row has status Attend, reallocateFlag false, note included, and no attendanceReason/attendanceNotice. | Student A = Attend |
| 2 | Set Student B to Late with reason and note. | Payload row has attendanceReason and note; attendanceNotice is omitted; reallocateFlag false. | Student B = Late |
| 3 | Set Student C to Absent with notice, reason, note, and reallocate ON. | Payload row has attendanceNotice, attendanceReason, attendanceNote, and reallocateFlag true. | Student C = Absent |
| 4 | Save and inspect request body. | Request body contains exactly one bulkUpdateStudentSessionAttendanceItems entry per student session with the expected fields. | endpoint = studentSessions/v1 PUT |

**Severity:** critical  
**Priority:** high

---

### [LT-102367] Student Session API - Bulk update marks and unflags reallocation

**Description:** AC 04.5 - Backend Regression - Bulk update preserves reallocation side effects for multiple student sessions.

**Preconditions:**
- Published lesson LES-102367-D has Student Session A with Reallocate_Flag__c = false and Student Session B with Reallocate_Flag__c = true.
- Reallocation records can be queried after save.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | Submit bulk update where Student Session A becomes Absent with reallocateFlag true. | Backend marks Student Session A for reallocation. | A old flag=false; new status=Absent; new flag=true |
| 2 | Submit Student Session B with reallocateFlag false. | Backend unflags Student Session B reallocation. | B old flag=true; new flag=false |
| 3 | Query both Student_Sessions__c records. | Attendance fields and Reallocate_Flag__c match submitted values. | expected A flag=true; B flag=false |
| 4 | Query related reallocation data. | Reallocation side effects are created/removed consistently with the flag changes. | expected mark/unflag applied |

**Severity:** critical  
**Priority:** high
