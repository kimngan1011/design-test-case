# Test Coverage: LT-101737 Event Participant and Staff CSV import

## Coverage Matrix

| ID | Area | Rule / Risk | Test Case |
| --- | --- | --- | --- |
| CV-01 | Event Master list view | Import mass actions must exist without row selection | TC01 |
| CV-02 | Event Master record page | Permission-specific buttons route to correct Data Importer objects | TC02 |
| CV-03 | Localization | JP list-button labels must match metadata translations | TC03 |
| CV-04 | Activity Event import create | Required fields and Event Master linkage are correct | TC04 |
| CV-05 | Activity Event import update | Salesforce ID updates existing Activity Event, no duplicate | TC05 |
| CV-06 | Activity Event import validation | Invalid rows rejected row-by-row | TC06 |
| CV-07 | Event Participant import create | Student, Event Master, Activity Event references saved | TC07 |
| CV-08 | Event Participant daily upsert | Existing participant data overwritten by Salesforce ID | TC08 |
| CV-09 | Lottery move | Participant moved from loss AE to win AE through CSV update | TC09 |
| CV-10 | Event Participant import validation | Bad references rejected and valid rows still processed | TC10 |
| CV-11 | Event Staff import create | Staff, Event Master, Activity Event references saved | TC11 |
| CV-12 | Event Staff import update | Existing Event Staff assignment overwritten, no duplicate | TC12 |
| CV-13 | Event Staff import validation | Bad references rejected and valid rows still processed | TC13 |
| CV-14 | Download participant | CSV exposes Salesforce ID as update key | TC14 |
| CV-15 | Attendance update | Existing attendance import still works from downloaded CSV | TC15 |
| CV-16 | Manual assignment compatibility | Imported participants/staff do not duplicate via Assign to Event | TC16 |
| CV-17 | Imported data display | Lists/detail surfaces show imported participant/staff data | TC17 |
| CV-18 | Multi-day import regression | Activity Event import remains compatible with start/end date range | TC18 |

## Existing Qase Impact

### Must Review / Re-run

- `PX-3518`, `PX-3519` - Activity Event import.
- `PX-4905` - Master Event list view action surface.
- `PX-3785` - Download Participant list.
- `PX-3498` to `PX-3505`, `PX-3510`, `PX-3511` - Master Staff flows.
- `PX-3512` to `PX-3517`, `PX-3772` to `PX-3777`, `PX-4907`, `PX-4908` - Assign to Event flows.
- `PX-4909` to `PX-4911` - Event participant response/attendance update.
- `PX-26055` to `PX-26058` - SF Bulk Import Activity Event multi-day import.

### Re-run If Regression Budget Allows

- `PX-3763` to `PX-3769`, `PX-18855` - Master Participant.
- `PX-3506` to `PX-3509` - Related Activity Event list.
- `PX-4906` - Activity Event list view.
- `PX-24896`, `PX-24901` to `PX-24905` - Event Participant detail/list consistency.
- `PX-28127` to `PX-28136` - Event bulk collect attendance.

## Out of Scope

- Building the external parent application form.
- Lottery algorithm itself.
- Multi-Activity Event bulk announcement, unless a later ticket adds that feature.
- New Event Participant custom fields from `LT-108353`, unless that ticket is included in the same QA scope.
