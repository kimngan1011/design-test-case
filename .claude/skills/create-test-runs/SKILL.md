---
name: create-test-runs
description: >
  **WORKFLOW SKILL** — Create test runs from a Qase test plan template.
  USE FOR: creating multiple test runs from a Qase test plan; assigning test runs to team members;
  bulk-creating runs with test cases from a plan; marking test cases as Skipped for retest;
  setting up regression or acceptance test runs from a template plan.
  INPUT: Qase test plan URL (e.g. https://app.qase.io/plan/PX/186) plus run titles and status update rules.
  OUTPUT: Test runs created in Qase under the specified plan, with optional bulk status updates.
  DO NOT USE FOR: importing test cases from local files (use import-to-qase skill);
  generating test cases (use generate-test-cases skill).
argument-hint: "Qase test plan URL and list of test run titles to create"
---

# Skill: Create Test Runs from Qase Test Plan

Senior QA. Create runs from a plan template, assign them to teammates, optionally bulk-update statuses to Retest.

## Input
1. Qase test plan URL — e.g. `https://app.qase.io/plan/PX/186`.
2. Test run definitions — list of run titles + their cases (either `"as in the template"` = all plan cases, or a specific subset of case IDs).
3. Status update rules (optional) — which runs should have bulk updates after creation.

## References
- Default run definitions + Retest pattern + summary template + key constraints → `.claude/references/qase-test-run-defaults.md`

---

## Workflow

### Step 1 — Parse plan URL
- Project code = segment after `/plan/` (e.g. `PX`).
- Plan ID = number at end of URL (e.g. `186`).

### Step 2 — Fetch plan + determine case assignments
1. `mcp_qase_get_plan(code, id)` → `title`, `cases` (flat list).
2. The API does NOT expose named entries/groups. To determine which cases belong to which run, look up existing runs as a reference template:
   - For each run title, `mcp_qase_list_runs(code, search=<title>, include=cases)`.
   - Find the most recent result with `plan_id` matching the current plan.
   - Extract its `cases` — this defines the membership for the new run.
3. Build mapping `run title → [case_id, ...]`.
4. If no reference run exists for a title, fall back to ALL cases from the plan.

### Step 3 — Create runs (linked to plan)
Each run is created with `plan_id` so it appears under the plan's "Test runs" tab. Pass the explicit `cases` subset together with `plan_id` — the API creates the run with exactly those cases (must already exist in the plan).

For each test run:
1. `mcp_qase_create_run` with `code`, `title`, `plan_id`, `cases` (subset), `environment_id` (same as reference run if available), optional `description`.
2. Record the returned run ID.
3. On failure, log and continue to next run.

Order: as they appear in the plan, or as specified by the user.

### Step 4 — Mark wanted cases as Skipped

For each of the 5 member runs, mark only the wanted cases (subset from Step 2) as `skipped`:
- `mcp_qase_create_results_bulk(code, id=<run_id>, results=[{case_id, status: "skipped"}, ...])`.
- Batch in groups of 100 if the list exceeds 100.

After this step: wanted cases → Skipped; unwanted cases → Untested.

### Step 5 — Reset cases to Retest (Playwright UI)
Same target runs as Step 4. The API does NOT support `retest` — it is UI-only.

Use `mcp_playwright_browser_run_code` with the snippet in `.claude/references/qase-test-run-defaults.md` § Playwright "Retest" pattern. The snippet:
1. Navigates to the run dashboard.
2. Removes the cached Untested filter (mandatory — else "Retest" button stays disabled).
3. Selects all visible cases.
4. Clicks Retest.

### Step 6 — Report summary
Print the summary using the template in `.claude/references/qase-test-run-defaults.md`.

---

## Quality checks
- All runs linked to the correct plan (`plan_id` set, runs appear under plan's "Test runs" tab).
- Each run contains the expected number of cases (unwanted cases not in the run).
- Status updates applied correctly (Skipped → Retest for the 5 member runs).
- No duplicate runs created (check by title before creating).
- Summary accurately reflects what was created.

## Defaults
If the user provides only a plan URL (no run titles), use the default 7-run configuration in `.claude/references/qase-test-run-defaults.md`. The user can override.
