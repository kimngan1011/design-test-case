# Test Cases: LT-107410 — Auto-delete Student Sessions

## Suite: Withdrawal (Qase 2577)

### Lesson Allocation – Cancel Withdrawal – Previously outside lesson – Student is not re-added

**Description:** AC-7 — State Transition — Cancelling Withdrawal restores the LA duration without re-adding the individual student.

**Preconditions:** HQ or CM Staff; Withdrawal ended LA `2026-02-08` and removed Student A from individual lesson `2026-02-15`.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Cancel the Partial Withdrawal. | The LA duration restores. | `restored_end = 2026-03-31` |
| 2 | Open the `2026-02-15` lesson. | Student A is not re-added. | `lesson_date = 2026-02-15` |

**Severity:** critical  
**Priority:** high
