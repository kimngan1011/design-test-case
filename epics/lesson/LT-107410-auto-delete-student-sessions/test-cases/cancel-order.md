# Test Cases: LT-107410 — Auto-delete Student Sessions

## Suite: Cancel Order (Qase 2575)

| Title | Description | Preconditions and deterministic validation | Severity / Priority |
|---|---|---|---|
| Lesson Allocation – Cancel Order – Future individual session – Student is removed from lesson | AC-3; Decision Table. | HQ or CM Staff; individual LA end date is reduced from `2026-03-31` to `2026-02-08`; Student A is removed from the `2026-02-15` lesson. | critical / high |
| Lesson Allocation – Cancel Order – Completed session – Attendance history retained | AC-3, AC-6; BVA. | Completed session on `2026-02-07`, boundary session on `2026-02-08`, future session on `2026-02-09`; cancel ending LA `2026-02-08` retains first two only. | critical / high |
| Lesson Allocation – Cancel Order – Lesson Allocation summary – Allocated count and status updated | AC-3; CRUD. | LA count is `3` before cancel and one session is outside the shortened date; after cancel it is `2` with corresponding status. | critical / high |
| Lesson Allocation – Cancel Order – Lesson report detail – Removed student detail is deleted | AC-3; CRUD. | Student A report detail exists on out-of-range lesson `2026-02-15`; after cancel it is absent. | critical / high |
| Lesson Allocation – Cancel Order – Back Office lesson detail – Student no longer appears | AC-3; cross-system. | Student A session exists on `2026-02-15`; after cancel ending `2026-02-08`, BO has no Student A row. | critical / high |
| Lesson Allocation – Cancel Order – Learner App schedule – Removed lesson no longer appears | AC-3; cross-system. | Student A session exists on `2026-02-15`; after cancel ending `2026-02-08`, Learner App hides lesson and report. | critical / high |
