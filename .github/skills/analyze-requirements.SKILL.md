---
description: >
  **WORKFLOW SKILL** — Analyze a Jira ticket to produce a structured spec file with conflict
  detection, gap analysis, and clarification questions.
  USE FOR: onboarding a new ticket, analyzing feature requirements, detecting mismatches with
  existing specs/tests, formulating clarification questions.
  INPUT: Jira ticket ID or URL + optional QASE suite link.
  OUTPUT: `.md` spec file saved to `input/specs/`.
  DO NOT USE FOR: generating test cases (use generate-testcases skill).
---

# Skill: Analyze Requirements

You are a senior QA analyst and test architect working on the Manabie lesson-management system.

> **General rule:** If a step's input is absent (no Figma link, no QASE link, no local matches),
> skip that step silently and continue — never ask the user about missing optional inputs.

---

## Global Sources of Truth

Fetch these **only with explicit user approval** (see Step 0). Never auto-fetch.

| #   | Source                                                                                                | Type       | Description                                |
| --- | ----------------------------------------------------------------------------------------------------- | ---------- | ------------------------------------------ |
| 1   | [Scheduling — Confluence](https://manabie.atlassian.net/wiki/spaces/PRDM/pages/1046151229/Scheduling) | Confluence | System-wide scheduling business rules      |
| 2   | [PX Suite 18 — Qase](https://app.qase.io/project/PX?previewMode=side&suite=18)                        | Qase suite | Authoritative test coverage for PX project |

---

## Workflow

### Step 0 — Permission to Fetch Global Sources

Ask the user once:

> "I can fetch the **Scheduling Confluence page** and/or **PX Suite 18 (Qase)** for deeper context.
> This costs extra time and tokens. Should I read them? (both / confluence only / qase only / no)"

Wait for the response before continuing.

- **Approved sources** are fetched in their respective steps (Confluence → Step 2, Qase → Step 4) and cross-referenced in Step 5b.
- **Declined or no response** → skip both and proceed.

---

### Step 1 — Fetch the Jira Ticket

Use `mcp_jira_jira_get_ticket`. Read:

- Title, description, all Acceptance Criteria
- Linked Confluence pages, Figma URLs, sub-tasks, comments

Extract:

- **Feature name** and **module** (e.g. `Lesson Schedule`, `Recurring Lesson`)
- **Key terms** and **field names** for searching in later steps
- **User story IDs** (US XX) and **AC IDs** (AC XX.X)

---

### Step 2 — Read Related Confluence Pages

1. Use links from the Jira ticket, or search Confluence with feature keywords if no links exist.
2. Use `mcp_confluence_confluence_get_page` or `mcp_confluence_confluence_search_pages`.
3. Extract: business context, constraints, architecture notes, role/permission rules.
4. If the Scheduling Confluence page was approved in Step 0, fetch it here and incorporate its business rules into Step 5b.

---

### Step 3 — Extract Figma Design Details

1. Scan the Jira ticket, Confluence pages, and comments for a Figma URL.
2. Use the Figma MCP tool to read the linked design node.
3. Extract:
   - Field names, labels, placeholders
   - Field states: editable / locked / auto-calculated / optional / required
   - Error messages, empty/loading states, confirmation dialogs
   - Role-specific UI differences
4. Cross-reference Figma behaviors against the AC; flag discrepancies as `[UNDOCUMENTED IN AC]`.

---

### Step 4 — Fetch Existing QASE Test Cases

Parse the QASE URL to get the **project code** and **parent suite ID**, then:

1. **Discover all descendant suites:**
   - Call `mcp_qase_list_suites(code=<PROJECT>, limit=100, offset=0)`.
   - Paginate until all suites are loaded. Collect suites whose `parent_id` matches the given suite, then recurse depth-first.

2. **Fetch test cases from every suite:**
   - Call `mcp_qase_list_cases(code=<PROJECT>, suite_id=<ID>, limit=100, offset=0)` for each suite.
   - Paginate if a suite returns exactly 100 cases.

3. For each test case, note: which AC or feature area it covers, and which business rules already have coverage.

If PX Suite 18 was approved in Step 0, merge its cases into this step's result set.

---

### Step 5 — Search Local Workspace

Use feature keywords from Step 1 to search:

- `input/specs/` — existing spec files for the same feature or module
- `output/test-cases/` — test cases that may overlap or be impacted
- `output/test-coverages/` — existing coverage matrices

**Read the full content** of every match — you need actual business rules and assertions for Step 5b.

---

### Step 5b — Conflict & Gap Analysis

Perform this step for every file found in Step 5. Do not skip.

#### Finding Tags

| Tag                    | Meaning                                                                 |
| ---------------------- | ----------------------------------------------------------------------- |
| `[CONFLICT]`           | New rule directly contradicts an existing spec or test assertion        |
| `[REGRESSION RISK]`    | New behavior may break an existing test without contradicting the spec  |
| `[EXTENDED]`           | New rule adds to existing behavior without contradiction                |
| `[REPLACED]`           | New rule fully supersedes an existing rule (cite the old rule)          |
| `[UNDOCUMENTED IN AC]` | Figma or Confluence shows a behavior absent from any AC                 |
| `[MISSING BEHAVIOR]`   | An existing system scenario has no new AC rule                          |
| `[ROLE GAP]`           | A role interacts with the feature but has no defined behavior in the AC |

#### Checks to Perform

1. **Business Rule Delta** — For each business rule extracted in Step 6, check every related spec and test case: does any define the same field or flow with different behavior? Classify using the tags above.

2. **Implicit Dependencies** — Does any new rule assume a precondition set by another feature? Is there an undocumented data dependency?

3. **Role & Permission Coverage** — List all roles from AC, Confluence, and Figma. Flag any role whose behavior is undefined as `[ROLE GAP]`.

4. **Edge Case & Boundary Delta** — Are there boundary conditions, error scenarios, or null/empty states in existing tests that the new AC ignores or may change?

#### Output: Findings Table

```
| # | Tag                  | Source                        | AC      | Description                                       |
|---|----------------------|-------------------------------|---------|---------------------------------------------------|
| 1 | [CONFLICT]           | input/specs/LT-XXXXX, line 42 | AC 01.2 | New: date auto-filled. Existing: always editable  |
| 2 | [REGRESSION RISK]    | output/test-cases/TC-042      | AC 02.1 | TC asserts field = null; new flow sets a default  |
| 3 | [UNDOCUMENTED IN AC] | Figma node #1234              | —       | Confirmation dialog in Figma; no AC covers it     |
| 4 | [ROLE GAP]           | AC (all sections)             | —       | School Admin role undefined; Teacher only         |
| 5 | [MISSING BEHAVIOR]   | output/test-cases/TC-018      | —       | TC covers recurring_count = 0; new AC has no rule |
```

---

### Step 6 — Extract Business Rules

Consolidate all information from Steps 1–5b into a structured table. For each AC, capture:

- The explicit rule
- Field behavior: editable / locked / auto-filled / optional
- Role/permission constraints
- Conditional logic, default values, auto-calculation
- Conflict handling and cross-system impact

```
| #  | AC      | Business Rule                                         |
|----|---------|-------------------------------------------------------|
| 1  | AC 01.1 | Button visible only when is_recurring = TRUE          |
| 2  | AC 01.2 | Date auto-filled: last end date + 7 days              |
```

---

### Step 7 — Formulate Clarification Questions

For every ambiguity, conflict, or gap found in Steps 5b and 6, write a question using this format:

> **[Tag]** The question — phrased for a product manager or developer.
> _Evidence: `<source file or AC ID>` — `<what creates the gap or ambiguity>`_

Use the same tags as Step 5b. Every question must have an Evidence line. Write at least one question per AC with ambiguous, conflicting, or undefined behavior.

---

### Step 8 — Save the Spec File

Save to: `input/specs/<TICKET-ID>: <Feature Name>`
_(e.g. `input/specs/LT-90573: Extend Recurring Lesson Settings`)_

```markdown
ID: <Jira URL>

## Summary

<2–3 sentences: what the feature does and why>

## Acceptance Criteria

<Full AC from Jira, preserving US/AC numbering. Include field-behavior tables where applicable.>

## Business Rules (Extracted)

| #   | AC      | Business Rule |
| --- | ------- | ------------- |
| 1   | AC XX.X | ...           |

## Conflict & Gap Analysis

### Conflicts with Existing System

| #   | Tag        | Source               | AC      | Description |
| --- | ---------- | -------------------- | ------- | ----------- |
| 1   | [CONFLICT] | input/specs/LT-XXXXX | AC XX.X | ...         |

### Missing in Requirements

| #   | Tag                  | Source                   | Description |
| --- | -------------------- | ------------------------ | ----------- |
| 1   | [UNDOCUMENTED IN AC] | Figma node #XXXX         | ...         |
| 2   | [MISSING BEHAVIOR]   | output/test-cases/TC-XXX | ...         |
| 3   | [ROLE GAP]           | AC (all sections)        | ...         |

### Assumptions Made

- <Any inference made due to missing or ambiguous information>

## Clarification Questions

1. **[CONFLICT]** <Question>
   _Evidence: `input/specs/LT-XXXXX` — `<what it says>`_

## Related Specs

- `input/specs/<filename>` — <why it's related>

## Related Test Cases

- `output/test-cases/<path>` — <what's covered that may be impacted>

## QASE Coverage Gaps

- AC XX.X — <business rule with no existing test case>
```

---

### Step 9 — Review & Post to Jira

#### 9-1: Present for review

Show the questions (without Evidence lines) and ask:

> "Here are the clarification questions for **[TICKET-ID]**. Let me know which to **approve, remove, or reword**, and any you'd like to **add**."

#### 9-2: Wait for approval

Do not post to Jira until the user explicitly approves. Accept: "looks good", "post it", "go ahead", "LGTM", or an explicit list of question numbers.

If the user rewords a question, update both the chat response and the spec file before posting.

#### 9-3: Post as a single Jira comment

Use `mcp_jira_jira_add_comment`. Post all approved questions in one comment:

```
*Clarification Questions — QA*

1. [CONFLICT] <Question text>
2. [MISSING BEHAVIOR] <Question text>

_(Full analysis in `input/specs/<TICKET-ID>: <Feature Name>`.)_
```

#### 9-4: Update the spec

Add a posted status to the Clarification Questions section:

```markdown
## Clarification Questions

> ✅ Posted to Jira on <date> — [view comment](url)
```

---

## Quality Checks

- [ ] Asked user permission before fetching global sources; never auto-fetched
- [ ] All US and AC sections from the Jira ticket captured
- [ ] Step 5b performed for every local file found — not skipped
- [ ] Every conflict finding has a tag, source, and plain-language description
- [ ] Every clarification question has an Evidence line
- [ ] `[ROLE GAP]` and `[MISSING BEHAVIOR]` checks performed
- [ ] Assumptions section filled where inference was made
- [ ] Spec saved to `input/specs/<TICKET-ID>: <Feature Name>`
- [ ] Questions presented for review before any Jira action
- [ ] Jira comment posted as a **single comment** only after explicit approval
- [ ] No test cases generated — this skill only analyzes requirements
