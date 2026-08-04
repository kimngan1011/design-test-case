# Lesson Teacher

The Lesson Teacher is the link between a Teacher and a Lesson. It determines who teaches the lesson and controls BO Calendar visibility.

## Entity Fields

| Field | Description |
|---|---|
| **Teacher** | The staff member assigned as teacher |
| **Lesson** | The lesson instance |
| **Lesson Schedule** | The chain (for "This and following" assignments) |

## Assignment Methods

| Method | Description |
|---|---|
| **Assign on Lesson Detail** | Staff assigns teacher from Lesson Detail page (27 cases) |
| **Assign on Lesson Teacher List** | Staff assigns from dedicated Teacher List view (4 cases) |
| **Import** | Teachers auto-assigned when importing lessons with teacher usernames |
| **Recurring: "Only this" / "This and following"** | Same logic as lesson edits |

## Teacher Filter Rules

Teachers filtered by:
- **Affiliation** — teacher must have an active affiliation.
- **Location** — teacher's affiliated location(s); defaults to lesson's location.
- **Working Type** — Full-time / Part-time.
- **Subject** — teacher's eligible subjects (used by Riso and other orgs).
- **Working Hours** — teacher's scheduled working time.

### Available Teacher / "Only teachers free at this time"

For substitute teacher candidate search (EN — LT-105350) and Add Teacher popup availability filtering, a teacher is available only when both checks pass:

| Check | Rule |
|---|---|
| Working-hours coverage | The target lesson must be fully covered by a non-Off Day working-hours record from LT-64009: `staff_start_time <= lesson_start_time < lesson_end_time <= staff_end_time`. Use the lesson's displayed local/JST date and time for weekday and time comparison. |
| Existing lesson no-overlap | The teacher must have no existing Draft/Published lesson overlapping the target lesson time in any location. Overlap is `existing_start < target_end AND target_start < existing_end`. Cancelled and Completed lessons are excluded from the conflict set. |
| Adjacent boundary | `existing_end = target_start` or `existing_start = target_end` is adjacent, not overlapping, so it must not exclude the teacher. |

## Clashing Alert (34 cases)

Time overlap detection between lessons assigned to the same teacher:

- `L1.end = L2.start` → **No clash** (adjacent, not overlapping).
- `L1.start = L2.start` → **Clash** (same start time = overlap).
- Any proper time overlap → **Clash** shown in Confirm popup AND Remark field on Lesson Detail.
- Clashing alerts check across all lessons, regardless of location.
- Alerts are recalculated on every time change (create, edit, drag & drop).

## Cross-Location Access

- Teachers can be assigned to lessons at **different locations** from their affiliation (triggers an alert but is allowed).
- Once assigned, teacher retains access to the lesson even if students from their location are removed (51 cases: "View from another location").
- CPU login (teacher) → sees only lessons they're assigned to on BO Calendar.
- SPU login (CM/staff) → sees all lessons at their affiliated locations.

## Interaction with Calendar

- Calendar SF shows **Teacher List** within each lesson detail (contextual list). See `calendar/student-teacher-reallocation-list.md`.
- **Clashing Alert** shown on both Calendar view and Lesson Detail.
- Teacher name visible on Calendar lesson cards.
- BO Calendar filters lessons by teacher (CPU) or by location (SPU).

## Cross-domain: Teacher ↔ Lesson ↔ Calendar

```
Teacher (SF) ──assign to──→ Lesson ──→ Calendar
                                │
                                ├── Clashing Alert (time overlap detection)
                                ├── View from another location (51 cases)
                                └── CPU Login ──→ BO Calendar (own lessons only)
```

Teachers from different locations can still access lessons if they're assigned, even after students from their location are removed.

---

## Monthly Lesson Count (Riso OOP — LT-96673, 2026-04-16)

A custom field on the Lesson Teacher SF object showing how many lessons a teacher is assigned to in a given month. Used by Riso to prevent teacher overwork.

| Surface | Field Label | Reference Period |
|---|---|---|
| SF Lesson Detail — Add Teacher popup | Monthly Lesson Count (今月の授業数) column | Selected lesson's month |
| SF Calendar — Teacher Details panel | Monthly Lesson Count (今月の授業数) field | Today's month (fixed — unaffected by calendar navigation) |

### Count logic

| Property | Rule |
|---|---|
| Statuses included | Draft, Published, Completed |
| Statuses excluded | Cancelled |
| Location scope | ALL locations (cross-location) |
| Zero value | Shows `0` (not blank) |
| Sortability | Not sortable in Add Teacher popup |
| Filter behavior | Applying popup filters does NOT update the count |
| Role access | No restriction — all SF users who can open the popup/panel see the count |

> **⚠️ Timezone risk:** Month boundary must use the lesson date as displayed in the UI (local timezone), NOT the raw UTC stored value. A lesson at 11:30pm JST (Jan 31) is stored as UTC Feb 1 — it must be counted in January. Implementation must derive month from UI local date. Added from LT-96673 (2026-04-16).
