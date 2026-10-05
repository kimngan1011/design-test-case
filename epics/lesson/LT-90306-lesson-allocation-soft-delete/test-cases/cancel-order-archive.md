# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 2575 — "Cancel Order"](https://app.qase.io/project/PX?suite=2575) (9 existing cases, US06). Existing cases 9922/9923 ("Slot-Based/One-Time – LA Deleted, Student Removed from Lessons") describe the full-cancellation scenario using legacy hard-delete wording. Per explicit instruction, existing cases are left untouched — this file adds new cases covering the archive-enabled behavior for the same trigger.

Code trace: `StudentPackageOrderHandler` → `LessonAllocationSyncService.synchronizeForChangedOrders`/`synchronizeForDeletedOrders`. `shouldArchiveAllocationOfStudentCourse` only fires archive when **every** `Student_Package_Order__c` for that student-course is removed (`isRemovedOrder`: `DeletedAt__c != null` or both Start/End dates null). A full Cancel Order (canceling the ONLY order for that student-course, as in cases 9922/9923 — Slot-Based/One-Time with no other product) satisfies this condition. With `Enable_Lesson_Allocation_Archive__c = true`, `archiveAllocations` runs instead of `BaseDML.doDelete`: a plain `UPDATE` stamping `Archived_At__c`, never a delete. The LA record survives, reachable by Id, with `Is_Archived__c` cascading to its Class Members/Student Sessions via formula — consistent with every other archive case already covered in this epic.

## Suite: Cancel Order

### Cancel Order – Slot-Based – Full Cancellation (Only Order for Student Course) – Lesson Allocation Archived, Not Deleted

**Description:** Gap/update case — Decision Table, contrasts with the legacy-wording baseline (case 9922, "Slot-Based – LA Deleted, Student Removed from Lessons") — when `Enable_Lesson_Allocation_Archive__c` is enabled, cancelling the only order for a student-course does not delete the Lesson Allocation record; it archives it. The record remains reachable by Id, excluded from active lists, with its Class Member/Student Session children hidden via the `Is_Archived__c` formula rather than removed.

**Preconditions:**
- Student A has a Slot-Based order for Course A with Require Allocation = True (the only order for this student-course). An individual lesson exists with Student A assigned.
- `Lesson_Custom_Settings__c.Enable_Lesson_Allocation_Archive__c` = TRUE in this org.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the order group detail for the Slot-Based product, clicks "Cancel", saves draft, and submits | The order is cancelled | Order status = Cancelled |
| 2 | HQ or CM Staff opens Student A's Lesson Allocation directly by record Id | The Lesson Allocation still exists and is reachable; Archived_At__c is populated | Archived_At__c = current timestamp; record NOT deleted |
| 3 | HQ or CM Staff navigates to Student A's Course tab / Lesson Allocation list | The Lesson Allocation no longer appears in the active list | Archived LA excluded from active-list queries (Archived_At__c = NULL filter) |
| 4 | HQ or CM Staff opens the individual lesson Student A was assigned to | Student A is removed from the lesson's Student Sessions, same end-user-visible outcome as the legacy "deleted" baseline (case 9922) | Student A's Student Session Is_Archived__c = TRUE (via formula) → hidden, not deleted |

**Severity:** major
**Priority:** high

---

### Cancel Order – New Order Submitted After Full Cancellation – Archived Lesson Allocation Restored, Not Re-Created

**Description:** Gap case — Decision Table — continuing from the scenario above: when a new order is later submitted for the same student-course (e.g. the family re-enrolls), `LessonAllocationSyncService` restores the SAME archived Lesson Allocation record (unarchive) rather than creating a brand-new one, since the record for that student-course already exists.

**Preconditions:**
- Following directly from the case above: Student A's Lesson Allocation for Course A is archived (Archived_At__c populated) after the only order was cancelled. Note its record Id.
- `Enable_Lesson_Allocation_Archive__c` = TRUE.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff submits a new order for Student A on the same Course A student-course | The order is submitted successfully | New order for Course A |
| 2 | HQ or CM Staff opens Student A's Lesson Allocation for Course A | The SAME Lesson Allocation record (same record Id as before) now shows Archived_At__c blank — it was restored, not replaced by a new record | Archived_At__c = null (restored); record Id unchanged from the archived state |
| 3 | HQ or CM Staff navigates to Student A's Course tab / Lesson Allocation list | The Lesson Allocation reappears in the active list | Is_Archived__c = FALSE (via formula) → visible again |

**Severity:** major
**Priority:** medium

---

### Cancel Order – Partial Cancellation (Future Effective Date, Order Not Removed) – Lesson Allocation End Date Updated Only, Not Archived

**Description:** Regression / boundary case — Decision Table, contrasts with the existing baseline (case 1777, "Frequency – Future Effective Date – LA End Date Updated") — cancelling an order with a future effective date only shortens the Lesson Allocation's end date; the order itself is not removed (it still has valid Start/End dates until the effective date), so `shouldArchiveAllocationOfStudentCourse`'s "all orders removed" condition is never satisfied and `Archived_At__c` is never touched. This locks in that the archive mechanism introduced by this epic has no effect on this already-covered partial-cancel behavior.

**Preconditions:**
- Student A has a Frequency order for Course A with Require Allocation = True and a class assigned; Student A is auto-assigned to lessons by class.
- `Enable_Lesson_Allocation_Archive__c` = TRUE.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the order group detail, clicks "Cancel", fills in an effective date in the future (after today, before the order's original end date), saves draft, and submits | The order's end date is updated to the effective date | effective_date > today |
| 2 | HQ or CM Staff opens Student A's Lesson Allocation | End_Date_Time__c is updated to the effective date; Archived_At__c remains blank throughout | Archived_At__c = null; only duration fields changed |
| 3 | HQ or CM Staff navigates to Student A's Course tab / Lesson Allocation list | The Lesson Allocation still appears in the active list, unaffected by the archive mechanism | Is_Archived__c = FALSE (via formula) → unaffected |

**Severity:** minor
**Priority:** medium

---
