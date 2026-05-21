# Events on Calendar

Events appear on both SF Calendar and BO Calendar, showing event schedules alongside lessons.

| Surface | Cases |
|---|---:|
| SF Calendar | 51 |
| BO Calendar | 51 |
| SF Calendar — staff-assigned events view | 7 |

Staff assigned to events see them on their SF Calendar view.

## Cross-domain context

```
Event Master ──creates──→ Activity Event ──shown on──→ Calendar (SF + BO)
                               │
                               ├── Assign staff ──→ staff sees on SF Calendar
                               ├── Assign students ──→ students see on Mobile
                               └── Booking system ──→ reserves slots
```

- Events and Lessons coexist on the Calendar.
- Events can assign staff (teachers) who see them on their calendar, similar to lesson teacher view.
- Students see assigned events on Mobile Learner App.
- Both events and lessons respect location-based access control.

## Related files

- Event Master (template): `event-master.md`
- Activity Event (instance): `activity-event.md`
- Booking System: `booking-system.md`
- Calendar SF: `../calendar/calendar-sf.md`
- Calendar BO: `../calendar/calendar-bo.md`
