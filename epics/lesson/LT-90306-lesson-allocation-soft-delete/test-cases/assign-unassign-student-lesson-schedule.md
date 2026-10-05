# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 219 — "Create Lesson in Lesson Schedule"](https://app.qase.io/project/PX?suite=219), specifically its manual Assign/Unassign Student cases (IDs 8759, 9696-9698). Those cases cover explicit staff assign/unassign actions and are unaffected by the archive filter themselves — but the underlying Lesson Allocation authorization check that gates every manual assignment is, which is what's covered here.

## Suite: Create Lesson in Lesson Schedule

### Assign Student – Add Student Picker – Lesson Allocation Archived – Student Not Selectable

**Description:** Feature Impact (LA authorization & Add Student) — Decision Table — the Add Student picker on a Lesson must exclude a student whose Lesson Allocation has been archived by the Lesson Allocation soft-delete, so staff cannot manually assign them.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- A lesson exists for Course Math 101 at Location Tokyo HQ on 2026-05-20.
- Student A has a Lesson Allocation for Math 101 that has been archived (Archived_At__c is populated) after its Student Package Order was fully removed.
- Student B has an active Lesson Allocation for Math 101 (Archived_At__c is blank).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the lesson on 2026-05-20 and clicks Add Student | The Add Student search modal opens | "" |
| 2 | HQ or CM Staff searches for Student B | Student B appears in the picker results | Student B Lesson Allocation Archived_At__c = blank → shown |
| 3 | HQ or CM Staff searches for Student A | Student A does not appear in the picker results | Student A Lesson Allocation Archived_At__c populated → hidden |
| 4 | HQ or CM Staff selects Student B and clicks Save | Student B is assigned to the lesson; a Student Session is created | — |
| 5 | HQ or CM Staff opens Student B's Lesson Allocation record | Lesson Allocated count has incremented by 1; Lesson Allocation Status reflects the active assignment; Report History shows the new lesson entry | Student B LA detail fields updated correctly after assignment |
| 6 | A living Student Package Order reappears for Student A's Student Course, so Student A's Lesson Allocation is unarchived on the same record Id | Student A's Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 7 | HQ or CM Staff reopens the lesson on 2026-05-20, clicks Add Student, and searches for Student A | Student A now appears in the picker results | Student A Archived_At__c = blank (restored) → shown |
| 8 | HQ or CM Staff selects Student A and clicks Save | Student A is assigned to the lesson; a Student Session is created | — |
| 9 | HQ or CM Staff opens Student A's Lesson Allocation record | Lesson Allocated count has incremented by 1; Lesson Allocation Status reflects the active assignment; Report History shows the new lesson entry, consistent with an LA that was never archived | Student A LA detail fields updated correctly after assignment |

**Severity:** critical
**Priority:** high

---

### Assign Student – Add Student Popup (REST-Backed Path) – Lesson Allocation Archived – Student Not Selectable (Control Case, Second Code Path)

**Description:** Regression / control case — Decision Table — found during a sweep of whether Nichibei (or any OOP tenant) forks the Add Student popup from Core (it doesn't — see `nichibei-lesson-list-smartphone-archive-gap.md` and `test-coverage.md` Addendum 7). The Add Student modal invoked from a lesson's Student tab (`DialogAddStandardStudentSF.tsx`, used identically by `TabStudentSF.tsx`/`TabStudentSFV2.tsx` regardless of tenant) calls `/services/apexrest/MANAERP/lessonAllocations/retrieve/v1` → `LessonAllocationHandler.cls:92`, a **second**, previously unenumerated query path distinct from the `LessonMasterHandler.cls:46` query already confirmed in the first case above — and it is independently confirmed to already filter `Archived_At__c = NULL`.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- A lesson exists for Course Math 101 on 2026-05-20. Student A has a Lesson Allocation for Math 101 archived (`Archived_At__c` populated). Student B has an active Lesson Allocation for Math 101.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the lesson's Student tab and clicks Add Student | The Add Student modal opens, backed by `LessonAllocationHandler.cls:92` via the REST retrieve endpoint | — |
| 2 | HQ or CM Staff searches for Student A and Student B | Student A does not appear (Archived_At__c populated → excluded); Student B appears (Archived_At__c blank → shown) | `LessonAllocationHandler.cls:92` filters Archived_At__c = NULL |

**Severity:** minor
**Priority:** medium

---

### Assign Student – Lesson Roster – Lesson Allocation Archived After Assignment – Student No Longer Shown

**Description:** Feature Impact (Student Session lifecycle) — Decision Table — after a student is assigned to a lesson, if their Lesson Allocation is later archived by the Lesson Allocation soft-delete, the student must no longer appear in the lesson's student roster / attendance list, even though their Student Session record is not deleted.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- A lesson exists for Course Math 101 at Location Tokyo HQ on 2026-05-20.
- Student A has an active Lesson Allocation for Math 101 (Archived_At__c is blank) and has already been assigned to the lesson — an active Student Session exists, Is_Archived__c = FALSE.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the lesson on 2026-05-20 and views the Student Sessions / attendance list | Student A is listed | Student A Student Session Is_Archived__c = FALSE → shown |
| 2 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation record shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff reopens the same lesson's Student Sessions / attendance list | Student A no longer appears in the list | Student A Student Session Is_Archived__c = TRUE (via formula) → hidden |
| 4 | HQ or CM Staff opens Student A's Student Session record directly by its record Id | The Student Session record still exists with its original attendance/report data; it was not deleted | Record preserved for history/restore |
| 5 | HQ or CM Staff opens Student A's Lesson Allocation record while it is still archived | Lesson Allocated count and Report History retain the values they had before archiving — archive performs no DML on these fields, only on Archived_At__c | Fields unchanged by the archive write |
| 6 | A living Student Package Order reappears for the same Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 7 | HQ or CM Staff reopens the lesson's Student Sessions / attendance list | Student A reappears in the list — the same original Student Session, not a new one | Student A Student Session Is_Archived__c = FALSE (restored) → shown again |
| 8 | HQ or CM Staff opens Student A's Lesson Allocation record | Lesson Allocated count, Lesson Allocation Status, and Report History match the values from before the archive, with no duplicate entries or lost history | LA detail fields consistent across the archive → restore round trip |

**Severity:** critical
**Priority:** high

---
