---
name: execute-test-cases
description: >
  **WORKFLOW SKILL** — Execute test cases from JSON files using Playwright browser automation.
  USE FOR: running structured JSON test cases step-by-step in the browser; recording pass/fail
  per step; producing an execution report in chat.
  INPUT: JSON file path from input/test-cases/ + environment name.
  OUTPUT: Test execution report with pass/fail per case and per step.
  DO NOT USE FOR: converting test cases to JSON (use convert-test-cases);
  generating test cases (use generate-test-cases); reporting results to Qase.
argument-hint: "JSON file path + env name (e.g. input/test-cases/lesson/create.json on staging)"
---

# Skill: Execute Test Cases

You are a senior QA automation engineer. Execute structured JSON test cases using
Playwright browser tools and produce a clear execution report.

**Before starting, read the execution rules:**
`input/templates/automation-execution-rules.md` — contains Playwright mapping, token
optimization rules, error handling, and report format. Follow these rules strictly.

**JSON format reference (if needed):**
`input/templates/automation-json-format.md` — contains JSON schema and action types.

---

## Environment Registry

Read credentials from memory:

```
/Users/manabie/.claude/projects/-Users-manabie-design-test-case/memory/environments.md
```

Each env has accounts per role (CM, HQ, Teacher). The `role` field in each test case
determines which account to use.

- Env not found → ask for URL + accounts in ONE prompt → save to environments.md
- Role credentials missing → ask → save for reuse

---

## Workflow

### Step 1 — Parse Input

Extract from user's message:

- **JSON file path** — must exist in `input/test-cases/`
- **Environment name** — e.g. `renseikai-rehearsal2`, `staging`

If either missing, ask in ONE prompt.

### Step 2 — Load Credentials & Session

Read environments.md → find env → extract role accounts.

**Session token reuse (bypass verification code):**

- Session storage path: `input/sessions/<env>-<role>.json`
- If session file exists → restore cookies via `browser_run_code`:
  ```js
  async (page) => {
    const fs = require("fs");
    const cookies = JSON.parse(fs.readFileSync("<session-file>", "utf8"));
    await page.context().addCookies(cookies);
    return "Session restored";
  };
  ```
- After restoring, navigate to start_url and take snapshot to verify session is valid (check for login page vs app page)
- If session invalid or missing → proceed with full login → after successful login, save cookies:
  ```js
  async (page) => {
    const fs = require("fs");
    const cookies = await page.context().cookies();
    fs.writeFileSync("<session-file>", JSON.stringify(cookies));
    return "Session saved";
  };
  ```
- If login requires a verification code → pause, ask user for the code, then continue and save session

### Step 3 — Load & Sort Test Cases

1. Read JSON file (1 tool call)
2. **Group by `role`** to minimize re-logins
3. Within each group, sort by severity: critical → major → minor → trivial

### Step 4 — Present Execution Plan

Show summary table and wait for user confirmation:

```
| # | ID | Title | Steps | Role | Severity |
Proceed? (yes / yes but skip <ID> / no)
```

### Step 5 — Open Browser & Execute

1. Navigate to env URL → snapshot → login with first role
2. For each case: execute steps following the rules in `automation-execution-rules.md`
3. Record PASS/FAIL per step

### Step 6 — Close Browser

Always call `mcp__playwright__browser_close`, even if execution failed.

### Step 7 — Output Report

Follow the report format in `automation-execution-rules.md`.
Call `browser_console_messages` only if any case FAILED.

---

## Quality Checks

- [ ] JSON loaded successfully
- [ ] Credentials loaded or saved
- [ ] Cases grouped by role
- [ ] User confirmed plan
- [ ] Every step executed or failure recorded
- [ ] Browser closed
- [ ] Report output with summary + failed details

---

## Examples

> `/execute-test-cases` input/test-cases/lesson-management/create-lesson.json on renseikai-rehearsal2

> `/execute-test-cases` input/test-cases/student-session/lesson-allocation.json on staging
