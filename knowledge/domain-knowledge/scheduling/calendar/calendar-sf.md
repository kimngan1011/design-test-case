# Calendar on SF (560 test cases)

Calendar provides a visual view of lessons and events across time. SF Calendar is the primary management surface.

## Features

| Feature | Cases | Description |
|---|---:|---|
| **Lesson CRUD on Calendar** | 151 | Create/Read/Update/Delete lessons directly from calendar view |
| **Calendar View** | 144 | Day/Week/Month views; filter by location, teacher, student |
| **Student/Teacher/Reallocation List** | 114 | Contextual lists within calendar lesson detail (see `student-teacher-reallocation-list.md`) |
| **Drag & Drop** | 44 | Move/resize lessons on the calendar timeline |
| **Change Lesson** | 11 | Change lesson details from calendar context |
| **Clashing Alert** | 33 | Teacher time conflict warnings on calendar |
| **Events on Calendar** | 51 | Activity events shown on SF calendar |
| **Multiple Classes** | 8 | Handle lessons with multiple class assignments |
| **Calendar Filter** | 1 | Filter configuration |

## Drag & Drop

- Controlled by the **"Enable Calendar Drag And Drop"** custom setting in SF Lesson Custom Settings. Must be explicitly turned ON — not enabled by default.
- Available in **Weekly and Daily views only**; Month view does NOT support DnD.
- Calendar grid snaps to **10-minute intervals** — e.g., dragging to 14:07 snaps to 14:10.
- **One-time lessons:** directly updates date/time, no confirmation popup.
- **Recurring lessons:** triggers the Edit Lesson modal with "Only this / This and following" choice.
- Dropping **outside calendar bounds**: lesson time is NOT updated.
- **Clashing alerts** re-evaluated on every time change, including DnD.
- DnD to closed date is treated as a one-time lesson date change — system does NOT block or warn. Skip Closed Date logic applies only to recurring chain generation (see `../lesson-management/lesson.md` § Closed Date Skipping).

## Multiple Classes on Calendar

- A single lesson can have **multiple classes assigned** (see `../lesson-management/class-assignment.md`).
- SF Calendar displays lessons with multiple classes on the lesson card (Group teaching method shows multiple class names).
- Feature-flagged via `Lesson_BackOffice_LessonSF_MultipleClassesSF` (Unleash) and `Multiple_Classes_In_Lesson__c` (SF custom setting).
- Calendar class filter uses **ALL-match** (AND) logic:
  - Filtering by [Class X]: shows all lessons containing Class X (including multi-class lessons that also have Class Y).
  - Filtering by [Class X, Class Y]: shows only lessons containing BOTH Class X AND Class Y.

## Closed dates display

SF Calendar visually marks closed dates (18 cases). Closed-date logic for lesson generation: see `../lesson-management/lesson.md` § Closed Date Skipping.

## Bulk Publish timezone boundary (core SF - LT-110579, added 2026-09-09)

Bulk Publish Lesson date filtering must evaluate the selected Start Date and End Date in the Salesforce timezone, not by raw UTC day boundaries.

- For Salesforce timezone GMT+9, selecting Start Date = End Date = `2030-09-19` maps to `2030-09-18 15:00:00 UTC <= lesson start datetime < 2030-09-19 15:00:00 UTC`.
- Lessons starting on `2030-09-19 00:00` through `2030-09-19 23:59` in Salesforce local time are in scope.
- Lessons starting on `2030-09-18 23:59` or `2030-09-20 00:00` in Salesforce local time are out of scope.
- Existing Bulk Publish rules still apply after timezone conversion: location scope, selected-student scope when enabled, and Draft-only status transition.
- Regression cases live in `epics/calendar/LT-110579-bulk-publish-timezone/`.

## Student List (left panel) — Student Course Status filter (core SF - LT-108376, added 2026-10-07)

The left **Student** panel on Lesson Calendar lists Lesson Allocations (LAs) that staff can drag into lessons. Its filter popover (funnel icon) contains Location, Academic Year, Type, **Student Course Status**, Package Type, Course Master, Class, Grade, School, … with **Reset** / **Save** at the bottom.

- **Status is derived from the LA dates** (from code `LessonMasterHandler.getListAssignStudent`):

  | Status | LA condition | JP label |
  |---|---|---|
  | Active | Start Date Time ≤ TODAY **and** End Date Time ≥ TODAY | アクティブ |
  | Not Started | Start Date Time > TODAY | 未来のコース |
  | Inactive | End Date Time < TODAY | 過去のコース |

  `TODAY` is the Salesforce date literal: **date only, in the logged-in user's Salesforce timezone** (not the location's). An LA starting today at 18:00 is Active from 00:00; a user on GMT+7 and a user on JST can see a different status for an LA near midnight JST. Not defined in any spec — PO question open (LT-108376 Q3). Selected statuses are OR-combined; no status selected = no status condition.
- **Defaults on first load:** Location = calendar location (chip not removable); Academic Year = **current AY**; Type = all types (Regular, Seasonal, Trial); Student Course Status = **Active + Not Started** (since LT-108376; before it was Active only). The list and "N items" count are filtered by the defaults immediately, without opening the popover.
- **Lesson Master** uses the same component (`listStudentCalendar`) but keeps the **Active-only** default.
- **One row per LA, not per student.** A student with two LAs that match the filter (e.g. Change / Add Associated Course with a future effective date → old LA Active + new LA Not Started) shows two rows. Expected — no merge by student.
- **Academic Year scopes the list.** A newly ordered LA in the **next** academic year stays hidden with the default current AY until that AY is selected — by design.
- **Reset** clears every filter except the calendar location (Academic Year, Type and Student Course Status become empty = all values); it does **not** restore the defaults. Changes take effect only after **Save**; closing the popover without Save discards them.
- **Filter state:** changing the calendar location or switching view keeps the user's selection (only the Location chip follows the calendar location). A page reload re-applies the defaults.
- The list loads only the first **200 LA rows** (sorted by Phonetic Name → Name → Created Date) — accepted Salesforce limitation; use name search to reach others.
- Not to be confused with the **calendar grid** student filter used by Bulk Publish "Apply to selected students" (section below).
- Qase: suite 3698 (PX-29506 → PX-29522, incl. timezone cases), existing suite 483 "Student Filter" (PX-4639 default, PX-13084 / PX-4653 Reset). Spec: `epics/calendar/LT-108376-not-started-default-student-filter/`.

---

## Bulk Publish (Riso — LT-98532, confirmed 2026-05-12)

Riso-specific bulk publish flow on SF Calendar. Allows staff to publish multiple Draft lessons at once.

### "Apply to Selected Students" Checkbox

- Present in ALL SF Calendar Bulk Publish modal variants (weekly view, daily view, teacher view).
- **State is driven solely by the SF Calendar student filter:**
  - 0 students in filter → checkbox **DISABLED**.
  - 1+ students in filter → checkbox **ENABLED** (unchecked by default).
- When **activated**: location field locked to calendar's current location (disabled, read-only); user cannot add extra locations.
- **The student filter cannot be modified while the Bulk Publish modal is open.** User must close modal, update filter, then reopen.
- When **not activated** (with students in filter): existing publish-all behavior retained.

### Notification Trigger and Deduplication

- Bulk publish notifications are a **separate notification path** from per-lesson "Publish and Notify" (Renseikai — see `../lesson-management/lesson-mobile.md`).
- **Cross-type deduplication:** Before sending a bulk notification for a lesson, the system checks if that lesson was already published+notified via the Renseikai per-lesson flow (LT-96662). If yes, the lesson is **excluded from the bulk notification** — no duplicate notification sent.
- **Partial failure ("Completed with Errors"):** Notifications ARE sent for students of **successfully published lessons** only.
- **0 Draft lessons in scope:** Job skips silently — no notification, no user-facing warning.
- **Student with no Parent Contact:** Student is **skipped entirely** — no notification sent to student or parents.

### Bulk Action Monitoring (Riso-only)

- Config-gated: "Bulk Action Monitoring config" (ON = Riso, OFF = others).
- Permission-gated: "Bulk Action Monitoring permission" (HQ Admin or CM only).
- For Bulk Publish: **1 monitoring record per student+location pairing**.
- Records from the same batch (same user trigger) are grouped by Batch ID.
- Job statuses: Pending → Processing → Completed / Completed with Errors / Failed.
- Processed Count = Success + Failed (auto-calculated).
- Data retention: **2 weeks** then auto-purged.

---

## Related files

- Three contextual lists on lesson detail popup: `student-teacher-reallocation-list.md`.
- Calendar access matrix: `access-by-user-type.md`.
- BO Calendar: `calendar-bo.md`.
- Lesson entity (core CRUD, recurrence, closed dates): `../lesson-management/lesson.md`.
- Multi-class lessons: `../lesson-management/class-assignment.md`.
