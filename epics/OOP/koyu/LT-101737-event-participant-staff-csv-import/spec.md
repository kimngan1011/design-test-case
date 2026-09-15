# LT-101737: Event Participant and Staff CSV import

## Sources

- Jira: `LT-101737` - `[koyu2] Core | 525 - Event Participant and Staff CSV import`
- Related Jira: `PBT-1838`, `LT-98081`, `LT-101739`
- Confluence: `Koyu (ph2) Outdoor Event`
- Confluence: `No.525_Event Participant Lottery`
- Dev evidence: `erp-salesforce` commits `2113d2d9d0`, `e918456af8`, `479d023a3e`

## Requirement Summary

Koyu2 outdoor event operations need CSV-based import/upsert because participants and staff are managed outside Manabie during application and lottery operations.

The feature adds import entry points from Event Master and relies on Salesforce Import Wizard/Data Importer for:

- Activity Event create/update import.
- Event Participant create/update import using Student, Event Master, and Activity Event.
- Event Staff create/update import using Staff, Event Master, and Activity Event.
- Existing Event Attendance download/update flow remains usable.

## Dev Change Summary

The implementation is Salesforce metadata-heavy:

- `Event_Master__c` list view search layout now exposes mass action buttons:
  - `Import_Activity_Event_List_Button`
  - `Import_Participant_List_Button`
  - `Import_Event_Staff_List_Button`
- Event Master record page action bar exposes record-level buttons:
  - `Import_Activity_Event`
  - `Import_Participant`
  - `Import_Event_Staff`
- Button URLs open Data Importer with object selection:
  - `/dataImporter/dataImporter.app?objectSelection=MANAERP__Activity_Event__c`
  - `/dataImporter/dataImporter.app?objectSelection=MANAERP__Event_Participant__c`
  - `/dataImporter/dataImporter.app?objectSelection=MANAERP__Event_Staff__c`
- Record page visibility rules are permission based:
  - `Create_Activity_Event`
  - `Add_Master_Participant`
  - `Add_Master_Staff`
- Japanese translations were added for the list-view import buttons.

## Field and Validation Inventory

### Activity Event

Core required fields:

- `Event_Master__c`
- `Location__c`
- `Start_Date_Time__c`
- `End_Date_Time__c`
- `Allow_Response__c`
- `Send_To__c`

Important validations and behavior:

- Start Date Time cannot be greater than End Date Time.
- Event Capacity cannot be zero.
- Paid Activity Event requires Product Offering and Order Location.
- Status cannot move from Draft to Completed directly.
- Future Activity Event cannot be completed.

### Event Participant

Core fields:

- Required: `Contact__c`, `Event_Master__c`
- Optional but in scope: `Activity_Event__c`, `Attendance_Status__c`, `Attendance_Note__c`, `Response__c`, `Response_Note__c`, `Reserved_By__c`

Operational requirement:

- Daily import/upsert should overwrite existing participant data during application period.
- Lottery move can be performed by updating participant `Activity_Event__c` from a loss Activity Event to a win Activity Event.
- The download participant CSV must expose Salesforce ID for update/import flows.

### Event Staff

Core fields:

- Required: `Staff__c`, `Event_Master__c`
- Optional but in scope: `Activity_Event__c`, `Working_Type__c`, `Status__c`

Operational requirement:

- Staff CSV import creates or updates Event Staff assignments to Master Event and Activity Event.

## Acceptance Criteria

### AC 01 - Import buttons

- Event Master list view shows three import mass-action buttons: Import Activity Event, Import Participant, Import Event Staff.
- Event Master record page shows the same three import buttons when the user has the corresponding custom permissions.
- Each button opens Data Importer with the correct object selected.
- List-view mass actions do not require row selection.
- Japanese labels are correct for JP locale.

### AC 02 - Activity Event CSV import

- Valid Activity Event CSV rows create Activity Events under the selected Event Master.
- Valid update rows overwrite an existing Activity Event by Salesforce ID.
- Invalid required field, lookup, date order, capacity, and paid-event rows are rejected without creating corrupt data.
- Mixed valid and invalid rows create/update only valid rows.

### AC 03 - Event Participant CSV import

- Valid participant CSV rows create Event Participant records linked to Student, Event Master, and Activity Event.
- Valid update rows overwrite existing Event Participant data by Salesforce ID and do not create duplicates.
- Daily application upsert can update applicant preference/assignment data during the application period.
- Lottery move updates participants from a loss Activity Event to a win Activity Event.
- Invalid Student, Event Master, or Activity Event references are rejected row-by-row.

### AC 04 - Event Staff CSV import

- Valid staff CSV rows create Event Staff records linked to Staff, Event Master, and Activity Event.
- Valid update rows overwrite Activity Event assignment and staff metadata by Salesforce ID.
- Invalid Staff, Event Master, or Activity Event references are rejected row-by-row.
- Imported staff records appear in Master Staff and Assign Staff surfaces.

### AC 05 - Existing flows remain compatible

- Existing Download Participant List still works and its update identifier is Salesforce ID.
- Existing Import Attendance still updates attendance using the exported identifier.
- Manual Assign to Event and Master Staff flows still avoid duplicates when records were imported by CSV.
- Event Participant detail/list data remains consistent after import.

## Qase Existing Impact

Directly impacted existing Qase cases:

- `PX-3518`, `PX-3519` - Activity Event CSV import valid/invalid.
- `PX-4905` - Master Event list view.
- `PX-3785` - Download Participant list.
- `PX-3498` to `PX-3505`, `PX-3510`, `PX-3511` - Master Staff add/remove.
- `PX-3512` to `PX-3517`, `PX-3772` to `PX-3777`, `PX-4907`, `PX-4908` - Assign to Event staff/student and remove flows.
- `PX-4909` to `PX-4911` - Event Participant response/attendance update.
- `PX-26055` to `PX-26058` - Koyu2 SF Bulk Import Activity Event multi-day import.

Near-impact regression cases:

- `PX-3763` to `PX-3769`, `PX-18855` - Master Participant creation/list display.
- `PX-3506` to `PX-3509` - Related Activity Event list.
- `PX-4906` - Activity Event list view.
- `PX-24896`, `PX-24901` to `PX-24905` - Event Participant detail page and list consistency.
- `PX-28127` to `PX-28136` - Event bulk collect attendance participant status update.

## Qase Placement

- Parent suite: `Event Master > update testcase` (`suite_id=2628`)
- Imported child suite: `Event Participant and Staff CSV Import` (`suite_id=3530`, `suite_parent_id=2628`)
- Imported cases: `PX-28145` to `PX-28162`
- Test run: `PX-3537` - https://app.qase.io/run/PX/dashboard/3537
