# Test Cases: LT-107410 — Auto-delete Student Sessions

## Suite: Void Order (Qase 2576)

| Title | Description | Preconditions and expected result | Severity / Priority |
|---|---|---|---|
| Lesson Allocation – Void Cancel Order – Individual outside lesson – Student is not re-added | AC-7; State Transition. | HQ or CM Staff; Cancel Order shortened LA to `2026-02-08` and removed Student A from `2026-02-15`; void the Cancel Order. LA duration restores but Student A is not re-added to the `2026-02-15` lesson. | critical / high |
| Lesson Allocation – Void Change Associated Course – Old-course outside lesson – Student is not re-added | AC-7; State Transition. | HQ or CM Staff; partial Course Change effective `2026-02-08` removed Student A from old-course `2026-02-15`; void the Course Change. Old LA duration restores but Student A is not re-added to that old-course lesson. | critical / high |
| Lesson Allocation – Void Update Duration – Outside lesson – Student is not re-added | AC-7; State Transition. | HQ or CM Staff; reduced-duration Update ended LA `2026-02-08` and removed Student A from `2026-02-15`; void the Update. LA duration restores but Student A is not re-added to the lesson. | critical / high |
