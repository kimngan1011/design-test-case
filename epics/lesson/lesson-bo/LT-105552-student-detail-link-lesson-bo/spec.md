---
ticket_id: LT-105552
ticket_url: https://manabie.atlassian.net/browse/LT-105552
title: Add link to student detail page from Lesson Detail in BO
module: lesson-management
status: in QA
internal_uat_date: null
production_release_date: null
last_updated: 2026-07-16
---

# LT-105552: Add link to student detail page from Lesson Detail in BO

## Summary

Add clickable hyperlinks on each student name in the Student List on the Lesson Detail page in BO. Clicking a student name navigates the user to the BO Student Detail page. Access to view and edit the student detail page is governed by the user's SF permissions.

---

## Acceptance Criteria

### Objective
Add a link from each student name in the Lesson Detail page to the student detail page in BO.

### Context
Staff members and teachers who can access BO need to open student details from the Lesson Detail page.

### Scope
- AC 01.1: Add a link to the student detail page from each student name in the Student List on the Lesson Detail page in BO.
- AC 01.2: Student detail page view and edit access must follow SF permissions.
- AC 01.3: The link should work for everyone (all BO users).

### Success Criteria
- SC 01: A staff member or teacher can click a student name in BO and open the student detail page.
- SC 02: The student detail page shows details according to the user's access permissions.
- SC 03: View and edit behavior follows SF permissions.

> **Confirmed via comment (Tuyen Hua, 2026-07-14):** The link navigates to the **BO Student Detail page** (not SF). Evidence: _"BO student details em @Loi Pham — Lesson → navigate to BO Student detail page"_

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---|---|---|---|---|---|
| BR-01 | AC 01.1 | Each student name in the Student List on the Lesson Detail page is rendered as a clickable hyperlink | Student name | clickable link | [BO] |
| BR-02 | AC 01.1 | Clicking a student name navigates the user to the BO Student Detail page for that student | Student name link | navigates to BO student detail | [BO] |
| BR-03 | AC 01.2 | View access on the BO Student Detail page is controlled by the user's SF permissions | Student Detail page | view-only / editable based on SF role | [BO] |
| BR-04 | AC 01.2 | Edit access on the BO Student Detail page is controlled by the user's SF permissions; users without edit rights cannot modify student data | Student Detail page | locked / editable based on SF role | [BO] |
| BR-05 | AC 01.3 | The student name hyperlink is visible to all BO users regardless of role (HQ Staff, Centre Manager, Teacher CPU/SPU) | Student name | visible to all BO roles | [BO] |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---|---|---|---|---|
| — | — | — | — | No direct conflicts with existing documented behavior |

### Missing in Requirements

| # | Tag | Source | Description |
|---|---|---|---|
| 1 | [MISSING BEHAVIOR] | AC 01.2, AC 01.3 | No AC defines what happens when a user has **no permission to view the BO Student Detail page at all** — does the link still render but show an access-denied/error page, or is the link hidden/disabled for restricted users? |
| 2 | [ROLE GAP] | AC 01.3 ("for everyone") | AC says link "should work for everyone" but does not confirm behavior for **Teacher CPU/SPU** roles specifically. CPU can only see lessons assigned to them — does the student detail link respect or bypass that scoping? |
| 3 | [MISSING BEHAVIOR] | Lesson Detail → Student List | No AC specifies behavior when the student name link is clicked on a **Completed or Cancelled lesson** — should the link still navigate to student detail? |
| 4 | [UNDOCUMENTED IN AC] | Comment by Tuyen Hua (2026-07-14) | The Jira description does not explicitly state the destination is BO (not SF). This was confirmed only via comment. AC should be updated to explicitly state "navigates to BO Student Detail page." |

### Lesson-Learned Risks

| # | Incident | Date | AC | Risk | Guardrail |
|---|---|---|---|---|---|
| — | — | — | — | No past incidents directly relevant to this navigation feature | — |

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-01 | Lesson Lifecycle — Create, Teach, Report, View | Step 9: Teacher on BO Lesson Detail can now click student names to navigate to BO Student Detail | UPDATE — add optional step after Step 9 |

### Assumptions Made

- The destination is the BO Student Detail page (confirmed via comment). SF Student Detail is out of scope.
- "All users who can access BO" includes HQ Staff, Centre Manager, and Teacher roles (CPU/SPU).
- The Student List where the link appears is the same Student Sessions section already visible on the Lesson Detail page in BO.
- SF permissions that govern the student detail page view/edit are the existing role-based permissions — no new permission model is introduced.

---

## Clarification Questions

1. **[MISSING BEHAVIOR]** When a user with **no access** to the BO Student Detail page clicks the student name link, what should happen — does the system show an error/access-denied page, or should the link be hidden/disabled for that user?
   _Evidence: AC 01.2 says "access must follow SF permissions" but does not define the no-permission UI state._

2. **[ROLE GAP]** Does the student name link work for **Teacher (CPU/SPU)** roles in BO? CPU teachers are scoped to only see lessons assigned to them — is the student detail page accessible to a CPU teacher even for a student from that scoped lesson?
   _Evidence: AC 01.3 says "The link should work for everyone" — clarify if this includes Teacher roles explicitly._

3. **[MISSING BEHAVIOR]** Should the student name link still be active (clickable) on **Completed or Cancelled lessons**, or should it behave differently than on Draft/Published lessons?
   _Evidence: No AC specifies lesson-status scope for the link behavior._

---

## Related Specs

- `epics/lesson/LT-XXXX-student-assignment/` — student session management on Lesson Detail (student list structure)
- `epics/lesson/LT-XXXX-edit-lesson/test-cases/edit-lesson-bo.md` — BO Lesson Detail test cases (context for existing BO detail page structure)
- `epics/lesson/LT-96152-collect-attendance-entry-points-bo/spec.md` — another BO Lesson Detail entry-point feature (pattern reference)

## Related Test Cases

- `epics/lesson/LT-XXXX-student-assignment/test-cases/student-assignment-lesson-detail.md` — existing Student List tests on Lesson Detail (may need link-behavior cases added)
- `epics/lesson/LT-XXXX-edit-lesson/test-cases/edit-lesson-bo.md` — BO Lesson Detail tests (general structure reference)

## QASE Coverage Gaps

- AC 01.1 — Student name rendered as hyperlink on BO Lesson Detail Student List
- AC 01.2 — Student detail page view/edit follows SF permissions (view-only user, edit user, no-access user)
- AC 01.3 — Link accessible to all BO roles (HQ Staff, Centre Manager, Teacher CPU, Teacher SPU)
- SC 01 — Click student name → BO Student Detail opens for correct student
- SC 02 — Student detail content reflects user's permission level
