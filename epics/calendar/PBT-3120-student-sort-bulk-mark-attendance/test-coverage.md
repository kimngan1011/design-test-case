# Test Coverage: PBT-3120 - Student Sort in Bulk Mark Attendance

**Jira:** https://manabie.atlassian.net/browse/PBT-3120
**Date:** 2026-07-02
**Module:** scheduling / calendar
**Platform:** BO Calendar (Renseikai priority)

---

## 1. Business Rules Extracted

| # | AC | Business Rule |
|---|---|---|
| 1 | AC 01.1 | Student list order uses Grade as first sort key |
| 2 | AC 01.1 | When Grade is equal, sort by Phonetic Name |
| 3 | AC 01.1 | When Grade and Phonetic Name are equal, sort by Student Name |
| 4 | AC 01.1 | When first three keys are equal, sort by Created at |
| 5 | AC 01.2 | Target flow sorting must match LT-77063 behavior baseline |
| 6 | AC 02.2 | Type labels render as 通常 / 体験 / 講習 |

---

## 2. Logic Type Categorization

| AC | Business Rule # | Logic Type |
|---|---|---|
| AC 01.1 | 1, 2, 3, 4 | Ordering / Sort, Conditional logic |
| AC 01.2 | 5 | Cross-system impact, Regression |
| AC 02.2 | 6 | Display completeness, Conditional logic |

---

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
|---|---|
| Ordering / Sort | Scenario, Pairwise |
| Conditional logic | Decision Table, Negative |
| Cross-system impact | Regression |
| Display completeness | Component, Negative |

---

## 4. Structured Coverage Strategy

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
|---|---|---|---|---|---|
| AC 01.1 | Grade is the primary sort key in Bulk Mark Attendance student list | Ordering / Sort | Scenario | High | Deep |
| AC 01.1 | Phonetic Name resolves ties inside same Grade group | Ordering / Sort, Conditional logic | Scenario, Decision Table | High | Deep |
| AC 01.1 | Student Name resolves ties when Grade + Phonetic Name are equal | Ordering / Sort | Scenario | Medium | Standard |
| AC 01.1 | Created at resolves final ties to deterministic order | Ordering / Sort | Scenario, Pairwise | Medium | Standard |
| AC 01.1 | Empty/Null Phonetic Name ordering is deterministic and stable | Conditional logic, Ordering / Sort | Decision Table, Negative | High | Deep |
| AC 01.2 | Sorting output matches LT-77063 baseline for equivalent datasets | Cross-system impact, Regression | Regression, Scenario | Medium | Standard |
| AC 02.2 | Type options show exact JP strings 通常 / 体験 / 講習 | Display completeness | Component | Medium | Standard |
| AC 02.2 | Untranslated English Type labels are absent in target scope | Conditional logic, Display completeness | Negative, Component | Medium | Standard |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| _None_ | No data write or destructive state transition in this ticket | N/A |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| AC 01.1 multi-key sorting | Non-deterministic ordering causes attendance mistakes and repeated user re-checks | Use mixed dataset with tie conditions for each key and assert exact row-by-row order |
| AC 01.1 null phonetic fallback | Null/empty phonetic values are common and often regress tie-break logic | Add dedicated null/empty phonetic dataset and explicit expected ordering |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
|---|---|---|
| AC 01.2 parity with LT-77063 | Future code divergence can reintroduce inconsistent sorting across surfaces | Add one parity regression case with same fixture data and expected order |
| AC 02.2 JP translations | Missing label mapping leaves mixed EN/JP UX | Assert exact strings and assert English labels are absent in target scope |

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Multi-key sort (Grade > Phonetic > Name > Created at) in Bulk Mark Attendance | epics/lesson/LT-XXXX-student-assignment/test-cases/student-assignment-lesson-detail.md | Partial (sorting exists in different screen) | ✅ New suite for Bulk Mark Attendance sort |
| Null/empty phonetic fallback in this page | None found for this page | None | ✅ Dedicated tie-break fallback tests |
| Parity with LT-77063 behavior | No direct parity case in current epic folder | None | ✅ One regression parity case |
| Type label JP translation in this page | No direct case found in this epic folder | None | ✅ New suite for JP label mapping |

---

## 7. Suggested Test Suite Structure

```text
epics/calendar/PBT-3120-student-sort-bulk-mark-attendance/test-cases/
├── 01-student-sort-order.md
│   └── AC 01.1, AC 01.2 - multi-key sort order, null fallback, baseline parity
└── 02-type-option-translation.md
    └── AC 02.2 - JP translation exact-string checks and untranslated-label absence
```

Estimated total: 7 test cases.

---

## 8. Mandatory Edge-Case Checklist Application (Step 4.5)

### A. Configuration-driven thresholds
- N/A: No configuration threshold rule in requirement.

### B. Date / Time logic
- N/A: Created at is used as a tie-break key but no time-window gating or timezone boundary logic is introduced.

### C. Concurrent / stale state
- N/A: No write action or race-sensitive submit flow in this requirement.

### D. Permission & role
- Yes: BO Calendar has role-dependent visibility (CPU/SPU), so one coverage row should assert ordering and label consistency across eligible roles.

### E. State transition
- N/A: No entity status transition.

### F. Cross-system / cross-surface
- Yes: AC 01.2 requires parity against LT-77063 baseline behavior.

### G. Downstream effects inventory (CRUD/state-change)
- N/A: No CREATE/UPDATE/DELETE behavior introduced.

### H. Display completeness and ordering
- Yes: Primary requirement is ordering behavior and exact display labels.
- Required inventory:
  - Screen / Component: Bulk Mark Attendance student list
  - Required Fields: grade, phonetic name, student name, created at
  - Sort Rule: Grade > Phonetic Name > Student Name > Created at
  - Tooltip / Text to Assert: Type options exactly 通常 / 体験 / 講習

### H.1 Spec-Figma mismatch
- H.1 - N/A: No Figma URL available in the spec.
