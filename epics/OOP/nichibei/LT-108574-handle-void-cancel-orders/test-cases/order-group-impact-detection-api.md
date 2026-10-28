# Test Cases: LT-108574 — Order Group impact detection

## Suite: [Nichibei] Order Group Impact Detection API

### [Nichibei] Order Group Impact Detection – Empty impact state – No impact and zero detail returned

**Description:** AC 01.1 — Decision Table — An Order Group without scheduled assignments or consumed points produces an empty impact result.

**Preconditions:**
- HQ or CM Staff is logged in to the Nichibei Salesforce org and can use Developer Console.
- Test Order Group `OG-NB-API-001A` has Assignment LA `LA-NB-API-001A` with `Require Allocation = true` and zero scheduled student sessions.
- Test Order Group `OG-NB-API-001P` has Point LA `LA-NB-API-001P` with `Require Allocation = false` and consumed points of `0`.
- The actual Salesforce IDs for both test Order Groups are recorded for this execution.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff runs one detector request with the recorded IDs for `OG-NB-API-001A` and `OG-NB-API-001P`. | One response is returned for the request. | orderGroupIds = [OG-NB-API-001A, OG-NB-API-001P] |
| 2 | HQ or CM Staff inspects the response impact flags and aggregate values. | `hasImpact`, `hasAssignment`, and `hasConsumedPoints` are `false`; assigned-session count is `0`; consumed-points total is `0`. | expectedAssignedSessionCount = 0; expectedConsumedPoints = 0 |
| 3 | HQ or CM Staff inspects the affected allocation IDs and summaries. | Both affected-allocation ID lists and both summary lists are empty. | expectedAssignedAllocationIds = []; expectedConsumedPointAllocationIds = [] |

**Severity:** major
**Priority:** high

---

### [Nichibei] Order Group Impact Detection – Scheduled assignment sessions – Assignment impact returned without point impact

**Description:** AC 01.2 — Decision Table — Scheduled sessions are reported from the Assignment LA while consumed points on an out-of-scope Point LA are excluded.

**Preconditions:**
- HQ or CM Staff is logged in to the Nichibei Salesforce org and can use Developer Console.
- Test Order Group `OG-NB-API-002A` has Assignment LA `LA-NB-API-002A` with `Require Allocation = true` and exactly two scheduled student sessions.
- A separate, active Order Group `OG-NB-API-002P` has Point LA `LA-NB-API-002P` with `Require Allocation = false` and consumed points of `4` from those sessions.
- The actual Salesforce ID for `OG-NB-API-002A` is recorded; `OG-NB-API-002P` is deliberately excluded from the request.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff runs the supplied detector request with the recorded ID for `OG-NB-API-002A`. | One response is returned for the request. | orderGroupIds = [OG-NB-API-002A]; excludedOrderGroupId = OG-NB-API-002P |
| 2 | HQ or CM Staff inspects the assignment section of the response. | `hasAssignment` and `hasImpact` are `true`; total assigned-session count is `2`; affected assignment ID list contains only `LA-NB-API-002A`; its summary has assigned-session count `2`. | expectedAssignedSessionCount = 2; expectedAssignmentAllocationIds = [LA-NB-API-002A] |
| 3 | HQ or CM Staff inspects the consumed-point section of the response. | `hasConsumedPoints` is `false`; total consumed points is `0`; consumed-point IDs and summaries are empty. | expectedConsumedPoints = 0; expectedConsumedPointAllocationIds = [] |

**Severity:** critical
**Priority:** high

---

### [Nichibei] Order Group Impact Detection – Consumed points without scheduled sessions – Point impact returned without assignment impact

**Description:** AC 01.3 — Decision Table — A point-only Lesson Allocation is reported even when it has no scheduled student session.

**Preconditions:**
- HQ or CM Staff is logged in to the Nichibei Salesforce org and can use Developer Console.
- Test Order Group `OG-NB-API-003P` has Point LA `LA-NB-API-003P` with `Require Allocation = false` and consumed points of `3.5`.
- A separate, active Order Group `OG-NB-API-003A` has Assignment LA `LA-NB-API-003A` with `Require Allocation = true` and two scheduled student sessions.
- The actual Salesforce ID for `OG-NB-API-003P` is recorded; `OG-NB-API-003A` is deliberately excluded from the request.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff runs the supplied detector request with the recorded ID for `OG-NB-API-003P`. | One response is returned for the request. | orderGroupIds = [OG-NB-API-003P]; excludedOrderGroupId = OG-NB-API-003A |
| 2 | HQ or CM Staff inspects the consumed-point section of the response. | `hasConsumedPoints` and `hasImpact` are `true`; total consumed points is `3.5`; affected point ID list contains only `LA-NB-API-003P`; its summary has consumed points `3.5`. | expectedConsumedPoints = 3.5; expectedConsumedPointAllocationIds = [LA-NB-API-003P] |
| 3 | HQ or CM Staff inspects the assignment section of the response. | `hasAssignment` is `false`; total assigned-session count is `0`; assignment IDs and summaries are empty because Assignment LA `LA-NB-API-003A` belongs to excluded `OG-NB-API-003A`. | expectedAssignedSessionCount = 0; expectedAssignmentAllocationIds = [] |

**Severity:** critical
**Priority:** high

---

### [Nichibei] Order Group Impact Detection – Assignment and point impact – Both categories and summaries returned

**Description:** AC 01.4 — Decision Table — The response retains assignment and consumed-point details when both impacts exist.

**Preconditions:**
- HQ or CM Staff is logged in to the Nichibei Salesforce org and can use Developer Console.
- Test Order Group `OG-NB-API-004A` has Assignment LA `LA-NB-API-004A` with `Require Allocation = true` and three scheduled student sessions.
- Separate Test Order Group `OG-NB-API-004P` has Point LA `LA-NB-API-004P` with `Require Allocation = false` and consumed points of `4.25` from those sessions.
- The actual Salesforce IDs for both test Order Groups are recorded for this execution.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff runs one detector request with the recorded IDs for `OG-NB-API-004A` and `OG-NB-API-004P`. | One response is returned for the request. | orderGroupIds = [OG-NB-API-004A, OG-NB-API-004P] |
| 2 | HQ or CM Staff inspects the assignment impact in the response. | `hasAssignment` is `true`; total assigned-session count is `3`; the assignment IDs and summaries contain `LA-NB-API-004A` with assigned-session count `3`. | expectedAssignedSessionCount = 3; expectedAssignmentAllocationIds = [LA-NB-API-004A] |
| 3 | HQ or CM Staff inspects the consumed-point impact in the response. | `hasConsumedPoints` is `true`; total consumed points is `4.25`; the point IDs and summaries contain `LA-NB-API-004P` with consumed points `4.25`. | expectedConsumedPoints = 4.25; expectedConsumedPointAllocationIds = [LA-NB-API-004P] |
| 4 | HQ or CM Staff inspects the combined impact flag. | `hasImpact` is `true` and neither category's IDs or summary is omitted. | expectedHasImpact = true |

**Severity:** critical
**Priority:** high

---

### [Nichibei] Order Group Impact Detection – Four Order Groups – Totals and affected allocations aggregated

**Description:** AC 01.5 — Decision Table — One request aggregates distinct assignment and point impact from two supplied Order Groups.

**Preconditions:**
- HQ or CM Staff is logged in to the Nichibei Salesforce org and can use Developer Console.
- Test Order Groups `OG-NB-API-005A1` and `OG-NB-API-005A2` have Assignment LAs `LA-NB-API-005A1` and `LA-NB-API-005A2`, each with `Require Allocation = true` and respectively one and two scheduled student sessions.
- Separate Test Order Groups `OG-NB-API-005P1` and `OG-NB-API-005P2` have Point LAs `LA-NB-API-005P1` and `LA-NB-API-005P2`, each with `Require Allocation = false` and respectively consumed points of `1.5` and `2.75`.
- The actual Salesforce IDs for all four test Order Groups are recorded for this execution.

| # | Action | Expected Result | Test Data |
|---|---|---|---|
| 1 | HQ or CM Staff runs one detector request containing the recorded IDs for all four test Order Groups. | One aggregated response is returned for the request. | orderGroupIds = [OG-NB-API-005A1, OG-NB-API-005A2, OG-NB-API-005P1, OG-NB-API-005P2] |
| 2 | HQ or CM Staff inspects assignment impact and its summary. | `hasAssignment` is `true`; total assigned-session count is `3`; assignment IDs and summaries contain `LA-NB-API-005A1` with count `1` and `LA-NB-API-005A2` with count `2`. | expectedAssignedSessionCount = 3; expectedAssignmentAllocationIds = [LA-NB-API-005A1, LA-NB-API-005A2] |
| 3 | HQ or CM Staff inspects consumed-point impact and its summary. | `hasConsumedPoints` is `true`; total consumed points is `4.25`; point IDs and summaries contain `LA-NB-API-005P1` with points `1.5` and `LA-NB-API-005P2` with points `2.75`. | expectedConsumedPoints = 4.25; expectedConsumedPointAllocationIds = [LA-NB-API-005P1, LA-NB-API-005P2] |
| 4 | HQ or CM Staff inspects the combined result. | `hasImpact` is `true`; each affected allocation appears once in the category matching its Require Allocation value. | expectedHasImpact = true; expectedDistinctAllocationCount = 4 |

**Severity:** major
**Priority:** high
