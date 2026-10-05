# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 331 — "Lesson Survey"](https://app.qase.io/project/PX?suite=331) (18 existing cases, under OOP FEATURES → Aso, parent 330, custom setting "Delete Lesson Survey"). Four existing cases (#27137, #28915, #28916, #28917) assert that `Lesson_Survey_Response__c` ("Lesson Survey") is **hard-deleted** when a student is removed from a lesson.

**Code trace — confirmed new gap, parallel to spec Gap #10.** `LessonSurveyHandler.removeRelatedLessonSurveys` (`packages/lesson/main/default/classes/LessonSurveyHandler.cls:167-194`) does the actual delete:
```
List<Lesson_Survey_Response__c> relatedLessonSurveys = baseDQL.doQueryWithBinds(query, binds);
if (!relatedLessonSurveys.isEmpty()) { BaseDML.doDelete(relatedLessonSurveys); }
```
Called from `StudentSessionsHandler.removeRelatedLessonSurvey` (`StudentSessionsHandler.cls:2176-2200`), gated by `Lesson_Custom_Settings__c.Delete_Lesson_Survey__c`. It fires only on two `Student_Sessions__c` trigger events: `afterDelete` (record actually deleted, `cls:2165-2170`) or `afterUpdate` when `Lesson__c` transitions non-null→null (`cls:1749`, condition at `cls:2188-2195`). Both the order-driven removal path (cancel/void → `LessonClassMemberHandler.cls:349` → `StudentSessionsHandler.unassignStudentSessionsFromLesson`, `cls:470-548`) and the manual-removal UI path (`cls:586,592`) funnel through this same mechanism.

Under the archive flow, **neither trigger event ever fires**: `Student_Sessions__c.Is_Archived__c` is a formula, so archiving the parent LA writes zero DML to `Student_Sessions__c` — `Lesson__c` is never nulled. Confirmed directly: `LessonAllocationHandler.afterUpdate` skips archived LAs before the cleanup enqueue (`Archived_At__c != null → continue`, `cls:1326-1332`), and `ManualSessionCleanupMasterQueueExecutor` filters `WHERE ... Archived_At__c = NULL` (`cls:7`) / `Is_Archived__c = FALSE` (`cls:53`) — the entire pipeline that triggers survey deletion is bypassed by design once an LA archives. `Lesson_Survey_Response__c`'s own fields (`Answer__c`, `Lesson__c`, `Question__c`, `Question_Name__c`, `Response__c`, `Student__c`) carry no `Is_Archived__c` and no formula referencing either parent's archive state.

**Not affected:** case #27137 (LA end-date reduction while other orders keep the LA alive) routes through `ManualSessionCleanupMasterQueueExecutor`, which only processes LAs where `Archived_At__c = NULL` — i.e. exactly the condition under which deletion already works today. Included below as a control case, not a gap.

## Suite: Lesson Survey

### [Aso] Lesson Survey – Cancel Full Order – Student's Lesson Allocation Archived – Survey Record Orphaned, Not Deleted

**Description:** AC-1 / Gap #10-class (new, code-confirmed) — Decision Table — contrasts with existing baseline (#28916 "Auto-removal by cancelling a full order – Survey is deleted"). Cancelling the full order that is the sole active order behind Student A's enrollment archives the Lesson Allocation (per AC-1); the associated `Lesson_Survey_Response__c` is expected — per the code trace above — to remain in the system rather than being deleted, since the delete trigger never fires for an archived allocation.

**Preconditions:**
- HQ or CM Staff is logged in to the Aso Salesforce org.
- Student A is enrolled in a Lesson through a full order, where this order is the only active order in Student A's `Student_Course_ID__c` group (so cancelling it satisfies AC-1's archive trigger).
- A `Lesson_Survey_Response__c` exists for Student A for that Lesson.
- `Lesson_Custom_Settings__c.Enable_Lesson_Allocation_Archive__c = TRUE`.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff cancels the full order associated with Student A's lesson enrollment | The full order is cancelled successfully; Student A's Lesson Allocation shows `Archived_At__c` populated (archived, not deleted) | Lesson_Allocation Archived_At__c = current timestamp |
| 2 | HQ or CM Staff opens the affected Lesson and checks Student A's participant status | Student A's Student Session shows `Is_Archived__c = TRUE` via formula; `Lesson__c` remains set to the affected lesson (not nulled) — Student A is excluded from active participant views but the session record itself still exists | Student_Sessions Is_Archived__c = TRUE; Lesson__c unchanged |
| 3 | HQ or CM Staff opens or searches for the `Lesson_Survey_Response__c` associated with Student A and the affected lesson | The Lesson Survey record still exists — it was not deleted, since no `Student_Sessions__c` delete/field-nulling trigger fired for the archived allocation | Expect: 1 Lesson_Survey_Response__c record found, unchanged from before archive |

**Severity:** critical
**Priority:** high

---

### [Aso] Lesson Survey – Void New Order – Student's Lesson Allocation Archived – Survey Record Orphaned, Not Deleted

**Description:** AC-1 / Gap #10-class (new, code-confirmed) — Decision Table — contrasts with existing baseline (#28917 "Auto-removal by voiding a new order – Survey is deleted"). Same mechanism as the cancel-order case above, triggered via Void instead of Cancel.

**Preconditions:**
- HQ or CM Staff is logged in to the Aso Salesforce org.
- Student A is enrolled in a Lesson through a new order, where this order is the only active order in Student A's `Student_Course_ID__c` group.
- A `Lesson_Survey_Response__c` exists for Student A for that Lesson.
- `Lesson_Custom_Settings__c.Enable_Lesson_Allocation_Archive__c = TRUE`.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff voids the new order associated with Student A's lesson enrollment | The new order is voided successfully; Student A's Lesson Allocation shows `Archived_At__c` populated | Lesson_Allocation Archived_At__c = current timestamp |
| 2 | HQ or CM Staff opens the affected Lesson and checks Student A's participant status | Student A's Student Session shows `Is_Archived__c = TRUE`; `Lesson__c` remains set (not nulled) | Student_Sessions Is_Archived__c = TRUE; Lesson__c unchanged |
| 3 | HQ or CM Staff opens or searches for the `Lesson_Survey_Response__c` associated with Student A and the affected lesson | The Lesson Survey record still exists, unchanged — no deletion trigger fired | Expect: 1 Lesson_Survey_Response__c record found |

**Severity:** critical
**Priority:** high

---

### [Aso] Lesson Survey – Teacher Views Responses in Back Office – Archived Student's Orphaned Survey Still Listed

**Description:** AC-5 (downstream impact) — Negative — extends the existing baseline (#1987 "Teacher views all student survey responses for a lesson in Back Office", which has no archive dimension). Because the orphaned survey from the gap cases above has no `Is_Archived__c` of its own and the BO list query is not confirmed to join back to `Student_Sessions__c.Is_Archived__c`, an archived student's stale survey response risks still appearing in the teacher's list as if the student were an active participant.

**Preconditions:**
- Teacher has access to Back Office.
- Student A's Lesson Allocation for a given Lesson is archived (per either gap case above), and Student A's `Lesson_Survey_Response__c` for that Lesson was left orphaned (not deleted).
- Student B is still actively enrolled in the same Lesson and has also submitted a survey response.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Teacher logs into Back Office and navigates to the Lesson detail page's survey response section | The survey response list is displayed | Lesson has 2 survey responses on file: Student A (archived) and Student B (active) |
| 2 | Teacher reviews the list of student responses | Per AC-5's principle, an archived student's response should not be presented as belonging to an active participant — record actual behavior: Student A's orphaned response is excluded or clearly marked as inactive (pass), or appears indistinguishable from Student B's active response (fail — route to the engineering owner of this gap) | Actual result to be captured; no code trace confirmed either way for the BO list's own filter |

**Severity:** major
**Priority:** high

---

### [Aso] Lesson Survey – Reduce Lesson Allocation End Date While Other Orders Remain – Survey Still Deleted as Before

**Description:** AC-1 (parity) — Regression — control case confirming existing baseline #27137 ("Reduce Lesson Allocation End Date – Survey for removed Individual Student is deleted") is unaffected by the archive refactor, since `ManualSessionCleanupMasterQueueExecutor` only processes Lesson Allocations where `Archived_At__c = NULL` — exactly the state of an LA whose end date shrank but did not fully archive.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- Individual Student A has an individual Lesson Allocation ending on 2026-03-31; other orders in the group remain active, so the allocation itself does not archive.
- A Student Session and `Lesson_Survey_Response__c` for Student A exist on the lesson dated 2026-02-15.
- The Lesson Allocation end date is reduced to 2026-02-08.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff reduces the Lesson Allocation end date to 2026-02-08 | The Lesson Allocation ends on 2026-02-08; `Archived_At__c` remains null (the allocation itself never archives) | new_end_date = 2026-02-08; Archived_At__c = null |
| 2 | HQ or CM Staff opens the lesson dated 2026-02-15 (now outside the allocation's range) | Individual Student A is removed from the lesson via the normal cleanup pipeline, since the allocation is not archived and `ManualSessionCleanupMasterQueueExecutor` still processes it | lesson_date = 2026-02-15 |
| 3 | HQ or CM Staff opens the Lesson Survey for the 2026-02-15 lesson | No Lesson Survey record exists for Individual Student A — deletion still works exactly as before, confirming this path is not part of the archive gap | Expect: 0 Lesson_Survey_Response__c records for Student A on this lesson |

**Severity:** minor
**Priority:** medium

---

### [Aso] Lesson Survey – Unarchive Round Trip – Lesson Allocation Restored – No Duplicate Survey Created

**Description:** AC-3 (same-Id restore) — Regression — confirms that once a living Student Package Order reappears and the archived Lesson Allocation is restored on the same Id, no second `Lesson_Survey_Response__c` is created for the same (student, lesson) pair — the orphaned original (per the gap cases above) should remain the single record of truth.

**Preconditions:**
- Student A's Lesson Allocation was archived per the cancel/void gap case above, leaving one orphaned `Lesson_Survey_Response__c` for Student A on the affected Lesson.
- A living Student Package Order reappears for Student A's Student Course, and the Lesson Allocation is unarchived on the same record Id (`Archived_At__c` cleared).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff confirms the Lesson Allocation is restored | `Archived_At__c` is null again (restored, same Id); Student A's Student Session shows `Is_Archived__c = FALSE` | LA Archived_At__c = null (restored) |
| 2 | HQ or CM Staff opens or searches for `Lesson_Survey_Response__c` records belonging to Student A on the affected Lesson | Exactly one record is found — the original orphaned one, untouched by the restore. No duplicate was created | Expect: 1 Lesson_Survey_Response__c record for (Student A, affected lesson) |
| 3 | Student A logs into the mobile app and opens the affected lesson's survey | The original survey response is shown normally, consistent with attendance/report history surviving the archive→unarchive round trip | Student A can view their prior response without error |

**Severity:** minor
**Priority:** medium

---
