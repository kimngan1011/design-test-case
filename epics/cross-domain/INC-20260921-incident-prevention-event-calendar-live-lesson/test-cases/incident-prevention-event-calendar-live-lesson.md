# Test Cases: Incident Prevention - Event, Calendar, Live Lesson, Lesson-Learn

## Qase Suite

`Incident Prevention - Event Calendar Live Lesson Lesson-Learn` (`suite_id=3569`) under parent suite `Incident Prevention` (`suite_id=2183`).

Created Qase cases: `PX-28764` through `PX-28777`.

## Cases

### [Incident Prevention] Live Lesson - Provider token refresh before starting from Calendar or BO

**Description:** Prevent expired Salesforce/custom/provider token from blocking Teacher Web or Live Lesson entry.

**Preconditions:**
- Staff user can open SF Calendar and BO Lesson Detail.
- Online lesson exists with valid teacher, students, teaching medium, and live lesson provider config.
- Test setup can simulate or prepare an expired/near-expired session token.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open the online lesson from SF Calendar and click Start Lesson. | User is redirected to the live lesson room without `INVALID_SESSION_ID`, blank page, or infinite loading. | lesson = online |
| 2 | Repeat the start action from BO Lesson Detail. | BO path also refreshes token and enters the same lesson room successfully. | entry = BO |
| 3 | Keep session idle until token is near expiry, then start the lesson again. | Token is refreshed before use; no manual app restart is required. | session = near_expiry |
| 4 | Check logs/monitoring for the start action. | Token refresh and room join are logged; failures are visible as alerts or searchable logs. | monitor = token_refresh |

### [Incident Prevention] Live Lesson - Reconnect and shared-session stability

**Description:** Prevent join-state loss after network interruption, browser refresh, tab switch, or shared device/session.

**Preconditions:**
- Published online lesson exists with teacher and at least two students.
- Teacher and student can join from supported browser/device combinations.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Teacher starts lesson and two students join. | All participants appear in the room; lesson remains active. | participants = teacher+2_students |
| 2 | Disconnect one student network for 30 seconds, reconnect, and rejoin. | Student can rejoin without requiring lesson recreation; attendance/join state is not duplicated. | network = temporary_disconnect |
| 3 | Switch browser tab/app away and back during the lesson. | Audio/video/join state remains active or recovers automatically. | action = tab_switch |
| 4 | Log out one shared device account, log in as another teacher, and start a different online lesson. | Teacher identity and lesson room are not reused from the previous session. | device = shared |

### [Incident Prevention] Live Lesson - Whiteboard, poll, pen, and text latency guard

**Description:** Prevent class-blocking latency or broken whiteboard actions during operational live lesson flow.

**Preconditions:**
- Online lesson supports whiteboard/material sharing, poll, pen, text, undo, and redo.
- At least one teacher and five students can join the room.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Teacher shares a PDF/material and moves between pages. | Page movement appears for students within acceptable latency; no blank/sunk page. | material = PDF |
| 2 | Teacher draws with pen, types text, and uses undo/redo. | Each action is visible to students; undo/redo affects the teacher's own annotation correctly. | tools = pen,text,undo,redo |
| 3 | Run a poll and close it. | Student poll ribbon updates correctly; no stale poll remains after the teacher closes it. | feature = poll |
| 4 | Repeat on one lower-spec supported device and one desktop browser. | Behavior stays within supported-device expectation; unsupported-device gaps are documented. | devices = desktop+tablet |

### [Incident Prevention] Zoom - One-way sync, regeneration, and stale link handling

**Description:** Prevent stale Zoom link after lesson edit/delete or Zoom-side changes.

**Preconditions:**
- Online lesson with Zoom integration exists.
- Zoom owner is assigned and Zoom link is generated.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Edit lesson date/time in SF and regenerate Zoom link. | New Zoom meeting reflects updated date/time; SF, BO, and Learner App show the same link. | action = edit_time |
| 2 | Delete/cancel the lesson in SF. | Manabie lesson state changes correctly; any remaining Zoom-side meeting behavior is documented and does not show as an active Manabie lesson. | action = delete_lesson |
| 3 | Delete or edit the meeting directly in Zoom. | Manabie does not silently assume bidirectional sync; starting stale link shows clear error/recovery guidance. | action = zoom_side_change |
| 4 | Start Zoom from BO and Learner App. | Both paths use the current valid link or show the same controlled error. | entry = BO+App |

### [Incident Prevention] Calendar Lesson - Published/imported lesson has Student Sessions

**Description:** Prevent lessons being created or published without Student Sessions despite active Class Members.

**Preconditions:**
- Class has active Class Members.
- Lesson import/generation or publish flow is available.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Generate or import lessons for a class with active members. | Lessons are created with expected status and schedule data. | class_members = active |
| 2 | Publish the created lessons. | Student Sessions are created for every eligible active class member. | status = Published |
| 3 | Open SF Calendar, BO Lesson Detail, and attendance/report entry. | Same student list appears across surfaces; attendance can be collected. | surfaces = SF,BO |
| 4 | Check data checker/monitor for zero-session lessons. | No Published lesson with active Class Members and zero Student Sessions is left unalerted. | monitor = zero_student_session |

### [Incident Prevention] Calendar Lesson - Lesson Allocation lifecycle does not mislink or silently remove sessions

**Description:** Prevent LA/order lifecycle actions from leaving wrong LA linkage, wrong total sessions, or unexpected session deletion.

**Preconditions:**
- Student has active Lesson Allocation and linked Student Sessions.
- Staff can perform order lifecycle actions: cancel, void, update slot/duration, change course.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Create a lesson linked to the student's current LA. | Student Session contains the correct LA reference and consumed-session basis. | LA = active |
| 2 | Perform update slot/duration or change associated course. | Only sessions outside the valid range are removed or relinked according to business rules. | action = update_duration |
| 3 | Perform cancel/void order scenario. | LA/session counts are recalculated correctly; financial/point impact is not lost. | action = cancel_or_void |
| 4 | Review SF Calendar, BO Lesson Detail, and report/attendance data. | No manually assigned session is silently deleted unless explicitly intended and auditable. | audit = session_source |

### [Incident Prevention] Calendar Lesson - Location, report publish, and student-session consistency

**Description:** Prevent missing Main Location, mismatched report data, or blank Student Session after lesson/report publish and student re-add.

**Preconditions:**
- Published lesson exists with location, teacher, student, and lesson report.
- Staff can remove/re-add student and publish lesson report.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Publish lesson report for a lesson shown on calendar. | Report and calendar event keep Main Location and student-session linkage. | status = report_published |
| 2 | Remove a student, save report, then re-add the same student. | Student Session is recreated/linked with nonblank report detail state. | action = remove_readd_student |
| 3 | Reopen BO Lesson Detail and SF Calendar lesson drawer. | Student, attendance, report, and location values are consistent. | surfaces = SF,BO |
| 4 | Run data checker for mismatch records. | Any mismatch is reported with lesson/student/report IDs for recovery. | checker = report_session_mismatch |

### [Incident Prevention] Calendar Lesson - Recurring/full-year import duplicate and partial-failure guard

**Description:** Prevent duplicate lessons or partial schedule creation during recurring lesson edits and full-year imports.

**Preconditions:**
- Full-year or large recurring lesson import data is prepared.
- Staff can edit recurring lessons with Only this / This and following.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Import or generate a large recurring lesson set. | All valid lessons are created once; no duplicate lesson codes or duplicate schedule rows. | import = full_year |
| 2 | Edit one lesson with This and following. | Future lessons are updated once and keep expected lesson code behavior. | edit = this_and_following |
| 3 | Remove a student assignment and repeat import/edit. | Removed assignment is not recreated unless the source rule explicitly requires it. | action = remove_assignment |
| 4 | Force a partial failure or retry the import. | Retry is idempotent; partial failures are visible and recoverable. | retry = import_retry |

### [Incident Prevention] Event Booking - Org config, internal/external route, and direct link matrix

**Description:** Prevent booking behavior from diverging by org configuration or entry route.

**Preconditions:**
- One org has Event enabled; one org has Event disabled or does not use Event.
- Event Master has target segment, booking settings, internal booking path, and external direct link.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open booking from an Event-enabled org as eligible student/parent. | Eligible event appears and can be booked according to target segment rules. | org = event_enabled |
| 2 | Open booking from an org where Event is disabled/not used. | No broken booking link or unexpected event UI appears. | org = event_disabled |
| 3 | Book via internal staff path. | Participant records are created once and visible in Event Master/Activity Event. | route = internal |
| 4 | Book via external/direct link. | Documented direct-link eligibility behavior is preserved; no unintended target-segment bypass beyond spec. | route = external_direct |

### [Incident Prevention] Event Booking - Search/list limit and target segment query scale

**Description:** Prevent valid students/events from being hidden by pagination, 100-record UI limit, or aggregate query limits.

**Preconditions:**
- Event Master has more than 100 eligible candidates or participant records.
- Target segment includes location, grade, school, and course filters.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open booking/search modal with more than 100 possible records. | Search queries all eligible data, not only records currently displayed. | records = 100_plus |
| 2 | Search for a candidate not in the first displayed page. | Candidate appears and can be selected/booked if eligible. | candidate = page_2_or_later |
| 3 | Apply target segment filters with large data volume. | Query completes without aggregate/too-many-row failure and returns correct eligible list. | segment = large |
| 4 | Compare Event Master participant, Activity Event participant, and booking UI. | Counts and records stay consistent after booking. | verify = participant_records |

### [Incident Prevention] Event Booking - Participant idempotency under account switching and concurrency

**Description:** Expand existing participant-duplication prevention to cover account switch and concurrent booking.

**Preconditions:**
- Parent has multiple linked students.
- Event has limited capacity and is bookable by the students.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Parent books event for Student A, switches account/student, then returns to Student A. | Only one Event Participant exists for Student A. | switch = parent_student |
| 2 | Student account books the same event while parent account is open. | Duplicate participant creation is blocked idempotently. | users = parent+student |
| 3 | Two sessions reserve the last available slot at nearly the same time. | Only one reservation succeeds; loser sees clear capacity/full message. | concurrency = last_slot |
| 4 | Refresh Activity Event and Event Master records. | Participant count and capacity are correct with no duplicate rows. | verify = capacity |

### [Incident Prevention] Lesson-Learn - Large course study plan update is batched and idempotent

**Description:** Prevent large course study plan updates from timing out or creating duplicate/empty Study Plan Items.

**Preconditions:**
- Course has at least 400 students or enough data to exercise batching.
- Course study plan CSV/update path is available.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Upload or update course study plan for the large course. | Processing is batched and completes without request timeout. | course_size = large |
| 2 | Re-run the same update. | Existing Study Plan Items are updated idempotently; no duplicate rows are created. | retry = same_csv |
| 3 | Add students with empty individual study plans and update from course study plan. | Empty individual study plans receive expected items. | students = empty_study_plan |
| 4 | Check Learner App and Teacher Web. | Items, order, visibility, and teacher progress view are consistent. | surfaces = Learner+TW |

### [Incident Prevention] Lesson-Learn - Multi-tab learning time and stale session guard

**Description:** Prevent incorrect learning time from multi-tab, pause/resume, idle, or stale sessions.

**Preconditions:**
- Student can open Learner Web/App and access at least two LOs.
- Learning time is visible in teacher/parent/report surfaces.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Open LO A, then open LO B in another tab/session. | Only the active learning tab/session accumulates learning time. | tabs = two |
| 2 | Leave LO A idle for an extended period, then return and complete it. | Idle/stale time is capped or excluded according to product rule. | session = stale |
| 3 | Trigger pause/resume by backgrounding app or switching tabs. | Pause/resume events are handled; no overnight/24h learning time is recorded. | event = pause_resume |
| 4 | Check teacher/parent/report surfaces. | Displayed learning time is consistent and any anomaly is detectable by data checker. | verify = learning_time |

### [Incident Prevention] Release and Config - Feature flag, hotfix, job, and provider SDK guard

**Description:** Prevent release/config changes from breaking event/calendar/live lesson operations.

**Preconditions:**
- Release candidate or hotfix includes event, calendar, live lesson, provider SDK, feature flag, or background job changes.
- UAT/staging and PROD flag/config snapshots are available.

| Step | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | Compare UAT/staging and PROD feature flags/custom settings for the affected features. | Required flags are aligned or documented with explicit rollout plan. | flags = pre_release |
| 2 | Run smoke paths for event booking, SF Calendar lesson list/detail, and live lesson start. | Critical operations still work after deployment/hotfix. | smoke = event_calendar_live |
| 3 | Verify background jobs/platform events/provider integrations after deployment. | Jobs/events are running; provider SDK/API health is confirmed. | monitor = jobs_provider |
| 4 | Confirm rollback/disable path. | Team can disable feature safely without leaving partial data or hidden broken UI. | rollback = ready |
