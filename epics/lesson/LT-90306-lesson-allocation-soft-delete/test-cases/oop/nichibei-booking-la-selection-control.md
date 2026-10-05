# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 2762 — "Book a Lesson"](https://app.qase.io/project/PX?suite=2762) (19 existing cases, under "[Nichibei] Lesson Booking System", LT-96620/LT-104607, parent 2759). This is spec.md's named Critical "Nichibei Lesson Booking" risk. None of the 19 cases reference `Archived_At__c`/`Is_Archived__c`.

**Code-trace confirmation.** `BookingLessonHandlerOutSide.cls:reserveLesson()`, lines 638-651:
```
WHERE MANAERP__Student__c = :studentContact.Id
  AND MANAERP__Location_Course__r.MANAERP__Account__c = :locationId
  AND MANAERP__Start_Date_Time__c <= :lessonDate AND MANAERP__End_Date_Time__c >= :lessonDate
  AND MANAERP__Require_Allocation__c = TRUE AND MANAERP__Type__c INCLUDES ('Regular')
  AND MANAERP__Archived_At__c = NULL
ORDER BY MANAERP__Start_Date_Time__c ASC, CreatedDate ASC LIMIT 1
```
This single query backs every "LA Selection" case in this suite (#20886-#20889: location-matching is a hard equality filter on the lesson's own location, not a priority step, so a non-matching-location LA is never a candidate at all; then earliest-start, then earliest-created break ties) — already archive-filtered. The same query re-runs at Confirmation time, so an LA that archives between Browse and Confirmation is caught there too, throwing `NO_LESSON_ALLOCATION` — the same error path already covered by baseline #20893, but that case's precondition ("LA deleted mid-flow") predates this epic and needs updating to the archive mechanism, which has zero dedicated test today.

## Suite: Book a Lesson

### [Nichibei] Book a Lesson – LA Selection – Archived LA Excluded Even When It Would Otherwise Win on Location and Date

**Description:** AC-5 (parity) — Regression — control case. Contrasts with existing baseline (#20887 "Location-matching LA prioritized over non-matching", #20888 "Earliest start date LA selected"). An LA that matches the lesson's location and would win the earliest-start/earliest-created tiebreak must still be excluded from selection if it is archived.

**Preconditions:**
- Student A has two Lesson Allocations at the lesson's Location A: LA-A (start = 2026-01-01, would normally win the tiebreak) and LA-B (start = 2026-03-01, the next-best candidate). Both are otherwise eligible (Require_Allocation = TRUE, Type includes Regular, date range covers the lesson date).
- LA-A's `Archived_At__c` is populated (archived via its order group being fully removed).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A books a lesson at Location A | Per the code's `Archived_At__c = NULL` filter, LA-A should not be selected despite having the earliest start date | LA-A Archived_At__c = populated |
| 2 | HQ or CM Staff checks which LA the resulting Student Session is linked to | LA-B is used, confirming the archived LA was correctly excluded from the candidate set before the tiebreak even ran | LA-B is the Lesson_Allocation__c on the new Student Session |

**Severity:** minor
**Priority:** medium

---

### [Nichibei] Book a Lesson – LA Archives Between Browse and Confirmation – Booking Blocked (Archive Replaces Legacy "LA Deleted Mid-Flow")

**Description:** AC-5 — Decision Table — regression-contrast with existing baseline (#20893 "No active LA – Booking blocked," precondition: "Student's LA has expired between Browse and Confirmation step (or LA deleted mid-flow)"). That case's wording predates this epic's archive mechanism — under the new flow, an LA is never hard-deleted mid-flow, it is archived. This case explicitly covers the archive variant, since it has zero dedicated coverage today despite reusing the identical code path and error.

**Preconditions:**
- Student A has exactly one active Lesson Allocation and has reached the Booking Confirmation screen for a lesson at that LA's location.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A opens a bookable lesson and proceeds to the Confirmation screen | Confirmation screen shown normally, LA still active at this point | Archived_At__c = blank |
| 2 | While the Confirmation screen is still open, the Student Package Order group behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | Student A taps "Confirm" to complete the booking | The booking is rejected — `reserveLesson()`'s re-run of the LA-selection query finds no eligible LA and throws `NO_LESSON_ALLOCATION`, surfacing the same "no active LA" error as baseline #20893 | reserveLesson() query excludes the now-archived LA; no Student Session created |
| 4 | HQ or CM Staff confirms no Student Session was created for this attempt | No orphaned or partial Student Session exists for Student A on this lesson | No DML occurred past the LA-selection failure |

**Severity:** major
**Priority:** high

---
