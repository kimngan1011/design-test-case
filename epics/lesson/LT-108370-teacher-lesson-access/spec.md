---
ticket_id: LT-108370
ticket_url: https://manabie.atlassian.net/browse/LT-108370
title: "[SF] Handle case when a teacher is assigned to lessons without user account"
module: scheduling
bucket: lesson
status: Done
internal_uat_date: null
production_release_date: null
last_updated: 2026-10-08
---

# LT-108370 — Teacher Lesson Access

## Summary

A teacher may be assigned to one or more lessons before the teacher's Salesforce User exists or while that User is inactive. The normal lesson-driven sharing calculation cannot create `Lesson__Share` without an active User, leaving the teacher with an empty lesson list in Back Office after login. The linked implementation creates a user-driven recovery flow: active User creation or reactivation queues the Contact, then grants only the missing lesson and lesson-allocation shares.

Source PBT-2876 reports the issue affected at least 52 teachers from January 2026. The linked implementation is PR #22832, merged to `develop`.

## Acceptance Criteria

| ID | Criterion |
|---|---|
| AC-01 | When an active Salesforce User is created for a Contact already assigned as a lesson teacher, the teacher can access all assigned lessons in Back Office. |
| AC-02 | When an inactive teacher User is reactivated, missing access for the Contact's assigned lessons is restored. |
| AC-03 | The recovery creates the required lesson and non-deleted student-session lesson-allocation shares with Edit access and `Lesson_Teacher__c` row cause. |
| AC-04 | Reprocessing is idempotent: it does not duplicate shares or alter another teacher's shares. |
| AC-05 | The process does not enqueue or grant shares for a Contact that has no lesson-teacher assignment. |
| AC-06 | The Master Queue prevents duplicate pending/failed work for the same Contact, but a completed run may be queued again after a later activation. |
| AC-07 | The recovery remains reliable at 100 teacher Users × 100 lesson assignments. |

## Business Rules

| ID | Rule |
|---|---|
| BR-01 | An active User created after the Contact was assigned to a lesson must trigger repair of access for that Contact. |
| BR-02 | Reactivating an inactive User must trigger the same repair. |
| BR-03 | Each missing qualifying `Lesson__Share` is inserted for the linked active User with Edit access and `Lesson_Teacher__c` row cause. |
| BR-04 | Each missing `Lesson_Allocation__Share` for a non-deleted Student Session of a qualifying lesson is inserted for the same active User. |
| BR-05 | A Contact without `Lesson_Teacher__c` records creates neither queue work nor shares. |
| BR-06 | The repair is insert-only and idempotent; existing shares, including another teacher's, stay intact. |
| BR-07 | The User-triggered flow uses Master Queue asynchronously to avoid mixed DML between User and `Master_Queue__c`. |
| BR-08 | Existing Pending or Failed queue records suppress another enqueue for the same Contact; Success does not suppress a later legitimate run. |
| BR-09 | One Contact is processed per batch transaction to protect governor limits for teachers with a long lesson history. |
| BR-10 | The feature must be proven under the requested 100 Users × 100 Lessons stress scenario. |

## Conflict & Gap Analysis

- **[REGRESSION RISK]** PBT-2876 describes a proposed scheduled job for recovery of the known affected population, while PR #22832 implements event-driven recovery on User creation/reactivation. No evidence confirms a backfill job for users who were already active before this feature deployed.
- **[SCOPE OBSERVATION]** PR #22832 also removes the Lesson Allocation related-list **New** action, apparently linked to LT-108372 rather than LT-108370. It must not be counted as this feature's acceptance coverage.
- **[PERFORMANCE RISK]** The ticket comment explicitly requests a 100 × 100 stress scenario. The implementation's batch size of one Contact limits per-transaction DML, but execution timing and final queue state still need measurement in the target environment.

## Clarification Questions

Not posted. The Jira ticket is Done and the linked PR is merged; questions below are verification decisions for QA rather than release blockers.

1. Is a separate scheduled backfill expected for the 52 teachers already affected before deployment, or is remediation handled outside this feature?
2. What completion threshold and environment should define passing the 100 × 100 performance test?

## Related Specs

- [LT-108370](https://manabie.atlassian.net/browse/LT-108370)
- [PBT-2876](https://manabie.atlassian.net/browse/PBT-2876)
- [PR #22832](https://github.com/manabie-com/erp-salesforce/pull/22832)

## Related Test Cases

No existing Qase cases found in PX suite 3703 as of 2026-10-08.

## QASE Coverage Gaps

All coverage for this feature is new in suite PX/3703. Required coverage includes create-active-user recovery, reactivation recovery, lesson/allocation share content, no-assignment behavior, idempotency, queue deduplication/requeue, deleted-session handling, and 100 × 100 stress behavior.
