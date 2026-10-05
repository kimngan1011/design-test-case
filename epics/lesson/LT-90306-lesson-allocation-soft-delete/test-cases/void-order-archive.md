# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 2576 — "Void Order"](https://app.qase.io/project/PX?suite=2576) (14 existing cases, US07). Existing cases 1790/1791/1792/1795 ("LA Deleted, Student Removed from Lessons") and 1797/1799/1800 ("New LA Deleted") describe full-removal scenarios using legacy hard-delete wording. Per explicit instruction, existing cases are left untouched — this file adds new cases for the archive-enabled behavior.

Code trace: same engine as Cancel Order — `shouldArchiveAllocationOfStudentCourse` fires archive (not delete) when every order for the student-course is removed. Voiding an order (the ONLY order for that student-course) satisfies this condition identically to cancelling it. With `Enable_Lesson_Allocation_Archive__c = true`, this means: (1) voiding a student's only order archives their LA instead of deleting it; (2) voiding a *Cancel Order* (the baseline case 1802, "Void Cancel Order – LA Duration Restored") that had fully archived the LA restores it via `unarchiveAllocations` (same record, same mechanism as Cancel Order's own restore case), not a date-revert on a surviving record if the LA had actually been archived rather than just end-dated; (3) voiding a *Change Associated Course* that fully archived the "old" LA (case 1797/1800, "Old LA Restored, New LA Deleted") similarly restores the old LA via unarchive and the never-used "new" LA (which also only had one order, now voided) is itself archived rather than deleted.

## Suite: Void Order

### Void Order – One-Time – Full Order Void (Only Order for Student Course) – Lesson Allocation Archived, Not Deleted

**Description:** Gap/update case — Decision Table, contrasts with the legacy-wording baseline (case 1790, "One-Time – LA Deleted, Student Removed from Lessons") — voiding the only order for a student-course archives the Lesson Allocation rather than deleting it, consistent with the Cancel Order archive behavior (same underlying engine).

**Preconditions:**
- Student A has a One-Time order for Course A (the only order for this student-course), with Require Allocation = True. Student A is assigned to an individual lesson.
- `Enable_Lesson_Allocation_Archive__c` = TRUE.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the order group detail for the One-Time product and clicks "Void", then confirms | The order is voided | Order status = Voided |
| 2 | HQ or CM Staff opens Student A's Lesson Allocation directly by record Id | The Lesson Allocation still exists and is reachable; Archived_At__c is populated | Archived_At__c = current timestamp; record NOT deleted |
| 3 | HQ or CM Staff opens the individual lesson Student A was assigned to | Student A is removed from the lesson's Student Sessions — same end-user-visible outcome as the legacy baseline (case 1790) | Student A's Student Session Is_Archived__c = TRUE (via formula) → hidden, not deleted |

**Severity:** major
**Priority:** high

---

### Void Cancel Order – Lesson Allocation Was Fully Archived (Not Just End-Dated) – Void Restores the Same Archived Record

**Description:** Gap case — Decision Table, contrasts with the existing baseline (case 1802, "Void Cancel Order – LA Duration Restored", which covers the partial end-date-shortening scenario) — when the Cancel Order being voided had fully archived the Lesson Allocation (per the "Cancel Order – Full Cancellation" archive case), voiding it restores the SAME archived record via `unarchiveAllocations`, not a duration-only revert on a record that was never removed from the active list.

**Preconditions:**
- Student A's Lesson Allocation for Course A was archived (Archived_At__c populated) after their only order was cancelled. Note its record Id.
- `Enable_Lesson_Allocation_Archive__c` = TRUE.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the cancelled order group detail and clicks "Void", then confirms | The cancel order is voided | Cancel order status = Voided |
| 2 | HQ or CM Staff opens Student A's Lesson Allocation for Course A | The SAME record (same Id as the archived one) now shows Archived_At__c blank | Archived_At__c = null (restored); record Id unchanged |
| 3 | HQ or CM Staff navigates to Student A's Course tab / Lesson Allocation list | The Lesson Allocation reappears in the active list | Is_Archived__c = FALSE (via formula) → visible again |

**Severity:** major
**Priority:** medium

---

### Void Change Associated Course – Both Old and New LA Were Archived (Not Deleted/End-Dated) – Void Restores Old, Archives New

**Description:** Gap case — Decision Table, contrasts with the existing baseline (case 1797, "Void Change Course Order – Effective Date = Start Date – Old LA Restored, New LA Deleted") — when a Change Associated Course (effective date = start date) fully archived the old course's Lesson Allocation and created a new one, voiding that change restores the OLD Lesson Allocation via unarchive (same record Id as before the course change), and the "new" course's Lesson Allocation — which now has zero remaining orders since the one that created it was just voided — gets archived in turn, not hard-deleted.

**Preconditions:**
- Student A changed their associated course from Course A to Course B with effective date = start date — Course A's Lesson Allocation was archived, and a new Lesson Allocation for Course B was created and is active with Class A auto-assigned.
- `Enable_Lesson_Allocation_Archive__c` = TRUE.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Change Associated Course order group detail and clicks "Void", then confirms | The change-course order is voided | Change-course order status = Voided |
| 2 | HQ or CM Staff opens Student A's original Course A Lesson Allocation by its original record Id | The SAME Course A record shows Archived_At__c blank again — restored, not newly re-created; the student is auto-assigned to a lesson by class per the restored Class Member | Archived_At__c = null (restored); same record Id as before the course change |
| 3 | HQ or CM Staff opens the Course B Lesson Allocation that was created by the now-voided change | The Course B Lesson Allocation still exists and is reachable by Id, but now shows Archived_At__c populated — archived because voiding removed its only order, not hard-deleted | Course B LA Archived_At__c = current timestamp; record NOT deleted |

**Severity:** minor
**Priority:** medium

---

### Void Add Associated Course Order – Future Effective Date – Newly-Added Course's Lesson Allocation Archived, Not Deleted

**Description:** Gap/update case — Decision Table, contrasts with the legacy-wording baseline (case 1799, "Void Add Course Order – Future Effective Date – Added LA Deleted") — when Student A adds a new associated Course B with a future effective date (creating a new, not-yet-started Lesson Allocation per the Add Associated Course baseline, case 1775), and that add-course order is then voided, Course B's Lesson Allocation — which only ever had that one order — now has zero remaining orders, satisfying `shouldArchiveAllocationOfStudentCourse`. It gets archived, not hard-deleted; Course A (the pre-existing course) is completely unaffected throughout, since it was never touched by the add-course order in the first place.

**Preconditions:**
- Student A has an active Lesson Allocation for Course A. Student A also added a new associated Course B with a future effective date and a class (per case 1775) — Course B's Lesson Allocation exists, not yet started (future Start_Date_Time__c).
- `Enable_Lesson_Allocation_Archive__c` = TRUE.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the order group detail for the add-course order (Course B) and clicks "Void", then confirms | The add-course order is voided | Add-course order status = Voided |
| 2 | HQ or CM Staff opens the Course B Lesson Allocation directly by record Id | The record still exists and is reachable; Archived_At__c is populated — archived because its only order was voided, not hard-deleted | Course B LA Archived_At__c = current timestamp; record NOT deleted |
| 3 | HQ or CM Staff navigates to Student A's Course tab / Lesson Allocation list | Course B's Lesson Allocation no longer appears in the active list; Course A's Lesson Allocation is unaffected and still appears normally | Course B Is_Archived__c = TRUE (via formula); Course A LA untouched throughout |

**Severity:** minor
**Priority:** medium

---

### Void Update Slot Order – Purchased Slot Reverted – Lesson Allocation Not Archived; Existing Behavior Unchanged

**Description:** Regression case — Decision Table, contrasts with the existing baseline (case 1796, "Void Update Slot Order – Purchased Slot Reverted to Original") — voiding an Update Slot order only reverts Purchased_Slot_Number__c and Total_Session_Count__c to their pre-update values; it never touches Archived_At__c, since neither the update nor its void ever changes the order's removed/not-removed state. This locks in that the archive mechanism introduced by this epic has no effect on this already-covered void-of-update-slot behavior.

**Preconditions:**
- Student A has a Frequency order for Course A; an Update Slot order increased it from 2 to 3 slots/week and is still in a voidable state.
- `Enable_Lesson_Allocation_Archive__c` = TRUE.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Update Slot order group detail and clicks "Void", then confirms | Purchased slot reverts to the original value (2/week); total session count updated accordingly | Purchased_Slot_Number__c reverts to 2 |
| 2 | HQ or CM Staff opens Student A's Lesson Allocation | Archived_At__c remains blank throughout — only slot/session-count fields were ever touched | Archived_At__c = null |
| 3 | HQ or CM Staff navigates to Student A's Course tab / Lesson Allocation list | The Lesson Allocation still appears in the active list | Is_Archived__c = FALSE (via formula) → unaffected |

**Severity:** minor
**Priority:** low

---
