# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite: [PX suite 3756 — "[Renseikai] Lesson Report Notification – Archive"](https://app.qase.io/project/PX?suite=3756), created under the LT-90306 soft-delete suite. The source feature is LT-61333, whose Scheduled Report Delivery suite covers published-report selection and recipient delivery but did not include the Lesson Allocation archive state.

## Suite: [Renseikai] Lesson Report Notification – Archive

### [Renseikai] Lesson Report Notification – Archived Lesson Allocation – Eligible Report Sends No Notification

**Description:** AC-5 and LT-61333 REQ-01/REQ-02 — Decision Table. An otherwise eligible Published Lesson Report is excluded from scheduled delivery while the student's Lesson Allocation is archived.

**Preconditions:**
- The scheduler time is 2026-10-12 12:00 JST.
- Report R-201 for Math Archive is Published with updated_at = 2026-10-12 09:00 JST.
- Student A's sole Lesson Allocation is archived after its Student Package Order is fully removed.
- Student A and Default Parent A are logged in to their apps.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | System runs the daily report-notification batch. | System does not select R-201 and creates no delivery for either recipient. | run=2026-10-12 12:00 JST; report=R-201; allocation=archived |
| 2 | Student A opens the Learner App notification inbox. | No notification for Math Archive is present. | recipient=Student A |
| 3 | Default Parent A opens the Parent App notification inbox. | No notification for Math Archive is present. | recipient=Default Parent A |

**Severity:** critical
**Priority:** high

---

### [Renseikai] Lesson Report Notification – Restored Lesson Allocation – Subsequent Eligible Report Sends Normally

**Description:** AC-3/AC-5 and LT-61333 REQ-01/REQ-02 — State Transition. After restore, a subsequently eligible Published Lesson Report is delivered once to the Student and Default Parent; restore does not replay the report skipped while archived.

**Preconditions:**
- Student A's Lesson Allocation was archived, then restored on the same record after a living Student Package Order reappeared.
- Report R-202 for Math Restore is Published with updated_at = 2026-10-12 09:00 JST, after the allocation is restored.
- The scheduler time is 2026-10-12 12:00 JST.
- Student A and Default Parent A are logged in to their apps.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | System runs the daily report-notification batch. | System selects R-202 once and creates one delivery for each intended recipient. | run=2026-10-12 12:00 JST; report=R-202; allocation=restored |
| 2 | Student A opens the Learner App notification inbox. | Exactly one notification for Math Restore is present. | recipient=Student A; expected_count=1 |
| 3 | Default Parent A opens the Parent App notification inbox. | Exactly one notification for Math Restore is present. | recipient=Default Parent A; expected_count=1 |

**Severity:** critical
**Priority:** high
