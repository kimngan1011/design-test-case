# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 290 — "Trial Student"](https://app.qase.io/project/PX?suite=290) (20 existing cases). Code trace confirms Trial Lesson Allocations are created and managed entirely by `TrialLessonAllocationHandler.cls` (package `trial-lesson`), with **zero references** to `Student_Package_Order__c`, `Student_Course_ID__c`, or `Archived_At__c` — Trial LA never participates in `LessonAllocationSyncService`'s archive/unarchive group logic, the same way Riso manual LA is out of scope. This control case documents and locks in that independence.

## Suite: Trial Student

### Trial Student – Core Lesson Allocation Soft Delete Feature Enabled – Trial LA Lifecycle Unaffected

**Description:** Control case / regression boundary — Decision Table — with the Core Lesson Allocation archive feature enabled org-wide, a Trial Lesson Allocation's creation, assignment, and cancellation continue to work exactly as before, since the Trial LA lifecycle is managed by a separate code path that never writes to or reads `Archived_At__c`.

**Preconditions:**
- The Core Lesson Allocation soft-delete feature flag (`Enable_Lesson_Allocation_Archive__c`) is enabled org-wide.
- A trial lesson request exists for Student A.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff submits the trial lesson for Student A and opens the resulting Lesson Allocation detail | LA created with Type = Trial; Archived_At__c is blank and is never populated by this flow | Archived_At__c = blank, untouched by TrialLessonAllocationHandler |
| 2 | HQ or CM Staff opens a one-time lesson and adds Student A via Add Student | Student A is added with session type = Trial, exactly as in the pre-archive-feature baseline (case 1479) | No regression from the Core archive mechanism |
| 3 | HQ or CM Staff cancels the trial via the normal trial-lesson cancellation flow | The Trial LA and its sessions are handled by the existing trial-specific cleanup logic, independent of the archive/unarchive sync engine | Trial lifecycle unaffected by the Core LA soft-delete feature |

**Severity:** minor
**Priority:** low

---
