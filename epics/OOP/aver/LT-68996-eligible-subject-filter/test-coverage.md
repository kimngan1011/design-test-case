# Test Coverage: LT-68996 — A.ver eligible subject filter

**Jira:** https://manabie.atlassian.net/browse/LT-68996  
**Date:** 2026-07-23  
**Module:** scheduling / OOP/aver  
**Platforms:** Salesforce and Manacalendar

## 1. Business Rules

| # | AC | Business Rule |
|---|---|---|
| 1 | AC 01 | For A.ver, selecting two or more subjects uses AND matching. |
| 2 | AC 02 | A teacher who is eligible for only one selected subject is excluded. |
| 3 | AC 03 | With one selected subject, every teacher eligible for that subject remains available. |
| 4 | AC 04 | The same rule applies in Add Teacher, Teacher list, and Calendar filter. |
| 5 | AC 05 | The tenant customization does not change the existing OR behavior outside A.ver. |

## 2. Coverage Strategy

| AC | Surface | Technique | Risk | Depth |
|---|---|---|---|---|
| AC 01, AC 04 | Add Teacher | Decision Table | High | Standard |
| AC 02 | Add Teacher | Negative | High | Standard |
| AC 03 | Add Teacher | Equivalence Partitioning | Medium | Standard |
| AC 01, AC 04 | Teacher list | Decision Table | High | Standard |
| AC 02 | Teacher list | Negative | High | Standard |
| AC 05 | Teacher list | Regression | High | Standard |
| AC 01, AC 04 | Calendar filter | Decision Table | High | Standard |
| AC 02 | Calendar filter | Negative | High | Standard |
| AC 03 | Calendar filter | Equivalence Partitioning | Medium | Standard |

## 3. High-Risk Areas

- Partial matches must never be shown as eligible when multiple subjects are selected for A.ver.
- All three entry points must produce the same eligible-teacher set from identical data.
- The A.ver configuration must not alter a non-A.ver tenant's existing OR behavior.

## 4. Coverage Gaps

No linked Qase cases exist for LT-68996. All listed coverage is new.

## 5. Suggested Test Suite Structure

```text
test-cases/
|- 01-add-teacher-eligible-subject-filter.md
|- 02-teacher-list-eligible-subject-filter.md
|- 03-calendar-eligible-subject-filter.md
```
