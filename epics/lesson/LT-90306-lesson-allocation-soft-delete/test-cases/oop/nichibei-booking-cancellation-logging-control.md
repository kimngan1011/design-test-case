# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 3100 — "Cancellation Logging – CM Chatter Notification"](https://app.qase.io/project/PX?suite=3100) (12 existing cases, LT-104607, under "[Nichibei] Lesson Booking System", parent 2759). This directly addresses spec.md's own named risk for Nichibei Lesson Booking: "Unarchive must not silently recreate a booking or resend a notification." None of the 12 cases reference `Archived_At__c`/`Is_Archived__c`.

**Code-trace confirmation — structurally safe, not just incidentally safe.** The CM Chatter post and the "last-student-cancels → revert to Draft" logic are both gated behind a single platform event, `MANAERP__Lesson_Platform_Event__e` (`Operation__c = 'CancelLessonBooking'`), published from exactly one place in the entire codebase: `BookingLessonHandlerOutSide.cancelReservedLesson` (`cls:736-815`). `LessonPlatformEventHandler.cancelLessonBooking` (`cls:281-342`) does both the Draft-revert (`:317-327`) and the Chatter post (`:329-333`) from that one event. Archiving an LA only runs `LessonAllocationHandler.afterUpdate`, which explicitly skips archived records (`cls:1326-1329`, `if (Archived_At__c != null) continue;`) and never calls into this event-publishing code at all — there is no code path connecting them, so an archive event cannot spuriously fire either side effect. The Chatter post's `[Student Name]` → LA-record hyperlink (`ChatterPostHandler.cls:131` → `LessonUtils.buildRecordUrl:388-396`) is a raw Id-based permalink with no SOQL/archive filter, so it resolves correctly for an archived LA too.

## Suite: Cancellation Logging – CM Chatter Notification

### [Nichibei] Archiving a Lesson Allocation Does Not Spuriously Create a CM Chatter Post or Revert a Published Lesson to Draft

**Description:** AC-1 / AC-5 (parity) — Regression — control case, directly verifying the spec's named concern. Contrasts with existing baseline (#23901 "Student self-cancels via app – Chatter post created for CM", #23902 "Staff manually removes Student Session via SF – No Chatter post created" — the latter already proves non-self-cancel removal paths don't trigger the notification; this case extends that same guarantee to the archive mechanism specifically, which is structurally incapable of reaching the trigger at all).

**Preconditions:**
- Published Lesson X (auto-published via booking) has exactly 1 Student Session, Student A, booked via the self-service app. No existing Chatter post exists on Lesson X under topic 予約授業のキャンセル.
- CM1 is assigned to Lesson X's Location.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff confirms Lesson X's status = Published, 1 Student Session, 0 Chatter posts | Baseline confirmed | Published; count = 1; 0 posts |
| 2 | The Student Package Order group behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived (NOT via the app's self-cancel action) | The Lesson Allocation shows Archived_At__c populated; Student A's Student Session becomes Is_Archived__c = TRUE via formula — hidden, but not deleted | Archived_At__c = current timestamp; Student Session record still exists |
| 3 | HQ or CM Staff checks Lesson X's status in Salesforce | Lesson X remains Published — no Draft-revert occurred, since archiving never publishes the `CancelLessonBooking` platform event this logic depends on | Lesson X Status = Published, unchanged |
| 4 | HQ or CM Staff checks Lesson X's Chatter/Activity tab | No new Chatter post was created — still 0 posts under topic 予約授業のキャンセル | 0 posts, unchanged |

**Severity:** minor
**Priority:** medium

---

### [Nichibei] Unarchive Does Not Resend a Cancellation Notification or Recreate a Booking

**Description:** AC-3 (parity) — Regression — control case, directly verifying the spec's named concern ("unarchive must not silently recreate a booking or resend a notification"). Confirms that restoring a Lesson Allocation on the same record Id is a pure visibility change with no side-effect notifications, matching the general "restore works normally, nothing extra happens" principle already established throughout this epic.

**Preconditions:**
- Following directly from the case above: Lesson X's Lesson Allocation for Student A is archived; Lesson X remains Published with 0 Chatter posts.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id | The Lesson Allocation shows Archived_At__c blank again; Student A's Student Session returns to Is_Archived__c = FALSE | Archived_At__c = null (restored) |
| 2 | HQ or CM Staff checks Lesson X's Chatter/Activity tab | No new Chatter post was created by the restore — still 0 posts | 0 posts, unchanged |
| 3 | HQ or CM Staff checks whether a second Student Session was created for Student A on Lesson X | Exactly one Student Session exists — the same original record, not a newly "recreated" booking | Expect: 1 Student Session, same Id as before archive |
| 4 | HQ or CM Staff checks Lesson X's status | Lesson X remains Published, unaffected by the restore | Lesson X Status = Published, unchanged |

**Severity:** minor
**Priority:** medium

---

### [Nichibei] CM Chatter Post's Student Name Link Still Resolves Correctly After the Referenced LA Later Archives

**Description:** AC-5 (parity) — Regression — control case. Contrasts with existing baseline (#23904 "Student Name and Lesson Name are hyperlinked to correct records"). Confirms the historical-record-access principle (archived records remain reachable by direct Id) holds for this specific permalink, built before the archive and never re-queried.

**Preconditions:**
- Student A previously self-cancelled a different booking, creating a CM Chatter post whose `[Student Name]` token links to Student A's Lesson Allocation (LA-A), per baseline #23904.
- LA-A has since archived (`Archived_At__c` populated), unrelated to the cancellation itself.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | CM1 opens the existing Chatter post and clicks the Student Name link | The link still navigates to LA-A's record, now showing it as archived (Archived_At__c populated) | LA-A Archived_At__c = populated |
| 2 | CM1 confirms the record is viewable, not an error/broken-link page | LA-A's detail page loads normally, consistent with AC-5's "archived records remain reachable by direct record Id" principle | Permalink is a raw Id reference with no archive-filtered query |

**Severity:** minor
**Priority:** medium

---
