# Test Cases: LT-90306 — Lesson Allocation Soft Delete (Archive)

Source Qase suite reviewed: [PX suite 1294 — "Single Assign Class"](https://app.qase.io/project/PX?suite=1294) (16 existing cases). The suite covers active, future, and past Class Member effective-date behavior, but none of its cases archives the parent Lesson Allocation. These cases add the archive state without duplicating the existing effective-date baseline.

## Suite: Single Assign Class

### Single Assign Class – Archived Lesson Allocation – Existing Class Member – Student Excluded from New Class Lesson

**Description:** AC-2 / AC-5 — Decision Table — A Class Member retained under an archived Lesson Allocation is excluded from class auto-assignment.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- Today is 2026-05-20 in the organisation time zone.
- Class A belongs to Course Math 101 at Location Tokyo HQ.
- Student A has one active Lesson Allocation for Math 101 from 2026-05-01 through 2026-12-31.
- Student A has one Class A membership from 2026-05-01 through 2026-12-31.
- No Class A lesson exists on 2026-05-21.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff removes every Student Package Order for Student A's Math 101 allocation and waits for allocation processing to finish | Student A's Lesson Allocation is archived, while the existing Class A membership keeps its original dates and becomes archived | today = 2026-05-20; allocation_start = 2026-05-01; allocation_end = 2026-12-31; class_start = 2026-05-01; class_end = 2026-12-31 |
| 2 | HQ or CM Staff creates a one-time Group lesson for Class A on 2026-05-21 | The new lesson is created | lesson_date = 2026-05-21 |
| 3 | HQ or CM Staff waits for class auto-assignment to finish | Class auto-assignment finishes without an error | class = Class A |
| 4 | HQ or CM Staff opens the new lesson's Student Sessions list | Student A is absent from the list because the retained Class A membership is archived | Student A allocation archived → class member excluded |

**Severity:** critical
**Priority:** high

---

### Single Assign Class – Restored Lesson Allocation – Same Class Member – Student Included in Later Class Lesson

**Description:** AC-2 / AC-3 / AC-5 — State Transition — Restoring an archived Lesson Allocation restores the same Class Member for later class auto-assignment without creating a duplicate membership.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- Today is 2026-05-20 in the organisation time zone.
- Class A belongs to Course Math 101 at Location Tokyo HQ.
- Student A has an archived Lesson Allocation for Math 101 that was active from 2026-05-01 through 2026-12-31.
- Student A's original Class A membership still exists with dates 2026-05-01 through 2026-12-31 and is archived with its parent allocation.
- No Class A lesson exists on 2026-05-22.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff restores one living Student Package Order for Student A's Math 101 allocation and waits for allocation processing to finish | The archived Lesson Allocation is restored on its original record, and the original Class A membership becomes active again with the same dates | today = 2026-05-20; restored_order_start = 2026-05-01; restored_order_end = 2026-12-31 |
| 2 | HQ or CM Staff opens Student A's Class history | One Class A membership is present for 2026-05-01 through 2026-12-31; no duplicate Class A membership was created during restoration | class = Class A; expected_membership_count = 1 |
| 3 | HQ or CM Staff creates a one-time Group lesson for Class A on 2026-05-22 | The new lesson is created | lesson_date = 2026-05-22 |
| 4 | HQ or CM Staff waits for class auto-assignment to finish and opens the lesson's Student Sessions list | Student A appears once in the lesson as an auto-assigned student | Student A restored Class A membership → one student session |

**Severity:** critical
**Priority:** high

---

### Single Assign Class – Archived Lesson Allocation – Change Class Action – Archived Membership Cannot Drive Student Sessions

**Description:** AC-5 — Negative — A class-change action cannot use an archived Class Member as an active membership or create an active Student Session from it.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- Today is 2026-05-20 in the organisation time zone.
- Class A and Class B both belong to Course Math 101 at Location Tokyo HQ.
- Student A has an archived Lesson Allocation for Math 101.
- Student A's retained Class A membership runs from 2026-05-01 through 2026-12-31 and is archived with the parent allocation.
- A Group lesson for Class B exists on 2026-05-22.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff opens Student A's Course tab and starts the class-change flow for Math 101 | The archived Class A membership is not available as an active class assignment to change | today = 2026-05-20; archived_class = Class A; requested_class = Class B |
| 2 | HQ or CM Staff attempts to complete a change from Class A to Class B | The system does not create an active Class B membership or an active student assignment while Student A's Lesson Allocation remains archived | allocation_status = archived |
| 3 | HQ or CM Staff opens the Class B lesson on 2026-05-22 after class processing finishes | Student A is absent from the Student Sessions list | lesson_date = 2026-05-22; expected_student_sessions_for_student_a = 0 |

**Severity:** critical
**Priority:** high

---

### Single Assign Class – Archived Lesson Allocation – JST and UTC Boundary – Student Excluded from Class Assignment

**Description:** AC-1 / AC-2 / AC-5 — Boundary Value Analysis — An archive stamped across a JST/UTC calendar boundary still excludes the Class Member from later auto-assignment.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- Class A belongs to Course Math 101 at Location Tokyo HQ.
- Student A has one active Lesson Allocation and one active Class A membership, both valid from 2026-05-01 through 2026-12-31.
- No Class A lesson exists at 2026-05-20 09:00 JST.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff removes every Student Package Order for Student A's Math 101 allocation at the stated boundary time and waits for allocation processing to finish | Student A's Lesson Allocation and Class A membership are archived | archive_time = 2026-05-20 00:30 JST (= 2026-05-19 15:30 UTC); class_start = 2026-05-01; class_end = 2026-12-31 |
| 2 | HQ or CM Staff creates a Group lesson for Class A at 2026-05-20 09:00 JST | The lesson is created | lesson_start = 2026-05-20 09:00 JST (= 2026-05-20 00:00 UTC) |
| 3 | HQ or CM Staff waits for class auto-assignment to finish and opens the lesson's Student Sessions list | Student A is absent; the archive state is not treated as active because its UTC date is the prior calendar day | archive_time < lesson_start; archived membership → excluded |

**Severity:** critical
**Priority:** high

---

### Single Assign Class – Archived Class Member – Back Office Student Course Tab – Membership Hidden

**Description:** AC-5 — Decision Table — Back Office excludes a Class Member whose parent Lesson Allocation is archived.

**Preconditions:**
- HQ Staff is logged in to Back Office.
- Today is 2026-05-20 in the organisation time zone.
- Student A has a Class A membership for Math 101 from 2026-05-01 through 2026-12-31.
- Student A's Math 101 Lesson Allocation has been archived after every related Student Package Order was removed.
- Salesforce-to-Back Office synchronisation is complete after the archive.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ Staff opens Student A's profile in Back Office and selects the Student Course tab | The Student Course tab is displayed | today = 2026-05-20; class = Class A; allocation_status = archived |
| 2 | HQ Staff looks for Class A under Student A's Math 101 course | Class A is absent because its Class Member is archived | class_member_status = archived → hidden |

**Severity:** critical
**Priority:** high

---

### Single Assign Class – Restored Class Member – Back Office Student Course Tab – Same Membership Shown

**Description:** AC-2 / AC-3 / AC-5 — State Transition — Back Office shows the original Class Member again after the parent Lesson Allocation is restored.

**Preconditions:**
- HQ Staff is logged in to Back Office.
- Today is 2026-05-20 in the organisation time zone.
- Student A has an archived Math 101 Lesson Allocation and its original archived Class A membership from 2026-05-01 through 2026-12-31.
- Class A is absent from Student A's Back Office Student Course tab.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff restores one living Student Package Order for Student A's Math 101 allocation and waits for Salesforce-to-Back Office synchronisation to finish | The original Lesson Allocation and Class A membership are restored; no additional Class A membership is created | today = 2026-05-20; restored_order_start = 2026-05-01; restored_order_end = 2026-12-31 |
| 2 | HQ Staff refreshes Student A's Back Office Student Course tab | Class A appears under Math 101 with start date 2026-05-01 and end date 2026-12-31 | class = Class A; expected_membership_count = 1 |

**Severity:** critical
**Priority:** high

---

### Single Assign Class – Past Class Member Restored After Archive – New Lesson – Student Remains Unassigned

**Description:** AC-2 / AC-3 / AC-5 — Boundary Value Analysis — Restoring a parent Lesson Allocation does not reactivate a Class Member whose effective period has already ended.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- Today is 2026-05-20 in the organisation time zone.
- Class A belongs to Course Math 101 at Location Tokyo HQ.
- Student A's Math 101 Lesson Allocation was archived on 2026-05-15.
- Student A's retained Class A membership started on 2026-05-01 and ended on 2026-05-19.
- No Class A lesson exists on 2026-05-21.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff restores one living Student Package Order for Student A's Math 101 allocation and waits for allocation processing to finish | The Lesson Allocation is restored on the same record, and the historical Class A membership remains with start date 2026-05-01 and end date 2026-05-19 | today = 2026-05-20; archived_on = 2026-05-15; class_start = 2026-05-01; class_end = 2026-05-19 |
| 2 | HQ or CM Staff creates a one-time Group lesson for Class A on 2026-05-21 | The new lesson is created | lesson_date = 2026-05-21; lesson_date > class_end |
| 3 | HQ or CM Staff waits for class auto-assignment to finish and opens the lesson's Student Sessions list | Student A is absent because the restored Class A membership is historical; no new Class Member is created | restored_membership_end = 2026-05-19; expected_student_sessions_for_student_a = 0 |

**Severity:** major
**Priority:** high

---

### Single Assign Class – Restored Lesson Allocation – Cancelled Lesson Schedule Class – Student Remains Unassigned

**Description:** AC-3 / AC-5 — State Transition — Restoring a Lesson Allocation does not override a prior removal of the class from the Lesson Schedule.

**Preconditions:**
- HQ or CM Staff is logged in to Salesforce.
- Today is 2026-05-20 in the organisation time zone.
- A recurring Group Lesson Schedule for Math 101 at Location Tokyo HQ originally used Class A.
- Student A has an archived Math 101 Lesson Allocation and its retained archived Class A membership from 2026-05-01 through 2026-12-31.
- Class A was removed from the Lesson Schedule on 2026-05-18 while Student A's Lesson Allocation was archived.
- The Lesson Schedule has no active Class A assignment.

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | HQ or CM Staff restores one living Student Package Order for Student A's Math 101 allocation and waits for allocation processing to finish | Student A's original Lesson Allocation and Class A membership are restored; Class A remains removed from the Lesson Schedule | today = 2026-05-20; restored_order_start = 2026-05-01; restored_order_end = 2026-12-31; class_removed_on = 2026-05-18 |
| 2 | HQ or CM Staff extends the Lesson Schedule to create a lesson on 2026-05-22 | The new lesson is created without Class A | lesson_date = 2026-05-22; lesson_schedule_class = none |
| 3 | HQ or CM Staff waits for class auto-assignment to finish and opens the new lesson's Student Sessions list | Student A is absent; restoring the Lesson Allocation does not re-add Class A to the Lesson Schedule or create a Student Session | expected_student_sessions_for_student_a = 0; Class A remains removed |

**Severity:** critical
**Priority:** high
