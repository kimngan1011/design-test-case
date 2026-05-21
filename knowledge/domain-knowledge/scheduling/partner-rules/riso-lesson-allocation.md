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

### Two sources for Purchased Slot

| Source | When |
|---|---|
| **Manual entry** | At UI creation time; user types the number |
| **Auto-calculated from Contracts** (pending PBT-1812) | `LA.Purchased_Slot = SUM(Contract.Slot)` excluding Cancelled/Voided/deleted contracts |

Auto-calculation is recalculated when: contract updated, new contract added, contract cancelled/voided/deleted.

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
