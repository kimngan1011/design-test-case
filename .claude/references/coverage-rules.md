# Coverage Rules — Logic Types, Techniques, Risk, Quality

Reference for `define-test-coverage` skill. Used in Steps 3, 4, 5, and Quality Checks.

For the mandatory edge-case checklist (Step 4.5), see `.claude/references/coverage-edge-case-checklist.md`.

---

## Logic Types (Step 3)

| Logic Type | When to use |
|---|---|
| **Validation logic** | Field is required, has format constraints, or fixed set of allowed values. |
| **Boundary/range logic** | Numeric/date with min, max, or directional constraint (extend-only, increase-only). |
| **Conditional logic** | Behavior changes based on condition (`is_recurring = TRUE`, role = Admin). |
| **Recurrence logic** | Recurring chain: creation, continuation, propagation across lessons. |
| **State transition** | Entity moves between states (Draft → Published → Cancelled). |
| **Permission logic** | Rule differs per role (Admin, CM, Teacher, Student, Parent). |
| **Data integrity** | Prevents duplicate/conflict/partial failure; ensures referential consistency. |
| **Cross-system impact** | Change must appear on multiple surfaces (SF, BO, Calendar, Reports). |
| **Display completeness** | A UI screen/card/list must show a defined set of required fields. |
| **Ordering / Sort** | Items must appear in a specific sequence; a tiebreaker rule exists. |

---

## Test Techniques (Step 4)

| Logic Type | Primary | Secondary |
|---|---|---|
| Validation | Equivalence Partitioning | Negative |
| Boundary/range | Boundary Value Analysis | Negative |
| Conditional | Decision Table | Negative |
| Recurrence | State Transition | Regression |
| State transition | State Transition | CRUD |
| Permission | Permission Matrix | Decision Table |
| Data integrity | CRUD | Regression, Decision Table |
| Cross-system | Regression | CRUD |
| Display completeness | Component | Negative (field absent) |
| Ordering / Sort | Scenario | Pairwise (multi-criteria) |

**Guidance:**
- **Equivalence Partitioning** — group valid/invalid inputs; one test per partition.
- **Boundary Value Analysis** — exact boundary, one below, one above.
- **Decision Table** — map meaningful input combinations to outcomes.
- **State Transition** — trace valid + invalid transitions; include guards.
- **Pairwise** — when 3+ independent variables interact.
- **CRUD** — verify Create, Read, Update, Delete paths.
- **Permission Matrix** — one row per role, one column per action.
- **Regression** — identify existing TCs at risk from this change.
- **Negative** — invalid inputs, blocked actions, edge errors.
- **Component** — enumerate every required field; one TC asserts all together.
- **Scenario** — 2+ items differing on sort criteria; assert order explicitly.

---

## Risk Levels (Step 5)

| Level | Criteria |
|---|---|
| **Critical** | Failure causes data corruption, billing error, or user-facing data loss. |
| **High** | Failure causes incorrect system behavior visible to users or affecting reporting. |
| **Medium** | Failure causes display inconsistency or minor incorrect behavior. |
| **Low** | Cosmetic or non-blocking. |

## Coverage Depths (Step 5)

| Depth | Meaning |
|---|---|
| **Deep** | BVA at all boundaries, multiple input combinations, cross-surface verification. |
| **Standard** | Happy path + one or two negative cases. |
| **Smoke** | Primary happy path only. |

---

## Quality Checks (apply before finishing)

- Every business rule has a logic type assigned.
- Every logic type has at least one test technique assigned.
- Every item in `.claude/references/coverage-edge-case-checklist.md` is filled for applicable rules, with "N/A + reason" otherwise.
- Every "yes" in the edge-case checklist appears in the Coverage Strategy table AND in the gap analysis.
- Section G Downstream Effects table filled for every CRUD/state-change rule; primary entity verification is NOT enough — every counter, child record, staff/peer surface, continuation flow, and idempotency has its own TC row.
- Inverse-action rule: every "+1/create" has a matching "−1/delete" on the inverse.
- Every AC has a row in Coverage Strategy with Risk Level and Coverage Depth.
- At least one Critical/High risk area identified (if feature has state changes, data writes, or cross-system sync).
- Gap table marks every uncovered rule with ✅.
- Suggested test suite structure groups related ACs logically.
- Output saved to correct path with correct naming.
- No test cases generated — this skill only produces coverage strategy.
