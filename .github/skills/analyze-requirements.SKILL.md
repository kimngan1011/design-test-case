---
description: >
  **WORKFLOW SKILL** — Analyze requirements from a Jira ticket to produce a structured spec file.
  USE FOR: onboarding a new ticket, analyzing feature requirements, formulating clarification
  questions, discovering scope from Jira + Confluence + Figma.
  INPUT: Jira ticket ID or URL + optional QASE link.
  OUTPUT: structured `.md` spec file saved to `input/specs/`.
  DO NOT USE FOR: generating test cases (use generate-testcases skill) or creating test coverage (use test-coverage template).
---

# Skill: Analyze Requirements

You are a senior QA analyst and test architect working on the Manabie lesson-management system.

---

## Input

- **Jira ticket** — URL or ID (e.g. `LT-12345` or `https://manabie.atlassian.net/browse/LT-12345`)
- **QASE link** — optional, URL or project/suite reference to the existing QASE test suite

---

## Workflow

### Step 1 — Fetch the Jira Ticket

1. Use the **Jira MCP** tool (`mcp_jira_jira_get_ticket`) to fetch the full ticket by ID.
2. Read:
   - Title and description
   - All Acceptance Criteria sections
   - Linked Confluence pages, Figma URLs, and sub-tasks
   - Comments (for any clarifications or decisions already made)
3. Extract:
   - **Feature name** and **module** (e.g. `Lesson Schedule`, `Recurring Lesson`)
   - **Key terms** and **field names** to use as search keywords in later steps
   - **User stories** (US XX) and **AC IDs** (AC XX.X)

---

### Step 2 — Read Related Confluence Pages

1. Identify Confluence page links from the Jira ticket description or "Web links" section.
2. Use **Confluence MCP** (`mcp_confluence_confluence_get_page` or `mcp_confluence_confluence_search_pages`) to read each relevant page.
3. If no direct links exist, search Confluence using feature keywords extracted in Step 1.
4. Extract:
   - Additional business context or background
   - Constraints not mentioned in the Jira ticket
   - Architecture or data model notes
   - Role/permission rules

---

### Step 3 — Extract Figma Design Details

1. Scan the Jira ticket description, Confluence pages, and comments for a Figma URL.
2. **If no Figma link is found, skip this step silently and continue to Step 4.**
3. If a Figma link is present, use the **Figma MCP** tool to read the linked design node.
4. Extract:
   - UI field names, labels, and placeholders
   - Field states: editable / locked / auto-calculated / optional / required
   - Error messages and validation text
   - Empty states, loading states, and confirmation dialogs
   - Role-specific UI differences (if applicable)
5. Cross-reference Figma field behaviors with the AC to identify discrepancies.

---

### Step 4 — Fetch Existing Test Cases from QASE

If a QASE link was provided as input:

1. Parse the QASE URL to identify the **project code** and **suite ID** (or test run ID).
2. Use **QASE MCP** (`mcp_qase_list_cases`) with the project code and suite ID to retrieve all existing test cases in that suite.
3. For each test case, note:
   - Which AC or feature area it covers (based on title and description)
   - Which scenarios are already tested
   - Which business rules from Step 5 already have coverage
   - Gaps: business rules with no corresponding test case

If no QASE link was provided, skip this step silently.

---

### Step 5 — Search Local Workspace for Related Specs and Test Cases

Use keywords from Step 1 (feature name, module, field names) to search locally:

1. **Search `input/specs/`** — look for any existing spec files mentioning the same feature or module.
2. **Search `output/test-cases/`** — find existing test cases that may overlap with or be impacted by this ticket.
3. **Search `output/test-coverages/`** — check if a coverage matrix already exists for this feature.

For each match, note:

- Which ACs or business rules are already covered
- Which scenarios may be **impacted** by this new feature (regression risk)
- Which edge cases are already tested vs. missing

---

### Step 6 — Extract Business Rules and Acceptance Criteria

Consolidate all information from Steps 1–4 into a structured list:

**For each AC**, extract:

- The explicit rule stated in the AC
- Field behavior: editable / locked / auto-filled / optional
- Role/permission constraints
- Conditional logic (e.g. "only if `is_recurring = TRUE`")
- Default values and auto-calculation logic
- Conflict handling (e.g. "lesson not created if date already exists")
- Cross-system / integration impact (e.g. "reflected on SF Calendar, BO detail")

Format: numbered list grouped by AC ID, e.g.:

```
| #  | AC    | Business Rule                          |
|----|-------|----------------------------------------|
| 1  | AC 01.1 | Button only visible when is_recurring = TRUE |
| 2  | AC 01.2 | Date field auto-filled: last end date + 7 days |
```

---

### Step 7 — Formulate Clarification Questions

Based on the extracted business rules, compare against the Figma design, Confluence pages, existing test cases (QASE + local), to identify gaps:

**Categories to check:**

| Category                       | Questions to ask                                                   |
| ------------------------------ | ------------------------------------------------------------------ |
| **Ambiguity**                  | Is this rule clearly defined? Does it contradict another AC?       |
| **Missing behavior**           | What happens when the field is empty / null / zero?                |
| **Boundary conditions**        | What is the exact min/max value? What happens at the limit?        |
| **Error handling**             | What error message is shown? Can the user retry?                   |
| **Role/permission gaps**       | Is this behavior the same for all roles? What about edge roles?    |
| **Cross-feature impact**       | Does this interact with feature X? Which existing tests may break? |
| **Data integrity**             | What if the operation partially fails? Is it atomic?               |
| **Nichibei / tenant-specific** | Does this feature behave differently per tenant/org?               |

Write all questions directly into the spec file under `## Clarification Questions`. Do **not** post them to Jira or any external tool.

---

### Step 8 — Create the Spec File

Save a new `.md` file at:

```
input/specs/<TICKET-ID>: <Feature Name>
```

> Example: `input/specs/LT-90573: Extend Recurring Lesson settings`

Use this structure:

```markdown
ID: <Jira URL>

## Summary

<2–3 sentence overview of the feature and its purpose>

## Acceptance Criteria

<Paste the full AC from the Jira ticket, preserving US and AC numbering.
Include tables for field behaviors where applicable.>

## Business Rules (Extracted)

| #   | AC      | Business Rule |
| --- | ------- | ------------- |
| 1   | AC XX.X | ...           |

## Clarification Questions

1. <Question about ambiguity or missing behavior>
2. <Question about boundary condition>
3. ...

## Related Specs

- `input/specs/<related spec filename>` — <why it's related>

## Related Test Cases

- `output/test-cases/<path>` — <what's already covered that may be impacted>

## QASE Coverage Gaps

<!-- List business rules from the table above that have no existing QASE test case -->

- AC XX.X — <business rule with no test case yet>
```

---

## Quality Checks

Before finishing, verify:

- [ ] All User Stories and AC sections from the Jira ticket are captured
- [ ] Figma field states cross-referenced with AC (skipped silently if no Figma link found)
- [ ] QASE existing test cases fetched and coverage gaps identified (skipped silently if no QASE link provided)
- [ ] At least one clarification question for each AC that has ambiguous or undefined behavior
- [ ] Clarification questions are written to the spec file only — not posted to Jira
- [ ] Existing local test cases that may be impacted by this change are listed
- [ ] Spec file is saved to `input/specs/` with the format `<TICKET-ID>: <Feature Name>`
- [ ] No test cases are generated — this skill only analyzes and documents requirements

---

## Example Invocation

```
Analyze requirements for ticket LT-99999.
QASE: https://app.qase.io/project/LM?suite=42
```

The skill will fetch the Jira ticket, find related Confluence pages and Figma links, search
existing specs and test cases, extract all business rules, formulate clarification questions,
and save a structured spec to `input/specs/LT-99999: <Feature Name>`.
