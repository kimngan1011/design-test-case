# Manabie Scheduling — Domain Knowledge

> **Purpose:** Reference document for QA analysis. Read this before analyzing any Jira ticket related to Manabie Scheduling.
> **Last updated:** 2026-04-05
> **Source:** 4,191 test cases (Qase PX suite 18), 11 system diagrams, existing test case and specs files.

---

## 1. System Overview

Manabie Scheduling is a lesson-scheduling and event-management platform used by Japanese education companies. It runs across **three platforms**:

| Platform                 | Role                         | Users                                          |
| ------------------------ | ---------------------------- | ---------------------------------------------- |
| **Salesforce (SF)**      | Primary management UI        | Staff (HQ Admin, Centre Manager, Centre Staff) |
| **Back Office (BO)**     | Teaching and lesson delivery | Teachers (CPU/SPU), Centre Managers            |
| **Learner App (Mobile)** | Viewing and attendance       | Students, Parents                              |

Data flows **SF → BO → Mobile**. SF is the source of truth for lesson creation and student/teacher management. BO syncs from SF and extends with teaching features (reports, materials, Zoom). Mobile shows published lessons and reports.

---

## 2. Three Core Domains

### 2.1 Lesson

The central entity. A lesson has date, time, duration, name, code, type, teaching medium, teaching method, location, academic year, course, class, classrooms, and capacity.

#### Lesson Schedule (Recurring Lessons)

A Lesson Schedule is a chain of recurring lessons. Each lesson in the chain shares the same schedule but has its own date and incremented lesson code.

| Recurrence          | Description                                    |
| ------------------- | ---------------------------------------------- |
| **One-time**        | Single lesson, no recurrence                   |
| **Daily**           | Repeats every N day(s)                         |
| **Weekly**          | Repeats on selected weekday(s) every N week(s) |
| **Custom**          | Repeats on specific dates                      |
| **Course Schedule** | Linked to Program Master with week order       |

End conditions: **On** (end date) or **After** (lesson count).

**Skip Closed Date** checkbox excludes lessons falling on Academic Calendar closed dates.

#### Lesson Statuses

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

#### Lesson CRUD Operations

| Operation                     | SF  | BO           | Notes                                                                                                     |
| ----------------------------- | --- | ------------ | --------------------------------------------------------------------------------------------------------- |
| **Create on Lesson List**     | ✅  | —            | Full form: date/time, name, type, medium, method, location, AY, course, class, classrooms, capacity       |
| **Create in Lesson Schedule** | ✅  | —            | "Add Lesson" pre-fills from schedule; location/AY/course/class are read-only                              |
| **Import Lesson (CSV)**       | ✅  | —            | Via SF import wizard; auto-creates teacher assignments and lesson reports                                 |
| **Duplicate Lesson**          | ✅  | —            | Pre-fills from source; can change recurrence type                                                         |
| **Edit Lesson**               | ✅  | ✅ (limited) | One-time: direct edit; Recurring: "Only this" or "This and following"; Course code + type read-only on BO |
| **Delete Lesson**             | ✅  | —            | Removes lesson + reports + student sessions; updates Lesson Allocation                                    |
| **View Lesson**               | ✅  | ✅           | BO shows materials, Zoom links, report tab                                                                |
| **Bulk Status Update**        | ✅  | —            | Change status for multiple lessons at once                                                                |

#### Lesson Code Generation

- **User-provided base code.** When creating a lesson (on Lesson List or on Calendar), the Lesson Code field is **blank by default** — the user must input it manually. There is no system auto-generation of the base code.
- **Auto-increment (+1) for subsequent lessons in a recurring chain.** Once the first lesson has a code, each subsequent lesson in the chain gets `previous_code + 1`. Format is purely numeric (e.g., codes 5 → 6 → 7 → 8).
- **Read-only on BO** — `lesson_code` and `lesson_type` are always read-only on BO. Editable only on SF.
- **CSV import requires lesson code.** The import CSV requires the lesson code as a mandatory field — auto-generated after importing successfully and lesson-related is created.
- **"Add Lesson" from Lesson Schedule Detail:** The Lesson Code field is blank — the user must manually enter a code even when other fields are pre-filled from the schedule.
- **Extend Recurring:** The extension form auto-calculates `Lesson Code = last existing lesson code + 1`. Subsequent new lessons in the extension continue incrementing from there.
- **"This and Following" edit:** Lesson codes of following lessons are **NOT recalculated** — codes stay as originally assigned even if dates shift.
- **Closed date skipping + code behavior:** When a recurring date falls on a closed date and is skipped, that slot takes **no code number**. The next valid lesson simply receives the next sequential code — no gaps, no reserved slots. _(e.g., if lessons 1 and 3 are generated but date 2 is skipped, the result is codes 1 and 2, not 1 and 3)_

| Scenario                                              | Behavior                                                                          |
| ----------------------------------------------------- | --------------------------------------------------------------------------------- |
| Create recurring 5 lessons; date 3 is closed, skip=ON | Codes: lesson 1, lesson 2, lesson 3, lesson 4, lesson 5 — no gap for skipped date |
| "This and Following" edits dates                      | Codes stay as assigned; no renumbering                                            |
| Extend recurring from code 10                         | Extension starts at code 11, continues 12, 13…                                    |
| Duplicate one-time lesson → recurring chain           | New chain gets its own codes from user-entered base                               |
| Extension date conflicts with manually added lesson   | That date skipped; code sequence continues without that slot                      |
| Editing lesson code on SF (one-time)                  | Allowed — editable field on SF                                                    |

#### End Date Logic (Recurring Lessons)

- **"End by On" (end date):** Lessons are created on all valid dates **up to and including** the specified end date. If the end date falls on a closed date AND Skip Closed Date = ON, no lesson is created on that date — the last lesson is the closest valid date before it. The Lesson Schedule's stored end date still shows the user-specified date.
- **"End by After" (lesson count):** Exactly N lessons are created. If Skip Closed Date = ON, the system generates exactly N lessons by skipping closed dates, extending the chain further into the future as needed.
- **Maximum N:** Import is capped at 500 lessons. Direct creation: 50 is accepted; no lower documented maximum.
- **Lesson Schedule end date is always dynamic.** It always derives from the **last lesson's date** in the chain, not from the user's original input:

| Action                                          | Schedule End Date Effect                                       |
| ----------------------------------------------- | -------------------------------------------------------------- |
| Add a lesson with date > current last           | End date **expands** to that lesson's date                     |
| Add a lesson with date < current first          | **Start** date also updates to that lesson's date              |
| Delete the **last** lesson                      | End date moves back to the new last lesson's date              |
| Delete a **middle** lesson                      | End date **unchanged** (last lesson hasn't moved)              |
| "This and Following" shifts dates forward       | End date updates to the new last lesson's date                 |
| End date itself falls on closed date (skip=ON)  | No lesson on end date; last lesson = last valid date before it |
| End date itself falls on closed date (skip=OFF) | Lesson **IS** created on that closed date                      |

**Extend Recurring Lesson feature:**

- "Extend Recurrence" button auto-fills new start date as `current_end_date + 7 days` (non-editable).
- User sets either a **new end date** (must be **later** than current) or a **new lesson count** (must be **greater** than current). Equal/earlier values are blocked with a validation error.
- Newly extended lessons are **DRAFT** with no teacher or student pre-assigned.
- Lesson Schedule end date updates across all 5 surfaces: SF Lesson Schedule detail, SF Lesson edit form, SF Calendar related list, BO Lesson detail recurring settings, BO Calendar related list.
- If Skip Closed Dates is ON, closed dates within the extension range are automatically skipped.

#### Closed Date Skipping

**Source:** Closed dates defined in Academic Calendar Items (ACI) linked via Academic Calendar Master to the lesson's **location**. Only that location's closed dates apply.

**When Skip Closed Date = OFF:**

- Recurring lessons land on closed dates without error or warning.
- One-time lessons on closed dates are **always allowed** regardless of the Skip setting.
- "Add Lesson" (manually from Lesson Schedule detail) on a closed date is **always allowed**.

**When Skip Closed Date = ON:**

- Any potential lesson date matching a closed date is entirely skipped — no lesson created, no code gap.
- For "End by After N", the chain extends further in time to produce exactly N lessons.
- For "End by On", the chain stops at the last valid date before (or on) the end date.
- The Skip Closed Dates flag is **set at creation time and is non-editable** afterward — inherited by edit and Extend Recurring operations.

**Non-retroactive behavior:**

- Adding, editing, or deleting a closed date (ACI) **does NOT retroactively adjust** any existing lessons. Only new lesson creation or "This and Following" edits respect the updated closed dates.
- Closed date added after lessons already exist on that date → those lessons remain unchanged.
- Closed date deleted after lessons were previously skipped → no lessons are retroactively added back.

**"This and Following" edits + Closed Dates:**

- Skip=ON: Following lessons recalculated from new date, closed dates re-skipped forward.
- Skip=OFF: Following lessons recalculate but **no** closed date skipping — lessons land on closed dates.
- When a "This and Following" generates a date that already has a manually added lesson in the same Lesson Schedule, that auto-generated date is **skipped** (no duplicate created).

**Drag & Drop to a closed date:**

- DnD on SF Calendar is treated as a one-time lesson date change — the system does **NOT** block or warn when dragging to a closed date. Skip Closed Date logic applies only to recurring chain generation, not to individual edits or DnD.

| Scenario                                                              | Behavior                                             |
| --------------------------------------------------------------------- | ---------------------------------------------------- |
| All dates in recurrence window are closed (skip=ON, "End by On")      | No lessons created at all                            |
| All dates in recurrence window are closed (skip=ON, "End by After N") | Chain extends until N valid dates are found          |
| One-time lesson set to closed date                                    | Allowed; lesson created normally                     |
| Edit single lesson date to closed date                                | Allowed; no blocking                                 |
| DnD to closed date on SF Calendar                                     | Allowed; no blocking or warning                      |
| Closed date added after lesson created on that date                   | Existing lesson remains; not retroactively cancelled |

#### Calendar Sync Implications

**Sync direction:** SF is the **source of truth**. SF → BO sync is near real-time. BO Calendar does not support lesson CRUD (teachers use BO to view and to submit reports, not to create/edit/delete lessons).

**Lesson status → Calendar visibility across platforms:**

| Status    | SF Calendar      | BO Calendar | Mobile                    |
| --------- | ---------------- | ----------- | ------------------------- |
| Draft     | Visible          | Visible     | NOT visible               |
| Published | Visible          | Visible     | Visible                   |
| Completed | Visible          | Visible     | Visible (report viewable) |
| Cancelled | Visible (marked) | Visible     | NOT visible               |

Draft → Published syncs to Mobile immediately. Cancelled → Draft removes lesson from Mobile.

**Drag & Drop on SF Calendar:**

- Controlled by the **"Enable Calendar Drag And Drop"** custom setting in SF Lesson Custom Settings. Must be explicitly turned ON — not enabled by default.
- DnD is available in **Weekly and Daily views only**; Month view does not support DnD.
- Calendar grid snaps to **10-minute intervals** — e.g., dragging to 14:07 snaps to 14:10.
- DnD for **one-time lessons**: directly updates date/time, no confirmation popup.
- DnD for **recurring lessons**: triggers the Edit Lesson modal with "Only this / This and following" choice.
- Dropping **outside calendar bounds**: lesson time is NOT updated.
- **Clashing alerts** are re-evaluated on every time change, including DnD.

**Zoom Calendar sync:**

- Zoom links are created and managed on **BO**, not SF. SF sets the Zoom Owner (the teacher who owns the meeting); BO generates the actual Zoom link.
- Editing Zoom Owner ("This and Following"): new links generated for current + future lessons. Previous lessons keep their original links unchanged.
- Zoom links sync to Mobile so students can join from the Learner App.

**Access patterns by login type:**

- **CPU login (teacher, Aver-specific):** Sees only lessons they are assigned to as teacher in BO Calendar.
- **SPU login (CM/Staff):** Sees all lessons at affiliated locations.
- **Other orgs (Renseikai, Nichibei, etc.):** All users follow affiliation-based location access.
- A teacher assigned to a lesson at a different location can still see it in their BO Calendar.

**Multiple Classes on Calendar:**

- A single lesson can have **multiple classes assigned**, auto-enrolling students from all classes.
- Both SF and BO Calendar display lessons with multiple classes. Feature-flagged — not all orgs.

**Non-obvious behaviors:**

| Behavior                        | Detail                                                                                                                                                  |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DnD requires explicit config ON | "Enable Calendar Drag And Drop" flag must be set                                                                                                        |
| 10-minute snap granularity      | Cannot set lesson to arbitrary minute via DnD                                                                                                           |
| BO Calendar: bulk attendance    | Renseikai-specific; 34 test cases; not universal                                                                                                        |
| Closed dates visually marked    | SF Calendar (18 cases) and BO Calendar (4 cases) both display closed dates                                                                              |
| Calendar student/teacher lists  | Clicking a lesson in SF Calendar opens popup with 3 embedded lists (Student, Teacher, Reallocation); actions from here trigger the full LA/Report chain |
| No CRUD from BO Calendar        | BO Calendar is read-only for lesson content; navigation only                                                                                            |

#### Edit Rules for Recurring Lessons

- **"Only this lesson"** — edits the selected lesson only
- **"This and the following lessons"** — edits selected + all subsequent lessons in the chain, skipping Completed/Cancelled lessons
- Closed date logic re-applies during edit
- Course schedule: lesson date must match correct week order; cross-week edits blocked

#### Dual Lesson (EEA)

Paired Lesson Schedules across two locations (Partner Lesson). A "related LS" links LS at Location 1 with LS at Location 2. Creates a bidirectional pairing between lesson schedules.

#### Lesson Zoom

Zoom integration for online/hybrid lessons:

| Zoom Type         | Description                                            |
| ----------------- | ------------------------------------------------------ |
| **Single Zoom**   | One Zoom link per lesson                               |
| **Multiple Zoom** | Multiple Zoom links per lesson (one per student/group) |

- **Zoom Owner:** The teacher who owns the Zoom meeting. Start/end dates derive from lesson dates.
- **Zoom Participant:** Students added to Zoom meetings via Student Session.
- Recurring lesson: editing Zoom Owner regenerates links for current + following lessons; old lessons keep old links.
- Zoom links sync to BO and are joinable from BO and Mobile.

#### Lesson Report

- Auto-created with **Draft** status when a lesson is created
- Tied to lesson and student (Lesson Report Detail per student)
- **SF → BO → Mobile** sync
- Teacher submits/publishes report on BO
- Student/Parent views published report on Mobile
- Aver customization: extended report fields, subject-based reports

#### Lesson on Mobile (Learner App)

- Students/Parents see **Published** lessons only
- View lesson details, materials
- Join Zoom meetings for zoom/online lessons
- Submit attendance (student self-attendance) and receive notifications on attendance changes
- View lesson reports after teacher publishes
- Receive notifications on lesson date/time changes

---

### 2.1.1 Lesson Student Session

The Student Session is the link between a Student and a Lesson. It represents a student's participation in a specific lesson.

#### Entity Fields

| Field                 | Description                                                      |
| --------------------- | ---------------------------------------------------------------- |
| **Student**           | The enrolled student                                             |
| **Lesson**            | The lesson instance                                              |
| **Attendance Status** | Present / Absent / Late / Leave Early                            |
| **Lesson Allocation** | The LA record that authorizes this assignment                    |
| **New Flag**          | Indicates newly assigned student (3 cases)                       |
| **Risk Flag**         | Flags at-risk students based on attendance/performance (9 cases) |
| **Trial Flag**        | Marks trial students (20 cases)                                  |

#### Assignment Methods

| Method                          | Description                                                                                                                                                                                     |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Add Student (manual)**        | Staff manually adds student on Lesson Detail (70 cases). Student must have LA with `Require Allocation = True`.                                                                                 |
| **Class-based auto-assignment** | Students auto-assigned via Class Member when class is assigned to lesson (118 cases total). Triggered by: create/import lesson, assign class, update LA duration, update lesson schedule class. |
| **Reallocation**                | Move student from one lesson to another (23 cases). LA and point consumption recalculated.                                                                                                      |
| **Import**                      | Bulk assign via CSV import (3 cases)                                                                                                                                                            |

**Recurring lesson scope — when assigning or unassigning a student from a recurring lesson, the system presents a scope selection:**

| Option                             | Assign Behavior                                                                                                                                       | Unassign Behavior                                                                                          |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Only this lesson**               | Student added to the selected lesson only                                                                                                             | Student removed from the selected lesson only; LA Lesson Allocated decrements by 1                         |
| **This and the following lessons** | Student added to selected + all subsequent lessons in the chain                                                                                       | Student removed from selected + all subsequent; LA Lesson Allocated decrements by count of removed lessons |
| **Apply to Next X Lessons**        | Student added to selected lesson + next X lessons in the chain. If remaining lessons < X, assigns to all remaining instead (confirmation alert shown) | —                                                                                                          |

**Recurring assignment rules:**

- **Completed and Cancelled lessons are always skipped.** "This and the following" never assigns to or removes from Completed/Cancelled lessons. Add Student and Remove Student buttons are **disabled** on Completed lessons.
- **Duplicate prevention.** If a student is already assigned to some lessons in the chain, "This and the following" skips those — no duplicate sessions created.
- **Out-of-LA-duration warning.** If the student's LA duration does not cover some lessons in the following chain, the assignment still proceeds but a **warning indicator** is shown on those specific lessons.
- **Extend Recurring + "This and following".** If "This and following" is applied from a lesson before the extension point, the assignment spans into the extended lessons as well. If applied from within the extended range, only extended following lessons are affected.
- **LA Lesson Allocated count** increments by the exact number of new sessions created across all assigned lessons (not just 1 per action).
- **Manual lessons within a schedule.** A manually added lesson within the recurring chain IS included when using "This and the following" — it is not excluded.
- **Over-assignment.** If `current Assigned Sessions + new assignments > Total Session Count`, the system shows an Over Assigned alert and requires confirmation before proceeding; LA status updates to "Over Assigned".

#### Student Filter Rules

When adding a student manually, the filter requires:

- Student's **location** = lesson's location (excluding "Closed Down" locations)
- Student has **Lesson Allocation** with `Require Allocation = True`
- Filtered by: affiliation, course, grade, student type, school, academic year

#### Student Name Display

- Format: `Name (Phonetic)/(Nickname)`
- Empty phonetic or nickname fields are hidden — no empty `()` or "Null" shown
- **Sorting:** Japanese characters first (by phonetic reading), then alphabetical, then alphanumeric

#### Interaction with Lesson Allocation

- Assigning a student → LA `Lesson Allocated` count increments, LA status updated, `Report History` updated
- Removing a student → LA count decrements, Lesson Report Detail record removed
- When lesson is deleted → all student sessions removed, LA updated accordingly

#### Interaction with Calendar

- Calendar SF shows **Student List** within each lesson detail (contextual list)
- **Reallocation List** on Calendar shows students moved between lessons
- Student count visible on Calendar lesson cards

---

### 2.1.2 Lesson Teacher

The Lesson Teacher is the link between a Teacher and a Lesson. It determines who teaches the lesson and controls BO Calendar visibility.

#### Entity Fields

| Field               | Description                                      |
| ------------------- | ------------------------------------------------ |
| **Teacher**         | The staff member assigned as teacher             |
| **Lesson**          | The lesson instance                              |
| **Lesson Schedule** | The chain (for "This and following" assignments) |

#### Assignment Methods

| Method                                            | Description                                                          |
| ------------------------------------------------- | -------------------------------------------------------------------- |
| **Assign on Lesson Detail**                       | Staff assigns teacher from Lesson Detail page (27 cases)             |
| **Assign on Lesson Teacher List**                 | Staff assigns from dedicated Teacher List view (4 cases)             |
| **Import**                                        | Teachers auto-assigned when importing lessons with teacher usernames |
| **Recurring: "Only this" / "This and following"** | Same logic as lesson edits                                           |

#### Teacher Filter Rules

Teachers filtered by:

- **Affiliation** — teacher must have an active affiliation
- **Location** — teacher's affiliated location(s); defaults to lesson's location
- **Working Type** — Full-time / Part-time
- **Subject** — teacher's eligible subjects (used by Riso and other orgs)
- **Working Hours** — teacher's scheduled working time

#### Clashing Alert (34 cases)

Time overlap detection between lessons assigned to the same teacher:

- `L1.end = L2.start` → **No clash** (adjacent, not overlapping)
- `L1.start = L2.start` → **Clash** (same start time = overlap)
- Any proper time overlap → **Clash** shown in Confirm popup AND Remark field on Lesson Detail
- Clashing alerts check across all lessons, regardless of location
- Alerts are recalculated on every time change (create, edit, drag & drop)

#### Cross-Location Access

- Teachers can be assigned to lessons at **different locations** from their affiliation (triggers an alert but is allowed)
- Once assigned, the teacher retains access to the lesson even if students from their location are removed (51 cases: "View from another location")
- CPU login (teacher) → sees only lessons they're assigned to on BO Calendar
- SPU login (CM/staff) → sees all lessons at their affiliated locations

#### Interaction with Calendar

- Calendar SF shows **Teacher List** within each lesson detail (contextual list)
- **Clashing Alert** shown on both Calendar view and Lesson Detail
- Teacher name visible on Calendar lesson cards
- BO Calendar filters lessons by teacher (CPU) or by location (SPU)

---

### 2.2 Calendar

Calendar provides a visual view of lessons and events across time. Exists on both SF and BO.

#### Calendar on SF (560 test cases)

| Feature                               | Cases | Description                                                   |
| ------------------------------------- | ----: | ------------------------------------------------------------- |
| **Lesson CRUD on Calendar**           |   151 | Create/Read/Update/Delete lessons directly from calendar view |
| **Calendar View**                     |   144 | Day/Week/Month views; filter by location, teacher, student    |
| **Student/Teacher/Reallocation List** |   114 | Contextual lists within calendar lesson detail (see below)    |
| **Drag & Drop**                       |    44 | Move/resize lessons on the calendar timeline                  |
| **Change Lesson**                     |    11 | Change lesson details from calendar context                   |
| **Clashing Alert**                    |    33 | Teacher time conflict warnings on calendar                    |
| **Events on Calendar**                |    51 | Activity events shown on SF calendar                          |
| **Multiple Classes**                  |     8 | Handle lessons with multiple class assignments                |
| **Calendar Filter**                   |     1 | Filter configuration                                          |

#### Student/Teacher/Reallocation List on Calendar (114 cases) — Core Feature

This is a **core feature** of the SF Calendar. When a user clicks on a lesson in the Calendar view, the lesson detail popup shows three contextual lists that integrate deeply with other entities:

**Student List:**

- Shows all students assigned to the lesson (via Student Session)
- Displays: student name, attendance status, Lesson Allocation info
- Staff can **add/remove students** directly from the Calendar lesson detail
- Adding a student triggers: Student Session creation → LA update (Lesson Allocated + status) → Lesson Report Detail auto-created
- Removing a student triggers: Student Session deletion → LA update → Lesson Report Detail removed
- If the student has point-consuming LA (Nichibei), points are consumed/refunded on add/remove

**Teacher List:**

- Shows all teachers assigned to the lesson (via Lesson Teacher)
- Staff can **assign/unassign teachers** directly from the Calendar lesson detail
- Assigning a teacher triggers clashing alert check against all other lessons
- Teacher name appears on the Calendar lesson card for quick visibility

**Reallocation List:**

- Shows students who have been **reallocated** (moved) to/from this lesson
- Displays the source/target lesson for each reallocation action
- Staff can initiate **reallocation** from the Calendar — move a student from one lesson to another
- Reallocation triggers: Student Session moved → LA updated → Point consumption recalculated (Nichibei)

**Cross-entity interactions from Calendar lists:**

- **Calendar → Lesson:** CRUD lesson directly from Calendar
- **Calendar → Student Session:** Add/remove students from lesson
- **Calendar → Lesson Teacher:** Assign/unassign teachers
- **Calendar → Lesson Allocation:** LA count updated when students added/removed
- **Calendar → Lesson Report:** Report detail auto-created/removed when students added/removed
- **Calendar → Point Consumption:** Points consumed/refunded when students added/removed (Nichibei)
- **Calendar → Clashing Alert:** Teacher time conflict checked on teacher assignment

#### Calendar on BO (224 test cases)

| Feature                    | Cases | Description                                           |
| -------------------------- | ----: | ----------------------------------------------------- |
| **Calendar Filter**        |    37 | Filter by location, teacher, date range               |
| **Calendar View**          |    67 | Day/Week/Month views                                  |
| **Events on Calendar**     |    51 | Activity events from Event Master                     |
| **Lesson View**            |    35 | View lesson details from calendar                     |
| **Bulk Update Attendance** |    34 | Renseikai: bulk collect attendance from calendar view |

#### Calendar Access by User Type

| User Type      | Login Type          | Access Method                     |
| -------------- | ------------------- | --------------------------------- |
| PT Teacher     | CPU (teacher login) | Get lesson by **lesson teacher**  |
| Teacher        | CPU                 | Get lesson by **lesson teacher**  |
| Centre Manager | SPU (staff login)   | Get lesson by **lesson location** |
| HQ Staff       | SPU                 | Get lesson by **lesson location** |
| Centre Staff   | SPU                 | Get lesson by **lesson location** |
| Brand Staff    | SPU                 | Get lesson by **lesson location** |

**Access behavior by organization:**

- **Aver:** CPU users (teachers) see only lessons they're assigned to as teacher. SPU users see lessons at their affiliated locations. This CPU/SPU distinction is Aver-specific.
- **Other partners (Renseikai, Nichibei, Aso, etc.):** All users follow **affiliation-based location access** — they see lessons at locations they are affiliated with, regardless of CPU/SPU login type.

---

### 2.3 Event

Events are activities managed via Event Master, scheduled for students, and displayed on Calendar.

#### Event Master (568 test cases)

The master record defining an event template. Contains event details, target segments, participant rules.

| Feature                    | Cases | Description                                                 |
| -------------------------- | ----: | ----------------------------------------------------------- |
| **Creating Event Master**  |    15 | Create event templates                                      |
| **Editing Event Master**   |     5 | Modify event details                                        |
| **Deleting Event Master**  |     4 | Remove event records                                        |
| **Searching Event Master** |     2 | Find events                                                 |
| **Importing**              |     2 | CSV import                                                  |
| **Master Record Details**  |    95 | Record page with participant/staff lists and related events |

#### Target Segments

Define who can participate in an event:

| Segment Type        | Operations                       |
| ------------------- | -------------------------------- |
| **Target Location** | Create (7), Edit (4), Delete (3) |
| **Target School**   | Create (6), Edit (4), Delete (3) |
| **Target Grade**    | Create (6), Edit (4), Delete (3) |
| **Target Course**   | Create (6), Edit (4), Delete (3) |

#### Activity Event (64 test cases)

Individual event instances created from Event Master:

- Creating (22), Editing (3), Deleting (3), Importing (2)
- Status changes (7), Download participants (1), Reports (2)
- Edit response/attendance (3), Event history (2)
- **Learner App Activity Card** (14): students interact with events on mobile — Accept/Decline (4), Cancel (3)

#### Booking System (201 test cases)

Reservation and booking for events:

| Type                 | Cases | Description                      |
| -------------------- | ----: | -------------------------------- |
| **Internal Booking** |    93 | Staff reserve slots for students |
| **External Booking** |   108 | External link for self-booking   |

Sub-features: Reserve by target segment (22), Notification (3), Remove price (3), External link (4), Koyu Auto Create Application (51).

#### Koyu Event Features

- **Koyu Auto Create Application** (51 cases): Auto-generate application records for event participants
- **Koyu Cancel Booked Event** (68 cases): Cancel event bookings with business rules
- **Update Cancel Booked Event** (65 cases): Modify cancellation records (10 user stories)
- **Koyu Draft Status** (19 cases): Handle draft status for event bookings (5 user stories)

#### Events on Calendar

Events appear on both SF Calendar (51 cases) and BO Calendar (51 cases), showing event schedules alongside lessons. Staff assigned to events see them on their SF Calendar view (7 cases).

---

## 3. Cross-Domain Interactions

### 3.1 Lesson ↔ Calendar

```
Lesson (SF) ──create/edit──→ Calendar (SF) ──view──→ Calendar (BO)
                                  │
                                  ├── Drag & Drop to reschedule
                                  ├── Click to view/edit lesson detail
                                  ├── Teacher clashing alerts
                                  └── Filter by location/teacher/student
```

- Lessons created on SF auto-appear on SF Calendar and sync to BO Calendar
- Calendar provides visual management: drag-and-drop reschedule, click-to-edit
- Teacher clashing alerts show on both Calendar and Lesson detail
- Calendar views filter lessons by the user's access level (CPU sees own lessons, SPU sees location lessons)

### 3.2 Lesson ↔ Event

```
Event Master ──creates──→ Activity Event ──shown on──→ Calendar (SF + BO)
                               │
                               ├── Assign staff ──→ staff sees on SF Calendar
                               ├── Assign students ──→ students see on Mobile
                               └── Booking system ──→ reserves slots
```

- Events and Lessons coexist on the Calendar
- Events can assign staff (teachers) who then see them on their calendar, similar to lesson teacher view
- Students see assigned events on Mobile Learner App
- Both events and lessons respect location-based access control

### 3.3 Lesson ↔ Student: Core Lesson Allocation (LA)

The Lesson Allocation is the **authorization record** that allows a student to be assigned to lessons. It answers: "Does this student have the right to attend lessons for this course?"

```
Order Group (SF) ──→ Student Product Offering (SPO) ──→ Lesson Allocation (LA)
                                                              │
                                                              ├── Require Allocation: True → used to assign student to lesson
                                                              ├── Require Allocation: False → used for point calculation only
                                                              ├── Duration (start/end dates)
                                                              ├── Lesson Allocated (count)
                                                              ├── Lesson Allocation Status
                                                              └── Report History
```

#### Core LA Fields

| Field                        | Description                                                                                                                                                                                                        |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Require Allocation**       | `True` = student CAN be assigned to lessons via this LA. `False` = LA exists for **point calculation only**, student cannot be assigned via this LA.                                                               |
| **Duration**                 | Start and end dates defining when this LA is valid                                                                                                                                                                 |
| **Lesson Allocated**         | Count of lessons this student is currently assigned to                                                                                                                                                             |
| **Lesson Allocation Status** | **None Assigned** (Lesson Allocated = 0) / **Partial Assigned** (0 < Allocated < Total Session Count) / **Fully Assigned** (Allocated = Total Session Count) / **Over Assigned** (Allocated > Total Session Count) |
| **Report History**           | List of student reports for this LA, sorted by date                                                                                                                                                                |
| **Course**                   | The course this LA authorizes                                                                                                                                                                                      |

#### LA Lifecycle (Mirrors Order Lifecycle)

**Creation triggers:**

| Trigger                                      | LA Effect                                                                                                                                                            |
| -------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **New Order Group** (new enrollment)         | LA created per course where `Require Allocation = True`. Start date = order start date. End date = order end date. Total session count = 0.                          |
| **Enrollment Order** (application)           | Same rules as New Order Group                                                                                                                                        |
| **Add New Associated Course** (update order) | New LA created with start date = effective date. Other existing LAs unchanged. Effective date must be ≥ product start date. Past effective dates allowed (PBT-1859). |
| **Import Order via CSV**                     | LA created with same rules as manual order                                                                                                                           |

**Update triggers:**

| Trigger                                          | LA Effect                                                                                                                                                                                                               |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Change Course** (update order, replace course) | Old course LA: end date = effective date. New course LA: created with start date = effective date. Both co-exist until effective date if it is in the future.                                                           |
| **Update Slot** (update order)                   | Purchased slot updated on LA. LA duration (start/end) unchanged. Total session count recalculated. No student session auto-created.                                                                                     |
| **Cancel Product** — Schedule or Frequency type  | LA end date updated = effective date (cancel date). Students removed from lessons outside new duration. Class member end date updated. Completed/cancelled past lessons remain visible. Past effective dates supported. |
| **Cancel Product** — Slot-Based or One-Time type | LA is **deleted** entirely. Students removed from all associated lessons.                                                                                                                                               |
| **Withdrawal Application**                       | LA end date = last attendance day. Students removed from lessons outside the new range. Lesson reports of removed students hidden. Lesson Allocated, Status, Report History updated. Cancel withdrawal → LA reverted.   |
| **LOA Application**                              | LA end date = last attendance day. Students removed from lessons outside the new range. Cancel LOA → LA reverted. Resume LOA → new LA created from resume date. Cancel resume LOA → new LA deleted.                     |

**Deletion / restoration triggers:**

| Trigger                                                        | LA Effect                                       |
| -------------------------------------------------------------- | ----------------------------------------------- |
| **Void New Order**                                             | LA deleted entirely                             |
| **Void Update Order** — slot change                            | LA slot reverts to previous value               |
| **Void Update Order** — course change (effective date = start) | Old LA restored; new LA deleted                 |
| **Void Update Order** — course change (effective date > start) | New LA deleted; old LA end date restored        |
| **Void Update Order** — add associated course                  | Added course LA deleted; original LAs unchanged |
| **Void Cancel Order**                                          | LA restored to its state before cancellation    |

**Special cases:**

- **Monthly product type** → LA is **NOT created** (regardless of Require Allocation setting)
- **`Require Allocation = False`** → LA is **NOT created**; LA is not updated when slot changes
- **Multiple product offerings for same student** → separate LAs created per product, counted independently
- **Multiple courses per product** → separate LA per course (all with `Require Allocation = True`)
- **Multiple LAs with same course and duration** → allowed; counted independently
- **Missing Lesson Allocation Week (LAW)** → LA created, but total session count depends on LAW availability
- **LA duration outside any week order** → LA created; session count = 0

#### LA Impact on Student Session

- Student can only be assigned to a lesson if they have an LA with `Require Allocation = True` for the lesson's course
- When LA is deleted (order voided/cancelled), all student sessions linked to that LA are removed
- When LA duration is updated, class-based auto-assignment is re-triggered (students may be added/removed from lessons)

### 3.4 Student ↔ Class ↔ Lesson (Auto-Assignment)

```
Student ──enrolled in──→ Course ──→ Class ──→ Class Member (with duration)
                                                    │
                                 ┌──────────────────┘
                                 ↓
                          Run Master Queue
                                 │
                    ┌────────────┼────────────┐
                    ↓            ↓            ↓
              Assign student  Remove student  Remain in
              to lesson       from lesson     completed
              (within class   (outside class  lessons
              member duration) member duration)
```

Triggers for class-based auto-assignment:

1. Create/Import new lesson
2. Assign a class to student
3. Update LA duration
4. Update lesson schedule class

### 3.5 Teacher ↔ Lesson ↔ Calendar

```
Teacher (SF) ──assign to──→ Lesson ──→ Calendar
                                │
                                ├── Clashing Alert (time overlap detection)
                                ├── View from another location (51 cases)
                                └── CPU Login ──→ BO Calendar (own lessons only)
```

Teachers from different locations can still access lessons if they're assigned, even after students from their location are removed.

### 3.6 Nichibei Lesson Allocation — Point Consumption Model (221 cases)

Nichibei extends Core LA with a **point-based consumption system**. Instead of just counting lessons, each lesson assignment deducts "points" from the student's allocation. This enables flexible scheduling where different courses cost different amounts of points.

#### 3.6.1 Architecture

```
Course Category (Point_Consumption_Value__c)
    └── Course Master (inherits category, General_Flag__c)
         └── Lesson Allocation (Consumed/Remaining Points, Priority__c, Duration)
              └── Student Session (lesson assigned) ──→ Consume Points
```

**Key difference from Core LA:** In Core LA, the system only tracks Lesson Allocated (count). In Nichibei, the system tracks **Consumed Points**, **Remaining Points**, and **Total Remainings**, and uses a priority chain to decide which LA provides the points.

#### 3.6.2 Nichibei LA Fields (in addition to Core LA fields)

| Field                       | Location                          | Description                                                                                      |
| --------------------------- | --------------------------------- | ------------------------------------------------------------------------------------------------ |
| **Consumed Points**         | LA record                         | Number of points already consumed across all assigned lessons                                    |
| **Remaining Points**        | LA record                         | `Total_Remainings - Consumed_Points`                                                             |
| **Total Remainings**        | LA record                         | Total points allocated to this LA                                                                |
| **Priority**                | LA record (`Priority__c`)         | Boolean. When `True`, this LA is preferred in the consumption chain                              |
| **General Flag**            | Course Master (`General_Flag__c`) | When `True`, this course's LA can provide points for **any** course's lesson (not just matching) |
| **Point Consumption Value** | Course Category                   | The number of points consumed per lesson session for courses in this category                    |

#### 3.6.3 The Two Types of LA in Nichibei

A Nichibei student typically has BOTH types:

| LA Type           | Require Allocation | Purpose                                     | Appears in Add Students popup | Used for Points |
| ----------------- | ------------------ | ------------------------------------------- | ----------------------------- | --------------- |
| **Assignment LA** | `True`             | Authorize student to be assigned to lessons | Yes                           | No              |
| **Point Pool LA** | `False`            | Provide points for consumption              | No                            | Yes             |

**Example:** Student has:

- LA-A: Math course, RA=True → student can be **assigned** to Math lessons
- LA-B: General Studies, RA=False, General Flag=True → **provides points** for any course
- LA-C: Math course, RA=False, Priority=True → **priority point source** for Math lessons

When assigning to a Math lesson: LA-A authorizes the assignment, then the system selects LA-C for points (Priority+Matching) over LA-B (non-Priority+General).

#### 3.6.4 Point Consumption Algorithm (Step by Step)

When a staff assigns a student to a lesson:

**Step 1 — Find Assignment LA:**

- System looks for LA with `Require Allocation = True` matching the lesson's course
- If none found → student does NOT appear in "Add Students" popup

**Step 2 — Validate Duration:**

- The **Point LA's** date range must cover the lesson date
- If invalid → **error; assignment blocked**

**Step 3 — Find Point LA:** (evaluated in strict order)

| Priority | Condition                                              | Description                       |
| -------- | ------------------------------------------------------ | --------------------------------- |
| **1st**  | `Priority = True` AND course matches lesson's course   | Priority + exact course match     |
| **2nd**  | `Priority = True` AND `General Flag = True` on course  | Priority + general-purpose course |
| **3rd**  | `Priority = False` AND course matches lesson's course  | Standard + exact course match     |
| **4th**  | `Priority = False` AND `General Flag = True` on course | Standard + general-purpose course |

Only LAs with `Require Allocation = False` are considered as Point LAs.

**Step 4 — Consume Points:**

- `Points consumed = Course Category's Point_Consumption_Value`
- `LA.Consumed_Points += Point_Consumption_Value`
- `LA.Remaining_Points -= Point_Consumption_Value`

#### 3.6.5 Concrete Priority Examples

**Setup:** Student has 3 Point LAs (all RA=False):

- LA-1: Course = Math, Priority = True, Remaining = 10pts
- LA-2: Course = General Studies (General Flag = True), Priority = False, Remaining = 5pts
- LA-3: Course = Math, Priority = False, Remaining = 8pts

| Scenario                                    | Evaluation                                                                      | Selected |
| ------------------------------------------- | ------------------------------------------------------------------------------- | -------- |
| Assign to Math lesson                       | LA-1 matches (Priority=True + course match → 1st)                               | **LA-1** |
| LA-1 expired (lesson outside LA-1 duration) | LA-3 (Priority=False + match → 3rd) beats LA-2 (Priority=False + General → 4th) | **LA-3** |
| Assign to Science lesson (no match LA)      | LA-2 only option (Priority=False + General → 4th)                               | **LA-2** |
| All Priority LAs expired, no match          | LA-2 (General fallback)                                                         | **LA-2** |

#### 3.6.6 Error Scenarios

| Scenario                                         | Result                                                   |
| ------------------------------------------------ | -------------------------------------------------------- |
| LA duration valid but **no Point LA found**      | Error → student cannot be assigned                       |
| LA duration **invalid** but Point LA exists      | Error → assignment blocked                               |
| RA=True LA valid but no RA=False Point LA        | Error → no point source available                        |
| Insufficient remaining points                    | Depends on config — may allow over-consumption or block  |
| Over-assignment (Assigned > Total Session Count) | Alert shown; user must confirm; status = "Over Assigned" |

#### 3.6.7 Point Refund & Recurring Lessons

| Scenario                                           | Behavior                                                                                                                                                        |
| -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Assign to recurring ("This and following")**     | Points consumed for EACH lesson in the chain within LA duration. If points run out mid-chain, may show error.                                                   |
| **Unassign from single lesson ("Only this")**      | Points refunded for that one lesson. Remaining Points increases.                                                                                                |
| **Unassign from recurring ("This and following")** | Points refunded for ALL removed lessons in the chain.                                                                                                           |
| **Delete lesson with students**                    | All sessions removed → points refunded for each student.                                                                                                        |
| **Remove student from lesson**                     | Points refunded to the same LA that originally consumed them.                                                                                                   |
| **Reallocation (move between lessons)**            | No point recalculation — reallocation is a session-move only; point consumption is NOT affected.                                                                |
| **LA deleted (order voided)**                      | All sessions removed. Points become irrelevant.                                                                                                                 |
| **LA duration updated**                            | No effect on existing sessions or points. Nichibei does not use class-based auto-assignment, so updating LA duration does NOT remove students or refund points. |

#### 3.6.8 Reallocation Flow (Nichibei-specific — 19+23 cases)

Reallocation in Nichibei involves point recalculation on top of the core move:

**Triggering Reallocation:**

1. Set student's attendance to **"Absent"** on the lesson
2. The **Reallocate checkbox** becomes enabled (only for Absent status — disabled for Attend/Late/Leave Early)
3. Check the Reallocate checkbox → system creates a Reallocation Request:
   - Original Lesson Name/Date populated
   - New Lesson Name/Date = blank (pending)
   - Reallocate Counter = 0, Status = Open
4. LA total session count is recalculated

**Completing Reallocation:**

1. Navigate to LA Detail → Student Session → select reallocated session
2. Open Reallocate popup → shows available target lessons
3. Select target lesson → confirm
4. System performs:
   - Points **refunded** to source LA
   - Student removed from original lesson
   - Student assigned to target lesson
   - Points **consumed** from target LA (via priority chain — may be a different LA)
   - Reallocation Request updated: New Lesson populated, Counter incremented, Status = Completed

**Cancelling Reallocation:**
| Action | Result |
|--------|--------|
| Change attendance back to Attend/Late | Reallocate checkbox auto-unchecked; request removed |
| Manually uncheck Reallocate | Request removed from Reallocation list |
| Remove student from lesson | Request and session both removed |

#### 3.6.9 Trial Lesson (20 cases)

Trial LA is a special type that differs from Regular LA:

| Aspect                  | Regular LA                     | Trial LA                                                                 |
| ----------------------- | ------------------------------ | ------------------------------------------------------------------------ |
| **Creation**            | Through Order Group submission | Through **Trial Lesson Application** in SF (Draft → Submitted)           |
| **Type field**          | Trial                          | Trial                                                                    |
| **Purchased Slot edit** | Not editable via UI            | Editable **only upward** (can increase, cannot decrease or keep same)    |
| **Calendar indicator**  | No special marker              | **"Trial Student" dot** on lesson card                                   |
| **Point consumption**   | Normal priority chain          | **No point calculation** — Trial lessons do not consume or refund points |
| **Lesson assignment**   | Appears in Add Students popup  | Also appears in Add Students popup with `LA type = Trial`                |

#### 3.6.10 Limit Teacher (6 cases)

Config: `lesson.limit_teacher_access_other_lessons.is_enabled` (Nichibei-specific)

When enabled:
| BO Area | Behavior |
|---------|----------|
| **Lesson List** | Teacher sees only own lessons; Teacher Name filter auto-set and **disabled** |
| **Calendar** | "Show my Schedule" checked and **disabled** |
| **Calendar Teacher Filter** | Disabled; cannot search other teachers' lessons |
| **Lesson Detail** | Can only open own lessons |
| **SPU users** | Unaffected — retain location-based access |

#### 3.6.11 Lesson Syllabus (24 cases)

Links lesson codes to syllabus descriptions automatically:

```
Syllabus Master → Syllabus Detail (Code + Description)
    └── Associated to → Course Master
         └── Lesson (lesson_code maps to syllabus_code → auto-fill description)
```

| Scenario                                  | Behavior                                                  |
| ----------------------------------------- | --------------------------------------------------------- |
| Create lesson with code matching syllabus | Syllabus description **auto-filled**                      |
| Lesson code has no match                  | Description = blank                                       |
| Edit lesson code                          | Description **not re-looked up** (unchanged)              |
| Change syllabus master on course          | Only **new** lessons use new syllabus; existing unchanged |
| Extend Recurring                          | New lessons auto-fill from lesson code mapping            |

Visible on: SF Lesson Detail, BO Lesson Detail, BO Calendar, Mobile App.

#### 3.6.12 Point Consumption Report (6 cases)

Report shows per-student point tracking:

| Column                       | Description                  |
| ---------------------------- | ---------------------------- |
| Student Name                 | Grouped & sorted ASC         |
| LA                           | All student LAs              |
| Course Name                  | Course tied to LA            |
| Total Purchased Points       | Points allocated             |
| Remaining Points             | Points available             |
| Lesson Date                  | Lessons that consumed points |
| Consumed Points (per lesson) | Points each lesson consumed  |

Filters: location, course, date range, student.

### 3.7 Riso Lesson Allocation — Manual UI Model (105 cases)

Riso extends Core LA in a fundamentally different direction: instead of adding point consumption, Riso allows **manual creation of LAs directly on the UI**, independent of any order flow. This is because Riso's ERP does not use order modules.

#### 3.7.1 Core Difference from Core LA and Nichibei

| Aspect                 | Core LA                                              | Nichibei LA                                  | Riso LA                                                                   |
| ---------------------- | ---------------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------------- |
| **Creation**           | Through order flow only                              | Through order flow only                      | **Manual UI creation** + CSV import (no order needed)                     |
| **Order association**  | Always linked to an order                            | Always linked to an order                    | **No order** — product details, student course ID, package course = empty |
| **Capacity model**     | Lesson Allocated (count)                             | Point consumption (consumed/remaining/total) | **Purchased Slot** (simple counter)                                       |
| **Lifecycle coupling** | Tied to order (void → delete, withdrawal → end date) | Tied to order                                | **Independent** from order lifecycle                                      |
| **LA types**           | From course type                                     | From course type                             | **Regular / Seasonal / Trial** (user-selected)                            |
| **Deletion**           | System-driven (via order void/cancel)                | System-driven                                | **User-driven** on UI (future start date only)                            |
| **Require Allocation** | Set via order product config                         | Set via order product config                 | Always **TRUE** automatically                                             |
| **Subject on lesson**  | Not present                                          | Not present                                  | **Subject field** (Subject Master lookup)                                 |

#### 3.7.2 Manual LA Creation on UI

Staff accesses **Contact → Course tab → "New Lesson Allocation"** button on SF.

**Creation Form Fields:**

| Field                  | Behavior                                                                                                                                                                                                          |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Academic Year (AY)** | Pre-filled with current active AY; editable dropdown                                                                                                                                                              |
| **Location**           | Pre-filled if student has exactly 1 active enrolled location. Blank if 0 or 2+ enrolled locations. Shows enrolled locations or user's affiliated locations                                                        |
| **Course**             | Selection table loads only after AY + Location are set. Shows Course Masters with both a Course Offering (for AY) and a Location Course (for Location). Supports JP partial search. Reloads on AY/Location change |
| **Type**               | Single-select: **Regular**, **Seasonal**, **Trial**                                                                                                                                                               |
| **Purchased Slot**     | Numeric input (user-entered)                                                                                                                                                                                      |
| **Start Date**         | Date picker; must be before End Date                                                                                                                                                                              |
| **End Date**           | Date picker; must be a **future date** (> today)                                                                                                                                                                  |

Users can **select multiple courses** in one flow → creates multiple LAs at once.

**What gets set automatically:** `Require Allocation = TRUE` (always).

**What stays empty (no order):** Product Detail, Student Course ID, Package Course, Order Remarks.

#### 3.7.3 Validation Rules

| Rule                                              | Error Message                                                                                                                                       |
| ------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| Overlapping dates for same AY + Location + Course | _"The selected course has a duration that overlaps with another instance of the same course created earlier. Please adjust the start or end date."_ |
| End date in the past                              | _"End date must be a future date."_                                                                                                                 |
| Start date ≥ End date                             | _"Start date must be earlier than End date."_                                                                                                       |

#### 3.7.4 Edit LA

| Field              | Edit Rules                                                                                                                   |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| **Start Date**     | Can be changed to any valid date (no forward-only restriction)                                                               |
| **End Date**       | Can be changed to any valid date (no forward-only restriction)                                                               |
| **Purchased Slot** | Editable **only** for **Trial** type LAs, and only to a value **greater than** the original. Regular/Seasonal → not editable |
| **All edits**      | Must re-pass all creation validations (overlap, past end date, start ≥ end)                                                  |

#### 3.7.5 Delete LA

| Condition                          | Behavior                                                                                 |
| ---------------------------------- | ---------------------------------------------------------------------------------------- |
| Start date > today (future)        | Delete button **enabled**; confirmation dialog shown                                     |
| Start date ≤ today (today or past) | Delete button **disabled** (greyed out)                                                  |
| On confirm                         | LA deleted; all allocated lessons **synchronously unlinked** (immediate, not background) |

#### 3.7.6 Purchased Slot — The "Slot" Concept

A **Slot** in Riso represents a lesson enrollment capacity unit — how many lesson sessions a student is entitled to. Unlike Nichibei's point system, Riso uses a simpler counter model.

**Two sources for Purchased Slot:**

| Source                                                | When                                                                                  |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **Manual entry**                                      | At UI creation time; user types the number                                            |
| **Auto-calculated from Contracts** (pending PBT-1812) | `LA.Purchased_Slot = SUM(Contract.Slot)` excluding Cancelled/Voided/deleted contracts |

Auto-calculation is recalculated when: contract updated, new contract added, contract cancelled/voided/deleted.

#### 3.7.7 Order Lifecycle Isolation

UI-created LAs are **explicitly isolated** from order lifecycle triggers:

- **Void order** → does NOT delete UI-created LA
- **Withdrawal** → does NOT update UI-created LA end date
- **LOA** → does NOT adjust UI-created LA dates
- **Cancel** → does NOT affect UI-created LA

This isolation means UI-created LAs persist regardless of any order operations.

#### 3.7.8 Interaction with Student Assignment

| Scenario                                              | Behavior                                                                                                                                         |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| UI-created LA → student appears in Add Students popup | Yes — `require_allocation = TRUE` ensures visibility                                                                                             |
| Calendar student list — LA duration check             | Calendar does **NOT** check LA duration when filtering. Student with UI-created LA **always appears** regardless of lesson date vs LA date range |
| Assign to recurring ("This and following")            | Student assigned to all instances in series                                                                                                      |
| Update LA dates                                       | Does NOT trigger auto-assign/unassign. Existing assignments remain unchanged                                                                     |
| Delete LA                                             | Synchronously unlinks student from ALL lessons (immediate)                                                                                       |
| Trial LA type                                         | Calendar shows **"Trial Student" dot** indicator                                                                                                 |
| First enrollment                                      | Calendar shows **"New Student" dot** indicator                                                                                                   |

#### 3.7.9 Subject in Lesson Detail (25 cases — LT-94698)

Riso adds a **Subject field** (Subject Master lookup) to the lesson detail:

| Property        | Value                                     |
| --------------- | ----------------------------------------- |
| **Type**        | Subject Master lookup (reference field)   |
| **Cardinality** | Single-select (one subject per lesson)    |
| **Required**    | No — optional                             |
| **Position**    | Displayed above Location on lesson detail |

**Where Subject is Displayed:**

| Surface                 | Visible                      |
| ----------------------- | ---------------------------- |
| SF Lesson Detail        | Yes                          |
| SF Calendar Lesson Info | Yes                          |
| BO Lesson Detail        | Yes                          |
| BO Calendar Lesson Info | Yes                          |
| Mobile Learner App      | Yes                          |
| Aver custom pages       | **No** (explicitly excluded) |

**Subject Assignment Methods:**

1. Manual on lesson create/edit — pick from Subject Master lookup
2. CSV import — Subject column mapped to Subject Master
3. No auto-assignment — subject is per-lesson, independent of course

**Constraints:**

- No teacher-subject validation — any teacher can teach any subject
- No course-subject relationship — subject is independent metadata per lesson
- Supports search on SF Lessons list and BO Lesson Management
- Supports filter on SF Calendar, BO Calendar, BO Lesson Management

#### 3.7.10 CSV Import

Same data rules and validations as UI creation. Validation errors are row-level with same error messages. Partial success supported (valid rows imported, invalid rows rejected).

## 4. Customization by Organization

| Organization         | Key Features                                                                                                                   | Cases |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ----: |
| **Aver**             | Extended lesson reports (203), Permission (9), Test prep/Subject (24), Lesson Report corrections (178)                         |   414 |
| **Aso**              | Lesson Survey (12), Student Group (41), Curriculum & Syllabus (219), Class enforcement (7)                                     |   279 |
| **Renseikai/Rensei** | Collect attendance on SF (2) and BO (2), Configure error messages (15), Bulk update attendance (34), Class name uniqueness (8) |    61 |
| **Nichibei**         | Point Consumption (145), Lesson Syllabus (24), Limit Teacher (6), Reallocation (26), Trial Lesson (20)                         |   221 |
| **Withus Juku**      | Lesson/Course (9), Event management (59), Custom event (23)                                                                    |    91 |
| **EEA**              | Acquire Teacher (20), Dual Lesson (40)                                                                                         |    60 |
| **Riso**             | Lesson Allocation management (80), Subject in Lesson Detail (25)                                                               |   105 |
| **Koyu**             | Auto Create Application (51), Cancel Booked Event (68), Update Cancel (65), Draft Status (19)                                  |   203 |

---

## 5. Master Data

| Entity                             | Description                                             | Impact                                                 |
| ---------------------------------- | ------------------------------------------------------- | ------------------------------------------------------ |
| **Academic Calendar Master (ACM)** | Year-based calendar per location; contains Closed Dates | Closed dates skip lesson creation; 94 test cases       |
| **Academic Calendar Item (ACI)**   | Individual closed date entry within ACM                 | Lesson and LA duration calculation                     |
| **Location**                       | Physical center/school                                  | Scopes courses, classes, teachers, students, calendars |
| **Course Master**                  | Course definition; linked to Course Category            | Determines lesson type, point consumption              |
| **Course Category**                | Groups courses; defines Point Consumption value         | Point calculation base                                 |
| **Program Master**                 | Defines week orders for Course Schedule lessons         | Controls course schedule recurrence                    |
| **Class**                          | Group of students within a course at a location         | Auto-assignment of students to lessons                 |
| **Classroom**                      | Physical room at a location                             | Assigned to lessons for capacity                       |
| **Student Group**                  | Custom grouping of students                             | Filtered by location; supports bulk class assign       |

---

## 6. Key Data Relationships

```
Location
├── Academic Calendar Master → Academic Calendar Items (Closed Dates)
├── Course → Class → Class Member (Student)
├── Classroom
├── Teacher (via Affiliation)
└── Student (via Affiliation)

Student
├── Student Product Offering (SPO) → Lesson Allocation (LA)
├── Class Member → auto-assigned to Lessons
└── Student Session → Lesson

Lesson
├── Lesson Schedule (chain)
├── Lesson Report → Lesson Report Detail (per student)
├── Student Session (students)
├── Lesson Teacher (teachers)
├── Zoom Link (online)
└── Calendar (view)

Event Master
├── Target Segments (Location, School, Grade, Course)
├── Master Participants / Master Staff
├── Activity Event → Booking
└── Calendar (view)
```

---

## 7. Test Coverage Summary (4,191 cases)

| Domain                  | Cases |     % |
| ----------------------- | ----: | ----: |
| Lesson Management       | 1,495 | 35.7% |
| Customization           | 1,134 | 27.1% |
| Calendar                |   784 | 18.7% |
| Event Master            |   568 | 13.6% |
| Master Data             |   104 |  2.5% |
| Extend Recurring Lesson |    64 |  1.5% |
| SF Report               |    18 |  0.4% |
| Incident Prevention     |    16 |  0.4% |
| Configuration           |     3 |  0.1% |
| Lesson Master           |     3 |  0.1% |
| Live Lesson             |     2 |  0.0% |
