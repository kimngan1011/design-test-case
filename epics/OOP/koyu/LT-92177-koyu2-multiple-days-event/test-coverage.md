# Test Coverage: LT-92177 — Koyu2 Multiple Days Event

## Scope Correction

The previous 31 generated cases must be treated as invalid wherever they put Start Date, End Date, Start Time, or End Time on Event Master. Those fields belong to Activity Event.

## Coverage Matrix

| ID | Area | Cases | Risk |
|---|---|---:|---|
| ACT-01 | Event Master remains template; no schedule fields | 1 | critical |
| ACT-02 | Activity Event multi-day create/edit/duplicate/date validation | 14 | critical |
| CAL-01 | SF Calendar weekly/daily multi-day rendering and filters | 9 | critical |
| BO-01 | BO Calendar feature config and rendering | 3 | critical |
| DET-01 | SF/BO detail Date vs Date Range labels | 3 | major |
| APP-01 | Learner App calendar/detail/response | 3 | critical |
| BOOK-01 | Booking list/reserve/search/capacity/cancellation deadline | 5 | critical |
| API-01 | Get Event API and Activity Event API date range rules | 5 | major |
| OPS-01 | Attendance, participant export, paid/extra participant regressions | 5 | major |

## Required Regression Rules

- Multi-day means one Activity Event record, not one record per day.
- Attendance, response, reservation, capacity, and auto-create application must happen once per Activity Event.
- Calendar can show the same Activity Event on multiple days, but clicking any visible entry must open the same Activity Event ID.
- Booking and API date filtering must be tested explicitly because API uses full-containment date range logic.
- Feature flags must be split: SF custom setting and BO FeatureSettingConfig.
