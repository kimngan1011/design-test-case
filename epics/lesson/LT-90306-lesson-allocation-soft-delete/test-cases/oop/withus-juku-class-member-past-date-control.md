# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suites reviewed: "Direct Class Assignment" (3304, 8 cases), "Order Group Class Member" (3306, 8 cases), "Class Member History" (3307, 5 cases) — all under "Withus Juku | Allowing past dates for Classmember start date" (LT-107256, parent 3303). Completes the sweep started in `withus-juku-class-member-import-archive-gap.md` for the one confirmed gap (Import). None of these 21 cases reference `Archived_At__c`/`Is_Archived__c`.

**Code-trace confirmation — all three already safe, control cases only.** This feature is generic shared code (`LessonClassMemberHandler.cls`, `modalAssignClass.js`), not WithUs-Juku-specific. The Contact/Course picker (and, by the same code, Location Course and LA Student Session) already excludes archived LAs (`LessonAllocationController.cls:15`). Create Order / Add New Course correctly implements AC-3's same-Id restore (`LessonAllocationSyncService.collectAllocationsToUnarchive:660`, `buildUnarchivedAllocation:1011/1019`, duplicate-prevention via `shouldSkipAllocationCreation:880/901`). Class Member History's timeline queries already filter `Is_Archived__c = FALSE` (`LessonClassMemberRepo.cls:138-146`, `LessonClassMemberHandler.cls:515-529`).

## Suite: Direct Class Assignment

### [WithUs Juku] Direct Class Assignment – Archived LA Not Selectable in the Contact/Course Picker

**Description:** AC-5 (parity) — Regression — control case. Contrasts with existing baseline (#26082 "Contact Course Assignment – LA Start Date – Past effective date accepted"). Code-confirmed: `LessonAllocationController.cls:15` already filters `Archived_At__c = NULL`, so an archived LA never appears as an assignable candidate in the Contact > Course "Assign Class" picker.

**Preconditions:**
- Student A has a Course A Lesson Allocation, archived (`Archived_At__c` populated). Student B has an active Course A Lesson Allocation.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Student A's Contact > Course record and selects Assign Class for Course A | Student A's archived LA does not appear as an assignable target | Student A LA Archived_At__c = populated |
| 2 | HQ or CM Staff opens Student B's Contact > Course record and selects Assign Class for Course A | Student B's active LA appears and is assignable, with the normal "Allow Start In The Past" lower-bound validation applying | Student B LA Archived_At__c = blank |

**Severity:** minor
**Priority:** medium

---

## Suite: Order Group Class Member

### [WithUs Juku] Add New Course – Student Previously Had an Archived LA for the Same Course – Existing LA Restored, Not Duplicated

**Description:** AC-3 (parity) — Regression — control case. Contrasts with existing baseline (#26103 "Add New Course – One-Time product – Class Member synced to Back Office", which assumes a brand-new LA with no prior history). Code-confirmed: `LessonAllocationSyncService.collectAllocationsToUnarchive`/`buildUnarchivedAllocation` restore the existing LA by the same record Id when a living order reappears for the same `Student_Course_ID__c` grouping; `shouldSkipAllocationCreation` prevents a duplicate regardless of archive state.

**Preconditions:**
- Student A previously had a Course B Lesson Allocation (same Student_Course_ID__c grouping Student A would re-enroll into) that is now archived (`Archived_At__c` populated, order group previously fully removed).
- Student A has an active One-Time product for Course A.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff starts an update order for Student A's existing One-Time product, adds Course B (the same course as the archived LA), selects Class B, and submits | Per AC-3, the system should restore Student A's existing archived Course B Lesson Allocation on the same record Id, not create a second, separate one | Archived LA's Student_Course_ID__c matches the new order's grouping |
| 2 | HQ or CM Staff opens Student A's Course B Lesson Allocation | Exactly one Lesson Allocation record exists for Course B — the original Id, now with `Archived_At__c` cleared | Expect: 1 LA record, same Id as before archive |
| 3 | HQ or CM Staff opens the Course B Class Member | The Class Member is linked to the restored (same-Id) Lesson Allocation, with start/end dates recomputed per the new order | Class Member Lesson_Allocation__c = the restored LA's Id |

**Severity:** minor
**Priority:** medium

---

## Suite: Class Member History

### [WithUs Juku] Class Member History – Archived LA's Old Class Members Do Not Interfere With a New Assignment's Timeline

**Description:** AC-5 (parity) — Regression — control case. Contrasts with existing baseline (#26096 "History – Same effective date as active class – Latest class becomes active", which assumes only currently-active Class Members exist). Code-confirmed: the timeline/overlap queries (`LessonClassMemberRepo.getActiveClsMembersByLessonAllocationId`, `LessonClassMemberHandler.buildClassMemberTimeline`) already filter `Is_Archived__c = FALSE`.

**Preconditions:**
- Student A has a Course A Lesson Allocation that was previously archived and later restored (same Id). Before the archive, Class A was assigned to it (now `Is_Archived__c = TRUE` via the old archive cycle, since it predates the restore). After restore, a fresh assignment history starts clean.
- Student A's restored Course A LA runs 2026-07-01 through 2026-12-31. No new Class has been assigned since the restore.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Student A's Contact > Course record and selects Assign Class for Course A, selects Class B, and enters 2026-07-01 (the LA's restored start date) | Per AC-5, the assignment is accepted purely on today's state — the old, now-historical Class A record (from before the archive cycle) must not be treated as a currently-overlapping active class | Old Class A Is_Archived__c = TRUE (pre-restore history); not considered by the timeline query |
| 2 | HQ or CM Staff opens Student A's Class Member history | Class B is active from 2026-07-01 through 2026-12-31; the old Class A entry remains visible only as historical record (not affecting the new timeline calculation) | Timeline query excludes Is_Archived__c = TRUE rows |

**Severity:** minor
**Priority:** medium

---
