---
name: verify-bug
description: >
  **WORKFLOW SKILL** — Verify a bug report using Playwright browser automation.
  USE FOR: confirming whether a reported bug is reproducible; navigating the UI step-by-step
  and capturing actual vs expected behavior; producing a structured verification report.
  INPUT: Jira bug ticket ID/URL (or manual bug description) + env name (or URL/account on
  first use). Credentials are saved per environment and reused automatically.
  OUTPUT: a structured bug verification report printed in the chat (pass/fail + evidence).
  DO NOT USE FOR: writing test cases (use generate-test-cases skill) or analyzing requirements
  (use analyze-requirements skill).
---

# Skill: Verify Bug

Senior QA engineer. Reproduce a reported bug with Playwright, capture evidence, output a structured verification report.

## Input
- Jira ticket ID or URL, OR manual bug description (summary + steps + expected + actual).
- Env name (`staging` / `uat` / `prod`). Credentials are saved per env and reused.

## References
- Report template → `.claude/references/bug-verification-report-template.md`

## Environment registry
Saved env credentials live at:
`/Users/manabie/.claude/projects/-Users-manabie-design-test-case/memory/environments.md`

Each entry: `### <env-name>` → `URL`, `Account`, `Password`.

- **User provides new URL/account/password** → read the memory file, add/overwrite the entry, save. Confirm: `Saved credentials for env <name>. I'll reuse these next time.`
- **User provides only env name, not yet saved** → ask in ONE prompt for URL + account + password, then save.

---

## Workflow

### Step 1 — Parse input and fetch bug details
The user may mix Jira ID/URL, env name, and manual description in one message. Determine what is missing, then ask for everything missing in ONE prompt.

**Jira ticket found:**
1. Extract the key. `mcp_jira_jira_get_ticket`.
2. From the ticket extract: bug summary, steps to reproduce (numbered list or "Steps to Reproduce" section), expected result, actual result, environment, ticket URL.
3. If steps to reproduce missing/unclear, show what was found and ask the user to clarify before continuing.

**Manual bug description:**
Extract from user message: summary, numbered steps, expected, actual.

**Env name** is always required. If absent: `Which environment should I verify this on? (e.g. staging, uat, prod)`

### Step 2 — Load environment config
Read the env entry from memory. Extract `URL`, `Account`, `Password`. If user provided new credentials in this message, update memory first.

### Step 3 — Open browser and navigate
1. `mcp__playwright__browser_navigate` → base URL.
2. `mcp__playwright__browser_snapshot` to confirm load.
3. If login screen: fill username + password, click submit, wait for navigation, snapshot to confirm.

**IMPORTANT:** Use `mcp__playwright__browser_snapshot` (accessibility tree) for all state checks. Do NOT use `browser_take_screenshot`.

### Step 4 — Follow steps to reproduce
Execute each step in order using `browser_navigate`, `browser_click`, `browser_fill_form`, `browser_type`, `browser_select_option`, `browser_press_key`. Use `browser_snapshot` between steps to verify state. If a step fails (element not found, navigation error, unexpected state), record the failure and stop — note the step number.

### Step 5 — Capture evidence
At final state (or failure point):
- `mcp__playwright__browser_console_messages` for console errors.
- `mcp__playwright__browser_network_requests` if the bug appears API-related.

### Step 6 — Close browser
`mcp__playwright__browser_close`.

### Step 7 — Produce the report
Output the report in chat using `.claude/references/bug-verification-report-template.md`. Verdict is one of: REPRODUCED / NOT REPRODUCED / PARTIALLY REPRODUCED.

---

## Quality checks
- Jira ticket fetched and parsed (if ID/URL provided).
- Env credentials loaded (or saved when newly provided).
- Every step from bug report executed, or failure noted with step number.
- Console errors captured.
- Verdict is one of the three allowed values.
- Report includes both actual and expected behavior.
- Browser closed.

## Example
```
/verify-bug LT-12345 on staging
```
Looks up `staging` in memory, fetches Jira, runs verification, prints report. First-time env: asks once for URL + account + password, saves, continues.
