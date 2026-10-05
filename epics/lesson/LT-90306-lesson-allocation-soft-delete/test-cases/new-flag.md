# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 263 — "New flag"](https://app.qase.io/project/PX?suite=263) (3 existing cases). The New flag is displayed per Student Session row, which is already hidden entirely when its Lesson Allocation is archived (no separate archive-exclusion logic to test on this suite). This control case confirms that restoring a previously archived Lesson Allocation does not interfere with the flag's own enrolled-date-window logic once the session is visible again.

## Suite: New flag

### New Flag – Lesson Allocation Restored – Flag Still Shown Correctly for a Lesson Within the Valid Window

**Description:** Control case — Decision Table — after a previously archived Lesson Allocation is restored (unarchived, same record Id), adding the student to a lesson within the New flag's enrolled-date window displays the flag normally, confirming the archive → restore cycle has no side effect on this unrelated display feature.

**Preconditions:**
- New flag threshold config = 15 days.
- Student A has an active enrollment order submitted on 2026-05-01 (enrolled date = 2026-05-01).
- Student A's Lesson Allocation was previously archived, then unarchived (same record Id) after a living Student Package Order reappeared for the same Student Course, so Student A's Student Session Is_Archived__c = FALSE again.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff adds Student A to a lesson with lesson date = 2026-05-10 (enrolled date + 9 days, within the 15-day window) | Student A is added, and the New flag icon is displayed for Student A in the Student Session row | Lesson date within 15-day window AND Is_Archived__c = FALSE (restored) — both conditions satisfied |
| 2 | HQ or CM Staff logs in to BO and opens the same lesson | New flag icon is shown for Student A on BO as well | Consistent with SF |

**Severity:** minor
**Priority:** medium

---
