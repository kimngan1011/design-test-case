---
name: define-test-coverage
description: >
  **WORKFLOW SKILL** — Define a structured test coverage matrix from a spec file.
  USE FOR: after analyzing requirements, before generating test cases; planning test strategy
  per AC; categorizing business rules into logic types; selecting test techniques; identifying
  high-risk areas and coverage gaps vs. existing test cases.
  INPUT: spec file path from `epics/<epic-folder>/spec.md`.
  OUTPUT: structured `.md` coverage file saved to `epics/<epic-folder>/test-coverage.md`.
  DO NOT USE FOR: generating test cases (use generate-test-cases skill) or analyzing a raw Jira
  ticket (use analyze-requirements skill).
---

# Skill: Define Test Coverage

Senior QA test architect producing a coverage strategy for one epic. Input is a populated `spec.md`; output is the epic's `test-coverage.md`.

## Input
- Spec file: `epics/<epic-folder>/spec.md` — must already contain extracted Business Rules and AC IDs (from analyze-requirements).

## References
- Logic types, test techniques, risk levels, coverage depths, quality checks → `.claude/references/coverage-rules.md`
- Mandatory edge-case checklist (Step 4.5, A–H.1) → `.claude/references/coverage-edge-case-checklist.md`
- Output Markdown template → `.claude/references/coverage-output-template.md`
- Epic folder layout + naming → `.claude/references/epic-folder-convention.md`

---

## Workflow

### Step 1 — Read the spec
Read `epics/<epic-folder>/spec.md`. Extract:
- All User Stories (US XX) and Acceptance Criteria (AC XX.X)
- The Business Rules (Extracted) table — each numbered rule, its AC, description
- Any clarification questions affecting scope
- Front-matter: `ticket_id`, `title`, `module`

### Step 2 — Scan existing coverage and test cases
- Existing coverage for this epic: `epics/<epic-folder>/test-coverage.md` (if any).
- Other epics in same module: `ls epics/` and scan related `test-coverage.md` to avoid duplicate strategy.
- For each existing test case found, note: which AC/rule it covers, whether impacted by the new feature (regression risk), what gaps remain.

### Step 3 — Categorize each business rule by logic type
Assign one or more logic types per rule using the table in `.claude/references/coverage-rules.md` § Logic Types (Validation, Boundary/range, Conditional, Recurrence, State transition, Permission, Data integrity, Cross-system, Display completeness, Ordering/Sort).

### Step 4 — Select test techniques per logic type
Use the technique mapping in `.claude/references/coverage-rules.md` § Test Techniques. Each logic type gets at least one primary technique; add secondaries when applicable.

### Step 4.5 — Run the Mandatory Edge-Case Patterns Checklist
Open `.claude/references/coverage-edge-case-checklist.md` and apply sections A–H.1 to every relevant rule:
- **A** Configuration-driven thresholds
- **B** Date / time logic (incl. timezone gaps)
- **C** Concurrent / stale state
- **D** Permission & role
- **E** State transition
- **F** Cross-system / cross-surface
- **G** Downstream effects (MANDATORY for every CRUD/state-change rule — fill Downstream Effects Inventory Table)
- **H** Display completeness & ordering (MANDATORY for every UI component — fill Display & Ordering Inventory Table)
- **H.1** Spec–Figma display mismatch (MANDATORY when spec has Figma URL — STOP and surface 🔴/🟡 rows for user resolution before proceeding)

Every "yes" answer must become a row in the Coverage Strategy table (Step 5) AND the gap analysis (Step 7). "N/A" requires a stated reason.

### Step 5 — Build the Coverage Strategy table

| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |

Risk levels (Critical/High/Medium/Low) and Coverage Depth (Deep/Standard/Smoke) definitions are in `.claude/references/coverage-rules.md`.

### Step 6 — Group high-risk areas
List 🔴 Critical, 🟠 High, 🟡 Medium rules. For each: state risk reason and recommended testing approach.

### Step 7 — Gap analysis vs. existing test cases

| Gap Area | Existing Test Case | Overlap | New Coverage Needed |

Mark uncovered rules with ✅ and describe what new TCs are needed.

### Step 8 — Propose test suite structure
Suggest file layout under the epic:
```
epics/<epic-folder>/test-cases/
├── <file-1>.md   → AC XX.X — what this file covers
├── <file-2>.md   → AC XX.X — what this file covers
```
Group logically related ACs into the same file. One area of behavior per file.

### Step 9 — Write the coverage file
Save to `epics/<epic-folder>/test-coverage.md` using the layout in `.claude/references/coverage-output-template.md`.

---

## Quality gate
Before finishing, run the full Quality Checks list in `.claude/references/coverage-rules.md`. Pay special attention to:
- Step 4.5 checklist filled for every applicable rule.
- Section G Downstream Effects table for every CRUD/state-change rule.
- Section H Display Inventory + H.1 Figma mismatch resolution for every UI component.
- No test cases generated — this skill only produces coverage strategy.

## Example invocation
```
Define test coverage for epics/LT-99999-feature-name
```
The skill reads `spec.md`, scans existing cases, categorizes rules, selects techniques, applies the edge-case checklist, builds the strategy, identifies gaps, and writes `test-coverage.md` in the same epic folder.
