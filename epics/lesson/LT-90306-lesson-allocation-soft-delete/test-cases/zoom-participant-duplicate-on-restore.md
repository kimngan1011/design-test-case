# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 2256 — "Check clashing across locations"](https://app.qase.io/project/PX?suite=2256) (parent 2129 "CM/Teacher Verify Zoom Owner") — this file continues the investigation already done for suite 2256 (zoom-owner-clash-across-locations-archive.md), but covers a different angle raised by the reviewer: when a student's Lesson Allocation is restored and the "Generate the multiple zoom" action (the same action used throughout suite 2256's baseline cases) is re-run for that lesson, is there any deduplication risk for the student's Zoom Participant record?

Code trace: the actual creation flow behind "Generate the multiple zoom" is `LessonZoomRestAPI.AddMultipleZoomLink.run()` (`packages/lesson/main/default/classes/restapi/LessonZoomRestAPI.cls:236-256`) — a different code path from `LessonZoomHandler.calcRenewLessonZoomLinks` (the date/time-edit UPDATE path already covered in `edit-lesson-datetime-zoom-regen-archive.md`). This flow is a **delete-all-then-insert-all**, not an upsert:
- `cleanZoomParticipants(lessons)` (:155-164, called at :249) selects ALL existing `Zoom_Participant__c WHERE Lesson__c IN :lessons` (no student filter) and routes them to `DeleteRecordEventHandler.deleteAsynchronous(...)` (`DeleteRecordEventHandler.cls:17-30`), which only **publishes** a `Lesson_Platform_Event__e` — the actual hard DELETE happens later, in a separate transaction, inside `LessonPlatformEventHandler`/`LessonPlatformEventSubscriber.trigger` (:46-49, 108-110).
- `extractStudentSessionInfo` (:176-192) — the "who is eligible for a new link" query — is `Student_Sessions__c WHERE Lesson__c IN :lessons AND Is_Deleted__c = FALSE AND Is_Archived__c = FALSE`. A just-restored student correctly passes this filter.
- `insertZoomParticipants` (:194-234) then **synchronously** inserts a brand-new `Zoom_Participant__c` row for every eligible session from the query above — including the restored student — in the SAME transaction, before the async delete event from step 1 has had any chance to run.

Because the old row's deletion is asynchronous while the new row's insertion is synchronous and immediate, the old (pre-archive) and new (post-restore) `Zoom_Participant__c` rows for the same student+lesson coexist for at least the duration of the async event's processing delay. No upsert/unique-key constraint on `(Lesson__c, Student_Session__c)` was found anywhere in this flow, and no retry/dead-letter handling was found in `LessonPlatformEventHandler` for a failed delete — if the async delete event errors or never processes, the old row becomes a permanent orphaned duplicate.

## Suite: Check clashing across locations (suite TBD)

### Restoring an Archived Student Then Re-Generating the Multiple Zoom Creates a Transient Duplicate Zoom Participant Row

**Description:** Gap case — Decision Table — demonstrates the directly-observable, easily-reproducible half of the finding: right after restoring a student's Lesson Allocation and re-running "Generate the multiple zoom" for their lesson, the student's OLD Zoom Participant row (from before the archive) and a brand-new one both exist simultaneously, because the old row's deletion is only an asynchronously-published platform event at the moment the new row is inserted.

**Preconditions:**
- Lesson 1 (Teaching Medium = Zoom, Zoom Type = Multiple) has Student A assigned, with Zoom_Participant__c (ZP_A) already generated for them.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | Student A's Student Session shows Is_Archived__c = TRUE; ZP_A is untouched | Archived_At__c = current timestamp |
| 2 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is restored (Archived_At__c cleared) | Student A's Student Session shows Is_Archived__c = FALSE again | Archived_At__c = null (restored) |
| 3 | CM/Teacher clicks "Generate the multiple zoom" again for Lesson 1 (e.g., because a new Student C was just added and also needs a link) | The action completes and reports success; `extractStudentSessionInfo`'s eligibility query includes Student A (Is_Archived__c = FALSE), so `insertZoomParticipants` synchronously creates a NEW Zoom_Participant__c row (ZP_A2) for Student A in the same transaction | cleanZoomParticipants only PUBLISHES a delete event for ZP_A at this point; it has not executed yet |
| 4 | SF Admin immediately queries Zoom_Participant__c WHERE Lesson__c = Lesson 1 AND Student_Session__c = Student A's session, right after step 3's save completes | BOTH ZP_A (old) and ZP_A2 (new) are returned — two Zoom Participant rows exist simultaneously for the same student+lesson, since the async delete of ZP_A has not yet run | Transient duplicate window confirmed |
| 5 | SF Admin re-queries the same records a few minutes later, after the async platform event has had time to process | Only ZP_A2 remains; ZP_A has been hard-deleted by `LessonPlatformEventSubscriber` — the expected, correct end state once the async cleanup completes normally | Happy-path resolution, assuming the async delete succeeds |

**Severity:** major
**Priority:** high

---

### [To Verify With Engineering] If the Async Zoom Participant Cleanup Event Fails, the Pre-Archive Zoom Participant Row Becomes a Permanent, Undetected Duplicate

**Description:** Gap case — Decision Table, extends the transient-window case above — no retry or dead-letter handling was found in `LessonPlatformEventHandler`/`LessonPlatformEventSubscriber.trigger` for a failed deletion of the old `Zoom_Participant__c` row. If that async delete event errors, hits a governor limit, or is otherwise never successfully processed (e.g., subscriber exception, event bus backlog), the old row (ZP_A) is never cleaned up and permanently coexists with the newly-inserted row (ZP_A2) for the same student+lesson. Since `Student_Session__c` is only correctly re-pointed on the NEW row, the old row is left stale and orphaned, but still a real Zoom-API-backed meeting that nobody is tracking. This case requires engineering support (checking platform event failure logs/monitoring, or deliberately inducing a subscriber failure in a sandbox) to fully reproduce — QA should flag it for review rather than attempt to force the failure via UI alone.

**Preconditions:**
- Same setup as the previous case, immediately after step 3 (both ZP_A and ZP_A2 exist in the transient window).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Engineering checks Salesforce Setup → Apex Exception Email / Platform Event monitoring for any failed `Lesson_Platform_Event__e` deliveries tied to this lesson's delete-participant event around the time of step 3 | Ideally: no failures, and the event completes normally (covered by the happy-path case above). If failures ARE found in general monitoring for this event type, flag as confirmed systemic risk | Check Setup → Apex Jobs / Platform Event usage, or application logs for LessonPlatformEventHandler exceptions |
| 2 | (If reproducible in a sandbox) Temporarily disable or break `LessonPlatformEventSubscriber.trigger` (or induce an exception in its handler), then repeat steps 1-3 of the previous case | ZP_A is never hard-deleted; it remains indefinitely alongside ZP_A2 | Simulated async failure |
| 3 | Re-enable the subscriber and check whether any backlog/catch-up mechanism exists to retroactively clean up the now-stale ZP_A | Determine whether Salesforce's platform event retry window (24-hour replay) or any custom retry logic eventually cleans this up, or whether the row is permanently orphaned once the retry window lapses | No custom retry/dead-letter logic found in LessonPlatformEventHandler at the time of this trace — likely permanent if the native platform event retry window is exhausted |

**Severity:** critical
**Priority:** medium

---
