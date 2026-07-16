# Test Coverage: LT-102422 - Publish lesson menu in Lesson Calendar

**Jira:** https://manabie.atlassian.net/browse/LT-102422
**Date:** 2026-07-03
**Module:** scheduling / calendar
**Platform:** SF only

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
| --- | --- | --- |
| 1 | AC 01.1 | Draft lesson shows Publish Lesson in calendar right-side menu |
| 2 | AC 01.2 | Published lesson hides Publish Lesson in calendar right-side menu |
| 3 | AC 01.3 | Completed lesson hides Publish Lesson in calendar right-side menu |
| 4 | AC 01.4 | Cancelled lesson hides Publish Lesson in calendar right-side menu |
| 5 | AC 01.5 | User can publish a draft lesson directly from calendar menu without opening lesson detail |
| 6 | AC 01.6 | Publish Lesson from calendar menu is SF-only scope |

---

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
| --- | --- | --- |
| AC 01.1 | 1 | Conditional logic, Display completeness |
| AC 01.2 | 2 | Conditional logic, State transition |
| AC 01.3 | 3 | Conditional logic, State transition |
| AC 01.4 | 4 | Conditional logic, State transition |
| AC 01.5 | 5 | State transition, Cross-system impact |
| AC 01.6 | 6 | Permission logic, Cross-system impact |

---

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
| --- | --- |
| Conditional logic | Decision Table, Negative |
| Display completeness | Component |
| State transition | State Transition, CRUD |
| Cross-system impact | Regression, CRUD |
| Permission logic | Permission Matrix, Decision Table |

---

## 4. Edge-Case Checklist Application (A-H.1)

| Checklist Area | Applicability | Notes |
| --- | --- | --- |
| A. Configuration-driven thresholds | N/A | No config threshold in ACs |
| B. Date/time logic | N/A | No date/time gate in ACs |
| C. Concurrent/stale state | Yes | Menu stale state after another actor publishes same draft must be handled |
| D. Permission and role | Yes | SF-only scope requires explicit non-SF coverage |
| E. State transition | Yes | Draft to Published from calendar menu and invalid transitions |
| F. Cross-system/cross-surface | Yes | Calendar entry point change must not leak to BO/mobile entry points |
| G. Downstream effects inventory | Yes | Publish action changes lesson status; status must refresh in calendar surface |
| H. Display completeness and ordering | Yes | Menu item presence/absence matrix by status |
| H.1 Spec-Figma mismatch | N/A | No Figma URL in spec |

### Downstream Effects Inventory Table

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner |
| --- | --- | --- | --- |
| Publish from calendar menu | Lesson status changes from Draft to Published | SF lesson record + calendar card | TC-LT102422-06 |
| Publish from calendar menu | Publish menu item no longer available after refresh | SF calendar right-side menu | TC-LT102422-07 |
| Publish from calendar menu | No required navigation to lesson detail | SF calendar workflow | TC-LT102422-06 |

### Display and Ordering Inventory Table

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
| --- | --- | --- | --- | --- |
| Lesson calendar right-side lesson menu | Publish Lesson item for draft lesson | Publish Lesson hidden for Published/Completed/Cancelled | N/A | Publish Lesson |

---

## 5. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
| --- | --- | --- | --- | --- | --- |
| AC 01.1 | Draft lesson menu shows Publish Lesson | Conditional, Display completeness | Decision Table, Component | High | Standard |
| AC 01.2 | Published lesson menu hides Publish Lesson | Conditional, State transition | Decision Table, Negative | High | Standard |
| AC 01.3 | Completed lesson menu hides Publish Lesson | Conditional, State transition | Decision Table, Negative | Medium | Standard |
| AC 01.4 | Cancelled lesson menu hides Publish Lesson | Conditional, State transition | Decision Table, Negative | Medium | Standard |
| AC 01.5 | Publish can be triggered directly from calendar menu | State transition, Cross-system | State Transition, Regression | Critical | Deep |
| AC 01.6 | Entry point remains SF-only, no BO/mobile exposure | Permission, Cross-system | Permission Matrix, Regression | High | Standard |
| AC 01.5 (edge) | Concurrent stale menu click handled when lesson already published | Conditional, State transition | Negative, Decision Table | High | Standard |

---

## 6. High-Risk Areas Requiring Deeper Testing

### Red Critical Risk

| Area | Reason | Recommended Approach |
| --- | --- | --- |
| Direct publish from calendar changes lesson status | Wrong status transition can publish wrong lesson or leave stale menu state | State transition path with immediate status assertion and refresh assertion |

### Orange High Risk

| Area | Reason | Recommended Approach |
| --- | --- | --- |
| Status-specific menu visibility matrix | Menu regressions are often status-dependent and easy to miss | Decision table for Draft/Published/Completed/Cancelled |
| SF-only scope | New action could appear on unintended surfaces | Regression checks on BO and mobile surfaces |
| Stale state under concurrent action | A second click on stale draft menu can produce inconsistent feedback | Negative case where another actor publishes first |

### Yellow Medium Risk

| Area | Reason | Recommended Approach |
| --- | --- | --- |
| Completed and Cancelled visibility | Lower frequency statuses but still user-facing menu risk | Include matrix assertions for both statuses |

---

## 7. Coverage Gaps vs Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
| --- | --- | --- | --- |
| Draft status shows Publish Lesson in calendar menu | epics/lesson/LT-XXXX-lesson-status/ (detail-page oriented) | Partial | Yes - add calendar menu visibility case |
| Published/Completed/Cancelled hide Publish Lesson in menu | epics/lesson/LT-XXXX-lesson-status/ (status transitions, not calendar menu) | Partial | Yes - add status matrix hide cases |
| Image-based status menu expectations in PBT-2340 attachments | Existing cases validate only Publish Lesson visibility | Partial | Yes - add screenshot parity suite to compare full menu/status presentation per status |
| Direct publish from calendar without navigating detail | epics/calendar/LT-98532-bulk-publish-lessons-by-student/test-cases/ (bulk path) | None | Yes - add single-lesson direct publish flow |
| SF-only scope for entry point | No explicit existing case in this epic | None | Yes - add non-SF surface exclusion case |
| Stale concurrent publish click behavior | No explicit existing case | None | Yes - add stale-state negative case |

---

## 8. Suggested Test Suite Structure

```
epics/calendar/LT-102422-publish-lesson-menu-calendar/test-cases/
|- 01-publish-menu-visibility.md -> AC 01.1 to AC 01.4 status-based menu visibility matrix
|- 02-publish-action-execution.md -> AC 01.5 to AC 01.6 publish action flow and SF-only scope
|- 03-status-screenshot-parity.md -> screenshot parity checks for Draft/Published/Completed/Cancelled menus based on PBT-2340 attachments
```
