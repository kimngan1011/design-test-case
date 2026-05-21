# Calendar on BO (224 test cases)

BO Calendar provides a read-only view of lessons for teachers and centre managers. No CRUD from BO Calendar — navigation only.

## Features

| Feature | Cases | Description |
|---|---:|---|
| **Calendar Filter** | 37 | Filter by location, teacher, date range |
| **Calendar View** | 67 | Day/Week/Month views |
| **Events on Calendar** | 51 | Activity events from Event Master |
| **Lesson View** | 35 | View lesson details from calendar |
| **Bulk Update Attendance** | 34 | **Renseikai-only**: bulk collect attendance from calendar view |

## Closed dates display

BO Calendar visually marks closed dates (4 cases).

## Renseikai Bulk Update Attendance

Renseikai-specific feature (34 cases). Staff can collect attendance for multiple students/lessons in bulk directly from the BO Calendar view. NOT available to other partners.

## Access by user type

See `access-by-user-type.md` for the full CPU/SPU vs affiliation-based access matrix.

## Sync direction

SF is the source of truth. SF → BO sync is near real-time. BO Calendar does NOT support lesson CRUD (teachers use BO to view and submit reports, not to create/edit/delete lessons).
