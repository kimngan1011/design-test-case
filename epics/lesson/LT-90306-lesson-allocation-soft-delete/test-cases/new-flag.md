# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 263 — "New flag"](https://app.qase.io/project/PX?suite=263) (4 cases). The New flag is displayed per Student Session row, which is already hidden entirely when its Lesson Allocation is archived (no separate archive-exclusion logic to test on this suite). The New window is calculated from the linked Enrollment Status (V2) `Enrolled Date`, with the V1 `Enrollment Start Date` used only when V2 data is absent. This control case confirms that restoring a previously archived Lesson Allocation does not interfere with that logic once the session is visible again.

## Suite: New flag

### New Flag – Lesson Allocation Restored – Flag Still Shown Correctly for a Lesson Within the Valid Window

**Description:** Control case — Decision Table — after a previously archived Lesson Allocation is restored (unarchived, same record Id), adding the student to a lesson within the New flag window calculated from the linked Enrollment Status (V2) Enrolled Date displays the flag normally. This confirms that the archive → restore cycle has no side effect on this unrelated display feature.

**Preconditions:**
- New flag threshold config = 15 days.
- Student A has a current active Enrolled V1 record linked through Enrollment Status Record to an active Enrollment Status (V2) record whose Enrolled Date = 2026-05-01.
- Student A's Lesson Allocation was previously archived, then unarchived (same record Id) after a living Student Package Order reappeared for the same Student Course, so Student A's Student Session Is_Archived__c = FALSE again.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff adds Student A to a lesson with lesson date = 2026-05-10 (V2 Enrolled Date + 9 days, within the 15-day window) | Student A is added, and the New flag icon is displayed for Student A in the Student Session row | Lesson date within 15 days of Enrollment Status (V2) Enrolled Date AND Is_Archived__c = FALSE (restored) — both conditions satisfied |
| 2 | HQ or CM Staff logs in to BO and opens the same lesson | New flag icon is shown for Student A on BO as well | Consistent with SF |

**Severity:** minor
**Priority:** medium

---
