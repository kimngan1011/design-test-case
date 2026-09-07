# Lesson Allocation (LA) — Core

The Lesson Allocation is the **authorization record** that allows a student to be assigned to lessons. It answers: "Does this student have the right to attend lessons for this course?"

For partner-specific extensions, see:
- `../partner-rules/nichibei-lesson-allocation.md` — point consumption model.
- `../partner-rules/riso-lesson-allocation.md` — manual UI creation (no order).

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

## Core LA Fields

| Field | Description |
|---|---|
| **Require Allocation** | `True` = student CAN be assigned to lessons via this LA. `False` = LA exists for **point calculation only**, student cannot be assigned via this LA. |
| **Duration** | Start and end dates defining when this LA is valid |
| **Lesson Allocated** | Count of lessons this student is currently assigned to |
| **Lesson Allocation Status** | **None Assigned** (0) / **Partial Assigned** (0 < Allocated < Total Session Count) / **Fully Assigned** (Allocated = Total Session Count) / **Over Assigned** (Allocated > Total Session Count) |
| **Report History** | List of student reports for this LA, sorted by date |
| **Course** | The course this LA authorizes |

## LA Lifecycle (Mirrors Order Lifecycle)

### Creation triggers

| Trigger | LA Effect |
|---|---|
| **New Order Group** (new enrollment) | LA created per course where `Require Allocation = True`. Start = order start, End = order end. Total session count = 0. |
| **Enrollment Order** (application) | Same rules as New Order Group. |
| **Add New Associated Course** (update order) | New LA created with start = effective date. Other existing LAs unchanged. Effective date must be ≥ product start date. Past effective dates allowed (PBT-1859). |
| **Import Order via CSV** | LA created with same rules as manual order. |

### Order-group class assignment

When an Order Group includes a course-to-class selection, the order creates a Class Member for the LA after submission. The class is resolved from the selected course and the LA duration; this keeps allocations distinct when the same course appears more than once in the same order with different durations.

| Flow and product type | Class member start date | Notes |
|---|---|---|
| **Create Order — all product types** | Product start date, or **today** when the product start is in the past | Class Member end date follows the product end date. No effective-date field is used in this flow. |
| **Add New Course — Schedule / Frequency** | Selected effective date | Staff enters the effective date as part of the add-course flow. |
| **Add New Course — One-Time / Slot-Based** | Order Group Class (OGC) start date | The flow does not ask staff for an effective date; OGC defaults it to the submission date. |

- If no class is selected, the LA is still created but no Class Member and no class-based Student Session are created.
- If the same course has multiple product rows in one Order Group, match each LA to the OGC row using both **course** and **duration**. Two rows with the same class remain separate Class Member records because their durations are different.

### Update triggers

| Trigger | LA Effect |
|---|---|
| **Change Course** (replace course) | Old course LA: end = effective date. New course LA: created with start = effective date. Both co-exist until effective date if it's in the future. |
| **Update Slot** | Purchased slot updated on LA. Duration unchanged. Total session count recalculated. No student session auto-created. |
| **Cancel Product** — Schedule/Frequency type | LA end = effective date (cancel date). Students removed from lessons outside new duration. Class member end updated. Completed/cancelled past lessons remain visible. Past effective dates supported. |
| **Cancel Product** — Slot-Based/One-Time type | LA **deleted** entirely. Students removed from all associated lessons. |
| **Withdrawal Application** | LA end = last attendance day. Students removed from lessons outside new range. Lesson reports of removed students hidden. Allocated, Status, Report History updated. Cancel withdrawal → LA reverted. |
| **LOA Application** | LA end = last attendance day. Students removed from lessons outside new range. Cancel LOA → LA reverted. Resume LOA → new LA from resume date. Cancel resume LOA → new LA deleted. |

### Deletion / restoration triggers

| Trigger | LA Effect |
|---|---|
| **Void New Order** | LA deleted entirely |
| **Void Update Order** — slot change | LA slot reverts to previous value |
| **Void Update Order** — course change (eff date = start) | Old LA restored; new LA deleted |
| **Void Update Order** — course change (eff date > start) | New LA deleted; old LA end date restored |
| **Void Update Order** — add associated course | Added course LA deleted; original LAs unchanged |
| **Void Cancel Order** | LA restored to its state before cancellation |

## Special cases

- **Monthly product type** → LA is **NOT created** (regardless of Require Allocation setting).
- **`Require Allocation = False`** → LA is **NOT created**; LA not updated when slot changes.
- **Multiple product offerings for same student** → separate LAs per product, counted independently.
- **Multiple courses per product** → separate LA per course (all with `Require Allocation = True`).
- **Multiple LAs with same course and duration** → allowed; counted independently.
- **Same course with different durations in one Order Group** → separate LAs and Class Members; the selected class is matched by course + duration, not course alone.
- **Missing Lesson Allocation Week (LAW)** → LA created, but total session count depends on LAW availability.
- **LA duration outside any week order** → LA created; session count = 0.

## LA Impact on Student Session

- Student can only be assigned to a lesson if they have an LA with `Require Allocation = True` for the lesson's course.
- When LA is deleted (order voided/cancelled) → all student sessions linked to that LA are removed.
- When LA duration is updated → class-based auto-assignment re-triggered (students may be added/removed from lessons). See `class-assignment.md`.
