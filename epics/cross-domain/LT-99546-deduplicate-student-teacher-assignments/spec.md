# Spec: LT-99546 — Duplicate Students and Teachers Assignment Improvement

**Ticket:** [LT-99546](https://manabie.atlassian.net/browse/LT-99546)  
**Feature Name:** Deduplicate Student and Teacher Assignments  
**Module:** lesson-management  
**Epic Status:** Ready for QA  
**Priority:** Medium  
**Partner Scope:** All partners (Core issue — not Aso-specific)  
**Reporter:** The Khuong Dang | **Assignee:** Tran Quoc Bao  
**Created:** 2026-04-15 | **Updated:** 2026-05-05  
**Analysis Date:** 2026-05-12

---

## Summary

Root cause: on SF Calendar, creating a lesson with a class of 35 active students, then manually adding one of those same students on the Calendar lesson popup → duplicate Student Session created. The same race condition applies to Teacher assignments. This resulted in **1,655 duplicate records** first observed on Aso 2026-04-07, but the issue is a **Core problem that affects all partners**.

**Fix approach (LT-99548 — Done):**  
DB-level unique key constraint added for `(student_id, lesson_id)` and `(teacher_id, lesson_id)` composite keys.

- Error handling is **code-level only** — no UI error message is shown to the user.
- From a QA perspective, the goal is to verify that **no duplicate data is created** through any assignment flow.
- The fix is transparent to the user: flows complete normally; duplicate inserts are silently rejected at the DB layer.

**QA Focus:** Verify that **all student & teacher assignment flows** cannot produce duplicate `student_session` or `lesson_teacher` records.

**Out of scope for this QA cycle:**

- [MED] Bulk Action Queue for importing lessons / assigning students — handle later
- [MED] Notification when async processing is done — handle later

---

## Acceptance Criteria

| ID    | Summary                                                                                                                                                                               | Status                           |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| AC 01 | DB-level unique key for `(student_id, lesson_id)` — any flow attempting to create a duplicate Student Session is silently rejected at DB level; **no duplicate record created**       | **In Scope (Done via LT-99548)** |
| AC 02 | DB-level unique key for `(teacher_id, lesson_id)` — any flow attempting to create a duplicate Lesson Teacher record is silently rejected at DB level; **no duplicate record created** | **In Scope (Done via LT-99548)** |
| AC 03 | [MED] Bulk Action Queue for importing lessons / assigning students                                                                                                                    | **OUT OF SCOPE — handle later**  |
| AC 04 | [MED] Notification when bulk/async job completes                                                                                                                                      | **OUT OF SCOPE — handle later**  |

---

## Business Rules

### Student Session (AC 01)

| ID    | Rule                                                                                                                                                                                                                                             | Field                                                | Platform    | Condition                                                |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------- | ----------- | -------------------------------------------------------- |
| BR-01 | A Student Session record must be unique for the `(student_id, lesson_id)` composite key. The DB enforces this via unique constraint. Error handling is code-level — **no UI message shown to user**.                                             | Student Session                                      | SF          | Always — for any flow                                    |
| BR-03 | Duplicate prevention applies to: **Add Student (manual)** on Lesson Detail page.                                                                                                                                                                 | Add Student button (Lesson Detail)                   | SF          | When student already assigned                            |
| BR-04 | Duplicate prevention applies to: **Class-based auto-assignment** (via class member assignment, lesson creation with class, import class members, update LA duration, update lesson schedule class) — runs as background Master Queue.            | Class-based auto-assign (Master Queue)               | SF          | When queue generates already-existing session            |
| BR-05 | Duplicate prevention applies to: **Add Student from Calendar** (SF Calendar → Lesson Detail popup → Student List → Add). This is the **confirmed root cause flow**.                                                                              | Add Student from Calendar                            | SF          | When student already assigned                            |
| BR-08 | Duplicate prevention applies to: **"This and following"** recurring student assignment. Existing behavior preserved: if a student is already assigned to some lessons in the chain, those lessons are silently skipped (no error shown to user). | Assign student — This and following                  | SF          | When some lessons in chain already have student assigned |
| BR-09 | Duplicate prevention applies to: **Nichibei Lesson Booking** self-booking flow (app-initiated Student Session creation).                                                                                                                         | Lesson Booking (Nichibei) — Student Session creation | SF / Mobile | When student already has session for same lesson         |
| BR-14 | For async/background flows (Master Queue), duplicate inserts are **silently skipped** at DB level — must NOT cause the entire queue job to fail.                                                                                                 | Background auto-assign queue error handling          | SF          | When queue encounters already-existing session           |
| BR-17 | NEGATIVE: Staff creates lesson with class (35 students) → manually adds same student via Calendar → **no second session must be created**.                                                                                                       | Manual add after class auto-assign                   | SF          | Original incident root cause                             |
| BR-18 | NEGATIVE: Concurrent dual-path creation — manual Add Student (on Calendar) + class import auto-assign running at the same time for overlapping (student, lesson) pairs → only **ONE session** created; duplicate insert silently rejected at DB. | Concurrent dual-path session creation                | SF          | Known root cause 2026-04-07                              |
| BR-19 | LA Lesson Allocated count must NOT be double-incremented when a duplicate is rejected. Only successful session creations update the count.                                                                                                       | LA Lesson Allocated count                            | SF          | When duplicate session rejected                          |
| BR-20 | Lesson Report Detail must NOT be created for a rejected duplicate session. Only successful session creations create a Lesson Report Detail.                                                                                                      | Lesson Report Detail                                 | SF          | When duplicate session rejected                          |
| BR-21 | For Nichibei: point consumption must NOT be double-charged when a duplicate student booking is rejected. A rejected student session insert must NOT trigger a point charge.                                                                      | Point Consumption (Nichibei)                         | SF / Mobile | When duplicate student session rejected for Nichibei     |

### Lesson Teacher (AC 02)

| ID    | Rule                                                                                                                                                                                                         | Field                             | Platform | Condition                                    |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------- | -------- | -------------------------------------------- |
| BR-10 | A Lesson Teacher record must be unique for the `(teacher_id, lesson_id)` composite key. DB enforces via unique constraint. Error handling is code-level only.                                                | Lesson Teacher                    | SF       | Always — for any flow                        |
| BR-12 | Teacher duplicate prevention applies to all creation flows: Assign teacher on Lesson Detail, Assign teacher from Calendar, Import lessons with teacher assignments, "This and following" teacher assignment. | All Lesson Teacher creation flows | SF       | When teacher already assigned to that lesson |

### Bulk Action Queue / Notification (AC 03 / AC 04 — OUT OF SCOPE)

> AC 03 and AC 04 are out of scope for this QA cycle. No test cases will be written for these items.

---

## Conflict & Gap Analysis

**Active findings: 8** (10 removed as resolved by Q&A)  
CONFLICT: 0 | REGRESSION_RISK: 2 | UNDOCUMENTED: 1 | ROLE_GAP: 1 | LESSON_LEARNED_RISK: 1 | EXTENDED: 2 | DATA_INTEGRITY: 2

| ID   | Tag                   | AC                    | Finding                                                                                                                                                                                                                          | Field                                                   |
| ---- | --------------------- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| F-04 | [DATA_INTEGRITY]      | AC 01 / BR-19         | LA Lesson Allocated count may increment BEFORE session insert. If insert fails on duplicate, count could be wrong. Transaction boundary not confirmed.                                                                           | LA count — integrity on duplicate rejection             |
| F-05 | [DATA_INTEGRITY]      | AC 01 / BR-20         | Lesson Report Detail auto-created on session creation. Risk of orphaned/duplicate report detail if transactional boundary is not atomic.                                                                                         | Lesson Report Detail — integrity on duplicate rejection |
| F-06 | [REGRESSION RISK]     | AC 01                 | Nichibei atomic booking: validate → create Student Session → save remarks → auto-publish. Dedup constraint may silently reject an already-booked session in a retry scenario, creating orphaned booking data.                    | Nichibei Lesson Booking atomic flow                     |
| F-07 | [REGRESSION RISK]     | AC 01                 | Bulk Publish Lessons (LT-98532) queries student sessions for bulk operations. If sessions were previously duplicated and are now deduplicated, bulk publish counts may change.                                                   | Bulk Publish — student count integrity                  |
| F-08 | [UNDOCUMENTED IN AC]  | AC 01                 | BO teacher role (bo_teacher = TRUE for student assign) can trigger student assignment. QA must verify BO teacher cannot create duplicate student sessions (same data integrity rule).                                            | BO teacher student assignment                           |
| F-10 | [ROLE GAP]            | AC 01 / AC 02         | bo_teacher = FALSE for teacher assignment. All 3 roles can trigger student assignment but only full_access/center_level_edit can assign teachers. Dedup must cover all roles for student, but teacher dedup only covers 2 roles. | Role coverage — student (3 roles) vs. teacher (2 roles) |
| F-11 | [LESSON-LEARNED RISK] | AC 01 / BR-17 / BR-18 | Original incident (2026-04-07: concurrent bulk manual + class-import auto-assign → 1,655 duplicates) was a **Core issue affecting all partners** — not Aso-specific. Must be explicitly regression-tested for all partners.      | Dual-path concurrent creation — Core regression         |
| F-15 | [EXTENDED]            | AC 01                 | Reallocation (move student between lessons): delete session + create new session. New DB constraint must NOT block the new session creation for the target lesson.                                                               | Reallocation — unique constraint compatibility          |
| F-18 | [EXTENDED]            | AC 02                 | Clashing alert fires AFTER teacher assignment. Rejected duplicate (DB constraint) should NOT trigger clashing alert — no new assignment = no new clash to check.                                                                 | Clashing alert — not triggered on rejected duplicate    |

**Removed findings (resolved by Q&A):**

| ID   | Tag                   | Reason removed                                                                                                                |
| ---- | --------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| F-01 | [CONFLICT]            | "This and following" app-level skip — confirmed: behavior preserved as silent skip. No visible error to user. Same as before. |
| F-02 | [MISSING BEHAVIOR]    | Error message UX — confirmed: code-level only, no UI message. Not a QA concern.                                               |
| F-03 | [MISSING BEHAVIOR]    | Master Queue error handling — Q-02: ignore.                                                                                   |
| F-09 | [UNDOCUMENTED]        | MED items (AC 03/04) — confirmed out of scope for this cycle.                                                                 |
| F-12 | [LESSON-LEARNED RISK] | Nichibei points — merged into F-06 (Nichibei regression) and BR-21.                                                           |
| F-13 | [CONFLICT]            | School Tomas (LT-99479) — confirmed not related to this ticket.                                                               |
| F-14 | [MISSING BEHAVIOR]    | Calendar Add Student UI error — confirmed: just verify no duplicate. No specific UI to check.                                 |
| F-16 | [MISSING BEHAVIOR]    | CSV import — confirmed: import completes normally, async job assigns. Captured in BR-06.                                      |
| F-17 | [REGRESSION RISK]     | "This and following" UX change — confirmed no UX change (no visible error). Same as F-01 resolution.                          |

---

## Clarification Questions

**Status: ✅ All resolved — NOT posted to Jira**

| ID   | Tag                   | Question                                                                | Resolution                                                                                                                   |
| ---- | --------------------- | ----------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| Q-01 | [MISSING BEHAVIOR]    | What exact error message / UI placement is shown on duplicate?          | **Error is code-level only. No UI message shown to user. QA verifies no duplicate data is created.**                         |
| Q-02 | [MISSING BEHAVIOR]    | Master Queue on duplicate: skip-and-continue or fail-entire-job?        | **Ignore — out of QA scope.**                                                                                                |
| Q-03 | [CONFLICT]            | "This and following": app-level skip still exists after DB constraint?  | **Behavior preserved. No visible error to user. QA verifies no duplicate at data level.**                                    |
| Q-04 | [MISSING BEHAVIOR]    | Are MED items (Bulk Queue + Notification) in scope for this QA cycle?   | **Out of scope — handle later. AC 03/AC 04 removed from test scope.**                                                        |
| Q-05 | [MISSING BEHAVIOR]    | Calendar Add Student: grayed out (blocked) or error after clicking Add? | **Just verify student is not duplicated. No specific UI behavior requirement.**                                              |
| Q-06 | [MISSING BEHAVIOR]    | CSV import: skip / fail / silent skip?                                  | **Import is unaffected (completes normally). Background async job assigns students after — dedup constraint applies there.** |
| Q-07 | [ROLE GAP]            | BO teacher: same error as SF staff?                                     | **Just verify teacher/student is not duplicated. Same data integrity rule.**                                                 |
| Q-08 | [CONFLICT]            | Aso (LT-99548) same implementation as School Tomas (LT-99479)?          | **Not related.**                                                                                                             |
| Q-09 | [LESSON-LEARNED RISK] | Regression test for original Aso scenario planned?                      | **This is a Core issue affecting ALL partners — not Aso-specific. Must be in Core regression suite.**                        |

---

## Related Specs

| File                                                                     | Relevance                                                                                         |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------- |
| `input/specs/LT-98532: Bulk Publish Lessons by Student/spec.md`          | References Aso duplicate sessions incident; bulk publish queries student sessions                 |
| `input/specs/LT-96620 Nichibei App - Lesson Booking System/spec.md`      | Third Student Session creation path (app booking); duplicate validation race condition documented |
| `input/specs/LT-96673 Monthly Lesson Count in Add Teacher Popup/spec.md` | References Aso duplicate sessions in teacher context                                              |

---

## Related Test Cases

| Path                                                               | Relevance                                                                      |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| `output/test-cases/lesson-management/student-session/`             | Existing student session test cases — must be reviewed for regression coverage |
| `output/test-cases/lesson-management/lesson-teacher/`              | Existing teacher assignment test cases — must be reviewed for regression       |
| `output/test-coverages/LT-96620-nichibei-lesson-booking-system.md` | AC 03.3 — Duplicate allocation risk already noted                              |

---

## Qase Coverage Gaps

| Gap  | Description                                                                                                                              |
| ---- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| G-01 | No existing test case covers the confirmed root cause: Calendar → class lesson → add same student manually → verify no duplicate session |
| G-02 | No test case covers concurrent dual-path creation (Master Queue auto-assign + manual Add Student simultaneously) — Core regression       |
| G-03 | No test case covers LA count integrity when duplicate session is rejected                                                                |
| G-04 | No test case covers Lesson Report Detail integrity when duplicate session is rejected                                                    |
| G-05 | No test case covers CSV import with duplicate rows (async assignment dedup)                                                              |
| G-06 | No test case covers teacher duplicate from Calendar (same principle as student)                                                          |
| G-06 | No test case covers Nichibei booking when student already assigned via SF (point consumption integrity)                                  |
| G-07 | No test case covers Reallocation flow compatibility with unique constraint                                                               |

---

## Student & Teacher Assignment Flow Inventory

> All flows that create Student Sessions or Lesson Teacher records — all must be covered by the dedup fix.  
> **QA verification method:** After triggering each flow with a pre-existing (student/teacher, lesson) pair, verify via data check that only **ONE record** exists in the DB.

### Student Session Creation Flows (AC 01 scope)

| #    | Flow                                                  | Entry Point          | Sync/Async        | Test Priority                       |
| ---- | ----------------------------------------------------- | -------------------- | ----------------- | ----------------------------------- |
| S-01 | Add Student manually — Lesson Detail page             | SF BO                | Sync              | Critical                            |
| S-02 | **Add Student from Calendar — Lesson popup**          | SF Calendar          | Sync              | **Critical — confirmed root cause** |
| S-03 | Class-based auto-assign on lesson creation with class | Master Queue         | Async             | Critical                            |
| S-04 | Class member import → auto-assign to active lessons   | Master Queue         | Async             | High                                |
| S-05 | Update LA duration → auto-recalculate sessions        | Master Queue         | Async             | High                                |
| S-06 | Update lesson schedule class → re-assign              | Master Queue         | Async             | High                                |
| S-07 | "This and following" recurring assignment             | SF Lesson Detail     | Sync (multi-step) | High                                |
| S-08 | Nichibei app self-booking                             | Mobile App           | Sync              | High                                |
| S-09 | Reallocation (move student to another lesson)         | SF Lesson Detail     | Sync              | Medium                              |
| S-10 | BO Teacher assigns student                            | SF (BO Teacher role) | Sync              | Medium                              |

### Lesson Teacher Creation Flows (AC 02 scope)

| #    | Flow                                               | Entry Point      | Sync/Async        | Test Priority |
| ---- | -------------------------------------------------- | ---------------- | ----------------- | ------------- |
| T-01 | Assign teacher — Lesson Detail page                | SF BO            | Sync              | Critical      |
| T-02 | Assign teacher from Calendar — Lesson popup        | SF Calendar      | Sync              | Critical      |
| T-03 | Import lessons with teacher assignments (CSV/bulk) | SF Import        | Sync/Batch        | High          |
| T-04 | "This and following" teacher assignment            | SF Lesson Detail | Sync (multi-step) | High          |
| T-05 | Class-based teacher auto-assign (if applicable)    | Master Queue     | Async             | Medium        |
