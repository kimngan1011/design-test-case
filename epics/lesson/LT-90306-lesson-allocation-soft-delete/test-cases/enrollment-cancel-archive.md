# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 2571 — "Create LA – Enrollment Order"](https://app.qase.io/project/PX?suite=2571) (3 existing cases, US02). Existing case 1808 ("Cancel Enrollment – All LAs and Class Members Deleted") describes the full-cancellation scenario using legacy hard-delete wording. Per explicit instruction, existing cases are left untouched — this file adds a new case for the archive-enabled behavior.

Code trace: Cancel Enrollment removes every order created by that enrollment application in one action, which for each affected student-course satisfies `shouldArchiveAllocationOfStudentCourse`'s "all orders removed" condition identically to a single Cancel Order. With `Enable_Lesson_Allocation_Archive__c = true`, every Lesson Allocation created by the enrollment gets archived (not deleted) in the same `synchronize()` call — this is a bulk application of the same mechanism already confirmed for Cancel Order/Void Order, just triggered across multiple student-courses at once.

## Suite: Create LA – Enrollment Order

### Cancel Enrollment – All Lesson Allocations Archived, Not Deleted

**Description:** Gap/update case — Decision Table, contrasts with the legacy-wording baseline (case 1808, "Cancel Enrollment – All LAs and Class Members Deleted") — cancelling an enrollment application archives every Lesson Allocation it created rather than deleting them. All records remain reachable by Id, excluded from active lists, with their Class Member/Student Session children hidden via the `Is_Archived__c` formula.

**Preconditions:**
- Student A has an enrollment application that created Lesson Allocations for Course A (One-Time) and Course B (Schedule), both with classes auto-assigned and students appearing in their respective lessons' Student Sessions.
- `Enable_Lesson_Allocation_Archive__c` = TRUE.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the enrollment application detail and clicks "Cancel Enrollment" | The enrollment is cancelled | Enrollment status = Cancelled |
| 2 | HQ or CM Staff opens Student A's Course A and Course B Lesson Allocations directly by record Id | Both Lesson Allocations still exist and are reachable; both show Archived_At__c populated | Archived_At__c = current timestamp on both; neither record deleted |
| 3 | HQ or CM Staff navigates to Student A's Course tab / Lesson Allocation list | Neither Lesson Allocation appears in the active list | Both excluded from active-list queries (Archived_At__c = NULL filter) |
| 4 | HQ or CM Staff opens the Course A and Course B lessons Student A was assigned to | Student A is removed from both lessons' Student Sessions — same end-user-visible outcome as the legacy "deleted" baseline (case 1808) | Both Student Sessions' Is_Archived__c = TRUE (via formula) → hidden, not deleted |

**Severity:** major
**Priority:** high

---
