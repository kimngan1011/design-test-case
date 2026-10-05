# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 2760 — "My Lessons"](https://app.qase.io/project/PX?suite=2760) (11 existing cases, under "[Nichibei] Lesson Booking System", LT-96620/LT-104607, parent 2759). This is spec.md's named Critical "Nichibei Lesson Booking" risk. None of the 11 cases reference `Archived_At__c`/`Is_Archived__c`.

**Code-trace confirmation — already safe, control cases only.** `BookingLessonHandlerOutSide.cls`: `getReservationSetting()` (`lines 547-574`) already filters `Archived_At__c = NULL` (line 570) when counting active LAs to set `allowReserveMore` (which gates the Browse/Reserve-New-Lesson button). `getReservationList()` (`lines 487-545`) already filters `Is_Archived__c = FALSE` (line 505) when building the student's own booked-lesson list. These cases exist to manually re-verify both on the live Nichibei org, matching the general "archived unusable, restore normal" principle already proven elsewhere in this epic.

## Suite: My Lessons

### [Nichibei] My Lessons – Browse/Reserve New Lesson Button Hides When the Student's Only LA Archives

**Description:** AC-5 (parity) — Regression — control case. Contrasts with existing baseline (#20856 "Browse Lessons Button – Student has active LA – Button visible", #20857 "...no active LA – Button hidden", which only test never-created/expired LA, not the archive trigger). Code-confirmed: `getReservationSetting()` already excludes archived LAs from its active-LA count (`Archived_At__c = NULL`, `cls:570`).

**Preconditions:**
- Student A has exactly one active Lesson Allocation; the "Browse Lessons" (+) / "Reserve New Lesson" button is currently visible on the My Lessons screen.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A opens the "Lesson Booking" menu and confirms the Browse/Reserve New Lesson button is visible | Button visible and tappable | Archived_At__c = blank |
| 2 | The Student Package Order group behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | Student A reopens the "Lesson Booking" menu | The Browse/Reserve New Lesson button is no longer visible; the "No courses available for booking" empty state is shown (same as the never-had-an-LA case, #21674) | Archived LA excluded from allowReserveMore's count |
| 4 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again | Archived_At__c = null (restored) |
| 5 | Student A reopens the "Lesson Booking" menu | The Browse/Reserve New Lesson button is visible again | Archived_At__c = blank (restored) |

**Severity:** minor
**Priority:** medium

---

### [Nichibei] My Lessons – Booking Hidden When Its Lesson Allocation Archives; Restored – Reappears

**Description:** AC-5 / AC-3 (parity) — Regression — control case. Contrasts with existing baseline (#20853 "Booking List – Student with booked lessons – All shown"). Code-confirmed: `getReservationList()` already filters `Is_Archived__c = FALSE` (`cls:505`) on the student's own booked-lesson list.

**Preconditions:**
- Student A has a booked lesson (Booking_Flag = TRUE, lesson_date >= today) currently shown on the My Lessons screen.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A opens My Lessons and confirms the booked lesson card is shown | Lesson card visible | Student Session Is_Archived__c = FALSE |
| 2 | The Student Package Order group behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Student Session becomes Is_Archived__c = TRUE via formula | Archived_At__c = current timestamp |
| 3 | Student A reopens My Lessons | The booking no longer appears in the list | Excluded by getReservationList's Is_Archived__c = FALSE filter |
| 4 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id | The Student Session returns to Is_Archived__c = FALSE | Archived_At__c = null (restored) |
| 5 | Student A reopens My Lessons | The booking reappears — the same original Student Session, not a new one | Session restored, not duplicated |

**Severity:** minor
**Priority:** medium

---
