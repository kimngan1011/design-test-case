---
ticket_id: LT-108574
ticket_url: https://manabie.atlassian.net/browse/LT-108574
title: "[Nichibei] Handle void/cancel orders to prevent unexpected LA deletion"
module: scheduling
bucket: OOP/nichibei
status: In QA
internal_uat_date: null
production_release_date: null
last_updated: 2026-10-09
---

# Specification: LT-108574 — Nichibei void/cancel order impact detection

## Scope

The Lesson side supplies a detector for the Order side before an Order Group is voided or fully cancelled. The detector reports whether removing the related Lesson Allocations would affect scheduled lesson assignments or Nichibei consumed points. The Order side owns the action type and the warning/confirmation experience.

## API contract

**Input**

`DetectAssignmentByOrderGroupsRequest`

- `orderGroupIds`: required list of Order Group IDs.

**Output**

`DetectAssignmentByOrderGroupsResponse`

- `hasImpact`: `hasAssignment || hasConsumedPoints`.
- Assignment data: `hasAssignment`, `totalAssignedSessionCount`, `assignedLessonAllocationIds`, `assignedLessonAllocations`.
- Consumed-point data: `hasConsumedPoints`, `totalConsumedPoints`, `consumedPointLessonAllocationIds`, `consumedPointLessonAllocations`.
- Each allocation summary includes `lessonAllocationId`, `assignedSessionCount`, and `consumedPoints`.

## User stories and acceptance criteria

### US 01 — Detect impact for Order Group Lesson Allocations

**AC 01.1** — When the supplied Order Group has no scheduled lesson assignment and no consumed point, the detector returns no impact and empty/zero detail.

**AC 01.2** — When a supplied Order Group has one or more scheduled lesson assignments, the detector returns assignment impact, the total assigned-session count, and the affected Lesson Allocation IDs and summaries.

**AC 01.3** — In Nichibei, when a supplied Order Group has consumed points, the detector returns consumed-point impact, the total consumed points, and the affected Lesson Allocation IDs and summaries.

**AC 01.4** — When both conditions exist, the detector returns both categories and a combined impact without losing either allocation's summary.

**AC 01.5** — A request containing multiple Order Group IDs aggregates the relevant Lesson Allocation impact across those IDs.

### US 02 — Use detector only for destructive order actions

**AC 02.1** — Order invokes the detector before **Void** and before **full-order Cancel**.

**AC 02.2** — When impact exists, Order presents a soft warning/confirmation. Cancelling that confirmation leaves the Order Group and related Lesson Allocations unchanged; continuing keeps the existing Void/full-order Cancel flow.

**AC 02.3** — Partial cancellation and order updates that do not delete a Lesson Allocation do not invoke the detector and retain their existing flow.

## Out of scope

- Determining the requested action from the detector input. The request contains only Order Group IDs; Order supplies the Void/full-order Cancel context.
- Partial cancellation behavior beyond confirming that the detector is not invoked.
- Changes to the existing void/cancel business outcome after the user confirms the warning.
- UI wording/design not specified in the epic.

## Evidence and assumptions

- Jira epic LT-108574 and linked feature LT-108579 define Lesson-side detection and Order-side soft validation.
- The supplied Execute Anonymous snippet calls `OrderGroupAssignmentDetector.detectAssignmentByOrderGroups` with a list of request objects.
- The class was executed successfully in the Nichibei pre-production org during exploratory validation; exact response values require purpose-built data states.
