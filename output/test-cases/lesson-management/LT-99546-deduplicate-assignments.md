# LT-99546 — Deduplicate Student and Teacher Assignments

> **Focus:** Concurrent / simultaneous assignment — two actors or two flows attempting to assign
> the **same student or teacher to the same lesson at the same time** from different surfaces.
> Root cause (2026-04-07): Calendar manual add + class auto-assign queue running in parallel → 1,655 duplicate records.
> Fix: DB unique constraints on `(student_id, lesson_id)` and `(teacher_id, lesson_id)` silently reject any second insert.

---

## Suite: Concurrent Add — Lesson Detail + Calendar (Same Time)

### Student Assignment – Staff Submits via Lesson Detail While Another Staff Submits via Calendar Simultaneously – Only One Session Created

**Description:** AC 01 / BR-03 / BR-05 — Negative Testing. Simulates two staff members adding the same student to the same lesson from different surfaces at the same moment. Only one `student_session` must be created; the second concurrent insert is silently rejected at DB level.

**Preconditions:**
- Staff User A is logged in and has Lesson X detail page open, Add Student popup open, Student A selected (not yet submitted)
- Staff User B is logged in and has the SF Calendar open, Lesson X popup open, Add Student popup open, Student A selected (not yet submitted)
- Student A is not yet assigned to Lesson X

**Severity:** critical
**Priority:** high

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Staff User A and Staff User B **both click Add at the same moment** (within the same second) | Both requests are submitted to the server concurrently | Student A on both sessions |
| 2 | Wait for both responses to return | At least one response succeeds; the other is silently ignored — no error screen shown to either user | - |
| 3 | Count `student_session` records for (Student A, Lesson X) | Exactly **1** record | - |
| 4 | Open Lesson X detail page | Student A appears **once** in the Student Sessions list | - |

---

### Student Assignment – Staff Adds via Calendar While Class Auto-Assign Queue Is Running – Only One Session Created

**Description:** AC 01 / BR-05 / BR-18 / F-11 — Negative Testing. This is the **exact root cause scenario** of the 2026-04-07 incident. Staff manually adds a class student from the Calendar popup while the class auto-assign queue is simultaneously creating sessions for all class members including that student.

**Preconditions:**
- A group lesson with Class A (35 students including Student A) has been created — class auto-assign queue triggered but **not yet completed**
- Staff User is on the SF Calendar lesson popup with the Add Student popup open and Student A selected (not yet submitted)

**Severity:** critical
**Priority:** high

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | While the class auto-assign queue is still running, Staff User clicks **Add** for Student A in the Calendar popup | The manual add request is submitted concurrently with the queue | Student A |
| 2 | Wait for the queue job to finish | The queue completes **without error** — the already-inserted session is silently skipped | - |
| 3 | Count `student_session` records for (Student A, Lesson X) | Exactly **1** record — the first insert won; the second was rejected at DB level | - |
| 4 | Verify the other 34 class students each have exactly 1 session | Each of the 34 students has exactly 1 session — the queue did not fail or skip them | - |

---

### Student Assignment – Staff Adds via Lesson Detail While Class Auto-Assign Queue Is Running – Only One Session Created

**Description:** AC 01 / BR-03 / BR-04 — Negative Testing. Same concurrent scenario but via the Lesson Detail surface instead of Calendar. Staff adds a student via the Lesson Detail "Add Students" button while the background class auto-assign queue is mid-run.

**Preconditions:**
- A group lesson with Class A (including Student A) has been created — class auto-assign queue triggered but not yet completed
- Staff User is on Lesson X detail page, Add Student popup open, Student A selected (not yet submitted)

**Severity:** critical
**Priority:** high

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | While the queue is still running, Staff User clicks **Add** for Student A on Lesson Detail | The manual add is submitted concurrently with the queue | Student A |
| 2 | Wait for the queue job to complete | Queue completes without error | - |
| 3 | Count `student_session` records for (Student A, Lesson X) | Exactly **1** record | - |

---

## Suite: Concurrent Add — Class Import Triggers Queue + Manual Add (Same Time)

### Student Assignment – Class Member Import Triggers Queue + Staff Manually Adds Same Student Simultaneously – Only One Session Created

**Description:** AC 01 / BR-04 / BR-14 — Regression Analysis + Negative Testing. Staff imports a class member list (triggering the Master Queue), and at the same time another staff manually adds one of those students from the lesson detail. The queue must silently skip the already-inserted student without failing.

**Preconditions:**
- Lesson X is linked to Class A (5 students including Student A)
- Staff User A is about to import the class member list (CSV)
- Staff User B has Lesson X detail page open and Student A selected in the Add Student popup (not yet submitted)

**Severity:** critical
**Priority:** high

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Staff User A imports the class member list — the Master Queue starts assigning sessions for all 5 students | Queue job starts | Class A CSV |
| 2 | Staff User B immediately clicks **Add** for Student A in the Lesson Detail popup (before queue finishes) | Manual add submitted concurrently | Student A |
| 3 | Wait for the queue job to complete | Queue job completes successfully — not failed by the duplicate | - |
| 4 | Count `student_session` records for (Student A, Lesson X) | Exactly **1** record | - |
| 5 | Count `student_session` records for the other 4 class students on Lesson X | Each has exactly **1** record — queue processed them correctly | - |

---

### Student Assignment – Create LA with Class Triggers Queue + Staff Adds Same Student from Calendar Simultaneously – Only One Session Created

**Description:** AC 01 / BR-04 — Regression Analysis. Creating a new LA with a class assignment triggers the Master Queue to auto-assign sessions for all class members. If staff concurrently adds one of those class students from the Calendar popup while the queue is still running, only one session must exist.

**Preconditions:**
- Lesson X is already created and linked to Class A (including Student A)
- Staff User A is about to create a new LA for Class A (LA creation will trigger the Master Queue for Lesson X)
- Staff User B has the SF Calendar lesson popup for Lesson X open and Student A selected in Add Student popup (not yet submitted)
- Student A does NOT yet have a `student_session` for Lesson X

**Severity:** critical
**Priority:** high

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Staff User A creates the LA for Class A — the Master Queue is triggered and starts assigning sessions for all class members including Student A | Queue job starts | Class A, Lesson X |
| 2 | Staff User B clicks **Add** for Student A from the Calendar popup while the queue is still running | Concurrent add submitted | Student A |
| 3 | Wait for the queue to complete | Queue completes without error — the duplicate insert is silently rejected at DB level | - |
| 4 | Count `student_session` records for (Student A, Lesson X) | Exactly **1** record | - |

---

### Student Assignment – Lesson Import with Class Assignment Triggers Queue + Staff Adds Same Student from Calendar Simultaneously – Only One Session Created

**Description:** AC 01 / BR-04 / BR-14 — Regression Analysis + Negative Testing. Importing a lesson file that includes a class assignment triggers the Master Queue to auto-assign sessions for all class members of that lesson. If staff concurrently adds one of those class students from the Calendar popup while the queue is still running, only one session must exist.

**Preconditions:**
- A lesson import file is prepared with Lesson X assigned to Class A (including Student A)
- Staff User A is about to upload the lesson import file
- Staff User B has the SF Calendar lesson popup for Lesson X open and Student A selected in Add Student popup (not yet submitted)
- Student A does NOT yet have a `student_session` for Lesson X

**Severity:** critical
**Priority:** high

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Staff User A uploads the lesson import file — Lesson X is created with Class A, and the Master Queue is triggered to assign sessions for all class members | Queue job starts; Lesson X created | Lesson import file with Lesson X + Class A |
| 2 | Staff User B clicks **Add** for Student A from the Calendar popup while the queue is still running | Concurrent add submitted | Student A |
| 3 | Wait for the queue to complete | Queue completes without error — the duplicate insert is silently rejected at DB level | - |
| 4 | Count `student_session` records for (Student A, Lesson X) | Exactly **1** record | - |
| 5 | Count `student_session` records for the other class members on Lesson X | Each has exactly **1** record — queue processed them correctly | - |

---

## Suite: Concurrent Add — "This and Following" + Direct Add (Same Time)

### Student Assignment – "This and Following" Running + Another Staff Adds Same Student on a Later Lesson Simultaneously – No Duplicate

**Description:** AC 01 / BR-08 — State Transition Testing + Negative Testing. "This and following" creates sessions across a chain of lessons. If a second staff concurrently adds the same student directly to one of those future lessons at the same moment, only one session must exist on that lesson.

**Preconditions:**
- Recurring lesson chain: Lesson 1 (Jan 1), Lesson 2 (Jan 8), Lesson 3 (Jan 15)
- Student A is not yet assigned to any lesson in the chain
- Staff User A is on Lesson 1 with "This and the following lessons" selected for Student A (not yet submitted)
- Staff User B has Lesson 2 detail page open with Student A selected in Add Student popup (not yet submitted)

**Severity:** major
**Priority:** high

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Staff User A and Staff User B **both click Add at the same moment** | Both requests submitted concurrently: "This and following" for Lessons 1–3, and direct add for Lesson 2 | Student A |
| 2 | Wait for both operations to complete | Both complete without error | - |
| 3 | Count `student_session` records for (Student A, Lesson 1) | Exactly **1** record | - |
| 4 | Count `student_session` records for (Student A, Lesson 2) | Exactly **1** record — not duplicated by the concurrent insert | - |
| 5 | Count `student_session` records for (Student A, Lesson 3) | Exactly **1** record | - |

---

## Suite: Data Integrity After Concurrent Rejection

### Concurrent Add – Duplicate Rejected – LA Lesson Allocated Count Not Double-Incremented

**Description:** AC 01 / BR-19 — CRUD Testing + Regression Analysis. When two concurrent inserts race for the same (student, lesson) slot and the second is rejected, the Lesson Allocation "Lessons Allocated" count must only increment once.

**Preconditions:**
- Student A has an active LA with Lessons Allocated count = **5**
- Student A is not yet assigned to Lesson X
- Two staff sessions are both about to add Student A to Lesson X simultaneously (e.g., Lesson Detail + Calendar)

**Severity:** critical
**Priority:** high

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Note the LA "Lessons Allocated" count for Student A | Count = **5** | - |
| 2 | Two staff submit concurrent Add requests for Student A on Lesson X at the same time | Both requests processed | Student A |
| 3 | Count `student_session` records for (Student A, Lesson X) | Exactly **1** record | - |
| 4 | Check the LA "Lessons Allocated" count for Student A | Count = **6** — incremented exactly **once**, not twice | - |

---

### Concurrent Add – Duplicate Rejected – No Extra Lesson Report Detail Created

**Description:** AC 01 / BR-20 — CRUD Testing + Regression Analysis. When concurrent inserts race and the duplicate is rejected, only one Lesson Report Detail record must be created.

**Preconditions:**
- Student A is not yet assigned to Lesson X
- No Lesson Report Detail exists for (Student A, Lesson X)
- Two staff sessions are both about to add Student A to Lesson X simultaneously

**Severity:** critical
**Priority:** high

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Two staff submit concurrent Add requests for Student A on Lesson X at the same time | Both requests processed | Student A |
| 2 | Count `student_session` records for (Student A, Lesson X) | Exactly **1** record | - |
| 3 | Count `lesson_report_detail` records for (Student A, Lesson X) | Exactly **1** record — not duplicated | - |

---

## Suite: BO Teacher Role — Concurrent Assignment

### Student Assignment – BO Teacher and Full-Access Staff Add Same Student Simultaneously – Only One Session Created

**Description:** AC 01 / BR-03 / F-08 / F-10 — Permission Matrix + Negative Testing. Both BO Teacher and full_access staff roles can assign students. Verifies that concurrent adds from these two different roles also produce exactly one session.

**Preconditions:**
- BO Teacher User A has Lesson X detail open, Student A selected in Add Student popup (not submitted)
- Full-Access Staff User B has the SF Calendar lesson popup open, Student A selected in Add Student popup (not submitted)
- Student A is not yet assigned to Lesson X

**Severity:** critical
**Priority:** high

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Both users click **Add** at the same moment | Both requests submitted concurrently | Student A |
| 2 | Wait for both responses | Both complete without error screens | - |
| 3 | Count `student_session` records for (Student A, Lesson X) | Exactly **1** record | - |

---

## Suite: Reallocation Compatibility

### Reallocate Student – Move to New Lesson – No Constraint Violation, One Session on Target

**Description:** AC 01 / F-15 — CRUD Testing. Reallocation deletes the source session then creates a session on the target lesson. Verifies the new DB constraint does not block the target insert (since source was deleted first).

**Preconditions:**
- Student A is assigned to Lesson X (source) — 1 session exists
- Student A is **not** assigned to Lesson Y (target)

**Severity:** minor
**Priority:** medium

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Initiate reallocation of Student A from Lesson X to Lesson Y | Reallocation form opens | - |
| 2 | Confirm the reallocation | Reallocation completes without error | Lesson Y |
| 3 | Count `student_session` records for (Student A, Lesson X) | **0** records — source session removed | - |
| 4 | Count `student_session` records for (Student A, Lesson Y) | Exactly **1** record on target | - |

---


## Suite: Concurrent Assign — Lesson Detail + Calendar (Same Time)

### Teacher Assignment – Staff Submits via Lesson Detail While Another Staff Submits via Calendar Simultaneously – Only One Teacher Record Created

**Description:** AC 02 / BR-10 / BR-12 — Negative Testing. Simulates two staff members assigning the same teacher to the same lesson from different surfaces at the same moment. Only one `lesson_teacher` record must be created; the second concurrent insert is silently rejected at DB level.

**Preconditions:**
- Staff User A is logged in and has Lesson X detail page open, Add Teacher popup open, Teacher A selected (not yet submitted)
- Staff User B is logged in and has the SF Calendar open, Lesson X popup open, Add Teacher popup open, Teacher A selected (not yet submitted)
- Teacher A is **not yet assigned** to Lesson X

**Severity:** critical
**Priority:** high

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Staff User A and Staff User B **both click Add at the same moment** | Both requests are submitted to the server concurrently | Teacher A on both sessions |
| 2 | Wait for both responses | At least one succeeds; the other is silently ignored — no error screen shown to either user | - |
| 3 | Count `lesson_teacher` records for (Teacher A, Lesson X) | Exactly **1** record | - |
| 4 | Open Lesson X detail page | Teacher A appears **once** in the Lesson Teacher section | - |

---

### Teacher Assignment – Rejected Concurrent Duplicate – Clashing Alert NOT Triggered

**Description:** AC 02 / BR-10 / F-18 — Regression Analysis. When two concurrent teacher inserts race and the second is rejected by the DB constraint, no new teacher record is created — therefore the clashing alert check must NOT fire for the rejected insert.

**Preconditions:**
- Staff User A and Staff User B both submit concurrent Add requests for Teacher A on Lesson X (same time)
- Teacher A is not yet assigned to Lesson X

**Severity:** critical
**Priority:** high

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Both staff submit concurrent Add requests for Teacher A on Lesson X | One insert wins; the other is rejected by the DB constraint | Teacher A |
| 2 | Observe whether a clashing alert or warning dialog appears for either user | No clashing alert is triggered for the rejected insert — because no new teacher record was created | - |
| 3 | Count `lesson_teacher` records for (Teacher A, Lesson X) | Exactly **1** record | - |

---

## Suite: Concurrent Assign — Lesson Import + Manual Add (Same Time)

### Teacher Assignment – Lesson Import Running + Staff Manually Assigns Same Teacher via Lesson Detail Simultaneously – Only One Record Created

**Description:** AC 02 / BR-12 — Regression Analysis + Negative Testing. A lesson import file (which includes teacher assignments) is being processed while another staff member manually assigns the same teacher via the Lesson Detail popup at the same time.

**Preconditions:**
- Lesson X has no teacher assigned yet
- Staff User A is about to upload a lesson import file that includes Teacher A assigned to Lesson X
- Staff User B has Lesson X detail page open with Teacher A selected in the Add Teacher popup (not yet submitted)

**Severity:** major
**Priority:** high

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Staff User A uploads the lesson import file — import starts processing and assigns Teacher A to Lesson X | Import job starts | Lesson import file with Teacher A for Lesson X |
| 2 | Staff User B immediately clicks **Add** for Teacher A in the Lesson Detail popup (before import finishes) | Manual add submitted concurrently with import | Teacher A |
| 3 | Wait for the import to complete | Import completes without unhandled error | - |
| 4 | Count `lesson_teacher` records for (Teacher A, Lesson X) | Exactly **1** record | - |

---

## Suite: Concurrent Assign — "This and Following" + Direct Add (Same Time)

### Teacher Assignment – "This and Following" Running + Another Staff Assigns Same Teacher on a Later Lesson Simultaneously – No Duplicate

**Description:** AC 02 / BR-12 — State Transition Testing + Negative Testing. "This and following" creates teacher assignments across a chain of lessons. If a second staff concurrently assigns the same teacher directly to one of those future lessons at the same moment, only one record must exist on that lesson.

**Preconditions:**
- Recurring lesson chain: Lesson 1 (Jan 1), Lesson 2 (Jan 8), Lesson 3 (Jan 15)
- Teacher A is **not yet assigned** to any lesson in the chain
- Staff User A is on Lesson 1 with "This and the following lessons" selected for Teacher A (not yet submitted)
- Staff User B has Lesson 2 detail page open with Teacher A selected in Add Teacher popup (not yet submitted)

**Severity:** major
**Priority:** high

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Staff User A and Staff User B **both click Add at the same moment** | Both requests submitted concurrently: "This and following" for Lessons 1–3, and direct add for Lesson 2 | Teacher A |
| 2 | Wait for both operations to complete | Both complete without error | - |
| 3 | Count `lesson_teacher` records for (Teacher A, Lesson 1) | Exactly **1** record | - |
| 4 | Count `lesson_teacher` records for (Teacher A, Lesson 2) | Exactly **1** record — not duplicated | - |
| 5 | Count `lesson_teacher` records for (Teacher A, Lesson 3) | Exactly **1** record | - |

---

---


## Suite: [Nichibei] Concurrent Booking — App + Staff (Same Time)

### [Nichibei] Student Books via App While Staff Assigns Same Student via SF Simultaneously – Only One Session Created, No Extra Point Charge

**Description:** AC 01 / BR-09 / BR-21 — CRUD Testing + Regression Analysis. Simulates a Nichibei student tapping Reserve on the app at the exact same moment a staff member assigns that student from SF (Calendar or Lesson Detail). Only one `student_session` must be created and only one point must be consumed.

**Preconditions:**
- Nichibei partner feature is enabled
- Lesson X has Booking Flag = TRUE, date >= today + X days, capacity available, location matches Student A's active LA
- Student A has an active LA with **10** remaining bookable points
- Student A is **not yet assigned** to Lesson X
- Student A is logged in to the student/parent app and has the Reserve button visible for Lesson X
- Staff User is logged in to SF Calendar with the Add Student popup open for Lesson X, Student A selected (not yet submitted)

**Severity:** major
**Priority:** high

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A taps **Reserve** on Lesson X in the app **and** Staff User clicks **Add** for Student A in the Calendar popup at the same moment | Both requests are submitted concurrently | Student A |
| 2 | Wait for both responses | At least one succeeds; the other is silently rejected — no error screen on either side | - |
| 3 | Count `student_session` records for (Student A, Lesson X) | Exactly **1** record | - |
| 4 | Check Student A's remaining bookable points on the LA | Points = **9** — exactly **one** point consumed, not two | - |

---

### [Nichibei] Student Books via App While Class Auto-Assign Queue Runs Simultaneously – Only One Session Created, No Extra Point Charge

**Description:** AC 01 / BR-09 / BR-04 / BR-21 — Regression Analysis. The class auto-assign queue creates sessions for class members while a student simultaneously self-books from the app. If the student is in the class, only one session must be created and only one point charged.

**Preconditions:**
- Nichibei partner feature is enabled
- Lesson X is linked to Class A; Student A is a member of Class A
- Student A has an active LA with **10** remaining bookable points
- Lesson X has Booking Flag = TRUE and is available for self-booking
- Class auto-assign queue for Lesson X has been triggered but **not yet completed**
- Student A has the Reserve button visible in the app

**Severity:** major
**Priority:** high

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A taps **Reserve** on Lesson X while the class auto-assign queue is still running | The booking request races with the queue's session insert for Student A | Student A |
| 2 | Wait for the queue to complete | Queue completes without error | - |
| 3 | Count `student_session` records for (Student A, Lesson X) | Exactly **1** record | - |
| 4 | Check Student A's remaining bookable points | Points = **9** — only one point consumed (whichever insert won) | - |

---

### [Nichibei] Atomic Booking – Concurrent Insert Causes Mid-Flow Rejection – No Orphaned Data

**Description:** AC 01 / BR-09 / F-06 — Regression Analysis. The Nichibei atomic booking flow is: validate → create session → save remarks → auto-publish. If a concurrent insert (staff or queue) wins the race and the app's session insert is rejected mid-flow, the entire booking must be rolled back atomically — no orphaned session, remark, or premature publish.

**Preconditions:**
- Nichibei partner feature is enabled
- Lesson X is a Draft lesson, Booking Flag = TRUE
- Student A has a valid active LA with 10 available points
- Student A is logged in and has Reserve visible for Lesson X
- Staff User is on SF Calendar, Add Student popup open, Student A selected, about to submit at the same time Student A taps Reserve

**Severity:** major
**Priority:** high

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Student A taps **Reserve** on Lesson X **and** Staff User clicks **Add** simultaneously | Both requests submitted; the staff-side insert wins the race; the app-side insert is rejected mid-flow by the DB constraint | - |
| 2 | Check `student_session` records for (Student A, Lesson X) | Exactly **1** record (the staff-assigned session) | - |
| 3 | Check `attendance_response_remark` for (Student A, Lesson X) | No "Booking Note:" remark was created (app booking rolled back before the remark step) | - |
| 4 | Check the publish status of Lesson X | Lesson X remains **Draft** — it was NOT auto-published (app booking rolled back before auto-publish) | - |
| 5 | Check Student A's remaining bookable points | Points remain at **10** — no point consumed for the rejected app booking | - |

---

---


## Suite: Student Reallocation — Constraint Compatibility

### Reallocate Student – Move to New Lesson – No Constraint Violation, One Session on Target

**Description:** AC 01 / F-15 — CRUD Testing. Reallocation deletes the source session then creates a session on the target lesson. Verifies the DB unique constraint does not block the target insert since the source was deleted first.

**Preconditions:**
- Student A is assigned to Lesson X (source) — 1 `student_session` exists
- Student A is **not** assigned to Lesson Y (target)

**Severity:** minor
**Priority:** medium

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Navigate to the reallocation flow for Student A | Reallocation screen opens with Lesson X as the current lesson | - |
| 2 | Select Lesson Y as the target lesson and confirm | Reallocation completes without error | Lesson Y |
| 3 | Count `student_session` records for (Student A, Lesson X) | **0** records — source session removed | - |
| 4 | Count `student_session` records for (Student A, Lesson Y) | Exactly **1** record on target | - |

---

### Reallocate Student – Staff Reallocates While Another Staff Concurrently Assigns Same Student to Target Lesson – Only One Session on Target

**Description:** AC 01 / F-15 — Negative Testing. Concurrent scenario: Staff A reallocates Student A to Lesson Y, while Staff B is simultaneously directly assigning Student A to Lesson Y. Only one session must exist on Lesson Y after both complete.

**Preconditions:**
- Student A is assigned to Lesson X (source)
- Student A is **not** assigned to Lesson Y (target)
- Staff User A is about to confirm reallocation of Student A to Lesson Y (not yet submitted)
- Staff User B has Lesson Y detail page open with Student A selected in Add Student popup (not yet submitted)

**Severity:** minor
**Priority:** medium

| # | Action | Expected Result | Test Data |
|---|--------|-----------------|-----------|
| 1 | Staff User A confirms the reallocation to Lesson Y **and** Staff User B clicks **Add** for Student A on Lesson Y at the same moment | Both requests submitted concurrently | Student A / Lesson Y |
| 2 | Wait for both to complete | Both complete without unhandled errors | - |
| 3 | Count `student_session` records for (Student A, Lesson Y) | Exactly **1** record — not duplicated | - |
