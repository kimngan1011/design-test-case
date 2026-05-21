# E2E Coverage — Mandatory Checklist

Used by `review-e2e-scenario` agent. Every sub-item MUST be verified against `knowledge/e2e-scenario/e2e-scenarios.md`. Record the scenario ID(s) that cover each item.

A flow is **covered** only if there is a clear step or "Features covered" entry for it. Partial coverage (e.g. "This and following" covered but "Only this" missing) → mark the specific missing variant as a gap.

---

## 1. Lesson Creation

| # | Flow | Variants |
|---|---|---|
| 1.1 | One-time lesson | Created from Lesson List; created from Calendar |
| 1.2 | Recurring — Weekly | End after N lessons; end by date |
| 1.3 | Recurring — Daily | End after N lessons; end by date |
| 1.4 | Recurring — Custom (Mon/Wed/Fri) | End after N lessons; end by date |
| 1.5 | End Date constraint | Recurring with end-date config |
| 1.6 | Number of Lessons constraint | Recurring with count config |
| 1.7 | Course Schedule | Create lesson via Course Schedule configuration |
| 1.8 | Import Lesson | CSV import with teacher column |
| 1.9 | Add lesson via Lesson Schedule | Add to existing schedule from Lesson Schedule Detail |
| 1.10 | Extend Recurring Lesson | Extend an existing chain with more occurrences |
| 1.11 | Create on Calendar | Click empty time slot on SF Calendar |

## 2. Student Assignment

| # | Flow | Variants |
|---|---|---|
| 2.1 | Recurring scope — Only this | Assign to a single occurrence |
| 2.2 | Recurring scope — This and following | Assign to current + all future |
| 2.3 | Recurring scope — Specific number | Assign to N occurrences from current |
| 2.4 | Class assignment — Course tab | Assign Class in Course tab |
| 2.5 | Class assignment — Bulk Assign | From Student Group or list |
| 2.6 | Class assignment — LA Detail | Assign from Lesson Allocation Detail |
| 2.7 | Class assignment — Import Class Member | CSV import of class members |
| 2.8 | Modify Course/Class in Lesson Schedule | Change triggers reassignment |
| 2.9 | Modify Location/Class in Lesson Allocation | Change triggers reassignment |
| 2.10 | Assign via Calendar | Add student from SF Calendar popover |
| 2.11 | Assign via BO | Add from BO Lesson Detail |

## 3. Student Unassignment

| # | Flow | Variants |
|---|---|---|
| 3.1 | Recurring scope — Only this | Remove from single occurrence |
| 3.2 | Recurring scope — This and following | Remove from current + all future |
| 3.3 | Change Class in Course tab | Triggers unassignment from old class lessons |
| 3.4 | Bulk Change Class | Batch unassignment from old class lessons |
| 3.5 | LA Detail — Remove lesson | Remove from LA Detail list |
| 3.6 | Class Member duration updated by Order | Shortened duration → auto-unassign out-of-scope lessons |
| 3.7 | Unassign via Calendar | Remove from SF Calendar popover |
| 3.8 | Unassign via BO | Remove from BO Lesson Detail |
| 3.9 | Change Lesson on Calendar | Move student session from one date to another |
| 3.10 | Change Lesson on LA Detail | Move/remove from LA Detail |

## 4. Teacher Management

### 4A. Teacher Assignment

| # | Flow |
|---|---|
| 4A.1 | One-time lesson assignment |
| 4A.2 | Recurring — Only this |
| 4A.3 | Recurring — This and following |
| 4A.4 | Assign on Lesson Teacher List |
| 4A.5 | Assign via Import Lesson |
| 4A.6 | Assign via Calendar |
| 4A.7 | Assign via BO |

### 4B. Teacher Unassignment

| # | Flow |
|---|---|
| 4B.1 | One-time lesson unassignment |
| 4B.2 | Recurring — Only this |
| 4B.3 | Recurring — This and following |
| 4B.4 | Unassign on Lesson Teacher List |
| 4B.5 | Unassign via Calendar |
| 4B.6 | Unassign via BO |

## 5. System Automation & Mobile Integration

| # | Flow |
|---|---|
| 5.1 | Lesson Report auto-created for every lesson creation method (Calendar, recurring, extend, import, Lesson Schedule add) |
| 5.2 | Lesson Report Detail auto-created for every student assignment method |
| 5.3 | Lesson Report Detail auto-deleted on every student unassignment method |
| 5.4 | Mobile — View Lesson (student sees published lesson on Learner App) |
| 5.5 | Mobile — Submit Attendance (student submits via Learner App) |

## 6. Session Logic & E2E Standards

| # | Rule |
|---|---|
| 6.1 | Student Session updated before removal — Collect Attendance scenario |
| 6.2 | Student Session updated before removal — Trial Lesson scenario |
| 6.3 | Student Session updated before removal — Reallocated scenario |
| 6.4 | Every E2E scenario has ≤ 20 steps (flag for splitting if more) |
