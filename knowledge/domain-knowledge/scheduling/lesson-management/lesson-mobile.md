# Lesson on Mobile (Learner App) — Viewing + Notifications

This file covers everything students and parents see/do on the Mobile Learner App related to lessons, plus all notification flows triggered by lesson lifecycle events.

For Mobile-side lesson booking (self-book/self-cancel from app), see `../partner-rules/nichibei-lesson-booking.md`.

## Mobile viewing rules

- Students/Parents see **Published** lessons only.
- View lesson details, materials.
- Join Zoom meetings for zoom/online lessons.
- Submit attendance (student self-attendance); receive notifications on attendance changes.
- View lesson reports after teacher publishes.
- Receive notifications on lesson date/time changes.

### Status → visibility

| Status | Mobile visibility |
|---|---|
| Draft | NOT visible |
| Published | Visible |
| Completed | Visible (report viewable) |
| Cancelled | NOT visible |

Draft → Published syncs to Mobile immediately. Cancelled → Draft removes lesson from Mobile.

---

## Publish & Notify Student (Renseikai — LT-96662, 2026-04-15)

> Per-lesson notification flow. For bulk publish notification (Riso), see `../calendar/calendar-sf.md` § Bulk Publish.

Renseikai-only feature, controlled by custom permission **"Publish Lesson With Notification"** added to the OOP Permission Set.

### "Publish and Notify" Button

| Property | Value |
|---|---|
| Platform | SF Lesson Detail page |
| Visibility | Draft OR Published lessons only; hidden for Completed/Cancelled |
| Permission | Requires "Publish Lesson With Notification" custom permission |
| Partner scope | Renseikai only on initial release; other partners considered per request |

### State transition on click

| Lesson status when clicked | Result |
|---|---|
| Draft | Lesson published (status → Published) **immediately** THEN confirmation modal shown |
| Published | No status change THEN confirmation modal shown |

> **Important:** Status change happens **before** the modal appears. If user selects "Don't Send" on a formerly-Draft lesson, the lesson **remains Published** — status is NOT reverted.

### Confirmation Modal

- Message: _"Would you like to send notifications about the publishing lesson to all allocated students?"_
- Options: **Send** / **Don't Send**.
- "Send" → triggers notification flow immediately.
- "Don't Send" → no notification sent; lesson state preserved as-is.

### Notification Recipients

- All students assigned to the lesson + ALL parent contacts linked via Relationship.
- Student with no linked parent → notification sent to student only.
- Student/parent with no device token (never logged into app) → notification silently skipped; no error.

### Notification Content

| Field | Value |
|---|---|
| Title | "Lesson Published" (JP: 授業公開のおしらせ) |
| Body | Lesson name + lesson date + start/end time + CTA to view lesson details |
| Delivery | Real-time (not batched) |
| Deep-link | Tapping notification navigates to the specific Lesson Detail page of the published lesson |

### Retry & Reliability

- Up to 3 automatic retry attempts with short delay between each.
- **Idempotent delivery** — only one notification delivered even if multiple retries succeed.
- Every attempt (success or failure) logged for audit.
- If all 3 attempts fail → failure logged clearly to error log / admin dashboard.

---

## Nichibei booking — silent auto-publish

When a Nichibei student self-books a Draft lesson via the Learner App, the lesson auto-publishes but the publish is **silent** — no push notification triggered (confirmed by PdM, 2026-05-05). Auto-published lesson stays Published even if all bookings are later cancelled — does NOT revert to Draft.

For the full booking flow, see `../partner-rules/nichibei-lesson-booking.md`.
