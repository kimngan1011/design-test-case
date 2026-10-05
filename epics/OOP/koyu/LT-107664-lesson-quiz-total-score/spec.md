---
ticket_id: LT-107664
ticket_url: https://manabie.atlassian.net/browse/LT-107664
title: Koyu Lesson Quiz and Total Score
module: scheduling
bucket: OOP/koyu
status: Ready for QA
internal_uat_date: null
production_release_date: null
last_updated: 2026-10-05
---

# LT-107664: Koyu Lesson Quiz and Total Score

## Summary

Koyu needs to retain the existing percentage-based Lesson Quiz field while providing two alternate score fields: Total Score and Test Result. Both new fields are optional and accept negative values with at most one decimal place. A Lesson Custom Setting selects the SF layout while an internal configuration selects the BO/Learner App layout; the change must preserve the existing layout when disabled and synchronize saved score data across platforms.

The linked PRD is the primary source. This analysis intentionally focuses on the PRD; its linked Figma design has not yet been compared.

---

## Acceptance Criteria

### US01 — View/Edit Lesson Quiz as Before

| ID | Actor and condition | Expected behavior |
|---|---|---|
| AC 1.1 | Lesson Custom Setting is **OFF** (default); staff opens the Lesson Report tab on Lesson Detail or Lesson Report in SF/BO | Lesson Quiz is displayed and editable with its automatic `%` behavior. Total Score and Test Result are hidden. |
| AC 1.2 | Lesson Custom Setting is **OFF** (default); student opens the Lesson Report tab on Lesson Detail in the App | Lesson Quiz is displayed; Total Score and Test Result are hidden. |

### US02 — Use new fields (Total Score and Test Result)

| ID | Actor and condition | Expected behavior |
|---|---|---|
| AC 2.1.1 | Lesson Custom Setting is **ON**; staff opens the Lesson Report tab on Lesson Detail or Lesson Report in SF/BO | Lesson Quiz is hidden. Total Score and Test Result are displayed and editable. Both are optional and allow negative values with up to one decimal place. Invalid input blocks Save and shows the locale-appropriate validation error. A successful change is reflected across the platform immediately. |
| AC 2.1.2 | Configuration is **ON**; student or parent opens the Lesson Report tab on Lesson Detail in the App | Lesson Quiz is hidden; both Total Score and Test Result are displayed read-only. Published-report visibility remains the App baseline. |

### Scope and data model stated by the PRD

| Item | PRD statement |
|---|---|
| Total Score | `MANAERP__Total_Score__c`, Number (16,1), represents the maximum score; optional; supports negative values and at most one decimal place. |
| Test Result | `MANAERP__Test_Result__c`, Number (16,1), permits negative values and one decimal place. |
| Included surfaces | SF Lesson Report tab on Lesson Detail and Lesson Report, BO Lesson Report, App read-only. |
| Explicitly excluded | Altering Lesson Quiz behavior, historical-data migration, analytics/reporting changes, and automatic calculations between new fields. |
| Localization | Total Score / `満点`; Test Result / `テスト結果`. |

---

## Business Rules (Extracted)

| # | AC | Business Rule | Field | Field Behavior | Platform |
|---:|---|---|---|---|---|
| 1 | AC 1.1 | With config OFF, staff see Lesson Quiz. | Lesson Quiz | editable | SF / BO |
| 2 | AC 1.1 | With config OFF, Lesson Quiz retains automatic `%` formatting. | Lesson Quiz | auto-formatted percentage | SF / BO |
| 3 | AC 1.1 | With config OFF, Total Score is hidden. | Total Score | hidden | SF / BO |
| 4 | AC 1.1 | With config OFF, Test Result is hidden. | Test Result | hidden | SF / BO |
| 5 | AC 1.2 | With config OFF, the App shows Lesson Quiz and hides both new fields. | all score fields | visible read-only / hidden | App |
| 6 | AC 2.1.1 | With config ON, staff do not see Lesson Quiz. | Lesson Quiz | hidden | SF / BO |
| 7 | AC 2.1.1 | With config ON, staff can edit Total Score. | `MANAERP__Total_Score__c` | editable | SF / BO |
| 8 | AC 2.1.1 | Total Score is optional and accepts negative values with at most one decimal place. | Total Score | validated numeric | SF / BO |
| 9 | AC 2.1.1 | Invalid Total Score blocks Save and displays the locale-appropriate stated error. | Total Score | validation error | SF / BO |
| 10 | AC 2.1.1 | With config ON, staff can edit Test Result. | `MANAERP__Test_Result__c` | editable | SF / BO |
| 11 | AC 2.1.1 | Test Result accepts negative values with at most one decimal place. | Test Result | validated numeric | SF / BO |
| 12 | AC 2.1.1 | Invalid Test Result blocks Save and displays the stated EN/JP error. | Test Result | validation error | SF / BO |
| 13 | AC 2.1.1 | Successful saves are reflected across the platform immediately. | both new fields | cross-platform synchronization | SF → BO → App |
| 14 | AC 2.1.2 | With config ON, the App hides Lesson Quiz and shows Total Score and Test Result read-only to students and parents. | all score fields | hidden / visible read-only | App |
| 15 | Localization | Field labels are localized for EN/JP. | both new fields | localized labels | SF / BO / App |
| 16 | Scope | New values are independent; no calculation, migration, analytics change, or Lesson Quiz behavior change is included. | all score fields | independent stored values | all |

---

## Conflict & Gap Analysis

### Conflicts with Existing System

| # | Tag | Source | AC | Description |
|---:|---|---|---|---|
| 1 | [REGRESSION RISK] | `knowledge/domain-knowledge/scheduling/lesson-management/lesson.md`; `lesson-mobile.md` | AC 1.1 / 1.2 | A conditional layout changes the SF → BO → App Lesson Report synchronization path. Config OFF must retain the percentage Lesson Quiz and must not render new fields or alter its payload. |

### Missing in Requirements

| # | Tag | Source | Description |
|---:|---|---|---|
| 1 | [UNDOCUMENTED IN AC] | Linked Figma URL in Jira/PRD | Figma comparison was deferred for this PRD-focused analysis. Its control states, visual text, and App layout must be reconciled before final test-case approval. |

### Lesson-Learned Risks

No relevant historical incidents found. Core and OOP lesson-learned entries were checked using entity and operation overlap; their student-assignment, bulk-write, and point-sync incidents do not match this Lesson Report score-field edit/save flow.

### E2E Scenario Impact

| Scenario | Title | Impact | Action |
|---|---|---|---|
| E2E-01 | Lesson Lifecycle — Create, Teach, Report, View | Add Koyu config ON/OFF branches to BO report editing and Mobile published-report viewing; validate persistence and display. | UPDATE |
| E2E-34 / E2E-35 | Automated Reports — report lifecycle and Mobile flow | Add regression checks that score fields do not affect report auto-creation, per-student ownership, or OFF-layout Mobile rendering. | UPDATE |

### Assumptions Made

- This is a Koyu-specific, configuration-gated feature and belongs under `OOP/koyu`.
- Total Score and Test Result are independent optional values on each student's Lesson Report Detail. Negative values with at most one decimal place are allowed for both; the Salesforce `Number (16,1)` schema supplies the stored precision/range boundary.
- The SF Custom Setting controls the SF layout; the internal config `lesson.test_scores_lesson_report.is_enabled` controls BO and Learner App. Disabled layouts hide, rather than delete, stored values.
- SF is the source of truth, BO is a report-editing surface, and the App is read-only. The App renders the scores on the existing published-report lifecycle.
- All staff permission categories may view/edit the score fields; students and parents both receive the defined App visibility.
- EN and JP each render only their respective localized labels and validation messages.
- Figma was intentionally not analyzed because the requested focus was the PRD. No Figma-derived behavior has been inferred.
- No Qase suite was supplied, so no existing Qase coverage was inspected.

---

## Clarification Questions

All seven clarification points were answered by the requester on 2026-10-05 and incorporated into this specification. No Jira comment is required or will be posted.

## Related Specs

- No directly matching existing feature spec was found for Koyu Lesson Quiz, Total Score, Test Result, or either cited configuration name.
- `knowledge/domain-knowledge/scheduling/lesson-management/lesson.md` — Lesson Report ownership and SF → BO → Mobile synchronization baseline.
- `knowledge/domain-knowledge/scheduling/lesson-management/lesson-mobile.md` — published-report Mobile visibility baseline.

## Related Test Cases

- `epics/lesson/LT-90306-lesson-allocation-soft-delete/test-cases/published-report-student-mobile-archive.md` — related published-report Mobile regression surface; noted but not used as a direct feature baseline.
- `epics/OOP/nichibei/PBT-3507-nichibei-improvements/test-cases/lesson-report-display.md` — related learner-App report-display surface for another tenant; noted only.

## QASE Coverage Gaps

- Qase suite was not provided, so existing Qase coverage is unknown.
- AC 1.1 / 1.2 — Config OFF layout, automatic `%` preservation, and SF/BO/App non-regression need coverage.
- AC 2.1.1 — optional negative/one-decimal validation, field ownership, SF → BO → App propagation, and invalid-save behavior need coverage.
- AC 2.1.2 — both score fields' App visibility and existing published-report lifecycle behavior need coverage.
