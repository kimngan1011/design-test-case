# Lesson Learned — Core Domain Issues

---

## [2026-04-13] Aso — Duplicate Student Sessions from Manual Assign + Auto Assign

**Slack thread:** https://manabie.slack.com/archives/C037409QQ4S/p1775610509175129

### Issue
Students were assigned to the same lesson multiple times, resulting in duplicate student session records.

**Root cause:**
A staff member performed **2 actions that both created student sessions for the same group of students**:
1. Used **"Add Student Sessions by Bulk"** (manual assignment)
2. Then **Imported Class Members** → system automatically auto-assigned student sessions

Both flows created student session records independently, generating **1,655 duplicate records** on 2026-04-07.

**Data:**
- Manually created by staff: 4,561 student sessions
- Auto-assigned by system: 35,522 student sessions
- Duplicates: **1,655**

### Resolution
- Deleted the **manually assigned** student sessions, kept the **auto-assigned** ones
- Total deleted: **1,809 records** (1,655 on 2026-04-07 + 154 on the day of resolution)

### Lessons Learned / Design Notes
- When **2 flows can both create student sessions** (bulk manual + auto-assign from class import), implement a **deduplication or duplicate-prevention** mechanism at the business logic layer.
- Check for existence before inserting a student session: if a session already exists for the same `(student, lesson)` pair, skip creation.
- Consider a **UI warning** when staff manually assigns a student who already has a session from auto-assign.

---

## [2026-06-18] Aso — Duplicate Students on Lesson Copy Due to Missing `Unique_Key__c` Backfill

**Slack thread:** https://manabie.slack.com/archives/C037409QQ4S/p1781748589810049

### Issue

After copying lessons in Aso Prod, students were found assigned twice to the same lesson. The bug was introduced by the June 15 release of the auto-assign-by-class-member flow.

**Root cause:**
1. The auto-assign flow uses `Unique_Key__c` (a composite key of Lesson ID + Student ID) to detect and skip duplicate enrollments.
2. Old student session records created before `Unique_Key__c` was introduced did not have this field populated.
3. When the auto-assign flow processed these legacy records, it could not detect the existing enrollment and inserted duplicate student sessions.

### Resolution

- Removed the duplicate student session records created on or after the June 15 release (Aso Prod data fix).
- Ran a backfill migration to populate `Unique_Key__c` on all legacy student session records across all partners (tracked in LT-104284).
- Reverted lesson surveys (lesson inquiries) that were inadvertently deleted when the duplicate enrollments were cleaned up.

### Lessons Learned / Design Notes

- When introducing a new deduplication key field, **backfill it for all existing records in the same release** — never assume old data has the field populated.
- The auto-assign flow should use a raw `(lesson_id, student_id)` existence check as a **fallback deduplication guard** for records where the composite key is missing, rather than relying solely on `Unique_Key__c`.
- Before running any data-cleanup script, **audit cascading dependencies** (e.g., lesson surveys, submissions) linked to the records being deleted to avoid unintended data loss.
- When a fix removes records across partners, ensure the migration scope covers **all partners**, not just the one that reported the issue.

---

## [2026-08-18] Renseikai — Published Lesson Missing Student Sessions Due to Salesforce 10,000-Record Bulk Write Limit

**Slack thread:** https://manabie.slack.com/archives/C02B6RYSD7A/p1787034274581849

### Issue

A bulk lesson-generation import (~1,300 lesson schedules across ~1,200 classes) created the lessons successfully, but the follow-up step that queues students for auto-assignment silently failed for one batch, leaving Published Lessons with zero Student Sessions despite having active Class Members. This blocked attendance tracking.

**Root cause:**
1. Lesson generation ran in batches; one batch processed 1,000 schedules and, at its last step, looked up every student enrolled across the corresponding ~1,200 classes (~9,000 students) to queue auto-assign rows.
2. That single operation attempted to write ~9,000 auto-assign queue rows plus 1,000 schedule rows = 10,001 records in one call, exceeding Salesforce's hard limit of 10,000 records per single write operation.
3. The write was rejected, but lesson creation (an earlier, already-committed step) was unaffected — so lessons existed with no student sessions, and the failure was not surfaced as an error to the importer.

**Data:**

- ~1,300 lesson schedules / ~1,200 classes in the source import
- 1,000 schedules processed in the failing batch
- ~9,000 students queued for auto-assign in that batch
- 10,001 total records attempted vs. Salesforce's 10,000-record-per-operation limit

### Resolution

- Reproduced the failure on preprod to confirm root cause.
- Re-ran auto-assign for all class members that were missed — a data fix only, no re-import needed.
- Follow-up work planned to improve the performance/batching of the auto-assign queueing step.

### Lessons Learned / Design Notes

- Any batch operation that writes to Salesforce must chunk its payload to stay under the 10,000-record-per-operation limit — size the chunk dynamically off the number of students to queue, not just the number of schedules/lessons, since the queue step scales with class enrollment.
- A step that depends on an earlier step's success (auto-assign depending on lesson creation) should fail loudly and be retryable/idempotent rather than leaving lessons in a partially-processed state with no student sessions and no visible error.
- Add monitoring/alerting for "lesson exists but has zero Student Sessions despite active Class Members" as a detectable data-integrity signal, so partial failures like this surface before a partner reports missing attendance tracking.

---

## [2026-08-19] Renseikai — Manually-Assigned Student Sessions Auto-Removed by Class-Assignment Re-Scan Logic

**Slack thread:** https://manabie.slack.com/archives/C02B6RYSD7A/p1787111883369399

### Issue

83 Student Sessions across 12 school-specific lessons were unexpectedly deleted between 18–19 Aug 2026, blocking attendance management. The lessons themselves remained active; only the student assignments were removed.

**Root cause:**
1. When a Lesson Allocation (LA) class member's duration is updated — or a class is added/removed on an overlapping lesson — the system triggers a re-auto-assign that re-scans not just which lessons to *assign*, but also which existing student sessions should be *removed*, treating them as "invalid" if they no longer match current class-assignment rules.
2. The re-scan does not distinguish sessions that were manually assigned by staff from ones the system auto-assigned, so manual assignments get swept up in the same cleanup.
3. Two distinct deletion patterns occurred from the same re-scan run:
   - Manually-assigned sessions in a lesson group **without a class** that falls within the class member's duration → incorrectly treated as invalid and removed (this is the actual bug).
   - Manually-assigned sessions in a lesson group **with a class**, where the lesson's class doesn't match the class member's duration → removed as well, but this is **correct** per the existing auto-assign design (confirmed with the partner, not reverted).

**Data:**

- 83 Student Sessions deleted across 12 lessons total (35 on 19 Aug, 48 on 23 Aug) as originally reported
- 916 records deleted from lesson groups without a class (Type 1 — the bug)
- 3,333 records deleted from lesson groups with a mismatched class (Type 2 — correct/intended behavior)

### Resolution

- Reverted the 916 Type-1 records (manually assigned sessions in class-less lesson groups).
- Did not revert the 3,333 Type-2 records — confirmed by the requester as expected auto-assign behavior.
- Filed bug ticket [LT-109020](https://manabie.atlassian.net/browse/LT-109020) — "[SF] Auto-remove assigned student from the group lesson without class when triggering class assignment flow" — for the Type-1 bug.
- An existing improvement ticket, [LT-107584](https://manabie.atlassian.net/browse/LT-107584), already planned for the Sep release, will exclude intentional manual assignments from the system's re-scan/removal logic more broadly.

### Lessons Learned / Design Notes

- The auto-assign re-scan/cleanup logic must distinguish manually-assigned student sessions from auto-assigned ones before removing "invalid" lessons — a manual assignment reflects explicit staff intent and shouldn't be silently deleted by a background re-scan.
- Any update to a class member's duration, or adding/removing a class on an overlapping lesson, can silently trigger this re-scan and delete existing student sessions — this side effect is not obvious from the triggering action and should be called out (and ideally require confirmation) wherever such updates are made.
- Even where auto-removal is by-design (class-mismatch case), deletions are user-visible and partner-impacting — communicate the behavior to partners proactively rather than only after an incident is raised.

---

## [2026-09-21] Cross-Domain — Incident Prevention Patterns for Event, Calendar, Live Lesson, and Lesson-Learn Flows

**Slack thread:** https://manabiebiz.slack.com/archives/C0BPM7GABDW

### Issue

Historical JP incidents show repeated escape patterns across event booking, lesson calendar, live lesson, and lesson-learn data flows. Existing Incident Prevention coverage was present but narrow: only 16 cases existed under Qase suite 2183 and most gaps were around integrated, operationally realistic flows.

**Root cause:**
1. Test coverage was split by feature area, while incidents often crossed systems: Salesforce calendar, BO, Learner App, Zoom/Agora, booking, class/course/location sync, and background jobs.
2. Several failures were not pure UI bugs; they were data integrity, idempotency, batching, configuration, feature flag, timezone, provider SDK, or environment-parity problems.
3. Existing prevention cases did not consistently assert downstream records, retries, duplicate prevention, or monitoring signals after the visible user action.

### Resolution

- Added new Incident Prevention test design artifacts for event/calendar/live lesson/lesson-learn themes.
- Added Qase cases under the Incident Prevention suite to cover gaps not represented by existing cases.
- Kept existing case IDs as impacted coverage rather than duplicating them.

### Lessons Learned / Design Notes

- Incident-prevention cases should validate the full chain: user action, source object, downstream record, mobile/BO visibility, retry/idempotency, and monitoring signal.
- Calendar and lesson tests must include generated/imported lessons, recurring edits, location/timezone boundaries, class-member assignment, Student Session integrity, and Lesson Allocation side effects.
- Event booking tests must include enabled/disabled org configuration, internal vs external booking, search/list limits, target segment filtering, direct booking links, and participant idempotency under account switching/concurrency.
- Live lesson tests must include provider token refresh, shared device/session behavior, reconnect, tab switch, whiteboard/poll latency, Zoom one-way sync, and SDK upgrade smoke coverage.
- Lesson-learn tests must include large-course batching, duplicate/empty study plan item prevention, CSV update behavior, multi-tab learning time, stale session caps, and data checkers.

---

## [2026-09-29] Core — Teacher List Filter Fails Silently When Subject + Location + Working Time Are Combined (SOQL 2 Semi-Join Limit)

**Jira:** [LT-107834](https://manabie.atlassian.net/browse/LT-107834) (related: [LT-107836](https://manabie.atlassian.net/browse/LT-107836), fix commit `9deddb4` in erp-salesforce)

### Issue

In the SF Lesson Calendar 7-Day Teacher Schedule View, the selected teacher count dropped to 0 and the calendar exited back to the standard view. It only happened when the Teacher List filter had **Subject, Location and Working time applied together**. In every other view the same filter just showed an **empty Teacher List with no error message**, so the bug looked like "no teacher matches" and was only noticed because the 7-Day View exits when the count is not 1.

**Root cause:**
1. *(Confirmed by dev — Long, 2026-09-29)* With these 3 filters the teacher list API `LessonMasterHandler.getAssignTeacher` returns an error, so no new teacher list is loaded and the selected teacher count drops to 0.
2. *(From reading the Apex code — not yet confirmed from a debug log)* Each of the 3 filters adds a **semi-join sub-query** to the same `WHERE` clause:
   - Location → `Id IN (SELECT Contact__c FROM Affiliation__c …)`
   - Subject → `Id IN (SELECT Contact__c FROM Eligible_Subject__c …)`
   - Working time → `Id IN (SELECT Staff__c FROM Working_Hour__c …)`

   **SOQL allows at most 2 semi-join (`IN (SELECT …)` / `NOT IN (SELECT …)`) sub-queries per `WHERE` clause**; the 3rd makes the query fail (expected message: *"Maximum 2 semi join sub-selects are allowed"*).
3. The bug depends on org configuration:
   - When **Restrict Teacher Match All Subjects** (`MANAERP__Lesson_Custom_Settings__c.MANAERP__Restrict_Teacher_Match_All_Subjects__c`, org default) is ON, the Subject filter binds a pre-computed ID list (`Id IN :eligibleTeacherIds`) instead of a sub-query → only 2 semi-joins → no error.
   - When the **Lesson_Staff_Working_Hour** feature flag is OFF, the Working time filter does not exist → no error.
4. The LWC `listTeacherCalendar` handles the API error with only `console.warn`, clears the list and does not re-add the selected (pinned) teacher, so the failure is invisible in the UI.

### Resolution

- LT-107836 fix (`9deddb4`) makes the LWC ignore empty selection events while re-syncing the selection; it does not fix the Apex query.
- LT-107834 is still In Progress. Expected fix: run one or more of the sub-queries first in Apex and bind the resulting ID set (as the Subject filter already does when the setting is ON), so the main query keeps at most 2 semi-joins; and show an error to the user when the API fails.
- Qase: PX-25846 (precondition: 3 filters + setting OFF + flag ON) and new PX-29120 (Teacher List 3-filter case that checks the `getAssignTeacher` response state in DevTools).

### Lessons Learned / Design Notes

- **Any filter panel that builds one SOQL query from several optional filters** can hit the 2-semi-join limit only when a specific combination is applied. Test the combination of all sub-query-based filters together, not each filter alone.
- **Same limit applies to Salesforce GraphQL** (`inq` / `ninq` = semi-join / anti-join). Found again on 2026-09-29: [LT-111933](https://manabie.atlassian.net/browse/LT-111933) Aver Lesson Report list (a default `inq` + student search + Teacher) and [LT-111934](https://manabie.atlassian.net/browse/LT-111934) Lesson List for Aver (student search + Teacher Name + Report Status). GraphQL returns HTTP 200 with an `errors` array (`DataFetchingException`, generic "We couldn't find the record…" message) — check the response body, not the status code.
- **Silent API errors hide bugs.** An empty result list can mean "no match" or "the API failed". For filter/search features, QA must check the API response in DevTools (Aura `actions[0].state` = `SUCCESS` vs `ERROR`), not only the UI. Ask dev to surface API errors as a toast instead of `console.warn`.
- **Feature settings change the query shape.** Record which org setting / feature flag each filter depends on (here: Restrict Teacher Match All Subjects, Lesson_Staff_Working_Hour) and put the required values in test case preconditions; otherwise the bug "does not reproduce" on orgs with a different setting.
- Other Salesforce governor limits worth keeping in mind for filter/list features: 10,000 records per DML operation (see 2026-08-18 entry), 50,000 query rows per transaction, 100 SOQL queries per synchronous transaction.

---

## [2026-09-29] Core — Calendar Grid May Hit the 50,000 Query-Row Limit on Monthly View (Untested Risk)

**Source:** Code review of `LessonCalendarHandler` (erp-salesforce `develop`, 2026-09-29) — not a production incident yet. **Not covered by any test so far.**

### Issue

The SF and BO calendar grid load lessons through `/LessonCalendar/v1/retrieveV2` → `LessonCalendarHandler.getLessonsCalendarDeserializeV3`. Salesforce allows **50,000 query rows per transaction** (`Too many query rows: 50001` is a `LimitException` and cannot be caught). Dense orgs on Monthly view with Grade / Course / Student filters can approach this limit.

**Why (from code):**
1. Filters Grade, Course and Student first query `Student_Sessions__c` in the date range to get lesson IDs. This pre-query is limited by date only — **not by location** — so it scans the whole org's student sessions for the month.
2. The main lesson query uses `LIMIT (50,000 − rows already used)`, which protects the **lesson rows only**. Its child sub-queries (`Lesson_Teachers__r`, `Lesson_Classrooms__r`, `Student_Sessions__r`) also count toward the 50,000 rows but are not reserved. Example: 8,000 lessons × 6 student sessions ≈ 56,000 rows → `LimitException` → API error → empty calendar.
3. When the lesson rows alone exceed the remaining limit, the extra lessons are **dropped silently** (no message).
4. BO splits a range longer than 2 days into 2 requests (`chunkRequest`), which halves the risk on BO but not on SF calendar.

### Resolution

- None yet. Needs a data-volume test on an org with the largest lesson / student-session volume (per month) before closing.

### Lessons Learned / Design Notes

- Test the calendar grid with **Monthly view + dense location(s)**, and with **Grade / Course / Student filters**, on a production-like data volume. Check: no API error, lesson count on the grid equals the count from a report/SOQL for the same range.
- Count rows as **parents + all child sub-query rows + pre-query rows**; a `LIMIT` on the parent query is not enough.
- Pre-queries used to build ID lists should be limited by the same location as the main query when possible.
- When a result is truncated by a limit, the UI should say so instead of silently showing fewer records.
- Related: the Teacher List SOQL semi-join limit (LT-107834, entry above) — same family of "filter combination / data volume hits a Salesforce limit and the UI hides it".

---

## [2026-09-29] Core — BO Lesson List Filter Chain: Location → Course → Class (Behavior Differs From the Original Spec)

**Source:** Code review of school-portal-admin `develop` (2026-09-25) while reproducing LT-111934; original spec [Lesson | Group Teaching Lesson – US 06](https://manabie.atlassian.net/wiki/spaces/LT/pages/427033765).

### Issue

While trying to combine the Class filter with other filters on BO Lesson Management > Lesson List, QA could not select a Class and could not find a Course by name. The fields depend on each other, and this dependency is only in code, not in the spec.

**Current behavior (from code):**
1. **Course needs Location first.** `useLocationCourseAutocompleteSF` only queries when at least one Location is selected (`isEnabledQuery = arrayHasItem(location_ids)`). With no Location, the Course list is always empty, whatever name is typed. With Location(s), Course is searched by name (`Name like %text%`) among the courses of those locations (`Location_Course__c`).
2. **Class needs Course first.** `FilterLessonListSF` passes `isDisabledClassIfNoCourse={!arrayHasItem(watchingCourses)}` → the Class field is disabled until a Course is selected (since LT-51751, Lesson List V2 SF UI, 2024-03). Class options are limited to the selected course(s) and location(s) (LT-73401 fixed duplicate classes).
3. **Teacher Name has a default.** The logged-in user is pre-filled as Teacher Name unless feature setting `lesson.remove_default_teacher_filter.is_enabled` is on — so the Teacher semi-join is often already active when the page opens.

**Original spec (US 06, AC 06.1)** says: if no Course is selected, the Class filter shows **all classes**; if a Course is selected, only its classes; changing/deleting the Course resets the Class. It does not require Location before Course. AC 06.2: all filters are combined with AND.

### Resolution

- Not a confirmed bug: the current Location → Course → Class chain is not documented anywhere. **Needs PO confirmation** whether it is the intended ERPv2 SF behavior or a deviation from the spec.

### Lessons Learned / Design Notes

- To test Class-related filters on Lesson List (and Lesson Report, which uses the same `isDisabledClassIfNoCourse`), always select **Location → Course → Class** in that order; write test data and preconditions in this order.
- "Search by name returns nothing" can be a **disabled query**, not a search bug — check whether a parent filter must be selected first.
- Remember the default Teacher Name when counting filter combinations (e.g. semi-join limit: Teacher + Class + student search = 3 on Lesson List, see LT-111934 and the semi-join entries above).
- When code behavior and the spec differ, record both and get a PO decision before writing expected results.

---
## [2026-09-29] Core — Infinite-Scroll / Paged Lists Stop at ~2,000 Rows (SOQL OFFSET Limit), Search Is the Workaround

**Source:** Code review of event / lesson report list APIs (erp-salesforce `develop` 2026-09-29, school-portal-admin `develop` 2026-09-25). The limit is **known and accepted by the team**; this entry records the exact behavior so it is tested, not rediscovered.

### Issue

SOQL `OFFSET` cannot be greater than **2,000** (`NUMBER_OUTSIDE_VALID_RANGE`). Lists that page with `LIMIT … OFFSET (page × size)` cannot load records beyond that point:

| Screen | Page size | Last rows that load | What the user sees after that |
|---|---|---|---|
| Add Master Participant (`addEventParticipantExt` → `EventParticipantHandler.getTargetParticipants`) | 50 | ~2,050 | scrolling just stops (error only in console) |
| Add Master Staff (`addEventStaffExt` → `EventStaffHandler.getStaffByFilter`) | 50 | ~2,050 | scrolling just stops |
| Assign Staff to Activity Event (`addEventStaffOnAssignEvent` → `getEventStaffOnAssignEvent`) | 100 | ~2,100 | scrolling just stops |
| Assign Participant to Activity Event (`addEventParticipantOnAssignEvent` → `getEventParticipantFilters`) | 100 | ~2,100 | code caps at `offset <= 2000` but one page late: the request at offset 2,100 still fails silently |
| Aver Lesson Report List, V1 (Unleash `Lesson_BackOffice_LessonSF_AllowViewLessonOtherLocations` OFF) | 25 | row 2,025 | pages starting after row 2,025 show "Unable to load data"; total count is not capped |
| Change Lesson popup from lesson detail on SF calendar (`modalChangeLessonInLessonCalendar` → `LessonHandler.getReallocateLessonList`) | 20 | ~2,020 | scrolling just stops |
| Reallocate to new lesson popup (`modalNewReallocateLesson` → `getReallocateLessonList`) | set by parent | ~2,000 | scrolling just stops |
| Add Student popup on Lesson Detail (`modalNewStudentSession` → `LessonAllocationHandler.getLessonAllocationListByLessonInfo`) | 20 | ~2,020 | scrolling just stops |

**Workaround / accepted behavior:** the search box is applied in the query **before** `LIMIT/OFFSET`, so searching by name returns a record even if it is beyond row 2,000 in the unfiltered list.

Lists that are **not** affected: cursor-paged lists (Aver Lesson Report V2 via GraphQL `after`, Booking System Event Master API `Id > nextPointer`) and lists with a fixed first page only (SF calendar Teacher / Student List, first 200 rows by design).

### Resolution

- Accepted limitation. Test cases PX-29124 (Add Master Participant), PX-29125 (Add Master Staff), PX-29126 (Assign Staff to Event), PX-29127 (Assign to Event students), PX-29128 (Aver Lesson Report V1), PX-29132 (Change Lesson popup), PX-29133 (Reallocate popup), PX-29134 (Add Student popup) confirm that search reaches records beyond row 2,000.
- Not covered on purpose: Available Events table on the Student record (50 per page, no search box; a student is not expected to have > 2,050 available Event Masters), Mark Attendance participant list and Product Offering lookup (per-event / per-product volumes far below 2,000), learner-side event / lesson lists (`ActivityEventHandlerOutside.getCalendarActivityEvents`, `LessonDataHandlerOutSide.getLessonList` — one student's data in a date range).

### Lessons Learned / Design Notes

- For any paged list backed by SOQL `OFFSET`, test with **more than 2,000 matching records**: (1) note where loading stops, (2) search by the name of a record that is not loaded and confirm it is returned.
- Silent stop is the risky part: the error is only logged with `console.warn`. If the limit is ever not accepted, the fix is cursor/keyset pagination (`WHERE Name > :lastName` / `Id > :lastId`) or a visible "refine your search" message when the offset would exceed 2,000.
- Off-by-one guards: a cap must check `offset + pageSize <= 2000` for the **next** request, not the current one.

---
