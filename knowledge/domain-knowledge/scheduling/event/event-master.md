# Event Master

Events are activities managed via Event Master, scheduled for students, and displayed on Calendar.

## Event Master (568 test cases)

The master record defining an event template. Contains event details, target segments, participant rules.

| Feature | Cases | Description |
|---|---:|---|
| **Creating Event Master** | 15 | Create event templates |
| **Editing Event Master** | 5 | Modify event details |
| **Deleting Event Master** | 4 | Remove event records |
| **Searching Event Master** | 2 | Find events |
| **Importing** | 2 | CSV import |
| **Master Record Details** | 95 | Record page with participant/staff lists and related events |

## Target Segments

Define who can participate in an event:

| Segment Type | Operations |
|---|---|
| **Target Location** | Create (7), Edit (4), Delete (3) |
| **Target School** | Create (6), Edit (4), Delete (3) |
| **Target Grade** | Create (6), Edit (4), Delete (3) |
| **Target Course** | Create (6), Edit (4), Delete (3) |

## Related entities

- **Activity Event** — instances created from this master. See `activity-event.md`.
- **Booking System** — Reservation/booking for events. See `booking-system.md`.
- **Events on Calendar** — display on SF/BO Calendar. See `events-on-calendar.md`.
- **Koyu partner features** — Auto Create Application, Cancel Booked Event, Update Cancel, Draft Status. See `partner-rules/koyu-event-features.md`.
