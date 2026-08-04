---
ticket_id: LT-57816
ticket_url: https://manabie.atlassian.net/browse/LT-57816
title: "[Renseikai] Copy lesson report fields values to lesson report details (per student)"
module: scheduling
bucket: lesson/lesson report
status: Done
internal_uat_date: null
production_release_date: null
last_updated: 2026-07-31
---

# LT-57816: Copy Lesson Report Values to Lesson Report Details

## Summary

For a Group lesson, the system must persist the shared Lesson Report values for **Content**, **Next Lesson's Announcement**, and **Next Lesson's Homework** in every per-student Lesson Report Detail. When any of these shared values is changed, all affected details must be updated to the new value so mobile report requests can read per-student data without extra aggregation.

The requested QA scope confirms the value-persistence behaviour on both Salesforce (SF) and Back Office (BO), and on both report surfaces: **Lesson Report under Lesson** and **Lesson Report Detail**.

## Acceptance Criteria

- **AC 01.1 — Initial value propagation:** Given a lesson has Teaching Method = Group, when Content, Next Lesson's Announcement, and Next Lesson's Homework are stored on the Lesson Report, the respective value is stored on each Lesson Report Detail for the students in that lesson.
- **AC 01.2 — Update propagation:** Given a Group lesson already has Lesson Report Details, when a shared Lesson Report value is updated, the corresponding value on every existing Lesson Report Detail is replaced by the updated value.
- **AC 01.3 — Preserve stored values on unrelated updates:** Given the three shared values have been stored, when the user updates any other Lesson Report field, Content, Next Lesson's Announcement, and Next Lesson's Homework retain their existing values on the Lesson Report and every Lesson Report Detail.
- **AC 01.4 — Stored-value evidence:** After an SF or BO update, the persisted values are evidenced for each student in both systems: in Salesforce, open the student's Lesson Allocation → **Report History** → **Lesson Report Details**; in BO, open the target Lesson → the student's **Report History**. The target lesson row's `Content`, `Next Lesson - Homework`, and `Next Lesson - Announcement` values must match the saved values.
- **AC 01.5 — Learner App visibility after publication:** Given the Lesson and its Lesson Report are Published, the enrolled student sees the same stored Content, Next Lesson's Announcement, and Next Lesson's Homework values on the Learner App.

## Business Rules

| # | AC | Business rule | Field / entity | Behaviour | Platform |
| --- | --- | --- | --- | --- | --- |
| 1 | AC 01.1 | Propagation applies only when the lesson Teaching Method is Group. | Lesson.Teaching Method | Conditional | SF, BO |
| 2 | AC 01.1 | A stored Content value is copied to the Content field of every Lesson Report Detail belonging to the Lesson Report. | Lesson Report → Lesson Report Detail.Content | Auto-copied | SF, BO |
| 3 | AC 01.1 | A stored Next Lesson's Announcement value is copied to the respective field of every Lesson Report Detail belonging to the Lesson Report. | Lesson Report → Lesson Report Detail.Next Lesson's Announcement | Auto-copied | SF, BO |
| 4 | AC 01.1 | A stored Next Lesson's Homework value is copied to the respective field of every Lesson Report Detail belonging to the Lesson Report. | Lesson Report → Lesson Report Detail.Next Lesson's Homework | Auto-copied | SF, BO |
| 5 | AC 01.2 | Updating any of the three shared Lesson Report values updates that same field on all existing per-student details; a previously stored value must not remain. | Lesson Report Detail (per student) | Update / overwrite | SF, BO |
| 6 | AC 01.3 | Updating a Lesson Report field other than Content, Next Lesson's Announcement, or Next Lesson's Homework does not clear, replace, or change any of those three stored values on the source report or its per-student details. | Lesson Report → Lesson Report Detail | Preserve on unrelated update | SF, BO |
| 7 | AC 01.4 | The saved values are stored for each student and shown in Salesforce Student Lesson Allocation → Report History → Lesson Report Details and BO Lesson → Student Report History, in the Content, Next Lesson - Homework, and Next Lesson - Announcement fields. | Student Report History | Stored-value evidence | SF, BO |
| 8 | AC 01.5 | After both the Lesson and Lesson Report are Published, the enrolled student sees the same three stored values on the Learner App. | Lesson Report Detail → Learner App | Published visibility / cross-system persistence | Mobile |

## Conflict & Gap Analysis

| # | Tag | Source | AC | Finding |
| --- | --- | --- | --- | --- |
| 1 | [EXTENDED] | Scheduling domain model | AC 01.1–01.2 | The existing model establishes Lesson → Lesson Report → Lesson Report Detail (per student). LT-57816 adds the explicit shared-field propagation and update-overwrite rule for Group lessons. |
| 2 | [REGRESSION RISK] | Qase PX suites 427 and 1748 | AC 01.3–01.4 | Existing BO suites cover Lesson Report under Lesson and Lesson Report Detail separately. The new cases must confirm that an unrelated update neither overwrites the shared values nor makes the surfaces diverge. |
| 3 | [REGRESSION RISK] | SF → BO data flow | AC 01.3–01.4 | SF is the source of truth for lesson management and BO exposes teaching/report features. A delayed or partial save could leave the source report and student details with different values. |
| 4 | [REGRESSION RISK] | Learner App report display | AC 01.5 | The feature's purpose is to simplify Mobile API access. Published reports must expose each student's stored detail values rather than stale or missing shared-field data. |
| 5 | [MISSING BEHAVIOR] | Jira ticket | — | The ticket does not state whether an Individual teaching method receives the same propagation. It is out of scope; the proposed tests use Group lessons only. |

## Clarification Questions

No open question for this scope. The user confirmed that validation must cover SF and BO, and both Lesson Report under Lesson and Lesson Report Detail. Individual lessons are not included because the Jira condition is explicitly Group.

## Related Specs

- `knowledge/domain-knowledge/scheduling/lesson-management/lesson.md` — Lesson Report is tied to a lesson and student, with per-student Lesson Report Details; SF → BO → Mobile data flow and published report visibility on Mobile.
- `knowledge/domain-knowledge/scheduling/lesson-management/student-session.md` — Student sessions represent the per-lesson student relationship that determines the affected per-student records.

## Related Test Cases

- Qase PX suite 292 — Lesson Report BO (target suite supplied by the user).
- Qase PX suite 427 — Lesson Report under Lesson (BO child suite).
- Qase PX suite 1748 — Lesson Report Detail (BO child suite).
- Qase PX suite 254 / child suites 401 and 426 — SF Lesson Report surfaces.

## QASE Coverage Gaps

No Qase case with a title matching “Copy lesson report” was found. New coverage is needed for initial propagation, update-overwrite, preservation on unrelated updates, and post-publication Learner App visibility of all three values.
