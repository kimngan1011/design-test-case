# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 2684 — "Collect Attendance"](https://app.qase.io/project/PX?suite=2684) (7 existing cases, Jira LT-96152, under parent 292). This suite covers two NEW entry points — Lesson Detail → Report tab, and Lesson Report Detail page — for the SAME "Collect Attendance" popup already fully traced in suite 326 (`collect-attendance-bo-archive.md`). Every existing case explicitly confirms this ("the existing Collect Attendance popup opens", "uses the same persistence and sync flow as the current collect-attendance path") — same `bulkUpdateStudentSessionAttendance` backend, same student list queries. None of the 7 cases test an archived Lesson Allocation.

Code trace: since both new entry points render the same popup/dialog component already confirmed to read via `Is_Archived__c = false`-filtered queries and write via the already-documented silent-drop-prone `bulkUpdateStudentSessionAttendance`, no new backend investigation was needed — this file locks in that the already-known behavior (and the already-known gap) hold consistently across both new surfaces, not just the original Student tab entry point.

## Suite: Collect Attendance

### Lesson Report Detail – Archived Student – No Collect Attendance Entry Point Available

**Description:** Regression / control case — Decision Table, contrasts with the baseline (case 19738, "Lesson Report BO – Lesson Report Detail – Published lesson – Collect Attendance popup opens") — a student whose Lesson Allocation is archived has no "Collect Attendance" button to click from the Lesson Report Detail page at all, since the page itself never lists that student (same exclusion mechanism already confirmed for suite 426/1748's SRD list). Restoring the Lesson Allocation makes the student (and their Collect Attendance entry point) reappear.

**Preconditions:**
- Student A has an active Lesson Allocation and currently appears on a Published lesson's Lesson Report Detail page with a visible, enabled "Collect Attendance" button.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Student A's Lesson Report Detail page and confirms the "Collect Attendance" button is visible and enabled | Button visible, enabled | Student A Is_Archived__c = FALSE |
| 2 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff reopens this lesson's Report tab / Lesson Report Detail | Student A no longer appears anywhere on the page — there is no "Collect Attendance" entry point to click for them | Student A Is_Archived__c = TRUE (via formula) → excluded from the underlying student list query |
| 4 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 5 | HQ or CM Staff reopens Student A's Lesson Report Detail page | Student A reappears with the "Collect Attendance" button visible and enabled again, same as before archiving | Student A Is_Archived__c = FALSE (restored) |

**Severity:** minor
**Priority:** medium

---

### Lesson Detail Report Tab – Bulk Collect Attendance – Same Silent-Drop Gap Applies When Reached via This New Entry Point

**Description:** Gap case — Decision Table, contrasts with the baseline (case 19741, "Lesson BO – Report Tab – Absent attendance saved – Student session and mobile updated") — this is the same silent-drop-on-archive gap already documented for the Student tab's Collect Attendance dialog (`collect-attendance-bo-archive.md`, suite 326), now confirmed reachable identically via the new Report tab entry point: if a teacher opens Collect Attendance from the Report tab with multiple students loaded, and one student's Lesson Allocation is archived in the background before Save, that student's update is silently dropped while a success toast is still shown for the whole batch.

**Preconditions:**
- HQ or CM Staff has opened Collect Attendance from a Published lesson's Report tab, with Student A and Student B both loaded.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff sets Student A's status = Absent and Student B's status = Attend, but does not yet click Save | Both students' form fields show the selected values, unsaved | Dialog still open |
| 2 | In a separate session, the Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | HQ or CM Staff (on the stale Report tab dialog) clicks "Save" | A success toast is shown for the whole batch, with no indication Student A's update was dropped | Same bulkUpdateStudentSessionAttendance backend as the Student tab entry point, already confirmed to silently skip archived sessions |
| 4 | HQ or CM Staff refreshes and checks both students | Student B's Attend status is saved correctly; Student A no longer appears at all, and their Absent update was never applied | Student A Is_Archived__c = TRUE; Student B unaffected |

**Severity:** major
**Priority:** medium

---
