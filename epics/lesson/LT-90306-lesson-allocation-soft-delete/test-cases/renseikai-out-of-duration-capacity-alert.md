# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 2495 — "[Renseikai] Configure Lesson (Student Session) Error message display"](https://app.qase.io/project/PX?suite=2495) (15 existing cases). None test a student whose Lesson Allocation is archived.

Code trace: both the "Out of Duration" banner (`alertLessonOutCourseDuration`) and the "Classroom Capacity" banner (`alertLessonCapacity`) are driven from the exact same filtered dataset as suite 1647 above — `StudentSessionsHandler.getStudentSessionsByLessonId`, which filters `Is_Deleted__c = FALSE AND Is_Archived__c = FALSE`. The per-student `isLessonOutCourseDuration` flag and the lesson's `studentSessionCount` (used for the capacity comparison) are both computed only from rows in that same filtered result. So an archived student's Student Session row is excluded from both the out-of-duration evaluation and the capacity count — there is no path in this codebase where an archived-but-technically-out-of-duration student triggers a stale banner, or where an archived student inflates the capacity count. **This is already correct, but has zero regression coverage** for the archived-LA case specifically.

## Suite: [Renseikai] Configure Lesson (Student Session) Error message display

### [Renseikai] Configure Alert – Student Out of Duration AND Lesson Allocation Archived – Student Excluded from Both Out-of-Duration Banner and Capacity Count; Restored – Alert and Count Reflect Student Again

**Description:** Regression / control case — Decision Table, contrasts with the baseline (case 18276, "SF Out of Duration – Config enabled – Out-of-duration banner displayed"): a student who is both out-of-duration AND has an archived Lesson Allocation is excluded from the lesson entirely — the out-of-duration banner does not fire for them, and they do not count toward the classroom capacity — because both banners share the same `Is_Archived__c = FALSE`-filtered data source as every other active-session view. On restore, the student reappears and the out-of-duration banner correctly re-evaluates based on their actual dates.

**Preconditions:**
- Renseikai tenant has both "Out of Duration" and "Classroom Capacity" alert configs enabled.
- Lesson L1 has classroom capacity = 2. Student S1 has an active Lesson Allocation whose End_Date_Time__c falls before L1's date (out of duration) and is currently assigned to L1 — the out-of-duration banner is shown, and S1 counts toward the capacity total.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson L1 and confirms the out-of-duration banner is shown, and views the current student count | Out-of-duration banner shown; S1 counted in the capacity total | S1 Is_Archived__c = FALSE; isLessonOutCourseDuration = TRUE |
| 2 | The Student Package Order behind S1's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff reopens Lesson L1 | S1 no longer appears in the student list; the out-of-duration banner is no longer shown (not because S1's dates changed, but because the row is hidden); S1 no longer counts toward the capacity total | S1 Is_Archived__c = TRUE (via formula) → excluded from getStudentSessionsByLessonId entirely |
| 4 | A living Student Package Order reappears for S1's Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 5 | HQ or CM Staff reopens Lesson L1 | S1 reappears in the student list; the out-of-duration banner is shown again, since S1's underlying dates still place them out of duration; S1 counts toward the capacity total again | S1 Is_Archived__c = FALSE (restored) → row and flags recomputed correctly |

**Severity:** minor
**Priority:** medium

---
