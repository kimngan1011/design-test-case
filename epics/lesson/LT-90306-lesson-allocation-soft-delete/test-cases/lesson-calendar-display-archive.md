# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Feature: Lesson Calendar read-path archive exclusion (`LessonCalendarHandler.cls` → `calendar`/`calendarV2`/`individualCalendar` LWCs via `LessonCalendarRestAPIHandler.cls`; `LessonHandler.getLessonAttendeeStatuses`; `AvailableTeacherHandler.getStudentLessonsForMonth`/`getStudentAssignmentInfo`). Source-code audit (2026-10-02) confirmed every `Student_Sessions__r` subquery in this path already filters `Is_Archived__c = FALSE` (and direct `Lesson_Allocation__c` queries filter `Archived_At__c = NULL`), and `school-portal-admin`'s calendar hooks (`useGetLessonsOnCalendarSF.ts`, `useGetLessonDetailSF.ts`) do no client-side filtering of their own — they inherit safety entirely from these Apex endpoints. No existing Qase suite/local test case exercises this exclusion on the core Calendar grid/detail/attendee-badge/teacher-overlay surfaces specifically (the only prior calendar-archive coverage is `bulk-publish-lesson-calendar-with-student.md`, which is about the bulk-publish action, not calendar display). These cases lock in the confirmed-safe behavior as regression coverage for the AC-5 "Lesson calendar" scope row.

## Suite: Lesson Calendar – Archived Record Exclusion

### Lesson Calendar – Monthly Grid – Student with Archived Lesson Allocation – Not Shown as Lesson Attendee

**Description:** AC-5 — Decision Table — A student whose Lesson Allocation has been archived is excluded from the attendee list of lessons shown on the Lesson Calendar grid, since `LessonCalendarHandler`'s `Student_Sessions__r` subquery filters `Is_Archived__c = FALSE`.

**Preconditions:**
- Lesson L1 is scheduled on 2026-05-18 at Location Tokyo HQ, with Student A and Student B both assigned via Student Sessions.
- Student A's Lesson Allocation has since been archived (Archived_At__c is populated, session Is_Archived__c = TRUE).
- Student B's Lesson Allocation remains active (Archived_At__c is blank, session Is_Archived__c = FALSE).

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the Lesson Calendar and navigates to 2026-05-18 at Location Tokyo HQ | Lesson L1 is shown on the calendar grid | calendar_date = 2026-05-18 |
| 2 | HQ or CM Staff opens Lesson L1's card/detail from the calendar | The attendee list shows Student B only | Student A Is_Archived__c = TRUE → excluded; Student B Is_Archived__c = FALSE → included |

**Severity:** major
**Priority:** high

---

### Lesson Calendar – Lesson Detail Drawer – Attendance Status Badge – Archived Student Excluded from Count

**Description:** AC-5 — Boundary / Decision Table — The attendance-status badges (absent/trial/reallocated counts) shown on a Calendar lesson card exclude a student whose Lesson Allocation is archived, since `LessonHandler.getLessonAttendeeStatuses` filters `Is_Archived__c = FALSE`.

**Preconditions:**
- Lesson L2 is scheduled on 2026-05-19 at Location Tokyo HQ with 3 Student Sessions: Student A (active, marked Absent), Student B (active, Trial), Student C (Lesson Allocation archived, Archived_At__c populated).

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the Lesson Calendar for 2026-05-19 at Location Tokyo HQ | Lesson L2 is shown with attendance badges | calendar_date = 2026-05-19 |
| 2 | HQ or CM Staff inspects the Absent/Trial count badges on Lesson L2's card | Absent count = 1 (Student A), Trial count = 1 (Student B); Student C is not counted in any badge | Student C Is_Archived__c = TRUE → excluded from getLessonAttendeeStatuses |

**Severity:** minor
**Priority:** medium

---

### Available Teacher Calendar – Month Overlay – Student with Archived Lesson Allocation – Lesson Not Shown

**Description:** AC-5 — Decision Table — A student's lesson is excluded from the Available-Teacher Calendar's student-month overlay when the student's Lesson Allocation is archived, since `AvailableTeacherHandler.getStudentLessonsForMonth` filters `Is_Archived__c = FALSE`.

**Preconditions:**
- Student A has Lesson L3 on 2026-05-20 at Location Tokyo HQ, assigned via a Student Session whose Lesson Allocation has since been archived (Archived_At__c populated).
- Student A has a second Lesson L4 on 2026-05-21 with an active Lesson Allocation (Archived_At__c blank).

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the Available Teacher Calendar, selects Student A, and views May 2026 | The month overlay shows Lesson L4 only on 2026-05-21 | month = 2026-05 |
| 2 | HQ or CM Staff inspects 2026-05-20 on the overlay | No lesson is shown for Student A on this date | Student A's L3 session Is_Archived__c = TRUE → excluded |

**Severity:** minor
**Priority:** medium

---

### Lesson Calendar – Unarchive Round Trip – Same Lesson Allocation Restored – Student Reappears Without Duplicate Session

**Description:** AC-3 / AC-5 — State Transition — After a student's archived Lesson Allocation is restored (same Id, Archived_At__c cleared), the student reappears as an attendee on the Lesson Calendar using the original Student Session, with no duplicate session created.

**Preconditions:**
- Lesson L5 is scheduled on 2026-05-22 at Location Tokyo HQ. Student A's Lesson Allocation LA-1 was archived on 2026-05-10 (Archived_At__c = 2026-05-10), hiding Student A's existing Student Session SS-1 from the calendar.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the Lesson Calendar for 2026-05-22 at Location Tokyo HQ | Lesson L5's attendee list does not include Student A | LA-1 Archived_At__c = 2026-05-10 |
| 2 | A living Student Package Order reappears for Student A's course group, triggering the sync to rebuild and unarchive LA-1 (same Id) | LA-1's Archived_At__c is cleared | LA-1 Id unchanged; Archived_At__c = null |
| 3 | HQ or CM Staff reopens the Lesson Calendar for 2026-05-22 at Location Tokyo HQ | Lesson L5's attendee list now includes Student A again, using the original Student Session SS-1 | SS-1 Id unchanged, Is_Archived__c = FALSE; no duplicate session created |

**Severity:** major
**Priority:** high

---
