# Test Cases: LT-107410 — Auto-delete Student Sessions

## Suite: Change Associated Course (Qase 2573)

| Qase ID | Title | AC / deterministic validation | Severity / Priority |
|---|---|---|---|
| PX-26659 | Lesson Allocation – Change Associated Course – Individual session removal and downstream consistency | AC-4 end-to-end: partial course change ends the old LA; Student A is removed from an old-course outside lesson, while an in-range old-course session and a new-course session remain active. Verify old LA count/status, lesson report detail, BO lesson detail, and Learner App schedule. | critical / high |
| PX-26661 | Lesson Allocation – Change Associated Course – Last attendance boundary – Completed session retained | AC-4, AC-6; completed old-course session `2026-02-07`, boundary `2026-02-08`, future `2026-02-09`; first two retained. | critical / high |
