# Test Cases: LT-101737 Event Participant and Staff CSV import

## Suite: Event Participant and Staff CSV Import

### [LT-101737] Event Master list view - Import mass actions open correct Data Importer objects

**Description:** AC 01 - Component and Navigation - Import Activity Event, Import Participant, and Import Event Staff are available as list-view mass actions and do not require selected rows.

**Preconditions:**
- User has Salesforce access to Event Master list view.
- User has permissions for Activity Event create, Add Master Participant, and Add Master Staff.

| Step | Action | Expected Result | Data |
| --- | --- | --- | --- |
| 1 | Open Event Master list view. | List view loads with Event Master rows. | object = Event_Master__c |
| 2 | Open list view actions without selecting any row. | Three actions are visible: Import Activity Event, Import Participant, Import Event Staff. | requireRowSelection = false |
| 3 | Click Import Activity Event. | Data Importer opens with Activity Event object selected. | objectSelection = MANAERP__Activity_Event__c |
| 4 | Return and click Import Participant. | Data Importer opens with Event Participant object selected. | objectSelection = MANAERP__Event_Participant__c |
| 5 | Return and click Import Event Staff. | Data Importer opens with Event Staff object selected. | objectSelection = MANAERP__Event_Staff__c |

### [LT-101737] Event Master record page - Permission-specific import buttons are visible

**Description:** AC 01 - Permission Matrix - Record page import buttons follow custom permission visibility rules and route to the correct object.

**Preconditions:**
- Event Master EM-101737-A exists.
- Three test users exist with different custom permissions: Create Activity Event only, Add Master Participant only, Add Master Staff only.

| Step | Action | Expected Result | Data |
| --- | --- | --- | --- |
| 1 | Login as user with Create Activity Event only and open EM-101737-A. | Only Import Activity Event is visible among the three import buttons. | permission = Create_Activity_Event |
| 2 | Click Import Activity Event. | Data Importer opens for Activity Event. | objectSelection = MANAERP__Activity_Event__c |
| 3 | Login as user with Add Master Participant only and open EM-101737-A. | Only Import Participant is visible among the three import buttons. | permission = Add_Master_Participant |
| 4 | Click Import Participant. | Data Importer opens for Event Participant. | objectSelection = MANAERP__Event_Participant__c |
| 5 | Login as user with Add Master Staff only and open EM-101737-A. | Only Import Event Staff is visible among the three import buttons. | permission = Add_Master_Staff |
| 6 | Click Import Event Staff. | Data Importer opens for Event Staff. | objectSelection = MANAERP__Event_Staff__c |

### [LT-101737] Event Master import buttons - Japanese labels are displayed

**Description:** AC 01 - Localization - Japanese users see the translated import button labels.

**Preconditions:**
- User locale is Japanese.
- User can access Event Master list and record page import actions.

| Step | Action | Expected Result | Data |
| --- | --- | --- | --- |
| 1 | Open Event Master list view in Japanese locale. | Import buttons display Japanese labels. | locale = ja |
| 2 | Verify Activity Event import label. | Label is `アクティビティイベントのインポート`. | button = Import_Activity_Event_List_Button |
| 3 | Verify Event Staff import label. | Label is `イベントスタッフのインポート`. | button = Import_Event_Staff_List_Button |
| 4 | Verify Event Participant import label. | Label is `イベント参加者のインポート`. | button = Import_Participant_List_Button |
| 5 | Open an Event Master record page. | Record-level import buttons are still understandable and route correctly. | record = EM-101737-A |

### [LT-101737] Activity Event CSV import - Valid rows create Activity Events under Event Master

**Description:** AC 02 - CRUD - Data Importer creates multiple Activity Events with required fields and correct Event Master linkage.

**Preconditions:**
- Event Master EM-101737-B exists.
- Location LOC-101737-A exists.
- User opens Data Importer for Activity Event from Event Master import button.

| Step | Action | Expected Result | Data |
| --- | --- | --- | --- |
| 1 | Upload Activity Event CSV with two valid rows. | CSV is accepted for mapping. | rows = Win AE, Loss AE |
| 2 | Map Event Master, Location, Start Date Time, End Date Time, Allow Response, Send To. | All required columns are mapped. | object = Activity_Event__c |
| 3 | Run import. | Import finishes successfully with 2 created rows. | expected created = 2 |
| 4 | Open EM-101737-B related Activity Events. | Both Activity Events are listed under EM-101737-B. | master = EM-101737-B |
| 5 | Open each Activity Event detail. | Required fields match CSV values. | status = Published |

### [LT-101737] Activity Event CSV import - Salesforce ID updates existing Activity Event without duplicate

**Description:** AC 02 - Upsert - Import by Salesforce ID overwrites an existing Activity Event instead of creating a duplicate.

**Preconditions:**
- Activity Event AE-101737-C exists under EM-101737-C.
- Salesforce ID for AE-101737-C is known.

| Step | Action | Expected Result | Data |
| --- | --- | --- | --- |
| 1 | Export or capture AE-101737-C Salesforce ID. | Salesforce ID is available for update CSV. | id = AE-101737-C.Id |
| 2 | Upload Activity Event CSV containing that Salesforce ID and updated date/description. | CSV maps to update mode. | changed fields = End Date Time, Description |
| 3 | Run import. | Import finishes with 1 updated row and 0 created rows. | expected updated = 1 |
| 4 | Refresh AE-101737-C. | New date/description values are shown. | no duplicate |
| 5 | Check EM-101737-C related Activity Events. | Only one record exists for that Activity Event. | duplicate count = 0 |

### [LT-101737] Activity Event CSV import - Invalid rows are rejected row-by-row

**Description:** AC 02 - Validation - Invalid Activity Event rows do not create corrupt records and valid rows in the same file still import.

**Preconditions:**
- Event Master EM-101737-D and Location LOC-101737-D exist.
- Data Importer is open for Activity Event.

| Step | Action | Expected Result | Data |
| --- | --- | --- | --- |
| 1 | Upload mixed CSV with one valid row and invalid rows. | File is accepted for processing. | invalid = missing Location, Start > End, capacity 0 |
| 2 | Run import. | Import result shows partial success. | valid rows = 1 |
| 3 | Review failed rows. | Each invalid row shows field-level failure reason. | required/date/capacity validation |
| 4 | Open EM-101737-D related Activity Events. | Only the valid row was created. | created = 1 |
| 5 | Verify no Activity Event exists for invalid rows. | Invalid rows did not create records. | corrupt data = none |

### [LT-101737] Event Participant CSV import - Valid rows create assigned participants

**Description:** AC 03 - CRUD - Event Participant import creates participant records linked to Student, Event Master, and Activity Event.

**Preconditions:**
- Event Master EM-101737-E and Activity Event AE-101737-E exist.
- Students STU-101737-A and STU-101737-B exist.
- Data Importer is open for Event Participant.

| Step | Action | Expected Result | Data |
| --- | --- | --- | --- |
| 1 | Upload Event Participant CSV for two students. | CSV maps Student, Event Master, Activity Event, Reserved By, Response. | students = A, B |
| 2 | Run import. | Import finishes with 2 created participant rows. | expected created = 2 |
| 3 | Open EM-101737-E Master Participant list. | Both students appear under Event Master participants. | master = EM-101737-E |
| 4 | Open AE-101737-E Event Participant related list. | Both students appear under Activity Event participants. | activity = AE-101737-E |
| 5 | Open each Event Participant detail. | Student, Event Master, Activity Event, Reserved By and Response match CSV. | object = Event_Participant__c |

### [LT-101737] Event Participant daily upsert - Existing participant overwritten by Salesforce ID

**Description:** AC 03 - Upsert - Daily application import updates an existing Event Participant and does not create duplicates.

**Preconditions:**
- Event Participant EP-101737-F exists for Student A under EM-101737-F.
- EP-101737-F Salesforce ID is known.
- Activity Events AE-101737-F1 and AE-101737-F2 exist.

| Step | Action | Expected Result | Data |
| --- | --- | --- | --- |
| 1 | Prepare update CSV with EP-101737-F Salesforce ID and Activity Event = AE-101737-F2. | CSV represents a changed preference/assignment. | original activity = AE-101737-F1 |
| 2 | Run Event Participant import. | Import finishes with 1 updated row. | expected updated = 1 |
| 3 | Open EP-101737-F. | Activity Event and response fields reflect the latest CSV. | latest wins |
| 4 | Search Event Participants for Student A and EM-101737-F. | Only one participant record exists. | duplicate count = 0 |
| 5 | Re-run the same CSV. | Record remains one row and values are unchanged. | idempotent re-run |

### [LT-101737] Event Participant lottery move - CSV update moves participant from loss AE to win AE

**Description:** AC 03 - State Transition - Staff can move lottery winners from a loss Activity Event to a win Activity Event by CSV update.

**Preconditions:**
- Event Master EM-101737-G has AE-LOSS and AE-WIN.
- Event Participant EP-101737-G exists in AE-LOSS.
- EP-101737-G Salesforce ID is known.

| Step | Action | Expected Result | Data |
| --- | --- | --- | --- |
| 1 | Upload Event Participant CSV with EP-101737-G Salesforce ID and Activity Event = AE-WIN. | Update row is accepted. | old activity = AE-LOSS |
| 2 | Run import. | Import finishes with 1 updated row. | expected updated = 1 |
| 3 | Open AE-WIN Event Participant list. | Student appears in AE-WIN. | new activity = AE-WIN |
| 4 | Open AE-LOSS Event Participant list. | Student no longer appears as assigned to AE-LOSS. | old activity removed |
| 5 | Open EP-101737-G detail. | Same Salesforce ID is retained with updated Activity Event. | no new participant |

### [LT-101737] Event Participant CSV import - Invalid references are rejected and valid rows still import

**Description:** AC 03 - Negative and Partial Success - Bad Student, Event Master, or Activity Event references fail row-by-row.

**Preconditions:**
- One valid Student, Event Master, and Activity Event exist.
- Data Importer is open for Event Participant.

| Step | Action | Expected Result | Data |
| --- | --- | --- | --- |
| 1 | Upload mixed Event Participant CSV. | CSV contains one valid row and three invalid reference rows. | invalid = unknown student/master/activity |
| 2 | Run import. | Import result shows partial success. | valid rows = 1 |
| 3 | Review failed rows. | Each invalid reference row is rejected with an error. | lookup errors |
| 4 | Open Event Master participant list. | Only the valid participant is shown. | created = 1 |
| 5 | Search by invalid students/activities. | No invalid participant records were created. | corrupt data = none |

### [LT-101737] Event Staff CSV import - Valid rows create assigned staff

**Description:** AC 04 - CRUD - Event Staff import creates staff records linked to Staff, Event Master, and Activity Event.

**Preconditions:**
- Event Master EM-101737-H and Activity Event AE-101737-H exist.
- Staff contacts STF-101737-A and STF-101737-B exist.
- Data Importer is open for Event Staff.

| Step | Action | Expected Result | Data |
| --- | --- | --- | --- |
| 1 | Upload Event Staff CSV for two staff members. | CSV maps Staff, Event Master, Activity Event, Working Type, Status. | staff = A, B |
| 2 | Run import. | Import finishes with 2 created Event Staff rows. | expected created = 2 |
| 3 | Open EM-101737-H Master Staff list. | Both staff are listed under the Event Master. | master = EM-101737-H |
| 4 | Open AE-101737-H staff related list or Assign Staff surface. | Both staff are assigned to the Activity Event. | activity = AE-101737-H |
| 5 | Open each Event Staff detail. | Staff, Event Master, Activity Event, Working Type and Status match CSV. | object = Event_Staff__c |

### [LT-101737] Event Staff CSV import - Existing staff assignment overwritten by Salesforce ID

**Description:** AC 04 - Upsert - Existing Event Staff row can be updated to a different Activity Event without duplicate staff assignment.

**Preconditions:**
- Event Staff ES-101737-I exists for Staff A under EM-101737-I and AE-101737-I1.
- AE-101737-I2 exists.
- ES-101737-I Salesforce ID is known.

| Step | Action | Expected Result | Data |
| --- | --- | --- | --- |
| 1 | Prepare Event Staff update CSV with ES-101737-I Salesforce ID and Activity Event = AE-101737-I2. | CSV maps update by Salesforce ID. | old activity = AE-101737-I1 |
| 2 | Run import. | Import finishes with 1 updated row. | expected updated = 1 |
| 3 | Open ES-101737-I. | Activity Event is AE-101737-I2 and updated staff metadata is saved. | new activity = AE-101737-I2 |
| 4 | Search Event Staff for Staff A and EM-101737-I. | Only one Event Staff row exists. | duplicate count = 0 |
| 5 | Open Assign Staff popup for AE-101737-I2. | Staff A is treated as already assigned. | no duplicate selectable |

### [LT-101737] Event Staff CSV import - Invalid references are rejected and valid rows still import

**Description:** AC 04 - Negative and Partial Success - Bad Staff, Event Master, or Activity Event references fail row-by-row.

**Preconditions:**
- One valid Staff, Event Master, and Activity Event exist.
- Data Importer is open for Event Staff.

| Step | Action | Expected Result | Data |
| --- | --- | --- | --- |
| 1 | Upload mixed Event Staff CSV. | CSV contains one valid row and invalid reference rows. | invalid = unknown staff/master/activity |
| 2 | Run import. | Import result shows partial success. | valid rows = 1 |
| 3 | Review failed rows. | Invalid reference rows are rejected with lookup errors. | lookup errors |
| 4 | Open Event Master Master Staff list. | Only the valid staff row is shown. | created = 1 |
| 5 | Search invalid staff/activity references. | No invalid Event Staff records were created. | corrupt data = none |

### [LT-101737] Download Participant CSV - Salesforce ID is exported for update flow

**Description:** AC 05 - Regression - Existing Download Participant List exports the update key as Salesforce ID instead of Event Participant ID.

**Preconditions:**
- Activity Event AE-101737-J has at least two Event Participants.
- User can use Download Participant List.

| Step | Action | Expected Result | Data |
| --- | --- | --- | --- |
| 1 | Open AE-101737-J. | Activity Event detail page opens. | activity = AE-101737-J |
| 2 | Click Download Participant List. | CSV file is downloaded. | action = Download Participant |
| 3 | Open the CSV header. | Identifier column is named Salesforce ID. | not Event Participant ID |
| 4 | Compare Salesforce ID values to Event Participant records. | Each value matches the record Id. | object = Event_Participant__c |
| 5 | Confirm participant fields are still present. | Attendance/response/student columns remain available for update flow. | regression |

### [LT-101737] Import Attendance - Downloaded Salesforce ID updates existing participant attendance

**Description:** AC 05 - Regression - Existing attendance update remains compatible after participant CSV identifier change.

**Preconditions:**
- CSV is downloaded from AE-101737-K participant list.
- At least one participant has blank attendance.

| Step | Action | Expected Result | Data |
| --- | --- | --- | --- |
| 1 | Edit downloaded CSV and set Attendance Status = Attend for Participant A. | CSV keeps Salesforce ID unchanged. | status = Attend |
| 2 | Use existing Import Attendance action. | Import mapping accepts Salesforce ID as update identifier. | action = Import_Attendance |
| 3 | Run import. | Import succeeds with 1 updated participant. | updated = 1 |
| 4 | Refresh AE-101737-K participant list. | Participant A attendance is Attend. | readback |
| 5 | Check participant count. | No duplicate participant is created. | duplicate count = 0 |

### [LT-101737] Manual Assign to Event - Imported participants and staff do not duplicate

**Description:** AC 05 - Regression - Manual Assign to Event respects records created by CSV import.

**Preconditions:**
- EM-101737-L has Participant A and Staff A imported by CSV.
- Activity Event AE-101737-L exists.

| Step | Action | Expected Result | Data |
| --- | --- | --- | --- |
| 1 | Open Assign to Event for EM-101737-L and AE-101737-L. | Assign screen opens. | master = EM-101737-L |
| 2 | Assign Participant A manually. | If already assigned by CSV, Participant A is not duplicated. | participant = A |
| 3 | Assign Staff A manually. | If already assigned by CSV, Staff A is not duplicated. | staff = A |
| 4 | Open AE-101737-L participant/staff lists. | Each person appears only once. | duplicate count = 0 |
| 5 | Reopen Assign to Event popup. | Already assigned imported rows are excluded or shown as already assigned according to existing behavior. | regression |

### [LT-101737] Imported participant data - Participant list and detail remain consistent

**Description:** AC 05 - Display Consistency - Imported Event Participant data is visible and consistent across list and detail pages.

**Preconditions:**
- Event Participant EP-101737-M was created by CSV import.
- User can access Event Participant list and detail.

| Step | Action | Expected Result | Data |
| --- | --- | --- | --- |
| 1 | Open Event Master participant list. | Imported participant is listed. | record = EP-101737-M |
| 2 | Open EP-101737-M detail page. | Detail page opens successfully. | navigation |
| 3 | Compare list and detail fields. | Student, Event Master, Activity Event, Response and Attendance fields match. | consistency |
| 4 | Use back navigation. | User returns to originating list context. | context retained |
| 5 | Login as unauthorized user and try to open detail. | Access is blocked according to existing permission rules. | permission regression |

### [LT-101737] Activity Event bulk import - Multi-day date range remains supported

**Description:** AC 02 and AC 05 - Regression - Existing Koyu2 Activity Event multi-day import remains valid through the new import entry points.

**Preconditions:**
- Koyu2 multi-day Activity Event feature is enabled.
- Event Master EM-101737-N exists.
- Data Importer is opened through Import Activity Event.

| Step | Action | Expected Result | Data |
| --- | --- | --- | --- |
| 1 | Upload Activity Event CSV with Start Date Time on Day 1 and End Date Time on Day 3. | CSV maps both date fields. | multi-day = 3 days |
| 2 | Run import. | Import succeeds. | expected created = 1 |
| 3 | Open the created Activity Event. | Date range matches CSV. | start/end |
| 4 | Search Calendar or Activity Event list for the date range. | Multi-day event appears according to existing multi-day behavior. | regression |
| 5 | Upload invalid row with End Date Time before Start Date Time. | Row is rejected by validation. | invalid date order |
