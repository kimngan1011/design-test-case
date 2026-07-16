---
ticket_id: LT-104011
ticket_url: https://manabie.atlassian.net/browse/LT-104011
title: [Aver] Core | Add Next and Prev lesson button in BO
module: scheduling
bucket: OOP/aver
status: In Development
internal_uat_date: null
production_release_date: null
last_updated: 2026-07-14
---

# LT-104011: [Aver] Core | Add Next and Prev lesson button in BO

## Summary

This epic adds `Previous Lesson` and `Next Lesson` buttons to the Back Office Lesson Detail page so Aver users can move across adjacent lessons in the same recurring chain without leaving the detail surface.
The ticket is sparse and explicitly delegates behavior to LT-84885, so this spec derives the operational acceptance criteria from the current ticket, the referenced Jira logic, and the local BO lesson-detail baselines already documented in the repo.

---

## Acceptance Criteria

Derived from LT-104011 description, linked reference ticket LT-84885, and LT-84885 reference Figma node `37045:26181`.

### US 01 - Navigate between adjacent lessons from BO Lesson Detail

- AC 01.1: On BO Lesson Detail, `Previous Lesson` and `Next Lesson` buttons are available for the Aver flow.
- AC 01.2: Clicking `Previous Lesson` or `Next Lesson` redirects the user to the adjacent lesson detail in the same recurring lesson schedule without opening a new tab.
- AC 01.3: When the current lesson is in the middle of the recurring chain, both buttons are enabled.
- AC 01.4: When the current lesson is the first lesson, `Previous Lesson` is disabled; when it is the last lesson, `Next Lesson` is disabled.
- AC 01.5: Labels follow the provided translation mapping: Aver uses `前の特訓` / `次の特訓`, while Core uses `前の授業` / `次の授業` if the feature is not Aver-only.

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---|---|---|---|---|---|
| 1 | AC 01.1 | BO Lesson Detail shows a Previous Lesson button for the Aver flow. | Previous Lesson button | visible | BO |
| 2 | AC 01.1 | BO Lesson Detail shows a Next Lesson button for the Aver flow. | Next Lesson button | visible | BO |
| 3 | AC 01.2 | Clicking Previous Lesson redirects the user to the previous lesson detail in the same recurring lesson schedule. | Previous Lesson button | enabled | BO |
| 4 | AC 01.2 | Clicking Next Lesson redirects the user to the next lesson detail in the same recurring lesson schedule. | Next Lesson button | enabled | BO |
| 5 | AC 01.3 | When the current lesson is in the middle of the recurring chain, Previous Lesson and Next Lesson are both enabled. | Lesson navigation state | computed | BO |
| 6 | AC 01.4 | When the current lesson is the first lesson in the chain, Previous Lesson is disabled. | Previous Lesson button | disabled | BO |
| 7 | AC 01.4 | When the current lesson is the last lesson in the chain, Next Lesson is disabled. | Next Lesson button | disabled | BO |
| 8 | AC 01.2 | Navigation keeps the user on the same browser tab and reuses the BO detail surface rather than opening a new tab. | Lesson detail navigation mode | restricted | BO |
| 9 | AC 01.5 | Aver label mapping uses `前の特訓` / `次の特訓`. | Lesson navigation label | computed | BO |
| 10 | AC 01.5 | Core label mapping uses `前の授業` / `次の授業` if the feature is not Aver-only. | Lesson navigation label | computed | BO |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---|---|---|---|---|
| 1 | [EXTENDED] | reports/qase-snapshots/PX-2026-04-13.json | AC 01.2 | Extends the existing Aver BO `Previous Report` / `Next Report` pattern from Report Detail to Lesson Detail. |
| 2 | [REGRESSION RISK] | epics/lesson/LT-XXXX-edit-lesson/test-cases/edit-lesson-bo.md | AC 01.2 | Recurring BO lesson-detail flows already depend on the opened lesson instance being the active target; Prev/Next navigation can stale-load the source lesson context. |
| 3 | [EXTENDED] | reports/qase-snapshots/PX-2026-04-13.json | AC 01.3 | The middle-of-chain dual-enable pattern already exists for Aver `Previous Report` / `Next Report` and is being extended to BO Lesson Detail lesson navigation. |
| 4 | [EXTENDED] | epics/lesson/LT-99482-lesson-calendar-button-trial-lesson/test-cases/01-button-visibility-navigation.md | AC 01.1 | Adds another action-button pair to a lesson detail page, extending an existing detail-page navigation pattern. |
| 5 | [REGRESSION RISK] | epics/lesson/LT-96152-collect-attendance-entry-points-bo/test-cases/LT-96152-collect-attendance-entry-points.md | AC 01.2 | BO Lesson Detail already hosts tabbed teacher workflows; navigation between lessons can break expected destination tab/view state. |

### Missing in Requirements

| # | Tag | Source | Description |
|---|---|---|---|
| 1 | [MISSING BEHAVIOR] | LT-104011 requirement | No explicit rule for one-time lessons or any lesson with no recurring-chain neighbor. |
| 2 | [UNDOCUMENTED IN AC] | LT-84885 Jira + Figma node 37045:26181 | Reference feature defines boundary behavior on Report Detail, but LT-104011 does not explicitly confirm the exact Lesson Detail equivalent. |
| 3 | [ROLE GAP] | scheduling-feature-permission-matrix.csv + access-by-user-type.md | Ticket does not define which Aver BO roles can see/use the buttons. |
| 4 | [MISSING BEHAVIOR] | knowledge/domain-knowledge/scheduling/lesson-management/lesson.md | No rule defines whether navigation includes Draft/Published/Completed/Cancelled adjacent lessons or skips some statuses. |
| 5 | [MISSING BEHAVIOR] | LT-104011 translation note | Scope is ambiguous: body says “for Aver” while translation notes also define Core labels. |

### Lesson-Learned Risks

| # | Incident | Date | AC | Risk | Guardrail |
|---|---|---|---|---|---|
| None | — | — | — | No relevant historical incident matched this BO lesson-detail navigation change. | Keep focus on chain-boundary, destination-state, and role-scope validation. |

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-01 | Lesson Lifecycle — Create, Teach, Report, View | BO teacher flow gains a lesson-detail navigation surface that can change which lesson the teacher is acting on. | UPDATE |
| E2E-02 | Recurring Lesson — Create, Edit Chain, Delete, Calendar Drag | Recurring-chain adjacency is now directly traversable from BO Lesson Detail. | UPDATE |

### Assumptions Made

- LT-104011 intentionally reuses LT-84885 behavior on a different BO surface because the ticket says “the same logic and design can be applied”.
- The feature targets Lesson Detail for a recurring lesson chain, not an arbitrary cross-lesson search flow.
- `OOP/aver` was chosen because the ticket body says “for Aver” and the repo permission matrix already models Aver as an OOP customization, even though the rollout text still needs clarification.
- No Confluence page was linked from LT-104011, and no current-ticket Figma node was provided; only the LT-84885 reference Figma was available.

---

## Clarification Questions

1. **[ROLE GAP]** Which BO roles should be able to see and click `Previous Lesson` / `Next Lesson` in the Aver flow: Teacher only, or all Lesson Detail viewers such as Centre Manager, Centre Staff, and HQ Staff as well?
   _Evidence: `knowledge/domain-knowledge/scheduling/scheduling-feature-permission-matrix.csv` + `knowledge/domain-knowledge/scheduling/calendar/access-by-user-type.md` — BO Lesson Detail is available to multiple Aver role paths, but LT-104011 does not specify button-level access._

2. **[MISSING BEHAVIOR]** What should happen on BO Lesson Detail when the lesson is one-time or otherwise has no recurring-chain neighbor at all? Should `Previous Lesson` / `Next Lesson` be hidden, shown disabled, or shown only when an adjacent lesson exists?
   _Evidence: `LT-104011 requirement` — the ticket defines recurring-chain navigation by analogy to LT-84885, but it does not define the no-chain case._

3. **[REGRESSION RISK]** After clicking `Previous Lesson` or `Next Lesson` from BO Lesson Detail, should the destination always open on the default Lesson Detail view, or should it preserve the user’s current BO sub-view/tab context if they were on a nested surface such as Report?
   _Evidence: `epics/lesson/LT-96152-collect-attendance-entry-points-bo/test-cases/LT-96152-collect-attendance-entry-points.md` — BO Lesson Detail already contains tabbed action flows whose state depends on the current lesson context._

4. **[MISSING BEHAVIOR]** When the adjacent lesson exists but has status Draft, Published, Completed, or Cancelled, should navigation still land on that lesson, or should some statuses be skipped or blocked?
   _Evidence: `knowledge/domain-knowledge/scheduling/lesson-management/lesson.md` — recurring lessons can exist across multiple statuses, but LT-104011 defines adjacency only by chain position._

5. **[UNDOCUMENTED IN AC]** Should first-lesson and last-lesson behavior on BO Lesson Detail exactly match LT-84885 report navigation, including disabled boundary buttons and any fallback feedback when no adjacent lesson/report data exists?
   _Evidence: `LT-84885 Jira + Figma node 37045:26181` — the reference feature documents boundary button states on Report Detail, but LT-104011 does not explicitly restate the Lesson Detail equivalent._

6. **[MISSING BEHAVIOR]** Is LT-104011 Aver-only, or should Core tenants also receive the feature? The ticket body says “for Aver”, but the translation section also defines Core labels (`前の授業` / `次の授業`).
   _Evidence: `LT-104011 requirement + translation note` — scope statement and label mapping imply different rollout possibilities._

> Posted status: not posted

---

## Related Specs

- `epics/lesson/LT-99482-lesson-calendar-button-trial-lesson/spec.md` — closest in-repo example of adding a navigation button to a lesson-related detail page.
- `epics/lesson/LT-96152-collect-attendance-entry-points-bo/spec.md` — BO lesson-detail entry-point extension pattern and destination-state regression surface.

## Related Test Cases

- `epics/lesson/LT-99482-lesson-calendar-button-trial-lesson/test-cases/01-button-visibility-navigation.md` — button visibility, enablement, navigation, and repeated-click stability pattern.
- `epics/lesson/LT-96152-collect-attendance-entry-points-bo/test-cases/LT-96152-collect-attendance-entry-points.md` — BO lesson-detail tab/state regression pattern.
- `epics/lesson/LT-XXXX-edit-lesson/test-cases/edit-lesson-bo.md` — recurring BO lesson-detail target identity baseline.
- `reports/qase-snapshots/PX-2026-04-13.json` — local Qase snapshot containing the analogous Aver `Previous Report` / `Next Report` behavior.

## QASE Coverage Gaps

- AC 01.1 — No suite-251 case currently asserts `Previous Lesson` / `Next Lesson` visibility on BO Lesson Detail.
- AC 01.2 — No suite-251 case currently asserts same-tab navigation from one BO lesson detail record to its adjacent recurring lesson.
- AC 01.3 — No suite-251 case currently asserts both buttons enabled on a middle lesson in the chain.
- AC 01.4 — No suite-251 case currently asserts first-lesson/last-lesson boundary disablement on BO Lesson Detail.
- AC 01.5 — No suite-251 case currently asserts tenant-specific label mapping or rollout scope for Aver vs Core.