# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suites reviewed: [PX suite 2761 — "Lesson Lists"](https://app.qase.io/project/PX?suite=2761) (21 cases) and [PX suite 2763 — "Cancel Booking"](https://app.qase.io/project/PX?suite=2763) (17 cases), both under "[Nichibei] Lesson Booking System" (parent 2759). Completes the control-case sweep started in `nichibei-booking-my-lessons-control.md` and `nichibei-booking-la-selection-control.md` — the user asked for every confirmed-safe path in this area to get its own explicit test case for live re-verification, not just a subset. None of the 38 cases across these two suites reference `Archived_At__c`/`Is_Archived__c`.

**Code-trace confirmation.** `BookingLessonHandlerOutSide.cls`:
- `getLessonBookingList()` (`lines 296-310`): `locationScopeIds` — the set of locations a student is allowed to browse lessons at — is derived only from the student's Lesson Allocations with `Archived_At__c = NULL` (line 307). If a student's only LA covering a given location archives, that location (and every lesson at it) drops out of Browse scope entirely.
- Cancel Booking's point refund (case #20939, "Points refunded to Point LA on cancellation") rides the same `unassignStudentSessionsFromLesson`-family code already confirmed in this epic's Point Consumption work (`nichibei-point-consumption-lesson-detail-archive-gap.md`) to have no archive guard on the write side — a refund still writes correctly to the target Point LA even if it has since archived, consistent with AC-8 (archive must never block an otherwise-legitimate write).

## Suite: Lesson Lists

### [Nichibei] Lesson Lists – Archived LA Removes Its Location From Browse Scope Entirely

**Description:** AC-5 (parity) — Regression — control case. Contrasts with existing baseline (#20868 "Location Filter – Only student's LA's Location Course locations shown"). If a student's only Lesson Allocation covering a given location archives, lessons at that location must disappear from Browse entirely — not just become unbookable — since the location itself is no longer in the student's `locationScopeIds`.

**Preconditions:**
- Student A has exactly one active Lesson Allocation, linked to a Location Course for Location A. Bookable lessons exist at both Location A and Location B; only Location A's lessons currently appear in Browse (per baseline #20868).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A opens Browse/Lesson Lists and confirms only Location A's lessons appear | Location A lessons shown; Location B lessons absent | LA Archived_At__c = blank; locationScopeIds = {Location A} |
| 2 | The Student Package Order group behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | Student A reopens Browse/Lesson Lists | No lessons appear at all (Location A dropped out of locationScopeIds, and Student A has no other LA covering Location B) — consistent with the empty-state behavior already covered for "no active LA" (#20860) | locationScopeIds now empty → Browse shows the empty state |
| 4 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 5 | Student A reopens Browse/Lesson Lists | Location A's lessons reappear, exactly as before the archive | locationScopeIds = {Location A} again |

**Severity:** minor
**Priority:** medium

---

### [Nichibei] Lesson Lists – "Bookable Only" Toggle – Archived Session Wrongly Excludes a Re-Bookable Lesson (Confirmed Gap)

**Description:** AC-5 — Negative — confirmed gap, not a control case. Contrasts with existing baseline (#20871 "Filter – Bookable Only toggle shows only bookable lessons"). Code-confirmed inconsistency within `getLessonBookingList()` itself: the `isBookedAlready` flag (`cls:289`) correctly filters `Is_Archived__c = FALSE`, but the separate `bookableOnly = true` exclusion subquery (`cls:352`) only filters `Is_Deleted__c = FALSE` — missing the archive filter. A lesson the student should be able to re-book (their only prior session on it is archived) is silently dropped from the list instead of being offered, whenever the student toggles "Bookable Only" on Browse.

**Preconditions:**
- Student A previously had a Student Session on Lesson X, but that session's Lesson Allocation has since archived (`Archived_At__c` populated), so the session is `Is_Archived__c = TRUE`.
- Lesson X is otherwise fully bookable again (Published, Bookable_Flag = TRUE, within deadline, capacity available) via a different, currently-active Lesson Allocation Student A now holds for the same location/course.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A opens Browse/Lesson Lists with the "Bookable Only" toggle OFF | Lesson X appears, with `isBookedAlready = false` (correctly excludes the archived old session) | Line 289 subquery correctly filters Is_Archived__c = FALSE |
| 2 | Student A turns the "Bookable Only" toggle ON | Per AC-5, Lesson X should still appear, consistent with step 1's correct `isBookedAlready = false` | Expected: Lesson X still shown |
| 3 | Student A checks the Bookable-Only-filtered list | [Confirmed by code] Lesson X is missing from the list — the `bookableOnly` exclusion subquery at `cls:352` treats the archived session as if Student A were still booked, silently dropping the lesson instead of offering it (fail — route to the engineering owner of `getLessonBookingList`) | `cls:352` lacks `Is_Archived__c = FALSE`, inconsistent with cls:289 in the same method |

**Severity:** major
**Priority:** high

---

## Suite: Cancel Booking

### [Nichibei] Cancel Booking – Point Refund Still Lands on the Target Point LA Even If Now Archived

**Description:** AC-3 / AC-8 (parity) — Regression — control case. Contrasts with existing baseline (#20939 "Points refunded to Point LA on cancellation"). Per AC-3/AC-8's design principle (archive is a pure state marker that never blocks an otherwise-legitimate write, and archiving never deletes financial history), self-cancelling a booking must still refund points to the correct Point LA — identified by the same record Id — even if that LA has since archived between the original booking and the cancellation.

**Preconditions:**
- Student A booked Lesson 1, with 2 points deducted from Point LA-B (Remaining went from 5 → 3 pts) at booking time.
- Point LA-B's `Archived_At__c` becomes populated (its order group is fully removed) after the booking but before Student A cancels, while the booking itself remains within the cancellation deadline.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff confirms LA-B's Remaining Points = 3 and `Archived_At__c` is populated, before cancellation | LA-B is archived but its point balance is unchanged from the booking | LA-B Archived_At__c = populated; Remaining = 3 |
| 2 | Student A opens My Lessons, taps Cancel on Lesson 1, and confirms "Cancel Reservation" | Cancellation is confirmed; the Student Session is removed from Lesson 1 | Student Session deleted |
| 3 | HQ or CM Staff checks LA-B's Remaining Points and Consumed Points after cancellation | Remaining Points = 5 (3 + 2 refunded); Consumed Points decremented by 2 — the refund succeeds and lands on LA-B (same Id) despite it being archived | LA-B Remaining = 5; refund not blocked or misdirected by the archived state |

**Severity:** minor
**Priority:** medium

---
