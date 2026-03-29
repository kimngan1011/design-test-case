---
description: >
  **WORKFLOW SKILL** — Import test cases from a local file into Qase.
  USE FOR: uploading newly generated test cases to Qase; creating missing suites in Qase;
  restructuring an existing .md or .csv test case file to match Qase import format;
  syncing local test case files with Qase after generation.
  INPUT: Qase project URL or project code + test case file path (.md or .csv from `output/test-cases/`).
  OUTPUT: all test cases created in Qase under the correct suite hierarchy; .csv file updated
  with real Qase suite IDs.
  DO NOT USE FOR: generating test cases (use generate-test-cases skill); analyzing requirements
  or defining coverage.
---

# Skill: Import Test Cases to Qase

You are a senior QA engineer responsible for maintaining the Qase test management project for the Manabie lesson-management system.

---

## Input

- **Qase link** — a URL like `https://app.qase.io/project/LM` or just the project code (e.g. `LM`)
- **Test case file** — path to a `.md` or `.csv` file in `output/test-cases/` (e.g. `output/test-cases/lesson-management/lesson/extend-recurring/LT-90573-extend-recurring-lesson.md`)

---

## Workflow

### Step 0 — Prompt for Parent QASE Suite Link

1. If the user did not provide a specific QASE suite link (with a `suite=` parameter, e.g., `https://app.qase.io/project/LM?suite=42`) in their initial input, you **MUST STOP** and ask the user:
> "Please provide the QASE suite link where you want to import these new test cases. This will be used as the parent suite."
2. Wait for the user to provide the link before proceeding to Step 1.

---

### Step 1 — Parse the Qase Project Code

1. From the Qase link, extract the **project code** — the uppercase segment after `/project/` (e.g. `LM` from `https://app.qase.io/project/LM`).
2. If only a project code is given, use it directly.
3. From the suite URL provided (e.g. `.../project/LM?suite=42`), extract the **target parent suite ID**. All root suites from the file MUST be nested under this parent suite.

---

### Step 2 — Read the Test Case File

Read the input file fully.

**If the file is a `.md`:** extract the following per test case:

- `## Suite:` heading → suite name
- `### <title>` heading → test case title
- `**Description:**` → description
- `**Preconditions:**` → preconditions block
- Table rows `| # | Action | Expected Result | Test Data |` → steps
- `**Severity:**` → severity
- `**Priority:**` → priority

**If the file is a `.csv`:** parse all rows:

- Rows where only `suite_id`, `suite_parent_id`, and `suite` are filled → suite definition rows
- Rows where `title` is filled → test case rows
- Map all column values per the Qase CSV schema (see Step 5)

---

### Step 3 — Fetch Existing Suites from Qase

1. Call `mcp_qase_list_suites` with the project code to retrieve all existing suites.
2. Build a lookup map: `suite title → suite ID` (e.g. `"Extend Recurrence Button" → 101`).
3. If the suite list is paginated (more than 100 suites), paginate using `offset` until all suites are retrieved.

---

### Step 4 — Resolve Suite Hierarchy

For each suite name found in the test case file:

1. Look up the suite name in the map from Step 3.
2. **If the suite exists** in Qase → record its real `suite_id`.
3. **If the suite does not exist** → create it using `mcp_qase_create_suite`:
   - `code`: project code
   - `title`: suite name
   - `parent_id`: parent suite's real ID (if the suite is nested; otherwise omit)
   - After creation, record the returned `suite_id`.
4. **Suite nesting rule:** create parent suites before child suites. The hierarchy found in the file (suite → sub-suite) must be preserved in Qase.

Build a final map: `local suite name → real Qase suite_id`.

---

### Step 5 — Prepare Test Cases for Import

For each test case extracted in Step 2, construct the import payload:

| Field           | Source               | Rules                                                           |
| --------------- | -------------------- | --------------------------------------------------------------- |
| `title`         | Test case title      | Max 255 characters; strip markdown formatting                   |
| `description`   | Description field    | Plain text; strip markdown bold/italic                          |
| `preconditions` | Preconditions block  | Plain text; preserve bullet structure as newlines               |
| `steps`         | Table rows           | Array of `{ action, expected_result, data }` objects            |
| `suite_id`      | Resolved from Step 4 | Real Qase suite ID (integer)                                    |
| `severity`      | Severity field       | Map: critical→critical, major→major, normal→normal, minor→minor |
| `priority`      | Priority field       | Map: high→high, medium→medium, low→low                          |
| `type`          | Fixed                | `functional`                                                    |
| `behavior`      | Fixed                | `undefined`                                                     |
| `automation`    | Fixed                | `is-not-automated`                                              |
| `status`        | Fixed                | `draft`                                                         |
| `is_flaky`      | Fixed                | `false`                                                         |
| `layer`         | Fixed                | `unknown`                                                       |
| `steps_type`    | Fixed                | `classic`                                                       |

**Step formatting rule:**
Each step is an object: `{ action: "...", expected_result: "...", data: "..." }`

- `action` = the "Action" column value
- `expected_result` = the "Expected Result" column value
- `data` = the "Test Data" column value (empty string `""` if blank)

---

### Step 6 — Check for Duplicates

Before creating any test case, call `mcp_qase_list_cases` with:

- `code`: project code
- `suite_id`: the resolved suite ID for this batch
- `search`: the test case title (or a distinctive substring)

If an existing case with an identical title is found in the same suite:

- **Skip** that test case and log: `SKIP: "<title>" already exists in suite "<suite name>" (ID: <existing_id>)`
- Do NOT create a duplicate.

---

### Step 7 — Import Test Cases to Qase

Group test cases by suite (to minimize API calls). For each suite batch:

1. Call `mcp_qase_bulk_create_cases` with:
   - `code`: project code
   - `cases`: array of test case objects (from Step 5, filtered by Step 6)

2. After each batch, record the returned case IDs.

3. If a batch fails, retry individual cases using the same payload. Log any failures with the test case title and error message.

---

### Step 8 — Update the CSV File with Real Suite IDs

After all suites and test cases are created, update the companion `.csv` file to reflect the real Qase suite IDs:

1. Find the `.csv` file at the same path as the `.md` (or use the `.csv` directly if that was the input).
2. Replace all placeholder suite IDs (e.g. `100`, `101`) in the suite definition rows and test case rows with the real Qase suite IDs from Step 4.
3. Save the updated `.csv` file.

This keeps the local file in sync with Qase for future reference.

---

### Step 9 — Report Summary

After completing the import, output a summary:

```
## Import Summary

**Project:** <project code>
**File:** <file path>
**Date:** <today's date>

### Suites
| Suite Name | Status | Qase Suite ID |
|---|---|---|
| Extend Recurrence Button | Created | 101 |
| Extend Recurrence Form   | Existed | 88  |

### Test Cases
| Title | Suite | Status | Qase Case ID |
|---|---|---|---|
| Extend Recurrence Button – Recurring Lesson – Button Visible | Extend Recurrence Button | Created | 1042 |
| Extend Recurrence Form – Date Field – Auto-calculated       | Extend Recurrence Form   | Skipped (duplicate) | — |

### Totals
- Suites created: X
- Suites already existed: X
- Test cases created: X
- Test cases skipped (duplicates): X
- Test cases failed: X
```

---

## Quality Checks

Before finishing, verify:

- [ ] All suite names from the file are resolved to real Qase suite IDs (no placeholder integers remain)
- [ ] No parent suite is missing — each child suite has its parent created first
- [ ] No duplicate test cases created — titles deduplicated per suite
- [ ] Every test case has `suite_id` set (no orphaned test cases at root level)
- [ ] Steps are structured as `{ action, expected_result, data }` arrays — not flat strings
- [ ] The local `.csv` file is updated with real Qase suite IDs after import
- [ ] Import summary is printed with counts and any failures listed

---

## Example Invocations

```
Import test cases to Qase from output/test-cases/lesson-management/lesson/extend-recurring/LT-90573-extend-recurring-lesson.md
Qase project: LM
```

```
Import test cases to Qase.
Qase: https://app.qase.io/project/LM?suite=100
File: output/test-cases/lesson-management/lesson/extend-recurring/LT-90573-extend-recurring-lesson.csv
```

The skill will parse the project code, fetch existing suites, create missing ones, deduplicate against existing test cases, bulk-create all new cases under the correct suite hierarchy, update the local CSV with real suite IDs, and print a full import summary.
