# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Feature: `LessonAllocationSyncService.MasterDataSnapshot.allocationsByStudentCourseId` (see spec.md Gap #14, Clarification Question #8). No Qase suite identified yet — this scenario requires two `Lesson_Allocation__c` records that deliberately share the same `Student_Course_ID__c` value, which does not happen through any normal UI flow (the field has no uniqueness constraint, but nothing in the standard flows creates a collision either). **Setup method is not yet finalized** — file under whichever suite ends up owning data-integrity/sync edge cases once a reproducible setup (direct data load, a specific re-enrollment sequence, or a dev/data script) is confirmed.

Code trace: `LessonAllocationSyncService.cls:1408-1431` (`SoqlLessonAllocationReader.findAllocationsByStudentCourseIdIncludingRemoved`) builds `allocationsByStudentCourseId` as a strict one-to-one map, keyed by `Student_Course_ID__c`, using `ORDER BY Student_Course_ID__c, Archived_At__c ASC NULLS FIRST, IsDeleted, CreatedDate DESC` and keeping only the first row per key. `Lesson_Allocation__c.Student_Course_ID__c` has `unique = false` and `externalId = false` at the schema level — nothing blocks a duplicate from existing.

## Suite: Lesson Allocation Sync — Data Integrity (suite TBD)

### Lesson Allocation Sync – Duplicate Student_Course_ID – Only the Tie-Break Winner Is Archived, Unarchived, or Updated

**Description:** Boundary / data-integrity — Decision Table — when two `Lesson_Allocation__c` records share the same `Student_Course_ID__c`, the archive/unarchive sync engine only ever manages the one selected by its tie-break rule (non-archived first, then most recently created); the losing duplicate is silently excluded from every subsequent archive, unarchive, and update cycle, regardless of its own order-removal state.

**Preconditions:**
- Two `Lesson_Allocation__c` records, LA-1 and LA-2, exist for the same `Student_Course_ID__c` value. **Setup method TBD** — not achievable through a normal order/enrollment flow; requires a deliberately engineered duplicate (e.g. direct data load, or a specific data-migration/re-enrollment sequence once identified).
- LA-1 is the older record (earlier CreatedDate); LA-2 is the newer record (later CreatedDate). Both currently have Archived_At__c blank (active).
- At least one Student_Package_Order__c exists under this Student_Course_ID__c, tied to LA-2 (the record actually referenced going forward).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | All Student_Package_Order__c records under this Student_Course_ID__c are removed, triggering the archive sync | The sync engine evaluates the Student_Course_ID__c group | Student_Course_ID shared by LA-1 and LA-2 |
| 2 | Open LA-2 (the more recently created of the two) | LA-2's Archived_At__c is now populated — it was the record the sync engine selected to represent this Student_Course_ID group | LA-2 Archived_At__c = current timestamp |
| 3 | Open LA-1 (the older duplicate) | LA-1's Archived_At__c is unchanged from before step 1 — the sync engine never touched it, since its internal map only tracked LA-2 for this Student_Course_ID | LA-1 state frozen; not managed by this sync run |
| 4 | A living Student_Package_Order__c reappears for the same Student_Course_ID, triggering the unarchive sync | The sync engine unarchives LA-2 (the same record it has been tracking); Archived_At__c is cleared on LA-2 | LA-2 Archived_At__c = null (restored) |
| 5 | Open LA-1 again | LA-1 remains exactly as it was before step 1 — still not archived, not unarchived, not updated by any sync run in between | Confirms the duplicate-key blind spot persists across a full archive → restore cycle |

**Severity:** major
**Priority:** medium

---
