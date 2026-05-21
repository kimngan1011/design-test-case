# Event Booking System (201 test cases)

Reservation and booking for events.

## Booking Types

| Type | Cases | Description |
|---|---:|---|
| **Internal Booking** | 93 | Staff reserve slots for students |
| **External Booking** | 108 | External link for self-booking |

## Sub-features

- **Reserve by target segment** (22) — auto-filter participants by Target Location/School/Grade/Course.
- **Notification** (3) — sent on booking actions.
- **Remove price** (3) — admin can remove pricing.
- **External link** (4) — generate shareable booking link.
- **Koyu Auto Create Application** (51) — see `partner-rules/koyu-event-features.md`.

## Related entities

- **Event Master** — see `event-master.md`.
- **Activity Event** — booked instance. See `activity-event.md`.
- **Koyu Cancel Booked Event** + **Update Cancel** + **Draft Status** — see `partner-rules/koyu-event-features.md`.
