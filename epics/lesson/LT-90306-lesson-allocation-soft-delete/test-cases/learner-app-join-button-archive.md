# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 450 — "View lesson and lesson report"](https://app.qase.io/project/PX?suite=450) (6 existing cases, under parent 320) — the home suite for the Student Mobile (Learner App) lesson+report viewing feature, including its "Join" button / Live Streaming Link. This file documents both a confirmed-correct control case and a newly-found gap, raised by the reviewer's question about the Join button on Learner App. None of the 6 existing cases test an archived Lesson Allocation.

Code trace: the Flutter Learner App calls two distinct Apex endpoints via `flutterCommunicate.js`, both routed through `LessonDataHandlerOutSide.cls` (`outside-packages/dlrs/main/default/classes/lesson/`):

- **`get-lessons-list` → `getLessonList()`** (lines 278-375) — the student's lesson schedule. Its SOQL (lines 297-305) filters `WHERE Lesson_Allocation__r.Student__c = :contactId AND ... AND Is_Deleted__c = FALSE AND Is_Archived__c = FALSE`, and only computes a `zoomUrl` for rows that pass this filter. **An archived student's lesson is correctly absent from this list entirely — no Join button is ever rendered for it, because the lesson row itself never reaches the client.**
- **`get-lesson-detail` → `getLessonInfo()` → `getLesson()`** (lines 8-90, 537-585) — a per-`lessonId` detail/Join-screen fetch, used whenever a specific lesson is opened directly (cached detail screen, deep link, push notification) rather than freshly derived from the filtered list above. Its outer query (`FROM Lesson__c WHERE Id IN :lessonIds`, lines 582-583) has **no Student_Sessions__c gate at all** — it returns the Lesson record purely by Id. The embedded attendance subquery (lines 560-567) filters `Is_Archived__c = FALSE` but **omits `Is_Deleted__c = FALSE`** (inconsistent with the other three Student_Sessions__c queries in the same class, all of which filter both). Critically, `getLessonInfo`'s zoomUrl resolution (lines 76-87) sources the Join link directly from `Lesson__c.Live_Streaming_Link__c` / `Lesson__c.Zoom_Link__c` for two of three Teaching-Medium/Zoom-Type branches (non-Zoom medium, and Zoom Type = "Single") — **with zero dependency on the student's session state at all** — so an archived student who already has this lesson's detail screen open, or who follows a stale push-notification/deep-link to it, can still see and use the Join button.

## Suite: Student Mobile — Lesson Join Button / Live Streaming Link (suite TBD)

### Learner App – Lesson Schedule List – Archived Student's Lesson Removed Entirely; No Join Button Ever Rendered

**Description:** Regression / control case — Decision Table — once a student's Lesson Allocation is archived, their upcoming lesson disappears from the Learner App's lesson schedule list entirely (not merely hiding the Join button on an otherwise-visible row), because `getLessonList()`'s query filters `Is_Archived__c = FALSE` before any zoomUrl is even computed. This is already correct and should be locked in with regression coverage.

**Preconditions:**
- Student A has an upcoming Zoom lesson (Teaching Medium = Zoom) today, currently visible in their Learner App lesson schedule with a "Join" button.
- Student A has an active Lesson Allocation for this course.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A opens the Learner App lesson schedule and confirms the upcoming lesson is shown with a "Join" button | The lesson row is visible with a Join button | Student A Is_Archived__c = FALSE; getLessonList returns this row |
| 2 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated | Archived_At__c = current timestamp |
| 3 | Student A refreshes the Learner App lesson schedule | The lesson no longer appears in the schedule at all — not grayed out, not missing only the Join button, but entirely absent | Student A's Student Session Is_Archived__c = TRUE (via formula) → excluded from getLessonList's WHERE clause before zoomUrl computation |
| 4 | A living Student Package Order reappears for Student A's Student Course, so the Lesson Allocation is unarchived on the same record Id, and Student A refreshes the schedule | The lesson reappears in the schedule with its Join button restored | Archived_At__c = null (restored); getLessonList includes the row again |

**Severity:** minor
**Priority:** medium

---

### Learner App – Lesson Detail Screen Opened Directly (Cached/Deep-Linked) – Archived Student Can Still See and Use the Join Button

**Description:** Gap case — Decision Table, contrasts with the control case above — if Student A already has a specific lesson's detail screen cached, bookmarked, or reached via a push-notification deep link (bypassing a fresh fetch of the filtered schedule list), the "Join" button and Zoom link still resolve and work even after their Lesson Allocation is archived, because `getLessonInfo`/`getLesson`'s Join-link resolution for non-"Zoom + Multiple-type" lessons reads `Live_Streaming_Link__c`/`Zoom_Link__c` directly off the `Lesson__c` record with no Student_Sessions__c archive/delete gate at all.

**Preconditions:**
- Student A has an upcoming lesson today with Teaching Medium = Offline with a Live Streaming Link configured (or Teaching Medium = Zoom with Zoom Type = "Single"). Student A has already opened this lesson's detail screen on Learner App once (e.g., via a push notification), so the client has the `lessonId` cached independent of the schedule list.
- Student A has an active Lesson Allocation for this course.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A opens the cached lesson detail screen for this lesson and confirms the Join button / Live Streaming Link is shown and functional | The Join button is shown; tapping it opens the configured link | Student A Is_Archived__c = FALSE |
| 2 | The Student Package Order behind Student A's Lesson Allocation is fully removed, so the Lesson Allocation is archived | The Lesson Allocation shows Archived_At__c populated; the lesson no longer appears in Student A's schedule list (per the control case above) | Archived_At__c = current timestamp |
| 3 | Student A reopens the SAME cached lesson detail screen directly (not via the schedule list) and taps "Join" | The Join button is still shown and still works — the student can still access the lesson's Live Streaming Link / Zoom meeting despite being archived | getLessonInfo's outer Lesson__c query has no session gate; for non-Zoom or Zoom-Type-Single lessons, zoomUrl resolves straight from Lesson__c fields regardless of Student_Sessions__c.Is_Archived__c |
| 4 | (Zoom Type = "Multiple" variant) Student A has a soft-deleted-but-not-archived Student Session for this lesson (Is_Deleted__c = TRUE, Is_Archived__c = FALSE) and reopens the cached detail screen | The per-student Zoom URL for this session still resolves and is shown, because getLesson()'s attendance subquery filters Is_Archived__c but omits Is_Deleted__c | getLesson() subquery (lines 560-567) missing Is_Deleted__c = FALSE, inconsistent with getLessonList/getLessonReportDetailFromStudentSession/getLessonReportMedias in the same class |

**Severity:** major
**Priority:** high

---
