# Test Coverage: LT-90573 — Extend Recurring Lesson Settings

**Jira:** https://manabie.atlassian.net/browse/LT-90573
**Date:** 2026-03-04

---

## 1. Business Rules Extracted

| #   | AC               | Business Rule                                                                                                                                                                             |
| --- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | AC 01.1          | "Extend Recurrence" button is available on Lesson Schedule detail page                                                                                                                    |
| 2   | AC 01.1          | Clicking the button opens the Lesson Creation Form                                                                                                                                        |
| 3   | AC 01.1          | User can only review and update allowed fields                                                                                                                                            |
| 4   | AC 01.2          | Start Time, End Time, Duration, Teaching Medium, Lesson Name → pre-filled & editable (from Lesson Schedule)                                                                               |
| 5   | AC 01.2          | Classroom → searchable dropdown, user selects from available classrooms                                                                                                                   |
| 6   | AC 01.2          | Day of the Week → auto-calculated from Lesson Date                                                                                                                                        |
| 7   | AC 01.2          | Date → auto-calculated: current end date + 7 days                                                                                                                                         |
| 8   | AC 01.2          | Lesson Code → auto-calculated: last existing lesson code + 1 for each new lesson                                                                                                          |
| 9   | AC 01.2          | Lesson Type → default "Regular", editable                                                                                                                                                 |
| 10  | AC 01.2          | Lesson Capacity → blank, optional                                                                                                                                                         |
| 11  | AC 01.2          | Location, Academic Year, Course, Class, Teaching Method → locked (non-editable)                                                                                                           |
| 12  | AC 01.2          | Recurrence Type → display saved value, not editable                                                                                                                                       |
| 13  | AC 01.2          | Recurrence Days (custom) → display saved value, not editable                                                                                                                              |
| 14  | AC 01.2          | Recurrence End Date → editable only to extend (later date)                                                                                                                                |
| 15  | AC 01.2          | Lesson Count → editable only to increase                                                                                                                                                  |
| 16  | AC 01.2          | Skip Closed Dates → display saved state, not editable                                                                                                                                     |
| 17  | AC 01.3          | Button only available when `is_recurring = TRUE`                                                                                                                                          |
| 18  | AC 01.3          | User can only extend End Date beyond current value OR increase Lesson Count beyond current number and check all lesson information of all new created lessons following the defined logic |
| 19  | AC 01.4          | New lessons added to same recurring chain with DRAFT status                                                                                                                               |
| 20  | AC 01.4          | New lessons NOT created if existing lesson on that date (created by Add Lesson manually)                                                                                                  |
| 21  | AC 01.4          | Lesson code auto-calculated for following lessons based on defined code                                                                                                                   |
| 22  | AC 01.4          | Teachers and students must be manually allocated to new lessons                                                                                                                           |
| 23  | AC 01.4          | Nichibei only: update syllabus description for new lessons based on lesson code                                                                                                           |
| 24  | AC 01.5          | Update Lesson Schedule End Date when End Date is extended                                                                                                                                 |
| 25  | AC 01.5          | Update Lesson Schedule End Date when Lesson Count is increased (derived from last lesson date)                                                                                            |
| 26  | AC 01.5          | Update reflected on: SF Lesson Schedule detail, SF Lesson edit form, SF Calendar Related list, BO Lesson detail Recurring settings, BO Calendar Related list                              |
| 27  | AC 02.1          | "Apply this and the following" and "Apply to the specific number lessons" on recurring lessons updates all lessons — including extended ones                                              |
| 28  | AC 02.1          | One-time lesson edit only impacts that specific lesson                                                                                                                                    |
| 29  | AC 02.1          | Manually created one-time lessons are NOT affected by recurring "Apply this and the following" edits                                                                                      |
| 30  | AC 02.2          | Assign/Unassign Student "Apply this and the following" reflects across old, extended, and manually created lessons                                                                        |
| 31  | AC 02.2          | Assign/Unassign Student "Apply to the specific number lessons" reflects from old + extended lessons, and reassigns to new lessons                                                         |
| 32  | AC 02.2          | Assign/Unassign Teacher "Apply this and the following" reflects across old, extended, and manually created lessons                                                                        |
| 33  | AC 02.2          | Assign/Unassign Teacher "Apply to the specific number lessons" reflects from old + extended lessons, and reassigns to new lessons                                                         |
| 34  | Additional logic | Add lesson manual to the last lesson of the chain, after that extend the end date of the chain                                                                                            |
| 35  | Additional logic | Add lesson manual to the last lesson of the chain, after that increase the lesson count of the chain                                                                                      |
| 36  | Additional logic | Edit lesson date to the last lesson of the chain, after that extend the end date of the chain                                                                                             |
| 37  | Additional logic | Edit lesson date to the last lesson of the chain, after that increase the lesson count of the chain                                                                                       |
| 38  | Additional logic | Completed the last lesson of the chain, after that extend the end date of the chain                                                                                                       |
| 39  | Additional logic | Completed the last lesson of the chain, after that increase the lesson count of the chain                                                                                                 |
| 40  | Additional logic | Cancelled the last lesson of the chain, after that extend the end date of the chain                                                                                                       |
| 41  | Additional logic | Cancelled the last lesson of the chain, after that increase the lesson count of the chain                                                                                                 |
| 42  | Additional logic | Edit lesson on BO, after extending the end date of the chain                                                                                                                              |
| 43  | Additional logic | Edit lesson on BO, after increasing the lesson count of the chain                                                                                                                         |
| 44  | Additional logic | Assign/Unassign student on BO, after extending the end date of the chain, then edit with "Apply this and the following"                                                                   |
| 45  | Additional logic | Assign/Unassign student on BO, after increasing the lesson count of the chain, then edit with "Apply this and the following"                                                              |
| 46  | Additional logic | Assign/Unassign teacher on BO, after extending the end date of the chain, then edit with "Apply this and the following"                                                                   |
| 47  | Additional logic | Assign/Unassign teacher on BO, after increasing the lesson count of the chain, then edit with "Apply this and the following"                                                              |
| 48  | Additional logic | We have a existing feature about generating zoom link, if we extend the end date of the chain, we need to generate zoom link for new lessons on BO                                        |
| 49  | Additional logic | We have a existing feature about generating zoom link, if we increase the lesson count of the chain, we need to generate zoom link for new lessons on BO                                  |

---

## 2. Logic Type Categorization

| AC      | Business Rule # | Logic Type                              |
| ------- | --------------- | --------------------------------------- |
| AC 01.1 | 1, 2, 3         | Conditional logic, Permission logic     |
| AC 01.2 | 4, 5            | Validation logic                        |
| AC 01.2 | 6, 7, 8         | Boundary/range logic, Validation logic  |
| AC 01.2 | 9, 10           | Validation logic                        |
| AC 01.2 | 11              | Validation logic                        |
| AC 01.2 | 12, 13, 16      | Conditional logic, Validation logic     |
| AC 01.2 | 14, 15          | Boundary/range logic, Conditional logic |
| AC 01.3 | 17              | Conditional logic, Permission logic     |
| AC 01.3 | 18              | Boundary/range logic                    |
| AC 01.4 | 19              | State transition, Recurrence logic      |
| AC 01.4 | 20              | Data integrity, Recurrence logic        |
| AC 01.4 | 21              | Data integrity                          |
| AC 01.4 | 22              | State transition                        |
| AC 01.4 | 23              | Data integrity                          |
| AC 01.5 | 24, 25, 26      | Cross-system impact, Data integrity     |
| AC 02.1 | 27, 28, 29      | Recurrence logic, Conditional logic     |
| AC 02.2 | 30              | Recurrence logic, Data integrity        |

---

## 3. Test Technique Selection

| Logic Type           | Applicable Techniques                         |
| -------------------- | --------------------------------------------- |
| Validation logic     | Equivalence Partitioning, Negative Testing    |
| Boundary/range logic | Boundary Value Analysis, Negative Testing     |
| Conditional logic    | Decision Table, Negative Testing              |
| Recurrence logic     | State Transition Testing, Regression Analysis |
| State transition     | State Transition Testing                      |
| Permission logic     | Permission Matrix, Decision Table             |
| Data integrity       | CRUD Testing, Regression Analysis             |
| Cross-system impact  | Regression Analysis, CRUD Testing             |

---

## 4. Structured Coverage Strategy

| AC                                                                                                  | Logic Type                              | Test Technique                                | Risk Level | Coverage Depth                                                                                                          |
| --------------------------------------------------------------------------------------------------- | --------------------------------------- | --------------------------------------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------- |
| AC 01.1 — Button visibility (recurring)                                                             | Permission logic, Conditional logic     | Decision Table, Permission Matrix             | High       | Deep — verify button present only for `is_recurring = TRUE`; absent for one-time, course schedule                       |
| AC 01.1 — Button opens creation form                                                                | Conditional logic                       | CRUD Testing                                  | Medium     | Standard — verify form opens with correct initial state                                                                 |
| AC 01.2 — Pre-filled editable fields (Start Time, End Time, Duration, Teaching Medium, Lesson Name) | Validation logic                        | Equivalence Partitioning                      | Medium     | Standard — verify each field sourced correctly; verify user can modify and save                                         |
| AC 01.2 — Classroom searchable dropdown                                                             | Validation logic                        | Equivalence Partitioning                      | Medium     | Standard — verify dropdown loads available classrooms, search works                                                     |
| AC 01.2 — Date auto-calculated (end date + 7 days)                                                  | Boundary/range logic                    | Boundary Value Analysis                       | High       | Deep — verify exact calculation; edge cases: end date on week boundary, year boundary, DST transition                   |
| AC 01.2 — Lesson Code auto-calculated (last + 1)                                                    | Boundary/range logic                    | Boundary Value Analysis                       | High       | Deep — verify N+1 logic; edge cases: code = 0, code with gaps, large code numbers                                       |
| AC 01.2 — Lesson Type default "Regular"                                                             | Validation logic                        | Equivalence Partitioning                      | Low        | Standard — verify default and ability to change                                                                         |
| AC 01.2 — Locked fields (Location, Academic Year, Course, Class, Teaching Method)                   | Validation logic                        | Negative Testing                              | High       | Deep — attempt to edit each locked field; verify all remain read-only                                                   |
| AC 01.2 — Recurrence End Date: extend-only                                                          | Boundary/range logic, Conditional logic | Boundary Value Analysis, Negative Testing     | High       | Deep — BVA: same date (reject), earlier date (reject), 1 day later (accept), far future (accept)                        |
| AC 01.2 — Lesson Count: increase-only                                                               | Boundary/range logic, Conditional logic | Boundary Value Analysis, Negative Testing     | High       | Deep — BVA: same count (reject), lower count (reject), +1 (accept), large increase (accept)                             |
| AC 01.2 — Recurrence Type and Recurrence Days read-only                                             | Conditional logic, Validation logic     | Negative Testing                              | Medium     | Standard — verify display and non-editability                                                                           |
| AC 01.2 — Skip Closed Dates read-only                                                               | Validation logic                        | Negative Testing                              | Medium     | Standard — verify display matches saved state, not editable                                                             |
| AC 01.3 — Button hidden for non-recurring                                                           | Conditional logic, Permission logic     | Decision Table                                | High       | Deep — check: one-time lesson, course schedule lesson, non-recurring schedule                                           |
| AC 01.4 — New lessons added in DRAFT (via End Date)                                                 | State transition, Recurrence logic      | State Transition Testing, CRUD Testing        | Critical   | Deep — verify all new lessons have DRAFT status; verify chain continuity (daily, weekly, custom)                        |
| AC 01.4 — New lessons added in DRAFT (via Lesson Count)                                             | State transition, Recurrence logic      | State Transition Testing, CRUD Testing        | Critical   | Deep — same verification via lesson count path                                                                          |
| AC 01.4 — Duplicate date conflict (manual lesson blocks creation)                                   | Data integrity, Recurrence logic        | Decision Table, Negative Testing              | Critical   | Deep — manual lesson on first/middle/last new date; verify skip logic; verify remaining dates still created             |
| AC 01.4 — Lesson code auto-increment for extended chain                                             | Data integrity                          | Boundary Value Analysis, CRUD Testing         | High       | Deep — verify each new lesson has correct incremented code                                                              |
| AC 01.4 — No teacher/student auto-allocation                                                        | State transition                        | Negative Testing                              | Medium     | Standard — verify newly created lessons have empty teacher/student lists                                                |
| AC 01.4 — Nichibei syllabus description update                                                      | Data integrity                          | CRUD Testing, Regression Analysis             | Medium     | Standard — verify syllabus description matches lesson code per Nichibei configuration                                   |
| AC 01.5 — Schedule End Date sync (End Date path)                                                    | Cross-system impact, Data integrity     | CRUD Testing, Regression Analysis             | Critical   | Deep — verify in all 5 surfaces: SF detail, SF edit form, SF Calendar, BO Recurring settings, BO Calendar               |
| AC 01.5 — Schedule End Date sync (Lesson Count path)                                                | Cross-system impact, Data integrity     | CRUD Testing, Regression Analysis             | Critical   | Deep — derived from last lesson date; verify all 5 surfaces                                                             |
| AC 02.1 — "Apply this and the following" includes extended lessons                                  | Recurrence logic, Conditional logic     | State Transition Testing, Regression Analysis | Critical   | Deep — edit from before extension point; edit from within extended range; verify all following lessons updated          |
| AC 02.1 — One-time lesson isolation                                                                 | Conditional logic                       | Decision Table, Negative Testing              | High       | Deep — verify one-time lesson edits don't cascade                                                                       |
| AC 02.1 — Manual lesson not affected by recurring edit                                              | Conditional logic, Data integrity       | Negative Testing, Decision Table              | High       | Deep — verify manually created lesson in schedule is untouched by "Apply this and the following"                        |
| AC 02.2 — Student/teacher propagation across old + extended lessons                                 | Recurrence logic, Data integrity        | Pairwise Testing, Regression Analysis         | Critical   | Deep — assign/unassign from various positions; verify lesson allocation data (Lesson Allocated, Status, Report History) |
| AC 02.2 — Student/teacher propagation includes manually created lesson                              | Recurrence logic, Data integrity        | CRUD Testing, Regression Analysis             | High       | Deep — verify manually created lesson also receives student/teacher assignment                                          |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area                                                                  | Reason                                                                                                                                                                    | Recommended Approach                                                                                                                                                      |
| --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Duplicate date conflict — manual lesson blocks creation (AC 01.4)** | If a manually added lesson already occupies a date, the system must skip only that date and still create all others. Failure → missing or duplicate lessons in the chain. | Decision Table: manual lesson on first new date, middle, last, consecutive dates. Verify final lesson count = expected count minus conflicts.                             |
| **Lesson Schedule End Date sync across 5 surfaces (AC 01.5)**         | Data inconsistency between SF and BO is highly visible to end users. Caching, async sync, or separate read paths could cause drift.                                       | Verify each of the 5 surfaces independently after both End Date and Lesson Count extension paths. Test both immediate and after-refresh consistency.                      |
| **"Apply this and the following" into extended chain (AC 02.1)**      | Extended lessons must be part of the same recurrence chain. If the chain link is broken, edits silently miss newly created lessons — data corruption.                     | Test from 3 positions: (1) before original chain boundary, (2) at original/extended boundary, (3) within extended range. Verify completed/cancelled lessons are excluded. |
| **Student/teacher propagation across extended lessons (AC 02.2)**     | Lesson allocation records (student sessions, allocation status, report history) must be correctly updated. Incorrect propagation → billing and reporting errors.          | Assign from before extension point → verify extended lessons included. Unassign → verify session deletion and allocation status for all affected lessons.                 |
| **New lessons DRAFT status (AC 01.4)**                                | If new lessons are created with a status other than DRAFT (e.g., Published), they could appear in student Mobile views prematurely or affect lesson reports.              | Verify status = DRAFT for every new lesson in daily, weekly, and custom recurrence types.                                                                                 |

### 🟠 High Risk

| Area                                                                  | Reason                                                                                                                                                                           | Recommended Approach                                                                                                                        |
| --------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **Recurrence End Date / Lesson Count boundary enforcement (AC 01.2)** | System must reject same or earlier End Date, and same or lower Lesson Count. Ambiguity in spec about error display vs. silent prevention.                                        | BVA at exact boundary (current value, current - 1, current + 1). Test with both End Date and Lesson Count fields.                           |
| **Lesson Code auto-increment (AC 01.4)**                              | Incorrect codes corrupt chain identity and break Nichibei syllabus mapping.                                                                                                      | BVA: extend from code = 1, code = 50, code = 100. Verify N+1 for each new lesson. Test code gap scenarios.                                  |
| **Locked fields remain non-editable (AC 01.2)**                       | UI could allow editing after re-render, form reset, or field focus events.                                                                                                       | Negative testing: attempt to type in each locked field. Inspect DOM/field state.                                                            |
| **Button visibility for all schedule types (AC 01.1 + AC 01.3)**      | Button must NOT appear for one-time, course schedule, or non-recurring. False positive would expose invalid functionality.                                                       | Decision Table across: one-time lesson, course schedule, daily recurring, weekly recurring, custom recurring. Test with Admin and CM roles. |
| **Manual lesson isolation from recurring edit (AC 02.1)**             | Manual lessons exist in the same schedule but should be excluded from "Apply this and the following." Existing TCs (TC-9691–9693) cover Add Lesson flow but NOT the Extend flow. | Regression + new TCs: create manual lesson → extend → edit recurring with following → verify manual lesson unchanged.                       |

### 🟡 Medium Risk

| Area                                                             | Reason                                                                                                                         | Recommended Approach                                                                                                 |
| ---------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------- |
| **Nichibei syllabus description for extended lessons (AC 01.4)** | Tenant-specific logic; may be missed in general regression. Existing TC-2845 covers Add Lesson but not Extend.                 | Dedicated test with Nichibei config: extend recurring → verify syllabus desc = mapped desc for each new lesson code. |
| **Skip Closed Dates carry-over (AC 01.2)**                       | Extended lessons should respect the inherited skip-closed-dates setting. A closed date in the extension range must be skipped. | Test with closed date falling in extension range; verify lesson not created on that date.                            |
| **Pre-filled field accuracy (AC 01.2)**                          | If source values change between schedule creation and extension, the form must still show current schedule values.             | Scenario: edit lesson schedule fields → extend → verify form reflects latest values.                                 |

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area                                           | Existing Test Case                                                                    | Overlap                                                                                           | New Coverage Needed                                                        |
| -------------------------------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Extend Recurrence button visibility                | TC-1028 (Add Lesson button hidden for one-time/course schedule), TC-1029 (permission) | Partial — different button                                                                        | ✅ New TCs for Extend Recurrence button per schedule type and role         |
| Extend form pre-fill & locked fields               | TC-1017 (Add Lesson form pre-fill)                                                    | Partial — similar structure, different behavior (locked recurring settings, Lesson Code = last+1) | ✅ New TCs: verify pre-fill, locked fields, recurring settings inheritance |
| Recurrence End Date / Lesson Count boundary        | None                                                                                  | None                                                                                              | ✅ New TCs: BVA for extend-only enforcement                                |
| New lessons in DRAFT status                        | None                                                                                  | None                                                                                              | ✅ New TCs: verify DRAFT status for all new lessons                        |
| Duplicate date conflict (extend vs. manual lesson) | TC-1024 (duplicate date in Add Lesson)                                                | Partial — same concept, different trigger                                                         | ✅ New TCs: extend encounters manual-lesson date                           |
| Lesson code auto-increment for extended chain      | None                                                                                  | None                                                                                              | ✅ New TCs: verify code increment logic                                    |
| Lesson Schedule End Date sync (5 surfaces)         | TC-9006/9008/9009/9010 (end date sync after Add Lesson)                               | Partial — same surfaces, different trigger                                                        | ✅ New TCs: all 5 surfaces after extension                                 |
| "Apply this and following" into extended chain     | TC-1896, TC-9812, TC-9813 (edit with following in daily/weekly/custom)                | Partial — does not cover extended lessons                                                         | ✅ New TCs: edit from before/at/within extension boundary                  |
| Manual lesson isolation after extension            | TC-9691–9693 (manual lesson isolation for Add Lesson flow)                            | Partial — same logic, different trigger                                                           | ✅ Regression + new TCs for extend-specific flow                           |
| Student/teacher propagation into extended lessons  | TC-8759, TC-9696–9698 (assign/unassign with manual lesson)                            | Partial — does not cover extended lessons                                                         | ✅ New TCs: assign/unassign across old + extended lessons                  |
| Nichibei syllabus for extended lessons             | TC-2845 (Add lesson with syllabus), TC-2843 (recurring with syllabus)                 | Partial — does not cover extend flow                                                              | ✅ New TC: extend → verify syllabus description mapping                    |

---

## 7. Suggested Test Suite Structure

```
3-testcases/lesson-management/lesson/extend-recurring/
  ├── extend-recurrence-button.md
  │     → AC 01.1, AC 01.3
  │     → Button visibility per schedule type (recurring/one-time/course schedule)
  │     → Button visibility per role (Admin, CM)
  │
  ├── extend-recurrence-form.md
  │     → AC 01.2
  │     → Pre-filled editable fields verification
  │     → Auto-calculated fields (Date, Lesson Code, Day of Week)
  │     → Locked fields negative testing
  │     → Recurring settings inheritance & extend-only enforcement
  │
  ├── extend-recurrence-create-lessons.md
  │     → AC 01.4
  │     → New lessons in DRAFT status (daily/weekly/custom × end date/lesson count)
  │     → Duplicate date conflict with manual lessons
  │     → Lesson code auto-increment
  │     → No auto-allocation of teacher/student
  │     → Nichibei syllabus description update
  │
  ├── extend-recurrence-schedule-sync.md
  │     → AC 01.5
  │     → Lesson Schedule End Date update via End Date extension
  │     → Lesson Schedule End Date update via Lesson Count increase
  │     → Verification across 5 surfaces (SF detail, SF edit form, SF Calendar, BO Recurring, BO Calendar)
  │
  ├── extend-recurrence-edit-following.md
  │     → AC 02.1
  │     → "Apply this and the following" propagates to extended lessons
  │     → One-time lesson isolation
  │     → Manual lesson isolation from recurring edits
  │
  └── extend-recurrence-student-teacher.md
        → AC 02.2
        → Student assignment propagation across old + extended + manual lessons
        → Teacher assignment propagation across old + extended + manual lessons
        → Unassign propagation and allocation data verification
```
