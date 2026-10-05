# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source: this suite closes a self-review gap in the Calendar coverage — prior cases exercised archive-state exclusion and gap discovery, but under-tested the RESTORE path: whether displayed/calculated values on the Calendar recompute correctly after a Lesson Allocation is unarchived, and whether normal Calendar actions (assign, mark attendance, reschedule) keep working for a restored student without error or duplication. Grounded in AC-3 (same-Id rebuild), AC-4 (post-unarchive de-duplication: sessions restored by unarchive are walked by CreatedDate ASC; if another active allocation already holds the same (student, lesson) key, the restored session is detached, never deleted), and the confirmed-safe `LessonCalendarHandler` read path already verified in `lesson-calendar-display-archive.md`.

## Suite: Lesson Calendar – LA Restore – Functional Continuity & Recalculation

### Lesson Calendar – Student Count Badge – Recalculates Correctly After Lesson Allocation Restore

**Description:** AC-3 / AC-5 — State Transition — The "x/y" student-count badge on a Lesson Calendar card recalculates from 1 to 2 after a previously archived student's Lesson Allocation is restored (same Id), since the badge is computed live from `LessonCalendarHandler`'s archive-filtered `Student_Sessions__r` subquery on every page load.

**Preconditions:**
- Lesson L9 (capacity 5) is scheduled on 2026-05-26 at Location Tokyo HQ. Student A's Lesson Allocation LA-6 was archived on 2026-05-15 (Archived_At__c = 2026-05-15), hiding Student A's Student Session SS-2 from the count. Student B has an active Lesson Allocation and is also assigned to L9.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the Lesson Calendar for 2026-05-26 at Location Tokyo HQ and checks L9's student-count badge | The badge shows 1/5 (Student B only) | LA-6 Archived_At__c = 2026-05-15 |
| 2 | A living Student Package Order reappears for Student A's course group, triggering the sync to rebuild and unarchive LA-6 (same Id) | LA-6's Archived_At__c is cleared | LA-6 Id unchanged; Archived_At__c = null |
| 3 | HQ or CM Staff refreshes the Lesson Calendar for 2026-05-26 at Location Tokyo HQ | L9's student-count badge now shows 2/5 | Count recalculated live from Is_Archived__c = FALSE sessions |

**Severity:** major
**Priority:** high

---

### Assign Student Panel (Calendar) – Restored Lesson Allocation – Colliding Session Detached, Not Duplicated

**Description:** AC-4 — State Transition / Decision Table — When a student's restored Student Session collides on the same (student, lesson) key with a session already held by another active Lesson Allocation, the restored session is detached (not deleted, not left as a duplicate), consistent with the documented de-duplication rule, verified via the Calendar's lesson attendee view.

**Preconditions:**
- Student A's Lesson Allocation LA-1 was archived on 2026-05-10, hiding Student A's Student Session SS-1 (CreatedDate 2026-04-01) on Lesson L10.
- While LA-1 was archived, HQ or CM Staff used the Calendar's Assign Student panel to assign Student A to Lesson L10 again under a different, active Lesson Allocation LA-7, creating Student Session SS-7 (CreatedDate 2026-05-12).

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the Lesson Calendar for Lesson L10 | Student A appears once, via SS-7 (LA-7, active) | SS-7 Is_Archived__c = FALSE |
| 2 | A living Student Package Order reappears for Student A's original course group, triggering the sync to rebuild and unarchive LA-1 (same Id), restoring SS-1 | SS-1's Is_Archived__c formula flips to FALSE, but SS-1 collides with SS-7 on the (Student A, L10) key | SS-1 CreatedDate 2026-04-01 < SS-7 CreatedDate 2026-05-12 |
| 3 | HQ or CM Staff reopens the Lesson Calendar for Lesson L10 | Student A still appears exactly once, via SS-7; SS-1 is detached (Lesson__c = null, Assigned_Lesson__c = false) rather than shown as a duplicate attendee | SS-1 detached per AC-4; no duplicate row shown |

**Severity:** critical
**Priority:** high

---

### Lesson Calendar – Attendance Marking – Restored Student's Session Can Be Marked Normally

**Description:** AC-3 / AC-5 — State Transition — After a student's Lesson Allocation is restored, their original Student Session can be marked Present/Absent from the Calendar like any active session, with no residual block from the prior archive state.

**Preconditions:**
- Lesson L11 is scheduled on 2026-05-27 at Location Tokyo HQ. Student A's Lesson Allocation LA-8 was archived then restored (same Id) before the lesson date, so Student A's Student Session SS-3 is active again (Is_Archived__c = FALSE) with no prior attendance marked.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens Lesson L11 from the Calendar and opens Student A's attendance row | Student A's row is editable, same as any other active attendee | SS-3 Is_Archived__c = FALSE |
| 2 | HQ or CM Staff marks Student A as Present and saves | The attendance status is saved successfully on SS-3, with no error | Attendance_Status__c = Present on SS-3 (original session Id, not a new record) |

**Severity:** major
**Priority:** high

---

### Lesson Calendar – Drag-and-Drop Reschedule – Lesson with a Restored Student Moves Normally

**Description:** AC-5 — Regression — Rescheduling a lesson by dragging it to a new date/time on the Calendar completes normally when one of its attendees is a student whose Lesson Allocation was archived and later restored, since the clash-validation and Zoom-regeneration logic on reschedule does not depend on each attendee's archive history.

**Preconditions:**
- Lesson L12 is scheduled on 2026-05-28 at Location Tokyo HQ, Teaching Medium = Zoom. Student A's Lesson Allocation LA-9 was archived then restored (same Id) before this date, so Student A's Student Session SS-4 is active again and attached to L12.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff drags Lesson L12 on the Calendar from 2026-05-28 to 2026-05-29, same time slot | The lesson moves successfully with no clash error | new_date = 2026-05-29 |
| 2 | HQ or CM Staff opens L12's attendee list and Zoom link after the move | Student A (via SS-4) is still listed as an attendee, and the Zoom link is regenerated for the new date like any other lesson | SS-4 Id unchanged; Is_Archived__c = FALSE |

**Severity:** minor
**Priority:** medium

---
