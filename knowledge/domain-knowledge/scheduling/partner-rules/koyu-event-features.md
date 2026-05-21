# Koyu Event Features

Koyu-specific extensions to the Event domain. See `../event/event-master.md` and `../event/booking-system.md` for the core Event entities.

## Koyu Auto Create Application (51 cases)

Auto-generate application records for event participants. When a participant is added to an event, the system creates a linked Application record automatically.

## Koyu Cancel Booked Event (68 cases)

Cancel event bookings with Koyu-specific business rules:
- Cancellation deadlines per partner config.
- Refund/credit handling.
- Notification to staff and student on cancellation.

## Update Cancel Booked Event (65 cases — 10 user stories)

Modify cancellation records after they've been created:
- Edit cancellation reason.
- Restore booking if cancelled in error.
- Adjust refund/credit values.

## Koyu Draft Status (19 cases — 5 user stories)

Handle draft status for event bookings:
- Drafts saved without finalizing the booking.
- Transition from Draft → Submitted → Confirmed.
- Visibility rules per status (staff vs student).

## Related files

- `../event/event-master.md` — core Event Master entity.
- `../event/booking-system.md` — Internal + External booking flows.
- `../event/activity-event.md` — Activity Event instances.
