---
name: import-to-qase
description: >
  **WORKFLOW SKILL** — Import test cases from a local file into Qase.
  USE FOR: uploading newly generated test cases to Qase; creating missing suites in Qase;
  restructuring an existing .md or .csv test case file to match Qase import format;
  syncing local test case files with Qase after generation.
  INPUT: Qase project URL or project code + test case file path (.md or .csv from `epics/<bucket>/<epic-folder>/test-cases/`).
  OUTPUT: all test cases created in Qase under the correct suite hierarchy; .csv file updated
  with real Qase suite IDs.
  DO NOT USE FOR: generating test cases (use generate-test-cases skill); analyzing requirements
  or defining coverage.
---

# Skill: Import Test Cases to Qase

Senior QA engineer. Push a local `.md`/`.csv` test case file into Qase, creating missing suites and deduplicating against existing cases.

## Input
- Qase link or project code (e.g. `https://app.qase.io/project/LM` → `LM`).
- Test case file path: `.md` or `.csv` under `epics/<bucket>/<epic-folder>/test-cases/`.

## References
- Field mapping + multi-line rules + summary template → `.claude/references/qase-import-rules.md`
- Qase CSV header → `.claude/references/qase-format.csv`
- TC output structure (input format) → `.claude/references/test-case-output-template.md`

---

## Workflow

### Step 0 — Require parent suite link
If the user did not provide a suite URL with `suite=<ID>` (e.g. `https://app.qase.io/project/LM?suite=42`), **STOP** and ask:
> "Please provide the QASE suite link where you want to import these new test cases. This will be used as the parent suite."

Wait for the link before proceeding.

### Step 1 — Parse project code + parent suite ID
- Project code: uppercase segment after `/project/` (e.g. `LM`).
- Target parent suite ID: the `suite=` query value. All root suites from the file MUST nest under this parent.

### Step 2 — Read the test case file
**`.md`:**
- `## Suite:` → suite name.
- `### <title>` → TC title.
- `**Description:**` → description.
- `**Preconditions:**` → preconditions block.
- Table rows `| # | Action | Expected Result | Test Data |` → steps.
- `**Severity:**` / `**Priority:**` → severity / priority.

**`.csv`:**
- Rows with only `suite_id`/`suite_parent_id`/`suite` filled → suite definition rows.
- Rows with `title` filled → TC rows.
- Map columns per Qase schema (see qase-import-rules.md).

### Step 3 — Confirm runtime Qase MCP capabilities
Before reading or changing Qase, inspect the Qase MCP tools actually available in the current runtime. Do not assume the operations named in this skill are exposed.

- Record the available read/create/update/delete operations needed for this import.
- If a requested operation (especially delete) is unavailable, stop before partial restructuring and report the exact capability gap to the user.
- Do not substitute Browser automation merely because an MCP operation is unavailable unless the user explicitly asks for that fallback.

### Step 4 — Fetch existing suites
`mcp_qase_list_suites` for the project. Paginate (`offset`) until exhausted. Build `suite title → suite ID` map.

### Step 5 — Resolve suite hierarchy
For each suite name in the file:
1. Look up in the map from Step 4.
2. **Exists** → record its `suite_id`.
3. **Does not exist** → `mcp_qase_create_suite` with `code`, `title`, and `parent_id` (real ID of parent; omit if root-of-batch — root sits under the user-provided target parent).
4. **Order:** create parent suites before children. Preserve file hierarchy in Qase.

Build final map: `local suite name → real Qase suite_id`.

### Step 6 — Prepare TC payloads
Construct payloads per TC using the field mapping in `.claude/references/qase-import-rules.md`. **Apply the multi-line content rule** (real newlines or `<br>`, no literal `\n` strings).

Before sending any payload, validate it against `.claude/references/test-case-rules.md`: one setup condition per capitalized precondition bullet; no actor-only bullet; and every step action uses `Actor + present-tense verb + action`.

### Step 7 — Check for duplicates
For each suite batch, `mcp_qase_list_cases` with `code`, `suite_id`, `search=<title>`. If a case with identical title exists in the same suite:
- **Skip** and log: `SKIP: "<title>" already exists in suite "<suite name>" (ID: <existing_id>)`.

### Step 8 — Import
Group cases by suite. For each suite batch:
1. `mcp_qase_bulk_create_cases` with `code` and `cases` (filtered after Step 7).
2. Record returned case IDs.
3. On batch failure, retry individual cases; log failures with title + error.

### Step 9 — Update CSV with real suite IDs
Find the companion `.csv` (same path as `.md`, or use the input `.csv`). Replace placeholder suite IDs with real Qase IDs from Step 5. Save.

### Step 10 — Verify and report summary
For every case created or changed in this run, re-fetch it from Qase and compare the title, preconditions, step count, and every action/expected-result pair with the approved local source. Stop and correct any mismatch before reporting completion.

Print the summary using the template in `.claude/references/qase-import-rules.md`.

---

## Quality checks
- All suite names resolved to real Qase IDs (no placeholders).
- Each child suite has its parent created first.
- No duplicate cases created.
- Every case has `suite_id` set (no orphans at root).
- Steps are `{ action, expected_result, data }` arrays, not flat strings.
- No literal `\n`/`/n`/`\\n` text remains; multi-line uses real newlines or `<br>`.
- At least one imported case spot-checked in Qase UI for line breaks.
- Every changed case re-fetched and matches the approved local source, including its step count.
- Local `.csv` updated with real suite IDs.
- Summary printed with counts and failures.

## Example
```
Import test cases to Qase.
Qase: https://app.qase.io/project/LM?suite=100
File: epics/LT-90573-extend-recurring-lesson/test-cases/extend-recurring.csv
```
