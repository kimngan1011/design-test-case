---
ticket_id: LT-101769
ticket_url: https://manabie.atlassian.net/browse/LT-101769
title: "[Core] Improve Lesson popup UI"
module: lesson-management
bucket: lesson
status: Ready for QA
internal_uat_date: null
production_release_date: null
last_updated: 2026-08-05
---

# LT-101769: Improve Lesson popup UI

## Summary

Improve the scanability and consistency of the Lesson UI using Figma as the source of truth. This scope adds UI/UX regression coverage only; it does not change or retest lesson creation, update, recurrence generation, or persistence logic already covered in Qase suite PX/218.

## Acceptance Criteria

### AC 01.1 — SF Create Lesson UI

The SF New Lesson popup follows the Figma layout, including its default, validation-error, and success-feedback states. Visual controls, sectioning, modal actions, and feedback must match the design without asserting lesson-creation logic.

### AC 02.1 — SF Edit Lesson UI

The SF lesson edit affordance and Edit Lesson popup follow Figma from open through error and success feedback. The success feedback text is `You have edited lesson successfully.`

### AC 03.1 — BO Edit Lesson UI

BO supports the Edit Lesson entry point from both Calendar and Lesson Detail. The Edit Lesson dialog presents Basic information, Schedule, Location Course, and Recurring Settings in the designed hierarchy, including its error and success states.

### AC 04.1 — Recurring Settings for New Lesson

The New Lesson recurring UI follows Figma for recurring off/on states, the default Weekly presentation, Daily/Weekly/Custom/Course Schedule selection states, end-option controls, and the absence of a Skip Closed Date control for Course Schedule. This is display coverage only.

### AC 05.1 — Recurring Settings for Edit Lesson

The Edit Lesson recurring UI follows Figma. `One Time` and `Weekly Recurring` are the correct BO recurring-setting choices. This verifies only labels, visibility, selection appearance, and layout.

### AC 06.1 — Japanese localization across Lesson UI

When the interface locale is Japanese, each in-scope screen—SF Create, SF Edit, BO Edit, Recurring New, and Recurring Edit—shows Japanese user-facing labels, actions, feedback, and helper text. Approved product names and technical proper nouns are excluded.

## Business Rules (Extracted)

| # | AC | Business Rule | Field / Component | Field Behavior | Platform |
|---|---|---|---|---|---|
| 1 | AC 01.1 | New Lesson opens in the Figma-defined modal hierarchy with standard controls and actions. | New Lesson popup | display completeness | SF |
| 2 | AC 01.1 | Validation-error and success-feedback presentations follow the Figma states. | New Lesson feedback | conditional display | SF |
| 3 | AC 02.1 | The edit affordance opens the Figma-defined Edit Lesson popup. | Edit action and modal | conditional display | SF |
| 4 | AC 02.1 | SF edit error and success feedback use the designed presentation and copy. | Toast / feedback | conditional display | SF |
| 5 | AC 03.1 | Calendar and Lesson Detail expose the designed BO Edit Lesson entry point. | Edit action | display completeness | BO |
| 6 | AC 03.1 | BO Edit Lesson groups Basic information, Schedule, Location Course, and Recurring Settings in the designed dialog. | Edit Lesson dialog | display completeness | BO |
| 7 | AC 04.1 | New Lesson shows the recurring settings appropriate to the selected UI state; Weekly is the default when recurring is enabled. | Recurring Settings | conditional display / default | SF |
| 8 | AC 04.1 | Course Schedule does not expose a Skip Closed Date UI control. | Course Schedule | conditional display | SF |
| 9 | AC 05.1 | BO recurring settings label and present One Time and Weekly Recurring as designed. | Recurring Settings | display completeness | BO |
| 10 | AC 06.1 | Each in-scope Lesson UI screen renders user-facing text in Japanese when the locale is Japanese. | Localized UI copy | display completeness | SF, BO |
| 11 | AC 01.1 | SF opens the New Lesson popup from both the Lesson and Calendar flows. | Create entry point | display completeness | SF |
| 12 | AC 02.1 | SF opens the Edit Lesson popup from both the Lesson and Calendar flows. | Edit entry point | display completeness | SF |
| 13 | AC 01.1 | SF opens the New Lesson popup from the Duplicate flow with the designed create UI. | Duplicate entry point | display completeness | SF |

## Conflict & Gap Analysis

### Resolved Figma alignment

| # | Tag | Source | AC | Resolution |
|---|---|---|---|---|
| 1 | [UNDOCUMENTED IN AC] | Figma `12152:124895` | AC 03.1 | BO Edit entry points, dialog grouping, and feedback states are included in UI coverage. |
| 2 | [UNDOCUMENTED IN AC] | Figma `12463:54991` | AC 05.1 | User confirmed that One Time and Weekly Recurring are the correct BO choices. |
| 3 | [REPLACED] | User instruction | All | Functional creation, update, recurrence, and persistence assertions are excluded; existing Qase cases remain the logic coverage. |

## Related Test Cases

- Qase PX suite 218 — 32 existing cases covering create/recurrence functional behavior; do not duplicate.
