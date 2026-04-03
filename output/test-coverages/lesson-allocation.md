# Test Coverage: Lesson Allocation — Full Lifecycle

**Spec:** `input/specs/lesson-allocation.md`
**Date:** 2026-04-02
**Improvement:** PBT-1859 — Add new course with past effective date

---

## 1. Business Rules Extracted

| #   | AC       | Business Rule                                                               |
| --- | -------- | --------------------------------------------------------------------------- |
| 1   | AC 01.1  | LA created per course where Require Allocation = True                       |
| 2   | AC 01.2  | LA start date = order start date                                            |
| 3   | AC 01.3  | LA end date = order end date                                                |
| 4   | AC 01.4  | LA teaching method = course master's teaching method                        |
| 5   | AC 01.5  | LA type = course type                                                       |
| 6   | AC 01.6  | LA product detail = course + package type                                   |
| 7   | AC 01.7  | Purchased slot depends on package type                                      |
| 8   | AC 01.8  | Total session count = 0 at creation; no student session auto-created        |
| 9   | AC 01.9  | LA visible in Contact → Course tab                                          |
| 10  | AC 01.10 | Class assigned → class_member created with LA duration                      |
| 11  | AC 01.11 | Past start date supported for all product types                             |
| 12  | AC 02.2  | Enrollment past start date supported                                        |
| 13  | AC 03.1  | Add new course (update order) → new LA, start = effective date              |
| 14  | AC 03.2  | Effective date < product start date → blocked with EN+JP error              |
| 15  | AC 03.3  | Past effective date ≥ product start date → allowed (PBT-1859)               |
| 16  | AC 03.6  | Existing LAs unchanged when new course added                                |
| 17  | AC 04.1  | Change course: old LA end date = effective date                             |
| 18  | AC 04.2  | Change course: new LA start date = effective date                           |
| 19  | AC 05.1  | Update slot → purchased slot updated                                        |
| 20  | AC 05.2  | Update slot → LA duration unchanged                                         |
| 21  | AC 05.3  | Update slot → total session count recalculated                              |
| 22  | AC 05.5  | Update slot → no student session auto-created                               |
| 23  | AC 05.6  | Update slot: effective date = past / today / future                         |
| 24  | AC 06.1  | Cancel Schedule/Frequency → LA end date = cancel date                       |
| 25  | AC 06.2  | Cancel Slot-Based/One-Time → LA deleted                                     |
| 26  | AC 06.3  | Cancel → student removed from out-of-range lessons                          |
| 27  | AC 06.5  | Cancel → completed/cancelled past lessons remain                            |
| 28  | AC 06.6  | Past-date cancel supported for Schedule and Frequency                       |
| 29  | AC 07.1  | Void new order → LA deleted                                                 |
| 30  | AC 07.2  | Void update (slot) → slot reverted                                          |
| 31  | AC 07.6  | Void update (add course, past date) → added LA deleted; original unchanged  |
| 32  | AC 08.1  | Withdrawal (last attendance > today) → LA end date updated; student removed |
| 33  | AC 08.2  | Withdrawal (last attendance < today) → same, different date boundary        |
| 34  | AC 09.1  | LOA (last attendance > today) → LA end date updated                         |
| 35  | AC 09.2  | LOA (last attendance < today) → same                                        |
| 36  | AC 09.4  | Resume LOA → new LA created from resume date                                |
| 37  | AC 10.7  | Require Allocation = False → no LA created or updated                       |
| 38  | AC 10.8  | Monthly product → LA NOT created                                            |

---

## 2. Logic Type Categorization

| AC            | Business Rule # | Logic Type                                                |
| ------------- | --------------- | --------------------------------------------------------- |
| AC 01.1–01.10 | 1–10            | CRUD Testing, Conditional logic                           |
| AC 01.11      | 11              | Boundary/range logic                                      |
| AC 02.2       | 12              | Boundary/range logic                                      |
| AC 03.1       | 13              | CRUD Testing, State transition                            |
| AC 03.2       | 14              | Boundary/range logic, Validation logic                    |
| AC 03.3       | 15              | Boundary/range logic                                      |
| AC 03.6       | 16              | Data integrity                                            |
| AC 04.1–04.2  | 17–18           | State transition                                          |
| AC 05.1–05.5  | 19–22           | CRUD Testing, Conditional logic                           |
| AC 05.6       | 23              | Boundary/range logic                                      |
| AC 06.1–06.6  | 24–28           | State transition, Conditional logic, Boundary/range logic |
| AC 07.1–07.6  | 29–31           | State transition                                          |
| AC 08.1–08.5  | 32–33           | State transition, Boundary/range logic                    |
| AC 09.1–09.5  | 34–36           | State transition                                          |
| AC 10.7–10.8  | 37–38           | Conditional logic, Permission logic                       |

---

## 3. Test Technique Selection

| Logic Type           | Applicable Techniques                                          |
| -------------------- | -------------------------------------------------------------- |
| CRUD Testing         | Create, update, delete paths; happy path + conflict/error path |
| Conditional logic    | Decision Table — one TC per distinct condition branch          |
| Boundary/range logic | BVA — test at exact boundary, below boundary, above boundary   |
| Validation logic     | Equivalence Partitioning + Negative Testing                    |
| State transition     | Valid transitions + invalid/blocked transitions                |
| Data integrity       | Verify related entity unchanged; side-effect isolation         |

---

## 4. Structured Coverage Strategy

| AC            | Business Rule Summary                                              | Logic Type                  | Test Technique           | Risk Level | Coverage Depth |
| ------------- | ------------------------------------------------------------------ | --------------------------- | ------------------------ | ---------- | -------------- |
| AC 01.1–01.11 | Create LA via new order group (all product types, past start date) | CRUD + Boundary             | CRUD Testing, BVA        | High       | Standard       |
| AC 02.1–02.2  | Create LA via enrollment (past start date)                         | CRUD + Boundary             | CRUD Testing, BVA        | High       | Standard       |
| AC 03.1       | Add new course (update order) → new LA                             | State transition            | CRUD + State Transition  | High       | Standard       |
| AC 03.2       | Effective date < product start date → blocked, error               | Validation                  | Negative Testing, BVA    | Critical   | Deep           |
| AC 03.3       | Effective date = past ≥ product start date → allowed               | Boundary                    | BVA                      | Critical   | Deep           |
| AC 03.6       | Existing LAs unchanged after add-course update                     | Data integrity              | Regression Analysis      | High       | Standard       |
| AC 04.1–04.2  | Change course: old LA closed, new LA opened                        | State transition            | State Transition Testing | High       | Standard       |
| AC 05.1–05.5  | Update slot: purchased slot updated, duration unchanged            | CRUD + Conditional          | CRUD Testing             | Medium     | Standard       |
| AC 05.6       | Update slot: past / today / future effective date                  | Boundary                    | BVA                      | High       | Deep           |
| AC 06.1       | Cancel Schedule/Frequency: LA end date = cancel date               | State transition            | State Transition + BVA   | High       | Standard       |
| AC 06.2       | Cancel Slot-Based/One-Time: LA deleted                             | State transition            | State Transition         | High       | Standard       |
| AC 06.3–06.5  | Cancel: lesson + class_member impact                               | Cross-system                | Regression Analysis      | High       | Standard       |
| AC 06.6       | Cancel with past effective date                                    | Boundary                    | BVA                      | High       | Standard       |
| AC 07.1–07.7  | Void order: LA deleted or reverted                                 | State transition            | State Transition Testing | Critical   | Deep           |
| AC 08.1–08.5  | Withdrawal: LA end date updated, student removed                   | State transition + Boundary | BVA + State Transition   | High       | Standard       |
| AC 09.1–09.5  | LOA: LA end date updated; resume creates new LA                    | State transition            | State Transition Testing | High       | Standard       |
| AC 10.7–10.8  | Require Allocation=False; Monthly product                          | Conditional                 | Decision Table           | Medium     | Smoke          |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area                                                   | Reason                                                                                                                                      | Recommended Approach                                                                                                      |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| AC 03.2 — Blocked past date < product start            | Data corruption risk: a wrongly-accepted invalid date would create an LA with incorrect start date, poisoning billing and lesson assignment | Negative Testing + BVA at exact boundary (date = product start - 1 day); assert error EN+JP message exactly               |
| AC 03.3 — Past date ≥ product start allowed (PBT-1859) | New behavior for Renseikai; incorrect LA start date silently corrupts lesson history                                                        | BVA: test at product start date (boundary), product start +1, and mid-past date; assert LA start = effective date exactly |
| AC 07.6 — Void add-course-past update order            | Must delete only the new course LA; if original LA is accidentally altered, student's lesson history is corrupted                           | Regression: verify original LA start/end/slot unchanged after void                                                        |

### 🟠 High Risk

| Area                                                | Reason                                                                                                                     | Recommended Approach                                                                                 |
| --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| AC 05.6 — Update slot past/today/future             | No explicit past-date variant tested; slot update with past effective date may behave differently in billing recalculation | Decision Table: 3 TCs (past / today / future) each verifying slot, session count, duration unchanged |
| AC 06.2/06.6 — Cancel Slot-Based/One-Time past date | TC 9922/9923 have no effective date; cancel with past date may leave orphaned LA if not handled                            | Negative path: cancel past date → assert LA deleted (not end-date updated)                           |
| AC 02.2 — Enrollment past start date                | TC 1807 only uses future date; past-path untested; enrollment is the primary LA creation trigger                           | Standard: create enrollment with past start; assert LA created with start = past date                |

### 🟡 Medium Risk

| Area                                 | Reason                                                                | Recommended Approach                                    |
| ------------------------------------ | --------------------------------------------------------------------- | ------------------------------------------------------- |
| AC 10.7 — Require Allocation = False | Existing TCs cover this but not in combination with slot update       | Decision Table coverage                                 |
| AC 10.8 — Monthly product no LA      | Specific to product type; easy to regress during new product type add | Smoke: create monthly order, assert no LA in Course tab |

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area                                          | Existing Test Case                | Overlap | New Coverage Needed            |
| ------------------------------------------------- | --------------------------------- | ------- | ------------------------------ |
| Add course — past date ≥ product start            | TC 1775 (future), TC 1776 (today) | Partial | ✅ TC A1: past date happy path |
| Add course — past date = product start (boundary) | None                              | None    | ✅ TC A2: boundary BVA         |
| Add course — past date < product start (blocked)  | None                              | None    | ✅ TC A3: negative/validation  |
| Void update that added course with past date      | TC 1799 (future only)             | Partial | ✅ TC A4: void past-date add   |
| Cancel Slot-Based with past date                  | TC 9922 (no date specified)       | Partial | ✅ TC B1                       |
| Cancel One-Time with past date                    | TC 9923 (no date specified)       | Partial | ✅ TC B2                       |
| Enrollment with past start date                   | TC 1807 (future only)             | Partial | ✅ TC C1                       |
| Update slot — past effective date                 | TC 1668/1672 (date unspecified)   | Partial | ✅ TC D1                       |
| Update slot — today effective date                | TC 1668/1672 (date unspecified)   | Partial | ✅ TC D2                       |
| Update slot — future effective date               | TC 1668/1672 (date unspecified)   | Partial | ✅ TC D3                       |

---

## 7. Suggested Test Suite Structure

```
output/test-cases/lesson-management/student-session/lesson-allocation/
├── PBT-1859-add-course-past-date.md   → AC 03.1–03.3, AC 03.6, AC 07.6 (Group A, TCs 1–4)
│                                         → maps to new Qase sub-suite under 280
└── PBT-1859-renseikai-past-date-gaps.md → AC 06.2+06.6, AC 02.2, AC 05.6 (Groups B/C/D, TCs 5–10)
                                           → maps to suite 280 directly
```
