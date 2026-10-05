---
ticket_id: LT-96228
ticket_url: https://manabie.atlassian.net/browse/LT-96228
title: "[Riso] OOP | Restrict editing lessons after completion"
module: scheduling
bucket: OOP/riso
status: Ready for QA
internal_uat_date: null
production_release_date: null
last_updated: 2026-09-09
---

# LT-96228: Restrict editing lessons after completion

## Summary

Riso needs to protect completed lessons from an unauthorized rollback to Published. The restriction is controlled by the custom permission defined for this epic: any staff member with that permission may perform the correction; staff without it may not.

The requirement is limited to two Salesforce entry points: SF Lesson Details and SF Lesson List bulk status change. It restricts only Completed → Published; it does not freeze other lesson edits or add a monthly-closing rule.

---

## Acceptance Criteria

### US01 — Prevent non-HQ users from reverting a completed lesson

As a staff member without the custom permission defined for this epic, I should not change a completed lesson back to Published, to preserve data integrity and compliance.

#### AC01.1

**Given** the lesson is marked as `Complete` and the user does **not** have the epic's custom permission  
**When** the user tries to revert the completed lesson status to `Publish`  
**Then** show: `You are not allowed to change the status of a completed lesson.`

Japanese message supplied in the ticket: `完了済の授業のステータスを変更するには権限が必要です。`

Named surfaces:

1. [SF] Lesson Details
2. [SF] Lesson List — Bulk Change Lesson Status

### US02 — Allow authorized corrections

As a staff member with the custom permission defined for this epic, I can update a completed lesson status to make an approved correction.

#### AC02.1

**Given** the lesson is marked as `Complete` and the user has the epic's custom permission  
**When** the user tries to revert the completed lesson status to `Publish`  
**Then** the lesson status changes to `Publish` and Lesson Details become editable again.

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---:|---|---|---|---|---|
| 1 | AC01.1 | A completed lesson cannot be reverted to Published by a user without the custom permission defined for this epic. | Lesson Status | locked | SF |
| 2 | AC01.1 | An unauthorized rollback attempt shows the exact English error. | Lesson Status | locked | SF |
| 3 | AC01.1 | An unauthorized rollback attempt in Japanese locale uses the supplied Japanese message. | Lesson Status | locked | SF |
| 4 | AC02.1 | A staff member with the custom permission defined for this epic may revert a completed lesson to Published. | Lesson Status | editable | SF |
| 5 | AC02.1 | After an authorized rollback, Lesson Details are editable again. | Lesson Details | editable | SF |
| 6 | AC01.1 | A blocked Completed → Published attempt does not send a teacher email. | Teacher email | no-send | SF |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---:|---|---|---|---|
| 1 | [CONFLICT] | `epics/lesson/LT-XXXX-lesson-status/test-cases/lesson-status.md` — TC-1456 step 3; TC-1470 bulk update | AC01.1, AC02.1 | Existing core tests expect Completed → Published without a permission condition. Riso must add a tenant-and-custom-permission-specific exception while retaining the authorized path. |

### Missing in Requirements

| # | Tag | Source | Description |
|---:|---|---|---|
| 1 | [REPLACED] | `epics/lesson/LT-XXXX-lesson-status/test-cases/lesson-status.md` — TC-1456 step 3; TC-1470 bulk update | Riso replaces the core unrestricted rollback expectation with a custom-permission check across the named entry points. |
| 2 | [EXTENDED] | `epics/OOP/riso/LT-101725-lesson-publish-notifications/spec.md` — AC-09 / BR-16–BR-25 | A blocked Completed → Published attempt must send no teacher email; this preserves the existing Draft → Published notification trigger boundary. |

### Lesson-Learned Risks

No relevant historical incidents found after reviewing all scheduling core and OOP lesson-learned entries. The prior incidents concern student-session assignment, duplication, or allocation synchronization rather than status-rollback authorization.

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| New | [Riso] Completed Lesson Rollback Authorization | No scenario covers the two in-scope Salesforce entry points with and without the epic custom permission. | CREATE |

### Assumptions Made

- The feature is Riso-only because the Jira title and description state `Riso | OOP`.
- `Publish` in the Jira text means the documented `Published` lesson status.
- The custom permission's API name and assignment model are implementation details to be resolved from the epic; test cases will identify it by its configured label/API name once available.
- The ticket’s date custom field is not treated as an internal-UAT or production-release date because its semantic field name was not available.

---

## Clarification Questions

All three clarification questions were resolved by the requester on 2026-09-09. No Jira comment was requested or posted.

1. Authorization is determined by the custom permission defined for this epic, not by staff role. Any staff member with that permission may revert Completed → Published.
2. When the change is blocked, no teacher email is sent.
3. Scope is limited to restricting Completed → Published; do not expand it to a monthly-closing or general lesson-edit freeze.

---

## Related Specs

- `epics/OOP/riso/LT-101725-lesson-publish-notifications/spec.md` — Riso bulk-publish notifications from the same named action surfaces.

## Related Test Cases

- `epics/lesson/LT-XXXX-lesson-status/test-cases/lesson-status.md` — Core detailed and bulk Completed → Published assertions that must be scoped for Riso authorization.
- `epics/OOP/riso/LT-101725-lesson-publish-notifications/test-cases/bulk-publish-email.md` — Teacher-email trigger boundary for bulk publishing.

## QASE Coverage Gaps

- The linked Qase PX suite 3492 exists but has no test cases.
- AC01.1 — No Qase coverage for an unauthorized Completed → Published attempt at any named entry point, including exact English/Japanese error, no status change, and no teacher email.
- AC02.1 — No Qase coverage for a staff member with the epic custom permission to correct the status and restore Lesson Details editability.
- Cross-surface consistency for the two in-scope Salesforce entry points has no case coverage in the linked suite.
