# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 274 — "Collect Attendance"](https://app.qase.io/project/PX?suite=274) (8 existing cases). Earlier review of this suite found no new gap beyond what's already flagged as spec.md Gap #13 (the edit form's `upsertStudentSession` has no archive re-check, but the UI roster already hides archived sessions — same root cause as the picker/roster coverage in suites 219/1841). This case complements the restore round trip already tested on the Teacher/BO side (`teacher-report-attendance.md`, TC3) by confirming the same reversibility on the **SF** Edit Student Session form specifically, using the full attendance field set (Status, Reason, Notice, Note) this suite's own cases exercise.

## Suite: Collect Attendance

### Collect Attendance (SF) – Lesson Allocation Restored – Student Session Reappears and Attendance Fields Update Normally

**Description:** Feature Impact (Attendance, Lesson Report, Report Detail), control case — Decision Table — after a previously archived Lesson Allocation is restored (unarchived, same record Id), the student's Student Session reappears on the SF Lesson Detail page, and staff can edit the full attendance field set (Status, Reason, Notice, Note) normally, with the change syncing to BO as usual.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce (SF) with Collect Attendance access.
- A published lesson TC-ATTEND-SF exists with Student A assigned.
- Student A's Lesson Allocation was previously archived, then unarchived (same record Id) after a living Student Package Order reappeared for the same Student Course, so Student A's Student Session Is_Archived__c = FALSE again.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens the SF Lesson Detail page for TC-ATTEND-SF and views the Student Session section | Student A's row is visible again | Student A Is_Archived__c = FALSE (restored) → shown |
| 2 | HQ or CM Staff clicks Edit on Student A's Student Session row, sets Attendance Status = Absent, Reason = Traffic Issue, Notice = No Contact, Note = "Late bus", and submits | The form accepts the update; Student A's row shows Status = Absent, Reason = Traffic Issue, Notice = No Contact, Note = "Late bus" | Full attendance field set accepted |
| 3 | HQ or CM Staff logs in to BO, opens the same lesson's Collect Attendance view for Student A | BO shows the same Attendance Reason = Traffic Issue, consistent with SF | SF ↔ BO sync intact for a restored student too |

**Severity:** major
**Priority:** high

---
