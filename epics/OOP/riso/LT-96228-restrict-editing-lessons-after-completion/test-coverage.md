# Test Coverage: LT-96228 — Restrict Editing Lessons After Completion

**Jira:** https://manabie.atlassian.net/browse/LT-96228  
**Date:** 2026-09-09

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---:|---|---|
| 1 | AC01.1 | A completed lesson cannot be reverted to Published by a user without the custom permission defined for this epic. |
| 2 | AC01.1 | A blocked rollback shows the exact English error: `You are not allowed to change the status of a completed lesson.` |
| 3 | AC01.1 | A blocked rollback in Japanese locale shows: `完了済の授業のステータスを変更するには権限が必要です。` |
| 4 | AC02.1 | A staff member with the epic custom permission can revert a completed lesson to Published. |
| 5 | AC02.1 | After an authorized rollback, Lesson Details are editable again. |
| 6 | AC01.1 | A blocked Completed → Published attempt does not send a teacher email. |

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---:|---|
| AC01.1 | 1 | Permission logic; Conditional logic; State transition; Data integrity |
| AC01.1 | 2, 3 | Validation logic; Display completeness; Cross-system impact |
| AC02.1 | 4 | Permission logic; Conditional logic; State transition; Data integrity |
| AC02.1 | 5 | State transition; Cross-system impact |
| AC01.1 | 6 | Conditional logic; Cross-system impact; Data integrity |

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Permission logic | Permission Matrix; Decision Table; Negative |
| Conditional logic | Decision Table; Negative |
| State transition | State Transition; Regression |
| Data integrity | CRUD; Regression; Decision Table |
| Validation logic | Equivalence Partitioning; Negative |
| Display completeness | Component; Negative |
| Cross-system impact | Regression; CRUD |

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC01.1 | Deny Completed → Published when custom permission is absent, consistently across SF Lesson Details and SF Lesson List bulk change. | Permission; Conditional; State transition | Permission Matrix; Decision Table; Negative | Critical | Deep |
| AC01.1 | Preserve the Completed status and prevent bypass through rapid repeat action, stale UI, or a different named entry point when permission is absent. | Permission; Data integrity; State transition | Negative; State Transition; Regression | Critical | Deep |
| AC01.1 | Display the exact English denial text. | Validation; Display completeness | Component; Negative | High | Standard |
| AC01.1 | Display the exact Japanese denial text when Japanese locale is selected. | Validation; Display completeness | Equivalence Partitioning; Component | High | Standard |
| AC01.1 | Do not send teacher email after a blocked rollback. | Conditional; Cross-system; Data integrity | Decision Table; Regression | Critical | Deep |
| AC02.1 | Allow Completed → Published when the custom permission is present in SF Lesson Details and SF Lesson List bulk change. | Permission; Conditional; State transition | Permission Matrix; Decision Table; State Transition | Critical | Deep |
| AC02.1 | Restore Lesson Details editability after the authorized state change. | State transition; Cross-system | State Transition; Regression | High | Deep |

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Server-side custom-permission enforcement | An unauthorized Completed → Published correction can compromise Riso’s completed-record integrity; client-only enforcement leaves a bulk or stale-request bypass. | Permission matrix for granted/absent permission × both in-scope Salesforce surfaces; assert status remains Complete on every denied request. |
| Blocked-change notification isolation | A blocked correction must not send a teacher email. A generic "status changed to Published" event could notify teachers despite denial. | Exercise denied changes from each applicable bulk/single surface and assert zero outbound email/event records. |
| Authorized rollback state integrity | Authorized correction must write the intended state exactly once and restore Lesson Details editability. | State-transition and repeated-submit tests across the two in-scope Salesforce surfaces. |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Two-surface consistency | SF Lesson Details and SF Lesson List bulk change can implement different permission checks. | Execute the same permission matrix at both in-scope entry points. |
| Locale-specific denial text | Compliance-facing errors must be precise; a translation fallback or wrong locale misleads staff. | Assert the complete EN and JP strings verbatim. |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Existing core status tests | Core tests expect unrestricted rollback; improper scoping could change non-Riso or permitted-user behavior. | Regression-test a permitted Riso user and the unaffected core status-transition baseline. |

## 6. Mandatory Edge-Case Checklist

| Section | Applicable? | Coverage Decision |
|---|---|---|
| A. Configuration-driven thresholds | N/A | No numeric or configuration threshold is specified. The epic custom permission is an authorization input, covered in Section D rather than threshold BVA. |
| B. Date / time logic | N/A | Completed status is the sole confirmed trigger; no current-date, timezone, or deadline condition is in scope. |
| C. Concurrent / stale state | Yes | Denied rapid repeat/multi-tab action cannot bypass permission or produce an email; authorized repeated submit produces one resulting state and no duplicate side effect. |
| D. Permission & role | Yes | Test custom permission **present** and **absent** at both in-scope Salesforce surfaces. Tenant isolation is N/A because the updated scope defines only Riso behavior. |
| E. State transition | Yes | Positive: permitted Completed → Published. Negative: absent permission keeps Complete. |
| F. Cross-system / cross-surface | Yes | Verify outbound teacher-email absence after a denied action. Sync-failure behavior is N/A because no SLA or failure handling is specified; verify no partial status write on an error response. |
| G. Downstream effects | Yes | Inventory below maps every known status, editability, surface, and email outcome to a test case. |
| H. Display completeness & ordering | Yes | Inventory below covers the only specified UI output: exact denial text. Sorting, empty state, pagination, tooltips, and non-error required field sets are N/A because the spec defines none. |
| H.1 Spec–Figma mismatch | N/A | No Figma URL is present in the approved spec. |

### G. Downstream Effects Inventory

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner (TC) |
|---|---|---|---|
| Denied Completed → Published request | Lesson status remains `Complete`; no partial write. | Lesson record / initiating surface | `completed-lesson-rollback-authorization.md` — denied matrix |
| Denied Completed → Published request | No teacher email is sent. | Teacher email delivery/event log | `completed-lesson-rollback-authorization.md` — denied no-email |
| Denied Completed → Published request | A retry, multi-tab request, or another named entry point remains denied. | Server authorization boundary | `completed-lesson-rollback-authorization.md` — bypass/idempotency |
| Authorized Completed → Published request | Lesson status becomes `Published`. | Lesson record / SF Lesson Details / SF Lesson List | `completed-lesson-rollback-authorization.md` — authorized matrix |
| Authorized Completed → Published request | Lesson Details become editable. | SF Lesson Details | `completed-lesson-rollback-authorization.md` — editability restoration |

### H. Display & Ordering Inventory

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| Error notification on named action surface | Denial message | English for EN locale; Japanese for JP locale | N/A — no list/order specified | `You are not allowed to change the status of a completed lesson.` / `完了済の授業のステータスを変更するには権限が必要です。` |
| Lesson Details after permitted rollback | Status `Published`; fields become editable | Editability applies only after custom-permission-authorized rollback | N/A — no list/order specified | N/A — no additional exact UI text specified |

## 7. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Permission-based Completed → Published restriction | `epics/lesson/LT-XXXX-lesson-status/test-cases/lesson-status.md` — TC-1456 and TC-1470 | Core cases cover rollback but have no Riso custom-permission condition. | ✅ Permission-present/absent matrix for all four named surfaces. |
| Denied exact EN/JP messages | No linked Qase case; core status tests do not assert these messages. | None. | ✅ Verbatim error tests for EN and JP locale. |
| No-email result after denied change | `epics/OOP/riso/LT-101725-lesson-publish-notifications/test-coverage.md` covers email only for Draft → Published. | Partial notification-boundary baseline. | ✅ Denied rollback produces no teacher email/event. |
| Editability after authorized rollback | Core cases verify status transition but not permission-gated restoration of Lesson Details editability. | Partial. | ✅ Verify editable fields after permitted rollback and no editability bypass when denied. |

## 8. Suggested Test Suite Structure

```text
epics/OOP/riso/LT-96228-restrict-editing-lessons-after-completion/test-cases/
└── completed-lesson-rollback-authorization.md  → AC01.1 and AC02.1 — custom-permission matrix, exact messages, no-email guard, editability restoration, and named-surface regression
```
