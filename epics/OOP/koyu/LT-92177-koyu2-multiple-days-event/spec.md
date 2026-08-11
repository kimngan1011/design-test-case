# LT-92177 — Koyu2 Multiple Days Event

## Requirement Summary

Koyu2 needs Activity Events that span multiple calendar days, such as 2025-12-12 10:00 to 2025-12-14 17:00, treated as a single event with the same attendance and booking lifecycle.

## Correct Domain Model

- Event Master is a template: event type, description, booking settings, target segment, reminders, notification settings.
- Activity Event is the scheduled event instance: Event Master lookup, location, medium, capacity, classrooms, start datetime, end datetime, status, participant settings.
- Start Date, End Date, Start Time, End Time, and Duration Days belong to Activity Event only.
- Event Master must not be tested as if it has event Start Date or End Date fields.

## Implementation Notes From Repo

- Salesforce Activity Event form is gated by Lesson Custom Setting `MANAERP__Enable_Multiple_Event_Days__c`.
- When enabled, the Activity Event form shows Start Date, Start Time, Duration Days, End Date, End Time.
- When disabled, the legacy form shows Event Date, Start Time, End Time.
- BO calendar uses FeatureSettingConfig `calendar.multiple_event_day.is_enabled`.
- SF calendar uses `MANAERP__Enable_Multiple_Event_Days__c`.
- Get Event API currently returns Activity Events only when `Start_Date_Time__c >= start_date` and `End_Date_Time__c <= end_date`; partial overlap is excluded.

## Impacted Surfaces

- Salesforce Activity Event create/edit/duplicate/detail.
- Salesforce weekly and daily calendar.
- Back Office weekly and daily calendar.
- Learner App calendar and event detail.
- Booking System event list, reservation, capacity, cancellation deadline.
- Koyu auto-create application.
- Get Event API and Activity Event API.
- Attendance, participant list, and CSV export.
