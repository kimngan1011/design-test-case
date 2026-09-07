# Test Coverage: LT-101769 — Improve Lesson popup UI

**Jira:** https://manabie.atlassian.net/browse/LT-101769
**Date:** 2026-08-05

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|---|---|
| 1 | AC 01.1 | SF New Lesson popup, its actions, and its feedback states match Figma. |
| 2 | AC 02.1 | SF Edit entry, modal, error, and success feedback match Figma. |
| 3 | AC 03.1 | BO Edit is reachable from Calendar and Lesson Detail and presents the designed dialog hierarchy. |
| 4 | AC 04.1 | New Lesson recurring UI reflects off/on, default Weekly, recurrence-type, end-option, and Course Schedule display states. |
| 5 | AC 05.1 | Edit recurring UI presents Figma labels and the confirmed One Time / Weekly Recurring choices. |
| 6 | AC 06.1 | All five in-scope UI screens show Japanese user-facing copy when the locale is Japanese. |

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---:|---|
| AC 01.1 | 1 | Display completeness, Conditional logic |
| AC 02.1 | 2 | Display completeness, Conditional logic |
| AC 03.1 | 3 | Display completeness, Cross-system impact |
| AC 04.1 | 4 | Display completeness, Conditional logic |
| AC 05.1 | 5 | Display completeness, Conditional logic |
| AC 06.1 | 6 | Display completeness |

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Display completeness | Component, Negative (field absent) |
| Conditional logic | Decision Table, Negative |
| Cross-system impact | Regression |

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC 01.1 | Assert New Lesson modal hierarchy and action layout. | Display completeness | Component | Medium | Standard |
| AC 01.1 | Assert the designed error and success feedback presentations. | Conditional | Decision Table, Negative | High | Standard |
| AC 02.1 | Assert SF edit affordance and Edit Lesson modal hierarchy. | Display completeness | Component | Medium | Standard |
| AC 02.1 | Assert SF edit error feedback and success toast copy. | Conditional | Decision Table, Negative | High | Standard |
| AC 03.1 | Assert Calendar and Lesson Detail edit entry points. | Cross-system impact | Regression | Medium | Standard |
| AC 03.1 | Assert BO dialog sections, editable/disabled appearance, saving option, and feedback presentation. | Display completeness, Conditional | Component, Decision Table | High | Standard |
| AC 04.1 | Assert recurring-off and recurring-on presentations; Weekly is visually selected by default. | Conditional | Decision Table | High | Standard |
| AC 04.1 | Assert type- and end-option-dependent controls, including no Skip Closed Date control for Course Schedule. | Conditional | Decision Table, Negative | High | Deep |
| AC 05.1 | Assert recurring edit labels and One Time / Weekly Recurring selections. | Display completeness, Conditional | Component, Decision Table | Medium | Standard |
| AC 06.1 | Assert Japanese user-facing copy on each in-scope screen. | Display completeness | Component | Medium | Standard |
| AC 01.1 | Assert that the Lesson and Calendar flows each open the SF Create form. | Display completeness | Regression | Medium | Standard |
| AC 02.1 | Assert that the Lesson and Calendar flows each open the SF Edit form. | Display completeness | Regression | Medium | Standard |
| AC 01.1 | Assert that the Duplicate flow opens the SF Create form with its designed UI. | Display completeness | Regression | Medium | Standard |

## 5. High-Risk Areas Requiring Deeper Testing

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| SF edit and BO edit feedback | An error or success state that is absent, obscured, or misleading leaves staff without reliable UI confirmation. | Cover designed error and success presentations separately; assert visible copy where Figma provides it. |
| Recurring-state controls | Incorrect visible/hidden controls can cause users to configure the wrong mode even when backend logic is unchanged. | Decision-table coverage for off/on, recurrence type, end option, and Course Schedule. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Modal/dialog hierarchy | Missing or misgrouped fields makes the long form difficult to scan. | Component assertions for all specified sections, actions, and visual states. |
| SF/BO edit entry points | A UI-only release can leave one surface without an accessible edit path. | Open the designed edit UI from Calendar and Lesson Detail. |

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Lesson create/update and recurrence generation | PX/218, 32 functional cases | Full | No — logic explicitly excluded. |
| SF Create popup UI states | PX/218 functional create cases | Partial | ✅ Modal hierarchy, actions, error, and success UI. |
| SF Edit popup UI states | PX/218 functional create cases | None | ✅ Edit affordance, modal, error, and success UI. |
| BO Edit UI and entry points | PX/218 functional create cases | None | ✅ Calendar/Detail entry points, dialog sections, options, and feedback UI. |
| Recurring New and Edit presentation | PX/218 recurrence cases | Partial | ✅ Visibility, labels, default/selection appearance, and course-schedule control absence only. |
| Japanese localization of UI copy | PX/218 functional cases | None | ✅ One localization scenario for each in-scope screen. |
| SF Create and Edit entry points | Existing SF popup cases | Partial | ✅ Separate Lesson-flow and Calendar-flow entry scenarios. |
| SF Create duplicate entry point | Existing SF popup cases | None | ✅ Duplicate-flow create-form scenario. |

## 7. Display & Ordering Inventory

| Screen / Component | Required Fields / Controls | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| SF New Lesson | modal header, content, footer actions | error / success feedback | N/A — form UI | `You have created lesson item successfully!` |
| SF Edit Lesson | edit action, Edit Lesson header, content, footer actions | error / success toast | N/A — form UI | `You have edited lesson successfully.` |
| BO Edit Lesson | Basic information, Schedule, Location Course, Recurring Settings, saving option | error / success feedback; disabled/read-only appearance | N/A — form UI | `One Time`, `Weekly Recurring` |
| Recurring New | recurring toggle, frequency type, end option controls | off/on; Daily/Weekly/Custom/Course Schedule | N/A — form UI | `Weekly` |
| Recurring Edit | recurring setting labels and choices | One Time / Weekly Recurring selection | N/A — form UI | `One Time`, `Weekly Recurring` |

## 8. Suggested Test Suite Structure

```
epics/lesson/LT-101769-lesson-popup-ui/test-cases/
├── sf-create-lesson-ui.md       → AC 01.1 — SF Create popup UI
├── sf-edit-lesson-ui.md         → AC 02.1 — SF Edit popup UI
├── bo-edit-lesson-ui.md         → AC 03.1 — BO Edit entry points and dialog UI
├── recurring-new-lesson-ui.md   → AC 04.1 — Recurring Settings for New Lesson UI
└── recurring-edit-lesson-ui.md  → AC 05.1 — Recurring Settings for Edit Lesson UI
```
