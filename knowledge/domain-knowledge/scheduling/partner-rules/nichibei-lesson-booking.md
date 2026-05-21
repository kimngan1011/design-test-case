# Lesson Booking System (Nichibei — LT-96620, 2026-05-05)

Nichibei-only feature. Disabled by default; must be enabled per partner. Allows students to self-book and cancel lessons via the Learner App. **Parent users have no access — Student scope only.**

## Actors

- Student only. Parent cannot access the Lesson Booking menu.

## Lesson Visibility Rules (Browse Screen)

All four conditions must be met simultaneously:

| Condition | Rule |
|---|---|
| Bookable Flag | = TRUE on the lesson |
| Lesson status | Draft OR Published |
| Location | Lesson location linked to student's active LA |
| Booking deadline | Lesson date >= today + X days (partner `minimum_days_before_booking` config) |

## Booking Flow (Atomic)

Steps execute atomically: validate → create Student Session (`Booking_Flag = TRUE`) → save remarks → auto-publish if Draft.

### LA Selection Priority (when student has multiple active LAs)

1. LA active (lesson date within LA Start–End date)
2. LA location = Lesson location
3. LA start date earlier
4. LA created earlier

## Auto-Publish on Booking

- If lesson status = Draft when booking submitted → **automatically set to Published**.
- This auto-publish is **silent** — no push notification triggered (confirmed by PdM, 2026-05-05).
- **Auto-published lesson stays Published** even if all bookings are later cancelled — does NOT revert to Draft.

## Points Check

- Uses the **same point-deduction mechanism as manual staff assignment** in Nichibei (see `nichibei-lesson-allocation.md`).
- Booking blocked if remaining points insufficient (same validation as existing flow).

## Teacher Notifications (SF)

- When student books: SF notification to assigned teacher within 30 seconds.
- When student cancels: SF notification to assigned teacher within 30 seconds.
- SF-only notifications (not push); triggered by app actions only, NOT by staff SF assignments.

## Cancel Rules

- Only lessons with `Booking_Flag = TRUE` (student self-booked) show Cancel button in app.
- Staff-allocated lessons (`Booking_Flag = FALSE/blank`) show no Cancel button.
- Cancellation deadline: X hours before lesson start (partner config).
- Cancel is atomic: delete Student Session → remove from Booking List → notify teacher.

## Bookable Flag

- Set per lesson in SF Lesson Detail (checkbox, default OFF).
- Turning OFF does not cascade — existing Student Sessions are unaffected.
- Also available on Lesson Schedule for CSV bulk import (low priority MVP).

---

## BO Lesson List Enhancements — LT-96616 (2026-05-11)

### Lesson Status Filter Default

- Filter defaults to "Published" on every Lesson List page load.
- PERSISTENT — retains user-selected value across navigation; resets to "Published" only when user manually clears the filter.
- For Limit Teacher profile: Published default applies together with the Limit Teacher scope filter (both active simultaneously — teacher sees only their assigned Published lessons).

### Collect Attendance — Student Attendance Response Display (LT-96656)

- Collect Attendance page EXTENDED: student-submitted `Attendance_Response_Remark` shown as a read-only inline field per student row (reuses existing UI — no new column on Lesson List).
- Sources: Booking flow (prefixed `"Booking Note: "` per LT-96620) + Submit Attendance on Mobile — displayed as a single field with no visual distinction between sources.
- Blank when no student has submitted a response.
- Staff attendance recording (radio buttons + Save) remains fully functional.

### Collect Attendance — New Entry Point from Lesson List (LT-96657)

- New entry point on BO Lesson List row opens the existing Collect Attendance page.
- Available for **Published lessons ONLY** — hidden/disabled for Draft, Completed, and Cancelled.
- Page retains full collect attendance functionality; only the student-submitted remark field is read-only.
