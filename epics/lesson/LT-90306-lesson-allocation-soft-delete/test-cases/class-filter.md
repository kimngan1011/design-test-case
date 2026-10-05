# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 1410 — "Class Filter"](https://app.qase.io/project/PX?suite=1410) (15 existing cases), child of suite 1291. The filter operates entirely on the dataset already returned by `getActiveLessonAllocationByLocationCourseId`/`getInactiveLessonAllocationByLocationCourseId`, both of which exclude archived Lesson Allocations upstream (see `location-course-active-student.md`). This case locks in that an archived student is therefore never miscategorized under any filter option (including "No Assigned Class"), since they are absent from the base dataset entirely rather than being reclassified.

## Suite: Class Filter

### Class Filter – Lesson Allocation Archived – Student Not Miscategorized Under Any Filter Option; Restored Student Filterable by Class Again

**Description:** Regression / control case — Decision Table — a student whose Lesson Allocation has been archived does not appear under the matching class filter, nor does it get miscategorized under "No Assigned Class" (even though their underlying Class Member record still technically exists, archived) — they are simply absent from the page entirely until restored.

**Preconditions:**
- Student A is a member of Class A; Student B is also a member of Class A and remains active throughout.
- Student A's Lesson Allocation is subsequently archived (Archived_At__c populated) after its Student Package Order was fully removed.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Class Filter on the Location Course's Active Student page and selects Class A | Only Student B appears; Student A does not appear under Class A | Student A excluded at the base query level, before class filtering |
| 2 | HQ or CM Staff resets the filter and selects "No Assigned Class" instead | Student A does NOT appear here either, even though their Class Member record technically still exists (archived) | Student A excluded from the entire underlying dataset, not reclassified as unassigned |
| 3 | HQ or CM Staff resets the filter to show the full unfiltered Active Student list | Student A still does not appear anywhere on this page | Confirms archived students are excluded upstream of all Class Filter options, not selectively miscategorized |
| 4 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id | Student A's Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 5 | HQ or CM Staff selects Class A in the Class Filter again | Student A now appears alongside Student B under Class A | Student A Archived_At__c = blank (restored) → correctly filterable again |

**Severity:** major
**Priority:** medium

---
