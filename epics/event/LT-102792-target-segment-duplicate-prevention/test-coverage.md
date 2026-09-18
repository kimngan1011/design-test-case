# Test Coverage: LT-102792 - Target Segment duplicate prevention

**Jira:** https://manabie.atlassian.net/browse/LT-102792
**Date:** 2026-09-18
**Module:** scheduling / event
**Platforms:** Salesforce

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|---|---|
| 1 | AC 01.1 | Existing Target Location cannot be selected again. |
| 2 | AC 01.2 | Existing Target Grade cannot be selected again. |
| 3 | AC 01.3 | Existing Target School cannot be selected again. |
| 4 | AC 01.4 | Existing Target Course cannot be selected again. |
| 5 | AC 02.1-02.4 | Save/API validation rejects duplicate Target Segment child records. |
| 6 | AC 03.1 | OR logic within one segment remains unchanged. |
| 7 | AC 03.2 | AND logic between different segments remains unchanged. |
| 8 | AC 03.3 | Target Location Enrollment Status filtering remains unchanged. |

## 2. Coverage Strategy

| Area | Technique | Risk | Coverage |
|---|---|---|---|
| Duplicate UI option prevention | Negative, Component | High | Target Location, Grade, School, Course |
| Backend/save duplicate rejection | API/CRUD negative | Critical | Stale UI/API payload for all child objects |
| Filtering regression | Decision table | High | OR within dimension, AND across dimensions, Enrollment Status |

## 3. New Test Cases

| # | Case | AC | Purpose |
|---|---|---|---|
| 1 | Target Location duplicate option disabled/hidden | AC 01.1 | UI prevents duplicate location selection. |
| 2 | Target Location duplicate save validation | AC 02.1 | Backend rejects duplicate location payload. |
| 3 | Target Grade duplicate option disabled/hidden and save blocked | AC 01.2 / AC 02.2 | UI and save validation for grade. |
| 4 | Target School duplicate option disabled/hidden and save blocked | AC 01.3 / AC 02.3 | UI and save validation for school. |
| 5 | Target Course duplicate option disabled/hidden and save blocked | AC 01.4 / AC 02.4 | UI and save validation for course. |
| 6 | Mixed unique Target Segment values remain selectable and save successfully | AC 03.1-03.3 | Regression that duplicate prevention does not block valid unique setup. |

## 4. Existing Related Qase Cases For Combined Run

| Case | Why included |
|---|---|
| `PX-19038` | Target Location lookup constraint baseline. |
| `PX-19039` | OR logic within Target Segment remains unchanged. |
| `PX-19042` | Enrollment Status filtering with Target Location remains unchanged. |
| `PX-19043` | Null Enrollment Status behavior remains unchanged. |
| `PX-19067` | Positive add Target Location flow. |
| `PX-19068` | Positive add Target Location with Enrollment Status flow. |
| `PX-19069` | Positive add Target School flow. |
| `PX-19070` | Positive add Target Grade flow. |
| `PX-19071` | Positive add Target Course flow. |
| `PX-19072` | Save & New multiple target record flow. |
| `PX-21530` | Existing duplicate Target Location UI prevention path. |
| `PX-21555` | Existing duplicate Target Location API rejection path. |

## 5. Coverage Gap Closed

Before LT-102792, Qase had positive Target Segment add flows and a Renseikai-specific duplicate Target Location path, but no direct case for duplicate Grade, School, Course, or core backend duplicate rejection across all four target segment child objects.
