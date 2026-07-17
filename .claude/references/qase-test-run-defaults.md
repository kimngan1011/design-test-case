# Qase Test Run — Defaults, Retest Pattern, Summary

Reference for `create-test-runs`.

---

## Default run definitions

When the user provides a plan URL without specifying run titles, use this configuration:

| Run Title | Cases | Steps 4–5 Applied | Status Update |
|---|---|---|---|
| `PSG AverCM - Hoang - Aver lesson report` | From reference run | ✓ Yes | Untested → Skipped → Retest |
| `PSG PT teacher - Long - Aver lesson report` | From reference run | ✓ Yes | Untested → Skipped → Retest |
| `Quoc Bao` | From reference run | ✓ Yes | Untested → Skipped → Retest |
| `Van Loi` | From reference run | ✓ Yes | Untested → Skipped → Retest |
| `PSv1 Regression test for Renseikai full sandbox` | From reference run | ✗ Skip | (no bulk status update) |
| `PSv2 Regression test OOP features for EEA, Juku, Riso` | From reference run | ✗ Skip | (no bulk status update) |

"From reference run" = look up the most recent existing run with the same title and `plan_id`. If no reference run exists, fall back to all cases from the plan.

The user can override this by providing their own list of run titles and status update rules.

---

## Playwright "Retest" pattern (Step 5)

The Qase API does NOT support a `retest` status — valid API statuses are `passed`, `failed`, `blocked`, `skipped`, `invalid`. "Retest" is UI-only.

For each target run, use `mcp_playwright_browser_run_code`:

```javascript
async (page) => {
  await page.goto("https://app.qase.io/run/PX/dashboard/<RUN_ID>");
  await page.waitForTimeout(3000);
  // Remove the cached Untested filter (mandatory — else Retest button stays disabled)
  await page.getByRole("button", { name: "Remove filter", exact: true }).click();
  await page.waitForTimeout(1500);
  await page.locator("label").filter({ hasText: "Select all" }).click();
  await page.waitForTimeout(1500);
  await page.getByRole("button", { name: "Retest", exact: true }).click();
  await page.waitForTimeout(2000);
  return "Done";
};
```

The Qase UI caches the Status filter across navigations. Always remove the filter before selecting cases.

---

## Summary template (Step 6)

```markdown
## Test Run Creation Summary

**Project:** <project code>
**Plan:** <plan title> (ID: <plan_id>)
**Date:** <today's date>

### Runs Created
| # | Run Title | Run ID | Cases | Status Updated |
|---|-----------|--------|-------|----------------|
| 1 | Long - Calendar | 2301 | 45 | Skipped → Retest |
| 2 | Hoang - Calendar | 2302 | 45 | Skipped → Retest |

### Totals
- Runs created: X
- Runs failed: X
- Cases per run: X
- Runs with status updates: X
```

---

## Key constraints
- `plan_id` can only be set at run creation. The `PATCH /v1/run/{code}/{id}` endpoint does NOT support updating it.
- `plan_id` + `cases` creates a run with exactly the listed cases (must be a subset of the plan).
- "Retest" status is UI-only; API has no equivalent.
- Qase UI caches the Status filter across page navigations — always remove it before selecting.
