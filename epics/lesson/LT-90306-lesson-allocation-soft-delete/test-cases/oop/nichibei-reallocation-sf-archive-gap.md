# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 1274 — "SF Reallocation"](https://app.qase.io/project/PX?suite=1274) (21 existing cases, under "Reallocation" / LT-85058, OOP FEATURES → Nichibei, parent 371). This is spec.md's named "Nichibei Reallocation" High-risk OOP impact and directly instantiates spec Business Rule #10's gap list, which already names `Reallocation__c` as an object with no archived state. None of the 21 cases reference `Archived_At__c`/`Is_Archived__c`.

**Business logic (from the existing cases):** marking an absent student session `Reallocate = TRUE` creates a `Reallocation__c` request, visible in a "Reallocation list." Staff later link it to a new lesson via the "Reallocate Lesson" picker (filtered by location/date range/capacity), creating a linked "Reallocate" Student Session. The request/session auto-deletes when the original is unflagged, attendance reverts, the student is removed, or the original lesson is deleted — but only while the linked new lesson is Draft/Published/Cancelled; once Completed, the system blocks the change instead. Removing the original also refunds points (shared with the already-covered Point Consumption flow).

**Code-trace confirmation (same architecture as the already-confirmed Lesson Survey gap):** cleanup (`ReallocationHandler.unflagReallocationStudentSession(s)`, `modifyReallocationAfterUnassignSessions`, `updateReallocationAfterRemoveStudentSessions`) is bound entirely to actual `Student_Sessions__c` DML (deleted, or `Lesson__c` nulled) — the same shared `unassignStudentSessionsFromLesson` method used by the Point Consumption refund flow. Archiving an LA (`LessonAllocationSyncService.cls:1450-1464`) only updates `Archived_At__c`, firing none of this. `ManualSessionCleanupMasterQueueExecutor` (the one job that does reconcile Reallocation pairs) is explicitly skipped for archived LAs (`LessonAllocationHandler.cls:1327-1329`). The "Reallocation list" query (`ReallocationHandler.buildReallocationListWithFilterQuery:413-474`) has no archive filter at all. **More severe than other gaps in this epic:** the "Reallocate Lesson" picker itself (`LessonHandler.getReallocateLessonList:481-494`, `ReallocationHandler.updateReallocationBySessionTypeRegular/Reallocate:113-164`) never checks the request's own Lesson Allocation archive state before allowing a new lesson to be linked — unlike every other LA-selection picker already confirmed elsewhere in this epic.

## Suite: SF Reallocation

### [Nichibei] Reallocation – Open Request Survives LA Archive – Remains Listed and Actionable in the Reallocation List

**Description:** AC-1 / Gap (Business Rule #10) — Decision Table. Contrasts with existing baseline (#10392 "Update the Reallocate flag with no linked lesson", #10406 "Remove original student with no linked lesson" — both confirm the request disappears from the list once the original is properly removed/unflagged through the legacy hard-delete path). Under the archive flow, the equivalent cleanup never fires, so an open request for an archived student's session stays listed as if the student were still actively enrolled.

**Preconditions:**
- Student A's Student Session on Lesson A is marked Absent with `Reallocate = TRUE` — an open `Reallocation__c` request exists (Request Status = Open, no linked New Lesson).
- `Lesson_Custom_Settings__c.Enable_Lesson_Allocation_Archive__c = TRUE`.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff confirms the open Reallocate request for Student A appears in the Reallocation list | The request is listed with Request Status = Open | Reallocation__c exists, Reallocate_Status__c = Open |
| 2 | The Student Package Order group behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated; Student A's Student Session on Lesson A becomes Is_Archived__c = TRUE via formula, hidden from the lesson's active roster | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff reopens the Reallocation list | Per AC-5's general exclusion principle, an archived student's request should no longer be actionable here — but since `buildReallocationListWithFilterQuery` has no archive filter, the request remains listed as Open, as if Student A were still actively enrolled | Request still shown — gap, route to the engineering owner of the Reallocation__c archive-state work |

**Severity:** critical
**Priority:** high

---

### [Nichibei] Reallocation – "Reallocate Lesson" Picker Has No Archive Filter – Staff Can Complete a Request Against an Archived Source Session

**Description:** AC-5 — Negative. Contrasts with existing baseline (#10393 "Verify the Reallocate popup", #10394 "User reallocates student to the new lesson" — neither tests an archived source). Directly instantiates the spec's named risk: "must not complete a request against an already-archived record." Unlike the Add-Student picker (`LessonMasterHandler.cls:46`) and Point Consumption priority chain (`BookingLessonHandlerOutSide.cls:638-651`), the Reallocate Lesson picker never checks the request's own Lesson Allocation archive state.

**Preconditions:**
- Student A has an open Reallocate request (per the case above) whose original Lesson Allocation is now archived (`Archived_At__c` populated).
- A new lesson exists that would otherwise be a valid Reallocate Lesson candidate (same location, within the date range, capacity available).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Student A's (still-listed) Reallocate request and clicks "Reallocate Lesson" | Per the spec's named risk, the system should block completing this request since the source session's LA is archived | LA Archived_At__c = populated |
| 2 | HQ or CM Staff selects the candidate new lesson and clicks "Add" | [UNVERIFIED — but code-confirmed no filter exists] Record actual behavior: the student is assigned to the new lesson and the request is marked Approved exactly as if the source were still active, with no block or warning (fail — matches spec's named risk, route to the engineering owner) | No Archived_At__c check anywhere in `updateReallocationBySessionTypeRegular/Reallocate` |

**Severity:** critical
**Priority:** high

---

### [Nichibei] Reallocation – Already-Linked (Approved) Pair Survives LA Archive – Neither Session Is Cleaned Up

**Description:** AC-1 / Gap (Business Rule #10) — Decision Table. Contrasts with existing baseline (#10397/#10398/#10399 "Auto-delete Reallocate session... when unflagging Reallocate" for Draft/Published/Cancelled-status linked lessons — all confirm cleanup under the legacy hard-delete path). Once an LA archives, the equivalent cleanup for an already-Approved Reallocate pair never fires either, since it rides the same `Student_Sessions__c`-DML-bound mechanism.

**Preconditions:**
- Student A's Reallocate request was already completed: Original Lesson A's session is linked to New Lesson B's Reallocate session (Request Status = Approved, Reallocate Counter = 1).
- The Student Package Order group behind Student A's Lesson Allocation is fully removed.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | The Lesson Allocation archives | Both the original session (Lesson A) and the linked Reallocate session (Lesson B) become Is_Archived__c = TRUE via formula — both hidden from their respective lessons' active rosters | Archived_At__c = current timestamp |
| 2 | HQ or CM Staff reopens the Reallocation list | The pair remains listed with Request Status = Approved, exactly as before the archive — neither session was cleaned up, since the cleanup trigger never fired | Reallocate_Status__c = Approved, unchanged |
| 3 | HQ or CM Staff opens Lesson B directly | The orphaned Reallocate session is still attached to Lesson B, even though Student A is no longer actively enrolled anywhere under this Lesson Allocation | Session record exists but Is_Archived__c = TRUE |

**Severity:** critical
**Priority:** high

---

### [Nichibei] Reallocation – Unarchive – Previously Orphaned Request Resumes Normal Behavior, No Duplicate

**Description:** AC-3 — Regression. Confirms that once a living Student Package Order reappears and the Lesson Allocation is restored on the same record Id, the previously-orphaned Reallocate request (open or approved) resumes exactly the behavior it would have had if it had never been archived — cleanup rules apply normally again, and no duplicate request is created.

**Preconditions:**
- Student A's open Reallocate request survived an LA archive per the first case above (still listed as Open).
- A living Student Package Order reappears for the same `Student_Course_ID__c` group, and the Lesson Allocation is unarchived on the same record Id.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff confirms the Lesson Allocation is restored (`Archived_At__c` cleared) | Student A's original Student Session on Lesson A shows Is_Archived__c = FALSE again | Archived_At__c = null (restored) |
| 2 | HQ or CM Staff reopens the Reallocation list | Exactly one open request still exists for Student A — the same original `Reallocation__c` record, not a new one | Expect: 1 Reallocation__c record, Reallocate_Status__c = Open |
| 3 | HQ or CM Staff unflags the Reallocate status on Student A's original session | Per the normal (non-archived) cleanup rule, the request is now correctly removed from the Reallocation list, confirming the cleanup mechanism works again post-restore | Reallocation__c record deleted/updated per normal unflag behavior |

**Severity:** minor
**Priority:** medium

---
