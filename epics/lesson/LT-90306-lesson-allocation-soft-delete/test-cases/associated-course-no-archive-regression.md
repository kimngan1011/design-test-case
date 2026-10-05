# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suites reviewed: [PX suite 2572 — "Add Associated Course"](https://app.qase.io/project/PX?suite=2572) (6 existing cases, US03) and [PX suite 2573 — "Change Associated Course"](https://app.qase.io/project/PX?suite=2573) (4 existing cases, US04). Neither suite's existing cases explicitly assert the OLD course's Lesson Allocation is left unarchived when a course is only added (not replaced) or changed with a future effective date. This file adds regression-lock cases.

Code trace: Adding an Associated Course only inserts a new `Student_Package_Order__c` row for the new course — it has no effect at all on the existing course's order, so `shouldArchiveAllocationOfStudentCourse` never evaluates true for the existing LA. Changing an Associated Course with a future effective date (case 1774 baseline) only updates the OLD order's end date to the effective date — the order remains alive (not removed) until that date arrives, so the old LA is only end-dated, never archived, until the change actually takes effect.

## Suite: Add Associated Course

### Add Associated Course – Future Effective Date – Existing Course's Lesson Allocation Unaffected, Not Archived

**Description:** Regression case — Decision Table, contrasts with the existing baseline (case 1775, "Add Associated Course – Future Effective Date – New Course LA Created, Auto-Assigned to Lessons") — adding a new associated course never touches the existing course's Lesson Allocation at all; it remains fully active and unarchived throughout, since its own order was never modified or removed.

**Preconditions:**
- Student A has an active Lesson Allocation for Course A (existing course), with a class assigned and lessons scheduled.
- `Enable_Lesson_Allocation_Archive__c` = TRUE.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff adds a new associated Course B with a future effective date and a class, then submits | Course B's new Lesson Allocation is created with start date = effective date | New Course B LA created |
| 2 | HQ or CM Staff opens Student A's existing Course A Lesson Allocation | Course A's Lesson Allocation is completely unchanged — same Start/End dates, Archived_At__c still blank | Archived_At__c = null; Course A LA untouched |
| 3 | HQ or CM Staff navigates to Student A's Course tab / Lesson Allocation list | Both Course A's (existing, active) and Course B's (new, future-starting) Lesson Allocations appear in the list | Course A Is_Archived__c = FALSE throughout |

**Severity:** minor
**Priority:** low

---

## Suite: Change Associated Course

### Change Associated Course – Future Effective Date (Order Not Yet Removed) – Old Lesson Allocation End Date Updated Only, Not Archived

**Description:** Regression / boundary case — Decision Table, contrasts with the existing baseline (case 1774, "Future Effective Date – Old LA End Date Updated, New LA Created") — changing the associated course with an effective date in the future only updates the OLD course's Lesson Allocation end date; since its order remains alive (not removed) until the effective date, `Archived_At__c` is never touched for the old LA while this case's pre-effective-date window is in play. The archive-triggering "old LA archived" scenario is only reached once the effective date arrives and the order is actually removed (already covered separately for the effective-date = start-date case).

**Preconditions:**
- Student A has an active Lesson Allocation for Course A with a class assigned and a recurring group lesson by class.
- `Enable_Lesson_Allocation_Archive__c` = TRUE.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff changes the associated course from Course A to Course B with an effective date in the future (after today), assigns a class for Course B, saves draft, and submits | Course A's Lesson Allocation end date updates to the effective date; a new Course B Lesson Allocation is created starting on the effective date | effective_date > today |
| 2 | HQ or CM Staff opens Student A's Course A Lesson Allocation before the effective date arrives | Archived_At__c remains blank — only End_Date_Time__c was touched; the LA is still active | Archived_At__c = null (before effective date) |
| 3 | HQ or CM Staff navigates to Student A's Course tab / Lesson Allocation list before the effective date | Course A's Lesson Allocation still appears in the active list alongside the new future-starting Course B Lesson Allocation | Is_Archived__c = FALSE (via formula) → unaffected until the order is actually removed on the effective date |

**Severity:** minor
**Priority:** medium

---
