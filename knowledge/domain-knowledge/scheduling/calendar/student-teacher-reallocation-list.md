# Student / Teacher / Reallocation List on SF Calendar (114 cases) — Core Feature

When a user clicks on a lesson in the SF Calendar view, the lesson detail popup shows **three contextual lists** that integrate deeply with other entities. These are NOT separate pages — they live inside the calendar popup.

## Student List

- Shows all students assigned to the lesson (via Student Session).
- Displays: student name, attendance status, Lesson Allocation info.
- Staff can **add/remove students** directly from the Calendar lesson detail.
- Adding a student triggers: Student Session creation → LA update (Lesson Allocated + status) → Lesson Report Detail auto-created.
- Removing a student triggers: Student Session deletion → LA update → Lesson Report Detail removed.
- If the student has point-consuming LA (Nichibei), points are consumed/refunded on add/remove.

## Teacher List

- Shows all teachers assigned to the lesson (via Lesson Teacher).
- Staff can **assign/unassign teachers** directly from the Calendar lesson detail.
- Assigning a teacher triggers clashing alert check against all other lessons.
- Teacher name appears on the Calendar lesson card for quick visibility.

## Reallocation List

- Shows students who have been **reallocated** (moved) to/from this lesson.
- Displays the source/target lesson for each reallocation action.
- Staff can initiate **reallocation** from the Calendar — move a student from one lesson to another.
- Reallocation triggers: Student Session moved → LA updated → Point consumption recalculated (Nichibei).

## Cross-entity interactions from Calendar lists

- **Calendar → Lesson:** CRUD lesson directly from Calendar (see `calendar-sf.md`).
- **Calendar → Student Session:** Add/remove students from lesson (see `../lesson-management/student-session.md`).
- **Calendar → Lesson Teacher:** Assign/unassign teachers (see `../lesson-management/lesson-teacher.md`).
- **Calendar → Lesson Allocation:** LA count updated when students added/removed.
- **Calendar → Lesson Report:** Report detail auto-created/removed when students added/removed.
- **Calendar → Point Consumption:** Points consumed/refunded when students added/removed in Nichibei (see `../partner-rules/nichibei-lesson-allocation.md`).
- **Calendar → Clashing Alert:** Teacher time conflict checked on teacher assignment.
