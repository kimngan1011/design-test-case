---
description: >
  **WORKFLOW SKILL** — Execute manual test cases on Salesforce using Playwright browser automation.
  USE FOR: running a specific Qase test case step-by-step on the SF sandbox; verifying preconditions
  (lesson schedule setup, academic calendar closed dates, field states); performing UI interactions
  (filling forms, clicking buttons, reading field values); comparing actual results with expected
  results; and saving a structured execution record to `output/execute-test-cases/`.
  INPUT: Qase case ID + Jira ticket + (optionally) test data hints.
  OUTPUT: a Markdown execution record saved to `output/execute-test-cases/<TICKET>/<CASE_ID>-run-<DATE>.md`.
  DO NOT USE FOR: generating test cases (use generate-test-cases skill), importing to Qase (use
  import-to-qase skill), or reviewing automation runs (use review-automation-tests skill).
---

# Skill: Execute Test Cases (Manual via Playwright)

You are a senior QA engineer executing manual test cases on the Manabie Salesforce sandbox.
Your job is to faithfully run each test case step, verify preconditions from the system (not by assumption),
capture actual results, and save a complete execution record.

---

## Input

- **Qase case ID** — e.g. `PX-17169`
- **Jira ticket** — e.g. `LT-90573` (used to organise output folder)
- **Test data hints** (optional) — e.g. "use LS with end date < 2026-05-01" or a specific LS number

---

## Workflow

### Step 1 — Fetch Test Case Definition from Qase

Use `mcp_qase_get_case` to retrieve the full test case:

```
mcp_qase_get_case(code=<PROJECT>, id=<CASE_ID>)
```

Extract:

- `title` — test case name
- `preconditions` — what must be true before the test starts
- `steps[]` — each step: `action`, `expected_result`
- `suite_id`, `priority`, `severity`

Hold this definition as the **ground truth** for the entire execution.

---

### Step 2 — Find Suitable Test Data

**Never assume test data is ready.** Actively look it up in SF.

#### 2a — Navigate to the relevant SF object list

Use Playwright to navigate and search for records matching the precondition criteria:

- Identify required field constraints from the preconditions (e.g. `Skip Closed Dates = True`, `End Date < X`)
- Browse the SF list view or use filters to find matching records
- Select the most appropriate record (prefer records with end dates **strictly less than** any closed date boundary, not equal)

#### 2b — Verify preconditions on the chosen record

For each precondition in the test case definition:

1. Open the record detail page
2. Use `mcp_playwright_browser_evaluate` to deep-read field values from the SF Lightning DOM (shadow DOM traversal required)
3. Confirm each condition is met — record `✅ Met` or `⚠️ Partial` or `❌ Not met`

**Do not proceed to Step 3 if any precondition is ❌ Not met.** Find a different record or note the blocker.

#### 2c — For tests involving Academic Calendar closed dates

The closed dates must be looked up from the system — never guess or assume:

1. From the chosen LS record, note its **Location** and **Academic Year**
2. Navigate to `Academic Calendars` list view, filter/find the calendar matching `<Year>_<Location>`
3. Click into the calendar → open the **Closed Date** tab
4. Extract ALL closed dates and their day-of-week
5. Identify which closed dates fall **on the same day-of-week as the LS recurrence** and **within the planned extension range**
6. Confirm at least one such closed date exists — this is a critical precondition

---

### Step 3 — Execute Each Test Step

Work through every step in the Qase definition in order.

For each step:

1. **Perform the action** using Playwright tools:
   - `mcp_playwright_browser_navigate` — navigate to a URL
   - `mcp_playwright_browser_click` — click a button or link by ref
   - `mcp_playwright_browser_evaluate` — read/set field values via deep shadow DOM
   - `mcp_playwright_browser_snapshot` — capture accessible tree (use sparingly — large output)
   - `mcp_playwright_browser_take_screenshot` — visual confirmation when needed

2. **Capture the actual result**:
   - Read field states (checked/unchecked, disabled/enabled, current value)
   - Read counts (e.g. lesson count before and after save)
   - Read date lists (all records in a related list, sorted by date)

3. **Compare with expected result** from the Qase definition

4. **Record the outcome**: `✅ PASS`, `⚠️ PARTIAL`, or `❌ FAIL` with detail

#### Shadow DOM pattern (SF Lightning)

SF Lightning uses Web Components with Shadow DOM. Standard `querySelector` only works at the top level. Always use deep traversal:

```js
function deepFind(root, id) {
  const el = root.querySelector(`#${id}`);
  if (el) return el;
  for (const child of Array.from(root.querySelectorAll("*"))) {
    if (child.shadowRoot) {
      const found = deepFind(child.shadowRoot, id);
      if (found) return found;
    }
  }
  return null;
}
```

For setting input values (React/LWC controlled components):

```js
const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
nativeInputValueSetter.call(inputEl, "new value");
inputEl.dispatchEvent(new Event("input", { bubbles: true }));
inputEl.dispatchEvent(new Event("change", { bubbles: true }));
inputEl.dispatchEvent(new Event("blur", { bubbles: true }));
```

#### Clicking buttons in Shadow DOM

If a button ref is stale (page re-rendered), use deep search:

```js
function deepFindButton(root, text) {
  const buttons = Array.from(root.querySelectorAll("button"));
  const found = buttons.find((b) => b.innerText?.trim() === text);
  if (found) return found;
  for (const child of Array.from(root.querySelectorAll("*"))) {
    if (child.shadowRoot) {
      const f = deepFindButton(child.shadowRoot, text);
      if (f) return f;
    }
  }
  return null;
}
deepFindButton(document, "Save")?.click();
```

---

### Step 4 — Post-Save Verification

After saving a form or triggering a system action, verify the outcome:

1. Wait for the page to reload (check `document.title` or URL change)
2. Read updated counts, field values, or related list entries
3. For lessons: extract all lesson dates from the related list using `[role="rowheader"]` with deep traversal
4. Cross-reference actual lesson dates with expected — especially for **closed date skipping**:
   - List all expected recurrence dates in the range
   - Mark which ones are closed dates (from Step 2c)
   - Confirm those dates are absent from the actual lesson list

---

### Step 5 — Save Execution Record

Save a structured Markdown file to:

```
output/execute-test-cases/<JIRA_TICKET>/<CASE_ID>-run-<YYYY-MM-DD>.md
```

The file must include:

```markdown
# Test Execution Record — <CASE_ID>

## Test Case Info

| Field        | Value                          |
| ------------ | ------------------------------ |
| Qase Case ID | ...                            |
| Title        | ...                            |
| Jira Ticket  | ...                            |
| Run Date     | ...                            |
| Executed By  | ...                            |
| Environment  | ...                            |
| Result       | ✅ PASS / ❌ FAIL / ⚠️ PARTIAL |

## Preconditions Verified

| #   | Precondition           | Status       |
| --- | ---------------------- | ------------ |
| 1   | <from Qase definition> | ✅ / ⚠️ / ❌ |

...

## Test Data

| Field               | Value                 |
| ------------------- | --------------------- |
| Lesson Schedule     | <number> — "<name>"   |
| LS SF Record URL    | `<url>`               |
| Original End Date   | <date>                |
| New End Date (used) | <date>                |
| Location            | <name>                |
| Academic Year       | <year>                |
| Academic Calendar   | <cal name> (ID: <id>) |

...

## Academic Calendar — Closed Dates (<cal name>)

| Date | Day | In Extension Range? |
| ---- | --- | ------------------- |

...

## Test Steps & Results

### Step 1 — <step title>

- **Action:** ...
- **Expected:** ...
- **Actual:** ...

...

## Extended / Result Data

<table of all relevant records, dates, states>

## Overall Result: ✅ PASS / ❌ FAIL

## Observation / Notes

> Any deviations, bugs, or interesting behaviors observed during execution.

## Re-run Checklist

### Finding suitable test data

- [ ] <criteria for next LS selection>
- [ ] <academic calendar check>

### Before running

- [ ] <reset steps if any data was mutated>
```

---

## Quality Checks Before Closing

Before finishing, verify the record file contains:

- [ ] Every Qase precondition is addressed with a system-verified status
- [ ] Every Qase step has an Action / Expected / Actual recorded
- [ ] Closed dates were retrieved from the system (not assumed)
- [ ] The cross-reference table clearly shows which dates were skipped vs. created
- [ ] Any anomalies (day shifts, boundary behaviors, unexpected states) are noted
- [ ] Re-run checklist includes test data criteria specific enough for the next runner

---

## SF Navigation Reference

| Object               | List View URL                                                          |
| -------------------- | ---------------------------------------------------------------------- |
| Lesson Schedules     | `/lightning/o/MANAERP__Lesson_Schedule__c/list`                        |
| Academic Calendars   | `/lightning/o/MANAERP__Academic_Calendar__c/list?filterName=__Recent`  |
| Lessons (all for LS) | Dynamic related list URL found from the LS detail page "View All" link |

**LS detail page pattern:**

```
/lightning/r/MANAERP__Lesson_Schedule__c/<RECORD_ID>/view
```

**Extend Recurrence action URL pattern:**

```
/lightning/action/quick/MANAERP__Lesson_Schedule__c.MANAERP__Extend_Recurrence?context=RECORD_DETAIL&recordId=<RECORD_ID>
```

---

## SF Sandbox Credentials

Stored in `mcp.json` env vars and `/memories/sf-credentials.md`.
Do **not** hard-code credentials in output files.
