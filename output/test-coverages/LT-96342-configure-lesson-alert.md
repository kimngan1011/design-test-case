# Test Coverage: LT-96342 — [Renseikai] Configure Lesson Student Session Error Message Display

## Coverage Strategy Table

| #   | AC      | Business Rule Summary                                           | Logic Type                           | Test Technique                    | Risk Level | Coverage Depth |
| --- | ------- | --------------------------------------------------------------- | ------------------------------------ | --------------------------------- | ---------- | -------------- |
| 1   | AC 01.1 | Per-partner config flag for Out-of-Duration alert               | Permission logic / Conditional logic | Decision Table                    | High       | Standard       |
| 2   | AC 01.2 | Per-partner config flag for Classroom Capacity alert            | Permission logic / Conditional logic | Decision Table                    | High       | Standard       |
| 3   | AC 01.3 | Two config flags are independent                                | Conditional logic                    | Decision Table                    | Medium     | Standard       |
| 4   | AC 02.1 | SF: Out-of-Duration alert hidden when config = disabled         | Conditional logic                    | Decision Table + Negative Testing | Critical   | Deep           |
| 5   | AC 02.2 | SF: Out-of-Duration alert shown when config = enabled           | Conditional logic                    | Decision Table                    | Critical   | Deep           |
| 6   | AC 02.3 | Alert suppression applies for multiple out-of-duration students | Conditional logic                    | Equivalence Partitioning          | High       | Standard       |
| 7   | AC 03.1 | BO: Out-of-Duration alert hidden when config = disabled         | Conditional logic                    | Decision Table + Negative Testing | Critical   | Deep           |
| 8   | AC 03.2 | BO: Out-of-Duration alert shown when config = enabled           | Conditional logic                    | Decision Table                    | High       | Standard       |
| 9   | AC 04.1 | SF: Classroom Capacity alert hidden when config = disabled      | Conditional logic                    | Decision Table + Negative Testing | Critical   | Deep           |
| 10  | AC 04.2 | SF: Classroom Capacity alert shown when config = enabled        | Conditional logic                    | Decision Table                    | Critical   | Deep           |
| 11  | AC 05.1 | BO: Classroom Capacity alert hidden when config = disabled      | Conditional logic                    | Decision Table + Negative Testing | High       | Standard       |
| 12  | AC 05.2 | BO: Classroom Capacity alert shown when config = enabled        | Conditional logic                    | Decision Table                    | High       | Standard       |
| 13  | AC 06.1 | Default behavior: both alerts shown for unconfigured partners   | Regression Analysis                  | Regression Analysis               | Critical   | Smoke          |
| 14  | AC 06.2 | Alert config for one partner does not affect other partners     | Data integrity                       | Regression Analysis               | High       | Standard       |

---

## High-Risk Areas

### 🔴 Critical Risk

**Config = disabled → Alert is still shown (false positive)**

- ACs: 02.1, 03.1, 04.1, 05.1
- Risk: If the config flag is not correctly wired on SF or BO, staff at Renseikai will continue to see suppressed alerts, defeating the purpose of the feature.
- Approach: Deep Decision Table testing; explicitly test with realistic Renseikai data (student assigned to lesson outside their shorter-LA duration).

**Default behavior regression**

- AC: 06.1, 06.2
- Risk: Implementing per-partner config could accidentally suppress alerts for all partners if default value is misapplied.
- Approach: Smoke test with a non-Renseikai partner to confirm both alerts remain visible after the config is deployed.

### 🟠 High Risk

**Config independence (two flags independent)**

- AC: 01.3
- Risk: A bug could cause enabling one flag to silently affect the other.
- Approach: Test each combination — both enabled, both disabled, one enabled/one disabled (2×2 decision table).

**Alert suppression on both SF AND BO**

- ACs: 02.1 vs 03.1, 04.1 vs 05.1
- Risk: Config may touch only the SF layer and not BO (or vice versa), leaving one surface still showing the alert.
- Approach: Test both surfaces explicitly for each config state.

### 🟡 Medium Risk

**Multiple out-of-duration students**

- AC: 02.3
- Risk: If the suppression logic is per-student, it might suppress for some but not all.
- Approach: Equivalence Partitioning — test with 1 out-of-duration student and with 3 out-of-duration students.

---

## Coverage Gaps

| Gap Area                            | Existing Test Case | Overlap | New Coverage Needed        |
| ----------------------------------- | ------------------ | ------- | -------------------------- |
| SF Out-of-Duration alert display    | None               | None    | Full — AC 02.1, 02.2, 02.3 |
| BO Out-of-Duration alert display    | None               | None    | Full — AC 03.1, 03.2       |
| SF Classroom Capacity alert display | None               | None    | Full — AC 04.1, 04.2       |
| BO Classroom Capacity alert display | None               | None    | Full — AC 05.1, 05.2       |
| Partner-level config flag           | None               | None    | Full — AC 01.1–01.3        |
| Default behavior regression         | None               | None    | Smoke — AC 06.1, 06.2      |

---

## Proposed Test Suite Structure

```
output/test-cases/lesson-management/lesson/
└── configure-alert/
    └── LT-96342-configure-lesson-alert.md
    └── LT-96342-configure-lesson-alert.csv
```

### Suite breakdown (within the file)

| Suite                                   | Covers       | File                               |
| --------------------------------------- | ------------ | ---------------------------------- |
| Configure Alert – Partner Config Flag   | AC 01.1–01.3 | LT-96342-configure-lesson-alert.md |
| Configure Alert – SF Out of Duration    | AC 02.1–02.3 | LT-96342-configure-lesson-alert.md |
| Configure Alert – BO Out of Duration    | AC 03.1–03.2 | LT-96342-configure-lesson-alert.md |
| Configure Alert – SF Classroom Capacity | AC 04.1–04.2 | LT-96342-configure-lesson-alert.md |
| Configure Alert – BO Classroom Capacity | AC 05.1–05.2 | LT-96342-configure-lesson-alert.md |
| Configure Alert – Default Behavior      | AC 06.1–06.2 | LT-96342-configure-lesson-alert.md |
