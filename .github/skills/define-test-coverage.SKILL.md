---
description: >
  **WORKFLOW SKILL** — Define a structured test coverage matrix from a spec file.
  USE FOR: after analyzing requirements, before generating test cases; planning test strategy
  per AC; categorizing business rules into logic types; selecting test techniques; identifying
  high-risk areas and coverage gaps vs. existing test cases.
  INPUT: spec file path from `input/specs/`.
  OUTPUT: structured `.md` coverage file saved to `output/test-coverages/`.
  DO NOT USE FOR: generating test cases (use generate-testcases skill) or analyzing a raw Jira
  ticket (use analyze-requirements skill).
---

# Skill: Define Test Coverage

You are a senior QA test architect working on the Manabie lesson-management system.

---

## Input

- **Spec file** — path to an existing spec file in `input/specs/` (e.g. `input/specs/LT-99999: Feature Name`)
- The spec file must already contain extracted Business Rules and AC IDs (produced by the analyze-requirements skill)

---

## Workflow

### Step 1 — Read the Spec File

1. Read the full spec file from `input/specs/`.
2. Extract:
   - All **User Stories** (US XX) and **Acceptance Criteria** (AC XX.X)
   - The **Business Rules (Extracted)** table — each numbered rule, its AC, and its description
   - Any clarification questions that may affect test scope
   - The **Jira ticket ID** (for naming the output file)
   - The **feature name / module** (for naming the test suite)

---

### Step 2 — Read Existing Test Coverages and Test Cases

Search the local workspace for related coverage and test case files:

1. **Search `output/test-coverages/`** — check if a prior coverage for this feature or module already exists; note which business rules are already categorized.
2. **Search `output/test-cases/`** — scan for existing test case files in the same module folder (e.g. `lesson-management/lesson/`); read their titles to understand what is already covered.

For each existing test case found, note:

- Which AC or business rule it corresponds to
- Whether it will be **impacted** by the new feature (regression risk)
- Which gaps remain (new rules with no existing test case)

---

### Step 3 — Categorize Business Rules into Logic Types

For **each business rule** from the spec, assign one or more logic types:

| Logic Type               | When to use                                                                                    |
| ------------------------ | ---------------------------------------------------------------------------------------------- |
| **Validation logic**     | Field is required, has format constraints, or has a fixed set of allowed values                |
| **Boundary/range logic** | A numeric or date value has a min, max, or directional constraint (extend-only, increase-only) |
| **Conditional logic**    | Behavior changes based on a condition (e.g. `is_recurring = TRUE`, role = Admin)               |
| **Recurrence logic**     | Rule involves a recurring chain: creation, continuation, or propagation across lessons         |
| **State transition**     | Entity moves between states (Draft → Published → Cancelled) or a dependent state changes       |
| **Permission logic**     | Rule differs per role (Admin, CM, Teacher, Student, Parent)                                    |
| **Data integrity**       | Rule prevents duplicate, conflict, or partial failure; or ensures referential consistency      |
| **Cross-system impact**  | Change must be reflected on multiple surfaces (SF, BO, Calendar, Reports)                      |

---

### Step 4 — Select Test Techniques per Logic Type

For each logic type assigned, select one or more techniques:

| Logic Type           | Primary Techniques       | Secondary Techniques                |
| -------------------- | ------------------------ | ----------------------------------- |
| Validation logic     | Equivalence Partitioning | Negative Testing                    |
| Boundary/range logic | Boundary Value Analysis  | Negative Testing                    |
| Conditional logic    | Decision Table           | Negative Testing                    |
| Recurrence logic     | State Transition Testing | Regression Analysis                 |
| State transition     | State Transition Testing | CRUD Testing                        |
| Permission logic     | Permission Matrix        | Decision Table                      |
| Data integrity       | CRUD Testing             | Regression Analysis, Decision Table |
| Cross-system impact  | Regression Analysis      | CRUD Testing                        |

**Technique guidance:**

- **Equivalence Partitioning** — group valid/invalid inputs; one test per partition
- **Boundary Value Analysis** — test at exact boundary, one below, one above
- **Decision Table** — map all meaningful input combinations to expected outcomes
- **State Transition Testing** — trace valid and invalid state transitions; include guards
- **Pairwise Testing** — use when 3+ independent variables interact; reduce combinations intelligently
- **CRUD Testing** — verify Create, Read, Update, Delete paths for the entity
- **Permission Matrix** — one row per role, one column per action; mark allowed/denied
- **Regression Analysis** — identify existing test cases at risk from this change
- **Negative Testing** — attempt invalid inputs, blocked actions, or edge error states

---

### Step 5 — Build the Coverage Strategy Table

Produce a structured table with one row per AC (or sub-rule when a single AC has multiple distinct behaviors):

```
| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
```

**Risk Level definitions:**

| Level        | Criteria                                                                         |
| ------------ | -------------------------------------------------------------------------------- |
| **Critical** | Failure causes data corruption, billing error, or user-facing data loss          |
| **High**     | Failure causes incorrect system behavior visible to users or affecting reporting |
| **Medium**   | Failure causes display inconsistency or minor incorrect behavior                 |
| **Low**      | Cosmetic or non-blocking issue                                                   |

**Coverage Depth definitions:**

| Depth        | Meaning                                                                        |
| ------------ | ------------------------------------------------------------------------------ |
| **Deep**     | BVA at all boundaries, multiple input combinations, cross-surface verification |
| **Standard** | Happy path + one or two negative cases                                         |
| **Smoke**    | Only the primary happy path                                                    |

---

### Step 6 — Identify High-Risk Areas

Group high-risk rules into three tiers and explain why they need deeper testing:

**🔴 Critical Risk** — rules where failure causes data corruption, billing impact, or silent data loss.
For each: state the risk reason and the recommended testing approach.

**🟠 High Risk** — rules where failure causes visible incorrect behavior or regression.
For each: state the risk reason and the recommended testing approach.

**🟡 Medium Risk** — rules involving tenant-specific behavior, edge cases, or UI accuracy.
For each: state the risk reason and the recommended testing approach.

---

### Step 7 — Map Coverage Gaps vs. Existing Test Cases

Produce a gap analysis table:

```
| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
```

- **Gap Area** — the business rule or AC that needs coverage
- **Existing Test Case** — any TC number or file that partially covers it (from Step 2)
- **Overlap** — describe what is already covered (Partial / Full / None)
- **New Coverage Needed** — ✅ mark with description of what new test cases are needed

---

### Step 8 — Propose Test Suite Structure

Suggest a folder and file layout for the test cases that will be generated next:

```
output/test-cases/lesson-management/lesson/<feature-folder>/
  ├── <file-1>.md   → AC XX.X — describe what this file covers
  ├── <file-2>.md   → AC XX.X — describe what this file covers
```

Group logically related ACs into the same file. Keep each file scoped to one area of behavior.

---

### Step 9 — Create the Coverage File

Save the output `.md` file at:

```
output/test-coverages/<TICKET-ID>-<kebab-case-feature-name>.md
```

> Example: `output/test-coverages/LT-90573-extend-recurring-lesson.md`

Use this exact structure:

```markdown
# Test Coverage: <TICKET-ID> — <Feature Name>

**Jira:** <Jira URL>
**Date:** <today's date>

---

## 1. Business Rules Extracted

| #   | AC      | Business Rule |
| --- | ------- | ------------- |
| 1   | AC XX.X | ...           |

---

## 2. Logic Type Categorization

| AC      | Business Rule # | Logic Type |
| ------- | --------------- | ---------- |
| AC XX.X | 1, 2            | ...        |

---

## 3. Test Technique Selection

| Logic Type | Applicable Techniques |
| ---------- | --------------------- |
| ...        | ...                   |

---

## 4. Structured Coverage Strategy

| AC  | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
| --- | --------------------- | ---------- | -------------- | ---------- | -------------- |
| ... | ...                   | ...        | ...            | ...        | ...            |

---

## 5. High-Risk Areas Requiring Deeper Testing

### 🔴 Critical Risk

| Area | Reason | Recommended Approach |
| ---- | ------ | -------------------- |

### 🟠 High Risk

| Area | Reason | Recommended Approach |
| ---- | ------ | -------------------- |

### 🟡 Medium Risk

| Area | Reason | Recommended Approach |
| ---- | ------ | -------------------- |

---

## 6. Coverage Gaps vs. Existing Test Cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
| -------- | ------------------ | ------- | ------------------- |

---

## 7. Suggested Test Suite Structure

\`\`\`
output/test-cases/<module>/<feature>/
├── <file>.md → AC XX.X — <description>
\`\`\`
```

---

## Quality Checks

Before finishing, verify:

- [ ] Every business rule from the spec has a logic type assigned
- [ ] Every logic type has at least one test technique assigned
- [ ] Every AC has a row in the Coverage Strategy table with Risk Level and Coverage Depth
- [ ] At least one Critical or High risk area is identified and explained (if the feature has state changes, data writes, or cross-system sync)
- [ ] The gap table lists all business rules with no existing test case marked ✅ as needing new TCs
- [ ] The suggested test suite structure groups related ACs logically
- [ ] Output file is saved to `output/test-coverages/` with the correct naming convention
- [ ] No test cases are generated — this skill only produces the coverage strategy

---

## Example Invocation

```
Define test coverage for input/specs/LT-99999: Feature Name
```

The skill will read the spec, scan existing test cases, categorize all business rules by logic type,
select test techniques, produce a risk-tiered coverage strategy, identify gaps, and save the result
to `output/test-coverages/LT-99999-feature-name.md`.
