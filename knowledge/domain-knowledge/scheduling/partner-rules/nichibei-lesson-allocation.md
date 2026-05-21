# Nichibei Lesson Allocation — Point Consumption Model (221 cases)

Nichibei extends Core LA (`../lesson-management/student-session.md` § Core LA) with a **point-based consumption system**. Instead of just counting lessons, each lesson assignment deducts "points" from the student's allocation.

## Architecture

```
Course Category (Point_Consumption_Value__c)
    └── Course Master (inherits category, General_Flag__c)
         └── Lesson Allocation (Consumed/Remaining Points, Priority__c, Duration)
              └── Student Session (lesson assigned) ──→ Consume Points
```

**Key difference from Core LA:** Core LA only tracks Lesson Allocated (count). Nichibei tracks **Consumed Points**, **Remaining Points**, **Total Remainings**, and uses a priority chain to decide which LA provides the points.

## Nichibei LA Fields (in addition to Core LA fields)

| Field | Location | Description |
|---|---|---|
| **Consumed Points** | LA record | Points already consumed across all assigned lessons |
| **Remaining Points** | LA record | `Total_Remainings - Consumed_Points` |
| **Total Remainings** | LA record | Total points allocated to this LA |
| **Priority** | LA record (`Priority__c`) | Boolean. When `True`, this LA is preferred in the consumption chain |
| **General Flag** | Course Master (`General_Flag__c`) | When `True`, this course's LA can provide points for **any** course's lesson (not just matching) |
| **Point Consumption Value** | Course Category | Points consumed per lesson session for courses in this category |

## Two Types of LA in Nichibei

A Nichibei student typically has BOTH types:

| LA Type | Require Allocation | Purpose | Appears in Add Students popup | Used for Points |
|---|---|---|---|---|
| **Assignment LA** | `True` | Authorize student to be assigned to lessons | Yes | No |
| **Point Pool LA** | `False` | Provide points for consumption | No | Yes |

**Example:** Student has:
- LA-A: Math course, RA=True → student can be **assigned** to Math lessons.
- LA-B: General Studies, RA=False, General Flag=True → **provides points** for any course.
- LA-C: Math course, RA=False, Priority=True → **priority point source** for Math lessons.

When assigning to a Math lesson: LA-A authorizes the assignment, then the system selects LA-C for points (Priority+Matching) over LA-B (non-Priority+General).

## Point Consumption Algorithm

When a staff assigns a student to a lesson:

**Step 1 — Find Assignment LA:**
- System looks for LA with `Require Allocation = True` matching the lesson's course.
- If none found → student does NOT appear in "Add Students" popup.

**Step 2 — Validate Duration:**
- The **Point LA's** date range must cover the lesson date.
- If invalid → **error; assignment blocked**.

**Step 3 — Find Point LA** (evaluated in strict order):

| Priority | Condition | Description |
|---|---|---|
| **1st** | `Priority = True` AND course matches lesson's course | Priority + exact course match |
| **2nd** | `Priority = True` AND `General Flag = True` on course | Priority + general-purpose course |
| **3rd** | `Priority = False` AND course matches lesson's course | Standard + exact course match |
| **4th** | `Priority = False` AND `General Flag = True` on course | Standard + general-purpose course |

Only LAs with `Require Allocation = False` are considered as Point LAs.

**Step 4 — Consume Points:**
- `Points consumed = Course Category's Point_Consumption_Value`.
- `LA.Consumed_Points += Point_Consumption_Value`.
- `LA.Remaining_Points -= Point_Consumption_Value`.

## Concrete Priority Examples

**Setup:** Student has 3 Point LAs (all RA=False):
- LA-1: Course = Math, Priority = True, Remaining = 10pts.
- LA-2: Course = General Studies (General Flag = True), Priority = False, Remaining = 5pts.
- LA-3: Course = Math, Priority = False, Remaining = 8pts.

| Scenario | Evaluation | Selected |
|---|---|---|
| Assign to Math lesson | LA-1 matches (Priority=True + course match → 1st) | **LA-1** |
| LA-1 expired (lesson outside LA-1 duration) | LA-3 (Priority=False + match → 3rd) beats LA-2 (Priority=False + General → 4th) | **LA-3** |
| Assign to Science lesson (no match LA) | LA-2 only option (Priority=False + General → 4th) | **LA-2** |
| All Priority LAs expired, no match | LA-2 (General fallback) | **LA-2** |

## Error Scenarios

| Scenario | Result |
|---|---|
| LA duration valid but **no Point LA found** | Error → student cannot be assigned |
| LA duration **invalid** but Point LA exists | Error → assignment blocked |
| RA=True LA valid but no RA=False Point LA | Error → no point source available |
| Insufficient remaining points | Depends on config — may allow over-consumption or block |
| Over-assignment (Assigned > Total Session Count) | Alert shown; user must confirm; status = "Over Assigned" |

## Point Refund & Recurring Lessons

| Scenario | Behavior |
|---|---|
| **Assign to recurring ("This and following")** | Points consumed for EACH lesson in chain within LA duration. If points run out mid-chain, may show error. |
| **Unassign from single lesson ("Only this")** | Points refunded for that one lesson. Remaining Points increases. |
| **Unassign from recurring ("This and following")** | Points refunded for ALL removed lessons in the chain. |
| **Delete lesson with students** | All sessions removed → points refunded for each student. |
| **Remove student from lesson** | Points refunded to the same LA that originally consumed them. |
| **Reallocation (move between lessons)** | No point recalculation — reallocation is a session-move only; point consumption is NOT affected. |
| **LA deleted (order voided)** | All sessions removed. Points become irrelevant. |
| **LA duration updated** | No effect on existing sessions or points. Nichibei does not use class-based auto-assignment, so updating LA duration does NOT remove students or refund points. |

## Reallocation Flow (Nichibei-specific — 19+23 cases)

Reallocation in Nichibei involves point recalculation on top of the core move.

**Triggering Reallocation:**

1. Set student's attendance to **"Absent"** on the lesson.
2. The **Reallocate checkbox** becomes enabled (only for Absent status — disabled for Attend/Late/Leave Early).
3. Check the Reallocate checkbox → system creates a Reallocation Request:
   - Original Lesson Name/Date populated.
   - New Lesson Name/Date = blank (pending).
   - Reallocate Counter = 0, Status = Open.
4. LA total session count is recalculated.

**Completing Reallocation:**

1. Navigate to LA Detail → Student Session → select reallocated session.
2. Open Reallocate popup → shows available target lessons.
3. Select target lesson → confirm.
4. System performs:
   - Points **refunded** to source LA.
   - Student removed from original lesson.
   - Student assigned to target lesson.
   - Points **consumed** from target LA (via priority chain — may be a different LA).
   - Reallocation Request updated: New Lesson populated, Counter incremented, Status = Completed.

**Cancelling Reallocation:**

| Action | Result |
|---|---|
| Change attendance back to Attend/Late | Reallocate checkbox auto-unchecked; request removed |
| Manually uncheck Reallocate | Request removed from Reallocation list |
| Remove student from lesson | Request and session both removed |

## Trial Lesson (20 cases)

Trial LA is a special type that differs from Regular LA:

| Aspect | Regular LA | Trial LA |
|---|---|---|
| **Creation** | Through Order Group submission | Through **Trial Lesson Application** in SF (Draft → Submitted) |
| **Type field** | Trial | Trial |
| **Purchased Slot edit** | Not editable via UI | Editable **only upward** (can increase, cannot decrease or keep same) |
| **Calendar indicator** | No special marker | **"Trial Student" dot** on lesson card |
| **Point consumption** | Normal priority chain | **No point calculation** — Trial lessons do not consume or refund points |
| **Lesson assignment** | Appears in Add Students popup | Also appears in Add Students popup with `LA type = Trial` |

## Limit Teacher (6 cases)

Config: `lesson.limit_teacher_access_other_lessons.is_enabled` (Nichibei-specific).

When enabled:

| BO Area | Behavior |
|---|---|
| **Lesson List** | Teacher sees only own lessons; Teacher Name filter auto-set and **disabled** |
| **Lesson List — Status Filter** | Published default (per LT-96616) applies WITH the Limit Teacher scope; teacher sees only their assigned Published lessons |
| **Calendar** | "Show my Schedule" checked and **disabled** |
| **Calendar Teacher Filter** | Disabled; cannot search other teachers' lessons |
| **Lesson Detail** | Can only open own lessons |
| **SPU users** | Unaffected — retain location-based access |

## Lesson Syllabus (24 cases)

Links lesson codes to syllabus descriptions automatically:

```
Syllabus Master → Syllabus Detail (Code + Description)
    └── Associated to → Course Master
         └── Lesson (lesson_code maps to syllabus_code → auto-fill description)
```

| Scenario | Behavior |
|---|---|
| Create lesson with code matching syllabus | Syllabus description **auto-filled** |
| Lesson code has no match | Description = blank |
| Edit lesson code | Description **not re-looked up** (unchanged) |
| Change syllabus master on course | Only **new** lessons use new syllabus; existing unchanged |
| Extend Recurring | New lessons auto-fill from lesson code mapping |

Visible on: SF Lesson Detail, BO Lesson Detail, BO Calendar, Mobile App.

## Point Consumption Report (6 cases)

Report shows per-student point tracking:

| Column | Description |
|---|---|
| Student Name | Grouped & sorted ASC |
| LA | All student LAs |
| Course Name | Course tied to LA |
| Total Purchased Points | Points allocated |
| Remaining Points | Points available |
| Lesson Date | Lessons that consumed points |
| Consumed Points (per lesson) | Points each lesson consumed |

Filters: location, course, date range, student.
