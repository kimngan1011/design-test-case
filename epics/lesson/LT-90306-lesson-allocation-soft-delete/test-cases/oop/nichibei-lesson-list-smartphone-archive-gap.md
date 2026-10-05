# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 2783 — "[Nichibei] Lesson List in BO (Smartphone view)"](https://app.qase.io/project/PX?suite=2783) (18 existing cases, Jira LT-96616, OOP FEATURES → Nichibei, parent 371). Reviewed as part of a proactive sweep of Nichibei's remaining table/list-view suites, prompted by the fact that Nichibei relies heavily on `outside-packages/` custom code not shared with Core (already proven true for the Point Consumption priority chain and the Reallocate Lesson picker, both found to lack the archive filter). None of the 18 existing cases reference `Archived_At__c`/`Is_Archived__c`.

**Code-trace confirmation — already safe, not a gap.** The "Smartphone view" is not separate Nichibei-only code: it's the same `WrapperTableLessonSF` component rendered at a mobile breakpoint (`school-portal-admin/.../WrapperTableLessonSF.tsx:404`), wiring the identical `DialogsCollectAttendance` dialog already assessed for the desktop entry points. Its roster query, `Lesson_GetStudentSessionAttendance` (`lesson-student-session.query.graphql:113-121`), already filters `Is_Archived__c: { eq: false }` (line 119). The "Attendance Remark"/"Booking Note" feature (cases 21098-21100) has no separate query either — both the Nichibei-booking write path (`BookingLessonHandlerOutSide.cls:667,716`) and the Mobile-submission write path (`LessonSubmitAttendanceEventHandler.cls:32-37,51-55`) write to the same already-filtered `Student_Sessions__c.Attendance_Response__c` field the roster reads. The Lesson Status filter (Published/Draft/Completed/Cancelled) is a clean, separate concern operating only on `Lesson__c.Status__c`, with no interaction with student/LA archive state.

## Suite: [Nichibei] Lesson List in BO (Smartphone view)

### [Nichibei] Smartphone Lesson List – Collect Attendance Roster – Archived Student Excluded, Including Booking Remark (Control Case)

**Description:** AC-5 (parity) — Regression — control case, not a gap. Contrasts with existing baseline (#21094 "Collect Attendance – Published Lesson – Entry point opens Collect Attendance page", #21098 "Attendance Remark – Student Booked with Remark – 'Booking Note:' prefix shown"). Code-confirmed: this Smartphone-view roster shares the exact same `Is_Archived__c`-filtered query and dialog as the already-covered desktop Collect Attendance entry points — locks in that it is unaffected by this epic, including for a student whose booking remark was written via Nichibei's Lesson Booking flow.

**Preconditions:**
- Logged into BO as a Nichibei staff user on the Smartphone view.
- Published Lesson X has Student A (booked via Nichibei Lesson Booking, remark = "Please arrange front row seat", stored with "Booking Note:" prefix) and Student B (active, no remark) both assigned.
- Status filter = "Published" (default).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Staff taps into Lesson X's Collect Attendance entry point from the Smartphone Lesson List | Both Student A (with "Booking Note: Please arrange front row seat" shown read-only) and Student B appear in the roster | Both sessions Is_Archived__c = FALSE |
| 2 | The Student Package Order group behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | Student A's Student Session becomes Is_Archived__c = TRUE via formula | Archived_At__c = current timestamp |
| 3 | Staff reopens Lesson X's Collect Attendance entry point from the Smartphone Lesson List | Student A no longer appears in the roster at all — neither their attendance row nor their booking remark leaks through; Student B is unaffected | Student A excluded by Lesson_GetStudentSessionAttendance's Is_Archived__c = FALSE filter |
| 4 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id | Student A's Student Session returns to Is_Archived__c = FALSE | Archived_At__c = null (restored) |
| 5 | Staff reopens the Collect Attendance entry point | Student A reappears in the roster with their original booking remark intact ("Booking Note: Please arrange front row seat") | Same Student_Sessions__c record, Attendance_Response__c unchanged by the archive/restore cycle |

**Severity:** minor
**Priority:** medium

---
