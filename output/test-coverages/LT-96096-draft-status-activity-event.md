# Test Coverage: LT-96096 — Draft Status to Activity Event

**Jira:** https://manabie.atlassian.net/browse/LT-96096
**Epic:** https://manabie.atlassian.net/browse/LT-93068
**Date:** 2026-03-26

---

## Coverage Strategy Table

| AC      | Business Rule Summary                                              | Logic Type           | Test Technique          | Risk Level | Coverage Depth |
|---------|--------------------------------------------------------------------|----------------------|-------------------------|------------|----------------|
| AC 01.1 | "Draft" picklist value exists in Activity Event Status field       | Validation logic     | Equivalence Partitioning | High       | Standard       |
| AC 01.2 | Create form shows Draft and Published as status options            | Validation logic     | Equivalence Partitioning | High       | Standard       |
| AC 01.3 | Default status on new Activity Event = Published                   | Conditional logic    | Decision Table          | Critical   | Deep           |
| AC 02.1 | Draft events enforce same mandatory field validation as Published  | Validation logic     | Equivalence Partitioning, Negative Testing | Critical | Deep |
| AC 02.2 | Participants can be added/removed on a Draft event                 | Data integrity       | CRUD Testing            | High       | Standard       |
| AC 02.3 | Draft events can be deleted                                        | State transition     | State Transition Testing | High      | Standard       |
| AC 02.4 | Draft events can be edited                                         | Data integrity       | CRUD Testing            | High       | Standard       |
| AC 02.5 | Draft events can be duplicated                                     | Data integrity       | CRUD Testing            | Medium     | Standard       |
| AC 03.1 | Draft → Published is allowed                                       | State transition     | State Transition Testing | Critical  | Deep           |
| AC 03.2 | Draft → Completed is blocked — 'Completed' IS visible in the status path bar but clicking it triggers an error message (EN/JP) | State transition     | State Transition Testing, Negative Testing | Critical | Deep |
| AC 03.3 | Draft → Cancel is allowed                                          | State transition     | State Transition Testing | High      | Standard       |
| AC 04.1 | Draft events not shown in Learner app Calendar                     | Cross-system impact  | Regression Analysis     | Critical   | Deep           |
| AC 04.2 | Draft events not shown in Learner app Booking system               | Cross-system impact  | Regression Analysis     | Critical   | Deep           |
| AC 05.1 | Feature gated by feature flag                                      | Conditional logic    | Decision Table          | High       | Standard       |

---

## High-Risk Areas

### 🔴 Critical Risk
- **AC 03.2 — Draft → Completed blocked**: Core status transition guard. The status path bar (Draft → Published → Completed → Cancelled) shows all 4 stages, but clicking Completed from a Draft event triggers an error: "You cannot mark a Draft event to Complete. Please Publish first." (EN) / `下書きのイベントを完了にすることはできません。イベントを公開してください。` (JP). If broken, Draft events could be accidentally completed.
- **AC 01.3 — Default = Published**: If broken, new events would default to Draft, hiding them from learners unexpectedly.
- **AC 04.1/04.2 — Learner app visibility**: Draft events leaking to learner app would cause confusion. Cross-system validation required.
- **AC 02.1 — Mandatory field validation on Draft**: If Draft bypasses validation, incomplete events can be created.

### 🟠 High Risk
- **AC 03.1 — Draft → Published**: Main happy-path transition. Must not break.
- **AC 03.3 — Draft → Cancel**: If blocked, Draft events become un-cancelable.
- **AC 01.1/01.2 — Picklist values**: Foundation for the entire feature.
- **AC 02.2 — Participant management**: Data integrity risk if participants can't be managed on Draft.
- **AC 05.1 — Flag control**: If flag logic is wrong, feature may be exposed or hidden incorrectly.

### 🟡 Medium Risk
- **AC 02.3/02.4/02.5 — Edit, Delete, Duplicate**: Standard CRUD operations on Draft events.

---

## Coverage Gaps

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
|---|---|---|---|
| Draft status picklist | None | None | Full |
| Status transitions (Draft) | None | None | Full |
| Draft visibility on Learner app | None | None | Full |
| Flag control | None | None | Full |
| Draft CRUD operations | None | None | Full |

---

## Suggested Test Suite Structure

```
Qase PX > Suite 19 (parent)
  ├── US01: Activity Event Status Picklist     → AC 01.1–01.3 (3 cases)
  ├── US02: Draft Event Operations             → AC 02.1–02.5 (6 cases)
  ├── US03: Status Transitions                 → AC 03.1–03.3 (5 cases)
  ├── US04: Learner App Visibility             → AC 04.1–04.2 (3 cases)
  └── US05: Flag Control                       → AC 05.1 (2 cases)
```

Estimated total: ~19 test cases
