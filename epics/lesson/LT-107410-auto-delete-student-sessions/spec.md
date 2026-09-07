---
ticket_id: LT-107410
ticket_url: https://manabie.atlassian.net/browse/LT-107410
title: "[Renseikai] Core | Remove Student Sessions after the Last Attendance Day in Application"
module: scheduling
bucket: lesson
status: Ready for Development
internal_uat_date: null
production_release_date: null
last_updated: 2026-08-17
---

# LT-107410: Auto-delete Student Sessions after Lesson Unassignment

## Summary

When an order action shortens an individual student's Lesson Allocation (LA), the system must automatically remove the Student Sessions linked to lessons outside the reduced duration. This eliminates future orphan sessions while preserving historical attendance and leaving class-based behavior unchanged.

This QA scope covers Partial Withdrawal, Partial LOA, Cancel, an Update that shortens the end date, and partial Course Change. **Graduate is explicitly excluded by user direction.** Existing class behavior is already covered and is excluded from new test-case generation.

---

## Acceptance Criteria

| ID | Requirement |
|---|---|
| AC-1 | A Partial Withdrawal that shortens an individual student's LA auto-deletes sessions linked to lessons after the last attendance day. |
| AC-2 | A partial LOA that shortens an individual student's LA auto-deletes sessions linked to lessons after the last attendance day. |
| AC-3 | A Cancel or Update order that reduces the LA end date auto-deletes sessions linked to out-of-range lessons. An Update deletes sessions only when it shortens the package duration. |
| AC-4 | A partial Course Change effective after the LA start date auto-deletes old-course sessions linked to out-of-range lessons. |
| AC-6 | Sessions linked to completed or past lessons are retained; only future sessions after the last attendance day are affected. |
| AC-7 | When an in-scope action is voided, deleted sessions are not restored; expected slots revert and staff re-assigns students to create fresh sessions. |
| AC-8 | Class-based students retain existing automatic-deletion behavior; individual sessions gain the new deletion behavior without class regression. |
| AC-9 | Slot-only or frequency-only Updates do not unassign lessons or auto-delete sessions. |

### Scope exclusions

- `ORDER_TYPE_GRADUATE` / Graduate is excluded from test design and Qase import by user direction.
- Slot/frequency increases and decreases without a duration reduction are out of the automatic-deletion trigger.
- The existing manual LA Detail **Remove Lesson** UI action is a separate, out-of-scope regression boundary and remains unchanged.

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---:|---|---|---|---|---|
| 1 | AC-1 | Partial Withdrawal removes students from outside lessons after the last attendance day when the LA is shortened. | Student Session | removed from lesson | SF / system |
| 2 | AC-2 | Partial LOA removes students from outside lessons after the last attendance day when the LA is shortened. | Student Session | removed from lesson | SF / system |
| 3 | AC-3 | Cancel that reduces the LA end date removes students from outside lessons. | Student Session | removed from lesson | SF / system |
| 4 | AC-3, AC-9 | Update is a trigger only when the package end date is shortened; slot-only or frequency-only changes do not delete sessions. | LA duration | updated / no deletion | SF / system |
| 5 | AC-4 | Partial Course Change removes the student only from old-course, outside lessons. | Student Session | removed from lesson | SF / system |
| 6 | AC-6 | Completed/past lessons and their sessions are retained. | Student Session | retained | SF / system |
| 7 | AC-7 | Void restores LA duration and expected slots but does not restore an **individual** session deleted by this feature; later re-assignment creates a fresh session. | Student Session | not restored | SF / system |
| 8 | AC-8 | Existing class-based automatic deletion remains unchanged and is already covered by existing cases; no new class test is required. | Student Session | existing behavior retained | SF / system |
| 9 | QA scope | Graduate processing is excluded. | Order Type | out of scope | N/A |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---:|---|---|---|---|
| 1 | [CONFLICT — RESOLVED] | Qase PX-1802 and PX-25725, suite 2576 | AC-7, AC-8 | The non-restoration rule applies only to **individual** sessions. Existing class-based coverage remains unchanged; no new class cases are needed. |

### Regression Risks and Extensions

| # | Tag | Source | AC | Description |
|---:|---|---|---|---|
| 1 | [EXTENDED] | Qase suite 2577 — Withdrawal | AC-1 | Existing coverage removes students from future lessons; add assertions for individual session deletion and LA/session-count consistency. |
| 2 | [EXTENDED] | Qase suite 2578 — LOA | AC-2 | Extend partial-LOA coverage to prove deletion of future individual sessions. |
| 3 | [REGRESSION RISK] | Qase PX-9925, suite 2574 | AC-3 | Existing reduced-duration Update verifies only LA duration; it can pass while orphan sessions remain. |
| 4 | [EXTENDED] | Qase PX-1774, suite 2573 | AC-4 | Existing Course Change coverage is class-driven; add individual old-course session coverage. |
| 5 | [REGRESSION RISK] | Qase Update Slot cases in suite 2574 | AC-3, AC-9 | The new deletion logic must be guarded by duration reduction and never run for slot/frequency-only changes. |
| 6 | [REGRESSION RISK — EXISTING COVERAGE] | `epics/lesson/LT-107255-order-group-class-assignment/spec.md` | AC-8 | Existing class coverage remains the regression baseline; no new class case is required for this ticket. |

### Missing in Requirements

| # | Tag | Source | Description |
|---:|---|---|---|
| 1 | [MISSING BEHAVIOR — RESOLVED] | Qase PX-1852 / PRD §7 and §9 | Automatic deletion must update **all** downstream data: Lesson Report Detail, LA count/status, BO student list, and Mobile visibility. Manual UI removal remains unchanged and out of scope. |

### Lesson-Learned Risks

| # | Incident | Date | AC | Risk | Guardrail |
|---:|---|---|---|---|---|
| 1 | Aso — Duplicate Student Sessions from Manual Assign + Auto Assign | 2026-04-13 | AC-7 | Void then re-assignment may invoke two creation paths or collide with a previously removed assignment, duplicating a session. | Assert one active `(student, lesson)` session, one LA count, and one report detail after void and re-assignment. |
| 2 | Aso — Duplicate Students on Lesson Copy Due to Missing `Unique_Key__c` Backfill | 2026-06-18 | AC-1–AC-7 | Deletion/re-creation can fail for legacy records or cause unintended dependent-record cleanup. | Exercise legacy-like data without a uniqueness key and validate the intended dependency cascade. |

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-09 | Lesson Allocation — New Order, Change Course & Void | Add an individual-student branch for old-course session deletion and non-restoration on void. | UPDATE |
| E2E-10 | Lesson Allocation — LOA, Add Course & Lesson Assignment | Add a partial-LOA branch for future-session deletion and explicit re-assignment. | UPDATE |

### Assumptions Made

- “After the last attendance day” means the lesson occurring on the last attendance day is retained; later lessons are eligible for deletion.
- This is a Core feature; artifacts live under `epics/lesson/`. The Jira title's Renseikai prefix is not treated as a partner-only scope gate.
- No Figma behavior is linked in the Jira ticket or PRD.
- Graduate is excluded even though the source PRD describes it as using the same mutation API.

---

## Clarification Questions

1. **[RESOLVED — not posted]** The non-restoration rule applies only to individual sessions. Existing class behavior is already covered and does not need new cases.
2. **[RESOLVED — not posted]** After void and re-assignment, there must be exactly one active Student Session for a student–lesson pair; generate coverage for this uniqueness check.
3. **[RESOLVED — not posted]** Automatic deletion updates all downstream data: Lesson Report Detail, LA allocated count/status, BO student list, and Mobile lesson visibility.
4. **[RESOLVED — not posted]** Manual LA Detail **Remove Lesson** remains unchanged and out of scope.

---

## Related Specs

- `epics/lesson/LT-107255-order-group-class-assignment/spec.md` — class-session origin preservation and automatic reconciliation behavior.
- `knowledge/domain-knowledge/scheduling/lesson-management/student-session.md` — Student Session removal effects, including LA count and Lesson Report Detail.

## Related Test Cases

- `Qase PX suite 2577 — Withdrawal` — existing last-attendance-day variants.
- `Qase PX suite 2578 — LOA (Leave of Absence)` — existing last-attendance-day variants.
- `Qase PX suite 2575 — Cancel Order` — existing cancellation duration variants.
- `Qase PX suite 2573 — Change Associated Course` — existing old-LA and class-driven removal behavior.
- `Qase PX suite 2574 — Update Slot` — Update Duration and non-trigger slot/frequency coverage.
- `Qase PX suite 2576 — Void Order` — class-based void behavior requiring clarification.
- `Qase PX suite 324 — Student Session tab > Remove lesson` — separate manual UI regression boundary.

## QASE Coverage Gaps

- AC-1 — Explicit individual-session deletion, LA/session-count, and historical-session assertions for Partial Withdrawal.
- AC-2 — Equivalent individual-session coverage for Partial LOA.
- AC-3 / AC-9 — Duration reduction versus slot/frequency-only decision table with session effects.
- AC-4 — Partial Course Change: only old-course out-of-range individual sessions are deleted.
- AC-6 — Completed/past attendance data is retained.
- AC-7 — Individual void non-restoration, re-assignment, and deduplication (one active session per student–lesson pair).
- AC-8 — Existing class coverage is sufficient; no new test case is required.
