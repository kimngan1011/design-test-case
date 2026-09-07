# Test Cases: LT-107410 — Auto-delete Student Sessions

## Suite: LOA (Qase 2578)

| Title | Description | Preconditions and deterministic validation | Severity / Priority |
|---|---|---|---|
| Lesson Allocation – LOA – Future individual session – Student is removed from lesson | AC-2; Decision Table. | HQ or CM Staff; individual LA has sessions on `2026-02-01`, `2026-02-08`, `2026-02-15`; submit partial LOA with `last_attendance_day = 2026-02-08`; Student A is removed from the `2026-02-15` lesson. | critical / high |
| Lesson Allocation – LOA – Last attendance boundary – Past and boundary sessions retained | AC-2, AC-6; BVA. | Sessions are `2026-02-07`, `2026-02-08`, `2026-02-09`; completed attendance is recorded on `2026-02-07`; after LOA dated `2026-02-08`, first two remain active and `2026-02-09` is deleted. | critical / high |
| Lesson Allocation – LOA – Lesson Allocation summary – Allocated count and status updated | AC-2; CRUD. | LA starts with `Lesson Allocated = 3`; after removing the one out-of-range session, LA shows `Lesson Allocated = 2` and status for two remaining sessions. | critical / high |
| Lesson Allocation – LOA – Lesson report detail – Removed student detail is deleted | AC-2; CRUD. | Student A has a report detail for `2026-02-15`; after LOA dated `2026-02-08`, Student A is absent from that lesson report. | critical / high |
| Lesson Allocation – LOA – Back Office lesson detail – Student no longer appears | AC-2; cross-system. | Student A has a `2026-02-15` session; after LOA dated `2026-02-08`, BO lesson detail has no Student A row. | critical / high |
| Lesson Allocation – LOA – Learner App schedule – Removed lesson no longer appears | AC-2; cross-system. | Student A has a `2026-02-15` session; after LOA dated `2026-02-08`, Learner App does not show that lesson or report. | critical / high |
