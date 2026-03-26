---
description: >
  **WORKFLOW SKILL** — Analyze requirements from a Jira ticket to produce a structured spec file,
  including deep conflict detection, gap analysis, and inconsistency mapping between new requirements
  and the current system.
  USE FOR: onboarding a new ticket, analyzing feature requirements, formulating clarification
  questions, discovering scope from Jira + Confluence + Figma, detecting mismatch/conflicts with
  existing specs and test cases, identifying missing behaviors in new requirements.
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
   - Which business rules from Step 6 already have coverage
   - Gaps: business rules with no corresponding test case

If no QASE link was provided, skip this step silently.

---

### Step 5 — Search Local Workspace for Related Specs and Test Cases

Use keywords from Step 1 (feature name, module, field names) to search locally:

1. **Search `input/specs/`** — look for any existing spec files mentioning the same feature or module.
2. **Search `output/test-cases/`** — find existing test cases that may overlap with or be impacted by this ticket.
3. **Search `output/test-coverages/`** — check if a coverage matrix already exists for this feature.

For each match, **read the full content** of the file — do not just note the filename. You need the actual business rules, field behaviors, and assertions to compare in Step 5b.

---

### Step 5b — Conflict & Gap Analysis Against Current System

This step is **mandatory** whenever related specs or test cases are found in Step 5. Its purpose is to surface mismatches, inconsistencies, and missing behaviors **before** writing the spec.

#### 5b-1: Business Rule Delta

For each business rule you will extract in Step 6, check against every related spec and test case:

- Does an existing spec define the **same field or flow** with **different behavior**?
- Does an existing test case **assert a value or state** that this ticket would change or invalidate?
- Does the new rule **extend**, **replace**, or **conflict** with the existing behavior?

Classify each finding using one of these tags:

| Tag                    | Meaning                                                                     |
| ---------------------- | --------------------------------------------------------------------------- |
| `[CONFLICT]`           | New rule directly contradicts an existing spec or test assertion            |
| `[REGRESSION RISK]`    | New behavior may break an existing test case without contradicting the spec |
| `[EXTENDED]`           | New rule adds to existing behavior without contradiction                    |
| `[REPLACED]`           | New rule fully supersedes an existing rule (note the old rule explicitly)   |
| `[UNDOCUMENTED IN AC]` | Figma or Confluence shows a behavior not mentioned in any AC                |
| `[MISSING BEHAVIOR]`   | A scenario exists in the system but this ticket provides no rule for it     |

#### 5b-2: Implicit Dependency Check

Ask for each new rule:

- Does it **assume a precondition** that is set by another feature or ticket?
- If that upstream feature changes, does this ticket's behavior break?
- Is there a **data dependency** (e.g. a field value produced by another flow) that is not documented in the AC?

#### 5b-3: Role & Permission Coverage Check

- List all roles that interact with this feature (from AC, Confluence, Figma).
- For each role mentioned, verify: does the AC define behavior for **every role**, or only some?
- Flag roles where behavior is undefined as `[ROLE GAP]`.

#### 5b-4: Edge Case & Boundary Check Against Existing Tests

Compare the scope of existing test cases against the new AC:

- Are there **boundary conditions** already tested that the new AC does not address?
- Are there **error scenarios** covered in existing tests that the new AC ignores?
- Are there **null/empty/zero** states tested previously that may now behave differently?

#### 5b-5: Format Findings as a Table

Consolidate all findings into a conflict and gap table:

```
| # | Tag                | Source                          | AC      | Description                                                      |
|---|--------------------|---------------------------------|---------|------------------------------------------------------------------|
| 1 | [CONFLICT]         | input/specs/LT-XXXXX, line 42   | AC 01.2 | New: date auto-filled. Existing: date always editable by teacher |
| 2 | [REGRESSION RISK]  | output/test-cases/TC-042        | AC 02.1 | TC asserts field = null on create; new flow sets a default value |
| 3 | [UNDOCUMENTED IN AC]| Figma node #1234               | —       | Confirmation dialog shown in Figma; no AC covers this dialog     |
| 4 | [ROLE GAP]         | AC (all sections)               | —       | School Admin role not mentioned; Teacher role only               |
| 5 | [MISSING BEHAVIOR] | output/test-cases/TC-018        | —       | Existing test covers recurring_count = 0; new AC has no rule     |
```

---

### Step 6 — Extract Business Rules and Acceptance Criteria

Consolidate all information from Steps 1–5b into a structured list:

**For each AC**, extract:

- The explicit rule stated in the AC
- Field behavior: editable / locked / auto-filled / optional
- Role/permission constraints
- Conditional logic (e.g. "only if `is_recurring = TRUE`")
- Default values and auto-calculation logic
- Conflict handling (e.g. "lesson not created if date already exists")
- Cross-system / integration impact (e.g. "reflected on SF Calendar, BO detail")

Format: numbered list grouped by AC ID:

```
| #  | AC      | Business Rule                                            |
|----|---------|----------------------------------------------------------|
| 1  | AC 01.1 | Button only visible when is_recurring = TRUE             |
| 2  | AC 01.2 | Date field auto-filled: last end date + 7 days           |
```

---

### Step 7 — Formulate Clarification Questions

Based on the extracted business rules and the conflict/gap findings from Step 5b, write targeted questions.

**Every question MUST follow this format:**

> **[Category]** The question itself — phrased clearly for a product manager or developer.
> _Evidence: `<source file or AC ID>` — `<what it says that creates the gap or ambiguity>`_

**Categories:**

| Category             | Trigger condition                                           |
| -------------------- | ----------------------------------------------------------- |
| `[CONFLICT]`         | Two sources define the same behavior differently            |
| `[REGRESSION RISK]`  | Existing test may fail under new behavior                   |
| `[MISSING BEHAVIOR]` | No AC rule exists for a scenario the system already handles |
| `[ROLE GAP]`         | A role is not covered by any AC                             |
| `[BOUNDARY]`         | Min/max or limit value is undefined                         |
| `[ERROR HANDLING]`   | No AC describes what happens on failure or invalid input    |
| `[AMBIGUITY]`        | A rule is stated but its exact behavior is unclear          |
| `[DATA INTEGRITY]`   | Partial failure or atomicity is not addressed               |
| `[TENANT-SPECIFIC]`  | Behavior may vary per tenant/org but AC does not clarify    |

Write all questions to the spec file first. They will be reviewed and posted to Jira in Step 9.

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

## Conflict & Gap Analysis

### Conflicts with Existing System

| #   | Tag               | Source                   | AC      | Description                                     |
| --- | ----------------- | ------------------------ | ------- | ----------------------------------------------- |
| 1   | [CONFLICT]        | input/specs/LT-XXXXX     | AC XX.X | <new behavior> vs <existing behavior>           |
| 2   | [REGRESSION RISK] | output/test-cases/TC-XXX | AC XX.X | <what the existing test asserts that may break> |

### Missing in Requirements

| #   | Tag                  | Source                   | Description                                      |
| --- | -------------------- | ------------------------ | ------------------------------------------------ |
| 1   | [UNDOCUMENTED IN AC] | Figma node #XXXX         | <behavior visible in Figma but absent from AC>   |
| 2   | [MISSING BEHAVIOR]   | output/test-cases/TC-XXX | <scenario already in system with no new AC rule> |
| 3   | [ROLE GAP]           | AC (all sections)        | <role not addressed>                             |

### Assumptions Made

<!-- List any assumption this analysis made due to missing or ambiguous information -->

- Assumed behavior X applies to all tenants unless stated otherwise.

## Clarification Questions

1. **[CONFLICT]** <Question>
   _Evidence: `input/specs/LT-XXXXX` — `<what it says>`_

2. **[MISSING BEHAVIOR]** <Question>
   _Evidence: `output/test-cases/TC-XXX` — `<what the test covers>`_

## Related Specs

- `input/specs/<related spec filename>` — <why it's related>

## Related Test Cases

- `output/test-cases/<path>` — <what's already covered that may be impacted>

## QASE Coverage Gaps

<!-- List business rules from the Business Rules table that have no existing QASE test case -->

- AC XX.X — <business rule with no test case yet>
```

---

### Step 9 — Review & Post Clarification Questions to Jira

After the spec file is saved, present the clarification questions to the user for review **before** posting anything to Jira.

#### 9-1: Present questions for review

Display all questions in a clean, readable format — without the Evidence lines, just the numbered questions. Tell the user:

> "Here are the clarification questions I've drafted for **[TICKET-ID]**. Please review and let me know:
>
> - Which questions are **approved** to post as a Jira comment
> - Which should be **removed or reworded**
> - Any additional questions you'd like to **add**"

#### 9-2: Wait for user confirmation

**Do not post anything to Jira until the user explicitly approves.**

Accept any of these as approval signals:

- "looks good", "post it", "go ahead", "approved", "LGTM"
- A modified list from the user
- Explicit confirmation like "post questions 1, 2, 4"

If the user asks to reword a question, update it in both the chat and the spec file before posting.

#### 9-3: Post approved questions as a Jira comment

Once approved, use the **Jira MCP** tool (`mcp_jira_jira_add_comment`) to post a single comment to the ticket containing all approved questions.

Format the Jira comment as:

```
*Clarification Questions — [Your Name / QA]*

Please help clarify the following before test case generation begins:

1. [CONFLICT] <Question text>

2. [MISSING BEHAVIOR] <Question text>

3. [ROLE GAP] <Question text>

_(Generated from spec analysis. Full details in `input/specs/<TICKET-ID>: <Feature Name>`.)_
```

> **Note:** Post as a **single comment** — do not post one comment per question.

#### 9-4: Confirm and update spec

After posting, tell the user the comment was added and include the Jira comment URL if available.
Update the spec file to note that questions were posted:

```markdown
## Clarification Questions

> ✅ Posted to Jira on <date> — [view comment](jira-comment-url)

1. **[CONFLICT]** <Question>
   _Evidence: ..._
```

---

## Quality Checks

Before finishing, verify:

- [ ] All User Stories and AC sections from the Jira ticket are captured
- [ ] Figma field states cross-referenced with AC (skipped silently if no Figma link found)
- [ ] QASE existing test cases fetched and coverage gaps identified (skipped silently if no QASE link provided)
- [ ] Step 5b was performed for every related spec/test case found — not skipped
- [ ] Every conflict finding in the table has a tag, a source with line reference if possible, and a plain-language description
- [ ] Every clarification question includes an _Evidence_ line pointing to a specific source
- [ ] At least one question per AC that has ambiguous, conflicting, or undefined behavior
- [ ] `[ROLE GAP]` check performed — all roles identified and gaps noted
- [ ] `[MISSING BEHAVIOR]` check performed — existing test scenarios compared against new AC scope
- [ ] Assumptions section is filled if any inference was made
- [ ] Clarification questions presented to user for review before any Jira action
- [ ] Jira comment posted only after explicit user approval — never auto-posted
- [ ] Jira comment is a single comment containing all approved questions
- [ ] Spec file updated with posted status and Jira comment URL after posting
- [ ] Spec file saved to `input/specs/` with format `<TICKET-ID>: <Feature Name>`
- [ ] No test cases are generated — this skill only analyzes and documents requirements

---

## Example Invocation

```
Analyze requirements for ticket LT-99999.
QASE: https://app.qase.io/project/LM?suite=42
```

The skill will fetch the Jira ticket, read related Confluence and Figma sources, search existing
specs and test cases, extract all business rules, perform a structured conflict and gap analysis
(Step 5b), formulate evidence-backed clarification questions, save a complete spec to
`input/specs/LT-99999: <Feature Name>`, then **present the questions for user review** before
posting them as a single Jira comment upon approval.
