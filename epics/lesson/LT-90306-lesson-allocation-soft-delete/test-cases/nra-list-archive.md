# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 3040 — "Contract List – Not Require Allocation (NRA) List"](https://app.qase.io/project/PX?suite=3040) (2 existing cases, epic LT-98531). Both existing cases only test that the NRA list is hidden for the Riso tenant and that hiding it doesn't break the adjacent Contract List section — neither tests an archived Lesson Allocation.

Code trace: the NRA list (`tableNotRequireLessonAllocation` LWC, Contact → Course tab) calls the same `LessonAllocationHandler.getLessonAllocationByFilter` Apex method as the main "Lesson Allocation" list (`tableStudentCourseSubscription`), just with `requireAllocation: false` instead of `true`. Both branches share one unconditional `WHERE Student__c = :studentId AND Archived_At__c = NULL` clause (`LessonAllocationHandler.cls:518`), applied before the `Require_Allocation__c` filter is even appended — so an archived Not-Require-Allocation LA is already correctly excluded from the NRA list, exactly like an archived Require-Allocation=True LA is excluded from the main list (suite 1291/1293, already covered elsewhere in this epic). This is already correct, but has zero regression coverage specific to the NRA list — the case below locks it in.

## Suite: Contract List – Not Require Allocation (NRA) List

### NRA List – Lesson Allocation (Require Allocation = False) Archived – Excluded from Active and Inactive NRA Lists; Restored – Reappears

**Description:** Regression / control case — Decision Table — a Not-Require-Allocation Lesson Allocation is excluded from both the Active and Inactive NRA list sections once archived, via the same `Archived_At__c = NULL` filter shared with the main Require-Allocation=True list (`LessonAllocationHandler.getLessonAllocationByFilter`), and reappears correctly once restored.

**Preconditions:**
- Student A has a Lesson Allocation for Course A with Require Allocation = False, End_Date_Time__c in the future (so it currently appears in the NRA list's Active section). The tenant is non-Riso (NRA list is shown).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Student A's Contact record, clicks the Course tab, and views the NRA list's Active section | Student A's Course A Lesson Allocation appears in the NRA Active list | Require_Allocation__c = FALSE; Archived_At__c = blank → included |
| 2 | The Student Package Order behind this Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff reopens the Course tab and checks both the NRA Active and Inactive sections | The Lesson Allocation does not appear in either NRA section | Archived LA excluded from getLessonAllocationByFilter regardless of requireAllocation value |
| 4 | A living Student Package Order reappears for Student A's Course A Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 5 | HQ or CM Staff reopens the Course tab and views the NRA list's Active section | The Lesson Allocation reappears in the NRA Active list | Archived_At__c = blank (restored) → included again |

**Severity:** minor
**Priority:** medium

---
