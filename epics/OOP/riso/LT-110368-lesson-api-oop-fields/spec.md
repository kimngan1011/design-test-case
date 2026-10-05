---
ticket_id: LT-110368
ticket_url: https://manabie.atlassian.net/browse/LT-110368
title: Riso | Update Lesson API for Riso integration and handle OOP fields
module: scheduling
bucket: OOP/riso
status: in QA
internal_uat_date: null
production_release_date: null
last_updated: 2026-09-28
---

# LT-110368: Riso Lesson API — OOP fields and related-change sync

## Summary

Riso consumes Manabie's lesson feed through the read-only endpoint
`GET /services/apexrest/lessons-oop/v1`. This epic finalizes the payload fields
needed by JStaff and makes incremental sync reliable when a record related to a
Lesson changes.

The authoritative response timestamp remains:

```text
last_updated_at = MANAERP__Lesson__c.LastModifiedDate
```

`MANAERP__Lesson__c.Last_Related_Change__c` is an internal text field used by
the related-change tracker. It is **not** a response field and must not replace
`last_updated_at`. Updating it must result in the parent Lesson's Salesforce
`LastModifiedDate` changing, so the normal incremental API query returns that
Lesson.

**PRD:** [Riso | Lesson API — Finalized Fields (IF05 時間割情報)](https://manabie.atlassian.net/wiki/spaces/PRDM/pages/2725216271/Riso+Lesson+API+Finalized+Fields+IF05)

**Superseded reference:** [PBT-1501](https://manabie.atlassian.net/browse/PBT-1501) is Closed. LT-110368 is the active epic for the finalized API and OOP-field work.

---

## Acceptance Criteria

### AC-01 — Retrieve finalized lesson payload

Given a Riso integration caller supplies valid required filters, when it calls
`GET /services/apexrest/lessons-oop/v1`, then the API returns only Lessons in
the requested scope and each `data[]` item follows the finalized response
contract below.

### AC-02 — Support full and incremental lesson pulls

- `lesson_status`, `lesson_start_date`, `lesson_end_date`, and `location_id`
  are mandatory.
- `last_updated_since` is optional. When supplied, the API returns Lessons
  whose `SystemModstamp >= last_updated_since`.
- Pagination is cursor-based through `limitQuery` and `paging.next_pointer`.

### AC-03 — Map OOP fields safely

The Riso OOP fields (`TOMAS_JStaff_*`) are serialized as strings. If an OOP
field does not exist in the current org, its response value is `null`; the
endpoint must not fail or omit unrelated payload data.

### AC-04 — Surface related changes through the normal timestamp

For every operation in the change matrix below, the tracker updates the
associated Lesson's internal related-change field. As a result:

1. `Lesson__c.LastModifiedDate` advances;
2. the API returns that Lesson in a `last_updated_since` pull; and
3. `last_updated_at` equals the updated `Lesson__c.LastModifiedDate`, in ISO
   8601 UTC format.

The response must never expose `Last_Related_Change__c` as a substitute for
`last_updated_at`.

### AC-05 — Return the current related collections

The `teachers`, `classrooms`, and `students` arrays reflect the current active
related data after related-record lifecycle changes. In particular, `students`
includes only `Student_Sessions__c` records where both `Is_Deleted__c = false`
and `Is_Archived__c = false`.

---

## API Contract

### Endpoint and request parameters

| Parameter | Type | Required | Rule |
|---|---|---:|---|
| `lesson_status` | String | Yes | Comma-separated, case-insensitive values: `Draft`, `Published`, `Completed`, `Cancelled`. |
| `lesson_start_date` | Date (`YYYY-MM-DD`) | Yes | Compared with `Lesson__c.Start_Date_Time__c` in UTC. |
| `lesson_end_date` | Date (`YYYY-MM-DD`) | Yes | Inclusive and must be on or after `lesson_start_date`. |
| `location_id` | String | Yes | Lesson Schedule location's `Account.Partner_Internal_Id__c`. |
| `last_updated_since` | ISO 8601 UTC DateTime | No | Filter: `SystemModstamp >= last_updated_since`. |
| `limitQuery` | Integer | No | Default `200`; controls page size. |
| `next_pointer` | Salesforce Id | No | Value returned by the prior page's `paging.next_pointer`. |

### Response envelope

| Field | Type | Rule |
|---|---|---|
| `data` | Array of Lesson | One item per returned Lesson. |
| `paging.next_pointer` | String / `null` | Id of the last Lesson only when the page has exactly `limitQuery` records; otherwise `null`. |

All DateTimes use UTC `yyyy-MM-ddTHH:mm:ssZ`. The API returns `null` for a
field with no value. In the Riso org, every defined response key is returned,
including `compensation_ratio`.

### `data[]` — Lesson fields

| Response field | Type | Source / mapping |
|---|---|---|
| `lesson_schedule` | String | `Lesson__c.Lesson_Schedule__c` (Id) |
| `lesson_id` | String | `Lesson__c.Id` |
| `lesson_name` | String | `Lesson__c.Name` |
| `start_date` | DateTime | `Lesson__c.Start_Date_Time__c` |
| `end_date` | DateTime | `Lesson__c.End_Date_Time__c` |
| `timeslot.id` | String | `Lesson__c.Timeslot__c` (Id) |
| `subject` | String | `Lesson__c.Subject__r.Name` |
| `lesson_status` | String | `Lesson__c.Status__c` |
| `academic_year` | String | `Lesson__c.Academic_Year__c` |
| `day` | String | `Lesson__c.Day__c` |
| `course_id` | String | `Lesson_Schedule__c.Location_Course__r.Course_Master__c` (Id) |
| `location_id` | String | `Lesson_Schedule__c.Account__r.Partner_Internal_Id__c` |
| `teaching_medium` | String | `Lesson__c.Teaching_Medium__c` |
| `teaching_method` | String | `Lesson__c.Teaching_Method__c` |
| `cancellation_reason` | String | `Lesson__c.Cancellation_Reason__c` |
| `compensation_ratio` | String | `Lesson__c.Compensation_Ratio__c`; this field is always available in the Riso org. |
| `location_partner_id` | String | `Lesson__c.TOMAS_JStaff_KOU_CODE__c` |
| `timeslot_sequence` | String | `Lesson__c.TOMAS_JStaff_ZIGEN_CODE__c` |
| `subject_partner_id` | String | `Lesson__c.TOMAS_JStaff_ZIKANWARI_KAMOKU_CODE__c` |
| `day_of_week` | String | `Lesson__c.TOMAS_JStaff_YOUBI_CODE__c` |
| `course_partner_id` | String | All Lesson Schedule Classes' `Class__c.TOMAS_JStaff_G_BANGOU__c`, sorted and joined by `;`. |
| `created_at` | DateTime | `Lesson__c.CreatedDate` |
| `last_updated_at` | DateTime | **`Lesson__c.LastModifiedDate`** |
| `teachers` | Array | Current Lesson Teacher collection; see below. |
| `classrooms` | Array | Current Lesson Classroom collection; see below. |
| `students` | Array | Current eligible Student Session collection; see below. |

### Nested collection mappings

| Collection | Response field | Source |
|---|---|---|
| `teachers[]` | `teacher_id` | `Lesson_Teacher__c.Contact__r.Manabie_Id__c` |
|  | `name` | `Lesson_Teacher__c.Contact__r.Name` |
|  | `teacher_external_id` | `Lesson_Teacher__c.TOMAS_JStaff_KOUSI_BANGOU__c` |
| `classrooms[]` | `classroom_id` | `Lesson_Classroom__c.Classroom__c` (Id) |
|  | `name` | `Lesson_Classroom__c.Classroom__r.Name` |
| `students[]` | `student_id` | `Student_Sessions__c.Lesson_Allocation__r.Student__r.Manabie_Id__c` |
|  | `student_name` | `Student_Sessions__c.Lesson_Allocation__r.Student__r.Name` |
|  | `session_type` | `Student_Sessions__c.Session_Type__c` |
|  | `student_user_name` | `Student_Sessions__c.TOMAS_JStaff_SEITO_BANGOU__c` |
|  | `course_partner_id` | `Student_Sessions__c.TOMAS_JStaff_SYOUHIN_BUNRUI_CODE__c` |
|  | `lesson_division` | `Student_Sessions__c.TOMAS_JStaff_ZYUGYOU_KUBUN__c` |
|  | `grade_code` | `Student_Sessions__c.TOMAS_JStaff_GAKUNEN_CODE__c` |
|  | `attendance_status` | `Student_Sessions__c.TOMAS_JStaff_SYUSSEKI_KUBUN__c` |
|  | `slot_consumption` | `Student_Sessions__c.TOMAS_JStaff_KOMA_SYOUKA_KUBUN__c` |
|  | `payroll_occurrence_flag` | `Student_Sessions__c.TOMAS_JStaff_KYUUYOHASSEI_FLAG__c` |

---

## Related Lesson Change Tracking

### Implementation components (epic comment)

| Component | Purpose |
|---|---|
| `Lesson__c.Last_Related_Change__c` | Internal `Text(255)` field touched by the tracker; not part of the external API schema. |
| `LessonRelatedChangeTracker` | Shared Apex logic that resolves related lessons and updates the internal field. |
| `LessonRelatedChangeTrackerTest` | Apex tests for tracker behavior. |
| `Lesson_Related_Change_Access` | Permission Set for access to the custom field/implementation. |

### Related-object matrix

The following list is explicitly confirmed by the epic screenshot and comment.
Every trigger must handle **created, updated, and deleted** records. Restore
flows are out of scope for this epic.

| Related Lesson object | Salesforce object | Trigger | Expected API-visible effect |
|---|---|---|---|
| Lesson Teacher | `MANAERP__Lesson_Teacher__c` | `LessonTeacherRelatedChangeTrigger` | Parent Lesson timestamp advances; `teachers[]` reflects the active teacher set. |
| Lesson Classroom | `MANAERP__Lesson_Classroom__c` | `LessonClassroomRelatedChangeTrigger` | Parent Lesson timestamp advances; `classrooms[]` reflects the active classroom set. |
| Student Session | `MANAERP__Student_Sessions__c` | `StudentSessionRelatedChangeTrigger` | Parent Lesson timestamp advances; `students[]` respects active/non-archived eligibility. |
| Lesson Report | `MANAERP__Lesson_Report__c` | `LessonReportRelatedChangeTrigger` | Parent Lesson timestamp advances even though Lesson Report is not a direct response array. |
| Lesson Survey Response | `MANAERP__Lesson_Survey_Response__c` | `LessonSurveyResponseRelatedChangeTrigger` | Parent Lesson timestamp advances even though Survey Response is not a direct response array. |
| Lesson Schedule | `MANAERP__Lesson_Schedule__c` | `LessonScheduleRelatedChangeTrigger` | Every Lesson associated with the changed schedule must be eligible for the incremental pull. |
| Lesson Schedule Class | `MANAERP__Lesson_Schedule_Class__c` | `LessonScheduleClassRelatedChangeTrigger` | Every Lesson under the schedule must be eligible for the incremental pull; `course_partner_id` is recomputed from current classes. |

### Required lifecycle behaviour

For each matrix row and each lifecycle event:

1. Capture the Lesson's existing `LastModifiedDate` / API `last_updated_at`.
2. Create, modify, or delete the related record.
3. Confirm the tracker updates `Last_Related_Change__c` on every affected
   Lesson and that `Lesson__c.LastModifiedDate` is later than the baseline.
4. Call the API with a `last_updated_since` timestamp at or just before the
   baseline. The affected Lesson must be returned with
   `last_updated_at = Lesson__c.LastModifiedDate`.
5. Confirm the nested collection (where applicable) represents the post-event
   active state, not logically deleted or archived data.

For a schedule-level or schedule-class-level event, coverage must include a
schedule containing multiple Lessons. The change must not update only an
arbitrary one of those lesson instances.

---

## Business Rules

| ID | Rule |
|---|---|
| BR-01 | The endpoint is GET-only and read-only for Riso; it does not create, update, or delete Lesson data. |
| BR-02 | Required filters are `lesson_status`, `lesson_start_date`, `lesson_end_date`, and `location_id`; invalid/missing parameter or date format returns `400`. |
| BR-03 | `lesson_end_date` is inclusive and cannot precede `lesson_start_date`. |
| BR-04 | `lesson_status` is case-insensitive and supports only Draft, Published, Completed, and Cancelled; invalid values and invalid `limitQuery`/`next_pointer` return `422`. |
| BR-05 | Incremental selection uses `SystemModstamp >= last_updated_since`; the response value is still `Lesson__c.LastModifiedDate`. |
| BR-06 | `last_updated_at` maps exactly to `Lesson__c.LastModifiedDate`, including after a tracked related-record change. |
| BR-07 | Child-object create/update/delete must touch the associated Lesson via the tracker; the custom `Last_Related_Change__c` value itself is not exposed to Riso. |
| BR-08 | `students[]` excludes Student Sessions that are deleted or archived. |
| BR-09 | OOP fields serialize as String; Riso has the required OOP fields, including `Compensation_Ratio__c`. A field with no record value is returned as `null`. |
| BR-10 | `course_partner_id` is deterministic: all classes of the Lesson Schedule, sorted, semicolon-delimited. |
| BR-11 | A full page returns the last Lesson Id in `paging.next_pointer`; a non-full page returns `null`. |

---

## Scope and regression impact

### In scope

- Riso-only Lesson GET API response, filtering, pagination, and error contract.
- Mapping of Riso OOP fields in lesson-, teacher-, and student-level payloads.
- Incremental-sync visibility caused by direct Lesson changes and the seven
  confirmed related Lesson objects.
- Permission-set deployment needed for the related-change implementation.

### Out of scope

- Any API that mutates Lessons or related records.
- JStaff-side transformations, data reconciliation, or checkpoint storage.
- New UI for `Last_Related_Change__c`.
- Fields or related objects not in the confirmed seven-object matrix.

### Key regression paths

1. Lesson Schedule and Lesson Schedule Class changes affect shared schedule
   data and can fan out to many Lesson records.
2. Student Session exclusion rules must survive delete/archive and must not
   leak historical sessions to `students[]`.
3. A Riso record with an empty optional value must yield `null` without an API
   error or changes to core fields.
4. Cursor pagination combined with `last_updated_since` must neither lose nor
   duplicate affected Lessons at the time boundary.

---

## Conflict and gap analysis

| # | Type | Source | Finding / QA handling |
|---|---|---|---|
| 1 | Resolved | PRD + current epic comment | The PRD maps `last_updated_at` to `Lesson__c.LastModifiedDate`. The comment adds `Last_Related_Change__c`; treat it only as the parent-touch mechanism, never as the response source. |
| 2 | Test-critical | API comment | Filter field (`SystemModstamp`) differs from displayed field (`LastModifiedDate`). Assert both the incremental inclusion and exact response mapping for every tracked event. |
| 3 | Resolved | User clarification, 2026-09-28 | `Compensation_Ratio__c` always exists in Riso. Assert that the `compensation_ratio` key is always returned; its value may be `null` when the Lesson has no value. |
| 4 | Test-critical | Screenshot + epic comment | Schedule and Schedule Class are not one-to-one with a Lesson. Use a multi-lesson schedule to verify that related-change fan-out covers all associated Lessons. |
| 5 | Scope decision | User clarification, 2026-09-28 | Restore is out of scope. Do not create tracker or payload test cases for undelete / logical-restore behavior. |
| 6 | Open | API comment | API authentication/authorization behaviour is not stated in the current finalized comment. Reuse the existing Riso integration authentication contract; add 401/403 cases once its expected response is confirmed. |

---

## Test design handoff

The test-coverage phase should build suites around:

- request validation, inclusive date range, status filter, location filter, and
  pagination;
- full payload field mapping, null-value handling, and deterministic class-code
  aggregation;
- direct Lesson `LastModifiedDate` mapping;
- a `7 objects × 3 lifecycle events` tracker matrix, with separate direct-child
  collection assertions and schedule fan-out coverage;
- `last_updated_since` boundary and multi-page incremental-pull regression;
- Riso tenant isolation and permission-set deployment/access checks.

## Sources consulted

- LT-110368 description and all three epic comments (2026-09-10 and 2026-09-28).
- Riso Lesson API Finalized Fields PRD, version 7 (2026-09-07).
- Attached epic-comment screenshot, which confirms the seven related Lesson
  object types and four lifecycle operations.
- `knowledge/domain-knowledge/scheduling/lesson-management/{lesson,lesson-teacher,student-session,class-assignment}.md`.
