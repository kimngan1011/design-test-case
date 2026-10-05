# Test Coverage: LT-108371 — Remove "New" button from Lesson Report in LA detail page

**Jira:** https://manabie.atlassian.net/browse/LT-108371  
**Date:** 2026-09-15

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---:|---|---|
| 1 | AC 01 | `New` is absent for a Core Partner on STAG. |
| 2 | AC 01 | `New` is absent for Renseikai Core Partner on PREPROD. |
| 3 | AC 01 | `New` is absent for Nichibei Custom Partner on PREPROD. |
| 4 | AC 01 | `New` is absent for EEA Custom Partner on PREPROD. |
| 5 | AC 01 | `New` is absent for Aver Custom Partner on PREPROD. |
| 6 | AC 01 | `New` is absent for Riso Custom Partner on PREPROD. |
| 7 | AC 01 | `New` is absent for `full_access` PS. |
| 8 | AC 01 | `New` is absent for `center_level_edit` PS. |
| 9 | AC 01 | `New` is absent for Admin. |

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC 01 | 1–6 | Display completeness; Conditional logic |
| AC 01 | 7–9 | Display completeness; Permission logic |

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Display completeness | Component; Negative (named control absent) |
| Conditional logic | Decision Table (environment × partner × expected visibility) |
| Permission logic | Permission Matrix (profile × expected visibility) |

## 4. Mandatory Edge-Case Checklist

| Section | Assessment |
|---|---|
| A. Configuration-driven thresholds | N/A — no numeric threshold or configurable value is specified. |
| B. Date / time logic | N/A — no date or time condition affects the button. |
| C. Concurrent / stale state | N/A — read-only UI visibility; no shared mutable resource or time-based gate. |
| D. Permission & role | Applicable — separately assert absence for `full_access` PS, `center_level_edit` PS, and Admin. Cross-tenant access is outside scope. |
| E. State transition | N/A — this change does not transition an entity state. |
| F. Cross-system / cross-surface | N/A — only Salesforce LA Detail is in scope. |
| G. Downstream effects | N/A — no CREATE, UPDATE, DELETE, state change, counter, notification, or sync is performed. |
| H. Display completeness & ordering | Applicable — assert the Lesson Report tab loads and `New` is absent. One case covers each tenant/profile condition. No sort rule, tooltip, empty state, or pagination applies. |
| H.1 Spec–Figma mismatch | N/A — no Figma URL is in the Jira ticket or spec. |

### Downstream Effects Inventory

| Primary Action | Downstream Effect | Affected Entity / Surface | Verification Owner (TC) |
|---|---|---|---|
| Open LA Detail → Lesson Report tab | None — UI visibility only | Salesforce LA Detail | N/A |

### Display & Ordering Inventory

| Screen / Component | Required Fields | Conditional Fields | Sort Rule | Tooltip / Text to Assert |
|---|---|---|---|---|
| Salesforce LA Detail → Lesson Report tab | Lesson Report tab content loads; no `New` button is present | STAG Core; PREPROD Renseikai/Nichibei/EEA/Aver/Riso; three access profiles | None | Exact button label: `New` |

## 5. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC 01 | STAG Core Partner: `New` absent | Display completeness; Conditional logic | Component; Decision Table; Negative | Medium | Smoke |
| AC 01 | PREPROD Renseikai Core Partner: `New` absent | Display completeness; Conditional logic | Component; Decision Table; Negative | Medium | Smoke |
| AC 01 | PREPROD Nichibei Custom Partner: `New` absent | Display completeness; Conditional logic | Component; Decision Table; Negative | Medium | Smoke |
| AC 01 | PREPROD EEA Custom Partner: `New` absent | Display completeness; Conditional logic | Component; Decision Table; Negative | Medium | Smoke |
| AC 01 | PREPROD Aver Custom Partner: `New` absent | Display completeness; Conditional logic | Component; Decision Table; Negative | Medium | Smoke |
| AC 01 | PREPROD Riso Custom Partner: `New` absent | Display completeness; Conditional logic | Component; Decision Table; Negative | Medium | Smoke |
| AC 01 | `full_access` PS: `New` absent | Display completeness; Permission logic | Component; Permission Matrix; Negative | Medium | Smoke |
| AC 01 | `center_level_edit` PS: `New` absent | Display completeness; Permission logic | Component; Permission Matrix; Negative | Medium | Smoke |
| AC 01 | Admin: `New` absent | Display completeness; Permission logic | Component; Permission Matrix; Negative | Medium | Smoke |

## 6. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

None — the change neither writes data nor affects billing, state, or cross-system synchronization.

### 🟠 High Risk

None — there is no behavior beyond UI visibility in the stated scope.

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| Tenant and permission rollout | An incomplete deployment can leave `New` visible for one tenant or profile. | Run all six tenant cases and all three access-profile cases independently. |

## 7. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| STAG Core Partner | None in Qase suite 3533 | None | ✅ One absence assertion |
| PREPROD Renseikai Core Partner | None in Qase suite 3533 | None | ✅ One absence assertion |
| PREPROD Nichibei / EEA / Aver / Riso Custom Partners | None in Qase suite 3533; Riso has other hidden-control coverage | No `New` button coverage | ✅ Four absence assertions |
| `full_access` PS / `center_level_edit` PS / Admin | None in Qase suite 3533 | None | ✅ Three absence assertions |

## 8. Suggested Test Suite Structure

```
epics/lesson/lesson report/LT-108371-remove-new-button-lesson-report/test-cases/
└── new-button-visibility.md → AC 01 — six tenant and three access-profile cases
└── new-button-visibility.csv → Qase import source for the same nine cases
```
