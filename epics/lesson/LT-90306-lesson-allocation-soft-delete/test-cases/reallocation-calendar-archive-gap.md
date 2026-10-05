# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source: direct code audit (2026-10-02) of `ReallocationHandler.cls` — `buildReallocationListWithFilterQuery` / `getReallocationListWithFilterLWC` / `getReallocationListWithFilter`, which back the `listReallocationCalendar` LWC (the Reallocation Calendar view). Unlike every other calendar-family read path in this audit, this query has **no** `Is_Archived__c`, `Archived_At__c`, or `Is_Deleted__c` condition anywhere in its WHERE clause — a complete gap, not a partial one. The Reallocation Calendar is explicitly named in the spec's AC-5 scope ("reallocation list"), so this is a direct AC-5 violation, distinct from `reallocate-to-new-lesson.md`'s coverage of the request-creation path (`createReallocationByStudentSessionId`), which is already correctly filtered.

## Suite: Reallocation Calendar – Archive Filter Gap

### Reallocation Calendar – List View – Request Tied to Archived Lesson Allocation Still Shown

**Description:** Gap case — AC-5 — Decision Table — The Reallocation Calendar list shows a reallocation request whose originating Student Session/Lesson Allocation has been archived, since `ReallocationHandler`'s list query has no archive or deleted filter at all.

**Preconditions:**
- An Open reallocation request R1 exists, sourced from Student A's Student Session SS-1 under Lesson Allocation LA-1, for Location Tokyo HQ in the date range 2026-05-18 to 2026-05-22.
- LA-1 has since been archived (Archived_At__c populated), so SS-1's Is_Archived__c = TRUE, while R1 itself is left untouched by the archive (no DML on Reallocation__c during archive).

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the Reallocation Calendar for Location Tokyo HQ and sets the date range to 2026-05-18–2026-05-22 | Reallocation request R1 is still listed, with its originating session SS-1 showing as archived elsewhere in the system | LA-1 Archived_At__c = populated; reallocation list query has no Is_Archived__c/Archived_At__c/Is_Deleted__c filter |
| 2 | HQ or CM Staff compares this list against the Lesson Calendar for the same Location and date range | The Lesson Calendar correctly excludes Student A's archived session from its own attendee lists, while the Reallocation Calendar still surfaces R1 — an inconsistency between the two calendar surfaces | Lesson Calendar (LessonCalendarHandler) filters Is_Archived__c = FALSE; Reallocation Calendar does not |

**Severity:** major
**Priority:** high

---

### Reallocation Calendar – Action Attempt – Archived-Session Reallocation Request Can Still Be Opened

**Description:** Gap case — AC-5 — Negative Testing — Because the Reallocation Calendar list has no archive filter, staff can open and act on a reallocation request whose source session belongs to an archived Lesson Allocation, even though the underlying session is no longer active.

**Preconditions:**
- An Open reallocation request R2 exists, sourced from Student B's Student Session SS-2 under Lesson Allocation LA-2, for Location Tokyo HQ.
- LA-2 has since been archived (Archived_At__c populated), so SS-2's Is_Archived__c = TRUE.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff opens the Reallocation Calendar for Location Tokyo HQ and locates request R2 | R2 is listed and selectable, with no visual indicator that its source session is archived | LA-2 Archived_At__c = populated |
| 2 | HQ or CM Staff opens R2 and attempts to approve/complete the reallocation to a new session | The system's behavior for completing a reallocation against an archived-session source is undefined by current code — this action path is not blocked by any archive check at the list or detail level | No Is_Archived__c check found in ReallocationHandler's list or filter query |

**Severity:** major
**Priority:** high

---
