# Test Coverage: LT-107960 - Duplicate Lesson Duration validation

**Jira:** https://manabie.atlassian.net/browse/LT-107960
**Date:** 2026-09-18
**Module:** scheduling / lesson
**Platforms:** Salesforce, Calendar

---

## 1. Business Rules Extracted

| # | Rule |
|---|---|
| 1 | Duplicate Lesson form pre-populates Duration from Start/End time. |
| 2 | A valid populated Duration must not show `Complete this field.` on Save. |
| 3 | Duplicate Lesson from Lesson Detail saves successfully. |
| 4 | Duplicate Lesson from Calendar saves successfully. |
| 5 | Edit, Extend Recurrence, and drag/drop flows must not regress with the same false required validation. |

## 2. Coverage Strategy

| Area | Technique | Risk | Coverage |
|---|---|---|---|
| Lesson Detail duplicate | Regression, State transition | Critical | Exact reported bug path |
| Calendar duplicate | Entry-point regression | High | Same form opened from Calendar |
| Edit mode | Regression | High | Jira note says issue also occurs in edit mode |
| Extend Recurrence / Drag-drop | Regression | High | Jira note says same validation issue occurs in adjacent forms |

## 3. New Test Cases

| # | Case | Purpose |
|---|---|---|
| 1 | Duplicate individual lesson from Lesson Detail | Exact Jira reproduction path. |
| 2 | Duplicate lesson from Calendar popup | Calendar entry point for duplicate form. |
| 3 | Edit lesson with valid Duration | Adjacent edit-mode regression. |
| 4 | Extend Recurrence and drag/drop derived Duration | Adjacent derived-duration form regression. |

## 4. Existing Related Cases For Run

| Case | Why included |
|---|---|
| `PX-1207` | Duplicate Lesson happy path baseline. |
| `PX-20708` | Lesson form Duration field visibility baseline. |
| `PX-20734` | Calendar form Duration field visibility baseline. |
| `PX-11708` | Calendar Duplicate Lesson baseline. |
