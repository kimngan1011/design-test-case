---
description: >
  **WORKFLOW SKILL** — Review automation test results from a Qase test run.
  USE FOR: reviewing an automated Playwright/automated test run in Qase; reading step-results.json
  from each test case execution; comparing automation results against the original test case
  (preconditions, actions, expected results); identifying failures, flakiness, or mismatches;
  and exporting a structured review report.
  INPUT: Qase test run URL or run ID + project code (e.g. `https://app.qase.io/run/PX/dashboard/2187`).
  OUTPUT: a Markdown review report saved to `output/review-automation-tests/`.
  DO NOT USE FOR: generating test cases, importing test cases, or analyzing Jira requirements.
---

# Skill: Review Automation Test Run

You are a senior QA engineer reviewing automated test execution results from Qase.
Your job is to verify that each automated test case ran correctly — that its actual step-by-step execution matches the defined preconditions, actions, and expected results.

---

## Input

- **Qase run URL or run ID** — e.g. `https://app.qase.io/run/PX/dashboard/2187` or just `PX run 2187`
- **Project code** — extracted from the URL (e.g. `PX`)

---

## Workflow

### Step 1 — Fetch Run Summary

Use `mcp_qase_get_run` with the project code and run ID:

- Get: title, status, start/end time, total/passed/failed/skipped stats
- Note any cases with **failed**, **invalid**, or **blocked** status — these are priority review targets

```
mcp_qase_get_run(code=<PROJECT>, id=<RUN_ID>)
```

### Step 2 — Fetch All Execution Results

Use `mcp_qase_list_results` to get all result entries for the run:

- Each result entry has: `case_id`, `status`, `steps[]`, `time_spent_ms`, `end_time`, `attachments[]`
- Extract the `step-results.json` URL from `attachments` (mime: `application/json`, filename: `step-results.json`)

```
mcp_qase_list_results(code=<PROJECT>, run=<RUN_ID>, limit=100)
```

> **Important:** There may be **multiple result entries per case** (retries). For each unique `case_id`, use only the **latest result entry** (highest `end_time`) as the final result. Track all prior statuses as retry history.

Build a result map:

```
case_id → {
  final_status,
  retry_history: [status, ...],
  time_spent_ms,
  step_results_md_url,
  steps: [{position, status}]
}
```

### Step 3 — Read step-results.json for Each Test Case

For each test case in the result map, fetch the `step-results.json` attachment URL using `fetch_webpage`.

The file contains for each step:

- Step name (e.g. `## Verify Lesson Grid UI`)
- Status: PASSED / FAILED
- Duration (ms)
- Runtime logs with `[INFO]`, `[PASS]`, `[FAIL]`, `[ERROR]` entries

**New JSON format — structured step entries:**

Step entries in `step-results.json` now include structured prefix labels in their JSON content. Each step log block may contain one or more of the following prefixed lines:

```
PRECONDITION: <text describing the setup state or data used>
ACTION:       <text describing what the automation did>
EXPECTED:     <text describing what was verified>
```

These prefixes map directly to fields in the original Qase test case definition:

| Step-results prefix | Qase test case field         |
| ------------------- | ---------------------------- |
| `PRECONDITION:`     | `preconditions` (case level) |
| `ACTION:`           | `steps[N].action`            |
| `EXPECTED:`         | `steps[N].expected_result`   |

When reading step-results.json, extract all `PRECONDITION:`, `ACTION:`, and `EXPECTED:` lines per step and store them for the mapping comparison in Step 5.

**Unmapped entries:** If a step log block contains `ACTION:` or `EXPECTED:` lines that have **no corresponding Qase step** (by position or content), it must be flagged as an unmapped automation action. See Step 5 and the Quality Checks section.

**Prioritize reading failures first:**

- Start with cases where `final_status` = `failed` or `invalid`
- Then read passed cases that had prior retries (flaky candidates)
- Optionally read clean-pass cases for completeness

### Step 4 — Fetch Original Test Case Details

For each unique `case_id`, fetch the original test case from Qase using `mcp_qase_get_case`:

```
mcp_qase_get_case(code=<PROJECT>, id=<CASE_ID>)
```

Extract from the general tab:

- `title` — test case name
- `preconditions` — setup conditions required
- `steps[]` — each step has: `action`, `expected_result`, `position`
- `severity`, `priority`, `automation` status
- `suite_id` — which suite it belongs to

Build a definition map for each case:

```
case_id → {
  preconditions: <string>,
  steps: [
    { position: N, action: <string>, expected_result: <string> },
    ...
  ]
}
```

This map is used in Step 5 to align each `PRECONDITION:` / `ACTION:` / `EXPECTED:` entry in step-results.json against the defined case fields.

### Step 5 — Compare Execution vs. Definition (per Suite → per Test Case)

**Organize all test cases by suite before comparing.** Group cases using the `suite_id` from the Qase case definition. For each suite, iterate through every test case in the suite one by one.

#### Mapping PRECONDITION / ACTION / EXPECTED to Original Test Case Fields

For each test case, align the structured entries extracted from step-results.json (Step 3) against the definition map built in Step 4:

| Step-results entry  | Maps to                         | How to verify                                                                                                 |
| ------------------- | ------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `PRECONDITION: ...` | `case.preconditions`            | The automation's setup state/data must match every condition stated in the Qase `preconditions` field         |
| `ACTION: ...`       | `case.steps[N].action`          | Match each `ACTION:` line to the corresponding step position in Qase; order and content must align            |
| `EXPECTED: ...`     | `case.steps[N].expected_result` | Each `EXPECTED:` line must cover every sub-condition listed in the corresponding Qase `expected_result` field |

**Unmapped automation entries (highlight required):**

- An `ACTION:` or `EXPECTED:` entry in step-results.json that has **no corresponding Qase step** (by position or by content match) is an **unmapped automation action**.
- An `ACTION:` or `EXPECTED:` entry where the position exists in Qase but the content does **not match** the defined action/expected_result is a **mismatched mapping**.
- All unmapped and mismatched entries must be **highlighted** in the review report (see output format below).

For each individual test case, perform the following checklist and record a **Matching** or **Not Matching** verdict:

| Check                | What to verify                                                                                         |
| -------------------- | ------------------------------------------------------------------------------------------------------ |
| **Preconditions**    | `PRECONDITION:` entries in step-results match every condition in `case.preconditions`                  |
| **Step coverage**    | Number of `ACTION:` entries matches number of defined steps; every defined step has a mapped entry     |
| **Step actions**     | Each `ACTION:` entry corresponds (by position and content) to `steps[N].action` in the Qase definition |
| **Expected results** | Each `EXPECTED:` entry covers every sub-condition in `steps[N].expected_result`                        |
| **Unmapped entries** | Any `ACTION:`/`EXPECTED:` entries without a matching Qase step are flagged as unmapped                 |
| **Failures**         | For failed steps, extract the specific `[FAIL]` or `[ERROR]` log lines as evidence                     |
| **Flakiness**        | Cases with retries before passing are flagged as potentially flaky                                     |

**Verdict rules — applied per test case:**

- **Matching** — every defined step action has a corresponding automation step, every expected result sub-condition is explicitly verified in the logs, no extra undocumented actions, precondition data matches definition
- **Not Matching** — one or more of the following applies:
  - Executed steps don't match defined steps (`DEFINITION_MISMATCH`)
  - A defined expected result sub-condition has no matching log line (`EXPECTED_RESULT_FAIL`)
  - Precondition data is wrong or missing (`PRECONDITION_FAIL`)
  - Automation performs extra undocumented actions (`EXTRA_ACTION`)
  - Test passed after retries with no code change (`FLAKY`)
  - Test could not run due to environment/infra issue (`INVALID`)
  - Vague scope phrases in expected result prevent full verification (`SCOPE_AMBIGUITY`)
  - Definition has quality issues (contradictory data, image-only result, copy-paste error) (`DEFINITION_QUALITY`)

After checking all cases in a suite, move to the next suite. Do not mix cases across suites in the per-case output table.

---

### Mandatory Deep-Check Rules for Step 5

When comparing each Qase step against its execution, apply ALL of the following checks — do not skip any even if the step is marked ✅:

#### 1. Input Values vs. Actual Values in Precondition Snapshot

- Read the Precondition Data Snapshot in `step-results.json` (JSON block after `[INFO] Precondition :`)
- Compare **each field individually** against what Qase step 1 action specifies
- Flag if automation uses a different value from what is defined (e.g. wrong `lessonType`, wrong `teachingMethod`, wrong `skipCloseDate` setting)
- **Critical pattern**: If automation sets `expectedValue` = `actualValue` = `WRONG_VALUE`, the step passes green but the wrong thing is being tested — always trace back to the definition

#### 2. Expected Results — Check EVERY Sub-Condition

- Each Qase `expected_result` may contain **multiple sub-conditions** as bullet points
- For each sub-condition, trace a corresponding `[CHECK]`, `[PASS]`, or `[INFO]` log line in the step-results
- If a sub-condition has no matching log line, it is **NOT verified** — flag it as `⚠️ Partial`
- **Critical pattern — negative assertions**: sub-conditions phrased as "User does NOT see X" or "X is absent" require an explicit absence assertion in the log. A test that only checks presence of expected items does NOT cover a "does not see" expected result.

#### 3. Precondition vs. Execution Start State

- Read the Qase `preconditions` field (e.g. "User has created a published report with a student")
- Compare against what the automation does in its first step
- If the automation creates or modifies precondition state **as part of a test step** (rather than a setup fixture), flag as `⚠️ Precondition setup embedded in test step`
- Also flag if the Qase precondition specifies attributes (e.g. "with a student") that do not exist before step 1 execution

#### 4. Extra Automation Actions Not in Qase Definition

- For each automation step, check if it does MORE than the Qase action describes
- Common patterns: adding students, creating data, navigating to extra screens, running extra verification loops
- Flag each undocumented extra action as `➕ Extra action (not in definition)`
- Also flag entire automation steps that have no matching Qase step (e.g. `Verify Lesson Schedule UI List`)

#### 5. Step Action vs. Automation Step Name

- The automation step name (e.g. `Verify Lesson Grid UI`) should correspond to the Qase step action
- If step names are mismatched or vague (e.g. "Verify BackOffice Details" covers 4 different expected results), flag as traceability gap

#### 6. Shallow Verification — Check What Is NOT Logged

- When a Qase expected result says "User sees all fields", read the automation log and enumerate what fields were NOT checked
- A `[PASS] Pass SUCCESS: <step name>` log line without field-level checks is a shallow pass — flag with a list of missing field checks
- For BO/backend verification steps especially: check if lesson code, lesson type (with correct value), report status, and read-only attributes are ALL verified

#### 7. Lesson Type Verification (Critical for Manabie)

- The Manabie system has multiple similar lesson types: `通常特訓`, `通常特訓（時間変更）`, etc.
- Always extract the `lessonType` from the Precondition Data Snapshot and compare to Qase step 1 input
- Always extract the `[PASS] Pass LessonType: [actual] vs [expected]` log lines and compare both values to the Qase step definition's expected result
- **A lesson type check that shows `[actual] = [expected] = WRONG_TYPE` is a false green — both sides must match the Qase definition**

#### 8. Definition Quality Issues to Note

- Step action contains contradictory data for the test scenario (e.g. step says "Check Skip Closed Date" but test is a "No Skip" case)
- Expected result defined only as an image (no textual assertion to verify against)
- Multiple test cases sharing the same step hash but describing different scenarios (copy-paste error)
- Note these as `⚠️ Definition quality issue — requires correction in Qase`

#### 9. Defined Steps vs. Executed Steps — Beyond Count (GAP-2 pattern)

- Do **not** rely solely on the count of defined steps vs. executed steps — a count match can hide a missing step if automation also runs an undocumented step of its own
- For each defined Qase step (by position and action), confirm there is a **corresponding** automation step in `step-results.json`
- Common miss: a high-numbered step (e.g. "Student login Mobile", "Verify on external system") is entirely absent from automation while automation runs an extra undocumented step that keeps the count equal
- If any defined step has no executed counterpart, flag as `MISSING_STEP` — this is more severe than a count mismatch because it means an entire expected result is permanently unverified
- When a step is missing: note whether it implies a different platform (mobile, BO, external API) that the automation framework doesn't reach

#### 10. Silent Skip Log Pattern (GAP-3 pattern)

- Scan **every** step log for skip-like messages before accepting a PASSED status:
  - `[INFO] I temporarily skipped the field`
  - `[WARN] skipping`
  - `cannot find this field`
  - `skipped due to`
  - Any variant of "skip", "cannot locate", "not found on form" followed by continuing execution
- A step that logs a skip but still returns `PASSED` is **NOT** a verified pass — the skipped assertion is a hidden missing check
- Flag as `⚠️ Silent skip — <field/action> not verified` and state what was skipped
- Do not accept an automation-level `[INFO]` skip as equivalent to a Qase definition change — the definition may still require that field, meaning the definition and automation are out of sync
- This pattern appears especially in "Edit all fields" steps where individual form fields are silently bypassed

#### 11. Recurring Lesson Chain — Verify ALL Affected Lessons Explicitly (GAP-7 pattern)

- When a Qase step involves a **chain-scope selection** (`Only this Lesson` / `This and the following lessons` / `All lessons`), the automation must explicitly navigate to and verify **each individual lesson** affected by the scope
- **"Only this Lesson" scope**: Automation must open EVERY other lesson in the chain (not just the selected one) and confirm the change is ABSENT there — a single success message is not sufficient
- **"This and following lessons" scope**: Automation must open EVERY lesson from the selected lesson to the last lesson in the chain and confirm the change is PRESENT in each — checking only the first or second lesson is not sufficient
- Tracing the chain: read the Qase precondition to determine how many lessons are in the chain (e.g. "4-lesson recurring, Week 1 / 3 / 5 / 10") and enumerate each lesson that must be verified
- Missing lesson checks are a `SCOPE_AMBIGUITY` + `EXPECTED_RESULT_FAIL` combined: the definition is vague (no explicit lesson numbers) AND the automation exploits that vagueness by checking only a subset
- **Required log evidence for "Only this" scope**: one `[CHECK] absent` log per non-selected lesson
- **Required log evidence for "This and following" scope**: one `[CHECK] present` log per following lesson (lesson N+1 through last)
- Note: if the Qase definition itself uses vague language ("other lessons", "the following lesson" — singular), flag the definition as `DEFINITION_QUALITY` needing explicit lesson-number scope

### Step 6 — Generate Review Report

Save the report to `output/review-automation-tests/<project>-run-<run_id>-review.md`.

Use this structure:

```markdown
# Automation Test Run Review

**Project:** <PROJECT>
**Run ID:** <RUN_ID>
**Run Title:** <title>
**Run Date:** <start_time>
**Reviewed By:** GitHub Copilot
**Review Date:** <today>

---

## Summary

| Metric                 | Value |
| ---------------------- | ----- |
| Total Cases            | N     |
| Passed (clean)         | N     |
| Passed (after retries) | N     |
| Failed                 | N     |
| Invalid/Blocked        | N     |
| Matching               | N     |
| Not Matching           | N     |

---

## Per-Suite Verification Table

One row per test case, organized by suite. Describes every check performed against the test run and original definition.

| Suite        | Test Case        | Checks Performed                                                                                                        | Verdict         |
| ------------ | ---------------- | ----------------------------------------------------------------------------------------------------------------------- | --------------- |
| <Suite Name> | PX-<id>: <title> | Preconditions ✅ · Step coverage ✅ · Step actions ✅ · Expected results ✅ · Unmapped entries ✅ · No extra actions ✅ | ✅ Matching     |
| <Suite Name> | PX-<id>: <title> | Preconditions ✅ · Step coverage ✅ · Step actions ✅ · Expected results ⚠️ · Unmapped entries ⚠️ · No extra actions ✅ | ❌ Not Matching |

> **Checks Performed** column must enumerate every individual check done for that case (use ✅, ⚠️, or ❌ per check).

> **Unmapped entries** — if any `ACTION:` or `EXPECTED:` entry in step-results.json has no corresponding Qase step, mark the "Unmapped entries" check as ⚠️ and include a detail block under "Not Matching Cases — Detail" listing the unmapped entries.

---

## ⚠️ Unmapped Automation Test Cases

List every test case (or step within a test case) where an `ACTION:` or `EXPECTED:` entry in step-results.json could **not be mapped** to any step in the original Qase definition. Group by suite.

| Suite        | Case ID | Step Position | Unmapped Entry Type | Content (truncated)         | Impact                                          |
| ------------ | ------- | ------------- | ------------------- | --------------------------- | ----------------------------------------------- |
| <Suite Name> | PX-<id> | Step N        | ACTION / EXPECTED   | `<first 80 chars of entry>` | No defined step to trace this execution back to |

> A test case row appears here only if it has at least one unmapped `ACTION:` or `EXPECTED:` entry. Cases with full mapping are not listed in this table.

---

## Not Matching Cases — Detail

For each ❌ Not Matching row in the table above, provide a full detail block:

### <Suite Name> — PX-<id>: <title>

**Verdict:** Not Matching  
**Mismatch type(s):** DEFINITION_MISMATCH | EXPECTED_RESULT_FAIL | PRECONDITION_FAIL | EXTRA_ACTION | FLAKY | INVALID | SCOPE_AMBIGUITY | DEFINITION_QUALITY

#### What to Check in the Test Run

- Step N: <exactly which log line or log section shows the problem>
- Paste the specific `[FAIL]`, `[ERROR]`, or missing `[CHECK]` evidence:
```

[FAIL] <log line>
[ERROR] <log line>

```
- If the issue is a missing check: state which sub-condition of the expected result has no matching log line
- If the issue is a false green: show the `expectedValue` vs `actualValue` in the Precondition Snapshot and explain why they are wrong

#### How to Fix the Test Case Definition

- State the specific Qase field that needs updating: `preconditions`, `step N action`, or `step N expected_result`
- Provide the current (problematic) wording:
> **Current:** "User does not see the teacher is added to other lessons in the chain"
- Provide the corrected wording:
> **Should be:** "User does not see the teacher in lessons 1, 3, and 4 (only the selected lesson 2 is affected)"
- If the fix requires changes to a **shared step**, note this explicitly, as the fix will propagate to all cases using that step
- If the fix requires a new step or split of an existing step, describe the new step structure

---

## Cases with Issues (Technical)

### ❌ Failed Cases

For each failed case:

#### PX-<id>: <title>

- **Suite:** <suite name>
- **Final Status:** FAILED
- **Retries:** N
- **Step that failed:** <step name>
- **Failure evidence:**
```

[FAIL] <log line>
[ERROR] <log line>

```
- **Expected result (from definition):** <expected_result text>
- **Assessment:** EXPECTED_RESULT_FAIL | PRECONDITION_FAIL | DEFINITION_MISMATCH

---

### ⚠️ Flaky Cases (passed after retries)

For each flaky case:

#### PX-<id>: <title>
- **Suite:** <suite name>
- **Retry history:** failed → failed → passed
- **Step that was unstable:** <step name>
- **Assessment:** FLAKY — recommend investigation

---

### ✅ Clean Pass Cases

List as a table:

| Case ID | Title | Steps | Duration |
|---------|-------|-------|----------|
| PX-<id> | <title> | N | Xs |

---

## Recommendations

- List specific test cases to re-run or investigate
- Note environment issues if patterns suggest infra instability
- Recommend test case definition updates if mismatches found
- For shared-step fixes: list the shared step hash and all affected case IDs
```

### Step 7 — Update Automation Status (Matching → Automated, Not Matching → Manual)

After completing Step 5, update the **Automation Status** in Qase for every analyzed test case according to its verdict:

| Verdict         | Current Status | Update To | Qase API value   |
| --------------- | -------------- | --------- | ---------------- |
| ✅ Matching     | In Review      | Automated | `automation = 2` |
| ❌ Not Matching | In Review      | Manual    | `automation = 0` |

Only update cases whose current automation status is **In Review** (`automation = 3`). Skip cases already set to Automated or Manual.

#### Sub-step 7a — Request Approval Before Updating

Before making any changes, **present a summary table** of all proposed updates and **ask the user for confirmation**:

```
I am about to update the automation status for the following cases. Please confirm (yes/no):

| Case ID  | Title    | Verdict      | Current Status | → New Status |
| -------- | -------- | ------------ | -------------- | ------------ |
| PX-<id>  | <title>  | ✅ Matching  | In Review      | Automated    |
| PX-<id>  | <title>  | ❌ Not Match | In Review      | Manual       |

Total: N cases to update (X → Automated, Y → Manual). Proceed?
```

Do **not** call any update API until the user explicitly approves.

#### Sub-step 7b — Auto-Update via API

Once approved, for each case in the approval table, call `mcp_qase_update_case`:

```
# Matching → Automated
mcp_qase_update_case(code=<PROJECT>, id=<CASE_ID>, automation=2)

# Not Matching → Manual
mcp_qase_update_case(code=<PROJECT>, id=<CASE_ID>, automation=0)
```

After each call, verify the update succeeded by re-fetching the case:

```
mcp_qase_get_case(code=<PROJECT>, id=<CASE_ID>)
→ confirm case.automation == 2 (Automated) or 0 (Manual)
```

If the API does not persist the change (returns success but field unchanged on re-fetch), fall back to the manual UI method:

1. Open `https://app.qase.io/case/<PROJECT>?id=<CASE_ID>`
2. Click **Edit** → **Automation status** → set the correct value → **Save**
3. Note the case ID as "manually updated" in the report

#### Sub-step 7c — Record Updates in the Report

Append the following section to the review report:

```markdown
## Automation Status Updates

| Case ID | Title   | Verdict      | Updated To | Method   | Date       |
| ------- | ------- | ------------ | ---------- | -------- | ---------- |
| PX-<id> | <title> | ✅ Matching  | Automated  | API / UI | YYYY-MM-DD |
| PX-<id> | <title> | ❌ Not Match | Manual     | API / UI | YYYY-MM-DD |
```

---

## Output Naming

```
output/review-automation-tests/<project>-run-<run_id>-review.md
```

Example: `output/review-automation-tests/PX-run-2187-review.md`

---

## Quality Checks

Before finalizing the report, verify:

- [ ] All failed/invalid cases have failure evidence extracted from logs
- [ ] All flaky cases (retries) are identified and listed
- [ ] Each reported failure includes the specific `[FAIL]`/`[ERROR]` log line
- [ ] The summary counts match the individual case sections
- [ ] The report is saved to the correct output path

**Per-suite/per-case table:**

- [ ] Every test case in the run appears in the Per-Suite Verification Table — no case is omitted
- [ ] Cases are grouped by suite (not mixed across suites)
- [ ] The "Checks Performed" column enumerates every individual check done per case with a ✅/⚠️/❌ indicator, including the "Unmapped entries" check
- [ ] Every ❌ Not Matching row has a corresponding detail block in the "Not Matching Cases — Detail" section
- [ ] Each detail block contains both "What to Check in the Test Run" AND "How to Fix the Test Case Definition"
- [ ] For shared-step mismatches: the detail block notes the shared step hash and lists all other cases affected

**PRECONDITION / ACTION / EXPECTED mapping:**

- [ ] Every `PRECONDITION:` entry in step-results.json is compared against `case.preconditions` — mismatches are flagged
- [ ] Every `ACTION:` entry is matched to its corresponding `steps[N].action` by position — content drift is flagged
- [ ] Every `EXPECTED:` entry is matched to `steps[N].expected_result` — missing sub-conditions are flagged
- [ ] Any `ACTION:` or `EXPECTED:` entry with **no corresponding Qase step** is listed in the "⚠️ Unmapped Automation Test Cases" table in the report
- [ ] Any test case with at least one unmapped entry has its "Unmapped entries" check marked ⚠️ in the Per-Suite Verification Table and a corresponding detail block in "Not Matching Cases — Detail"

**For definition-vs-execution comparison, additionally verify:**

- [ ] Every Qase `expected_result` sub-condition is checked against a log line — not just the overall step status
- [ ] Negative assertions ("User does NOT see X") are explicitly verified with an absence check in the logs — not assumed from a count match
- [ ] The `lessonType` (or equivalent key fields) in the Precondition Data Snapshot matches the Qase step 1 definition value
- [ ] `[PASS] Pass LessonType: [actual] vs [expected]` — BOTH values match the Qase definition (not just each other)
- [ ] Automation extra actions within a step (not described in Qase) are flagged
- [ ] Precondition state required by Qase "preconditions" field is set up BEFORE step 1, not created during step 1
- [ ] Definition quality issues (contradictory input data, image-only expected results, copy-paste errors) are noted
- [ ] Every defined Qase step has a **corresponding executed step** — not just an equal total count (Rule 9 / GAP-2 pattern)
- [ ] Every step log is scanned for **silent skip messages** (`[INFO] skipped`, `cannot find field`, etc.) — a PASSED step with a skip log is flagged (Rule 10 / GAP-3 pattern)
- [ ] For recurring-lesson chain steps: **every individual lesson** in scope is explicitly verified — success message alone is insufficient (Rule 11 / GAP-7 pattern)
- [ ] A **pre-update approval table** was shown to the user before any API calls were made (Step 7a)
- [ ] Every **Matching** case with "In Review" status has been updated to **Automated** (`automation = 2`) via API (Step 7b)
- [ ] Every **Not Matching** case with "In Review" status has been updated to **Manual** (`automation = 0`) via API (Step 7b)
- [ ] Each update was verified by re-fetching the case after the API call (Step 7b)
- [ ] All updates (API or manual fallback) are recorded in the "Automation Status Updates" table in the report (Step 7c)

---

## Notes

- **PRECONDITION / ACTION / EXPECTED format**: step-results.json now contains structured prefix labels in step JSON blocks. Always extract all three prefix types before comparing against Qase definitions. If a prefix entry cannot be matched to any defined step, it is unmapped and must appear in the "\u26a0\ufe0f Unmapped Automation Test Cases" table.
- The Qase results API may return **293+ entries for 118 cases** — always deduplicate by `case_id` using latest `end_time`
- `step-results.json` files can be large (up to 52KB) — focus on log lines containing `[FAIL]`, `[ERROR]`, or `[PASS] Pass SUCCESS` for efficiency
- Cases with `status=invalid` often indicate environment/infra issues, not test logic failures — note this distinction in the report
- For passed cases with no retries, a full step-by-step comparison is optional unless specifically requested
- **False green pattern**: When automation sets `expectedValue = actualValue = WRONG_VALUE`, the step passes but tests the wrong behavior. Always trace expected values back to the Qase definition, not just confirm they match each other in the log.
- **Negative assertion gap pattern**: A "User does NOT see X" expected result requires an explicit `[CHECK] X is absent` log line. A count-based check (e.g. `total = 4`) only provides indirect coverage and does NOT satisfy a negative assertion requirement.
- **Lesson type in Manabie**: `通常特訓`, `通常特訓（時間変更）`, and other variants are distinct types. Always verify the exact type value in both precondition input and expected result assertions.
- **Precondition setup**: If step 1 of the automation does more than the Qase step 1 action (e.g. adds a student, creates data), compare against the Qase `preconditions` field — the extra work may be covering something the precondition claimed was already done.
- **Missing step pattern (Rule 9)**: A defined step that is entirely absent from automation is not caught by a count check if automation also runs an extra undocumented step. Always match by content/position, not by total count. Steps involving a different platform (mobile, external system) are often the ones silently dropped.
- **Silent skip pattern (Rule 10)**: `[INFO] I temporarily skipped the field "X"` is a red flag. Automation frameworks sometimes continue execution and report PASS after skipping a field they cannot locate. Always grep every step log for skip variants before accepting a clean PASSED status.
- **Recurring chain scope pattern (Rule 11)**: "Only this Lesson" requires absence-of-change verified on every other lesson in the chain. "This and following lessons" requires presence-of-change verified on every lesson from the selected one to the last. A single success message is never enough. Count lessons from the Qase precondition and verify each explicitly.
- **Automation status update (Step 7)**: Always request user approval before calling any update API. Use `mcp_qase_update_case` with `automation=2` (Automated) for Matching cases and `automation=0` (Manual) for Not Matching cases. Always re-fetch the case after each API call to confirm the field was persisted — if not, fall back to manual UI update and note it in the report.
