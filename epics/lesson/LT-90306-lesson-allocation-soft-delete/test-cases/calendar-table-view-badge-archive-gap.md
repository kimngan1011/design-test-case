# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source: direct code audit (2026-10-02) of `lessonDetailCollapsible.js` (`packages/lesson/main/default/lwc/lessonDetailCollapsible/lessonDetailCollapsible.js:260-313`), embedded via `splitViewRightManaCalendarMultipleAssign.html` → `tableViewManaCalendar.html` on the Mana Calendar's table-view / Multiple-Assign surface. Its `Student_Sessions__r` related-list query (`getRelatedListRecords`, where clause `{ MANAERP__Is_Deleted__c: { eq: false } }`) filters only `Is_Deleted__c`, with no `Is_Archived__c` check — unlike the main calendar grid (`LessonCalendarHandler`, confirmed safe in the first audit pass). This component drives the Trial/New/Reallocate badges and attendee rows shown on this calendar surface.

## Suite: Calendar Table View (Multiple-Assign) – Archive Filter Gap

### Calendar Table View – Multiple-Assign – Archived Student Session Still Shown as Attendee Row

**Description:** Gap case — AC-5 — Decision Table — `lessonDetailCollapsible`'s Student Sessions related-list query filters `Is_Deleted__c = FALSE` only, so a student whose Lesson Allocation is archived still appears as an attendee row on the Mana Calendar's table-view (Multiple-Assign) surface, unlike the main calendar grid which correctly excludes them.

**Preconditions:**
- Lesson L6 is scheduled on 2026-05-23 at Location Tokyo HQ, with Student A (Lesson Allocation archived, Archived_At__c populated, session Is_Archived__c = TRUE) and Student B (active Lesson Allocation) both having Student Sessions.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the main Lesson Calendar grid for 2026-05-23 at Location Tokyo HQ and checks Lesson L6's attendee list | Student A is excluded; only Student B is shown | LessonCalendarHandler filters Is_Archived__c = FALSE |
| 2 | HQ or CM Staff switches to the Mana Calendar table view (Multiple-Assign) for the same lesson L6 | Student A still appears as an attendee row, inconsistent with step 1 | lessonDetailCollapsible's Student_Sessions__r query filters Is_Deleted__c = FALSE only, no Is_Archived__c check |

**Severity:** major
**Priority:** high

---

### Calendar Table View – Multiple-Assign – Trial/Reallocate Badge Computed from an Archived Student Session

**Description:** Gap case — AC-5 — Decision Table — Because `lessonDetailCollapsible` does not exclude archived Student Sessions, the Trial and Reallocate badges on the Mana Calendar table-view can be computed using a student whose underlying Lesson Allocation is archived.

**Preconditions:**
- Lesson L7 is scheduled on 2026-05-24 at Location Tokyo HQ. Student C has a Trial-flagged Student Session under Lesson Allocation LA-3, which has since been archived (Archived_At__c populated, session Is_Archived__c = TRUE).

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the Mana Calendar table view (Multiple-Assign) for Lesson L7 | Student C's row is still shown with the Trial badge, sourced from the archived session | LA-3 Archived_At__c = populated; isTrial computed from an Is_Archived__c = TRUE session |
| 2 | HQ or CM Staff compares this with the main Lesson Calendar grid for the same lesson | The main grid correctly omits Student C entirely | LessonCalendarHandler filters Is_Archived__c = FALSE |

**Severity:** minor
**Priority:** medium

---
