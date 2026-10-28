# Test Coverage: LT-108574 — Nichibei void/cancel order impact detection

**Jira:** https://manabie.atlassian.net/browse/LT-108574
**Date:** 2026-10-09

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|---|---|
| 1 | AC 01.1 | An Order Group with neither scheduled assignments nor consumed points returns `hasImpact = false` and empty/zero detail. |
| 2 | AC 01.2 | Scheduled assignments produce assignment impact, aggregate count, affected allocation IDs, and per-allocation summaries. |
| 3 | AC 01.3 | Consumed points produce point impact, aggregate points, affected allocation IDs, and per-allocation summaries. |
| 4 | AC 01.4 | Simultaneous assignment and point impact returns both categories and `hasImpact = true`. |
| 5 | AC 01.5 | Multiple supplied Order Group IDs are evaluated as one request and their relevant details are aggregated. |
| 6 | AC 02.1 | Order calls the detector only before Void and full-order Cancel. |
| 7 | AC 02.2 | An impact warning is a soft gate: abandoning confirmation makes no change; continuing follows the existing destructive action. |
| 8 | AC 02.3 | Partial cancellation and non-deleting order updates do not call the detector and their existing behavior is unchanged. |

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC 01.1 | 1 | Conditional logic, Data integrity |
| AC 01.2 | 2 | Conditional logic, Data integrity |
| AC 01.3 | 3 | Conditional logic, Data integrity |
| AC 01.4 | 4 | Decision table, Data integrity |
| AC 01.5 | 5 | Data integrity, Boundary/range logic |
| AC 02.1 | 6 | State transition, Cross-system impact |
| AC 02.2 | 7 | State transition, Data integrity |
| AC 02.3 | 8 | Negative, Regression |

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Conditional logic | Decision Table, Negative |
| Data integrity | CRUD, Decision Table, Regression |
| Boundary/range logic | Boundary Value Analysis |
| State transition | State Transition, CRUD |
| Cross-system impact | Regression, Scenario |

## 4. Mandatory Edge-Case Review

| Checklist area | Applicability | Coverage decision |
|---|---|---|
| A. Configuration-driven thresholds | N/A | The API contract has no configurable threshold. |
| B. Date/time logic | N/A | The API reports current assignment/consumption state; it accepts no date/time input and has no documented date rule. |
| C. Concurrent/stale state | Yes | Include a retry/duplicate invocation scenario only if Order exposes retry behavior; it is not asserted as an API contract because the epic gives no idempotency requirement. |
| D. Permission/role | N/A | No role gate is specified for detector invocation; test data setup requires a staff account with Salesforce access. |
| E. State transition | Yes | Cover Void and full-order Cancel separately, plus the abort/continue confirmation branches. |
| F. Cross-system/cross-surface | Yes | Confirm the Order action invokes Lesson detection and uses its result before the destructive action. |
| G. Downstream effects | Yes | For confirmation abort, verify Order Group and Lesson Allocation remain unchanged. For continue, verify the existing Void/full-order Cancel flow executes; detailed archive/delete behavior is covered by legacy Lesson Allocation suites. |
| H. Display/ordering | N/A | The epic does not specify fields, wording, sort, or a Figma design for the warning. |
| H.1 Spec–Figma mismatch | N/A | No Figma URL is supplied. |

### Downstream Effects Inventory

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner |
|---|---|---|---|
| Void with impact, abandon warning | No destructive action occurs | Order Group and related Lesson Allocations | Integration TC 03 |
| Void with impact, continue | Existing Void flow executes after warning | Order Group and related Lesson Allocations | Integration TC 04 |
| Full-order Cancel with impact, abandon warning | No destructive action occurs | Order Group and related Lesson Allocations | Integration TC 05 |
| Full-order Cancel with impact, continue | Existing full-order Cancel flow executes after warning | Order Group and related Lesson Allocations | Integration TC 06 |

## 5. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC 01.1 | No assignment and no consumed point | Conditional, Data integrity | Decision Table | High | Standard |
| AC 01.2 | Assignment-only impact and summaries | Conditional, Data integrity | Decision Table | Critical | Deep |
| AC 01.3 | Consumed-point-only impact and summaries | Conditional, Data integrity | Decision Table | Critical | Deep |
| AC 01.4 | Both impact types in one response | Conditional, Data integrity | Decision Table | Critical | Deep |
| AC 01.5 | Multiple Order Group IDs aggregate results | Boundary/range, Data integrity | BVA, Decision Table | High | Standard |
| AC 02.1 | Invocation before Void and full-order Cancel | State transition, Cross-system | State Transition, Scenario | Critical | Deep |
| AC 02.2 | Soft-warning abort and continue branches | State transition, Data integrity | State Transition | Critical | Deep |
| AC 02.3 | Partial Cancel and update skip invocation | Negative, Regression | Decision Table, Regression | High | Standard |

## 6. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Impact calculation for assigned sessions and consumed points | A false negative permits unexpected Lesson Allocation removal; an incomplete summary misleads staff. | Prepared data for each impact combination; assert all booleans, totals, IDs, and summaries. |
| Gating the destructive action | Calling too late or bypassing the warning causes unintended data loss. | Trace Void/full-order Cancel from Order action through detector response to warning, abort, and continue branches. |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Multi-Order-Group aggregation | Omitting an affected allocation produces an unsafe false negative. | Use two Order Groups with distinct affected allocation data and assert combined totals and IDs. |
| Action scoping | A detector call during partial Cancel or normal update changes an out-of-scope flow. | Assert no detector invocation and unchanged existing flow for each non-target action. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Warning presentation | The epic specifies a soft gate but not exact wording. | Assert presence/absence and confirm/cancel behavior only; do not freeze unspecified text. |

## 7. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| API impact result | None found in this epic or related archive suites | None | ✅ All four data-state combinations and multi-Order-Group aggregation. |
| Void/full-order Cancel invocation | Legacy Void Order / Cancel Order archive cases | Partial | ✅ Pre-action detector invocation and soft-warning branches. |
| Partial cancellation | `Cancel Order – Partial Cancellation ... Lesson Allocation End Date Updated Only, Not Archived` | Partial | ✅ Assert detector is not invoked. |
| Non-deleting update | `Void Update Slot Order ... Existing Behavior Unchanged` | Partial | ✅ Assert detector is not invoked for a normal update flow. |

## 8. Suggested Test Suite Structure

```
epics/OOP/nichibei/LT-108574-handle-void-cancel-orders/test-cases/
├── order-group-impact-detection-api.md → AC 01.1–01.5 — Lesson-side detector contract
└── void-full-cancel-impact-integration.md → AC 02.1–02.3 — Order-to-Lesson integration and action scoping
```
