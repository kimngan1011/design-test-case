# Test Cases: LT-107410 — Auto-delete Student Sessions

## Suite: Update Slot (Qase 2574)

| Title | Description and explicit test data | Expected result | Severity / Priority |
|---|---|---|---|
| Lesson Allocation – Update Duration – Shortened end date – Student is removed from outside lesson | AC-3; HQ or CM Staff; LA end `2026-03-31`; reduce end to `2026-02-08`; individual session `2026-02-15`. | Student is removed from the `2026-02-15` lesson. | critical / high |
| Lesson Allocation – Update Duration – JST and UTC boundary – Student is removed by business date | AC-3; `lessonDate = 2026-02-09 00:30 JST = 2026-02-08 15:30 UTC`; LA end `2026-02-08 JST`. | Student is removed using the JST business date `2026-02-09`. | critical / high |
| Lesson Allocation – Update Duration – Lesson Allocation summary – Allocated count and status updated | AC-3; count `3`; one session after new end `2026-02-08`. | Count is `2` and status reflects remaining sessions. | critical / high |
| Lesson Allocation – Update Duration – Lesson report detail – Removed student detail is deleted | AC-3; Student A report detail on `2026-02-15`. | Report detail is absent. | critical / high |
| Lesson Allocation – Update Duration – Back Office lesson detail – Student no longer appears | AC-3; Student A session on `2026-02-15`. | BO student list has no Student A row. | critical / high |
| Lesson Allocation – Update Duration – Learner App schedule – Removed lesson no longer appears | AC-3; Student A session on `2026-02-15`. | Learner App hides the lesson and report. | critical / high |
| Lesson Allocation – Update Slot – Slot decrease only – Sessions remain unchanged | AC-9; reduce purchased slots with end date unchanged `2026-03-31`. | All individual sessions remain active. | major / high |
| Lesson Allocation – Update Frequency – Frequency decrease only – Sessions remain unchanged | AC-9; decrease frequency with end date unchanged `2026-03-31`. | All individual sessions remain active. | major / high |
