---
name: review-automation-tests
description: >
  **WORKFLOW SKILL** — Review automation test results from a Qase test run.
  USE FOR: reviewing an automated Playwright/automated test run in Qase; reading step-results.json
  from each test case execution; comparing automation results against the original test case
  (preconditions, actions, expected results); identifying failures, flakiness, or mismatches;
  and exporting a structured review report.
  INPUT: Qase test run URL or run ID + project code (e.g. `https://app.qase.io/run/PX/dashboard/2187`).
  OUTPUT: a Markdown review report saved to `reports/automation-reviews/`.
  DO NOT USE FOR: generating test cases, importing test cases, or analyzing Jira requirements.
---

# Skill: Review Automation Test Run

Review automated Playwright test runs in Qase. Compare each case's execution log against its Qase definition (preconditions, actions, expected results). Output a structured Markdown report and update Qase automation status per verdict.

## Input
- Qase run URL or run ID — e.g. `https://app.qase.io/run/PX/dashboard/2187` or `PX run 2187`.
- Project code — extracted from URL (e.g. `PX`).

## References
- Deep-check rules + verdict codes + quality checklist → `.claude/references/automation-review-rules.md`
- Report Markdown template → `.claude/references/automation-review-report-template.md`

---

## Workflow

### Step 1 — Fetch run summary
`mcp_qase_get_run(code=<PROJECT>, id=<RUN_ID>)` → title, status, start/end time, totals. Mark `failed`/`invalid`/`blocked` cases as priority targets.

### Step 2 — Fetch all execution results
`mcp_qase_list_results(code=<PROJECT>, run=<RUN_ID>, limit=100)`. There may be multiple result entries per case (retries). For each `case_id`, use only the latest entry (highest `end_time`); track prior statuses as retry history.

Build a result map per `case_id`: `{ final_status, retry_history, time_spent_ms, step_results_md_url, steps[] }`.

### Step 3 — Read `step-results.json` per case
Fetch the attachment URL (mime: `application/json`, filename: `step-results.json`) via `fetch_webpage`.

Each step's JSON content contains structured prefix labels:
```
PRECONDITION: <setup state or data used>
ACTION:       <what automation did>
EXPECTED:     <what was verified>
```

Mapping:
| Prefix | Qase field |
|---|---|
| `PRECONDITION:` | `preconditions` (case-level) |
| `ACTION:` | `steps[N].action` |
| `EXPECTED:` | `steps[N].expected_result` |

Extract all three per step. Any entry with no matching Qase step is an **unmapped automation action** (see Step 5).

Read order: failed/invalid first, then retried-then-passed (flaky candidates), then clean-pass if needed.

### Step 4 — Fetch original case definition
`mcp_qase_get_case(code=<PROJECT>, id=<CASE_ID>)` for each unique `case_id`. Extract `title`, `preconditions`, `steps[]` (action, expected_result, position), `severity`, `priority`, `automation`, `suite_id`.

Build a definition map: `case_id → { preconditions, steps: [{position, action, expected_result}] }`.

### Step 5 — Compare execution vs. definition
Group cases by `suite_id`. For each suite, iterate cases.

For each case, run the **deep-check rules** in `.claude/references/automation-review-rules.md` (11 mandatory checks: input values, sub-conditions, precondition state, extra actions, name vs. action, shallow verification, lesson type, definition quality, defined-vs-executed steps, silent skips, recurring chain scope).

Verdict per case:
- **Matching** — every defined step has a corresponding executed step, every expected sub-condition verified, no extras, precondition matches.
- **Not Matching** — any of the verdict codes in the rules reference applies.

### Step 6 — Generate review report
Use the template in `.claude/references/automation-review-report-template.md`. Save to:
```
reports/automation-reviews/<project>-run-<run_id>-review.md
```

### Step 7 — Update automation status

| Verdict | Update To | Qase value |
|---|---|---|
| ✅ Matching | Automated | `automation = 2` |
| ❌ Not Matching | Manual | `automation = 0` |

Only update cases currently set to **In Review** (`automation = 3`). Skip others.

**7a — Approval gate.** Show the user a summary table of proposed updates and ask "Proceed? (yes/no)". Do not call any update API until the user approves.

**7b — Apply.** For each approved case, `mcp_qase_update_case(code, id, automation=<2|0>)`. Re-fetch each case after update to confirm. If the field doesn't persist, fall back to manual UI update at `https://app.qase.io/case/<PROJECT>?id=<CASE_ID>` and note the case as "manually updated".

**7c — Record.** Append an "Automation Status Updates" table to the review report (see template).

---

## Quality gate

Before finalizing, run the full quality checklist in `.claude/references/automation-review-rules.md` (sections: Coverage, PRECONDITION/ACTION/EXPECTED mapping, Deep checks, Automation status updates).
