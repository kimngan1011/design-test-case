# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 2577 — "Withdrawal"](https://app.qase.io/project/PX?suite=2577) (8 existing cases, US08). All existing cases describe a partial withdrawal (Last Attendance Day in the future or past, but the order is only end-dated, not removed). None explicitly assert that `Archived_At__c` is untouched by this flow. This file adds a regression-lock case confirming the archive mechanism introduced by this epic has no effect on Withdrawal's existing behavior.

Code trace: a Withdrawal application's resulting order change (Last Attendance Day sets a new end date on the order) leaves the order itself alive with valid Start/End dates — it is never marked `DeletedAt__c` nor left with both dates null, so `shouldArchiveAllocationOfStudentCourse` never fires for a Withdrawal regardless of how close the Last Attendance Day is to today. Only `DefaultAllocationDurationRecalculator`-style end-date/session-count recalculation occurs, identical to Cancel Order/LOA's partial-removal path.

## Suite: Withdrawal

### Withdrawal – Last Attendance Day = Today (Narrowest Valid Boundary) – Lesson Allocation End Date Updated Only, Not Archived

**Description:** Regression / boundary case — Decision Table, contrasts with the existing baseline cases (1812/10191, "Last Attendance Day > Today" / "< Today") — submitting a withdrawal with Last Attendance Day = today (the narrowest valid boundary, shortening the Lesson Allocation as much as possible without removing the order outright) never archives the Lesson Allocation. Only the end date and downstream session count are updated; `Archived_At__c` remains untouched throughout.

**Preconditions:**
- Student A has an active enrollment with a Lesson Allocation for Course A, Require Allocation = True, with a class assigned and lessons scheduled beyond today.
- `Enable_Lesson_Allocation_Archive__c` = TRUE.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff creates a Withdrawal application with Last Attendance Day = today, adds the Withdrawal Product, saves draft, and submits | The Lesson Allocation's end date updates to today; sessions beyond today are removed from future lessons | last_attendance_day = today |
| 2 | HQ or CM Staff opens Student A's Lesson Allocation | Archived_At__c remains blank — only End_Date_Time__c and Total_Session_Count__c were touched | Archived_At__c = null throughout |
| 3 | HQ or CM Staff navigates to Student A's Course tab / Lesson Allocation list | The Lesson Allocation still appears in the active list, unaffected by the archive mechanism | Is_Archived__c = FALSE (via formula) → unaffected |

**Severity:** minor
**Priority:** medium

---
