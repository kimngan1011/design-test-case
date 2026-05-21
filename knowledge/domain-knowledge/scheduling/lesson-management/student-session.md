# Lesson Student Session

The Student Session is the link between a Student and a Lesson. It represents a student's participation in a specific lesson.

See `lesson-allocation.md` for the LA authorization model; see `class-assignment.md` for class-based auto-assignment + multi-class lessons.

## Entity Fields

| Field | Description |
|---|---|
| **Student** | The enrolled student |
| **Lesson** | The lesson instance |
| **Attendance Status** | Present / Absent / Late / Leave Early |
| **Lesson Allocation** | The LA record that authorizes this assignment |
| **New Flag** | Indicates newly assigned student (3 cases) |
| **Risk Flag** | Flags at-risk students based on attendance/performance (9 cases) |
| **Trial Flag** | Marks trial students (20 cases) |

## Assignment Methods

| Method | Description |
|---|---|
| **Add Student (manual)** | Staff manually adds student on Lesson Detail (70 cases). Student must have LA with `Require Allocation = True`. |
| **Class-based auto-assignment** | Students auto-assigned via Class Member when class assigned to lesson (118 cases). See `class-assignment.md`. |
| **Reallocation** | Move student from one lesson to another (23 cases). LA and point consumption recalculated. |
| **Import** | Bulk assign via CSV import (3 cases) |

### Recurring lesson scope

When assigning or unassigning a student from a recurring lesson, the system presents a scope selection:

| Option | Assign Behavior | Unassign Behavior |
|---|---|---|
| **Only this lesson** | Student added to selected lesson only | Student removed from selected only; LA Lesson Allocated decrements by 1 |
| **This and the following lessons** | Student added to selected + all subsequent in chain | Student removed from selected + all subsequent; LA Lesson Allocated decrements by count of removed |
| **Apply to Next X Lessons** | Student added to selected + next X in chain. If remaining < X, assigns to all remaining (confirmation alert) | — |

### Recurring assignment rules

- **Completed and Cancelled lessons are always skipped.** "This and following" never assigns to or removes from Completed/Cancelled. Add Student and Remove Student buttons are **disabled** on Completed lessons.
- **Duplicate prevention.** If student already assigned to some lessons in the chain, "This and following" skips those.
- **Out-of-LA-duration warning.** If LA duration doesn't cover some lessons in the following chain, assignment still proceeds but a **warning indicator** shows on those specific lessons.
- **Extend Recurring + "This and following".** If "This and following" applied from a lesson before the extension point → assignment spans into extended lessons. From within the extended range → only extended following lessons affected.
- **LA Lesson Allocated count** increments by the exact number of new sessions created across all assigned lessons.
- **Manual lessons within a schedule.** A manually added lesson within the recurring chain IS included when using "This and following".
- **Over-assignment.** If `current Assigned Sessions + new assignments > Total Session Count`, shows Over Assigned alert and requires confirmation; LA status updates to "Over Assigned".

## Student Filter Rules (manual add)

- Student's **location** = lesson's location (excluding "Closed Down" locations).
- Student has **Lesson Allocation** with `Require Allocation = True`.
- Filtered by: affiliation, course, grade, student type, school, academic year.

## Student Name Display

- Format: `Name (Phonetic)/(Nickname)`.
- Empty phonetic or nickname fields are hidden — no empty `()` or "Null" shown.
- **Sorting:** Japanese characters first (by phonetic reading), then alphabetical, then alphanumeric.

## Interaction with Lesson Allocation

- Assigning a student → LA `Lesson Allocated` count increments, LA status updated, `Report History` updated.
- Removing a student → LA count decrements, Lesson Report Detail record removed.
- When lesson is deleted → all student sessions removed, LA updated accordingly.

## Interaction with Calendar

- Calendar SF shows **Student List** within each lesson detail (contextual list). See `../calendar/student-teacher-reallocation-list.md`.
- **Reallocation List** on Calendar shows students moved between lessons.
- Student count visible on Calendar lesson cards.
