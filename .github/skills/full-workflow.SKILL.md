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

### Step 1.1 — Fetch the Jira Ticket

1. Use `mcp_jira_jira_get_ticket` to fetch the full ticket by ID.
2. Read: title, description, all Acceptance Criteria, linked Confluence pages, Figma URLs, sub-tasks, and comments.
3. Extract: feature name, module, key terms, user stories (US XX), and AC IDs (AC XX.X).

### Step 1.2 — Read Related Confluence Pages

1. Identify Confluence links from the Jira ticket.
2. Use `mcp_confluence_confluence_get_page` or `mcp_confluence_confluence_search_pages` to read each page.
3. Extract: business context, constraints, architecture notes, role/permission rules.

### Step 1.3 — Extract Figma Design Details

1. Scan for a Figma URL in the ticket, Confluence pages, or comments.
2. **If no Figma link is found, skip this step silently.**
3. Extract: field names, labels, states (editable/locked/auto-calculated), error messages, role-specific UI differences.

### Step 1.4 — Fetch Existing Test Cases from Qase

If a Qase link was provided:

1. Parse the URL to extract the project code and suite ID.
2. Use `mcp_qase_list_cases` to retrieve existing test cases in that suite.
3. Note which ACs or business rules are already covered and which are gaps.

### Step 1.5 — Search Local Workspace

Search `input/specs/`, `output/test-cases/`, and `output/test-coverages/` using feature keywords to find:

- Existing specs that overlap with this ticket
- Existing test cases that may be impacted (regression risk)

### Step 1.6 — Extract Business Rules and Acceptance Criteria

Consolidate all information into a structured table:

```
| #  | AC      | Business Rule                          |
|----|---------|----------------------------------------|
| 1  | AC 01.1 | ...                                    |
```

### Step 1.7 — Formulate Clarification Questions

Check for: ambiguity, missing behavior, boundary conditions, error handling, role/permission gaps, cross-feature impact, data integrity, tenant-specific behavior.
Write all questions into the spec file — do NOT post them to Jira.

### Step 1.8 — Save the Spec File

Save to: `input/specs/<TICKET-ID>: <Feature Name>`

Use this structure:

```markdown
ID: <Jira URL>

## Summary

<2–3 sentence overview>

## Acceptance Criteria

<Full AC from Jira, preserving US and AC numbering>

## Business Rules (Extracted)

| #   | AC  | Business Rule |
| --- | --- | ------------- |

## Clarification Questions

1. ...

## Related Specs

- `input/specs/<file>` — <why related>

## Related Test Cases

- `output/test-cases/<path>` — <what's covered>

## QASE Coverage Gaps

- AC XX.X — <business rule with no test case yet>
```

**→ After saving the spec file, pause and ask:**

> "Phase 1 complete — spec saved to `input/specs/<TICKET-ID>: <Feature Name>`. Continue to Phase 2 (Define Test Coverage)?"

---

## PHASE 2 — Define Test Coverage

> Goal: Produce a structured test coverage matrix from the spec file.

### Step 2.1 — Read the Spec File

Read the full spec file from `input/specs/`. Extract: all US/AC IDs, Business Rules table, Jira ticket ID, and feature name.

### Step 2.2 — Read Existing Test Coverages and Test Cases

Search `output/test-coverages/` and `output/test-cases/` for related files.
Note which business rules are already covered and identify regression risk.

### Step 2.3 — Categorize Business Rules into Logic Types

For each business rule, assign one or more logic types:

| Logic Type           | When to use                                                             |
| -------------------- | ----------------------------------------------------------------------- |
| Validation logic     | Field is required, has format constraints, or fixed allowed values      |
| Boundary/range logic | Numeric or date value has min, max, or directional constraint           |
| Conditional logic    | Behavior changes based on a condition (e.g. `is_recurring = TRUE`)      |
| Recurrence logic     | Rule involves a recurring chain: creation, continuation, or propagation |
| State transition     | Entity moves between states or a dependent state changes                |
| Permission logic     | Rule differs per role (Admin, CM, Teacher, Student, Parent)             |
| Data integrity       | Prevents duplicate, conflict, or partial failure                        |
| Cross-system impact  | Change must be reflected on multiple surfaces (SF, BO, Calendar)        |

### Step 2.4 — Select Test Techniques

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

### Step 2.5 — Build the Coverage Strategy Table

```
| AC | Business Rule Summary | Logic Type | Test Technique | Risk Level | Coverage Depth |
```

Risk Level: Critical / High / Medium / Low
Coverage Depth: Deep / Standard / Smoke

### Step 2.6 — Identify High-Risk Areas

Group rules into: 🔴 Critical Risk / 🟠 High Risk / 🟡 Medium Risk. For each, state the risk reason and recommended testing approach.

### Step 2.7 — Map Coverage Gaps

```
| Gap Area | Existing Test Case | Overlap | New Coverage Needed |
```

### Step 2.8 — Propose Test Suite Structure

```
output/test-cases/lesson-management/lesson/<feature-folder>/
  ├── <file-1>.md   → AC XX.X — describe scope
  ├── <file-2>.md   → AC XX.X — describe scope
```

### Step 2.9 — Save the Coverage File

Save to: `output/test-coverages/<TICKET-ID>-<kebab-case-feature>.md`

**→ After saving the coverage file, pause and ask:**

> "Phase 2 complete — coverage saved to `output/test-coverages/<filename>`. Continue to Phase 3 (Generate Test Cases)?"

---

## PHASE 3 — Generate Test Cases

> Goal: Produce structured `.md` and `.csv` test case files from the coverage matrix.

### Step 3.1 — Read All Required Files

Read in parallel:

1. The coverage file — extract: Business Rules table, Coverage Strategy table, High-Risk Areas, Coverage Gaps, Suggested Suite Structure.
2. `input/templates/test-case-rules.md` — internalize all design rules before writing a single test case.
3. Existing test cases in the same feature folder — to avoid duplication.

### Step 3.2 — Apply Test Case Design Rules

**Title format:** `[Feature] – [Sub-feature] – [Component] – Condition – Expected Behavior`

**Forbidden title words:** Verify, Check, Test, Properly, Correctly, Successfully

**Rules:**

- One test case = one logical validation
- Avoid UI-only test cases
- OOP prefix: core tests → no prefix; tenant-specific → prefix with `[TenantName]`

### Step 3.3 — Generate Test Cases per AC

For each AC in the Coverage Strategy table:

1. Apply the technique pattern (EP / BVA / Decision Table / State Transition / CRUD / Permission Matrix / Regression / Negative Testing).
2. Apply Coverage Depth (Deep / Standard / Smoke).
3. Apply Risk Level (Critical/High → always add negative and boundary cases).
4. Skip rules already fully covered (Overlap = Full from Phase 2).

### Step 3.4 — Write Each Test Case

Each test case must include all fields:

| Field         | Rules                                                               |
| ------------- | ------------------------------------------------------------------- |
| Title         | Format: `[Feature] – [Sub-feature] – Condition – Expected Behavior` |
| Description   | Reference AC ID + technique + one-sentence summary                  |
| Preconditions | Bullet list with explicit test data values                          |
| Step Actions  | Numbered; one atomic action per step; present tense                 |
| Step Results  | One result per step; deterministic and observable                   |
| Steps Data    | One data entry per step; exact boundary values for BVA              |
| Severity      | Critical→critical, High→major, Medium→normal, Low→minor             |
| Priority      | Critical/High→high, Medium→medium, Low→low                          |

### Step 3.5 — Group into Suites and Save

Follow the Suggested Test Suite Structure from Phase 2.
Save `.md` files to `output/test-cases/<module>/<feature>/`.

Also produce a `.csv` companion file per the Qase CSV schema (matching `input/templates/qase-format.csv`).

Use this structure per `.md` file:

```markdown
# Test Cases: <TICKET-ID> — <Feature Name>

## Suite: <Suite Name>

### <Test Case Title>

**Description:** <AC ID> — <Technique> — <one-sentence summary>

**Preconditions:**

- <bullet list>

| #   | Action | Expected Result | Test Data |
| --- | ------ | --------------- | --------- |
| 1   | ...    | ...             | ...       |

**Severity:** <severity>
**Priority:** <priority>
```

**→ After saving test case files, pause and ask:**

> "Phase 3 complete — test cases saved to `output/test-cases/...`. Continue to Phase 4 (Import to Qase)?"

---

## PHASE 4 — Import to Qase

> Goal: Create suites and test cases in Qase; update the `.csv` with real suite IDs.

### Step 4.1 — Parse the Qase Project Code

Extract the project code from the Qase URL (e.g. `LM` from `https://app.qase.io/project/LM`).

### Step 4.2 — Read the Test Case File

Parse the `.md` or `.csv` file to extract suites and test cases with all fields.

### Step 4.3 — Fetch Existing Suites

Call `mcp_qase_list_suites` with the project code. Build a lookup map: `suite title → suite ID`. Paginate if needed.

### Step 4.4 — Resolve Suite Hierarchy

For each suite name:

- If exists → record real `suite_id`.
- If missing → create via `mcp_qase_create_suite` (create parent before child).

Build final map: `local suite name → real Qase suite_id`.

### Step 4.5 — Check for Duplicates

Before creating each test case, call `mcp_qase_list_cases` with the suite ID and title.
If a case with the same title already exists in the same suite → skip it and log `SKIP`.

### Step 4.6 — Import Test Cases

Call `mcp_qase_bulk_create_cases` per suite batch with these fixed values:

- `type`: `functional`
- `automation`: `is-not-automated`
- `status`: `draft`
- `steps_type`: `classic`

Record all returned case IDs.

### Step 4.7 — Update the CSV File

Replace all placeholder suite IDs in the `.csv` with real Qase suite IDs from Step 4.4. Save the updated file.

### Step 4.8 — Print Import Summary

```
## Import Summary

**Project:** <project code>
**File:** <file path>
**Date:** <today's date>

### Suites
| Suite Name | Status | Qase Suite ID |
|---|---|---|

### Test Cases
| Title | Suite | Status | Qase Case ID |
|---|---|---|---|

### Totals
- Suites created: X
- Suites already existed: X
- Test cases created: X
- Test cases skipped (duplicates): X
- Test cases failed: X
```

---

## Quality Checks (All Phases)

Before finishing the full pipeline, verify:

**Phase 1:**

- [ ] Spec file exists at `input/specs/<TICKET-ID>: <Feature Name>`
- [ ] Business Rules table is populated with AC IDs
- [ ] Clarification questions are written (not posted to Jira)

**Phase 2:**

- [ ] Coverage file exists at `output/test-coverages/<TICKET-ID>-<feature>.md`
- [ ] Every business rule has a logic type, technique, risk level, and coverage depth
- [ ] Suite structure is proposed

**Phase 3:**

- [ ] All `.md` test case files saved per the proposed suite structure
- [ ] All `.csv` companion files generated
- [ ] No forbidden title words used
- [ ] Each test case covers exactly one logical validation

**Phase 4:**

- [ ] All suites resolved to real Qase suite IDs (no placeholder integers remain)
- [ ] No duplicate test cases created per suite
- [ ] The companion `.csv` updated with real suite IDs
- [ ] Import summary printed with totals and any failures
