# Test Cases: LT-110368 — Riso Lesson API OOP Fields and Related Change Sync

## Suite: [Riso] Get Lesson API – OOP Fields & Related Change Sync

### [Riso] Lesson Retrieval – Populated Lesson – Finalized Response – All Values Match Source Data

**Description:** AC-01 — Component — A populated Lesson returns the complete finalized lesson, teacher, classroom, student, and Riso information.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- A published Riso Lesson exists on `2026-10-05` at location `RISO_LOC_001` with known core fields, compensation ratio, location partner ID, timeslot sequence, subject partner ID, day-of-week code, one teacher, one classroom, and one active student session.
- The Lesson has three configured schedule classes with partner codes `C10`, `C02`, and `C05`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The Riso integration caller requests published lessons for the Lesson date and location. | The response returns HTTP `200` and contains the target Lesson once. | `lesson_status = Published; lesson_start_date = 2026-10-05; lesson_end_date = 2026-10-05; location_id = RISO_LOC_001` |
| 2 | The Riso integration caller compares the returned Lesson details with the Salesforce Lesson and schedule. | Identity, date/time, status, course, location, teaching, cancellation, created, and modified values match; compensation ratio, location partner ID, timeslot sequence, subject partner ID, day-of-week code, and sorted course partner codes also match their configured sources. | `lesson = L-API-01; expected_lesson_oop_fields = compensation_ratio,location_partner_id,timeslot_sequence,subject_partner_id,day_of_week,course_partner_id` |
| 3 | The Riso integration caller compares the returned teacher, classroom, and student collections with active related records. | The teacher contains its external ID; the student contains user name, course partner ID, lesson division, grade code, attendance status, slot consumption, and payroll occurrence flag; classroom identifier and name also match. | `teacher_count = 1; classroom_count = 1; active_student_count = 1; expected_teacher_oop_field = teacher_external_id; expected_student_oop_fields = student_user_name,course_partner_id,lesson_division,grade_code,attendance_status,slot_consumption,payroll_occurrence_flag` |

**Severity:** major  
**Priority:** high

---

### [Riso] Lesson Retrieval – Compensation Ratio – Populated Value – Key and Value Are Returned

**Description:** AC-01 — Decision Table — A populated compensation ratio remains present and unchanged in the Riso response.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-COMP-01` has compensation ratio `1.25`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The Riso integration caller requests the Lesson for its date and location. | The response returns HTTP `200` with Lesson `L-COMP-01`. | `lesson_date = 2026-10-06; location_id = RISO_LOC_001` |
| 2 | The Riso integration caller inspects the compensation ratio in the returned Lesson. | The compensation ratio key is present and its value is `1.25`. | `expected_compensation_ratio = 1.25` |

**Severity:** major  
**Priority:** high

---

### [Riso] Lesson Retrieval – Compensation Ratio – Empty Value – Key Is Returned as Null

**Description:** AC-01 — Decision Table — The Riso response retains the compensation-ratio key when the Lesson has no value.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-COMP-02` has no compensation-ratio value.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The Riso integration caller requests the Lesson for its date and location. | The response returns HTTP `200` with Lesson `L-COMP-02`. | `lesson_date = 2026-10-07; location_id = RISO_LOC_001` |
| 2 | The Riso integration caller inspects the compensation ratio in the returned Lesson. | The compensation ratio key is present and its value is `null`; no response error occurs. | `expected_compensation_ratio = null` |

**Severity:** major  
**Priority:** high

---

### [Riso] Lesson Retrieval – Optional Riso Value – Empty Source Value – Key Is Returned as Null

**Description:** AC-03 — Decision Table — An empty configured Riso field does not omit its key or fail the response.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-OOP-NULL-01` has no timeslot-sequence value and has all other required data.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The Riso integration caller requests the Lesson for its date and location. | The response returns HTTP `200` with Lesson `L-OOP-NULL-01`. | `lesson_date = 2026-10-08; location_id = RISO_LOC_001` |
| 2 | The Riso integration caller inspects the returned optional Riso values. | The timeslot-sequence key is present with `null`; populated fields remain unchanged. | `expected_timeslot_sequence = null` |

**Severity:** major  
**Priority:** high

---

### [Riso] Lesson Retrieval – Schedule Classes – Unordered Source Records – Partner Codes Are Sorted and Delimited

**Description:** AC-01 — Scenario — Class partner codes are deterministically sorted before they are joined.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-CLASS-01` belongs to one schedule with class partner codes created in order `C10`, `C02`, `C05`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The Riso integration caller requests the Lesson for its date and location. | The response returns HTTP `200` with Lesson `L-CLASS-01`. | `lesson_date = 2026-10-09; location_id = RISO_LOC_001` |
| 2 | The Riso integration caller inspects the returned course partner codes. | The value is `C02;C05;C10`, with one semicolon between sorted codes. | `source_order = C10,C02,C05; expected_order = C02;C05;C10` |

**Severity:** major  
**Priority:** high

---

### [Riso] Lesson Retrieval – Timezone Boundary – Midnight in Japan – UTC Timestamps Preserve the Correct Instant

**Description:** AC-01 — Boundary Value Analysis — A Lesson crossing a JST/UTC calendar boundary returns the correct UTC instant.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-TZ-01` starts at `2026-10-01 00:30 JST` and ends at `2026-10-01 01:30 JST`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The Riso integration caller requests the Lesson using its UTC calendar date. | The response returns Lesson `L-TZ-01`. | `start_jst = 2026-10-01 00:30 JST; start_utc = 2026-09-30T15:30:00Z; request_date = 2026-09-30 UTC` |
| 2 | The Riso integration caller compares the returned start and end timestamps with the source Lesson. | The response shows `2026-09-30T15:30:00Z` and `2026-09-30T16:30:00Z`, representing the original JST lesson times. | `end_jst = 2026-10-01 01:30 JST; end_utc = 2026-09-30T16:30:00Z` |

**Severity:** major  
**Priority:** high

---

### [Riso] Lesson Retrieval – Supported Statuses – Matching Scope – Each Requested Status Is Returned

**Description:** AC-02 — Equivalence Partitioning — Each supported status filters the requested lesson scope.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Four Lessons at `RISO_LOC_001` on `2026-10-10` have statuses Draft, Published, Completed, and Cancelled.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The Riso integration caller requests the four supported statuses for the shared date and location. | The response contains the four matching Lessons and no Lesson with another status or location. | `lesson_status = Draft,Published,Completed,Cancelled; lesson_start_date = 2026-10-10; lesson_end_date = 2026-10-10; location_id = RISO_LOC_001` |

**Severity:** minor  
**Priority:** medium

---

### [Riso] Lesson Retrieval – Date Filter – Malformed Date – Bad Request Is Returned

**Description:** AC-02 — Negative — A malformed required date is rejected.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The Riso integration caller requests Lessons with a malformed start date. | The response returns HTTP `400` and does not return lesson data. | `lesson_start_date = 2026-13-40; lesson_end_date = 2026-10-10; location_id = RISO_LOC_001; lesson_status = Published` |

**Severity:** major  
**Priority:** high

---

### [Riso] Lesson Retrieval – Date Range – End Before Start – Bad Request Is Returned

**Description:** AC-02 — Boundary Value Analysis — A reversed inclusive date range is rejected.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The Riso integration caller requests Lessons with an end date before the start date. | The response returns HTTP `400` and does not return lesson data. | `lesson_start_date = 2026-10-11; lesson_end_date = 2026-10-10; location_id = RISO_LOC_001; lesson_status = Published` |

**Severity:** major  
**Priority:** high

---

### [Riso] Lesson Retrieval – Status Filter – Unsupported Status – Unprocessable Request Is Returned

**Description:** AC-02 — Negative — An unsupported status value is rejected.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The Riso integration caller requests Lessons with an unsupported status. | The response returns HTTP `422` and does not return lesson data. | `lesson_status = Archived; lesson_start_date = 2026-10-10; lesson_end_date = 2026-10-10; location_id = RISO_LOC_001` |

**Severity:** major  
**Priority:** high

---

### [Riso] Lesson Retrieval – Page Size – Invalid Value – Unprocessable Request Is Returned

**Description:** AC-02 — Negative — An invalid requested page size is rejected.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The Riso integration caller requests Lessons with an invalid page size. | The response returns HTTP `422` and does not return lesson data. | `limitQuery = 0; lesson_status = Published; lesson_start_date = 2026-10-10; lesson_end_date = 2026-10-10; location_id = RISO_LOC_001` |

**Severity:** major  
**Priority:** high

---

### [Riso] Lesson Retrieval – Page Cursor – Unknown Value – Unprocessable Request Is Returned

**Description:** AC-02 — Negative — An unknown cursor cannot advance the result set.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The Riso integration caller requests Lessons with an unknown cursor. | The response returns HTTP `422` and does not return lesson data. | `next_pointer = 001000000000000AAA; lesson_status = Published; lesson_start_date = 2026-10-10; lesson_end_date = 2026-10-10; location_id = RISO_LOC_001` |

**Severity:** major  
**Priority:** high

---

### [Riso] Lesson Retrieval – Incremental Watermark – Exact Timestamp – Matching Lesson Is Returned

**Description:** AC-02 — Boundary Value Analysis — A Lesson modified exactly at the incremental watermark is included.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-WATERMARK-EQ` has System Modified timestamp `2026-09-29T00:00:00Z`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The Riso integration caller requests changed Lessons from the exact watermark. | The response contains `L-WATERMARK-EQ`. | `last_updated_since = 2026-09-29T00:00:00Z; lesson_date = 2026-10-11; location_id = RISO_LOC_001` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Lesson Retrieval – Incremental Watermark – Earlier Timestamp – Lesson Is Excluded

**Description:** AC-02 — Boundary Value Analysis — A Lesson modified before the watermark is not included.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-WATERMARK-BEFORE` has System Modified timestamp `2026-09-28T23:59:59Z`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The Riso integration caller requests changed Lessons from the later watermark. | The response does not contain `L-WATERMARK-BEFORE`. | `last_updated_since = 2026-09-29T00:00:00Z; lesson_date = 2026-10-11; location_id = RISO_LOC_001` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Lesson Retrieval – Pagination – Full and Final Pages – Every Lesson Is Returned Once

**Description:** AC-02 — Boundary Value Analysis — Cursor pagination returns the complete unique result set.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Five published Lessons match the same date range and location in a stable order.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The Riso integration caller requests the first page with a page size of two. | The response contains two Lessons and a non-null next pointer. | `lesson_start_date = 2026-10-12; lesson_end_date = 2026-10-12; location_id = RISO_LOC_001; limitQuery = 2` |
| 2 | The Riso integration caller requests the second page with the returned pointer. | The response contains two new Lessons and a non-null next pointer. | `expected_unique_lessons_after_page_2 = 4` |
| 3 | The Riso integration caller requests the final page with the returned pointer. | The response contains the final Lesson and a null next pointer. | `expected_unique_lessons_after_page_3 = 5` |

**Severity:** major  
**Priority:** high

---

### [Riso] Lesson Retrieval – Direct Lesson Change – Parent Modification – Incremental Timestamp Matches Lesson

**Description:** AC-04 — CRUD / Component — A direct Lesson edit is returned incrementally and uses the Lesson modified timestamp.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-DIRECT-01` has baseline modified timestamp `2026-09-29T00:10:00Z`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The Riso integration caller records the baseline Lesson response. | The baseline response shows `2026-09-29T00:10:00Z` as the last-updated value. | `baseline = 2026-09-29T00:10:00Z` |
| 2 | HQ or CM Staff changes the Lesson name and saves it. | The Lesson saves with its later Salesforce Last Modified Date. | `new_lesson_name = Algebra Updated` |
| 3 | The Riso integration caller requests changes from the baseline. | The response contains `L-DIRECT-01` and its last-updated value equals the parent Lesson Last Modified Date and is later than the baseline. | `last_updated_since = 2026-09-29T00:10:00Z` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Related Teacher – Created – Parent Lesson Is Returned with New Teacher

**Description:** AC-04 — CRUD / Regression — Adding a Lesson Teacher updates the parent Lesson and teacher collection.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-TEACHER-01` has baseline modified timestamp `2026-09-29T00:20:00Z` and no teacher named `Teacher A`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff assigns `Teacher A` to the Lesson. | The teacher assignment is created for `L-TEACHER-01`. | `teacher = Teacher A` |
| 2 | The Riso integration caller requests changes from the baseline. | The response contains the Lesson with a later last-updated value matching its parent Last Modified Date. | `last_updated_since = 2026-09-29T00:20:00Z` |
| 3 | The Riso integration caller inspects the returned teacher collection. | `Teacher A` appears with the configured teacher identifier and name. | `expected_teacher = Teacher A` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Related Teacher – Updated – Parent Lesson Is Returned with Updated Teacher Data

**Description:** AC-04 — CRUD / Regression — Updating a Lesson Teacher updates the parent Lesson and response.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-TEACHER-02` has an assigned teacher whose external identifier is `T001` and baseline timestamp `2026-09-29T00:25:00Z`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff changes the assigned teacher's Riso external identifier to `T002`. | The Lesson Teacher record saves with identifier `T002`. | `old_identifier = T001; new_identifier = T002` |
| 2 | The Riso integration caller requests changes from the baseline. | The response contains the Lesson with a later last-updated value matching its parent Last Modified Date. | `last_updated_since = 2026-09-29T00:25:00Z` |
| 3 | The Riso integration caller inspects the returned teacher collection. | The teacher entry shows external identifier `T002`. | `expected_identifier = T002` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Related Teacher – Deleted – Parent Lesson Is Returned without Removed Teacher

**Description:** AC-04 — CRUD / Regression — Removing a Lesson Teacher updates the parent Lesson and active teacher collection.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-TEACHER-03` has assigned `Teacher A` and baseline timestamp `2026-09-29T00:30:00Z`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff removes `Teacher A` from the Lesson. | The teacher assignment is deleted. | `teacher = Teacher A` |
| 2 | The Riso integration caller requests changes from the baseline. | The response contains the Lesson with a later last-updated value matching its parent Last Modified Date. | `last_updated_since = 2026-09-29T00:30:00Z` |
| 3 | The Riso integration caller inspects the returned teacher collection. | `Teacher A` is absent from the active teacher collection. | `expected_teacher_count = 0` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Related Classroom – Created – Parent Lesson Is Returned with New Classroom

**Description:** AC-04 — CRUD / Regression — Adding a classroom updates the parent Lesson and classroom collection.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-ROOM-01` has baseline timestamp `2026-09-29T00:35:00Z` and no classroom `Booth 1`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff assigns classroom `Booth 1` to the Lesson. | The classroom assignment is created. | `classroom = Booth 1` |
| 2 | The Riso integration caller requests changes from the baseline. | The response contains the Lesson with a later last-updated value matching its parent Last Modified Date. | `last_updated_since = 2026-09-29T00:35:00Z` |
| 3 | The Riso integration caller inspects the returned classroom collection. | `Booth 1` appears with its configured classroom identifier and name. | `expected_classroom = Booth 1` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Related Classroom – Updated – Parent Lesson Is Returned with Updated Classroom Data

**Description:** AC-04 — CRUD / Regression — Updating a classroom assignment updates the parent Lesson and response.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-ROOM-02` has classroom `Booth 1` and baseline timestamp `2026-09-29T00:40:00Z`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff changes the Lesson classroom from `Booth 1` to `Booth 2`. | The classroom assignment saves as `Booth 2`. | `old_classroom = Booth 1; new_classroom = Booth 2` |
| 2 | The Riso integration caller requests changes from the baseline. | The response contains the Lesson with a later last-updated value matching its parent Last Modified Date. | `last_updated_since = 2026-09-29T00:40:00Z` |
| 3 | The Riso integration caller inspects the returned classroom collection. | `Booth 2` appears and `Booth 1` is absent. | `expected_classroom = Booth 2` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Related Classroom – Deleted – Parent Lesson Is Returned without Removed Classroom

**Description:** AC-04 — CRUD / Regression — Removing a classroom updates the parent Lesson and active classroom collection.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-ROOM-03` has classroom `Booth 1` and baseline timestamp `2026-09-29T00:45:00Z`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff removes classroom `Booth 1` from the Lesson. | The classroom assignment is deleted. | `classroom = Booth 1` |
| 2 | The Riso integration caller requests changes from the baseline. | The response contains the Lesson with a later last-updated value matching its parent Last Modified Date. | `last_updated_since = 2026-09-29T00:45:00Z` |
| 3 | The Riso integration caller inspects the returned classroom collection. | `Booth 1` is absent from the active classroom collection. | `expected_classroom_count = 0` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Related Student Session – Created – Parent Lesson Is Returned with New Student

**Description:** AC-04 — CRUD / Regression — Adding an active Student Session updates the parent Lesson and student collection.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-STUDENT-01` has baseline timestamp `2026-09-29T00:50:00Z` and no session for `Student A`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff assigns `Student A` to the Lesson with an active Student Session. | An active Student Session is created for `Student A`. | `student = Student A; is_deleted = false; is_archived = false` |
| 2 | The Riso integration caller requests changes from the baseline. | The response contains the Lesson with a later last-updated value matching its parent Last Modified Date. | `last_updated_since = 2026-09-29T00:50:00Z` |
| 3 | The Riso integration caller inspects the returned student collection. | `Student A` appears with the configured student and session values. | `expected_student = Student A` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Related Student Session – Updated – Parent Lesson Is Returned with Updated Session Data

**Description:** AC-04 — CRUD / Regression — Updating an active Student Session updates the parent Lesson and student response data.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-STUDENT-02` has active `Student A` session type `Standard` and baseline timestamp `2026-09-29T00:55:00Z`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff changes `Student A` session type to `Trial`. | The Student Session saves with type `Trial`. | `old_session_type = Standard; new_session_type = Trial` |
| 2 | The Riso integration caller requests changes from the baseline. | The response contains the Lesson with a later last-updated value matching its parent Last Modified Date. | `last_updated_since = 2026-09-29T00:55:00Z` |
| 3 | The Riso integration caller inspects the returned student collection. | `Student A` shows session type `Trial`. | `expected_session_type = Trial` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Related Student Session – Deleted – Parent Lesson Is Returned without Removed Student

**Description:** AC-04, AC-05 — CRUD / Regression — Deleting a Student Session updates the parent Lesson and excludes that student.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-STUDENT-03` has active `Student A` and baseline timestamp `2026-09-29T01:00:00Z`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff deletes `Student A` Student Session. | The Student Session is deleted. | `student = Student A` |
| 2 | The Riso integration caller requests changes from the baseline. | The response contains the Lesson with a later last-updated value matching its parent Last Modified Date. | `last_updated_since = 2026-09-29T01:00:00Z` |
| 3 | The Riso integration caller inspects the returned student collection. | `Student A` is absent from the returned students. | `expected_student_count = 0` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Related Student Session – Archived – Parent Lesson Is Returned without Archived Student

**Description:** AC-05 — Decision Table / Regression — An archived Student Session is excluded while its changed parent Lesson remains retrievable.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-STUDENT-ARCHIVE-01` has active `Student A` and baseline timestamp `2026-09-29T01:05:00Z`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff archives `Student A` Student Session. | The Student Session is marked archived. | `student = Student A; is_archived = true` |
| 2 | The Riso integration caller requests changes from the baseline. | The response contains the changed parent Lesson. | `last_updated_since = 2026-09-29T01:05:00Z` |
| 3 | The Riso integration caller inspects the returned student collection. | `Student A` is absent from the returned students. | `expected_student_count = 0` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Related Lesson Report – Created – Parent Lesson Is Returned Incrementally

**Description:** AC-04 — CRUD / Regression — Creating a Lesson Report makes the associated Lesson available to the incremental pull.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-REPORT-01` has no Lesson Report and baseline timestamp `2026-09-29T01:10:00Z`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff creates a Lesson Report for the Lesson. | A Lesson Report is created and linked to `L-REPORT-01`. | `lesson = L-REPORT-01` |
| 2 | The Riso integration caller requests changes from the baseline. | The response contains the Lesson with a later last-updated value matching its parent Last Modified Date. | `last_updated_since = 2026-09-29T01:10:00Z` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Related Lesson Report – Updated – Parent Lesson Is Returned Incrementally

**Description:** AC-04 — CRUD / Regression — Updating a Lesson Report makes the associated Lesson available to the incremental pull.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-REPORT-02` has a Lesson Report and baseline timestamp `2026-09-29T01:15:00Z`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff changes a report value and saves the Lesson Report. | The Lesson Report update is saved. | `report_value = Updated feedback` |
| 2 | The Riso integration caller requests changes from the baseline. | The response contains the Lesson with a later last-updated value matching its parent Last Modified Date. | `last_updated_since = 2026-09-29T01:15:00Z` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Related Lesson Report – Deleted – Parent Lesson Is Returned Incrementally

**Description:** AC-04 — CRUD / Regression — Deleting a Lesson Report makes the associated Lesson available to the incremental pull.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-REPORT-03` has a Lesson Report and baseline timestamp `2026-09-29T01:20:00Z`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff deletes the Lesson Report. | The Lesson Report is deleted. | `lesson = L-REPORT-03` |
| 2 | The Riso integration caller requests changes from the baseline. | The response contains the Lesson with a later last-updated value matching its parent Last Modified Date. | `last_updated_since = 2026-09-29T01:20:00Z` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Related Survey Response – Created – Parent Lesson Is Returned Incrementally

**Description:** AC-04 — CRUD / Regression — Creating a Lesson Survey Response makes the associated Lesson available to the incremental pull.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-SURVEY-01` has no Lesson Survey Response and baseline timestamp `2026-09-29T01:25:00Z`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff creates a Lesson Survey Response for the Lesson. | A Lesson Survey Response is created and linked to `L-SURVEY-01`. | `lesson = L-SURVEY-01` |
| 2 | The Riso integration caller requests changes from the baseline. | The response contains the Lesson with a later last-updated value matching its parent Last Modified Date. | `last_updated_since = 2026-09-29T01:25:00Z` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Related Survey Response – Updated – Parent Lesson Is Returned Incrementally

**Description:** AC-04 — CRUD / Regression — Updating a Lesson Survey Response makes the associated Lesson available to the incremental pull.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-SURVEY-02` has a Lesson Survey Response and baseline timestamp `2026-09-29T01:30:00Z`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff changes a survey answer and saves the Lesson Survey Response. | The Lesson Survey Response update is saved. | `survey_answer = Updated answer` |
| 2 | The Riso integration caller requests changes from the baseline. | The response contains the Lesson with a later last-updated value matching its parent Last Modified Date. | `last_updated_since = 2026-09-29T01:30:00Z` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Related Survey Response – Deleted – Parent Lesson Is Returned Incrementally

**Description:** AC-04 — CRUD / Regression — Deleting a Lesson Survey Response makes the associated Lesson available to the incremental pull.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-SURVEY-03` has a Lesson Survey Response and baseline timestamp `2026-09-29T01:35:00Z`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff deletes the Lesson Survey Response. | The Lesson Survey Response is deleted. | `lesson = L-SURVEY-03` |
| 2 | The Riso integration caller requests changes from the baseline. | The response contains the Lesson with a later last-updated value matching its parent Last Modified Date. | `last_updated_since = 2026-09-29T01:35:00Z` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Related Lesson Schedule – Created – Every Schedule Lesson Is Returned Incrementally

**Description:** AC-04 — CRUD / Regression — Creating a Lesson Schedule change affects every associated Lesson.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- A new Riso Lesson Schedule is created with two published Lessons `L-SCHEDULE-01A` and `L-SCHEDULE-01B`, each baseline timestamp `2026-09-29T01:40:00Z`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff saves the newly created Lesson Schedule. | The Lesson Schedule is created with both associated Lessons. | `schedule = LS-CREATE-01; expected_lessons = L-SCHEDULE-01A,L-SCHEDULE-01B` |
| 2 | The Riso integration caller requests changes from the baseline. | Both associated Lessons are returned, each with a later last-updated value matching its parent Last Modified Date. | `last_updated_since = 2026-09-29T01:40:00Z; expected_count = 2` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Related Lesson Schedule – Updated – Every Schedule Lesson Is Returned Incrementally

**Description:** AC-04 — CRUD / Regression — Updating a Lesson Schedule affects every associated Lesson.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Lesson Schedule `LS-UPDATE-01` has two published Lessons `L-SCHEDULE-02A` and `L-SCHEDULE-02B`, each baseline timestamp `2026-09-29T01:45:00Z`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff changes the Lesson Schedule name and saves it. | The Lesson Schedule update is saved. | `new_schedule_name = October Schedule Updated` |
| 2 | The Riso integration caller requests changes from the baseline. | Both associated Lessons are returned, each with a later last-updated value matching its parent Last Modified Date. | `last_updated_since = 2026-09-29T01:45:00Z; expected_count = 2` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Related Lesson Schedule – Deleted – Every Former Schedule Lesson Is Returned Incrementally

**Description:** AC-04 — CRUD / Regression — Deleting a Lesson Schedule affects every associated Lesson.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Lesson Schedule `LS-DELETE-01` has two published Lessons `L-SCHEDULE-03A` and `L-SCHEDULE-03B`, each baseline timestamp `2026-09-29T01:50:00Z`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff deletes the Lesson Schedule. | The Lesson Schedule is deleted according to Salesforce lifecycle rules. | `schedule = LS-DELETE-01` |
| 2 | The Riso integration caller requests changes from the baseline. | Every affected Lesson is returned with a later last-updated value matching its parent Last Modified Date. | `last_updated_since = 2026-09-29T01:50:00Z; expected_lessons = L-SCHEDULE-03A,L-SCHEDULE-03B` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Related Schedule Class – Created – Every Schedule Lesson Returns Updated Class Codes

**Description:** AC-04 — CRUD / Regression — Adding a schedule class affects every schedule Lesson and its class-code aggregation.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Lesson Schedule `LS-CLASS-01` has two published Lessons `L-CLASS-01A` and `L-CLASS-01B`, one class code `C02`, and baseline timestamp `2026-09-29T01:55:00Z`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff adds a schedule class with partner code `C05`. | The schedule class is created under `LS-CLASS-01`. | `new_class_code = C05` |
| 2 | The Riso integration caller requests changes from the baseline. | Both schedule Lessons are returned with later last-updated values matching their parent Last Modified Dates. | `last_updated_since = 2026-09-29T01:55:00Z; expected_count = 2` |
| 3 | The Riso integration caller inspects the returned class partner codes. | Each returned Lesson shows `C02;C05`. | `expected_course_partner_id = C02;C05` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Related Schedule Class – Updated – Every Schedule Lesson Returns Updated Class Codes

**Description:** AC-04 — CRUD / Regression — Updating a schedule class affects every schedule Lesson and its class-code aggregation.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Lesson Schedule `LS-CLASS-02` has two published Lessons `L-CLASS-02A` and `L-CLASS-02B`, class code `C02`, and baseline timestamp `2026-09-29T02:00:00Z`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff changes the schedule class partner code from `C02` to `C05`. | The schedule class update is saved. | `old_class_code = C02; new_class_code = C05` |
| 2 | The Riso integration caller requests changes from the baseline. | Both schedule Lessons are returned with later last-updated values matching their parent Last Modified Dates. | `last_updated_since = 2026-09-29T02:00:00Z; expected_count = 2` |
| 3 | The Riso integration caller inspects the returned class partner codes. | Each returned Lesson shows `C05`. | `expected_course_partner_id = C05` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Related Schedule Class – Deleted – Every Schedule Lesson Returns Remaining Class Codes

**Description:** AC-04 — CRUD / Regression — Deleting a schedule class affects every schedule Lesson and removes its class code.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Lesson Schedule `LS-CLASS-03` has two published Lessons `L-CLASS-03A` and `L-CLASS-03B`, class codes `C02` and `C05`, and baseline timestamp `2026-09-29T02:05:00Z`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | HQ or CM Staff deletes the schedule class with partner code `C05`. | The schedule class is deleted. | `deleted_class_code = C05` |
| 2 | The Riso integration caller requests changes from the baseline. | Both schedule Lessons are returned with later last-updated values matching their parent Last Modified Dates. | `last_updated_since = 2026-09-29T02:05:00Z; expected_count = 2` |
| 3 | The Riso integration caller inspects the returned class partner codes. | Each returned Lesson shows only `C02`. | `expected_course_partner_id = C02` |

**Severity:** critical  
**Priority:** high

---

### [Riso] Lesson Retrieval – Lesson OOP Fields – Configured Values – Every Field Matches Its Source

**Description:** AC-01, AC-03 — Component — Every Lesson-level Riso OOP value is returned from its configured Salesforce source with the expected value and type.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-OOP-LESSON-01` has compensation ratio `1.25`, location partner ID `KOU-001`, timeslot sequence `3`, subject partner ID `SUB-101`, and day-of-week code `1`.
- The Lesson Schedule has three classes with partner codes `C10`, `C02`, and `C05`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The Riso integration caller requests the populated Lesson for its date and location. | The response returns HTTP `200` with Lesson `L-OOP-LESSON-01`. | `lesson_status = Published; lesson_date = 2026-10-15; location_id = RISO_LOC_001` |
| 2 | The Riso integration caller compares the Lesson-level Riso values in the response with the configured Salesforce values. | Compensation ratio is `"1.25"`; location partner ID is `"KOU-001"`; timeslot sequence is `"3"`; subject partner ID is `"SUB-101"`; day-of-week code is `"1"`; and course partner codes are `"C02;C05;C10"`. | `expected_compensation_ratio = 1.25; expected_location_partner_id = KOU-001; expected_timeslot_sequence = 3; expected_subject_partner_id = SUB-101; expected_day_of_week = 1; expected_course_partner_id = C02;C05;C10` |
| 3 | The Riso integration caller inspects the data types of the returned OOP values. | Each configured Lesson OOP value is a string, including numeric-looking values such as `"1.25"`, `"3"`, and `"1"`. | `expected_type = String` |

**Severity:** major  
**Priority:** high

---

### [Riso] Lesson Retrieval – Teacher OOP Field – Configured External ID – Value Matches Teacher Source

**Description:** AC-01, AC-03 — Component — The teacher collection exposes the configured Riso external teacher ID for the correct teacher.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-OOP-TEACHER-01` has one active Lesson Teacher: name `Yamada Riku`, Manabie ID `01KEV2255CKFQYPHFW8JXH0M0E`, and Riso external teacher ID `T0501`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The Riso integration caller requests the populated Lesson for its date and location. | The response returns HTTP `200` with Lesson `L-OOP-TEACHER-01`. | `lesson_status = Published; lesson_date = 2026-10-16; location_id = RISO_LOC_001` |
| 2 | The Riso integration caller finds `Yamada Riku` in the returned teacher collection. | The teacher entry has Manabie ID `01KEV2255CKFQYPHFW8JXH0M0E`, name `Yamada Riku`, and external teacher ID `"T0501"`. | `expected_teacher_id = 01KEV2255CKFQYPHFW8JXH0M0E; expected_name = Yamada Riku; expected_external_id = T0501` |
| 3 | The Riso integration caller inspects the external teacher ID type. | The external teacher ID is returned as a string. | `expected_type = String` |

**Severity:** major  
**Priority:** high

---

### [Riso] Lesson Retrieval – Student OOP Fields – Configured Session Values – Every Field Matches Student Session Source

**Description:** AC-01, AC-03 — Component — The student collection exposes every configured Riso OOP value from the active Student Session.

**Preconditions:**

- A Riso integration caller has valid access to lesson retrieval.
- Published Lesson `L-OOP-STUDENT-01` has one active, non-archived Student Session for `Sato Hana`.
- The Student Session has user name `S100234`, course partner ID `C21`, lesson division `1`, grade code `08`, attendance status `Present`, slot consumption `1`, and payroll occurrence flag `true`.

| # | Action | Expected Result | Test Data |
|---:|---|---|---|
| 1 | The Riso integration caller requests the populated Lesson for its date and location. | The response returns HTTP `200` with Lesson `L-OOP-STUDENT-01`. | `lesson_status = Published; lesson_date = 2026-10-17; location_id = RISO_LOC_001` |
| 2 | The Riso integration caller finds `Sato Hana` in the returned student collection. | The student entry shows user name `"S100234"`, course partner ID `"C21"`, lesson division `"1"`, grade code `"08"`, attendance status `"Present"`, slot consumption `"1"`, and payroll occurrence flag `"true"`. | `expected_student_user_name = S100234; expected_course_partner_id = C21; expected_lesson_division = 1; expected_grade_code = 08; expected_attendance_status = Present; expected_slot_consumption = 1; expected_payroll_occurrence_flag = true` |
| 3 | The Riso integration caller inspects the data types of the returned Student OOP values. | Each configured Student OOP value is a string, including `"1"`, `"08"`, and `"true"`. | `expected_type = String` |

**Severity:** major  
**Priority:** high
