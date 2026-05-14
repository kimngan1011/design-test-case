# Test Coverage: LT-99546 — Deduplicate Student and Teacher Assignments

**Jira:** https://manabie.atlassian.net/browse/LT-99546  
**Date:** 2026-05-12

---

## 1. Business Rules Extracted

| #   | AC    | Business Rule                                                                                                                                                                     |
| --- | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | AC 01 | BR-01: Student Session `(student_id, lesson_id)` must be unique — DB unique constraint, code-level error handling only, no UI message                                             |
| 2   | AC 01 | BR-03: Duplicate prevention applies to Add Student (manual) on Lesson Detail page                                                                                                 |
| 3   | AC 01 | BR-04: Duplicate prevention applies to Class-based auto-assign (Master Queue) — lesson creation with class, class member import, update LA duration, update lesson schedule class |
| 4   | AC 01 | BR-05: Duplicate prevention applies to Add Student from Calendar — the confirmed root cause flow                                                                                  |
| 5   | AC 01 | BR-08: Duplicate prevention applies to "This and following" recurring student assignment — existing silent-skip behavior preserved                                                |
| 6   | AC 01 | BR-09: Duplicate prevention applies to Nichibei Lesson Booking self-booking flow                                                                                                  |
| 7   | AC 01 | BR-14: Master Queue async flows silently skip duplicates — must NOT fail the entire queue job                                                                                     |
| 8   | AC 01 | BR-17 (negative): Class lesson (35 students) created → same student manually added via Calendar → no second session created                                                       |
| 9   | AC 01 | BR-18 (negative): Concurrent dual-path creation (Calendar manual add + class import auto-assign) → only ONE session created                                                       |
| 10  | AC 01 | BR-19: LA Lesson Allocated count must NOT double-increment when duplicate session is rejected                                                                                     |
| 11  | AC 01 | BR-20: Lesson Report Detail must NOT be created for a rejected duplicate session                                                                                                  |
| 12  | AC 01 | BR-21: Nichibei point consumption must NOT be charged when a duplicate student booking is rejected                                                                                |
| 13  | AC 02 | BR-10: Lesson Teacher `(teacher_id, lesson_id)` must be unique — DB unique constraint, code-level only                                                                            |
| 14  | AC 02 | BR-12: Teacher duplicate prevention applies to all flows: Lesson Detail, Calendar, import, This and following                                                                     |

---

## 2. Logic Type Categorization

| AC    | Business Rule # | Logic Type                                             |
| ----- | --------------- | ------------------------------------------------------ |
| AC 01 | 1 (BR-01)       | Data integrity, Cross-system impact                    |
| AC 01 | 2 (BR-03)       | Data integrity, Conditional logic                      |
| AC 01 | 3 (BR-04)       | Data integrity, Conditional logic, Cross-system impact |
| AC 01 | 4 (BR-05)       | Data integrity, Conditional logic                      |
| AC 01 | 5 (BR-08)       | Data integrity, Recurrence logic, Conditional logic    |
| AC 01 | 6 (BR-09)       | Data integrity, Conditional logic, Cross-system impact |
| AC 01 | 7 (BR-14)       | Data integrity, Conditional logic                      |
| AC 01 | 8 (BR-17)       | Data integrity, Conditional logic                      |
| AC 01 | 9 (BR-18)       | Data integrity, Conditional logic                      |
| AC 01 | 10 (BR-19)      | Data integrity, Cross-system impact                    |
| AC 01 | 11 (BR-20)      | Data integrity, Cross-system impact                    |
| AC 01 | 12 (BR-21)      | Data integrity, Cross-system impact                    |
| AC 02 | 13 (BR-10)      | Data integrity, Cross-system impact                    |
| AC 02 | 14 (BR-12)      | Data integrity, Conditional logic, Cross-system impact |

---

## 3. Test Technique Selection

| Logic Type          | Applicable Techniques                             |
| ------------------- | ------------------------------------------------- |
| Data integrity      | CRUD Testing, Regression Analysis, Decision Table |
| Conditional logic   | Decision Table, Negative Testing                  |
| Recurrence logic    | State Transition Testing, Regression Analysis     |
| Cross-system impact | Regression Analysis, CRUD Testing                 |
| Permission logic    | Permission Matrix, Decision Table                 |

---

## 4. Structured Coverage Strategy

| AC    | Business Rule Summary                                                                            | Logic Type                          | Test Technique                                | Risk Level | Coverage Depth |
| ----- | ------------------------------------------------------------------------------------------------ | ----------------------------------- | --------------------------------------------- | ---------- | -------------- |
| AC 01 | BR-03: Add Student (manual) on Lesson Detail — no duplicate session created                      | Data integrity                      | CRUD Testing, Negative Testing                | Critical   | Deep           |
| AC 01 | BR-05: Add Student from Calendar — no duplicate session created (root cause flow)                | Data integrity                      | CRUD Testing, Negative Testing                | Critical   | Deep           |
| AC 01 | BR-04: Class-based auto-assign (Master Queue) — no duplicate session created                     | Data integrity, Cross-system impact | CRUD Testing, Regression Analysis             | Critical   | Deep           |
| AC 01 | BR-17: Class lesson → manual add same student via Calendar → no second session                   | Data integrity, Conditional logic   | Negative Testing, Decision Table              | Critical   | Deep           |
| AC 01 | BR-18: Concurrent dual-path (Calendar manual + auto-assign) → only one session                   | Data integrity, Conditional logic   | Negative Testing, Decision Table              | Critical   | Deep           |
| AC 01 | BR-08: "This and following" — student already assigned in chain → silently skipped, no duplicate | Data integrity, Recurrence logic    | State Transition Testing, Regression Analysis | High       | Standard       |
| AC 01 | BR-09: Nichibei self-booking — student already assigned via SF → no duplicate session            | Data integrity, Cross-system impact | CRUD Testing, Regression Analysis             | High       | Standard       |
| AC 01 | BR-14: Master Queue encounters duplicate → skips silently, job does not fail                     | Data integrity, Conditional logic   | Regression Analysis, Negative Testing         | High       | Standard       |
| AC 01 | BR-19: LA Lesson Allocated count — no double-increment when duplicate rejected                   | Data integrity, Cross-system impact | CRUD Testing, Regression Analysis             | Critical   | Deep           |
| AC 01 | BR-20: Lesson Report Detail — not created for rejected duplicate session                         | Data integrity, Cross-system impact | CRUD Testing, Regression Analysis             | Critical   | Deep           |
| AC 01 | BR-21: Nichibei point consumption — not charged for rejected duplicate booking                   | Data integrity, Cross-system impact | CRUD Testing, Regression Analysis             | High       | Standard       |
| AC 02 | BR-10: Assign Teacher on Lesson Detail — no duplicate teacher record created                     | Data integrity                      | CRUD Testing, Negative Testing                | Critical   | Deep           |
| AC 02 | BR-12: All teacher creation flows (Calendar, import, This and following) — no duplicate          | Data integrity, Conditional logic   | Decision Table, Regression Analysis           | Critical   | Deep           |

> **Note on BO Teacher role (F-10):** bo_teacher can assign students (TRUE) but not teachers (FALSE). Student dedup tests must include BO Teacher role as an additional test path. Teacher dedup is only for full_access / center_level_edit roles.

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area                                        | Reason                                                                                                                                        | Recommended Approach                                                                                                                 |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Add Student from Calendar (BR-05 / BR-17)   | This is the **confirmed root cause** of the 2026-04-07 incident — 1,655 duplicates. Must be verified as definitively fixed.                   | Create lesson with class → attempt to add the same student via Calendar popup → verify DB has exactly 1 `student_session` record.    |
| Concurrent dual-path creation (BR-18)       | Race condition between manual Calendar add + class-import auto-assign. Fix only works if the DB constraint fires correctly under concurrency. | Trigger both paths simultaneously for the same (student, lesson) pair. Verify exactly 1 record in DB after both operations complete. |
| LA Lesson Allocated count integrity (BR-19) | If LA count increments before session insert and the insert fails, the count is permanently wrong. This is a silent data integrity issue.     | Add student that is already assigned → check that LA `lessons_allocated` count does NOT change after the duplicate is rejected.      |
| Lesson Report Detail integrity (BR-20)      | An orphaned Lesson Report Detail (no matching session) would cause UI anomalies in lesson reports and break reporting.                        | Add student that is already assigned → verify no new `lesson_report_detail` row is created.                                          |

### 🟠 High Risk

| Area                                                   | Reason                                                                                                                               | Recommended Approach                                                                                                                                                                  |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Class-based auto-assign (Master Queue) (BR-04 / BR-14) | The root cause involved the Master Queue creating sessions concurrently with manual add. Queue must skip duplicates without failing. | Create lesson with class → then add one of those students manually first → re-trigger class-based auto-assign → verify the already-assigned student is not duplicated.                |
| "This and following" recurring assignment (BR-08)      | Existing silent-skip behavior must not be broken. A regression here would cause visible duplicates on all following lessons.         | Assign student to a lesson → use "This and following" to assign same student from an earlier lesson in the chain → verify all future lessons have exactly 1 session for this student. |
| Nichibei point consumption (BR-21)                     | A spurious point charge on a rejected duplicate would be a billing error for Nichibei partners.                                      | Attempt duplicate Nichibei booking for a student already assigned via SF → verify no extra point is consumed.                                                                         |

### 🟡 Medium Risk

| Area                                                 | Reason                                                                                                                                                    | Recommended Approach                                                                                                      |
| ---------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Nichibei self-booking regression (BR-09 / F-06)      | The Nichibei atomic booking flow (validate → session → remarks → publish) may behave unexpectedly if the dedup constraint fires mid-flow.                 | Book via Nichibei app for a student already assigned → verify booking is blocked cleanly with no orphaned booking record. |
| Reallocation compatibility (F-15)                    | Reallocation involves delete + create session. The new DB constraint must not block the new session for the target lesson if the old session was deleted. | Reallocate student from lesson A to lesson B → verify session exists on B, does not exist on A, and no duplicate on B.    |
| Clashing alert regression (F-18)                     | Teacher clashing alert fires after assignment. Rejected duplicate teacher insert must not trigger false clash alert.                                      | Attempt to add already-assigned teacher → verify clashing alert is NOT triggered.                                         |
| BO Teacher role for student assignment (F-08 / F-10) | BO Teacher can trigger student assignment but AC does not explicitly cover this role. Must ensure same dedup rules apply.                                 | Login as BO Teacher → add student to a lesson where that student is already assigned → verify no duplicate session.       |

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area                                                      | Existing Test Case                                                     | Overlap                                   | New Coverage Needed                                                                                                              |
| ------------------------------------------------------------- | ---------------------------------------------------------------------- | ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Add Student from Calendar → duplicate (BR-05 / BR-17)         | None                                                                   | None                                      | ✅ New: verify no duplicate when student already assigned via class auto-assign, then manually added from Calendar               |
| Concurrent dual-path creation (BR-18)                         | None                                                                   | None                                      | ✅ New: trigger Calendar manual add + class-import auto-assign simultaneously for same (student, lesson) pairs → verify 1 record |
| LA count integrity on duplicate rejection (BR-19)             | TC-10533 (covers LA update on successful assign)                       | Partial — covers positive path only       | ✅ New: verify LA count does NOT change when duplicate session is rejected                                                       |
| Lesson Report Detail integrity on duplicate rejection (BR-20) | TC-10533 (covers report detail creation on successful assign)          | Partial — covers positive path only       | ✅ New: verify no new lesson_report_detail when duplicate session rejected                                                       |
| Add Student (Lesson Detail) → duplicate (BR-03)               | TC-1261 (covers popup display, filters)                                | Partial — no dedup test                   | ✅ New: verify Add Student popup cannot add an already-assigned student twice                                                    |
| Class auto-assign queue → duplicate (BR-04 / BR-14)           | TC-10533, TC-10534 (cover assignment via class, check session created) | Partial — no duplicate path               | ✅ New: verify queue silently skips already-assigned student, does not create duplicate                                          |
| "This and following" — no duplicate (BR-08)                   | None found for this specific path                                      | None                                      | ✅ New: assign same student via "This and following" when already assigned on some lessons → verify no duplicate                 |
| Nichibei self-booking → duplicate (BR-09 / BR-21)             | TC-14942–TC-14945 (Nichibei lesson number assignment)                  | None — covers different flow              | ✅ New: book via Nichibei app for student already assigned via SF → verify no duplicate, no extra point charge                   |
| Teacher duplicate — Lesson Detail (BR-10 / BR-12)             | TC-1214 (covers popup display)                                         | Partial — no dedup test                   | ✅ New: attempt to assign already-assigned teacher on Lesson Detail → verify no duplicate teacher record                         |
| Teacher duplicate — Calendar (BR-12)                          | None                                                                   | None                                      | ✅ New: attempt to assign already-assigned teacher from Calendar → verify no duplicate                                           |
| Teacher duplicate — "This and following" (BR-12)              | None                                                                   | None                                      | ✅ New: assign same teacher via "This and following" when already assigned on some lessons → verify no duplicate                 |
| Reallocation compatibility (F-15)                             | None                                                                   | None                                      | ✅ New: reallocate student → verify correct single session on target lesson, no constraint violation                             |
| Clashing alert not triggered on rejected duplicate (F-18)     | clashing-alert.md (covers normal clashing scenarios)                   | Partial — no duplicate rejection scenario | ✅ New: rejected duplicate teacher insert must not trigger clashing alert                                                        |
| BO Teacher role — student dedup (F-08 / F-10)                 | None                                                                   | None                                      | ✅ New: BO Teacher adds already-assigned student → verify no duplicate                                                           |

---

## 7. Suggested Suite Structure

```
output/test-cases/lesson-management/student-session/
  ├── dedup-student-session.md
  │     → AC 01 — All student session dedup test cases:
  │       - Add Student (Lesson Detail) → duplicate check
  │       - Add Student (Calendar) → duplicate check (root cause flow)
  │       - Class-based auto-assign (Master Queue) → duplicate check
  │       - "This and following" → duplicate check
  │       - Concurrent dual-path (root cause scenario)
  │       - LA count integrity on duplicate rejection
  │       - Lesson Report Detail integrity on duplicate rejection
  │       - BO Teacher role → student duplicate check

output/test-cases/lesson-management/student-session/
  ├── dedup-nichibei-booking.md
  │     → AC 01 (Nichibei) — Nichibei-specific dedup test cases:
  │       - Nichibei self-booking → student already assigned via SF
  │       - Point consumption integrity on rejected duplicate

output/test-cases/lesson-management/lesson-teacher/
  ├── dedup-lesson-teacher.md
  │     → AC 02 — All teacher assignment dedup test cases:
  │       - Add Teacher (Lesson Detail) → duplicate check
  │       - Add Teacher (Calendar) → duplicate check
  │       - "This and following" teacher assignment → duplicate check
  │       - Clashing alert NOT triggered on rejected duplicate

output/test-cases/lesson-management/student-session/
  ├── dedup-reallocation.md
  │     → AC 01 (extended) — Reallocation compatibility:
  │       - Move student to another lesson → no constraint violation, correct single session
```
