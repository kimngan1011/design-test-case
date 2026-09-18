# Test Coverage: LT-111026 - Aver Lesson Report duplicate prevention

**Jira:** https://manabie.atlassian.net/browse/LT-111026
**Date:** 2026-09-18
**Module:** scheduling / OOP/aver
**Platforms:** Salesforce, Back Office

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|---|---|
| 1 | AC 01.1 | Parallel create requests for the same Aver lesson create at most one active report. |
| 2 | AC 01.2 | A later create request returns or reuses the existing active report. |
| 3 | AC 01.3 | Duplicate prevention covers same-user multi-tab and different-user concurrent scenarios. |
| 4 | AC 02.1 | Existing active Draft report is reused. |
| 5 | AC 02.2 | Existing active Published report is reused; no new Draft is created. |
| 6 | AC 02.3 | A new report is created when no active report exists. |
| 7 | AC 03.1 | Lesson List, card, and detail show the same report status. |
| 8 | AC 03.2 | Student Session and detail records remain linked to one report. |
| 9 | AC 03.3 | Rapid retries do not introduce duplicates or orphan records. |

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC 01.* | 1, 2, 3 | Concurrency, Idempotency, Data integrity |
| AC 02.* | 4, 5, 6 | Decision table, Existing-record reuse, Boundary |
| AC 03.* | 7, 8, 9 | Regression, Relationship integrity, Status consistency |

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Concurrency/idempotency | Race-condition simulation, API-level parallel execution, Repeated-action regression |
| Existing-record reuse | Decision Table, State Transition |
| Status consistency | End-to-end regression, Cross-surface comparison |
| Relationship integrity | Data validation, CRUD verification |

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC 01.1-01.3 | Duplicate creation is prevented under same-user and different-user parallel creation. | Concurrency | Race-condition simulation | Critical | Deep |
| AC 02.1-02.3 | Existing active report is reused, while no-active state can still create one report. | Decision table | State Transition | High | Deep |
| AC 03.1 | Lesson List, report card, and detail status stay consistent after publish/reuse. | Regression | End-to-end comparison | High | Standard |
| AC 03.2-03.3 | Report details and Student Session links are not split by retry paths. | Data integrity | Query validation | High | Standard |

## 5. High-Risk Areas Requiring Deeper Testing

| Area | Reason | Recommended Approach |
|---|---|---|
| Backend race condition | UI-only prevention cannot stop two users or two tabs submitting at the same time. | Use automation/API-level parallel requests and verify one active `Lesson_Report__c` by lesson. |
| Published status mismatch | The incident showed detail page Published while Lesson List displayed Draft from the duplicate record. | Publish the single report, refresh all surfaces, and compare report ID/status. |
| Relationship split | Duplicate creation can split `Lesson_Report_Detail__c` and `Student_Sessions__c.Lesson_Report__c` across records. | Query relationships after retry and assert all active references point to one report. |

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Aver lesson report lifecycle | `LT-105354` covers report improvements and report status regressions. | Partial | Add concurrency and existing-report reuse cases. |
| Lesson Report navigation/card status | Existing cases cover card/list behavior indirectly. | Partial | Add list/card/detail same-report status validation after duplicate-prevention flow. |
| Race-condition creation | No direct `LT-111026` testcase found in the repo. | None | Add same-user two-tab, two-staff, and rapid retry cases. |

## 7. Suggested Test Suite Structure

```text
epics/OOP/aver/LT-111026-aver-lesson-report-duplicate-race-condition/test-cases/
|- aver-lesson-report-duplicate-prevention.md -> readable testcase design
|- aver-lesson-report-duplicate-prevention.csv -> Qase import format
```

Qase suite recommendation:

- Parent suite: `251` (same Aver Lesson Report parent used by `LT-105354`)
- New suite name: `[Aver] Lesson Report Duplicate Prevention`
