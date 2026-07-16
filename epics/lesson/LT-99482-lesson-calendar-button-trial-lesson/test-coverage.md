# Test Coverage: LT-99482 - Add Lesson Calendar button to Trial Lesson page

**Jira:** https://manabie.atlassian.net/browse/LT-99482
**Date:** 2026-07-03

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|---|---|
| 1 | AC 01.1 | Trial Lesson detail shows Lesson Calendar button |
| 2 | AC 01.2 | Clicking Lesson Calendar opens Lesson Calendar |
| 3 | AC 01.3 | Trial Lesson student is pre-selected in calendar context |
| 4 | AC 01.4 | Assignment flow can continue without re-selecting student |
| 5 | AC 01.5 | Scope is SF for this entry point |

---

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC 01.1 | 1 | Display completeness, Conditional logic |
| AC 01.2 | 2 | State transition, Cross-system impact |
| AC 01.3 | 3 | Conditional logic, Data integrity |
| AC 01.4 | 4 | State transition, Cross-system impact |
| AC 01.5 | 5 | Permission logic, Cross-system impact |

---

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Display completeness | Component, Negative |
| Conditional logic | Decision Table, Negative |
| State transition | State Transition, Regression |
| Data integrity | CRUD, Regression |
| Permission logic | Permission Matrix, Decision Table |
| Cross-system impact | Regression, CRUD |

---

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC 01.1 | Lesson Calendar button visible on Trial Lesson detail | Display completeness, Conditional | Component, Decision Table | High | Standard |
| AC 01.2 | Clicking button opens Lesson Calendar | State transition, Cross-system | State Transition, Regression | High | Standard |
| AC 01.3 | Trial Lesson student pre-selected on calendar | Conditional, Data integrity | Decision Table, CRUD | Critical | Deep |
| AC 01.4 | User continues assignment flow without manual re-selection | State transition, Cross-system | Scenario, Regression | Critical | Deep |
| AC 01.5 | Non-SF surfaces unchanged for this entry point | Permission, Cross-system | Permission Matrix, Regression | High | Standard |
| AC 01.3 edge | Missing/inactive student at click time handled predictably | Conditional, Data integrity | Negative, Decision Table | Medium | Standard |

---

## 5. High-Risk Areas Requiring Deeper Testing

### Red Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Student context transfer Trial Lesson -> Calendar | Wrong selected student can cause assignment to wrong learner | Deep context assertions with explicit student ID and name on destination |
| Assignment continuation after navigation | Flow break causes manual rework and scheduling mistakes | End-to-end scenario from button click to slot assignment-ready state |

### Orange High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Entry point navigation behavior | New route can break destination initialization | State-transition and regression checks across SF calendar entry |
| Surface scope leakage | Entry point could unintentionally appear in BO/mobile | Permission matrix across SF/BO/mobile |

### Yellow Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Missing/inactive student edge | Requirement does not define fallback behavior | Negative case + clarified expected message behavior |

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Trial Lesson detail button visibility | None identified in this epic | None | Yes |
| Trial Lesson to Calendar navigation | epics/calendar/LT-102422-publish-lesson-menu-calendar/test-cases/02-publish-action-execution.md | Partial | Yes |
| Student pre-selection from Trial Lesson context | epics/cross-domain/LT-96188-student-classification-event-lesson-calendar/test-cases/02-lesson-calendar.md | Partial | Yes |
| Assignment continuation without re-search | None identified in this epic | None | Yes |
| Non-SF unchanged | No direct coverage identified for this entry point | None | Yes |

---

## 7. Suggested Test Suite Structure

```
epics/lesson/LT-99482-lesson-calendar-button-trial-lesson/test-cases/
|- 01-button-visibility-navigation.md -> AC 01.1, AC 01.2
|- 02-student-context-transfer.md -> AC 01.3, AC 01.4
|- 03-scope-regression.md -> AC 01.5 + edge/regression
```
