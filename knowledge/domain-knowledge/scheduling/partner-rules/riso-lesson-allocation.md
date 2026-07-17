# Riso Lesson Allocation — Manual UI Model (105 cases)

Riso extends Core LA in a fundamentally different direction: instead of adding point consumption, Riso allows **manual creation of LAs directly on the UI**, independent of any order flow. This is because Riso's ERP does not use order modules.

## Core Difference from Core LA and Nichibei

| Aspect | Core LA | Nichibei LA | Riso LA |
|---|---|---|---|
| **Creation** | Through order flow only | Through order flow only | **Manual UI creation** + CSV import (no order needed) |
| **Order association** | Always linked to an order | Always linked to an order | **No order** — product details, student course ID, package course = empty |
| **Capacity model** | Lesson Allocated (count) | Point consumption (consumed/remaining/total) | **Purchased Slot** (simple counter) |
| **Lifecycle coupling** | Tied to order (void → delete, withdrawal → end date) | Tied to order | **Independent** from order lifecycle |
| **LA types** | From course type | From course type | **Regular / Seasonal / Trial** (user-selected) |
| **Deletion** | System-driven (via order void/cancel) | System-driven | **User-driven** on UI (future start date only) |
| **Require Allocation** | Set via order product config | Set via order product config | Always **TRUE** automatically |
| **Subject on lesson** | Not present | Not present | **Subject field** (Subject Master lookup) |

## Manual LA Creation on UI

Staff accesses **Contact → Course tab → "New Lesson Allocation"** button on SF.

### Creation Form Fields

| Field | Behavior |
|---|---|
| **Academic Year (AY)** | Pre-filled with current active AY; editable dropdown |
| **Location** | Pre-filled if student has exactly 1 active enrolled location. Blank if 0 or 2+ enrolled locations. Shows enrolled locations or user's affiliated locations |
| **Course** | Selection table loads only after AY + Location are set. Shows Course Masters with both a Course Offering (for AY) and a Location Course (for Location). Supports JP partial search. Reloads on AY/Location change |
| **Type** | Single-select: **Regular**, **Seasonal**, **Trial** |
| **Purchased Slot** | Numeric input (user-entered) |
| **Start Date** | Date picker; must be before End Date |
| **End Date** | Date picker; must be a **future date** (> today) |

Users can **select multiple courses** in one flow → creates multiple LAs at once.

**What gets set automatically:** `Require Allocation = TRUE` (always).

**What stays empty (no order):** Product Detail, Student Course ID, Package Course, Order Remarks.

## Validation Rules

| Rule | Error Message |
|---|---|
| Overlapping dates for same AY + Location + Course | _"The selected course has a duration that overlaps with another instance of the same course created earlier. Please adjust the start or end date."_ |
| End date in the past | _"End date must be a future date."_ |
| Start date ≥ End date | _"Start date must be earlier than End date."_ |

## Edit LA

| Field | Edit Rules |
|---|---|
| **Start Date** | Can be changed to any valid date (no forward-only restriction) |
| **End Date** | Can be changed to any valid date (no forward-only restriction) |
| **Purchased Slot** | Editable **only** for **Trial** type LAs, and only to a value **greater than** the original. Regular/Seasonal → not editable |
| **All edits** | Must re-pass all creation validations (overlap, past end date, start ≥ end) |

## Delete LA

| Condition | Behavior |
|---|---|
| Start date > today (future) | Delete button **enabled**; confirmation dialog shown |
| Start date ≤ today (today or past) | Delete button **disabled** (greyed out) |
| On confirm | LA deleted; all allocated lessons **synchronously unlinked** (immediate, not background) |

## Purchased Slot — The "Slot" Concept

A **Slot** in Riso represents a lesson enrollment capacity unit — how many lesson sessions a student is entitled to. Unlike Nichibei's point system, Riso uses a simpler counter model.

### Slot Concepts: Purchased Slot vs Total Session Count

There are two distinct fields on the Lesson Allocation tracking capacity:

| Field | Description | Source |
|---|---|---|
| **Purchased Slot** | Manually managed by SF users on UI | Manual entry only |
| **Total Session Count** | Automatically aggregated from Riso Contracts | `SUM(contract.total)` for all Active contracts linked to the LA |

- ~~**Auto-calculated from Contracts** (pending PBT-1812) | `LA.Purchased_Slot = SUM(Contract.Slot)` excluding Cancelled/Voided/deleted contracts~~ *(Superseded by LT-98533)*

**Contract Aggregation Rules (LT-98533, 2026-06-19):**
- `LA.Total_Session_Count` = SUM of `contract.total` for all Active contracts linked to the LA.
- `LA.Start_Date` = Earliest `start_date` among all Active contracts.
- `LA.End_Date` = Latest `end_date` among all Active contracts.
- **Logical Deletion**: When the LAST Active contract on an LA is logically deleted, `Total_Session_Count` becomes 0, but `Start_Date` and `End_Date` retain their last known values.

## Order Lifecycle Isolation

UI-created LAs are **explicitly isolated** from order lifecycle triggers:

- **Void order** → does NOT delete UI-created LA.
- **Withdrawal** → does NOT update UI-created LA end date.
- **LOA** → does NOT adjust UI-created LA dates.
- **Cancel** → does NOT affect UI-created LA.

This isolation means UI-created LAs persist regardless of any order operations.

## Interaction with Student Assignment

| Scenario | Behavior |
|---|---|
| UI-created LA → student appears in Add Students popup | Yes — `require_allocation = TRUE` ensures visibility |
| Calendar student list — LA duration check | Calendar does **NOT** check LA duration when filtering. Student with UI-created LA **always appears** regardless of lesson date vs LA date range |
| Assign to recurring ("This and following") | Student assigned to all instances in series |
| Update LA dates | Does NOT trigger auto-assign/unassign. Existing assignments remain unchanged |
| Delete LA | Synchronously unlinks student from ALL lessons (immediate) |
| Trial LA type | Calendar shows **"Trial Student" dot** indicator |
| First enrollment | Calendar shows **"New Student" dot** indicator |

## Subject in Lesson Detail (25 cases — LT-94698)

Riso adds a **Subject field** (Subject Master lookup) to the lesson detail:

| Property | Value |
|---|---|
| **Type** | Subject Master lookup (reference field) |
| **Cardinality** | Single-select (one subject per lesson) |
| **Required** | No — optional |
| **Position** | Displayed above Location on lesson detail |

### Where Subject is Displayed

| Surface | Visible |
|---|---|
| SF Lesson Detail | Yes |
| SF Calendar Lesson Info | Yes |
| BO Lesson Detail | Yes |
| BO Calendar Lesson Info | Yes |
| Mobile Learner App | Yes |
| Aver custom pages | **No** (explicitly excluded) |

### Subject Assignment Methods

1. Manual on lesson create/edit — pick from Subject Master lookup.
2. CSV import — Subject column mapped to Subject Master.
3. No auto-assignment — subject is per-lesson, independent of course.

### Constraints

- No teacher-subject validation — any teacher can teach any subject.
- No course-subject relationship — subject is independent metadata per lesson.
- Supports search on SF Lessons list and BO Lesson Management.
- Supports filter on SF Calendar, BO Calendar, BO Lesson Management.

### Subject on Recurring Lessons (LT-94698, 2026-04-15)

| Scenario | Behavior |
|---|---|
| Create recurring lesson with subject set | All generated lessons in the chain receive the same subject |
| Edit subject "Only this lesson" | Only the selected lesson updated; all others in chain unchanged |
| Edit subject "This and the following" | Selected + following lessons updated; prior lessons unchanged; Completed/Cancelled lessons skipped |
| Add lesson from Lesson Schedule Detail ("Add Lesson") | Subject field blank by default; user can set it manually; does not affect the rest of the chain |
| Extend Recurring — newly extended lessons | Subject is blank (not inherited from prior lessons in chain); user must set manually |
| Duplicate lesson with subject set | Subject pre-filled in the new lesson's create form |

## CSV Import

Same data rules and validations as UI creation. Validation errors are row-level with same error messages. Partial success supported (valid rows imported, invalid rows rejected).

## Lesson Publish Notifications to Teachers (LT-101725, 2026-06-23)

Riso adds two notification paths triggered on lesson publish. Both are gated by a **Lesson Publish Notification config flag** (Riso org only; OFF for all other tenants — AC-03, BR-27).

### Path 1 — Single Publish: SF Chatter Post + Notification Center

**Trigger:** lesson status changes Draft → Published (individual publish action).

**Mechanism:** SF Flow Builder creates a Chatter post on the lesson record.

| Aspect | Behavior |
|---|---|
| **Who is notified** | Each Lesson Teacher where `working_status = Available` AND `working_type IN (Full Time, Part Time)` |
| **Notification mechanism** | Chatter post with @mention → SF Notification Center alert |
| **Post content** | Lesson name, lesson date/time, @mention of each eligible teacher; hyperlink to lesson record (opens in new tab) |
| **Language** | EN or JP based on teacher's SF locale setting |
| **LBAC** | HQ Admin and Centre Manager with LBAC access can **view** the Chatter post but do **NOT** receive the notification center alert (not @mentioned) |
| **Republish** | Each Draft→Published transition creates a **new** Chatter post; previous posts persist |
| **Unavailable teachers** | Working_status=Unavailable → excluded from @mention |

### Path 2 — Bulk Publish: Teacher Email

**Trigger:** Bulk publish action (multi-lesson) from any of 3 surfaces.

| Surface | Email Period Calculation |
|---|---|
| SF Lesson List | `min(lesson_date)` – `max(lesson_date)` in the batch |
| SF Lesson Calendar | Calendar view **Start Date** – **End Date** (not individual lesson dates) |
| BO Lesson Management | `min(lesson_date)` – `max(lesson_date)` in the batch |

| Aspect | Behavior |
|---|---|
| **Who receives email** | Each unique Lesson Teacher where `working_status = Available` AND `working_type IN (Full Time, Part Time)` who has ≥1 Draft→Published lesson in the batch |
| **Email count** | **One email per teacher per bulk publish action** (not per lesson) |
| **Silent skip** | If 0 Draft→Published transitions (all already Published), no email sent, no error |
| **Email failure isolation** | If email send fails, the lesson **remains Published** (not rolled back) |
| **Regression (LT-98532)** | Student push notification fires on the same bulk publish event independently; neither blocks the other |

### Config Flag Behavior

| Config Flag | Single Publish | Bulk Publish |
|---|---|---|
| ON (Riso org) | Chatter post created | Teacher email sent |
| OFF (non-Riso org) | No Chatter post | No teacher email |

### What Does NOT Trigger Notifications

- Bulk publish does NOT create a Chatter post (Path 1 = single publish only)
- Single publish does NOT send an email (Path 2 = bulk publish only)
- No cross-type dedup defined (open question Q1): a lesson single-published then included in a bulk publish may trigger both a Chatter @mention and an email

