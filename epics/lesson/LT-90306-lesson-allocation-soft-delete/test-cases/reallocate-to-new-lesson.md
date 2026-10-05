# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 3421 — "Reallocate to new lesson"](https://app.qase.io/project/PX?suite=3421) (9 existing cases). None test the interaction between the archive/unarchive cycle and an in-flight reallocation request.

Code trace: `ReallocationHandler.createReallocationByStudentSessionId` (and two other methods at lines 92/785) all look up the `Student_Sessions__c` by Id with `Is_Deleted__c = FALSE AND Is_Archived__c = FALSE`. `LessonAllocationSyncService.executeSyncPlan` never touches `Reallocation__c` — archiving an LA only writes `Archived_At__c` on the LA itself, so an Open or Approved reallocation request is left completely untouched by the archive/restore cycle; only the underlying session's visibility changes (via the formula).

## Suite: Reallocate to new lesson

### Reallocation – Open Request – Lesson Allocation Archived Before Lesson Selected – Request Becomes Unprocessable

**Description:** Feature Impact / data-integrity — Decision Table — if a student's Lesson Allocation is archived while their reallocation request is still Open (no lesson selected yet), the request record itself is left unchanged, but the session lookup backing lesson-selection is excluded by the archive filter, so the request cannot be completed through the normal flow.

**Preconditions:**
- Student A has an Absent Student Session in Lesson A with Reallocate_Flag__c = TRUE.
- An Open reallocation request exists for Student A, with no linked lesson yet.
- Student A's Lesson Allocation is subsequently archived (Archived_At__c populated) after its Student Package Order was fully removed, so the original session's Is_Archived__c = TRUE.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Reallocation list and looks for Student A's Open request | The request is still listed with status = Open — the archive write never touched the Reallocation__c record | Reallocation request status unchanged |
| 2 | HQ or CM Staff opens Lesson A and views the Student Sessions section | Student A no longer appears in the list | Student A Is_Archived__c = TRUE → hidden |
| 3 | HQ or CM Staff opens the Reallocate Lesson popup from Student A's request and selects Lesson B, then confirms | The reallocation does not complete normally — Student A is not added to Lesson B's Student Sessions, and/or an error/failure is surfaced, since the session lookup behind this action excludes archived sessions | Student A's session excluded by Is_Archived__c = TRUE from the lookup backing this action |

**Severity:** major
**Priority:** high

---

### Reallocation – Open Request – Lesson Allocation Restored – Student Can Be Reallocated to a New Lesson Normally

**Description:** Feature Impact / data-integrity, control case — Decision Table — after a previously archived Lesson Allocation is restored (unarchived, same record Id), the student's original session reappears and a still-Open reallocation request can be completed normally, confirming the request record survives the archive → restore cycle intact.

**Preconditions:**
- Student A has an Absent Student Session in Lesson A with Reallocate_Flag__c = TRUE; an Open reallocation request exists for Student A, with no linked lesson yet.
- Student A's Lesson Allocation was previously archived, then unarchived (same record Id) after a living Student Package Order reappeared for the same Student Course, so Student A's original session Is_Archived__c = FALSE again.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson A's Student Sessions section | Student A's session is visible again | Student A Is_Archived__c = FALSE (restored) → shown |
| 2 | HQ or CM Staff opens the Reallocation list and finds Student A's request | The request is still listed with status = Open, unaffected by the archive/restore cycle | Reallocation request preserved |
| 3 | HQ or CM Staff opens the Reallocate Lesson popup for this request, selects Lesson B, and confirms | Student A is added to Lesson B's Student Sessions with session type = Reallocate | Normal reallocation completes |
| 4 | HQ or CM Staff checks Student A's reallocation request again | Request status = Approved, linked lesson = Lesson B, reallocation counter incremented by 1 — identical to a student whose LA was never archived | Reallocation proceeds exactly as the non-archived baseline (case 1447) |

**Severity:** major
**Priority:** high

---
