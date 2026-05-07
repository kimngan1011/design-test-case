# Automation Execution Rules

Rules for executing JSON test cases via Playwright MCP tools.

---

## Action → Playwright Mapping

| `action` | Playwright tool | Snapshot rule |
|----------|-----------------|---------------|
| `click` | `browser_snapshot` (get ref) → `browser_click` | Always before (need ref) |
| `fill` | `browser_fill_form` with ref + value | Only if `expected` != null |
| `type` | `browser_type` | Only if `expected` != null |
| `select` | `browser_select_option` | Only if `expected` != null |
| `navigate` | `browser_navigate` with target as URL | After navigation |
| `press_key` | `browser_press_key` with data as key | Only if `expected` != null |
| `verify` | `browser_snapshot` + text match | Always (this IS verification) |
| `wait` | `browser_wait_for` with target | No |
| `login` | `browser_run_code` batch (fill + click) | After login |
| `scroll` | `browser_evaluate` (`window.scrollBy()`) | No |

---

## Token Optimization Rules

### 1. Snapshot only when needed
- Skip `browser_snapshot` if step has `expected: null` AND next step doesn't need ref
- Exception: `click` always needs snapshot to find element ref
- Reuse refs from previous snapshot if still on same page

### 2. Batch consecutive fills
If 3+ consecutive steps are `fill`/`select`, use ONE `browser_run_code`:
```js
async (page) => {
  await page.fill('[selector-for-field1]', 'value1');
  await page.fill('[selector-for-field2]', 'value2');
  await page.selectOption('[selector-for-field3]', 'value3');
  return 'Filled 3 fields';
}
```
Adapt selectors from the most recent snapshot.

### 3. Batch login
Use ONE `browser_run_code` for login instead of 3-4 separate calls:
```js
async (page) => {
  await page.fill('[selector-email]', '<email>');
  await page.fill('[selector-password]', '<password>');
  await page.click('[selector-submit]');
  await page.waitForNavigation();
  return 'Login complete';
}
```

### 4. Between cases
- Same role + same start_url → skip re-login and re-navigation
- Same role, different start_url → just navigate
- Different role → re-login

---

## Error Handling

| Failure | Behavior |
|---------|----------|
| Element not found | `browser_wait_for` 3s → re-snapshot → retry once → FAIL step, stop case |
| Navigation timeout | Wait 15s → FAIL step |
| Login failed | Check snapshot for error → report, skip all cases for this role |
| Unexpected popup/dialog | Snapshot to identify → dismiss → retry step |
| Action throws error | Record error → FAIL step, stop case |
| **Any error during execution** | **Pause immediately → report error details to user → ask user to confirm before closing browser or continuing. Do NOT auto-close session.** |

---

## Timeouts

- Per step: 30 seconds
- Per case: 3 minutes
- Total run: 30 minutes

---

## Guardrails

- **No production:** Refuse if env URL lacks `sandbox`/`staging`/`rehearsal`/`prep`/`dev`
- **Always close browser:** Even on crash or timeout
- **No destructive actions outside steps:** Only execute actions from JSON
- **No screenshots:** Use `browser_snapshot` (accessibility tree) exclusively

---

## Verification Logic

When `expected` is not null:
1. Call `browser_snapshot`
2. Search accessibility tree text for expected content
3. PASS if found, FAIL if not found

---

## Report Format

```
## Test Execution Report

**Source:** <json file path>
**Env:** <env name> (<URL>)
**Executed by:** Claude (Playwright automation)
**Date:** <today>

### Summary
| Total | Passed | Failed | Skipped |
|-------|--------|--------|---------|
| N     | X      | Y      | Z       |

### Results
| # | ID | Title | Steps | Status | Failed At |
|---|-----|-------|-------|--------|-----------|
| 1 | TC-001 | ... | 4/4 | PASSED | — |
| 2 | TC-002 | ... | 3/6 | FAILED | Step 4 |

### Failed Cases Detail
#### <ID>: <title>
- **Failed at step N:** <action> → "<target>"
- **Expected:** "<expected text>"
- **Actual:** "<what was observed>"

### Console Errors (if any)
<From browser_console_messages for failed cases, or "None">
```
