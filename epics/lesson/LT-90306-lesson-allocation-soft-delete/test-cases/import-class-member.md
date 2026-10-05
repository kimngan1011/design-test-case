# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 1292 — "Import Class Member"](https://app.qase.io/project/PX?suite=1292) (3 existing cases: "New Class Assignment", "Change Existing Class", "Invalid CSV Data"). None test a CSV row that references an archived Lesson Allocation.

Code trace: `ClassMemberTrigger` fires `before insert`/`after insert` on **every** `Class_Member__c` insert regardless of origin (CSV import, Data Loader, LA Detail "Assign Class" button, Location Course "Active Student" assign flow). `before insert` calls `LessonClassMemberHandler.beforeInsert` → `validateClassMember` → the inner `ClassMemberValidator` class. Its `retrieveData` method builds `lessonAllocationMap` with `WHERE Id IN :lessonAllocationIds AND Archived_At__c = NULL` — an archived LA is never in this map. Then `validateClassMember(Class_Member__c)` does:
```
if (this.lessonAllocationMap.containsKey(classMember.Lesson_Allocation__c) == false) {
    return;
}
```
This is a **silent early return** — when the row's Lesson Allocation is archived, **all validation is skipped** (no "Effective Start Date must be today or later", no "cannot be before/after Student Course Start/End Date", no "Class not belong to Location Course" check), and the insert proceeds with no error of any kind. `after insert` then calls `onAfterInsertClsMembers` → `createAssignClassMemberJobs`, which enqueues `AssignClassMemberBatchable`. That batchable's own `doStart` query filters `WHERE Id IN :lessonAllocationIds AND Archived_At__c = NULL`, so the archived LA is excluded there too — no Student Sessions are ever created/synced for the new Class Member. The net effect: a CSV row for an archived LA imports as "successful" (no row-level error reported) but produces a Class Member that is immediately hidden (`Is_Archived__c` formula) and never synced to BO — the same silent-gap pattern already found on the LA Detail page's "Assign Class" button (suite 1293).

## Suite: Import Class Member

### Import Class Member – CSV Row References Archived Lesson Allocation – Row Imports as Successful with Validation Skipped, Class Member Never Synced to BO

**Description:** Feature Impact (Class Assignment / Master Queue), negative/gap case — Decision Table — contrasts with the existing "Invalid CSV Data" baseline (case 10555, which expects row-level error messages for non-existent IDs or missing fields): a CSV row pointing at a valid but **archived** Lesson Allocation is not treated as invalid at all. `ClassMemberValidator` silently skips all its checks for a row whose Lesson Allocation is archived (it is absent from the validator's lookup map), so even a row with an out-of-range Effective Start Date would pass silently in this state. The import reports success, but the resulting Class Member is immediately hidden by the `Is_Archived__c` formula and is excluded from `AssignClassMemberBatchable`'s sync, so it never reaches BO.

**Preconditions:**
- Student A's Lesson Allocation for Math 101 has been archived (Archived_At__c populated) after its Student Package Order was fully removed.
- Class A exists for Math 101 at Location Tokyo HQ. A CSV file is prepared with one row: Student A's archived Lesson Allocation Id, Class A, Effective Start Date = today.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff uploads the CSV via the Import Class Member flow | The import completes with no row-level error for Student A's row — unlike the "Invalid CSV Data" baseline (case 10555), an archived-LA row is not flagged as invalid | CSV row: Lesson Allocation Id = Student A's archived LA, Class = Class A, Effective Start Date = today |
| 2 | HQ or CM Staff opens the created Class Member record directly by record Id | The Class Member record exists, tied to the archived Lesson Allocation, with no validation error ever raised against it | ClassMemberValidator.retrieveData's lessonAllocationMap excludes archived LAs (`Archived_At__c = NULL` filter) → validateClassMember's containsKey check is false → all checks silently skipped |
| 3 | HQ or CM Staff opens Student A's Student Detail → Courses tab on BO | Class A does NOT appear as Student A's class on BO | Student A's Class Member Is_Archived__c = TRUE (via formula) immediately after creation |
| 4 | HQ or CM Staff checks whether any Student Session was created for Student A on Class A's lessons | No Student Session is created for Student A on any Class A lesson | AssignClassMemberBatchable.doStart excludes the archived LA (`Archived_At__c = NULL` filter) → the sync job never processes this Class Member |

**Severity:** major
**Priority:** medium

---

### Import Class Member – Student Auto-Assigned via CSV Import – Lesson Allocation Archived – Hidden from Lesson; Restored – Shown Again

**Description:** Feature Impact (Class Assignment / Master Queue) — Decision Table — a student successfully auto-assigned to a Class's lessons via the "Import Class Member" CSV flow (case 10532 baseline, LA active at import time) disappears from that Class's lesson Student Sessions once their Lesson Allocation is later archived, and reappears on the same record once the Lesson Allocation is restored — same pattern already locked in for the Location Course "Active Student" assign flow (suite 1291, case "Location Course – Class Assigned to Student"), now confirmed for the CSV import path too, since both paths share the same `ClassMemberTrigger` → `AssignClassMemberBatchable` sync mechanism.

**Preconditions:**
- Student A has an active Lesson Allocation for Math 101 at Location Tokyo HQ (Archived_At__c blank).
- HQ or CM Staff has imported a CSV assigning Class A to Student A (Effective Start Date = today) via the Import Class Member flow; the Class Member record was created successfully, and a lesson for Class A exists today — Student A currently appears in that lesson's Student Sessions.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the Class A lesson's Student Sessions section | Student A is listed as an active student | Student A Is_Archived__c = FALSE → shown |
| 2 | The Student Package Order behind Student A's Math 101 Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated; Student A's imported Class Member flips to archived via the same formula | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff reopens the Class A lesson's Student Sessions section | Student A no longer appears in the list | Student A Is_Archived__c = TRUE (via formula) → hidden |
| 4 | A living Student Package Order reappears for Student A's Math 101 Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 5 | HQ or CM Staff reopens the Class A lesson's Student Sessions section | Student A reappears in the list — the same original Student Session and Class Member created by the CSV import, not newly created | Student A Is_Archived__c = FALSE (restored) → shown again |

**Severity:** major
**Priority:** high

---
