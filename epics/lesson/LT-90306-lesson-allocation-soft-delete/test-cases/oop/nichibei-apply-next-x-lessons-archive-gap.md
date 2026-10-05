# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 2195 — "Assign a student on Calendar SF"](https://app.qase.io/project/PX?suite=2195) (7 existing cases, under "Apply specific lesson number when assigning selected lessons onwards" / LT-92191, OOP FEATURES → Nichibei → Point Consumption, parent 372). A bulk-assign flow: staff pick a Lesson Allocation first, then assign a student to a lesson chain starting at a selected lesson with "Apply to Next X Lessons" (a specific number). None of the 7 cases reference `Archived_At__c`/`Is_Archived__c`.

**Code-trace findings:** the "Select a LA" step reuses the same generic picker already confirmed elsewhere in this epic (`LessonMasterHandler.cls:46`, `WHERE ... AND Archived_At__c = NULL`) — already safe. The "existing student not duplicated" check (`StudentSessionsHandler.cls:2373-2385`) already filters `Is_Deleted__c = FALSE AND Is_Archived__c = FALSE` before building its dedup map — an archived-only existing session is correctly treated as "not currently assigned." Both included below as control cases, not gaps.

**New finding:** "Lesson Allocation Status = Over Assigned" (`Status__c` formula comparing roll-up `Allocated_Sessions__c` — filtered only by `Assigned_Lesson__c = TRUE AND Is_Deleted__c = FALSE`, no archive awareness — against `Total_Session_Count__c`) is inert while an LA is archived (the LA is hidden everywhere else anyway), but AC-3 requires `Total_Session_Count__c`/`Purchased_Slot_Number__c` to be recomputed from only the living orders at restore time. If that recomputed total comes back smaller than the actual session count retained through the archive/restore round trip (archiving never deletes sessions), the LA can surface as "Over Assigned" immediately after restore even though it was never over-assigned before archiving.

**Scope:** archived LA must not be selectable/usable in this flow; restore must work normally — including surfacing (not silently hiding) the Over Assigned edge case above so QA/dev know to check it.

## Suite: Assign a student on Calendar SF

### [Nichibei] Apply to Next X Lessons – Select a LA – Archived LA Not Selectable (Control Case)

**Description:** AC-5 (parity) — Regression — control case, not a gap. Code-confirmed: `LessonMasterHandler.cls:46` already filters `Archived_At__c = NULL` for the student/LA search feeding this bulk-assign flow's "Select a LA" step. Locks in that this separate LWC entry point (`splitViewRightManaCalendarMultipleAssign`) is already correct and unaffected by this epic, parallel to the already-covered single Add-Student picker.

**Preconditions:**
- HQ or CM Staff is on the Calendar SF view with a recurring/custom lesson chain available.
- Student A has an archived Lesson Allocation for the relevant course (`Archived_At__c` populated); Student B has an active Lesson Allocation for the same course.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the student/LA search panel and searches for Student A | Student A's archived Lesson Allocation does not appear as a selectable candidate | Student A LA Archived_At__c = populated → excluded |
| 2 | HQ or CM Staff searches for Student B | Student B's active Lesson Allocation appears and is selectable | Student B LA Archived_At__c = null → shown |

**Severity:** minor
**Priority:** medium

---

### [Nichibei] Apply to Next X Lessons – Duplicate Check – Archived-Only Existing Session Does Not Block Re-Assignment (Control Case)

**Description:** AC-5 (parity) — Regression — control case, not a gap. Code-confirmed: `StudentSessionsHandler.cls:2373-2385` filters `Is_Deleted__c = FALSE AND Is_Archived__c = FALSE` before building the dedup map, so a student whose only existing session for a lesson in the assignment range is archived is correctly treated as "not currently assigned" — extends existing baseline #15533 "Verify existing student is not duplicated."

**Preconditions:**
- Student A previously had a Student Session for Lesson 3 in the chain, but that session's Lesson Allocation has since archived (`Archived_At__c` populated), so the session is `Is_Archived__c = TRUE`.
- HQ or CM Staff selects a new, active Lesson Allocation for Student A and starts "Apply to Next X Lessons" from Lesson 1, with X covering Lesson 3.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff selects the active LA and assigns Student A with "Apply to Next X Lessons" covering Lessons 1 through 4 (including Lesson 3) | Per the dedup check's `Is_Archived__c = FALSE` filter, Student A is treated as not currently assigned to Lesson 3 and receives a fresh Student Session there, not skipped | Old Lesson 3 session Is_Archived__c = TRUE → excluded from dedup map |
| 2 | HQ or CM Staff checks Lesson 3's Student Sessions | Two Student Session records exist for Student A on Lesson 3: the old archived one (preserved for history) and a new active one tied to the new LA | Expect: 1 archived + 1 active session, no error or skip |

**Severity:** minor
**Priority:** medium

---

### [Nichibei] Apply to Next X Lessons – Lesson Allocation Archived – Bulk-Assigned Sessions Hidden; Restored – Sessions Reappear

**Description:** AC-5 — Regression — confirms the general `Is_Archived__c` formula principle (already proven for the single Add-Student picker in `assign-unassign-student-lesson-schedule.md`) also holds for sessions created via this separate bulk-assign LWC (`splitViewRightManaCalendarMultipleAssign`), since it's a different code path worth its own confirmation rather than being assumed.

**Preconditions:**
- HQ or CM Staff selected an LA and bulk-assigned Student A to Lessons 1–4 via "Apply to Next X Lessons" (X = 4). Student A currently appears in all 4 lessons' Student Sessions, `Is_Archived__c = FALSE`.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | The Student Package Order group behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 2 | HQ or CM Staff reopens Lessons 1–4's Student Session lists | Student A no longer appears in any of the 4 lessons — all 4 sessions' Is_Archived__c = TRUE via formula | All 4 sessions hidden |
| 3 | A living Student Package Order reappears for the same Student_Course_ID__c group, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 4 | HQ or CM Staff reopens Lessons 1–4's Student Session lists | Student A reappears in all 4 lessons — the same original sessions, not newly created | All 4 sessions Is_Archived__c = FALSE (restored) |

**Severity:** major
**Priority:** high

---

### [Nichibei] Restore – Recomputed Total Session Count Smaller Than Retained Sessions – Lesson Allocation Surfaces as Over Assigned

**Description:** AC-3 — Decision Table — [UNVERIFIED]. New finding, not covered by any existing case: per AC-3, unarchiving recomputes `Total_Session_Count__c`/`Purchased_Slot_Number__c` from only the orders that are living at restore time. Since archiving never deletes any Student Session, if the restored LA's recomputed total is smaller than the number of sessions it already holds (because fewer orders came back alive than were present before the archive), the `Status__c` formula (`Allocated_Sessions__c > Total_Session_Count__c` → `Over_Assigned`) can flip the LA to "Over Assigned" immediately on restore, even though it was never over-assigned before archiving.

**Preconditions:**
- Student A's Lesson Allocation originally had Purchased_Slot_Number/Total_Session_Count = 10, with exactly 10 active Student Sessions assigned (`Allocated_Sessions__c = 10`, Status = normal, not Over Assigned).
- The full order group is removed, archiving the Lesson Allocation (`Archived_At__c` populated). The 10 Student Sessions become `Is_Archived__c = TRUE` but are not deleted.
- Only a subset of the original orders reappears as living — enough to support a recomputed Total_Session_Count__c of 6, not the original 10 — and the Lesson Allocation is unarchived on the same record Id.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff confirms the Lesson Allocation is restored and checks `Total_Session_Count__c` | Per AC-3, the recomputed value reflects only the living orders — 6, not the original 10 | Total_Session_Count__c = 6 (recomputed) |
| 2 | HQ or CM Staff checks the 10 original Student Sessions | All 10 are restored to `Is_Archived__c = FALSE` — none were deleted by the archive/restore cycle, since archiving never touches `Is_Deleted__c` | Allocated_Sessions__c rollup = 10 (unchanged, filtered only by Is_Deleted__c) |
| 3 | HQ or CM Staff opens the Lesson Allocation record and checks its Status | [UNVERIFIED] Record actual behavior: Status shows "Over Assigned" (10 > 6) immediately upon restore, surfacing a condition that did not exist before the archive — this is an expected consequence of AC-3's recompute rule, not a defect in the archive mechanism itself, but staff must be made aware it can happen so they aren't confused by an unexpected status change on a routine restore | Status__c = Over Assigned if Allocated_Sessions__c (10) > Total_Session_Count__c (6) |

**Severity:** critical
**Priority:** high

---
