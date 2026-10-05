# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 2578 — "LOA (Leave of Absence)"](https://app.qase.io/project/PX?suite=2578) (8 existing cases, US09). Existing case 1826 ("Cancel LOA Resume – Resume LA Deleted") uses legacy hard-delete wording. Existing case 1825 ("LOA Resume – ... New LA Created from Resume Date") is likely stale even with archive enabled, since the sync service is confirmed to prefer restoring the same record over creating a new one. Per explicit instruction, existing cases are left untouched — this file adds new cases for the archive-enabled behavior.

Code trace: an LOA that fully removes the student's only order for a student-course satisfies `shouldArchiveAllocationOfStudentCourse`, archiving (not deleting) the LA. On Resume, `LessonAllocationSyncService`'s `shouldRestoreAllocationOfStudentCourse` → `collectAllocationsToUnarchive` → `buildUnarchivedAllocation` **reuses the archived allocation's own record Id** and clears `Archived_At__c` — it only falls back to creating a genuinely new `Lesson_Allocation__c` when no existing record is found at all for that student-course. Since the LOA's archived LA for that exact student-course already exists, Resume restores it rather than creating a new one — contradicting the existing case 1825's "New LA Created" wording. Cancelling a LOA Resume (case 1826) similarly re-archives the restored record rather than deleting it.

## Suite: LOA (Leave of Absence)

### LOA Resume – Previously Archived Lesson Allocation – Same Record Restored, Not a New LA Created

**Description:** Gap case — Decision Table, directly contrasts with the existing case (1825, "LOA Resume – Resume Date > Scheduled Resume Date – New LA Created from Resume Date") — when the LOA fully archived the student's Lesson Allocation (as opposed to only shortening its end date), submitting a Resume restores the SAME archived record (same record Id, Archived_At__c cleared) rather than creating a brand-new Lesson Allocation, since `LessonAllocationSyncService` always prefers unarchiving an existing record for that student-course over creating a new one.

**Preconditions:**
- Student A's Lesson Allocation for Course A was fully archived (Archived_At__c populated) by a completed LOA application (the LOA removed Student A's only order for this student-course). Note its record Id.
- `Enable_Lesson_Allocation_Archive__c` = TRUE.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the LOA Order, clicks "Create Resume", adds the Resume Product, saves draft, and submits (Resume Date > Scheduled Resume Date) | The resume is submitted successfully | Resume Date > Scheduled Resume Date |
| 2 | HQ or CM Staff opens Student A's Course A Lesson Allocation by its original (pre-LOA) record Id | The SAME record now shows Archived_At__c blank, with Start_Date_Time__c = the resume date — it was restored, not replaced | Archived_At__c = null (restored); record Id unchanged; Start_Date_Time__c = resume date |
| 3 | HQ or CM Staff navigates to Student A's Course tab / Lesson Allocation list | Only ONE Lesson Allocation for Course A is listed — the restored original, not a second newly-created record | Lesson Allocation count for Course A = 1 |

**Severity:** major
**Priority:** high

---

### Cancel LOA Resume – Resumed Lesson Allocation Archived Again, Not Deleted

**Description:** Gap/update case — Decision Table, contrasts with the legacy-wording baseline (case 1826, "Cancel LOA Resume – Resume LA Deleted") — cancelling a Resume (continuing from the scenario above) re-archives the Lesson Allocation rather than deleting it, since the underlying order that justified the resume is removed again, satisfying the same "all orders removed" archive condition.

**Preconditions:**
- Following directly from the case above: Student A's Lesson Allocation for Course A was restored via LOA Resume (Archived_At__c blank, same original record Id).
- `Enable_Lesson_Allocation_Archive__c` = TRUE.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the LOA application detail and clicks "Cancel LOA Resume" | The resume is cancelled | Resume status = Cancelled |
| 2 | HQ or CM Staff opens Student A's Course A Lesson Allocation by the same record Id | The record still exists and is reachable; Archived_At__c is populated again | Archived_At__c = current timestamp again; record NOT deleted |
| 3 | HQ or CM Staff navigates to Student A's Course tab / Lesson Allocation list | The Lesson Allocation no longer appears in the active list | Archived LA excluded from active-list queries |

**Severity:** minor
**Priority:** medium

---

### LOA – Partial (Last Attendance Day in the Future, Order Not Removed) – Lesson Allocation End Date Updated Only, Not Archived

**Description:** Regression / boundary case — Decision Table, contrasts with the existing baseline cases (1821/10195, "Last Attendance Day > Today" / "< Today — LA End Date Updated") — a partial LOA (Last Attendance Day leaves the order alive with valid Start/End dates, as opposed to removing it entirely) never archives the Lesson Allocation, since `shouldArchiveAllocationOfStudentCourse` only fires when every order for the student-course is removed. This locks in that the archive mechanism has no effect on the already-covered partial-LOA behavior, distinct from the full-archive LOA scenario covered in the cases above.

**Preconditions:**
- Student A has an active Lesson Allocation for Course A with a class assigned, lessons scheduled beyond today.
- `Enable_Lesson_Allocation_Archive__c` = TRUE.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff creates an LOA application with Last Attendance Day > today, adds the LOA Product, saves draft, and submits | The Lesson Allocation's end date updates to the Last Attendance Day; sessions beyond it are removed from future lessons | last_attendance_day > today |
| 2 | HQ or CM Staff opens Student A's Lesson Allocation | Archived_At__c remains blank — only End_Date_Time__c and Total_Session_Count__c were touched | Archived_At__c = null throughout |
| 3 | HQ or CM Staff navigates to Student A's Course tab / Lesson Allocation list | The Lesson Allocation still appears in the active list, unaffected by the archive mechanism | Is_Archived__c = FALSE (via formula) → unaffected |

**Severity:** minor
**Priority:** medium

---
