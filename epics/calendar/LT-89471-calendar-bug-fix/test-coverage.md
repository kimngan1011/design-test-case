# Test Coverage: LT-89471 — Calendar bug fix (Daily scrollbar + recurring metadata)

**Jira:** https://manabie.atlassian.net/browse/LT-89471
**Date:** 2026-06-29
**Module:** scheduling / calendar
**Platform:** SF Calendar, BO Calendar

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|---|---|
| 1 | AC 01.1 | Daily view must expose horizontal navigation when timeline overflows viewport width |
| 2 | AC 02.1 | Recurring-until date must render as yyyy/mm/dd for Japanese locale users |
| 3 | AC 02.1 | Non-Japanese locale formatting remains locale-specific unless explicitly changed |
| 4 | AC 02.2 | Weekly Recurring label is replaced with Recurring Settings in recurring section |

---

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC 01.1 | 1 | Display completeness, Conditional logic, Cross-system impact |
| AC 02.1 | 2 | Display completeness, Conditional logic |
| AC 02.1 | 3 | Conditional logic, Regression |
| AC 02.2 | 4 | Display completeness, Conditional logic |

---

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Display completeness | Component, Negative |
| Conditional logic | Decision Table |
| Cross-system impact | Regression |
| Regression | Regression, Decision Table |

---

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC 01.1 | SF Daily view shows horizontal scrollbar when timeline overflows | Display completeness, Conditional | Component, Decision Table | High | Deep |
| AC 01.1 | BO Daily view shows horizontal scrollbar when timeline overflows | Display completeness, Conditional, Cross-system | Component, Regression | High | Deep |
| AC 01.1 | No-overflow state keeps full content reachable without broken layout | Conditional | Decision Table, Negative | Medium | Standard |
| AC 02.1 | Japanese locale renders recurring-until date in yyyy/mm/dd format | Display completeness, Conditional | Component, Decision Table | High | Deep |
| AC 02.1 | Non-Japanese locale keeps existing locale-specific format | Conditional, Regression | Decision Table, Regression | Medium | Standard |
| AC 02.1 | Runtime locale switch updates recurring-until date rendering consistently | Cross-system impact, Conditional | Regression, Decision Table | Medium | Standard |
| AC 02.2 | Recurring section label displays exact text Recurring Settings in SF right panel | Display completeness | Component | Medium | Standard |
| AC 02.2 | Recurring section label displays exact text Recurring Settings in BO right panel | Display completeness, Cross-system impact | Component, Regression | Medium | Standard |
| AC 02.2 | Legacy label Weekly Recurring is no longer shown on the target panel | Conditional, Regression | Negative, Regression | Medium | Standard |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| _None_ | No data write, no state mutation, and no cross-entity side effects in this ticket | N/A |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| AC 01.1 overflow scrollbar behavior | If scrollbar is still hidden under constrained viewport, users cannot reach right-side timeline and scheduling actions are blocked | Run viewport/zoom matrix for SF and BO, then assert both visibility and reachability of far-right timeline |
| AC 02.1 Japanese date format | Incorrect locale output causes user confusion and recurring chain misread in JP operations | Assert exact yyyy/mm/dd output with anchored date values and locale switch regression |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| AC 02.2 label rename scope | Scope is likely right panel only; if old text persists on target panel, UX remains inconsistent | Assert exact label text on target panel and ensure old text is absent there |
| AC 02.1 non-JP behavior | Fix for JP locale can accidentally force one format globally | Add non-JP regression case to ensure existing locale behavior remains |

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| AC 01.1 constrained-width horizontal scrollbar visibility + reachability | None found in this epic folder | None | ✅ New suite: Daily view scrollbar behavior |
| AC 02.1 ja-JP recurring-until date format | None found in this epic folder | None | ✅ New suite: Recurring date format by locale |
| AC 02.1 non-ja regression | None found in this epic folder | None | ✅ Add non-JP regression cases |
| AC 02.2 Recurring Settings exact wording | None found in this epic folder | None | ✅ New suite: Recurring section label |

---

## 7. Suggested Test Suite Structure

```text
epics/calendar/LT-89471-calendar-bug-fix/test-cases/
├── 01-daily-view-scrollbar.md
│   └── AC 01.1 — constrained-width overflow, scrollbar visibility/reachability on SF + BO
├── 02-recurring-date-format-locale.md
│   └── AC 02.1 — ja-JP yyyy/mm/dd rendering, non-ja regression, runtime locale switch
└── 03-recurring-settings-label.md
    └── AC 02.2 — exact label text assertion and old label removal on target panel
```

Estimated total: 11 test cases.

---

## 8. Mandatory Edge-Case Checklist Application (Step 4.5)

### A. Configuration-driven thresholds
- N/A: No config threshold rule in spec.

### B. Date / Time logic
- Yes: AC 02.1 is date-formatting and locale-sensitive.
- Include anchored test data (`recurring_until_source = YYYY-MM-DD`, explicit locale value) in all AC 02.1 cases.
- TZ and DST: N/A for this ticket because format rule is locale-based and does not derive from current timezone threshold.

### C. Concurrent / stale state
- N/A: No shared resource, no booking/capacity mutation.

### D. Permission & role
- N/A in requirement text: no role-specific branching is defined.

### E. State transition
- N/A: No entity status transition in this ticket.

### F. Cross-system / cross-surface
- Yes: SF and BO right-panel/calendar surfaces are both in scope.
- Covered in strategy rows for AC 01.1 and AC 02.2.

### G. Downstream effects inventory (CRUD/state-change)
- N/A: No CREATE/UPDATE/DELETE behavior is introduced by these ACs.

### H. Display completeness and exact text
- Yes: Scrollbar presence/absence, recurring date text format, and exact label text are display requirements.
- Covered by Component and Negative techniques.

### H.1 Spec-Figma mismatch
- H.1 — N/A: No Figma URL in spec.
