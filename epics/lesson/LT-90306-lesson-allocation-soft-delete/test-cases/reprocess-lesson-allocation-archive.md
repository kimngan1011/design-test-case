# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 306 — "Reprocess lesson allocation"](https://app.qase.io/project/PX?suite=306) (4 existing cases). None test an archived Lesson Allocation.

Code trace: this is one of the few flows already well-protected against archive. `LessonAllocationHandler.getLessonAllocationByFilter` (the picker populating the selectable table) filters `Archived_At__c = NULL` — an archived LA can never be selected. `reprocessLessonAllocation(List<Id>)` (the Apex method behind the "Reprocess" button) independently re-filters `WHERE Id IN :lessonAllocationIds ... AND Archived_At__c = NULL` as defense-in-depth. The only reachable gap is a race condition: if an LA is archived in a different session/tab *after* being selected on this page but *before* the "Reprocess" confirmation is clicked, the Apex method's query returns zero rows and the method just `return`s with no exception — the LWC still shows its generic success toast, silently doing nothing.

## Suite: Reprocess lesson allocation

### Reprocess – Lesson Allocation Archived After Selection, Before Confirm – Success Toast Shown but Nothing Recalculated

**Description:** Gap case — Decision Table — if a Lesson Allocation is selected for reprocessing and then archived (by another user/session) before the "Reprocess" confirmation is clicked, the Apex method's `Archived_At__c = NULL` guard silently filters it out and returns early with no error — the UI still shows a success toast, misleading staff into believing the reprocess ran when nothing was recalculated.

**Preconditions:**
- Student A has a Schedule Lesson Allocation for Course A with no program master yet, start date in the future, LA generated (Total_Session_Count__c = 0).
- A program master is added to Course A's course offering, making this LA eligible for reprocessing.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff navigates to Student A's Course tab, selects the Schedule LA row, and opens the "Reprocess" confirmation dialog (does not yet confirm) | The confirmation dialog is shown with the LA selected | LA selected, dialog open |
| 2 | In a separate session, the Student Package Order behind this LA is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff (on the original, stale page) clicks "Confirm" on the Reprocess dialog | A success toast is shown, with no indication that nothing happened | reprocessLessonAllocation's query (`Id IN :ids AND Archived_At__c = NULL`) returns zero rows → method returns early, no exception |
| 4 | HQ or CM Staff refreshes the page and opens the archived Lesson Allocation directly by record Id | Total_Session_Count__c and Allocated_Sessions__c remain unchanged (still 0) — the reprocess never actually ran, despite the success toast from step 3 | No DML occurred; Archived_At__c still populated |

**Severity:** minor
**Priority:** low

---
