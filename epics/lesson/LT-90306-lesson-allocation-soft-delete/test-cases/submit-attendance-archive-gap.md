# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suites reviewed: [PX suite 3276 — "Submit Attendance and Send Notification"](https://app.qase.io/project/PX?suite=3276) (16 existing cases, LT-107666) and its sibling [PX suite 1241 — "Attendance submission without duplicate notifications"](https://app.qase.io/project/PX?suite=1241) (2 existing cases, LT-85859/LT-85860) — same underlying feature, 1241 being the original multi-lesson/no-duplicate-notification baseline that 3276 extends. Suites 3277 ("Submit Attendance Page") and 3278 ("View Chatter Post") were also reviewed: 3277 is pure form-UI validation (character limits, required fields) with no archive dependency — the lesson list it populates from is already covered by the `getLessonList()` filter confirmed elsewhere in this epic; 3278's hyperlink-navigation cases inherit correctness entirely from whether a notification was sent in the first place, so no additional case is needed there beyond the one below. None of the existing cases in any of these suites test an archived Lesson Allocation.

Code trace — this is a genuinely new and significant architectural gap, more severe than any other "silent drop" pattern already found in this epic, because the entire flow is asynchronous with no feedback path to the UI:

1. **Flutter → `LessonMiddlewareHandler.submitLessonAttendance`** → `LessonDataHandlerOutSide.doSubmitAttendance` (`outside-packages/dlrs/main/default/classes/lesson/LessonDataHandlerOutSide.cls:176-195`). This method does **zero SOQL against `Student_Sessions__c`** — it only validates the Contact exists, then publishes a platform event (`Lesson_Submit_Attendance_Event__e`) carrying the raw, unchecked `lessonIds` the client submitted, and returns success **immediately**, before any actual data is written.
2. **Async subscriber does the real write** — `LessonSubmitAttendanceEventHandler` (triggered off the platform event, in a separate transaction, after the Apex call already returned to the UI) queries:
   ```apex
   WHERE Lesson_Allocation__c IN (SELECT ID FROM Lesson_Allocation__c WHERE Student__c IN :studentIds)
     AND Lesson__c IN :lessonIds AND Is_Deleted__c = FALSE AND Is_Archived__c = FALSE
   ```
   Only the rows that pass this filter get their `Attendance_Response__c` updated.
3. **Notifications** (Chatter post to CM/Teacher, push notification to Parent) fire from `StudentSessionsHandler.afterUpdate`, triggered only by whatever rows survived step 2 — their correctness is entirely inherited from that filter, with no independent archive check of their own (except `sentChatterPost`'s secondary `resolveLessonIdsByLocationId` re-filter, a narrower belt-and-suspenders check for the same transaction window).
4. **There is no code anywhere in this chain that diffs the originally-submitted `lessonIds` against what was actually updated, and no feedback path back to the UI reporting partial success.** Confirmed via test coverage review: `IndividualRecurringLessonTest.cls` has 4 tests for `LessonSubmitAttendanceEventHandler`, none exercising an archived/deleted session or a multi-lesson event with mixed archive states — this scenario has zero existing Apex test coverage either.

**Practical consequence**: a student/parent submits attendance for multiple lessons at once (exactly the scenario already tested by suites 1241/3276, e.g. case 10131/10132, "2 lessons sharing same allocation" / "3 lessons across 2 allocations"). If one of those lessons' Lesson Allocation is archived between the moment the lesson list was loaded and the moment the async event subscriber processes the submission, that lesson's attendance is silently dropped — no record created, no CM/Teacher notification, no parent confirmation for it — while the Learner App still shows "Submitted successfully" for the full batch, with no indication anything was missed.

## Suite: Submit Attendance and Send Notification

### Submit Attendance for Multiple Lessons – One Lesson's Allocation Archived Mid-Flight – That Lesson Silently Dropped (No Record, No Notification); UI Still Reports Full Success

**Description:** Gap case — Decision Table, contrasts with the baseline (case 10132 from suite 1241 / case 4025 from this suite, "3 Lessons Across 2 Allocations – 3 Separate Notifications Sent, No Duplicates") — submitting attendance for 3 lessons at once, where one lesson's Lesson Allocation becomes archived while the submission is still being processed asynchronously, results in only 2 of the 3 lessons' attendance being recorded and notified, while the Learner App reports the submission as fully successful for all 3, with no error, warning, or partial-failure indication anywhere in the flow.

**Preconditions:**
- Student A has parent B. Student A has 3 lessons scheduled: L1, L2, L3. L1 and L2 share Lesson Allocation A1; L3 has Lesson Allocation A2. All three lessons currently appear in Student A's Submit Attendance lesson list.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student/Parent selects L1, L2, and L3 on the Submit Attendance form, sets Attendance = Absent with a reason, and taps Submit | The app shows "Submitted successfully" (or equivalent) immediately — this happens before any Student_Sessions__c record is actually written, since `doSubmitAttendance` only publishes a platform event | EventBus.publish returns synchronously; no DML has occurred yet at this point |
| 2 | In a separate session, immediately after the submit action (while the async event is still queued/processing), the Student Package Order behind Lesson Allocation A1 (covering L1 and L2) is fully removed, so A1 is archived | A1 shows Archived_At__c populated; L1 and L2's Student Sessions now have Is_Archived__c = TRUE via formula | Archived_At__c = current timestamp on A1 |
| 3 | Wait for the async `LessonSubmitAttendanceEventHandler` to process the submission event | Only L3's Student Session (tied to still-active A2) gets Attendance_Response__c updated; L1 and L2's sessions are excluded by the subscriber's `Is_Archived__c = FALSE` filter and never updated | L1/L2 sessions excluded from `updatedStudentSessions`; L3 updated |
| 4 | CM checks the Notification Center / Chatter feed | Only 1 notification (for L3) is received — not 3 — since notifications only fire for rows that were actually updated in step 3 | sentChatterPost/sentNotificationForParent only process the 1 surviving row |
| 5 | Parent B checks Learner App notifications | Only 1 notification (for L3) is received by the parent as well — L1 and L2 produce no notification and no error, indistinguishable from "the student never submitted for L1/L2 at all" | No feedback anywhere in the app indicates L1/L2 were dropped |
| 6 | Student/Parent reopens the Submit Attendance history / lesson detail for L1 | L1 still shows no attendance response recorded, despite the app having reported a successful submission for it in step 1 | Attendance_Response__c remains blank on L1's (now-archived) Student Session |

**Severity:** critical
**Priority:** high

---

### Submit Attendance – Student Has Multiple Lesson Allocations, Only One Archived – Notification for the Lesson Under the Still-Active Allocation Sent Normally

**Description:** Regression / control case — Decision Table, isolates one specific aspect of the gap case above for direct, standalone verification — a student with multiple Lesson Allocations, only one of which is archived, continues to receive attendance-submission notifications normally for lessons tied to their OTHER, still-active Lesson Allocation(s). Archiving one allocation must not suppress or interfere with notifications for lessons under a different, unaffected allocation for the same student.

**Preconditions:**
- Student A has two Lesson Allocations: A1 for Course X (archived — Archived_At__c populated) and A2 for Course Y (active). Student A has a lesson L4 scheduled under A2, currently in the Submit Attendance lesson list (L4 is not affected by A1's archive, since they are unrelated allocations).

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student/Parent confirms L4 (Course Y, allocation A2) appears in the Submit Attendance lesson list | L4 is listed and selectable | A2 Is_Archived__c = FALSE → L4's Student Session included in getLessonList |
| 2 | Student/Parent selects only L4, sets Attendance = Absent with a reason, and submits | The app shows "Submitted successfully" | doSubmitAttendance publishes the event for L4 only |
| 3 | Wait for the async LessonSubmitAttendanceEventHandler to process the event | L4's Student Session is found and updated with Attendance_Response__c, since it belongs to A2 (not archived) — A1's archived state has no bearing on this record at all | L4's Lesson_Allocation__c = A2, independent of A1 |
| 4 | CM checks the Notification Center / Chatter feed | A notification for L4 is received normally, exactly as it would be if Student A had no archived allocation at all | sentChatterPost processes L4's updated row normally |
| 5 | Parent checks Learner App notifications | A notification for L4 is received normally | sentNotificationForParent processes L4's updated row normally |

**Severity:** minor
**Priority:** medium

---

### Group Lesson – Multiple Students Submit Attendance, One Archived – Archived Student's Name Never Appears in Any Chatter Post; Other Students' Posts Unaffected

**Description:** Regression / control case — Decision Table — confirms a structural guarantee, not just a query-filter behavior: `StudentSessionsHandler.sentChatterPost` builds exactly ONE Chatter post per (student, lesson) pair (`feedItemInputByStudentLesson`, keyed by `studentId + '_' + lessonId`), with the student's name embedded as literal hyperlink text in that single post's body (`CreateLessonChatterPostParams.CONTENT_TEMPLATE`, "`<a href="{student_link}">{student_name}</a> has submitted attendance response for...`") — there is no code path anywhere in this feature that aggregates multiple students' names into one shared post. Since an archived student's Student Session is excluded upstream (before any `FeedItemInput` is ever built for them), their name cannot appear in any Chatter post at all — not partially, not redacted from a shared post, simply never created — while every other non-archived student's individually-scoped post is completely unaffected by that exclusion.

**Preconditions:**
- A Group lesson has Student A (Lesson Allocation archived — Archived_At__c populated) and Student B (active Lesson Allocation) both scheduled. Both submit attendance for this lesson at roughly the same time.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A and Student B both submit attendance (e.g., Absent with a reason) for the same Group lesson via Learner App | Both submissions show "Submitted successfully" in the app | doSubmitAttendance publishes one event per submission |
| 2 | Wait for the async event subscriber to process both submissions | Only Student B's Student Session gets Attendance_Response__c updated; Student A's archived session is excluded | Student A Is_Archived__c = TRUE → excluded; Student B Is_Archived__c = FALSE → updated |
| 3 | CM/Teacher opens the lesson's Chatter feed | Exactly one Chatter post is visible — for Student B only. There is no post, no partial mention, and no trace of Student A's name anywhere in the feed for this lesson | feedItemInputByStudentLesson never received an entry for Student A, since their row was never in the updated Student_Sessions__c set that reaches StudentSessionsHandler.afterUpdate |
| 4 | CM/Teacher reads Student B's Chatter post content in full | The post correctly reads "[Student B's name] has submitted attendance response for [Lesson Name]..." with a working hyperlink to Student B's Contact record — completely normal, unaffected by Student A's archived state | Student B's post is single-student-scoped and independent of any other student's archive state |

**Severity:** minor
**Priority:** low

---

### Submit Attendance – Previously Archived Lesson Allocation Restored – New Attendance Submission Records and Notifies Normally

**Description:** Regression / control case — Decision Table, contrasts with the gap case above — once an archived Lesson Allocation is restored, submitting attendance for a lesson under that allocation works exactly like it would for an allocation that was never archived: the record is written and notifications are sent normally. This confirms the archive/restore cycle leaves no lasting breakage in the Submit Attendance mechanism once the Lesson Allocation is active again.

**Preconditions:**
- Student A's Lesson Allocation A1 (Course X) was previously archived; lesson L1 under A1 is now visible again in the Submit Attendance lesson list after a living Student Package Order reappeared and A1 was restored (Archived_At__c cleared) on the same record Id.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student/Parent confirms L1 reappears in the Submit Attendance lesson list after A1's restore | L1 is listed and selectable again | A1 Is_Archived__c = FALSE (restored) → L1's Student Session included in getLessonList again |
| 2 | Student/Parent selects L1, sets Attendance = Absent with a reason, and submits | The app shows "Submitted successfully" | doSubmitAttendance publishes the event for L1 |
| 3 | Wait for the async LessonSubmitAttendanceEventHandler to process the event | L1's Student Session is found and updated with Attendance_Response__c normally, since it now passes the Is_Archived__c = FALSE filter | L1 no longer excluded by the subscriber's WHERE clause |
| 4 | CM checks the Notification Center / Chatter feed | A notification for L1 is received normally | sentChatterPost processes L1's updated row |
| 5 | Parent checks Learner App notifications | A notification for L1 is received normally | sentNotificationForParent processes L1's updated row; mechanism fully functional post-restore, not left in a broken or permanently-suppressed state |

**Severity:** minor
**Priority:** medium

---
