# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 3422 — "Handle auto-delete Reallocate type"](https://app.qase.io/project/PX?suite=3422) (18 existing cases). All existing cases cover auto-delete of the linked Reallocate session when the original session/lesson is removed via unflag, student removal, lesson deletion, or LA end-date reduction. None test what happens when the Lesson Allocation itself is archived while an Approved reallocation is in flight.

## Suite: Handle auto-delete Reallocate type

### Reallocation – Approved Request – Lesson Allocation Archived – Both Sessions Hidden Together but Request Left Stale; Restore Brings Both Back

**Description:** Feature Impact / data-integrity — Decision Table — when the Lesson Allocation behind an Approved reallocation is archived, the original session (Lesson A) and the linked Reallocate session (Lesson B) disappear from their respective lessons at the same instant, since both share the same parent LA formula — but the `Reallocation__c` request record itself is never updated or closed by the archive write, unlike the existing auto-delete behavior for Draft/Published/Cancelled linked lessons (cases 6134-6136, 9286-9288). Restoring the Lesson Allocation brings both sessions back together, with the request unchanged throughout.

**Preconditions:**
- Student A has an Approved reallocation request: original Absent session in Lesson A, linked Reallocate session in Lesson B.
- Student A's Lesson Allocation is archived (Archived_At__c populated) after its Student Package Order was fully removed — both sessions share this Lesson Allocation, so both flip Is_Archived__c = TRUE simultaneously via the formula.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson A's and Lesson B's Student Sessions sections | Student A no longer appears in either lesson — both the original and the Reallocate session are hidden at the same instant | Both sessions' Is_Archived__c = TRUE via the same parent LA |
| 2 | HQ or CM Staff opens the Reallocation list and looks for Student A's request | The request still shows status = Approved, still referencing Lesson B — archiving the LA does not update or close the reallocation request, unlike the existing auto-delete behavior when the linked lesson itself is deleted/cancelled | Reallocation__c record untouched; archive only writes Lesson_Allocation__c.Archived_At__c |
| 3 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id | Both the original session (Lesson A) and the Reallocate session (Lesson B) reappear automatically in their respective lessons | Both sessions Is_Archived__c = FALSE (restored) → shown again, same records, no duplication |
| 4 | HQ or CM Staff opens the Reallocation list again | The request still shows status = Approved, consistent with before the archive — the round trip did not corrupt or lose the reallocation state | Reallocation record consistent across the archive → restore cycle |

**Severity:** major
**Priority:** high

---
