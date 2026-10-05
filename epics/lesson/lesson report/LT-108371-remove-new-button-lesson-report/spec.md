---
ticket_id: LT-108371
ticket_url: https://manabie.atlassian.net/browse/LT-108371
title: Remove "New" button from Lesson Report in LA detail page
module: scheduling
bucket: lesson
status: Ready for QA
internal_uat_date: null
production_release_date: null
last_updated: 2026-09-15
---

# LT-108371: Remove "New" button from Lesson Report in LA detail page

## Summary

Remove the `New` button from the Lesson Report tab on the Salesforce Lesson Allocation (LA) Detail page. Validation covers the requested STAG/PREPROD tenant matrix plus three access profiles.

Deep impact analysis was intentionally skipped at the user's direction. This specification is limited to the supplied Jira requirement and the matrix below.

---

## Acceptance Criteria

### AC 01 — New button removal

On the Salesforce Lesson Allocation Detail page, the Lesson Report tab must not display a button labelled `New`.

| Test scope | Environment | Partner type | Partner / access profile |
|---|---|---|---|
| Tenant | STAG | Core Partner | Core Partner |
| Tenant | PREPROD | Core Partner | Renseikai |
| Tenant | PREPROD | Custom Partner | Nichibei |
| Tenant | PREPROD | Custom Partner | EEA |
| Tenant | PREPROD | Custom Partner | Aver |
| Tenant | PREPROD | Custom Partner | Riso |
| Access profile | Execution environment selected in Qase | N/A | `full_access` permission set |
| Access profile | Execution environment selected in Qase | N/A | `center_level_edit` permission set |
| Access profile | Execution environment selected in Qase | N/A | Admin |

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---:|---|---|---|---|---|
| 1 | AC 01 | `New` is not displayed for a Core Partner on STAG. | New button | hidden | Salesforce / STAG |
| 2 | AC 01 | `New` is not displayed for Renseikai Core Partner on PREPROD. | New button | hidden | Salesforce / PREPROD |
| 3 | AC 01 | `New` is not displayed for Nichibei Custom Partner on PREPROD. | New button | hidden | Salesforce / PREPROD |
| 4 | AC 01 | `New` is not displayed for EEA Custom Partner on PREPROD. | New button | hidden | Salesforce / PREPROD |
| 5 | AC 01 | `New` is not displayed for Aver Custom Partner on PREPROD. | New button | hidden | Salesforce / PREPROD |
| 6 | AC 01 | `New` is not displayed for Riso Custom Partner on PREPROD. | New button | hidden | Salesforce / PREPROD |
| 7 | AC 01 | `New` is not displayed for a user with the `full_access` permission set. | New button | hidden | Salesforce |
| 8 | AC 01 | `New` is not displayed for a user with the `center_level_edit` permission set. | New button | hidden | Salesforce |
| 9 | AC 01 | `New` is not displayed for an Admin user. | New button | hidden | Salesforce |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

No conflicts were assessed because the user asked to skip deep analysis. The local Riso LA Detail tests demonstrate tenant-specific hidden controls, but do not document the `New` button in the Lesson Report tab.

### Missing in Requirements

| # | Tag | Source | Description |
|---:|---|---|---|
| 1 | [MISSING BEHAVIOR] | Jira LT-108371 | Other pages, tabs, and action menus are not in scope; no assertion is made about a `New` button outside the Lesson Report tab. |

### Lesson-Learned Risks

No lesson-learned analysis was performed at the user's direction.

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-01 | Core Lesson Lifecycle | LA and Lesson Report entities are used, but the `New` button is not covered. | No E2E change requested |

### Assumptions Made

- `LA Detail` means the Salesforce Lesson Allocation Detail page accessed from Contact → Course.
- The expected text of the removed control is exactly `New`.
- The four Custom Partner cases are PREPROD, following the user's prior direction that remaining tenant coverage is PREPROD.
- Role-case titles intentionally do not identify an environment; the Qase execution environment will be chosen when the cases run.

---

## Clarification Questions

Not posted. No Jira comment was created because deep analysis was skipped.

## Related Specs

- `epics/OOP/riso/LT-92532-riso-create-update-la-on-ui/test-cases/la-detail.md` — establishes a precedent for tenant-specific absent controls on LA Detail.

## Related Test Cases

- `epics/OOP/riso/LT-92532-riso-create-update-la-on-ui/test-cases/la-detail.md` — related LA Detail visibility coverage; not a duplicate.

## QASE Coverage Gaps

- AC 01 — Qase suite 3533 contains no test cases; nine visibility cases are required.
