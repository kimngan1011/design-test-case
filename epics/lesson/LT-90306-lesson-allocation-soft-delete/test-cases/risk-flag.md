# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 275 — "Risk Flag"](https://app.qase.io/project/PX?suite=275) (9 existing cases). None test the Risk flag's consecutive-absent-days calculation when one of the absent sessions belongs to a Lesson Allocation that has since been archived.

Code trace: `CalculateStudenRiskFlagMetric.cls` resolves the attendance window via `StudentSessionsRepo.getAssignedStudentSessionsByDates`, which filters `Is_Deleted__c = FALSE AND Is_Archived__c = FALSE`. An archived session is invisible to this calculation — not counted as absent, not counted as present, simply absent from the result set. Archiving a Lesson Allocation does not itself write to `Student_Sessions__c`, so it doesn't directly re-trigger recalculation (per the existing negative case 1384, attendance changes don't automatically flip the flag either) — but the **next** recalculation that does run (triggered by a genuine attendance save within the window) will silently exclude the archived day. **The exact recalculation trigger plumbing was not fully traced — treat the expected results below as the best code-grounded prediction, to be confirmed during execution.**

## Suite: Risk Flag

### Risk Flag – Auto-trigger – One of Two Consecutive Absent Sessions Archived – Archived Day Excluded from Recalculation Window

**Description:** Feature Impact (Risk flag calculation) — Decision Table — if one of the two sessions that originally satisfied the consecutive-absent-days threshold has its Lesson Allocation archived, the next Risk flag recalculation excludes that day entirely from the window, potentially turning the flag OFF even though the student was genuinely absent for the full original window.

**Preconditions:**
- Risk flag auto-trigger config = 2 consecutive absent days.
- Student A has Student Sessions marked Absent on 2026-05-18 and 2026-05-19, satisfying the 2-day threshold — Risk flag is currently ON.
- The Lesson Allocation behind the 2026-05-18 session is archived (Archived_At__c populated) after its Student Package Order was fully removed, so that session's Is_Archived__c = TRUE. The 2026-05-19 session remains under a separate, still-active Lesson Allocation.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff navigates to Student A's detail → Risk tab | Risk flag = ON, reflecting the original trigger before the archive | Baseline state |
| 2 | HQ or CM Staff edits the attendance note on the 2026-05-19 session and saves, triggering a fresh auto-trigger recalculation | The recalculation runs via `getAssignedStudentSessionsByDates`, which now returns only the 2026-05-19 session for this window — the archived 2026-05-18 session is excluded entirely | Window recalculated with 1 visible absent day instead of 2 |
| 3 | Observe the Risk flag state after the recalculation | Risk flag turns OFF, since only 1 absent day is now visible to the 2-day-threshold check — even though the student was genuinely absent for the full original 2-day window | Flag downgraded due to the archived day being invisible to the calculation, not due to any real change in attendance history |

**Severity:** major
**Priority:** medium

---
