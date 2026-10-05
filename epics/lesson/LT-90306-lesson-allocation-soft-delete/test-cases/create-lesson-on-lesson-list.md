# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 218 — "Create Lesson on Lesson list"](https://app.qase.io/project/PX?suite=218) (32 existing cases). Only the gap introduced by the Lesson Allocation archive refactor is covered here — the 32 existing cases (recurring patterns, closed dates, lesson count boundaries, timezone, UI/localization, bulk migration, location filter) are unrelated to `Archived_At__c`/`Is_Archived__c` and are left unchanged.

## Suite: Create Lesson on Lesson list

### Create Lesson – One-time – Group – Class Member Archived – Student Not Auto-Assigned

**Description:** Feature Impact (Class Assignment / Master Queue) — Decision Table — Creating a one-time Group lesson for a Class must not auto-assign a Student Session to a student whose Class Member has been archived by the Lesson Allocation soft-delete.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- Class A exists, linked to Course Math 101 and Location Tokyo HQ.
- Student A has a Class Member record on Class A whose Lesson Allocation has been archived (Archived_At__c is populated) after its Student Package Order was fully removed, so Class Member Is_Archived__c = TRUE.
- Student B has a Class Member record on Class A with an active Lesson Allocation (Archived_At__c is blank), so Class Member Is_Archived__c = FALSE.
- No lesson exists for Class A on 2026-05-20.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff creates a new one-time Group lesson for Class A on 2026-05-20 | The lesson is created with Draft status | class = Class A; lesson_date = 2026-05-20 |
| 2 | The system completes the Class Member auto-assignment job for the new lesson | The job completes with no error | "" |
| 3 | HQ or CM Staff opens the new lesson's Student Sessions related list and looks for Student B | Student B's Student Session is listed, auto-assigned by the job | Student B Class Member Is_Archived__c = FALSE → included |
| 4 | HQ or CM Staff looks for Student A in the same related list | Student A's Student Session is absent; Student A was not auto-assigned | Student A Class Member Is_Archived__c = TRUE → excluded |

**Severity:** critical
**Priority:** high

---

### Create Lesson – One-time – Group – Lesson Allocation Unarchived – Student Auto-Assigned After Restore

**Description:** Feature Impact (Class Assignment / Master Queue) — Decision Table — After a previously archived Lesson Allocation is unarchived (its Class Member returns to Is_Archived = FALSE on the same record), a new Group lesson created for the same Class must auto-assign that student, proving the archive filter does not permanently block a restored student.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- Class A exists, linked to Course Math 101 and Location Tokyo HQ.
- Student A previously had its Class Member on Class A archived, then unarchived after a living Student Package Order reappeared for the same Student Course, so the same Class Member record now has Is_Archived__c = FALSE.
- No lesson exists for Class A on 2026-05-21.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff creates a new one-time Group lesson for Class A on 2026-05-21 | The lesson is created with Draft status | class = Class A; lesson_date = 2026-05-21 |
| 2 | The system completes the Class Member auto-assignment job for the new lesson | The job completes with no error | "" |
| 3 | HQ or CM Staff opens the new lesson's Student Sessions related list and looks for Student A | Student A's Student Session is listed, auto-assigned by the job | Student A Class Member Is_Archived__c = FALSE (restored) → included |
| 4 | HQ or CM Staff opens Student A's Lesson Allocation record | Exactly one Lesson Allocation record exists for Student A on this Student Course, with the same record Id as before the archive | One record, same Id across archive → unarchive |

**Severity:** major
**Priority:** high

---
