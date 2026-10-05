# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 1791 — "Change Course and Class in Lesson Schedule Detail"](https://app.qase.io/project/PX?suite=1791) (32 existing cases). None test the add-class auto-merge behavior when a student's Lesson Allocation is archived.

Code trace: adding a Class to a Lesson Schedule (`LessonScheduleClassHandler.lwcCreateLessonScheduleClasses` → `createLessonScheduleClasses` → `LessonClassMemberHandler.createAssignClassMemberJobByClassIds` → `LessonClassMemberRepo.getActiveClassMembersByClassIds`) filters `Is_Archived__c = FALSE` on `Class_Member__c`. The downstream merge executor, `ClassMemberMasterQueueExecutor.doStart`, independently re-queries the Lesson Allocation with `Archived_At__c = NULL`. So a student whose Class Member is tied to an already-archived Lesson Allocation is excluded from the one-time "add class → merge students into future lessons" job at two independent layers — same convention as every other flow already covered in this epic.

**Confirmed gap:** `LessonAllocationSyncService`'s restore/unarchive path (`executeSyncPlan` → `DmlLessonAllocationWriter.unarchiveAllocations` → `UnarchivedSessionDeduplicator`) never calls `resyncClassMemberByLessonAllocationId`, `createAssignClassMemberJobs`, or enqueues `ASSIGN_CLASS_MEMBER`. Restoring the Lesson Allocation flips `Class_Member__c.Is_Archived__c` back to `FALSE` immediately via formula (so the record is now *data-correct*), but nothing re-triggers the "merge into future lessons" job that already ran and skipped this student while the allocation was archived. Unlike the Location Course / LA Detail flows (suite 1291/1293, where the student's session already existed and only needed the formula to flip to reappear), here no session was ever created for this student on this class's future lessons — the student stays silently excluded until staff manually re-trigger a resync (e.g., `resyncClassMemberByLessonAllocationId`, or remove-and-re-add the Class on the schedule).

## Suite: Change Course and Class in Lesson Schedule Detail

### Lesson Schedule – Add Class to Classless Schedule – Student's Lesson Allocation Archived – Excluded from Auto-Merge into Future Lessons

**Description:** Regression / control case — Decision Table, contrasts with the baseline (case 13962, "Add Class to Classless Schedule... Class A students auto-assigned to all future lesson instances") — a student with a Class Member for the newly-added class is excluded from the auto-merge into future lessons because their Lesson Allocation is already archived at the moment the class is added.

**Preconditions:**
- Lesson Schedule exists with Course X and no classes assigned. Future lessons exist with no students.
- Class A is available under Course X. Student A has a Class Member for Class A, but Student A's Lesson Allocation for Course X has already been archived (Archived_At__c populated) after its Student Package Order was fully removed. Student B also has a Class Member for Class A, with an active (non-archived) Lesson Allocation.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff adds Class A to the Lesson Schedule | Class A is added; the schedule now has one class | Schedule now has one class |
| 2 | HQ or CM Staff opens a future lesson from this schedule | Student B appears in the lesson's Student Sessions; Student A does NOT appear | Student B Is_Archived__c = FALSE → merged in; Student A Is_Archived__c = TRUE (via formula) → excluded from the merge job |
| 3 | HQ or CM Staff opens Student A's Class Member record directly by record Id | The Class Member record exists and is tied to Class A, but no Student Session was ever created for Student A on this schedule's lessons | getActiveClassMembersByClassIds / ClassMemberMasterQueueExecutor excluded Student A at the merge-query layer, before any session creation |

**Severity:** major
**Priority:** high

---

### Lesson Schedule – Student Excluded from Class-Add Merge Due to Archive – Lesson Allocation Restored – Student Does Not Automatically Reappear in Future Lessons

**Description:** Gap case — Decision Table — continuing from the scenario above, once Student A's Lesson Allocation is restored, their Class Member becomes data-correct (`Is_Archived__c` flips to FALSE via formula) but the one-time "merge into future lessons" job that already ran while archived is never automatically re-triggered. Unlike the Location Course / LA Detail restore cases (suite 1291/1293) where a previously-hidden session simply reappears, here no session was ever created for Student A on this class's future lessons, so nothing exists to reappear — Student A stays silently excluded until a manual resync.

**Preconditions:**
- Following directly from the scenario above: Class A was added to the Lesson Schedule while Student A's Lesson Allocation was archived, so Student A's Class Member exists but was excluded from the merge — Student A does not appear in any future lesson for this schedule, and no Student Session record for Student A/Class A exists yet.
- A living Student Package Order reappears for Student A's Course X Student Course, so the Lesson Allocation is unarchived on the same record Id.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff confirms Student A's Lesson Allocation shows Archived_At__c blank again | The Lesson Allocation is restored | Archived_At__c = null (restored); Student A Class Member Is_Archived__c = FALSE (via formula) |
| 2 | HQ or CM Staff opens the same future lesson from this schedule (no other action taken) | Student A still does NOT appear in the lesson's Student Sessions, even though their Class Member is now data-correct | No DML path in LessonAllocationSyncService's restore flow (executeSyncPlan / UnarchivedSessionDeduplicator) re-enqueues ASSIGN_CLASS_MEMBER or calls resyncClassMemberByLessonAllocationId for this allocation |
| 3 | HQ or CM Staff manually triggers a resync for Student A's Lesson Allocation (e.g., via the LA Detail "Assign Class" resync action, or by removing and re-adding Class A on the schedule) | Student A now appears in the lesson's Student Sessions, same as Student B | Manual resync re-enqueues ASSIGN_CLASS_MEMBER, which now includes Student A since Is_Archived__c = FALSE |

**Severity:** major
**Priority:** high

---

### Lesson Schedule – Student Auto-Assigned via Class Add – Lesson Allocation Archived – Hidden from Lesson; Restored – Shown Again

**Description:** Feature Impact (Class Assignment / Master Queue) — Decision Table — contrasts with the two cases above: here Student A's Lesson Allocation is still active at the moment Class A is added to the Lesson Schedule, so Student A IS merged into future lessons normally (per the case 13962 baseline). Only afterward does the Lesson Allocation get archived — since the Student Session already exists at that point, it is hidden purely by the `Is_Archived__c` formula (no re-merge needed), and reappears on the same record once the Lesson Allocation is restored, matching the pattern already locked in for the Location Course and CSV import flows (suite 1291, "Import Class Member").

**Preconditions:**
- Lesson Schedule exists with Course X and no classes assigned. Future lessons exist with no students.
- Class A is available under Course X with Student A as an active Class Member (Student A's Lesson Allocation for Course X is active, Archived_At__c blank). HQ or CM Staff has added Class A to the Lesson Schedule, and Student A now appears in this schedule's future lessons' Student Sessions.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens a future lesson from this schedule | Student A is listed as an active student in Student Sessions | Student A Is_Archived__c = FALSE → shown |
| 2 | The Student Package Order behind Student A's Course X Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated; Student A's Student Session (created by the class-add merge) flips to archived via the same formula | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff reopens the same future lesson from this schedule | Student A no longer appears in Student Sessions | Student A Is_Archived__c = TRUE (via formula) → hidden |
| 4 | A living Student Package Order reappears for Student A's Course X Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 5 | HQ or CM Staff reopens the same future lesson from this schedule | Student A reappears in Student Sessions — the same original record created by the class-add merge, not newly created | Student A Is_Archived__c = FALSE (restored) → shown again |

**Severity:** major
**Priority:** high

---
