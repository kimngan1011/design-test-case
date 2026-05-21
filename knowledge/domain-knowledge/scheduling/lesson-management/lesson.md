# Lesson

The central entity. A lesson has date, time, duration, name, code, type, teaching medium, teaching method, location, academic year, course, class, classrooms, and capacity.

Related sub-domain files:
- `student-session.md` — student assignment to lessons.
- `lesson-allocation.md` — LA authorization model.
- `class-assignment.md` — auto-assign by class + multi-class lessons.
- `lesson-teacher.md` — teacher assignment + clashing.
- `lesson-mobile.md` — Mobile viewing + publish notifications.
- `../calendar/calendar-sf.md` — SF Calendar features (drag & drop, multi-class display, bulk publish).
- `../calendar/calendar-bo.md` — BO Calendar features.

## Lesson Schedule (Recurring Lessons)

A Lesson Schedule is a chain of recurring lessons. Each lesson in the chain shares the same schedule but has its own date and incremented lesson code.

| Recurrence | Description |
|---|---|
| **One-time** | Single lesson, no recurrence |
| **Daily** | Repeats every N day(s) |
| **Weekly** | Repeats on selected weekday(s) every N week(s) |
| **Custom** | Repeats on specific dates |
| **Course Schedule** | Linked to Program Master with week order |

End conditions: **On** (end date) or **After** (lesson count).
**Skip Closed Date** checkbox excludes lessons falling on Academic Calendar closed dates.

## Lesson Statuses

```
Draft ──→ Published ──→ Completed
  │           │              │
  │           ↓              │
  └───→ Cancelled ←──────────┘ (rollback: Completed → Published)
        (requires reason)
```

- **Draft:** Not visible on Mobile. Editable.
- **Published:** Visible on Mobile. Editable.
- **Completed:** Not editable. Can rollback to Published.
- **Cancelled:** Not editable. Can reactivate to Draft. Requires cancellation reason.

For Mobile-side visibility per status, see `lesson-mobile.md`.

## Lesson CRUD Operations

| Operation | SF | BO | Notes |
|---|---|---|---|
| **Create on Lesson List** | ✅ | — | Full form: date/time, name, type, medium, method, location, AY, course, class, classrooms, capacity |
| **Create in Lesson Schedule** | ✅ | — | "Add Lesson" pre-fills from schedule; location/AY/course/class are read-only |
| **Import Lesson (CSV)** | ✅ | — | Via SF import wizard; auto-creates teacher assignments and lesson reports |
| **Duplicate Lesson** | ✅ | — | Pre-fills from source; can change recurrence type |
| **Edit Lesson** | ✅ | ✅ (limited) | One-time: direct edit; Recurring: "Only this" or "This and following"; Course code + type read-only on BO |
| **Delete Lesson** | ✅ | — | Removes lesson + reports + student sessions; updates Lesson Allocation |
| **View Lesson** | ✅ | ✅ | BO shows materials, Zoom links, report tab |
| **Bulk Status Update** | ✅ | — | Change status for multiple lessons at once |

## Lesson Code Generation

- **User-provided base code.** When creating a lesson, the Lesson Code field is **blank by default** — user must input it manually. No system auto-generation.
- **Auto-increment (+1) for subsequent lessons in a recurring chain.** Once the first lesson has a code, each subsequent gets `previous_code + 1`. Purely numeric (e.g., 5 → 6 → 7 → 8).
- **Read-only on BO** — `lesson_code` and `lesson_type` are always read-only on BO. Editable only on SF.
- **CSV import requires lesson code.** Mandatory field — auto-generated after import success.
- **"Add Lesson" from Lesson Schedule Detail:** Lesson Code blank — user must enter manually.
- **Extend Recurring:** Auto-calculates `Lesson Code = last existing lesson code + 1`. Subsequent extension lessons continue incrementing.
- **"This and Following" edit:** Codes of following lessons are NOT recalculated — codes stay as originally assigned even if dates shift.
- **Closed date skipping + code behavior:** When a recurring date is skipped, that slot takes **no code number**. The next valid lesson receives the next sequential code — no gaps, no reserved slots.

| Scenario | Behavior |
|---|---|
| Create recurring 5 lessons; date 3 closed, skip=ON | Codes: 1, 2, 3, 4, 5 — no gap |
| "This and Following" edits dates | Codes stay as assigned; no renumbering |
| Extend recurring from code 10 | Extension starts at code 11, continues 12, 13… |
| Duplicate one-time → recurring chain | New chain gets its own codes from user-entered base |
| Extension date conflicts with manually added lesson | That date skipped; code sequence continues |
| Editing lesson code on SF (one-time) | Allowed — editable on SF |

## End Date Logic (Recurring Lessons)

- **"End by On" (end date):** Lessons created on all valid dates up to and including the specified end date. If end date falls on closed date AND Skip Closed Date = ON, no lesson on that date.
- **"End by After" (lesson count):** Exactly N lessons created. If Skip Closed Date = ON, system generates N by skipping closed dates, extending further into the future.
- **Maximum N:** Import capped at 500 lessons. Direct creation: 50 accepted; no lower documented max.
- **Lesson Schedule end date is always dynamic** — derived from last lesson's date, not user's original input:

| Action | Schedule End Date Effect |
|---|---|
| Add a lesson with date > current last | End date **expands** to that lesson's date |
| Add a lesson with date < current first | **Start** date updates to that lesson's date |
| Delete the **last** lesson | End date moves back to new last lesson's date |
| Delete a **middle** lesson | End date **unchanged** |
| "This and Following" shifts dates forward | End date updates to new last lesson's date |
| End date on closed date (skip=ON) | No lesson on end date; last = last valid date before |
| End date on closed date (skip=OFF) | Lesson **IS** created on that closed date |

### Extend Recurring Lesson feature

- "Extend Recurrence" button auto-fills new start date as `current_end_date + 7 days` (non-editable).
- User sets either a **new end date** (must be **later** than current) or **new lesson count** (must be **greater** than current). Equal/earlier blocked.
- Newly extended lessons are **DRAFT** with no teacher or student pre-assigned.
- End date updates across all 5 surfaces: SF Lesson Schedule detail, SF Lesson edit form, SF Calendar related list, BO Lesson detail recurring settings, BO Calendar related list.
- If Skip Closed Dates = ON, closed dates within the extension range are automatically skipped.

## Closed Date Skipping

**Source:** Closed dates defined in Academic Calendar Items (ACI) linked via Academic Calendar Master to the lesson's **location**. Only that location's closed dates apply.

**Skip = OFF:** Recurring lessons land on closed dates without error or warning. One-time lessons on closed dates are **always allowed** regardless of skip setting. "Add Lesson" (manually from Schedule detail) on closed date is **always allowed**.

**Skip = ON:** Any potential lesson date matching a closed date is entirely skipped — no lesson, no code gap. For "End by After N", chain extends further to produce exactly N lessons. For "End by On", chain stops at last valid date before/on end date. The flag is **set at creation time and is non-editable** afterward — inherited by edit and Extend Recurring.

**Non-retroactive behavior:** Adding/editing/deleting a closed date (ACI) does NOT retroactively adjust existing lessons. Closed date added after lessons exist → those lessons remain. Closed date deleted → no lessons retroactively added back.

**"This and Following" + Closed Dates:**
- Skip=ON: Following lessons recalculated from new date; closed dates re-skipped forward.
- Skip=OFF: Following lessons recalculate; no closed date skipping.
- "This and Following" generates a date that already has a manually added lesson in the same Schedule → auto-generated date is **skipped** (no duplicate).

**Drag & Drop to closed date:** DnD on SF Calendar is treated as a one-time lesson date change — system does NOT block or warn. See `../calendar/calendar-sf.md` § Drag & Drop.

| Scenario | Behavior |
|---|---|
| All dates closed (skip=ON, "End by On") | No lessons created at all |
| All dates closed (skip=ON, "End by After N") | Chain extends until N valid dates are found |
| One-time lesson on closed date | Allowed; lesson created normally |
| Edit single lesson date to closed date | Allowed; no blocking |
| DnD to closed date on SF Calendar | Allowed; no blocking or warning |
| Closed date added after lesson created | Existing lesson remains; not retroactively cancelled |

## Edit Rules for Recurring Lessons

- **"Only this lesson"** — edits the selected lesson only.
- **"This and the following lessons"** — edits selected + all subsequent in chain; skips Completed/Cancelled.
- Closed date logic re-applies during edit.
- Course schedule: lesson date must match correct week order; cross-week edits blocked.

## Sync direction

SF is the **source of truth**. SF → BO sync is near real-time. BO Calendar does NOT support lesson CRUD (teachers view + submit reports; not create/edit/delete).

## Dual Lesson (EEA)

Paired Lesson Schedules across two locations (Partner Lesson). A "related LS" links LS at Location 1 with LS at Location 2 — bidirectional pairing.

## Lesson Zoom

Zoom integration for online/hybrid lessons:

| Zoom Type | Description |
|---|---|
| **Single Zoom** | One Zoom link per lesson |
| **Multiple Zoom** | Multiple Zoom links per lesson (one per student/group) |

- **Zoom Owner:** The teacher who owns the Zoom meeting. Start/end dates derive from lesson dates.
- **Zoom Participant:** Students added to Zoom meetings via Student Session.
- Recurring: editing Zoom Owner regenerates links for current + following; old lessons keep old links.
- Zoom links sync to BO and are joinable from BO and Mobile.

## Lesson Report

- Auto-created with **Draft** status when a lesson is created.
- Tied to lesson and student (Lesson Report Detail per student).
- **SF → BO → Mobile** sync.
- Teacher submits/publishes report on BO.
- Student/Parent views published report on Mobile (see `lesson-mobile.md`).
- Aver customization: extended report fields, subject-based reports.
- **New BO entry points for Collect Attendance (LT-96152, 2026-04-15):**
  - Entry 1: BO Lesson Detail → **Report tab** → "Collect Attendance" button.
  - Entry 2: **BO Lesson Report Detail** page → "Collect Attendance" button.
  - Both open the **existing** collect-attendance popup (same UI, same save pipeline).
  - Both **disabled** for Draft and Completed lessons.
  - Saving from either updates the same data: student-session, lesson allocation/report-history, Mobile-facing attendance values.
  - Reopening shows previously saved attendance values (reason, notice, note pre-filled).
