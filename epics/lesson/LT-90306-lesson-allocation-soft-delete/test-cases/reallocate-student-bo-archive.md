# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 1171 — "Reallocate student"](https://app.qase.io/project/PX?suite=1171) (11 existing cases, BO Collect Attendance's Reallocate flag/session lifecycle). None test an archived Lesson Allocation. This suite's Reallocate flag is set/cleared through the same Collect Attendance "Save" action already traced for suite 326, so the silent-drop bulk-save gap documented there (`collect-attendance-bo-archive.md`) applies equally to Reallocate flag changes — not repeated here. This file adds the two angles specific to the Reallocate session's own lifecycle.

Code trace: when a student is marked Absent + Reallocate, a second `Student_Sessions__c` row is created with `Session_Type__c = 'Reallocate'`, linked to the SAME `Lesson_Allocation__c` as the student's original (Standard-type) session, but pointing at a different `Lesson__c` (the "new"/reallocate lesson, once assigned). Since `Is_Archived__c` is a formula derived purely from the shared parent `Lesson_Allocation__c.Archived_At__c`, archiving that LA hides **both** sessions (the original Standard-type one in Lesson A, and the Reallocate-type one in Lesson B) simultaneously via the same formula — this has not been explicitly tested for the Reallocate-type session specifically in this suite.

## Suite: Reallocate student

### Reallocate Session on New Lesson – Lesson Allocation Archived – Hidden from New Lesson Alongside the Original Session; Restored – Both Reappear

**Description:** Regression / control case — Decision Table, contrasts with the baseline (case 10379, "Mark Absent with Reallocate Flag – Reallocate Session Created") — once the student's Lesson Allocation is archived, BOTH their original (now-inactive, Absent+Reallocate) session in Lesson A and their pending Reallocate-type session in the new Lesson B disappear simultaneously, since both share the same archived parent LA and the same `Is_Archived__c` formula.

**Preconditions:**
- Student A was marked Absent + Reallocate in original Lesson A — a Reallocate-type Student Session was created and later linked to new Lesson B (Student A currently appears in Lesson B's Student Sessions as the reallocated student).
- Student A has an active Lesson Allocation for this course.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Lesson B and confirms Student A appears in the Student Sessions as the reallocated student | Student A is listed | Reallocate-type session Is_Archived__c = FALSE → shown |
| 2 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff reopens Lesson B's Student Sessions | Student A no longer appears — the Reallocate-type session is hidden by the same formula as the original session | Reallocate-type session Is_Archived__c = TRUE (via formula, same parent LA) → hidden |
| 4 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 5 | HQ or CM Staff reopens Lesson B's Student Sessions | Student A reappears as the reallocated student — the same original Reallocate-type session, not newly created | Reallocate-type session Is_Archived__c = FALSE (restored) → shown again |

**Severity:** minor
**Priority:** medium

---

### Already-Reallocated Student – Archive/Restore Cycle – Original and New Lesson Both Display Correctly Throughout; Student Can Reallocate Again Afterward

**Description:** Regression / end-to-end case — Decision Table, broader than the case above — confirms that for a student who has already completed a full reallocation (Absent + Reallocate in original Lesson A, successfully reallocated to new Lesson B), the archive/restore cycle leaves BOTH lessons' displays accurate at every step (not just "hidden vs not hidden"), and — critically — that the student's ability to be reallocated again afterward is not broken by having gone through an archive/restore cycle.

**Preconditions:**
- Student A was marked Absent + Reallocate in original Lesson A and has been successfully reallocated to new Lesson B (Reallocate-type session active on Lesson B). Student A has an active Lesson Allocation.
- Student A also has a separate, unrelated future Lesson C they are normally assigned to (Standard-type session), to be used later in this test for a fresh reallocation.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens original Lesson A's Collect Attendance / Student Sessions and confirms Student A's status | Student A shows Attendance Status = Absent, Reallocate = On | Original session Is_Archived__c = FALSE |
| 2 | HQ or CM Staff opens new Lesson B's Student Sessions | Student A appears as the reallocated student, correctly linked to the original Lesson A absence | Reallocate-type session Is_Archived__c = FALSE |
| 3 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 4 | HQ or CM Staff reopens both Lesson A's and Lesson B's Student Sessions | Student A is absent from BOTH lessons' displays — neither shows stale, partial, or incorrect data; both are cleanly empty of Student A | Both sessions' Is_Archived__c = TRUE (via the same parent LA formula) → both hidden consistently |
| 5 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 6 | HQ or CM Staff reopens both Lesson A's and Lesson B's Student Sessions | Lesson A again shows Student A with Attendance Status = Absent, Reallocate = On (unchanged); Lesson B again shows Student A as the reallocated student on the same original session — both exactly as they were before archiving | Both sessions Is_Archived__c = FALSE (restored); no data loss or corruption on either side |
| 7 | HQ or CM Staff opens Student A's unrelated Lesson C, marks Student A Absent, and checks the Reallocate checkbox, then saves | The Reallocate flag is turned on for this new instance, and a new Reallocate-type Student Session is created for Student A, independent of the earlier Lesson A/B reallocation | New Reallocate-type session created successfully; reallocation mechanism fully functional after the archive/restore cycle, not left in a broken or stuck state |
| 8 | HQ or CM Staff assigns Student A's new reallocate session to a future Lesson D | Student A appears in Lesson D's Student Sessions as the reallocated student, exactly like a normal first-time reallocation | Second, independent reallocation completes normally |

**Severity:** major
**Priority:** high

---

### Unflag Reallocate via Collect Attendance – Original Session Archived Mid-Edit – Reallocate Session Cleanup Silently Skipped, Becomes Orphaned

**Description:** Gap case — Decision Table, contrasts with the baseline (case 9295, "Unflag Reallocate – Linked Draft Lesson – Reallocate Session Auto-Deleted") — this is the Reallocate-specific consequence of the Collect Attendance silent-drop gap already documented in `collect-attendance-bo-archive.md`: if a teacher opens Collect Attendance for the original lesson, changes Student A's status from Absent to Attend (intending to unflag Reallocate and trigger auto-deletion of the linked Reallocate session) while Student A's Lesson Allocation is archived in the background before Save, the whole update — including the Reallocate-session cleanup — is silently dropped. The Reallocate session is left pointing at the new lesson indefinitely, orphaned, with no error ever surfaced.

**Preconditions:**
- Student A has Reallocate = On in original Lesson A (Absent status), with a linked Reallocate session on new Lesson B. HQ or CM Staff has Lesson A's Collect Attendance dialog open for Student A.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff changes Student A's status from Absent to Attend in the open dialog, but does not yet click Save | Form shows the new status, unsaved | Dialog still open |
| 2 | In a separate session, the Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff (on the original, stale dialog) clicks "Save" | A success toast is shown, with no indication that the update was dropped | bulkUpdateStudentSessionAttendance's re-query excludes Student A's now-archived session; no DML, no Reallocate-session cleanup triggered |
| 4 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id, and HQ or CM Staff reopens Lesson A's Collect Attendance | Student A's status still shows Absent + Reallocate = On, unchanged from before step 1 — the intended unflag never applied | Student session data unchanged, since the update in step 3 never reached any DML |
| 5 | HQ or CM Staff opens Lesson B's Student Sessions | Student A's Reallocate session is still present on Lesson B — it was never auto-deleted, remaining orphaned from the original intent to unflag it in step 1 | Reallocate session not cleaned up; requires staff to notice and manually repeat the unflag action post-restore |

**Severity:** minor
**Priority:** low

---
