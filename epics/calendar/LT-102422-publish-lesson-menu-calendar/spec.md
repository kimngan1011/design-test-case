---
ticket_id: LT-102422
ticket_url: https://manabie.atlassian.net/browse/LT-102422
title: Publish lesson menu in Lesson Calendar
module: scheduling
bucket: calendar
status: Ready for Internal UAT
internal_uat_date: null
production_release_date: null
last_updated: 2026-07-03
---

# LT-102422: Publish lesson menu in Lesson Calendar

## Summary

This epic adds a direct Publish Lesson action in the Lesson Calendar right-side menu for draft lessons so users can publish without opening lesson detail.
The current behavior gap is that draft lessons have no status-change action on calendar context menu, which increases steps for operational publishing.
Scope is explicitly SF-only based on linked requirement details.

---

## Acceptance Criteria

### US 01 - Add publish action for draft lessons in Lesson Calendar

- AC 01.1: In Lesson Calendar, draft lessons expose a new context-menu action `Publish Lesson` on the right-side lesson menu.
- AC 01.2: Published lessons do not show `Publish Lesson` (since status transition is not applicable).
- AC 01.3: Completed lessons do not show `Publish Lesson`.
- AC 01.4: Cancelled lessons do not show `Publish Lesson`.
- AC 01.5: User can publish a draft lesson directly from calendar menu without navigating to lesson detail page.
- AC 01.6: Scope is SF only.

Source note: LT-102422 epic has no filled requirement text; ACs above are normalized from linked PBT-2340 description and linked implementation work item LT-102426.

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---|---|---|---|---|---|
| 1 | AC 01.1 | Draft lesson shows `Publish Lesson` in calendar right-side menu | Lesson context menu | visible | SF |
| 2 | AC 01.2 | Published lesson hides `Publish Lesson` in context menu | Lesson context menu | hidden | SF |
| 3 | AC 01.3 | Completed lesson hides `Publish Lesson` in context menu | Lesson context menu | hidden | SF |
| 4 | AC 01.4 | Cancelled lesson hides `Publish Lesson` in context menu | Lesson context menu | hidden | SF |
| 5 | AC 01.5 | Publishing can be triggered from calendar menu directly | Publish trigger entry point | enabled | SF |
| 6 | AC 01.6 | BO/mobile are not in scope for this entry point | Surface scope | restricted | SF |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---|---|---|---|---|
| 1 | [EXTENDED] | epics/calendar/LT-98532-bulk-publish-lessons-by-student/spec.md | AC 01.5 | Adds per-lesson publish entry point on calendar menu; does not replace existing bulk publish flows. |
| 2 | [REGRESSION RISK] | epics/lesson/LT-XXXX-lesson-status/ | AC 01.5 | Existing lesson-status transitions validated from lesson detail path may miss calendar-origin publish path and status sync timing. |

### Missing in Requirements

| # | Tag | Source | Description |
|---|---|---|---|
| 1 | [MISSING BEHAVIOR] | PBT-2340 description | Post-click behavior is not explicitly defined: confirm action, success toast, and resulting status refresh behavior are unspecified. |
| 2 | [MISSING BEHAVIOR] | PBT-2340 description | Failure path is undefined (permission denied, server failure, stale status change by another user). |
| 3 | [ROLE GAP] | LT-102422 / LT-102426 side-panel fields | Roles allowed to execute `Publish Lesson` are not explicitly listed in requirement text. |
| 4 | [UNDOCUMENTED IN AC] | PBT-2340 attachments (status screenshots) | Images imply status-specific menu differences, but exact menu text/state beyond `Publish Lesson` is not formally documented. |

### Lesson-Learned Risks

| # | Incident | Date | AC | Risk | Guardrail |
|---|---|---|---|---|---|
| 1 | Calendar status/action regressions are commonly role/state dependent in scheduling flows | N/A | AC 01.1-01.5 | Menu visibility can pass for one status but regress for others after status update. | Add matrix coverage for status x role x surface refresh behavior. |

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-01 | Lesson lifecycle from scheduling to reporting | Publish entry point changes from detail-only to calendar + detail | UPDATE |
| E2E-02 | Calendar lesson operations | New status action path from context menu | UPDATE |

### Assumptions Made

- The requirement baseline is taken from linked PBT-2340 because LT-102422 and LT-102426 descriptions are empty in current Jira fields.
- `Publish Lesson` performs the same status transition semantics as existing publish action in lesson detail (entry point extension only).
- Calendar row/menu state updates may require explicit refresh unless implementation performs optimistic update; this is currently undefined.

---

## Clarification Questions

1. **[ROLE GAP]** Which exact roles can see and execute `Publish Lesson` in calendar menu (HQ, CM, Teacher, others)?
   _Evidence: LT-102422/LT-102426 has no role matrix in requirement fields._

2. **[MISSING BEHAVIOR]** After clicking `Publish Lesson`, what are expected UI outcomes: confirmation modal, toast text, and whether calendar state auto-refreshes?
   _Evidence: PBT-2340 only states action addition, not post-action UX contract._

3. **[MISSING BEHAVIOR]** What is expected behavior when publish fails (network/server/permission/stale lesson status)?
   _Evidence: no error-path rules in requirement text._

4. **[UNDOCUMENTED IN AC]** Are there any additional status-based menu text/state requirements besides visibility of `Publish Lesson`?
   _Evidence: screenshot-driven states are present, but no formal textual rules._

> Posted status: not posted

---

## Related Specs

- epics/calendar/LT-98532-bulk-publish-lessons-by-student/spec.md - related calendar publish domain behavior and status transition context.
- epics/calendar/LT-89471-calendar-bug-fix/spec.md - recent calendar UI behavior changes on scheduling surface.

## Related Test Cases

- epics/lesson/LT-XXXX-lesson-status/ - existing status-transition suites likely impacted by additional calendar entry point.
- epics/calendar/LT-98532-bulk-publish-lessons-by-student/test-cases/ - publish behavior and post-action calendar verification patterns.

## QASE Coverage Gaps

- AC 01.1-01.4: status-based menu visibility matrix for Draft/Published/Completed/Cancelled.
- AC 01.5: direct publish action from calendar including post-action state/result message.
- AC 01.6: negative coverage to confirm non-SF surfaces do not expose this menu action.
