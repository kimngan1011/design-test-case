# Test Coverage: LT-104011 - Add Next and Prev lesson button in BO

**Jira:** https://manabie.atlassian.net/browse/LT-104011
**Date:** 2026-07-14
**Module:** scheduling / OOP/aver
**Platform:** BO

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
| --- | --- | --- |
| 1 | AC 01.1 | BO Lesson Detail shows a Previous Lesson button for the Aver flow |
| 2 | AC 01.1 | BO Lesson Detail shows a Next Lesson button for the Aver flow |
| 3 | AC 01.2 | Clicking Previous Lesson redirects the user to the previous lesson detail in the same recurring lesson schedule |
| 4 | AC 01.2 | Clicking Next Lesson redirects the user to the next lesson detail in the same recurring lesson schedule |
| 5 | AC 01.3 | When the current lesson is in the middle of the recurring chain, Previous Lesson and Next Lesson are both enabled |
| 6 | AC 01.4 | When the current lesson is the first lesson in the chain, Previous Lesson is disabled |
| 7 | AC 01.4 | When the current lesson is the last lesson in the chain, Next Lesson is disabled |
| 8 | AC 01.2 | Navigation keeps the user on the same browser tab and reuses the BO detail surface rather than opening a new tab |
| 9 | AC 01.5 | Aver label mapping uses `前の特訓` / `次の特訓` |
| 10 | AC 01.5 | Core label mapping uses `前の授業` / `次の授業` if the feature is not Aver-only |

---

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
| --- | --- | --- |
| AC 01.1 | 1, 2 | Display completeness, Conditional logic |
| AC 01.2 | 3, 4, 8 | State transition, Cross-system impact, Data integrity |
| AC 01.3 | 5 | Conditional logic, Recurrence logic |
| AC 01.4 | 6, 7 | Boundary/range logic, Conditional logic |
| AC 01.5 | 9, 10 | Display completeness, Permission logic |

---

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
| --- | --- |
| Display completeness | Component, Negative |
| Conditional logic | Decision Table, Negative |
| State transition | State Transition, Regression |
| Cross-system impact | Regression, CRUD |
| Data integrity | CRUD, Regression |
| Recurrence logic | State Transition, Regression |
| Boundary/range logic | Boundary Value Analysis, Negative |
| Permission logic | Permission Matrix, Decision Table |

---

## 4. Edge-Case Checklist Application (A-H.1)

| Checklist Area | Applicability | Notes |
| --- | --- | --- |
| A. Configuration-driven thresholds | N/A | No partner-config threshold or numeric limit is defined for the navigation buttons |
| B. Date/time logic | N/A | No current-time gate or date comparison is defined in the ticket; lesson adjacency is based on recurring-chain order, not today's date |
| C. Concurrent/stale state | Yes | Navigation can stale-load when the source lesson context changes or the user rapidly clicks Previous/Next multiple times |
| D. Permission and role | Yes | Ticket scope is Aver-specific but does not define which BO roles can see or use the buttons |
| E. State transition | Yes | The page state transitions from one lesson detail record to an adjacent lesson detail record and boundary states must be enforced |
| F. Cross-system/cross-surface | Yes | BO Lesson Detail navigation must not break existing BO Report tab and lesson-context-dependent actions after landing on the adjacent lesson |
| G. Downstream effects inventory | Yes | Navigation changes the active lesson context; all lesson-detail dependent surfaces must point to the destination lesson after navigation |
| H. Display completeness and ordering | Yes | The action area must show both buttons with exact tenant labels and correct enabled or disabled state |
| H.1 Spec-Figma mismatch | N/A | No direct Figma URL is stored in the spec; only a reference node from LT-84885 is cited, so mismatch review remains an open clarification rather than a coverage blocker |

### Downstream Effects Inventory Table

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner |
| --- | --- | --- | --- |
| Click Previous Lesson | BO route and header switch to the immediately previous lesson in the recurring chain | BO Lesson Detail shell | TC-LT104011-03 |
| Click Next Lesson | BO route and header switch to the immediately next lesson in the recurring chain | BO Lesson Detail shell | TC-LT104011-04 |
| Click Previous Lesson or Next Lesson | Current lesson metadata, student list, and lesson-specific content reload for the destination lesson rather than persisting source-lesson data | BO Lesson Detail content | TC-LT104011-05 |
| Click Previous Lesson or Next Lesson | Existing nested BO actions such as Report-tab entry points remain bound to the destination lesson after navigation | BO Lesson Detail related actions | TC-LT104011-06 |
| Repeated click on Previous Lesson or Next Lesson | Navigation remains idempotent and does not open duplicate tabs or stale mixed content | BO route handling | TC-LT104011-07 |

### Display and Ordering Inventory Table

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
| --- | --- | --- | --- | --- |
| BO Lesson Detail action area | Previous Lesson button, Next Lesson button | Previous Lesson disabled on first lesson; Next Lesson disabled on last lesson; both enabled on middle lesson | N/A | `前の特訓`, `次の特訓`, `前の授業`, `次の授業` |

---

## 5. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
| --- | --- | --- | --- | --- | --- |
| AC 01.1 | Aver BO Lesson Detail shows Previous Lesson and Next Lesson buttons in the action area | Display completeness, Conditional logic | Component, Decision Table | High | Standard |
| AC 01.2 | Clicking Previous Lesson opens the immediately previous lesson detail in the same tab | State transition, Data integrity | State Transition, Regression | High | Deep |
| AC 01.2 | Clicking Next Lesson opens the immediately next lesson detail in the same tab | State transition, Data integrity | State Transition, Regression | High | Deep |
| AC 01.2 | Destination lesson content fully reloads and replaces the source lesson context after navigation | Cross-system impact, Data integrity | CRUD, Regression | High | Deep |
| AC 01.3 | Middle lesson in the recurring chain enables both navigation buttons | Conditional logic, Recurrence logic | Decision Table, State Transition | High | Standard |
| AC 01.4 | First lesson disables Previous Lesson while keeping Next Lesson available | Boundary/range logic, Conditional logic | Boundary Value Analysis, Negative | High | Standard |
| AC 01.4 | Last lesson disables Next Lesson while keeping Previous Lesson available | Boundary/range logic, Conditional logic | Boundary Value Analysis, Negative | High | Standard |
| AC 01.5 | Aver tenant shows `前の特訓` and `次の特訓` labels exactly | Display completeness, Permission logic | Component, Permission Matrix | Medium | Standard |
| AC 01.5 | Core rollout, if enabled, shows `前の授業` and `次の授業` labels exactly | Display completeness, Permission logic | Component, Decision Table | Medium | Standard |
| AC 01.2 edge | Rapid repeated clicks do not create duplicate tabs, mixed lesson content, or broken back-stack behavior | State transition, Data integrity | Negative, Regression | High | Standard |
| AC 01.2 edge | Report-tab and lesson-detail dependent actions remain bound to the destination lesson after navigation | Cross-system impact, Regression | Regression, CRUD | High | Deep |
| AC 01.1 edge | Unauthorized or non-target BO role does not see or cannot use the buttons until role scope is clarified | Permission logic, Conditional logic | Permission Matrix, Negative | Medium | Standard |

---

## 6. High-Risk Areas Requiring Deeper Testing

### Red Critical Risk

| Area | Reason | Recommended Approach |
| --- | --- | --- |
| None identified | The feature does not write lesson data, create records, or trigger irreversible state changes | N/A |

### Orange High Risk

| Area | Reason | Recommended Approach |
| --- | --- | --- |
| Adjacent lesson navigation target identity | Landing on the wrong recurring instance can make users operate on the wrong lesson record | Deep navigation assertions using explicit lesson IDs, dates, and chain order on source and destination |
| Source-to-destination context replacement | BO Lesson Detail already hosts lesson-specific data and actions; stale content after navigation would be user-visible and dangerous | Reload assertions for header, student content, and action surfaces after each navigation |
| Boundary button behavior on first and last lessons | Disabled-state regressions are common when chain position is computed dynamically | Boundary matrix using first, middle, and last recurring lessons in the same chain |
| Report-tab and related-action regression after navigation | Existing BO actions may stay bound to the original lesson if context is cached incorrectly | Regression scenario that navigates, then opens a lesson-dependent secondary surface from the destination lesson |
| Rapid repeat navigation | Multi-click or back-stack instability can leave the route and screen content mismatched | Negative scenario with repeated click, browser back, and second navigation on the same chain |

### Yellow Medium Risk

| Area | Reason | Recommended Approach |
| --- | --- | --- |
| Tenant-specific label mapping | Wrong label text is user-facing but does not corrupt lesson data | Exact-text assertion on Aver labels and conditional Core labels if rollout is enabled |
| Role scope ambiguity | Ticket does not specify whether all BO lesson viewers or only teachers can use the feature | Permission-matrix coverage held as conditional until product clarifies target roles |

---

## 7. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
| --- | --- | --- | --- |
| Button visibility on BO Lesson Detail | epics/lesson/LT-99482-lesson-calendar-button-trial-lesson/test-cases/01-button-visibility-navigation.md | Partial - validates action button visibility pattern on another detail surface, not BO recurring lesson navigation | Yes - add BO lesson-detail button visibility and enabled-state cases |
| Previous navigation to adjacent recurring lesson | epics/lesson/LT-XXXX-edit-lesson/test-cases/edit-lesson-bo.md | Partial - existing recurring cases open explicit lessons in a chain but do not navigate between adjacent lesson details | Yes - add previous-lesson same-tab navigation case |
| Next navigation to adjacent recurring lesson | epics/lesson/LT-XXXX-edit-lesson/test-cases/edit-lesson-bo.md | Partial - recurring chain context exists, but adjacent next-lesson navigation is not asserted | Yes - add next-lesson same-tab navigation case |
| Destination lesson context replaces source lesson content | epics/lesson/LT-96152-collect-attendance-entry-points-bo/test-cases/LT-96152-collect-attendance-entry-points.md | Partial - validates lesson-detail dependent actions, not context switch after intra-detail navigation | Yes - add destination-content reload case |
| First and last lesson boundary disablement | reports/qase-snapshots/PX-2026-04-13.json | Partial - analogous Previous Report / Next Report behavior exists, but not on Lesson Detail | Yes - add first/middle/last boundary matrix cases |
| Tenant-specific exact label mapping | No direct existing suite-251 coverage identified | None | Yes - add exact-text assertions for Aver and conditional Core labels |
| Role-based exposure and blocked access | No direct existing suite-251 coverage identified | None | Yes - add role-scope matrix once product clarifies eligible roles |
| Repeated click and back-stack stability | No direct existing suite-251 coverage identified | None | Yes - add repeated-navigation regression case |

---

## 8. Suggested Test Suite Structure

```text
epics/OOP/aver/LT-104011-next-prev-lesson-button-bo/test-cases/
|- 01-button-visibility-boundary-states.md -> AC 01.1, AC 01.3, AC 01.4 action-area visibility and first/middle/last enablement matrix
|- 02-prev-next-navigation.md -> AC 01.2 same-tab Previous/Next navigation and destination lesson identity
|- 03-context-labels-and-regression.md -> AC 01.2, AC 01.5 destination content reload, tenant labels, repeated-click, and related-action regression
```