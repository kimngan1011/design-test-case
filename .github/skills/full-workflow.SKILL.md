---
description: >
  **WORKFLOW SKILL** — End-to-end QA workflow: from a Jira ticket to test cases imported into Qase.
  USE FOR: running the full pipeline in one command — analyze requirements, define test coverage,
  generate test cases, and import to Qase.
  INPUT: Jira ticket ID or URL + optional Qase project URL.
  OUTPUT: spec file in `input/specs/`, coverage file in `output/test-coverages/`,
  test case files in `output/test-cases/`, and all test cases imported into Qase.
  DO NOT USE FOR: running only one phase of the pipeline (use the individual skills instead).
---

# Skill: Full QA Workflow (End-to-End)

You are a senior QA analyst and test architect working on the Manabie lesson-management system.
This skill orchestrates the complete pipeline from a Jira ticket to test cases imported into Qase.

---

## Input

- **Jira ticket** — URL or ID (e.g. `LT-12345` or `https://manabie.atlassian.net/browse/LT-12345`)
- **Qase project link** — optional, URL or project code (e.g. `https://app.qase.io/project/LM` or `LM`)

---

## Pipeline Overview

```
[Jira Ticket]
      ↓
  PHASE 1: Analyze Requirements
      ↓ produces → input/specs/<TICKET-ID>: <Feature Name>
  PHASE 2: Define Test Coverage
      ↓ produces → output/test-coverages/<TICKET-ID>-<feature>.md
  PHASE 3: Generate Test Cases
      ↓ produces → output/test-cases/.../<filename>.md + .csv
  PHASE 4: Import to Qase
      ↓ produces → test cases in Qase + updated .csv with real suite IDs
```

After each phase, pause and ask the user:

> "Phase X is complete. Do you want to continue to Phase Y, or stop here to review?"

Only proceed to the next phase after explicit confirmation.

---

## PHASE 1 — Analyze Requirements

> Goal: Produce a structured spec file from the Jira ticket.

**Read and follow the full instructions in `.github/skills/analyze-requirements.SKILL.md`.**

Pass these inputs to the skill:

- **Jira ticket** — the ticket ID or URL provided by the user
- **QASE link** — the Qase project link provided by the user (if any)

Execute all steps defined in that skill file (Steps 1–9), including:

- Fetching the Jira ticket, Confluence pages, and Figma designs
- Searching the local workspace for related specs and test cases
- Performing the full **Conflict & Gap Analysis** (Step 5b)
- Extracting business rules and formulating clarification questions
- Saving the spec file to `input/specs/<TICKET-ID>: <Feature Name>`
- Presenting clarification questions for user review before posting to Jira (Step 9)

**→ After completing Phase 1, pause and ask:**

> "Phase 1 complete — spec saved to `input/specs/<TICKET-ID>: <Feature Name>`. Continue to Phase 2 (Define Test Coverage)?"

---

## PHASE 2 — Define Test Coverage

> Goal: Produce a structured test coverage matrix from the spec file.

**Read and follow the full instructions in `.github/skills/define-test-coverage.SKILL.md`.**

Pass this input to the skill:

- **Spec file** — the spec file path produced by Phase 1 (e.g. `input/specs/LT-12345: Feature Name`)

Execute all steps defined in that skill file (Steps 1–9), including:

- Reading the spec file and existing test coverages/cases
- Categorizing business rules into logic types
- Selecting test techniques per logic type
- Building the coverage strategy table with risk levels and coverage depth
- Identifying high-risk areas (Critical / High / Medium tiers)
- Mapping coverage gaps vs. existing test cases
- Proposing the test suite structure
- Saving the coverage file to `output/test-coverages/<TICKET-ID>-<feature>.md`

**→ After completing Phase 2, pause and ask:**

> "Phase 2 complete — coverage saved to `output/test-coverages/<filename>`. Continue to Phase 3 (Generate Test Cases)?"

---

## PHASE 3 — Generate Test Cases

> Goal: Produce structured `.md` and `.csv` test case files from the coverage matrix.

**Read and follow the full instructions in `.github/skills/generate-test-cases.SKILL.md`.**

Pass this input to the skill:

- **Coverage file** — the coverage file path produced by Phase 2 (e.g. `output/test-coverages/LT-12345-feature-name.md`)

Execute all steps defined in that skill file (Steps 1–7), including:

- Reading the coverage file, `input/templates/test-case-rules.md`, and existing test cases
- Applying test case design rules (title format, forbidden words, one-TC-per-rule)
- Generating test cases per AC using the correct technique pattern and coverage depth
- Writing each test case with all required fields (title, description, preconditions, steps, severity, priority)
- Grouping test cases into suites per the proposed structure
- Saving both `.md` and `.csv` files to `output/test-cases/<module>/<feature>/`

**→ After completing Phase 3, pause and ask:**

> "Phase 3 complete — test cases saved to `output/test-cases/...`. Continue to Phase 4 (Import to Qase)?"

---

## PHASE 4 — Import to Qase

> Goal: Create suites and test cases in Qase; update the `.csv` with real suite IDs.

**Read and follow the full instructions in `.github/skills/import-to-qase.SKILL.md`.**

Pass these inputs to the skill:

- **Qase link** — the project URL or code provided by the user (e.g. `https://app.qase.io/project/LM` or `LM`)
- **Test case file** — the `.md` or `.csv` file produced by Phase 3

Execute all steps defined in that skill file (Steps 1–9), including:

- Parsing the Qase project code
- Reading and parsing the test case file
- Fetching existing suites from Qase and resolving the suite hierarchy
- Checking for duplicate test cases before creating
- Importing test cases via `mcp_qase_bulk_create_cases`
- Updating the `.csv` file with real Qase suite IDs
- Printing the import summary with totals

---

## Quality Checks (All Phases)

Each phase's individual skill file contains its own detailed quality checks. After completing the full pipeline, verify these top-level checks:

**Phase 1 (see `analyze-requirements.SKILL.md` for full checklist):**

- [ ] Spec file exists at `input/specs/<TICKET-ID>: <Feature Name>`
- [ ] Business Rules table is populated with AC IDs
- [ ] Conflict & Gap Analysis (Step 5b) was performed
- [ ] Clarification questions presented to user for review before any Jira action

**Phase 2 (see `define-test-coverage.SKILL.md` for full checklist):**

- [ ] Coverage file exists at `output/test-coverages/<TICKET-ID>-<feature>.md`
- [ ] Every business rule has a logic type, technique, risk level, and coverage depth
- [ ] High-risk areas identified with recommended approach
- [ ] Suite structure is proposed

**Phase 3 (see `generate-test-cases.SKILL.md` for full checklist):**

- [ ] All `.md` test case files saved per the proposed suite structure
- [ ] All `.csv` companion files generated
- [ ] No forbidden title words used
- [ ] Each test case covers exactly one logical validation
- [ ] Every step has a deterministic expected result

**Phase 4 (see `import-to-qase.SKILL.md` for full checklist):**

- [ ] All suites resolved to real Qase suite IDs (no placeholder integers remain)
- [ ] No duplicate test cases created per suite
- [ ] The companion `.csv` updated with real suite IDs
- [ ] Import summary printed with totals and any failures
