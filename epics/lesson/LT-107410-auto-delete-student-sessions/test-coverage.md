# Test Coverage: LT-107410 — Auto-delete Student Sessions after Lesson Unassignment

**Jira:** https://manabie.atlassian.net/browse/LT-107410  
**Date:** 2026-08-17  
**Scope:** Core individual Student Sessions only. Graduate and new class-based coverage are excluded.

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---:|---|---|
| BR-01 | AC-1 | Partial Withdrawal deletes individual sessions after the last attendance day when the LA is shortened. |
| BR-02 | AC-2 | Partial LOA deletes individual sessions after the last attendance day when the LA is shortened. |
| BR-03 | AC-3 | Cancel that reduces the LA end date deletes individual out-of-range sessions. |
| BR-04 | AC-3, AC-9 | Only an Update that shortens the duration deletes sessions; slot/frequency-only Updates do not. |
| BR-05 | AC-4 | Partial Course Change deletes only old-course, out-of-range individual sessions. |
| BR-06 | AC-6 | Completed/past sessions and sessions on the last attendance day are retained. |
| BR-07 | AC-7 | Void restores LA duration and expected slots but does not restore deleted individual sessions; explicit re-assignment creates one fresh session. |
| BR-08 | AC-8 | Existing class behavior is already covered; no new test case is required. |
| BR-09 | Scope | Graduate is excluded. |

---

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC-1 | BR-01 | Conditional; Boundary/range; Data integrity; Cross-system impact |
| AC-2 | BR-02 | Conditional; Boundary/range; Data integrity; Cross-system impact |
| AC-3 | BR-03, BR-04 | Conditional; Boundary/range; State transition; Data integrity |
| AC-4 | BR-05 | Conditional; Boundary/range; Data integrity; Cross-system impact |
| AC-6 | BR-06 | Boundary/range; State transition; Data integrity |
| AC-7 | BR-07 | State transition; Data integrity; Cross-system impact |
| AC-8 | BR-08 | Regression (existing coverage only) |
| AC-9 | BR-04 | Conditional; Negative; Data integrity |

---

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Conditional | Decision Table; Negative |
| Boundary/range | Boundary Value Analysis; Negative |
| State transition | State Transition; CRUD |
| Data integrity | CRUD; Regression; Decision Table |
| Cross-system impact | Regression; CRUD |
| Regression | Regression |

---

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC-1 | Partial Withdrawal deletes only future individual sessions after the last attendance day. | Conditional; Boundary/range; Cross-system | Decision Table; BVA; CRUD | Critical | Deep |
| AC-2 | Partial LOA deletes only future individual sessions after the last attendance day. | Conditional; Boundary/range; Cross-system | Decision Table; BVA; CRUD | Critical | Deep |
| AC-3 | Cancel that shortens LA duration deletes out-of-range individual sessions. | Conditional; State transition; Cross-system | Decision Table; State Transition; CRUD | Critical | Deep |
| AC-3 | Update Duration deletion occurs only when the end date is shortened. | Conditional; Boundary/range; Data integrity | Decision Table; BVA; Negative | Critical | Deep |
| AC-4 | Partial Course Change deletes only old-course, out-of-range individual sessions. | Conditional; Boundary/range; Data integrity | Decision Table; BVA; CRUD | Critical | Deep |
| AC-6 | Completed/past sessions and the session on the last attendance day are retained. | Boundary/range; State transition | BVA; Negative | Critical | Deep |
| AC-7 | Void does not restore an individual deleted session; explicit re-assignment yields one active session only. | State transition; Data integrity; Cross-system | State Transition; CRUD; Regression | Critical | Deep |
| AC-8 | Existing class behavior remains baseline only. | Regression | Existing-case regression reference | Low | Smoke |
| AC-9 | Slot-only and frequency-only Updates do not delete sessions. | Conditional; Negative | Decision Table; Negative | High | Deep |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Automatic deletion after order actions | Incorrect scope causes future data loss or leaves orphan sessions. | Run a decision table across each action, individual session, lesson date relative to last attendance day, and all downstream effects. |
| Historical attendance preservation | Deleting a completed/past session destroys attendance history. | Test lesson date `<`, `=`, and `>` last attendance day; include completed lesson with attendance data. |
| Action reversal and re-assignment | Reversing Cancel Order, Change Associated Course, or Update Duration can lead to an unwanted restore or duplicate session. | State transition: remove → reverse the originating action → explicit re-assign; assert exactly one active session, correct count, and one report detail. |
| Downstream cascade | Session deletion affects reports, LA, BO, and Mobile. | Give every dependent record/surface its own deterministic assertion. |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Update trigger gating | A shared Update handler may delete sessions for slot/frequency-only changes. | Pair shortened-end-date, slot decrease, frequency decrease, and unchanged duration in a decision table. |
| Partial Course Change scope | Incorrect course selection can delete new-course or in-range sessions. | Use two courses and both retained/out-of-range sessions for the old course. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Manual Remove Lesson boundary | The UI flow must not regress into the order-triggered flow. | Retain existing suite 324 coverage; no new case is created for this ticket. |

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Withdrawal automatic session deletion + cascade | Suite 2577: Withdrawal last-attendance-day cases | Removes student from future/out-of-range lessons | ✅ Add individual-session state, LA count/status, report-detail, BO, and Mobile assertions. |
| LOA automatic session deletion + cascade | Suite 2578: LOA last-attendance-day cases | Updates LA and removes student from lessons | ✅ Add equivalent individual-session and downstream assertions. |
| Cancel automatic session deletion | Suite 2575: Cancel Order | LA end-date and historical-lesson coverage | ✅ Add individual-session deletion and full downstream cascade. |
| Reduced-duration Update | PX-9925 / PX-9928 in suite 2574 | Verifies duration update only | ✅ Add deletion after end-date reduction; include exact date boundary. |
| Update non-trigger variants | Update Slot cases in suite 2574 | Slot/frequency updates with unchanged duration | ✅ Add explicit no-unassignment/no-session-deletion assertions. |
| Partial Course Change | PX-1774 in suite 2573 | Old LA update and class auto-removal | ✅ Add individual old-course session scope and preservation of new-course/in-range sessions. |
| Action-reversal non-restoration and fresh re-assignment | PX-1802 / PX-25725 in suite 2576 | Existing **class** auto-reassignment after reversal | ✅ Add individual-only reversal paths for Cancel Order, Change Associated Course, and Update Duration: no restore, then one fresh active session after re-assignment. |
| Completed/past attendance safeguard | Withdrawal/LOA past-date variants | Past lesson is retained at title level | ✅ Add attendance-record and last-attendance-day equality assertions. |
| Class behavior | Existing class suites and void cases | Existing coverage | No new case — explicitly excluded by approved scope. |
| Graduate | PRD AC-5 only | N/A | No new case — explicitly excluded by approved scope. |

---

## G. Downstream Effects Inventory

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner (TC) |
|---|---|---|---|
| Partial Withdrawal / LOA / Cancel / reduced Update / partial Course Change | Student is removed from the eligible future lesson | SF Student Session | Action-suite removal case |
| Same actions | Retained sessions produce the correct LA allocated count and status | SF Lesson Allocation | Action-suite LA integrity case |
| Same actions | Linked Lesson Report Detail is removed | SF Lesson Report Detail | Action-suite report-cascade case |
| Same actions | Student no longer appears in the affected lesson | BO Lesson Detail student list | Action-suite BO cascade case |
| Same actions | Student no longer sees the affected lesson/report | Learner App | Action-suite Mobile cascade case |
| Action reversal | LA duration and expected slots restore without restoring deleted individual sessions | SF Lesson Allocation / Student Session | Action-reversal non-restoration case |
| Explicit re-assignment after reversal | Exactly one active session and one report detail are created | SF Student Session / Lesson Report Detail | Re-assignment uniqueness case |
| Explicit re-assignment after reversal | Restored student visibility is consistent on BO and Mobile | BO Lesson Detail / Learner App | Re-assignment cross-surface case |
| Any order-processing retry | No duplicate active session or duplicate dependent record | Server / SF records | Action idempotency case |

---

## H. Display & Ordering Inventory

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| N/A — no new UI specified | N/A: requirement is an order-triggered backend behavior | N/A | N/A | N/A |

**H.1 — N/A:** No Figma URL is present in the ticket or spec.

---

## 7. Suggested Test Suite Structure

All files map to existing Qase suites; no new Qase suite is needed.

```
epics/lesson/LT-107410-auto-delete-student-sessions/test-cases/
├── withdrawal.md                → Qase 2577: AC-1, AC-6 and full cascade
├── loa.md                       → Qase 2578: AC-2, AC-6 and full cascade
├── cancel-order.md              → Qase 2575: AC-3, AC-6 and full cascade
├── update-duration.md           → Qase 2574: AC-3, AC-9; duration trigger versus slot/frequency non-trigger
├── change-associated-course.md  → Qase 2573: AC-4 and old/new-course isolation
├── order-reversals.md           → Qase 2576: reverse Cancel Order / Change Associated Course / Update Duration; non-restoration
├── cancel-withdrawal.md         → Qase 2577: cancel Withdrawal; non-restoration
├── cancel-loa.md                → Qase 2578: cancel LOA; non-restoration
└── transfer-order.md             → Qase 2967: Transfer Order; prior-location outside lesson removal
```

No new file is planned for AC-8 (existing class coverage) or Graduate (excluded scope).
