# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source: direct code audit (2026-10-02) of `LessonScheduleHandler.getLessonSchedulesFromLessonMaster` (`packages/lesson/main/default/classes/LessonScheduleHandler.cls:1235-1371`), which backs the Lesson Master weekly-grid card (`school-portal-admin`: `LessonScheduleItem.tsx` / `LessonScheduleGroupItem.tsx` / `LessonScheduleIndividualItem.tsx`, rendered in `CalendarV2/Calendar/.../WeeklyTimeView`). Its `Lesson_Schedule_Student__r` subquery (lines 1356-1371) has **no WHERE clause at all** filtering `Is_Archived__c`/`Archived_At__c` on the allocation or the junction record — unlike the main lesson occurrence card (`LessonItem.tsx`), whose "x/y" student-count badge and attendee rows are safely inherited from the already-filtered `LessonCalendarHandler` payload (confirmed in prior audit passes). The relevant junction here is `Lesson_Schedule_Student__c`, a distinct object from the `Class_Member__c`/`Student_Sessions__c` gaps already found elsewhere — same root cause (soft-delete not honored), different query.

## Suite: Lesson Master Calendar – Weekly Card – Archive Filter Gap

### Lesson Master Calendar – Weekly Card – Student Count Badge – Archived Allocation Still Counted

**Description:** Gap case — AC-5 — Decision Table — The "x/y" student-count badge on a Lesson Master weekly card includes a student whose Lesson Allocation has been archived, because `LessonScheduleHandler.getLessonSchedulesFromLessonMaster`'s `Lesson_Schedule_Student__r` subquery has no archive or deleted filter at all.

**Preconditions:**
- Lesson Schedule LS-1 (capacity 5) has 3 Lesson Schedule Students: Student A, Student B (both active Lesson Allocations), and Student C (Lesson Allocation archived, Archived_At__c populated).

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the Lesson Master weekly calendar and locates LS-1's card | The card shows a student-count badge of 3/5, including archived Student C | capacity = 5; raw Lesson_Schedule_Student__r count = 3 |
| 2 | HQ or CM Staff opens the same lesson's occurrence card on the main Lesson Calendar grid | The main grid's student-count badge shows 2/5, correctly excluding Student C | LessonCalendarHandler filters Is_Archived__c = FALSE -> count = 2 |
| 3 | HQ or CM Staff compares the two badges from steps 1 and 2 | The Lesson Master card (3/5) and the main Calendar card (2/5) disagree for the same lesson, because only the main grid's query excludes the archived allocation | Lesson_Schedule_Student__r subquery has no Is_Archived__c/Archived_At__c filter |

**Severity:** major
**Priority:** high

---

### Lesson Master Calendar – Weekly Card – Student List – Archived Allocation Student Still Named

**Description:** Gap case — AC-5 — Decision Table — Expanding a Lesson Master weekly card's student list shows the name of a student whose Lesson Allocation has been archived, since the underlying query that feeds `LessonScheduleIndividualItem` has no archive filter.

**Preconditions:**
- Lesson Schedule LS-2 has 2 Lesson Schedule Students: Student D (active Lesson Allocation) and Student E (Lesson Allocation archived, Archived_At__c populated).

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the Lesson Master weekly calendar, locates LS-2's card, and expands the student list | Both Student D and Student E are listed by name, grade, and course | Student E Is_Archived__c = TRUE (via parent allocation) but still listed |
| 2 | HQ or CM Staff opens the same lesson's attendee list on the main Lesson Calendar grid | Only Student D is listed | LessonCalendarHandler filters Is_Archived__c = FALSE |

**Severity:** minor
**Priority:** medium

---
