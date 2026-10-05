# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 1493 — "Edit lesson info in lesson detail on SF"](https://app.qase.io/project/PX?suite=1493) (3 existing cases, under parent 1492), covering the general "Edit lesson date/time/info" flow shared by one-time and recurring lessons (daily/weekly/custom — suites 1494/1495/1496, already reviewed and confirmed out of scope since their date-shift cascade never touches `Student_Sessions__c`/`Lesson_Allocation__c`). This file documents a DIFFERENT, Zoom-specific sub-path reached by the SAME "Edit lesson date/time" action, raised by the reviewer's question: when editing a lesson's date/time, does the system regenerate the Zoom link for a student whose Lesson Allocation is already archived?

Code trace: `UpdateLessonHandler.updateSingleLesson` calls `LessonZoomHandler.calcRenewLessonZoomLinks(params, toBeUpdatedLessons)` (`LessonZoomHandler.cls:600-655`) whenever `isDateTimeChanged` is true (`UpdateLessonHandler.cls:65-76`), regardless of "only this" or "Apply this and the following". The participant data this reads comes from `LessonZoomLinkDataMapper.retrieveZoomParticipantData()` (`LessonZoomHandler.cls:513-545`), whose SOQL is `SELECT ... FROM Zoom_Participant__c WHERE Lesson__c IN :lessonIds` — **no `Is_Archived__c`, `Archived_At__c`, or `Is_Deleted__c` predicate anywhere**. Behavior then splits by Zoom type:
- **Multiple Zoom** (one `Zoom_Participant__c` row per student): the loop at `LessonZoomHandler.cls:657-718` iterates every `Lesson_Allocation__c` key found in the unfiltered participant map and calls `generateZoomLinkWithParams` → `CalloutManabieLesson.generateZoomLink` — a real external Zoom API callout — **once per allocation, including an archived one**, then writes the new link/time back onto that archived student's own `Zoom_Participant__c` row (`:687-714`, `BaseDML.doUpdate` at `:717`).
- **Single Zoom** (one shared lesson-level link): `LessonZoomHandler.cls:607-655` generates exactly one link keyed off `rootLesson.Id`, independent of any specific student — archive state of any individual student has zero bearing here.

Exposure check: `LessonDataHandlerOutSide.cls`'s `getLessonList` (:297-305) and `getLesson`'s `Student_Sessions__r` subquery (:560-567) both correctly filter `Is_Archived__c = FALSE`, so the archived student never sees this regenerated link via Learner App — the waste is confined to the backend. The BO "Multiple Zoom" detail section (`DetailSectionMultipleZoomInfo.tsx` in `school-portal-admin`) renders whatever its GraphQL query returns with no archived filter visible in the component itself; whether the upstream query already excludes archived students was not conclusively traced and needs to be verified manually during test execution.

## Suite: Edit lesson info in lesson detail on SF (suite TBD)

### Editing Lesson Date/Time on a Multiple-Zoom-Type Lesson Regenerates an Archived Student's Zoom Link, Consuming an Unnecessary External Zoom API Call

**Description:** Gap case — Decision Table — `LessonZoomLinkDataMapper.retrieveZoomParticipantData()`'s unfiltered `Zoom_Participant__c` query means editing a lesson's date/time regenerates the Zoom meeting (via a real external Zoom API callout) for EVERY student's `Lesson_Allocation__c` found on the lesson, including one whose allocation is already archived — identical treatment to an active student's. The archived student never sees the result (Learner App correctly filters them out upstream), so there is no direct customer-facing leak on that surface, but the external Zoom resource is consumed needlessly, and the BO "Multiple Zoom" detail list's exposure of this stale entry to staff is unverified and should be checked manually.

**Preconditions:**
- Lesson 1 (Teaching Medium = Zoom, Zoom Type = Multiple) has Student A and Student B both assigned, each with their own Zoom link already generated (Student A's Zoom_Participant__c = ZP_A, Student B's = ZP_B).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | Student A's Student Session shows Is_Archived__c = TRUE; Student A's Zoom_Participant__c (ZP_A) record is untouched by this step | Archived_At__c = current timestamp |
| 2 | CM/Teacher edits Lesson 1's date/time ("only this lesson") and saves | The lesson's date/time updates successfully | New Start_Date_Time__c triggers isDateTimeChanged = TRUE |
| 3 | SF Admin inspects Student A's Zoom_Participant__c (ZP_A) record after the save | ZP_A shows a newly regenerated meeting link/occurrence time matching the lesson's new date/time — an external Zoom API call was made for Student A's (archived) allocation exactly as for an active student | retrieveZoomParticipantData's query has no Is_Archived__c filter; Student A's Lesson_Allocation__c Id is included in the regeneration loop |
| 4 | SF Admin inspects Student B's Zoom_Participant__c (ZP_B) record after the save | ZP_B also shows a correctly regenerated meeting link/occurrence time — expected, normal behavior for an active student | Student B Is_Archived__c = FALSE |
| 5 | Student A (archived) opens Learner App and checks their lesson schedule | Lesson 1 does not appear at all for Student A — the wasted Zoom regeneration in step 3 has no direct customer-facing exposure on this surface | getLessonList/getLesson's Is_Archived__c = FALSE filter excludes Student A's row entirely |
| 6 | CM/Teacher opens the BO "Multiple Zoom" detail section for Lesson 1 | [To verify at execution] Confirm whether Student A's (archived) row still appears in this list alongside Student B's — if it does, staff see a needlessly regenerated zoom entry for a student who is no longer actually assigned to the lesson | DetailSectionMultipleZoomInfo.tsx renders its query's result with no archived filter visible in the component itself; upstream filtering unconfirmed by static code trace |

**Severity:** major
**Priority:** medium

---

### Editing Lesson Date/Time on a Single-Zoom-Type Lesson Is Unaffected by Any Individual Student's Archive State

**Description:** Regression / control case — Decision Table, contrasts with the Multiple-Zoom gap above — for a Single-Zoom-type lesson, the Zoom link is generated once per lesson (keyed to the lesson's own Id, not to any specific student's allocation), so archiving one of several assigned students has zero bearing on the date/time-edit Zoom regeneration path. This should be locked in as a regression case since it demonstrates the two Zoom types diverge in how (and whether) the gap above applies.

**Preconditions:**
- Lesson 1 (Teaching Medium = Zoom, Zoom Type = Single) has Student A and Student B both assigned, sharing one lesson-level Zoom link (Zoom_Participant__c = ZP_1).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | Student A's Student Session shows Is_Archived__c = TRUE; the lesson's single Zoom_Participant__c (ZP_1) is untouched, since it is not keyed to any individual student | Archived_At__c = current timestamp |
| 2 | CM/Teacher edits Lesson 1's date/time ("only this lesson") and saves | The lesson's date/time updates successfully | New Start_Date_Time__c triggers isDateTimeChanged = TRUE |
| 3 | SF Admin inspects Lesson 1's single Zoom_Participant__c (ZP_1) record after the save | Exactly one regenerated meeting link/occurrence time is produced, matching the new lesson date/time — identical to what would happen if Student A had never been archived at all, since this path is lesson-level, not student-level | LessonZoomHandler's SINGLE branch (lines 607-655) keys regeneration off rootLesson.Id only |

**Severity:** minor
**Priority:** low

---
