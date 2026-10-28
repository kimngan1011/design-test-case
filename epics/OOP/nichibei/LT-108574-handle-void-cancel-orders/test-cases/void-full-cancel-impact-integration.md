# Test Cases: LT-108574 — Void and full-order Cancel impact integration

## Suite: [Nichibei] Void and Full-order Cancel Impact Integration

### [Nichibei] Void order impact handling – No impact – Void proceeds without impact warning

**Description:** AC 02.1 — State Transition — Void calls impact detection and proceeds without a warning when no assignment or consumed point exists.

**Preconditions:**
- HQ or CM Staff is logged in to the Nichibei Salesforce org.
- Test Order Group `OG-NB-INT-001A` is eligible for Void and has Assignment LA `LA-NB-INT-001A` with `Require Allocation = true` and no scheduled student sessions.
- Separate active Order Group `OG-NB-INT-001P` has Point LA `LA-NB-INT-001P` with `Require Allocation = false` and consumed points of `0`.
- An Order transaction log or debug trace is enabled for this execution.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff starts Void for `OG-NB-INT-001A` and confirms the standard Void action. | The transaction requests impact detection before the Void completes. | action = Void; orderGroupId = OG-NB-INT-001A; expectedDetectorResult = no impact |
| 2 | HQ or CM Staff observes the transaction and completion screen. | No impact warning is presented and the Order Group is voided through the existing flow. | expectedWarning = absent; expectedOrderStatus = Voided |
| 3 | HQ or CM Staff reviews the transaction trace. | The recorded impact result has no assignment and no consumed-point impact. | expectedHasImpact = false |

**Severity:** critical
**Priority:** high

---

### [Nichibei] Void order impact handling – Scheduled assignment – Abandoning warning keeps records unchanged

**Description:** AC 02.1, AC 02.2 — State Transition — An assignment impact opens a soft warning and abandoning it prevents the Void action.

**Preconditions:**
- HQ or CM Staff is logged in to the Nichibei Salesforce org.
- Test Order Group `OG-NB-INT-002A` is eligible for Void and has Assignment LA `LA-NB-INT-002A` with `Require Allocation = true` and two scheduled student sessions.
- Separate active Order Group `OG-NB-INT-002P` has Point LA `LA-NB-INT-002P` with `Require Allocation = false`; it is not part of the Void scope.
- The current Order Group status and related Lesson Allocation state are recorded before the action.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff starts Void for `OG-NB-INT-002A`. | The transaction requests impact detection before changing the Order Group. | action = Void; expectedAssignedSessionCount = 2; excludedOrderGroupId = OG-NB-INT-002P |
| 2 | HQ or CM Staff reviews the impact warning. | A warning is presented because scheduled assignment impact exists. | expectedHasAssignment = true; expectedHasImpact = true |
| 3 | HQ or CM Staff abandons the warning without continuing the Void action. | The Void action is not submitted. | confirmationChoice = abandon |
| 4 | HQ or CM Staff reopens the Order Group and related Lesson Allocation. | The Order Group status and the two scheduled sessions are unchanged from the recorded state. | expectedOrderStatus = pre-action status; expectedAssignedSessionCount = 2 |

**Severity:** critical
**Priority:** high

---

### [Nichibei] Void order impact handling – Scheduled assignment – Continuing warning completes existing Void flow

**Description:** AC 02.1, AC 02.2 — State Transition — Staff can continue a warned Void action and the existing Void flow completes.

**Preconditions:**
- HQ or CM Staff is logged in to the Nichibei Salesforce org.
- Test Order Group `OG-NB-INT-003A` is eligible for Void and has Assignment LA `LA-NB-INT-003A` with `Require Allocation = true` and two scheduled student sessions.
- Separate active Order Group `OG-NB-INT-003P` has Point LA `LA-NB-INT-003P` with `Require Allocation = false`; it is not part of the Void scope.
- The expected existing Void outcome for `OG-NB-INT-003A` is documented before execution.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff starts Void for `OG-NB-INT-003A`. | An impact warning is presented before the destructive action completes. | action = Void; expectedAssignedSessionCount = 2; excludedOrderGroupId = OG-NB-INT-003P |
| 2 | HQ or CM Staff continues from the warning. | The warning is accepted and the existing Void flow continues. | confirmationChoice = continue |
| 3 | HQ or CM Staff reviews the Order Group and related Lesson Allocation after completion. | The Order Group is voided and the documented existing Void outcome is applied after confirmation. | expectedOrderStatus = Voided; expectedLessonAllocationOutcome = documented baseline |

**Severity:** critical
**Priority:** high

---

### [Nichibei] Full-order Cancel impact handling – No impact – Cancel proceeds without impact warning

**Description:** AC 02.1 — State Transition — Full-order Cancel calls impact detection and proceeds without a warning when no impact exists.

**Preconditions:**
- HQ or CM Staff is logged in to the Nichibei Salesforce org.
- Test Order Group `OG-NB-INT-004P` is eligible for full-order Cancel and has Point LA `LA-NB-INT-004P` with `Require Allocation = false` and consumed points of `0`.
- Separate active Order Group `OG-NB-INT-004A` has Assignment LA `LA-NB-INT-004A` with `Require Allocation = true`; it is not part of the Cancel scope.
- An Order transaction log or debug trace is enabled for this execution.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff submits a full-order Cancel for `OG-NB-INT-004P`. | The transaction requests impact detection before the full-order Cancel completes. | action = full-order Cancel; orderGroupId = OG-NB-INT-004P; expectedDetectorResult = no impact |
| 2 | HQ or CM Staff observes the transaction and completion screen. | No impact warning is presented and the Order Group is cancelled through the existing full-order flow. | expectedWarning = absent; expectedOrderStatus = Cancelled |
| 3 | HQ or CM Staff reviews the transaction trace. | The recorded impact result has no assignment and no consumed-point impact. | expectedHasImpact = false |

**Severity:** critical
**Priority:** high

---

### [Nichibei] Full-order Cancel impact handling – Consumed points – Abandoning warning keeps records unchanged

**Description:** AC 02.1, AC 02.2 — State Transition — Consumed-point impact opens a soft warning and abandoning it prevents full-order Cancel.

**Preconditions:**
- HQ or CM Staff is logged in to the Nichibei Salesforce org.
- Test Order Group `OG-NB-INT-005P` is eligible for full-order Cancel and has Point LA `LA-NB-INT-005P` with `Require Allocation = false` and consumed points of `3.5`.
- Separate active Order Group `OG-NB-INT-005A` has Assignment LA `LA-NB-INT-005A` with `Require Allocation = true`; it is not part of the Cancel scope.
- The current Order Group status and related Lesson Allocation state are recorded before the action.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff starts a full-order Cancel for `OG-NB-INT-005P`. | The transaction requests impact detection before changing the Order Group. | action = full-order Cancel; expectedConsumedPoints = 3.5; excludedOrderGroupId = OG-NB-INT-005A |
| 2 | HQ or CM Staff reviews the impact warning. | A warning is presented because consumed-point impact exists. | expectedHasConsumedPoints = true; expectedHasImpact = true |
| 3 | HQ or CM Staff abandons the warning without continuing the full-order Cancel. | The full-order Cancel is not submitted. | confirmationChoice = abandon |
| 4 | HQ or CM Staff reopens the Order Group and related Lesson Allocation. | The Order Group status and consumed-points value are unchanged from the recorded state. | expectedOrderStatus = pre-action status; expectedConsumedPoints = 3.5 |

**Severity:** critical
**Priority:** high

---

### [Nichibei] Full-order Cancel impact handling – Assignment and consumed points – Continuing warning completes existing Cancel flow

**Description:** AC 02.1, AC 02.2 — State Transition — Combined impact is surfaced before staff continues the existing full-order Cancel flow.

**Preconditions:**
- HQ or CM Staff is logged in to the Nichibei Salesforce org.
- The full-order Cancel scope contains `OG-NB-INT-006A` with Assignment LA `LA-NB-INT-006A`, `Require Allocation = true`, and one scheduled session.
- The same full-order Cancel scope contains separate `OG-NB-INT-006P` with Point LA `LA-NB-INT-006P`, `Require Allocation = false`, and consumed points of `2.75` from that session.
- The expected existing full-order Cancel outcome for this scope is documented before execution.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff starts a full-order Cancel for the scope containing `OG-NB-INT-006A` and `OG-NB-INT-006P`. | An impact warning is presented before the destructive action completes. | action = full-order Cancel; orderGroupIds = [OG-NB-INT-006A, OG-NB-INT-006P]; expectedAssignedSessionCount = 1; expectedConsumedPoints = 2.75 |
| 2 | HQ or CM Staff reviews the warning detail. | The warning is based on both assignment and consumed-point impact. | expectedHasAssignment = true; expectedHasConsumedPoints = true |
| 3 | HQ or CM Staff continues from the warning. | The warning is accepted and the existing full-order Cancel flow continues. | confirmationChoice = continue |
| 4 | HQ or CM Staff reviews the Order Group and related Lesson Allocations after completion. | The Order Group is cancelled and the documented existing full-order Cancel outcome is applied after confirmation. | expectedOrderStatus = Cancelled; expectedLessonAllocationOutcome = documented baseline |

**Severity:** critical
**Priority:** high

---

### [Nichibei] Partial cancellation – Future-effective partial Cancel – Impact detection is not invoked

**Description:** AC 02.3 — Regression — A partial cancellation remains outside the destructive-action detector scope.

**Preconditions:**
- HQ or CM Staff is logged in to the Nichibei Salesforce org.
- Test Order Group `OG-NB-INT-007` supports partial cancellation with effective date `2026-11-30` before its original end date `2026-12-31`.
- An Order transaction log or debug trace is enabled for this execution.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff submits a partial Cancel for `OG-NB-INT-007` with effective date `2026-11-30`. | The partial cancellation follows its existing process without an impact warning. | action = partial Cancel; effectiveDate = 2026-11-30; originalEndDate = 2026-12-31 |
| 2 | HQ or CM Staff reviews the transaction trace. | No impact-detection request is recorded for the partial cancellation. | expectedDetectorInvocationCount = 0 |
| 3 | HQ or CM Staff reviews the related Lesson Allocation. | The existing partial-cancellation outcome is retained; no full-order destructive action is applied. | expectedLessonAllocationOutcome = existing partial-cancellation baseline |

**Severity:** major
**Priority:** high

---

### [Nichibei] Non-deleting order update – Update Slot order – Impact detection is not invoked

**Description:** AC 02.3 — Regression — A normal order update that does not delete a Lesson Allocation does not enter the detector flow.

**Preconditions:**
- HQ or CM Staff is logged in to the Nichibei Salesforce org.
- Test Order Group `OG-NB-INT-008` supports an Update Slot order from `2` to `3` purchased slots.
- An Order transaction log or debug trace is enabled for this execution.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff submits an Update Slot order for `OG-NB-INT-008` from `2` to `3` purchased slots. | The update follows its existing process without an impact warning. | action = Update Slot; originalPurchasedSlots = 2; updatedPurchasedSlots = 3 |
| 2 | HQ or CM Staff reviews the transaction trace. | No impact-detection request is recorded for the update. | expectedDetectorInvocationCount = 0 |
| 3 | HQ or CM Staff reviews the related Lesson Allocation. | The Lesson Allocation remains active and reflects only the documented update outcome. | expectedLessonAllocationOutcome = existing Update Slot baseline |

**Severity:** major
**Priority:** high
