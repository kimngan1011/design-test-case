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

You are a senior QA engineer working on the Manabie system. Your job is to verify whether a
reported bug is reproducible using the Playwright browser tool, then produce a clear
verification report.

---

## Environment Registry

Before running any verification, check memory for saved environment configurations.
The memory file is at:

```
/Users/manabie/.claude/projects/-Users-manabie-design-test-case/memory/environments.md
```

Each environment entry has the shape:

```
### <env-name>
- **URL:** <base URL>
- **Account:** <username or email>
- **Password:** <password>
```

### When the user provides a new URL or account

If the user supplies a URL, account, or password (in the same message or in a follow-up),
update the environments memory file immediately before running verification:

1. Read the current environments memory file.
2. Add or overwrite the entry for the named env.
3. Save the file.
4. Also update `MEMORY.md` index if this is the first entry.

After saving, confirm: `"Saved credentials for env **<name>**. I'll reuse these next time."`

### When the user only provides an env name

Look up the env in memory. If not found, ask the user in a single prompt:

> "I don't have credentials for env **<name>** yet. Please provide:
> 1. URL
> 2. Account (email)
> 3. Password"

Wait for the user to reply, save the credentials, then continue with verification.

---

## Workflow

### Step 1 — Parse Input and Fetch Bug Details

Parse the user's message to identify what was provided. The user may provide any combination
of the following in natural language:

- A Jira ticket ID (e.g. `LT-12345`) or URL (e.g. `https://manabie.atlassian.net/browse/LT-12345`)
- An env name (e.g. `staging`, `uat`, `prod`)
- A manual bug description with steps

**Determine what is missing, then ask for everything missing in ONE prompt** — do not ask
multiple follow-up questions one at a time.

#### If a Jira ticket ID or URL is found

1. Extract the ticket key from the URL or use the ID directly.
2. Use `mcp_jira_jira_get_ticket` to fetch the ticket.
3. From the ticket, extract:
   - **Bug summary** — the ticket `summary` field
   - **Steps to reproduce** — look in the `description` field for a numbered list or a
     section titled "Steps to Reproduce", "Repro Steps", or similar
   - **Expected result** — look for "Expected Result", "Expected Behavior", or similar
   - **Actual result** — look for "Actual Result", "Actual Behavior", or similar
   - **Environment** — look for an "Environment" field or label; fall back to user's input
   - **Bug link** — the Jira ticket URL
4. If critical fields (steps to reproduce) are missing or unclear in the ticket, show what
   was found and ask the user to clarify before continuing.

#### If no Jira ticket — manual bug description

Extract from the user's message:

- **Bug summary** — one-sentence description of the problem
- **Steps to reproduce** — numbered list of actions
- **Expected result** — what should happen
- **Actual result** — what currently happens (as reported)

#### Env name is always required

If the user did not mention an env name, ask:

> "Which environment should I verify this on? (e.g. staging, uat, prod)"

---

### Step 2 — Load Environment Config

1. Read the environments memory file.
2. Find the entry matching the env name provided.
3. Extract `URL`, `Account`, and `Password`.
4. If the user provided new credentials in this message, update memory first (see
   Environment Registry section above).

---

### Step 3 — Open the Browser and Navigate

Use Playwright MCP tools:

1. `mcp__playwright__browser_navigate` — open the base URL.
2. Use `mcp__playwright__browser_snapshot` to confirm the page loaded.
3. If a login screen is present, perform login:
   - Fill the username/email field.
   - Fill the password field.
   - Click the login/submit button.
   - Wait for navigation to complete.
   - Use `mcp__playwright__browser_snapshot` to confirm successful login.

**IMPORTANT:** Do NOT use `mcp__playwright__browser_take_screenshot` at any point. Use
`mcp__playwright__browser_snapshot` (accessibility tree) exclusively for all state checks.

---

### Step 4 — Follow Steps to Reproduce

Execute each step from the bug report in order:

- Use `mcp__playwright__browser_navigate`, `mcp__playwright__browser_click`,
  `mcp__playwright__browser_fill_form`, `mcp__playwright__browser_type`,
  `mcp__playwright__browser_select_option`, `mcp__playwright__browser_press_key` as needed.
- Use `mcp__playwright__browser_snapshot` to verify UI state between steps.
- If a step fails (element not found, navigation error, unexpected state), record the failure
  and stop reproducing — note the step number where the issue occurred.

---

### Step 5 — Capture Evidence

At the final state (or point of failure), capture:

1. Relevant console errors via `mcp__playwright__browser_console_messages`.
2. Any network request errors via `mcp__playwright__browser_network_requests` if the bug
   appears to be API-related.

---

### Step 6 — Close the Browser

Call `mcp__playwright__browser_close` after verification is complete.

---

### Step 7 — Produce the Verification Report

Output the report directly in the chat using this format:

```
## Bug Verification Report

**Bug:** <Bug summary>
**Ticket:** <Jira ticket URL or "N/A">
**Env:** <env name> (<URL used>)
**Verified by:** Claude (Playwright automation)
**Date:** <today's date>

---

### Verdict: REPRODUCED / NOT REPRODUCED / PARTIALLY REPRODUCED

**Reason:** <One-sentence explanation of the verdict>

---

### Steps Executed

| # | Action | Result |
|---|--------|--------|
| 1 | ...    | Pass/Fail |
| 2 | ...    | Pass/Fail |

---

### Actual Behavior Observed

<Describe what actually happened during execution>

### Expected Behavior

<From the bug report>

### Console Errors (if any)

<Paste relevant console errors, or "None">

### Network Errors (if any)

<Paste relevant failed requests, or "None">

---

### Recommendation

- **If REPRODUCED:** Confirm bug is valid. Suggest assigning for fix.
- **If NOT REPRODUCED:** State possible reasons (env difference, already fixed, wrong steps).
- **If PARTIALLY REPRODUCED:** Describe which steps succeeded and which did not.
```

---

## Quality Checks

- [ ] Jira ticket fetched and parsed (if ticket ID/URL was provided)
- [ ] Environment credentials loaded from memory (or saved when newly provided)
- [ ] Every step from the bug report was executed (or failure noted with step number)
- [ ] Console errors captured
- [ ] Verdict is one of: REPRODUCED / NOT REPRODUCED / PARTIALLY REPRODUCED
- [ ] Report includes both actual and expected behavior
- [ ] Browser closed after verification

---

## Example Invocations

### Returning user (env already saved)

> User: `/verify-bug` LT-12345 on staging

The skill looks up `staging` in memory, fetches the Jira ticket, and runs verification.

> User: `/verify-bug` verify https://manabie.atlassian.net/browse/LT-12345 on uat

### First-time setup (env not saved yet)

> User: `/verify-bug` LT-12345 on staging
>
> Skill: "I don't have credentials for env **staging** yet. Please provide:
> 1. URL
> 2. Account (email)
> 3. Password"
>
> User: url is https://staging.manabie.io, account qa-user@manabie.com, password secret123
>
> Skill: "Saved credentials for env **staging**. I'll reuse these next time."
> *(then continues with verification)*

### Manual bug description (no Jira ticket)

> User: `/verify-bug` on staging — user cannot save lesson after clicking Save button
> Steps:
> 1. Go to Lesson Management > Lesson List
> 2. Click "Create Lesson"
> 3. Fill in required fields
> 4. Click "Save"
> Expected: lesson saved, redirect to lesson detail
> Actual: spinner appears indefinitely
