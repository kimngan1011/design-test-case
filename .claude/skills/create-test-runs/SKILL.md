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
  generating test cases (use generate-test-cases skill); executing test cases (use execute-test-cases skill).
argument-hint: "Qase test plan URL and list of test run titles to create"
---

# Skill: Create Test Runs from Qase Test Plan

You are a senior QA engineer responsible for setting up test runs in Qase for the Manabie QA team.

---

## Input

The user provides:

1. **Qase test plan URL** — e.g. `https://app.qase.io/plan/PX/186`
2. **Test run definitions** — a list of run titles with their associated test cases. Each run specifies either:
   - `"as in the template"` → use all case IDs from the plan
   - A specific subset of case IDs
3. **Status update rules** (optional) — which runs should have their cases bulk-updated after creation (e.g. `Untested → Skipped` for certain assignees)

---

## Workflow

### Step 1 — Parse the Test Plan URL

1. Extract the **project code** from the URL — the segment after `/plan/` (e.g. `PX` from `https://app.qase.io/plan/PX/186`).
2. Extract the **plan ID** — the number at the end of the URL (e.g. `186`).

---

### Step 2 — Fetch the Test Plan and Determine Case Assignments

1. Call `mcp_qase_get_plan` with `code` = project code and `id` = plan ID.
2. From the response, extract:
   - `title` — the plan name
   - `cases` — the flat list of all case objects (the API does NOT expose entry/group structure)
3. Log the plan title and total number of cases found.

**Important:** The Qase API returns only a flat list of cases — it does NOT expose the named entries/groups that define which cases belong to which run. To determine the case assignment per run, **look up existing runs from the same plan** as a reference template:

4. For each expected run title, call `mcp_qase_list_runs` with:
   - `code`: project code
   - `search`: the run title (e.g. `"Long - Calendar"`)
   - `include`: `cases`
5. From the results, find the most recent run with `plan_id` matching the current plan.
6. Extract the `cases` array — this defines which case IDs belong to this run.
7. Build a mapping: `run title → [case_id_1, case_id_2, ...]`.

If no previous run exists for a given title, fall back to using ALL cases from the plan.

---

### Step 3 — Create Test Runs (Linked to Plan)

Each run is created with `plan_id` so it appears under the plan's "Test runs" tab. Pass the explicit `cases` subset together with `plan_id` — the API will create the run with exactly those cases (cases must already exist in the plan).

For each test run:

1. Call `mcp_qase_create_run` with:
   - `code`: project code
   - `title`: the run title (e.g. `"Long - Calendar"`)
   - `plan_id`: the plan ID (this links the run to the plan)
   - `cases`: the exact list of case IDs from the reference run (must be a subset of the plan's cases)
   - `environment_id`: use the same environment as the reference run if available
   - `description`: (optional) any description provided by the user

2. Record the returned **run ID** for each created run.

3. If creation fails, log the error and continue to the next run.

**Run creation order:** Create runs in the order they appear in the plan (or as specified by the user).

---

### Step 4 — Mark Wanted Cases as Skipped

**Only applies to:** `Long - Calendar`, `Hoang - Calendar`, `Thanh Hai`, `Quoc Bao`, `Van Loi`.

Skip this step for `Regression test for OOP features` and `Regression test for Renseikai full sandbox`.

For each of the 5 member runs, mark only the **wanted** cases (the subset from the reference run in Step 2) as "skipped". This distinguishes them from the unwanted cases which remain "untested".

1. Call `mcp_qase_create_results_bulk` (or use the REST API `POST /v1/result/{code}/{run_id}/bulk`) with:
   - `code`: project code
   - `id`: the run ID
   - `results`: array of result objects, one per **wanted** case:
     ```json
     {
       "case_id": <case_id>,
       "status": "skipped"
     }
     ```
   - Batch in groups of 100 if the case list exceeds 100.

2. After this step, each run has two groups:
   - **Wanted cases** → status: `Skipped`
   - **Unwanted cases** → status: `Untested`

---

### Step 5 — Reset Cases to Retest (Playwright UI)

**Only applies to:** `Long - Calendar`, `Hoang - Calendar`, `Thanh Hai`, `Quoc Bao`, `Van Loi`.

Skip this step for `Regression test for OOP features` and `Regression test for Renseikai full sandbox`.

For the 5 member runs, remove the Untested filter and set all remaining (Skipped) cases to Retest.

**Why Playwright?** The Qase API does NOT support a `"retest"` status — the valid statuses for `create_results_bulk` are: `passed`, `failed`, `blocked`, `skipped`, `invalid`. The "Retest" action is only available through the Qase web interface.

For each target run:

1. Navigate to `https://app.qase.io/run/{project_code}/dashboard/{run_id}`.
2. If a Status filter is active ("Status:Untested Remove filter" button visible), click the **"Remove filter"** button first:
   ```javascript
   await page.getByRole("button", { name: "Remove filter", exact: true }).click();
   ```
3. Wait for cases to load, then click the **"Select all run cases"** checkbox.
4. Click the **"Retest"** button (becomes enabled after selecting cases).
5. Verify that cases now show `Retest` status in the dashboard.

Use `mcp_playwright_browser_run_code` with this pattern:

```javascript
async (page) => {
  await page.goto("https://app.qase.io/run/PX/dashboard/<RUN_ID>");
  await page.waitForTimeout(3000);
  // Remove cached status filter if present
  await page.getByRole("button", { name: "Remove filter", exact: true }).click();
  await page.waitForTimeout(1500);
  // Select all and Retest
  await page.locator("label").filter({ hasText: "Select all" }).click();
  await page.waitForTimeout(1500);
  await page.getByRole("button", { name: "Retest", exact: true }).click();
  await page.waitForTimeout(2000);
  return "Done";
};
```

**Important:** The Qase UI caches the Untested filter from Step 5. Always remove the filter before selecting cases, or the "Retest" button will remain disabled (no cases visible to select).

---

### Step 6 — Report Summary

After all runs are created and statuses updated, output a summary:

```
## Test Run Creation Summary

**Project:** <project code>
**Plan:** <plan title> (ID: <plan_id>)
**Date:** <today's date>

### Runs Created
| # | Run Title | Run ID | Cases | Status Updated |
|---|-----------|--------|-------|----------------|
| 1 | Long - Calendar | 2301 | 45 | Skipped → Retest |
| 2 | Hoang - Calendar | 2302 | 45 | Skipped → Retest |
| 3 | Thanh Hai | 2303 | 45 | Skipped → Retest |
| 4 | Quoc Bao | 2304 | 45 | Skipped → Retest |
| 5 | Van Loi | 2305 | 45 | Skipped → Retest |
| 6 | Regression test for OOP features | 2306 | 109 | Skipped → Retest |
| 7 | Regression test for Renseikai full sandbox | 2307 | 367 | Skipped → Retest |

### Totals
- Runs created: X
- Runs failed: X
- Cases per run: X
- Runs with status updates: X
```

---

## Default Run Definitions

When the user provides a plan URL without specifying run titles, use this default configuration:

| Run Title                                    | Cases              | Steps 4–5 Applied | Status Update               |
| -------------------------------------------- | ------------------ | ----------------- | --------------------------- |
| `Long - Calendar`                            | From reference run | ✓ Yes             | Untested → Skipped → Retest |
| `Hoang - Calendar`                           | From reference run | ✓ Yes             | Untested → Skipped → Retest |
| `Thanh Hai`                                  | From reference run | ✓ Yes             | Untested → Skipped → Retest |
| `Quoc Bao`                                   | From reference run | ✓ Yes             | Untested → Skipped → Retest |
| `Van Loi`                                    | From reference run | ✓ Yes             | Untested → Skipped → Retest |
| `Regression test for OOP features`           | From reference run | ✗ Skip            | (no bulk status update)     |
| `Regression test for Renseikai full sandbox` | From reference run | ✗ Skip            | (no bulk status update)     |

"From reference run" means: look up the most recent existing run with the same title and `plan_id` to get the case list. If no reference run exists, use all cases from the plan.

All runs are created with `plan_id` (linked to the plan), then trimmed to the correct case subset using the Skip → Filter → Remove workflow (Steps 4–6).

The user can override this by providing their own list of run titles and status update rules.

---

## Quality Checks

Before finishing, verify:

- [ ] All runs are created and linked to the correct plan (plan_id is set, runs appear under plan's "Test runs" tab)
- [ ] Each run contains the expected number of test cases (unwanted cases were removed)
- [ ] Status updates were applied correctly (Retest for all runs)
- [ ] No duplicate runs were created (check by title before creating)
- [ ] The summary accurately reflects what was created

---

## Key Learnings & Constraints

- **`plan_id` can only be set at run creation time.** The Qase API `PATCH /v1/run/{code}/{id}` does NOT support updating `plan_id` after creation.
- **`plan_id` + `cases`** creates a run with exactly the specified cases (must be a subset already in the plan). This is the correct approach.
- **The "Retest" status is UI-only.** The API only supports: `passed`, `failed`, `blocked`, `skipped`, `invalid`.
- **The Qase UI caches the Status filter** across page navigations. Always check for and remove active filters before selecting cases.
