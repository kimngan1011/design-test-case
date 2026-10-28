# Test Coverage: LT-108370 — Teacher Lesson Access

**Jira:** https://manabie.atlassian.net/browse/LT-108370  
**Date:** 2026-10-08

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|---|---|
| BR-01 | AC-01 | Creating an active User repairs access for its Contact's existing lesson-teacher assignments. |
| BR-02 | AC-02 | Reactivating a User repairs missing access for its Contact. |
| BR-03 | AC-03 | Missing Lesson shares have Edit access and `Lesson_Teacher__c` row cause. |
| BR-04 | AC-03 | Missing allocation shares are created only through non-deleted student sessions. |
| BR-05 | AC-05 | A Contact with no lesson-teacher assignment produces no work and no shares. |
| BR-06 | AC-04 | Reprocessing is idempotent and preserves other teachers' shares. |
| BR-07 | AC-01, AC-02 | Eligible work enters Master Queue asynchronously. |
| BR-08 | AC-06 | Pending/Failed work deduplicates; Success permits a later reconciliation run. |
| BR-09 | AC-07 | One Contact per batch protects governor limits. |
| BR-10 | AC-07 | The 100 Users × 100 Lessons recovery completes with correct shares. |

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC-01 | BR-01, BR-03, BR-07 | Conditional logic; State transition; Data integrity; Cross-system impact; Display completeness |
| AC-02 | BR-02, BR-07 | State transition; Conditional logic; Cross-system impact |
| AC-03 | BR-03, BR-04 | Data integrity; Conditional logic; Permission logic |
| AC-04 | BR-06 | Data integrity; Conditional logic |
| AC-05 | BR-05 | Conditional logic; Negative |
| AC-06 | BR-08 | State transition; Data integrity; Conditional logic |
| AC-07 | BR-09, BR-10 | Boundary/range logic; Data integrity; Cross-system impact |

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Conditional logic | Decision Table; Negative |
| State transition | State Transition; CRUD |
| Data integrity | CRUD; Regression; Decision Table |
| Cross-system impact | Regression; CRUD |
| Permission logic | Permission Matrix; Decision Table |
| Display completeness | Component; Negative |
| Boundary/range logic | Boundary Value Analysis; Negative |

## G. Downstream Effects Inventory

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner (TC) |
|---|---|---|---|
| Create active User for assigned Contact | Queue request is created asynchronously | `Master_Queue__c` | TC-MQ-01 |
| Create/activate eligible User | Missing lesson share is created with recipient, Edit access, and row cause | `Lesson__Share` | TC-SHARE-01 / TC-SHARE-02 |
| Create/activate eligible User | Missing allocation share is created only for a non-deleted session | `Lesson_Allocation__Share` | TC-SHARE-03 / TC-SHARE-04 |
| Share creation | Assigned lesson becomes visible to that teacher in BO | BO lesson list/detail | TC-BO-01 |
| Retry/reprocess Contact | Existing shares are unchanged and no duplicate exists | Share records | TC-IDEMP-01 |
| User reactivation after a successful run | A later queue request can reconcile later-missing access | `Master_Queue__c`, share records | TC-MQ-03 |
| Queue retry state | Pending/Failed duplicate request is suppressed | `Master_Queue__c` | TC-MQ-02 |

Inverse action: N/A. This feature only repairs missing shares; revocation remains outside LT-108370.

## H. Display & Ordering Inventory

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| BO teacher lesson list | Assigned lesson name is visible after access recovery | N/A | No ordering contract in the ticket | N/A |

H.1 — N/A: No Figma URL in the spec.

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC-01 | Active User created after assignment recovers all assigned lesson access | Conditional; State transition; Cross-system | State Transition; Regression | High | Deep |
| AC-01 | Queue is submitted for an eligible Contact without mixed-DML failure | Data integrity; Cross-system | CRUD; Regression | High | Deep |
| AC-01 | Recovered teacher sees the assigned lesson name in BO | Display completeness; Cross-system | Component; Regression | High | Standard |
| AC-02 | Inactive-to-active transition recovers missing access | State transition; Conditional | State Transition; Decision Table | High | Deep |
| AC-03 | Lesson share has correct recipient, Edit level, and row cause | Data integrity; Permission | CRUD; Permission Matrix | High | Deep |
| AC-03 | Allocation share is added for a non-deleted Student Session | Conditional; Data integrity | Decision Table; CRUD | High | Deep |
| AC-03 | Deleted Student Session does not cause allocation share creation | Conditional; Negative | Decision Table; Negative | Medium | Standard |
| AC-04 | Reprocessing produces exactly one share and does not alter another teacher's share | Data integrity | CRUD; Regression | High | Deep |
| AC-05 | Contact with no lesson assignment does not enqueue or receive any share | Conditional | Equivalence Partitioning; Negative | Medium | Standard |
| AC-06 | Existing Pending/Failed work blocks a duplicate request | State transition; Data integrity | State Transition; Decision Table | High | Deep |
| AC-06 | Completed Success work allows a new reconciliation request | State transition; Data integrity | State Transition; CRUD | Medium | Standard |
| AC-07 | One Contact with many lesson assignments completes without partial shares | Boundary/range; Data integrity | Boundary Value Analysis; Regression | High | Deep |
| AC-07 | 100 active/re-activated Users × 100 lessons produce complete and unique access | Boundary/range; Cross-system | Boundary Value Analysis; Regression | High | Deep |

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| None identified | The change repairs access records but does not alter financial, billing, or destructive data. | N/A |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| User activation recovery | A failure leaves a teacher unable to see every assigned lesson in BO. | Cover create-active and inactive→active paths, then validate SF shares and BO visibility. |
| Share data integrity | Wrong recipient, access level, row cause, or duplicate affects authorization. | Inspect exact `Lesson__Share` and `Lesson_Allocation__Share` fields; re-run recovery and compare counts. |
| Master Queue lifecycle | Duplicate, stuck, or failed work delays recovery and wastes asynchronous capacity. | Exercise Pending, Failed, and Success states; validate queue status and share outcome. |
| High assignment volume | A long lesson history can exceed per-transaction limits or create partial recovery. | Execute one-contact high-volume case and the requested 100 × 100 stress run; reconcile expected vs actual share counts. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| No assignment / deleted session | Incorrect filtering could create unnecessary queue work or allocation access. | Negative cases for a non-teacher Contact and deleted Student Session. |

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Active-user recovery | None in PX/3703 | None | ✅ Create-active recovery, queue, exact lesson share, and BO visibility |
| Reactivation recovery | None in PX/3703 | None | ✅ Inactive→active state transition and recovered shares |
| Allocation sharing | None in PX/3703 | None | ✅ Non-deleted vs deleted student-session branches |
| Idempotency / authorization isolation | None in PX/3703 | None | ✅ Reprocess same Contact and preserve another teacher's share |
| Queue lifecycle | None in PX/3703 | None | ✅ Pending/Failed suppression and Success requeue |
| Scale | None in PX/3703 | None | ✅ Per-contact high volume and 100 × 100 stress reconciliation |

## 7. Suggested Test Suite Structure

```
epics/lesson/LT-108370-teacher-lesson-access/test-cases/
├── user-activation-recovery.md       → AC-01, AC-02, AC-03: activation/recovery and BO visibility
├── sharing-integrity.md              → AC-03, AC-04, AC-05: share fields, deleted sessions, idempotency, no-assignment
├── master-queue-lifecycle.md         → AC-01, AC-02, AC-06: enqueue, duplicate suppression, and requeue
└── recovery-performance.md           → AC-07: high-volume and 100 × 100 stress coverage
```
